# 投机解码：EAGLE 系列与工业标准

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、技术博客、开源项目和第三方分析整理生成。部分信息可能未经同行评审，建议读者直接查阅原始论文验证。arXiv 预印本论文中的加速比数据受测试条件（模型规模、硬件、任务类型）影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮更新；v1 为 2026 年 6 月）
> **本次改动**：新增 §3.3.5「限定条件：T>0 下动态草稿树的塌缩」，对 EAGLE-2/EAGLE-3 的既有结论**加限定条件**，并指向 [speculative-stochastic-verification.md](speculative-stochastic-verification.md)。这是本轮更新中 EAGLE 章节最实质的变化。
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦 EAGLE 系列特征级 draft 方法。主报告见 [report.md](report.md)。

---

## 3.3 EAGLE 系列：当前工业标准（2024-2025）

**EAGLE（Extrapolation for Autoregressive Generation with a Learned Extension）** 系列由北京大学等团队提出，是当前工业界最广泛部署的投机解码方案。

### 3.3.1 EAGLE-1（ICLR 2024）

- **核心创新**：**特征级自回归（Feature-level Autoregression）**
  - 不直接预测 token，而是预测 target 模型第一层的**隐藏特征（hidden features）**
  - 基于预测的特征，通过 target 模型的 LM head 解码为 token
- **架构**：单层 Transformer 作为 draft 模型，参数量约为 target 的 **~7%**
- **优势**：特征空间比 token 空间更平滑，draft 质量显著优于 token 级小模型
- **加速比**：3-4×（LLaMA-2-7B/13B/70B 上验证）

### 3.3.2 EAGLE-2（EMNLP 2024）

- **核心创新**：**动态草案树（Dynamic Draft Tree）**
  - 上下文感知分支策略：根据当前序列的熵动态调整树的分支因子
  - 低熵位置（如代码/公式）增加分支深度，高熵位置（如开放对话）减少分支
  - 实现细节：用 draft 概率 $q(x)$ 做**确定性 top-$K$ 扩展** + **全局剪枝**，路径分数为沿路径的 $q$ 连乘
- **加速比**：3.5-4.5×，比 EAGLE-1 提升约 10-15%
- **⚠️ 限定条件**：上述数字与"动态树优于静态树"的结论**以 greedy（T=0）解码为前提**，见 §3.3.5

### 3.3.3 EAGLE-3（NeurIPS 2025）

- **核心创新**：**多层特征融合 + TTT（Training-Time Test）**
  - 融合 target 模型多层特征（而非仅第一层）作为 draft 输入
  - TTT：在训练阶段模拟验证过程，使 draft 模型直接优化"被接受后的分布"
  - 推理侧沿用 EAGLE-2 的动态树：树宽 60、深度 8 是常见默认设置
- **性能（口径澄清，2026-10 修订）**：
  - **4.79×** 是 **LLaMA-3.3-70B 特定设定下的表值**，接受率 **70-80%**；引用时应连同模型与设定一起给出，不可当作 EAGLE-3 的通用指标。
  - **论文摘要口径**：EAGLE-3 "achieves a speedup ratio **up to 6.5×**, with about **1.4× improvement over EAGLE-2**"，实验覆盖 **chat 模型与 reasoning 模型、五个任务**——**6.5× 是摘要给出的上限**，**4.79× 是上述特定设定值**，两者并不矛盾。
  - **吞吐口径（另一个数）**：论文摘要另称 "In the **SGLang** framework, EAGLE-3 achieves a **1.38× throughput improvement at a batch size of 64**"——这是 **batch=64 下的吞吐提升**，与单请求延迟加速比**不是同一量纲**，不可混用。 **[精读原文：arXiv:2503.01840 摘要]**
- **工业地位**：截至 2026 年，EAGLE-3 是 vLLM、SGLang 等主流推理框架的默认投机解码方案
- **⚠️ 限定条件**：**4.79× 与 70-80% 接受率均为 greedy 设定下的报告值**，在 T>0 采样下会显著下降，见 §3.3.5

### 3.3.4 SpecForge（2026-03）

**SpecForge** 是首个生产级 EAGLE-3 训练框架：

