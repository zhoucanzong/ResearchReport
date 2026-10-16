# 📊 统计明细 · Statistics

本文件是 **ResearchReport** 的完整体积与数量统计。仓库首页 [README](../README.md) 只保留一张紧凑摘要表；校验留证见 [verification.md](verification.md)。

**统计时点**：2026-10-16（**本批（vLLM 条目）**新增 [vLLM 仓库代码分析报告](../Repo-Research/vllm-research/report.md) 与其三份子文档 [kv-cache-and-prefix-reuse.md](../Repo-Research/vllm-research/kv-cache-and-prefix-reuse.md) / [scheduling-and-spec-decode.md](../Repo-Research/vllm-research/scheduling-and-spec-decode.md) / [claim-audit.md](../Repo-Research/vllm-research/claim-audit.md)；此前同批含 [SGLang 仓库代码分析报告](../Repo-Research/sglang-research/report.md)、[EmbodiedVLA 技术专题调研](../AIGC-Research/TechnicalTopics/EmbodiedVLA-research/report.md) 与 [Decision Models 技术专题](../LLM-Research/TechnicalTopics/DecisionModels-research/report.md)；**Decision Models 条目已升格为领域研究第一批**，新增 [taxonomy.md](../LLM-Research/TechnicalTopics/DecisionModels-research/taxonomy.md) / [calibration.md](../LLM-Research/TechnicalTopics/DecisionModels-research/calibration.md) / [experiments.md](../LLM-Research/TechnicalTopics/DecisionModels-research/experiments.md) 三份子文档；**第二批·证据层**又新增 [`papers/`](../LLM-Research/TechnicalTopics/DecisionModels-research/papers/) 12 篇与 [open-implementations.md](../LLM-Research/TechnicalTopics/DecisionModels-research/open-implementations.md)，**本批（结论行修正）**再将 `report.md` 推至 846 行）· **统计方法**见文末 §6。**§1、§2 的数字由 [`scripts/library_index.py`](../scripts/library_index.py) 产出**（机器可读版 [`index/stats.json`](../index/stats.json)，重建命令 `python3 scripts/library_index.py --repo-root . --out-root . --write-stats`）；§3–§5 的逐目录明细由 `find` / `stat` / `wc` 实测，未沿用任何估算。

**术语**

- **条目**：文件名字面为 `report.md` 的主文档，全仓库 47 份（每个 `<topic>-research/` 目录一份）；同目录其它 `.md`（分册 / `plan.md` / `notes/` / `raw-extracts/` 等）是它的**子文档**，`README.md` 与 `docs/*.md` 两者都不是。
- **报告正文**：`AIGC-Research/`、`LLM-Research/` 中的 63 份报告文件（含分册 / 辅文档 / 子文档），**不含**这两个库的 `README.md`。
- **深读文档**：`Repo-Research/` 中的 16 个 `.md`（该库无 `README.md`）。
- **front-matter**：仅 `Repo-Research/sglang-research/report.md` 一份带 front-matter（9 行 = 7 个字段 + 首尾围栏，符合 [`team.md`](team.md) 的 `type` / `domain` / `subject` / `upstream` / `date` / `evidence` / `status` 契约）；其余条目仍无元数据。
- **库内 `.md`**：含库内 `README.md`；**全仓库 `.md`** 另含根目录 `README.md`、`docs/*.md`、`scripts/README.md` 与生成物 `INDEX.md` / `index/*.md`。
- 所有字节数均为文件实际字节（`stat -f '%z'`），磁盘占用为 `du -sk`（含文件系统块开销，故大于字节数之和）。**生成物（`INDEX.md`、`index/*`）不计入条目 / 文档统计。**

---

## 1. 按库汇总

