# 精读：两条生成路线怎样走到 NG1 与 DN1

## 固定原文与范围

[Krishnan et al., “A generative deep learning approach to de novo antibiotic design”](https://doi.org/10.1016/j.cell.2025.07.033)，Cell 188(21), 5962–5979.e22 (2025)，Epub 2025-08-14。优先阅读 [PubMed/PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12790861/) 的 Figs. 1–3、5–7、Data S1–S2；author's final manuscript 在 [MIT DSpace](https://dspace.mit.edu/entities/publication/2520b244-129a-4cc9-9bb6-49bfa0f21c93)，CC BY-NC-SA 4.0。论文期刊版不是该开放许可版本。

## 亮点与差异

- **贡献**：把物种表型预测、片段筛选、片段扩展和不依赖片段的从头生成接到合成与动物模型，获得 NG1、DN1 两种作用机制不同的 lead。
- **新颖差异**：相较 abaucin 的已存在分子库重定位、SyntheMol 的固定反应/building-block MCTS，这里并行考察 F-CReM/F-VAE 片段扩展与 JT-VAE 从头生成；论文并没有在同一数据/预算下与 SyntheMol 做 head-to-head。
- **证据强度**：训练用数万条已有实验表型；24 个合成/测试分子中 7 个在体外显示选择性活性，两个 lead 各有机制实验和局部感染小鼠结果；没有临床数据。
- **引用价值**：适合引用为“生成模型在实际合成约束下发现小分子并完成早期感染模型验证”的案例；命中率只适用于各自经过筛选与供应商审查的待测分子集。

## 路线 A：从菌种表型数据筛片段，再扩展化学结构

论文先对超过 45 million 的化学片段打分，目标分别是 *Neisseria gonorrhoeae* 和 *S. aureus* 的生长抑制预测。针对片段 F1，使用遗传算法式 F-CReM 和 F-VAE 扩展分子。作者挑出 80 个兼顾预测分数、结构差异和可合成性的分子；27 个进入供应商合成尝试，最后成功合成 NG1 与 NG2，只有 NG1 在 *N. gonorrhoeae* ATCC 49226 上有效（MIC 0.5 μg/mL，Fig. 2G）。因此不能把“80 个排序候选”“27 个下单/尝试合成”和“2 个成功合成”混为同一个分母。

NG1 在体外的 MBC 为 1 μg/mL；作者报告对耐药分离株仍有活性，并在小鼠阴道感染模型中测试。Fig. 3J–K：菌株 ATCC 49226；vehicle `n=8`、NG1 `n=9`、ceftriaxone `n=5`；感染后 2 h 开始局部给药，24 h 内共五次。NG1 相比 vehicle 的 vaginal bacterial load 约下降 3 log，Mann–Whitney 检验 `p=0.0120`。结果是短期、局部动物模型，不能推成系统治疗或人体疗效。

机制方面，NG1 对 *N. gonorrhoeae* 造成膜 rigidification/permeabilization；PISA 在处理后的裂解液中发现 LptA 热稳定性变化，RNA-seq 又观察到 `lptA` 上调和 LOS 通路变化，联合 polymyxin B 有协同。论文将证据归纳为 LptA 很可能是主要靶点，但并没有提供配体-蛋白复合物结构或纯化蛋白结合常数。更准确的说法是多条证据**指向** LptA，而非直接证明特定原子结合姿态。

## 路线 B：无片段起点的从头 JT-VAE 生成

CReM 与 junction-tree VAE 共生成约 29,014,974 个分子。去重、属性过滤和人工结构/合成审查后，90 个候选交由供应商审查，22 个实际采购并测试。6 个分子对 *S. aureus* 有活性（Fig. 5F–G），作者称为 working true discovery rate `6/22 = 27.3%`；这一定义只适用于该经过筛选与供应商采购的测试集，不是模型对其全部 2,900 万候选的实验成功率。

DN1 对 MSSA RN4220 与 MRSA BAA1556 MIC 均为 4 μg/mL，三种人细胞测得的 therapeutic index 为 32（Fig. 6A）。膜电位、Laurdan 与 cryo-TEM 结果支持膜活性机制。MRSA BAA1556 中性粒细胞减少皮肤伤口模型中，vehicle、DN1、fusidic acid 各 `n=6`；约 `10^5 CFU` 接种后，以 `1% w/v` 外用制剂分六次给药，感染后 25 h 测 wound CFU；DN1 相对 vehicle 约下降 10 倍（Fig. 7E–F，`p=0.0043`）。

## 学习要点

- 生成模型帮助探索候选，但合成成功率由化学可达性决定；生成、筛选、供应商接受和实际成品是不同阶段。
- 片段路线与无片段 JT-VAE 路线采用不同训练/过滤/实验流程，不能用单一 hit rate 对比。
- 两条路线的 lead 针对不同菌种和局部感染；模型命中与动物效果仍是临床前信号，不代表可治疗患者。
- 论文列有与 Phare Bio、Integrated Biosciences、Enamine/Chemspace 等相关的利益声明；引述转化判断时应一并参照。代码与数据集未在本条目中独立复现。

## 七问证据核验

| 判据 | 原文证据和可支持的结论 |
| :-- | :-- |
| 解决什么问题 | 提高具有结构新颖性的小分子抗生素发现率，并避免模型只对已有库分子打分；针对 *N. gonorrhoeae* 与 *S. aureus* 分别建立路线。Abstract、Introduction、Fig. 1。 |
| 核心方法 | 两组物种特异 Chemprop D-MPNN ensembles（每组 20 模型）；片段路线为 GNN scoring + F-CReM genetic search/F-VAE 扩展；无片段路线为 CReM/JT-VAE。Methods “Machine learning models”, “De novo design”。 |
| 数据与规模 | 训练：*N. gonorrhoeae* 38,765、*S. aureus* 39,312 compounds（Data S1）；片段筛选 >45 million；从头生成约 29,014,974；总计 24 个成功合成并测试。Fig. 1、5、Methods。 |
| 带条件结果 | NG1 MIC `0.5 μg/mL`、MBC `1 μg/mL`，小鼠 ATCC 49226 vaginal model  vehicle `n=8`/NG1 `n=9`/ceftriaxone `n=5`、五次局部剂量，vehicle 比较约下降 3 log、`p=0.0120`。DN1 对 RN4220/BAA1556 MIC 4 μg/mL；BAA1556 皮肤模型各 `n=6`，1% topical 六次，25 h endpoint，约 10 倍 vehicle 差异、`p=0.0043`。Figs. 2G、3J–K、7E–F。 |
| 消融或对照 | 两条任务路径内部比较 F-CReM/F-VAE 与 CReM/JT-VAE；DN1 的 time-kill 对 vancomycin、动物阳性对照 fusidic acid、vehicle、以及 MIC/CC50 和膜实验对照提供实验参照。论文未报告一项把整个模型与 SyntheMol 在相同 assay、菌种及合成预算下比较的控制实验。Figs. 2–7。 |
| 失效边界 | 片段路线 27 次启动合成只得到 NG1/NG2 两个化合物，NG2 不活跃；CReM 部分候选合成性差，JT-VAE shortlist 经人工与供应商再筛。DN1/NG1 的谱系、局部给药和单一短期小鼠模型不能外推为广谱/系统/人体疗效。Figs. 2、5–7，Methods。 |
| 与同类系统可判定差异 | 本文生成候选并做了双 lead 的机制和动物验证；和 SyntheMol 的单一 MCTS over Enamine space 不同，且把 fragment-guided 与 no-fragment JT-VAE 路线分别实验。与 abaucin 的已有化合物排序也不同。数据/任务不同，不能直接比较命中率。Figs. 1–7。 |

其中方法和数据规模已回查论文 Methods；体外与机制锚点见 PubMed/PMC Fig. captions；小鼠组数、检测、剂量和统计量见 Fig. 3J–K、Fig. 7E–F。`29,014,974`、F-CReM/F-VAE 路线细节来自原文正文/Data S2，不由 PubMed 摘要单独支持。模型未重跑，合成和动物实验未复现。
