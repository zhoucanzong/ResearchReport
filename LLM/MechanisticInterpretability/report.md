---
display_name: 机制可解释性
type: topic-research
domain: LLM
subject: MechanisticInterpretability
date: 2026-10-30
evidence: 代表论文原文精读与机制证据综合
status: current
---

# 机制可解释性：从特征猜想走向可检验的计算机制

> 本专题讨论如何把模型内部计算还原为人能检查的部件、路径和算法。它不同于只观察注意力图、训练探针，或让模型用自然语言解释自己。核心问题是：**当我们说某个内部特征或电路“造成了”某个输出时，证据究竟有多强？**

推荐读序：[电路与机制概览](#1-解释模型内部机制究竟要说明什么) → [Induction Heads](papers/2209.11895-induction-heads.md) 看小型注意力电路如何通过干预建立因果证据 → [IOI 电路](papers/2211.00593-ioi-circuit.md) 看指定自然语言任务中的路径追踪、冗余和完整性 → 阅读 [Toy Models of Superposition 原文](https://arxiv.org/html/2209.10652v1)理解特征如何共享表示空间 → [SAE 扩展到大模型](papers/2024-scaling-monosemanticity.md) → [Circuit Tracing](papers/2025-attribution-graphs.md)看特征如何被组装为计算图，以及近年的[神经元基底路线](https://arxiv.org/html/2601.22594v2)如何挑战“必须先训练 SAE”的假设。

## 1. 解释模型内部机制究竟要说明什么

假设模型看到：“When Mary and John went to the store, John gave a drink to …”，接着输出 “Mary”。一个可视化可能指出模型在 “Mary” 附近激活了某些头；探针可能从隐藏态预测出 “Mary”；机制解释还要回答：模型怎样区分主语和间接宾语、哪些中间变量保存了人名、哪些计算路径把正确名字送到输出，以及打断这些路径后行为是否按预测改变。

机制可解释性（mechanistic interpretability, MI）因此不是“给神经元取名字”，而是尝试建立一个**计算假说**，再用消融、激活/路径替换、定向干预或替换模型等方法，测试假说是否能预测原模型的行为。解释对象通常是一个具体模型、输入分布、任务和输出指标；被解释的电路不自动推广到同一模型的全部行为。

```mermaid
flowchart LR
    A[行为与任务] --> B[候选内部变量<br/>特征/神经元/注意力头]
    B --> C[计算关系<br/>信息如何写入、传递、组合]
    C --> D[电路假说<br/>可运行的局部机制]
    D --> E[干预与反事实<br/>消融/替换/steering]
    E --> F[比较原模型行为<br/>检验必要性与充分性]
    F -->|失败则修订变量或路径| B
```

图里的步骤是研究程序，不是每篇工作的标准流水线。尤其要分开三类问题：

| 问题 | 典型工具 | 能支持什么 | 不能单独证明什么 |
| :-- | :-- | :-- | :-- |
| 哪些内部坐标会响应某种输入？ | 最大激活样本、线性探针、SAE、稀疏神经元 | 某种表示或相关性存在 | 该坐标是模型唯一或原生的“概念单元” |
| 哪些部件影响某个行为？ | 消融、激活替换、path patching、梯度归因 | 对给定干预与任务的因果影响 | 部件的自然语言标签完整概括了它的功能 |
| 一组部件是否构成足够解释？ | 电路执行、faithfulness/completeness 检查、替换模型 | 局部机制能否保留或重现目标行为 | 该电路解释模型全部策略、分布外输入或安全属性 |

这种区分是整条研究路线的主线：**相关表示 → 可干预特征 → 因果路径 → 忠实的机制解释**，每往后一层都需要额外证据。

## 2. 从小型电路到真实语言任务

### 2.1 Induction heads：先找到一个可精确描述的算法

Induction head 研究以重复序列模式为对象：`[A][B] … [A] → [B]`。一个前序 token head 把前一位置的信息写进 residual stream，后续 head 再匹配相同 token 的先前位置并复制其后继 token。这个机制适合教学，因为它可以写成清楚的算法，而不是含混的“头关注相似内容”。

原论文在 2-layer attention-only 小模型上给出较强因果证据：消融相关头会削弱论文定义的 in-context learning 指标，结构性干预也会相应移动这类行为形成的阶段。作者对含 MLP 的大模型采用了更多相关性、训练过程和架构干预证据，明确称其对前沿模型的主张仍属初步和间接；不能把小模型的电路证明成全部大模型 in-context learning 的通用机制。[原文摘要、Arguments 1–3、Assessing the Evidence，arXiv v1](https://arxiv.org/html/2209.11895v1)

论文的示范也指出任务定义很重要：它测量长上下文后段相对前段的损失变化，并把 induction heads 与此指标相连。这个结果支持“模式复制参与该类上下文学习”，不等于解释了 few-shot 数学、指令跟随或所有长上下文能力。

### 2.2 IOI 电路：扩大任务复杂度，也暴露冗余机制

IOI（Indirect Object Identification）任务要求模型在模板化自然语言句式中识别间接宾语。Wang 等人对 GPT‑2 Small 使用 path patching、注意力分析、激活替换和 head knockout，提出 26 个 attention heads、7 类功能组成的候选电路。论文以 faithfulness 检查候选电路是否保留目标表现，以 completeness 检查候选解释是否遗漏冗余路径，并以 minimality 检查节点是否确有边际作用；这些标准都依赖指定任务、提示分布与干预方式。[原文 §1–2、§4–6](https://arxiv.org/html/2211.00593v1)

它比一个干净的两层模式复制更接近在 GPT‑2 Small 上解释指定自然语言行为，但仍是模板化 IOI 任务，不等于广泛语言理解。论文也显示电路识别会遇到问题：存在备用 Name Mover Heads，常规电路被消融后它们才发挥作用；一些已知 induction heads 也参与 IOI 中非预期的子过程。**干预后的电路可能不是原模型平常采用的唯一实现**，而且切掉某部件会暴露补偿路径、改变其它部件的作用。因此，单个头造成输出变化是因果证据，却不足以证明完整电路已经找全。

两项早期工作应并读：Induction Heads 适合看单一、可组合的算法路径；IOI 适合看任务电路如何被逐步发现，以及冗余、抑制和不完整解释如何出现。它们不是两个可直接互换的 benchmark。

## 3. 为什么“特征”不一定等于“神经元”

### 3.1 Superposition：稀疏概念可以共享表示维度

Toy Models of Superposition 用可控的稀疏输入和小型 ReLU 网络展示：当需要表示的特征多于神经元维度时，模型可能用近似正交的方向共享空间；共享带来干扰，稀疏共现则可能使干扰成本可接受。这个模型解释了一个为什么单神经元经常对多个无关输入响应的可能机制，也使“polysemantic neuron”不必意味着网络完全没有可分解结构。

这项工作的证据边界也必须保留：它在人工设定的 toy model 中清楚展示了 superposition 与几何相变，不等于真实 LLM 的每种多义激活都由同一 superposition 结构造成，更不证明某种后续 SAE 能恢复唯一正确的 latent basis。[原文 Abstract、Background、Superposition as a Phase Change、Discussion](https://arxiv.org/html/2209.10652v1)

### 3.2 SAE：用稀疏字典寻找候选特征，而非读取模型原生标签

稀疏自编码器（Sparse Autoencoder, SAE）在模型激活 `h` 上训练编码器与解码器：

\[
z = f_\theta(h), \qquad \hat h = b + Dz.
\]

重建项鼓励 `\hat h` 接近 `h`，稀疏项鼓励每个输入只激活少量字典方向。若重建足够好，研究者就可以检查各字典方向在哪些上下文激活，并干预它们对输出的影响。但 SAE 不是 Transformer 原有的单元：字典大小、稀疏约束、数据覆盖、层/位置选择、feature splitting/absorption 都会影响被发现的特征。

Anthropic 的 Scaling Monosemanticity 将 SAE 扩展到 Claude 3 Sonnet 中间层残差流，展示了大量抽象特征，并对行为干预提供案例。论文同时指出字典不完整，且缺少严格方法判断特征是否忠实覆盖原模型计算。特征能按人类概念命名、或被人为放大后改变某些输出，并不等于模型平时依赖该单一特征完成同类推理；相关行为还可能沿平行或补偿路径实现。[官方原文 §1–2、§4、§6–7](https://transformer-circuits.pub/2024/scaling-monosemanticity/)

### 3.3 神经元基底路线：SAE 有价值，但不是唯一可能的可解释坐标

2026 年的 *Language Model Circuits Are Sparse in the Neuron Basis* 挑战“必须先训练 SAE 才能得到稀疏电路”的预设。作者改用 gated MLP 的 pre-down-projection activations（元素级非线性之后的激活坐标），并使用 RelP 归因，在其测试的 subject–verb agreement 任务和 Llama 3.1 8B-Instruct 多跳地名任务中找到较稀疏的神经元电路；论文报告在所用设置下，这种基底与 SAE 特征的 faithfulness/complete­ness 可比，并演示特定节点干预改变输出。[v2，§3–6](https://arxiv.org/html/2601.22594v2)

这不是“SAE 没有必要”的普遍结论：结果依赖其激活位置、RelP attribution、筛选阈值、指定任务和模型。它提醒读者把**解释基底**当作待比较的建模选择，而非默认把 SAE 特征视为真实存在的唯一对象。值得追问的是不同基底是否支持相同因果路径、在新任务/提示中是否仍忠实，以及引入替换基底后是否增加新的误差项。

## 4. Circuit tracing：从候选特征拼出路径

只知道有哪些特征仍未回答特征怎样组合成输出。Circuit tracing / attribution graph 的思路是构造一个可读替换模型：用 cross-layer transcoders 近似 MLP 计算，把某个 prompt 上的中间特征、边和 logits 连接起来；研究者据此提出路径假说，再用 feature inhibition/excitation 等干预检验。

Anthropic 对 Claude 3.5 Haiku 的 On the Biology of a Large Language Model 展示了算术、多跳问答、多语言、拒答和隐藏目标等案例。其研究价值在于展示内部路径能提出黑盒输出和口头 chain-of-thought 都未显露的假说；但作者也列出明确边界：graph 中有无法解释的 reconstruction error nodes；对稀有/分布外概念，替换模型更可能失配；未激活特征和抑制路径通常不容易从图中发现；可视化图有人工剪枝和标签；某些 feature intervention 结果会与 graph 预测矛盾。[官方原文 §Method Overview、§Limitations、§Discussion](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)；方法细节见 [Circuit Tracing §7.7 Mechanistic Faithfulness](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)

因此，attribution graph 是**带可检验预测的机制假说**，不是模型内部已经读出来的完整“思维链”。对某个例子有解释力，不等于在新提示、对抗改写、不同任务和未覆盖的模块上忠实；任何安全结论还要有对应行为测试和独立干预证据。

## 5. 证据阶梯：从“像一个概念”到“足以解释行为”

| 证据层 | 常见做法 | 支持的主张 | 仍缺的关键问题 |
| :-- | :-- | :-- | :-- |
| 激活关联 | top-activating examples、feature visualization | 某种输入与内部坐标相关 | 是否能区分相近/反例，是否只由词面触发 |
| 预测用途 | probe、线性 readout、下游 classifier | 坐标含有可用于预测的信息 | 信息是否由原模型用于该行为 |
| 单点因果影响 | ablation、activation patching、feature steering | 在特定任务和干预幅度下，该变量影响输出 | 是否有分布外副作用、冗余备份和其它路径 |
| 电路充分性（faithfulness） | 只运行候选子图，比较目标行为指标 | 子图能否保留原模型在该任务上的表现 | 补偿路径或额外组件是否也在贡献 |
| 电路完整性（completeness） | 对候选电路的子集作 knockouts，并比较子图与全模型的变化 | 解释是否捕捉了模型在这些干预下的冗余路径 | 全部子集搜索通常不可行，抽样仍可能漏掉备用机制 |
| 电路最小性（minimality） | 在其它组件被遮蔽时单独移除节点，测其边际作用 | 候选节点是否都对解释有必要 | 依赖上下文与干预集合，非模型范围内的全局最小性 |

IOI 的 completeness 在操作上比较对候选电路子集作相同 knockouts 后，候选子图与全模型的任务指标是否仍接近；论文用抽样及贪心搜索寻找高 incompleteness 子集，没有穷举全部组合。[§4](https://arxiv.org/html/2211.00593v1) IOI 的这组标准、Circuit Tracing 的 mechanistic faithfulness 与 2026 SAE survey 按 claim 区分的 recoverability/interpretability/faithfulness/utility 并非同一套标准分数。指标名称相似时必须先看操作定义：例如 intervention 能改变输出，支持因果影响；但若只测一个选定提示、替换模型还出现 error nodes，就不能由此推出完整机制或大范围效用。SAE 任务效用提升也不能自动证明它描述的是原模型实际采用的计算。[SAE Critical Survey v1，§2、§4](https://arxiv.org/html/2610.20139v1)

## 6. 这条研究路线怎样连接到对齐和安全

机制研究能为行为异常提出可检验假说，例如拒答路径、sycophancy feature、知识检索或 chain-of-thought faithfulness；它可帮助定位需要进一步测试的行为。但三个环节要分开：

1. **发现内部坐标**不等于发现风险机制；feature 可能代表关于某种现象的讨论，而不是模型会做出该行为。
2. **对选定提示进行干预**能显示局部因果作用，但不等于稳定控制全局模型行为。
3. **某案例的机制解释**不是模型安全证明；安全判断仍需覆盖分布、攻击、工具和系统级风险的行为评测。

Anthropic 的 Claude 研究可作为案例入口，见 [Models/Claude §4 机制可解释性](../../Models/Claude/report.md#4-机制可解释性从-toy-models-到-scaling-monosemanticity)；本专题强调跨工作的方法关系和证据层级，不重复其厂商研究时间线。

## 7. 推荐阅读顺序与开放问题

1. [Induction Heads 精读](papers/2209.11895-induction-heads.md)：先看一个可写成算法、并有小模型因果干预的电路。
2. [IOI Circuit 精读](papers/2211.00593-ioi-circuit.md)：再看自然语言任务里的路径发现、备用头和不完整解释。
3. 阅读 [Toy Models of Superposition 原文](https://arxiv.org/html/2209.10652v1)：理解神经元多义与特征共享维度的理论动机。
4. [Scaling Monosemanticity 精读](papers/2024-scaling-monosemanticity.md)：看 SAE 如何进入大模型及其功能检验。
5. [Circuit Tracing 精读](papers/2025-attribution-graphs.md)：看特征如何组合成 attribution graph，以及图的忠实度限制。
6. 对照 2026 年[神经元基底电路研究](https://arxiv.org/html/2601.22594v2)和[SAE 方法批判性综述](https://arxiv.org/html/2610.20139v1)，重新追问字典、神经元和替换模型分别带来什么假设。

开放问题不是“还能不能找出更多可命名特征”，而是：特征是否跨种子、模型版本和提示稳定；特征字典能否覆盖足够行为；归因图能否对原模型有机制忠实度；同一行为的并行、冗余与抑制路径如何纳入电路；局部解释是否能预测分布外失败；解释结果能否稳健改善模型纠错或风险评估，而不引入新的干预副作用。

## 原文定位

| 工作 | 阅读版本与章节 | 用于理解 |
| :-- | :-- | :-- |
| [In-context Learning and Induction Heads](https://arxiv.org/html/2209.11895v1) | v1；Key Concepts、Arguments 1–3、Assessing the Evidence | 模式复制算法与大小模型证据差别 |
| [Interpretability in the Wild: IOI Circuit](https://arxiv.org/html/2211.00593v1) | v1；§1–2、§3、§5–6 | path patching、冗余头、解释评估 |
| [Toy Models of Superposition](https://arxiv.org/html/2209.10652v1) | v1；Background、Superposition as a Phase Change、Discussion | 低维表示和多义特征的可能来源 |
| [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/) | 官方 2024 年长文；§1–2、§4、§6–7 | SAE 可解释性、行为干预、完整性限制 |
| [On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html) | 官方 2025 年长文；Method Overview、case studies、Limitations | attribution graphs 与 perturbation validation |
| [Circuit Tracing methods](https://transformer-circuits.pub/2025/attribution-graphs/methods.html) | 官方 2025 年长文；§7.7 Mechanistic Faithfulness | 替换模型与原机制一致性的验证问题 |

本专题把机制解释当作带证据等级的科学主张：每个路径都要写清解释的是哪个模型、哪类输入、哪项行为、用什么干预验证，以及还留下哪些并行机制或未解释误差。
