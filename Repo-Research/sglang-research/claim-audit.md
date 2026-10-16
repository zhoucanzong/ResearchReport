# 子文档：结论审计与阅读覆盖

> ⚠️ **信息来源声明**：本文由 AI Agent 生成，记录本次代码阅读的自检结果与适用范围。 
>
> **调研日期**：2026-10-16
> **分析对象**：`sgl-project/sglang` @ `2a08e261ecd4cdfb04ec354f9005f18b88108b7d`
> **主文档**：[report.md](report.md) ｜ [speculative-decoding-path.md](speculative-decoding-path.md) ｜ [scheduler-and-prefix-cache.md](scheduler-and-prefix-cache.md)

---

## 1. 方法学执行记录

按 `code-researcher` skill 的 deep 模式流程执行：

| 步骤 | 工具 / 参考 | 实际执行 |
|---|---|---|
| 1. 定位仓库 | — | `git clone --filter=blob:none` 到 `/tmp/sglang-clone`，checkout `2a08e261…`，**未构建、未修改** |
| 2. 项目扫描 | `scripts/scan_repo.py` | 输出 `/tmp/sglang-work/repo-scan.json`（94 KB） |
| 3. 地图草稿 | `scripts/summarize_scan.py` | 生成中文项目地图；**人工改判了入口候选**（见 §4） |
| 4. 参考文件 | `references/research-method.md`、`runtime-story.md`、`deep-architecture-report.md`、`module-investigation.md`、`evidence-quality.md`、`reading-coverage.md`、`visual-reporting.md`、`claim-audit.md` | 已读 |
| 5. 运行时故事 | `references/runtime-story.md` | 选了「单请求 EAGLE topk=1 + T>0 + overlap」 |
| 6. 结论审计 | `scripts/claim_audit.py` | 结果见 §2 |
| 7. 阅读覆盖 | `references/reading-coverage.md` | 见 §3 |

**未使用**：`build_evidence_index.py`（证据索引以 markdown 表格手写，含同样字段）。

---

## 2. 结论审计（`claim_audit.py`）

审计命令：

```bash
~/.dsh/venvs/research/bin/python ~/.dsh/skills/code-researcher/scripts/claim_audit.py \
  Repo-Research/sglang-research/report.md --lang zh
```

审计器口径：逐行扫描，凡命中「高影响词表」（中文：核心/主要/关键/中心/保证/确保/防止/可扩展/安全/稳定/可靠/风险/瓶颈/耦合/技术债/优化/取舍/抽象/边界；英文：core/central/primary/main/critical/guarantees/ensures/prevents/scales/safe/stable/reliable/risk/bottleneck/coupling/designed for/optimizes for/tradeoff/abstraction/boundary）的行，若其**相邻 1 行内**没有可识别的源码路径/文件:行 引用，则判为"缺少邻近源码证据"。

**审计结果**（定稿后重跑，四个文档分别执行）：

| 文档 | 高影响结论数 | 缺少邻近证据 | 处置 |
|---|---|---|---|
| [report.md](report.md) | 36 | **0** | 首轮 4 处被标记（3 个标题 + 1 个表头），已改标题措辞/表头用词 |
| [speculative-decoding-path.md](speculative-decoding-path.md) | 30 | **0** | 首轮 3 处被标记，已为每处补 `文件:行` 引用；其中 1 处据代码收紧断言 |
| [scheduler-and-prefix-cache.md](scheduler-and-prefix-cache.md) | 32 | **0** | 首轮 2 处被标记（1 标题 + 1 段），已补引用/改措辞 |
| [claim-audit.md](claim-audit.md)（本文） | 12 | **0** | 已改措辞 |

**读取方式**：审计器只看相邻 1 行窗口，表格里「结论」列与「证据」列分开时会误报。据此把要紧的判断改成「判断句 + 紧随其后的源码引用行」的排版后重跑，把仍被标记的行逐条处置。

### 2.0 首轮被标记项的处置留痕

