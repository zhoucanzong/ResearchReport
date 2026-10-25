---
display_name: 抗生素发现
type: research
domain: AI4Science
subject: AntibioticDiscovery
date: 2026-10-23
evidence: fixed-primary-papers
status: completed
---

# AI 辅助小分子抗生素发现：从活性筛选到机制与动物模型

> **范围**：只讨论 AI 如何帮助发现或生成抗菌小分子，以及候选如何经化学合成、体外实验、机制实验和动物感染模型验证。不覆盖抗菌肽、蛋白 binder 设计、临床抗菌药选择，也不把 AI 预测本身视为发现成功。

## 核心判断

这条研究线的关键进展不是“模型能生成多少分子”，而是 AI 候选进入了可追踪的实验链：小分子表型筛选得到 abaucin；合成约束生成器 SyntheMol 把搜索限制在可执行的反应与 building blocks；后续生成模型将片段筛选、结构扩展和从头生成连接到合成、体外活性、作用机制及小鼠感染模型。各论文的菌种、训练数据、命中阈值和 assay 不同，不能把命中率或 MIC 合并排名。

证据层级必须拆开看：**模型给分 → 候选被选出 → 化合物被合成/采购 → 体外抑菌 → 作用机制证据 → 动物模型**。例如，SyntheMol 的六个 hit 对 *A. baumannii* 的 MIC ≤8 μg/mL 是在外膜通透化剂 SPR741 或 colistin 的 1/4 MIC 联用条件下得到；对 LPS 缺失株和 *S. aureus* 的后续实验则不需该联用条件。若把它概括成六个候选都能独立杀灭野生型 *A. baumannii*，会越过原文证据。[SyntheMol, Fig. 5a–c](https://www.nature.com/articles/s42256-024-00809-7)

## 代表性工作与证据边界

| 工作 | AI 在流程中的位置 | 直接验证 | 阅读时的边界 |
| :-- | :-- | :-- | :-- |
| [Abaucin（2023）](https://doi.org/10.1038/s41589-023-01349-8) | 对 7,684 个小分子做 *A. baumannii* 生长抑制筛选，以活性数据训练深度模型，再对已有药物/化合物库排序；属于**AI 引导筛选与再定位**，不是从头生成新分子 | 对预测候选进行体外验证，得到对 *A. baumannii* 窄谱活性的 abaucin；原论文以 `lolE` 为线索报告机制，并做小鼠伤口感染模型 | Extended Data Fig. 1 给出训练筛选和高/低预测分数候选验证；Fig. 3–4 为机制与动物实验。2026 结构研究解析的是该菌的同源转运体 LolDF，不把 2023 年的 `lolE` 命名和后来的 LolDF 结构证据混成同一层级。 |
| [SyntheMol（2024）](https://doi.org/10.1038/s42256-024-00809-7) | MCTS 在 Enamine REAL 的反应和 building-block 组合空间中，联合抗菌活性、毒性等预测器搜索；论文所定义的子空间约 295.8 亿种可组合分子 | 58 个生成分子被合成并测 MIC；六个对 *A. baumannii* 达到 MIC ≤8 μg/mL，但该 hit 判据使用 SPR741 或 colistin 的 1/4 MIC 联用。六者对 LPS 缺失 *A. baumannii* 和 *S. aureus* 另有无通透化剂验证；论文还测了若干临床分离株 | 这证明“合成约束生成 + 实验命中”在该任务中可行，但 Gram-negative 外膜穿透是实际瓶颈；论文没有报告动物感染模型，不能把体外活性写成治疗效果。原文 Fig. 5、Extended Data Fig. 9。 |
| [片段扩展与从头生成（Cell 2025）](https://doi.org/10.1016/j.cell.2025.07.033) | GNN 对 *N. gonorrhoeae* 与 *S. aureus* 预测抗菌性；片段路线在 >4,500 万片段中筛选并用 F-CReM/F-VAE 扩展；另用 CReM、JT-VAE 从头生成分子 | 总计 24 个成功合成/测试的候选中，7 个显示选择性抗菌活性。NG1 对 *N. gonorrhoeae* MIC 0.5 μg/mL、MBC 1 μg/mL；DN1 对 MSSA/MRSA 的 MIC 为 4 μg/mL。NG1 与 DN1 分别在淋病和 MRSA 皮肤感染小鼠模型中降低细菌负荷 | **筛选、生成与实际合成不可混为一个命中率**：片段路线中曾选 80 个、对 27 个启动合成流程，成功合成两种；从头 JT-VAE 路线从 4,831 个 shortlist 到供应商可得的 22 个并测活性。NG1 的 LptA 由 PISA、转录和膜实验共同指向，尚不是结构级配体结合证明。小鼠试验是局部给药短期模型，不证明人体疗效。 |
| [SyntheMol-RL（2026）](https://doi.org/10.1038/s44320-026-00206-9) | 将原 MCTS 换成 RL value function，在 Enamine REAL 与 WuXi GalaXi 的组合空间生成；预测目标同时包含 *S. aureus* 活性和水溶性 | 两种 RL 版本共合成测试 79 个分子：RL-Chemprop 38 个中 11 个、RL-MLP 41 个中 2 个达到论文设定的 MIC ≤8 μg/mL。一个来自 RL-MLP 的化合物 MLP-01（synthecin）在 2% w/v 外用制剂的小鼠 MRSA 伤口模型中显著降低细菌负荷 | 作者对七个 hit 做了新颖性人工筛查后，选 synthecin 做动物实验；这不是广谱候选。该实验是小鼠、局部高浓度制剂和短时伤口模型，且论文未建立 synthecin 的分子作用机制。 |

## 模型路线与证据漏斗

这些论文并不是同一种生成器逐代升级。Abaucin 的监督学习器从已有化合物的表型数据学习，再为 Drug Repurposing Hub 候选排序；它回答“已有分子库里哪些值得测试”，并非从头设计 abaucin。SyntheMol 把可购买 building blocks 与反应模板作为搜索图，用 MCTS 遍历约 29.6 billion 个组合，并以多个活性预测器引导搜索；合成约束进入候选构造过程，但预测可合成不保证实际供货、纯度或反应成功。[Abaucin Nature Chemical Biology Fig. 1–2](https://www.nature.com/articles/s41589-023-01349-8) [SyntheMol Methods、Fig. 3–5](https://doi.org/10.1038/s42256-024-00809-7)

Cell 2025 把小分子生成拆成片段扩展与从头两条路径。前者用 GNN 在大量片段中做表型筛选，再由 CReM/VAE 扩展；后者直接从训练分布生成候选。两条路都经过化学审查、可得性筛选和实际合成，因此“生成数千万候选”与“24 个成功合成、7 个有活性”是不同分母。NG1 的 LptA/外膜机制线索与 DN1 的膜活性也不是同一作用机制。[Cell 2025 Fig. 1–3、5–7](https://doi.org/10.1016/j.cell.2025.07.033)

SyntheMol-RL 改变的是合成空间中的搜索策略，而不是变成无约束分子生成。value model 学习 building-block 组合节点的预期属性分数，以抗菌活性和水溶性联合指导扩展；主要训练菌株仍是 *S. aureus* RN4220。`11/38` 和 `2/41` 是两个 RL value-model variant 在成功合成并按论文 MIC 阈值检测后的命中数，不是全部生成候选的比例。RL 与 MCTS 的算法比较应以同一论文、同一预测器/空间/筛选流程下的对照为准。[SyntheMol-RL Methods、Figs. 2–4、Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13230741/)

跨论文的共同证据漏斗是：**模型筛选或生成 → 化学可得/合成 → 目标菌体外活性 → 机制 → 动物模型**。Abaucin 与 Cell 2025 给出机制和小鼠实验；原始 SyntheMol 主要提供体外活性，SyntheMol-RL 的 synthecin 有小鼠局部伤口模型但机制未明。候选命中数必须连同靶菌、MIC 阈值、通透化剂、筛选分母、合成成功数和给药方式一起解释，不能横向拼成生成器排行榜。

### Abaucin：AI 命中之后，机制证据如何变强

2023 年论文的 DMPNN/神经网络从已测试活性数据学习，再将预测用于已有化合物集合。原文 Extended Data Fig. 1 区分了训练集与预测候选的验证，Fig. 2 评估窄谱活性，Fig. 3 通过耐药突变、转录数据和 CRISPRi 等证据把 `lolE` 作为 lipoprotein trafficking 机制线索，Fig. 4 报告小鼠伤口感染结果。2026 年结构工作进一步以 *A. baumannii* LolDF 解析 abaucin 结合构象与转运抑制。因而准确表述是“AI 引导从已存在分子中筛出抗菌活性，并在模型中观察到体内效果”，不是“AI 从零创造了一种抗生素”。[2023 原文及图注](https://www.nature.com/articles/s41589-023-01349-8) · [2026 结构机制研究](https://www.nature.com/articles/s41467-026-75428-4)

2026 年的独立后续研究把机制从遗传关联推进到结构和生化证据：cryo-EM 显示两分子 abaucin 对称占据 *A. baumannii* LolDF 腔体；带 lipoprotein 的复合物结构及转运实验支持 abaucin **不阻断底物结合，而是阻止底物转移到 LolA**。同文还在西南医院临床分离的 CRAB 中测活性，并在中性粒细胞减少小鼠肺炎模型中测试治疗。后者使用 HX-R7、约 `10⁷ CFU` 感染，abaucin 20 mg/kg 给药四次；主要组织学指标每组 n=5，BALF 细菌负荷 n=3。它明显增强了机制和前临床证据，但单中心菌株、小样本和特定免疫抑制模型都限制外推。[Pang et al. 2026, Figs. 1–5](https://www.nature.com/articles/s41467-026-75428-4)

### 从生成到体内：Cell 2025 与 SyntheMol-RL 的两种路线

Cell 2025 说明“生成候选”不等于“生成后就能合成”。片段扩展路线先从 >45 million 片段中寻找抗菌片段，再用 F-CReM/F-VAE 扩展；作者对 80 个候选挑选了 27 个进入供应商合成流程，最后得到 NG1、NG2 两个成功合成物，只有 NG1 对目标淋病奈瑟菌表现出活性。独立的 JT-VAE 从头生成路线产生约 2,901 万结构，经过预测、人工化学审查和供应商采购后，22 个分子进入实验，6 个对 *S. aureus* 有抑制活性。NG1 与 DN1 的作用机制也不同：NG1 的证据指向 LptA/外膜相关效应；DN1 的膜电位、Laurdan 和 cryo-TEM 实验支持膜活性。作者报告 NG1 小鼠阴道感染模型 vehicle n=8、NG1 n=9，五次局部给药后约降低 3 log；DN1 在 MRSA BAA1556 中性粒细胞减少小鼠皮肤伤口模型 vehicle/DN1/fusidic-acid 各 n=6，六次 1% 外用给药后对 vehicle 的细菌负荷降低约 10 倍。详细计数和 p 值见精读笔记及原文 Fig. 3、6–7。[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12790861/)

SyntheMol-RL 的变化不是“搜索更大”，而是把生成策略改成在线学习的 building-block 价值函数，并在生成时同时优化预测抗菌活性与水溶性。它比较 RL、MCTS 和虚拟筛选，并实际合成多个类别候选。值得仔细读的是分母：`11/38` 与 `2/41` 指各自 RL 生成组中达到 MIC ≤8 μg/mL 的数量；其余生成方法及虚拟筛选有单独实验组，不能只报告 RL 组比例而略去对照。Synthecin 来自 RL-MLP 组的 MLP-01，体外对 *S. aureus* RN4220 有活性；小鼠伤口模型感染 MRSA USA300，vehicle 与 synthecin 各 n=5，synthecin 为 2% w/v 的外用配方。其作用机制仍待后续研究。[原文 Fig. 2–5](https://pmc.ncbi.nlm.nih.gov/articles/PMC13230741/)

## 这条研究线当前说明什么

1. **表型数据可用于有针对性的筛选，但适用面受菌种与数据集约束。** Abaucin 与生成模型都用生长抑制标签；它们不能因一次任务命中就被视为通用抗菌分子生成器。
2. **把反应和 building blocks 放进生成定义，有助于把模型输出接上合成。** SyntheMol/SyntheMol-RL 的意义在于输出候选时有指定反应路线；这仍不等同于每个候选都能按预测成本、纯度和规模合成。真实分母要从“生成”追到“短名单、供应商可得、实际成功合成、通过活性测试”。
3. **革兰阴性菌外膜是独立的化学与生物学障碍。** SyntheMol 的活性阈值需联用通透化剂，Cell 2025 的 DN 分子对多种 Gram-negative species 也受限于外膜/外排。仅优化模型评分或 MIC 不能取代对细胞进入、外排和毒性的实测。
4. **机制确定是从 hit 到可学习设计规则的关键连接。** Abaucin 后续结构解析及 Cell 2025 对 NG1/DN1 的机制调查说明，结构、遗传、蛋白组和细胞表型各自回答不同问题。热稳定性变化、耐药突变或膜损伤都不是单独的直接结合证明。
5. **目前证据仍在早期临床前。** 所选论文报告体外检测及小鼠模型，没有在人类中验证疗效或安全性；小鼠试验也不是人体剂量、给药途径或疾病结局的替代。

## 建议的精读顺序

1. [Abaucin 2023 + 2026 机制跟进](papers/abaucin-screen-to-mechanism.md)：读 Fig. 1 / Extended Data Fig. 1、2023 Fig. 3–4，再读 2026 Fig. 2–5；重点辨析预测命中、遗传证据、结构占位和运输功能测定的区别。
2. [SyntheMol 2024](papers/2024-synthemol-mcts.md)：先读清 MCTS 如何把合成反应和 building blocks 纳入搜索，再核对六个 hit 的 MIC 测试依赖通透化剂。
3. [SyntheMol-RL 2026](papers/2026-synthemol-rl.md)：关注生成空间、模型预测训练集、novelty 筛选、合成分母、MIC 阈值以及局部动物模型条件。
4. [Cell 2025 de novo design](papers/2025-cell-de-novo.md)：分别跟踪 fragment route 和 de novo JT-VAE route，核对每个候选从模型到合成、机制和动物验证的去向。

固定版本、许可、来源位置、PaperFetcher 检索记录与未复现边界见[来源清单](sources/MANIFEST.md)。
