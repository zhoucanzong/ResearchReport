# Candidate Screening — LLM Reinforcement Learning

截止 2026-10-23。**候选池 14 项，主报告深读 3 篇，原文选读 3 篇，失败边界选读 2 篇；其余 6 项保留为来源或待读。** 筛选标准是能否回答“轨迹来源、奖励可信度、策略更新与长时序探索”的教学问题；不是排行榜。

| 来源 ID | 工作 | 决定 | 取舍理由 |
|---|---|---|---|
| S1 | Online Preference Optimisation | **深读** | 用同一偏好目标拆出 online/offline 与 regularised sampling，适合解释两种轨迹分布的差别；实验范围清楚受限于摘要。 |
| S2 | PRIME | **深读** | 把 outcome supervision、隐式过程奖励的在线更新和 policy optimization 联成完整回路；有主结果、等步数比较、reward hacking 分析及 limitation。 |
| S3 | LOOP / long-horizon interactive agents | **深读** | 直接对比 token / turn / trajectory 更新粒度，含多环境交互任务、基准切分、消融与跨运行稳定性结果。 |
| S4 | WebRL | **选读** | 在线课程、终局 ORM、KL 约束、回放的组合为 agent RL 提供有解释力的案例；不另做逐篇分册以避免与 LOOP 的主线重复。 |
| S5 | WebAgent-R1 | **选读** | on-policy 多轮 rollout + rule reward，并有行为克隆起点消融；与 WebRL 互补地展示探索冷启动条件。 |
| S6 | LLMs Gaming Verifiers | **失败边界选读** | 2026 年原文研究验证器外延正确与规则泛化的差别；说明“可执行 reward”仍可能鼓励捷径。 |
| S7 | Verifier-Induced Support Reshaping (v2, 2026-09-29) | **摘要级候选** | 与探索支持集、跨任务泛化直接相关，但本轮只核到 v2 摘要，不将结论写成已全面复核。 |
| S8 | RLVR Implicitly Incentivizes Correct Reasoning | **候选** | 正向机制研究，ICLR 2026 摘要提出 CoT-Pass@K 与推理质量分析；尚未读正文，因此不纳入结论。 |
| S9 | AgentGym-RL | **候选** | 多环境 agent RL 与渐进增加交互 horizon；当前报告以 AppWorld 与 WebArena 两个可核细案例为主。 |
| S10 | OpenWebRL | **选读** | 将训练扩展至 live web 视觉 agent，公开研究 judge 类型、轨迹奖励及 judge hacking 对照；补充 WebArena 自托管环境案例。 |
| S11 | OREO | **候选** | 离线多步推理 RL，可补静态偏好数据与值函数/支持集方向；与本轮重点的轨迹来源比较较远，留待后续。 |
| S12 | DeepSeekMath / GRPO | **交叉参考** | Alignment 已覆盖 GRPO 的组内优势与来源；在此重写会造成机制重复。 |
| S13 | DAPO | **排除重复** | Alignment 已有 DAPO 四项设计、原文核对和消融，不再重复。 |
| S14 | VAPO | **排除重复** | Alignment 已有长链 critic/GAE 和长度异质奖励阅读，不再重复。 |

**筛选结论**：主文有 3 篇逐篇深读、3 篇原文选读，候选池其余工作均有状态和理由。S6 的奖励利用例子不代表 agent 普遍会作弊，也不代表任何产品的私有训练方法；只支撑“评分器对未检查属性无法给保证”。