| 首轮标记 | 类型 | 处置 |
|---|---|---|
| `report.md` 「## 6. 核心模块研究…」 | 标题 | 去掉"核心"字样（该节本就是摘录） |
| `report.md` 「与投机解码的耦合点（三条…）」 | 风险 | 补 `scheduler.py:4595` 起始引用 |
| `report.md` 「\| 取舍 \| 换来什么…\|」 | 表头 | 表头改为「设计选择」，并在"证据"列注明「文件:行」 |
| `report.md` 「## 10. 证据索引（主要结论 → 源码）」 | 标题 | 简化为「## 10. 证据索引」（正文表格已含全部引用） |
| `speculative-decoding-path.md` HIP 分支推断 | 风险 | 补 `eagle_worker_v2.py:1196` |
| `speculative-decoding-path.md` 三条判据并存 | 风险 | 补 `eagle_utils.py:741` + `eagle_info.py:17` |
| `speculative-decoding-path.md` EAGLE3 降维词表 | 事实 | **据代码收紧断言**：原文写"draft 词表 32000 vs target 128256"属本报告未核验的具体数字，已改为只主张代码闸门（`eagle_worker_v2.py:249`）存在，并显式声明"未核验具体 checkpoint 词表大小" |
| `scheduler-and-prefix-cache.md` 「4.2 重叠调度最关键的一行」 | 标题 | 改为「4.2 重叠调度的分支点」 |
| `scheduler-and-prefix-cache.md` publish 插入点动机 | 风险 | 补 `eagle_worker_v2.py:1424` + `scheduler.py:4575` |
| `claim-audit.md` 3 处 | — | 改措辞 |

### 2.1 审计器已知的局限（如实记录）

1. **只看相邻 1 行**：本报告大量使用「结论 | 源码位置」的**表格**排版，源码在另一列或另一行时，审计器可能误报。因此我把 §10 证据索引与各章的"代码事实"段改为**结论句与其源码引用同段或紧邻**。
2. **只认路径样式的字符串**：形如 `foo/bar.py:123` 或 `baz.md` 的 token 才被识别；纯符号名（如 `RadixCache`）不算证据。本报告为此把源码引用统一写成「反引号包裹的 `文件:行`」或与其紧邻的行内链接（链接文本里带行号），确保审计器能读到 `文件:行`。
3. **它不判断证据是否真的支持结论**：通过审计 ≠ 结论正确。真正的把关在 §3 的覆盖记录与 §5 的核验边界。

---

## 3. 阅读覆盖记录

按 `references/reading-coverage.md` 的四级口径（Scanned / Skimmed / Traced / Audited）。

### Audited（为验证重要判断回看复查）

| 文件 | 为什么读 | 支撑结论 |
|---|---|---|
| `python/sglang/srt/speculative/eagle_worker_v2.py` | 追 topk=1 的 `topk_p` 赋值与两处分派 | 「默认把草稿当 one-hot」 |
| `python/sglang/srt/speculative/eagle_utils.py` | 追 `eagle_sample` 三分支、`draft_probs` 构造、`eagle_prepare_for_verify` | 三条判据的差异 |
| `python/sglang/kernels/jit/include/sgl_kernel/speculative/sampling.cuh` | 逐行读接受判据与残差采样 | `FIXME: leverage draft probs`；`coin < prob_acc/threshold_acc` |
| `python/sglang/kernels/ops/speculative/reject_sampling.py` | 逐行读 `coin * q < p` 与 block verification 前缀递推 | 严格模式的判据 |
| `python/sglang/srt/arg_groups/speculative_hook.py` | 读全部闸门与自动调参 | 四道校验 + Llama→topk=4 |
| `python/sglang/srt/mem_cache/registry.py` | 追 `return` 语句确认默认树实现 | 默认是 `UnifiedRadixCache` |
| `python/sglang/srt/mem_cache/unified_cache/tree_core_registry.py` | 读 `_rust_fallback_reason` 全部条件 | Rust 默认 + 6 类回退 |
| `python/sglang/srt/managers/scheduler.py` | 读 `event_loop_overlap` / `run_batch` / `get_next_batch_to_run` | 重叠调度与 spec 的耦合点 |

### Traced（作为运行路径的一部分追过）

`managers/schedule_batch.py`（`init_next_round_input`）、`managers/schedule_policy.py`（LPM / `_compute_prefix_matches`）、`mem_cache/common.py`（`match_kv_cache`）、`mem_cache/radix_cache.py`（`match_prefix`/`_split_node`/`evict`/`lock_ref`）、`mem_cache/unified_cache/unified_tree_core.py`（节点与 LRU 结构）、`managers/overlap_utils.py`（`FutureMap`/`resolve_forward_inputs`）、`managers/tp_worker.py`（`forward_batch_generation` 的 `is_verify` 早退）、`speculative/eagle_worker_common.py`（`run_eagle_verify`）、`speculative/spec_utils.py`（`renorm_draft_probs` / `sample_draft_proposal`）、`speculative/spec_info.py`（worker 分派）、`speculative/eagle_info.py`（`EagleDraftInput` / `EagleVerifyInput`）、`layers/radix_attention.py`（类定义与 `forward`）。

