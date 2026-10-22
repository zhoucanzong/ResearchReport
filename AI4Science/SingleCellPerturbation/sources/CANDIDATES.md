# Candidate screening

筛选问题：哪些原始研究能帮助解释单细胞扰动预测中的**群体响应目标、异质性建模、泛化轴与评测偏差**？候选共 10 篇；入选 4 篇用于主报告（其中 2 篇有精读分册）。不按模型新旧或 foundation-model 标签单独入选。

## 入选

| Work | Decision | Reason |
| :-- | :-- | :-- |
| P2P, arXiv:2609.34391v1 | 主文 + 精读 | 最新群体视角：随机 cell-set views、memory-gated condition effect 与 variance readout；需特别界定其 target-condition training memory，避免误读为 zero-shot unseen perturbation。 |
| scEGFlow, arXiv:2610.02232v1 | 主文 + 精读 | 将 OT 伪配对、conditional flow 与 energy-guided endpoint correction 分解；同时评估剂量、context、组合和外部 consensus signatures，便于比较 population-distribution prediction。 |
| Systema, DOI:10.1038/s41587-025-02777-8 | 主文 | 直接研究 systematic variation 与 reference-sensitive evaluation，是理解常规扰动指标过估计风险的关键评测工作。 |
| scPerturBench, DOI:10.1038/s41592-025-02980-0 | 主文简述 | 27 methods / 29 datasets / 6 metrics 的多基准研究，给领域评测范围提供尺度参照；未据 abstract 以外内容写方法排名。 |

## 暂缓 / 排除

| Work | Decision | Reason |
| :-- | :-- | :-- |
| Stable-Shift, arXiv:2606.24940 | 暂缓 | 单一 K562 benchmark 的低秩 unseen-gene 预测，主题相关；当前主文聚焦 population distribution 而非 latent response basis，保留供下一轮对照。arXiv 页面给出 DOI `10.1145/3807503.3820871`。 |
| DeMixPert, arXiv:2608.23114 | 暂缓 | Gaussian mixture 分解未见扰动、系统响应与总体异质性，与主线紧密；尚需充分核对全文协议、split 与表格后才适合纳入，不能只依据摘要。 |
| CellxPert, arXiv:2605.00930 | 排除本条目 | 将多模态与空间输入和 foundation model 结合，范围超出当前 genetic/chemical transcriptomic population-response 主线；适合未来建立单独的空间/多模态方向。 |
| C3TL, arXiv:2603.13051 | 暂缓 | 以 bulk molecular data 预测 context-specific perturbation effects，研究对象与数据单位不同；题名中的 “causal” 不足以证明单细胞因果识别。可作跨数据模态比较。 |
| “Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines”, DOI:10.1038/s41592-025-02772-6 | 纳入检索但未作为独立主文 | 对简单基线的有力审计；后续 `Systema`、多任务评测已在本报告中直接处理指标/reference 偏差。引用这个摘要式口号会掩盖数据与指标条件，因此暂不复述其总括结论。 |
| “Deep learning perturbation models can outperform baselines on calibrated metrics”, DOI:10.1038/s41587-026-03307-w | 暂缓 | 2026 年针对基线与指标校准的反向研究，值得与上一工作成对精读；本轮不在未核对全文 split 与 metric 定义时把两方观点简化成争论标签。 |

## 检索记录

- Researcher deep topic search: single-cell perturbation response prediction, population-level effects, generalization, evaluation metrics, virtual-cell modeling。
- PaperFetcher query results were screened for original methods, controlled evaluations, and challenge studies. Semantic Scholar returned HTTP 429 on search; discovery continued with arXiv, Crossref, DOI, PubMed, PMC, and publisher records.
- 题名与元数据的候选发现不等于正文精读；只有 manifest 中标出的章节、图、表被用于具体结论。
