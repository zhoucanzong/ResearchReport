# 投机解码：块扩散与检索式方法

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、会议 proceedings（ICML / NeurIPS / NAACL）、arXiv 预印本、官方工程博客与框架文档整理生成。部分 2026 年信息可能未经同行评审，建议读者直接查阅原始论文验证。加速比数据受测试条件（模型规模、硬件、任务类型、batch、并发度）影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮更新；v1 为 2026 年 6 月）
> **本次改动**：DFlash 补齐 ICML 2026 一手来源；**新增 DSpark**（半自回归块草稿 + 置信度驱动变长验证）；**新增 BASTION**（预算感知 + 树状块扩散）；**新增成本感知建树**；**新增 Google TPU 扩散式投机**；修复 v1 中 I-DLM 与 NLD 的占位链接。
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦块扩散方法、检索式方法，以及扩散语言模型作为竞争范式的分析。主报告见 [report.md](../report.md)。
> **证据等级约定**：**[精读原文]**、**[摘要级]**、**[二手]**。
> **等级规则**：每条结论只取**一个主等级**（精读原文 / 摘要级 / 二手 / 受限核验）；**混合来源取最弱等级**并在正文注明来源类型（如 `[精读原文（vLLM 官方文档）]`）；不使用 `A + B`、`A（摘要层）` 这类复合标签。

---

## 3.4 块扩散方法

### 3.4.1 DFlash：块扩散草稿的开创工作（ICML 2026）**[精读原文]**

**基本信息**：Jian Chen, Yesheng Liang, Zhijian Liu（UCSD Z Lab）；arXiv 2602.06036（2026-02-05）；**ICML 2026 poster** <https://icml.cc/virtual/2026/poster/64301>。

**核心机制**

- **轻量级块扩散模型作为 drafter**：**单次前向**生成整个 token 块（block），而非逐个 token 自回归
- **条件于 target 模型隐藏特征**：draft 模型以从 target 抽取的 context 特征为条件，从而获得高质量草稿与更高接受率
- **问题动机**：既有方法仍依赖**自回归草稿**，起草阶段仍是串行的，**限制了实际可得的加速**

**性能（论文自报）**

| 指标 | DFlash | 说明 |
|---|---|---|
| 无损加速 | **超过 6×** | 跨多种模型与任务 |
| 相对 SOTA（EAGLE-3） | **最高 2.5× 更高的加速** | 论文原文表述 |

**关键论断**：论文主张"**投机解码是扩散模型天然且有效的用武之地**"——因为投机解码只需要 draft 产出**候选**，而不需要 draft 独立达到自回归生成的质量。

### 3.4.2 DSpark：半自回归块草稿 + 置信度驱动的变长验证 **[精读原文]**

**基本信息**：DeepSeek 的 DSpark 算法；工程集成见 SGLang 官方博客 *DSpark in SGLang: Speculative Decoding with Confidence-Driven, Variable-Length Verification*（SGLang Team，2026-07-06），以及 vLLM 的 `dspark` speculator 实现。已发布权重示例：`deepseek-ai/dspark_qwen3_14b_block7`（HF 模型页可达，模型卡为 "No model card"，故权重细节以官方博客为准）。

**问题：投机解码的收益随负载恶化**

> 在 batch size B、投机 token 数 K 时，target 每一步要验证 **B × K** 个 token；**超过某个点后，验证成本高于省下的解码步收益。**

这条表述与 vLLM 官方 *Adaptive Verification* 文档的说法一致（见 §3.4.5），也是本轮更新里**"系统协同"这条主线的核心论据**。

**机制：从两端同时攻击**

| 端点 | DSpark 的做法 | 目的 |
|---|---|---|
| **草稿侧** | **半自回归块草稿器**（semi-autoregressive block drafter）：每次 draft 前向出一个**整块** | 让**接受率保持高位**的同时获得块级并行 |
| **验证侧** | **按请求、随置信度变化的验证长度**：用草稿模型自身的置信度决定验证多长 | **停止验证那些负载不太可能接受的 token** |

**SGLang 集成的工程要点（这部分是"算法→wall-clock"的关键）**

