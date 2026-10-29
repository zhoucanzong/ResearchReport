# 选文说明与候选池 · SpeculativeDecoding

> 目的：**先筛选、后精读**。记录哪些工作因新增机制进入当前主线、哪些因重叠或证据不足仍作候选；覆盖项和版本以当前 `report.md`、`papers/` 与 `MANIFEST.md` 为准。本清单不以条目数衡量研究深度。
> 证据纪律：本页只做**选文判断**，不含未核实的论文结论。**带 ID 的排除项均已回查 arXiv 元数据**；未核实的按类别排除，**不编号、不编造 ID**。

## 1. 本条目要回答什么（决定选文标准）

本条目关心的不是“所有能加速解码的方法”，而是**“用低成本草稿 + target 并行验证，且输出分布可证等价（或明示有界风险）”**这条线。据此分三问：

- **(a) 草稿从哪来？**（独立模型 / target 自身 / 检索或轨迹 / 块扩散）
- **(b) 验证怎么保分布？**（严格等价 / 序列级 / 有界风险）
- **(c) 在什么系统条件下划算？**（batch、序列长度、硬件、温度）

**入选门槛（满足其一）**：提出新机制或新范式 ｜ 首次在某能力上成立且有规模证据 ｜ 成为后续基线 ｜ 证伪/纠正已有共识。
**淘汰标准（命中其一）**：增量调参无新机制 ｜ 只在玩具设置验证或无消融 ｜ 已被后续取代 ｜ 与本条目主题仅擦边 ｜ 拿不到正文。

## 2. 已纳入当前学习路线

