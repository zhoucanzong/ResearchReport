# 代码锚点审计 · SpeculativeDecoding

> **用途**：把两篇代码分册（vLLM / SGLang）与 EAGLE 代码核验里用到的**每一条代码事实**钉成可复核清单：`仓库@commit:文件:行` ｜ 支撑哪句断言 ｜ 核验日期 ｜ 备注（含行号更正历史）。
> **核验日期**：2026-10-17（只读快照；源码不入库）。
> **配套分册**：[vLLM 实现](../papers/vllm-implementation.md)、[SGLang 实现](../papers/sglang-implementation.md)、[EAGLE 系列](../papers/2401.15077-eagle-series.md)。
> **复核方式**：`/tmp` 只读快照 + 行号对照脚本；逐条检查“目标行/区间内是否出现断言关键词”，39/39 命中（见 §4）。

## 1. vLLM @ `2b85d9cb65c1f56c347cb7f56f1596a6b8b28373`（2026-10-17，Apache-2.0）

| # | 锚点 | 支撑的断言 | 备注 |
| --: | :-- | :-- | :-- |
| 1 | `vllm/config/speculative.py:604` | `draft_sample_method` 默认 `greedy`；greedy 时草稿概率按 one-hot 处理 | 字段本体 + docstring |
| 2 | `vllm/config/speculative.py:533` | `rejection_sample_method` 默认 `standard` | 字段本体 |
| 3 | `vllm/config/speculative.py:533–553` | `synthetic` 模式参数：rates 长度/范围/单调不增 | 含 `synthetic_acceptance_rates/length` 文档 |
| 4 | `vllm/config/speculative.py:555` | `enable_adaptive_verification` 字段；注释限定 method=`dspark` | 原引 560 → 555（见 §3） |
| 5 | `vllm/config/speculative.py:1836–1841` | 异构词表只允许 `greedy`，probabilistic 被拒绝 | 校验逻辑 |
| 6 | `vllm/v1/spec_decode/llm_base_proposer.py:73` | `SpecDecodeBaseProposer` 是 vLLM 草稿基类 | 类定义 |
| 7 | `.../llm_base_proposer.py:112–114` | `parallel_drafting`（DFlash 一类并行草稿）开关 | 字段与派生槽位 |
| 8 | `.../llm_base_proposer.py:257–261` | `probabilistic` 只在 `standard` 下启用 | `_enable_probabilistic_draft_probs` |
| 9 | `.../llm_base_proposer.py:449–475` | probabilistic 用 `compute_probs_and_sample_next_token` 真采样 | 非 probabilistic / 全 greedy → argmax |
| 10 | `.../llm_base_proposer.py:477–486` | greedy 时 `_sample_draft_tokens` 直接返回 `(ids, None)` | 早退分支 |
| 11 | `.../llm_base_proposer.py:508–509` | `take_last_draft_probs()` 取出上一步 `draft_probs` | 供 runner 缓存 |
| 12 | `.../llm_base_proposer.py:511` | `propose` 是草稿入口 | 函数定义 |
| 13 | `.../llm_base_proposer.py:459–472` | 并行草稿下 logits 行数 = batch×K，需广播 temperature | `repeat_interleave` |
| 14 | `vllm/v1/sample/rejection_sampler.py:410` | `rejection_sample` 入口；`draft_probs` 可为 `None` | 函数定义 |
| 15 | `.../rejection_sampler.py:445–480` | 纯贪心路径：`target_argmax` + `_rejection_greedy_sample` | 全 greedy 直接返回 |
| 16 | `.../rejection_sampler.py:487–520` | 随机路径：target softmax + 恢复 token + 随机拒绝 | `sample_recovered_tokens` / `_rejection_random_sample` |
| 17 | `.../rejection_sampler.py:678` | `sample_recovered_tokens` 定义 | 从残差重采 |
| 18 | `.../rejection_sampler.py:811` | `_rejection_greedy_sample` 定义 | 贪心 kernel |
| 19 | `.../rejection_sampler.py:934` | `_rejection_random_sample` 定义 | 采样 kernel |
| 20 | `.../rejection_sampler.py:949` | Triton kernel `NO_DRAFT_PROBS=draft_probs is None` | one-hot 提议分支 |
| 21 | `.../rejection_sampler.py:1128` | 同上（另一 kernel 的 `NO_DRAFT_PROBS`） | 恢复 token kernel |
| 22 | `vllm/v1/spec_decode/metrics.py:107–122` | acceptance rate 与 mean acceptance length 两个分母 | `1 + accepted/num_drafts` |
| 23 | `vllm/v1/worker/gpu_model_runner.py:4714–4741` | `draft_probs` 按请求拼装；缺失 → `None` 整批回退 | `_get_spec_decode_draft_probs` |
| 24 | `.../gpu_model_runner.py:4987–4990` | 从 drafter `take_last_draft_probs()` 缓存 | 与 11 对接 |

## 2. SGLang @ `2a08e261ecd4cdfb04ec354f9005f18b88108b7d`（2026-10-16，Apache-2.0）

