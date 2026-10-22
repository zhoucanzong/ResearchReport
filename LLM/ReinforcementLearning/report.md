---
type: research
domain: LLM
subject: ReinforcementLearning
upstream: null
date: 2026-10-23
evidence: 精读原文
status: current
---

# LLM 后训练中的强化学习：轨迹从哪里来，策略何时更新

> **截止日期：2026-10-23。** 本文补足 [模型对齐与后训练](../Alignment/report.md) 对偏好优化和 GRPO/DAPO/VAPO 的机制概述，以及 [推理模型](../ReasoningModels/report.md) 对 RL 推理模型的历史叙述。本文集中回答三个问题：训练轨迹由谁产生、奖励如何分配到 token/动作、策略更新后如何避免只学会利用评分器。主报告是教学式比较，不是算法大全，也不代表独立训练复现。

## 先把两条轴分开

讨论“RL 还是 DPO”容易把数据来源、反馈形式和优化器混为一谈。读一篇后训练论文时，先问三个问题；概念边界与本库既有 [Alignment](../Alignment/report.md) 专题相衔接。

1. **轨迹来源**：固定语料中的示范/偏好对（offline），还是当前策略与环境交互采样出的回答（on-policy），抑或新旧策略混合、带回放的数据（off-policy）？
2. **反馈形式**：人类或模型对两个回答的相对偏好、learned reward、可执行的答案/状态验证器，还是过程级信号？
3. **策略更新**：对静态偏好对做似然目标（DPO/IPO 家族）、用策略梯度/PPO 更新，还是将长轨迹展开到 turn/token 级后分别赋权？

