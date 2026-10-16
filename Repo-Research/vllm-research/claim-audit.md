# 子文档：结论审计、阅读覆盖与自检

> ⚠️ **信息来源声明**：本文由 AI Agent 生成，记录本次代码阅读的自检结果与适用范围。
>
> **调研日期**：2026-10-16
> **分析对象**：`vllm-project/vllm` @ `fa75d3456d60a5ffe923818c4b495295675b38e1`
> **主文档**：[report.md](report.md) ｜ [kv-cache-and-prefix-reuse.md](kv-cache-and-prefix-reuse.md) ｜ [scheduling-and-spec-decode.md](scheduling-and-spec-decode.md)

---

## 1. 方法学执行记录

按 `code-researcher` skill 的 deep 模式流程执行：

| 步骤 | 工具 / 参考 | 实际执行 |
|---|---|---|
| 1. 定位仓库 | — | `git clone --filter=blob:none --depth 1 https://github.com/vllm-project/vllm` 到 `/tmp/vllm-src`，**未构建、未修改、未提交任何源码**；`git rev-parse HEAD` = `fa75d3456d60a5ffe923818c4b495295675b38e1`；交付前删除（确认见 §4） |
| 2. 项目扫描 | `scripts/scan_repo.py` | 输出 `/tmp/vllm-scan.json`（82 KB）：Python 1,902,738 行 / Rust 140,024 行 / Markdown 52,509 行 / C++ 51,651 行 |
| 3. 入口候选复核 | — | 扫描器给出的入口多为 `.agents/skills/*/SKILL.md`（**开发流程用 skill，不是运行入口**），本报告据 §3.1 人工改判为 `vllm/v1/core/` 与 `vllm/v1/sample/` |
| 4. 参考文件 | `references/research-method.md`、`deep-architecture-report.md`、`evidence-quality.md`、`claim-audit.md` | 已读 |
| 5. 运行时故事 | `references/runtime-story.md` | 选了「长 prompt + decode 并发 + KV 压力触发抢占 + 开 spec decode」 |
| 6. 结论审计 | `scripts/claim_audit.py --lang zh` | 结果见 §2 |
| 7. 阅读覆盖 | `references/reading-coverage.md` | 见 §3 |

**未使用**：`build_evidence_index.py`（证据索引以 markdown 表格手写，字段等价）、`summarize_scan.py`（项目地图手写）。

---

## 2. 结论审计（canonical `claim_audit.py`）

审计命令（逐文档执行）：

```bash
~/.dsh/venvs/research/bin/python ~/.dsh/skills/code-researcher/scripts/claim_audit.py \
  Repo-Research/vllm-research/<doc>.md --lang zh
```

审计器口径：逐行扫描，凡命中「高影响词表」（中文：核心/主要/关键/中心/保证/确保/防止/可扩展/安全/稳定/可靠/风险/瓶颈/耦合/技术债/优化/取舍/抽象/边界）的行，若其**相邻 1 行内**没有可识别的源码路径 / `文件:行` 引用，则判为"缺少邻近源码证据"。

**审计结果（定稿后重跑）**：

| 文档 | 高影响结论 | 缺少邻近源码证据 | 处置 |
| :-- | --: | --: | :-- |
| [report.md](report.md) | 32 | **0** | 首轮 32/2，在 §6.4 与 §7 标题行补锚点后归零 |
| [kv-cache-and-prefix-reuse.md](kv-cache-and-prefix-reuse.md) | 28 | **0** | 首轮 28/5，在 Phase 2 / 全命中代价 / 抢占推断 / §5 标题与表头补锚点后归零 |
| [scheduling-and-spec-decode.md](scheduling-and-spec-decode.md) | 16 | **0** | 首轮 16/3，在 §2.4/§2.5/§4.3 补锚点后归零 |
| 本文（claim-audit.md） | 11 | **0** | 审计范围含本表的"风险 / 边界"措辞；0 缺证 |

**说明**：审计器只检查"相邻一行内有无路径"，**不判断路径是否真的支撑结论**。后者靠 §3 的阅读覆盖与 §5 的等级纪律人工兜底。

---

