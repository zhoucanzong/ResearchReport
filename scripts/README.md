# scripts/

本目录存放维护 Research 仓库的辅助脚本。目前只有一个：`library_index.py`。

这些脚本遵循「**只加不改**」原则：**只读取**仓库里的条目文件，**绝不**删除、
移动、重命名或改写它们。

---

## library_index.py

把仓库里的 Markdown 文档当作图书馆条目（entry）扫描一遍，生成一份总目录
`INDEX.md` 和若干分面索引 `index/*.md`。这是仓库「图书馆化」第 ① 步的落地工具。

### 用法

```bash
# 1) 只读预演：打印统计与「将生成什么」，一个字都不写盘
python3 scripts/library_index.py --repo-root . --dry-run

# 2) 正式生成：写出 INDEX.md 与 index/*.md
python3 scripts/library_index.py --repo-root . --out-root .

# 3) 生成并自检：校验生成文件内的相对链接是否都能解析
python3 scripts/library_index.py --repo-root . --out-root . --check-links
```

### 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--repo-root` | `.` | 仓库根目录，只读扫描的起点 |
| `--out-root` | 同 `--repo-root` | 索引输出根目录 |
| `--dry-run` | 关 | 只打印统计，不写任何文件 |
| `--recent-limit` | `20` | `index/recent.md` 保留条数 |
| `--stale-days` | `180` | `index/stale.md` 的「超期」天数阈值 |
| `--today` | 运行当天 | 覆盖「今天」（`YYYY-MM-DD`），便于产出可复现 |
| `--check-links` | 关 | 写盘后校验生成文件内的相对链接 |

### 产出

| 文件 | 内容 |
| --- | --- |
| `INDEX.md` | 统计总览 + 分面索引入口 + 全部条目清单 |
| `index/by-domain.md` | 按领域（`domain`）分组 |
| `index/by-subject.md` | 按主题（`subject`）分组 |
| `index/by-repo.md` | 按来源仓库（`upstream`，缺省时退回本地一级目录）分组 |
| `index/by-topic.md` | 按专题（`topic`）分组 |
| `index/recent.md` | 按 `date` 降序的最近条目 |
| `index/stale.md` | `status` 非 active 或 `date` 超期的待复核条目 |

所有生成文件都带「本文件由 scripts/library_index.py 自动生成，请勿手改」头部。

### front-matter 契约

脚本读取文档开头的 YAML front-matter（`---` 围栏），识别这些键：

`title` / `type` / `domain` / `subject` / `upstream` / `date` / `evidence` / `status`
（另容忍可选 `topic`）。其中 `upstream`、`evidence` 支持标量、内联列表 `[a, b]`
和折行列表三种写法。

**零第三方依赖**：装了 PyYAML 就用 PyYAML 解析；没装则自动退回内置的逐行
解析器（`parse_front_matter_fallback`），两条路径产出同一套键、同一套值。

**没有 front-matter 也能跑**：条目没有任何元数据时，脚本按路径推断
`domain`（一级目录）/ `subject`（二级目录）/ `topic`（更深目录），标题退回
取正文第一个标题，并把该条目归入 `unfiled` 分组——这样「待补多少元数据」
是可见的，而不是被静默吞掉。

### 只读基线实测数字

在提交 `scripts/library_index.py` 时，对本仓库跑
`python3 scripts/library_index.py --repo-root . --dry-run` 的实测结果：

| 指标 | 实测值 |
| --- | --- |
| 扫描到的 `.md` 总数 | **71** |
| 带 front-matter 的条目数 | **0** |
| 无 front-matter（`unfiled`） | 71 |
| 文件名 `report.md` 的份数 | **42** |
| 文件名 `README.md` 的份数 | **3** |
| `report.md` + `README.md` 合计 | **45** |
| 带合法 `date` 的条目数 | 0 |
| 判定为陈旧 / 超期 | 0 |

即：仓库现有 71 份 Markdown，**全部没有 front-matter**；其中 45 份是
`report.md` / `README.md` 这类泛化文件名。这正是「图书馆化」要解决的两件事——
补齐元数据、把泛化文件名改写成可检索的条目名。在元数据补齐之前，分面索引会
把它们全部归入 `unfiled`，`recent` / `stale` 分面则为空。

### 设计约束

* **只读扫描**：遍历 `**/*.md`（跳过 `.git` 等隐藏目录），只读内容，不写回。
* **只写派生索引**：唯一的写行为是 `INDEX.md` 与 `index/*.md`。
* **可重复**：给定相同仓库状态与 `--today`，输出逐字节一致，便于 diff。