- **Target-Draft 解耦**：打破 EAGLE 系列强耦合 target 架构的限制，支持为任意 target 模型训练 draft
- **训练加速**：相比原始 EAGLE-3 训练流程，**9.9× 训练加速**
- **SpecBundle**：发布生产级草案模型集合，覆盖主流开源模型（LLaMA、Qwen、Mistral 等）
- **意义**：解决了 EAGLE-3 最大的工程痛点——draft 模型训练成本过高

> **来源补正（本轮）**：v1 报告中 SpecForge 的 arXiv 编号为占位符（`2503.XXXXX`）。本轮已找到并核验**一手来源**：*SpecForge: A Flexible and Efficient Open-Source Training Framework for Speculative Decoding*，**arXiv 2603.18567**（2026-03-19），ICML 2026 poster <https://icml.cc/virtual/2026/poster/65558>。论文明确：为 EAGLE-3 提供完整支持，通过 target-draft 解耦、混合并行、优化训练内核与生产级推理引擎集成，在 **Qwen3-235B-A22B 上实现最高 9.9× 的 EAGLE-3 训练加速**，并发布 **SpecBundle** 生产级草案模型集合。 **[精读原文]**

### 3.3.5 限定条件：T>0 下动态草稿树的塌缩（2026 H2 新增）

> 本节是本轮更新的核心修正。详细分析见 [speculative-stochastic-verification.md](speculative-stochastic-verification.md)。

**结论**：EAGLE-2/EAGLE-3 的"动态树更优"这一结论**只在 greedy（T=0）下成立**。在随机采样（T>0）下，动态树的建树机制会导致 **draft 分布塌缩为 one-hot**，接受率显著下降。

**机制（为什么是机制性的，而不是实现问题）**

1. 动态树的扩展与剪枝按 **draft 概率 $q(x)$** 排序，路径分数是 $q$ 的连乘 → 树天然收敛到少数高 $q$ 分支，即近似 one-hot 的确定性结构。
2. T=0 时这不构成问题：draft 的 top-1 通常与 target 对齐，"$q$ 最大"≈"会被接受"。
3. T>0 时接受判据变为 $\eta \le \min(1, p(x)/q(x))$，**是否接受取决于比值而非 $q$ 的大小**。$q(x)$ 小的 token 若 $p(x)$ 足够大仍会被接受；$q(x)$ 大也不保证被接受。于是按 $q$ 建树既丢掉了随机性，又不再能预测接受。
4. 论文给出的两难表述：**动态树为保住上下文感知拓扑而牺牲了随机采样，静态树为保住随机采样而牺牲了上下文感知结构**。

**为什么不能"直接改成采样"**

若把 top-$K$ 替换为随机采样、但仍按 $q$ 排序，会**破坏无损性**：token 能否在树中存活取决于它自身的取值，对"存活"取条件会使条件分布偏离原采样分布 $\tilde q$，验证阶段再用 $\tilde q$ 判接受就是错的基准，输出分布不再等于 $p$。

**当前解法（2026 H2）**

| 解法 | 出处 | 思路 | 对 EAGLE-3 的效果 |
|---|---|---|---|
| **RheoSampling** | arXiv:2609.21827（2026-09-18） | 建树 / 验证**双身份解耦**：建树用 proxy 概率、验证用真实采样概率；OT 验证提高接受率；证明严格无损 | 在 6 benchmark × 3 模型上，平均接受长度 +0.14~+0.22；Llama-3.1-8B 上 5.04→**5.25**（+4.2%），加速 2.84×→**2.93×** |
| **Traversal Verification** | NeurIPS 2025 | 改验证遍历：叶到根 + 序列级接受判据；证明无损、单链最优 | 跨树结构平均接受长度 +2.2%~5.7%；更深更大的树收益更大 |
| **ARC-Decode** | ICML 2026 | 放宽验证为**有界风险**（JS 散度上界 + Local Tolerance Score 软接受） | 采样设定下相对 EAGLE-3 最高 **1.6×** 端到端加速，质量变化可忽略（摘要级） |

**指标口径提醒**：评估 EAGLE 变体时必须**成对报告** `mean_acceptance_length` 与 `draft_acceptance_rate`——两者分母不同、会反向移动。加深草稿树通常会降低 acceptance rate 却提高 mean accepted length，只报一个会得出相反结论。详见 [speculative-stochastic-verification.md](speculative-stochastic-verification.md) §2.2。

