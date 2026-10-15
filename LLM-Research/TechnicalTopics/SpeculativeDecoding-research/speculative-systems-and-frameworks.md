# 投机解码：系统级优化与框架生态

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、arXiv 预印本、官方框架文档、开源 PR 与工程博客整理生成。部分 2025-2026 年信息可能未经同行评审，建议读者直接查阅原始论文/文档验证。加速比数据受测试条件（模型规模、硬件、任务类型、batch、并发度）影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮更新；v1 为 2026 年 6 月）
> **本次改动**：新增「① 服务端调度：验证预算与上下文窗口」「② 指标口径」「六、框架与工具生态（刷新）」；修复/标注 v1 遗留的占位链接。
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦系统级优化方法与推理框架生态。主报告见 [report.md](report.md)；端侧与硬件约束见 [speculative-edge-cloud-hardware.md](speculative-edge-cloud-hardware.md)。
> **证据等级约定**：**[精读原文]**、**[摘要级]**、**[二手]**。
> **等级规则**：每条结论只取**一个主等级**（精读原文 / 摘要级 / 二手 / 受限核验）；**混合来源取最弱等级**并在正文注明来源类型（如 `[精读原文（vLLM 官方文档）]`）；不使用 `A + B`、`A（摘要层）` 这类复合标签。

---

## 3.7 系统级优化

| 方法 | 年份 | 核心贡献 | 信息可靠性 |
|------|------|---------|-----------|
| **SpecInfer** | 2023-2024 | 树状并行验证，将多个 draft 路径合并为树状注意力 | 高 |
| **Sequoia** | 2024 | 硬件感知树优化和调度，根据 GPU 带宽动态调整树深度 | 高 |
| **Mirror-SD** | 2024-2025 | 异构设备并行草案-验证（如 draft 在 CPU/小 GPU，target 在大 GPU） | 待确证（v1 占位链接） |
| **TriForce** | 2025 | 分层 KV 缓存加速长上下文投机解码 | 待确证（v1 占位链接） |
| **Speculative Decoding Scaling Laws** | 2025 | 系统研究草案模型设计规律，给出 draft 规模与加速比的量化关系 | 待确证（v1 占位链接） |
| **CAST** ⭐新增 | 2026 (ICLR) | 把推理成本（GPU 型号、batch）显式纳入动态建树 | 中（二手解读页） |
| **BASTION** ⭐新增 | 2026 (arXiv) | 预算感知 + 树状块扩散，按边际收益停止扩张 | 中（预印本） |
| **DSpark** ⭐新增 | 2026 | 半自回归块草稿 + 置信度驱动的变长验证 | 中（官方集成博客） |

**系统级关键发现（v1 保留）**：
- **树状验证的硬件瓶颈**：树状注意力虽提升理论并行度，但分支因子增加导致内存访问模式不规则，实际 GPU 利用率可能下降
- **异构并行是扩展路径**：Mirror-SD 证明将 draft 卸载到低端设备（CPU、边缘 GPU）可在几乎不占用 target GPU 资源的情况下实现加速

**系统级关键发现（本轮新增）**：
- **投机解码的收益随负载恶化，这是系统层面的结构性问题**。见 §①。
- **指标的报法本身就是系统结论的一部分**。见 §②。

---

## ① 服务端调度：验证预算与上下文窗口（本轮新增）

### ①.1 验证预算：batch 决定这笔交易划不划算 **[精读原文]**

vLLM 官方 *Adaptive Verification* 文档把"投机解码是否划算"讲得最明确：

> **batch size = 1 时这笔交易很划算**：GPU 处于 **memory-bound**，有多余算力，额外的 draft token 接近免费。
> **batch size = 256 时这笔交易很微妙**：draft token 开始与真实 token **争夺同样的算力**，**每一个被拒绝的 token 都是被浪费的算力**；足够多时，**吞吐会下降**。
> 原因在于**逐位置的接受率衰减很快**。当 GPU 还是 memory-bound 时那个槽位基本免费、值得赌一把；一旦饱和，这次赌博就有真实的吞吐成本。
> **交叉点随负载与负载相关的接受率移动，因此不存在一个静态的 `num_speculative_tokens` 能适配所有并发度。**

**vLLM 的 adaptive verification 机制**：

| 环节 | 做法 |
|---|---|
| 打分 | 每个 **(request, position)** 草稿槽按其**存活概率**打分（该请求逐位置接受率估计的连乘） |
| 准入 | 按分数从高到低准入，**直到耗尽全局预算** |
| 跨请求竞争 | 槽位**跨请求竞争**——"置信请求的位置 5 可以排在不置信请求的位置 1 之前"；一个请求可能保留完整块，另一个可能在验证一两个 token 后就被裁剪 |
| 预算来源 | **启动时 profiled 的成本模型**：在每个 shape 上测这一步的成本，再选出使"**期望接受 token 数/秒**"最大的 token 数 |
| 实际效果 | **一套配置可覆盖整个负载区间**，基本不再需要按部署调 `num_speculative_tokens` |

