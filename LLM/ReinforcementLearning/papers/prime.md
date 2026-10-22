# PRIME：用终局标签在线学习 token 级隐式过程奖励

> **原文版本**：arXiv:2502.01456v2，2025-09-26。选择性精读方法、主要结果、密集/稀疏对照及 PRM 初始化/在线更新分析；未复现训练。原文：[HTML](https://arxiv.org/html/2502.01456v2)。

## 亮点与差异

- **一句话亮点**：不收集逐步“正确/错误”标注，而以当前策略 rollout 的终局标签在线更新隐式 PRM，再从隐式 PRM 取得 token 级密集优势信号。
- **新在哪**：把 outcome reward、可在线更新的隐式过程 reward 和 PPO/RLOO policy update 放在一个回路中；过程信号由奖励模型与参考模型的逐 token log-prob 比构造。
- **证据强度**：七个数学/代码基准，Qwen2.5-Math-7B-Base 的 SFT 起点，8×A800；作者报告多个训练步数和 reward/verifier ablation，但未跨团队复现，且完整训练细节仍依赖其特定代码和数据流水线。
- **值不值得引用**：适合解释在线 reward-model 更新如何追踪 rollout 分布及密集信号的来源；不应写成逐 token 真值监督，也不保证去掉所有奖励漏洞。

## 七问

1. **解决什么问题？** 结果级奖励稀疏，传统 PRM 需要昂贵、定义含混的逐步标签；静态 PRM 又会在策略优化改变 rollout 分布后失准甚至被利用。PRIME 目标是在只有可判定终局标签的场景中，低成本地产生随策略更新的过程信号。[§2.2]
2. **核心方法？** 初始化 policy、implicit PRM、reference model 于同一 SFT/base checkpoint。每轮从当前 policy 为每个 prompt 采 4 个回答，用 outcome verifier 打分并筛选，再由 r_phi(y_t)=β log[π_phi(y_t|y_<t)/π_ref(y_t|y_<t)] 得到 token 级信号；使用终局标签的交叉熵在线更新 π_phi，结合 RLOO/Monte Carlo outcome-return 与 process-return 计算优势，最后 PPO clipping 更新策略。[§3.1–3.2、Algorithm 1]
3. **数据与规模？** 数学 outcome reward 是答案 exact match 的 0/1；代码 reward 是通过测试数占比。基准含 AIME 2024、AMC、MATH-500、MinervaMath、OlympiadBench、LeetCode、LiveCodeBench v2。用 veRL、8×A800；policy LR 5×10^-7，PRM LR 10^-6，batch 256、microbatch 8、每轮 256 prompts×4 rollouts；β=0.05，所有实验 KL coefficient=0。[§4.1]
4. **主要结果？** Eurus-2-7B-SFT 平均 28.8；PRIME 训练 592 步的 Eurus-2-7B-PRIME 平均 43.9，作者称平均提升 15.1%；AIME 2024 pass@1 为 26.7%。此组结果不是同预算比较：表 1 的 RLOO + outcome verifier 为 240 步，PRIME 主模型为 592 步；另一个等 240 步对照中，PRIME 在多项指标普遍更高。表格数值 43.9−28.8=15.1，是平均分数差；不要在不说明分母时把作者“15.1%”改写成相对百分比。[Table 1、§4.2]
5. **消融说明什么？** 同为 240 步时，PRIME 行的多项 benchmark 通常高于 outcome-only RLOO；较长训练的主模型最终更高。用 SFT checkpoint 直接初始化隐式 PRM，优于用额外 500K 合成数据训练的 EurusPRM；作者推断同源初始化降低策略与 PRM 分布差异。移除在线 PRM 更新后，PRM 分类准确率随 RL 逐渐下降，在线更新可缓解 overoptimization/reward hacking。[Table 1、§4.3、§5.1]
6. **什么条件下失效或证据不足？** 仅测试 32B 及以下，论文 limitation 明确提到资源约束和缩短的部分消融；PRM 的“正确性”仍受终局 verifier 制约。过程分数是 log-prob 差，不具备逐步真值解释。过程 reward 与 outcome reward 直接相加会有数值不稳定，论文采用分开计算回报。即使在线更新，若 verifier 错、任务未覆盖或奖励被利用，也无法从机制上保证真实目标。
7. **与同类工作的可判定差异？** outcome-only RL 将终局奖励传播到回答级优势；常见 PRM 要单独收集过程标签训练。PRIME 用 outcome 标签更新语言模型形式的 implicit PRM，把相对参考模型的 token 差值当过程信号，因此不需要单独的逐步标签收集，但仍需要可用的终局 verifier 和在线 rollout。

## 引用锚点

- 挑战与方法概览：§2.2、Figure 1。
- 隐式 PRM 定义：§3.1，式 (3)。
- rollout—标签—在线更新—策略更新流程：Algorithm 1。
- 优势函数：§3.2，式 (4)–(6)。
- 训练配置与基准：§4.1。
- 主要分数与公平预算注意：§4.2–4.3，Table 1；版本与来源入口见 [MANIFEST S2](../sources/MANIFEST.md#sources-manifest--llm-reinforcement-learning)。
- 初始化与在线更新消融、局限：§5.1、Appendix A。
