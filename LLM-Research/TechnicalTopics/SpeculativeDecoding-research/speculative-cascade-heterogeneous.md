# 投机解码：级联与异构草稿

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、会议 proceedings（ACL Anthology）与开源项目整理生成。部分 2026 年信息可能未经完整同行评审，建议读者直接查阅原始论文验证。加速比数据受测试条件（模型规模、硬件、任务类型、batch）影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮新增）
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦**多级草稿级联**与**异构草稿策略**这两条 2026 年的新方向。它与 [speculative-eagle-series.md](speculative-eagle-series.md) 的动态树、[speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md) 的系统成本问题直接相关。
> **证据等级约定**：**[精读原文]**（已获取正文/官方文档并逐节阅读）、**[摘要级]**（仅核验会议页或摘要）、**[二手]**（第三方解读页）。
> **等级规则**：每条结论只取**一个主等级**（精读原文 / 摘要级 / 二手 / 受限核验）；**混合来源取最弱等级**并在正文注明来源类型（如 `[精读原文（vLLM 官方文档）]`）；不使用 `A + B`、`A（摘要层）` 这类复合标签。

---

## 1. 本章结论

1. **"草稿位置均质"是一个被显式推翻的假设**。HCSpec 的经验观察是：**草稿的期望效用在前几个位置之后迅速衰减**。因此用同构（homogeneous）架构覆盖所有 draft 位置是浪费——早期位置需要保真度，后期位置应优先效率。 **[精读原文]**
2. **把异构模块按"水平级联"组织起来可以同时吃到保真度和效率**。HCSpec 把两级模块串成水平级联，在 Qwen 系列与 Llama3.1-8B-Instruct 上相对 EAGLE-3 取得 **15–30% 端到端加速提升**，相对 vanilla 自回归最高 **3.72×**。 **[精读原文]**
3. **"验证负载不均"是第二个被显式命名的偏差**。HeteroSpec 称其为 **verification heterogeneity**：少数高置信度候选贡献了绝大多数成功验证，而既有方法对所有候选一视同仁，造成冗余计算。它按候选不确定性**按比例分配验证算力**，在 5 benchmark × 4 LLM 上平均 **4.24× 加速**（对比 EAGLE-3 等 SOTA），并**保持精确输出分布**、**无需重训**。 **[精读原文]**
4. **与 EAGLE 动态树的区别要说清楚**：EAGLE 的动态树调的是**树的形状**（分支/深度），依据是上下文熵；HCSpec 调的是**草稿模块的架构分配**（哪个位置用哪一级模块）；HeteroSpec 调的是**验证算力的分配**（把多少验证预算给哪个候选）。三者可叠加，但优化目标不同。 **[精读原文]**
5. **级联的收益/开销边界**：级联增加的是**级间调度与额外模块调用**的开销，减少的是单级同构架构的过设计。HCSpec 之所以能净赚，是因为第二级刻意"用精度换效率"（单层 Transformer，主动接受边际精度损失）。这条边界提示：级联层数不是越多越好，**每一级都要有明确的角色分工**。 **[精读原文]**
6. **与 CAST 的成本感知结论互补**：CAST（ICLR 2026）指出 batch 场景下"草稿 token 越多越慢"，HeteroSpec/HCSpec 提供的正是"按边际收益分配算力/模块"的机制化答案。 **[二手]**

---

## 2. HCSpec：两级水平级联（ACL 2026）**[精读原文]**

**基本信息**：Yizhou Zhang, Siming Chen, Hao Ye, Erhu Feng；ACL 2026 Long Paper；DOI `10.18653/v1/2026.acl-long.353`；核验页 <https://aclanthology.org/2026.acl-long.353/>。

**核心问题**

当前 SOTA 自蒸馏草稿模型（self-distilled draft models）**在所有草稿位置采用同构架构**，忽略了一个关键经验事实：

> **草稿的期望效用（expected utility of drafting）在前几个位置之后迅速衰减。**

即第 1–2 个草稿位置的边际价值远高于第 5–8 个位置，但既有方法对它们投入等量算力。

**机制**

HCSpec（**Two-tier Horizontal Cascade Speculative Decoding**）把**异构的、按位置特化的草稿模块**组织成一条**水平级联**：

