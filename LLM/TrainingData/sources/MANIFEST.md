# TrainingData — 来源清单

核查截止：2026-10-24。以下结论分别来自固定原文版本；新补的两篇论文完整精读 arXiv HTML。没有运行作者训练或复现实验。

按本机 `researcher` 与 `paper-fetcher` 工作流检索、取源和精读；未把搜索摘要替代原文，也未将任何 benchmark 或训练实验重跑。

| ID | 固定来源 | 原文定位 | 本专题用法与边界 |
|---|---|---|---|
| S1 | Penedo et al., *The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale*, arXiv `2406.17557v2`, revised 2024-10-31; NeurIPS 2024 Datasets & Benchmarks; data released under ODC-By. | [官方 HTML v2](https://arxiv.org/html/2406.17557v2)：§3.1–3.6, Figures 1–5（抽取、过滤、去重消融）；Appendix D（1.71B 训练配方）；Appendix E.1–E.4, Figures 13–15, Table 2（MinHash 阈值、去重范围与附加过滤）。 | **[精读原文]** 控制设置下研究 HTML/WARC/WET 抽取、质量过滤、单快照与跨快照去重。图上读取的若干差值无表格误差条，正文标为近似；主任务以英语为主、小模型和有限基准，不外推为通用配方。 |
| S2 | Li et al., *DataComp-LM: In search of the next generation of training sets for language models*, arXiv `2406.11794v4`, revised 2025-04-21. | [官方 HTML v4](https://arxiv.org/html/2406.11794v4)：§3.2–3.5, Table 1（模型/训练 token 预算）；§4.2–4.6, Tables 3–6（抽取、过滤、去重和数据混合）；Appendix F（配方/超参）、N（人工标签）、U（datasheet 与 split）。 | **[精读原文]** 作为固定训练资源下数据策展对照；人工标签与下游效用不一致；下游任务被用于策展选择，Datasheet 没有推荐 corpus-level split，MMLU/HellaSwag 的污染检查为局部。 |
| S3 | Lee et al., *Deduplicating Training Data Makes Language Models Better*, arXiv `2107.06499v2`, revised 2022-03-24; ACL 2022. | [官方 HTML v2](https://arxiv.org/html/2107.06499v2)：§4.1.2（ExactSubstr）、§4.2（NearDup）、§5.2/Table 1（跨 split 去重）；§6.1–6.2, Figures 2/Table 4–5（PPL 与生成记忆）；§7（局限）；Appendix C/Table 13（训练配方和去重后样本/token 计数）。 | **[精读原文]** 去重降低文中定义的 50-token 生成记忆指标；PPL 不普遍受损。但作者明确不研究下游 benchmark 能力提升。结果限于 C4、英语和 T5 设置，记忆指标不代表所有隐私泄露。 |
| S4 | Xie et al., *DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining*, arXiv `2305.10429v3`, version dated 2023-10-24. | [官方 HTML v3](https://arxiv.org/html/2305.10429v3)：§2（reference-calibrated excess loss 与 Group DRO）；§3.1–3.2（The Pile/GLaM 实验与 8B 主模型结果）；§4（proxy/main scale 消融）；Appendix C（预处理、训练设置）。 | **[精读原文]** 用 proxy 相对 reference 的域级损失差得到混合权重。The Pile 上 280M proxy/reference 为 8B 主模型选权重；作者报告 five-task one-shot accuracy +6.5 pp、2.6×更少主模型 steps 达到基线。结论依赖域定义和英语任务集；权重会随 proxy 规模变化。未复现。 |
| S5 | Liu et al., *RegMix: Data Mixture as Regression for Language Model Pre-training*, arXiv `2407.01492v2`, version dated 2025-01-23. | [官方 HTML v2](https://arxiv.org/html/2407.01492v2)：§3–4（代理回归与 mixture-rank 预测）；§5.1–5.4、Table 4（候选混合、目标损失与任务比较）；Appendix B（限制）、E（训练配置）、I（rank invariance）、J（7B/100B-token 对比）、K（proxy 尺寸比较）。 | **[精读原文]** 17 个 Pile 子集、GPT-NeoX tokenizer；512 个 1M proxy mixtures、各 1B tokens，预测后用 1B/25B-token 主模型验证。Table 4 平均分 47.3 vs 人工配比 45.1；另报告 7B/100B-token 上 RegMix-vs-human 均分 56.5 vs 54.5。Pile-CC loss 因与多项任务相关性较强而被选作目标；mixture rank 的系统跨规模核验仅到 1B，7B 表只比较选定配比与人工基线。未复现。 |

## 审核口径

- FineWeb 的全局去重与单快照去重效果来自各自固定采样和 1.71B/训练 token 设置；图上差值不是精确表格数值。
- DataComp-LM 的固定训练预算比较仍使用作者的开发基准选择方案，不是独立盲测；数据集“质量”在这里指该下游效用协议下的结果。
- Deduplicating Training Data 的“记忆”是精确 50-token 子串匹配，不覆盖其他隐私泄露类型；论文没有下游能力结论。
- DoReMi 和 RegMix 都是语料域级配比研究，不是文档级过滤；前者目标为最坏域相对可学习性，后者预测 Pile-CC 验证损失。其任务、目标和模型规模不同，正文不直接横比绝对分数。
