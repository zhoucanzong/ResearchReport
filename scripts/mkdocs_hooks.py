# -*- coding: utf-8 -*-
"""mkdocs_hooks.py —— 站点构建钩子：让 MkDocs 渲染与 GitHub 口径完全一致。

站点是「只读渲染层」，源文件一个字符不改；两处口径差异由本钩子在构建期抹平：

1. **锚点 slugify**：`report.md` 的页内目录按 GitHub slugger 写死
   （小写、去标点、空格转连字符、CJK 保留），Python-Markdown 默认会把中文
   剥光导致锚点 404。`on_config` 把 toc 扩展的 slugify 换成 GitHub 口径。

2. **链接改写**（`on_page_markdown`，只改构建期的内存副本）：
   指向**目录**的链接（GitHub 上打开目录页）→ 该目录的 hub 索引页
   `index.md`（hub 由 library_index.py 的 staging 器生成）。
   指向根 `README.md` 的链接无需改写：门户首页正好占用 staging 根的
   `README.md` 槽位（仓库的 README.md 不镜像，避免与门户首页抢 `/`）。
"""

from __future__ import annotations

import os
import re
import urllib.parse
import hashlib

# GitHub slugger 保留：Unicode 字母/数字（\w 含 CJK）、下划线、连字符、空格；
# 其余（标点、符号、箭头 →、全角括号等）一律删除。
_GH_STRIP = re.compile(r"[^\w\- ]+", re.UNICODE)

# ](<path>) 与 ](path) 两种写法
_LINK = re.compile(r"\]\(<([^>]+)>\)|\]\(([^)\s]+)\)")


def github_slugify(value, separator="-"):
    """对齐 GitHub slugger：小写 → 去标点符号 → 空格转连字符。

    与 GitHub 的差异仅在极端 case（组合字符 Mn、重复标题去重后缀
    `_1` vs `-1`），本仓库语料不涉及。
    """
    slug = _GH_STRIP.sub("", str(value).lower())
    return slug.replace(" ", separator)


def on_config(config):
    """把 GitHub 口径的 slugify 注入 toc 扩展配置。"""
    mdx_configs = config.setdefault("mdx_configs", {})
    toc = mdx_configs.setdefault("toc", {})
    toc["slugify"] = github_slugify
    # CSS 与门户 HTML 同步更新；浏览器可缓存旧的无版本 URL，导致新布局失去样式。
    # 只给自己的静态样式添加内容指纹，不改第三方或远程资源。
    css_path = os.path.join(config["docs_dir"], "assets", "site.css")
    if os.path.isfile(css_path):
        with open(css_path, "rb") as source:
            version = hashlib.sha256(source.read()).hexdigest()[:12]
        config["extra_css"] = [
            f"assets/site.css?v={version}"
            if str(item).split("?", 1)[0] == "assets/site.css" else item
            for item in config.get("extra_css", [])
        ]
    return config


def _rewrite_target(target: str, page_dir: str, docs_dir: str) -> str:
    """计算链接目标的改写结果；不需要改写时返回原样字符串。"""
    if "://" in target or target.startswith("#") or target.startswith("mailto:"):
        return target
    anchor = ""
    core = target
    if "#" in core:
        core, anchor = core.split("#", 1)
        anchor = "#" + anchor
    decoded = urllib.parse.unquote(core)
    if not decoded:
        return target
    resolved = os.path.normpath(os.path.join(page_dir, decoded))

    # 目录链接 → hub 索引页（staging 器已为被链接目录生成 index.md）
    if os.path.isdir(resolved) and os.path.isfile(os.path.join(resolved, "index.md")):
        sep = "" if core.endswith("/") else "/"
        return f"{core}{sep}index.md{anchor}"

    return target


def on_page_markdown(markdown, page, config, files):
    """构建期改写本页 Markdown 里的链接（源文件不动）。"""
    docs_dir = config["docs_dir"]
    page_dir = os.path.dirname(os.path.join(docs_dir, page.file.src_path))

    def _sub(match):
        angle, plain = match.group(1), match.group(2)
        target = angle if angle is not None else plain
        new = _rewrite_target(target, page_dir, docs_dir)
        if new == target:
            return match.group(0)
        return f"](<{new}>)" if angle is not None else f"]({new})"

    return _LINK.sub(_sub, markdown)
