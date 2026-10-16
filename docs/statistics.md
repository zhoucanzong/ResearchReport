# 📊 统计明细 · Statistics

本文件是 **ResearchReport** 的完整体积与数量统计。仓库首页 [README](../README.md) 只保留一张紧凑摘要表；校验留证见 [verification.md](verification.md)。

**统计时点**：2026-10-16 · **统计方法**见文末 §6。**§1、§2 的数字由 [`scripts/library_index.py`](../scripts/library_index.py) 产出**（机器可读版 [`index/stats.json`](../index/stats.json)，重建命令 `python3 scripts/library_index.py --repo-root . --out-root . --write-stats`）；§3–§5 的逐目录明细由 `find` / `stat` / `wc` 实测，未沿用任何估算。

**术语**

- **条目**：文件名字面为 `report.md` 的主文档，全仓库 43 份（每个 `<topic>-research/` 目录一份）；同目录其它 `.md`（分册 / `plan.md` / `notes/` / `raw-extracts/` 等）是它的**子文档**，`README.md` 与 `docs/*.md` 两者都不是。
- **报告正文**：`AIGC-Research/`、`LLM-Research/` 中的 58 份报告文件（含分册 / 辅文档），**不含**这两个库的 `README.md`。
- **深读文档**：`Repo-Research/` 中的 8 个 `.md`（该项目无 `README.md`）。
- **库内 `.md`**：含库内 `README.md`；**全仓库 `.md`** 另含根目录 `README.md`、`docs/*.md`、`scripts/README.md` 与生成物 `INDEX.md` / `index/*.md`。
- 所有字节数均为文件实际字节（`stat -f '%z'`），磁盘占用为 `du -sk`（含文件系统块开销，故大于字节数之和）。**生成物（`INDEX.md`、`index/*`）不计入条目 / 文档统计。**

---

## 1. 按库汇总

| 指标 | AIGC-Research | LLM-Research | Repo-Research | 合计 |
| :-- | --: | --: | --: | --: |
| 模型系列目录数 | 8 | 15 | — | 23 |
| 技术专题目录数 | 9 | 10 | — | 19 |
| 项目目录数 | — | — | 2 | 2 |
| 报告数 / 文档数（不含 README） | 17 份报告 | 41 份报告 | 8 个 `.md` + 1 个 `.json` | **58 份报告 + 8 份深读文档** |
| ├ 文件名字面为 `report.md`（条目） | 17 | 25 | 1 | 43 |
| └ 其他 `.md`（分册 / 辅文档 / 深度报告） | 0 | 16 | 7 | 23 |
| 报告 / 深读正文**字节** | 625,871 | 1,239,521 | 172,767 | **2,038,159** |
| 报告 / 深读正文**行数** | 12,903 | 19,394 | 3,773 | **36,070** |
| `.md` 文件数（含库内 README） | 18 | 42 | 8 | **68** |
| 目录内文件数（全部类型） | 18 | 43 | 9 | **70** |
| 目录内容字节（不含 `.git`） | 633,625 | 1,252,315 | 189,061 | **2,075,001** |
| 磁盘占用 `du -sk` | 656 KB | 1,308 KB | 204 KB | **2,168 KB** |
| 纳入版本控制的文件 | 18 | 43 | 9 | **70** |

> **口径**：条目（`report.md`）数、文档数、目录内文件数 / 字节 / `du -sk` 由 [`scripts/library_index.py`](../scripts/library_index.py) 产出；「报告 / 深读正文」= 除库内 `README.md` 外的全部 `.md`（含子文档），沿用 §3–§5 的 `stat` / `wc` 口径，故其合计（58 份 / 2,038,159 B / 36,070 行）与「条目」口径（43 份 / 1,579,933 B / 28,210 行）不同。
> 脚本口径**跳过隐藏目录**（如 `LLM-Research/.claude/`）；若按 `find` 计入隐藏目录，LLM-Research 目录内为 44 个文件、三库合计 71 个；其中 `.claude/settings.local.json` 被全局 gitignore 规则忽略，故纳入版本控制的仍是 70 个。
> 「目录内容字节」不含 `.git`；`du -sk` 含文件系统块开销，故大于字节数之和。

## 2. 全仓库口径

