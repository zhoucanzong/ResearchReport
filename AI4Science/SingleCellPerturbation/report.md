---
display_name: 单细胞扰动预测
type: research
domain: AI4Science
subject: SingleCellPerturbation
date: 2026-10-23
evidence: fixed-primary-papers
status: completed
---

# 单细胞扰动预测：从“配对细胞”转向“群体响应”

> **范围**：本条目聚焦 Perturb-seq 等单细胞实验中的转录组扰动响应预测，尤其是模型怎样处理细胞间异质性，以及评测怎样区分扰动特异信号与数据中的系统性变化。它不是单细胞 foundation model 的全景综述，也不覆盖细胞注释、空间解卷积或多组学整合。

## 先给结论

单细胞 RNA 测序通常是破坏性测量：同一个细胞不会同时留下扰动前和扰动后的转录组。因此，模型把 control cell 映射到 perturbed cell 时，映射关系是算法构造出来的，不是实验观测到的一对一细胞命运。近年的方法开始显式建模**细胞群体的响应分布**，但其预测是否真正跨越了未见扰动、未见背景，取决于 split、reference 和标签来源，不能仅凭模型名称中的 “OOD” 或 “generalizable” 判断。

有三点尤其值得学习：

1. **目标量要讲清楚**：单细胞状态是一个观测向量；群体均值和响应分布是某一条件下多细胞的统计量；扰动效应则是相同背景下处理组与对照组的差异。表达矩阵重建得准，不一定意味着扰动效应方向或差异基因选得准。
2. **评测设计本身会改变答案**：Systema 显示常用 control-reference 指标可能主要奖励 control 与 perturb 之间共有的系统性差异。换成强调 perturbation-specific effect 的 reference 后，分数明显降低。模型性能数字必须连同 reference 与 held-out 轴来读。
3. **最新模型提供的是待验证方法假设**：P2P 用同一条件下随机抽出的 cell-set views 训练可重复的群体效应；scEGFlow 用 optimal transport 形成软伪配对，再以 flow matching 生成细胞群体、以能量梯度做条件化修正。这两篇是 2026 年 arXiv v1 预印本，尚无独立复现或新实验验证。

这些研究是在**已有干预实验数据**上学习或评估响应预测。即使输入标签来自 CRISPR 等干预，也不能直接把模型的预测解释成已识别的因果机制：预测性能不等于因果效应识别，更不等于发现了调控路径。后两者还需要明确的实验设计、识别假设与机制验证。

## 问题拆解：预测什么，在哪个轴上泛化？

| 任务说法 | 实际测试对象 | 能支持的结论 | 不能直接推出 |
| :-- | :-- | :-- | :-- |
| 同一 perturbation 下的细胞留出 | 已观测处理条件内部分细胞不参与训练 | 估计该条件下尚未见细胞的群体统计量 | 对未测基因、药物或新细胞类型的外推 |
| 未见 perturbation | 某个靶点/处理条件整体留出 | 对指定 split 上新干预条件的预测能力 | 新组织、实验室、剂量和测序流程同时泛化 |
| 未见 cellular context | 细胞系/细胞类型整体留出 | 对该 context 轴的迁移证据 | 机制已跨组织保守或因果效应已识别 |
| 处理组 vs 对照组重建 | 比较预测与实测表达/分布 | 对选定距离、相关或差异基因指标的拟合 | 治疗有效性、细胞命运变化或真实生物学机制 |

报告结果至少要记下四个量：**数据单位**（单细胞、条件均值或响应分布）、**held-out 轴**（细胞/干预/背景/剂量/组合）、**reference**（相对哪个控制或扰动群体计算 effect），以及**分数来源**（原实验标签还是模型/数据库代理）。同一数据集上的不同 split 可以回答完全不同的问题。

## 研究进展：两种群体建模路线

### P2P：让随机 cell-set views 学习共通响应

