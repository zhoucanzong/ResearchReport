# 投机解码：草稿模型训练新法（2026）

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、会议 proceedings（NeurIPS / ICML / ASPLOS）、arXiv 预印本与开源仓库整理生成。2026 年工作多为预印本，建议读者直接查阅原始论文验证。加速比数据受测试条件影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮新增）
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦**草稿模型（drafter）侧的 2026 年新方法与新分析**，与 [speculative-training-optimization.md](speculative-training-optimization.md)（训练目标优化）互补：本文关心**"训什么、怎么训、在什么场景训"**，后者关心**"用什么损失/奖励"**。
> **证据等级约定**：**[精读原文]**、**[摘要级]**、**[二手]**。
> **等级规则**：每条结论只取**一个主等级**（精读原文 / 摘要级 / 二手 / 受限核验）；**混合来源取最弱等级**并在正文注明来源类型（如 `[精读原文（vLLM 官方文档）]`）；不使用 `A + B`、`A（摘要层）` 这类复合标签。

---

## 1. 本章结论

1. **经典知识蒸馏（KD）的目标函数与投机解码的真实目标不一致**。KD 最小化 draft 与 target 在**所有 token** 上的 KL 散度，而 SD 的真实目标是**最大化 token 接受率**。这个错位是"draft 容量受限时无法吃透 target 知识"的根因。 **[精读原文]**
2. **"选择性蒸馏"是一个可量化的修正**：AdaSPEC 用一个 reference model 识别并**过滤掉难以拟合的 token**，只在"简单 token"上对齐 → 整体接受率提高且不牺牲生成质量，在 4 类任务上一致优于 DistillSpec，接受率最高提升 **15%**。 **[精读原文]**
3. **"草稿学到的注意力会漂移"是本轮最重要的新分析结论**。Attention Drift 发现：随着 drafter 在一条投机链内连续生成，**注意力逐渐从 prompt 移向它自己刚生成的 token**；该现象在 **EAGLE-3 drafter 与 MTP head 两类设计上都能观察到**，因此是**草稿设计层面的性质**，不是某个模型的偶然。 **[精读原文]**
4. **漂移有明确的机制解释与可行的架构修补**。根因是**链步之间未归一化的残差通路**：drafter 隐藏状态的幅值随链深单调增长，其动力学更像"叠在 target 上的额外 pre-norm transformer 层"，而非独立的自回归预测器。两个改动——**对 drafter 隐藏状态用 Post-norm**、**在捕获 target 隐藏状态后逐状态做 RMSNorm**——带来：模板扰动下接受长度最高 **2×**、长上下文任务 **1.18×**、7 个标准 benchmark **1.10×**。改动还让**较短的 train-time-test 深度可泛化到更长的草稿序列**。 **[精读原文]**
5. **训练侧的最大变量其实是"训练场景"而不是"训练算法"**。在 reasoning RL 训练中，响应生成呈**长尾分布**，少数超长响应主导执行时间。TLT 用 **Adaptive Drafter（在长尾生成期间利用空闲 GPU 持续训练 draft 模型，与 target 保持对齐、零额外成本）** + **Adaptive Rollout Engine（预捕获 CUDAGraph 池 + 按 batch 自适应选择 SD 策略）**，相对 SOTA 系统取得 **>1.7× 端到端 RL 训练加速**，保持模型精度，并把高质量 draft 模型作为**免费副产品**产出，可直接用于部署。 **[精读原文]**
6. **三条工作共同指向一个判断**：草稿质量的瓶颈**不在"训练得更久"，而在"训练目标 / 输入表征 / 训练时机"的选择上**。这与 EAGLE 系列"堆层数、堆特征"的路线形成对照。 **[综合]**

---

## 2. AdaSPEC：选择性知识蒸馏（NeurIPS 2025）**[精读原文]**

**基本信息**：Yuezhou Hu, Jiaxin Guo, Xinyu Feng, Tuo Zhao；NeurIPS 2025 主会（Advances in Neural Information Processing Systems 38）；核验页 <https://proceedings.neurips.cc/paper_files/paper/2025/hash/801a6708014185e951a95108b8cc8349-Abstract-Conference.html>；代码 <https://github.com/yuezhouhu/adaspec>（仓库自述"A selective knowledge distillation algorithm for efficient speculative decoders"）。

**问题与动机**

