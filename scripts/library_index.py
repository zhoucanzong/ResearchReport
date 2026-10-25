#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""library_index.py —— Research 仓库图书馆化：只读索引与统计生成器。

把仓库里的 Markdown 文档按**图书馆条目**（entry）组织成可检索的索引，并产出
可供文档引用的统计数字。

## 核心口径（重要）

* **条目 = `report.md`**。一个 `<topic>-research/report.md` 就是一个条目；
  同一目录下的其它 `.md`（分册、`plan.md`、`notes/`、`raw-extracts/`、
  `sources-index.md`、`knowledge-graph.md` …）是该条目的**子文档**。
* **文档（document）= 除生成物以外的所有 `.md`**。`README.md`（根 / 子库 /
  `scripts/`）、`docs/*.md` 都是文档，但**不是条目**。
* **生成物**：`INDEX.md`、`index/*.md`、`index/stats.json` —— 由本脚本产出，
  **不计入**条目或文档统计（否则「跑一次脚本，数字就变一次」，无法复现）。
* **front-matter**：目前仅 2 份条目带 `date`。索引与统计必须在无元数据时优雅退化
  （显示 `—`）；「最近更新」可按配置回退到 `git log -1 --format=%cs`（最近提交日）。

## 设计原则

1. **只加不改**：本脚本对条目文件是纯只读的，绝不删除、移动、重命名或改写它们。
   写行为只有两处：把 `INDEX.md`、`index/*.md`、`index/stats.json` 写到
   ``--out-root``；在根 `README.md` 里幂等替换 ``<!-- SCRIPT:* START/END -->``
   标记之间的区块（``<!-- STATIC -->`` 文案与标记本身永不触碰）。
2. **可复现**：给定相同的仓库状态，输出逐字节一致（`--today` 用于钉住日期）。
3. **零第三方依赖**：有 PyYAML 就用它解析 front-matter，没有就退回内置逐行解析器。
4. **口径可审计**：`lines`（剔除 front-matter）与 `lines_raw`（文件原始行数）都产出。
5. **板块配置外置**：全部板块映射在 `scripts/panels.json`；脚本里不硬编码任何目录名。
   每个条目必须**恰好**归入一个面板（未归类 / 重复归类 / 代表条目缺 `report.md`
   都会在生成前失败并返回非零）。

用法::

    python3 scripts/library_index.py --repo-root . --dry-run
    python3 scripts/library_index.py --repo-root . --out-root . --write-stats --check-links
"""

from __future__ import annotations

import argparse
import datetime as _dt
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse

# --------------------------------------------------------------------------
# 常量 / 契约
# --------------------------------------------------------------------------

SCHEMA_VERSION = 2

#: front-matter 元数据键（缺 pyyaml 时逐行解析这套键）。
KNOWN_KEYS = (
    "title",
    "display_name",
    "type",
    "domain",
    "subject",
    "topic",
    "upstream",
    "date",
    "evidence",
    "status",
)

#: 分面索引文件名 -> 人类可读标题
FACET_TITLES = {
    "by-domain": "按领域（domain）",
    "by-subject": "按主题（subject）",
    "by-repo": "按来源仓库（upstream / 本地库根）",
    "by-topic": "研究专题与分析分册",
    "by-report": "按条目（report.md）平铺",
    "recent": "最近更新（按 date 降序）",
    "stale": "陈旧 / 待复核（status 或超期）",
}

GENERATED_NOTE = "本文件由 scripts/library_index.py 自动生成，请勿手改。"
DRY_RUN_NOTE = "（dry-run 产物，未写盘）"

#: 条目文件名口径：只有 report.md 算图书馆条目。
ENTRY_BASENAME = "report.md"

#: 生成物（相对 out-root）：既排除在扫描之外，也是「请勿手改」的文件。
GENERATED_TOP = "INDEX.md"
GENERATED_DIR = "index"
GENERATED_FILES = ("INDEX.md", "index/stats.json")
STATS_FILE = "index/stats.json"

UNFILED = "unfiled"
ROOT_GROUP = "repository-root"

NON_STALE_STATUSES = ("active", "current", "ok", "stable", "published", "completed")

#: 资料库（含 `report.md` 条目的顶层目录）。顺序即展示顺序。
#: 顶层板块目录在 ``main`` 中由 ``scripts/panels.json`` 推导，不在脚本中硬编码。
PANEL_TOPS: tuple[str, ...] = ()
#: 兼容旧字段名（历史文案里仍叫「库」）。
LIBRARIES: tuple[str, ...] = ()


def category_of(rel_path: str) -> str:
    """条目分类：按板块顶层目录（Models / LLM / … / OpenSource）。"""
    parts = [p for p in rel_path.replace(os.sep, "/").split("/") if p]
    return parts[0] if parts else "Other"


# --------------------------------------------------------------------------
# front-matter 解析
# --------------------------------------------------------------------------

def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _coerce(value: str):
    """把标量字符串转成最合适的类型（int / bool / str）。"""
    v = _strip_quotes(value.strip())
    if v.lower() in ("true", "yes"):
        return True
    if v.lower() in ("false", "no"):
        return False
    if re.fullmatch(r"-?\d+", v):
        try:
            return int(v)
        except ValueError:
            pass
    return v


def parse_front_matter_fallback(text: str) -> dict:
    """不依赖 PyYAML 的逐行 front-matter 解析器（扁平 key: value）。

    覆盖 :data:`KNOWN_KEYS`，容忍行内注释、内联列表 ``[a, b]``、折行列表与引号标量。
    只按行内**第一个** ``:`` 切分，``upstream: https://...`` 不会被截断。
    """
    fm: dict = {}
    pending_list_key = None

    for raw_line in text.split("\n"):
        if not raw_line.strip():
            continue
        stripped = raw_line.strip()

        if stripped.startswith("#"):
            continue

        if stripped.startswith("- ") and pending_list_key is not None:
            fm.setdefault(pending_list_key, [])
            if isinstance(fm[pending_list_key], list):
                fm[pending_list_key].append(_coerce(stripped[2:].strip()))
            continue

        if ":" not in raw_line:
            continue

        key, _, value = raw_line.partition(":")
        key = key.strip().lower().lstrip("\ufeff")
        value = value.strip()
        value = re.sub(r"\s+#.*$", "", value).strip()

        if key not in KNOWN_KEYS:
            pending_list_key = None
            continue

        if value == "":
            fm[key] = []
            pending_list_key = key
            continue

        pending_list_key = None
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            fm[key] = [_coerce(p) for p in inner.split(",") if p.strip()] if inner else []
        else:
            fm[key] = _coerce(value)

    return fm


def split_front_matter(text: str):
    """返回 (front-matter 行数, 去 front-matter 后的正文行数, front-matter 文本)。

    行数与 ``wc_l``（`wc -l`）同口径：**末尾换行不算额外一行**，因此
    「front-matter 行数 + 正文行数」= 该文件的行数；没有 front-matter 时
    正文行数 = 文件行数（曾经这里用 ``text.split("\\n")`` 的元素个数，文件末尾
    有换行时每份文件会多计 1 行，与 `wc -l` 不一致——已修正）。

    无闭合围栏时视为没有 front-matter（行数 0，正文即全文）。
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return 0, wc_l(text), ""

    fm_body = []
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            rest = "\n".join(lines[i + 1:])
            return i + 1, wc_l(rest), "\n".join(fm_body)
        fm_body.append(line)
    return 0, wc_l(text), ""


def parse_front_matter(text: str) -> dict:
    """解析文档开头的 YAML front-matter，返回扁平字典（无则 ``{}``）。"""
    fm_lines, _body_lines, block = split_front_matter(text)
    if fm_lines == 0:
        return {}

    try:
        import yaml  # type: ignore
    except ImportError:
        return parse_front_matter_fallback(block)

    try:
        loaded = yaml.safe_load(block)
    except Exception:
        return parse_front_matter_fallback(block)

    if not isinstance(loaded, dict):
        return parse_front_matter_fallback(block)

    fm = {}
    for key, value in loaded.items():
        key = str(key).strip().lower()
        if key not in KNOWN_KEYS:
            continue
        if isinstance(value, list):
            fm[key] = [_coerce(str(v)) for v in value]
        elif value is None:
            fm[key] = ""
        else:
            fm[key] = value
    return fm


# --------------------------------------------------------------------------
# 路径 / 值 工具
# --------------------------------------------------------------------------

def split_path(rel_path: str) -> tuple:
    """把仓库相对路径拆成 (一级目录, 二级目录, 更深目录元组, 文件名)。"""
    parts = [p for p in rel_path.replace(os.sep, "/").split("/") if p]
    filename = parts[-1] if parts else ""
    dirs = parts[:-1]
    top = dirs[0] if len(dirs) >= 1 else ""
    second = dirs[1] if len(dirs) >= 2 else ""
    deeper = tuple(dirs[2:]) if len(dirs) >= 3 else ()
    return top, second, deeper, filename


def entry_dir(rel_path: str) -> str:
    """条目所属目录（即它的「专题目录」）。"""
    parts = [p for p in rel_path.replace(os.sep, "/").split("/") if p]
    return "/".join(parts[:-1])


def to_list(value) -> list:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if value is None:
        return []
    text = str(value).strip()
    return [text] if text else []


def to_str(value) -> str:
    values = to_list(value)
    return values[0] if values else ""


def heading(text: str) -> str:
    """取正文第一个 ATX 标题作为 title 兜底。"""
    for line in text.split("\n"):
        m = re.match(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            return m.group(1).strip()
    return ""


def looks_like_date(value) -> bool:
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}", str(value).strip()))


def wc_l(text: str) -> int:
    """`wc -l` 口径：换行符个数；末尾无换行的非空尾行也计 1 行。

    与 `docs/statistics.md` 的统计方法一致（那里用 `cat | wc -l`）。
    """
    n = text.count("\n")
    if text and not text.endswith("\n"):
        n += 1
    return n


def is_generated(rel_path: str) -> bool:
    """是否为脚本自身的生成物（不计入条目 / 文档统计）。"""
    rel = rel_path.replace(os.sep, "/")
    if rel == GENERATED_TOP:
        return True
    return rel.startswith(GENERATED_DIR + "/")


# --------------------------------------------------------------------------
# 扫描（只读）
# --------------------------------------------------------------------------

#: 站点渲染层的顶层目录（MkDocs staging 与构建产物）——扫描时必须跳过，
#: 否则第二次运行会把 staging 镜像里的 .md 再数一遍（破坏可复现性）。
#: 注意 ``scripts/`` 不在这里：它的 README.md 历来计入文档统计，口径保持不变；
#: staging 器另有更宽的跳过清单（见 stage_site_docs）。
SITE_DOCS_DIR = "site-docs"
SITE_BUILD_DIR = "site"
SITE_SKIP_TOPS = frozenset({SITE_DOCS_DIR, SITE_BUILD_DIR})

#: 构建产物 / 车间目录：**任意层级**跳过，不编目。
#: 隐藏目录（`.*`，如 `.paper-cache/`、`.vla-tmp/`、`.rehearsal/`、`.preview/`）
#: 另有一律跳过的规则（见 ``_is_skipped_dir``）。这里是给「非隐藏」的构建目录兜底。
BUILD_SKIP_DIRS = frozenset({"site", "site-docs", "node_modules", "__pycache__"})


def _is_skipped_dir(name: str) -> bool:
    """临时 / 草稿 / 构建位置：**车间地面**，一律不编目。

    - 隐藏目录（点开头）：`.git/`、`.paper-cache/`、`.vla-tmp/`、`.rehearsal/`、`.preview/` 等；
    - 构建产物目录：`site/`、`site-docs/`、`node_modules/`、`__pycache__/`。

    刻意**不**改成 `git ls-files`（tracked-only）——未跟踪的真内容（新写的
    ``papers/foo.md``）仍须进索引，等会随条目一起提交。
    """
    return name.startswith(".") or name in BUILD_SKIP_DIRS or name in SITE_SKIP_TOPS


def _collect_md_under(rel_dir: str, root: str) -> list:
    """收集被跳过目录下的 `.md` 相对路径，仅用于 ``skipped:`` 可见性报告（只读）。"""
    out = []
    base = os.path.join(root, rel_dir) if rel_dir else root
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            if name.lower().endswith(".md"):
                out.append(os.path.relpath(os.path.join(dirpath, name), root)
                           .replace(os.sep, "/"))
    return sorted(out)


