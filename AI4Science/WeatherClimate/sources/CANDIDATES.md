# WeatherClimate selection record

筛选截止：2026-10-23。选题目标是用少数原始研究教会读者天气预报、概率不确定性、气候模拟与系统评测之间的区别；不追求覆盖所有天气模型，也不按模型名堆目录。

## 本轮精读

| Paper | Decision | Why it is in this batch |
| :-- | :-- | :-- |
| [GraphCast](https://arxiv.org/abs/2212.12794v2) | 深读 | 确定性、再分析驱动、全球中期预报范式；含足够细的验证协议和限制分析。 |
| [GenCast](https://arxiv.org/abs/2312.15796v2) | 深读 | 在同一全球天气任务上把研究问题转为轨迹概率分布、校准与极端事件概率。 |
| [NeuralGCM](https://arxiv.org/abs/2311.07222v3) | 深读 | 连接数据驱动天气预测与可长期积分的混合大气模型，报告多初值稳定率和强迫外推失败。 |
| [Aurora](https://doi.org/10.1038/s41586-025-09005-y) | 深读 | 代表异质地球系统预训练和多任务微调，且各任务使用不同的真实领域基线。 |
| [Advancing subseasonal forecasting with machine learning](https://doi.org/10.1038/s41586-026-11126-x) | 深读 | 2026-10-14 发表；显示 3–4 周预测可以通过概率后处理提升，避免把研究等同于继续扩大家气象网络。 |

## 作为前史或边界证据引用

| Paper | Treatment | Why not a separate dossier here |
| :-- | :-- | :-- |
| [Pangu-Weather](https://arxiv.org/abs/2211.02556v1) | 来源清单列为前史；正文一处简述其 3D Earth-Specific Transformer 与时间层级聚合 | 与 GraphCast 在研究问题和时代位置有较大重叠；扩展为并列精读会挤占概率、气候和近期进展的篇幅。 |
| [AIFS Single 1.1.0 update](https://doi.org/10.5194/gmd-19-4703-2026) | 来源清单列为操作化上下文 | 论文发布时讨论的是 1.1.0；ECMWF 官方数据页已列出后续 v2。留作版本演进证据，不把 1.1.0 指标标成当前模型结果。 |
| [Numerical models outperform AI weather forecasts of record-breaking extremes](https://arxiv.org/abs/2508.15724v1) | 正文列为分布外极端天气的反例 | 该来源目前按 arXiv 预印本标注，只支撑边界讨论；不做独立模型排行。 |

## 暂缓但值得下一轮阅读

| Candidate | Primary anchor | Reason to defer |
| :-- | :-- | :-- |
| ACE2：跨季节至十年大气变率及强迫响应 | [npj Climate and Atmospheric Science (2025)](https://doi.org/10.1038/s41612-025-01090-0) | 与 NeuralGCM 同属长时间尺度气候模拟，但对 CO₂ 与 SST 分离响应有独特诊断；可作为气候强迫专项的中心论文，避免本轮重复讲边界条件模型。 |
| AIFS-SUBS：数据驱动次季节预报 | [arXiv 2607.05100](https://arxiv.org/abs/2607.05100) | PBC 论文评估中引用的底层系统之一；本轮重心是校正层。下一轮应读其训练数据、lead-time rollout、目标变量和 2025 实时比赛协议，再和 PBC 分开评价。 |
| FourCastNet / FuXi / FengWu 等确定性全球模型 | [FourCastNet, arXiv 2202.11214](https://arxiv.org/abs/2202.11214); [FuXi](https://doi.org/10.1038/s41612-023-00512-1) | 很重要的模型谱系和结构差异；可按谱系比较网格、Transformer/算子、预报时效与误差增长，而非在本轮加成同质模型名单。 |

## AI 材料发现方向的来源纠错备忘

下一轮若将材料发现与自动合成设为并行专题，不要把 arXiv `2309.00544` 当作 A-Lab 质疑论文：官方记录题为 *Modular, Multi-Robot Integration of Laboratories: An Autonomous Solid-State Workflow for Powder X-Ray Diffraction*，内容是机器人实验室工作流。A-Lab 争议相关的来源应从下列原始/正式记录开始：

- 原 A-Lab 论文：[Nature 2023](https://doi.org/10.1038/s41586-023-06734-w)。
- 作者正式勘误：[Nature Author Correction, DOI 10.1038/s41586-025-09992-y](https://www.nature.com/articles/s41586-025-09992-y)，2026-01-19。勘误澄清 novelty 原意，并报告 40 个宣称成功的样本中人工重分析确认 36 个、4 个在 XRD 证据下不确定；更新后的论文不再把材料称为“novel”。
- 独立领域批评：[Challenges in High-Throughput Inorganic Materials Prediction and Autonomous Synthesis](https://doi.org/10.1103/PRXEnergy.3.011002)；需要与作者后续更正并读，不能只选一方叙述。
- 生成材料候选可读 [GNoME](https://doi.org/10.1038/s41586-023-06735-9) 和 [MatterGen](https://doi.org/10.1038/s41586-025-08628-5)；另有 2026 年对 MatterGen 训练集记忆/无序相识别提出具体测试的 [Juelsholt, Materials Horizons](https://doi.org/10.1039/D6MH00268D)。

## 其他可独立成波的方向

- **材料逆向设计到实验证据**：GNoME → MatterGen → A-Lab，主题是稳定性筛选、目标性质条件生成、可合成性和结构表征之间的断点。
- **化学实验 Agent 与自驱实验室**：从 [Coscientist, Nature 2023](https://doi.org/10.1038/s41586-023-06792-0) 和 [end-to-end chemical synthesis development platform, Nature Communications 2024](https://doi.org/10.1038/s41467-024-54457-x) 出发，评估语言模型规划、仪器 API、闭环优化和人类监督；这与蛋白 binder 计算设计的证据链不同。
