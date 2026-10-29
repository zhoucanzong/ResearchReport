---
display_name: 测试时学习与适应
type: topic-research
domain: LLM
subject: TestTimeAdaptation
date: 2026-10-30
evidence: 代表性一手论文精读与跨论文机制综合
status: current
---

# 测试时学习与适应：模型在使用时如何更新

> 本专题讨论模型进入测试或部署阶段后，怎样从当前输入、检索样本、流式上下文或任务反馈中更新可用状态。核心问题不是“多想几步”，而是**到底更新了什么、用什么信号更新、更新保持多久、怎样判断更新没有把模型带偏**。

## 先把四种“推理时改变”分开

设部署时的基座参数为 \(\theta_0\)。对同一条新问题，系统可以做几种表面相似、内部却不同的操作：

| 操作 | 更新对象 | 是否训练参数 | 典型作用 | 对照专题 |
|---|---|---:|---|---|
| In-context learning | 当前上下文与 attention/KV 状态 | 否 | 用提示中的示例临时指定任务 | [GPT 报告](../../Models/GPT/report.md) |
| Test-time compute/search | 候选答案、搜索树或 verifier 轨迹 | 否 | 用更多采样、搜索、验证挑出更好答案 | [推理模型与测试时计算](../ReasoningModels/report.md) |
| RAG / Agent memory | 外部检索库或持久化记录 | 否 | 将相关资料读入提示或后续任务状态 | [RAG](../RAG/report.md)、[智能体系统](../../Agents/AgentSystems/report.md) |
| Test-time training / learning | 参数、LoRA、fast weights 或可学习状态 | 是/更新 fast state | 让当前数据改变后续预测 | 本专题 |

这些操作可能组合：TTT-NN 会先检索数据再做梯度更新；Agent 可把长期记录写入外部存储，同时调用测试时适应模块。应按“系统里究竟发生了哪种状态变化”分类，不能把检索、长上下文和模型学习都统称为适应。

一个最小更新表达式是 \(\theta_{t+1}=\theta_t-\eta\nabla_\theta \mathcal{L}_t\)。公式本身没有回答关键问题：\(\mathcal{L}_t\) 是真实标签损失、无标签的 next-token 信号、重构目标，还是环境奖励？\(\theta_t\) 是整套参数、LoRA、小块 fast weights，还是只在一段输入期间存在的临时状态？这些选择决定方法是否能上线、是否会遗忘，以及评测结果意味着什么。

## 四条机制路线

### 1. 每个测试样本构造一个局部“微型训练集”：TTT-NN

[Test-Time Training on Nearest Neighbors](papers/2305.18466-test-time-training-nearest-neighbors.md) 从训练语料建立嵌入索引。对每个测试实例先找相似序列，再用这些邻居对语言模型做少量梯度更新，最后再评估该测试实例。它把一个统一大模型对“平均训练分布”的能力，改为针对当前样本临时形成局部适应。

这不是普通 RAG：RAG 将检索文本追加到上下文中，模型权重不变；TTT-NN 使用检索序列更新模型，再预测目标。它也不是把整个测试流的更新永久积累起来：论文在每个测试实例后将可训练参数复位到基座，避免前一个测试实例污染后一个实例。由此可见“每样本局部适应”与“持续在线学习”是两种不同协议。

