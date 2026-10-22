# MathematicalDiscovery candidate screen

**筛选范围**：定向选读“机器提出数学/算法候选后，验证器能检查什么？”没有做穷尽式论文计数，也不把 PaperFetcher 搜索结果数量当候选池规模。筛选以原始论文/官方记录可读、机制与证据边界可定位为准。

| 处理 | 候选 | 选择理由 / 暂缓理由 |
| :-- | :-- | :-- |
| 入选 | AlphaProof, “Olympiad-level formal mathematical reasoning with reinforcement learning” (Nature 2026) | Lean kernel 检查形式证明项，提供 formal proof route；IMO 的题目翻译、答案候选和 AlphaGeometry 2 贡献可在原文逐项拆分。 |
| 入选 | FunSearch, “Mathematical discoveries from program search with large language models” (Nature 2024) | 组合对象构造与在线启发式共用程序搜索机制，但校验强度不同：前者可推出下界，后者为基准实测。 |
| 入选 | “Generative Modeling for Mathematical Discovery” (arXiv 2503.11061v2, 2025) | 不是新记录论文，而是适合与原 FunSearch 对照的复现/污染/跨任务诊断，能说明重复运行的重要性。 |
| 入选 | AI Feynman, “A Physics-Inspired Method for Symbolic Regression” (Science Advances 2020; arXiv v2) | 以已知解析式为目标恢复方程，适合展示符号回归离“新物理定律发现”还有哪些证据门槛。 |
| 暂缓 | AlphaDev, “Faster sorting algorithms discovered using deep reinforcement learning” (Nature 2023) | 低层指令搜索和排序算法验证有研究价值，但与本专题的 evaluator/program-search 路线重叠；硬件延迟和 libc++ 集成更适合另设算法优化精读。 |
| 暂缓 | AlphaGeometry 2 | 本专题用 AlphaProof 的正式证明路线作主例；该专用几何系统在组合 IMO 成绩中单独标识，但不展开其合成数据、符号演绎和几何搜索细节，避免扩成另一个系统专题。 |

## PaperFetcher 使用记录

- 按专题运行 PaperFetcher arXiv 定向检索；检索结果是搜索入口，不视为覆盖性综述。
- `fetch 2503.11061` 与 `fetch 1905.11481` 返回匹配元数据；AlphaProof Nature DOI 与 FunSearch Nature DOI 均无法由 PaperFetcher 转为 arXiv 记录，因此固定到期刊官网 DOI、Nature HTML/补充材料核对。
- FunSearch 原文 DOI 的 exact-title arXiv 搜索无命中，Crossref 返回与 Nature DOI 一致的期刊记录；探索时试到的 `2311.08660` 实际是无关代数几何论文，故未列作候选或引用。