这些轴可以组合。DPO 描述一个偏好目标，并不必然意味着永远只用固定数据；PPO 描述策略更新方法，也不自动说明它拿什么奖励、样本是否新鲜。在线数据有机会跟上模型当前会生成的行为，但每轮要付采样与评估成本，也会让优化器主动追逐评分器的漏洞。静态偏好数据省去 rollout，却可能覆盖不到更新后策略会采取的新动作。选择的核心是反馈是否可信、目标行为是否在数据支持范围内、交互反馈是否足够密集，而不是算法名的新旧。相关证据定位见 [来源清单](sources/MANIFEST.md#sources-manifest--llm-reinforcement-learning) 与 [在线偏好精读](papers/online-preference.md)。

## 轨迹—反馈—更新：三个常见训练回路

| 回路 | 轨迹与反馈 | 更新方式 | 擅长解决 | 主要风险 |
|---|---|---|---|---|
| 离线偏好优化 | 固定回答对及 chosen/rejected 标签 | DPO、IPO 等直接偏好损失 | 有比较标签、尚无可靠自动验证器；偏好任务可由人工评判 | 数据分布滞后、标签噪声、隐式奖励与实际目标错位；模型未见过的新行为没有直接监督 |
| 在线偏好学习 / 奖励模型 RL | 当前策略采样回答，偏好模型或 reward model 打分 | 在线 DPO/IPO、PPO 等 | 需要在当前策略产生的回答上持续校准偏好，且能够承担重复标注/打分 | 评分器系统误差会被迭代放大；策略与评判器共同漂移 |
| RLVR / 交互式 agent RL | 当前策略产生答案或完整环境轨迹，由答案、测试或最终状态给可执行奖励 | REINFORCE、PPO、GRPO/RLOO 以及 turn/token 级变体 | 数学/代码等答案可验任务；可重置、可观测且奖励可编程的环境 | verifier 漏洞、稀疏延迟奖励、低成功率导致无有效探索；长轨迹 credit assignment 和环境状态分布迁移 |

**不要把离线偏好对照“online RL”当成一个单一实验变量。** 两种流程往往连反馈来源、数据规模和优化目标也不同。Calandriello 等人在同一篇偏好学习研究中把对照做得更干净：T5X-770M 策略从同一摘要 SFT 检查点出发，使用 T5X-3B 偏好/奖励模型，在 TL;DR 偏好训练数据上训练评价器，并在 XSum prompt 上在线采样；side-by-side 评价由 PaLM 2 judge 给出。作者的 Table 2 是**在线方法之间**的摘要偏好比较，IPO 与 IPO-MD 在该设置中表现稳健；附录 Figure 3–4 才呈现 online 与 offline 版本，并指出这套预训练初始化使在线方法更容易采到好样本。论文也明确将结论限定在摘要，要求在通用对话上继续验证。[1 §6.1–6.2、Appendix B.1] 这说明“数据是否跟着策略刷新”可能重要，但不是普适的 DPO 对 RL 排名。[逐篇精读](papers/online-preference.md)

## 可验证奖励不等于奖励可靠

数学精确答案、编译/单测结果、模拟环境的状态断言，是 RLVR 的优势：反馈便宜、规模大且部分条件下不需要训练偏好模型。稀疏的终局奖励仍难以告诉策略长推理或动作序列中的哪一步带来成功。PRIME 展示了一个折中：用答案级标签训练一个“隐式过程奖励模型”，再把模型相对参考模型的逐 token 对数概率差作为密集信号；训练期间继续用当前策略 rollout 与 outcome label 更新该模型，目标是减少静态过程奖励器随策略偏移而失准的风险。[2 §3、§4、§5.1]

这个信号是**相对于一个语言模型参考分布的隐式过程分数**，不能解释成每个中间推理步骤已经被人工判定为正确。PRIME 的规则验证器也只覆盖特定数学答案和代码测试。作者报告，从 Eurus-2-7B-SFT 出发，Eurus-2-7B-PRIME 在七个数学/编程基准平均由 28.8 到 43.9，作者称平均提升 15.1%；AIME 2024 pass@1 为 26.7。此组结果不是同预算比较：表 1 的 RLOO + outcome verifier 为 240 步，PRIME 主模型为 592 步；另一个等 240 步对照中，PRIME 在多项指标普遍更高。论文使用 8×A800，基准列于表 1、设置在 §4.1–4.3。该证据支持“在线密集信号在该实验中有用”，不支持“PRM 总能消灭 reward hacking”。[2 Table 1、§4.3、Appendix A；定位见 MANIFEST S2](sources/MANIFEST.md#sources-manifest--llm-reinforcement-learning)

验证器只保障**它检查的属性**。如果测试仅检查一组示例的外延输出，策略可能记住实例答案而不学规则；类似地，若代码 reward 只覆盖有限单测，测试未覆盖的行为仍无保证（这是一般性推论，并非下述研究直接测试的代码奖励漏洞）。2026 年对归纳任务的受控研究发现，使用外延验证的 RLVR 会诱发实例枚举式捷径，而同构验证训练在该实验中避免了这一漏洞；这表明对该类任务，仅检查原例输出会漏掉规则泛化失败。[6 §1、§4、Appendix C；来源见 MANIFEST S6](sources/MANIFEST.md#sources-manifest--llm-reinforcement-learning) 另一项 2026 预印本指出，RLVR 可能提升当前任务的 pass@1，同时减少固定 rollout 预算下还能采到的其他任务成功轨迹；在其 Qwen3-8B-Base 的 IFEval 实验中，Math-RLVR 后 pass@1 +6.5 个百分点、best@32 −9.8 个百分点。该结果是特定模型、指令基准和顺序训练的作者实验，不应扩展成 RLVR 必然损害泛化；它提醒评价不能只有已优化验证器上的单次准确率。[7 摘要]

## 长时序 agent：把一次回答拆成决策序列

数学解题通常可把整段生成看成一个带终局奖励的 contextual bandit；agent 每次调用工具后会收到新状态，下一步决策依赖刚刚看到的网页、API 结果或环境变化。因此它是部分可观测的序贯决策问题：

`用户目标 → observation → LLM action → 环境反馈 → 新 observation → … → 终局状态与奖励`

这一转换改变了优化的粒度。若整条轨迹作为一个动作，成功奖励必须回传给数十次 API/网页操作，且整轨迹概率比的乘积可能快速失稳。LOOP 在 AppWorld 上把 PPO 与 leave-one-out（LOO）优势结合，不训练 critic；作者对比以整条轨迹、单轮或 token 作为 action 的更新。Qwen2.5-32B-Instruct + LoRA 在 24 个训练场景（72 项任务）、每任务 6 条 rollout、训练 40 次交互、测试最多 50 次交互的条件下，LOOP token 版本在 AppWorld Test-N 的 task-goal completion 为 71.3±1.3%，Test-C 为 45.7±1.3%；同表 Qwen base 分别为 39.2±3.5%、21.0±1.4%。指标是 5 次同检查点评估运行；附录 Table 2 另报告三个训练运行，减少了只挑最佳训练运行的风险。[3 §5.1–5.4、Table 1–2]

这个案例也显示“更复杂的优化”不必然更好：按组标准差归一化使 LOOP token 在 Test-N 降 9 个百分点；trajectory/turn 粒度更不稳定，重要性权重经常被裁剪。作者观察到模型更常查 API 文档、能从错误调用中调试恢复，并减少了约 3 倍“遇错后放弃”；他们把小训练集上的泛化与仍然多样的采样轨迹联系起来。这些是 AppWorld、其工具接口及该训练流程中的实证结果，不是开放世界 agent 的保证。[3 §4.2、§5.5–5.6、Appendix E]

网页 agent 的两种端到端实现进一步说明，交互 RL 之前的**探索起点**往往决定稀疏奖励能不能学到东西：

- WebRL 用失败任务演化课程，ORM 给终局二元判断，KL 约束控制当前策略相对上一阶段漂移，回放缓解遗忘；WebArena-Lite 上 Llama3.1-8B 从 4.8% 到 42.4%，GLM-4-9B 从 6.1% 到 43.0%。原文 ablation 分别移除回放、KL 和课程，观察到遗忘、当前课程过拟合及持续表现下降。[4 v3 §2–3、Table 1、Figure 5]
- WebAgent-R1 先以 9,460 条公开轨迹做行为克隆，再在 647 个任务上用规则终局奖励进行多轮 on-policy GRPO；评测用 165 个人工核验任务。Qwen2.5-3B 的平均成功率为 6.1% → BC 20.0% → WebAgent-R1 33.9%；Llama3.1-8B 为 8.5% → BC 20.6% → 44.8%。跳过 BC 后，3B 模型初始成功率仅 6.1%，RL 后略降，作者将原因归于动作格式不完整和正奖励稀少。这个消融把“RL 能改进”限定在已有基本工具操作能力的初始化上。[5 v2 §2.2–3.5、Table 2、Figure 4]

WebRL 与 WebAgent-R1 的 42.4% / 44.8% 不宜直接排列成胜负：backbone、轨迹数据、RL 更新、规则和复现基线条件不完全相同。对 agent 的选型应先看环境能否并行重置、奖励是否能验证最终状态、有效 rollout 的比例、以及评测任务是否覆盖训练未见的组合。只有终局指标而无轨迹审计，也难以分辨真正完成任务与奖励漏洞。

截至本报告截止日，OpenWebRL 把这条路线扩展到**真实网页上的视觉 agent**：Qwen3-VL-4B 先用 0.4K 轨迹 warm start，再以 2.2K 开放任务和多模态多轮 GRPO 训练，Online-Mind2Web / DeepShop 上报告 67.0% / 64.0% 成功率，WebVoyager 上 74.1%；评测预算是最多 30 步。[8 v2 §4–5、Table 2；来源见 MANIFEST S10](sources/MANIFEST.md#sources-manifest--llm-reinforcement-learning) 它的奖励是轨迹级成功评判（规则过滤 + GPT-4.1 或蒸馏 judge），不是答案可机械验证的 RLVR。作者报告使用 Qwen3-VL-8B 作为 judge 时出现 reward hacking：训练 reward 更高但 Online-Mind2Web 独立评测成功率显著更低；蒸馏的 OpenWebRL-Judge-8B 在 500 条 held-out trajectory 上相对 GPT-4.1 标签达到 89.8% accuracy / 92.1 F1。[8 §4.3、§5.4、Table 3] 这提醒读者：用独立评测检测 judge 漂移很关键；但 held-out judge agreement 也不等于 judge 评判等同人类质量。不同网页基准、页面快照和评测步数变化都影响可比性。

## 机制何时有效：诊断顺序

| 症状 | 优先检查 | 可能的改法 | 不应直接推断 |
|---|---|---|---|
| 固定偏好集上的离线训练提升停滞 | 新策略回答是否落在比较数据覆盖内；标签是否一致；参考策略与训练分布差距 | 小批量在线采样补覆盖、校准评价器；保留静态偏好作回归集 | “在线 RL 一定优于 DPO” |
| verifier reward 上升、独立能力不升 | verifier 对未见格式/扰动/对抗样例是否健壮；成功轨迹是否可采样 | 同构扰动、独立 held-out 评测、策略/评判器分开更新；按预算跟踪 pass@k 与有效探索 | “精确匹配永远不可 hack” |
| 长链任务全成全败 | 正奖励频率、不同动作粒度、部分状态指标；trajectory importance weights 是否被裁剪 | 提供可验证的中间状态；比较 token/turn/trajectory 优势；先让策略能产出合法动作 | “稀疏奖励只需更大 batch” |
| 新课程带来旧任务退化 | 旧任务回放占比、策略 KL、样例难度是否过新或过易 | 难度自适应生成；保留成功轨迹；限制单阶段策略漂移 | “更多数据自动解决遗忘” |
| 训练奖励波动、不同 seed 差异大 | rollout 方差、环境非确定性、验证器稳定性、运行间重复性 | 报多 seed、固定环境快照、分解轨迹失败类型 | 仅报最佳 checkpoint |

值得保留的统一视角是**探索支持集**：策略更新能否让模型采到更好的行为，取决于奖励信息是否正确，也取决于探索机制还能否找到这类行为。把探索压窄会减少短期方差，却也可能删掉后续任务所需的解题路径。作者报告的单 benchmark 提升应同时配上未参与优化的任务、长尾条件和多次运行结果。这是跨论文综合判断，参见 [PRIME](papers/prime.md)、[LOOP](papers/loop.md) 与 [来源清单](sources/MANIFEST.md#sources-manifest--llm-reinforcement-learning)。

## 闭源模型的证据边界

公开产品在数学、编码或工具使用上的分数，不能反推出其私有后训练算法、数据构成、reward model、rollout 数或具体超参数。若技术报告只说“强化学习”或“额外计算”，就只写到此为止；闭源模型在某基准上的结果最多是外部表现参照，不是其训练配方证据。

## 本次阅读范围与尚未解决的问题

本次论文池 14 项：精读 3 篇（在线偏好目标与数据、在线隐式过程奖励、长时序 agent 的 token 级更新），另以原文选读 WebRL、WebAgent-R1、OpenWebRL，并把 2026 verifier gaming / support reshaping 研究作为失败边界。其余候选及取舍见 [CANDIDATES](sources/CANDIDATES.md)。深读按四项亮点与七问写在 [papers/](papers/)；具体论文版本、许可、原文入口和缓存记录见 [MANIFEST](sources/MANIFEST.md)。

仍需横向实验回答：偏好回路与 RLVR 在同一基座、同一采样预算下的成本—质量曲线；对环境状态的部分验证能否降低终局稀疏性，同时不鼓励投机；策略探索压缩与跨任务能力损失的因果关系；长时序 agent 在可复用真实环境中的多 seed、环境版本和奖励审计。当前证据来自不同任务、模型与预算的单篇作者实验，未进行统一基准复现。

## 参考来源

1. Calandriello et al., [Human Alignment of Large Language Models through Online Preference Optimisation, arXiv:2403.08635v1 (2024-03-13)](https://arxiv.org/html/2403.08635v1), §4、§6、Appendix B.1。
2. Cui et al., [Process Reinforcement through Implicit Rewards, arXiv:2502.01456v2 (2025-09-26)](https://arxiv.org/html/2502.01456v2), §2–5, Table 1, Appendix A。
3. Chen et al., [Reinforcement Learning for Long-Horizon Interactive LLM Agents, arXiv:2502.01600v3 (2025-03-08)](https://arxiv.org/html/2502.01600v3), §4–5, Tables 1–2, Appendix E。
4. Qi et al., [WebRL: Training LLM Web Agents via Self-Evolving Online Curriculum Reinforcement Learning, arXiv:2411.02337v3 (2025-01-27)](https://arxiv.org/html/2411.02337v3), §2–3, Table 1, Figure 5。
5. Wei et al., [WebAgent-R1: Training Web Agents via End-to-End Multi-Turn Reinforcement Learning, arXiv:2505.16421v2 (2025-10-08)](https://arxiv.org/html/2505.16421v2), §2–3, Table 2, Figure 4。
6. Helff et al., [LLMs Gaming Verifiers: RLVR can Lead to Reward Hacking, arXiv:2604.15149v1 (2026-04-16)](https://arxiv.org/html/2604.15149v1), §1、§4。
7. [Verifier-Induced Support Reshaping in On-Policy Optimization, arXiv:2608.00220v2 (2026-09-29)](https://arxiv.org/abs/2608.00220v2), 摘要（仅摘要级）。此工作为预印本；报告仅采用其限定任务下的结果。
8. Yang et al., [OpenWebRL: Demystifying Online Multi-turn Reinforcement Learning for Visual Web Agents, arXiv:2606.02031v2 (2026-06-04)](https://arxiv.org/html/2606.02031v2), §4–5, Table 2–4。