def iter_markdown(repo_root: str, include_generated: bool = False,
                  skipped_out: list = None):
    """只读遍历 ``**/*.md``，返回排序后的仓库相对路径。

    跳过隐藏目录（`.git`、`.vla-tmp/` 等）与构建产物目录（``site-docs/``、``site/``、
    ``node_modules/``、``__pycache__/``）；默认排除本脚本的生成物，
    保证「跑一次脚本数字不变」。

    ``skipped_out``（可选）：传入一个 list，会被填入**被跳过的 `.md` 相对路径**，
    供调用方打印 ``skipped: N (...)``——让跳过可审计，别静默失明。
    """
    root = os.path.abspath(repo_root)
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        kept = []
        for d in sorted(dirnames):
            if _is_skipped_dir(d):
                # The local reading cache can contain full-text exports and
                # large source snapshots. Exclude it without traversing or
                # listing its contents in the ordinary scan report.
                if skipped_out is not None and d != ".paper-cache":
                    skipped_out.extend(
                        _collect_md_under(
                            os.path.relpath(os.path.join(dirpath, d), root)
                            .replace(os.sep, "/"), root))
            else:
                kept.append(d)
        dirnames[:] = kept
        for name in sorted(filenames):
            if not name.lower().endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/")
            if include_generated or not is_generated(rel):
                found.append(rel)
    return sorted(found)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def build_doc(repo_root: str, rel_path: str, today: _dt.date) -> dict:
    """读取单个 `.md`，产出文档记录（纯读取，不写回）。"""
    abs_path = os.path.join(repo_root, rel_path)
    text = read_text(abs_path)
    fm_lines, body_lines, _block = split_front_matter(text)
    raw_lines = wc_l(text)
    fm = parse_front_matter(text)

    top, second, deeper, filename = split_path(rel_path)

    domain = to_str(fm.get("domain")) or top or UNFILED
    subject = to_str(fm.get("subject")) or second or UNFILED
    topic = to_str(fm.get("topic")) or ("/".join(deeper) if deeper else subject)

    date_raw = str(fm.get("date") or "") if not isinstance(fm.get("date"), list) else " ".join(to_list(fm.get("date")))
    date_iso = date_raw[:10] if looks_like_date(date_raw) else ""
    date_valid = bool(date_iso)
    age_days = None
    if date_valid:
        try:
            age_days = (today - _dt.date.fromisoformat(date_iso)).days
        except ValueError:
            date_valid = False
            date_iso = ""

    return {
        "path": rel_path,
        "filename": filename,
        "title": to_str(fm.get("title")) or heading(text) or filename,
        "display_name": to_str(fm.get("display_name")),
        "type": to_str(fm.get("type")),
        "domain": domain,
        "subject": subject,
        "topic": topic,
        "upstream": to_list(fm.get("upstream")),
        "date": date_raw,
        "date_iso": date_iso,
        "date_valid": date_valid,
        "age_days": age_days,
        "evidence": to_list(fm.get("evidence")),
        "status": to_str(fm.get("status")),
        "has_front_matter": bool(fm),
        "fm_keys": sorted(fm.keys()),
        "top": top,
        "category": category_of(rel_path),
        "is_entry": filename.lower() == ENTRY_BASENAME,
        "bytes": os.path.getsize(abs_path),
        "lines": body_lines,
        "lines_raw": raw_lines,
        "fm_lines": fm_lines,
        "is_generated": is_generated(rel_path),
    }


def scan(repo_root: str, today: _dt.date, include_generated: bool = False,
         skipped_out: list = None) -> list:
    return [build_doc(repo_root, rel, today)
            for rel in iter_markdown(repo_root, include_generated, skipped_out)]


def attach_children(docs: list) -> list:
    """给条目挂上**整棵子树**内的非条目 `.md` 作为子文档；游离文档单独标记。

    子文档 = 位于该条目所在 `<topic>-research/` 目录（含 `notes/`、`raw-extracts/`
    等子目录）内、且自身不是条目的全部 `.md`。这样 `INDEX.md` 能直达每个子报告，
    不存在「库里有、索引里找不到」的文档。

    `orphans` = 资料库内既不是条目、也不属于任何条目目录的 `.md`（子库 `README.md`、
    没有 `report.md` 的深读项目主文档等），它们会被 INDEX.md 单独列出以便可达。
    """
    entry_dirs = {entry_dir(d["path"]) for d in docs if d["is_entry"]}

    for doc in docs:
        doc["children"] = []
    for doc in docs:
        if doc["is_entry"]:
            continue
        parent = entry_dir(doc["path"])
        # 向上一层层找最近的条目目录
        while parent and parent not in entry_dirs:
            parent = parent.rsplit("/", 1)[0] if "/" in parent else ""
        doc["parent_dir"] = parent

    for doc in docs:
        if not doc["is_entry"]:
            continue
        root = entry_dir(doc["path"])
        doc["children"] = sorted(
            [d for d in docs
             if not d["is_entry"] and (d["path"] == root or d["path"].startswith(root + "/"))],
            key=lambda d: d["path"],
        )

    orphans = [d for d in docs
               if not d["is_entry"] and not d["is_generated"] and not d.get("parent_dir")]
    return docs, orphans


# --------------------------------------------------------------------------
# 统计
# --------------------------------------------------------------------------

def git_tracked(repo_root: str) -> list:
    """`git ls-files -z`（-z 避免非 ASCII 路径被八进制转义）。不可用时返回 []。"""
    try:
        out = subprocess.run(
            ["git", "-C", repo_root, "ls-files", "-z"],
            capture_output=True, text=True, check=True,
        ).stdout
    except Exception:
        return []
    return sorted(p for p in out.split("\0") if p)


def dir_metrics(repo_root: str, rel_dir: str) -> dict:
    """目录内文件数 / 字节 / `.md` 数（跳过隐藏目录与 .DS_Store）。"""
    base = os.path.join(repo_root, rel_dir)
    files, md_files, total_bytes = 0, 0, 0
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            if name == ".DS_Store":
                continue
            abs_path = os.path.join(dirpath, name)
            files += 1
            try:
                total_bytes += os.path.getsize(abs_path)
            except OSError:
                pass
            if name.lower().endswith(".md"):
                md_files += 1
    return {"files": files, "md": md_files, "bytes": total_bytes}


def du_sk(path: str):
    """`du -sk` 磁盘块占用。部分沙箱不可用，返回 None（不假装成精确值）。"""
    try:
        out = subprocess.run(["du", "-sk", path], capture_output=True, text=True, check=True).stdout
        return int(out.split()[0])
    except Exception:
        return None


def tracked_bytes(repo_root: str) -> int:
    """**纳入版本控制的文件字节合计**（`git ls-files` 跟踪路径，逐个 `os.path.getsize` 求和）。

    为什么不用 `du -sk` 量工作树：工作树里除了入库内容，还会有构建产物（`site/`、
    `site-docs/`）、别人的未提交草稿、`.venv-mkdocs/` 等**车间地面**——它们**不属于
    入库内容**，却让这个数字「每个 clone 一个样」，生成物永远无法复现。
    改成只统计 `git ls-files` 跟踪文件之后：
      * 任意 clone / 任意工作树，只要提交树一致，这个值**就一致**（可复现优先）；
      * 不受 `du` 块开销影响，值是精确字节数；
      * 不受并发未提交工作影响。
    与 `version_control` 口径同源（同为 `git ls-files`）。
    """
    total = 0
    for rel in git_tracked(repo_root):
        try:
            total += os.path.getsize(os.path.join(repo_root, rel))
        except OSError:
            continue
    return total


def content_fingerprint(docs: list) -> str:
    """条目 + 文档内容的确定性指纹（sha256）。

    只取路径 / 字节 / 行数等**内容派生**字段，不含时间戳与绝对路径，
    因此「仓库内容不变 -> 指纹不变」，可用于验证索引与统计可复现。
    """
    h = hashlib.sha256()
    for doc in sorted(docs, key=lambda d: d["path"]):
        h.update(f"{doc['path']}\0{doc['bytes']}\0{doc['lines']}\0{int(doc['has_front_matter'])}\n"
                 .encode("utf-8"))
    return h.hexdigest()


def build_stats(repo_root: str, docs: list) -> dict:
    entries = [d for d in docs if d["is_entry"]]
    library_docs = [d for d in docs if d["top"] in LIBRARIES]
    lib_entries = [d for d in entries if d["top"] in LIBRARIES]

    libs = {}
    for lib in LIBRARIES:
        dm = dir_metrics(repo_root, lib)
        this_entries = [e for e in entries if e["top"] == lib]
        libs[lib] = {
            "entries": len(this_entries),
            "documents_md": sum(1 for d in docs if d["top"] == lib),
            "md_by_category": {
                cat: sum(1 for d in library_docs if d["top"] == lib and d["category"] == cat)
                for cat in PANEL_TOPS
            },
            "dirs_by_category": {
                cat: len({entry_dir(e["path"]) for e in this_entries if e["category"] == cat})
                for cat in PANEL_TOPS
            },
            "lines": sum(e["lines"] for e in this_entries),
            "bytes": sum(e["bytes"] for e in this_entries),
            "lines_raw": sum(e["lines_raw"] for e in this_entries),
            "dir_files": dm["files"],
            "dir_md": dm["md"],
            "dir_bytes": dm["bytes"],
            "du_sk": du_sk(os.path.join(repo_root, lib)),
        }

    tracked = git_tracked(repo_root)
    tracked_libraries = [p for p in tracked if p.split("/")[0] in PANEL_TOPS]

    stats = {
        "schema_version": SCHEMA_VERSION,
        "generated_by": "scripts/library_index.py",
        "content_fingerprint": content_fingerprint(docs),
        "repo_root": os.path.relpath(os.path.abspath(repo_root), os.getcwd()).replace(os.sep, "/"),
        "definitions": {
            "entry": "条目 = 文件名字面为 report.md 的 Markdown（每个 <topic>-research/ 一份）",
            "document": "文档 = 除 INDEX.md / index/* 生成物以外的所有 .md（含各 README.md、docs/*.md）",
            "lines": "正文行数，剔除 front-matter 围栏块（含首尾 --- 行）；lines_raw 为文件原始行数",
            "du_sk": "磁盘块占用（du -sk），含文件系统块开销，故大于字节数之和；不可用时为 null",
        "du_worktree": "**已移除**（原为工作树 du -sk 扣 `.git`）：它含构建产物与他人未提交草稿，任何干净 clone 都不可复现。取代字段见 `storage.tracked_bytes`",
        "tracked_bytes": "纳入版本控制的文件字节合计（git ls-files 逐个 getsize 求和）；与提交树同源，任意 clone 重跑一致，不受构建产物/未提交草稿/块开销影响",
        "version_control": "版本控制计数取自 git ls-files，**含生成物本身**；条目 / 文档计数则排除生成物",
        "repo_root": "相对运行目录的仓库根（按 `--repo-root .` 运行时为 `.`）：不写机器相关绝对路径，保证同一内容在不同目录下产出逐字节一致",
        },
        "entries": {
            "total": len(entries),
            "with_front_matter": sum(1 for d in entries if d["has_front_matter"]),
            "without_front_matter": sum(1 for d in entries if not d["has_front_matter"]),
            "with_date": sum(1 for d in entries if d["date_valid"]),
            "lines": sum(d["lines"] for d in entries),
            "bytes": sum(d["bytes"] for d in entries),
            "children": sum(len(d["children"]) for d in entries),
        },
        "documents": {
            "md_total": len(docs),
            "md_libraries": len(library_docs),
            "with_front_matter": sum(1 for d in docs if d["has_front_matter"]),
            "named_report_md": sum(1 for d in docs if d["filename"].lower() == "report.md"),
            "named_readme_md": sum(1 for d in docs if d["filename"].lower() == "readme.md"),
            "lines": sum(d["lines"] for d in docs),
            "bytes": sum(d["bytes"] for d in docs),
        },
        "libraries": libs,
        "totals": {
            "libraries": len(LIBRARIES),
            "library_entries": len(lib_entries),
            "library_documents_md": len(library_docs),
            "library_dir_files": sum(v["dir_files"] for v in libs.values()),
            "library_dir_bytes": sum(v["dir_bytes"] for v in libs.values()),
            "library_du_sk": sum(v["du_sk"] or 0 for v in libs.values()),
            "library_entry_lines": sum(v["lines"] for v in libs.values()),
            "library_entry_bytes": sum(v["bytes"] for v in libs.values()),
        },
        "version_control": {
            "tracked_total": len(tracked),
            "tracked_md": sum(1 for p in tracked if p.lower().endswith(".md")),
            "tracked_report_md": sum(1 for p in tracked if p.rsplit("/", 1)[-1].lower() == "report.md"),
            "tracked_libraries": len(tracked_libraries),
            "tracked_repo_root": sum(1 for p in tracked if "/" not in p),
            "tracked_docs": sum(1 for p in tracked if p.startswith("docs/")),
            "tracked_scripts": sum(1 for p in tracked if p.startswith("scripts/")),
        },
        "doc_stats": _doc_stats(repo_root, docs, entries, tracked),
        "storage": {
            "tracked_bytes": tracked_bytes(repo_root),
            "definition": (
                "纳入版本控制的文件字节合计（`git ls-files` 跟踪路径逐个 getsize 求和）；"
                "刻意**不**用 du 量工作树——工作树含 site/site-docs/构建产物、别人的未提交草稿、"
                "虚拟环境等「车间地面」，会让数字每个 clone 一个样、生成物不可复现。"
                "本字段与提交树同源，任意 clone 重跑一致。"
            ),
        },
    }
    return stats


