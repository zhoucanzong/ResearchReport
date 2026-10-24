---
display_name: 扩散语言模型
type: topic-research
domain: LLM
subject: DiffusionLM
date: 2026-10-23
evidence: 精读原文
status: current
---

# 扩散语言模型：从随机遮盖到大规模并行生成

> 本专题研究把语言模型本身训练成扩散生成器的工作。核心问题不是“扩散是不是更快”，而是：训练目标、生成顺序与可修改状态怎样共同影响能力、长度控制、推理计算和编辑能力。所有分数与速度均为论文作者报告；本专题没有独立复现。版本和阅读范围见 [来源清单](sources/MANIFEST.md)。

## 先区分两种“diffusion”

“扩散语言模型”至少指两件不同的事：一种是模型自身通过去噪生成完整或局部文本；另一种是用扩散模型生成草稿，再交给自回归 target 验证，以加速 target。前者是本专题主体；后者属于[投机解码专题](../../Infra/SpeculativeDecoding/report.md)，例如 DARTree。两类方法的训练目标、输出保证与性能指标不能混在一起。

读一篇 diffusion LM 论文，可以先问四件事：

1. **噪声加在哪里？** 离散 token 被替换为 `[MASK]`，还是对连续表示/概率轨迹加噪？
2. **哪些位置互相可见？** 全序列双向去噪、块间自回归而块内扩散，还是保持严格因果注意力？
3. **已经生成的 token 能否改？** 单调地从 mask 填入 token，还是允许后续上下文回头修订？
4. **一次生成需要做多少次全量或块级前向？** 并行预测一批 token 不等于总计算或延迟更低；还要看去噪轮数、块数、批量、注意力实现、长度控制和吞吐测量边界。论文条件对照见 [LLaDA2.1](papers/LLaDA2.1-Token-Editing.md) 与 [CARD](papers/2601.22031-card.md)。

## 研究路线不是一条“更快”曲线

表内证据按固定论文逐篇定位；缓存、许可和各自未核实边界见 [MANIFEST](sources/MANIFEST.md)。

| 论文分册（固定来源：[MANIFEST](sources/MANIFEST.md)） | 机制位置 | 规模 / 可读证据 | 关键边界 |
|---|---|---|---|
| [LLaDA](papers/2502.09992-llada.md) | 随机比例 token mask + 双向 Transformer；多轮 mask-to-token 去噪 | 8B、2.3T 预训练 token；同量级自建 AR 与多个任务对照 | 多项任务与 AR 接近或不同方向，非普遍胜出；固定生成长度，无专用推理架构，也未证明比 KV-cache AR 更快 |
| [LLaDA 1.5 / VRPO](papers/2505.19223-llada-1.5-vrpo.md) | 用 ELBO 估计 masked diffusion 的序列概率，并用方差缩减做偏好优化 | 350K 偏好对、LLaDA-8B 单 epoch；Table 1–3 对照 SFT 与朴素 DPO | 比较支持该估计/优化方案在所测任务中的价值，不等于扩散偏好优化已普遍优于 AR 对齐 |
| [LLaDA 2.0](papers/LLaDA2.0-Scaling-to-100B.md) | 将自回归模型转换为扩散生成，并扩展到 16B/100B MoE | WSD 转换阶段与 1.5M DPO 对；给出大模型能力及 blockwise 服务结果 | 总 CPT token、训练步数和 GPU-hours 未完整披露；不能据参数规模 alone 推断训练效率或同预算能力 |
| [LLaDA 2.1](papers/LLaDA2.1-Token-Editing.md) | Mask-to-Token 之外增加 Token-to-Token 修订及跨块编辑 | 16B mini、100B flash；分别报告 Speed/Quality 模式、TPF、任务分数与 TPS | 速度、任务成绩、TPF 是不同指标；训练、RL、量化、内核与编辑策略同时变化，不能把 headline TPS 全归于 token editing |
| [LLaDA 2.2](papers/LLaDA2.2-Levenshtein-Editing.md) | 将固定位置的替换扩展到 keep / substitute / insert / delete，面向 agent draft 修订 | 官方 technical report；Figure 4 的同基座 SWE-bench Verified 微调消融为 35.8→44.4 | 没有 arXiv 版本或 PDF 许可声明；agent 汇总与吞吐对比为作者报告，评测 scaffold 存在差异 |
| [Block Diffusion](papers/2503.09573-block-diffusion.md) | 块间自回归、块内离散扩散 | 110M 控制实验揭示可变长度与 KV-cache 的结构折中 | 小模型实验不是 LLM 规模能力对照；2048 token PPL 与 AR 差距显著 |
| [SDAR](papers/2510.06303-sdar.md) | 由预训练 AR 继续训练为块扩散生成 | 30B science 模型的特定领域实验与 8B H200 吞吐分析 | 领域结果与预训练/推理 SFT 共同作用；吞吐受 batch 与块大小影响，通用推理结论混合 |
| [CARD](papers/2601.22031-card.md) | 保持严格因果注意力，对尾部窗口加噪并做置信度并行去噪 | 1B、300B FineWeb token；报 PPL、准确率及质量—吞吐曲线 | 仍落后其 AR 平均基线；更激进解码可提高吞吐但使 generation PPL 变差 |