| 分册 | 入选理由（一句话） |
| :-- | :-- |
| [EAGLE 系列](../papers/2401.15077-eagle-series.md) | 工业默认；EAGLE-1/2/3 把“特征级 → 动态树 → TTT/多层融合”这条自投机主线讲全，且有 SGLang 生产 batch 曲线。 |
| [Medusa](../papers/2401.10774-medusa.md) | 并行头代表；typical acceptance 是“有界风险”的早期样本，正好与严格无损形成对照。 |
| [Lookahead](../papers/2402.02057-lookahead.md) | 免训练代表；明确论证“贪心草稿 = one-hot 提议仍无损”，是理解 `qx=1.0` 的关键背景。 |
| [SpecInfer](../papers/2305.09781-specinfer.md) | 树验证系统源头；多 SSM、树宽、batch 依赖，是后续所有树验证的公共祖先。 |
| [MagicDec](../papers/2408.11049-magicdec.md) | 系统条件代表；用“临界序列长度”把“大 batch 不适合投机”证伪一半，补上 batch×序列的第三维。 |
| [RheoSampling](../papers/2609.21827-rheosampling.md) | T>0 动态树的无损修复；本轮“转折点”的核心证据，且明确给出接受率 = `Σ min(p,q)`。 |
| [SecureSD](../papers/2610.08678-secure-sd.md) | 2026-10 新增安全维度：测量有损验证下 jailbreak/prompt-injection 相对 utility 的退化，并提出按位置校正；arXiv 元数据称已收 IEEE S&P 2027。 |
| [DARTree](../papers/2608.13524-dartree.md) | 把扩散块草稿的校正从一条链扩展到多条条件分支，并用分层并行扩展 + 延迟 top-B 替代逐节点 heap；代码可固定，适合解释 2026 diffusion draft 的树化。 |
| [DFlash](../papers/2602.06036-dflash.md) | 用 target KV 条件化块扩散 draft，建立“扩散并行提议、AR target 验收”的主线。 |
| [DFlare](../papers/2606.02091-dflare.md) | 为每个 draft layer 学不同的 target feature 融合权重，研究草稿容量扩大的收益与训练成本。 |
| [DDTree](../papers/2604.12989-ddtree.md) | 将单次块扩散的逐位置候选组织成树，并按 draft surrogate 目标配置 target 验证预算。 |
| [PRESTO](../papers/2607.22634-presto.md) | 揭示扩散边际分数与 AR 前缀验证的错位，用轻量 prefix signal 改善树排序。 |
| [Spiffy](../papers/2509.18085-spiffy.md) | 对 standalone dLLM 自己的未来 block state 做图式投机，并证明保留该 dLLM 的输出分布。 |
| [PoE-Bridge](../papers/2606.08048-poe-bridge.md) | 以中间分布缩小 DLM proposal 与 AR target 的差异；明示有限候选下非严格无损。 |
| [SpecStream](../papers/2609.33184-specstream.md) | 代表 serving 系统线：围绕已提交 KV、流式 full-attention、按 useful output 调 q 和共卡调度设计，且论文明确展示 PCIe offload 的速度边界。 |
| [DLite](../papers/2610.23787-dlite.md) | 10 月最新的 agentic drafter 工作：把 target hidden states 当上下文，删除的是 draft 历史 KV/重复历史编码；有论文与官方推理代码可相互核对。 |
| [HSD](../papers/2601.05724-hsd.md) | 用分层概率质量平衡扩展严格无损的序列级验证；同时区分正确性保证与 verifier 实现开销。 |
| [Delayed Tree Expansion](../papers/2602.16994-delayed-tree.md) | 配平 verifier 基线后再改变树分叉时机；保留跨模型比较中的负向子项，并披露 selector 的离线训练成本。 |
| [CaDDTree](../papers/2606.01813-caddtree.md) | 把接受长度优化改为每轮吞吐目标，解释固定候选预算怎样忽略 target 验证成本；停止保证依赖成本曲线条件。 |
| [TLAR](../papers/2610.07350-tlar.md) | 对生成历史检索做来源对照、SmallDraft 边际增量与验证反馈调度，同时报告长短输出的端到端收益差异。 |
| [EAGLE-4](../papers/eagle4-one-flexible-drafter.md) | 将实测 draft/verify 成本与硬件、并发条件一起用于在线调整树的深度和宽度；收益因此是配置属性而非家族常数。 |
| [Sequoia](../papers/2402.12374-sequoia.md) | 在树验证基础上加入节点预算动态规划、不放回验证与硬件成本树优化；补树形和运行成本的共同选择。 |
| [Traversal Verification](../papers/2505.12398-traversal-verification.md) | 以叶到根遍历和序列级路径接受为 verifier 设计，补树遍历顺序与严格无损保证的分工。 |
| [Approximate Speculative Decoding](../papers/2608.03447-approximate-sd.md) | 对 greedy verifier 的 mismatch 设置 regret 门、块内上限和请求级预算；明确作为近似路线而非无损方法。 |
| [VSD](../papers/2602.05774-vsd.md) | 把草稿训练从 token likelihood 扩到 path-level acceptance utility，并用变分优化与 EM 近似训练。 |
| [Component-Aware Self-Speculation](../papers/2605.01106-component-aware-self-spec.md) | 用 hybrid target 的 SSM/linear-attention 子图当内部 draft，展示模块并/串关系如何改变候选可用性。 |
| [AdaSPEC](../papers/2510.19779-adaspec.md) | 按拟合难度选择蒸馏 token，解释容量受限时“全 token KL”与接受收益的错位。 |
| [Attention Drift](../papers/2605.09992-attention-drift.md) | 从表示和注意力漂移分析草稿链深度为何影响上下文跟随，并测试归一化修补。 |
| [TLT / Adaptive Drafter](../papers/2511.16665-tlt-adaptive-drafter.md) | 在 RL rollout 长尾空档在线更新 draft，把草稿训练时机与 rollout 调度结合。 |
| [Acceptance-Aware Training](../papers/2609.24150-acceptance-aware-training.md) | 分别以 EAL/WTV 直接优化 greedy 与 sampling 的固定窗口接受长度。 |
| [EDR](../papers/2610.10411-expected-decoding-rounds.md) | 用状态访问概率直接优化全序列期望验证轮数，区别于 window-local 接受目标。 |
| [SpecLA](../papers/2607.16673-specla.md) | 面向 linear-attention target 设计树验证 kernel 和接受状态恢复，补递归状态的执行问题。 |
| [vLLM 实现核验](../papers/vllm-implementation.md) | 生产框架一手代码；`greedy` vs `probabilistic` 的语义分叉，是“论文 q 如何落地”的最佳样本。 |
| [SGLang 实现核验](../papers/sglang-implementation.md) | 生产框架一手代码；#10308 的处置对象，能同时回答“issue 状态”与“代码能力”。 |

## 3. 排除清单

### 3.1 带已核实 ID 的排除（3 条）

> 下列论文**本轮未精读**。理由仅为**选文判断**（主题分布、代际关系、与本条目判据的关系），**不构成对其质量的评价**。标题/作者/版本取自本轮 arXiv API 回查。