def _md_metrics(repo_root: str, rel_paths: list) -> dict:
    """对一组 `.md` 汇总行数（剔除 front-matter）与字节。"""
    lines = raw = nbytes = 0
    for rel in rel_paths:
        abs_path = os.path.join(repo_root, rel)
        try:
            text = read_text(abs_path)
        except OSError:
            continue
        _fm, body, _blk = split_front_matter(text)
        lines += body
        raw += wc_l(text)
        nbytes += os.path.getsize(abs_path)
    return {"files": len(rel_paths), "lines": lines, "lines_raw": raw, "bytes": nbytes}


def _doc_stats(repo_root: str, docs: list, entries: list, tracked: list) -> dict:
    """为 `docs/statistics.md` / 根 `README.md` 提供可直接引用的确定数值。

    按「资料库 -> 类别 -> 条目」聚合，并给出「条目 + 同库其它 .md」的库内合计。
    """
    md = [d["path"] for d in docs]
    return {
        "libraries": {
            lib: {
                "report_md": _md_metrics(repo_root, [d["path"] for d in entries if d["top"] == lib]),
                "report_md_by_category": {
                    cat: _md_metrics(repo_root, [d["path"] for d in entries
                                                 if d["top"] == lib and d["category"] == cat])
                    for cat in PANEL_TOPS
                },
                "other_md": _md_metrics(repo_root, [d["path"] for d in docs
                                                    if d["top"] == lib and not d["is_entry"]]),
                "dir_md": _md_metrics(repo_root, [q for q in md if q.split("/")[0] == lib]),
            }
            for lib in LIBRARIES
        },
        "repo_md": _md_metrics(repo_root, md),
        "library_md": _md_metrics(repo_root, [d["path"] for d in docs if d["top"] in LIBRARIES]),
        "root_readme": _md_metrics(repo_root, ["README.md"]),
        "docs_md": _md_metrics(repo_root, [q for q in md if q.startswith("docs/")]),
        "scripts_md": _md_metrics(repo_root, [q for q in md if q.startswith("scripts/")]),
        "tracked_root_non_md": sorted(q for q in tracked if "/" not in q and not q.lower().endswith(".md")),
    }


# --------------------------------------------------------------------------
# 渲染
# --------------------------------------------------------------------------

def display_root(repo_root: str, out_root: str) -> str:
    """生成物头部显示的「输出根目录」。

    返回**相对仓库根**的路径（默认 `--out-root` = 仓库根 → `.`），而不是绝对路径：
    绝对路径会随仓库所在位置变化，导致同一份内容在不同目录下产出的文件不逐字节一致，
    无法做幂等 / 可复现校验。
    """
    rel = os.path.relpath(os.path.abspath(out_root), os.path.abspath(repo_root))
    return "." if rel == "." else rel.replace(os.sep, "/")


def header(title: str, out_root: str, dry_run: bool) -> list:
    lines = [f"# {title}", "", f"> {GENERATED_NOTE}"]
    if dry_run:
        lines.append(f"> {DRY_RUN_NOTE}")
    lines += [
        "> 生成命令：`python3 scripts/library_index.py --repo-root . --out-root .`",
        f"> 输出根目录：`{out_root}`",
        f"> 条目口径：条目 = `{ENTRY_BASENAME}`",
        "",
        "---",
        "",
    ]
    return lines


def link(rel_path: str, prefix: str) -> str:
    target = f"{prefix}{rel_path}" if prefix else rel_path
    label = rel_path.replace("|", "\\|")
    return f"[{label}](<{target}>)"


def link_label(rel_path: str, prefix: str, label: str) -> str:
    target = f"{prefix}{rel_path}" if prefix else rel_path
    return f"[{label.replace('|', '\\|')}](<{target}>)"


def group_table(entries: list, key_fn) -> list:
    groups: dict = {}
    for entry in entries:
        groups.setdefault(str(key_fn(entry)), []).append(entry)

    lines = []
    for name in sorted(groups, key=lambda s: (s == UNFILED, str(s))):
        members = sorted(groups[name], key=lambda e: e["path"])
        lines += [f"## {name} ({len(members)})", ""]
        lines += ["| 条目 | 标题 | type | date | status |", "| --- | --- | --- | --- | --- |"]
        for entry in members:
            lines.append(
                "| {link} | {title} | {type} | {date} | {status} |".format(
                    link=link(entry["path"], "../"),
                    title=entry["title"].replace("|", "\\|") or "—",
                    type=entry["type"] or "—",
                    date=entry["date_iso"] or "—",
                    status=entry["status"] or "—",
                )
            )
        lines.append("")
    return lines


def entry_label(doc: dict) -> str:
    """折叠索引与其他入口共用条目展示名。"""
    return entry_short_name(doc)


def render_entry_block(doc: dict, prefix: str, indent: str = "") -> list:
    """单个条目的折叠块：摘要可直达条目，块内列出子文档（可直达子报告）。"""
    children = doc["children"]
    date = doc["date_iso"] or "—"
    summary = (
        f"<b>{entry_label(doc)}</b> · <code>{doc['path']}</code> · "
        f"{doc['lines']} 行 · {date}"
    )
    pad = indent + "  "
    lines = [f"{indent}<details>", f"{indent}<summary>{summary}</summary>", f"{indent}", ""]
    lines += [
        f"{pad}* **条目**：{link_label(doc['path'], prefix, doc['path'])}"
        f"（{doc['lines']} 行 / {doc['bytes']:,} B）",
        f"{pad}* **专题目录**：`{entry_dir(doc['path'])}`",
        f"{pad}* **元数据**：type=`{doc['type'] or '—'}` · domain=`{doc['domain']}` · "
        f"subject=`{doc['subject']}` · date=`{date}` · status=`{doc['status'] or '—'}`",
        f"{pad}* **子文档（{len(children)}）**",
    ]
    for child in children:
        label = os.path.relpath(child["path"], entry_dir(doc["path"]))
        lines.append(
            f"{pad}    * {link_label(child['path'], prefix, label)}"
            f" — {child['lines']} 行 / {child['bytes']:,} B"
        )
    if not children:
        lines.append(f"{pad}    * _该条目暂无子文档_")
    lines += ["", f"{indent}</details>", ""]
    return lines


def render_index(docs: list, orphans: list, stats: dict, out_root: str, dry_run: bool,
                 cfg: dict, mapping: dict) -> str:
    entries = [d for d in docs if d["is_entry"]]
    counts = stats["entries"]
    dc = stats["documents"]
    panel_counts = {p["id"]: sum(1 for v in mapping.values() if v["id"] == p["id"])
                    for p in cfg["panels"]}
    panel_summary = " · ".join(
        f"{p['title']} {panel_counts[p['id']]}" for p in cfg["panels"])

    lines = header("Research 仓库图书馆索引", out_root, dry_run)

    lines += [
        "## 统计总览",
        "",
        f"> 数字由 `scripts/library_index.py` 产出；机器可读版见 "
        f"[index/stats.json](<index/stats.json>)。生成物（本文件、`index/*`）不计入"
        f"**条目与文档**计数；「纳入版本控制」两行取自 `git ls-files`，**含**生成物本身。",
        "",
        "| 指标 | 数量 |",
        "| --- | --- |",
        f"| **条目数**（`{ENTRY_BASENAME}`） | **{counts['total']}** |",
        f"| 板块（[`{PANELS_FILE}`](<{PANELS_FILE}>)） | {panel_summary} |",
        f"| 条目子文档数 | {counts['children']} |",
        f"| 条目正文行数（剔除 front-matter） | {counts['lines']:,} |",
        f"| 条目字节 | {counts['bytes']:,} B |",
        f"| 带 front-matter 的条目 | {counts['with_front_matter']} |",
        f"| 带合法 `date` 的条目 | {counts['with_date']} |",
        f"| 文档（除生成物外的全部 `.md`） | {dc['md_total']} |",
        f"| 其中文件名 `README.md` | {dc['named_readme_md']} |",
        f"| 纳入版本控制的文件 | {stats['version_control']['tracked_total']} |",
        f"| 纳入版本控制的 `.md` | {stats['version_control']['tracked_md']} |",
        "",
        "> 条目 = `report.md`；`README.md`（根 / 子库 / `scripts/`）、`docs/*.md`、"
        "`notes/`、`raw-extracts/`、`plan.md`、`sources-index.md`、`knowledge-graph.md` "
        "都是**文档而非条目**，仅在所属条目的折叠块里作为子文档出现。",
        "> **板块**是逻辑视图（跨物理目录），映射全部在 "
        f"[`{PANELS_FILE}`](<{PANELS_FILE}>)；每个条目恰好归入一个板块，"
        "未归类 / 重复归类 / 代表条目缺 `report.md` 都会让脚本在生成前非零退出。",
        "",
        "## 按板块入口",
        "",
        "| 资料库 | 条目数 | 文档（`.md`） | 条目行数 | 条目字节 | 入口 |",
        "| --- | --: | --: | --: | --: | --- |",
    ]
    for lib in LIBRARIES:
        lib_stats = stats["libraries"][lib]
        lines.append(
            f"| {lib} | {lib_stats['entries']} | {lib_stats['documents_md']} | "
            f"{lib_stats['lines']:,} | {lib_stats['bytes']:,} B | "
            f"[板块页 →](<{lib}/README.md>) |"
        )
    lines += [
        f"| **合计** | **{counts['total']}** | **{dc['md_total']}** | "
        f"**{counts['lines']:,}** | **{counts['bytes']:,} B** | — |",
        "",
        "## 分面索引",
        "",
        "| 分面 | 说明 |",
        "| --- | --- |",
    ]
    for name, title in FACET_TITLES.items():
        lines.append(f"| [index/{name}.md](<index/{name}.md>) | {title} |")
    lines.append("")

    # ---- 按库折叠：条目 + 子报告直达 ----
    lines += ["## 条目索引（按板块目录折叠，可直达条目与子报告）", ""]
    for lib in PANEL_TOPS:
        lib_entries = sorted([d for d in entries if d["top"] == lib], key=lambda d: d["path"])
        lib_stats = stats["libraries"][lib]
        lines += [
            f"### {lib}（{len(lib_entries)} 条目 / {lib_stats['documents_md']} 文档）",
            "",
        ]
        for cat in PANEL_TOPS:
            cat_entries = [d for d in lib_entries if d["category"] == cat]
            if not cat_entries:
                continue
            child_total = sum(len(d["children"]) for d in cat_entries)
            cat_cn = {"Models": "模型系列", "LLM": "语言模型", "AIGC": "内容生成",
                      "WorldModel": "世界模型", "AI4Science": "科学研究",
                      "Evaluation": "评测科学",
                      "Infra": "基础设施", "OpenSource": "开源仓库"}.get(cat, cat)
            lines += [
                f"<details>",
                f"<summary><b>{cat_cn} {cat}（{len(cat_entries)} 条目 / {child_total} 子文档）</b></summary>",
                "",
            ]
            for doc in cat_entries:
                lines += render_entry_block(doc, "", "  ")
            lines += ["</details>", ""]

    # 游离文档：资料库内不属于任何条目目录的 .md（子库 README、无 report.md 的深读项目）
    if orphans:
        lines += [
            "### 游离文档（不属于任何条目目录）",
            "",
            "以下文档位于资料库内，但没有对应的 `report.md` 条目目录，索引在此单独列出以保证可达：",
            "",
            "| 文档 | 板块 | 行数 | 字节 |",
            "| --- | --- | --: | --: |",
        ]
        for doc in sorted(orphans, key=lambda d: d["path"]):
            lines.append(
                f"| {link(doc['path'], '')} | {doc['top']} | {doc['lines']:,} | {doc['bytes']:,} B |"
            )
        lines.append("")

    # 非资料库条目（根目录等）
    other_entries = [d for d in entries if d["top"] not in PANEL_TOPS]
    if other_entries:
        lines += ["### 其它位置条目", ""]
        for doc in other_entries:
            lines += render_entry_block(doc, "")
    lines.append("")

    lines += [
        "## 说明",
        "",
        "* 本索引是**派生数据**，仓库里的条目文件才是唯一事实来源；重建索引只需重跑脚本。",
        f"* 当前 {counts['with_front_matter']} 份条目带 front-matter；缺失的 `type` / `date` / `status` "
        "显示为 `—`，domain / subject / topic 缺失时由路径推断。",
        f"* 可选元数据：`{'` / `'.join(KNOWN_KEYS)}`。",
        "* 脚本只读扫描、只写生成物；**不会删除或改写任何条目文件**。",
        "",
    ]
    return "\n".join(lines)