## LLaDA：从左到右分解转向随机遮盖目标

自回归模型把序列概率写成逐 token 条件概率的乘积；LLaDA 则随机抽取遮盖率 `t∈(0,1]`，把序列 token 独立替换成 `[MASK]`，由双向 Transformer 同时预测所有被遮位置。训练损失只计遮盖位置，并以 `1/t` 加权；论文证明这一去噪目标是数据负对数似然的上界。[LLaDA §2.1–2.2、Appendix A.1](https://arxiv.org/html/2502.09992v3)

推理时模型从一段全 mask 的指定长度开始，反复预测所有未知位置，再按反向转移概率对一部分预测重新 mask。低置信度 remasking 在作者列出的设置中优于随机 remasking；这反映迭代顺序与错误修订策略很重要，不是训练目标的必然收益。用户必须预先给出回答长度，EOS 后内容再被裁掉；短答偏差与 EOS 处理因而是算法设计问题，不只是产品参数。[LLaDA §2.4、Appendix B.1、B.4、Table 9](papers/2502.09992-llada.md)

规模证据是可行性证据，不是“扩散胜过 AR”的证明。LLaDA 8B 使用 2.3T 预训练 token，论文报告与自建 LLaMA 3 8B 在 MMLU / GSM8K / HumanEval 上为 65.9 / 70.3 / 35.4 vs 65.4 / 48.7 / 34.8；但 BBH 为 49.7 vs 62.1。8B MDM 只训练一次且未调参，7B AR 基线并非完全同规模、同架构与同预算。阅读结果时应保留这个混合表，而不要抽出一项高分概括为整体能力优势。[Table 1、§3.1–3.2、Appendix B.2](papers/2502.09992-llada.md)

## 对齐：似然不可直接算，估计方差进入优化器（[LLaDA 1.5 分册](papers/2505.19223-llada-1.5-vrpo.md)）

自回归 DPO 可以直接算序列 log-probability；masked diffusion 的精确序列似然不可直接求，LLaDA 1.5 以 ELBO 的 Monte Carlo 估计替代。论文分析随机偏好分数经过 `log σ` 非线性后的估计误差，并用预算内增加 timestep 样本、policy/reference 共享样本等方法降低方差，提出 VRPO。[LLaDA 1.5 §2–4、Appendix B–D](https://arxiv.org/html/2505.19223v2)

该工作说明扩散对齐需要处理**目标估计的统计误差**，而不只是把 AR 的偏好算法名搬过来。它对 350K 内部偏好数据做单 epoch LLaDA-8B alignment；比较对象包含 SFT-only 与朴素 DPO。数字只支持该偏好集、训练预算和评测协议下的结果。它没有与强 AR 对齐模型在同一偏好数据、算力、评测脚本下完成全面对照，也没有独立复现。[Tables 1–3](papers/2505.19223-llada-1.5-vrpo.md)

## 扩展：规模、可修订状态与生成成本

LLaDA 2.0 把关注点从“能否训出 8B MDM”推进到**从 AR 基座转成 diffusion LM 时，转换训练和大规模推理怎样组织**。论文报告 16B/100B MoE 模型及 WSD 转换日程、DPO 阶段；但总继续预训练 token、优化步数和 GPU-hours 未完整披露，因此参数规模不能替代同算力预算对照。[LLaDA 2.0 §§3–7、Table 2、Figs. 1–6](papers/LLaDA2.0-Scaling-to-100B.md)

LLaDA 2.1 的 token editing 让模型不仅填 mask，也能撤回并替换已写 token；Multi-Block Editing (MBE) 允许后续上下文回看先前 block。S Mode 增加并行度，Q Mode 侧重质量：flash 平均任务分数/TPF 分别是 72.34/5.93 与 73.54/3.64；Table 3 的量化 HumanEval+ 吞吐为 891.74 TPS，但相对未量化项报告 −3.04 分。MBE 子集的平均分改善同时伴随 TPF 下降。由于训练目标、RL、量化和服务实现共同变化，这些证据不能把整体吞吐收益单因归给编辑机制。[Tables 1–4、Figs. 1–3、§6](papers/LLaDA2.1-Token-Editing.md)

LLaDA 2.2 在此基础上增加**局部长度变化**：以 draft/target 的最长公共子序列产生 keep、substitute、insert、delete 标签；插入将一个 token 扩成 `[MASK]` 与原 token，删除则移位后续 token，并在 block 内 padding 或截断恢复容量。官方技术报告在相同基座、相同 SWE trajectories 的微调比较中报告 SWE-bench Verified 从 35.8 到 44.4；这是直接支持“编辑动作对该训练设置有用”的证据，不是普遍 agent 能力提升的保证。该报告没有 arXiv 编号，官网标注 2026-07-01，而 commit-pinned PDF 元数据/上传时间为 2026-07-22；PDF 未声明许可。其 Ling 对比使用不同 SWE scaffold，吞吐缺少足够可移植的硬件与并发细节，不能将官网technical report等同经同行评审的 AR 基准排名。[PDF §§3–5、Fig. 4、Tables 1–3](papers/LLaDA2.2-Levenshtein-Editing.md)

跨论文看，扩散生成的工程问题至少有三层：固定长度与 EOS 规则决定输出长度能否自然停止；全局迭代去噪与分块生成决定前向次数和 KV 管理；已有 token 能否修订决定并行草稿错误是否可以回滚。若论文仅报告 tokens-per-forward (TPF)，还不足以知道墙钟吞吐；如果只报 TPS，则还要核对硬件、并发、prompt/output 长度、量化、内核和计时边界。完整 evidence matrix 与实验配置见各论文分册和 [MANIFEST](sources/MANIFEST.md)。

## 阅读路线与范围

建议按问题阅读：先读 [LLaDA](papers/2502.09992-llada.md)理解随机 mask objective 和固定长度反向采样；接着读 [LLaDA 1.5](papers/2505.19223-llada-1.5-vrpo.md)看扩散概率估计怎样影响 DPO；再读 [LLaDA 2.0](papers/LLaDA2.0-Scaling-to-100B.md)看模型转换与大规模训练；最后依次读 [LLaDA 2.1](papers/LLaDA2.1-Token-Editing.md)与 [LLaDA 2.2](papers/LLaDA2.2-Levenshtein-Editing.md)，比较替换修订与插入/删除编辑。Block Diffusion、SDAR 与 CARD 用来比较不同条件化和生成顺序，而不是扩充模型名录。

纳入边界：视觉生成 diffusion 不属于本专题；用 diffusion drafter 为自回归 target 加速的 DFlash / DARTree / BASTION 归[投机解码专题](../../Infra/SpeculativeDecoding/report.md)。若某论文只是在 related work 提及 LLaDA，或只给一个推理速度数字却不交代任务和评测条件，不作为主线证据。候选范围与暂缓理由见 [CANDIDATES](sources/CANDIDATES.md)。

## 尚未解决的问题

- 双向去噪、块级自回归和因果扩散模型在相同 token、算力、数据质量、模型规模下，能力与训练效率如何变化？
- 训练算力之外，怎样统一计入全序列迭代前向、KV cache、量化与并发服务成本，形成可复算的质量—延迟—吞吐曲线？
- 允许 token revision 后，错误修复与错误引入各有多常见；如何避免反复改写、长程事实漂移和结构性回归？
- 扩散模型的可变长度生成、EOS 学习、长上下文和工具调用稳定性，能否在同一开放评测协议里检验？这些边界在 [LLaDA](papers/2502.09992-llada.md) 与 [LLaDA2.2 技术报告](papers/LLaDA2.2-Levenshtein-Editing.md) 中已有局部证据，但尚非同协议对照。
- 大规模 LLaDA 转换结果中，哪些增益来自扩散目标，哪些来自新增数据、RL、采样器、服务内核与评测预算？

本专题精读范围、版本、许可、缓存路径、具体表图位置及未复现事项见 [来源清单](sources/MANIFEST.md)。
