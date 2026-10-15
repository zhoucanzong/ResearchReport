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
* **front-matter**：当前 0 份。索引与统计必须在无元数据时优雅退化（显示 `—`）。

## 设计原则

1. **只加不改**：本脚本对条目文件是纯只读的，绝不删除、移动、重命名或改写它们。
   唯一的写行为是把 `INDEX.md`、`index/*.md`、`index/stats.json` 写到 ``--out-root``。
2. **可复现**：给定相同的仓库状态，输出逐字节一致（`--today` 用于钉住日期）。
3. **零第三方依赖**：有 PyYAML 就用它解析 front-matter，没有就退回内置逐行解析器。
4. **行数口径**：`lines`（剔除 front-matter）与 `lines_raw`（文件原始行数）都产出。

用法::

    python3 scripts/library_index.py --repo-root . --dry-run
    python3 scripts/library_index.py --repo-root . --out-root . --write-stats --check-links
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys

# --------------------------------------------------------------------------
# 常量 / 契约
# --------------------------------------------------------------------------

SCHEMA_VERSION = 2

#: front-matter 元数据键（缺 pyyaml 时逐行解析这套键）。
KNOWN_KEYS = (
    "title",
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
    "by-topic": "按专题（topic）",
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

ACTIVE_STATUSES = ("active", "current", "ok", "stable", "published")

#: 资料库（含 `report.md` 条目的顶层目录）。顺序即展示顺序。
LIBRARIES = ("AIGC-Research", "LLM-Research", "Repo-Research")


def category_of(rel_path: str) -> str:
    """条目分类：ModelSeries / TechnicalTopics / 其它（按目录名原样）。"""
    parts = [p for p in rel_path.replace(os.sep, "/").split("/") if p]
    for i, part in enumerate(parts):
        if part in ("ModelSeries", "TechnicalTopics"):
            return part
    return "Other"


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

def iter_markdown(repo_root: str, include_generated: bool = False):
    """只读遍历 ``**/*.md``，返回排序后的仓库相对路径。

    跳过隐藏目录（`.git` 等）；默认排除本脚本的生成物，保证「跑一次脚本数字不变」。
    """
    root = os.path.abspath(repo_root)
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
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


def scan(repo_root: str, today: _dt.date, include_generated: bool = False) -> list:
    return [build_doc(repo_root, rel, today) for rel in iter_markdown(repo_root, include_generated)]


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
               if not d["is_entry"] and d["top"] in LIBRARIES and not d.get("parent_dir")]
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
                for cat in ("ModelSeries", "TechnicalTopics", "Other")
            },
            "dirs_by_category": {
                cat: len({entry_dir(e["path"]) for e in this_entries if e["category"] == cat})
                for cat in ("ModelSeries", "TechnicalTopics", "Other")
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
    tracked_libraries = [p for p in tracked if p.split("/")[0] in LIBRARIES]

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
        "du": {
            "worktree_including_git": du_sk(repo_root),
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
                    for cat in ("ModelSeries", "TechnicalTopics", "Other")
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
    """条目的展示名：用所属专题目录名（对 report.md 更可读）。"""
    return os.path.basename(entry_dir(doc["path"])) or doc["filename"]


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


def render_index(docs: list, orphans: list, stats: dict, out_root: str, dry_run: bool) -> str:
    entries = [d for d in docs if d["is_entry"]]
    counts = stats["entries"]
    dc = stats["documents"]

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
        "",
        "## 按库入口",
        "",
        "| 资料库 | 条目数 | 文档（`.md`） | 条目行数 | 条目字节 | 入口 |",
        "| --- | --: | --: | --: | --: | --- |",
    ]
    for lib in LIBRARIES:
        lib_stats = stats["libraries"][lib]
        lines.append(
            f"| {lib} | {lib_stats['entries']} | {lib_stats['documents_md']} | "
            f"{lib_stats['lines']:,} | {lib_stats['bytes']:,} B | "
            f"[#{lib}](#{lib.lower()}) |"
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
    lines += ["## 条目索引（按库折叠，可直达条目与子报告）", ""]
    for lib in LIBRARIES:
        lib_entries = sorted([d for d in entries if d["top"] == lib], key=lambda d: d["path"])
        lib_stats = stats["libraries"][lib]
        lines += [
            f"### {lib}（{len(lib_entries)} 条目 / {lib_stats['documents_md']} 文档）",
            "",
        ]
        for cat in ("ModelSeries", "TechnicalTopics", "Other"):
            cat_entries = [d for d in lib_entries if d["category"] == cat]
            if not cat_entries:
                continue
            child_total = sum(len(d["children"]) for d in cat_entries)
            cat_cn = {"ModelSeries": "模型系列", "TechnicalTopics": "技术专题", "Other": "其它"}[cat]
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
            "| 文档 | 所属库 | 行数 | 字节 |",
            "| --- | --- | --: | --: |",
        ]
        for doc in sorted(orphans, key=lambda d: d["path"]):
            lines.append(
                f"| {link(doc['path'], '')} | {doc['top']} | {doc['lines']:,} | {doc['bytes']:,} B |"
            )
        lines.append("")

    # 非资料库条目（根目录等）
    other_entries = [d for d in entries if d["top"] not in LIBRARIES]
    if other_entries:
        lines += ["### 其它位置条目", ""]
        for doc in other_entries:
            lines += render_entry_block(doc, "")
    lines.append("")

    lines += [
        "## 说明",
        "",
        "* 本索引是**派生数据**，仓库里的条目文件才是唯一事实来源；重建索引只需重跑脚本。",
        "* 当前 front-matter 为 0 份：所有条目的 `type` / `date` / `status` 显示为 `—`，"
        "domain / subject / topic 由路径推断。补齐 front-matter 后重跑即可自动填充。",
        f"* 键位契约：`{'` / `'.join(KNOWN_KEYS[:7])}`（另容忍可选 `topic`）。",
        "* 脚本只读扫描、只写生成物；**不会删除或改写任何条目文件**。",
        "",
    ]
    return "\n".join(lines)


def render_by_report(entries: list, out_root: str, dry_run: bool) -> str:
    lines = header(FACET_TITLES["by-report"], out_root, dry_run)
    lines += [
        f"共 **{len(entries)}** 个条目（`{ENTRY_BASENAME}`）。「行数」为正文行数，已剔除 front-matter。",
        "",
        "| 条目 | 所属库 | 路径 | 子报告数 | 行数 | 日期 |",
        "| --- | --- | --- | --: | --: | --- |",
    ]
    for doc in sorted(entries, key=lambda d: d["path"]):
        lines.append(
            "| {label} | {lib} | {path} | {kids} | {lines} | {date} |".format(
                label=entry_label(doc),
                lib=doc["top"] or ROOT_GROUP,
                path=link(doc["path"], "../"),
                kids=len(doc["children"]),
                lines=f"{doc['lines']:,}",
                date=doc["date_iso"] or "—",
            )
        )
    total_children = sum(len(d["children"]) for d in entries)
    total_lines = sum(d["lines"] for d in entries)
    lines += [
        f"| **合计** | — | **{len(entries)} 条目** | **{total_children}** | **{total_lines:,}** | — |",
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
        lines += ["| 条目 | date | 所属库 | 专题 |", "| --- | --- | --- | --- |"]
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
    if status and status not in ACTIVE_STATUSES:
        reasons.append(f"status={entry['status']}")
    if entry["date_valid"] and entry["age_days"] is not None and entry["age_days"] > stale_days:
        reasons.append(f"date={entry['date_iso']}（{entry['age_days']} 天前）")
    return reasons


def render_stale(entries: list, out_root: str, dry_run: bool, stale_days: int) -> str:
    lines = header(FACET_TITLES["stale"], out_root, dry_run)
    lines += [
        "判定口径：`status` 不是 active/current/ok/stable/published，或 `date` 早于 "
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


def render_facets(entries: list, out_root: str, dry_run: bool, args) -> dict:
    return {
        "by-domain": "\n".join(header(FACET_TITLES["by-domain"], out_root, dry_run)
                               + group_table(entries, lambda e: e["domain"])),
        "by-subject": "\n".join(header(FACET_TITLES["by-subject"], out_root, dry_run)
                                + group_table(entries, lambda e: e["subject"])),
        "by-repo": render_by_repo(entries, out_root, dry_run),
        "by-topic": "\n".join(header(FACET_TITLES["by-topic"], out_root, dry_run)
                              + group_table(entries, lambda e: e["topic"] or UNFILED)),
        "by-report": render_by_report(entries, out_root, dry_run),
        "recent": render_recent(entries, out_root, dry_run, args.recent_limit),
        "stale": render_stale(entries, out_root, dry_run, args.stale_days),
    }


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
    """自检：生成文件里的相对链接是否都指向真实存在的文件。"""
    offenders = []
    pattern = re.compile(r"\]\(<([^>]+)>\)")
    for path in written:
        if not path.endswith(".md"):
            continue
        base = os.path.dirname(os.path.abspath(path))
        with open(path, "r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                for target in pattern.findall(line):
                    if "://" in target or target.startswith("#"):
                        continue
                    if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                        offenders.append(f"{path}:{lineno} -> {target}")
    return offenders


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
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

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

    docs, orphans = attach_children(scan(repo_root, today, args.include_generated))
    entries = [d for d in docs if d["is_entry"]]
    stats = build_stats(repo_root, docs)

    facets = render_facets(entries, display_root(repo_root, out_root), args.dry_run, args)
    index_text = render_index(docs, orphans, stats, display_root(repo_root, out_root), args.dry_run)

    print("library_index.py —— Research 仓库图书馆化索引")
    print("=" * 60)
    for line in baseline_lines(stats, out_root, args.dry_run):
        print(line)
    print("=" * 60)

    if args.dry_run:
        print(f"[dry-run] 将生成：{os.path.join(out_root, GENERATED_TOP)}")
        for name in sorted(facets):
            print(f"[dry-run] 将生成：{os.path.join(out_root, GENERATED_DIR, name + '.md')}")
        if args.write_stats:
            print(f"[dry-run] 将生成：{os.path.join(out_root, STATS_FILE)}")
        print("[dry-run] 未写入任何文件；未修改任何条目文件。")
        return 0

    written = write_outputs(out_root, index_text, facets, stats if args.write_stats else None)
    print(f"[ok] 已写入 {len(written)} 个文件（条目文件保持原样，未删除、未改写）：")
    for path in written:
        print(f"     {os.path.relpath(path, repo_root)}")

    if args.check_links:
        offenders = verify_links(written)
        if offenders:
            print("[FAIL] 生成文件内存在悬挂相对链接：", file=sys.stderr)
            for item in offenders:
                print(f"       {item}", file=sys.stderr)
            return 1
        print("[ok] 生成文件内的相对链接全部可解析。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
