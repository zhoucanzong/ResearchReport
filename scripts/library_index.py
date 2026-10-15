#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""library_index.py —— Research 仓库图书馆化：只读索引生成器。

本脚本是 Research 仓库「图书馆化」第 ① 步的落地工具：把仓库里已有的
Markdown 文档当作图书馆条目（entry）扫一遍，产出一份目录（INDEX.md）和
若干分面索引（index/*.md）。

设计原则（重要）：

1. **只加不改**：脚本对仓库是纯只读的。它只遍历 ``**/*.md``、读取内容，
   绝不删除、移动、重命名或改写任何条目文件。它唯一的写入行为是把
   ``INDEX.md`` 与 ``index/`` 下的派生索引写到 ``--out-root``。
2. **可以安全地反复运行**：输出近似纯函数（给定相同的仓库状态与 --today，输出逐字节相同）。
3. **零第三方依赖**：有 PyYAML 就用它解析 front-matter；没有就用内置的
   逐行解析器（见 ``parse_front_matter_fallback``），两条路径产出同一套键。
4. **没 front-matter 也能跑**：当前仓库 71 份 .md 全部没有 front-matter，
   脚本会退回按路径推断（domain/subject/topic），并把这些条目计入
   ``unfiled``，让「待补元数据」的工作量显式可见。

生成的文件都带「脚本生成、勿手改」头部。

用法::

    python3 scripts/library_index.py --repo-root . --dry-run   # 只报告，不写盘
    python3 scripts/library_index.py --repo-root .             # 生成 INDEX.md + index/
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import sys

# --------------------------------------------------------------------------
# 常量 / 契约
# --------------------------------------------------------------------------

SCHEMA_VERSION = 1

#: 允许在 front-matter 里出现的元数据键（缺 pyyaml 时逐行解析这套键）。
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
    "recent": "最近更新（按 date 降序）",
    "stale": "陈旧 / 待复核（status 或超期）",
}

GENERATED_NOTE = "本文件由 scripts/library_index.py 自动生成，请勿手改。"
DRY_RUN_NOTE = "（dry-run 产物，未写盘）"

#: 路径推断用的占位值：用来把「元数据缺口」显式暴露出来，而不是假装分组成功。
UNFILED = "unfiled"
ROOT_GROUP = "repository-root"

ACTIVE_STATUSES = ("active", "current", "ok", "stable", "published")


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

    覆盖 :data:`KNOWN_KEYS` 里的键，并容忍：

    * 行内注释（``key: value  # 注释``）
    * YAML 内联列表（``key: [a, b]``）
    * 折行列表（``key:`` 之后紧跟 ``  - a`` / ``  - b``）
    * 引号包裹的标量

    只按行内**第一个** ``:`` 切分，因此 ``upstream: https://...`` 这类含冒号的
    值不会被截断。
    """
    fm: dict = {}
    pending_list_key = None

    for raw_line in text.split("\n"):
        if not raw_line.strip():
            continue
        stripped = raw_line.strip()

        if stripped.startswith("#"):
            continue

        # 折行列表项： "- value" 归队到上一个形如 "key:" 的键
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

        # 去掉行尾注释（仅当注释前有空格，避免误伤 URL 里的 #）
        value = re.sub(r"\s+#.*$", "", value).strip()

        if key not in KNOWN_KEYS:
            pending_list_key = None
            continue

        if value == "":
            fm[key] = []          # 可能是折行列表，也可能是空值
            pending_list_key = key
            continue

        pending_list_key = None
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            fm[key] = [_coerce(p) for p in inner.split(",") if p.strip()] if inner else []
        else:
            fm[key] = _coerce(value)

    return fm


def parse_front_matter(text: str) -> dict:
    """解析文档开头的 YAML front-matter（``---`` 围栏），返回扁平字典。

    有 PyYAML 时优先用 PyYAML；缺失、解析失败或结果不是字典时退回
    :func:`parse_front_matter_fallback`。没有 front-matter 时返回 ``{}``。
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}

    body = []
    closed = False
    for line in lines[1:]:
        if line.strip() == "---":
            closed = True
            break
        body.append(line)
    if not closed:
        # 没有闭合围栏 —— 视为没有 front-matter
        return {}

    block = "\n".join(body)

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
# 路径推断
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