def render_by_report(entries: list, out_root: str, dry_run: bool, mapping: dict) -> str:
    """全部条目的平铺索引 —— README 的「完整索引」只链接到这里，不再复制第二份。

    前 3 列是核心视图（条目 | 板块 | 路径），其余列（子报告数 / 行数 / 日期）
    保留在后面；「板块」列由 ``scripts/panels.json`` 驱动，**只出现一次**（条目之后）。
    """
    lines = header(FACET_TITLES["by-report"], out_root, dry_run)
    lines += [
        f"共 **{len(entries)}** 个条目（`{ENTRY_BASENAME}`）。「行数」为正文行数，已剔除 front-matter；"
        f"「板块」列由 [`{PANELS_FILE}`](<../{PANELS_FILE}>) 驱动。",
        "",
        "| 条目 | 板块 | 路径 | 子报告数 | 行数 | 日期 |",
        "| --- | --- | --- | --: | --: | --- |",
    ]
    for doc in sorted(entries, key=lambda d: d["path"]):
        panel = mapping.get(doc["path"])
        lines.append(
            "| {label} | {panel} | {path} | {kids} | {lines} | {date} |".format(
                label=entry_label(doc),
                panel=panel["title"] if panel else "—",
                path=link(doc["path"], "../"),
                kids=len(doc["children"]),
                lines=f"{doc['lines']:,}",
                date=doc["date_iso"] or "—",
            )
        )
    total_children = sum(len(d["children"]) for d in entries)
    total_lines = sum(d["lines"] for d in entries)
    lines += [
        f"| **合计** | — | — | **{total_children}** | **{total_lines:,}** | — |",
        "",
    ]
    return "\n".join(lines)


def render_by_repo(entries: list, out_root: str, dry_run: bool) -> str:
    lines = header(FACET_TITLES["by-repo"], out_root, dry_run)
    groups: dict = {}
    for entry in entries:
        keys = entry["upstream"] or ([entry["top"]] if entry["top"] else [ROOT_GROUP])
        for key in keys or [ROOT_GROUP]:
            groups.setdefault(str(key), []).append(entry)

    for name in sorted(groups, key=lambda s: (s in (UNFILED, ROOT_GROUP), str(s))):
        members = sorted(groups[name], key=lambda e: e["path"])
        lines += [f"## {name} ({len(members)})", ""]
        for entry in members:
            lines.append(f"* {link(entry['path'], '../')} — {entry['lines']:,} 行")
        lines.append("")
    return "\n".join(lines)


def render_recent(entries: list, out_root: str, dry_run: bool, limit: int) -> str:
    lines = header(FACET_TITLES["recent"], out_root, dry_run)
    dated = sorted([e for e in entries if e["date_valid"]],
                   key=lambda e: (e["date_iso"], e["path"]), reverse=True)
    undated = sorted([e for e in entries if not e["date_valid"]], key=lambda e: e["path"])

    lines += [f"## 最近 {limit} 条（按 date 降序）", ""]
    if dated:
        lines += ["| 条目 | date | 板块 | 专题 |", "| --- | --- | --- | --- |"]
        for entry in dated[:limit]:
            lines.append(f"| {link(entry['path'], '../')} | {entry['date_iso']} | "
                         f"{entry['top']} | {entry['subject']} |")
    else:
        lines.append(f"_当前没有任何条目带合法 `date`（front-matter 共 "
                     f"{sum(1 for e in entries if e['has_front_matter'])} 份）。_")
    lines.append("")

    lines += [f"## 无 date 元数据（{len(undated)}）", ""]
    lines.append("以下条目缺少可解析的 `date`，无法参与「最近更新」排序：")
    lines.append("")
    for entry in undated:
        lines.append(f"* {link(entry['path'], '../')}")
    lines.append("")
    return "\n".join(lines)


def stale_reasons(entry: dict, stale_days: int) -> list:
    reasons = []
    status = entry["status"].strip().lower()
    if status and status not in NON_STALE_STATUSES:
        reasons.append(f"status={entry['status']}")
    if entry["date_valid"] and entry["age_days"] is not None and entry["age_days"] > stale_days:
        reasons.append(f"date={entry['date_iso']}（{entry['age_days']} 天前）")
    return reasons


def render_stale(entries: list, out_root: str, dry_run: bool, stale_days: int) -> str:
    lines = header(FACET_TITLES["stale"], out_root, dry_run)
    lines += [
        "判定口径：`status` 不是 active/current/ok/stable/published/completed，或 `date` 早于 "
        f"{stale_days} 天。",
        "",
    ]

    flagged, no_meta = [], []
    for entry in sorted(entries, key=lambda e: e["path"]):
        reasons = stale_reasons(entry, stale_days)
        if reasons:
            flagged.append((entry, reasons))
        elif not entry["date_valid"] and not entry["status"]:
            no_meta.append(entry)

    lines += [f"## 已标记（{len(flagged)}）", ""]
    if flagged:
        lines += ["| 条目 | 原因 |", "| --- | --- |"]
        for entry, reasons in flagged:
            lines.append(f"| {link(entry['path'], '../')} | {'；'.join(reasons)} |")
    else:
        lines.append("_无。_")
    lines.append("")

    lines += [f"## 无 date 且无 status（无法判定，{len(no_meta)}）", ""]
    if no_meta:
        lines.append("以下条目既没有 `date` 也没有 `status`，陈旧度无法评估（不算作已标记）：")
        lines.append("")
        for entry in no_meta:
            lines.append(f"* {link(entry['path'], '../')}")
    else:
        lines.append("_无。_")
    lines.append("")
    return "\n".join(lines)


def render_by_topic(entries: list, out_root: str, dry_run: bool) -> str:
    """先按展示名列主报告，再列可直达的 topics/ 分析分册。"""
    lines = header(FACET_TITLES["by-topic"], out_root, dry_run)
    lines += [
        "上半部分使用主报告的展示名，未设置时回退到 `topic` 元数据；下半部分汇总各报告下的 `topics/` 分册。"
        "分析分册属于父专题，不单独计为独立研究专题。",
        "",
    ]
    lines += group_table(entries, lambda e: e.get("display_name") or e["topic"] or UNFILED)

    children = []
    for entry in entries:
        for child in entry.get("children", []):
            if "topics" in child["path"].split("/"):
                children.append((entry, child))
    if children:
        lines += [f"## 专题内分析分册（{len(children)}）", "",
                  "| 所属报告 | 分册入口 |", "| --- | --- |"]
        for entry, child in sorted(children, key=lambda pair: (pair[0]["path"], pair[1]["path"])):
            lines.append(
                f"| {link_label(entry['path'], '../', entry_short_name(entry))} | "
                f"{link_label(child['path'], '../', child['title'] or child['filename'])} |"
            )
        lines.append("")
    return "\n".join(lines)


def render_facets(entries: list, out_root: str, dry_run: bool, args, mapping: dict) -> dict:
    return {
        "by-domain": "\n".join(header(FACET_TITLES["by-domain"], out_root, dry_run)
                               + group_table(entries, lambda e: e["domain"])),
        "by-subject": "\n".join(header(FACET_TITLES["by-subject"], out_root, dry_run)
                                + group_table(entries, lambda e: e["subject"])),
        "by-repo": render_by_repo(entries, out_root, dry_run),
        "by-topic": render_by_topic(entries, out_root, dry_run),
        "by-report": render_by_report(entries, out_root, dry_run, mapping),
        "recent": render_recent(entries, out_root, dry_run, args.recent_limit),
        "stale": render_stale(entries, out_root, dry_run, args.stale_days),
    }


# --------------------------------------------------------------------------
# 板块（scripts/panels.json）
# --------------------------------------------------------------------------

#: 板块配置：**所有**板块映射都在这里，脚本里不硬编码任何目录名。
PANELS_FILE = "scripts/panels.json"
ENTRY_MARK = "-research"
DATE_SOURCE_FRONT_MATTER = "front-matter date"
DATE_SOURCE_GIT = "最近提交日"
TOPIC_CATEGORY = "TechnicalTopics"


class ConfigError(Exception):
    """板块配置或 README 契约不满足 —— 属于「生成前就必须失败」的错误。"""


def load_panels(repo_root: str) -> dict:
    """读取并校验 ``scripts/panels.json``。"""
    path = os.path.join(repo_root, PANELS_FILE)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
    except OSError as exc:
        raise ConfigError(f"无法读取板块配置 {PANELS_FILE}：{exc}")
    except json.JSONDecodeError as exc:
        raise ConfigError(f"板块配置 {PANELS_FILE} 不是合法 JSON：{exc}")

    if not isinstance(cfg, dict):
        raise ConfigError(f"{PANELS_FILE} 顶层必须是 JSON 对象")
    panels = cfg.get("panels")
    if not isinstance(panels, list) or not panels:
        raise ConfigError(f"{PANELS_FILE} 缺少非空的 panels 列表")

    seen = set()
    for panel in panels:
        if not isinstance(panel, dict):
            raise ConfigError(f"panels 元素必须是对象：{panel!r}")
        for key in ("id", "title", "emoji", "tagline", "match", "representatives"):
            if key not in panel:
                raise ConfigError(f"面板缺少字段 `{key}`：{panel.get('id', panel)}")
        if panel["id"] in seen:
            raise ConfigError(f"面板 id 重复：{panel['id']}")
        seen.add(panel["id"])
        for key in ("match", "representatives"):
            if not isinstance(panel[key], list) or not panel[key]:
                raise ConfigError(f"面板 {panel['id']} 的 `{key}` 必须是非空列表")
        entry_order = panel.get("entry_order")
        if entry_order is not None:
            if (not isinstance(entry_order, list)
                    or any(not isinstance(item, str) or not item.strip() for item in entry_order)):
                raise ConfigError(f"面板 {panel['id']} 的 `entry_order` 必须是非空路径字符串列表")
            if len(entry_order) != len(set(entry_order)):
                raise ConfigError(f"面板 {panel['id']} 的 `entry_order` 不能有重复路径")
        if "topic_index" in panel and not isinstance(panel["topic_index"], bool):
            raise ConfigError(f"面板 {panel['id']} 的 `topic_index` 必须是布尔值")

    limit = cfg.get("recent_limit")
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ConfigError(f"recent_limit 必须是正整数：{limit!r}")
    fallback = cfg.get("date_fallback")
    if fallback not in ("none", "git"):
        raise ConfigError(f"date_fallback 只能是 `none` 或 `git`：{fallback!r}")
    return cfg


def panel_top_dirs(cfg: dict) -> tuple[str, ...]:
    """从板块匹配规则推导顶层目录，保证统计口径与 panels.json 同源。"""
    roots = []
    for panel in cfg["panels"]:
        panel_roots = {pattern.replace(os.sep, "/").split("/", 1)[0]
                       for pattern in panel["match"]}
        if len(panel_roots) != 1:
            raise ConfigError(
                f"面板 {panel['id']} 的 match 必须落在同一个顶层目录：{sorted(panel_roots)}"
            )
        root = next(iter(panel_roots))
        if any(ch in root for ch in "*?["):
            raise ConfigError(f"面板 {panel['id']} 的顶层目录不能是 glob：{root}")
        if panel.get("directory", panel["title"]) != root:
            raise ConfigError(
                f"面板 {panel['id']} 的 directory 与 match 根目录不一致："
                f"directory={panel.get('directory')!r}, match={root!r}"
            )
        if root in roots:
            raise ConfigError(f"多个面板映射到同一顶层目录：{root}")
        roots.append(root)
    return tuple(roots)


def panel_dir(panel: dict) -> str:
    """物理目录名；通常等于展示名，少数板块可用独立 display title。"""
    return panel.get("directory", panel["title"])


def sort_panel_entries(members: list, panel: dict) -> list:
    """按可选的 entry_order 排列板块入口；未配置时维持路径排序。"""
    order = panel.get("entry_order", [])
    if not order:
        return sorted(members, key=lambda d: d["path"])
    rank = {directory: index for index, directory in enumerate(order)}
    return sorted(
        members,
        key=lambda d: (rank.get(entry_dir(d["path"]), len(rank)), d["path"]),
    )


def match_panels(entries: list, cfg: dict) -> tuple:
    """把每个条目目录映射到**唯一**面板。

    返回 ``(mapping, unassigned, duplicated)``；``mapping`` 的键是条目
    ``report.md`` 的仓库相对路径。函数本身只计算，不退出 —— 由调用方决定。
    """
    panels = cfg["panels"]
    mapping, unassigned, duplicated = {}, [], []
    for doc in sorted(entries, key=lambda d: d["path"]):
        directory = entry_dir(doc["path"])
        hits = [p for p in panels
                if any(fnmatch.fnmatchcase(directory, pat) for pat in p["match"])]
        if not hits:
            unassigned.append((doc["path"], directory))
        elif len(hits) > 1:
            duplicated.append((doc["path"], [p["id"] for p in hits]))
        else:
            mapping[doc["path"]] = hits[0]
    return mapping, unassigned, duplicated


def panel_representatives(repo_root: str, cfg: dict) -> list:
    """代表条目里必须存在真实 ``report.md``；返回缺失清单。"""
    missing = []
    for panel in cfg["panels"]:
        for rep in panel["representatives"]:
            if not os.path.isfile(os.path.join(repo_root, rep, ENTRY_BASENAME)):
                missing.append((panel["id"], rep))
        for directory in panel.get("entry_order", []):
            if not os.path.isfile(os.path.join(repo_root, directory, ENTRY_BASENAME)):
                missing.append((panel["id"], directory))
    return missing


