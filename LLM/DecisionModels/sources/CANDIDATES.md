# 候选与取舍 · DecisionModels

> 本文回答三个问题：**哪些进了本轮精读（12 篇设分册）**、**哪些只在 `report.md` 被引用而没设分册**、**为什么**。
> 纪律：**本文出现的每一个 arXiv ID 都在 2026-10-18 回查过 `arxiv.org/abs/<id>`（标题 / 作者 / 版本以该页与 Atom API 为准）**，不含凭记忆补写或推测的编号。逐篇元数据见 [MANIFEST.md](MANIFEST.md)。
> 计数：**入选 12 + 引用但未设分册 7 = 19 个已核验 ID**。

## 1. 筛选标准（先定口径，再挑论文）

| # | 标准 | 说明 |
| --: | :-- | :-- |
| A | **与"类型化 / 决策模型"直接相关** | 论文的**主张对象**必须是这类模型（Jev / this-that-model 一类），而不是"用 LLM 顺带做了个分类" |
| B | **有一手可核的数字** | 必须能在 arXiv HTML 正文里逐字 `grep` 到（本库的 `find:` 串制度），否则降为摘要级 |
| C | **覆盖面不重复** | 成本 / 吞吐 / 记忆 / 评测器 / 校准 / 失效机制 / 安全 各留位置，宁缺不堆同质论文 |
| D | **能写进 `report.md` 的结论** | 只服务于"某处已有或应有主张"的论文才设分册；纯背景引用不设 |

## 2. 入选：本轮设分册的 12 篇

| # | arXiv ID | 分册 | 入选理由（一句话） | 在报告中的角色 |
| --: | :-- | :-- | :-- | :-- |
| 1 | 2609.23886 | [`papers/2609.23886-this-that-model.md`](<../papers/2609.23886-this-that-model.md>) | 给出该类模型**最强的成本/延迟主张**（30.9 ms、零非法输出），是评估其余条目的参照基线 | 成本与合法性基线 |
| 2 | 2609.23986 | [`papers/2609.23986-jev-mem.md`](<../papers/2609.23986-jev-mem.md>) | 把"控制类决策移出自回归循环"做成**完整架构主张**，效率侧有同条件对照可复算 | 架构分工 / 记忆 |
| 3 | 2609.24052 | [`papers/2609.24052-crash-narrative-calibration.md`](<../papers/2609.24052-crash-narrative-calibration.md>) | 在**高后果领域**（事故叙述编码）验证校准与规模化，是少见的真实业务落地证据 | 领域落地 / 校准 |
| 4 | 2609.24574 | [`papers/2609.24574-css-text-annotation.md`](<../papers/2609.24574-css-text-annotation.md>) | 把决策模型放进**科研标注流程**并与人工/LLM 对照，提供方法学侧证据 | 科研工作流 / 评测 |
| 5 | 2609.25845 | [`papers/2609.25845-visual-jev.md`](<../papers/2609.25845-visual-jev.md>) | **多模态吞吐**：同图多问共享视觉上下文，是"批处理省前缀"的代表 | 吞吐 / 多模态 |
| 6 | 2609.26532 | [`papers/2609.26532-reflex-selective-control.md`](<../papers/2609.26532-reflex-selective-control.md>) | 回答"**何时用快模型、何时升级**"，补上系统集成侧的选择性控制 | 选择性控制 / 系统集成 |
| 7 | 2609.26550 | [`papers/2609.26550-jev-as-a-judge.md`](<../papers/2609.26550-jev-as-a-judge.md>) | 把模型放到**评测器**位置（置信时接受、不确定时升级），且版本迭代多（v5）需盯 | 评测器 / 置信度 |
| 8 | 2609.26758 | [`papers/2609.26758-option-name-vs-definition.md`](<../papers/2609.26758-option-name-vs-definition.md>) | 揭示**失效机制**：类型安全 ≠ 语义正确（跟"名字"而非"定义"绑定），是最有价值的负面证据 | 失效机制 |
| 9 | 2609.28613 | [`papers/2609.28613-decision-hijacking.md`](<../papers/2609.28613-decision-hijacking.md>) | 首次量化**安全边界**：闭集输出仍有注入面，且"概率位移 ≠ 动作选择" | 安全 / 威胁模型 |
| 10 | 2609.30243 | [`papers/2609.30243-jevout-natural-context-flip.md`](<../papers/2609.30243-jevout-natural-context-flip.md>) | 证明**自然上下文即可翻转决策**（无需对抗构造），把失效边界从"攻击"扩到"日常输入" | 失效机制 |
| 11 | 2609.33209 | [`papers/2609.33209-probability-axioms-coherence.md`](<../papers/2609.33209-probability-axioms-coherence.md>) | 追问**概率是否满足公理**（超越"校准"），补上"概率能不能当概率用"这一层（**v1正文已复核，2026-10-22**） | 概率合法性 |
| 12 | 2610.09683 | [`papers/2610.09683-system-switch.md`](<../papers/2610.09683-system-switch.md>) | **闭环切换**研究（何时停 / 何时想），在 Doom 环境里给出决策—思考切换的实测（**v1正文已复核，2026-10-22**） | 系统切换 |