def to_list(value) -> list:
    """把 front-matter 的值统一成字符串列表。"""
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


# --------------------------------------------------------------------------
# 扫描（只读）
# --------------------------------------------------------------------------

def iter_markdown(repo_root: str):
    """只读遍历 ``**/*.md``，产出排序后的仓库相对路径。跳过隐藏目录（如 .git）。"""
    root = os.path.abspath(repo_root)
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            if name.lower().endswith(".md"):
                abs_path = os.path.join(dirpath, name)
                rel = os.path.relpath(abs_path, root)
                found.append(rel.replace(os.sep, "/"))
    return sorted(found)


def build_entry(repo_root: str, rel_path: str, today: _dt.date) -> dict:
    """读取单个文件，产出索引条目（纯读取，不写回）。"""
    with open(os.path.join(repo_root, rel_path), "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    fm = parse_front_matter(text)
    top, second, deeper, filename = split_path(rel_path)

    domain = to_str(fm.get("domain")) or top or UNFILED
    subject = to_str(fm.get("subject")) or second or UNFILED
    # topic 三级兜底：front-matter > 更深目录 > subject
    topic = to_str(fm.get("topic"))
    if not topic:
        topic = "/".join(deeper) if deeper else subject

    upstream = to_list(fm.get("upstream"))
    title = to_str(fm.get("title")) or heading(text) or filename

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
        "title": title,
        "type": to_str(fm.get("type")),
        "domain": domain,
        "subject": subject,
        "topic": topic,
        "upstream": upstream,
        "date": date_raw,
        "date_iso": date_iso,
        "date_valid": date_valid,
        "age_days": age_days,
        "evidence": to_list(fm.get("evidence")),
        "status": to_str(fm.get("status")),
        "has_front_matter": bool(fm),
        "fm_keys": sorted(fm.keys()),
        "top": top,
    }


def scan(repo_root: str, today: _dt.date) -> list:
    return [build_entry(repo_root, rel, today) for rel in iter_markdown(repo_root)]


# --------------------------------------------------------------------------
# 渲染
# --------------------------------------------------------------------------

def header(title: str, out_root: str, dry_run: bool) -> list:
    lines = [f"# {title}", "", f"> {GENERATED_NOTE}"]
    if dry_run:
        lines.append(f"> {DRY_RUN_NOTE}")
    lines += [
        "> 生成命令：`python3 scripts/library_index.py --repo-root .`",
        f"> 输出根目录：`{out_root}`",
        "",
        "---",
        "",
    ]
    return lines


def link(rel_path: str, prefix: str) -> str:
    target = f"{prefix}{rel_path}" if prefix else rel_path
    # 用尖括号包裹，避免空格/括号/非 ASCII 文件名破坏 Markdown 链接
    label = rel_path.replace("|", "\\|")
    return f"[{label}](<{target}>)"


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