## 3. 阅读覆盖

| 模块 | 覆盖 | 依据 |
|---|---|---|
| `vllm/v1/core/block_pool.py`（905 行） | **精读** | 类结构、`get_new_blocks`、`free_blocks`、`_maybe_evict_cached_block`、`unpin_blocks`、`get_cached_block` |
| `vllm/v1/core/kv_cache_utils.py`（1,217 行） | **部分精读** | `request_block_hasher`、`FreeKVCacheBlockQueue` docstring、`BlockHashListWithBlockSize` 声明；其余从略 |
| `vllm/v1/core/single_type_kv_cache_manager.py`（2,712 行） | **部分精读** | `FullAttentionManager.find_longest_cache_hit` 全读；Mamba / SlidingWindow / CrossAttention 分支**未读** |
| `vllm/v1/core/kv_cache_manager.py`（922 行） | **部分精读** | `get_computed_blocks`、`allocate_slots` docstring；分配三段式实现细节未逐行 |
| `vllm/v1/core/sched/scheduler.py`（3,520 行） | **重点精读 ~15%** | `schedule` 主循环、预抢占与抢占、`_preempt_request`、`update_draft_token_ids*`、`get_grammar_bitmask`、`update_from_output` 的 spec 段、指标口径段 |
| `vllm/v1/sample/rejection_sampler.py`（1,130 行） | **重点精读** | 类 docstring、`forward`、`_rejection_greedy_sample`、`rejection_random_sample_kernel` 内层循环、warmup 路径 |
| `vllm/v1/structured_output/` | **部分精读** | `__init__.py` 的 `validate_tokens` / `grammar_bitmask`；四个 backend 只读 xgrammar 的 `num_speculative_tokens` 相关行 |
| `vllm/v1/worker/gpu/` | **部分精读** | `model_runner.py` 的掩码与采样次序、`structured_outputs.py` 的 triton kernel、`spec_decode/utils.py` |
| `vllm/v1/worker/gpu_model_runner.py`（7,223 行） | **抽样** | 仅 spec/structured 相关段落；**与 `gpu/model_runner.py` 的关系未确证** |
| `vllm/config/speculative.py` / `cache.py` / `vllm.py` | **精读（相关字段）** | `draft_sample_method`、`rejection_sample_method`、`synthetic_acceptance_*`、`enable_prefix_caching`、watermarking 闸门 |
| `docs/design/prefix_caching.md`、`docs/design/paged_attention.md`、`docs/features/speculative_decoding/acceptance_metrics.md` | **精读（相关段落）** | 哈希键构成、append-only 声明、历史文档自废声明、指标口径 |
| `vllm/v1/worker/block_table.py`、`vllm/v1/request.py`、`vllm/v1/metrics/stats.py` | **部分精读** | 与 KV/指标直接相关的行 |
| `csrc/`、`rust/`、`tests/`、CI 配置 | **未读** | 本报告不涉及其结论；`docs/design/paged_attention.md` 已声明数据路径不在 `csrc/` |

---

## 4. 自检九项

| # | 检查项 | 结果 |
|---|---|---|
| 1 | 主工作树干净且在 `main` | ✅ `git status --short` 为空；`git rev-parse --abbrev-ref HEAD` = `main`（`5c3225e`） |
| 2 | 独立 worktree 串行化 | ✅ `git worktree list` 显示 `/private/tmp/wt-vllm [research/vllm-research-yanyan]` 与主工作树分离 |
| 3 | 无源码 / 克隆残留 | ✅ 新条目目录只含 4 个 `.md`；`git status --porcelain` 中无源码文件；clone（186 MB）在交付前删除 |
| 4 | 条目统计一致性 | 见 §6（`entries.total` 46 → 47，`children` 41 → 44） |
| 5 | front-matter 契约 | ✅ 仅 `report.md` 带 front-matter（9 行：7 字段 + 首尾围栏），与 `docs/team.md` 契约一致；三份子文档不带 |
| 6 | 链接回测 | 见 §5（0 新增失效） |
| 7 | gitlink 0 | ✅ `git ls-files -s` 中 `mode 160000` 计数为 0 |
| 8 | 远端分支 SHA = 本地 | 见 §7 |
| 9 | 证据标签单一主等级 | ✅ 每处引用只挂一个主等级；跨仓库对照明确标为「转引本仓库既有条目」 |

