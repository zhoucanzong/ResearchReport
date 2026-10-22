# 精读：SyntheMol-RL 的学习式合成空间搜索与实测分母

## 固定原文

[Swanson et al., “SyntheMol-RL: a flexible reinforcement learning framework for designing easily synthesizable antibiotics”](https://doi.org/10.1038/s44320-026-00206-9)，Molecular Systems Biology 22(6), 833–867 (2026)，version of record 2026-04-23；全文开放，CC BY 4.0。[官方 PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC13230741/)。主要位置：Figs. 1–5、Table 1、Methods、Appendix、Dataset EV1–EV12。

## 亮点与差异

- **贡献**：将原 SyntheMol 的 MCTS building-block 选择替换为可学习 building-block/node value function，并把水溶性与抗菌活性作为双目标，前瞻合成出 synthecin 并测小鼠局部感染模型。
- **新颖差异**：与旧 MCTS 的单节点访问统计不同，RL value network 能在化学相似的 building-block combinations 间共享预测；相较普通 virtual screening，按组合空间路径生成，并可附反应路线。
- **证据强度**：10,658 个抗菌训练分子、两预测目标、约 46 billion 可构造空间、MCTS/虚拟筛选/随机对照；79 个 RL 生成分子合成测试且有按条件定义的 MIC hits，另有一个小型 topical mouse model。尚无药代/临床/作用机制验证。
- **引用价值**：适合引用为“多目标奖励、合成约束与 RL 生成怎样连接到实验”；11/38 与 2/41 不可脱离 MIC cutoff、novelty review 和 strain 来复用。

## 它改了什么

SyntheMol 原版用 MCTS 选择 building blocks 和反应；SyntheMol-RL 用深度网络 value function 学习部分 building-block 组合将生成何种分子分数。作者同时设定两个预测属性：*S. aureus* 抑制活性和水溶性，后者针对早先模型候选溶解度不足这一实验障碍。组合空间是 Enamine REAL（使用 13 个反应，约 30 billion molecules）与 WuXi GalaXi（约 16 billion），总计约 46 billion 化学组合空间（Fig. 2E）。这个数字描述由指定 building blocks/reactions 构造的虚拟空间，并不表示逐一枚举或实验覆盖。

抗菌训练集不是公开大型药物数据库直接代替实测：团队把 10,716 个 Bioactives 2 compounds 以 50 μM 对 *S. aureus* RN4220 做两次生物重复的生长抑制 assay，终点 16 h。去重后 10,658 个化合物，1,137 个按作者阈值标为 active。分割用 10-fold cross-validation，包含 80/10/10 train/validation/test；Chemprop-RDKit 与 MLP-RDKit 的 test/validation performance 见 Table 1。该训练表型的覆盖与 assay 条件决定预测器的适用范围。

## 从候选到实验：不要删掉分母

| 阶段 | 原文数量/条件 | 应如何解释 |
| :-- | :-- | :-- |
| 生成 | RL-Chemprop 10,000 rollouts → 10,983 分子；RL-MLP → 9,228；MCTS → 11,630；虚拟筛选评估 21,000,000 个随机分子 | 比较的是搜索策略、属性预测和筛选设定，不是相同生成空间的完整穷举 |
| 可得与筛选 | 各策略 top-150 共 750 个候选先查询供应商可得性（747 个独特分子）；再从五种策略各选 50 个并按预测毒性筛出 250 个送合成；最终获得 196 个独特分子用于体外实验 | 生成数、top-150、供应商可得、提交合成、成功合成、实验测试是不同分母 |
| 主要 hit 定义 | *S. aureus* RN4220 MIC ≤8 μg/mL；RL-Chemprop `11/38`，RL-MLP `2/41`；MCTS 0 hit、VS-Chemprop 2 hit、随机 44 个 0 hit | 数字是指定模型组、成功合成并测试后的实验命中数；阈值是论文作为优化起点选用的 MIC，不是临床断点 |
| 新颖性人工复核 | 13 个抗菌 hit 中，人工 novelty review 后保留 RL-Chemprop 6 个、RL-MLP 1 个；作者指出若干结构含有或与已知 salicylanilide 类有重叠 | 机器筛分与人工结构审查共同决定下游研究对象；不应把所有“active”都叫新化学类 |

作者用 Cream Release Evaluation on Agar Media (C.R.E.A.M.) 比较候选的外用制剂表现，选择 MLP-01 / synthecin 进入动物试验。鼠伤口感染模型使用 MRSA USA300，vehicle 和 synthecin 组各 `n=5`，感染约 `2.15 × 10^7 CFU`，用 `2% w/v` synthecin/Glaxal Base 在 1、4、8、12、20 hpi 给药，24 hpi 取组织。vehicle 平均量约 `6.39 × 10^9 CFU/g`，synthecin 约 `5.14 × 10^7 CFU/g`；动物试验是 topical, single-model, short-duration proof-of-concept，不是 systemic dosing、PK/PD 或临床安全性评估。

## 机制与风险

论文在体外观察 synthecin 对细菌生长的 bacteriostatic activity；作者明确说其机制研究仍在进行。不要把文章 title/外用疗效包装成 mechanism-resolved candidate。其它 hits 对 ESKAPE panel 多呈窄谱或无显著效力；模型训练靶菌是 *S. aureus* RN4220，挑战 strain USA300 的验证有意义，但仍不足以概括不同人群分离株的普遍性。作者通过比较 GFlowNet/REINVENT 与自身模型强调合成可行性，不过具体成本、时间及模型来源空间差异是其自己定义的比较；本笔记不把这些宣传性比较当成本报告结论。

本分册仅核对论文方法与报告结果；模型、合成和动物实验均未独立复现。

## 七问证据核验

| 判据 | 原文证据和可支持的结论 |
| :-- | :-- |
| 解决什么问题 | 原 SyntheMol 搜索节点不能有效共享相似 building blocks 的价值，且只优化单属性；本研究希望更有效搜索并同时改善抗菌分数/水溶性。Abstract、Introduction、Fig. 1。 |
| 核心方法 | 两个 predictor architectures (Chemprop-RDKit、MLP-RDKit) 作为 RL value model；两目标用动态权重，node value network 每 10 rollouts 更新 5 epochs，探索温度按目标结构相似度 `0.6` 调整；两空间用合成反应约束。Methods “Generative model development” / “Dynamic RL parameters”。 |
| 数据与规模 | Bioactives 2: 10,716 screened → 10,658 unique, 1,137 active; solubility target 从 AqSolDB 9,982 molecules；Enamine 30b + WuXi 16b；每个实验组 10,000 rollouts。Fig. 2、Methods。 |
| 带条件结果 | RN4220 `MIC ≤8 μg/mL`：RL-Chemprop `11/38`、RL-MLP `2/41`；仅其中 7 hits 通过人工新颖性审查。Synthecin 是 RL-MLP 的 MLP-01，在 MRSA USA300 小鼠伤口模型 2% w/v topical 给药五次、vehicle/synthecin 各 `n=5`，24 hpi 计 CFU/g。Figs. 4–5。 |
| 消融或对照 | 同 10,000 rollouts 下的 RL-Chemprop、RL-MLP、原 MCTS、21m 虚拟筛选、随机 REAL/WuXi compounds；wet-lab groups MIC hit counts 分别 11/38、2/41、0/38、2/37、0/44。Appendix 另以 5 个 seeds 对 model architecture、fixed-vs-dynamic property weights、温度目标与 fixed temperature 做 ablations (Figs. EV2–EV3)；动态权重对预测双目标 hits 达最优或近优表现。Figs. 3–4、EV2–EV3。 |
| 失效边界 | 活性标签来自单一 lab strain + LB, 50 μM screening; 13 active hits 人工新颖性审查后只剩 7；后续谱系测试主要窄谱 *S. aureus*；synthecin 的机制作者未确立，鼠模型是高浓度局部外用短期实验。Figs. 2、4–5、Discussion。 |
| 与同类系统可判定差异 | 同一生成/预测实验中，RL 优于其 MCTS 与 VS baselines 的预测属性命中筛选；GFlowNet/REINVENT 4 比较是按 SAScore/分子量等过滤后的 in-silico comparison，因供应商可合成性较差未构成同分母 wet-lab 对照。Appendix Fig. EV7。相较 SyntheMol 2024，新增学习式节点价值、solubility 多目标和 MRSA topical mouse proof-of-concept；不能将不同研究的 `6/58` 与 `13/79` 直接比较。 |

原文也做了 ablation：动态权重对“同时通过预测活性与溶解度阈值”的筛选表现最优或近优；不同 value architecture 的权重/温度敏感程度不一致。它支持的是超参搜索机制的模拟输出，不是额外 wet-lab ablation 或动物疗效归因。该边界由 Fig. EV2–EV3 和 Appendix 的五种 seed 实验给出。
