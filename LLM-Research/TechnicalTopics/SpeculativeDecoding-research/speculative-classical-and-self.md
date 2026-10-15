# 投机解码：经典方法与自投机

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、会议 proceedings、arXiv 预印本与开源项目整理生成。部分信息可能未经同行评审，建议读者直接查阅原始论文验证。arXiv 预印本论文中的加速比数据受测试条件（模型规模、硬件、任务类型）影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮更新；v1 为 2026 年 6 月）
> **本次改动**：新增 §3.2.5「2025 年自投机新解法：SWIFT 与 CLaSp」；**修复 v1 中 Hydra 的错误链接**；新增 §3.2.6「回指：自投机与随机采样验证的关系」；新增「证据等级」列。
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦经典独立模型 draft 与自投机方法。主报告见 [report.md](report.md)；验证正确性的新章节见 [speculative-stochastic-verification.md](speculative-stochastic-verification.md)。
> **证据等级约定**：**[精读原文]**、**[摘要级]**、**[二手]**。

---

## 3.1 经典方法（2023）

### 3.1.1 Leviathan et al. (ICML 2023) / Chen et al. (2023) **[背景：已核验链接]**

2023 年，Google Research 的 **Leviathan et al.**（ICML 2023）和 DeepMind 的 **Chen et al.**（同期独立工作）几乎同时提出了投机解码的核心范式：

- **Leviathan et al.**：*Fast Inference from Transformers via Speculative Decoding*（ICML 2023）
  - 使用独立训练的小 Transformer 作为 draft model
  - 在 T5-XXL (11B) 上实现 **2-3× 加速**，draft 模型为 T5-small (60M)
  - 关键发现：draft 模型只需与 target 模型"同系列"（相同 tokenizer、相似训练数据），无需严格对齐

- **Chen et al.**：*Accelerating Large Language Model Decoding with Speculative Sampling*（2023）
  - 同样采用 draft-then-verify 框架
  - 强调接受-拒绝采样的数学正确性证明
  - 在 Chinchilla 系列模型上验证加速效果

**共同瓶颈**：
1. **分布失配（Distribution Mismatch）**：独立训练的 draft 模型难以精确匹配 target 模型的条件分布，尤其在高熵/开放式生成场景接受率骤降
2. **模型依赖**：需要为每个 target 模型准备对应的小变体，许多开源/商业模型无现成小版本
3. **内存开销**：draft 模型独立的 embedding / LM head / KV Cache 增加显存压力

---

## 3.2 自投机方法（2024-2025）

2024 年，社区转向"**自投机（Self-Speculative）**"路线——不依赖独立小模型，而是让目标模型自身或其轻量扩展生成 draft。

### 3.2.1 Medusa：多头并行预测（ICML 2024）**[背景：已核验链接]**

**Medusa** 在目标模型之上添加多个并行的"预测头"（Prediction Heads），每个头负责预测未来 $k$ 步的 token：

- **架构**：冻结 target backbone，添加 $K$ 个轻量级 LM heads（通常 1-2 层 MLP）
- **树状注意力（Tree Attention）**：将多头预测的候选组合成树状结构，通过单次树状注意力验证整棵树
- **训练**：仅需微调预测头，backbone 冻结
- **加速比**：2.5-3.5×（Vicuna-7B/13B 上验证）

**局限**：多头独立预测，未建模头之间的顺序依赖，长 horizon 上 draft 质量衰减较快。

### 3.2.2 Hydra：顺序依赖草案头（NeurIPS 2024）**[背景：已核验链接]**

**Hydra**（*Sequentially-Dependent Draft Heads for Medusa Decoding*，arXiv 2402.05109）改进 Medusa 的独立头设计，引入**顺序依赖**：

- 第 $k$ 个草案头的输入包含前 $k-1$ 个头的预测结果
- 通过自回归耦合增强 draft 的连贯性
- **加速比**：2.8-3.8×，在 Medusa 基础上有 10-20% 提升

> **v1 链接错误修复**：v1 报告中 Hydra 的链接为 `https://arxiv.org/abs/2402.02524`，该 arXiv 编号实际对应一篇**数论论文**（*A theta operator for the group GSp_4*），与 Hydra 无关。本报告已更正为已核验的 **`2402.05109`**。

### 3.2.3 Lookahead Decoding：完全免训练（NeurIPS 2024）**[背景：已核验链接]**