---

## 5. 全仓相对链接回测（正确顺序）

顺序按任务要求执行：**先剥围栏代码块与行内反引号 → 剥 `<>` → 判 scheme → percent-decode → 查存在**。

| 阶段 | 相对链接总数 | 失效 |
| :-- | --: | --: |
| 基线（`main` @ `5c3225e`，文档未落盘时实测） | 1,656 | **0** |
| 本批（`research/vllm-research-yanyan`，含 4 份新文档 + 生成物 + `README.md`/`statistics.md` 更新） | 1,735 | **0** |

**新增 79 条**（1,656 → 1,735），**新增失效 0**。其中新条目文档本身贡献 54 条，其余来自 `INDEX.md` / `index/*` 生成物与 `README.md`、`docs/statistics.md` 的索引补齐。

**基线绝对值说明**：`docs/statistics.md` 末次留痕记的 1,650 是 Decision Models 批次当时的实测值；本次在同一脚本（同一顺序、同一跳过规则：跳过 `.git`、跳过围栏内文本、跳过行内反引号）下测得 **1,656**。差异 6 条来自**生成物与既有文档的后续变化**，不是本批引入——本批文档若进入基线计数，只会增加。本报告按"同一脚本同期实测"口径记录 1,656，不沿用旧值。

---

## 6. 统计一致性

- `scripts/library_index.py --repo-root . --out-root . --write-stats --check-links`：先 `--dry-run` 核对（条目 47 / 子文档 44），落盘后 `--check-links` 报「生成文件内的相对链接全部可解析」。**注意脚本的 `tracked_*` 取自 `git ls-files`，因此追加提交后必须重跑一次**，否则版本控制口径会停在旧值。
- `entries.total`：**46 → 47**（新增 `Repo-Research/vllm-research/report.md`）。
- `entries.children`：**41 → 44**（新增三份子文档：`kv-cache-and-prefix-reuse.md`、`scheduling-and-spec-decode.md`、`claim-audit.md`）。
- `entries.lines`：由脚本重算，**不手改**。
- 派生数字同步至：根 `README.md`、`docs/statistics.md`、`INDEX.md`、`index/*.md`（后两者由脚本生成，不手改）。

---

## 7. 交付留痕

- **分支**：`research/vllm-research-yanyan`（自 `main` @ `5c3225e` 切出）。
- **本批新增**：`Repo-Research/vllm-research/` 下 4 个文件；另同步 `README.md`（含补齐 ③ SGLang / ④ vLLM 两条索引）、`docs/statistics.md`、`INDEX.md`、`index/*`。
  - [report.md](report.md)：303 行（正文 294 + front-matter 9）/ 35,224 B
  - [kv-cache-and-prefix-reuse.md](kv-cache-and-prefix-reuse.md)：206 行（正文 206）/ 18,691 B
  - [scheduling-and-spec-decode.md](scheduling-and-spec-decode.md)：244 行 / 22,669 B
  - 本文 [claim-audit.md](claim-audit.md)：131 行 / 10,273 B
- **未确证 / 待跟踪**（不入正文结论）：
  1. 抢占后 `get_computed_blocks` 是否真退化为零命中——§4.2 的推断需要构造实验确证（打印 `num_preemptions` 与命中数）。
  2. structured output 下验证判据的参照分布语义：是"近似"还是"仓库定义的正确答案"——仓库内**未找到明文定义**，检索 `docs/` 无结论。
  3. `vllm/v1/worker/gpu/model_runner.py` 与 `gpu_model_runner.py` 的默认关系（两套 runner 并存）。
  4. vLLM 是否有与 SGLang `event_loop_overlap` 对应的调度重叠机制。
  5. SGLang 侧的抢占恢复与语法约束下草稿处理——**本轮未 clone SGLang，不填对照表空格**。

---

*本文完。所有判断仅覆盖上表声明的阅读范围；范围外一律不作结论。*