1. **ragged verify + 完整 CUDA graph**：被裁剪的 batch **重放真正更小的图**，而不是填充过的图
2. **overlap-aware 投机路径**：把调度器隐藏在 forward 之后
3. **cost-table profiler**：让调度器**在线**为每个请求确定验证预算
4. **可观测性**：暴露"裁剪后本会被掩盖的接受上限"

**实验（SGLang 自测）**：DeepSeek-V4-Flash on H200，DP-attention 跨 4 卡，并发从 batch 1 扫到 256；对照为 non-spec floor 与 MTP（EAGLE 风格基线）。结论是 **DSpark 在整个并发区间给出最好的吞吐/延迟权衡**，明显优于 MTP 与非投机基线。**注意**：博客明确声明"硬件、引擎、流量都与论文不同，我们复现的是**机制与曲线形状**，不是论文数字"。

**与 HeteroSpec 的关系需要区分**：DSpark 论文将 calibrated prefix-survival 与当前 engine `SPS(B)` 曲线结合，对活动 batch 中各请求的验证前缀做全局吞吐调度；HeteroSpec 则用 path entropy 对上下文分层，再为 EAGLE-3 选择 draft depth、Top-N 与计算图。二者都会自适应验证/候选预算，但不是“单请求机制推广到跨请求”的同一方法。旧稿关于“第一个产品级调度”与优先级竞争的表述已撤回；机制和停止条件见 [DSpark 精读](../papers/2607.05147-dspark.md) 与[异质预算专题](../topics/heterogeneous-budget-allocation.md)。

### 3.4.3 BASTION：预算感知 + 树状块扩散（arXiv 2605.29727）**[精读原文]**

**基本信息**：Soowon Oh, Nam Cao, Yujin Kim, Hojung Jung, Huzama Ahmad, Sangmin Bae, Se-Young Yun；arXiv 2605.29727（2026-05-28）。

**问题**

块扩散 drafter 在单次并行步内预测**多个未来 token 的分布**，但这些并行预测是从**逐位置的边缘分布（position-wise marginals）**采样得到的，**不是完全条件化的序列**。因此：

> **只取一条贪心路径，往往抓不住 target 模型偏好的轨迹。**

**机制：BASTION（Budget-Aware Speculative Decoding with Tree-structured Block Diffusion Drafting）**

与依赖**静态树拓扑**的既有方法不同，BASTION 通过**平衡草稿质量与硬件约束**来**动态构建 query-dependent 的树**。三个协同组件：

| # | 组件 | 作用 |
|---|---|---|
| 1 | **Acceptance surrogate** | 通过**路径置信度**估计**期望接受长度** |
| 2 | **Online latency estimator** | 校准一个**硬件感知的 roofline 模型** |
| 3 | **Adaptive best-first expansion** | 持续生长树，**直到边际收益不再值得增量验证成本** |

**属性与结果（论文自报）**

- **免训练（training-free）**
- **保持 target 模型的分布**
- **无需逐场景调参**
- 跨多种 benchmark 与 GPU 架构：相对标准自回归**最高 6.61× 加速**，比 SOTA 块扩散基线**优 39%**

**与前文的关系**：BASTION 的"边际收益不再值得成本就停止扩张"与 CAST（ICLR 2026）的"成本感知效用最大化"、DSpark 的"变长验证"是**同一条系统思想的三次独立实现**——**"草稿 token 越多越好"这个假设在所有场景下都不成立。**

### 3.4.4 成本感知动态建树（CAST, ICLR 2026）**[二手]**

> **证据等级说明**：本条目的信息来源为**第三方论文解读页**，非一手原文。CAST 的论文页与代码（`EAGLE-Research/sglang-eagle4`）在解读页中被引用，但本报告未直接核验原始论文/代码。

CAST（**C**ost-**A**ware **S**peculative **T**ree）在 EAGLE-2/3 的动态草稿树上引入"**推理成本**"这一系统变量（GPU 型号、batch size），把树的**宽度、深度与验证 token 数**建模成"**接受收益 vs 推理代价**"的效用最大化问题。

