# 原文清单 · SpeculativeDecoding

> 本仓库**只存清单与我们的精读分册**（`papers/*.md`），**不存论文全文**（PDF 或转出的 markdown 都不入库）。
> 需要回看原文时：按下面的 arXiv 链接现取；本地缓存可选（`.paper-cache/<id>@<版本>/`），缓存同样不入库。
> **代码仓库**只记录 `仓库 @ commit` 与用到的 `文件:行`，**源码不入库**。

## 1. 论文（20 个精读分册覆盖 22 篇论文）

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
| 9 | [`papers/2610.08678-secure-sd.md`](<../papers/2610.08678-secure-sd.md>) | 2610.08678 | v1 | 2026-10-06 | Secure Speculative Decoding for Large Language Models | Zhang, Yichi | Not exposed in retrieved Atom metadata; not verified | https://arxiv.org/abs/2610.08678v1 |
| 10 | [`papers/2608.13524-dartree.md`](<../papers/2608.13524-dartree.md>) | 2608.13524 | v1 | 2026-08-13 | DARTree: Speculative Diffusion Decoding with Autoregressive Draft Trees | Li, Tianyi | CC BY 4.0 | https://arxiv.org/abs/2608.13524v1 |
| 11 | [`papers/2609.33184-specstream.md`](<../papers/2609.33184-specstream.md>) | 2609.33184 | v1 | 2026-09-27 | Resource-Efficient Speculative Decoding for Long-Context LLM Serving | Li, Fei | CC BY 4.0 | https://arxiv.org/abs/2609.33184v1 |
| 12 | [`papers/2610.23787-dlite.md`](<../papers/2610.23787-dlite.md>) | 2610.23787 | v1 | 2026-10-16 | DLite: History-free Speculative Decoding for Agentic AI | Xu, Jiaming | CC BY 4.0 | https://arxiv.org/abs/2610.23787v1 |
| 13 | [`papers/2601.05724-hsd.md`](<../papers/2601.05724-hsd.md>) | 2601.05724 | v2 | 2026-03-02 | Overcoming Joint Intractability with Lossless Hierarchical Speculative Decoding | Zhou | CC BY 4.0 | https://arxiv.org/abs/2601.05724v2 |
| 14 | [`papers/2602.16994-delayed-tree.md`](<../papers/2602.16994-delayed-tree.md>) | 2602.16994 | v1 | 2026-02-19 | Dynamic Delayed Tree Expansion For Improved Multi-Path Speculative Decoding | Thomas | CC BY 4.0 | https://arxiv.org/abs/2602.16994v1 |
| 15 | [`papers/2606.01813-caddtree.md`](<../papers/2606.01813-caddtree.md>) | 2606.01813 | v1 | 2026-06-01 | CaDDTree: Cost-Aware Diffusion Draft Trees for Speculative Decoding | Zhang, Shuai | CC BY 4.0 | https://arxiv.org/abs/2606.01813v1 |
| 16 | [`papers/2610.07350-tlar.md`](<../papers/2610.07350-tlar.md>) | 2610.07350 | v1 | 2026-10-05 | Trajectory-Retrieval Speculative Decoding: When Does a Model’s Own History Help? | Dai, Yuyang | CC0 1.0 | https://arxiv.org/abs/2610.07350v1 |
| 17 | [`papers/2602.06036-dflash.md`](<../papers/2602.06036-dflash.md>) | 2602.06036 | v2 | 2026-05-28 | DFlash: Block Diffusion for Flash Speculative Decoding | Chen, Jian | CC BY 4.0 | https://arxiv.org/abs/2602.06036v2 |
| 18 | [`papers/2606.02091-dflare.md`](<../papers/2606.02091-dflare.md>) | 2606.02091 | v2 | 2026-06-02 | DFlare: Scaling Up Draft Capacity for Block Diffusion Speculative Decoding | Zhang, Jiebin | CC BY 4.0 | https://arxiv.org/abs/2606.02091v2 |
| 19 | [`papers/2604.12989-ddtree.md`](<../papers/2604.12989-ddtree.md>) | 2604.12989 | v1 | 2026-04-14 | Accelerating Speculative Decoding with Block Diffusion Draft Trees | Ringel, Liran | arXiv.org perpetual non-exclusive | https://arxiv.org/abs/2604.12989v1 |
| 20 | [`papers/2607.22634-presto.md`](<../papers/2607.22634-presto.md>) | 2607.22634 | v1 | 2026-06-20 | PRESTO: Prefix-Aligned Tree Drafting for Diffusion Speculative Decoding | Wang, Zheng | CC BY 4.0 | https://arxiv.org/abs/2607.22634v1 |
| 21 | [`papers/2509.18085-spiffy.md`](<../papers/2509.18085-spiffy.md>) | 2509.18085 | v4 | 2026-06-11 | Structuring The Future: Diffusion LLM Speculative Decoding via Calibrated Draft Graphs | Agrawal, Sudhanshu | CC BY 4.0 | https://arxiv.org/abs/2509.18085v4 |
| 22 | [`papers/2606.08048-poe-bridge.md`](<../papers/2606.08048-poe-bridge.md>) | 2606.08048 | v1 | 2026-06-06 | Diffusion Language Model Parallel Decoding via Product-of-Experts Bridge | Shi, Juntong | CC BY 4.0 | https://arxiv.org/abs/2606.08048v1 |

## 2. 代码仓库（4 个实现/代码切面核验 + 1 个官方参考实现）