**逐位置接受率估计的两个来源**：

| 来源 | 适用条件 |
|---|---|
| **Confidence head** | **DSpark checkpoint 自带训练好的 confidence head** 时直接使用其预测 |
| **Online acceptance estimator** | 其他 drafter（EAGLE、MTP、DFlash、standalone draft）：用小 logistic 模型从 draft logits 预测接受率，**服务过程中依据 target 的验证结果持续重新校准** |

**支持范围**：基于模型的 drafter（**EAGLE、MTP、DFlash、DSpark** 与 standalone draft 模型）。默认关闭，通过 `enable_adaptive_verification` 开启。

### ①.2 上下文窗口：草稿注意力必须被界限 **[精读原文]**

**vLLM PR #61261**（`[Spec Decode] Add draft_context_window to bound DFlash/DSpark draft attention`，作者 brokenlander，提交 2026-10-12）提出的问题非常具体：

> **DFlash/DSpark drafter 一旦上下文超出它们被训练时的长度，就可能丢掉大部分接受率**——**即使 target 侧什么都没变**。

**解法**：新增一个 opt-in 的 speculative config 字段，**把 draft 的注意力限制在最近 N 个上下文 token**。

**实现要点（来自 PR 描述）**：

- 以**完整的 block-table 条目**为单位丢弃最旧的上下文（`block_size * dcp_size` 个位置，按 draft KV 组求 lcm），做法是**把每个请求的 draft block-table 行左移并缩短 draft seq_lens**
- **位置保持绝对值**，因此已缓存的 key 保留其 RoPE 相位
- 该移位在 **FULL CUDA graph 读取的缓冲区**上 eager 执行，**不引入 host sync**
- **target 的验证逻辑不变**
- **只对 dflash/dspark 生效**，且在 **Model Runner V1 上被拒绝**
- 文档字段：`draft_context_window`，类型 `integer >= 1`，默认 `None`，**仅 Model Runner V2**

**文档给出的用法**：

```bash
vllm serve <target-model> \
  --speculative-config '{
    "method": "dspark",
    "model": "<dspark-draft-model>",
    "num_speculative_tokens": 3,
    "draft_context_window": 32768
  }'
```

> **为什么这条 PR 值得写进系统章节**：它把"草稿模型与训练分布失配"这个**算法侧问题**，转成了**系统侧可配置的运行时参数**。这与 Attention Drift（[speculative-draft-training-2026.md](speculative-draft-training-2026.md) §3）从架构侧修同一类问题形成互补。

### ①.3 DSpark 的工程落地：把调度变成 wall-clock **[精读原文]**

SGLang 官方博客（2026-07-06）给出 DSpark 集成的四条工程要点：

1. **ragged verify + 完整 CUDA graph**：裁剪过的 batch **重放真正更小的图**，而不是填充过的图
2. **overlap-aware 投机路径**：把调度器隐藏在 forward 之后
3. **cost-table profiler**：让调度器**在线**为每个请求确定验证预算
4. **可观测性**：暴露"裁剪后本会被掩盖的接受上限"

**自测结论**（DeepSeek-V4-Flash on H200，DP-attention 4 卡，并发 1→256）：**DSpark 在整个并发区间给出最好的吞吐/延迟权衡**，明显优于 MTP 与非投机基线。**博客明确声明**："硬件、引擎、流量都与论文不同，我们复现的是**机制与曲线形状**，不是论文数字。"

---

## ② 指标口径（本轮新增，必读）

### ②.1 acceptance rate 与 mean accepted length 必须成对报告 **[精读原文]**

vLLM *Per-Request Acceptance Metrics* 文档给出的精确定义：

| 字段 | 定义 | 关键性质 |
|---|---|---|
| `mean_acceptance_length` | $1 + \text{num\_accepted\_draft\_tokens} / \text{num\_spec\_steps}$ | **每次验证步平均产出 token 数（含必得的 bonus token）**，范围 $[1, k+1]$ |
| `draft_acceptance_rate` | $\text{num\_accepted\_draft\_tokens} / \text{num\_draft\_tokens}$ | **被提议草稿中被接受的比例** |
| `acceptance_histogram` | 长度 $k+1$ 的数组，下标 $j$ = 恰好接受 $j$ 个草稿 token 的步数 | 排除 bonus token |
| `num_spec_steps` | 验证步数（等于 histogram 之和） | 对应 Prometheus 计数器 `vllm:spec_decode_num_drafts_total` |
| `num_draft_tokens` | 总提议草稿数，**已扣除被结构化输出约束作废的草稿** | 对应 `vllm:spec_decode_num_draft_tokens_total` |
| `per_step_accepted` / `per_step_drafted`（detailed 模式） | 逐步的接受/提议数 | **变长草稿（如 adaptive speculation）不需要改 schema** |