| 环节 | 传统 KD 的做法 | 问题 |
|---|---|---|
| 目标函数 | 在所有 token 上最小化 draft 与 target 的 **KL 散度** | **与 SD 的真实目标（最大化接受率）错位** |
| 后果 | draft 受容量约束，学不动难拟合的 token | 接受率次优 |

**机制**

AdaSPEC 在 KD 过程中加入**选择性 token 过滤（selective token filtering）**：

1. 引入一个 **reference model** 来识别并**过滤掉"难以拟合"（difficult-to-fit）的 token**
2. 让 draft 在**更简单的 token** 上与 target 更好对齐
3. 效果：**整体 token 接受率提高，且不牺牲生成质量**

**实验（论文自报）**

| 维度 | 内容 |
|---|---|
| 任务 | 算术推理、指令跟随、代码、摘要 |
| 模型配置 | **31M/1.4B** 与 **350M/2.7B**（draft/target） |
| 对比基线 | **DistillSpec**（当时的 SOTA） |
| 结果 | **所有任务一致优于 DistillSpec，接受率最高提升 15%** |

**为什么这条结论对本专题重要**：它把"接受率"从**间接代理目标**（KL 散度）变成了**直接可优化的对象**——与 [speculative-training-optimization.md](speculative-training-optimization.md) 中 LK Losses（用 TV 距离替代 KL）的思路同属一条主线：**"draft 学得像 target" ≠ "draft 被接受得多"**。

**局限（论文未展开，本报告标注为推断）**：reference model 本身从哪来、其能力强弱如何影响过滤质量，摘要未说明；"简单 token"的定义与任务相关性未量化。

---

## 3. Attention Drift：草稿学到了什么（arXiv:2605.09992）**[精读原文]**

**基本信息**：Doğaç Eldenk, Payal Mohapatra, Yigitcan Comlek, Kaan Oktay, Hongyang Zhang, Stephen Xia；arXiv 2605.09992，提交 2026-05-11；HF Papers 页 <https://huggingface.co/papers/2605.09992>。

**现象：注意力漂移（attention drift）**

论文的出发点是两个已被工程界观察到的退化现象：

- drafter 在**模板扰动（template perturbation）**下性能急剧下降
- drafter 在**长上下文输入**下性能急剧下降

作者识别出一个**此前未被报道**的现象：

> 当 drafter 在一条投机链（speculation chain）内连续生成 token 时，**注意力逐步从 prompt 转移到它自己最近生成的 token 上**。

**关键论据：这是草稿设计层面的性质**

- 该现象在 **EAGLE-3 drafter** 与 **MTP head** 两类设计上**均可观察到**
- 因此不能归因于某个模型的训练偶然，而应视为 **drafter 设计的共有属性**

**根因：链步之间未归一化的残差通路**

- drafter 的**隐藏状态幅值随链深单调增长**
- 其动力学表现**更像"叠在 target 之上的额外 pre-norm transformer 层"，而不是一个独立的（standalone）自回归预测器**
- 这解释了两件事：① 为什么"草稿链越深越不可靠"（与 [speculative-cascade-heterogeneous.md](speculative-cascade-heterogeneous.md) 中 HCSpec 的"期望效用快速衰减"经验观察**互相印证**）；② 为什么在长上下文/模板扰动下退化更严重。

**修补：两个架构改动**

| 改动 | 位置 | 作用 |
|---|---|---|
| **Post-norm** | drafter 的隐藏状态 | 抑制隐藏状态幅值随链深增长 |
| **Per-hidden-state RMSNorm** | 捕获 target 隐藏状态之后，逐隐藏状态做 | 让 draft 的输入表征稳定 |

**实验（论文自报，相对 pre-norm EAGLE-3）**

| 场景 | 接受长度提升 |
|---|---|
| 模板扰动（template perturbation） | 最高 **2×** |
| 长上下文任务 | **1.18×** |
| 7 个标准 benchmark（多轮对话 / 数学 / 代码） | **1.10×** |

**额外收益**：改动让**较短的 train-time-test 深度可以泛化到更长的草稿序列**——即训练时不必把链深推到推理时的长度，直接降低训练成本。

