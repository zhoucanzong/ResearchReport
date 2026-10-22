# Validation and analysis of 12,000 AI-driven CAR-T designs in the Bits to Binders competition

> **固定来源**：[Molecular Systems Biology full text](https://link.springer.com/article/10.1038/s44320-026-00246-1), DOI `10.1038/s44320-026-00246-1`; published 2026-10-08; CC BY 4.0. PaperFetcher does not resolve this DOI (HF 404, arXiv 400). This note was checked against the publisher's open-access article.
> **证据等级**：`[精读原文]`（Abstract、Results、Figs. 1–5 / EV1–EV5、Appendix Tables EV1–EV4、Methods、Discussion）。未复现分析代码或重做实验。

## 亮点与差异

- **一句话亮点**：把 12,000 个 de novo CD20 binder 直接放进 CAR-T 架构做功能筛查，显示候选的序列/结构分数、可恢复表达、增殖和特异杀伤是不同层次的成功条件。
- **规模与结果**：28 个团队、42 个国家，提交 12,000 个长度 80 aa 的设计。Pooled screen 找到 707 个至少两倍且显著的 CD20 特异富集候选，团队 hit rate 为 0.6%–38.4%（Abstract; Results “Screening…”; Fig. 2）。
- **功能拆分**：对前十个非冗余设计做个别测试，7/10 高于阴性对照的 CD20 特异增殖、扩增及细胞因子读数，4/10 高于对照的特异杀伤；这十个设计总体低于 scFv 阳性对照的功能读数（Fig. 3; Discussion）。孤立 80-mer 的 SPR 只有少数可量化结合，design 2383 的 KD 为 643 nM（Fig. 3F）。
- **适合支持的结论**：结构预测或结合分数不足以代表一个短 binder 能否合成、表达为 CAR、维持细胞适应度并驱动靶点依赖功能；应把这些实验终点分别报告。

## 关键方法与发现

团队只提交结合域，研究者将其装入同一第二代 CAR backbone 并整合至 TCR alpha-chain locus。Pooled screen 比较 CD20+ Raji challenge 与无靶培养两周后的 barcode abundance；统计分析使用每条件三个技术重复、单一供者来源的 primary T cells，显著性以 edgeR 控制 FDR（Methods; Fig. 2）。98.3% 设计通过 DNA QC，但只有 56.8% 达到增殖 assay 的最低测序读数；707 个显著 hits 因此代表 pooled enrichment，而不是经逐条验证的结合率或治疗有效率。

前十候选的细胞功能进一步分化：虽然 7 个在增殖、扩增和细胞因子方面优于阴性对照，只有 4 个提高 CD20 特异杀伤，且结果基于来自一个供者细胞的技术重复。作者对超过 400 个特征作探索性分析，发现一些序列规则与 DNA 合成失败或 CAR-T 细胞恢复相关；全局 ipTM、pLDDT 等结构置信度分数没有预测实验结果（Fig. 4–5; Appendix Table EV2）。

## 限制与解读

研究只覆盖 CD20、80-aa binder 和一个 CAR scaffold；方法来自自选的竞赛团队，不是严格控制的算法头对头实验。筛出的前十设计是从 pooled screen 排名中挑选后再测，因此不能代表全体 hits 的个体功能分布。事后应用序列过滤规则会提高同一数据集内的比例，但属于回顾性分析；作者也指出方法分类无法排除混杂或证明因果（Results; Discussion）。个别 SPR 用分离的 binder 和 detergent-solubilized CD20 测定，未包含 CAR 展示、折叠和 avidity 的情境（“Characterization of binding”）。因此这项研究是强功能筛查证据，不是跨靶标成功率、临床疗效或普遍序列规则的验证。