def validate_panels(entries: list, cfg: dict, repo_root: str) -> tuple:
    """生成前的板块校验：未归类 / 重复归类 / 代表条目缺 report.md 都必须为 0。"""
    mapping, unassigned, duplicated = match_panels(entries, cfg)
    missing = panel_representatives(repo_root, cfg)
    for rel in cfg.get("highlights", []):
        if not os.path.isfile(os.path.join(repo_root, rel, ENTRY_BASENAME)):
            missing.append(("highlights", rel))

    print(f"板块校验：条目 {len(entries)} · 已归类 {len(mapping)} · "
          f"未归类 {len(unassigned)} · 重复归类 {len(duplicated)} · "
          f"代表条目缺失 {len(missing)}")
    for path, directory in unassigned:
        print(f"  [未归类]   {directory}  <- {path}")
    for path, ids in duplicated:
        print(f"  [重复归类] {path} -> {' + '.join(ids)}")
    for pid, rep in missing:
        print(f"  [代表条目无 {ENTRY_BASENAME}] 面板 {pid}: {rep}")

    counts = {}
    for panel in cfg["panels"]:
        counts[panel["id"]] = sum(1 for p in mapping.values() if p["id"] == panel["id"])
    print("  各面板条目数：" + " · ".join(
        f"{p['title']}={counts[p['id']]}" for p in cfg["panels"]) + f"（合计 {sum(counts.values())}）")

    return mapping, (unassigned, duplicated, missing)


def git_last_commit_date(repo_root: str, rel_path: str) -> str:
    """条目文件的「最近提交日」（``git log --follow -1 --format=%cs``）。"""
    try:
        res = subprocess.run(
            ["git", "-C", repo_root, "log", "--follow", "-1", "--format=%cs", "--", rel_path],
            capture_output=True, text=True, check=True,
        )
        return res.stdout.strip()
    except Exception:
        return ""


def recent_rows(repo_root: str, entries: list, cfg: dict) -> list:
    """「最近更新」行：优先 front-matter ``date``，缺失时按配置回退 git 最近提交日。"""
    rows = []
    for doc in entries:
        if doc["date_valid"]:
            rows.append({"doc": doc, "date": doc["date_iso"], "source": DATE_SOURCE_FRONT_MATTER})
        elif cfg["date_fallback"] == "git":
            date = git_last_commit_date(repo_root, doc["path"])
            if date:
                rows.append({"doc": doc, "date": date, "source": DATE_SOURCE_GIT})
        # date_fallback=none 且无 front-matter date → 不进榜（避免用「—」占位）
    rows.sort(key=lambda r: r["doc"]["path"])
    # 稳定排序两级：日期降序；同日优先 front-matter 真值，再回退「最近提交日」。
    rows.sort(key=lambda r: (r["date"], r["source"] == DATE_SOURCE_FRONT_MATTER), reverse=True)
    return rows[:cfg["recent_limit"]]

def entry_short_name(doc: dict) -> str:
    """展示名优先使用元数据；未指定时保留目录短名。"""
    if doc.get("display_name"):
        return doc["display_name"]
    name = os.path.basename(entry_dir(doc["path"])) or doc["filename"]
    return name[: -len(ENTRY_MARK)] if name.endswith(ENTRY_MARK) else name


# --------------------------------------------------------------------------
# 根 README 的 SCRIPT 区块（幂等替换）
# --------------------------------------------------------------------------

README_FILE = "README.md"
README_BLOCKS = ("badges", "structure", "panels", "highlights", "topics", "recent", "index")

#: 站点与仓库的公开地址（README 徽章/入口、站点首页与 nav 互链使用）。
SITE_URL = "https://zhoucanzong.github.io/ResearchReport/"
REPO_URL = "https://github.com/zhoucanzong/ResearchReport"


def block_pattern(name: str):
    return re.compile(
        rf"(<!--\s*SCRIPT:{re.escape(name)} START[^>]*-->)(.*?)(<!--\s*SCRIPT:{re.escape(name)} END\s*-->)",
        re.S,
    )


def generated_md_count(out_root: str = "") -> int:
    """生成物里的 `.md` 个数：`INDEX.md` + `index/*.md`（stats.json 不算）。"""
    return 1 + len(FACET_TITLES)


def last_commit_date(repo_root: str, fallback: _dt.date) -> _dt.date:
    """「更新日期」徽章的口径：**最后一次提交日** `git log -1 --format=%cs`。

    为什么不取当天 wall-clock：跨零点会漂，幂等只在同日成立；取最后一次提交日
    之后，任意一天重跑生成物都**字节一致**。git 不可用（如导出的 tarball）时
    回退给定日期，保证脚本不因缺 git 而崩。
    """
    try:
        out = subprocess.run(
            ["git", "-C", repo_root, "log", "-1", "--format=%cs"],
            capture_output=True, text=True, timeout=15,
        )
        if out.returncode == 0:
            s = out.stdout.strip()
            if s:
                return _dt.date.fromisoformat(s)
    except Exception:
        pass
    return fallback



def render_badges(stats: dict, topics: int, today: _dt.date, panels: int | None = None) -> str:
    """GitHub 原生统计导航，不依赖远程徽章图片；保留旧调用签名。"""
    if panels is None:
        panels = stats.get("totals", {}).get("libraries", 0)
    items = [
        (stats["entries"]["total"], "主报告", "index/by-report.md"),
        (stats["entries"]["children"], "分册与子文档", "INDEX.md"),
        (topics, "研究专题", "index/by-topic.md"),
        (panels, "研究板块", "#研究板块"),
    ]
    return " &nbsp; · &nbsp; ".join(
        f"[**{count}** {label}]({target})" for count, label, target in items
    )


def render_structure_block(cfg: dict, mapping: dict, entries: list) -> str:
    """图书馆结构树（代码块，GitHub 与站点都可读）：板块计数、代表条目与生成管线。"""
    topic_ids = {p["id"] for p in cfg["panels"] if p.get("topic_index", False)}
    topics = sum(1 for d in entries if mapping.get(d["path"], {}).get("id") in topic_ids)
    lines = [
        "```text",
        f"ResearchReport/    {len(entries)} 条目 · {topics} 研究专题 · {len(cfg['panels'])} 板块",
        "│",
    ]
    panels = cfg["panels"]
    for i, panel in enumerate(panels):
        members = [d for d in entries
                   if mapping.get(d["path"], {}).get("id") == panel["id"]]
        branch = "├─"  # 生成管线才是树的最后一个分支（└─）
        by_dir = {entry_dir(d["path"]): d for d in entries}
        reps = " · ".join(
            entry_short_name(by_dir[rel.rstrip("/")])
            if rel.rstrip("/") in by_dir
            else rel.rstrip("/").rsplit("/", 1)[-1]
            for rel in panel.get("representatives", [])[:3]
        )
        rep_text = f"（{reps} …）" if reps else ""
        lines.append(
            f"{branch} {panel['emoji']} {panel_dir(panel) + '/':<14}"
            f" {len(members):>2} 条 · {panel['tagline']}{rep_text}"
        )
    lines += [
        "│",
        "└─ ⚙ 生成管线：scripts/panels.json（单一真值）→ library_index.py",
        "              → README / INDEX.md / index/* / 站点 nav",
        "```",
    ]
    return "\n".join(lines)



def render_highlights_block(cfg: dict, mapping: dict, entries: list) -> str:
    """精选入口由 panels.json 驱动，不将推荐等同于事实已全面验收。"""
    by_dir = {entry_dir(d["path"]): d for d in entries}
    lines = ["| 阅读入口 | 报告内容 |", "| :-- | :-- |"]
    for rel in cfg.get("highlights", []):
        doc = by_dir.get(rel)
        if doc is None:
            continue
        panel = mapping.get(doc["path"], {})
        title = doc["title"].replace("|", r"\|")
        lines.append(
            f"| **[{entry_short_name(doc)}](<{doc['path']}>)**"
            f"<br><sub>{panel.get('title', '')}</sub> | {title} |"
        )
    return "\n".join(lines)



def render_panels_block(cfg: dict, mapping: dict, entries: list, label_limit: int = 12) -> str:
    """GitHub 安全 HTML 卡片：只用语义元素，无样式属性和外部脚本。"""
    from html import escape

    by_panel = {}
    by_dir = {entry_dir(d["path"]): d for d in entries}
    for doc in entries:
        panel = mapping.get(doc["path"])
        if panel is not None:
            by_panel.setdefault(panel["id"], []).append(doc)
    captions = {
        "models": "模型系列", "llm": "语言模型方法", "agents": "智能体系统",
        "aigc": "AIGC",
        "worldmodel": "世界模型与具身", "ai4science": "科学研究应用",
        "evaluation": "跨领域评测科学",
        "infra": "训练与推理系统", "opensource": "开源代码深读",
    }
    cards = []
    for number, panel in enumerate(cfg["panels"], 1):
        top = panel_dir(panel)
        display_title = panel["title"]
        members = by_panel.get(panel["id"], [])
        reps = [
            f'<a href="{rel}/report.md">{escape(entry_short_name(by_dir[rel]))}</a>'
            for rel in panel.get("representatives", [])
        ]
        cards.append(
            f'<td width="33%" valign="top">\n'
            f'<h3>{number:02d} · <a href="{top}/README.md">{display_title}</a></h3>\n'
            f'<p><strong>{captions.get(panel["id"], display_title)}</strong>'
            f'<br><sub>{len(members)} 篇主报告 · {panel["tagline"]}</sub></p>\n'
            f'<p>{" · ".join(reps)}</p>\n'
            f'<p><a href="{top}/README.md"><strong>浏览板块 →</strong></a></p>\n'
            f'</td>'
        )
    lines = ["<table>"]
    for i in range(0, len(cards), 3):
        lines += ["<tr>", *cards[i:i + 3], "</tr>"]
    lines.append("</table>")
    return "\n".join(lines)



def render_topics_block(entries: list, mapping: dict, panels: list) -> str:
    """按板块列入口报告，并链接自动汇总的子专题索引。"""
    lines = ["| 方向 | 专题入口 |", "| :-- | :-- |"]
    for panel in panels:
        if not panel.get("topic_index", False):
            continue
        members = sort_panel_entries(
            (d for d in entries if mapping.get(d["path"], {}).get("id") == panel["id"]),
            panel,
        )
        links = " · ".join(f"[{entry_short_name(d)}](<{d['path']}>)" for d in members)
        lines.append(f"| **{panel['title']}** | {links} |")
    child_topics = sum(
        1 for entry in entries for child in entry.get("children", [])
        if "topics" in child["path"].split("/")
    )
    if child_topics:
        lines.append(
            f"| **分析分册** | [查看 {child_topics} 篇专题内分析](<index/by-topic.md>) |"
        )
    return "\n".join(lines)



def render_recent_block(rows: list, mapping: dict) -> str:
    lines = ["| 日期 | 阅读条目 | 板块 |", "| :-- | :-- | :-- |"]
    for row in rows:
        doc = row["doc"]
        panel = mapping.get(doc["path"])
        lines.append(
            f"| {row['date']} | [{entry_short_name(doc)}](<{doc['path']}>) | "
            f"{panel['title'] if panel else '—'} |"
        )
    return "\n".join(lines)


def render_index_block(entries: list, mapping: dict, panels: list) -> str:
    """README 的「完整索引」区块：**只放摘要 + 链接**，不逐行复制条目。

    单一真值在 `index/by-report.md`（含「条目 | 板块 | 路径」三列核心视图），
    README 里再抄一份只会带来两处不一致。
    """
    counts = {p["id"]: sum(1 for v in mapping.values() if v["id"] == p["id"]) for p in panels}
    summary = " · ".join(f"{p['title']} {counts[p['id']]}" for p in panels)
    return "\n".join([
        f"共 **{len(entries)}** 条，分属 **{len(panels)}** 个板块：{summary}。",
        f"完整 {len(entries)} 行（条目 | 板块 | 路径）见 "
        f"**[index/by-report.md](<{GENERATED_DIR}/by-report.md>)**；"
        f"按域 / 主题 / 来源分面见 [index/](<{GENERATED_DIR}/>)，总目录见 [INDEX.md](<{GENERATED_TOP}>)。",
    ])


def render_readme_blocks(cfg: dict, entries: list, stats: dict, mapping: dict,
                         repo_root: str, today: _dt.date) -> dict:
    topic_ids = {p["id"] for p in cfg["panels"] if p.get("topic_index", False)}
    topics = sum(1 for d in entries if mapping.get(d["path"], {}).get("id") in topic_ids)
    # 「更新日期」徽章取最后一次提交日，而非当天 wall-clock：跨零点不漂，任意一天重跑字节一致。
    badge_date = last_commit_date(repo_root, today)
    return {
        "badges": render_badges(stats, topics, badge_date, len(cfg["panels"])),
        "structure": render_structure_block(cfg, mapping, entries),
        "panels": render_panels_block(cfg, mapping, entries),
        "highlights": render_highlights_block(cfg, mapping, entries),
        "topics": render_topics_block(entries, mapping, cfg["panels"]),
        "recent": render_recent_block(recent_rows(repo_root, entries, cfg), mapping),
        "index": render_index_block(entries, mapping, cfg["panels"]),
    }


