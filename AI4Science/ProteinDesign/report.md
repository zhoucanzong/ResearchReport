---
type: research
domain: AI4Science
subject: ProteinDesign
date: 2026-10-23
evidence: fixed-primary-papers
status: completed
---

# 蛋白质 binder 发现：从复合物生成到候选筛选

> **范围**：这是 AI for Science 的首个专题条目，聚焦蛋白质/肽 binder 的计算发现流程，不代表整个 AI4Science 领域。主问题是：模型如何提出候选、怎样判断候选值得实验，以及结构/代理分数与真实结合结果之间还差什么？

## 核心结论

当前这组工作显示，AI 进入 binder 发现的环节正在从“生成更多序列”扩展为“同时生成复合物结构、在序列空间探索候选、按多种代理分数分配有限实验名额”。三篇论文各自研究的是流水线的不同阶段，数据、任务和指标不一致，不能合成一个模型排行榜。

1. **APM** 将多链复合物、序列、主链和侧链构象纳入统一生成框架；其抗体与肽设计结果是基准和计算能量证据。作者明确指出，实际有效性仍需湿实验确认。
2. **PepEDiff** 在蛋白语言模型嵌入空间中直接生成肽序列，减少生成阶段对中间结构预测的依赖；但 TIGIT 案例的构象、能量和稳定性评估仍调用 Boltz-2、Rosetta 与分子动力学，不能称为实验确认的 binder。
3. **自然语言引导的候选短名单**不训练新的 binder 生成器，而是在固定的候选池中组合 AF2-Multimer、Boltz-2、Protenix 和 Rosetta 的 17 个代理分数。对 10 个留出靶标，迭代 GPT-4o 策略的 Recall@10 为 0.589，单分数最强基线 Protenix binder ipTM 为 0.571；差距有限，且结果来自回顾性历史实验池（[arXiv 2608.20755v2, Table 3 / §6](https://arxiv.org/html/2608.20755v2)）。

所以阅读这条研究线时，应把证据拆成**候选生成、结构/界面代理、候选排序、实验测定**四层。前三层的提升有价值，但不能自动推出新靶点上的实验成功率或药物可开发性。

## 从生成到实验：一条分层证据链

| 环节 | 论文中的做法 | 能回答的问题 | 不能单独证明的事 |
| :-- | :-- | :-- | :-- |
| 复合物生成 | APM 联合生成序列、主链和侧链构象 | 能否直接表示多链原子级相互作用？ | 生成结构是否真实结合、表达稳定或具备功能 |
| 序列生成 | PepEDiff 在 ProtT5 嵌入空间做条件扩散 | 不先生成复合物结构，能否探索肽序列？ | 预测能量是否对应真实亲和力 |
| 候选排序 | LLM 将多模型置信度和界面描述组合成排序规则 | 在已生成候选中，哪些值得优先实验？ | 新靶点、不同 assay 或未见生成流程上的性能 |
| 实验确认 | 对候选做表达、结合和功能测定 | 候选是否在具体实验条件下有效？ | 对其他靶标、条件和生物体系的泛化 |

三个环节使用的 benchmark 和数据源不相同。APM 的 RAbD、PepBench/LNR 结果，PepEDiff 的 TIGIT 计算案例，以及短名单论文从公开实验结果汇总的 hit labels，均须按各自 split 和指标分别阅读。

## 代表工作

### 1. APM：多链、全原子复合物生成

APM 把单链蛋白建模扩展到多链复合物。论文的表示包含氨基酸类型、SE(3) 主链刚体帧和侧链 torsion angles。架构由 Seq&BB、Sidechain、Refine 三个模块组成：Seq&BB 用 flow matching 联合生成序列与主链，Sidechain 补侧链构象，Refine 作结构细化（§3.1–3.2）。

训练数据包括 187,494 条单链样本和 11,620 条多链样本；多链训练对超过 384 个残基的样本围绕界面随机裁剪（[arXiv 2504.13075v3, §4.1](https://arxiv.org/html/2504.13075v3)）。论文在 RAbD 抗体 CDR-H3 以及 PepBench/LNR 肽设计等任务上使用 AAR、RMSD、Rosetta 能量、折叠置信度和 DockQ 评估（[§4.4、Appendix D](https://arxiv.org/html/2504.13075v3)）。这些指标反映序列相似、预测结构或能量函数上的性质，并非 binder 的湿实验结合率。

一个值得注意的失败边界是：APM 的 zero-shot 抗体设计在计算结合能上可以较好，但序列/结构与天然 CDR-H3 差异较大；论文还展示了生成的环可能结合抗体轻链而非目标抗原（Appendix D.4）。这说明“能生成相互作用结构”与“生成符合生物学机制的目标特异性抗体”是不同判据。

### 2. PepEDiff：在蛋白嵌入空间生成肽序列

PepEDiff 接收目标受体序列与口袋残基 mask，将受体和 peptide 表示编码到 ProtT5 embedding 空间，再以条件扩散模型生成 peptide embedding 并解码为序列（§2）。作者报告 peptide binder 数据为 4,758 条（§2.4、§3.1）。

在 TIGIT 案例中，每种方法生成 100 条 15-aa 候选；论文从每种方法各取一个最高分候选做动力学模拟和 umbrella sampling（[arXiv 2601.13327v2, §3.3](https://arxiv.org/html/2601.13327v2)）。PepEDiff 候选的表面接触面积、分子动力学相互作用能和模拟自由能优于论文列出的两条计算基线（[§4.2](https://arxiv.org/html/2601.13327v2)）。但这一流程仍用 Boltz-2 预测 PepEDiff 序列的复合物构象，再通过 Rosetta 和 MD 评估；论文没有报告新生成候选的湿实验结合验证。

这篇工作的实质贡献是**把生成阶段从结构坐标转到蛋白语言模型的连续嵌入空间**，不是消除了结构预测或物理评估。TIGIT 只有一个靶标案例，不能据此得出普遍的靶点泛化结论。

### 3. 自然语言引导的短名单：把实验预算纳入问题定义

这项 2026 年工作将生成后的筛选形式化为 top-K 决策：固定每个靶点的候选池，用 17 个预计算特征组合排序。特征来自 AF2-Multimer、Boltz-2、Protenix/PXDesign 与 Rosetta 界面描述符（§3–4）。

10-target held-out split 含 2,269 个候选、251 个已验证 binder；迭代 GPT-4o 的五个策略样本平均 Recall@10 为 0.589，超过最强单特征基线 Protenix binder ipTM 的 0.571，但这是约 1.8 个百分点的增益。三靶点子集上 GPT-5.4 target-conditioned 迭代策略 Recall@10 为 0.519，固定 Protenix binder ipTM 为 0.504；小样本结果适合作为探索证据，不宜写成稳定普遍优势（[arXiv 2608.20755v2, Tables 1/3, §6](https://arxiv.org/html/2608.20755v2)）。

这里的标签来自既有实验释放数据，论文回顾的是**已有候选池的筛选**，没有报告本研究重新设计并进行湿实验。作者进行模型知识截止时间与标签公开日期的审计，但这不等于对新靶点、新 assay 或未来实验流程完成前瞻验证（Appendix B）。

## 阅读时应逐项核对的判据

- **新靶点隔离**：train/dev/test 是否按靶点、序列同源性和 assay 来源分开，而非只随机切分候选？
- **候选池来源**：正负标签来自哪些实验？未测试候选是否当作负例？同一候选跨公开 release 重复出现时如何处理？
- **代理指标**：ipTM、pDockQ2、Rosetta ΔG 与 MD 分别是预测置信度、经验打分还是模拟量，不能统称为“亲和力”。
- **实验闭环**：是否有本研究新做的表达、结合或功能实验？若没有，结论停留在计算筛选或回顾性排序。
- **可开发性**：结合之外，还需表达量、溶解度、聚集、稳定性、特异性与免疫原性等指标；结构和 docking 分数不覆盖这些要求。

## 当前结论与待跟进

这条线最值得关注的研究问题，是如何把结构预测与生成模型的 proxy scores 校准到前瞻性湿实验结果，并验证跨靶点、跨 assay 和跨生成器的泛化。近期工作已经开始优化候选筛选，但公开证据仍以计算评估和历史实验标签为主。本条目不推断候选可成为治疗分子，也不把不同论文的分数横向合并。

本报告仅为 AI4Science 的蛋白质 binder 方向首轮专题，尚未覆盖小分子药物发现、酶设计、材料科学或天气气候模型。

## 原文与分册

- [APM：An All-Atom Generative Model for Designing Protein Complexes](papers/2504.13075-apm.md)
- [PepEDiff：Zero-Shot Peptide Binder Design via Protein Embedding Diffusion](papers/2601.13327-pepediff.md)
- [候选短名单：Natural-Language-Guided Generator-Agnostic Shortlisting](papers/2608.20755-shortlisting.md)
- 固定版本、许可与原文位置见 [sources/MANIFEST.md](sources/MANIFEST.md)；入选与暂缓候选见 [sources/CANDIDATES.md](sources/CANDIDATES.md)。
