# 模型对齐与后训练：方法、目标与证据边界

> 初稿日期：2026-06-06；证据修订：2026-10-22。
> 本文核对 RLHF、DPO、IPO、GRPO、DAPO、VAPO 与 Constitutional AI 的原文方法及关键实验。范围是机制综述与部分结果对账，不是完整的 2026 年方法目录，也未独立复现训练。

## 1. 执行摘要

后训练包含不同任务：指令遵循、偏好优化、可验证推理与安全行为塑造。它们的奖励、数据和评价方式不同。数学答案准确率上升不能直接证明更符合人类偏好；有害请求拒绝率上升也不能单独证明模型更有用。

RLHF 通过学习偏好奖励并优化策略；DPO 在特定偏好模型与 KL 正则化目标下把优化转为偏好对上的分类损失；GRPO 用同题多样本的组内奖励替代独立价值模型；DAPO 与 VAPO 则分别改进无价值模型和带价值模型的长链推理训练。[A1–A6] 这些论文没有给出跨模型、跨任务通用的“质量上限”排名，也不支持固定的显存节省百分比。

安全侧，Constitutional AI 包含原则驱动的监督自我修订与 AI 偏好反馈 RL 两阶段；“不使用人类无害性偏好标签”不能改写成“整个系统完全无人类数据”。原则设计、有用性数据和人工评价仍需区分。[A7]

## 2. 核心文献与结论范围

| 编号 | 工作、时间与固定版本 | 一句话贡献 | 原文核验位置 |
|---|---|---|---|
| A1 | InstructGPT，2022，2203.02155v1 | 用示范、偏好比较和 PPO 改进指令遵循 | §3 方法；本轮仅方法核对，未重新对全部结果打分 |
| A2 | DPO，2023，2305.18290v2 | 在 Bradley–Terry 假设下以策略概率比表达隐式奖励 | §3–4，§6 |
| A3 | IPO，2023 预印本 / AISTATS 2024，2310.12036v2 | 在 ΨPO 框架中采用 identity 映射并推导可优化目标 | §4.2、§5 |
| A4 | DeepSeekMath，2024，2402.03300v3 | 提出 GRPO 并研究数学预训练、SFT 与 RL | §4.1–4.2 |
| A5 | DAPO，2025-03，2503.14476v1 | 组合四项训练改动并公开训练系统 | §3、§4 |
| A6 | VAPO，2025-04，2504.05118v1 | 对长 CoT 中的价值估计、长度异质与稀疏奖励做联合设计 | §4、§5 表 1 |
| A7 | Constitutional AI，2022，2212.08073v1 | 以原则生成修订与 AI 偏好信号来训练无害性 | §1.2、§3–4 |

以上是作者单篇实验或方法推导；彼此采用的基础模型、数据和预算不同，不视为多方独立复现。

## 3. RLHF 与 DPO：两种优化路径

RLHF 的典型流程是 SFT → 奖励模型 → 策略优化。[A1 §3] 对同一输入 (x) 的偏好对 (y_w,y_l)，常用 Bradley–Terry 模型拟合：

\[
\mathcal L_{RM}=-\mathbb E\log\sigma(r(x,y_w)-r(x,y_l)).
\]

策略目标可写成奖励与相对参考策略的 KL 惩罚之和。PPO 是一种优化实现，不能把抽象的奖励目标公式直接称为完整 PPO 算法：后者还涉及旧策略采样、概率比裁剪与优势估计。[A2 §3]

DPO 在同类偏好假设下得到：[A2 §4，式 7]

\[
\mathcal L_{DPO}=-\mathbb E\log\sigma\left(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)}-\beta\log\frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}\right).
\]

这避免了在该训练步骤中显式拟合奖励模型和在线 rollout，但不保证每项任务上都比在线 RL 稳定或准确。静态偏好数据的覆盖、标签噪声与参考策略都会影响效果。原稿“RLHF 质量上限最高”“DPO 只有中等质量”“显存固定为 1/2–1/3”缺少统一对照，已移除。

IPO 不是一般意义上的“高置信度处继续学习”补丁。其原文分析确定性偏好与弱正则化时 DPO 的过拟合，采用 identity 映射得到目标对数概率差的平方损失；其理论与示例说明应连同假设使用，不能据此承诺所有噪声数据上优于 DPO。[A3 §4.2、§5]

## 4. GRPO：组内相对奖励替代价值模型

对同题采样 (G) 个回答，以组内奖励均值和标准差构造优势；结果监督版本把该回答的优势用于各 token，再配合裁剪与 KL 项更新策略。[A4 §4.1] 原文也研究过程监督，不能把所有 GRPO 都简化为仅有末尾奖励。

去掉价值模型确实改变资源构成，但显存还包括策略/参考模型、优化器状态、激活、rollout 与并行方案，故不存在由算法名称直接推出的“固定节省 30%”或“固定节省 50%”。当同题所有回答奖励相同时，标准化的组内信号为零；实现还需处理零标准差。[A4, A5 §3.2]

## 5. DAPO：原文四项改动及消融含义

原稿把 DAPO 记为 2025-01、引用到错误 ID，并把四项改动写错。本次按 **2503.14476v1 §3** 更正为：

1. **Clip-Higher**：拆开概率比的上下裁剪阈值，提高上界以缓解熵塌缩；不是“策略裁剪与参考模型裁剪解耦”。
2. **Dynamic Sampling**：过采样并过滤组内全对或全错的问题，直到有效问题填满训练 batch；不是动态调整每题的组大小 (G)。
3. **Token-Level Policy Gradient Loss**：改变 batch 中 token 的归一化权重；不是新添逐 token 正确性奖励。
4. **Overlong Reward Shaping**：处理截断与超长回复的奖励噪声；不是把“熵奖励”列为第四项。