| # | arXiv ID | 论文（arXiv 标题，版本/日期） | 排除理由（一句话） |
| --: | :-- | :-- | :-- |
| 1 | `2310.08461` | DistillSpec: Improving Speculative Decoding via Knowledge Distillation（v2，2024-03-31，Zhou, Yongchao） | 训练目标线的早期基线；当前路线已有 EAGLE 系列、AdaSPEC、VSD、AAT、EDR 等不同角度的训练目标，单设分册需有新的比较结论。 |
| 2 | `2408.15766` | Learning Harmonized Representations for Speculative Sampling（HASS；v3，2025-02-26，Zhang, Lefan） | EAGLE-3 论文已直接对照 HASS 并说明差异（HASS 保留特征预测损失）；单设分册会与 EAGLE 分册重复。 |
| 3 | `2403.00835` | CLLMs: Consistency Large Language Models（v4，2024-06-13，Kou, Siqi） | **不是投机解码**（一致性模型的并行解码）；同时用作“素材层 EAGLE ID 误写”的更正样本，故只登记不设册。 |

### 3.2 类别性排除（8 项，**未逐一核实 ID，故不给 ID**）

| # | 类别 | 排除理由（一句话） |
| --: | :-- | :-- |
| 4 | **自投机子型**：Hydra、SWIFT、CLaSp、LayerSkip 等 | 现有 Medusa/EAGLE 与草稿侧专题已经建立并行头、特征级和层跳过阅读路线；单篇优先级低于这些路径之间的统一控制比较。 |
| 5 | **系统优化**：TriForce、Mirror-SD 等 | SpecStream 已补 KV offload / streaming / co-execution；其它系统仍需固定实现和同条件对照，避免与现有长上下文/服务材料重复。 |
| 6 | **量化/分层交叉**：QSpec、HiSpec 等 | 更适合归 `Infra/QuantizationEdge`；本条目只在谱系里提一句。 |
| 7 | **多模态/VLA 投机**：ViSpec、SpecVLM、MSD、SpecPrune-VLA 等 | 素材层已有线索，但需先区分目标模型、输出结构和正确性定义，再选代表作精读。 |
| 8 | **领域/语种、检索与端侧特化**：DictSpec、CDSL、REST、PLD、SAM、SMoLPU、SS-MoE、FlexSpec 等 | 属于扩展路线；若没有新的控制实验或明确使用场景，不再堆模型/应用名单。 |

## 4. 选文边界

精读入口按研究机制而不是发布数量扩展；类别性排除表示目前不单独拆册，不等于该方向不重要。ID、标题、版本和原文定位以 [MANIFEST](MANIFEST.md) 与各分册为准。扩散交叉、代码来源和其他不适合单篇精读的线索继续按主题关联，不拿候选数量或篇幅衡量覆盖深度。

## 5. 下一轮候选（按价值排序）

1. **DLite 的迁移边界**：扩展到其它 target 家族/尺寸，并检查 LiteSpec 完整训练栈、实际模型权重和输出等价性。
2. **SpecStream 源码/互联扩展**：找到作者实现固定 SHA，审计 SGLang 内核与 PCIe/NVLink/更大并发下的 trade-off。
3. **CAST 同名工作消歧**：先核对不同 arXiv ID、版本和机制，再决定是否值得单独精读，避免把硬件动态建树和 block-draft 树构造混为一篇。
4. **HCSpec / HeteroSpec**（ACL 2026）：级联/异构验证预算；需通读 PDF。
5. **多模态/VLA 投机**：素材层线索多，但正文质量参差；先筛 target、候选/接受定义与安全边界再读。
6. **Bole**（arXiv 2608.01651）：公开摘要涉及 hybrid-attention tree kernels，但当前 v1 稿件带“Confidential Draft / Do NOT Distribute”水印且 SGLang 链接快照未发现对应实现；在有清晰公开版本前只保留候选级别，不以摘要升级深度结论。

## 6. 与 `papers/` 的对应

- 代表性论文按各自研究问题设置独立精读；结构不要求固定模板，需让读者看清机制、作者证据、设计边界及与相邻工作的关系。
- 本页与 [MANIFEST.md](MANIFEST.md) 配套：**清单入库、全文不入库**；代码只记 `仓库@commit:文件:行`。
- 与 `report.md` 的推荐路线配合使用：本页记录选文判断，MANIFEST 记录固定版本和原文位置，`papers/` 分册负责深入解释。