## 3. 未设分册：`report.md` 有引用、但本轮不单独立篇的 7 篇

> 这 7 篇**不是"质量差"**，而是**不满足标准 D**（只作旁证/应用落点，或已降为摘要级）。它们仍出现在 `report.md` 的参考文献与链接核验清单里。

| # | arXiv ID | 标题（核验后） | 未设分册的理由（一句话） |
| --: | :-- | :-- | :-- |
| 1 | 2307.12950 | RLCD: Reinforcement Learning from Contrastive Distillation for Language Model Alignment | 与厂商自述的训练目标缩写**同名不同义**，只用于消歧；非决策模型文献 ⇒ 标 `摘要级·题录/摘要` |
| 2 | 2609.29429 | Just Ask Jev: Reinforcement Learning for Calibrated Decisions as a Zero-Shot Detector of AI Alignment Failures | "决策模型当检测器"的**旁支应用**，正文仅在 §6.2 旁证表出现 ⇒ 摘要级 |
| 3 | 2609.24965 | Jev for Scientific Decisions: Evaluating Semantic Choices and Their Consequences | 科研工作流应用线；且"最低观测中位时延"一条已按单一主等级**降为摘要级**，设分册收益低 |
| 4 | 2609.24395 | JEVQA - Video Quality from Metadata, Bitstream, and Pixel Features with a General-Purpose Decision Model | 应用落点（视频质量预测）偏离决策模型主干；正文等级已按"对源"改正为精读级，**主题不匹配**故不设分册 |
| 5 | 2609.23136 | Intent Interpretation at RIC Timescales: Jev Decision Models versus Large Language Models in 6G | 电信场景应用线，与主干共享同一模型但**场景外推**，留作下一轮候选 |
| 6 | 2609.22753 | Replacing Large Language Models with Jev Decision Models for Low-Latency Edge Service Orchestration | 边缘编排应用线，同上：**场景证据**而非模型机制证据 |
| 7 | 2609.23959 | Open-Jev Judgments on CallScreenBench: Calibrated One-Pass Scam Screening with a Small Language Model | 诈骗筛查应用线，本轮未触及该场景的 `report.md` 主张 |

**为什么"应用线"被成批排除**：它们共享同一模型、只换场景，设分册会产生**高度同质**的 8 份文件，违反标准 C；但它们的场景差异对未来"泛化性"结论有用，故保留为**下一轮候选**而非丢弃。

## 4. 待核（本轮记录、未擅自改动）

| # | 事项 | 证据 | 建议 |
| --: | :-- | :-- | :-- |
| 1 | `2609.33209`、`2610.09683` 曾在主文/分册/清单间等级冲突 | 2026-10-22 已读固定 v1 正文并核对 §5；主文补入一致性结果及33局未通关的失效边界，统一为正文级证据；不以字符串出现代替主张核验 | 已同步 |
| 2 | System Switch 题名与副标题 | 2026-10-22 已确认正文确含 Doom 副标题 | 元数据主标题和正文副标题分别记录，不再称副标题疑似虚构 |
| 3 | 两篇分册 version 曾仅到月 | **已同步**为 v1 (2026-09-27) / v1 (2026-10-07)，作者也已依正文补齐。 |

## 5. 复核方法（可重跑）

```bash
# 12 篇入选 + 7 篇未设分册，一次批量核验题名/作者/版本
curl -sS "https://export.arxiv.org/api/query?id_list=2609.23886,2609.23986,2609.24052,2609.24574,2609.25845,2609.26532,2609.26550,2609.26758,2609.28613,2609.30243,2609.33209,2610.09683,2307.12950,2609.29429,2609.24965,2609.24395,2609.23136,2609.22753,2609.23959&max_results=30"
# license：逐篇在 abs 页匹配 creativecommons.org 标识
for id in 2609.23886 2609.23986 2609.24052 2609.24574 2609.25845 2609.26532 2609.26550 2609.26758 2609.28613 2609.30243 2609.33209 2610.09683; do
  echo "$id -> $(curl -sS https://arxiv.org/abs/$id | grep -o 'creativecommons.org/licenses/[a-z-]*/[0-9.]*' | head -1)"
done
```

---

*编制时间：2026-10-18 ｜ 19 个 ID 全部回查 arXiv（0 个凭记忆写入）｜ 取舍标准 A–D 见 §1 ｜ 与 [MANIFEST.md](MANIFEST.md) 配套*