| 项目 | 数值 |
| :-- | --: |
| 资料库目录 | 3 个（`AIGC-Research/`、`LLM-Research/`、`Repo-Research/`） |
| 三库目录文件数 | 70 |
| 三库目录字节 | 2,075,001 B ≈ 1.98 MiB |
| 三库目录 `du -sk` | 2,168 KB |
| 全仓库跟踪文件数 | 87（三库 70 + 根 `README.md`、`.gitignore`、`INDEX.md` + `docs/` 4 个文件 + `scripts/` 2 个文件 + `index/` 8 个文件） |
| 全仓库 `.md` 数 | 82（74 份文档 + 生成物 `INDEX.md`(1) 与 `index/*.md`(7)） |
| 全仓库工作树 `du -sk`（不含 `.git` 与生成物） | 约 2,288 KB |
| 全仓库工作树字节（不含 `.git` 与生成物） | 约 2.17 MB（≈ 2.07 MiB） |
| 首页 `README.md` 体量 | 22,419 B / 263 行 |
| `docs/` 体量 | 约 34 KB / 545 行（4 个文件） |

> 全仓库与 `docs/` 的合计为**约值**：`statistics.md` 是本文自身，每次更新都会轻微改变这两个数字。
> `du -sk` 依赖文件系统块分配（macOS/APFS），换文件系统或换机器**无法保证逐字节复现**，故此处按上述口径标注。
> 「全仓库跟踪文件数 / `.md` 数」由 `git ls-files` / `git ls-files '*.md'` 实测，**含生成物**；去掉生成物即 78 个跟踪文件、74 份文档。

**`docs/` 明细**

| 文件 | 行数 | 字节 |
| :-- | --: | --: |
| [maintenance.md](maintenance.md) | 187 | 10,444 |
| [verification.md](verification.md) | 126 | 9,636 |
| [team.md](team.md) | 33 | 3,414 |
| statistics.md（本文自身） | — | 约 10.4 KB，随更新浮动 |

---

## 3. AIGC-Research 逐目录

**模型系列（8 个）**

| 目录 | 报告数 | 行数 | 字节 |
| :-- | --: | --: | --: |
| StabilityAI-research | 1 | 873 | 48,275 |
| OpenAI-Gen-research | 1 | 859 | 36,915 |
| Google-Gen-research | 1 | 826 | 33,598 |
| Alibaba-Gen-research | 1 | 803 | 36,092 |
| Runway-research | 1 | 732 | 33,709 |
| ByteDance-Gen-research | 1 | 711 | 41,175 |
| Midjourney-research | 1 | 587 | 35,037 |
| Kling-research | 1 | 537 | 28,134 |
| **小计** | **8** | **5,928** | **292,935** |

**技术专题（9 个）**

| 目录 | 报告数 | 行数 | 字节 |
| :-- | --: | --: | --: |
| ControllableGen-research | 1 | 923 | 43,040 |
| AudioGen-research | 1 | 913 | 41,460 |
| 3DGen-research | 1 | 898 | 46,655 |
| VideoGen-research | 1 | 898 | 34,716 |
| DiT-research | 1 | 892 | 45,829 |
| DiffusionModels-research | 1 | 855 | 36,106 |
| ImageEditing-research | 1 | 834 | 42,897 |
| AvatarGen-research | 1 | 592 | 27,383 |
| WorldModels-research | 1 | 170 | 14,850 |
| **小计** | **9** | **6,975** | **332,936** |

> 两个小计相加：17 份报告 · 12,903 行 · 625,871 B；加上库内 `README.md`（7,375 B）即目录内容 633,246 B。

---

## 4. LLM-Research 逐目录

**模型系列（15 个系列 / 20 份报告）**

| 目录 | 报告数 | 行数 | 字节 |
| :-- | --: | --: | --: |
| Qwen-research | 4 | 2,513 | 124,106 |
| DeepSeek-research | 3 | 1,525 | 116,669 |
| Gemini-research | 1 | 788 | 34,614 |
| GPT-research | 1 | 759 | 57,261 |
| Doubao-Seed-research | 1 | 643 | 27,470 |
| Claude-research | 1 | 611 | 47,565 |
| Hunyuan-research | 1 | 525 | 36,518 |
| GLM-research | 1 | 523 | 39,747 |
| MiniMax-research | 1 | 517 | 41,290 |
| MiMo-research | 1 | 510 | 34,754 |
| Mistral-research | 1 | 495 | 29,259 |
| LLaMA-research | 1 | 483 | 42,535 |
| Grok-research | 1 | 469 | 32,612 |
| Nemotron-research | 1 | 465 | 32,700 |
| Kimi-research | 1 | 431 | 33,338 |
| **小计** | **20** | **11,257** | **730,438** |

**技术专题（10 个 / 21 份报告）**

| 目录 | 报告数 | 行数 | 字节 |
| :-- | --: | --: | --: |
| RAG-research | 1 | 851 | 44,423 |
| QuantizationEdge-research | 1 | 777 | 34,205 |
| TrainingInfra-research | 1 | 720 | 31,849 |
| Agent-research | 1 | 698 | 31,433 |
| ReasoningModels-research | 1 | 681 | 34,752 |
| SpeculativeDecoding-research | **12** | **2,292** | **209,946** |
| LongContext-research | 1 | 608 | 30,373 |
| Alignment-research | 1 | 588 | 35,712 |
| VLM-research | 1 | 517 | 28,916 |
| MoE-research | 1 | 405 | 27,806 |
| **小计** | **21** | **8,137** | **509,083** |