| # | 分册/用途 | 仓库 | commit | 日期 | 用到的文件:行 | license |
| --: | :-- | :-- | :-- | :-- | :-- | :-- |
| 23 | [DARTree 精读](../papers/2608.13524-dartree.md) | `VILA-Lab/DARTree` | `5bb3240e806a9ccdc2c65e98d3bc40998a9845f1` | 2026-08-13 | `run_dartree.py:20–81`；`eval_dartree.py:586–760`（supertree）；`utils/draft_model.py:397–507`（draft/verify/commit） | 未核实（快照根目录未发现 LICENSE） |
| 24 | [DLite 精读](../papers/2610.23787-dlite.md) | `SJTU-DAI-Sys/DLite` | `e0aa3d55d792fc9088231e13779678bcfdb3188f` | 2026-10-21 | `dlite/engine.py:67–106`；`dlite/modeling/dlite.py:345–461,503–735`；`dlite/modeling/sequential_head.py:72–87`；`dlite/utils/sampling.py:73–125` | MIT |
| 25 | [vLLM 实现核验](../papers/vllm-implementation.md) | `vllm-project/vllm` | `2b85d9cb65c1f56c347cb7f56f1596a6b8b28373` | 2026-10-17 | `config/speculative.py:533,604`；`v1/spec_decode/llm_base_proposer.py:257–261,449–509`；`v1/sample/rejection_sampler.py:410–520,949,1128`；`v1/spec_decode/metrics.py:107–122`；`v1/worker/gpu_model_runner.py:4714–4741,4987–4990` | Apache-2.0 |
| 26 | [SGLang 实现核验](../papers/sglang-implementation.md) | `sgl-project/sglang` | `2a08e261ecd4cdfb04ec354f9005f18b88108b7d` | 2026-10-16 | `speculative/eagle_worker_v2.py:178–180,181–182,648–657,671–684,727–733`；`speculative/eagle_utils.py:157,384,741,860–916,947,1000–1013,1032–1038`；`speculative/eagle_info.py:35,162` | Apache-2.0 |
| 27 | [EAGLE 分册 §8.1 + report §8.1](../papers/2401.15077-eagle-series.md) | `SafeAILab/EAGLE` | `cb7e0841fe0c206c6ed74a197ad5e2a1f13f5a2b` | 2026-02-20 | `eagle/model/utils.py:398–399`（`qx=1.0`）；`eagle/model/ea_model.py:270,452`；`eagle/modeling_eagle.py:1427` | 未核实（仓库根有 LICENSE，未逐字读） |

逐条锚点、支撑断言与行号更正历史见 [CODE-AUDIT.md](CODE-AUDIT.md)。

## 3. 版本与引用规则

1. **版本日期**取 arXiv 元数据的 `updated`（最新版本），不是首次提交日；同一论文的后续版本可能改数字，引用以本表版本为准。
2. **标题/第一作者**已于本轮逐条回查 `export.arxiv.org/api`；完整作者列表未逐字核对，正式引用请回查原文。
3. **license** 来自论文 HTML 页脚（`License: ...`）；`arXiv.org perpetual non-exclusive` 不授予再分发权，因此本仓库不存全文。
4. **代码引用**一律 `仓库@commit:文件:行`；换 commit 后行号可能漂移，引用时保留 SHA。
5. **本地缓存（可选、不入库）**：`.paper-cache/<arXiv-ID>@<版本>/`；本清单不依赖缓存存在。

## 4. 未入库/未设分册的候选

DSpark / BASTION / HASS / DistillSpec / Sequoia 等仍未设分册的候选，处置理由见 [CANDIDATES.md](CANDIDATES.md)；其中只有 4 条在本轮重新核实过 ID，其余按类别排除、不给编号。

## SecureSD evidence scope (2026-10-22)

- Fixed paper: `2610.08678v1`, first submitted 2026-10-06, PDF SHA-256 `3d1ca0ac3e00a20606ab79fc22848678c52c18139d8b31d54d27d471fc53b675`; inspected §3–§7, including threat model, experimental setup, verifier definition, theory, and Tables 1/5/6/7. The arXiv Atom comment says “18 pages, accepted by IEEE S&P 2027”; conference proceedings and DOI were not independently checked.
- Model identities named in the paper are retained in the note. No checkpoint hashes/revisions are supplied in the paper; no model weights or runtime were tested.
- The arXiv Atom metadata exposes no license field in this retrieval; no redistribution rights are inferred.
- Author's code/benchmark URL is listed in the paper; its repository and commit were not inspected in this paper-only batch.

## DARTree, SpecStream and DLite evidence scope (2026-10-22)

- Fixed PDFs: `2608.13524v1` SHA-256 `aa243bef0fe85e125b01fa18d747ffa93c82ab8a6fe68a677d82f28072b6cca3`; `2609.33184v1` SHA-256 `75e268a5866351b41e512965e06d70a1bc72e7e62cd01cd93537f0cb5707603b`; `2610.23787v1` SHA-256 `0c0906929baf8182f11692ebe8a3916c95df8a9fff9d49c56e2864ea8ef244f8`.
- DARTree repository snapshot was inspected with code-researcher map/runtime/design workflow at `VILA-Lab/DARTree@5bb3240e806a9ccdc2c65e98d3bc40998a9845f1`. Repo scan found no test files; no experiment was run.
- DLite official inference snapshot was inspected at `SJTU-DAI-Sys/DLite@e0aa3d55d792fc9088231e13779678bcfdb3188f`. Four test files are present; they were not run. Paper training recipe and inference release are distinct; the repo README states benchmark output-token equality is not checked.
- SpecStream paper says implementation uses SGLang 0.5.17 but gives no author repository URL or commit in the inspected paper. The source claim is paper-only; no code audit or reproduction.
- No model checkpoint revision/hash is pinned by these papers; no weights were downloaded. Results remain author-reported and tied to their stated hardware, workload, settings and baseline.
