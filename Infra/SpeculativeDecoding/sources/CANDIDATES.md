# 选文说明与候选池 · SpeculativeDecoding

> 目的：**先筛选、后精读**。把“为什么选这 8 篇、为什么没选其它”写清楚，以后不必重复筛。
> 证据纪律：本页只做**选文判断**，不含未核实的论文结论。**带 ID 的排除项均已回查 arXiv 元数据**；未核实的按类别排除，**不编号、不编造 ID**。

## 1. 本条目要回答什么（决定选文标准）

本条目关心的不是“所有能加速解码的方法”，而是**“用低成本草稿 + target 并行验证，且输出分布可证等价（或明示有界风险）”**这条线。据此分三问：

- **(a) 草稿从哪来？**（独立模型 / target 自身 / 检索或轨迹 / 块扩散）
- **(b) 验证怎么保分布？**（严格等价 / 序列级 / 有界风险）
- **(c) 在什么系统条件下划算？**（batch、序列长度、硬件、温度）

**入选门槛（满足其一）**：提出新机制或新范式 ｜ 首次在某能力上成立且有规模证据 ｜ 成为后续基线 ｜ 证伪/纠正已有共识。
**淘汰标准（命中其一）**：增量调参无新机制 ｜ 只在玩具设置验证或无消融 ｜ 已被后续取代 ｜ 与本条目主题仅擦边 ｜ 拿不到正文。

## 2. 入选（8 篇，逐篇一句理由）

| 分册 | 入选理由（一句话） |
| :-- | :-- |
| [EAGLE 系列](../papers/2401.15077-eagle-series.md) | 工业默认；EAGLE-1/2/3 把“特征级 → 动态树 → TTT/多层融合”这条自投机主线讲全，且有 SGLang 生产 batch 曲线。 |
| [Medusa](../papers/2401.10774-medusa.md) | 并行头代表；typical acceptance 是“有界风险”的早期样本，正好与严格无损形成对照。 |
| [Lookahead](../papers/2402.02057-lookahead.md) | 免训练代表；明确论证“贪心草稿 = one-hot 提议仍无损”，是理解 `qx=1.0` 的关键背景。 |
| [SpecInfer](../papers/2305.09781-specinfer.md) | 树验证系统源头；多 SSM、树宽、batch 依赖，是后续所有树验证的公共祖先。 |
| [MagicDec](../papers/2408.11049-magicdec.md) | 系统条件代表；用“临界序列长度”把“大 batch 不适合投机”证伪一半，补上 batch×序列的第三维。 |
| [RheoSampling](../papers/2609.21827-rheosampling.md) | T>0 动态树的无损修复；本轮“转折点”的核心证据，且明确给出接受率 = `Σ min(p,q)`。 |
| [vLLM 实现核验](../papers/vllm-implementation.md) | 生产框架一手代码；`greedy` vs `probabilistic` 的语义分叉，是“论文 q 如何落地”的最佳样本。 |
| [SGLang 实现核验](../papers/sglang-implementation.md) | 生产框架一手代码；#10308 的处置对象，能同时回答“issue 状态”与“代码能力”。 |

## 3. 排除清单（14 条：4 条带已核实 ID + 10 条类别性排除）

### 3.1 带已核实 ID 的排除（4 条）

> 下列论文**本轮未精读**。理由仅为**选文判断**（主题分布、代际关系、与本条目判据的关系），**不构成对其质量的评价**。标题/作者/版本取自本轮 arXiv API 回查。

| # | arXiv ID | 论文（arXiv 标题，版本/日期） | 排除理由（一句话） |
| --: | :-- | :-- | :-- |
| 1 | `2310.08461` | DistillSpec: Improving Speculative Decoding via Knowledge Distillation（v2，2024-03-31，Zhou, Yongchao） | 训练目标线的早期基线；其结论已被 AdaSPEC/HASS/EAGLE-3 的训练章节覆盖，单设分册会重复。 |
| 2 | `2402.12374` | Sequoia: Scalable, Robust, and Hardware-aware Speculative Decoding（v3，2025-07-05，Chen, Zhuoming） | 硬件感知树优化；与 SpecInfer（树宽）、MagicDec（硬件条件）在系统轴上重叠，本轮优先保留后两者。 |
| 3 | `2408.15766` | Learning Harmonized Representations for Speculative Sampling（HASS；v3，2025-02-26，Zhang, Lefan） | EAGLE-3 论文已直接对照 HASS 并说明差异（HASS 保留特征预测损失）；单设分册会与 EAGLE 分册重复。 |
| 4 | `2403.00835` | CLLMs: Consistency Large Language Models（v4，2024-06-13，Kou, Siqi） | **不是投机解码**（一致性模型的并行解码）；同时用作“素材层 EAGLE ID 误写”的更正样本，故只登记不设册。 |