def update_readme(repo_root: str, blocks: dict) -> tuple:
    """在根 `README.md` 里幂等替换 SCRIPT 区块。

    只动 ``<!-- SCRIPT:<name> START -->`` 与 ``<!-- SCRIPT:<name> END -->`` 之间的
    内容；``<!-- STATIC -->`` 文案与标记本身逐字节保留。返回 (path, changed, missing)。
    """
    path = os.path.join(repo_root, README_FILE)
    if not os.path.isfile(path):
        return path, False, list(README_BLOCKS)

    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()

    missing = [name for name in README_BLOCKS if not block_pattern(name).search(text)]
    if missing:
        return path, False, missing

    original = text
    for name in README_BLOCKS:
        body = blocks[name]
        pattern = block_pattern(name)

        def _sub(match, body=body):
            return f"{match.group(1)}\n{body}\n{match.group(3)}"

        text = pattern.sub(_sub, text, count=1)

    if text == original:
        return path, False, []  # 已是最新：不写盘、不触碰 mtime
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path, True, []


# --------------------------------------------------------------------------
# 板块 README（每个板块目录一份，模板在脚本里，配置由 panels.json 驱动）
# --------------------------------------------------------------------------

PANEL_README_NAME = "README.md"
PANEL_README_BLOCK = "panel-readme"
PANEL_ONE_LINERS = {
    "Models": "厂商模型 / 系列逐个精读，按公司与模型家族归档。",
    "LLM": "语言模型能力与技术专题，覆盖推理、对齐、Agent、RAG 等方向。",
    "Agents": "建议按“系统闭环 → 电脑中的长程任务 → 安全与授权”阅读：先理解决策、状态和工具反馈，再看真实环境执行与信任边界。",
    "AIGC": "图像、视频、音频、3D、数字人生成及相关架构与编辑方法。",
    "WorldModel": "世界模型与具身 VLA，关注环境动力学与可部署动作策略。",
    "AI4Science": "科学问题中的 AI 方法与实验闭环，按具体领域和证据链深入。",
    "Evaluation": "跨领域研究 AI 评测的构念效度、数据污染、评分可靠性与真实任务外推。",
    "Infra": "推理 / 训练基础设施，覆盖投机解码、量化边缘与训练基建。",
    "OpenSource": "开源仓库代码深读，源码不入口、只留报告与证据引用。",
}


def render_panel_readme(panel: dict, members: list, repo_root: str) -> str:
    """单个板块 README：统一卡头 + 徽章 + 条目表 + 子文档折叠。

    卡头的 ``<div>`` 带 ``markdown="1"``：GitHub 与 MkDocs（md_in_html）都会
    正确渲染其中的 Markdown（不带时 MkDocs 会把整块当原始 HTML）。
    """
    directory = panel_dir(panel)
    top = panel["title"]
    names = sort_panel_entries(members, panel)
    one_liner = PANEL_ONE_LINERS.get(directory, panel["tagline"])
    lines = [
        '<div align="center" markdown="1">',
        '',
        f'# {panel["emoji"]} {top}',
        '',
        f'**{len(names)} 条** · {one_liner}',
        '',
        f'[← 返回首页](<../README.md>) · [完整索引](<../INDEX.md>)',
        '',
        '</div>',
        '',
        '<!-- SCRIPT:panel-readme START · 由 scripts/library_index.py 生成，勿手改 -->',
        '',
        f'![Entries](https://img.shields.io/badge/Entries-{len(names)}-3f51b5?style=flat-square)',
        f'![Panel](https://img.shields.io/badge/Panel-{top}-9e9e9e?style=flat-square)',
        '',
    ]
    topic_children = [
        (entry, child) for entry in names for child in entry.get("children", [])
        if "topics" in child["path"].split("/")
    ]
    if topic_children:
        lines += ["## 专题内分析", "", "| 所属报告 | 分册入口 |", "| --- | --- |"]
        for entry, child in sorted(topic_children, key=lambda pair: pair[1]["path"]):
            rel = os.path.relpath(child["path"], directory).replace(os.sep, "/")
            lines.append(
                f'| {entry_short_name(entry)} | '
                f'{link_label(rel, "", child["title"] or child["filename"])} |'
            )
        lines += ["", '[查看研究专题与分析分册](<../index/by-topic.md>)', "", "## 主报告", ""]
    lines += [
        '| 条目 | 报告 | 规模 |',
        '| :-- | :-- | --: |',
    ]
    for doc in names:
        label = entry_short_name(doc)
        rel = os.path.relpath(doc["path"], directory).replace(os.sep, "/")
        lines.append(
            f'| **{label}** | [{doc["title"] or label}](<{rel}>) '
            f'| {doc["lines"]:,} 行 |'
        )
    lines.append('')
    with_children = [d for d in names if d.get("children")]
    if with_children:
        lines.append('## 📎 子文档')
        lines.append('')
        for doc in with_children:
            label = entry_short_name(doc)
            lines.append('<details>')
            lines.append(f'<summary><b>{label}</b>（{len(doc["children"])} 份）</summary>')
            lines.append('')
            for child in doc["children"]:
                crel = os.path.relpath(child["path"], top).replace(os.sep, "/")
                clabel = os.path.relpath(child["path"], entry_dir(doc["path"])).replace(os.sep, "/")
                lines.append(f'* [{clabel}](<{crel}>) — {child["lines"]:,} 行 / {child["bytes"]:,} B')
            lines.append('')
            lines.append('</details>')
            lines.append('')
    lines += [
        '<!-- SCRIPT:panel-readme END -->',
        '',
        '---',
        '',
        '<sub>本 README 由 `scripts/library_index.py` 自动生成（`scripts/panels.json` 驱动）；'
        '完整索引见 [INDEX.md](<../INDEX.md>) 与 [index/](<../index/>)。</sub>',
        '',
    ]
    return '\n'.join(lines)


def write_panel_readmes(repo_root: str, cfg: dict, mapping: dict, docs: list) -> list:
    """为每个板块目录生成/更新 README.md；返回写入路径列表。"""
    entries = [d for d in docs if d["is_entry"]]
    written = []
    for panel in cfg["panels"]:
        top = panel_dir(panel)
        members = [d for d in entries if mapping.get(d["path"], {}).get("id") == panel["id"]]
        text = render_panel_readme(panel, members, repo_root)
        path = os.path.join(repo_root, top, PANEL_README_NAME)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        old = open(path, encoding="utf-8").read() if os.path.isfile(path) else None
        if old != text:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text if text.endswith("\n") else text + "\n")
        written.append(path)
    return written


# --------------------------------------------------------------------------
# 输出
# --------------------------------------------------------------------------

def baseline_lines(stats: dict, out_root: str, dry_run: bool) -> list:
    e, d = stats["entries"], stats["documents"]
    return [
        f"条目总数（{ENTRY_BASENAME}）     : {e['total']}",
        f"条目子文档数               : {e['children']}",
        f"条目正文行数（去 FM）      : {e['lines']}",
        f"条目字节                   : {e['bytes']}",
        f"带 front-matter 的条目数   : {e['with_front_matter']}",
        f"文档总数（除生成物的 .md） : {d['md_total']}",
        f"其中 README.md             : {d['named_readme_md']}",
        f"其中 report.md             : {d['named_report_md']}",
        f"纳入版本控制的文件数       : {stats['version_control']['tracked_total']}",
        f"纳入版本控制的 .md         : {stats['version_control']['tracked_md']}",
        f"输出根目录                 : {out_root}",
        f"模式                       : {'dry-run（不写盘）' if dry_run else 'write'}",
    ]


def write_outputs(out_root: str, index_text: str, facets: dict, stats: dict | None) -> list:
    written = []
    os.makedirs(out_root, exist_ok=True)
    # 折叠索引中的缩进空行没有语义，避免新增条目产生行尾空白。
    index_text = re.sub(r"(?m)^[ \t]+$", "", index_text)
    index_path = os.path.join(out_root, GENERATED_TOP)
    with open(index_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(index_text if index_text.endswith("\n") else index_text + "\n")
    written.append(index_path)

    index_dir = os.path.join(out_root, GENERATED_DIR)
    os.makedirs(index_dir, exist_ok=True)
    for name in sorted(facets):
        path = os.path.join(index_dir, f"{name}.md")
        text = facets[name]
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text if text.endswith("\n") else text + "\n")
        written.append(path)

    if stats is not None:
        path = os.path.join(out_root, STATS_FILE)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(stats, fh, ensure_ascii=False, indent=2, sort_keys=False)
            fh.write("\n")
        written.append(path)
    return written


