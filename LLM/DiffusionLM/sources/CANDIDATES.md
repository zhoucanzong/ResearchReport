# 选文说明与候选池 · DiffusionLM

> 核查截止：2026-10-25。目标不是列举所有 diffusion LM，而是用少数论文解释训练目标、条件化结构、生成/编辑策略和成本证据怎样彼此影响。核心论文均须有固定版本和可回看的原文定位；产品卡或榜单只作检索线索。扩散与 AR 投机解码的交叉精读统一汇入 [SpeculativeDecoding](../../../Infra/SpeculativeDecoding/topics/diffusion-drafters.md)。

## 纳入主线

| 工作 | 决定 | 作用与边界 |
|---|---|---|
| [LLaDA: Large Language Diffusion Models](../papers/2502.09992-llada.md) | 精读 | 从随机遮盖的 masked discrete diffusion 训练出 8B 模型；建立与 AR 的首个大规模对照，但不推断普遍胜出或更快。 |
| [LLaDA 1.5 / VRPO](../papers/2505.19223-llada-1.5-vrpo.md) | 精读 | 处理 masked diffusion 的序列偏好概率估计与方差缩减；对照范围限于论文数据和训练预算。 |
| [LLaDA2.0](../papers/LLaDA2.0-Scaling-to-100B.md) | 精读 | AR-to-diffusion 转换与 16B/100B 扩展；训练总成本披露不足，作为规模路线而非成本优势证明。 |
| [LLaDA2.1](../papers/LLaDA2.1-Token-Editing.md) | 精读 | 研究生成后修改 token 与跨块修订；速度、质量、训练、RL 与部署系统共同变化。 |
| [LLaDA2.2 / Levenshtein Editing](../papers/LLaDA2.2-Levenshtein-Editing.md) | 官方 technical report 补充 | 在 2.1 的固定位置替换上增加插入/删除；同基座 SWE 微调消融直接相关，但无 arXiv 版本、无 PDF 许可声明，且整体模型比较有 scaffold 与服务条件限制。 |
| [Block Diffusion](../papers/2503.09573-block-diffusion.md) | 精读 | 说明块间因果生成、块内并行去噪如何连接可变长度与 KV cache；保留小模型与 AR 的质量边界。 |
| [SDAR](../papers/2510.06303-sdar.md) | 精读 | AR 转换为块扩散的另一规模案例；保留科学领域增益和一般任务混合结果。 |
| [CARD](../papers/2601.22031-card.md) | 精读 | 严格因果注意力中的尾窗扩散；揭示并行度、PPL 与吞吐之间的可测折衷。 |

## 暂缓或交叉引用

| 工作 | 决定 | 理由 |
|---|---|---|
| Dream 7B | 暂缓 | AR 初始化与 context-adaptive noise 对 masked DLM 有比较价值；先完成主线七篇并核对与 LLaDA 的独立增量，再决定是否追加。 |
| LangFlow | 暂缓 | 连续/flow-matching 分支与离散 masked diffusion 的目标不同；适合后续扩展，不为追求模型覆盖率而并入本轮。 |
| Nemotron-Labs-Diffusion | 交叉引用 | 联合训练 AR 与 diffusion 模式并研究 self-speculation，主要交叉点已属于 [投机解码](../../../Infra/SpeculativeDecoding/report.md)；只在新专题说明边界。 |
| SEDD、MDLM | 背景引用 | 用于理解 score-entropy 与 masked diffusion 的前史，不扩成历史综述。 |
| DFlash、DFlare、DDTree、DARTree、PRESTO | 交叉到投机解码专题 | 扩散模型为 AR target 提出并行 draft，target 决定最终接受序列；精读与设计关系见[扩散交叉分析](../../../Infra/SpeculativeDecoding/topics/diffusion-drafters.md)。 |
| Spiffy | 交叉到投机解码专题 | 在 standalone dLLM 上对未来去噪状态自投机；保持的是原 dLLM 分布，不是 AR 分布。 |
| PoE-Bridge | 交叉到投机解码专题 | DLM proposal + AR 目标的有限采样质量桥接；论文承认有限预算下不严格无损。 |
| DSpark、BASTION | 候选，未精读 | 仅留作后续筛选线索；不以题录或产品材料替代方法分析。 |
| “Top 10 Open Challenges for Diffusion LMs” | outlook only | 观点/议程类材料可帮助列未解问题，但不能替代算法机制或受控实验原文。 |

**统计口径**：当前 standalone diffusion LM 核心池 7 篇固定版本论文 + 1 份官方 technical report 补充。另有多篇 diffusion-to-AR 与 dLLM self-speculation 论文，已按专题边界移至 SpeculativeDecoding 的交叉阅读路线；两种模型角色不合并成同一条性能曲线。没有对未逐篇搜索的文献全集作穷尽性主张；候选筛选是面向学习的定向覆盖。
