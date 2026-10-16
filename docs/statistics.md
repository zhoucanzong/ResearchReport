# 📊 统计明细 · Statistics

本文件是 **ResearchReport** 的完整体积与数量统计。仓库首页 [README](../README.md) 只保留一张紧凑摘要表；校验留证见 [verification.md](verification.md)。

**统计时点**：2026-10-16（**本批（vLLM 条目）**新增 [vLLM 仓库代码分析报告](../OpenSource/vllm/report.md) 与其三份子文档 [kv-cache-and-prefix-reuse.md](../OpenSource/vllm/kv-cache-and-prefix-reuse.md) / [scheduling-and-spec-decode.md](../OpenSource/vllm/scheduling-and-spec-decode.md) / [claim-audit.md](../OpenSource/vllm/claim-audit.md)；此前同批含 [SGLang 仓库代码分析报告](../OpenSource/sglang/report.md)、[EmbodiedVLA 技术专题调研](../WorldModel/EmbodiedVLA/report.md) 与 [Decision Models 技术专题](../LLM/DecisionModels/report.md)；**Decision Models 条目已升格为领域研究第一批**，新增 [taxonomy.md](../LLM/DecisionModels/taxonomy.md) / [calibration.md](../LLM/DecisionModels/calibration.md) / [experiments.md](../LLM/DecisionModels/experiments.md) 三份子文档；**第二批·证据层**又新增 [`papers/`](../LLM/DecisionModels/papers) 12 篇与 [open-implementations.md](../LLM/DecisionModels/open-implementations.md)，**本批（结论行修正）**再将 `report.md` 推至 846 行）· **统计方法**见文末 §6。**§1、§2 的数字由 [`scripts/library_index.py`](../scripts/library_index.py) 产出**（机器可读版 [`index/stats.json`](../index/stats.json)，重建命令 `python3 scripts/library_index.py --repo-root . --out-root . --write-stats`）；§3–§5 的逐目录明细由 `find` / `stat` / `wc` 实测，未沿用任何估算。

**术语**

- **条目**：文件名字面为 `report.md` 的主文档，重排后全仓库 **48 份**（每个板块条目目录一份，目录名已去 `-research` 后缀）；同目录其它 `.md`（分册 / `plan.md` / `notes/` / `raw-extracts/` 等）是它的**子文档**，`README.md` 与 `docs/*.md` 两者都不是。`OpenSource/mini-swe-agent/` 无 `report.md`，不计条目。
- **报告正文**（历史口径）：重排前 `AIGC-Research/`、`LLM-Research/` 中的 63 份报告文件。
- **深读文档**（历史口径）：重排前 `Repo-Research/` 中的 16 个 `.md`。
- **front-matter**：仅 `OpenSource/sglang/report.md` 一份带 front-matter（9 行 = 7 个字段 + 首尾围栏，符合 [`team.md`](team.md) 的 `type` / `domain` / `subject` / `upstream` / `date` / `evidence` / `status` 契约）；其余条目仍无元数据。
- **库内 `.md`**：含库内 `README.md`；**全仓库 `.md`** 另含根目录 `README.md`、`docs/*.md`、`scripts/README.md` 与生成物 `INDEX.md` / `index/*.md`。
- 所有字节数均为文件实际字节（`stat -f '%z'`），磁盘占用为 `du -sk`（含文件系统块开销，故大于字节数之和）。**生成物（`INDEX.md`、`index/*`）不计入条目 / 文档统计。**

---

## 1. 按板块汇总（重排后实测，脚本产出）

| 指标 | Models | LLM | VisualGen | WorldModel | Infra | OpenSource | 合计 |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| 条目数（`report.md`） | 23 | 8 | 8 | 2 | 3 | 4 | **48** |
| 板块内 `.md` 文档数 | 28 | 24 | 8 | 2 | 14 | 17 | **93** |
| 条目正文行数（去 front-matter） | 14,816 | 5,217 | 6,805 | 750 | 1,866 | 1,056 | **30,510** |
| 条目字节 | 900,388 | 341,216 | 318,086 | 77,496 | 100,011 | 105,316 | **1,842,513** |
| 目录内文件数（全部类型） | 28 | 24 | 8 | 2 | 14 | 18 | **94** |
| 目录内容字节（不含 `.git`） | 1,023,041 | 692,095 | 318,086 | 77,496 | 279,265 | 434,625 | **2,824,608** |
| 磁盘占用 `du -sk` | 1,060 KB | 720 KB | 328 KB | 80 KB | 292 KB | 456 KB | **2,936 KB** |