Qwen2.5-32B base、AIME 2024 条件下，作者报告 DAPO **50 分**，其初始 GRPO run **30 分**；论文还引用 DeepSeek-R1-Zero-Qwen-32B 的 **47 分**。[A5 §1、§4] 这区分了作者自己的复现基线与另文报告值，不能改写成“所有代码与数学任务普遍提升 5–10% pass@1”。

消融研究的是这套实现中的训练改动，无法证明每个组件在任意数据与 rollout 预算下都保持相同效应。比较时还应核对采样数、最大回复长度、训练步数与截断规则。

## 6. VAPO：价值模型路线的对照

VAPO 的全称是 **Value-based Augmented Proximal Policy Optimization**；原稿的“Value-based RL with Adaptive GAE”不是论文题名或准确展开。它保留价值模型，通过 value pretraining、decoupled GAE、length-adaptive GAE 等处理长链估计与训练问题。[A6 §4]

| 原文表 1 | AIME24 avg@32（论文表中整数） | 实验解释 |
|---|---:|---|
| 完整 VAPO | 60 | Qwen2.5-32B、作者配置下的结果 |
| 不做 value pretraining | 11 | 在同一配方中，初始价值估计很关键 |
| 去掉 decoupled GAE | 33 | policy 与 critic 的 GAE 配置有影响 |
| 去掉 length-adaptive GAE | 45 | 不能把整体增益全归给单一组件 |
| 去掉 token-level loss | 53 | token 权重同样影响结果 |

表中结果按原表整数保留；摘要的 **60.4** 与表 1 的 **60** 不应混写成两个独立实验。[A6 §5.2] 这支持“价值模型训练得当时可以有效”，并不推翻无价值模型路线，也不能外推成所有长文本、多轮对话都应使用 VAPO。

## 7. Constitutional AI：安全信号从何而来

监督阶段由原则引导批判与修订，再用修订答案训练；RL 阶段用原则引导的 AI 比较形成偏好信号，训练偏好模型并优化策略。[A7 §1.2、§3–4]

原稿遗漏第二阶段，并宣称“完全无需人类偏好数据”。准确边界是论文旨在减少**无害性监督**中的人工标签，仍使用人类编写原则与有用性反馈。AI 反馈也可能继承评判模型偏差；此处的有用性/无害性结果不能当作所有价值观和攻击分布的保证。

对安全方法的评价至少需要有害请求成功率、正常请求误拒绝率、任务效用以及攻击/语言/多轮条件。只提高拒绝率或奖励分数可能掩盖退化。这是本文的综合评价建议，不是某一算法附带的保证。

## 8. 选型与未决问题

| 目标 | 候选路径 | 接受前必须验证 |
|---|---|---|
| 已有离线配对偏好 | DPO；IPO 作有理论动机的对照 | 数据覆盖、噪声、参考策略、偏好与独立任务评价是否一致 |
| 有可验证数学/代码奖励 | GRPO / DAPO | 验证器漏洞、有效组比例、采样成本、长度偏差 |
| 能维护价值模型的长链 RL | VAPO 或 PPO 变体 | critic 初始化、GAE、价值误差与训练稳定性 |
| 原则驱动的无害性训练 | Constitutional AI 类流程 | 原则冲突、误拒绝、评判模型偏见、分布外攻击 |

不能仅按“少于 8 张 A100”或“偏好对少于 10K”直接决定算法。资源阈值依赖参数规模、序列长度、精度、并行和实现；原稿未给这些前提，已撤下相应硬性门槛。对闭源模型后训练过程，也只应引用技术报告明确披露的内容，不能从产品表现猜测 PPO、DPO 或 PRM 配方。

本轮偏向公开可读的经典与代表性论文，尚未做全面安全攻击文献检索、最新方法筛选及独立复现。KTO、ORPO、PRIME 等有待补相应原文精读；原稿未能定位原文的 SafeDPO、Cat-DPO、OPAD、AM3Safety、iStar、R2M、Amulet、SaFeR-Steer 不再用占位 arXiv 链接承担结论。名称是否真实及方法细节仍待逐一检索，不能用猜测 ID 补齐。

## 9. 来源索引

- **A1**：Ouyang et al. [Training language models to follow instructions with human feedback, v1](https://arxiv.org/abs/2203.02155v1)。
- **A2**：Rafailov et al. [Direct Preference Optimization: Your Language Model is Secretly a Reward Model, v2](https://arxiv.org/html/2305.18290v2)。
- **A3**：Azar et al. [A General Theoretical Paradigm to Understand Learning from Human Preferences, v2](https://arxiv.org/html/2310.12036v2)。
- **A4**：Shao et al. [DeepSeekMath, v3](https://arxiv.org/html/2402.03300v3)。
- **A5**：Yu et al. [DAPO: An Open-Source LLM Reinforcement Learning System at Scale, v1](https://arxiv.org/html/2503.14476v1)。
- **A6**：[VAPO: Efficient and Reliable Reinforcement Learning for Advanced Reasoning Tasks, v1](https://arxiv.org/html/2504.05118v1)。
- **A7**：Bai et al. [Constitutional AI: Harmlessness from AI Feedback, v1](https://arxiv.org/html/2212.08073v1)。

## 10. 修订证据

2026-10-22 按 `researcher` 的结构化阅读和报告生成规范重新核对；`paper-fetcher` 批量取回 DAPO、VAPO、IPO 的元数据与引用，然后按上述固定版本读正文和结果表。所取 HTML 与提取文本放在仓库外 `.paper-cache/research-audit-2026-10-22/`，URL 和 SHA-256 见同目录 `manifest.json`。本轮修正方法与实验归属，没有运行训练，也未将链接可达或字符串命中视作“全篇已验证”。