| 指标 | AIGC-Research | LLM-Research | Repo-Research | 合计 |
| :-- | --: | --: | --: | --: |
| 模型系列目录数 | 8 | 15 | — | 23 |
| 技术专题目录数 | 10 | 11 | — | 21 |
| 项目目录数 | — | — | 3 | 3 |
| 报告数 / 文档数（不含 README） | 18 份报告 | 45 份报告 | 16 个 `.md` + 1 个 `.json` | **63 份报告 + 16 份深读文档** |
| ├ 文件名字面为 `report.md`（条目） | 18 | 26 | 3 | **47** |
| └ 其他 `.md`（分册 / 辅文档 / 子文档 / 深度报告） | 1 | 33 | 10 | **44** |
| 报告 / 深读正文**字节** | 688,526 | 1,701,474 | 394,354 | **2,784,354** |
| 报告 / 深读正文**行数** | 13,483 | 23,501 | 5,763 | **42,747** |
| `.md` 文件数（含库内 README） | 19 | 59 | 16 | **94** |
| 目录内文件数（全部类型） | 19 | 60 | 17 | **96** |
| 目录内容字节（不含 `.git`） | 696,663 | 1,716,176 | 410,648 | **2,823,487** |
| 磁盘占用 `du -sk` | 720 KB | 1788 KB | 424 KB | **2,932 KB** |
| 纳入版本控制的文件 | 19 | 60 | 17 | **96** |

> **口径**：条目（`report.md`）数、文档数、目录内文件数 / 字节 / `du -sk` 由 [`scripts/library_index.py`](../scripts/library_index.py) 产出；「报告 / 深读正文」= 除库内 `README.md` 外的全部 `.md`（含子文档），沿用 §3–§5 的逐文件 `stat` / `wc` 实测口径（脚本已内建同一口径），故其合计（**94 份 / 2,784,354 B / 42,747 行**）与「条目」口径（47 份 / **1,818,281 B** / **30,264 行**；**自指量**，权威值见 [`index/stats.json`](../index/stats.json)）不同。**本批**含两部分：① vLLM 条目（新增 4 个文档：`report.md` 35,658 B / 正文 294 行 + 三份子文档，`children` 41 → 44、`entries.total` 46 → 47）；② 锚点复检（`claim-audit.md` 新增 §3.5 与附录 A 全表 207 行）。基线（`acafc4e`）的 `entries.lines` 为 **29,970**，本批终态 **30,264**。
> 脚本口径**跳过隐藏目录**（如 `LLM-Research/.claude/`）；若按 `find` 计入隐藏目录，LLM-Research 目录内为 61 个文件、三库合计 97 个；其中 `.claude/settings.local.json` 被全局 gitignore 规则忽略，故三库纳入版本控制的是 **96** 个。
> 「目录内容字节」不含 `.git`；`du -sk` 含文件系统块开销，故大于字节数之和。
> ⚠️ **本次校出的既有不一致（未擅改，留待确认）**：本表上一版在 LLM-Research「技术专题」小计中写 `22 份报告 / 8,745 行 / 575,272 B`（`DecisionModels-research` 记为 `1 / 608 / 66,189`），但工作树实测该专题为 **25 份 / 9,664 行 / 661,863 B**——差异恰为**三份子文档**（1,526−674 = 852 行、149,183−71,860 = 77,323 B）加 332 B 的 DeepSeek `report.md` 字节差（工作树 58,512 B，按旧小计反推为 58,844 B）。本轮按**实测值**重算 LLM-Research 全部数字；DeepSeek 那 332 B 属**修表前就已存在的口径漂移**，不在本批改动范围内，已记入 [DecisionModels report.md §11](../LLM-Research/TechnicalTopics/DecisionModels-research/report.md)。

## 2. 全仓库口径

| 项目 | 数值 |
| :-- | --: |
| 资料库目录 | 3 个（`AIGC-Research/`、`LLM-Research/`、`Repo-Research/`） |
| 三库目录文件数 | 96 |
| 三库目录字节 | 2,823,487 B ≈ 2.69 MiB |
| 三库目录 `du -sk` | 2,932 KB |
| 全仓库跟踪文件数 | **113**（三库 96 + 根 `README.md`、`.gitignore`、`INDEX.md` + `docs/` 4 个文件 + `scripts/` 2 个文件 + `index/` 8 个文件；`git ls-files` 实测） |
| 全仓库 `.md` 数 | **108**（100 份文档 + 生成物 `INDEX.md`(1) 与 `index/*.md`(7) 共 8 个） |
| 全仓库工作树 `du -sk`（不含 `.git` 与生成物） | 约 2,920 KB |
| 全仓库工作树字节（不含 `.git` 与生成物） | 约 2.67 MB（≈ 2.55 MiB） |
| 首页 `README.md` 体量 | 26,993 B / 290 行（本次复测；含 Repo-Research 四条目索引段） |
| `docs/` 体量 | 见文末 §6 的实时实测（本文自身写入后即变） |