- **既有痛点**：EAGLE-2/3 的构树规则**纯靠启发式**，只看 token 接受率，**无视 GPU 硬件与 batch size**。其隐含假设"草稿 token 越多越好"只在 **batch size = 1、GPU 未饱和**时成立。
- **核心矛盾**：批处理下 GPU 利用率已被 batch 拉高，再盲目加深加宽草稿树会让 draft/verify **争抢 GPU 资源**。论文实测 **EAGLE-2 在 batch=8 的 CNN/DM 上降到 0.84×（比原始自回归还慢）**。
- **机制**：离线预计算推理时间查找表 $f(B, c, n)$（batch、上下文长、序列长 → 时间），把"再多算 $k$ 个 token 的代价"与"接受收益"实时权衡；只保留**边际效用超过阈值**的节点。EAGLE-2/3 成为该框架在特定参数下的特例。
- **结果（解读页自报）**：**最高可达 5.2× 加速**，单样本场景小幅提升、batch 场景大幅超越既有 SOTA。

### 3.4.5 为什么"块扩散"必须与"验证预算"一起读（vLLM 官方文档）**[精读原文]**

vLLM *Adaptive Verification* 文档把这件事说得最清楚：

> **batch size = 1 时这笔交易很划算**：GPU 处于 **memory-bound**，有多余算力，额外的 draft token 接近免费。
> **batch size = 256 时这笔交易很微妙**：draft token 开始与真实 token **争夺同样的算力**，**每一个被拒绝的 token 都是被浪费的算力**；足够多时，**吞吐会下降**。
> 原因在于**逐位置的接受率衰减很快**：当 GPU 还是 memory-bound 时那个槽位基本免费、值得赌一把；一旦饱和，这次赌博就有真实的吞吐成本。
> **交叉点随负载与负载相关的接受率移动，因此不存在一个静态的 `num_speculative_tokens` 能适配所有并发度。**

vLLM 的 adaptive verification 机制：每个 **(request, position)** 草稿槽按其**存活概率**（该请求逐位置接受率估计的连乘）打分，**按分数从高到低准入直到耗尽全局预算**；槽位**跨请求竞争**——"置信请求的位置 5 可以排在不置信请求的位置 1 之前"。预算本身来自**启动时 profiled 的成本模型**（在每个 shape 上测这一步的成本，再选使"期望接受 token 数/秒"最大的 token 数）。

**支持范围**：基于模型的 drafter（**EAGLE、MTP、DFlash、DSpark** 与 standalone draft 模型）。逐位置接受率估计有两个来源：

| 来源 | 适用 |
|---|---|
| **Confidence head** | **DSpark checkpoint 自带训练好的 confidence head**时直接使用其预测 |
| **Online acceptance estimator** | 其他 drafter：用一个小 logistic 模型从 draft logits 预测接受率，**在服务过程中依据 target 的验证结果持续重新校准** |

默认关闭，通过 `enable_adaptive_verification` 开启。

### 3.4.6 Google TPU 上的扩散式投机（工程博客）**[精读原文]**

**基本信息**：Google Developers Blog，2026-05-04；作者 Weiren Yu、Yarong Mu、Lihao Ran、Zhaoxiang Feng、Yiming Zhao、Hao Zhang；核验页见 §参考文献。

**要解决的问题**：**自回归草稿的 O(K) 串行前向**——要产出 K 个候选 token 就要 K 次串行前向，这是起草阶段的结构性天花板。块扩散把它变成 **O(1) 单次前向出整块**。

**成果（博客自报，TPU v5p）**

| 指标 | 数值 |
|---|---|
| tokens/s 提升 | **平均 3.13×** |
| 峰值 | **接近 6×**（复杂数学任务） |
| DFlash vs EAGLE-3（端到端服务） | **2.29× vs 1.30×** |

**工程要点：双缓存架构**。TPU 高性能服务走 **paged attention + Pallas 内核**，而 DFlash 的**非因果块扩散与标准 paged attention 根本不兼容**。解法是：**target 继续用 paged KV cache**（保住 Pallas 内核性能），**draft 走专用的静态 on-device JAX 数组**路径。

