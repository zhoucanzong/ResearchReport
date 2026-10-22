# 精读：SyntheMol 如何把合成路线写进小分子生成

## 固定原文

[Swanson et al., “Generative AI for designing and validating easily synthesizable and structurally novel antibiotics”](https://doi.org/10.1038/s42256-024-00809-7)，Nature Machine Intelligence 6, 338–353 (2024)，published 2024-03-22。精读使用作者托管的出版版 PDF：[原文 PDF](https://www.newswise.com/pdf_docs/171095018136969_42256_2024_809_final.pdf)。核心锚点：Fig. 2–5、Extended Data Figs. 1–10、Methods “SyntheMol MCTS algorithm” / “Antibacterial potency analyses”。

## 亮点与差异

- **贡献**：SyntheMol 在化学反应与购买可得 building blocks 所定义的子空间内，以 MCTS 搜索预测有抗菌活性的结构，同时输出明确的合成反应路线。
- **新颖差异**：相较只对已有库分子逐个打分的虚拟筛选，模型搜索组合空间；相较用合成性打分奖励“可能容易做”的生成器，这里的 reaction template 直接构造每个候选。对 *A. baumannii* 的体外活性高度依赖外膜通透化剂。
- **证据强度**：三个生长抑制预测器、20,000 rollouts、三个模型生成路线；从 150 个 post-hoc shortlist 选 70 个供应商可得分子，58 个成功合成；六个候选满足特定联用 MIC 阈值。没有动物实验。
- **引用价值**：适合引用为“将反应和 building blocks 作为生成约束，再验证一批候选可否合成与抑菌”；不可引用成六个单药可独立治疗 *A. baumannii*。

## 问题与方法

作者的训练集由三个小分子库组成，对 *A. baumannii* ATCC 17978 在 `50 μM` 下测 OD600、生物学重复两次、培养 16 h。合并去重且去除活性标签冲突后得到 13,524 个独特分子：470 active、13,054 inactive；active 阈值是各库归一化 OD600 的 `μ−2σ`。三个分类器分别为 Chemprop、加 200 个 RDKit 描述符的 Chemprop-RDKit，以及以相同 RDKit 特征为输入的 100-tree random forest。十折交叉验证的 ROC-AUC 分别约 `0.803 / 0.827 / 0.835`，PR-AUC 为 `0.354 / 0.388 / 0.401`；由于 active 仅约 3.5%，PR-AUC 较 ROC-AUC 更能体现不平衡分类的困难。[PDF pp. 2–3, Fig. 2]

SyntheMol 在 Enamine REAL 的 132,479 个去盐、去重 building blocks 和 13 个反应模板中做 MCTS，每个产物由两个或三个 building blocks 经一次反应构成。候选被 property predictor 评分后，结果沿 MCTS 路径回传；`20,000` 次 rollouts 后输出分子与路线。选择流程再按 Tversky 与 470 个训练 hits / 1,005 个 ChEMBL 抗菌分子比较以排除高相似候选；保留模型分数前 20%，并用 `k=50` 的 Tanimoto k-means 选各簇最高分分子。该 13 反应子空间约 29.6 billion 个结构。[PDF pp. 3–4, Fig. 3–4、Methods]

## 候选到实验：各阶段的实际分母

Chemprop 版本做 20,000 rollouts，在约 8.5 h 内评价 452 million 个中间节点，生成 24,335 个完整候选；2,868 个抗菌分数 ≥0.5。相同约 8 h 内，Chemprop virtual screening 对 10 million 个随机 REAL 分子打分，374 个分数 ≥0.5。这是**预测候选的计算数量对照**，不是体外活性命中率对照。[PDF p. 4, Fig. 4f]

三个预测器版本各自选 50 个 post-hoc shortlist，共 150 个；其中仅 70 个在 Enamine REAL 中可购买/下单，成功合成 58 个，纯度 >90%，约四周获得。58 个的 MIC 检测对象是 *A. baumannii* ATCC 17978（训练使用同一菌株）。野生型外膜构成测定瓶颈：六个分子（Enamine 10、23、28、31、40、43）达到 MIC ≤8 μg/mL 的条件是加 `1/4 MIC` 的 SPR741 或 colistin；未加通透化剂时不能将六个都报作具有该 potency。对 LPS 缺失 *A. baumannii* ATCC 19606R，六个分子 MIC ≤4 μg/mL；对无外膜的 MRSA USA300，MIC 范围 `1–64 μg/mL`。`58` 个随机 REAL 分子对 WT 菌株单独或加 1/4 MIC SPR741 均无 hit；加 1/4 MIC colistin 时 3 个满足阈值。[PDF pp. 6–7, Fig. 5、Extended Data Fig. 9]

## 七问证据核验

| 判据 | 原文证据和能支持的结论 |
| :-- | :-- |
| 解决什么问题 | 生成模型往往输出难以合成的结构；研究目标是让分子生成时就受可采购 building blocks 和已验证反应约束，同时优化 *A. baumannii* 活性。Abstract、Introduction、Fig. 1。 |
| 核心方法 | Chemprop/Chemprop-RDKit/RF 为 property predictor；MCTS 平衡探索、利用和 building-block 多样性，20,000 rollouts，`nreaction=1`；每个分子输出真实可采购 building-block 组合和反应。Fig. 3、Methods。 |
| 数据与规模 | 13,524 体外测试分子、470 active；子空间 132,479 blocks + 13 reactions ≈29.6 billion；输出 24,335 complete molecules，post-hoc 150 shortlist。Fig. 2–4、Methods。 |
| 带条件结果 | 70 个真实可得候选中 58 个合成成功；`6/58` 命中只在 `1/4 MIC` SPR741/colistin 联用条件下对 WT *A. baumannii* 过 MIC≤8；LPS 缺失株和 MRSA 的独立 MIC 结果另列。Fig. 5a–c、Extended Data Fig. 9。 |
| 消融/对照 | 三种 predictor 单独生成的 sets；MCTS cLogP 任务用 random REAL 做算法筛选对照；随机 58 个 REAL 作体外比较；Extended Data Fig. 4 比较 diversity score penalty on/off。不同实验不能合并为单个统一 hit-rate 估计。Figs. 2、4–5、ED Figs. 4、9。 |
| 失效边界 | *A. baumannii* 外膜限制野生型单药进入，六个 nominated hits 的主要阈值依赖 potentiator；limited single-reaction subspace 与 post-hoc novelty/availability filtering 决定样本；无动物、PK/PD 或目标机制验证。Fig. 5、Discussion。 |
| 与同类系统差异 | 对照 abaucin 是从现有药物库筛选，SyntheMol 是 reaction-grounded MCTS de novo search；对照 2026 SyntheMol-RL，后者用学到的 value function 和双属性优化。论文未与 RL 在相同菌株、数据、合成预算下 head-to-head，因而无跨论文优劣结论。Fig. 3、Methods；与 SyntheMol-RL 研究对象不同。 |

**当前证据未覆盖**：未报告动物感染模型；无单药针对 WT *A. baumannii* 的六个 hit；没有 target-level mechanism；没有独立实验室复现。原文的体外结果说明方法能提名可合成、在具体 assay 条件下活跃的化学候选，不说明药物开发成功。
