# 原文清单 · DecisionModels

> 本仓库**只存清单与本条目的精读分册**（`papers/*.md`），**不存论文全文**（PDF 或转出的 markdown / txt 都不入库）。
> 需要回看原文时：按下面的 arXiv 链接现取，或用 `paper-fetcher` skill 下载到仓库外缓存。
> **本清单不依赖本地缓存存在**：下表每一格都是可独立复核的一手来源字段，复现命令见 §2。

## 1. 本轮 12 篇（逐篇设分册）

| # | 分册（我们的精读） | arXiv ID | 版本 | 版本日期（该版本发布日） | 标题（arXiv 元数据逐字核实） | 第一作者（核实） | license（`arxiv.org/abs/<id>` 页内核验） | 一手来源 |
| --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | [`papers/2609.23886-this-that-model.md`](<../papers/2609.23886-this-that-model.md>) | 2609.23886 | v1 | 2026-09-20 | this-that-model-1.0: A typed decision model that decides in 30 ms, for a millionth of a cent | Cheng, Zehua | arXiv 默认「永久非独占许可」（页内无 CC 标识） | https://arxiv.org/abs/2609.23886 |
| 2 | [`papers/2609.23986-jev-mem.md`](<../papers/2609.23986-jev-mem.md>) | 2609.23986 | v1 | 2026-09-21 | Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents | Jiang, Dongming | CC BY 4.0 | https://arxiv.org/abs/2609.23986 |
| 3 | [`papers/2609.24052-crash-narrative-calibration.md`](<../papers/2609.24052-crash-narrative-calibration.md>) | 2609.24052 | v1 | 2026-09-21 | Calibrated Decisions at Scale: Converting Police Crash Narratives into Probabilistic Crash Variables with a System One Model (Jev) | Rafe, Amir | arXiv 默认「永久非独占许可」（页内无 CC 标识） | https://arxiv.org/abs/2609.24052 |
| 4 | [`papers/2609.24574-css-text-annotation.md`](<../papers/2609.24574-css-text-annotation.md>) | 2609.24574 | v2 | 2026-09-23（v1 2026-09-21） | Evaluating Decision Models for Text Annotation in Computational Social Science | Ibrahim, Hazem | CC BY 4.0 | https://arxiv.org/abs/2609.24574 |
| 5 | [`papers/2609.25845-visual-jev.md`](<../papers/2609.25845-visual-jev.md>) | 2609.25845 | v1 | 2026-09-22 | Visual Jev: Accurate and Efficient Decisions from Shared Visual Context | Yu, Guanxu | **CC BY-NC-ND 4.0**（12 篇中唯一带 ND 者，见 §3） | https://arxiv.org/abs/2609.25845 |
| 6 | [`papers/2609.26532-reflex-selective-control.md`](<../papers/2609.26532-reflex-selective-control.md>) | 2609.26532 | v1 | 2026-09-22 | REFLEX with Jev for Efficient Selective Control in LLM Agents | Wu, Tiantong | CC BY 4.0 | https://arxiv.org/abs/2609.26532 |
| 7 | [`papers/2609.26550-jev-as-a-judge.md`](<../papers/2609.26550-jev-as-a-judge.md>) | 2609.26550 | v5 | 2026-10-09（v1 2026-09-22） | JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | Li, Yubo | CC BY 4.0 | https://arxiv.org/abs/2609.26550 |
| 8 | [`papers/2609.26758-option-name-vs-definition.md`](<../papers/2609.26758-option-name-vs-definition.md>) | 2609.26758 | v3 | 2026-10-08（v1 2026-09-22） | Type-Safe Is Not Error-Free: Typed Decision Models Follow the Option Name, Not the Definition Bound to It | Sun, Yu | CC BY 4.0 | https://arxiv.org/abs/2609.26758 |
| 9 | [`papers/2609.28613-decision-hijacking.md`](<../papers/2609.28613-decision-hijacking.md>) | 2609.28613 | v1 | 2026-09-23 | Decision Hijacking: Prompt Injection Attacks on Jev's Typed Probabilistic Decisions | Wu, Tiantong | CC BY 4.0 | https://arxiv.org/abs/2609.28613 |
| 10 | [`papers/2609.30243-jevout-natural-context-flip.md`](<../papers/2609.30243-jevout-natural-context-flip.md>) | 2609.30243 | v2 | 2026-10-08（v1 2026-09-24） | JevOut: Natural Context Can Flip Decision Models | Xu, Zixiang | arXiv 默认「永久非独占许可」（页内无 CC 标识） | https://arxiv.org/abs/2609.30243 |
| 11 | [`papers/2609.33209-probability-axioms-coherence.md`](<../papers/2609.33209-probability-axioms-coherence.md>) | 2609.33209 | v1 | 2026-09-27 | Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms? | Li, Keyi | CC BY 4.0 | https://arxiv.org/abs/2609.33209 |
| 12 | [`papers/2610.09683-system-switch.md`](<../papers/2610.09683-system-switch.md>) | 2610.09683 | v1 | 2026-10-07 | System Switch: When Should a Fast Decision Model Stop and Think? | Bailo, Gian Luca | CC BY 4.0 | https://arxiv.org/abs/2610.09683 |