> **本条结论与本专题既有章节的联动**：EAGLE-3 的 TTT（Training-Time Test）是"训练阶段模拟验证过程"；Attention Drift 说明 TTT 模拟的那条链本身存在**表征层面的系统性偏移**。两者结合读，可以理解为"TTT 的方向正确，但需要先修复隐藏状态归一化"。

---

## 4. Adaptive Drafter / TLT：推理 RL 训练侧（ASPLOS 2026）**[精读原文]**

**基本信息**：Qinghao Hu, Shang Yang, Junxian Guo, Xiaozhe Yao, Yujun Lin, Yuxian Gu, Han Cai, Chuang Gan, Ana Klimovic, Song Han（部分作者在发表时隶属 IBM）；ASPLOS 2026；发表日 2026-03-22；核验页 <https://research.ibm.com/publications/taming-the-long-tail-efficient-reasoning-rl-training-with-adaptive-drafter>；代码 <https://github.com/mit-han-lab/fastrl>（仓库自述 `[ASPLOS'26] Taming the Long-Tail: ...`）。

> 注意：任务书把这项工作归为"IBM/ASPLOS 2026"，一手页面确为 IBM Research 出版页，作者含 IBM 时间点关联成员，但核心团队与代码仓库属于 MIT HAN Lab。本报告如实标注。

**问题：推理 RL 训练的长尾瓶颈**

- 具备强推理能力的 LLM 主要依靠 **RL 训练**
- 但 RL 训练中的**响应生成（rollout）呈持久的长尾分布**：**少数超长响应主导执行时间**，浪费算力、抬高成本

**为什么在 RL 里用投机解码很难**

论文显式列出三个障碍：

1. **动态工作负载**（响应长度分布随训练变化）
2. **target 模型在演化**（每步更新权重，drafter 会对不上）
3. **draft 模型训练开销**（额外训练成本吃掉收益）

**机制：TLT 的两个协同组件**

| 组件 | 设计 | 解决的障碍 |
|---|---|---|
| **Adaptive Drafter** | 轻量 draft 模型，**在长尾生成期间利用空闲 GPU 持续训练**，与 target 保持对齐 | 障碍 2 + 3：**零额外成本**地维持对齐 |
| **Adaptive Rollout Engine** | 维护一个**内存高效的预捕获 CUDAGraph 池**，并为每个输入 batch **自适应选择适合的 SD 策略** | 障碍 1：动态负载下策略选择 |

**实验（论文自报）**

| 指标 | 结果 |
|---|---|
| 端到端 RL 训练加速 | **>1.7×**（相对 SOTA 系统） |
| 模型精度 | **保持**（losslessly） |
| 副产品 | **高质量 draft 模型**，可直接用于高效部署 |

**为什么这条工作的意义超出 RL 场景**：它把 drafter 的"训练时机"从"离线一次性"改成"**在线、用系统空闲资源持续更新**"。这与 [speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md) 中 vLLM 为 DFlash/DSpark 引入 `draft_context_window` 的动机**同源**——都是承认"drafter 与 target/上下文会持续失配，需要在系统层面持续补偿"。

---

## 5. 三条工作的对照与组合

| 维度 | AdaSPEC | Attention Drift | Adaptive Drafter (TLT) |
|---|---|---|---|
| 干预点 | **训练目标**（训哪些 token） | **架构 / 表征**（隐藏状态归一化） | **训练时机与系统调度** |
| 核心诊断 | KD 目标错位 | 隐藏状态幅值随链深增长 | RL rollout 长尾 + target 演化 |
| 主要收益 | 接受率最高 +15% | 接受长度最高 2×（扰动）/1.18×（长上下文）/1.10×（7 benchmark） | RL 训练 >1.7× |
| 是否需重训 drafter | 是 | 是（改动训练架构） | 是（但训练在空闲 GPU 上持续进行） |
| 与 EAGLE-3 的关系 | 可与之组合（改进蒸馏目标） | **直接修补 EAGLE-3 drafter** | 场景不同（RL 训练而非推理服务） |

**组合判断（本报告推断，非论文结论）**：三条改动**彼此正交**，理论上可叠加——用 AdaSPEC 的选择性蒸馏目标 + Attention Drift 的归一化架构 + TLT 的在线更新调度。但本专题**未找到任何论文做过这种组合实验**，故此判断仅为结构性推断，不构成已验证结论。

---

## 6. 尚未确证 / 待跟踪