**两个指标的分母不同**（一个按**验证步**、一个按**提议 token**），因此：

> **必须成对报告。** 加深草稿树通常会**降低** acceptance rate（多提议了低命中率的 token）却**提高** mean accepted length（一旦命中就一次吃更多）。只看其中之一会得出相反的系统结论。

**口径警示**：`num_draft_tokens` **已扣除被结构化输出约束作废的草稿** → **开启语法/JSON 约束后，acceptance rate 的分母会变小**，与无约束实验**不可直接对比**（详见 [speculative-domain-language.md](speculative-domain-language.md) §3.3）。

### ②.2 可观测性：`/metrics` 与逐请求字段的关系 **[精读原文]**

- 服务端**聚合计数**在 `/metrics`（Prometheus），逐请求字段是其"单请求对应物"
- 逐请求字段求和后**可与聚合计数对账**（`num_spec_steps` ↔ `vllm:spec_decode_num_drafts_total` 等）；但聚合计数**也统计 n>1 的请求**，故只有全 n=1 负载下总和才完全吻合
- 逐请求 `metrics.speculative_decoding` **仅在单序列请求（n=1）且开启 `--per-request-spec-decode-metrics`** 时出现，**n>1 时为 null**
- 流式响应中，metrics 挂在**最后一个 usage chunk** 上，需开启 usage 上报（`stream_options.include_usage: true`）

---

## 六、框架与工具生态（本轮刷新）

| 框架/工具 | 支持情况 | 备注 |
|----------|---------|------|
| **vLLM** | 原生 EAGLE-1 / EAGLE-3；**DFlash / DSpark**（含 `draft_context_window`，PR #61261）；**adaptive verification**（EAGLE/MTP/DFlash/DSpark/standalone） | 最广泛部署的开源推理框架 |
| **SGLang** | EAGLE-2 / EAGLE-3、**MTP**、standalone draft model、**n-gram speculation**；**DSpark**（含 ragged verify + CUDA graph + cost-table profiler） | 官方文档已把投机解码**常规化**为 Advanced Features 的正式章节；官方基准：LLaMA-3.1-8B-Instruct / MT-Bench / 1×H100 上 EAGLE-2 = 1.54×、**EAGLE-3 = 2.36×**（158.34 → 373.25 tokens/s） |
| **llama.cpp** | **MTP 进入主线**（把同一 GGUF 中的 MTP head 接成 draft context）；**DSpark** 有独立 PR（#25173） | 端侧/本地推理的关键信号 |
| **Ollama** | 在 MLX runner 中加入 **DFlash** 投机解码 | **[二手]** 来源为 RunAnywhere Inference Radar 2026-W20 周报，本轮未取一手 PR 核验 |
| **TensorRT-LLM** | NVIDIA 推理优化，支持投机解码 | 闭源，针对 NVIDIA 硬件优化 |
| **SpecBundle** | 生产级 EAGLE-3 草案模型集合 | SpecForge 发布，覆盖主流模型（一手来源见 [speculative-draft-training-2026.md](speculative-draft-training-2026.md) 参考文献 6） |
| **Red Hat AI** | 发布 Qwen3-8B-speculator.eagle3 | 企业级部署方案 |

**生态趋势（本轮更新）**：

1. **投机解码从"研究特性"变成"默认基础设施"**。llama.cpp 把 MTP 接进主线、SGLang 把它常规化为文档章节、vLLM 持续把投机与 offload 相关工作并入 Blackwell 时代的服务版本。
2. **系统侧开始出现"专用的动态调度层"**：vLLM 的 adaptive verification 与 SGLang 的 DSpark 集成在做同一件事——**按负载与置信度动态决定验证多少**，而不是让用户静态设 `num_speculative_tokens`。
3. **草稿与上下文的失配被显式参数化**：`draft_context_window` 把"drafter 训练长度之外接受率崩塌"从隐性坑变成可配置项。
4. **指标可观测性被补齐**：逐请求 acceptance metrics + 与 Prometheus 的对账关系，使"到底变快还是变慢"第一次可以逐请求归因。

---

## 参考文献

### 系统级优化

