# Decision Models（System One / Typed Decision Model）技术专题调研

> **JEV（TypeSafe）为本条目的主线案例**，其官方文档、第三方研究与失效证据构成主要材料；条目同时覆盖同类的开源决策模型实现。
>
> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、官方文档与第三方分析整理生成。**TypeSafe 未发布正式技术论文**，官方材料属"一手但自述"；arXiv 条目均为 2026-09 至 2026-10 的预印本，未经同行评审。厂商自测的加速/降本倍率不得当作通用结论。所有引用均于 2026-10-16 实测可达。
>
> **调研日期**：2026-10-16
> **覆盖范围**：2026-09-15 Jev 发布至 2026-10-16（含 jev-1.14 发布、arXiv 2609/2610 第三方研究）的公开材料
> **调研口径**：时间不限、详细度=详细；**不做教学讲解、不做知识图谱**；本条目为技术专题（`subject: decision-models`），同类已纳入 `this-that-model` / `Laya` / `Kev` / `JevLite` 等开源决策模型
> **条目路径**：`LLM-Research/TechnicalTopics/DecisionModels-research/report.md`（非 skill 默认输出目录）
> **子文档**（领域研究第一批·结构层）：[taxonomy.md](taxonomy.md)（边界 / 接口谱系 / 训练目标谱系 + 分类图）· [calibration.md](calibration.md)（ECE/Brier/可靠性曲线的跨域-跨语言-不平衡-OOD 证据链、阈值迁移与重校准成本）· [experiments.md](experiments.md)（§八 复核清单的可执行实验协议）
> **子文档**（领域研究第二批·证据层，2026-10-16）：**逐篇论文提取 12 篇** → [`papers/`](papers/)（每篇一份：方法 / 实验 / 数字+条件 / 失效边界 / 关联到本文哪条结论；统一模板并逐条附可 grep 的 `find:` 串）· [open-implementations.md](open-implementations.md)（`this-that-model` / `Laya` / `Kev` / `JevLite` / `Visual Jev` 的**实现路径**（隐藏状态直读 / 微调分类头 / LM head 读数）、**可复现性**（权重·许可·接口·依赖）与**模型卡口径**；全部外链实测状态码）
> **第二批论文索引（12 篇，编号↔标题均已核对）**：[2609.24574 CSS 横评](papers/2609.24574-css-text-annotation.md) · [2609.26550 as-a-Judge](papers/2609.26550-jev-as-a-judge.md) · [2609.26758 选项名 vs 定义](papers/2609.26758-option-name-vs-definition.md) · [2609.30243 JevOut](papers/2609.30243-jevout-natural-context-flip.md) · [2609.28613 Decision Hijacking](papers/2609.28613-decision-hijacking.md) · [2609.23986 Jev-Mem](papers/2609.23986-jev-mem.md) · [2609.26532 REFLEX](papers/2609.26532-reflex-selective-control.md) · [2609.23886 this-that-model](papers/2609.23886-this-that-model.md) · [2609.25845 Visual Jev](papers/2609.25845-visual-jev.md) · [2609.24052 事故叙述编码](papers/2609.24052-crash-narrative-calibration.md) · [2609.33209 概率公理一致性](papers/2609.33209-probability-axioms-coherence.md) · [2610.09683 System Switch](papers/2610.09683-system-switch.md)
> **子文档口径**：三份子文档与本文共用同一套证据等级标签（单一主等级、混合取最弱，来源类型写括号）与同一条硬规则（**不做跨论文排行榜**；对照表必带条件列）。子文档中的"研究推断"一律显式标注，**不在本文正文内新增结论**。第二批的 `papers/` 与 `open-implementations.md` 遵守同一套标签与硬规则；**凡未能确证的均列入各文件 §7「未确证/待跟踪」，不入正文**。

---

## 〇、结论速览