### 3.2 类别性排除（10 条，**未逐一核实 ID，故不给 ID**）

| # | 类别 | 排除理由（一句话） |
| --: | :-- | :-- |
| 5 | **块/扩散草稿**：DFlash、DSpark、BASTION 等（2026 预印本/工程博客） | 正文细节与复现条件不够稳定；本轮只做谱系定位，数字不入表，列为**下一轮首选**。 |
| 6 | **自投机子型**：Hydra、SWIFT、CLaSp、LayerSkip 等 | 机制已被 Medusa（并行头）与 EAGLE（特征级）覆盖；作为素材层保留，不重复设册。 |
| 7 | **系统优化**：TriForce、Mirror-SD 等 | 与 MagicDec（长上下文/大 batch）和 SpecInfer（树验证）在系统轴上重叠；本轮优先保留可核验正文的两篇。 |
| 8 | **量化/分层交叉**：QSpec、HiSpec 等 | 更适合归 `Infra/QuantizationEdge`；本条目只在谱系里提一句。 |
| 9 | **多模态投机**：ViSpec、SpecVLM、MSD、SpecPrune-VLA 等 | 素材层已有横切文档；本轮篇幅优先给“验证 + 系统”两条主线。 |
| 10 | **领域/语种特化**：DictSpec、CDSL 等 | 属于“检索式/受限输出”的补充；已在素材层保留，本轮不设册。 |
| 11 | **端侧/专用硅**：SMoLPU、SS-MoE、FlexSpec 等 | 指标口径不同（µJ/token、能效 vs tokens/s），无法与算法论文同表；素材层保留。 |
| 12 | **草稿训练新法**：AdaSPEC、Attention Drift、TLT 等 | 与 EAGLE-3 的训练/上下文对齐线交叉；本轮以 EAGLE 分册 + 素材层覆盖。 |
| 13 | **检索式**：REST、PLD、SAM 等 | 机制已被 Lookahead 的“免训练”轴代表；检索式作为其子型在 topic 1 提。 |
| 14 | **经典背景**：Leviathan / Chen（2023） | 范式源头，已在 topic 2 作为数学基础引用；不单设分册（无“新机制”可拆）。 |

## 4. 统计口径（可逐条核对）

| 项 | 数 | 说明 |
| :-- | --: | :-- |
| 候选池 N | **22** | 4 条带 ID 的排除 + 10 条类别排除 + 8 条入选 |
| 入选 M | **8** | 6 篇论文分册（覆盖 8 篇论文）+ 2 篇代码核验 |
| 排除 | **14** | 4 带 ID + 10 类别 |
| 其中本轮重新核 ID | **4** | `2310.08461` / `2402.12374` / `2408.15766` / `2403.00835` |
| 未设分册但进谱系 | 3+ | DFlash / DSpark / BASTION（只定位，不入表） |

**ID 纪律**：3.1 的 4 个 ID 与标题/版本/日期**已逐条回查 arXiv**；3.2 是类别性排除，**不编号、不编造 ID**。DFlash 等如需引用，请回素材层并自行回查。

## 5. 下一轮候选（按价值排序）

1. **DFlash / DSpark / BASTION**：块扩散/预算感知，2026 主线；需要正文与可复现条件。
2. **Traversal Verification**（NeurIPS 2025）：与 RheoSampling 正交的验证遍历改进，值得单独设册。
3. **CAST**（ICLR 2026）：成本感知建树；目前只有二手解读页，需一手正文。
4. **HCSpec / HeteroSpec**（ACL 2026）：级联/异构验证预算；需通读 PDF。
5. **多模态/VLA 投机**：素材层线索多，但正文质量参差；先筛再读。

## 6. 与 `papers/` 的对应

- 入选 8 篇各有独立分册；每篇开头含「亮点与差异」四行，正文展开七问。
- 本页与 [MANIFEST.md](MANIFEST.md) 配套：**清单入库、全文不入库**；代码只记 `仓库@commit:文件:行`。
- 与 `report.md` §9 一致：report 的“选文说明”是摘要，本页是完整清单。