def render_index(entries: list, out_root: str, counts: dict, dry_run: bool) -> str:
    lines = header("Research 仓库图书馆索引", out_root, dry_run)

    lines += [
        "## 统计总览",
        "",
        "| 指标 | 数量 |",
        "| --- | --- |",
        f"| 条目总数（`**/*.md`） | {counts['total']} |",
        f"| 带 front-matter | {counts['with_front_matter']} |",
        f"| 无 front-matter（归入 `{UNFILED}`，待补元数据） | {counts['without_front_matter']} |",
        f"| 文件名 = report.md | {counts['report_md']} |",
        f"| 文件名 = README.md | {counts['readme_md']} |",
        f"| report.md + README.md 合计 | {counts['report_readme_total']} |",
        f"| 有合法 date | {counts['dated']} |",
        f"| 标记为陈旧 / 超期 | {counts['stale']} |",
        "",
        "## 分面索引",
        "",
        "| 分面 | 说明 |",
        "| --- | --- |",
    ]
    for name, title in FACET_TITLES.items():
        lines.append(f"| [index/{name}.md](<index/{name}.md>) | {title} |")
    lines.append("")

    lines += ["## 全部条目", ""]
    lines += [
        "| 条目 | domain | subject | topic | type | date | status |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in sorted(entries, key=lambda e: e["path"]):
        lines.append(
            "| {link} | {domain} | {subject} | {topic} | {type} | {date} | {status} |".format(
                link=link(entry["path"], ""),
                domain=entry["domain"],
                subject=entry["subject"],
                topic=entry["topic"] or "—",
                type=entry["type"] or "—",
                date=entry["date_iso"] or "—",
                status=entry["status"] or "—",
            )
        )
    lines.append("")

    lines += [
        "## 说明",
        "",
        "* 本索引是**派生数据**，仓库里的条目文件才是唯一事实来源；重建索引只需重跑脚本。",
        "* 条目没有任何元数据时，脚本退回按路径推断 domain/subject/topic，并归入 "
        f"`{UNFILED}`，以便暴露「待补 front-matter」的工作量。",
        "* 键位契约：`title/type/domain/subject/upstream/date/evidence/status`（另容忍可选 `topic`）。",
        "* 脚本只读扫描、只写本索引；不会删除或改写任何条目文件。",
        "",
    ]
    return "\n".join(lines)


def render_by_repo(entries: list, out_root: str, dry_run: bool) -> str:
    lines = header(FACET_TITLES["by-repo"], out_root, dry_run)
    groups: dict = {}
    for entry in entries:
        if entry["upstream"]:
            keys = entry["upstream"]
        elif entry["top"]:
            keys = [entry["top"]]
        else:
            keys = [ROOT_GROUP]
        for key in keys or [ROOT_GROUP]:
            groups.setdefault(str(key), []).append(entry)

    for name in sorted(groups, key=lambda s: (s in (UNFILED, ROOT_GROUP), str(s))):
        members = sorted(groups[name], key=lambda e: e["path"])
        lines += [f"## {name} ({len(members)})", ""]
        for entry in members:
            lines.append(f"* {link(entry['path'], '../')}")
        lines.append("")
    return "\n".join(lines)


def render_recent(entries: list, out_root: str, dry_run: bool, limit: int) -> str:
    lines = header(FACET_TITLES["recent"], out_root, dry_run)
    dated = sorted(
        [e for e in entries if e["date_valid"]],
        key=lambda e: (e["date_iso"], e["path"]),
        reverse=True,
    )
    undated = sorted([e for e in entries if not e["date_valid"]], key=lambda e: e["path"])

    lines += [f"## 最近 {limit} 条（按 date 降序）", ""]
    if dated:
        lines += ["| 条目 | date | domain | subject |", "| --- | --- | --- | --- |"]
        for entry in dated[:limit]:
            lines.append(
                f"| {link(entry['path'], '../')} | {entry['date_iso']} | {entry['domain']} | {entry['subject']} |"
            )
    else:
        lines.append("_本仓库当前没有任何条目带合法 `date` 元数据。_")
    lines.append("")

    lines += [f"## 无 date 元数据（{len(undated)}）", ""]
    if undated:
        lines.append("以下条目缺少可解析的 `date`，无法参与「最近更新」排序：")
        lines.append("")
        for entry in undated:
            lines.append(f"* {link(entry['path'], '../')}")
    else:
        lines.append("_无。_")
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

    flagged = []
    no_meta = []
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
        "by-domain": "\n".join(
            header(FACET_TITLES["by-domain"], out_root, dry_run)
            + group_table(entries, lambda e: e["domain"])
        ),
        "by-subject": "\n".join(
            header(FACET_TITLES["by-subject"], out_root, dry_run)
            + group_table(entries, lambda e: e["subject"])
        ),
        "by-repo": render_by_repo(entries, out_root, dry_run),
        "by-topic": "\n".join(
            header(FACET_TITLES["by-topic"], out_root, dry_run)
            + group_table(entries, lambda e: e["topic"] or UNFILED)
        ),
        "recent": render_recent(entries, out_root, dry_run, args.recent_limit),
        "stale": render_stale(entries, out_root, dry_run, args.stale_days),
    }