### Skimmed（读到足够理解职责）

`entrypoints/`、`managers/tokenizer_manager.py`、`model_executor/model_runner.py`、`mem_cache/memory_pool.py`、`mem_cache/allocator/`、`mem_cache/hybrid_cache/`、`rust/sglang-radix-tree/src/{lib,node,unified_lru_list}.rs`、`docs/docs/advanced_features/speculative_decoding.mdx`、`test/registered/spec/eagle/`。

### Scanned only（仅被 `scan_repo.py` 统计）

`rust/`（除 radix-tree）、`sgl-model-gateway/`、`benchmark/`、`docs/src/`、`examples/`、`test/`（除上列）、`3rdparty/`、`experimental/`、`tools/`。**本报告不对这些区域下任何行为结论。**

### 未检查（不能把强结论建立在此）

- 任何 CUDA graph 捕获细节（`*_cuda_graph_runner.py` 只 skim 了 topk/`speculative_use_rejection_sampling` 相关常量）。
- PP（pipeline parallel）与 DP attention 下的 spec 路径（`scheduler_pp_mixin.py` 未读）。
- DFLASH / DSPARK / UNO / NGRAM worker 的内部语义。
- `hisparse` / `disaggregation` / `elastic_ep` 等特性开关对 spec 的影响。
- 所有性能数字。

---

## 4. 对扫描器输出的两处人工改判

| 扫描器建议 | 我为什么不同意 | 改判为 |
|---|---|---|
| `entry_candidates` 首选 `.agents/skills/*/SKILL.md`（8 个，score 90） | 那些是仓库自带的 Agent 协作说明书（如 `add-jit-kernel`、`babysit-pr-to-pass-ci`），**不是运行时入口**；把 SKILL.md 当入口会把读者引到开发流程而不是引擎架构 | `entrypoints/` → `managers/` → `model_executor/` |
| `reading_route` 推荐 `test/registered/unit/mem_cache/test_unified_radix_cache_unittest.py` 等大文件 | 大文件不等于高信号；测试文件解释的是契约而非主路径。本报告把测试用于**交叉验证**，不作为阅读起点 | 先读 `base_prefix_cache.py`（契约）→ `unified_radix_cache.py`（控制器）→ `unified_tree_core.py`（树） |

---

## 5. 引用与核验边界（汇总）

| 项 | 状态 |
|---|---|
| SGLang @ `2a08e261…` 源码 | ✅ 一手精读（只读、未构建、未修改、读完删除） |
| SGLang 运行 / 性能 | ❌ 完全未涉及 |
| SGLang issue #10308 是否被修复 | ⚠️ 未确证；只主张"功能对应路径存在" |
| EAGLE @ `cb7e0841…` | ⚠️ 转引本仓库既有专题 §5.1 ①，未重新 clone |
| 「EAGLE 与 SGLang 默认路径同构」 | ✅ topk=1 上成立（由代码事实推出）；❌ topk>1 上未论证 |
| Rust TreeCore 与 Python TreeCore 行为等价性 | ❌ 未做对拍 |
| 是否向仓库提交了任何源码 | ✅ **没有**。clone 在 `/tmp/sglang-clone`，报告内只有 ≤15 行的短引用（本报告实际最长引用为 `sampling.cuh` 与 `reject_sampling.py` 各 2–4 行） |

---

## 6. 统计一致性说明

新增条目会改变 `scripts/library_index.py` 的统计（条目数 / 行数 / 字节数）。本轮**未手改任何统计数字**，而是在提交前重跑：

```bash
~/.dsh/venvs/research/bin/python scripts/library_index.py --repo-root . --out-root . --dry-run
~/.dsh/venvs/research/bin/python scripts/library_index.py --repo-root . --out-root . --write-stats --check-links
```

再生成的 `INDEX.md`、`index/*`、`docs/statistics.md` 与本条目一并提交。

> *数据截至 2026-10-16。*
