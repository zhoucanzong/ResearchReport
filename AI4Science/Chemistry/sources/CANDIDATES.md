# Chemistry 候选筛选

核查日期：2026-10-23。以下是定向候选池，目的是选出一个窄而可核验的研究问题，不表示穷尽化学 AI 文献。**入选 3 项作为主线与边界锚点；其中 1 项为主线精读，2 项用于比较。**其余仅留筛选理由，不把摘要级候选写成已精读证据。

## 入选

| 文献 | 选择理由 | 用途 |
| :-- | :-- | :-- |
| Taylor et al. 2023, DOI `10.1021/acscentsci.3c00050` | 同一篇同时提供文献 surrogate 上的反复 benchmark、负迁移案例及新底物上的前瞻性流动化学实验；原文与补充数据入口公开，能逐层区分计算结果和实测化学结果 | 主线；精读 Fig. 1–6、Schemes 1–6、Table 1、Methods 与 SI 入口 |
| Shields et al. 2021, DOI `10.1038/s41586-021-03213-y` | 早期代表性化学 BO 工作；同时含实验数据 benchmark、人类决策比较和真实 reaction campaign，适合定位 MTBO 的技术增量 | 单任务 BO 前史对照；图表和摘要核验 |
| Garrido-Torres et al. 2022, DOI `10.1021/acscentsci.2c00207` | 明确显示 CASP 给出路线建议后仍要经过化学家筛选和反应开发，适合作为 retrosynthesis 与实验验证的边界案例 | 边界对照；摘要、Scheme 1、Figs. 3–5 核验 |

## 排除或暂缓

| 候选 | 处理理由 |
| :-- | :-- |
| Ahneman et al., “Predicting reaction performance in C–N cross-coupling using machine learning,” DOI `10.1126/science.aar5169` | 重要的高通量反应产率预测 benchmark，但本文聚焦条件优化中的跨任务数据迁移及新实验反馈；未把回顾性模型性能当成前瞻性条件推荐。若后续扩展“反应结果预测”专题再精读。 |
| Angello et al., “Closed-Loop Optimization of General Reaction Conditions for Heteroaryl Suzuki-Miyaura Coupling,” DOI `10.1126/science.adc8743` | 更关注跨底物一般条件的闭环筛选，和本文的 task-specific transfer 主问题相邻但不同；本文以 Taylor 2023 的 benchmark/实验分层更完整为取舍依据，未将其泛化结论并入主报告。 |
| Granda et al., “A robotic platform for flow synthesis of organic compounds informed by AI planning,” DOI `10.1126/science.aax1566` | 中心问题是 AI 合成规划与可重构流动平台的结合，和本库自主实验室报告及 retrosynthesis 范围重叠；不作为反应条件迁移主线证据。 |
| 2026 ChemRxiv, “Reaction-Level Machine Learning for Condition Optimization in Suzuki–Miyaura Cross-Coupling,” DOI `10.26434/chemrxiv.15010362/v1` | 当前检索命中的新预印本；处于预印本状态，且本轮未获取并精读正文，暂不把摘要或新近发表日期作为纳入理由。 |
| Manne & Yang, “Accelerated Chemical Reaction Optimization Using Multi-Task Learning”前期 ChemRxiv 版本，DOI `10.26434/chemrxiv.13250216.v2` | 与 Taylor 2023 期刊版本属于同一研究线的早期版本，不重复作为独立论文或额外验证证据。 |
| AutonomousLabs 中的 A mobile robotic chemist、A-Lab 等 | 研究目标分别为配方搜索或无机材料合成；设备闭环可作背景，但科学对象与反应条件迁移不同。本文不重复其平台能力论述。 |

## 范围边界

- **Retrosynthesis benchmark**：评估模型是否提出参考数据库/文献中可接受的拆解路线；不等价于实际合成成功。
- **Reaction-condition benchmark**：在历史数据或拟合代理函数上评价条件排序/优化算法；没有新实验时只能称回顾性或仿真基准。
- **前瞻性实验验证**：模型推荐条件实际进入新反应、产物经分析并形成模型反馈；需报告底物、实验数、测量协议和失败。
- **化学发现**：还需证明化合物、反应或功能层面的新颖性与重要性；优化出高产中间体不足以支持药物发现或新反应机理主张。
