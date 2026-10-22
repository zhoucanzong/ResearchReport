# MaterialsDiscovery candidate selection

筛选截止：2026-10-23。PaperFetcher 搜索了 `generative materials discovery inverse design experimental validation closed-loop autonomous laboratory`（arXiv 正常返回；Semantic Scholar 限流 429）。此条目只选能支撑“候选如何生成—怎样验证—证据边界在哪里”的少量一手研究；不把候选清单写成全领域综述。

| Candidate | Decision | Reason |
| :-- | :-- | :-- |
| [MatterGen, arXiv:2312.03687v2 / Nature 2025](https://doi.org/10.1038/s41586-025-08628-5) | **入选，主精读** | 有联合晶体扩散、性质条件化、DFT/hull/phonon 过滤以及一例实际合成，可贯穿计算到实验；并存在 2026 年对实验相新颖性的公开争议，适合讲清证据层级。 |
| [MnFeCo₄Si₂ GNoME experimental follow-up, arXiv:2603.22748v1](https://doi.org/10.1016/j.jmmm.2026.174056) | **入选，短精读** | 2026 年的独立实验跟进，报告晶体结构、元素成分和磁性实测；补充一例“数据库候选到真实样品”证据，但不把单个样品当总体命中率。 |
| [A-Lab, Nature 2023 + 2026 correction](https://doi.org/10.1038/s41586-023-06734-w) | **仅作交叉引用** | 其稳定性候选筛选与实验反馈和生成式模型互补，但 AI4Science 已有独立 AutonomousLabs 专题；这里仅澄清它不是 MatterGen 下游，避免重复完整评析。 |
| [MASTER, arXiv:2512.13930v1](https://arxiv.org/abs/2512.13930) | 暂缓 | 多智能体在电子结构模拟中主动选择 DFT 任务，提供有趣的模拟闭环；本轮已有 A-Lab 专题覆盖物理闭环，而 MASTER 当前摘要主张是仿真效率/推理，不是新材料实验确认。 |
| [ElementBERT, arXiv:2502.14912v2](https://arxiv.org/abs/2502.14912) | 暂缓 | 合金元素语义嵌入及多项预测/优化有代表性，但会扩展到独立的合金性质建模问题，无法补足本条“结构生成—弛豫—合成”的主证据链。 |
| [SyMDis, arXiv:2312.11487v1](https://arxiv.org/abs/2312.11487) | 暂缓 | 可解释符号规则做材料数据库优化，适合未来“可解释搜索”专题；不涉及晶体生成后经真实合成验证的连续证据链。 |
| [Artificial Intelligence and Generative Models for Materials Discovery — A Review, arXiv:2508.03278v1](https://arxiv.org/abs/2508.03278) | 不作为证据来源 | 综述可用作地图，但本条优先引用论文正文、期刊更正和原始实验数据；宽泛综述不替代具体机制/结果证据。 |

## 取舍原则

选入项优先满足至少一项：能读出明确的材料表示/筛选机制；包含真正的合成、表征或性质量测；或能揭示“预测正确”与“新颖/可合成”之间的误差来源。暂缓项不是否定其质量，只是与本轮学习目标和范围不匹配。