> **口径警示**：这 3.13× 是**特定硬件（TPU v5p）+ 特定引擎（vLLM TPU）+ 特定任务分布**下的数字，**不可与 GPU 上的 DFlash 报告值、或其他论文的加速比直接比较**。详见 [speculative-edge-cloud-hardware.md](speculative-edge-cloud-hardware.md)。

### 3.4.7 与 EAGLE-3 的本质差异

- **EAGLE-3**：draft 模型仍是**自回归**的，逐个生成 token，依赖树状验证并行化
- **DFlash / DSpark**：draft 模型是**扩散/块式**的，单次前向生成整个块，天然并行；DSpark 额外在**验证侧**做置信度驱动的变长裁剪
- **BASTION**：在块扩散之上再引入**动态树**与**在线延迟估计**，把"块扩散的边缘分布问题"用树搜索补回来
- **trade-off**：块级并行在 wall-clock 上更优，但块内 token 的**联合分布建模难度更高**（BASTION 明确指出"逐位置边缘分布的贪心路径抓不住 target 偏好轨迹"），可能导致接受率波动；因此**验证预算分配**成为与草稿质量同等重要的变量

---

## 3.5 检索式方法（2023-2024）

检索式投机解码完全绕过模型训练，从外部语料库或历史生成中检索候选。

### 3.5.1 REST（NAACL 2024）

- **从语料库检索 n-gram**：将大规模文本语料预索引为 n-gram 库
- 生成时检索与当前后缀匹配的候选续写
- **零训练成本**，但依赖语料库覆盖度
- **加速比**：1.5-2.5×

### 3.5.2 PLD（Prompt-Lookup Decoding, Saxena 2023）

- **Prompt 本地 n-gram 匹配**：仅在当前 prompt 的已生成部分中检索匹配片段
- 利用输入 prompt 的局部冗余（如重复代码模式、文档模板）
- 实现极简，无需外部语料库

### 3.5.3 SAM Decoding（2024-11）

- **后缀自动机（Suffix Automaton）** 高效检索，把 n-gram 匹配复杂度降至线性
- arXiv 2411.10666（2024-11-16），作者 Yuxuan Hu, Ke Wang, Xiaokang Zhang, Fanjin Zhang, Cuiping Li, Hong Chen 等

### 3.5.4 其他检索式方法

- **Token Recycling**：缓存 top-k 下一个 token，在相似上下文间复用
- **非拉丁语系的字典式草稿**：见 [speculative-domain-language.md](speculative-domain-language.md)

---

## 5.5 扩散语言模型的竞争

> 本节对应主报告"五、当前技术瓶颈与优化方向"中的相关条目，在此展开详细分析。

**新范式冲击**：

- **I-DLM**（*Introspective Diffusion Language Model*，arXiv 2604.11035）是**从 Qwen3-8B 转换**而来的扩散语言模型，自述"在 15 个 benchmark 上匹配同规模 AR 质量"，并提出 **Introspective Strided Decoding (ISD)**：单趟生成 + 验证（采用 **p/q 接受判据**）。可直接经 SGLang 服务（paged KV cache、连续批处理、CUDA graph），自述在**高并发下**吞吐比此前 DLM 高 **2.9–4.1×**。
- 关键差别：I-DLM 的"生成 + 验证"**内建在同一个模型里**，不是 draft-target 两段式；但它的验证判据（p/q 接受）与投机解码的经典判据**同源**。

**投机解码的防御性优势**：

- **无损保证**：投机解码的验证步骤严格保证输出分布等价（在 T=0 与满足 §[stochastic 章节](speculative-stochastic-verification.md)前提时）；扩散模型在强并行下可能精度下降
- **即插即用**：投机解码可叠加于任意 AR 模型；扩散模型需从头训练或做模型转换
- **互补而非替代**：**Nemotron-Labs-Diffusion (NLD)**（arXiv 2607.05722，2026-07-07，Yonggan Fu, Lexington Whalen, Abhinav Garg, Chengyue Wu 等，NVIDIA 等）提出**统一自回归、扩散与自投机解码的三模态语言模型**，证明 AR 与 Diffusion 可**联合训练、共享权重**
- **合流信号**：DFlash/DSpark 本身就是"把扩散/块式生成塞进投机解码框架"——两者不是竞争关系，而是**正在互相吸收**