> 全仓库与 `docs/` 的合计为**约值**：`statistics.md` 是本文自身，每次更新都会轻微改变这两个数字。
> `du -sk` 依赖文件系统块分配（macOS/APFS），换文件系统或换机器**无法保证逐字节复现**，故此处按上述口径标注。
> 「全仓库跟踪文件数 / `.md` 数」由 `git ls-files` / `git ls-files '*.md'` 实测，**含生成物**；去掉 8 个生成物即 **105** 个跟踪文件、**100** 份文档。

**`docs/` 明细**

| 文件 | 行数 | 字节 |
| :-- | --: | --: |
| [maintenance.md](maintenance.md) | 187 | 10,444 |
| [verification.md](verification.md) | 148 | 12,134 |
| [team.md](team.md) | 33 | 3,414 |
| statistics.md（本文自身） | 221 | 18,123 |
| **合计** | **589** | **44,115** |

> `docs/` 合计 = 四个文件之和（含本文自身）；本文每次更新都会改变这两行，故按写入后的实测值填写。

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

**技术专题（10 个）**

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
| **EmbodiedVLA-research** | **1** | **433** | **45,956** |
| WorldModels-research | 1 | **317** | **31,549** |
| **小计** | **10** | **7,555** | **395,591** |

> 两个小计相加：18 份报告 · 13,483 行 · 688,526 B；加上库内 `README.md`（8,137 B）即目录内容 696,663 B。
> **ModelSeries 小计**：20 份 `.md` 合计 **730,106 B**（含 DeepSeek `report.md` 相对更早版本的 332 B 字节漂移）。本表按实测值填写。

---

## 4. LLM-Research 逐目录

**模型系列（15 个系列 / 20 份报告）**

| 目录 | 报告数 | 行数 | 字节 |
| :-- | --: | --: | --: |
| Qwen-research | 4 | 2,513 | 124,106 |
| DeepSeek-research | 3 | 1,525 | 116,337 |
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
| **小计** | **20** | **11,257** | **730,106** |

**技术专题（11 个 / 38 份报告）**

| 目录 | 报告数 | 行数 | 字节 |
| :-- | --: | --: | --: |
| RAG-research | 1 | 851 | 44,423 |
| QuantizationEdge-research | 1 | 777 | 34,205 |
| TrainingInfra-research | 1 | 720 | 31,849 |
| Agent-research | 1 | 698 | 31,433 |
| ReasoningModels-research | 1 | 681 | 34,752 |
| SpeculativeDecoding-research | **12** | **2,293** | **213,211** |
| LongContext-research | 1 | 608 | 30,373 |
| Alignment-research | 1 | 588 | 35,712 |
| **DecisionModels-research** | **17** | **4,083** | **452,914** |
| VLM-research | 1 | 517 | 28,916 |
| MoE-research | 1 | 405 | 27,806 |
| **小计** | **38** | **12,221** | **965,594** |

