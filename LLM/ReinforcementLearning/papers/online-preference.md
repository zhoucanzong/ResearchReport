# Online Preference Optimisation：偏好数据分布随策略移动

> **原文版本**：arXiv:2403.08635v1，2024-03-13。选择性精读 §4–6 与 Appendix B.1，未重跑作者实验。原文：[HTML](https://arxiv.org/html/2403.08635v1)。

## 亮点与差异

- **一句话亮点**：将 IPO 偏好损失放进当前策略生成数据的在线回路，说明它的期望更新与偏好博弈自我对弈可等价，并提出带正则化混合采样的 IPO-MD。
- **新在哪**：不把 IPO、DPO、RL 简化为 loss 名称对比，而显式拆开 contrastive/non-contrastive、online/offline、regularised sampling 三个设计轴。
- **证据强度**：论文给出理论等价分析；实证只在 TL;DR/XSum 摘要任务、T5X 770M 策略上做，偏好评估由 PaLM 2 judge 产生，三个 seed；未证明一般对话任务上的排序。
- **值不值得引用**：适合支撑“在线/离线是独立于 DPO/IPO 损失形式的关键维度”，不适合引用成普遍的在线 RL 胜率定律。

## 七问

1. **解决什么问题？** 固定偏好数据在策略更新后可能不能代表当前策略会生成的回答；IPO 原为离线目标，而 Nash-MD-PG 是在线偏好模型方法。论文试图组合偏好对比损失与在线样本分布，并用正则化采样控制策略偏移。
2. **核心方法？** Online IPO 把离线 IPO 期望中的固定生成分布换为当前策略分布。Online IPO-MD 再以当前策略和参考策略 logits 混合采样。作者证明在线 IPO 的期望更新与偏好模型上的 Nash 自我对弈解有关；文中将其与 online DPO 区分。训练设置默认学习率 1e-4、30,000 步、batch 32、AdaFactor，正则系数 τ 固定，未用 warmup；最优 τ 需要 sweep。[§4–5、§6]
3. **数据与规模？** 摘要偏好训练集 D_Train 92,820 对；SFT policy 为 T5X-L、770M 参数，偏好/奖励模型为 T5X-XL、3B。偏好/奖励模型以 TL;DR 数据训练；在线生成使用 XSum 训练 prompts；验证/测试 prompts 为 XSum。在线实验在 4×4 TPU v5e 配置运行。[§6]
4. **主要结果？** 表 2 是对称的 pairwise preference 矩阵：在 IPO 与 IPO-MD 对比中，IPO 被偏好的比例为 0.515 (std 0.024)；在线 IPO 与 IPO-MD 对比也有相近差异。作者结合 seed 标准差后认为 IPO 与 IPO-MD 的表现统计上难以区分，且两者都稳健地胜过其他算法。不能把该表读成“在线优于全部离线方法”：它比较的是在线算法；离线结果在 Appendix B.1 单列。[Table 2、§6.1]
5. **消融说明什么？** 正则参数 τ 改变结果：小正则下 IPO 与 DPO 类似，较大 τ 时 IPO 分数衰减更快。更强正则还需要更多训练步数才到最佳点。作者用 online/offline regularisation sweep 展示在线方法在其设定下占优，但同时解释起点 SFT 已可生成优质摘要，数据条件对 online 有利。[§6.2、Appendix B.1]
6. **什么条件下失效或证据不足？** 任务限于文章摘要；偏好模型与 PaLM 2 judge 都可能有代理偏差；使用最佳 checkpoint 对照；初始化数据让当前策略很快产生高质量回答。论文自己要求在一般对话代理上继续验证。在线更新增加 rollout 与评估成本，不能只凭排序推断总体训练成本更低。
7. **与同类工作的可判定差异？** 标准 DPO/IPO 可在离线偏好对上直接优化；本文的 Online IPO 用当前策略重新生成回答再由偏好模型标注，IPO-MD 又额外混合 reference sampling。与 RLHF-PPO 不同，它仍以对比偏好损失为更新形式；数据在线并不等价于“使用 reward model 的 RL”。

## 引用锚点

- 在线/离线与其他方法属性：§3 Table 1。
- Online IPO 的分布替换与算法：§4.1，式 (10)–(11)。
- IPO-MD 的混合采样：§5.1。
- 数据、T5X 设置、评估模型及训练配置：§6，§6.1。
- side-by-side 与局限：§6.1 Table 2，§6.2，Appendix B.1。