> 两个小计相加：41 份报告 · 19,394 行 · 1,239,521 B；加上库内 `README.md`（12,502 B）与 `.gitignore`（292 B）即目录内容 1,252,315 B（脚本口径跳过 `.claude/`；若计入其中 `.claude/settings.local.json` 的 151 B 则为 1,252,466 B）。

---

## 5. Repo-Research 逐文件

| 文件 | 类型 | 行数 | 字节 |
| :-- | :-- | --: | --: |
| mini-swe-agent-research/mini-swe-agent-deep-report.md | 源码深度报告 | 735 | 34,490 |
| nemotron-tri-mode-diffusion/report.md | 论文综述报告 | 206 | 13,183 |
| nemotron-tri-mode-diffusion/notes/structured-reading.md | 结构化阅读笔记 | 169 | 10,416 |
| nemotron-tri-mode-diffusion/knowledge-graph.md | 核心概念卡片 | 136 | 10,088 |
| nemotron-tri-mode-diffusion/sources-index.md | 来源索引 | 41 | 2,363 |
| nemotron-tri-mode-diffusion/plan.md | 研究计划 | 28 | 2,561 |
| nemotron-tri-mode-diffusion/raw-extracts/nemotron-tri-mode-fulltext.md | PDF 全文提取 | 2,430 | 98,525 |
| nemotron-tri-mode-diffusion/raw-extracts/pdf-fu_等__…dif.md | PDF 提取占位（未完成） | 28 | 1,141 |
| nemotron-tri-mode-diffusion/papers/nemotron-labs-diffusion.json | 结构化阅读 JSON | 47 | 16,294 |
| **合计** | **9 个文件** | **3,820** | **189,061** |

> 8 个 `.md` 合计 172,767 B / 3,773 行；加上 `papers/nemotron-labs-diffusion.json`（16,294 B）即 189,061 B。
> 注：`.json` 的 47 "行"仅为文件行数，其价值在于结构化字段，不按文档篇幅计入正文行数。

---

## 6. 统计方法

```bash
# §1 / §2 的数字：由脚本统一产出（条目 / 文档 / 字节 / 行数 / du / 版本控制口径）
python3 scripts/library_index.py --repo-root . --out-root . --write-stats
cat index/stats.json

# 文件数 / 字节（逐库）
find <dir> -type f | wc -l
find <dir> -type f -exec stat -f '%z' {} + | awk '{s+=$1} END{print s}'

# 报告正文（排除库内 README）
find AIGC-Research LLM-Research -name '*.md' ! -name 'README.md' | wc -l

# 行数
find <dir> -name '*.md' -print0 | xargs -0 cat | wc -l

# 磁盘占用（不含 .git）
for d in AIGC-Research LLM-Research Repo-Research; do du -sk "$d"; done

# 版本控制口径
git ls-files | wc -l
git ls-files '*.md' | wc -l
```

**口径说明**

1. `du -sk` 反映磁盘块占用（通常大于字节数之和），用于衡量仓库体积；字节数用于内容体量。**本仓库为 macOS/APFS，`du -sk` 依赖文件系统块分配，换文件系统或换机器可能无法逐字节复现**，故 §1、§2 的 `du -sk` 行按此口径标注（§1 由脚本实时产出，§2 的工作树 `du -sk` 为 `du -sk .` 减 `.git` 的约值）。
2. 「报告正文」不包含任何 `README.md`，以避免文档性文件与调研报告混计；**「条目」= `report.md`**，与「报告正文」是两个口径（见 §1 的两组数字）。
3. **行数统一为 `wc -l` 口径**：脚本的「条目正文行数」（见 `INDEX.md`）与逐目录表（§3 / §4 / §5）都按换行符计数、**末尾换行不额外计一行**；剔除 front-matter 后 `front-matter 行数 + 正文行数 = 文件行数`，两个口径可直接对照相加。
4. 全仓库口径随 `docs/`、首页 `README.md` 的更新而变化；**库内报告与正文部分（表 1、3、4、5）在内容不变时保持稳定，可作为跨版本对比基准**。
5. 生成物（`INDEX.md`、`index/*`）不计入条目与文档统计——否则跑一次脚本数字就变一次，无法复现。

---

*最后更新：2026-10-16 · 数据来源：本仓库实际文件系统内容（§1、§2 由 `scripts/library_index.py` 产出，§3–§5 实测，无估算值）*
