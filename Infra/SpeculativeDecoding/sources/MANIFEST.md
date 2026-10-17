# 原文清单 · SpeculativeDecoding

> 本仓库**只存清单与我们的精读分册**（`papers/*.md`），**不存论文全文**（PDF 或转出的 markdown 都不入库）。
> 需要回看原文时：按下面的 arXiv 链接现取；本地缓存可选（`~/Documents/paper-cache/<id>@<版本>/`），缓存同样不入库。
> **代码仓库**只记录 `仓库 @ commit` 与用到的 `文件:行`，**源码不入库**。

## 1. 论文（6 个分册覆盖 8 篇论文）

| # | 分册（我们的精读） | arXiv ID | 版本 | 版本日期 | 标题（arXiv 元数据，逐条核实） | 第一作者（核实） | license | 去哪找原文 |
| --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | [`papers/2401.15077-eagle-series.md`](<../papers/2401.15077-eagle-series.md>) | 2401.15077 | v3 | 2025-03-04 | EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty（EAGLE-1） | Li, Yuhui | arXiv.org perpetual non-exclusive | https://arxiv.org/abs/2401.15077 |
| 2 | 同上（EAGLE-2 分节） | 2406.16858 | v2 | 2024-06-30 | EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees | Li, Yuhui | arXiv.org perpetual non-exclusive | https://arxiv.org/abs/2406.16858 |
| 3 | 同上（EAGLE-3 分节） | 2503.01840 | v3 | 2025-04-23 | EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test | Li, Yuhui | arXiv.org perpetual non-exclusive | https://arxiv.org/abs/2503.01840 |
| 4 | [`papers/2401.10774-medusa.md`](<../papers/2401.10774-medusa.md>) | 2401.10774 | v3 | 2024-06-14 | Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads | Cai, Tianle | CC BY 4.0 | https://arxiv.org/abs/2401.10774 |
| 5 | [`papers/2402.02057-lookahead.md`](<../papers/2402.02057-lookahead.md>) | 2402.02057 | v1 | 2024-02-03 | Break the Sequential Dependency of LLM Inference Using Lookahead Decoding | Fu, Yichao | arXiv.org perpetual non-exclusive | https://arxiv.org/abs/2402.02057 |
| 6 | [`papers/2305.09781-specinfer.md`](<../papers/2305.09781-specinfer.md>) | 2305.09781 | v4 | 2024-04-01 | SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification | Miao, Xupeng | CC BY 4.0 | https://arxiv.org/abs/2305.09781 |
| 7 | [`papers/2408.11049-magicdec.md`](<../papers/2408.11049-magicdec.md>) | 2408.11049 | v5 | 2025-04-02 | MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding | Sadhukhan, Ranajoy | CC BY 4.0 | https://arxiv.org/abs/2408.11049 |
| 8 | [`papers/2609.21827-rheosampling.md`](<../papers/2609.21827-rheosampling.md>) | 2609.21827 | v1 | 2026-09-18 | RheoSampling: Resolving the One-Hot Dilemma in Stochastic Dynamic-Tree Speculative Decoding | Hu, Qiao | arXiv.org perpetual non-exclusive | https://arxiv.org/abs/2609.21827 |

## 2. 代码仓库（2 个实现核验 + 1 个官方参考实现）

| # | 分册/用途 | 仓库 | commit | 日期 | 用到的文件:行 | license |
| --: | :-- | :-- | :-- | :-- | :-- | :-- |
| 9 | [vLLM 实现核验](../papers/vllm-implementation.md) | `vllm-project/vllm` | `2b85d9cb65c1f56c347cb7f56f1596a6b8b28373` | 2026-10-17 | `config/speculative.py:533,604`；`v1/spec_decode/llm_base_proposer.py:257–261,449–509`；`v1/sample/rejection_sampler.py:410–520,949,1128`；`v1/spec_decode/metrics.py:107–122`；`v1/worker/gpu_model_runner.py:4714–4741,4987–4990` | Apache-2.0 |
| 10 | [SGLang 实现核验](../papers/sglang-implementation.md) | `sgl-project/sglang` | `2a08e261ecd4cdfb04ec354f9005f18b88108b7d` | 2026-10-16 | `speculative/eagle_worker_v2.py:178–180,648–657,676–681,727–733`；`speculative/eagle_utils.py:157,384,741,860–916,947–1044`；`speculative/eagle_info.py:35,162` | Apache-2.0 |
| 11 | [EAGLE 分册 §8.1 + report §8.1](../papers/2401.15077-eagle-series.md) | `SafeAILab/EAGLE` | `cb7e0841fe0c206c6ed74a197ad5e2a1f13f5a2b` | 2026-02-20 | `eagle/model/utils.py:398–399`（`qx=1.0`）；`eagle/model/ea_model.py:270,452`；`eagle/modeling_eagle.py:1427` | 未核实（仓库根有 LICENSE，未逐字读） |

## 3. 版本与引用规则

1. **版本日期**取 arXiv 元数据的 `updated`（最新版本），不是首次提交日；同一论文的后续版本可能改数字，引用以本表版本为准。
2. **标题/第一作者**已于本轮逐条回查 `export.arxiv.org/api`；完整作者列表未逐字核对，正式引用请回查原文。
3. **license** 来自论文 HTML 页脚（`License: ...`）；`arXiv.org perpetual non-exclusive` 不授予再分发权，因此本仓库不存全文。
4. **代码引用**一律 `仓库@commit:文件:行`；换 commit 后行号可能漂移，引用时保留 SHA。
5. **本地缓存（可选、不入库）**：`~/Documents/paper-cache/<arXiv-ID>@<版本>/`；本清单不依赖缓存存在。

## 4. 未入库/未设分册的候选

DFlash / DSpark / BASTION / HASS / DistillSpec / Sequoia 等未设分册的候选，处置理由见 [CANDIDATES.md](CANDIDATES.md)；其中只有 4 条在本轮重新核实过 ID，其余按类别排除、不给编号。
