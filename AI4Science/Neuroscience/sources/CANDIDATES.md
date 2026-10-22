# Candidate screening

筛选问题：哪些原始研究能解释侵入式皮层脉冲活动到运动行为解码时的跨会话 token、预训练收益、泛化轴与标签泄漏？候选池 10 项；3 项进入主报告。本文按“研究问题匹配与可核验的对照”选文，不因 foundation-model 名称单独入选。

## 入选

| Work | Decision | Reason |
| :-- | :-- | :-- |
| NDT2, NeurIPS 2023, DOI `10.52202/075280-3523` | 主文精读 | 多上下文自监督脉冲建模的基线；区分跨会话、跨受试者、跨任务数据的来源价值，并报告小样本/实时控制证据及其在线限制。原文 §3–4、Fig. 2–5。 |
| A Generalist Intracortical Motor Decoder (NDT3), NeurIPS 2025 | 主文精读 | 配对神经—行为数据的尺度研究；不仅报告 8 个任务的收益，也主动量化通道结构敏感性、数据规模收益饱和和 held-out behavior/angular extrapolation 失败。原文 §§2–3、Fig. 2–5。 |
| TWS, arXiv `2610.03001v1` | 主文精读 | 直接把“可迁移 token 是什么”作为机制问题，提供 identity-free 群体状态编码、跨数据集线性 probe、任务边界/事件时间对照及信息保留分析。其 IBL movement 主分数受边界标签泄漏影响，报告中明确降格解释；新预印本尚待独立复现。 |

## 暂缓 / 排除

| Work | Decision | Reason |
| :-- | :-- | :-- |
| POYO, “A unified, scalable framework for neural population decoding,” NeurIPS 2023 | 不独立展开；作基线 | 是 NDT/TWS 比较中的重要按神经元建模方案。此处用它呈现 per-neuron token 跨新会话的限制，不重复写完整方法专题。 |
| SPINT, arXiv `2507.08402v1` | 暂缓 | 以空间置换不变读入处理跨会话 unit order，是与 TWS 直接相关的结构化基线；本轮优先核查固定论文的 held-out 数据、未见 unit 处理与结果，不足以在未读完其协议前综合其优势。 |
| NEDS, “Neural Encoding and Decoding at Scale,” arXiv `2504.08201` / ICLR 2026 | 主报告作为 TWS 的 IBL per-session baseline | 面向大规模神经编码/解码，与跨会话问题相关；本轮只按 TWS 的引用定位核对其基线角色，不将未逐篇核验的 NEDS 全文结果作为独立主张。 |
| Population Transformer, arXiv `2406.03044` / ICLR 2025 | 排除本条目 | 关注稀疏且不均匀的多通道 population-level aggregation，任务/预训练 embedding 来源更宽；可作为神经模态通用读入器专题候选，不是本轮三篇固定路线必要证据。 |
| BEAST, arXiv `2507.09513` | 排除本条目 | 主输入为视频行为而非神经脉冲到行为的映射，论文把神经编码列作相关应用；模态与核心问题不同。 |
| Foundation model of neural activity predicts response to new stimulus types, DOI `10.1038/s41586-025-08829-y` | 排除本条目 | 属视觉刺激到小鼠神经反应预测，不是运动行为解码；可形成独立的 sensory encoding / 神经响应预测方向。 |
| CEBRA, Nature 2023, DOI `10.1038/s41586-023-06031-6` | 作比较背景，不列核心证据 | 强调行为监督/无监督潜空间与神经—行为关系。TWS 对它报告“每会话单独拟合”等基线结果，但本轮不扩展成潜空间方法综述。 |

## 检索与筛选轨迹

- 先用 `researcher deep` 确认窄范围：侵入式 motor cortex electrophysiology，神经活动到运动行为解码，held-out 会话/个体迁移；不覆盖其他测量模态。
- 用 PaperFetcher 查询“neural activity behavior foundation model neural population behavior decoding cross-session”以及 NDT2/NDT3 题名。通用复合查询的 arXiv 返回无关结果、Semantic Scholar/OpenAlex 被限流；随后拆分为 NDT2 与 generalist intracortical motor decoder 的题名/主题检索，并用 Crossref、PubMed、arXiv 定位论文标识。
- 以原始论文为准筛选；主文结果均定位至章节、图表或 appendix。仅从候选页面/引文看到的工作不被扩写成已精读结论。
- 许可证和原文版本按 manifest 固定记录。arXiv HTML v1 是 TWS 唯一被核读版本；后续版本可能改变结果。
