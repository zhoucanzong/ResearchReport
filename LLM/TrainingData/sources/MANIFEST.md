# TrainingData — 来源清单

核查截止：2026-10-23。以下结论分别来自固定原文版本。全文/ PDF 暂存于 `/tmp` 的临时研究目录，不写入仓库或共享 `paper-cache`；均未运行作者训练、下载权重或复现实验。

按本机 `researcher` 与 `paper-fetcher` 工作流检索、取源和精读；未把搜索摘要替代原文，也未将任何 benchmark 或训练实验重跑。

| ID | 固定来源 | 原文定位 | 本专题用法与边界 |
|---|---|---|---|
| S1 | Penedo et al., *The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale*, arXiv `2406.17557v2`, revised 2024-10-31; NeurIPS 2024 Datasets & Benchmarks; arXiv PDF CC BY 4.0; released data ODC-By. | [官方 HTML v2](https://arxiv.org/html/2406.17557v2)：§3.1–3.6, Figures 1–5（抽取、过滤、去重消融）；Appendix D（1.71B 训练配方）；Appendix E.1–E.4, Figures 13–15, Table 2（MinHash 阈值、去重范围与附加过滤）。 | **[精读原文]** 控制设置下研究 HTML/WARC/WET 抽取、质量过滤、单快照与跨快照去重。图上读取的若干差值无表格误差条，正文标为近似；主任务以英语为主、小模型和有限基准，不外推为通用配方。PDF SHA-256 `ae632bd6618d2566e708962670f27ab1fbc5ba9bc8de3acaceee8fbda85fbdd4`，仅 `/tmp/fineweb-dedup/`。 |
| S2 | Li et al., *DataComp-LM: In search of the next generation of training sets for language models*, arXiv `2406.11794v4`, revised 2025-04-21. | [官方 HTML v4](https://arxiv.org/html/2406.11794v4)：§3.2–3.5, Table 1（模型/训练 token 预算）；§4.2–4.6, Tables 3–6（抽取、过滤、去重和数据混合）；Appendix F（配方/超参）、N（人工标签）、U（datasheet 与 split）。 | **[精读原文]** 作为固定训练资源下数据策展对照；人工标签与下游效用不一致；下游任务被用于策展选择，Datasheet 没有推荐 corpus-level split，MMLU/HellaSwag 的污染检查为局部。未运行训练。PDF SHA-256 `af8fc884ccd601f8c6fbbba8f8e381de652fce1233949c0c64f64b4ab4b0f5b2`，仅 `/tmp/datacomp-lm/`。 |
| S3 | Lee et al., *Deduplicating Training Data Makes Language Models Better*, arXiv `2107.06499v2`, revised 2022-03-24; ACL 2022. | [官方 HTML v2](https://arxiv.org/html/2107.06499v2)：§4.1.2（ExactSubstr）、§4.2（NearDup）、§5.2/Table 1（跨 split 去重）；§6.1–6.2, Figures 2/Table 4–5（PPL 与生成记忆）；§7（局限）；Appendix C/Table 13（训练配方和去重后样本/token 计数）。 | **[精读原文]** 去重降低文中定义的 50-token 生成记忆指标；PPL 不普遍受损。但作者明确不研究下游 benchmark 能力提升。结果限于 C4、英语和 T5 设置，记忆指标不代表所有隐私泄露。PDF SHA-256 `dcfa46d7aced43a97b9cf2ebd705919b65d4dd8a44d0914b1e646fe2d59ea8d3`，仅 `/tmp/dedup-memorization/`。 |

## 审核口径

- FineWeb 的全局去重与单快照去重效果来自各自固定采样和 1.71B/训练 token 设置；图上差值不是精确表格数值。
- DataComp-LM 的固定训练预算比较仍使用作者的开发基准选择方案，不是独立盲测；数据集“质量”在这里指该下游效用协议下的结果。
- Deduplicating Training Data 的“记忆”是精确 50-token 子串匹配，不覆盖其他隐私泄露类型；论文没有下游能力结论。