| # | 锚点 | 支撑的断言 | 备注 |
| --: | :-- | :-- | :-- |
| 25 | `python/sglang/srt/speculative/eagle_worker_v2.py:178–180` | 开启拒绝采样时**硬断言 `topk == 1`** | chain speculative sampling 的边界 |
| 26 | `.../eagle_worker_v2.py:181–182` | `speculative_num_steps` / `num_draft_tokens` 读取处 | 原引 184–186 → 181–182（见 §3） |
| 27 | `.../eagle_worker_v2.py:648–657` | CUDA graph 的 `draft_probs` 必须 `clone()` 出池 | 注释说明池会被复用 |
| 28 | `.../eagle_worker_v2.py:671–684` | `build_eagle_verify_input(..., draft_probs, topk=...)` | 原引 676–681 → 671–684 |
| 29 | `.../eagle_worker_v2.py:727–733` | 仅“非 greedy 且开启拒绝采样”才构造 `draft_probs` | `needs_draft_probs` |
| 30 | `.../eagle_utils.py:157` | `build_tree_kernel_efficient` 定义 | 树 mask/树构造 |
| 31 | `.../eagle_utils.py:384` | `verify_tree_greedy_func` 定义 | 贪心树验证 |
| 32 | `.../eagle_utils.py:741` | `eagle_sample` 统一验证入口 | 分流起点 |
| 33 | `.../eagle_utils.py:860` | `use_rejection_sampling = get_spec().speculative_use_rejection_sampling` | 开关读取 |
| 34 | `.../eagle_utils.py:861–916` | `_verify_uses_greedy(...)` → `verify_tree_greedy_func` | 原引 862–916 → 861–916 |
| 35 | `.../eagle_utils.py:947` | 开启拒绝采样 → `chain_speculative_sampling_triton` | 拒绝采样分支 |
| 36 | `.../eagle_utils.py:951–959` | 否则 → `tree_speculative_sampling_target_only` | **tree topk>1 仍 target-only 的代码依据**；新增锚 |
| 37 | `.../eagle_utils.py:1000–1013` | `draft_probs` 缺失/词表不匹配 → `ValueError` | 硬失败，非静默降级 |
| 38 | `.../eagle_utils.py:1032–1038` | `uniform_samples` / `target_probs` / `draft_probs` 传入采样 kernel | 原引 1030–1044 → 1032–1038 |
| 39 | `.../eagle_info.py:35` | `EagleVerifyInput.draft_probs` 字段 | verify 输入 |
| 40 | `.../eagle_info.py:162` | `EagleDraftInput.draft_probs` 字段 | draft 输出 |

## 3. EAGLE @ `cb7e0841fe0c206c6ed74a197ad5e2a1f13f5a2b`（2026-02-20）

| # | 锚点 | 支撑的断言 | 备注 |
| --: | :-- | :-- | :-- |
| 41 | `eagle/model/utils.py:398` | tree/EA 评估路径 `qx = 1.0` | 草稿按 one-hot |
| 42 | `eagle/model/utils.py:399` | `acp = px / qx` → 接受概率退化为 `p(x)` | 与 41 成对 |
| 43 | `eagle/model/ea_model.py:270`、`:452` | `evaluate_posterior` 调用点 | tree/EA 路径 |
| 44 | `eagle/modeling_eagle.py:1427` | HF 风格实现保留真实 `qx` | **边界**：不是全仓库共性 |

## 4. 复核结果与行号更正历史

**复核结果**：40 个文件级锚点（vLLM 24 + SGLang 16）逐条检查“目标行/区间含断言关键词”，**40/40 命中，0 偏行**（2026-10-17）。EAGLE 5 条另行逐行核对（`utils.py:398/399`、`ea_model.py:270/452`、`modeling_eagle.py:1427`）。

| 原值 | 新值 | 原因 |
| :-- | :-- | :-- |
| vLLM `speculative.py:560` | `speculative.py:555` | 560 是 `_acceptance_length_to_rates`，`enable_adaptive_verification` 在 555 |
| vLLM `speculative.py:533–560` | `speculative.py:533–553` | 560 越出 synthetic 字段区 |
| SGLang `eagle_worker_v2.py:184–186` | `:181–182` | 步数/草稿数实际在 181–182 |
| SGLang `eagle_worker_v2.py:676–681` | `:671–684` | `build_eagle_verify_input` 调用实际 671 起 |
| SGLang `eagle_utils.py:862–916` | `:861–916` | `_verify_uses_greedy` 分支从 861 起 |
| SGLang `eagle_utils.py:1030–1044` | `:1032–1038` | 三个实参在 1032–1038 |
| `sources/MANIFEST.md` SGLang 旧范围 | 同步为上表新范围 | 清单与分册一致 |

**新增锚**：SGLang `eagle_utils.py:951–959`（tree topk>1 的 target-only 依据），对应分册 §5 / §6.2 与 report §8.2。

## 5. 引用纪律

- 所有锚点绑定 commit；换 commit 后行号可能漂移，引用时保留 SHA。
- 代码只以 `仓库@commit:文件:行` 形式引用，**不贴大段源码、不入库源码文件**。
- 若一行只“间接支撑”断言（例如只是实参行），分册里须注明“间接”或换用定义/分支行；本清单已按此原则校正。