def verify_links(written: list) -> list:
    """自检：文件里的仓库内相对链接是否都指向真实存在的路径（文件或目录）。

    同时识别 ``](<path>)`` 与 ``](path)`` 两种写法；``scheme://``（含
    ``file://``）、``mailto:``、纯锚点一律跳过 —— 它们不是仓库内相对路径。
    链接按 URL 解码后再判定，因此百分号编码（GitHub 可解析）不会被误报。
    """
    offenders = []
    pattern = re.compile(r"\]\(<([^>]+)>\)|\]\(([^)\s]+)\)")
    for path in written:
        if not path.endswith(".md"):
            continue
        base = os.path.dirname(os.path.abspath(path))
        with open(path, "r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                for angle, plain in pattern.findall(line):
                    target = (angle or plain).strip()
                    if "://" in target or target.startswith("#") or target.startswith("mailto:"):
                        continue
                    target = target.split("#")[0]
                    if not target:
                        continue
                    resolved = os.path.normpath(
                        os.path.join(base, urllib.parse.unquote(target)))
                    if not os.path.exists(resolved):
                        offenders.append(f"{path}:{lineno} -> {target}")
    return offenders


# --------------------------------------------------------------------------
# 站点渲染层（MkDocs）：staging 镜像 + 门户首页 + nav 区块
#
# 站点是仓库 Markdown 的**只读渲染层**，不产生第二套内容源：
# * ``site-docs/`` 是内容文件的逐字节镜像（生成物，不入库，CI 里重建）；
# * 门户首页 ``site-docs/index.md`` 由本段生成（panels.json 驱动）；
# * ``mkdocs.yml`` 的 nav 区块由本段幂等替换（``# SCRIPT:nav START/END``）。
# --------------------------------------------------------------------------

MKDOCS_FILE = "mkdocs.yml"
SITE_NAV_BLOCK = "nav"
SITE_HOME_NAME = "README.md"
#: 门户首页占用 staging 根的 ``README.md`` 槽位：MkDocs 把 README.md 当目录
#: index 页（正好落在 ``/``），且不与同样 index 化的 ``INDEX.md`` 撞车
#: （实测：同目录 index.md 与 INDEX.md 会被当成同一个 index 而丢弃其一）。
#: 仓库根 README.md 不镜像（见 SITE_STAGE_DROP），指向它的链接自然落到门户首页。

#: staging 时跳过的顶层项（比扫描更宽：站点不渲染脚本与构建配置自身）。
#: ``assets/`` 不跳过：站点样式表 ``assets/site.css`` 需要镜像进 staging
#: （``extra_css`` 要求文件位于 docs_dir 内）；``scripts/`` 不跳过：
#: 生成物与 docs/ 里有指向 ``scripts/library_index.py``、``panels.json`` 的
#: 链接，镜像进去站点侧才能 0 失效（.py/.json 作为静态文件拷贝）。
SITE_STAGE_SKIP_TOPS = frozenset(
    {SITE_DOCS_DIR, SITE_BUILD_DIR, "__pycache__"}
)

#: staging 里额外跳过的文件名（操作系统 / 版本控制噪音）。
SITE_STAGE_SKIP_FILES = frozenset({".DS_Store"})

#: 根 README.md 不镜像：MkDocs 会把 README.md 当作目录 index 页，与站点门户
#: 首页 index.md 争抢 ``/``。指向它的链接由 mkdocs_hooks 改写为 ``index.md``。
SITE_STAGE_DROP = frozenset({"README.md"})

#: 站点「索引」导航区收录的 index/ 分面（顺序即展示顺序）。
SITE_INDEX_FACETS = (
    ("by-report", "按条目平铺"),
    ("by-topic", "按专题"),
    ("by-domain", "按领域"),
    ("by-subject", "按主题"),
    ("by-repo", "按来源"),
    ("recent", "最近更新"),
    ("stale", "待复核"),
)


def _yaml_dq(text: str) -> str:
    """YAML 双引号标量（JSON 字符串是 YAML 双引号标量的合法子集）。"""
    return json.dumps(str(text), ensure_ascii=False)


def _site_nav_entry_lines(entries: list, mapping: dict, panel: dict) -> list:
    """单个板块的 nav 行：板块 README 作 section index，条目按配置或路径排序，
    带子文档的条目折叠为二级分组（总报告在前，子文档按路径排序）。"""
    members = sort_panel_entries(
        [d for d in entries
         if mapping.get(d["path"], {}).get("id") == panel["id"]],
        panel,
    )
    top = panel_dir(panel)
    if panel["title"] == top:
        lines = [f"    - {_yaml_dq(top + '/README.md')}"]
    else:
        lines = [f"    - {_yaml_dq(panel['title'])}: {_yaml_dq(top + '/README.md')}"]
    for doc in members:
        label = entry_short_name(doc)
        children = [c for c in doc.get("children", [])
                    if c["filename"].lower() != PANEL_README_NAME.lower()]
        if not children:
            lines.append(f"    - {_yaml_dq(label)}: {_yaml_dq(doc['path'])}")
            continue
        lines.append(f"    - {_yaml_dq(label)}:")
        lines.append(f"        - {_yaml_dq('总报告')}: {_yaml_dq(doc['path'])}")
        for child in sorted(children, key=lambda c: c["path"]):
            stem = os.path.splitext(os.path.basename(child["path"]))[0]
            lines.append(f"        - {_yaml_dq(stem)}: {_yaml_dq(child['path'])}")
    return lines


def render_site_nav(cfg: dict, mapping: dict, docs: list, orphans: list) -> str:
    """生成 ``mkdocs.yml`` nav 区块的内容（2 空格缩进起，供幂等替换）。"""
    entries = [d for d in docs if d["is_entry"]]
    lines = [f"  - {_yaml_dq('首页')}: {_yaml_dq(SITE_HOME_NAME)}"]
    lines.append(
        f"  - {_yaml_dq('研究专题')}: "
        f"{_yaml_dq(GENERATED_DIR + '/by-topic.md')}"
    )
    for panel in cfg["panels"]:
        members = [d for d in entries
                   if mapping.get(d["path"], {}).get("id") == panel["id"]]
        title = f"{panel['emoji']} {panel['title']} · {len(members)}"
        lines.append(f"  - {_yaml_dq(title)}:")
        lines.extend(_site_nav_entry_lines(entries, mapping, panel))
        lines.extend(_site_nav_orphan_lines(orphans, panel_dir(panel)))

    # 索引区（生成物，作为站点内容渲染）
    lines.append(f"  - {_yaml_dq('📇 索引')}:")
    lines.append(f"      - {_yaml_dq('完整索引')}: {_yaml_dq(GENERATED_TOP)}")
    for name, title in SITE_INDEX_FACETS:
        lines.append(f"      - {_yaml_dq(title)}: {_yaml_dq(GENERATED_DIR + '/' + name + '.md')}")

    # 文档区（docs/*.md + scripts/*.md，按路径排序，标题取 front-matter/H1）
    meta_docs = sorted((d for d in docs
                        if d["top"] in ("docs", "scripts")
                        and not d["is_generated"] and not d["is_entry"]),
                       key=lambda d: d["path"])
    if meta_docs:
        lines.append(f"  - {_yaml_dq('📖 文档')}:")
        for doc in meta_docs:
            lines.append(f"      - {_yaml_dq(doc['title'])}: {_yaml_dq(doc['path'])}")
    # 外部互链：站点 ↔ 仓库（外链 nav 项，MkDocs 原生支持）
    lines.append(f"  - {_yaml_dq('🐙 GitHub 仓库')}: {_yaml_dq(REPO_URL)}")
    return "\n".join(lines)


def _site_nav_orphan_lines(orphans: list, top: str) -> list:
    """板块目录下游离文档（不属于任何条目，如进行中的 mini-swe-agent）的 nav 行。

    按二级目录分组；组内 README.md 作 section index 置前，其余按路径排序。
    """
    groups = {}
    for d in orphans:
        if d["top"] != top:
            continue
        _top, second, _deeper, _fn = split_path(d["path"])
        if not second:
            continue  # 板块根的 README.md 已在条目行里作为 section index
        groups.setdefault(second, []).append(d)
    lines = []
    for key in sorted(groups):
        members = sorted(groups[key],
                         key=lambda d: (d["filename"].lower() != PANEL_README_NAME.lower(),
                                        d["path"]))
        lines.append(f"    - {_yaml_dq(key)}:")
        for d in members:
            if d["filename"].lower() == PANEL_README_NAME.lower():
                lines.append(f"        - {_yaml_dq(d['path'])}")
            else:
                stem = os.path.splitext(d["filename"])[0]
                lines.append(f"        - {_yaml_dq(stem)}: {_yaml_dq(d['path'])}")
    return lines


def update_mkdocs_nav(repo_root: str, nav_body: str) -> tuple:
    """幂等替换 ``mkdocs.yml`` 里 ``# SCRIPT:nav START/END`` 之间的 nav 区块。

    与 update_readme 同口径：标记本身与标记外内容逐字节保留；
    已是最新则不写盘。返回 (path, changed, ok)。
    """
    path = os.path.join(repo_root, MKDOCS_FILE)
    if not os.path.isfile(path):
        return path, False, False
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    pattern = re.compile(
        r"(?ms)^([ \t]*#[ \t]*SCRIPT:" + SITE_NAV_BLOCK + r"[ \t]+START[^\n]*\n)"
        r".*?"
        r"^([ \t]*#[ \t]*SCRIPT:" + SITE_NAV_BLOCK + r"[ \t]+END[^\n]*)$"
    )
    if not pattern.search(text):
        return path, False, False
    new_text = pattern.sub(lambda m: f"{m.group(1)}{nav_body}\n{m.group(2)}",
                           text, count=1)
    if new_text == text:
        return path, False, True
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(new_text)
    return path, True, True


def _site_home_icon(panel_id: str) -> str:
    """首页专用的小型线性图标；内联矢量，离线与浅深色均可使用。"""
    paths = {
        "models": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
        "llm": '<path d="M5 4h14a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-6 4V6a2 2 0 0 1 2-2Z"/><path d="M7 9h10M7 13h6"/>',
        "agents": '<rect x="5" y="7" width="14" height="13" rx="4"/><path d="M12 3v4m-3 6h.01M15 13h.01M9 17h6"/><path d="M5 11H3m18 0h-2"/>',
        "aigc": '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1.5"/><path d="m3 17 5-5 4 4 4-6 5 7"/>',
        "worldmodel": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5h14M5 17.5h14"/>',
        "ai4science": '<path d="M9 3h6m-5 0v7l-4.5 8.2A1.5 1.5 0 0 0 6 20.5h12a1.5 1.5 0 0 0 1.5-2.3L15 10V3"/><path d="M7 15h10"/>',
        "evaluation": '<path d="M4 20h16M6 16V9m4 7V4m4 12v-5m4 5V7"/><path d="M4 4h2M18 4h2"/>',
        "infra": '<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M9 2v5m6-5v5M9 17v5m6-5v5M2 9h5m-5 6h5m10-6h5m-5 6h5"/><path d="M10 10h4v4h-4z"/>',
        "opensource": '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18"/>',
    }
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">' + paths.get(panel_id, paths["models"]) + '</svg>')


def render_site_home(cfg: dict, mapping: dict, entries: list,
                     recent: list, stats: dict) -> str:
    """研究图书馆门户；只改变展示，统计与条目归类仍使用原有扫描结果。"""
    from html import escape

    by_panel = {}
    by_dir = {entry_dir(d["path"]): d for d in entries}
    for doc in entries:
        panel = mapping.get(doc["path"])
        if panel is not None:
            by_panel.setdefault(panel["id"], []).append(doc)
    topic_ids = {p["id"] for p in cfg["panels"] if p.get("topic_index", False)}
    topics_entries = [d for d in entries
                      if mapping.get(d["path"], {}).get("id") in topic_ids]
    child_count = stats.get("entries", {}).get(
        "children", sum(len(d.get("children", [])) for d in entries))
    captions = {
        "models": "模型系列", "llm": "语言模型技术", "agents": "智能体系统",
        "aigc": "AIGC",
        "worldmodel": "世界模型与具身", "ai4science": "科学研究应用",
        "evaluation": "跨领域评测科学",
        "infra": "训练与推理系统", "opensource": "开源代码研究",
    }

    def label(value):
        # 标签来自文档题名；保持 Markdown 链接结构完整。
        return str(value).replace("\n", " ").replace("[", r"\[").replace("]", r"\]")

    lines = [
        "---", "hide:", "  - toc", "  - navigation", "---", "",
        f"<!-- {GENERATED_NOTE}（门户展示层；条目与统计同源） -->", "",
        '<div class="rr-home" markdown="1">', "",
        '<div class="rr-hero" markdown="1">', "",
        '<div class="rr-hero-copy" markdown="1">', "",
        '<p class="rr-eyebrow">RESEARCHREPORT · OPEN RESEARCH LIBRARY</p>', "",
        '# AI 论文与技术报告精读', "",
        '<p class="rr-intro">读懂研究问题与方法机制，按需追踪开源实现</p>', "",
        '<div class="rr-hero-links" markdown="1">', "",
        f'[浏览完整索引](<{GENERATED_TOP}>){{ .rr-button .rr-button-primary }}', "",
        f'[在 GitHub 阅读 ↗]({REPO_URL}){{ .rr-button .rr-button-secondary }}', "",
        '</div>', "", '</div>', "",
        '<div class="rr-stats" aria-label="图书馆内容统计">',
        f'<div><strong>{len(entries):02d}</strong><span>研究条目</span></div>',
        f'<div><strong>{child_count:02d}</strong><span>分册与子文档</span></div>',
        f'<div><strong>{len(cfg["panels"]):02d}</strong><span>研究板块</span></div>',
        '</div>', "", '</div>', "",
        '<div class="rr-discovery" markdown="1">', "",
        '<label for="__search" class="rr-search-launch"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg><span>搜索模型、论文或技术问题</span><kbd>/</kbd></label>', "",
        '<div class="rr-quicklinks" markdown="1">', "",
        f'[研究专题索引](<{GENERATED_DIR}/by-topic.md>) · '
        f'[查看最近更新](<{GENERATED_DIR}/recent.md>) · '
        f'[阅读与证据说明](<docs/research-method.md>)', "",
        '</div>', "", '</div>', "",
        '<section class="rr-section rr-collections" markdown="1">', "",
        '<div class="rr-section-heading" markdown="1">', "",
        '## 研究板块', "",
        '<span>从一个方向开始，连接相关方法与实现。</span>', "",
        '</div>', "", '<div class="rr-panel-grid" markdown="1">', "",
    ]
    for number, panel in enumerate(cfg["panels"], 1):
        members = by_panel.get(panel["id"], [])
        title = panel["title"]
        reps = []
        for rel in panel.get("representatives", []):
            if rel in by_dir:
                doc = by_dir[rel]
                reps.append(f'[{label(entry_short_name(doc))}](<{doc["path"]}>)')
        lines += [
            f'<div class="rr-panel rr-panel-{escape(panel["id"], quote=True)}" markdown="1">', "",
            '<div class="rr-panel-meta">'
            f'<span class="rr-panel-icon">{_site_home_icon(panel["id"])}</span>'
            f'<span class="rr-panel-number">{number:02d} / {len(members):02d} 条目</span></div>', "",
            f'### [{captions.get(panel["id"], label(title))}](<{panel_dir(panel)}/README.md>){{ .rr-panel-link }}', "",
            f'<p class="rr-panel-english">{escape(title)}</p>', "",
            f'<p class="rr-panel-description">{escape(panel["tagline"])}</p>', "",
            '<div class="rr-panel-reps" markdown="1">', "",
            ' · '.join(reps), "", '</div>', "",
            '<span class="rr-panel-arrow" aria-hidden="true">↗</span>', "", '</div>', "",
        ]
    lines += ['</div>', "", '</section>', "",
              '<div class="rr-reading-grid" markdown="1">', "",
              '<section class="rr-section rr-start" markdown="1">', "",
              '<div class="rr-section-heading" markdown="1">', "",
              '## 从这里开始', "", '<span>从入口报告建立研究坐标。</span>', "",
              '</div>', "", '<div class="rr-reading-list" markdown="1">', ""]
    for rel in cfg.get("highlights", []):
        doc = by_dir.get(rel)
        if doc is None:
            continue
        panel = mapping.get(doc["path"], {})
        lines += [
            '<div class="rr-reading-item" markdown="1">', "",
            f'<span class="rr-reading-category">{escape(panel.get("title", "研究"))}</span>', "",
            f'[{label(entry_short_name(doc))}](<{doc["path"]}>){{ .rr-reading-title }}', "",
            f'<p>{escape(doc["title"])}</p>', "", '</div>', "",
        ]
    lines += ['</div>', "", '</section>', "",
              '<section class="rr-section rr-recent" markdown="1">', "",
              '<div class="rr-section-heading" markdown="1">', "",
              '## 最近更新', "", f'[全部更新 →](<{GENERATED_DIR}/recent.md>)', "",
              '</div>', "", '<div class="rr-recent-list" markdown="1">', ""]
    for row in recent:
        doc = row["doc"]
        panel = mapping.get(doc["path"], {})
        lines += [
            '<div class="rr-recent-item" markdown="1">', "",
            f'<time datetime="{escape(row["date"], quote=True)}">{escape(row["date"])}</time>', "",
            f'[{label(entry_short_name(doc))}](<{doc["path"]}>){{ .rr-recent-title }}', "",
            f'<span class="rr-recent-category">{escape(panel.get("title", "研究"))}</span>', "",
            '</div>', "",
        ]
    if not recent:
        lines += ['暂时没有可用的更新日期，可从完整索引开始阅读。', ""]
    lines += ['</div>', "",
              '<p class="rr-recent-note">日期优先采用条目标注，缺失时回退至最近提交日。</p>', "",
              '</section>', "", '</div>', ""]
    if topics_entries:
        lines += ['<section class="rr-section rr-topics" markdown="1">', "",
                  '<div class="rr-section-heading" markdown="1">', "",
                  '## 研究专题', "",
                  f'<span>{len(topics_entries)} 个研究专题，选择感兴趣的方向开始阅读。</span>', "",
                  '</div>', "", '<div class="rr-topic-links" markdown="1">', ""]
        def _topic_sort_key(doc):
            panel = mapping.get(doc["path"], {})
            directory = entry_dir(doc["path"])
            order = panel.get("entry_order", [])
            rank = order.index(directory) if directory in order else len(order)
            return (directory.split("/", 1)[0], rank, doc["path"])

        for doc in sorted(topics_entries, key=_topic_sort_key):
            lines += [f'[{label(entry_short_name(doc))}](<{doc["path"]}>){{ .rr-topic }}', ""]
        lines += ['</div>', "", '</section>', ""]
    lines += ['<div class="rr-library-footer" markdown="1">', "",
              'ResearchReport · 让结论有出处，让阅读有路径。', "",
              f'[完整索引](<{GENERATED_TOP}>) · [所有报告](<{GENERATED_DIR}/by-report.md>) · [待复核内容](<{GENERATED_DIR}/stale.md>)', "",
              '</div>', "", '</div>', ""]
    return "\n".join(lines)


def _site_dir_link_targets(target: str) -> list:
    """扫描 staging 内 `.md` 的相对**目录**链接（``](dir/)`` / ``](dir)``），
    返回需要补 hub 索引页的目录（staging 相对路径，排序去重）。

    判定口径与 verify_links 一致：``](<...>)`` 与 ``](...)`` 两种写法、URL 解码、
    跳过 scheme/mailto/纯锚点。
    """
    pattern = re.compile(r"\]\(<([^>]+)>\)|\]\(([^)\s]+)\)")
    needed = set()
    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            if not name.lower().endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            base = os.path.dirname(path)
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    for angle, plain in pattern.findall(line):
                        t = (angle or plain).strip()
                        if "://" in t or t.startswith("#") or t.startswith("mailto:"):
                            continue
                        t = urllib.parse.unquote(t.split("#")[0]).rstrip("/")
                        if not t:
                            continue
                        resolved = os.path.normpath(os.path.join(base, t))
                        if os.path.isdir(resolved):
                            needed.add(
                                os.path.relpath(resolved, target).replace(os.sep, "/"))
    return sorted(needed)


def render_dir_hub(rel_dir: str, docs_by_path: dict, target: str) -> str:
    """目录 hub 索引页（staging 专属生成物）：列出该目录直接子 `.md`，
    供「目录链接」在站点上落脚（GitHub 上目录链接打开目录页，站点上打开 hub）。"""
    abs_dir = os.path.join(target, rel_dir)
    label = rel_dir.rstrip("/").rsplit("/", 1)[-1] or rel_dir
    lines = [
        f"<!-- {GENERATED_NOTE}（站点目录 hub，位于 {SITE_DOCS_DIR}/，不入库） -->",
        "",
        f"# 🗂 {label}",
        "",
    ]
    for name in sorted(os.listdir(abs_dir)):
        if not name.lower().endswith(".md") \
                or name in (SITE_HOME_NAME, "index.md"):
            continue
        rel = f"{rel_dir}/{name}" if rel_dir else name
        doc = docs_by_path.get(rel)
        title = (doc["title"] if doc else "") or os.path.splitext(name)[0]
        lines.append(f"- [{title}](<{name}>)")
    lines.append("")
    return "\n".join(lines)


def stage_site_docs(repo_root: str, cfg: dict, mapping: dict, docs: list,
                    stats: dict, recent: list) -> list:
    """把站点需要的内容镜像到 ``site-docs/`` 并写入门户首页。

    全量重建（先删后写）：staging 是本脚本的自留地，逐字节可复现；
    条目源文件只读。返回写入的文件数与 staging 目录路径。
    """
    target = os.path.join(repo_root, SITE_DOCS_DIR)
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target, exist_ok=True)

    count = 0
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = sorted(
            d for d in dirnames
            if not d.startswith(".")
            and os.path.relpath(os.path.join(dirpath, d), repo_root).replace(os.sep, "/")
                not in SITE_STAGE_SKIP_TOPS
        )
        for name in sorted(filenames):
            if name.startswith(".") or name in SITE_STAGE_SKIP_FILES \
                    or name.endswith(".pyc"):
                continue
            src = os.path.join(dirpath, name)
            rel = os.path.relpath(src, repo_root).replace(os.sep, "/")
            if rel in SITE_STAGE_DROP:
                continue
            dst = os.path.join(target, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            count += 1

    # 目录链接的落脚页：仓库里有 ](docs/)、](papers) 这类「目录链接」（GitHub 上
    # 打开目录页）；站点侧为每个被链接的目录生成一个 hub 索引页，
    # 构建钩子（mkdocs_hooks）再把目录链接改写到该 hub。
    docs_by_path = {d["path"]: d for d in docs}
    for rel_dir in _site_dir_link_targets(target):
        hub = render_dir_hub(rel_dir, docs_by_path, target)
        hub_path = os.path.join(target, rel_dir, "index.md")
        with open(hub_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(hub if hub.endswith("\n") else hub + "\n")
        count += 1

    home = render_site_home(cfg, mapping, [d for d in docs if d["is_entry"]],
                            recent, stats)
    with open(os.path.join(target, SITE_HOME_NAME), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(home if home.endswith("\n") else home + "\n")
    count += 1
    return count, target


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="library_index.py",
        description="Research 仓库图书馆化：只读扫描 .md，按条目（report.md）生成 INDEX.md 与 index/*。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python3 scripts/library_index.py --repo-root . --dry-run\n"
            "  python3 scripts/library_index.py --repo-root . --out-root . --write-stats --check-links\n"
        ),
    )
    parser.add_argument("--repo-root", default=".", help="仓库根目录（只读扫描起点），默认当前目录")
    parser.add_argument("--out-root", default=None, help="输出根目录，默认等于 --repo-root")
    parser.add_argument("--dry-run", action="store_true", help="只打印统计，不写任何文件")
    parser.add_argument("--write-stats", action="store_true",
                        help=f"额外产出机器可读统计 {STATS_FILE}（供 docs/statistics.md 等引用）")
    parser.add_argument("--recent-limit", type=int, default=20, help="recent.md 保留条数，默认 20")
    parser.add_argument("--stale-days", type=int, default=180, help="stale 判定天数阈值，默认 180")
    parser.add_argument("--today", default=None, help="覆盖「今天」（YYYY-MM-DD），钉住可复现输出")
    parser.add_argument("--include-generated", action="store_true",
                        help="把生成物（INDEX.md、index/*）也纳入扫描（默认排除，保证可复现）")
    parser.add_argument("--check-links", action="store_true", help="写盘后校验生成文件内的相对链接")
    parser.add_argument("--skip-site", action="store_true",
                        help="跳过站点渲染层（site-docs/ staging + mkdocs.yml nav + 门户首页）")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    global PANEL_TOPS, LIBRARIES

    repo_root = os.path.abspath(args.repo_root)
    out_root = os.path.abspath(args.out_root) if args.out_root else repo_root

    if not os.path.isdir(repo_root):
        print(f"[ERROR] --repo-root 不是目录: {repo_root}", file=sys.stderr)
        return 2

    try:
        today = _dt.date.fromisoformat(args.today) if args.today else _dt.date.today()
    except ValueError:
        print(f"[ERROR] --today 需要 YYYY-MM-DD 格式: {args.today}", file=sys.stderr)
        return 2

    try:
        cfg = load_panels(repo_root)
        PANEL_TOPS = panel_top_dirs(cfg)
        LIBRARIES = PANEL_TOPS
    except ConfigError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 3

    skipped_paths = []
    docs, orphans = attach_children(
        scan(repo_root, today, args.include_generated, skipped_out=skipped_paths))
    entries = [d for d in docs if d["is_entry"]]
    stats = build_stats(repo_root, docs)

    mapping, problems = validate_panels(entries, cfg, repo_root)
    unassigned, duplicated, missing = problems
    if unassigned or duplicated or missing:
        print("[FAIL] 板块校验未通过（明细见上），未生成任何文件。", file=sys.stderr)
        return 3

    facets = render_facets(entries, display_root(repo_root, out_root), args.dry_run, args, mapping)
    index_text = render_index(docs, orphans, stats, display_root(repo_root, out_root),
                              args.dry_run, cfg, mapping)
    readme_blocks = render_readme_blocks(cfg, entries, stats, mapping, repo_root, today)
    readme_path = os.path.join(repo_root, README_FILE)

    print("library_index.py —— Research 仓库图书馆化索引")
    print("=" * 60)
    for line in baseline_lines(stats, out_root, args.dry_run):
        print(line)
    print(f"板块（{PANELS_FILE}）        : "
          + " · ".join(f"{p['title']}={sum(1 for v in mapping.values() if v['id'] == p['id'])}"
                       for p in cfg["panels"]))
    print(f"最近更新口径               : front-matter date → 缺失时回退 `{cfg['date_fallback']}`"
          f"（取 {cfg['recent_limit']} 条）")
    print(f"最近提交日期               : `git log -1 --format=%cs`"
          f" = {last_commit_date(repo_root, today).isoformat()}（日期回退以版本记录为准）")
    # 跳过要可见：若将来真有该编目的目录被误跳，一眼可见，而不是「index 里莫名少条目」。
    uniq_skipped = sorted(set(skipped_paths))
    preview = "、".join(uniq_skipped[:5]) + ("…" if len(uniq_skipped) > 5 else "")
    print(f"skipped                    : {len(uniq_skipped)}"
          + (f"（{preview}）" if uniq_skipped else "（无）"))
    print("=" * 60)

    if args.dry_run:
        print(f"[dry-run] 将生成：{os.path.join(out_root, GENERATED_TOP)}")
        for name in sorted(facets):
            print(f"[dry-run] 将生成：{os.path.join(out_root, GENERATED_DIR, name + '.md')}")
        if args.write_stats:
            print(f"[dry-run] 将生成：{os.path.join(out_root, STATS_FILE)}")
        print(f"[dry-run] 将更新：{os.path.relpath(readme_path, repo_root)}"
              f"（区块：{', '.join(README_BLOCKS)}）")
        if not args.skip_site:
            print(f"[dry-run] 将重建：{SITE_DOCS_DIR}/（站点 staging + 门户首页）")
            print(f"[dry-run] 将更新：{MKDOCS_FILE}（区块：{SITE_NAV_BLOCK}）")
        print("[dry-run] 未写入任何文件；未修改任何条目文件。")
        return 0

    written = write_outputs(out_root, index_text, facets, stats if args.write_stats else None)
    print(f"[ok] 已写入 {len(written)} 个文件（条目文件保持原样，未删除、未改写）：")
    for path in written:
        print(f"     {os.path.relpath(path, repo_root)}")

    panel_readme_paths = write_panel_readmes(repo_root, cfg, mapping, docs)
    print(f"[ok] 板块 README：{len(panel_readme_paths)} 份（{', '.join(os.path.relpath(q, repo_root) for q in panel_readme_paths)}）")

    path, changed, missing = update_readme(repo_root, readme_blocks)
    if missing:
        print(f"[skip] {README_FILE} 未更新（缺少 SCRIPT 标记：{', '.join(missing)}）")
    else:
        print(f"[ok] {'已更新' if changed else '已是最新'}：{os.path.relpath(path, repo_root)}"
              f"（区块：{', '.join(README_BLOCKS)}）")

    if not args.skip_site:
        staged, site_dir = stage_site_docs(
            repo_root, cfg, mapping, docs, stats,
            recent_rows(repo_root, entries, cfg))
        print(f"[ok] 站点 staging：{os.path.relpath(site_dir, repo_root)}/"
              f"（镜像 {staged} 个文件，含门户首页 {SITE_HOME_NAME}）")
        nav_path, nav_changed, nav_ok = update_mkdocs_nav(
            repo_root, render_site_nav(cfg, mapping, docs, orphans))
        if not nav_ok:
            print(f"[skip] {MKDOCS_FILE} 未更新（缺少 SCRIPT:{SITE_NAV_BLOCK} 标记）")
        else:
            print(f"[ok] {'已更新' if nav_changed else '已是最新'}：{MKDOCS_FILE} 的 nav 区块")

    if args.check_links:
        targets = list(written)
        if os.path.isfile(readme_path):
            targets.append(readme_path)
        targets.extend(q for q in panel_readme_paths if os.path.isfile(q))
        offenders = verify_links(targets)
        if offenders:
            print("[FAIL] 存在悬挂的相对链接：", file=sys.stderr)
            for item in offenders:
                print(f"       {item}", file=sys.stderr)
            return 1
        print(f"[ok] {len(targets)} 个文件内的相对链接全部可解析。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