**Lookahead**（*Break the Sequential Dependency of LLM Inference Using Lookahead Decoding*，arXiv 2402.02057）是首个**完全免训练**的自投机方法：

- **Jacobi 迭代**：将自回归生成视为定点迭代问题，通过 Jacobi 方法并行更新多个位置
- **n-gram 池**：维护一个动态 n-gram 缓存池，从历史生成中检索匹配片段作为 draft
- **零训练成本**：无需任何微调或额外模型
- **加速比**：1.5-2.5×，受限于 n-gram 匹配命中率

### 3.2.4 其他早期退出方法 **[背景：已核验链接]**

- **LayerSkip**（arXiv 2404.16710）：利用早期层输出进行 draft 生成，跳过部分中间层
- **Kangaroo**：类似思路，在特定层退出并生成 draft

### 3.2.5 SWIFT 与 CLaSp：2025 年的"免训练层跳过"新解法（本轮新增） **[精读原文]**

2025 年的一个重要进展是：**把"层跳过"从固定配置做成在线自适应**，同时保持**完全免训练**。两条代表性工作如下。

#### 3.2.5.1 SWIFT：on-the-fly 自投机（ICLR 2025）

**基本信息**：Heming Xia, Yongqi Li, Jun Zhang, Cunxiao Du, Wenjie Li（香港理工大学）；ICLR 2025；核验页 <https://proceedings.iclr.cc/paper_files/paper/2025/hash/d74d002a9154b4cc433a234feb27c5f4-Abstract-Conference.html>；代码 <https://github.com/hemingkx/SWIFT>。

**问题定位**：既有 SD 方法**大多需要额外参数或大量训练**才能构建有效 draft 模型 → **限制其在不同 LLM 与任务上的适用性**。

**关键分析结论（论文自述）**：

> LLM 通过**层稀疏性（layer sparsity）**具备很大的自加速潜力，而且**这种稀疏性是任务相关的（task-specific）**。

这条"任务相关"的判断很重要：它意味着**一套固定的被跳层集合不可能对所有输入都最优**。

**机制**：SWIFT（**S**elf-speculative **W**ith **I**ntermediate layers, on-the-**F**ly **T**est）

- **plug-and-play**：**不需要辅助模型、不需要额外训练**
- **在推理时自适应地选择要跳过的中间层**
- 面向**多样化的输入数据流**（diverse input data streams）都能工作

**结果（论文自报）**：跨多种模型与下游任务取得 **1.3×–1.6× 加速**，且**保持生成文本的原始分布**。

#### 3.2.5.2 CLaSp：上下文内层跳过（ACL 2025）

**基本信息**：Longze Chen, Renke Shan, Huiming Wang, Lu Wang, Ziqiang Liu, Run Luo, Jiawei Wang, Hamid Alinejad-Rokny, Min Yang；ACL 2025 Long；DOI `10.18653/v1/2025.acl-long.1525`；核验页 <https://aclanthology.org/2025.acl-long.1525/>。

**问题定位**：SD 的效率**主要取决于 draft 模型与 verify 模型之间的一致性**；但既有 drafting 方法通常**需要训练额外模块**，实现困难且难以保证跨 LLM 的兼容性。

**机制：CLaSp（In-Context Layer Skip）**

| 设计 | 内容 |
|---|---|
| 基础思路 | **不需要额外 drafting 模块或额外训练**；即插即用 |
| draft 构造 | **跳过 verify 模型的中间层**，构造一个"压缩版 draft 模型" |
| 核心算法 | **动态规划（dynamic programming）**算法，以**上一验证阶段得到的完整隐藏状态**为目标函数来优化层跳过过程 |
| 关键特性 | **每个验证阶段后动态调整层跳过策略**，**不依赖预先优化好的被跳层集合** |

**结果（论文自报）**：LLaMA3 系列上 **1.3×–1.7× 加速**，且**不改变生成文本的原始分布**。

**在本章的意义**：SWIFT 与 CLaSp 把"自投机"从"训练一个额外模块"推进到"**诊断 target 自身哪几层可以省**"——前者依赖**任务相关层稀疏性**，后者依赖**上一次验证的隐藏状态**作为反馈信号。两者都声明保持原始分布（即无损）。 **[精读原文（摘要层）]**

### 3.2.6 回指：自投机与"随机采样下验证正确性"的关系（本轮新增）