> **口径**：本表数字全部由 [`scripts/library_index.py`](../scripts/library_index.py) `--write-stats` 产出（机器可读版 [`index/stats.json`](../index/stats.json)）；条目 = `report.md`，目录名已去 `-research` 后缀。`OpenSource/` 含 1 个非条目目录 `mini-swe-agent/`（`mini-swe-agent-deep-report.md` 计入「其他 `.md`」，不计条目）。

## 2. 全仓库口径

| 项目 | 数值 |
| :-- | --: |
| 板块目录 | 6 个（`Models/`、`LLM/`、`VisualGen/`、`WorldModel/`、`Infra/`、`OpenSource/`） |
| 板块树内文件数 | 94 |
| 板块树内容字节 | 2,824,608 B ≈ 2.69 MiB |
| 板块树 `du -sk` | 2,936 KB |
| 全仓库跟踪文件数 | **112**（`git ls-files` 实测，含生成物） |
| 全仓库 `.md` 数 | **107**（99 份文档 + 生成物 `INDEX.md`(1) 与 `index/*.md`(7) 共 8 个） |
| 全仓库工作树 `du -sk`（不含 `.git`） | 3,288 KB（脚本 `du.worktree_excluding_git`） |
| 首页 `README.md` 体量 | 见 [`index/stats.json`](../index/stats.json) `doc_stats.root_readme`（自指量） |

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

> ⚠️ **[历史实测 · 6 板块重排前]** 以下 §3–§5 逐目录明细为重排前口径（旧三库 + `-research` 后缀），仅作追溯留证。表内 `-research` 目录名行均属本历史段，**非当前性引用**。

## 3. AIGC-Research 逐目录（历史）

**模型系列（8 个）**

| 目录 | 报告数 | 行数 | 字节 |
| :-- | --: | --: | --: |
| StabilityAI-research | 1 | 873 | 48,275 |
| OpenAI-Gen | 1 | 859 | 36,915 |
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
| VideoGen | 1 | 898 | 34,716 |
| DiT-research | 1 | 892 | 45,829 |
| DiffusionModels-research | 1 | 855 | 36,106 |
| ImageEditing-research | 1 | 834 | 42,897 |
| AvatarGen-research | 1 | 592 | 27,383 |
| **EmbodiedVLA** | **1** | **433** | **45,956** |
| WorldModels | 1 | **317** | **31,549** |
| **小计** | **10** | **7,555** | **395,591** |

> 两个小计相加：18 份报告 · 13,483 行 · 688,526 B；加上库内 `README.md`（8,137 B）即目录内容 696,663 B。
> **ModelSeries 小计**：20 份 `.md` 合计 **730,106 B**（含 DeepSeek `report.md` 相对更早版本的 332 B 字节漂移）。本表按实测值填写。

---

## 4. LLM-Research 逐目录（历史）

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

> `DecisionModels-research` 的 **17 份** = 条目 [`report.md`](../LLM/DecisionModels/report.md)（**869 行 / ≈107,900 B**，自指量，以 `index/stats.json` 为准）+ 第一批三份子文档 [taxonomy.md](../LLM/DecisionModels/taxonomy.md)（254 行 / 24,958 B）、[calibration.md](../LLM/DecisionModels/calibration.md)（261 行 / 28,421 B）、[experiments.md](../LLM/DecisionModels/experiments.md)（349 行 / 25,200 B）+ 第二批 [`open-implementations.md`](../LLM/DecisionModels/open-implementations.md)（32,731 B）与 [`papers/`](../LLM/DecisionModels/papers) 12 篇（合计 219,545 B）。**条目行数演进**：第一批 608 → 709（+101，三份子文档导航与 §八 指引）→ 第二批 811（+102，`papers/` 导航与 §12）→ **本次 869（+58，§12.6 五条修正留痕、§12.7 自检九项与 §11.1 复跑块；自指量）**；`children` 41、`entries.total` 46 不变。
> 两个小计相加：**58 份报告 · 23,478 行 · 1,695,700 B**；加上库内 `README.md`（14,410 B）与 `.gitignore`（292 B）即目录内容 **1,710,402 B**（脚本口径跳过 `.claude/`；该目录内 `.claude/settings.local.json` 的 151 B 不计入）。

---

## 5. Repo-Research 逐文件（历史）

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
