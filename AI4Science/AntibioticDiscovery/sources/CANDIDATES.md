# 候选筛选记录

核查截止：2026-10-23（Asia/Shanghai）。这是为 AI4Science 图书馆小分子抗生素发现专题所做的**定向检索与证据筛选**，不是覆盖所有抗菌药 AI 论文的系统综述；未预设或声称固定候选池总数。检索经 PaperFetcher 的 arXiv/Crossref/PubMed 查询与网页搜索，再回到出版商、PubMed/PMC 和作者/机构托管的论文版本核对。PaperFetcher 的 DOI `fetch` 返回不支持错误，OpenAlex/Semantic Scholar 在定向检索中返回 HTTP 429；不以检索 API 返回与否代替纳入/排除判据。

## 入选

| 工作 | 入选理由 |
| :-- | :-- |
| [Abaucin / Deep learning-guided discovery](https://doi.org/10.1038/s41589-023-01349-8) (2023) | 代表监督学习从已测表型中优先选择小分子；有独立候选验证、抗菌谱、遗传机制线索和动物模型。 |
| [SyntheMol](https://doi.org/10.1038/s42256-024-00809-7) (2024) | 代表把化学反应/可采购 building blocks 纳入生成机制，并实际合成 58 个分子；外膜通透化剂条件是重要实验边界。 |
| [Krishnan et al., de novo antibiotic design](https://doi.org/10.1016/j.cell.2025.07.033) (2025) | 方法与实验证据跨越片段筛选、片段扩展、无片段生成；两种 lead 有不同机制线索和局部感染小鼠模型。 |
| [SyntheMol-RL](https://doi.org/10.1038/s44320-026-00206-9) (2026) | 同一研究中对 RL、MCTS、虚拟筛选与随机化学品做较完整对照；新增多属性优化及一个前瞻合成到动物模型的实例。 |
| [Abaucin LolDF mechanism and CRAB follow-up](https://doi.org/10.1038/s41467-026-75428-4) (2026) | 作为机制跟进而非 AI 方法论文入选：提供 abaucin-LolDF 结构/转运功能证据，且扩展到临床 CRAB 分离株和小鼠肺炎模型。 |

## 排除或暂缓

| 候选/类别 | 理由 |
| :-- | :-- |
| [APEX: Deep-learning-enabled antibiotic discovery through molecular de-extinction](https://doi.org/10.1038/s41551-024-01201-x) (2024)；2026 peptide AMP generation/optimization papers | AI 设计对象是抗菌肽序列，不是小分子化合物；与本专题范围不符，适合未来做独立抗菌肽专题。 |
| [ApexOracle](https://arxiv.org/abs/2507.07862) (2025) | 预测并生成针对未见病原体的候选，检索到的固定版本以计算预测/生成主张为主；本轮未发现可核查的前瞻合成、体外和动物验证，所以不作为核心经验型证据。可后续跟进版本/补充实验。 |
| [AI-guided Antibiotic Discovery Pipeline from Target Selection to Compound Identification](https://arxiv.org/abs/2504.11091) (2025) | 初步检索命中的是结构感知生成器评估与候选可用性分析；本轮未核实新的小分子实测命中或机制/动物实验，低于本专题以实验闭环为主的核心纳入门槛。 |
| [Pre-trained molecular representations enable antimicrobial discovery](https://doi.org/10.1038/s41467-025-58804-4) (2025) | 小分子表征与筛选工作值得后续补充，但它回答的是跨物种活性预测/已有分子筛选，与本条目中“筛选→合成设计→机制/动物模型”主线增量较有限；未在本轮逐篇深读，暂留候选池而非判为低质量。 |

暂缓仅表示本轮没有进入精读分册，不构成对研究质量或方向价值的否定。抗菌肽与跨物种预测/基础表征可分别另建专题。