**license 分布**：CC BY 4.0 **8 篇**（#2、#4、#6、#7、#8、#9、#11、#12）；**CC BY-NC-ND 4.0 1 篇**（#5）；**arXiv 默认许可 3 篇**（#1、#3、#10）。合计 12 篇。

### 1.1 版本日期的口径（重要，避免混用）

- 本列取**该版本的发布日期**：对只有 v1 的论文，`published`＝`updated`；对多版本论文（#4 v2、#7 v5、#8 v3、#10 v2），取 **`updated` 字段**＝最新版本发布日，并在括号内标出 **v1 `published`**。
- arXiv Atom API 的 `published` 恒为 **v1 提交日**；**引用具体数字时应以本表「版本」列为准**（例：`2609.26550` 引 v5，`2609.26758` 引 v3）。
- `2609.24574`（v2）、`2609.26550`（v5）、`2609.26758`（v3）、`2609.30243`（v2）与 [`../report.md`](../report.md) §6.2 的版本口径**一致**（已逐条比对）。

## 2. 核验方式（可复现）

| 环节 | 做法 | 命令 / 证据 |
| :-- | :-- | :-- |
| 元数据 + 版本 | `export.arxiv.org/api/query?id_list=<逗号分隔 12 个 ID>`，读 `title` / `published` / `updated` / `author` | 2026-10-18 实测 HTTP 200，12 条 entry 全部返回；标题逐字照抄 API `title` |
| ID 真实性 | **不凭记忆写 ID**：12 条均由 API `entry/id` 回读确认为 `arxiv.org/abs/<ID>v<N>` | 12/12 命中，无 404 |
| license | `curl https://arxiv.org/abs/<ID>`，在页内匹配 `creativecommons.org/licenses/<类型>/<版本>` | 命中即记 CC 具体版本；**无该标识则记 arXiv 默认许可**（不臆断为 CC） |
| 版本日期 | v1 用 `published`，多版本用 `updated` | 与本表第 5 列一一对应 |
| 分册↔原文 | 分册 front-matter 的 `arxiv` / `title` 与本表逐条对齐 | 12/12 一致（例外见 §5） |

## 3. 许可与「全文不入库」的合规说明

1. **arXiv 默认许可是「永久非独占许可」，不授予第三方再分发权**；CC BY 4.0 允许再分发但要求署名；**CC BY-NC-ND 4.0（#5）既禁商用也禁演绎**——因此更不能入库转发。
2. 本条目**只在仓库内保留自己的精读分册与这份来源清单**，PDF / txt / 转出的 markdown **一律不入库**；如需缓存，放仓库外（`paper-fetcher` skill 默认落盘位置）。
3. 分册内引用采用**短引用 + `arXiv ID + 版本` + 章节锚点**，不整段转录原文。

## 4. 未入本清单的引用（说明）

`report.md` 的参考文献中还包含**未设精读分册**的对象（官方仓库 / 产品文档 / 博客，以及若干**仅按摘要级引用**的预印本）。它们**不在本清单的 12 篇之内**，等级与出处逐条写在 `report.md` 的「参考文献」与「链接核验清单」中。**哪些候选被排除、为什么排除**，见 [CANDIDATES.md](CANDIDATES.md)（含 7 个"正文有引用但本轮未设分册"的 ID，已逐个回查 arXiv）。

## 5. 已知不一致（如实记录，未擅自改动他人分册）

| # | 现象 | 处置 |
| --: | :-- | :-- |
| 1 | `2609.33209`、`2610.09683` 的分册 front-matter 写 `evidence: 精读原文`，而 [`../report.md`](../report.md) §6.2 把这两篇 + `2609.29429` 标为**仅摘要级** | **两处等级互相矛盾**；按"单一主等级 + 宁降不升"，正文口径应取**摘要级**。分册归他人维护，本轮**只记录不改**，已列入 CANDIDATES.md 待核。 |
| 2 | `2610.09683` 分册 front-matter 的 `title` 带副标题（"; A closed-loop study with … in Doom"），而 arXiv API `title` 到 "Stop and Think?" 为止 | 本表按 **API 原文**记；副标题疑似来自摘要描述，**不作为题名引用**。 |
| 3 | `2609.33209`、`2610.09683` 分册的 `version` 只写到月（"v1 (2026-09)" / "v1 (2026-10)"） | 本表按 API 补全为 **2026-09-27** / **2026-10-07**，供引用时直接采用。 |

---

*编制时间：2026-10-18 ｜ 元数据：`export.arxiv.org/api/query`（12 条全命中）｜ license：`arxiv.org/abs/<id>` 页内 CC 标识 ｜ 版本日期：`published`（v1）/ `updated`（多版本） ｜ 全文不入库*