代价是依赖高覆盖率索引与每请求反向更新。检索数据是否与目标评测重叠、更新轮数是否过拟合、如何定义每个测试样本的 reset 边界，都属于方法协议而不是实现小节。原文以 Pile 语言建模、GPT-2/GPT-Neo 及 bits-per-byte 结果为证；不直接推出开放问答或高风险任务中的答案质量收益。[§3–§6](https://arxiv.org/html/2305.18466v3)

### 2. 在无标签测试流上适应分布：TLM 与选择性更新

[Test-Time Learning for LLMs (TLM)](papers/2505.20633-test-time-learning-llms.md) 让模型在测试阶段读取目标域的无标签文本，使用输入 perplexity 作为自监督目标，并用高 perplexity 样本选择和 LoRA 更新应对领域迁移。它不是对每个问题单独找邻居，而是在当前测试流上累积一个轻量的参数更新。

这里最大的假设是：降低输入的 next-token perplexity 会让模型形成更适合该域的表征，进而改善答案预测。作者给出梯度对齐分析与任务实验，但“更会预测用户输入”不等于“答案事实正确”。当模型对错误输入过拟合、语言偏差变成高 perplexity 或域内文本本身含噪，输入适应可能强化错误而非知识。

2026 年的 [FG-TTL (ICML 2026)，§3–§4](https://proceedings.mlr.press/v306/bian26b.html) 将问题推进到自回归生成中自我产生的训练 token：早期错误可能影响后续 token，再用错误输出更新会形成正反馈；其 Future-Gain / Risk-Aware Adaptation 试图只更新对后续不确定性有帮助、且风险较低的位置。它和 TLM 共享“无标签流上更新”的大类，但解决的是生成过程中更新信号可靠性，不是同一个输入 perplexity 方法。结论应按其具体模型、基准和更新协议阅读。

### 3. 把 fast weights 当作有限上下文记忆：TTT layers 到 In-Place TTT

常规 attention KV cache 保留原始上下文信息，随着历史增长而占用更多缓存；fast-weight 路线尝试把一部分历史压进可更新的参数化状态。2024 年的 [TTT layers v1，§2–§3](https://arxiv.org/html/2407.04620v1) 让隐藏状态本身成为一个小学习器，并在读取测试序列时更新；这是一个序列层/架构设计，不等于把现有聊天模型按用户一边使用一边全量微调。

2025 年的 [TTT-E2E v2，§2–§3.7](https://arxiv.org/html/2512.23675v2) 将长上下文建模解释成 continual learning：模型在当前上下文上用 next-token prediction 更新 fast state，并通过训练时 meta-learning 让模型学会这种内循环；其“从头训练与元学习”设定，与给现成 checkpoint 做临时适应不同。[In-Place TTT 精读](papers/2604.06169-in-place-ttt.md) 则将 MLP down-projection 复用为 fast weights，目标与自回归语言建模对齐，并以 chunk-wise update 维持上下文并行。

其后研究继续拆解“写入什么”和“何时写入”：[TTT-NTP v1，§3–§4.6](https://arxiv.org/html/2606.21803v1) 用下一位置的 contextual hidden state 作为局部写入目标；[Select-TTT v1，§4–§5.6](https://arxiv.org/html/2610.36794v1) 用 query relevance 调节不同 chunk 的写入强度；2026 年的 [IP-TTCD v1，§3–§4.4](https://arxiv.org/html/2608.01672v1) 用长窗口教师与短窗口学生之间的 hidden-state discrepancy，蒸馏对未来预测有用的远端上下文。它们都利用 fast weights，但分别强调预测对齐、查询选择和远程信息的未来效用，不应被统称为一个已解决的“长记忆模块”。

fast-weight 状态的持久性取决于 reset 规则：只在一个 document/session 生效，就像压缩后的上下文；跨用户或跨评测样本保留更新，则会产生遗忘、数据污染和隐私边界。报告任何长上下文增益时，必须说明适应参数、何时更新、何时清空，以及同一个测试实例是否同时用于更新与评价。

### 4. 针对单个问题学习怎样找出一个高价值解：TTT-Discover

[Learning to Discover at Test Time](papers/2601.16175-learning-to-discover.md) 将测试时更新用于数学、算法、GPU kernel 和单细胞分析等问题。它让模型在问题对应的环境中提出候选、获取奖励、把先前搜索经验放入 buffer，并通过强化学习更新当前策略。

这里的目标不是“让模型平均回答所有任务更好”，而是针对这一道题或这一段优化任务，尽量发现一个高奖励解。论文明确区分了 finding one best solution 与学习一个可重复部署的高期望策略；因此它处于 TTT 与 test-time search 的交界：搜索提供候选与奖励，TTT 则改变后续候选分布。若任务奖励稀疏、评测器不可靠或 reward 可被投机，测试时更新会更快地强化错误；若输出只需一次有效设计，其评估规则也不同于普通问答。

这一类研究与 [AI4Science 的闭环证据](../../AI4Science/AutonomousLabs/report.md)和[大模型辅助运筹](../OperationsResearch/report.md)相接，但论文中的模拟/可验证奖励结果不等于现实实验中的新发现。

## 更新对象与持久时间比论文名称更重要

| 路线 | 更新什么 | 更新目标 | 状态通常维持到哪里 | 主要失效风险 |
| :-- | :-- | :-- | :-- | :-- |
| TTT-NN | 基座上的参数/可训练部分 | 检索邻居上的 next-token loss | 每个测试实例后可 reset | 索引重叠、检索偏差、反向成本、单样本过拟合 |
| TLM / FG-TTL | LoRA 或选定参数 | 输入 perplexity / 未来有益 token | 当前测试域或流 | 自监督信号与下游答案脱钩、自我强化错误 |
| TTT layers / fast weights | 序列层内部的小学习器或 fast weights | 重构、next-token 或 context distillation | 文档、序列或 rollout，依协议 reset | 状态遗忘、长程写入冲突、更新计算与 attention 取舍 |
| TTT-Discover | 当前问题的策略参数 | 环境/验证器奖励 | 单问题优化过程 | reward hacking、无法跨问题泛化、验证器与目标不一致 |

因此，阅读新论文时先问三件事：**模型具体更新了什么？这份更新对谁、跨多久保留？用什么外部或自监督信号判断更新有用？** 如果一篇论文只增加采样、best-of-N 或 search tree，它扩展的是 test-time compute，而非参数适应；如果只把笔记存入数据库，它是外部记忆，而非模型自身通过 test-time learning 更新。

## 推荐阅读路线

1. 用 [TTT-NN 精读](papers/2305.18466-test-time-training-nearest-neighbors.md)建立“检索后适配一个测试实例”的基线，并对比 [RAG](../RAG/report.md) 的无权重更新机制。
2. 读 [TLM 精读](papers/2505.20633-test-time-learning-llms.md)，理解无标签目标域流上的 perplexity 更新，以及这类自监督信号的假设。
3. 读 [In-Place TTT 精读](papers/2604.06169-in-place-ttt.md)，再对照 TTT-E2E、TTT-NTP、Select-TTT 和 IP-TTCD，理解 fast-weight 写入目标、参数持久性和长上下文压缩。
4. 最后读 [TTT-Discover 精读](papers/2601.16175-learning-to-discover.md)，理解测试时训练如何服务于单问题优化，并与 test-time compute/search、AI4Science 奖励验证区分。
5. 回到[推理模型与测试时计算](../ReasoningModels/report.md)、[LLM 强化学习](../ReinforcementLearning/report.md)、[长上下文](../LongContext/report.md)和[智能体系统](../../Agents/AgentSystems/report.md)，比较测试时算力、训练期策略更新、上下文状态与持久外部记忆的边界。

## 开放问题

- **自监督目标可靠吗？** 输入 perplexity 较低、模型自评“有帮助”或局部 hidden-state 更吻合，都不能自动保证答案正确或未来检索有效。
- **更新怎样隔离？** 多用户部署中，实例/session reset、跨请求持久化和 opt-in memory 的边界会决定隐私、串扰和忘却语义。
- **怎么证明不是测试泄漏？** 需要说明用于更新的输入、相邻样本、检索索引与评测目标是否重叠；更新后衡量的是适应能力还是已经看过目标的成绩。
- **额外计算是否值得？** test-time update 需要前向之外的梯度、fast-weight写入或 reward rollout；应和不更新的检索、search、长上下文基线区分开，不能只报告最终准确率。
- **什么时候保留或撤销更新？** 需要稳定性、跨任务遗忘、置信校准、rollback/reset 与失败检测，而不只是证明某个 benchmark 上一次更新有效。

本专题选择了不同目标和状态机制的代表工作，不是所有 test-time adaptation/TTA 文献的系统目录；尤其视觉域适应、纯多模态测试时校准和上线安全策略仍不在当前范围。
