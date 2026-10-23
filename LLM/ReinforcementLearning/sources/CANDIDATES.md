# Candidate Screening — LLM Reinforcement Learning

截止 2026-10-23。**候选池 18 项；8 篇逐篇深读（含两篇 verifier 审计），3 篇原文选读、1 篇失败边界选读、其余 6 项保留为候选、排除或交叉引用。** 新增过程标签来源、PRM/ORM 评价差异与答案奖励隐式筛选 CoT 的条件机制。筛选标准是能否回答“轨迹来源、奖励可信度、策略更新、验证器信息边界与长时序探索”的教学问题；不是排行榜。

| 来源 ID | 工作 | 决定 | 取舍理由 |
|---|---|---|---|
| S1 | Online Preference Optimisation | **深读** | 用同一偏好目标拆出 online/offline 与 regularised sampling，适合解释两种轨迹分布的差别；实验范围清楚受限于摘要。 |
| S2 | PRIME | **深读** | 把 outcome supervision、隐式过程奖励的在线更新和 policy optimization 联成完整回路；有主结果、等步数比较、reward hacking 分析及 limitation。 |
| S3 | LOOP / long-horizon interactive agents | **深读** | 直接对比 token / turn / trajectory 更新粒度，含多环境交互任务、基准切分、消融与跨运行稳定性结果。 |
| S4 | WebRL | **选读** | 在线课程、终局 ORM、KL 约束、回放的组合为 agent RL 提供有解释力的案例；不另做逐篇分册以避免与 LOOP 的主线重复。 |
| S5 | WebAgent-R1 | **选读** | on-policy 多轮 rollout + rule reward，并有行为克隆起点消融；与 WebRL 互补地展示探索冷启动条件。 |
| S6 | LLMs Gaming Verifiers | **失败边界选读** | 2026 年原文研究验证器外延正确与规则泛化的差别；说明“可执行 reward”仍可能鼓励捷径。 |
| S7 | Verifier-Induced Support Reshaping (v2, 2026-09-29) | **摘要级候选** | 与探索支持集、跨任务泛化直接相关，但本轮只核到 v2 摘要，不将结论写成已全面复核。 |
| S8 | RLVR Implicitly Incentivizes Correct Reasoning, arXiv:2506.14245v2 | **深读** | 给出 answer-only GRPO 奖励何时能间接偏好正确 CoT 的条件假设，并用 CoT-Pass@K 显示 Pass@K 会漏掉“答案对、推理错”；保留 judge 与数据集反例。 |
| S9 | AgentGym-RL | **候选** | 多环境 agent RL 与渐进增加交互 horizon；当前报告以 AppWorld 与 WebArena 两个可核细案例为主。 |
| S10 | OpenWebRL | **选读** | 将训练扩展至 live web 视觉 agent，公开研究 judge 类型、轨迹奖励及 judge hacking 对照；补充 WebArena 自托管环境案例。 |
| S11 | OREO | **候选** | 离线多步推理 RL，可补静态偏好数据与值函数/支持集方向；与本轮重点的轨迹来源比较较远，留待后续。 |
| S12 | DeepSeekMath / GRPO | **交叉参考** | Alignment 已覆盖 GRPO 的组内优势与来源；在此重写会造成机制重复。 |
| S13 | DAPO | **排除重复** | Alignment 已有 DAPO 四项设计、原文核对和消融，不再重复。 |
| S14 | VAPO | **排除重复** | Alignment 已有长链 critic/GAE 和长度异质奖励阅读，不再重复。 |
| S15 | [Verifier Errors in RLVR](../papers/2609.35677-verifier-errors-selective-control.md) | **补充精读** | 用固定 verifier 下的可辨识性限制与审计控制分析 verifier reward 与 correctness 的分离；语言模型演示是构造的 0.5B 规则替换任务，不能推广到开放数学/代码训练。 |
| S16 | [Where the Verifier Fails](../papers/2609.01354-category-level-verifier-audit.md) | **补充精读** | 对四种答案 verifier 做类别级 metamorphic audit，分开 false-negative、false-positive 与 runtime failure；不含模型训练，不证明解析错误已导致 RLVR 策略改变。 |
| S17 | Let's Verify Step by Step, arXiv:2305.20050v1 | **精读并修订 ReasoningModels 旧概括** | 固定生成器采样 MATH 解答，人工标注正/负/中性步骤，第二阶段由 PRM 主动筛选高分但答案错的轨迹；不是 MCTS 生成轨迹。分开 Best-of-N 答案选择、过程错误定位和监督类型消融。 |
| S18 | The Lessons of Developing Process Reward Models in Mathematical Reasoning, arXiv:2501.07301v2 | **精读** | 比较 MC continuation 标签、LLM judge 与 PRM800K 人工标签。Best-of-8 终局准确率与 ProcessBench 首错定位 F1 排序不同；揭示 MC 标签是可解性代理、不是步骤真值。 |

**筛选结论**：S17–S18 补上过程标签如何构造、怎样评估与结果标签有何不同；S8 提供答案奖励可能隐式选择正确 CoT 的条件机制。它们与 S15–S16 的 verifier 可辨识性/实现审计相互补充，但分别测量训练标签、推理 judge、任务 verifier 的不同对象，不合并成“PRM 总优于 ORM”或“RLVR 必然学会正确推理”。