本章所有自投机方法（Medusa / Hydra / Lookahead / LayerSkip / SWIFT / CLaSp）都只在**草稿侧**做文章；它们默认**验证侧的规则不变**。但 2026 H2 的核心发现是：**在 T>0 随机采样下，动态树这类"按 draft 概率排序建树"的机制会塌缩为 one-hot，接受率显著下降**。

三点需要注意的联系：

1. **层跳过类方法（SWIFT / CLaSp / LayerSkip）相对更"抗"这个问题**：它们的草稿来自 target 自身的压缩前向，**不构造按 $q$ 排序的动态树**，因此不存在 RheoSampling 所描述的"建树/验证耦合"。但它们同样**没有解决验证规则本身在抽样下的次优性**。
2. **Medusa / Hydra 的树状候选 + 树状注意力属于动态/半静态树的范畴**，在 T>0 下同样需要重新标定接受率。
3. **验证规则的改进与草稿侧的改进是正交的**：Traversal Verification（叶到根遍历）与 RheoSampling（双身份解耦）都在**验证/建树规则**层面做文章，理论上可与本章任一种自投机草稿组合。

> 完整分析见 [speculative-stochastic-verification.md](speculative-stochastic-verification.md) §3、§4；对 EAGLE 章节的具体限定见 [speculative-eagle-series.md](speculative-eagle-series.md) §3.3.5。

---

## 参考文献

### 基础方法（本轮已核验）

| # | 论文 | 年份 | 链接 | 可靠性 | 证据等级 |
|---|------|------|------|--------|---------|
| 1 | Leviathan et al., *Fast Inference from Transformers via Speculative Decoding*, ICML 2023 | 2023 | https://arxiv.org/abs/2211.17192 | 高 | 已核验链接 |
| 2 | Chen et al., *Accelerating Large Language Model Decoding with Speculative Sampling* | 2023 | https://arxiv.org/abs/2302.01318 | 高 | 已核验链接 |

### 自投机方法（本轮已核验 + 更正）

| # | 论文 | 年份 | 链接 | 可靠性 | 证据等级 |
|---|------|------|------|--------|---------|
| 3 | Medusa, *Simple LLM Inference Acceleration Framework with Multiple Decoding Heads*, ICML 2024 | 2024 | https://arxiv.org/abs/2401.10774 | 高 | 已核验链接 |
| 4 | Hydra, *Sequentially-Dependent Draft Heads for Medusa Decoding*, NeurIPS 2024 | 2024 | https://arxiv.org/abs/2402.05109 | 高 | **已核验（v1 链接有误，已更正）** |
| 5 | Lookahead Decoding, *Break the Sequential Dependency of LLM Inference Using Lookahead Decoding*, NeurIPS 2024 | 2024 | https://arxiv.org/abs/2402.02057 | 高 | 已核验链接 |
| 6 | LayerSkip, *Enabling Early Exit Inference and Self-Speculative Decoding* | 2024 | https://arxiv.org/abs/2404.16710 | 高 | 已核验链接 |
| 7 | **SWIFT**, *On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration*, ICLR 2025 | 2025 | https://proceedings.iclr.cc/paper_files/paper/2025/hash/d74d002a9154b4cc433a234feb27c5f4-Abstract-Conference.html | 高 | **精读原文（本轮新增）** |
| 8 | **CLaSp**, *In-Context Layer Skip for Self-Speculative Decoding*, ACL 2025 | 2025 | https://aclanthology.org/2025.acl-long.1525/ | 高 | **精读原文（本轮新增）** |
| 9 | SWIFT 代码 | 2025 | https://github.com/hemingkx/SWIFT | 高 | 已核验链接 |

---

> **报告说明**：本报告所有技术细节均来自公开发表的论文、arXiv 预印本、官方技术博客及开源项目文档。本轮新增的 SWIFT（ICLR 2025）与 CLaSp（ACL 2025）均基于会议 proceedings 一手页面核验。**v1 中 Hydra 的 arXiv 链接指向一篇无关数论论文（2402.02524），本轮已更正为 2402.05109**。加速比数据受测试条件影响显著，跨论文对比需谨慎；**T>0 随机采样下需重新标定接受率，见 [speculative-stochastic-verification.md](speculative-stochastic-verification.md)**。
>
> *数据截至 2026-10-16（v1：2026-06-06）。*
