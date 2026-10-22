# LOOP：长时序交互中更新 token、turn 还是整条轨迹

> **原文版本**：arXiv:2502.01600v3，2025-03-08。选择性精读 LOOP 算法、AppWorld 设置、主表、多次训练运行和行为分析；未复现训练。原文：[HTML](https://arxiv.org/html/2502.01600v3)。

## 亮点与差异

- **一句话亮点**：把 LLM 对多轮有状态 API 环境的交互视为 POMDP，并以 LOO 优势加 PPO 更新，不训练 value network；实验显示 token 级更新比 turn/trajectory 粒度稳定。
- **新在哪**：不是再给单次回答加更长 CoT，而是从环境响应构造完整交互轨迹，过滤环境返回 token，只对策略产生的 token 做概率比与策略梯度。
- **证据强度**：AppWorld 的多个优化基线、24 个训练场景、包含未见 app 的 challenge 测试；主表 checkpoint 按 dev 选取后做 5 次评测，补充表跨 3 个训练运行，作者自报、未独立复现。
- **值不值得引用**：适合支撑长时序 agent 的决策粒度、反馈延迟和探索多样性讨论；不能外推成“无 critic 一定优于 critic”或“交互 RL 总优于 SFT/DPO”。

## 七问

1. **解决什么问题？** 既有推理 RL 常将整段生成看成一个回答动作；真实数字 agent 必须多次调用有状态 API，每次动作都改变后续观察。训练需要处理部分可观测状态、长轨迹终局奖励和昂贵 rollout。
2. **核心方法？** LOOP = leave-one-out proximal policy optimization。每个任务从当前策略采 K 条完整 POMDP trajectory，以其他 K−1 条轨迹的回报作 baseline，LOO advantage 为 A_k=K/(K−1)(R_k−mean_{i≠k} R_i)。PPO 对 rollout 更新若干 epoch；trajectory 的重要性比按策略生成 token 概率乘积计算。消融把 action 定义为全轨迹、turn 或 token；token 版本只对模型生成的 token 作更新，环境响应不进入策略概率。[§4.1–4.2、Algorithm 1]
3. **数据与规模？** Qwen2.5-32B-Instruct，LoRA；训练用难度 1/2 的 24 个场景，72 tasks；训练最多 40 次交互，eval 最多 50；每个任务 6 条 rollout；reward 是该任务 unit tests 通过比例。AppWorld 的 Test-N 为 56 场景/168 tasks，Test-C 为 139 场景/417 tasks，后者包含训练未见 app 的复杂任务。该基准有 9 个 app、457 API endpoints、1,470 个函数参数。[§5.1–5.2]
4. **主要结果？** Table 1 中 LOOP(token) 对 Test-N TGC 为 71.3±1.3、Test-C TGC 45.7±1.3；Qwen2.5-32B-Instruct base 分别 39.2±3.5、21.0±1.4，OpenAI o1 分别 61.9、36.7。作者报告 Test-N 相对 o1 +15%、Test-C +24%，这些是相对提升而不是百分点。主表是最佳 dev checkpoint 的 5 次评测；Table 2 跨 3 个训练运行平均，趋势相同但 LOOP bandit 训练方差高。[Table 1–2、§5.4、Appendix E]
5. **消融说明什么？** LOOP(token) > turn > trajectory；后两者更不稳定且重要性比更常被 clipping。GRPO 风格的 reward 标准差归一化让 Test-N 下降约 9 个百分点；作者认为它过度偏向回报一致、低标准差的轨迹。Monte Carlo baseline 的 RL 方法优于这组带 learned critic 的 PPO，但作者说明 critic PPO 需要额外调参、稳定性较差，不能推出所有 critic 都较差。[§4.2、§5.4]
6. **什么条件下失效或证据不足？** 方法依赖可重置、状态可验证的 AppWorld；只有 24 个训练场景，虽然 test-normal/challenge 评估较多，但环境仍是模拟 API。LOOP (bandit) 跨训练运行不稳定。不同算法的 action 粒度会改变优化和重要性权重，因此比较并非仅改一个系数。作者对小训练集泛化的解释是采样轨迹保持多样，仍是对该任务观察的机制解释，不是跨领域证明。
7. **与同类工作的可判定差异？** 与语言模型中把完整回复当作 bandit action 的 RLOO 不同，LOOP 允许 PPO 重用 rollout 多轮更新，并把交互序列拆成 token/turn/trajectory action 对照；相较 GRPO，LOOP 不必须按组标准差归一化，作者发现该归一化在 AppWorld 上有害。它也把环境反馈作为非策略生成 token 显式从概率比中排除。

## 引用锚点

- POMDP 轨迹及策略产生 token：§4.1，式 (6)–(8)。
- LOO 优势和 PPO：§4.2，Algorithm 1。
- AppWorld 任务、切分、奖励与训练预算：§5.1–5.2。
- 主结果和评估口径：Table 1、§5.4；跨训练运行 Table 2、Appendix E。
- 学到的行为、多样性及小数据解释：§5.5–5.6、Figure 3–4。