---

## 参考文献

### 块扩散方法

| # | 论文 / 来源 | 年份 | 链接 | 可靠性 |
|---|---|---|---|---|
| 1 | DFlash, *Block Diffusion for Flash Speculative Decoding* | ICML 2026, arXiv 2602.06036（2026-02-05） | https://icml.cc/virtual/2026/poster/64301 | 高（会议 + 预印本） |
| 2 | DSpark in SGLang, *Speculative Decoding with Confidence-Driven, Variable-Length Verification* | 2026-07-06 | https://www.lmsys.org/blog/2026-07-06-dspark-sglang | 中（官方集成博客，自测数字） |
| 3 | BASTION, *Budget-Aware Speculative Decoding with Tree-structured Block Diffusion Drafting* | arXiv 2605.29727（2026-05-28） | https://arxiv.org/abs/2605.29727 | 中（预印本） |
| 4 | CAST, *Inference-Cost-Aware Dynamic Tree Construction for Efficient Inference in LLMs* | ICLR 2026 | https://papernotes.org/ICLR2026/llm_efficiency/inference-cost-aware_dynamic_tree_construction_for_efficient_inference_in_large_/ | 中（**二手解读页**） |
| 5 | Google Developers Blog, *3X speedups with diffusion-style speculative decoding on TPUs* | 2026-05-04 | https://developers.googleblog.com/supercharging-llm-inference-on-google-tpus-achieving-3x-speedups-with-diffusion-style-speculative-decoding/ | 中（官方工程博客） |
| 6 | vLLM, *Adaptive Verification*（验证预算的官方口径） | 官方文档 | https://docs.vllm.ai/en/latest/features/speculative_decoding/adaptive_verification/ | 高 |

### 检索式方法

| # | 论文 | 年份 | 链接 | 可靠性 |
|---|---|---|---|---|
| 7 | REST, *Retrieval-Based Speculative Decoding*, NAACL 2024 | 2024 | https://arxiv.org/abs/2311.08252 | 高 |
| 8 | PLD, *Prompt Lookup Decoding* | 2023 | https://github.com/apoorvumang/prompt-lookup-decoding | 高 |
| 9 | SAM Decoding, *Speculative Decoding via Suffix Automaton* | 2024-11 | https://arxiv.org/abs/2411.10666 | 高 |

### 扩散语言模型（竞争/合流范式）

| # | 论文 | 年份 | 链接 | 可靠性 |
|---|---|---|---|---|
| 10 | I-DLM, *Introspective Diffusion Language Model*（从 Qwen3-8B 转换，ISD 单趟生成+验证） | 2026-04 | https://arxiv.org/abs/2604.11035 | 中（预印本 + HF 模型卡） |
| 11 | NLD, *Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding* | 2026-07-07 | https://arxiv.org/abs/2607.05722 | 中（预印本，NVIDIA 等） |

> **v1 链接修复记录**：v1 报告中 I-DLM 与 NLD 的链接为占位符（编号形如 `2505.xxxxx`，实测不可达），本轮已替换为可核验的 arXiv 编号（2604.11035 / 2607.05722）。DFlash 的 arXiv 编号（2602.06036）也已由 ICML 2026 poster 与 arXiv 页面双向确证。

---

> **报告说明**：本报告所有技术细节均来自公开发表的论文、arXiv 预印本、官方技术博客及开源项目文档。2023-2025 年方法的信息可靠性普遍较高（经同行评审）；2026 年方法多为 arXiv 预印本或官方集成博客，尚未经过完整同行评审，建议读者直接查阅原始论文验证。加速比数据受测试条件影响显著，跨论文对比需谨慎。**块扩散方法的收益高度依赖 batch / 并发度——在 batch=1（memory-bound）与高并发（compute-bound）下结论相反，务必同时报出接受率与平均接受长度。**
>
> *数据截至 2026-10-16（v1：2026-06-06）。*