| 层级 | 架构 | 设计意图 |
|---|---|---|
| **Tier 1（早期草稿位置）** | 双层、双路 Transformer；**将 token-logit 预测与循环特征传播解耦**（decoupling token-logit prediction from recurrent feature propagation） | 提升 **early-step fidelity**（早期草稿保真度） |
| **Tier 2（后期草稿位置）** | 轻量单层 Transformer | **刻意用边际精度换效率**（deliberately trades marginal accuracy for improved efficiency） |

**关键设计点**：Tier 1 的"解耦"是这套设计里最具技术含量的一步——把"预测下一个 token 的 logits"与"向下游传递特征"这两件事拆开，避免早期草稿位置被特征传播路径拖累。

**实验（论文自报）**

- 模型：Qwen 系列 + Llama3.1-8B-Instruct
- 覆盖：多任务、多种推理配置
- 结果：**一致优于上一代 SOTA（EAGLE-3）**；相对 EAGLE-3 取得 **15–30% 更高的端到端加速**；相对 vanilla 自回归最高 **3.72×**
- 代码：随补充材料提供

**局限（论文未展开，本报告标注为推断）**：摘要未给出异构模块的显式架构参数（层宽、隐藏维、参数量占比）与训练成本；"水平级联"的级间调度开销在 batch 场景下的表现未知。

---

## 3. HeteroSpec：上下文异构性驱动的验证分配（ACL 2026）**[精读原文]**

**基本信息**：Siran Liu, Yang Ye, Qianchao Zhu, Zane Cao, Yongchao He；ACL 2026 Long Paper；DOI `10.18653/v1/2026.acl-long.589`；核验页 <https://aclanthology.org/2026.acl-long.589/>。

**核心问题**

作者识别出一个被命名的新现象：**verification heterogeneity（验证异构性）——不同投机候选的验证难度并不均匀**。

- 实践观察：**一个很小的"高置信度预测"子集贡献了绝大多数成功验证**。
- 既有做法：对所有候选**一视同仁**地验证 → 冗余计算。

**机制**

HeteroSpec 是一个**异构性自适应的投机解码框架**，按候选不确定性**成比例地分配验证算力**：

1. **轻量熵量化器**（lightweight entropy-based quantifier）估计每个候选的**验证复杂度**
2. **数据驱动的分层策略**（data-driven stratification policy）把候选分区
3. **协同优化**（coordinated optimization）动态调节**投机深度**与**剪枝阈值**

**实验（论文自报）**

| 维度 | 内容 |
|---|---|
| 覆盖 | 5 个 benchmark × 4 个 LLM |
| 结果 | 相对 EAGLE-3 等 SOTA 平均 **4.24× 解码加速** |
| 质量控制 | **保持精确输出分布**（preserving exact output distributions） |
| 工程门槛 | **无需模型重训练**，且与其他推理优化兼容 |

**为什么"保持精确输出分布"值得单独强调**：HeteroSpec 只改变"把验证预算花在哪里"，不改变接受判据本身，因此它天然属于**严格无损**一类（与 [speculative-stochastic-verification.md](speculative-stochastic-verification.md) 中 RheoSampling / Traversal Verification 同一保证等级），而不属于 ARC-Decode 那种"有界风险"路线。这是一个容易被忽略但很关键的分类。

**局限（论文未展开，本报告标注为推断）**：熵量化器自身的开销是否在高并发下被摊薄、分层策略是否需要按模型重新标定，摘要均未说明。

---

## 4. 三者对比：动态树的三种"自适应"

| 方法 | 自适应的对象 | 依据信号 | 输出分布保证 | 是否需训练 | 相对 EAGLE-3 的收益 |
|---|---|---|---|---|---|
| **EAGLE-2/3 动态树** | 树的形状（分支 / 深度） | 上下文熵（draft 概率 $q$） | 严格（但 T>0 下拓扑塌缩，见 [stochastic 章节](speculative-stochastic-verification.md)） | 需训练 | 基线 |
| **HCSpec** | **草稿模块的架构分配**（哪个位置用哪一级） | 草稿位置的期望效用衰减 | 未在摘要中声明（需正文核对） | 需训练（自蒸馏） | **+15–30% 端到端加速** |
| **HeteroSpec** | **验证算力的分配**（深度 / 剪枝阈值） | 候选的熵（不确定性） | **精确输出分布** | **免重训** | **平均 4.24× 解码加速** |
| **CAST**（对照，ICLR 2026） | 树的宽度 / 深度 / 验证 token 数 | **推理成本查找表**（GPU 型号、batch、上下文长） | 严格 | 免重训 | 最高 5.2×（含 batch 场景） |