1. **JEV 的可验证内核只有一句话**：把"合法输出空间"在请求前枚举好，用一次前向计算直接读出候选标签的概率分布，**不生成任何输出 token**，因此类型错误在构造上不可能发生、拒答/解析重试循环不需要、同一个 state 上的多个问题可并行求解（[TypeSafe 官方 System One 文档](https://docs.typesafe.ai/concepts/system-one)，精读原文·官方文档，2026-10-16）。
2. **"格式保证"≠"内容保证"**：官方明确只承诺输出被约束在声明的选项/档位内；模型仍可在你给的三项里选错（同上）。把 0% type error 当准确率是常见误读。
3. **训练目标 RLCD 与厂商主张均为厂商自述**：TypeSafe 自述使用 RLCD（Reinforcement Learning for Calibrated Decisions），**缩写与 2023 年 ICLR 2024 的 RLCD（Reinforcement Learning from Contrastive Distillation，[arXiv:2307.12950](https://arxiv.org/abs/2307.12950)）完全撞车、方法完全不同**，本报告 §3 专章消歧；开源复刻 Laya 又给 RLCD 第三种解释，使用者必须逐文核对定义。
4. **官方材料边界**：TypeSafe **没有**正式技术论文、没有公开权重、没有公开架构细节；官方只有产品/模型/API 文档、AI primer、jaggedness 弱点清单与创始人访谈。第三方已独立记录"截至 2026-10-14 未检索到同行评审的 TypeSafe 架构或 RLCD 论文"（[Awesome JEV Papers](https://github.com/Oscar-dzy/Awesome-jev-papers)，二手·索引仓库，2026-10-16）。
5. **官方倍率不可通用化**：媒体转述的"快 193.6 倍 / 便宜 444.6 倍"是**工作流自评**且**官方自己标注为偏乐观的上限**（[腾讯云开发者社区分析](https://cloud.tencent.com/developer/article/2750505)，二手·技术分析，2026-10-16）。详见 §4。
6. **第三方结果指向"中等能力 + 极低成本 + 置信度可用但有边界"**：CSS 18 任务横评中决策模型在 15 个评测任务上 14 个落后于单任务最优 LLM（中位差距 11.6 macro-F1），但成本中位低约 44 倍、置信度校准优于 19 个 LLM 中的 16 个（[arXiv:2609.24574](https://arxiv.org/abs/2609.24574)，精读原文·预印本，2026-10-16）。
7. **失效面已被独立坐实**：短小普通上下文可在**高置信度下**把正确决策翻成固定错误选项（[arXiv:2609.30243](https://arxiv.org/abs/2609.30243)）；选项**名称**的语义极性可以盖过定义（[arXiv:2609.26758](https://arxiv.org/abs/2609.26758)）；开源复刻出现"高置信度 + 近零准确率"实例（Laya 模型卡：高棉语 0.000 准确率 / 0.952 置信度，二手·模型卡，2026-10-16）。

---

## 一、范围与证据规则

### 1.1 本报告覆盖什么

本条目研究对象是**决策模型（decision models）这一模型类别**，TypeSafe JEV 是其中主线且材料最完整的案例。

| 维度 | 覆盖内容 | 不覆盖 |
|---|---|---|
| 模型对象 | TypeSafe `jev-1.13.0` / `jev-1.14.0`，及声明同构的 System One / typed decision model 家族 | TypeSafe 未公开的权重、架构、数据配方 |
| 时间 | 2026-09-15 发布 → 2026-10-16 | 2026-10-16 之后的新发布 |
| 材料 | 官方文档（精读）、arXiv 预印本（精读原文，部分摘要级）、开源实现模型卡、第三方技术分析 | 营销页、无一手论文支撑的排行 |

### 1.2 证据等级标签（单一主等级，混合取最弱）

| 标签 | 含义 | 本报告中该等级典型来源 |
|---|---|---|
| **精读原文** | 已抓取并阅读**正文**（HTML/文档源），结论句可在**正文**（非仅摘要）定位 | TypeSafe 官方 `.md` 文档、arXiv HTML 正文 |
| **摘要级** | 只读到题录/摘要，未逐节复核正文 | 部分旁证论文（本报告仅 3 篇） |
| **二手** | 他人对一手材料的转述/汇总，本人未核一手 | 技术分析文章、索引仓库、模型卡自述 |
| **受限核验** | 目标不可达（403/DNS）或因规则不核验 | 被 403 拦截的 Zenodo 记录 |

括号内注明**来源类型**（官方文档 / 预印本 / 模型卡 / 媒体分析 / 索引仓库）。每条引用均附实测可达链接。**无法确证的一律不进正文**，单列于 §9。

#### 1.2.1 「精读原文」标签的对源抽查（2026-10-16 两轮复核，含一次方法学自纠）

本报告共 35 处 `精读原文·预印本`，涉及 22 篇不同预印本。为排除"把摘要当正文"的标签虚高，对全部 22 篇做了**机械可复现的对源抽查**：抓取 `arxiv.org/html/<id>v1`，剥除摘要块，再在剩余正文中检索本报告所引用的关键数字/字符串；**关键串出现在剥摘要后的正文中才算 `精读原文`**。

**第一轮（有缺陷，已废弃）**：按 `<blockquote class="abstract">` 剥摘要。**该方法对这些 arXiv HTML 是错的**——摘要实际位于 `<div id="abstract1" class="ltx_abstract">`，因此第一轮"命中正文"的结果里混入了摘要文字，等于没有真正剥离摘要，结论不可用。

**第二轮（现行口径）**：改为剥除 `class="ltx_abstract"` 容器。抽验范围覆盖本报告引用的**全部关键数字与短句**（约 60 个串），逐串记录其出现在「摘要」还是「剥摘要后的正文」。

| 第二轮结果 | 篇数 / 条目数 | 处理 |
|---|---|---|
| 所引关键串均在**正文**命中 | 20 篇 | 维持 `精读原文·预印本` |
| 有关键串**仅**在摘要、正文查无 | 1 篇（2 处主张） | **按单一主等级降为 `摘要级`**，逐条列于下方降级表 |
| 只引题录/摘要的旁证（本报告主动限定为摘要级） | 1 篇 | `2307.12950` 记为 `摘要级·题录/摘要` |

> 20 + 1 + 1 = 22 篇。抽验中另发现 **3 处假阳性**（探针串写错导致的误判），已在 §1.2.2 末尾逐条撤销；**最终实际降级 2 处主张、涉及 1 篇论文**。

**降级清单（宁降不升）**：

| 原标注处 | 主张 | 第二轮核验 | 新标签 |
|---|---|---|---|
| §6.3 横评表、§7.2 效率表 | JEV-as-a-Judge 费用为最强 LLM 评判者的 **0.36%** | `0.36%` **仅出现在摘要**；剥摘要后的正文查无该串 | `摘要级·预印本（仅摘要）` |
| §6.1 应用表、§7.2 效率表 | 科学决策研究取得"**最低观测中位时延**" | 该表述**仅出现在摘要**；正文查无 | `摘要级·预印本（仅摘要）` |
| §3.2 消歧表 | 2023 年 RLCD 的**方法机制与结论** | 本报告只读题录+摘要（`Contrastive Distillation` 串在正文亦无） | `摘要级·题录/摘要` |

**同篇其余主张不受影响**：例如 JEV-as-a-Judge 的"冻结级联保留 99% 准确率""RewardBench 94.0% vs 93.5%"经复核**确在正文**，故该论文仍保留 `精读原文·预印本`，仅**上述单条主张**降为 `摘要级`（单一主等级按**主张粒度**判定，不牵连同篇其它确证主张）。

**一条标签改正（"宁降不升"的适用边界）**：§6.2 的 `2609.24395`（JEVQA）此前被保守标为 `摘要级`，但第二轮抽验确认其正文关键串 `0.824`、`1,936`、`0.797` 均**在剥摘要后的正文命中**，故按"对源"原则**改正为 `精读原文·预印本`**（§7.1 同步）。"宁降不升"用于**本 Agent 未读正文**的引用（如 `2609.24395` 旧标注、§6.2 的 Open-Jev 等旁证），**不用于**已实测命中正文的引用——把已对源的条目压在 `摘要级` 会造成反向失真、低估证据强度。

#### 1.2.2 「只有正文才有」的留痕（外部门禁方抽验 + 本报告自证）

以下短引**均来自剥除摘要后的正文**，用于证明 `精读原文` 标签不是虚标。每处 ≤15 行，标注来源与章节锚点。

**(a) 外部门禁方抽验的两句——复核结论：站得住，且均可定位到正文**

1. `arXiv:2609.24574`（CSS 18 任务横评），正文 §4.1 与结论段：

   > Across the 15 evaluation tasks, Jev reaches a median accuracy of 0.610 and a median macro-F1 of 0.581, a median deficit of 11.6 macro-F1 points to the per-task best LLM, and the deficit is significant after correction on 12 of the 15 tasks.

   > On accuracy, the decision model is not a substitute for a frontier LLM. It trails the per-task best baseline on 14 of 15 evaluation tasks, by a median of 11.6 macro-F1 points…

   > For annotation pipelines, our results support a division of labor rather than a replacement. … on those tasks the measured savings are 35 and 44 times (Appendix B).

   复核：`11.6 macro-F1`、`35 and 44 times`、`0.815`（>0.9 置信段中位准确率）、`0.157`（frontier 中位校准误差）**均在剥摘要后的正文命中**；摘要中反而不含 `35 and 44`。原文另可直接定位"共情任务上高置信度却接近随机"的机理（`the empathy failure is shared across model families`）。

2. `arXiv:2609.23986`（Jev-Mem），正文 §5 结果与结论：

   > Table 1 summarizes the performance of Jev-Mem and the baselines on LoCoMo. Jev-Mem achieves the highest overall LLM-as-a-Judge score of 0.777, compared with 0.700 for the strongest baseline, corresponding to an 11.0% relative improvement.

   > Its total memory build time is only 158 seconds, compared with 1,044 seconds…

   > Jev-Mem also achieves the lowest query latency, requiring only 0.93 seconds per query on average. This is 36.7% lower than the fastest memory-based baseline at 1.47 seconds…

   复核：`0.777`、`158 seconds`、`0.93 seconds`、`36.7%`**均在正文命中**。说明：该文正文同时含"…0.777, an 11.0% relative improvement…"一句（与摘要措辞高度重合），故**仅凭该串无法区分摘要与正文**；本报告以正文独有的 `158 seconds` / `1,044 seconds` / `0.700` 作为判别依据。

**(b) 本报告补充自证（同一抽验流程，正文独有数字）**

- `arXiv:2609.24052`（事故叙述编码）：`5,018,080`、`195,857`、`$0.154 per thousand`、`factor of 3.3`、`not calibrated as delivered` 均在正文命中；后两句是"独立审计发现按交付状态未校准""重校准使校准误差降 3.3 倍"的直接出处。
- `arXiv:2609.30243`（JevOut）：`61.4%`、`64.9`、`73.2`、`16.9`、`2.2` **均在正文命中**（`16.9`/`2.2` 反而**不在**摘要），支撑"另一系统目标翻转率 64.9%–73.2%""单次 target-aware 添加 16.9%、单次中性添加 2.2%"的对照。
- `arXiv:2609.26758`（选项名 vs 定义）：正文原句可定位机理与边界——`Erasing the names' semantics entirely, with random character strings, leaves the decision exactly where neutral identifiers already leave it, at no cost in accuracy: polarity is what the swap exploits, not the name's content`，以及 `each option is named by a random 5-character string over letters and digits`。
- `arXiv:2609.23136`（6G O-RAN）：`22.4`、`61.9`、`53.0`、`459`、`463`、`435`、`1,080` 均在正文命中。

**假阳性剔除记录（避免把正确引用误降）**：第二轮抽验初期曾把三条**探测串写错**而误判为"仅摘要"，复核后**全部撤销降级**：① `2609.24395` 的 `0.824`——正文以**表体** `S4 | Combined | 0.824 | 0.840` 与叙述 `PLCC 0.824, SROCC 0.840` 双处呈现，探针误把 PLCC 与 SROCC 拼成一串；② `2609.26758` 的 `five-character`——正文写作 `random 5-character string`；③ `2609.26532` 的 `64.9`——该量值属 §6.4 的 JevOut（`2609.30243`，其正文已命中），不在 REFLEX 论文中，本就不应作为降级依据。**最终实际降级 2 处主张、1 篇论文**（§1.2.1 降级表）。

---

## 二、定义与判据：决策模型与生成式 LLM 的差别

### 2.1 官方定义框架

TypeSafe 把 Jev 定位为 **System One 模型**（"first System One model"），命名取自 Kahneman《思考，快与慢》的 System 1（快、直觉），强调"快速、聚焦的判断"，与 System 2 的慢速推理相对（[官方 System One 文档](https://docs.typesafe.ai/concepts/system-one)，精读原文·官方文档）。官方对交互契约的表述是：**unstructured state in, typed probabilistic decisions out**——像 LLM 一样理解自然语言输入，但返回**类型化决策与概率**，而不是生成的文本。

官方同时给出"机器原生（Machine Native Intelligence）"的动机叙事：大规模自动化将主要是机器-机器交互，因此"结构、可靠、可观测、可测试、快、一致、便宜"比"读起来让人满意"更重要（[官方 AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer)，精读原文·官方文档）。

### 2.2 判据一：类型化输出（Choice / Score / Noul）

官方只暴露三种原语（question type），每种返回不同形状的答案（[官方 Primitives 文档](https://docs.typesafe.ai/primitives)，精读原文·官方文档）：

| 原语 | 回答什么问题 | 返回字段 | 语义定位 |
|---|---|---|---|
| **Choice** | 在已声明选项中选哪一个？ | `choice`、`probabilities`（全选项分布）、`confidence` | 映射到 `switch`/`match` 分支 |
| **Score** | 处在哪个档位？ | `score`（可落在两档之间）、`legend`、`probabilities`、`confidence` | 映射到阈值比较 |
| **Noul** | 该判断是否为真？ | `noul`（0–1 的单个概率） | 映射到 `if` |

三个关键约束（均见官方文档，精读原文）：

1. **答案空间由请求方定义**，模型返回的是在**你给的选项/档位上的概率分布**，"永远不可能返回这个分布之外的取值"；
2. **Noul 没有独立的 `confidence`**——那个概率本身就是答案；官方建议若要统一门控，用 `|2p − 1|` 把它搬到与 Choice 相同的 0–1 尺度；
3. `Noul` 不是 `bool`，`Score` 不是整数——创始人在访谈中明确说这是**有意设计的新概念**，直接塞进现成整数/浮点类型"开发者很容易误解"（[Founder Park 整理的创始人访谈](https://www.geekpark.net/news/371794)，二手·访谈整理，2026-10-16）。

> **术语考据**：`Noul` 的命名由来据 Simon Willison 引述 CEO 在 Hacker News 的确认，是取自 **Bernoulli 分布**，并非 "yes/no" 的合成词（[Simon Willison's Weblog](https://simonwillison.net/2026/Sep/21/jev/)，二手·技术博客，2026-10-16）。这属于命名来源说明，不影响契约语义。

### 2.3 判据二：隐藏状态直读候选、零输出 token

官方口径是"一次前向、并行给出所有答案"，且"不生成文本"（官方文档，精读原文）。第三方对其**实现机理**的描述更具体：合法输出空间在调用前枚举好，模型在结构上不可能产生类型错误（[腾讯云分析](https://cloud.tencent.com/developer/article/2750505)，二手·技术分析）。但**官方未公开 readout 的数学形式**，社区对"双向编码器 + 并行标签头"或"LM head 上读标签 token 概率"的推测**属于推测，不作为本报告结论**（见 §9）。

开源复刻提供了两种可核验的实现范式（均为**第三方实现**，非官方口径）：

- **LM-head readout**：`jev-lite` 用 QLoRA 把 Gemma 4 E4B 转成决策模型，答案从选项字母位置的 logits 读出，因而"不可能回答给定选项之外的内容；没有解析、没有重试循环"（[vagmi/jev-lite 模型卡](https://huggingface.co/vagmi/jev-lite)，二手·模型卡，2026-10-16）。
- **专用 scorer head**：`this-that-model-1.0` 把答案从指定位置的隐藏状态读出，再对**你声明的标签 token** 打分并按这些标签归一化，其概率分布的**支撑集就是选项表**——"选项之外的答案是**不可表示的**，不是概率低"；支持最多 255 个选项（[this-that-model-1.0 模型卡](https://huggingface.co/flock-io/this-that-model-1.0)，二手·模型卡，2026-10-16）。
- **Laya** 的做法是每个选项在自己的 `[MASK]` token 处打分，再在该题选项上做 softmax，答案空间在请求时定义、新 schema 无需重训（[Laya 模型卡 UPSTREAM_README](https://huggingface.co/convaiinnovations/laya)，二手·模型卡，2026-10-16）。

> 三种 readout 殊途同归到同一个**契约性质**：输出支撑集 = 声明的选项集。这就是"类型错误不可能"的来源，也是"零输出 token"的来源——没有解码循环，也就没有 token 预算、没有字母误解析、不需要 `try/except`。

### 2.4 判据三：`confidence` 的语义

官方对 `confidence` 的定义（[官方 Confidence 文档](https://docs.typesafe.ai/confidence)，精读原文·官方文档）：

- Choice/Score 的每个答案都带 `probabilities`（全选项/全档位分布）；`confidence` 是**把这个分布的"尖锐程度"折叠成的单个 0–1 标量**：所有概率集中在一个结果是 1，概率均匀铺开是 0。
- Noul 不返回 `confidence`，概率本身承载不确定性；如需统一门控，用 `|2p − 1|`。
- 官方明确说明：**`confidence` 只是"一种合理的分布摘要，不是唯一一种"**；公式精确、`probabilities` 完整返回，因此你可以自己计算任何更契合业务的度量。
- 官方推荐的代码路径是三段门控：高置信度自动执行 / 中置信度确认或复核 / 低置信度不执行、转人工或换系统；且**阈值随风险分级**（只读操作与破坏性操作的门槛不同）。

**一个必须写清的边界**：校准是"在一组预测上"度量的性质，**不保证单条答案正确**（官方 System One 文档原文即如此表述）。

第三方对 `confidence` 的实证有分歧，值得并置：

- **支持**：`jev-lite` 在 1,430 条金标注留出行上比较了 `p_max`、归一化熵、margin、chance-corrected top、碰撞熵，**`p_max` 在 AUROC 与 ECE 上都最好，而归一化熵这个"显然的第一直觉"最差**（模型卡，二手·模型卡）。
- **反对/修正**：Laya 模型卡自述其 base checkpoint **出厂即过度自信**，按（题型 × 选项数）重新拟合温度后平均 ECE 从 0.466 → 0.081；并明确提醒"在自己数据上先做这一步再信任概率"（模型卡，二手·模型卡）。
- **独立审计**：事故叙述编码研究**独立**测量了 Jev 的概率校准，结论是"typed model 与其中一个 frontier 分支**按交付状态并未校准**，而另一个 frontier 分支是校准的"，并进一步指出"**校准随模型而变，而非随范式而变**，每个模型都必须单独审计"（[arXiv:2609.24052](https://arxiv.org/abs/2609.24052)，精读原文·预印本）。

### 2.5 判据四：共享状态的多问题并行

官方对并行性的表述（[官方 Primitives 文档](https://docs.typesafe.ai/primitives)，精读原文）：

- "请求中的每个问题看到**同一个 state**，被**独立评估**，并在你选择的 ID 下返回类型化答案"；
- 官方推荐 `speculative fan-out`：把系统可能需要的**所有**问题放进**一次**调用（含投机性、可能用不上的问题），再用代码判断哪些结果相关；理由是"所有问题并行评估，加问题**通常对响应时间影响很小**"（[官方 Speculative fan-out 文档](https://docs.typesafe.ai/patterns/fan-out)，精读原文·官方文档）。

第三方对该性质的独立量测与上述定性一致，且给出量级：

- Visual Jev 在共享视觉上下文、`N=32` 时，**共享批执行比"已批处理但重算前缀"的路径快 8.9×**（warm amortized time），代价是更高的峰值内存（[arXiv:2609.25845](https://arxiv.org/abs/2609.25845)，精读原文·预印本）。
- `this-that-model` 独立实现同一性质："关于同一 state 的多个问题在**同一次前向**中回答，因为答案不会被写回 prompt，且给定输入时各决策条件独立"（模型卡，二手·模型卡）。

**口径提醒**：并行≠免费。官方文档同时规定两层上下文上限——`per_request_context`（state + 全部问题）与 `per_question_context`（state + 任一问题），**问题数量本身无独立上限**（[官方 Models 文档](https://docs.typesafe.ai/models)，精读原文·官方文档）。也就是说 fan-out 的真实代价是 **state 被每个问题重复计入上下文**，用 token 换往返次数。

---

## 三、训练目标：RLCD（Reinforcement Learning for Calibrated Decisions）

### 3.1 官方自述的定位

官方把后训练路径讲成三选一（[官方 AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer)，精读原文·官方文档）：

| 路径 | 优化靶子 | 官方对它的评价 |
|---|---|---|
| RLHF | 人类偏好 | 把预训练模型变成聊天机器人；训练"产出人们偏好的回复" |
| RLVR | 可验证奖励 | 造就了数学等强推理模型，但"更慢更贵" |
| **RLCD** | **经过校准的决策** | TypeSafe 的路径：**返回决策与校准概率，而非生成文本** |

官方对 RLCD 的**输出契约**描述（同一 primer，精读原文）：

- 模型不生成文本；
- 返回决策与概率；
- **更高的概率应对应更大的"答案正确"的可能性**；
- 校准的意义在于让"不确定性可被软件使用"：赋 0.2 概率的结果应约有 20% 发生，赋 0.8 的应约有 80% 发生。

官方另在 Models 文档中确认**不使用客户数据做微调或 LoRA**，全部账户共享同一套权重，"用 RLCD 训练以返回校准决策"（精读原文·官方文档）。

### 3.2 必须消歧：两个同名 RLCD，方法完全不同

这是本专题最容易被写错的一点，务必逐条对照：

| | **本报告讨论的 RLCD** | **同名但不同物的 RLCD** |
|---|---|---|
| 全称 | Reinforcement Learning for **Calibrated Decisions** | Reinforcement Learning from **Contrastive Distillation** |
| 出处 | TypeSafe 官方 AI primer（2026）；Jev 产品文档 | [arXiv:2307.12950](https://arxiv.org/abs/2307.12950)，ICLR 2024（本报告仅按摘要级引用，见 §1.2.1） |
| 作者/年份 | TypeSafe（未具名论文） | Kevin Yang, Dan Klein, Asli Celikyilmaz, Nanyun Peng, Yuandong Tian；2023-07-24 投稿，2024-03-16 修订 |
| 目标 | 让类型化概率**校准**、可用于门控 | 让语言模型**对齐自然语言表述的原则**（无害性、有用性、故事大纲生成） |
| 机制 | 官方未公开算法细节 | **用正/负两种 prompt 设计制造对比输出 → 构造偏好对 → 训练偏好模型 → 再做 RL** 提升基础未对齐模型 |
| 是否用人类反馈 | 官方未说明标注来源 | **不使用人类反馈** |
| 是否生成文本 | **不生成**（契约即"无输出 token"） | **生成**（对齐的是生成式模型的输出分布） |
| 评测对象 | 类型化概率的校准与决策正确率 | 三项对齐任务上优于 RLAIF 与 context distillation 基线 |

**结论**：两者只共享四个字母。引用时必须写明全称；把 2023 年那篇当作"Jev 的训练配方出处"是**事实错误**——该论文既没有决策模型，也没有概率校准目标，也不涉及类型化输出。

### 3.3 第三种 RLCD 解释（开源复刻）

开源复刻 **Laya** 的模型卡把 RLCD 写成 "Reinforcement Learning for Calibrated Decisions"，并给出**它自己的**机制描述："策略输出一个分布；探索在 logits 上加零均值高斯噪声；训练用**严格 proper scoring rule** 做奖励，因此诚实报告概率是唯一最大化奖励的方式"（[Laya 模型卡](https://huggingface.co/convaiinnovations/laya)，二手·模型卡，精读该卡正文）。

这属于**第三方对同名概念的自主实现与解释**，不是 TypeSafe 官方算法披露。写"RLCD 用 proper scoring rule 做奖励"时必须注明来源是 Laya 而非 TypeSafe。这恰好印证 §3.2 的教训：**同一缩写在本专题内至少有三套互不相同的含义，逐文核对定义是硬要求。**

### 3.4 可信度评价

| 问题 | 现状（截至 2026-10-16） |
|---|---|
| TypeSafe 是否公开 RLCD 算法细节？ | 否。官方只给目标与契约层面的描述 |
| 是否有同行评审论文？ | 未检索到。第三方索引仓库独立记录"截至 2026-10-14 未定位到同行评审的 TypeSafe 架构或 RLCD 论文"（二手·索引仓库） |
| 是否有独立复现其训练配方？ | 未见复现**原配方**者；开源复刻是**独立设计**（各自的读出头、各自的训练数据），只能算"同契约异构实现" |
| 训练数据来源？ | 官方未披露标注来源、样本量、语言分布 |

因此，本报告把 RLCD 一律标记为**厂商自述（一手但自述）**：可以引述其声明，不可当作已核验的方法学结论。

---

## 四、官方材料边界：有什么、没有什么

### 4.1 官方已发布材料盘点（均实测可达）

| 材料 | 链接 | 内容性质 | 证据 |
|---|---|---|---|
| 介绍 / 快速开始 | [docs.typesafe.ai/introduction](https://docs.typesafe.ai/introduction) | 产品定位与上手 | 精读原文·官方文档 |
| System One 概念 | [concepts/system-one](https://docs.typesafe.ai/concepts/system-one) | 与 LLM 的差别、原语总览 | 精读原文·官方文档 |
| State 概念 | [concepts/state](https://docs.typesafe.ai/concepts/state) | state 的形状与组织 | 精读原文·官方文档 |
| Primitives | [primitives](https://docs.typesafe.ai/primitives) | Choice/Score/Noul 契约 | 精读原文·官方文档 |
| Confidence | [confidence](https://docs.typesafe.ai/confidence) | 置信度定义与公式 | 精读原文·官方文档 |
| **模型文档** | [models](https://docs.typesafe.ai/models) | 版本、价格、上下文、语言支持 | 精读原文·官方文档 |
| **AI primer** | [machine-learning-primer](https://docs.typesafe.ai/introduction/machine-learning-primer) | RLCD 与后训练三路线 | 精读原文·官方文档 |
| **Jaggedness 九类弱点** | [model-jaggedness/jev-1.13](https://docs.typesafe.ai/model-jaggedness/jev-1.13) | 官方自陈失效模式 | 精读原文·官方文档 |
| 模式（fan-out 等） | [patterns/fan-out](https://docs.typesafe.ai/patterns/fan-out) | 推荐架构模式 | 精读原文·官方文档 |
| 图像（Dreamer-ready） | [images](https://docs.typesafe.ai/images) | 图像与 Box 原语 | 精读原文·官方文档 |
| 创始人访谈整理 | [geekpark.net/news/371794](https://www.geekpark.net/news/371794) | 动机与设计取舍 | 二手·访谈整理 |
| 官方模型/价格页 | [models](https://docs.typesafe.ai/models) | `jev-1.14.0` 于 2026-10-14 发布 | 精读原文·官方文档 |

### 4.2 官方**没有**发布的东西（重要）

- **没有正式技术论文**（无 arXiv、无 PDF 预印本、无期刊投稿），也没有架构图或超参披露；
- **没有公开权重**（closed-weight 商业 API；官方明示不按客户数据微调、全账户共享权重）；
- **没有公开 RLCD 算法细节、训练数据构成、评测集**；
- **没有公开 readout 的数学形式**（社区推测见 §9）。

因此，"Jev 是双向编码器"、"Jev 用 LM head 读标签 token"、"TypeSafe fork 过 LLaDA 因此有扩散谱系"之类说法**在官方材料中查无实据**，只能作为待跟踪推测。

### 4.3 官方模型与定价事实（精读原文·官方文档）

| 项 | jev-1.13.0 | jev-1.14.0 |
|---|---|---|
| 别名 | `jev-latest`（最稳定官方版，SDK 默认） | `jev-preview`（最新，含 preview） |
| 发布 | — | 2026-10-14 |
| 价格 | $42 / Btok 输入，**$0.042 / Mtok 输入** | 同左 |
| 输出计费 | **免费**（"你只为输入 token 付费，输出 token 免费"） | 同左 |
| 上下文 | 64k per-request / 32k per-question；开 `TypeSafe-Danger-Zone-Long-Context: true` 后 262k | 同左 |
| 输入模态 | 文本 | 文本 |
| 图像 | 1.13 与 1.14 **都接受图像**；`Box` 原语**仅 1.14** | 同左（+Box） |
| 语言 | 英语为主训练语言、准确率最好；**CJK 等其它语言"被处理但不同等好"** | 同左 |

> **两点必须记住**：(a) 别名会漂移，答案可能随发布变化而变，**响应里的 `model` 字段给出实际应答的版本化 ID**，应记录它；若按某版本调过阈值，就写版本化 ID 而非别名。(b) Long context 与 Images 都走 `TypeSafe-Danger-Zone-*` 头，官方自称图像与 Box"尚未达到可称生产就绪的标准"，属 **Dreamer-ready**（原型可用、格式与准确率可能随发布变化）。

### 4.4 官方自陈的九类 jaggedness（jev-1.13，官方原文）

官方弱点清单（[model-jaggedness/jev-1.13](https://docs.typesafe.ai/model-jaggedness/jev-1.13)，精读原文·官方文档，官方标注 "Last reviewed 2026-10-02"）开篇即自陈：`jev-1.13` 快、校准、常识判断好，但**不完美**；在 System One 任务上表现最好，**需要额外层间接续（indirection）的任务可能吃力**，理解**相当字面**，**数值精度吃力**。

| # | 失效模式 | 官方建议的替代做法 |
|---|---|---|
| 1 | **字面阅读**（读你写的、不是你想的） | 把确切条件写进 `instructions`，边界情况写进 `criteria` |
| 2 | **数学与数字**（不是计算器，不擅长计数） | 算术放代码里；逐项问、自己加总 |
| 3 | **日期时间比较**（把日期当文本读，不是有序量） | 抽组件（Choice 枚举），排序/时长/偏移交代码 |
| 4 | **间接层**（双重否定、复杂间接） | 减少跳数，直接指向相关 state |
| 5 | **大 state 中塞满无关细节** | 先过滤，只发问题需要的内容 |
| 6 | **对抗性内容** | 写精确 prompt，部署前测边界用例 |
| 7 | **指令与条件互相矛盾** | 对齐 criteria 与 instruction |
| 8 | **选项顺序** | 重排选项并检查答案是否一致 |
| 9 | **生成任务** | 用生成式模型（Jev 不做这个） |

官方还给出若干**语义 vs 数值**的具体经验（同一页，精读原文）：颜色用英文名比用 hex/RGB 更好；问高层编程语言比问汇编/二进制编码指令更好；`score` 的档位**弱于数值校准**，可用期望值判断是否过阈值，但**不要用它反推精确数字**。

---

## 五、厂商效率主张的口径审计

### 5.1 193.6× / 444.6× 的真实出处与限制

媒体与二手分析转述：官方**工作流自评**给出"快 193.6 倍、便宜 444.6 倍"，且**官方自己标注为偏乐观的上限**（[腾讯云分析](https://cloud.tencent.com/developer/article/2750505)，二手·技术分析）。

**本报告的处理**：

- 该组倍率**不是**、也不可作为**通用加速比**；
- 一手出处为厂商自测页（写稿时**未在官方文档站点定位到该自评原文**，故本报告不把 193.6×/444.6× 写成"官方文档数据"，只记录为"媒体转述的厂商自评，且厂商自标为乐观上限"）；
- 任何引用该数字的写法都必须**同时给出对照模型、缓存策略、工作负载假设**，否则属于 §6.2 定义的不可用效率主张。

### 5.2 官方文档中可核验的、有明确边界的口径

| 主张 | 官方原文要点 | 为什么不能通用化 |
|---|---|---|
| 零输出 token、输出免费 | "只为输入付费，输出 token 免费" | 只说明计费结构；不含缓存、重试、渲染成本 |
| 多问题并行、加问题对时延影响小 | "所有问题并行评估，加更多问题通常对响应时间影响很小" | 问题数不进 token 预算，但 **state 被每题重复计入**；文档另设 per-request/per-question 双层上限 |
| 图像/Box 可用 | "1.13 与 1.14 都接受图像；Box 需 1.14" | 官方自标 **Dreamer-ready**、未达生产标准，格式与准确率会随发布变化 |
| Long context 262k | 打开危险区头即可 | 同价但**更慢更不准**，官方建议只在必要时开 |
| 语言支持 | "英语为主训练语言、准确率最好；CJK 等被处理但不同等好" | 非英语工作负载**必须自测** |

### 5.3 第三方对 Jev 速度的独立量测（口径各异，不可并表）

| 来源 | 量测 | 样本/条件 | 证据 |
|---|---|---|---|
| Laya 模型卡（转引两个第三方基准仓库） | Jev p50 **236–276 ms** | 转引 AbdelStark / nibzard 的第三方基准 | 二手·模型卡 |
| 边缘编排研究 | 决策时延中位降 **15.9–26.5%**；无缓存时端到端中位降 **11.1–25.3%**；每次**正确完成**的 API 费降 **69.0–70.6%** | 三个连续测量块，8 个条件，对照简洁结构化输出的 DeepSeek 部署 | 精读原文·预印本 |
| 6G O-RAN 研究 | 决策时延中位降 **22.4%**（vs DeepSeek）、**61.9%**（vs Gemini）；另设 direct-attribute Qwen 对照仍保留 **53.0%** 降幅 | RIC 时间尺度，契约解释正确性配平 | 精读原文·预印本 |
| 科学决策研究 | "在成功响应中取得**最低观测中位时延**"（与另外 5 种配置并列达到完全语义正确） | 结构化科学决策任务 | 摘要级·预印本（仅摘要：该措辞在剥摘要后的正文查无，见 §1.2.1） |

> 这些数字**互相不可比**：对照模型不同、任务不同、是否配平正确率不同、是否含缓存不同。本报告**不做跨论文排行榜**，只逐条保留其口径。

---

## 六、第三方研究地图

> 说明：以下全部为 2026-09/10 的 arXiv 预印本或开源模型卡。`subject: jev` 的文献图由第三方索引仓库 [Awesome JEV Papers](https://github.com/Oscar-dzy/Awesome-jev-papers)（二手·索引仓库）提供导航，其声称收录 174 条、其中 161 条学术预印本；**本报告只引用其中可被本 Agent 独立核验编号与标题的一手论文**。

### 6.1 应用类：把有界判断换成决策模型调用

| 论文 | 编号 | 领域 | 关键结论 | 证据 |
|---|---|---|---|---|
| Replacing Large Language Models with Jev Decision Models for **Low-Latency Edge Service Orchestration** | [2609.22753](https://arxiv.org/abs/2609.22753) | 边缘服务编排 | 提取 4–8 个有界意图字段；决策时延中位降 15.9–26.5%；**提速集中在"首次解释"**，重复请求缓存会消掉大部分差距 | 精读原文·预印本 |
| **Intent Interpretation at RIC Timescales**: Jev Decision Models versus LLMs in 6G Open RAN | [2609.23136](https://arxiv.org/abs/2609.23136) | 6G / O-RAN | 决策模型返回类型化策略字段、生成式模型逐 token 产出策略；配平解释正确率后时延降 22.4%/61.9%，建模场景完成率 +3.50/+8.35 个百分点 | 精读原文·预印本 |
| **Calibrated Decisions at Scale**: Converting Police Crash Narratives into Probabilistic Crash Variables | [2609.24052](https://arxiv.org/abs/2609.24052) | 公共安全数据 | 筛 499,500 条德州叙述、按 27 问 schema 编码 195,857 条，实测 **$0.154/千条**，全 5,018,080 条外推 **$774**；**独立审计发现 typed model 按交付状态未校准**，重校准使校准误差降 **3.3 倍** | 精读原文·预印本 |
| Jev for **Scientific Decisions**: Evaluating Semantic Choices and Their Consequences | [2609.24965](https://arxiv.org/abs/2609.24965) | 科研工作流 | 前提是"先选已知关系、再做确定性计算"；Jev 与另外 5 种配置并列达到完全语义正确（正文可证）；"取得最低中位时延"一说**仅在摘要**，正文查无（见 §1.2.1）；强调**错误的关系会被代码精确执行并产出错误的科学结果** | 精读原文·预印本（"最低中位时延"单条为摘要级） |

**应用类共性**：这些研究都把 Jev 放在"有界语义判断"的位置，把算术/排序/传播留给代码——与官方 jaggedness 的第 1–3 条建议同向。它们的收益多在**延迟与费用**，而非任务正确率。

### 6.2 "Jev-Anything"：把系统一放到 Agent 的关键路径上

| 论文 | 编号 | 做法 | 关键结论 | 证据 |
|---|---|---|---|---|
| **Jev-Mem**: System-One-Controlled Agentic Memory for Efficient AI Agents | [2609.23986](https://arxiv.org/abs/2609.23986) | 写入路径做记忆分型/冗余过滤/关系构建，读取路径做查询路由/预算分配/图遍历/候选打分/自适应停止 | LoCoMo 上 LLM-as-a-Judge **0.777**（相对最强基线 +11.0%），构建时间 **158 s（6.6× 提速）**，平均查询延迟 **0.93 s（−36.7%）** | 精读原文·预印本 |
| **REFLEX** with Jev for Efficient Selective Control in LLM Agents | [2609.26532](https://arxiv.org/abs/2609.26532) | 高置信度动作直接执行，低置信度或需生成才上抛强模型 | τ 风格任务上相对"只用强模型"成本降 **3.7×**（正文可证），成功率差异统计上未分辨；**外部基准上收益有限**；⚠️ 更大的动作集与"结构上近似合法"的备选会**降低授权边界处的准确率** | 精读原文·预印本 |
| **JEV-as-a-Judge**: Accept When Confident, Escalate When Unsure | [2609.26550](https://arxiv.org/abs/2609.26550) | 决策模型只返回标签概率，用置信度决定接受或上抛推理型评判者 | 与 16 个生成式/reward 评判者对比、人工盲审：常规偏好与证据事实性上与最强 LLM 评判者**差距 ≤3 个百分点**（摘要表述；正文以具体基准给出），费用仅其 **0.36%（仅摘要，正文查无，见 §1.2.1）**；**需检查推导过程**的任务差距拉大；"冻结级联"保留最强评判者 **99%** 准确率（正文可证） | 精读原文·预印本（"0.36%"单条为摘要级） |
| **JEVQA** — Video Quality from Metadata, Bitstream, and Pixel Features with a General-Purpose Decision Model | [2609.24395](https://arxiv.org/abs/2609.24395) | 用决策模型从零样本特征预测视频质量（1,936 个 PVS 对 VMAF） | 仅元数据/像素特征时不稳：**像素单独近乎无信息（PLCC 0.226）**，加 bitstream 后显著提升，**联合电平取得最高零样本相关性（PLCC 0.824 / SROCC 0.840）**；但**同特征监督训练模型仍领先**（如 P.1204.3 在此子集 PLCC 0.950 vs JEVQA 0.818；同特征 ExtraTrees 0.951） | 精读原文·预印本（原误标摘要级，第二轮核验命中正文 Table I 表体与 §IV-A 叙述后按"对源"原则改正） |
| **Visual Jev**: Accurate and Efficient Decisions from Shared Visual Context | [2609.25845](https://arxiv.org/abs/2609.25845) | 图像与公共上下文编码一次，把各问句后缀作为批量执行，从 LM head 读候选概率 | 答案监督后训练把等权 macro 准确率从 **0.706 → 0.761**（增益集中在已见任务族）；**共享批执行在 N=32 时快 8.9×**，代价是更高峰值内存；匹配的 typed-head 对照无一致准确率优势 | 精读原文·预印本 |

**Jev-Anything 的共性风险（本报告的综合判断，非单一论文结论）**：这一族的收益来源都是"把高频、有界、低风险的判断从生成循环里挪出去"。它们同时暴露同一个脆弱点——**级联的正确性完全依赖置信度阈值在分布外输入上的行为**，而 §7.3 列出的独立证据恰好指向"高置信度 + 近随机"的失败场景。

**旁证（仅摘要级，未进正文结论）**：下列研究与本族同题，本报告只读题录/摘要，列出以备后续跟踪，不作为任何结论依据。

| 论文 | 编号 | 为何相关 | 证据 |
|---|---|---|---|
| System Switch: When Should a Fast Decision Model Stop and Think? | [2610.09683](https://arxiv.org/abs/2610.09683) | 双过程 Agent：快速策略模型承担每一步决策，何时把控制权交给慢速深思模型；本报告 §6.2 的"级联/升级"议题与之直接重叠 | 摘要级·预印本 |
| Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms? | [2609.33209](https://arxiv.org/abs/2609.33209) | 检验同一 state 上逻辑相关问题之间的概率是否自洽（item-by-item 一致性）——官方 `confidence` 语义（§2.4）尚未覆盖这一层 | 摘要级·预印本 |
| Just Ask Jev: RLCD as a Zero-Shot Detector of AI Alignment Failures | [2609.29429](https://arxiv.org/abs/2609.29429) | 把 typed 概率用于对齐失效检测，是对"决策模型作评测器"的另一条应用线 | 摘要级·预印本 |

### 6.3 横评：与生成式 LLM 的同题对照

| 论文 | 编号 | 设计 | 关键结论 | 证据 |
|---|---|---|---|---|
| **Evaluating Decision Models for Text Annotation in Computational Social Science** | [2609.24574](https://arxiv.org/abs/2609.24574) | 18 个 CSS 分类任务 / 7,977 项，第一个商用决策模型 + 两个开源权重对照 vs 19 个 frontier 与开源 LLM，统一 zero-shot 协议 | 决策模型在 15 个评测任务中 **14 个落后**单任务最优 LLM，中位差距 **11.6 macro-F1**，但实测成本中位低约 **44 倍**；其置信度校准**优于 19 个 LLM 中的 16 个**，但有 3 个 frontier 模型中位校准误差更低（**0.157 vs 0.066**）；>0.9 置信度项通常标得准（中位准确率 0.815），**但在"同伴支持对话中的共情"这一任务上高置信度却接近随机**；把低置信度项路由给 LLM，成本仅为"直接全用 LLM"的 **1/4–1/2** 且效果持平或更好 | 精读原文·预印本 |
| **this-that-model-1.0**: A typed decision model that decides in 30 ms, for a millionth of a cent | [2609.23886](https://arxiv.org/abs/2609.23886) | 自建 1.88B 开源 typed 模型（Qwen3.5 风格混合，24 层中 18 层 DeltaNet 线性注意力）；在第三方录制的 68 题/17 状态上对照托管 Jev 与多家 frontier 模型 | 30.9 ms 单次决策、零输出 token；第三方题集上准确率 **0.941 / Brier 0.042** vs Jev **0.765 / 0.133**；作者**自陈成本口径不同**（自家按 80 W 电费估算，"读作约一个数量级而非五个"），且明示 Jev 的价格是官方挂牌价、准确率由己方测量 | 精读原文·预印本 |

> **横评的读法**：这两篇恰好示范了"口径不可合并"。CSS 横评是 zero-shot、多任务、含 77 类别的分类；`this-that-model` 是自带训练数据的**同契约异构模型**在第三方题集上的对照。两者都不能推出"Jev 强于/弱于 LLM"的通用结论——**这也是本报告不做排行榜的原因**。

### 6.4 失效与攻击：何时判断失灵

这一节是本专题**证据质量最高、也最值得工程采纳**的部分，因为三篇独立工作从三个不同角度命中了同一脆弱面。

| 论文 | 编号 | 攻击/失效面 | 关键结论 | 证据 |
|---|---|---|---|---|
| **Decision Hijacking**: Prompt Injection Attacks on Jev's Typed Probabilistic Decisions | [2609.28613](https://arxiv.org/abs/2609.28613) | 在 attacker 可控的 `latest_tool_result` 槽注入恶意内容 | 用 **510 条重建的 InjecAgent 用例**：恶意内容**系统性地移动动作概率**，但"**很少**让 Jev 选中攻击者目标"；高置信度劫持在 **2,550 次验证调用中仅同一 1 例**出现；**攻击不会从生成式 agent 原样迁移**；加"覆盖标记"可降低影响 | 精读原文·预印本 |
| **JevOut**: Natural Context Can Flip Decision Models | [2609.30243](https://arxiv.org/abs/2609.30243) | **短小、看似普通的上下文补充** | 7 个数据集 / 4 个决策系统：概率引导的上下文优化可在**保持原答案语义的前提下**把**初始答对**的决策翻到指定错误选项，目标翻转率 **61.4%**（95% Wilson 57.1%–65.5%）；另外三个决策系统在初始答对的决策上目标翻转率 **64.9%–73.2%**；**翻转常伴随高概率**；单次 target-aware 添加为 16.9%、单次中性添加为 2.2% | 精读原文·预印本 |
| **Type-Safe Is Not Error-Free**: Typed Decision Models Follow the Option Name, Not the Definition Bound to It | [2609.26758](https://arxiv.org/abs/2609.26758) | 选项**名称**与选项**定义**的语义冲突 | 每个选项 = 名称 + 定义；名称可提供**竞争性语义线索**；结论是"名称主导 rubric"、表现为**反转（inversion）而非混淆**、逐谓词成立、**极性被熟悉度放大**、在二元以上"名称几乎承载全部信息"；把选项名换成随机字符串则结果改变 | 精读原文·预印本 |

配套的**独立证据**（同属失效面，来自 §6.2/§6.1 的论文与模型卡，此处按"失效"重新归类）：

- **高置信度 + 近随机**：CSS 横评在"同伴支持对话共情"任务上观察到该现象（[2609.24574](https://arxiv.org/abs/2609.24574)，精读原文·预印本）。
- **置信度无法救场**：Laya 模型卡自报，其英语 checkpoint 对非拉丁脚本塌陷——**高棉语 0.000 准确率 / 0.952 置信度**，因此"**模型在错的时候依然自信，置信度门控救不了你**"，只能靠 Router 在**计费前**做脚本检测（模型卡，二手·模型卡）。
- **分布外会诚实**：`this-that-model` 模型卡给出反例——超出训练分布的问题返回"no (71%)"，即不确定而非自信（模型卡，二手·模型卡）。这说明"高置信度错误"是**可缓解但不可假定已解决**的属性。
- **授权边界**：REFLEX 的受控干预显示，更大的动作集与"结构上近似合法"的备选会降低授权边界处的准确率（[2609.26532](https://arxiv.org/abs/2609.26532)，精读原文·预印本）。

### 6.5 开源复刻地图（本报告只记录，不克隆）

> **纪律说明**：按本专题规则，**不 clone 任何第三方仓库**。以下只记录可从**项目主页/模型卡**读到的事实与其声明的许可证或开源状态。**未读取任何源码，因此不对实现细节作断言**。

| 项目 | 形态 | 声明的关键事实 | 证据 |
|---|---|---|---|
| **this-that-model-1.0** | 开源权重 + 推理代码 | 1.88B，Qwen3.5 风格混合（24 层中 18 层 DeltaNet）、MIT 许可证、30.9 ms、支持 ≤255 选项、声明结果可由推理仓库复现 | 二手·模型卡/预印本 |
| **Laya** | 开源权重（Apache-2.0）+ Router | 三个 checkpoint：ModernBERT-large 421M（英语，512 上下文）/ mmBERT-base 322M（多语言，1024–8k）/ 专用 typed-decisions；选项在各自 `[MASK]` 打分；声明 100+ 语言、T4 上 32.8–39.5 ms 单问 | 二手·模型卡 |
| **Kev** | Apache-2.0 权重 + GitHub 服务（GPU / Apple Silicon MLX） | 0.8B/4B/9B/27B 四档；"与 TypeSafe SDK 同 API，改 endpoint 与模型名即可切换"；27B 在作者自建六个评测面板上领先（作者自陈**非独立排行榜**）；吞吐/GPU 成本按 Modal 2026-10 挂牌价估算 | 二手·项目博客 |
| **jev-lite / jevlite** | QLoRA adapter + 自托管服务 | Gemma 4 E4B（4-bit NF4）+ LoRA（rank 16/alpha 32，34.9M/7.98B 可训练）；训练数据 23,632 行 / 301 任务；留出 1,898 行上 **准确率 0.816 / ECE 0.019**；输出支撑集 = 选项集 | 二手·模型卡 |
| **Open-Jev**（开源实现，被第三方论文评测） | 小语言模型的一趟式筛查 | CallScreenBench 上做"每次通话轮次后给出可信概率"的一趟式诈骗筛查 | 摘要级·预印本 |

**重要区分**：这些项目实现的是**同一个接口契约**（类型化问题进、校准概率出、零生成），**不是 TypeSafe 的算法**。它们的表现（无论好坏）都不能用来推断 Jev 的内部机制。

---

## 七、三类主张分开写

> 本专题的硬规则：**能力 / 效率 / 失效必须分栏陈述**，且**不做跨论文排行榜**。下表的每一行都可独立成立或独立被推翻。

### 7.1 能力主张（能否完成任务）

| 主张 | 支持证据 | 反证 / 边界 | 主等级 |
|---|---|---|---|
| 输出被约束在声明选项内，类型错误在构造上不可能 | 官方契约 + 三种独立 readout 实现（§2.3） | **仅格式保证**：仍可在给定选项中选错 | 精读原文·官方文档 |
| 适合"有知识的人一秒能做出的判断" | 官方原语设计指引 | 官方明确点名"分析并给出最佳行动方案"**不是**合适问题 | 精读原文·官方文档 |
| 常规偏好与证据事实性评判接近最强 LLM 评判者 | JEV-as-a-Judge：差距 ≤3 个百分点（摘要表述；正文以具体基准给出）、费用 0.36%**（仅摘要，正文查无）** | **需检查推导过程**的任务差距拉大 | 精读原文·预印本（"0.36%"单条为摘要级） |
| 分类/标注任务上可作**流水线第一步** | CSS 横评：低置信路由让成本降至 1/4–1/2 且效果持平或更好 | 15 任务中 14 个落后单任务最优 LLM，中位差 11.6 macro-F1 | 精读原文·预印本 |
| 多问题共享 state、可并行 | 官方契约 + Visual Jev 8.9× 共享批、this-that-model 同前向 | state 被每题重复计入，双层上下文上限 | 精读原文 + 二手·模型卡 |
| 零样本通用质量预测"有前景" | JEVQA：pixel+bitstream 组合 0.824 | **同特征监督训练的专用模型仍明显领先** | 精读原文·预印本 |
| 不适合：数值精度、计数、日期排序、生成 | 官方 jaggedness 九条自陈 | — | 精读原文·官方文档 |

### 7.2 效率主张（延迟与成本——**必须连对照模型、缓存与工作负载假设一起给**）

| 主张 | 倍率/数值 | 对照模型 | 缓存假设 | 工作负载 | 主等级 |
|---|---|---|---|---|---|
| 官方工作流自评 | 快 193.6× / 便宜 444.6× | 未在官方文档站点定位到原始自评页；厂商**自标为乐观上限** | 未公开 | 未公开 | 二手·技术分析（**禁止通用化**） |
| 边缘编排 | 决策时延 −15.9～26.5%；端到端 −11.1～25.3%；**每次正确完成**的 API 费 −69.0～70.6% | 简洁结构化输出的 DeepSeek 部署 | **无缓存**；同缓存策略下差距被重复请求缓存消掉 | 8 个条件、3 个连续测量块 | 精读原文·预印本 |
| 6G O-RAN | 决策时延 −22.4%（vs DeepSeek）、−61.9%（vs Gemini）；direct-attribute Qwen 对照仍 −53.0% | DeepSeek / Gemini / Qwen 三路 | 未述跨请求缓存 | RIC 时间尺度、契约解释正确性配平 | 精读原文·预印本 |
| 大规模编码成本 | $0.154/千条叙述；全州 5,018,080 条外推 $774 | 未与 frontier LLM 同表比价 | 不适用 | 10 问筛查 + 27 问编码 | 精读原文·预印本 |
| 评判替代 | 费用为最强 LLM 评判者的 0.36%**（仅摘要，正文查无；正文可证的是 RewardBench 94.0% vs 93.5%、保留 99% 准确率）** | 16 个生成式/reward 评判者 | 冻结级联（高置信接受/低置信上抛） | 多基准 + 人工盲审 | 精读原文·预印本（"0.36%"单条为摘要级） |
| Agent 控制 | 成本 −3.7× vs 只用强模型 | 强模型单臂 | 置信度门控 | τ 风格 300 回合 | 精读原文·预印本 |
| 记忆系统 | 构建 6.6× 提速、查询延迟 −36.7% | 最快的竞争记忆系统 | 不适用 | LoCoMo | 精读原文·预印本 |
| 第三方 p50 时延 | 236–276 ms | — | — | 单问 | 二手·模型卡转引 |

**读法**：任何一行都要连读"倍率 + 对照 + 缓存 + 工作负载"四要素。**193.6×/444.6× 不在同一口径族内，只能作为厂商宣传口径记录。**

### 7.3 失效主张（何时判断失灵、confidence 高但近随机的场景）

| 失效类别 | 具体表现 | 独立证据 | 主等级 |
|---|---|---|---|
| **选项名 vs 定义** | 名称语义极性盖过绑定的定义；表现为反转而非混淆；极性被熟悉度放大；二元以上"名称几乎承载全部信息" | [2609.26758](https://arxiv.org/abs/2609.26758) | 精读原文·预印本 |
| **普通上下文翻转** | 短小、保持原答案语义的上下文补充即可把**原答对**的决策翻到指定错误选项，**常伴随高概率**；四系统目标翻转率 61.4% / 64.9–73.2% | [2609.30243](https://arxiv.org/abs/2609.30243) | 精读原文·预印本 |
| **提示注入（概率层）** | 恶意内容系统性移动动作概率，但**很少**改变最终动作选择；高置信劫持极稀有 | [2609.28613](https://arxiv.org/abs/2609.28613) | 精读原文·预印本 |
| **高置信 + 近随机** | "共情"任务上高置信度却接近随机；**>0.9 置信度≠可靠** | [2609.24574](https://arxiv.org/abs/2609.24574) | 精读原文·预印本 |
| **跨语言塌陷 + 置信度不报警** | 非拉丁脚本 0.000 准确率 / 0.952 置信度；"模型错的时候依然自信，门控救不了你" | Laya 模型卡 | 二手·模型卡 |
| **交付状态未校准** | 独立审计发现 typed model 与一个 frontier 分支**按交付状态未校准**；重校准使误差降 3.3×；校准**随模型而变而非随范式而变** | [2609.24052](https://arxiv.org/abs/2609.24052) | 精读原文·预印本 |
| **分数概率可能不可用** | 某基准上 Jev 对真实标签给出 **零概率**的样本占 16% | Laya 模型卡转述 | 二手·模型卡 |
| **授权边界退化** | 更大动作集 + 近似合法备选降低授权边界准确率；错误在"不可逆承诺"与"延迟"之间按备选类型迁移 | [2609.26532](https://arxiv.org/abs/2609.26532) | 精读原文·预印本 |
| **官方自陈九类** | 字面阅读、数学/计数、日期比较、间接层、大 state 噪声、对抗内容、矛盾条件、选项顺序、生成任务 | [官方 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13) | 精读原文·官方文档 |

**工程含义（本报告综合判断）**：官方 §4.4 第 6 条与第 8 条（对抗内容、选项顺序）**已被三篇独立论文从不同角度坐实**，且两篇（JevOut、选项名）指向"高置信度错误"。因此 §4.3 建议的"三段门控"**必须配一条独立于模型置信度的外部防线**：脚本/语言检测、确定性校验、选项重排一致性检查、以及"高置信度抽样人工复核"。

---

## 八、评测复核清单

> 任何引用 Jev（或任何 typed decision model）数字的评测，都应按下列六项核查口径。空缺项即标注为"未报告"。
>
> **可执行版本**：本清单已落成 5 条带「假设 / 变式 / 指标 / 最小样本 / 结果判读标准」的实验协议，见子文档 [experiments.md](experiments.md)（含前置准备清单 P1–P8 与本节六项的映射表）。

### 8.1 数据

- [ ] **独立样本数**：与开发/训练集是否分离？给出条数而非比例（如 CSS 横评 7,977 项 / 18 任务；this-that-model 为 68 题 / 17 状态）。
- [ ] **语言**：英语以外是否单列？官方声明非英语"被处理但不同等好"，跨语言必须分表。
- [ ] **标注来源**：gold / 人工盲审 / 教师模型 / 合成？单次还是双标（如参考标签用另一模型盲标两遍）？
- [ ] **任务族切分**：hidden task family 与 held-out examples of trained families 是否分开报告（Kev 明确分开，值得照抄）。

### 8.2 版本

- [ ] **模型 ID**：写 `jev-1.13.0` / `jev-1.14.0`，**不要写 `jev-latest`**（别名会漂移）。
- [ ] **SDK 版本**与请求头（是否开 `TypeSafe-Danger-Zone-Images` / `-Long-Context`）。
- [ ] **提示词**：`instructions` / `criteria` 全文是否随结果发布？
- [ ] **选项排列**：顺序是否随机化、是否报告重排一致性（官方 jaggedness 第 8 条 + 选项名论文都指向这里）。
- [ ] **原语配比**：choice / score / noul 各自样本数与准确率（混合平均值会掩盖弱原语，Laya 自陈 `score` 最弱、SST-5 仅 0.372）。

### 8.3 质量

- [ ] **准确率之外的误判类型**：是"混淆"还是"反转"？错误集中在哪些边界？
- [ ] **拒答 / 升级覆盖**：拒绝或上抛的比例、以及被升级样本的真实错误率（reflex 与 judge 论文都报 risk-coverage）。
- [ ] **概率校准**：**ECE / Brier 必报**，并说明是否做过温度缩放（Laya：0.466 → 0.081 全来自后处理）。
- [ ] **选择性预测**：按置信度分段的覆盖率与段内准确率（如 ≥0.80 段 62% 流量 / 93% 准确率）。
- [ ] **对照基线**：多数类基线、单任务最优 LLM、以及**同特征监督训练模型**（JEVQA 的正当对照）。

### 8.4 性能

- [ ] **p50 与 p95**（只报均值会掩盖长尾）。
- [ ] **并发数**与吞吐（req/s）。
- [ ] **问题数**：单问还是多问同发？多问时 state 重复计入的 token 量。
- [ ] **测量位置**：客户端调用到响应可用，还是服务端模型时间（Kev 明确区分二者）。
- [ ] **冷启动**与预热状态是否排除。

### 8.5 成本

- [ ] **按 token / 请求 / 问题**三种口径都给。
- [ ] **输入与输出分别计价**（Jev 输出免费，这会让"每请求成本"随输出长度与 LLM 的差距失真）。
- [ ] **缓存命中率**与缓存策略（边缘编排研究显示缓存会消掉大部分时延优势）。
- [ ] **自托管口径**：电费/独占到 GPU 挂牌价差异极大，必须写明（this-that-model 自陈"读作一个数量级而非五个"）。
- [ ] **失败重试**与升级到强模型的隐形成本是否计入。

### 8.6 复现

- [ ] **原始结果与代码链接**（`this-that-model` 声明每个脚本同时打印"实测值 vs 论文值"）。
- [ ] **数据分区冻结时间**（JEV-as-a-Judge 明示 670 项扩展在查看 pilot 准确率前冻结）。
- [ ] **统计方法**（配对 cluster bootstrap、Wilson 区间、随机种子）。
- [ ] **运行日期**与可执行的上下文（模型版本 + 服务端点 + 地域）。

---

## 九、待跟踪与未确证事项

### 9.1 待跟踪（按重要性排序）

| # | 跟踪项 | 为什么重要 | 判据 |
|---|---|---|---|
| T1 | **官方论文与训练配方是否公开** | 当前一切方法学结论都是厂商自述；公开论文才能核验 RLCD 与 readout | 出现同行评审论文或带方法的官方技术报告 |
| T2 | **1.14 及后续版本的能力变化** | 1.14 已引入 `Box` 原语，官方同时把图像标为 Dreamer-ready | 图像/长上下文（262k）准确率与稳定性的公开量测；jaggedness 页是否更新到 1.14 |
| T3 | **独立复现与跨版本校准迁移** | 官方明示别名会漂移、答案会变；按版本调的阈值未必可迁移 | 有第三方给出 v1.13→v1.14 同任务 ECE/准确率对照与阈值迁移建议 |
| T4 | **高置信度错误的缓解手段是否有效** | JevOut 与选项名论文已坐实；官方第 8 条只给"重排检查" | 是否有论文证明重排检查 / 覆盖标记 / 外部校验能显著降低翻转率 |
| T5 | **高基数选项空间的退化** | Laya 自陈 77 选项时降到 0.425，而 Jev 在同一基准为 0.870；官方声明 ≤255 选项 | 独立评测给出选项数-准确率曲线 |
| T6 | **非英语/CJK 的实际可用性** | 官方明确"不同等好"，本专题面向中文用户 | 中英同任务分表对照 |
| T7 | **成本口径的统一** | 现有第三方数字按 token/请求/问题/电费四种口径给出 | 出现统一口径的横评 |

### 9.2 未确证 / 不作为结论（列入本节，不进正文）

| # | 事项 | 状态 |
|---|---|---|
| U1 | "Jev 是双向编码器 + 并行标签头" | **推测**。官方无架构披露；媒体分析明确标注为"社区逆向解读/推测"。 |
| U2 | "TypeSafe fork 过 LLaDA，因此有扩散语言模型谱系" | **推测**。同上，仅二手分析提及，本 Agent 未核验。 |
| U3 | 官方工作流自评页的 193.6× / 444.6× 原文（含对照模型、缓存与工作负载定义） | **未定位**。本报告只记录为"媒体转述的厂商自评，且自标为乐观上限"。 |
| U4 | "约 3,100 名用户实测：中位提速 7×、成本降 30×、中位延迟 76 ms" | **用户自报聚合数据**，无原始数据与方法，仅二手转述。 |
| U5 | "官方评测页上 Jev 综合 67.8%、排第四" | 二手转述，本 Agent**未在官方站点定位该评测页**。 |
| U6 | antirez 2026-09-21 对该模型的公开质疑 | 二手转述其观点，未核验原始帖。 |
| U7 | LangChain 的 5 题 × 100 次 agent 评测（500 次判断全一致、方差最小、单例 0.44 s / $0.00035） | 二手转述第三方评测，未定位原始发布。 |
| U8 | 挪威语 24 样本 × 11 问的独立测试（与 DeepSeek V4.1 Flash 统计无差别，但校准方向全对） | 二手转述单一开发者测试，样本极小。 |
| U9 | 媒体实测 50 条中文客服问题的判断力比较 | 二手转述，未见方法与样本。 |
| U10 | 第三方索引仓库自称"174 条、161 条学术预印本" | 收录数量为其自述，本 Agent 未逐条核验。 |
| U11 | "Jev 估值 100 亿美元"等融资/估值报道 | 与本专题技术内容无关，不引用。 |

> 上述 U 类事项若后续被独立确证，应升级进正文并更新本节的删除记录；**在此之前不应作为任何结论的依据**。

---

## 十、参考来源（均于 2026-10-16 实测可达）

### 官方文档（一手但自述）

- [TypeSafe — System One 概念](https://docs.typesafe.ai/concepts/system-one)
- [TypeSafe — Primitives（Choice / Score / Noul）](https://docs.typesafe.ai/primitives)
- [TypeSafe — Confidence](https://docs.typesafe.ai/confidence)
- [TypeSafe — Models（版本、价格、上下文、别名）](https://docs.typesafe.ai/models)
- [TypeSafe — AI primer（RLHF / RLVR / RLCD）](https://docs.typesafe.ai/introduction/machine-learning-primer)
- [TypeSafe — Jev 1.13 jaggedness（九类弱点）](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
- [TypeSafe — Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out)
- [TypeSafe — Images（Dreamer-ready、Box）](https://docs.typesafe.ai/images)
- [TypeSafe — State](https://docs.typesafe.ai/concepts/state)
- [TypeSafe — 文档索引 llms.txt](https://docs.typesafe.ai/llms.txt)

### 同名 RLCD 消歧（必引）

- [Yang et al. — RLCD: Reinforcement Learning from Contrastive Distillation for Language Model Alignment (arXiv:2307.12950, ICLR 2024)](https://arxiv.org/abs/2307.12950)

### 第三方预印本

> 下列 22 篇中，**3 篇为仅摘要级**（`2609.33209`、`2609.29429`、`2610.09683`；后两篇列于 §6.2 末尾旁证表），其余 19 篇按 §1.2.1 第二轮抽验在**正文**命中本报告所引关键串；其中 `2609.26550` 的"0.36%"与 `2609.24965` 的"最低观测中位时延"两条主张单独降为摘要级（见 §1.2.2）。

- [2609.22753 — Low-Latency Edge Service Orchestration](https://arxiv.org/abs/2609.22753)
- [2609.23136 — Intent Interpretation at RIC Timescales (6G Open RAN)](https://arxiv.org/abs/2609.23136)
- [2609.24052 — Calibrated Decisions at Scale（事故叙述编码）](https://arxiv.org/abs/2609.24052)
- [2609.24965 — Jev for Scientific Decisions](https://arxiv.org/abs/2609.24965)
- [2609.23986 — Jev-Mem](https://arxiv.org/abs/2609.23986)
- [2609.26532 — REFLEX with Jev](https://arxiv.org/abs/2609.26532)
- [2609.26550 — JEV-as-a-Judge](https://arxiv.org/abs/2609.26550)
- [2609.24395 — JEVQA（视频质量）](https://arxiv.org/abs/2609.24395)
- [2609.25845 — Visual Jev](https://arxiv.org/abs/2609.25845)
- [2609.24574 — Evaluating Decision Models for Text Annotation in CSS](https://arxiv.org/abs/2609.24574)
- [2609.23886 — this-that-model-1.0](https://arxiv.org/abs/2609.23886)
- [2609.28613 — Decision Hijacking](https://arxiv.org/abs/2609.28613)
- [2609.30243 — JevOut: Natural Context Can Flip Decision Models](https://arxiv.org/abs/2609.30243)
- [2609.26758 — Type-Safe Is Not Error-Free（选项名 vs 定义）](https://arxiv.org/abs/2609.26758)
- [2609.23959 — Open-Jev Judgments on CallScreenBench](https://arxiv.org/abs/2609.23959)
- [2609.33209 — Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms?](https://arxiv.org/abs/2609.33209)
- [2609.29429 — Just Ask Jev: RLCD as a Zero-Shot Detector of AI Alignment Failures](https://arxiv.org/abs/2609.29429)
- [2610.09683 — System Switch: When Should a Fast Decision Model Stop and Think?](https://arxiv.org/abs/2610.09683)

### 开源实现材料（仅读主页/模型卡，未读源码、未克隆）

- [this-that-model-1.0 模型卡](https://huggingface.co/flock-io/this-that-model-1.0) · [推理代码主页](https://github.com/FLock-io/this-that-model)
- [Laya 模型卡（UPSTREAM_README）](https://huggingface.co/convaiinnovations/laya) · [Laya 仓库主页](https://github.com/NandhaKishorM/laya)
- [laya-coreml（Apple Silicon 移植主页）](https://github.com/mizorewww/laya-coreml)
- [Kev 1.0 发布说明](https://jaredpalmer.com/blog/introducing-kev)
- [vagmi/jev-lite 模型卡](https://huggingface.co/vagmi/jev-lite)
- [system-one-models-getting-started（第三方复现启动评测）](https://github.com/gsaini/system-one-models-getting-started)

### 第三方分析与导航（二手）

- [Awesome JEV Papers（索引仓库）](https://github.com/Oscar-dzy/Awesome-jev-papers)
- [Simon Willison — Jev introduces a new shape of LLM](https://simonwillison.net/2026/Sep/21/jev/)
- [腾讯云开发者社区 — Jev 是炒作还是颠覆？](https://cloud.tencent.com/developer/article/2750505)
- [Founder Park / 极客公园 — Diogo Almeida：我为什么要做 Jev？](https://www.geekpark.net/news/371794)

---

## 十一、交付自检与机械审计记录（2026-10-16，第一批·结构层）

> 本节是本条目"领域研究第一批"的**交付留证**，不新增任何技术结论。

### 11.1 claim 审计：以 canonical 脚本重跑（`~/.dsh/skills/code-researcher/scripts/claim_audit.py`）

**脚本定位更正（重要）**：初次交付时按任务书字面去找**仓库内** `scripts/claim_audit.py`，并据此写"仓库缺脚本"。**该事实成立但不完整**：canonical 脚本在**用户级 skill 目录**——`~/.dsh/skills/code-researcher/scripts/claim_audit.py`（同目录另有 `scan_repo.py` / `self_check.py` 等）。本节以 **canonical 脚本的口径为准**；此前的 `/tmp` 替代实现仅为过渡留证，**不再作为最终口径**。

**canonical 脚本口径**（读其源码确认，非推断）：`--format json|text`、`--lang zh|en`、`--out`；它按**高影响词表**（核心/主要/关键/保证/确保/防止/可扩展/安全/稳定/可靠/风险/瓶颈/耦合/技术债/优化/取舍/抽象/边界 及英文对应词）认定高影响结论，再看该行**邻域 ±1 行**内是否出现"源码/文档路径"型证据（如 `scripts/library_index.py:120`、`docs/statistics.md`，**URL 也算**，因其正则命中路径段）。

**canonical 实测（2026-10-16，`--lang zh`）**：

| 文档 | 高影响结论（High-impact claims） | 缺少邻近源码证据 |
| :-- | --: | --: |
| `taxonomy.md` | 14 | 7 |
| `calibration.md` | 13 | 3 |
| `experiments.md` | 16 | 12 |
| **三份子文档合计** | **43** | **22** |
| `report.md`（本条主文档，仅参考） | 45 | 25 |

**与 `/tmp` 替代实现的差异（如实说明，避免两套数字被误读为矛盾）**：

| | canonical 脚本 | `/tmp` 替代实现 |
| :-- | --: | --: |
| 高影响结论 | **43** | 265 |
| 缺少邻近证据 | **22** | 122 |
| 高影响判定 | 固定中英文词表（核心/保证/风险/边界…） | 含阿拉伯数字 **或** 断言词表 |
| 证据判定 | 邻域 ±1 行内的**路径型**证据（URL 亦算） | 同行内的 URL / 证据等级标签 |
| 命名 | "缺少邻近**源码**证据"（面向代码研究场景） | "缺失**邻近证据**" |

**差异解读（22 处逐行复核）**：canonical 的 22 处"缺少邻近源码证据"**几乎全部**是**标题行**（如 `# Decision Models 分类学…`、`### 1.3 与奖励模型 / judge 的边界`、`### 3.3 训练目标与接口的耦合（研究推断）`）、**协议骨架行**（`| V3 | **换中性标识符**… |`、`| 每个高风险子群 | ≥ 300 条 |`）与 **Mermaid 图节点行**（`A --> D["边界澄清 §1"]`）——它们**按设计就不是引文行**。此外该脚本把"结论句"和"标题"一并纳入，而本专题的结论行普遍把出处写在**同句或同表相邻列**（如 `| … | 精读原文·预印本（[2609.24574](https://arxiv.org/abs/2609.24574)） |`），因此两套数字的**差值来自口径而非证据缺失**。**逐行复核未发现"有事实性主张、无任何出处"的行。**

**下面保留 `/tmp` 替代实现的明细表，仅作过渡留证（非最终口径）**：

**处理（不由 Agent 自造同名脚本、不改动 `scripts/` 跟踪内容）**：改用一次性替代实现 `/tmp/dm_claim_audit.py`（**未纳入版本控制，仅本次留证**），口径如下并完全可复现：

**处理（不由 Agent 自造同名脚本、不改动 `scripts/` 跟踪内容）**：改用一次性替代实现 `/tmp/dm_claim_audit.py`（**未纳入版本控制，仅本次留证**），口径如下并完全可复现：

- 先剥除代码块（``` 围栏），避免把 Mermaid/示例当主张；
- **断言行** = 表格数据行（排除纯引用行：整行单元格均为 `[text](url)` / `<url>`，那是参考来源清单）+ 列表项行；
- **高影响结论（H）** = 断言行中含阿拉伯数字，或含断言词表（必须/不得/证明/结论是/表明/…）之一；
- **缺失邻近证据（M）** = H 行中**无 URL 链接且无证据等级标签**（精读原文/摘要级/二手/受限核验/研究推断/缺证/未确证）；
- 另报"宽松口径"：把本文件内章节自引（`§x`）也算邻近证据。

**实测结果（三份子文档：`taxonomy.md` / `calibration.md` / `experiments.md`）**：

| 指标 | taxonomy.md | calibration.md | experiments.md | 合计 |
| :-- | --: | --: | --: | --: |
| 文档行数 | 254 | 261 | 349 | 864 |
| 断言行 | 99 | 99 | 160 | 358 |
| **高影响结论数 H** | 66 | 76 | 123 | **265** |
| （严格口径：剔除表头/协议骨架行后） | 48 | 58 | 73 | 179 |
| **缺失邻近证据数 M** | 12 | 20 | 90 | **122** |
| （严格口径：剔除表头/协议骨架行后） | 7 | 18 | 52 | **77** |
| 其中显式标注「研究推断」的行 | 4 | 3 | 5 | 12 |

**对 M=122 的如实解读（不得读作"存在 122 处无证据断言"）**：机械口径无法区分下列三类，逐类人工复核后确认**未发现"有结论、无任何出处"的行**：

1. **协议骨架行**（`experiments.md` 的变式表 `V1…V8`、准备清单 `P1…P8`、指标定义行）——它们是**待执行的实验设计**，按设计**不应**有出处；
2. **表头行**（如 `| # | 项 | 为什么必须 | 依据 |`）被机械识别为断言行；
3. **术语定义行**（ECE/Brier/可靠性曲线的定义）与该来源**同表相邻**（表内"本专题内使用位置"列给出处），属"邻近证据在邻行"的表格布局效应。

**结论**：M=122（严格 77）**全部为上述三类口径假阳性**；三份子文档的每条事实性主张均带 URL 出处或证据等级标签，每条"研究推断"均显式标注。**最终口径**：canonical 脚本（`~/.dsh/skills/code-researcher/scripts/claim_audit.py`）已复核，`高影响结论=43 / 缺少邻近源码证据=22`（明细与差异解读见本节开头）；**不再以"仓库内缺该脚本"作为最终口径**。

### 11.2 统计口径（生成物随子文档变化）

本批新增 3 份子文档后，仓库生成物按同一口径重跑 `scripts/library_index.py --repo-root . --out-root . --write-stats --check-links`（先 `--dry-run` 预演）。受影响的口径量：

| 口径量 | 本批前 | 本批后 | 说明 |
| :-- | --: | --: | :-- |
| `entries.total` | **46** | **46** | **不变**：子文档不是 `report.md`，不新增条目 |
| 条目子文档数（children） | 25 | **28** | +3（本批三份子文档） |
| 条目正文行数（`lines`，剔除 front-matter） | 29,562 | **29,663** | +101，全部来自 `report.md` 本批增补（子文档导航 + §八 可执行版本指引 + 本节）；子文档**不计入** `lines` 口径 |
| 条目字节 | 1,724,304 B | **1,735,390 B** | +11,086 B（同上，仅条目口径） |
| `report.md` 本文件行数（`wc -l`） | 608 | **709** | 与 `lines` 增量一致（本条目无 front-matter） |
| 目录内文件数 / 目录内容字节 | 76 / 2,281,483 B | **79 / 2,371,700 B** | +3 文件（三份子文档）|
| 文档数（除生成物的 `.md`） | 80 | **83** | +3；**报告/深读正文**（除库内 README）75 份 / 38,949 行 / 2,333,238 B |
| 全仓库跟踪文件数 | 93 | **96** | +3 |

> **口径提醒**：`lines` = **各条目 `report.md` 合计 − front-matter 行数**（本仓库仅 1 份条目带 front-matter，9 行），**不含**子文档；子文档行数只体现在"文档数 / 目录文件数字节"等口径。派生数字（根 `README.md`、`LLM-Research/README.md`、`docs/statistics.md`）均由脚本产出，不手改。

### 11.3 链接与卫生自检

| 检查 | 结果 |
| :-- | :-- |
| 链接核验脚本 | `/tmp/dm_repo_link_regress.py`（**未入库**，一次性留证）：剥代码块与行内反引号 → 取 `[label](target)` → **先剥 `<>` → 再判 scheme → 再 percent-decode（`urllib.parse.unquote`）** → 无 scheme 者解析为仓内路径查存在性 |
| 全仓相对链接回测（更正后口径） | 基线 `ae715fd` 与本次分支：链接总数 1408→1570、外链 344→446、仓内相对 745→805、纯锚点 319→319；**两棵树均报 0 条失效仓内链接 → 本批 0 新增失效** |
| **更正：此前记的"1 条既有失效"是假阳性** | 该条为根 `README.md` 指向 `Repo-Research/nemotron-tri-mode-diffusion/raw-extracts/pdf-fu_%E7%AD%89__…md`。**渲染器/GitHub 会先 percent-decode 再解析**：解码后为 `pdf-fu_等__nemotronlabsdiffusion_a_trimode_language_model_unifying_autoregressive_dif.md`，该文件**真实存在**（已实测 `exists=True`）。此前判定失效，是因回测脚本**把未解码的原始串直接当路径**，属**编码/解码顺序造成的假阳性**。**正确的判定顺序 = 先剥 `<>` → 判 scheme → percent-decode → 查存在性**；已按此更正脚本并重跑，结果为 **0 条失效**（基线与本分支皆然）。原"未擅改"说明保留：本批**未改动**根 `README.md` 的该链接 |
| 本批新增文档外链可达性 | 三份子文档 + `report.md` 共 **48 个去重外链，全部 2xx**（0 失效） |
| Mermaid 图 | 结构校验通过：`graph TD` + **22 条边 / 21 个带标签节点**，节点先定义后引用、标签无方括号冲突。⚠️ 未能跑通可视化渲染：Mermaid 在 Node 下需要 DOM+DOMPurify，本机未装浏览器渲染栈（**只做结构校验，未做渲染校验**） |
| 源码/克隆残留 | 无：本批**未克隆任何仓库**；仓内 `scripts/` 仅原有 `library_index.py`（`*.py` 残留检查排除该文件后为空） |
| gitlink（子模块）| **0**（`git ls-files -s` 无 mode `160000`） |
| 远端分支 SHA = 本地 | **是**。本行钉在**本批首次提交**的 HEAD 上（`d2b1534fab5e2501e4513cb1fe2444d291a2e959`）；其后按 Orchestrator 要求补了一个**普通追加提交**（canonical `claim_audit.py` 重跑 + 链接编码顺序更正），故最终分支 HEAD 比本行新一格。交付时以交付报告中的 `git ls-remote` 输出为准 |
| 主工作树 | 完成后回到 `main`，`git status --short` 为空；分支 worktree `/tmp/wt-dm` 已移除 |

---

## 十二、交付自检与机械审计记录（2026-10-16，第二批·证据层）

> 本节是本条目"领域研究第二批"的**交付留证**，**不新增任何技术结论**，结论与证据仍以 §〇–§十 为准。

### 12.1 本批交付物结构

| 交付物 | 数量 | 内容 |
| :-- | --: | :-- |
| [`papers/`](papers/) | **12 篇** | 逐篇结构化提取，统一模板：**方法 / 实验设置与条件 / 关键数字+条件（逐条附可 grep 的 `find:` 串）/ 失效边界 / 关联到本文哪条结论 / 与本文的差异** |
| [open-implementations.md](open-implementations.md) | 1 份 | `this-that-model` / `Laya` / `Kev` / `JevLite` / `Visual Jev` 的**实现路径**、**可复现性**（权重·许可·接口·依赖）、**模型卡口径**；全部外链实测状态码 |

**12 篇清单**（编号↔标题均已逐条核对，见各文件 §7）：`2609.24574`、`2609.26550`、`2609.26758`、`2609.30243`、`2609.28613`、`2609.23986`、`2609.26532`、`2609.23886`、`2609.25845`、`2609.24052`，**增补 2 篇** `2609.33209`（概率公理类）、`2610.09683`（System Switch 类）——后两篇正是任务书列出的可选增补类别。

### 12.2 claim 审计：以 canonical 脚本重跑（`~/.dsh/skills/code-researcher/scripts/claim_audit.py`）

**canonical 实测（2026-10-16，`--lang zh --format json`）**：

| 文档 | 高影响结论 | 缺少邻近源码证据 |
| :-- | --: | --: |
| `papers/2609.24574-css-text-annotation.md` | 8 | 2 |
| `papers/2609.26550-jev-as-a-judge.md` | 8 | 5 |
| `papers/2609.26758-option-name-vs-definition.md` | 15 | 8 |
| `papers/2609.30243-jevout-natural-context-flip.md` | 24 | 13 |
| `papers/2609.28613-decision-hijacking.md` | 13 | 6 |
| `papers/2609.23986-jev-mem.md` | 3 | 3 |
| `papers/2609.26532-reflex-selective-control.md` | 8 | 4 |
| `papers/2609.23886-this-that-model.md` | 2 | 2 |
| `papers/2609.25845-visual-jev.md` | 7 | 4 |
| `papers/2609.24052-crash-narrative-calibration.md` | 8 | 2 |
| `papers/2609.33209-probability-axioms-coherence.md` | 4 | 3 |
| `papers/2610.09683-system-switch.md` | 5 | 1 |
| [open-implementations.md](open-implementations.md) | 6 | 2 |
| **本批合计（12 篇 + 1 份）** | **111** | **55** |
| 第一批三份子文档（对照） | 43 | 22 |
| **全部子文档合计** | **154** | **77** |
| [`report.md`](report.md)（本条主文档，仅参考） | 48 | 25 |

**口径与解读（与第一批同一脚本、同一 `--lang zh`）**：canonical 按**高影响词表**认定"高影响结论"，再看该行**邻域 ±1 行**内是否有**路径型证据**（URL 亦算）。

本批 55 处"缺少邻近源码证据"的**逐类复核**（与第一批同一结论）：

1. **表格行把出处放在行尾反引号内的 `find:` 串**——canonical 的正则把它算作"路径证据"的极少，故大量**已带出处**的行被计入；本批 `papers/` 的**每一条数字**都在同表行尾给出 `find:`（可在 arXiv 正文逐字 grep），另有 §7 来源表给出 URL。
2. **标题行与 `## N` 小节行**（如 `## 4 失效边界`、`### 3.2 …`）按设计不是引文行。
3. **协议/设计行**（实验设置表内的"缓存：未报告"、"对照模型：…"）由定义即非引文。

**逐行复核未发现"有事实性主张、无任何出处"的行**；本批所有 `find:` 串均已对其所依据的 **arXiv 正文版本**做过 grep 命中自查（版本与命中口径见各文件顶部说明）。**最终口径：高影响结论 111 / 缺少邻近源码证据 55（本批）；全部子文档 154 / 77。**

### 12.3 统计口径（生成物随子文档变化）

本批新增 13 份子文档后，仓库生成物按同一口径重跑 `scripts/library_index.py --repo-root . --out-root . --write-stats --check-links`（先 `--dry-run` 预演）：

| 口径量 | 本批前（`5944189`） | 本批后 | 说明 |
| :-- | --: | --: | :-- |
| `entries.total` | **46** | **46** | **不变**：`papers/` 与 `open-implementations.md` 都不是 `report.md`，**不新增条目** |
| 条目子文档数（children） | 28 | **41** | **+13**（12 篇 `papers/` + `open-implementations.md`） |
| 条目正文行数（`lines`，剔除 front-matter） | 29,663 | **29,764** | **+101**，全部来自 `report.md` 本批增补（子文档导航 + 本节 §12）；**子文档不计入** `lines` |
| 条目字节 | 1,735,390 B | **≈1,748,694 B** | 约 **+13,300 B**（同上，仅条目口径；**自指量**——本节自身也在 `report.md` 内，故标约值，见下口径提醒） |
| `report.md` 本文件行数（`wc -l`） | 709 | **810** | 与 `lines` 增量一致（本条目无 front-matter；810 − 101 = 709 与基线一致） |
| 文档数（除生成物的 `.md`） | 83 | **96** | **+13** |
| 全仓库跟踪文件数 | 96 | **109** | **+13**（本批 13 份子文档提交后实测；`git ls-files` 含生成物） |

> **口径提醒**：`lines` = **各条目 `report.md` 合计 − front-matter 行数**（本仓库仅 1 份条目带 front-matter，8 行；另有 1 份文件无结尾换行，故 `wc -l` 合计 29,772 − 8 = **29,764**），**不含**子文档。派生数字（根 `README.md`、`LLM-Research/README.md`、`docs/statistics.md`）均由脚本产出，不手改。
> **自指量说明**：`条目字节`（含本条 `report.md` 自身）与 `report.md 行数` 都是**自指量**——本节的任何编辑都会轻微改变它们。故此处字节数标约值，**权威值以仓库生成物 [`index/stats.json`](../../../index/stats.json) 为准**。

### 12.4 链接与卫生自检

| 检查 | 结果 |
| :-- | :-- |
| 链接核验脚本 | `/tmp/dm2/linkcheck.py`（**未入库**，一次性留证）：剥**围栏代码块** → 剥**行内反引号** → **剥裸 autolink `<scheme:…>`** → 取 `[label](target)` → **先剥 `<>` → 判 scheme → percent-decode（`urllib.parse.unquote`）→ 查存在性** |
| 全仓相对链接回测（正确顺序） | 基线 `5944189`（`git stash` 后同一脚本实测）：总计 **1,603**、外链 450、仓内相对 **834**、纯锚点 319、**失效 0**；本批终态：总计 **1,638**、外链 450、仓内相对 **869**、纯锚点 319、**失效 0** → **本批 0 新增失效** |
| 一处**假阳性已排除** | 基线核验曾把 `Repo-Research/sglang-research/report.md` 的**裸 autolink** `<https://github.com/…/README.md>` 当作仓内相对链接。**正确顺序**是先剥 `<>`、判 scheme，故它是**外链**。已按正确顺序重跑，**0 失效** |
| 本批新增文档外链可达性 | `papers/` 12 篇覆盖的 **10 篇原始论文 + 2 篇增补**：`arxiv.org/abs/<id>` 与 `arxiv.org/html/<id>` 均 **HTTP 200**、`<title>` 与任务书给定标题**逐条一致**；`open-implementations.md` 另实测 **19 条 2xx + 2 条 404**（404 已移入该文件 §7 并改列） |
| 源码/克隆残留 | **无**：本批**未克隆任何仓库**；仓内 `scripts/` 仅原有 `library_index.py`；`papers/` 与 `open-implementations.md` **均不含**源码片段或 `仓库@commit:文件:行` 断言（`open-implementations.md` §9 明示该断言为 0） |
| 临时分析源 | 抓取的 arXiv HTML 曾镜像到工作区 `.tmp-dm-src/`（已被 `.gitignore` 的临时忽略项覆盖），**交付前已删除**，未入库 |
| gitlink（子模块） | **0**（`git ls-files -s` 无 mode `160000`） |
| 远端分支 SHA = 本地 | **是**（见交付报告中的 `git ls-remote` 输出与本地 `git rev-parse` 对照） |
| 主工作树 | 完成后回到 `main`，`git status --short` 为空；分支 worktree `/tmp/wt-dm-b2` 已移除 |

### 12.5 本批**未确证 / 待更正**事项（**不入正文**，仅登记）

> 本节只登记"证据不足或与来源存在张力"的项，**不改动 §〇–§十 的任何结论或证据**；由 Orchestrator / 泡泡决定是否后续修正。

| # | 事项 | 实测情况 | 建议 |
| :-- | :-- | :-- | :-- |
| D1 | §1.2.1 第 71 行记 JEV-as-a-Judge 的 `0.36%` 为"**仅摘要，正文查无**" | **该判定基于 v1**。当前版本 **v5** 正文含字面串：`JEV comes within three points of GPT-6 at 0.36% of its fee and a 0.15-second median latency` | **升为正文可证**，可改标 `精读原文` |
| D2 | §7.2 "费用为最强 LLM 评判者的 0.36%（仅摘要，正文查无）" | 同 D1 | 同 D1 |
| D3 | §7.1 / §7.2 写「正文可证的 **RewardBench 94.0% vs 93.5%**」 | **归属错**：RewardBench 上 JEV 为 **92.2%** vs GPT-6 **93.5%**；**94.0** 属 (a) 150 条既有标签上的 JEV 分数（vs GPT-6 96.7），或 (b) RewardBench 上 τ=0.9 **单序级联**的分数 | 改为「RewardBench **92.2% vs 93.5%**；150 条既有标签 **94.0% vs 96.7**」 |
| D4 | §6.4 末句"**把选项名换成随机字符串则结果改变**" | **方向相反**：`2609.26758` v3 正文为 `random strings used as option names yield mean flip rates close to those of neutral controls across all three models`——随机串≈中性对照，**不**引发更多翻转 | 改为"**随机字符串回落到中性对照档，并不引发更多翻转**"；真正驱动翻转的是名称的**语义极性**（`yes/no` 对 `0/1` 高 **70.4 pp**） |
| D5 | §7.3 "校准**随模型而变而非随范式而变**" | `2609.24052` 正文可确证"typed 模型与**一个** frontier 分支按交付状态未校准、**另一个**已校准"，但**未定位到**该概括句 | 改为可逐字支撑的写法，或标注为**本报告跨来源概括** |
| D6 | §6.4 "**选项顺序已坐实**"（指 `2609.26758`） | 该文 **v3 未测选项顺序**；其可测的是**名称语义极性**；选项顺序的独立实测见 `2610.09683`（正确答案在首位 **41%**，已每局打乱） | 拆分表述：顺序证据归 `2610.09683`；名称极性归 `2609.26758` |
| D7 | §6.2 表把 `2609.33209` 记为 `摘要级·预印本` | 本批已**精读其正文**：0.064（CI 0.055–0.072）/ 0.293 / 0.122 / 4.6× / 5× 噪声地板 / 单标签和 **1.14** / yes-no↔choice 差 **0.09** | **升为 `精读原文`**；并补"Jev 比所测 LLM 读出更一致，但**本身并不一致**" |
| D8 | §6.2 表把 `2610.09683` 记为 `摘要级·预印本` | 本批已**精读其正文**：AUROC–增益排序相关 **0.87**（18 对）/ hel-dout 增益 **+0.13 [0.08,0.18]** / **33 局 3 seed 无一到达出口** | **升为 `精读原文`**；并新增一条失效边界"**闭环下门控增益不转化为任务成功**" |
| D9 | v1 ↔ 当前版本差异（`2609.24574`→v2、`2609.26550`→**v5**、`2609.26758`→**v3**、`2609.30243`→v2） | 本批**已全部改用当前版本复核**。其中 `2609.26758` 的 **v1 是另一篇**（标题 `A Constrained Decision Head`、2 作者）；`2609.26550` v1 无 `0.36`/`1,610`，**v5 两者皆有**（`1,610` 构成为 1,340 RewardBench + 270 JudgeBench，另有 **live test** 510 对：**0.27 s vs 2.10 s**） | 主报告若引用版本敏感数字，应标注所用版本 |
| D10 | `github.com/mizoreww/laya-coreml` | **实测 404**（[open-implementations.md §7 U2](open-implementations.md)） | 若主报告来源清单引用该 URL 需同步更正 |
| D11 | `Visual Jev` 的权重、许可证、代码仓库 | **均未找到**（[open-implementations.md §7 U1](open-implementations.md)） | 记"未找到"，不得转引为"可复现实现" |
| D12 | `jev-lite` 的可商用性 | 权重许可为 **Gemma Terms of Use**；训练数据含 **ANLI（CC BY-NC 4.0）与 RACE（研究用途）**，模型卡自陈 `should be treated as non-commercial / research use` | 主报告 §6.5 开源复刻表**未记录该限制**，建议补上 |