P2P 的出发点是：control cells 和 treated cells 是各自采样的群体，没有自然的单细胞配对；随机抽两个 cell sets，二者共享条件层面的响应，但采样噪声不同。模型用 permutation-invariant set encoder 表示 control population，将扰动 token、细胞背景、剂量与组合特征编码为条件；一个 gate 混合经验条件效应和神经残差，另一个 head 输出基因层面的方差。[原文 §3.1–3.2、Fig. 1–2](https://arxiv.org/html/2609.34391v1)

论文在 Adamson、Norman、Replogle K562、Replogle RPE1 四个处理数据上报告五个 seed 的均值和标准差。在其固定评测协议里，P2P 的 Replogle K562 Effect Pearson 为 0.7018，Scouter 为 0.6432；DEG F1 为 0.1784 对 0.0671（Table 1）。这是两项**绝对指标值**的差，不是百分点意义上的准确率增幅。[原文 §4.1–4.3、Table 1](https://arxiv.org/html/2609.34391v1)

这里有一个重要的任务边界：论文的训练/验证/support/test 是按细胞角色划分；经验 effect memory 使用 target condition 的 training-role cells。因此，直接 readout 证明的是同一已观测 condition 中对保留细胞的估计表现，不能表述成对完全未见 gene perturbation 的零样本预测。论文还说明 gene vocabulary 从当前处理数据构造，是对 token identity 的 transductive setting；memory-assisted transfer 也使用目标 condition 的训练角色细胞。[原文 §4.1、Appendix B](https://arxiv.org/html/2609.34391v1)

### scEGFlow：群体输运加目标条件能量修正

scEGFlow 处理的是 control 与 perturb populations 未配对的问题：先用 optimal transport 得到软 cell correspondences，以这些伪配对训练 conditional flow-matching 模型，从 control 状态学习连续到 perturbed distribution 的 velocity field；推理时再用特定药物、剂量或 context 的能量梯度修正生成状态。关键点是把**群体输运**与**终点条件校准**拆开，后者可用于目标条件的小样本适配而无需重训 flow backbone。[原文 Fig. 1、§2.1、Methods §§4.2–4.4](https://arxiv.org/html/2610.02232v1)

论文在 4i imaging、SciPlex3、ComboSciPlex 和 LINCS L1000 上评估，涵盖药物剂量、细胞背景和药物组合留出。SciPlex3 的一个 unseen-context split 中，scEGFlow 的 Energy distance 为 3.8726，CellFlow 为 22.3046；但指标依赖该论文的预处理、所留条件和选定低维/表达统计定义，不能视为跨数据集通用分数。[原文 §2.3、Table 2](https://arxiv.org/html/2610.02232v1)

作者另以 LINCS L1000 的 Level 3 表达剖面训练、Level 5 consensus signature 作方向参考，在 111 个评估 contexts 上报告：最强扰动基因集的方向一致率均值由未加能量引导的 72.0% 提高至 81.0%，98/111 个 context 提升。[原文 §2.5、Fig. 5](https://arxiv.org/html/2610.02232v1) 这属于与既有共识 signature 的外部对照；仍不是研究新做的 perturbation assay，也不能当作因果通路验证。

### 评测先行：Systema 揭示“共变”可能冒充“扰动特异预测”

Systema 在 10 个数据集、3 种实验技术与 5 种细胞系上量化 systematic variation，指出一些常用指标容易受 control/perturb 间持续存在的系统性偏移影响。论文用 perturbed-centroid 作为替代 reference 来强调扰动间差异；其 control-reference 下的 perturbation-specific shift 与平均 shift 方向平均 cosine similarity 为 0.41 ± 0.18，说明两种 reference 聚焦的信号并不等价。[原文 Fig. 2、Fig. 4、Methods；Nature Biotechnology 2025](https://www.nature.com/articles/s41587-025-02777-8)

这不表示 perturbed-centroid 是唯一正确指标：作者也说明 reference-sensitive 指标会对 reference 选择敏感、对效应强度不具不变性，对弱扰动效果有限。因此要报告多指标和生物学 downstream utility，而不是把某个修正 reference 变成新排行榜。Systema 的核心贡献是让研究者检查**模型究竟复现了什么信号**，而不是证明所有现有模型皆无效。[原文 Discussion、Methods；PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC13271886/)

作为另一层背景，2025 年 scPerturBench 评估了 27 种方法、29 个数据集、6 种互补指标；其规模体现出该领域的比较基线正在从单数据集 leaderboard 转向多情境评估。不过跨论文 benchmark 的数据处理、基线版本和 split 仍须逐一对照，单凭“27 个方法”不能断言谁在所有任务胜出。[原文摘要与元数据；Nature Methods](https://pubmed.ncbi.nlm.nih.gov/41381899/)

## 如何读结果：三个常见误区

### 高表达相关不等于扰动信号预测准确

所有细胞共享大量基础表达结构。若指标直接比较预测表达与处理组表达，模型只需贴近总体均值就可能得高相关，但真实的扰动增量很小。P2P 报告的 expression Pearson 与 effect Pearson/DEG ranking 分开；Systema 则进一步检验 reference 带来的 systematic variation。阅读时应优先看 effect-level metric、差异基因排序、方向一致性和 distributional distance，并核查是否都在同一 held-out 任务上计算。

### “单细胞预测”不总是逐细胞预测

一个模型即使输出很多细胞，也不表示每个输出细胞都是某个真实细胞的反事实。P2P 主目标是条件均值和基因方差；scEGFlow 用 OT 伪配对提供学习轨迹，但这些是算法构造的对应关系。应将它们理解成群体分布或统计量预测，除非实验设计真的追踪同一个细胞并观察其变化。

### 干预标签不自动赋予因果机制

Perturb-seq 的 CRISPR/药物操作使监督数据具有干预背景；模型可以预测实验条件下的平均响应。但数据中的脱靶、存活选择、细胞周期与 batch effects 可能和处理标签共同变化。若任务是识别“基因 A 通过路径 B 导致表型 C”，还需更强的设计或假设，且应有正交实验验证。本文纳入模型论文所报告的预测，不将其升级成因果发现。

## 目前能下的判断

- 方向正在从“预测单个转录组”转向同时描述**群体响应、异质性和实验条件**。P2P 的核心是跨随机群体 views 学习共享 effect；scEGFlow 的核心是把状态输运与能量条件修正拆开。
- 比模型规模更先要解决的是任务和指标：held-out perturbation、held-out cells 与 few-shot support 是不同的泛化问题；相对 control 的差异评测也不同于处理组表达重建。
- foundation model 是这一领域中的一条路线，不代表扰动预测需要更大的预训练模型。现有研究同时表明生物先验、简单基线、群体统计和 reference 选择会显著影响结论。本条目暂不展开 foundation-model pretraining 的模型架构比较。
- 目前代表性 2026 新方法是预印本报告的离线基准结果，未完成独立重跑或前瞻性实验。预测模型可帮助提出实验优先级，但现有证据不足以称其已经构成可验证的 virtual cell 或因果数字孪生。

## 下一步最值得补的证据

1. 在研究设计中预先锁定全新 perturbation target、细胞背景和实验批次；公布按靶点与 batch 分组的 held-out 设置。
2. 同时报告 population mean、扰动效应、分布形状、差异基因排名与不确定性校准，且包含 mean/linear baselines。
3. 把 prediction 与 causality 分开验收：预测研究需前瞻性测量预测命中的条件；机制研究需额外的中介/救援或正交扰动实验。
4. 使用空间扰动筛选观察邻域与组织状态变化，将来能检验纯 dissociated scRNA-seq 预测是否保留空间背景；这属于下一条独立主线，本文不扩成空间组学综述。

## 精读材料与来源

- [P2P：Cross-View Population Denoising](papers/2609.34391-p2p.md)——重点看目标变量、memory 协议与 held-out 定义。
- [scEGFlow：Energy-Guided Flow Matching](papers/2610.02232-scegflow.md)——重点看 OT 伪配对、条件留出和 L1000 对照。
- 固定版本、日期、许可、原文定位和证据边界见 [sources/MANIFEST.md](sources/MANIFEST.md)；入选与淘汰记录见 [sources/CANDIDATES.md](sources/CANDIDATES.md)。