| # | 论文 / 来源 | 年份 | 链接 | 可靠性 |
|---|------|------|------|--------|
| 1 | SpecInfer, *Accelerating Generative LLM Serving with Speculative Inference and Token Tree Verification* | 2023 | https://arxiv.org/abs/2305.09781 | 高 |
| 2 | Sequoia, *Sequoia: Scalable, Robust, and Hardware-aware Speculative Decoding* | 2024 | https://arxiv.org/abs/2402.12374 | 高 |
| 3 | Mirror-SD, *Heterogeneous Device Parallel Speculative Decoding* | 2024-2025 | ⚠️ **未确证**（v1 占位符 `2405.XXXXX`） | 未确证 |
| 4 | TriForce, *Hierarchical KV Cache for Long-Context Speculative Decoding* | 2025 | ⚠️ **未确证**（v1 占位符 `2502.XXXXX`） | 未确证 |
| 5 | Speculative Decoding Scaling Laws, *Scaling Laws for Draft Model Design* | 2025 | ⚠️ **未确证**（v1 占位符 `2503.XXXXX`） | 未确证 |
| 6 | QSpec, *Quantized Speculative Decoding* | 2025 | ⚠️ **未确证**（v1 占位符 `2504.XXXXX`） | 未确证 |
| 7 | HierSpec, *Hierarchical Speculative Decoding* | 2025 | ⚠️ **未确证**（v1 占位符 `2505.XXXXX`） | 未确证 |
| 8 | CAST, *Inference-Cost-Aware Dynamic Tree Construction for Efficient Inference in LLMs*, ICLR 2026 | 2026 | https://papernotes.org/ICLR2026/llm_efficiency/inference-cost-aware_dynamic_tree_construction_for_efficient_inference_in_large_/ | 中（**二手解读页**） |
| 9 | BASTION, *Budget-Aware Speculative Decoding with Tree-structured Block Diffusion Drafting* | 2026-05-28 | https://arxiv.org/abs/2605.29727 | 中（预印本） |

### 框架与文档（本轮新增/核验）

| # | 来源 | 日期 | 链接 | 证据等级 |
|---|------|------|------|---------|
| 10 | vLLM PR #61261, *Add draft_context_window to bound DFlash/DSpark draft attention* | 2026-10-12 | https://github.com/vllm-project/vllm/pull/61261 | **精读原文**（PR 描述 + diff 摘要） |
| 11 | vLLM, *Adaptive Verification* | 官方文档 | https://docs.vllm.ai/en/latest/features/speculative_decoding/adaptive_verification/ | **精读原文** |
| 12 | vLLM, *Per-Request Acceptance Metrics* | 官方文档 | https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/ | **精读原文** |
| 13 | SGLang, *DSpark in SGLang: Speculative Decoding with Confidence-Driven, Variable-Length Verification* | 2026-07-06 | https://www.lmsys.org/blog/2026-07-06-dspark-sglang | **精读原文**（官方集成博客，自测数字） |
| 14 | SGLang, *Speculative Decoding* 官方文档 | 2026-03-04 | https://mintlify.wiki/sgl-project/sglang/advanced/speculative-decoding | **精读原文** |
| 15 | llama.cpp PR #25173, *spec: add DSpark speculative decoding* | 2026 | https://github.com/ggml-org/llama.cpp/pull/25173 | 二手（标题级核验） |
| 16 | RunAnywhere Inference Radar 2026-W20（MTP 进 llama.cpp 主线 / Ollama DFlash） | 2026-05-14~20 | https://www.runanywhere.ai/newsletter/2026-W20 | 二手（周报） |

> **v1 链接修复记录（诚实说明）**：v1 中 Mirror-SD / TriForce / Scaling Laws / QSpec / HierSpec 的 arXiv 链接均为 `XXXXX` 形式的**占位符**，本轮实测该类 ID 返回 **HTTP 404**，**无法核验** → 已在表中统一标注「未确证」，**不做猜测性替换、不据此展开结论**。Sequoia 的链接由 v1 的 `2404.14311` 更正为**已核验的 `2402.12374`**（标题：*Sequoia: Scalable, Robust, and Hardware-aware Speculative Decoding*）。

---

> **报告说明**：本报告所有技术细节均来自公开发表的论文、arXiv 预印本、官方框架文档、开源 PR 与工程博客。本轮新增的第 10–14 项均为**一手来源且已精读**；第 15–16 项为标题级/二手核验，已在表中标注。**投机解码的收益强依赖 batch 与并发度——在 batch=1（memory-bound）与高并发（compute-bound）下结论相反；报告加速比时必须同时给出 acceptance rate 与 mean accepted length，并声明测试的并发度。**
>
> *数据截至 2026-10-16（v1：2026-06-06）。*