**成本感知建树（补充维度）**：另一条独立的修正来自系统侧——**CAST**（ICLR 2026）指出 EAGLE-2/3 的构树规则纯靠启发式，只看"token 接受率"，**无视 GPU 型号与 batch size**。它的隐含假设"草稿 token 越多越好"只在 batch=1、GPU 未饱和时成立；开启批处理后加深加宽草稿树会让 draft/verify 争抢 GPU 资源，论文实测 EAGLE-2 在 batch=8 的 CNN/DM 上甚至降到 **0.84×（比原始自回归还慢）**。CAST 把树宽、层数、验证 token 数改写成"接受收益 vs 推理代价"的效用最大化问题，最高可达 **5.2× 加速**，并指出 EAGLE-2/3 是该框架在特定参数下的特例。

> **证据等级**：RheoSampling 与 Traversal Verification 的关键数字为**精读原文**；ARC-Decode 为**摘要级**（仅 ICML 会议页可核验）；CAST 为**二手来源**（第三方论文解读页，非一手原文）。

**对使用者的一句话建议**：在 greedy 场景使用 EAGLE-2/EAGLE-3 时，v1 报告中的结论仍然可用；一旦上线 `temperature > 0` 的服务，就应把接受率与接受长度按采样温度重新标定，并考虑 RheoSampling / Traversal Verification 这类把建树与验证解耦的方案。

---

## 参考文献

| # | 论文 | 年份 | 链接 | 可靠性 |
|---|------|------|------|--------|
| 1 | EAGLE-1, *Lossless Acceleration of LLMs by Encoding the Future as Single Token*, ICLR 2024 | 2024 | https://arxiv.org/abs/2403.00835 | 高 |
| 2 | EAGLE-2, *Faster Inference of Language Models with Dynamic Draft Trees*, EMNLP 2024 | 2024 | https://arxiv.org/abs/2406.16858 | 高 |
| 3 | EAGLE-3, *Scaling up Inference Acceleration of Large Language Models via Training-Time Test*, NeurIPS 2025 | 2025 | https://arxiv.org/abs/2503.01840 | 高 |
| 4 | SpecForge, *A Flexible and Efficient Open-Source Training Framework for Speculative Decoding*, ICML 2026 | 2026-03-19 | https://arxiv.org/abs/2603.18567 | 高（**已核验 + 精读原文**，v1 占位符已替换） |
| 5 | RheoSampling, *Resolving the One-Hot Dilemma in Stochastic Dynamic-Tree Speculative Decoding*, arXiv 2609.21827 | 2026-09-18 | https://arxiv.org/abs/2609.21827 | 中（预印本，已精读原文） |
| 6 | Traversal Verification, *Traversal Verification for Speculative Tree Decoding*, NeurIPS 2025 | 2025 | https://proceedings.neurips.cc/paper_files/paper/2025/hash/70596d70542c51c8d9b4e423f4bf2736-Abstract-Conference.html | 高（已精读原文） |
| 7 | ARC-Decode, *Accelerated Decoding with Risk-Bounded Acceptance*, ICML 2026 | 2026 | https://icml.cc/virtual/2026/poster/66788 | 中（仅会议页，摘要级） |
| 8 | CAST, *Inference-Cost-Aware Dynamic Tree Construction for Efficient Inference in LLMs*, ICLR 2026 | 2026 | https://papernotes.org/ICLR2026/llm_efficiency/inference-cost-aware_dynamic_tree_construction_for_efficient_inference_in_large_/ | 中（二手解读页） |

> **注**：第 4 项 SpecForge 在 v1 中为占位链接（`2503.XXXXX`），本轮已替换为**已核验**的 arXiv 2603.18567，并据摘要补充了 target-draft 解耦、混合并行与 9.9× 训练加速等要点（**精读原文**）。

---

> **报告说明**：本报告所有技术细节均来自公开发表的论文、arXiv 预印本、官方技术博客及开源项目文档。2023-2025 年方法的信息可靠性普遍较高（经同行评审）。加速比数据受测试条件影响显著，跨论文对比需谨慎。**EAGLE-2/EAGLE-3 的加速比与接受率为 greedy 设定下的报告值，T>0 采样下需重新标定（见 §3.3.5）。**
>
> *数据截至 2026-10-16（v1：2026-06-06）。*