| 项 | 状态 | 说明 |
|---|---|---|
| AdaSPEC 的 reference model 具体选择 | **未验证** | 摘要未说明其来源与规模 |
| AdaSPEC 在更大模型规模（如 8B/70B）上的表现 | **未验证** | 实验止于 350M/2.7B |
| Attention Drift 是否在 EAGLE-2 上也存在 | **未验证** | 摘要只声明 EAGLE-3 与 MTP head |
| Attention Drift 的 2× 是否为"相对 pre-norm EAGLE-3"的接受长度 | **已确认** | 论文明确写"improve acceptance length over ... pre-norm EAGLE3" |
| TLT 的 1.7× 是否为端到端（含 drafter 训练开销） | **已确认** | 论文写"over 1.7x end-to-end RL training speedup" |
| TLT 是否可用于非 RL 的推理服务场景 | **未验证** | 论文定位为 RL 训练；是否外推到 serving 未见讨论 |

---

## 7. 链接核验清单（本轮实测，2026-10-16）

| # | 来源 | 链接 | 核验结果 |
|---|---|---|---|
| 1 | AdaSPEC, NeurIPS 2025 | https://proceedings.neurips.cc/paper_files/paper/2025/hash/801a6708014185e951a95108b8cc8349-Abstract-Conference.html | ✅ HTTP 200，标题/作者/摘要一致 |
| 2 | AdaSPEC 代码 | https://github.com/yuezhouhu/adaspec | ✅ HTTP 200（仓库自述"selective knowledge distillation algorithm for efficient speculative decoders"） |
| 3 | Attention Drift, arXiv 2605.09992 | https://arxiv.org/abs/2605.09992 | ✅ HTTP 200，标题/作者/日期/摘要一致 |
| 4 | Attention Drift, HF Papers | https://huggingface.co/papers/2605.09992 | ✅ HTTP 200（页面标题与 arXiv 一致） |
| 5 | Adaptive Drafter / TLT, IBM Research | https://research.ibm.com/publications/taming-the-long-tail-efficient-reasoning-rl-training-with-adaptive-drafter | ✅ HTTP 200，作者列表、日期（2026-03-22）、ASPLOS 2026 归属、摘要一致 |
| 6 | TLT 代码 | https://github.com/mit-han-lab/fastrl | ✅ HTTP 200，仓库自述 `[ASPLOS'26] Taming the Long-Tail` |

> 本轮无失效链接。AdaSPEC 与 TLT 均以会议/机构一手页面核验；Attention Drift 为 arXiv 预印本（**未经同行评审**），其"幻觉/漂移"类分析结论建议以论文附录与复现为准。

---

## 参考文献

| # | 论文 | 年份 / 出处 | 链接 | 证据等级 |
|---|---|---|---|---|
| 1 | AdaSPEC, *Selective Knowledge Distillation for Efficient Speculative Decoders* | NeurIPS 2025 | https://proceedings.neurips.cc/paper_files/paper/2025/hash/801a6708014185e951a95108b8cc8349-Abstract-Conference.html | 精读原文 |
| 2 | Attention Drift, *What Autoregressive Speculative Decoding Models Learn* | arXiv 2605.09992（2026-05-11） | https://arxiv.org/abs/2605.09992 | 精读原文 |
| 3 | TLT / Adaptive Drafter, *Taming the Long-Tail: Efficient Reasoning RL Training with Adaptive Drafter* | ASPLOS 2026（2026-03-22） | https://research.ibm.com/publications/taming-the-long-tail-efficient-reasoning-rl-training-with-adaptive-drafter | 精读原文 |
| 4 | DistillSpec（AdaSPEC 的对比基线） | 2024 | https://arxiv.org/abs/2310.08461 | 背景 |
| 5 | EAGLE-3（Attention Drift 的对比基线） | NeurIPS 2025 | https://arxiv.org/abs/2503.01840 | 背景 |
| 6 | SpecForge（草稿训练框架，与本轮新增可互参） | ICML 2026, arXiv 2603.18567 | https://arxiv.org/abs/2603.18567 | 精读原文 |

---

> **报告说明**：本报告结论按证据等级标注。AdaSPEC、Attention Drift、TLT 的关键数字均来自一手会议/机构/arXiv 页面。所有加速比与接受率数字为论文自报值，跨论文、跨设定不可直接比较。
>
> *数据截至 2026-10-16。*