> `DecisionModels-research` 的 **17 份** = 条目 [`report.md`](../LLM-Research/TechnicalTopics/DecisionModels-research/report.md)（**869 行 / ≈107,900 B**，自指量，以 `index/stats.json` 为准）+ 第一批三份子文档 [taxonomy.md](../LLM-Research/TechnicalTopics/DecisionModels-research/taxonomy.md)（254 行 / 24,958 B）、[calibration.md](../LLM-Research/TechnicalTopics/DecisionModels-research/calibration.md)（261 行 / 28,421 B）、[experiments.md](../LLM-Research/TechnicalTopics/DecisionModels-research/experiments.md)（349 行 / 25,200 B）+ 第二批 [`open-implementations.md`](../LLM-Research/TechnicalTopics/DecisionModels-research/open-implementations.md)（32,731 B）与 [`papers/`](../LLM-Research/TechnicalTopics/DecisionModels-research/papers/) 12 篇（合计 219,545 B）。**条目行数演进**：第一批 608 → 709（+101，三份子文档导航与 §八 指引）→ 第二批 811（+102，`papers/` 导航与 §12）→ **本次 869（+58，§12.6 五条修正留痕、§12.7 自检九项与 §11.1 复跑块；自指量）**；`children` 41、`entries.total` 46 不变。
> 两个小计相加：**58 份报告 · 23,478 行 · 1,695,700 B**；加上库内 `README.md`（14,410 B）与 `.gitignore`（292 B）即目录内容 **1,710,402 B**（脚本口径跳过 `.claude/`；该目录内 `.claude/settings.local.json` 的 151 B 不计入）。

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
| **sglang-research/report.md** | **仓库代码分析报告（条目）** | **310**（正文，另有 9 行 front-matter 围栏块） | **32,226** |
| sglang-research/speculative-decoding-path.md | 子文档：投机解码路径与 EAGLE 对照 | 230 | 25,276 |
| sglang-research/scheduler-and-prefix-cache.md | 子文档：调度器 / 前缀缓存 / 连续批处理 | 174 | 20,863 |
| sglang-research/claim-audit.md | 子文档：结论审计与阅读覆盖 | 149 | 11,639 |
| **vllm-research/report.md** | **仓库代码分析报告（条目）** | **294**（正文，另有 9 行 front-matter 围栏块） | **35,658** |
| vllm-research/kv-cache-and-prefix-reuse.md | 子文档：KV 缓存 / 块池 / 前缀复用 | 206 | 19,069 |
| vllm-research/scheduling-and-spec-decode.md | 子文档：调度 / 投机解码 / 语法约束交互 | 244 | 24,076 |
| vllm-research/claim-audit.md | 子文档：结论审计、阅读覆盖与自检（含 §3.5 锚点复检 + 附录 A 全表 207 行） | **422** | **52,515** |
| **合计** | **17 个文件** | **5,867** | **410,648** |

> 16 个 `.md` 合计 **394,354 B / 5,820 行**（其中 vLLM 条目 4 份共 1,175 行 / 131,383 B）；加上 `papers/nemotron-labs-diffusion.json`（16,294 B / 47 行）即目录内容 **410,648 B**（脚本口径；「合计行」的行数只含 `.md` 行数，不含 JSON 的 47 行）。**正文字节与目录内容字节均取自 `index/stats.json`**（`libraries["Repo-Research"]` 的 `bytes` 与 `dir_bytes`）。
> 注：`.json` 的 47 "行"仅为文件行数，其价值在于结构化字段，不按文档篇幅计入正文行数。
> SGLang 子文档的行数 / 字节以 `wc -l` / `stat -f '%z'` 实测为准：`report.md` 319 行（正文 310 + front-matter 围栏块 9）/ 32,226 B、`speculative-decoding-path.md` 230 行 / 25,276 B、`scheduler-and-prefix-cache.md` 174 行 / 20,863 B、`claim-audit.md` **149 行** / 11,639 B。
> vLLM 条目同样以 `wc -l` / `stat -f '%z'` 实测（**本批终态**）：`report.md` **303 行（正文 294 + front-matter 围栏块 9）/ 35,658 B**、`kv-cache-and-prefix-reuse.md` 206 行 / 19,069 B、`scheduling-and-spec-decode.md` 244 行 / 24,141 B、`claim-audit.md` **422 行 / 52,515 B**（本次锚点复检后由 131 行 / 10,273 B 增长）。**vLLM 是本仓库第二个带 front-matter 的条目**（`with_front_matter` 由 1 → 2）。

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

*最后更新：2026-10-16（**vLLM 条目 + 锚点复检**：`entries.total` 基线 `acafc4e` 的 **46 → 47**、`children` **44**、条目口径行数 29,970 → **30,264**、条目字节 **1,818,281**、`with_front_matter` **1 → 2**、三库文件数 **92 → 96**；本批另完成锚点机械复检 207 处（归一化 123 条唯一断言，未命中 0，修正 17 处 + 正文残留 1 处，自洽校验 A/B/C 全通过），`claim-audit.md` 新增 §3.5 与附录 A；本次按实测重跑并同步根 `README.md` 与本节）· 数据来源：本仓库实际文件系统内容（§1、§2 由 `scripts/library_index.py` 产出，§3–§5 实测，无估算值）*