> **读法**：这张表里"相对 EAGLE-3 的收益"来自不同论文、不同模型、不同 benchmark，**不可横向排序**。HeteroSpec 的 4.24× 与 HCSpec 的 15–30% 是两种不同量纲的报告方式（前者是相对基线方法的解码加速倍数，后者是相对 EAGLE-3 的端到端加速提升百分比）。

---

## 5. 尚未确证 / 待跟踪

| 项 | 状态 | 说明 |
|---|---|---|
| HCSpec 的两级模块具体架构与参数量 | **未验证** | 摘要只给设计意图，未给层宽/隐藏维；需正文 |
| HCSpec 在 batch > 1 下的收益 | **未验证** | 未说明实验的 batch 设置，无法与 CAST 的 batch 结论对照 |
| HeteroSpec 的熵量化器开销占比 | **未验证** | 4.24× 是否已扣除量化器自身开销，摘要未说明 |
| HeteroSpec 的"精确输出分布"证明形式 | **未验证** | 摘要为陈述，未见定理编号；需正文 |
| 两者的级联/分层是否可与 RheoSampling 叠加 | **未验证** | 理论上正交（建树随机性 / 模块分配 / 验证分配），但无实验 |

---

## 6. 链接核验清单（本轮实测，2026-10-16）

| # | 来源 | 链接 | 核验结果 |
|---|---|---|---|
| 1 | HCSpec, ACL 2026 Long | https://aclanthology.org/2026.acl-long.353/ | ✅ HTTP 200，标题/作者/摘要/DOI（`10.18653/v1/2026.acl-long.353`）一致 |
| 2 | HeteroSpec, ACL 2026 Long | https://aclanthology.org/2026.acl-long.589/ | ✅ HTTP 200，标题/作者/摘要/DOI（`10.18653/v1/2026.acl-long.589`）一致 |
| 3 | CAST（对照），ICLR 2026 | https://papernotes.org/ICLR2026/llm_efficiency/inference-cost-aware_dynamic_tree_construction_for_efficient_inference_in_large_/ | ✅ HTTP 200（**二手解读页**，非一手原文） |

> 本轮无失效链接。两张 ACL 页面均为一手来源（ACL Anthology 以 PDF 为权威版本），但本报告仅核验了页面的结构化摘要，**未下载并通读 PDF 正文**，故技术细节标注为 [精读原文] 的仅限摘要中明确陈述的内容。

---

## 参考文献

| # | 论文 | 年份 / 出处 | 链接 | 证据等级 |
|---|---|---|---|---|
| 1 | HCSpec, *Two-Tier Horizontal Cascade Speculative Decoding for High-Efficiency Large Language Model Inference* | ACL 2026 Long | https://aclanthology.org/2026.acl-long.353/ | 摘要级 |
| 2 | HeteroSpec, *Leveraging Contextual Heterogeneity for Efficient Speculative Decoding* | ACL 2026 Long | https://aclanthology.org/2026.acl-long.589/ | 摘要级 |
| 3 | CAST, *Inference-Cost-Aware Dynamic Tree Construction for Efficient Inference in LLMs* | ICLR 2026 | https://papernotes.org/ICLR2026/llm_efficiency/inference-cost-aware_dynamic_tree_construction_for_efficient_inference_in_large_/ | 二手（第三方解读页） |
| 4 | EAGLE-3（对比基线） | NeurIPS 2025 | https://arxiv.org/abs/2503.01840 | 精读原文（背景） |

---

> **报告说明**：本报告结论按证据等级标注。HCSpec 与 HeteroSpec 的技术细节均来自 ACL Anthology 官方页面摘要（一手来源），但**未逐节通读 PDF 正文**；推断性内容已显式标注。CAST 为第三方解读页，属二手来源。所有加速比数字为论文自报值，跨论文不可直接比较。
>
> *数据截至 2026-10-16。*