def compute_counts(entries: list, stale_days: int) -> dict:
    total = len(entries)
    with_fm = sum(1 for e in entries if e["has_front_matter"])
    report_md = sum(1 for e in entries if e["filename"].lower() == "report.md")
    readme_md = sum(1 for e in entries if e["filename"].lower() == "readme.md")
    return {
        "total": total,
        "with_front_matter": with_fm,
        "without_front_matter": total - with_fm,
        "report_md": report_md,
        "readme_md": readme_md,
        "report_readme_total": report_md + readme_md,
        "dated": sum(1 for e in entries if e["date_valid"]),
        "stale": sum(1 for e in entries if stale_reasons(e, stale_days)),
    }


# --------------------------------------------------------------------------
# 输出
# --------------------------------------------------------------------------

def baseline_lines(counts: dict, out_root: str, dry_run: bool) -> list:
    return [
        f"扫描到的 .md 总数          : {counts['total']}",
        f"带 front-matter 的条目数   : {counts['with_front_matter']}",
        f"无 front-matter（unfiled） : {counts['without_front_matter']}",
        f"文件名 report.md 的份数    : {counts['report_md']}",
        f"文件名 README.md 的份数    : {counts['readme_md']}",
        f"report.md + README.md 合计 : {counts['report_readme_total']}",
        f"带合法 date 的条目数       : {counts['dated']}",
        f"判定为陈旧/超期的条目数    : {counts['stale']}",
        f"输出根目录                 : {out_root}",
        f"模式                       : {'dry-run（不写盘）' if dry_run else 'write'}",
    ]


def write_outputs(out_root: str, index_text: str, facets: dict) -> list:
    written = []
    os.makedirs(out_root, exist_ok=True)
    index_path = os.path.join(out_root, "INDEX.md")
    with open(index_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(index_text if index_text.endswith("\n") else index_text + "\n")
    written.append(index_path)

    index_dir = os.path.join(out_root, "index")
    os.makedirs(index_dir, exist_ok=True)
    for name in sorted(facets):
        path = os.path.join(index_dir, f"{name}.md")
        text = facets[name]
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text if text.endswith("\n") else text + "\n")
        written.append(path)
    return written


def verify_links(written: list) -> list:
    """自检：确认生成文件里的相对链接都指向真实存在的文件。"""
    offenders = []
    pattern = re.compile(r"\]\(<([^>]+)>\)")
    for path in written:
        base = os.path.dirname(os.path.abspath(path))
        with open(path, "r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                for target in pattern.findall(line):
                    if "://" in target or target.startswith("#"):
                        continue
                    resolved = os.path.normpath(os.path.join(base, target))
                    if not os.path.exists(resolved):
                        offenders.append(f"{path}:{lineno} -> {target}")
    return offenders


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="library_index.py",
        description="Research 仓库图书馆化：只读扫描 **/*.md 并生成 INDEX.md 与 index/*.md。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python3 scripts/library_index.py --repo-root . --dry-run\n"
            "  python3 scripts/library_index.py --repo-root . --out-root .\n"
        ),
    )
    parser.add_argument("--repo-root", default=".", help="仓库根目录（只读扫描起点），默认当前目录")
    parser.add_argument("--out-root", default=None, help="输出根目录，默认等于 --repo-root")
    parser.add_argument("--dry-run", action="store_true", help="只打印报告与统计，不写任何文件")
    parser.add_argument("--recent-limit", type=int, default=20, help="recent.md 保留条数，默认 20")
    parser.add_argument("--stale-days", type=int, default=180, help="stale 判定天数阈值，默认 180")
    parser.add_argument("--today", default=None, help="覆盖「今天」（YYYY-MM-DD），便于可复现输出")
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

    entries = scan(repo_root, today)
    counts = compute_counts(entries, args.stale_days)
    facets = render_facets(entries, out_root, args.dry_run, args)
    index_text = render_index(entries, out_root, counts, args.dry_run)

    print("library_index.py —— Research 仓库图书馆化索引")
    print("=" * 56)
    for line in baseline_lines(counts, out_root, args.dry_run):
        print(line)
    print("=" * 56)

    if args.dry_run:
        print(f"[dry-run] 将生成：{os.path.join(out_root, 'INDEX.md')}")
        for name in sorted(facets):
            print(f"[dry-run] 将生成：{os.path.join(out_root, 'index', name + '.md')}")
        print("[dry-run] 未写入任何文件；未修改任何条目文件。")
        return 0

    written = write_outputs(out_root, index_text, facets)
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
