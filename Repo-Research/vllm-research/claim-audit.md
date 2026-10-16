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
| 本文（claim-audit.md） | **24**（含 §3.5 与附录 A 的"不合格/风险/边界"措辞） | **0** | 0 缺证；§3.5 锚点复检为独立门禁，不属 claim_audit 口径 |

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

## 3.5 锚点复检（2026-10-16）

**触发**：门禁方按同一 commit 用 `raw.githubusercontent.com` 抽查 5 处锚点，判定 2 处不合格（`rejection_sampler.py:870` 实为 `if NO_DRAFT_PROBS:`、`block_pool.py:686` 实为注释行）。本轮据同一口径对**全部**锚点做机械复检。

**复检方法（可机械复现）**：

```bash
# 钉住 commit，逐条取该行原文
git show fa75d3456d60a5ffe923818c4b495295675b38e1:<path> | sed -n "<行>p"
```

- 抽取口径：用正则 `([A-Za-z0-9_./-]*\.py):(\d+)(?:-(\d+))?` 扫 `report.md` + 两份子文档的全文，得到**全部 162 处** `.py:行` 断言（去重后：`report.md` 65 / `scheduling-and-spec-decode.md` 54 / `kv-cache-and-prefix-reuse.md` 44）。
- 判定规则（门禁方给定）：**命中**=被引符号就在该行；**区间命中**=区间两端均为代码行；**注释段区间**=正文已明示为注释段且起/止行确为注释；**落在注释/空行**=不合格；**超出文件长度/路径不存在**=不合格。
- 对照源：先把该 commit `checkout` 到 `/tmp/vllm-verify`（`git rev-parse HEAD` = `fa75d3456d60a5ffe923818c4b495295675b38e1`），再用 `sed -n` 取行，**不依赖阅读印象**。

**复检结果**：

| 指标 | 数量 |
| :-- | --: |
| 抽取到的 `.py:行` 断言 | **162** |
| ✅ 命中（被引符号即该行） | 108 |
| ✅ 命中（区间端点均为代码行） | 49 |
| ✅ 命中（显式注释段区间，正文已注明） | 5 |
| ⚠️ 落在注释/空行 | **0** |
| ❌ 超出文件长度 / 路径不存在 | **0** |
| **未命中数** | **0** |

**修正清单（原值 → 新值，共 17 处，分布于 3 份文档）**：

| # | 文档 | 原值 | 新值 | 该行实际内容 | 说明 |
| --: | :-- | :-- | :-- | :-- | :-- |
| 1 | report / sched-spec | `rejection_sampler.py:870` | **`:872`** | `:870` = `else:`；`:872` = `draft_prob = 1` | 门禁方抽到的第 1 例；同时在 `:871` 标注 `if NO_DRAFT_PROBS:` |
| 2 | report / kv | `block_pool.py:686` | **`:689`** | `:686` = 注释 "In order to only iterate the list once…"；`:689` = `self._maybe_evict_cached_block(block)` | 门禁方抽到的第 2 例 |
| 3 | report / sched-spec | `rejection_sampler.py:881`（单行） | **`:884`** | `:884` = `accepted = draft_prob > 0 and target_prob / draft_prob >= uniform_prob` | 判据行归位 |
| 4 | sched-spec | `rejection_sampler.py:870-882` | **`:871-884`** | `:871` `if NO_DRAFT_PROBS:` / `:872` `draft_prob = 1` / `:884` 判据 | 区间两端口均归位 |
| 5 | report / sched-spec | `structured_outputs.py:199-204` | **`:195-198`** | `:195` `tl.store(`、`:197` `-float("inf")`、`:198` mask | 原区间止行 204 超出行长（文件 199 行）；**属"超出文件长度"类不合格** |
| 6 | report / sched-spec | `model_runner.py:1634`（及 `1634-1636`） | **`:1636`**（`1636-1641`） | `:1634` = 注释；`:1636` = `self.structured_outputs_worker.apply_grammar_bitmask(` | 原值落在注释行 |
| 7 | report | `block_pool.py:680` | **`:681`** | `:680` = 空行；`:681` = `ret: list[KVCacheBlock] = self.free_block_queue.popleft_n(num_blocks)` | 原值为空行 |
| 8 | report / sched-spec | `scheduler.py:623-632` | **`:623-641`** | `:623-632` 为 NOTE 注释段；实体代码自 `:634`、预算赋值 `:641` | 正文补注"NOTE 注释段"，避免单点被误读为代码行 |
| 9 | sched-spec | `rejection_sampler.py:864-865` | **`:864-866`** | `:864` `if draft_token_id < 0:`、`:866` `accepted = False` | 补上真正的赋值行 |
| 10 | sched-spec | `request_queue.py:13-18` | **`:13-17`** + `:131-159` | `:16` `FCFS`、`:17` `PRIORITY`；`:18` 为空行 | 区间收口并补 `PriorityRequestQueue` 显式锚点 |
| 11 | sched-spec | `speculative.py:533-548` | **`:533-547`** | `:533` `rejection_sample_method`、`:541` `synthetic_acceptance_rates` | `:548` 为空行 |
| 12 | sched-spec | `scheduler.py:2200`（指标段） | **`:2207`**（回滚）/ `:2210`（stats 调用） | `:2207` `request.num_computed_tokens -= num_rejected`；`:2210` `make_spec_decoding_stats(` | 拆成两个语义锚点 |
| 13 | sched-spec | `scheduler.py:1676`（`drop_stale_output` 写入点） | **`:1681`** | `:1676` = 注释；`:1681` = `request.drop_stale_output = drop_stale_output or (` | 原值落在注释行 |
| 14 | sched-spec | `scheduler.py:1676-1682` | **`:1674-1680` 注释 + `:1681` 赋值** | 原区间把注释与赋值混在一个跨度里 | 注释与实体分离 |
| 15 | kv | `kv_cache_manager.py:292` | **`:295`** | `:292` = 注释；`:295` = `max_cache_hit_length = request.num_tokens - 1` | 原值落在注释行 |
| 16 | kv | `block_pool.py:184-188` | `:184-188` + 注"赋值在 `:187`" | `:187` `self.null_block = self.free_block_queue.popleft()`、`:188` `.is_null = True` | 保留区间（含注释头），补赋值行 |
| 17 | kv / sched-spec | `kv_cache_manager.py:289-299` / `block_pool.py:729-747` / `block_pool.py:689` / `request_queue.py` 内联 `:131-159` 等 | **`kv_cache_manager.py:289-300`**；`block_pool.py:689` 补 `:738/:741/:747` 子锚点 | 区间端点归到代码行（`:300` `)`、`:747` 事件入队） | 端点收口 |

**门禁方原判"无误"的 6 处**经本轮机械复检**全部保持命中**，未作改动：`config/speculative.py:604`、`single_type_kv_cache_manager.py:786-792`、`scheduler.py:623-641`（原判 `623-632`，本轮扩到含预算赋值的 `:641`）、`scheduler.py:1671`/`:1692`、`block_pool.py:791-799`、`kv_cache_utils.py:1003`。

**可复现说明**：复检脚本为**临时**脚本（`/tmp`，**未入库**）。若要入库为 `scripts/verify_source_anchors.py`，需先评审其规格（输入=报告路径 + upstream commit；输出=上表五列 + 退出码），本批**不提交**该脚本。


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

- **分支**：`research/vllm-research-yanyan`（自 `main` @ `5c3225e` 切出；为适配 `origin/main` 推进到 **`acafc4e`**（WorldModels 第二轮 + 链接补齐）已 rebase 一次，rebase 后基线为 `acafc4e`）。
- **本批新增**：`Repo-Research/vllm-research/` 下 4 个文件；另同步 `README.md`（含补齐 ③ SGLang / ④ vLLM 两条索引）、`docs/statistics.md`、`INDEX.md`、`index/*`。
  - [report.md](report.md)：303 行（正文 294 + front-matter 9）/ 35,658 B
  - [kv-cache-and-prefix-reuse.md](kv-cache-and-prefix-reuse.md)：206 行 / 19,069 B
  - [scheduling-and-spec-decode.md](scheduling-and-spec-decode.md)：244 行 / 24,076 B
  - 本文 [claim-audit.md](claim-audit.md)：365 行 / 44,029 B（含 §3.5 锚点复检与附录 A 锚点全表 162 行）
- **未确证 / 待跟踪**（不入正文结论）：
  1. 抢占后 `get_computed_blocks` 是否真退化为零命中——§4.2 的推断需要构造实验确证（打印 `num_preemptions` 与命中数）。
  2. structured output 下验证判据的参照分布语义：是"近似"还是"仓库定义的正确答案"——仓库内**未找到明文定义**，检索 `docs/` 无结论。
  3. `vllm/v1/worker/gpu/model_runner.py` 与 `gpu_model_runner.py` 的默认关系（两套 runner 并存）。
  4. vLLM 是否有与 SGLang `event_loop_overlap` 对应的调度重叠机制。
  5. SGLang 侧的抢占恢复与语法约束下草稿处理——**本轮未 clone SGLang，不填对照表空格**。

---


---

## 附录 A：锚点全表（162 处机械核验）

核验命令模板（钉住 commit，逐条执行）：

```bash
git show fa75d3456d60a5ffe923818c4b495295675b38e1:<path> | sed -n "<行>p"
```

| # | 文档 | `文件:行` | 该行实际内容（截断） | 该行声明的符号 | 判定 |
| --: | :-- | :-- | :-- | :-- | :-- |
| 1 | kv-cache-and-prefix-reuse | `block_pool.py:136` | class BlockPool: | `class BlockPool` | ✅ 命中 |
| 2 | kv-cache-and-prefix-reuse | `block_pool.py:147-150` | 147: hash_block_size: The block size of which the block hashes are computed. // 150: actual  | `hash_block_size` | ✅ 命中（区间端点均为代码行） |
| 3 | kv-cache-and-prefix-reuse | `block_pool.py:178` | self.free_block_queue = FreeKVCacheBlockQueue(self.blocks) | `self.free_block_queue` | ✅ 命中 |
| 4 | kv-cache-and-prefix-reuse | `block_pool.py:182` | self.cached_block_hashes_by_block: dict[int, set[BlockHashWithGroupId]] = {} | `self.cached_block_hashes_by_block` | ✅ 命中 |
| 5 | kv-cache-and-prefix-reuse | `block_pool.py:184-188` | 184: # To represent a placeholder block with block_id=0. // 188: self.null_block.is_null = T | `# To represent a placeholder block with bloc` | ✅ 命中（显式注释段区间，起行或止行为注释） |
| 6 | kv-cache-and-prefix-reuse | `block_pool.py:187` | self.null_block = self.free_block_queue.popleft() | `self.null_block` | ✅ 命中 |
| 7 | kv-cache-and-prefix-reuse | `block_pool.py:213-224` | 213: cached_blocks = [] // 224: return cached_blocks | `cached_blocks` | ✅ 命中（区间端点均为代码行） |
| 8 | kv-cache-and-prefix-reuse | `block_pool.py:226` | def cache_full_blocks( | `def cache_full_blocks` | ✅ 命中 |
| 9 | kv-cache-and-prefix-reuse | `block_pool.py:35` | class BlockHashToBlockMap: | `class BlockHashToBlockMap` | ✅ 命中 |
| 10 | kv-cache-and-prefix-reuse | `block_pool.py:666` | def get_new_blocks(self, num_blocks: int) -> list[KVCacheBlock]: | `def get_new_blocks` | ✅ 命中 |
| 11 | kv-cache-and-prefix-reuse | `block_pool.py:681` | ret: list[KVCacheBlock] = self.free_block_queue.popleft_n(num_blocks) | `ret` | ✅ 命中 |
| 12 | kv-cache-and-prefix-reuse | `block_pool.py:689` | self._maybe_evict_cached_block(block) | `self._maybe_evict_cached_block(block)` | ✅ 命中 |
| 13 | kv-cache-and-prefix-reuse | `block_pool.py:690-691` | 690: assert block.ref_cnt == 0 // 691: block.ref_cnt += 1 | `assert block.ref_cnt == 0 // 691: block.ref_` | ✅ 命中（区间端点均为代码行） |
| 14 | kv-cache-and-prefix-reuse | `block_pool.py:708` | def unpin_blocks( | `def unpin_blocks` | ✅ 命中 |
| 15 | kv-cache-and-prefix-reuse | `block_pool.py:729` | def _maybe_evict_cached_block(self, block: KVCacheBlock) -> bool: | `def _maybe_evict_cached_block` | ✅ 命中 |
| 16 | kv-cache-and-prefix-reuse | `block_pool.py:752` | def touch(self, blocks: Sequence[KVCacheBlock]) -> None: | `def touch` | ✅ 命中 |
| 17 | kv-cache-and-prefix-reuse | `block_pool.py:776` | def free_blocks(self, ordered_blocks: Iterable[KVCacheBlock]) -> None: | `def free_blocks` | ✅ 命中 |
| 18 | kv-cache-and-prefix-reuse | `block_pool.py:851` | self.cached_block_hash_to_block = BlockHashToBlockMap() | `self.cached_block_hash_to_block` | ✅ 命中 |
| 19 | kv-cache-and-prefix-reuse | `block_table.py:80-83` | 80: self.block_table = self._make_buffer( // 83: self.num_blocks_per_row = np.zeros(max_num_ | `self.block_table` | ✅ 命中（区间端点均为代码行） |
| 20 | kv-cache-and-prefix-reuse | `kv_cache_manager.py:289-300` | 289: # NOTE: When all tokens hit the cache, we must recompute the last token // 300: ) | `# NOTE: When all tokens hit the cache, we mu` | ✅ 命中（显式注释段区间，起行或止行为注释） |
| 21 | kv-cache-and-prefix-reuse | `kv_cache_manager.py:295` | max_cache_hit_length = request.num_tokens - 1 | `max_cache_hit_length` | ✅ 命中 |
| 22 | kv-cache-and-prefix-reuse | `kv_cache_manager.py:35` | class KVCacheBlocks: | `class KVCacheBlocks` | ✅ 命中 |
| 23 | kv-cache-and-prefix-reuse | `kv_cache_manager.py:417-460` | 417: skip_zeroing_group_ids: Groups whose external-token blocks will be // 460: if we have s | `skip_zeroing_group_ids` | ✅ 命中（区间端点均为代码行） |
| 24 | kv-cache-and-prefix-reuse | `kv_cache_utils.py:1003` | caching_hash_fn, prev_block_hash_value, block_tokens, extra_keys | `caching_hash_fn, prev_block_hash_value, bloc` | ✅ 命中 |
| 25 | kv-cache-and-prefix-reuse | `kv_cache_utils.py:1111` | class BlockHashListWithBlockSize: | `class BlockHashListWithBlockSize` | ✅ 命中 |
| 26 | kv-cache-and-prefix-reuse | `kv_cache_utils.py:258` | class FreeKVCacheBlockQueue: | `class FreeKVCacheBlockQueue` | ✅ 命中 |
| 27 | kv-cache-and-prefix-reuse | `kv_cache_utils.py:258-274` | 258: class FreeKVCacheBlockQueue: // 274: blocks of a request. This operation is outside of  | `class FreeKVCacheBlockQueue` | ✅ 命中（区间端点均为代码行） |
| 28 | kv-cache-and-prefix-reuse | `kv_cache_utils.py:267-274` | 267: The queue is ordered by block ID in the beginning. When a block is allocated // 274: bl | `The queue is ordered by block ID in the begi` | ✅ 命中（区间端点均为代码行） |
| 29 | kv-cache-and-prefix-reuse | `kv_cache_utils.py:966` | def request_block_hasher(request: Request) -> list[BlockHash]: | `def request_block_hasher` | ✅ 命中 |
| 30 | kv-cache-and-prefix-reuse | `kv_cache_utils.py:993` | break | `break` | ✅ 命中 |
| 31 | kv-cache-and-prefix-reuse | `request.py:225` | self.block_hashes: list[BlockHash] = [] | `self.block_hashes` | ✅ 命中 |
| 32 | kv-cache-and-prefix-reuse | `request.py:285-288` | 285: def update_block_hashes(self) -> None: // 288: self.block_hashes.extend(self._block_has | `def update_block_hashes` | ✅ 命中（区间端点均为代码行） |
| 33 | kv-cache-and-prefix-reuse | `scheduler.py:1649` | def _preempt_request( | `def _preempt_request` | ✅ 命中 |
| 34 | kv-cache-and-prefix-reuse | `scheduler.py:1664` | ) | `)` | ✅ 命中 |
| 35 | kv-cache-and-prefix-reuse | `scheduler.py:1671` | request.num_computed_tokens = 0 | `request.num_computed_tokens` | ✅ 命中 |
| 36 | kv-cache-and-prefix-reuse | `scheduler.py:1692` | self.reset_preempted_req_ids.add(request.request_id) | `self.reset_preempted_req_ids.add(request.req` | ✅ 命中 |
| 37 | kv-cache-and-prefix-reuse | `single_type_kv_cache_manager.py:735` | def find_longest_cache_hit( | `def find_longest_cache_hit` | ✅ 命中 |
| 38 | kv-cache-and-prefix-reuse | `vllm/v1/core/kv_cache_manager.py:295` | max_cache_hit_length = request.num_tokens - 1 | `max_cache_hit_length` | ✅ 命中 |
| 39 | kv-cache-and-prefix-reuse | `vllm/v1/core/kv_cache_utils.py:993` | break | `break` | ✅ 命中 |
| 40 | kv-cache-and-prefix-reuse | `vllm/v1/core/sched/scheduler.py:1671` | request.num_computed_tokens = 0 | `request.num_computed_tokens` | ✅ 命中 |
| 41 | kv-cache-and-prefix-reuse | `vllm/v1/core/single_type_kv_cache_manager.py:769` | fine_grained = ( | `fine_grained` | ✅ 命中 |
| 42 | kv-cache-and-prefix-reuse | `vllm/v1/core/single_type_kv_cache_manager.py:806` | for fine_idx in range(max_partial_idx - 1, first_partial_idx - 1, -1): | `for fine_idx in range(max_partial_idx - 1, f` | ✅ 命中 |
| 43 | kv-cache-and-prefix-reuse | `vllm/v1/core/single_type_kv_cache_manager.py:827` | num_blocks = cdiv(hit_length, block_size) | `num_blocks` | ✅ 命中 |
| 44 | report | `block_pool.py:136` | class BlockPool: | `class BlockPool` | ✅ 命中 |
| 45 | report | `block_pool.py:190-193` | 190: self.enable_kv_cache_events = enable_kv_cache_events // 193: self.metrics_collector = m | `self.enable_kv_cache_events` | ✅ 命中（区间端点均为代码行） |
| 46 | report | `block_pool.py:35` | class BlockHashToBlockMap: | `class BlockHashToBlockMap` | ✅ 命中 |
| 47 | report | `block_pool.py:681` | ret: list[KVCacheBlock] = self.free_block_queue.popleft_n(num_blocks) | `ret` | ✅ 命中 |
| 48 | report | `block_pool.py:689` | self._maybe_evict_cached_block(block) | `self._maybe_evict_cached_block(block)` | ✅ 命中 |
| 49 | report | `block_pool.py:729` | def _maybe_evict_cached_block(self, block: KVCacheBlock) -> bool: | `def _maybe_evict_cached_block` | ✅ 命中 |
| 50 | report | `block_pool.py:791-799` | 791: continue // 799: blocks_to_evict_first.append(block) | `continue // 799: blocks_to_evict_first.appen` | ✅ 命中（区间端点均为代码行） |
| 51 | report | `block_table.py:114` | def append_row( | `def append_row` | ✅ 命中 |
| 52 | report | `block_table.py:49` | class BlockTable: | `class BlockTable` | ✅ 命中 |
| 53 | report | `block_table.py:80` | self.block_table = self._make_buffer( | `self.block_table` | ✅ 命中 |
| 54 | report | `cache.py:142` | enable_prefix_caching: bool = True | `enable_prefix_caching` | ✅ 命中 |
| 55 | report | `kv_cache_coordinator.py:89` | class KVCacheCoordinator(ABC): | `class KVCacheCoordinator` | ✅ 命中 |
| 56 | report | `kv_cache_manager.py:417-460` | 417: skip_zeroing_group_ids: Groups whose external-token blocks will be // 460: if we have s | `skip_zeroing_group_ids` | ✅ 命中（区间端点均为代码行） |
| 57 | report | `kv_cache_utils.py:1003` | caching_hash_fn, prev_block_hash_value, block_tokens, extra_keys | `caching_hash_fn, prev_block_hash_value, bloc` | ✅ 命中 |
| 58 | report | `kv_cache_utils.py:258` | class FreeKVCacheBlockQueue: | `class FreeKVCacheBlockQueue` | ✅ 命中 |
| 59 | report | `kv_cache_utils.py:993` | break | `break` | ✅ 命中 |
| 60 | report | `llm_base_proposer.py:454` | if not self._enable_probabilistic_draft_probs: | `if not self._enable_probabilistic_draft_prob` | ✅ 命中 |
| 61 | report | `model_runner.py:1636` | self.structured_outputs_worker.apply_grammar_bitmask( | `self.structured_outputs_worker.apply_grammar` | ✅ 命中 |
| 62 | report | `model_runner.py:1636-1641` | 1636: self.structured_outputs_worker.apply_grammar_bitmask( // 1641: ) | `self.structured_outputs_worker.apply_grammar` | ✅ 命中（区间端点均为代码行） |
| 63 | report | `rejection_sampler.py:106` | def forward( | `def forward` | ✅ 命中 |
| 64 | report | `rejection_sampler.py:45` | class RejectionSampler(nn.Module): | `class RejectionSampler` | ✅ 命中 |
| 65 | report | `rejection_sampler.py:471` | target_argmax = target_logits.argmax(dim=-1) | `target_argmax` | ✅ 命中 |
| 66 | report | `rejection_sampler.py:487` | target_probs = target_logits.softmax(dim=-1, dtype=torch.float32) | `target_probs` | ✅ 命中 |
| 67 | report | `rejection_sampler.py:871-872` | 871: if NO_DRAFT_PROBS: // 872: draft_prob = 1 | `if NO_DRAFT_PROBS` | ✅ 命中（区间端点均为代码行） |
| 68 | report | `rejection_sampler.py:872` | draft_prob = 1 | `draft_prob` | ✅ 命中 |
| 69 | report | `rejection_sampler.py:884` | accepted = draft_prob > 0 and target_prob / draft_prob >= uniform_prob | `accepted` | ✅ 命中 |
| 70 | report | `rejection_sampler_utils.py:1024` | draft_logits: torch.Tensor / None, | `draft_logits` | ✅ 命中 |
| 71 | report | `request_queue.py:13` | class SchedulingPolicy(Enum): | `class SchedulingPolicy` | ✅ 命中 |
| 72 | report | `scheduler.py:1649` | def _preempt_request( | `def _preempt_request` | ✅ 命中 |
| 73 | report | `scheduler.py:1664-1671` | 1664: ) // 1671: request.num_computed_tokens = 0 | `) // 1671: request.num_computed_tokens = 0` | ✅ 命中（区间端点均为代码行） |
| 74 | report | `scheduler.py:1671` | request.num_computed_tokens = 0 | `request.num_computed_tokens` | ✅ 命中 |
| 75 | report | `scheduler.py:1692` | self.reset_preempted_req_ids.add(request.request_id) | `self.reset_preempted_req_ids.add(request.req` | ✅ 命中 |
| 76 | report | `scheduler.py:2210` | spec_decoding_stats = self.make_spec_decoding_stats( | `spec_decoding_stats` | ✅ 命中 |
| 77 | report | `scheduler.py:2679` | spec_token_ids = self.structured_output_manager.validate_tokens( | `spec_token_ids` | ✅ 命中 |
| 78 | report | `scheduler.py:2679-2686` | 2679: spec_token_ids = self.structured_output_manager.validate_tokens( // 2686: num_invalid_ | `spec_token_ids` | ✅ 命中（区间端点均为代码行） |
| 79 | report | `scheduler.py:3058` | num_draft_tokens -= num_invalid_spec_tokens.get(request_id, 0) | `num_draft_tokens -= num_invalid_spec_tokens.` | ✅ 命中 |
| 80 | report | `scheduler.py:621` | def schedule(self, throttle_prefills: bool = False) -> SchedulerOutput: | `def schedule` | ✅ 命中 |
| 81 | report | `scheduler.py:623-632` | 623: # NOTE(woosuk) on the scheduling algorithm: // 632: # and the "jump decoding" optimizat | `# NOTE(woosuk) on the scheduling algorithm:` | ✅ 命中（显式注释段区间，起行或止行为注释） |
| 82 | report | `scheduler.py:623-641` | 623: # NOTE(woosuk) on the scheduling algorithm: // 641: token_budget = self.max_num_schedul | `# NOTE(woosuk) on the scheduling algorithm:` | ✅ 命中（显式注释段区间，起行或止行为注释） |
| 83 | report | `scheduler.py:641` | token_budget = self.max_num_scheduled_tokens | `token_budget` | ✅ 命中 |
| 84 | report | `scheduler.py:641-644` | 641: token_budget = self.max_num_scheduled_tokens // 644: input_budget = self.scheduler_conf | `token_budget` | ✅ 命中（区间端点均为代码行） |
| 85 | report | `scheduler.py:643` | draft_slots = spec.max_num_new_slots_for_drafting if spec is not None else 0 | `draft_slots` | ✅ 命中 |
| 86 | report | `scheduler.py:716` | if input_budget <= draft_slots: | `if input_budget <= draft_slots` | ✅ 命中 |
| 87 | report | `scheduler.py:833-861` | 833: new_blocks = self.kv_cache_manager.allocate_slots( // 861: break | `new_blocks` | ✅ 命中（区间端点均为代码行） |
| 88 | report | `single_type_kv_cache_manager.py:49` | class SingleTypeKVCacheManager(ABC): | `class SingleTypeKVCacheManager` | ✅ 命中 |
| 89 | report | `single_type_kv_cache_manager.py:786` | for block_hash in itertools.islice(full_block_hashes, max_length // block_size): | `for block_hash in itertools.islice(full_bloc` | ✅ 命中 |
| 90 | report | `single_type_kv_cache_manager.py:786-792` | 786: for block_hash in itertools.islice(full_block_hashes, max_length // block_size): // 792 | `for block_hash in itertools.islice(full_bloc` | ✅ 命中（区间端点均为代码行） |
| 91 | report | `single_type_kv_cache_manager.py:796-815` | 796: if fine_grained: // 815: break | `if fine_grained` | ✅ 命中（区间端点均为代码行） |
| 92 | report | `spec_decode/utils.py:64-68` | 64: if not input_batch.has_structured_output_reqs: // 68: return | `if not input_batch.has_structured_output_req` | ✅ 命中（区间端点均为代码行） |
| 93 | report | `speculative.py:604` | draft_sample_method: DraftSampleMethod = "greedy" | `draft_sample_method` | ✅ 命中 |
| 94 | report | `speculator.py:413-419` | 413: return // 419: if not hasattr(self.model, "get_top_tokens"): | `return // 419: if not hasattr(self.model, "g` | ✅ 命中（区间端点均为代码行） |
| 95 | report | `stats.py:367` | num_draft_tokens: Total proposed draft tokens, after the | `num_draft_tokens` | ✅ 命中 |
| 96 | report | `structured_output/__init__.py:346` | def validate_tokens(self, request: "Request", spec_tokens: list[int]) -> list[int]: | `def validate_tokens` | ✅ 命中 |
| 97 | report | `structured_output/__init__.py:455-489` | 455: failed_index: int / None = None // 489: bitmask[cumulative_index].copy_(bitmask[failed_ | `failed_index` | ✅ 命中（区间端点均为代码行） |
| 98 | report | `structured_output/__init__.py:458` | if failed_index is not None: | `if failed_index is not None` | ✅ 命中 |
| 99 | report | `structured_output/utils.py:48` | def strip_speculative_padding(token_ids: list[int]) -> list[int]: | `def strip_speculative_padding` | ✅ 命中 |
| 100 | report | `structured_outputs.py:173` | bitmask_idx = tl.program_id(0) | `bitmask_idx` | ✅ 命中 |
| 101 | report | `structured_outputs.py:195-198` | 195: tl.store( // 198: mask=position_is_active & bitmask & (block_offset < vocab_size), | `tl.store( // 198: mask=position_is_active &` | ✅ 命中（区间端点均为代码行） |
| 102 | report | `vllm.py:1308-1316` | 1308: speculative_config = self.speculative_config // 1316: "Speculative decoding with water | `speculative_config` | ✅ 命中（区间端点均为代码行） |
| 103 | report | `vllm/v1/core/block_pool.py:793` | other_pools.setdefault(block.pool, []).append(block) | `other_pools.setdefault(block.pool, []).appen` | ✅ 命中 |
| 104 | report | `vllm/v1/core/kv_cache_utils.py:1003` | caching_hash_fn, prev_block_hash_value, block_tokens, extra_keys | `caching_hash_fn, prev_block_hash_value, bloc` | ✅ 命中 |
| 105 | report | `vllm/v1/core/single_type_kv_cache_manager.py:786` | for block_hash in itertools.islice(full_block_hashes, max_length // block_size): | `for block_hash in itertools.islice(full_bloc` | ✅ 命中 |
| 106 | report | `vllm/v1/sample/rejection_sampler.py:487` | target_probs = target_logits.softmax(dim=-1, dtype=torch.float32) | `target_probs` | ✅ 命中 |
| 107 | report | `vllm/v1/worker/gpu/model_runner.py:1636` | self.structured_outputs_worker.apply_grammar_bitmask( | `self.structured_outputs_worker.apply_grammar` | ✅ 命中 |
| 108 | report | `vllm/v1/worker/gpu/structured_outputs.py:197` | -float("inf"), | `-float("inf"),` | ✅ 命中 |
| 109 | scheduling-and-spec-decode | `gpu_model_runner.py:4987-4990` | 4987: if hasattr(self.drafter, "take_last_draft_probs"): // 4990: self._draft_probs = draft_ | `if hasattr(self.drafter, "take_last_draft_pr` | ✅ 命中（区间端点均为代码行） |
| 110 | scheduling-and-spec-decode | `llm_base_proposer.py:257-260` | 257: self._enable_probabilistic_draft_probs = ( // 260: ) | `self._enable_probabilistic_draft_probs` | ✅ 命中（区间端点均为代码行） |
| 111 | scheduling-and-spec-decode | `llm_base_proposer.py:454` | if not self._enable_probabilistic_draft_probs: | `if not self._enable_probabilistic_draft_prob` | ✅ 命中 |
| 112 | scheduling-and-spec-decode | `llm_base_proposer.py:511` | def propose( | `def propose` | ✅ 命中 |
| 113 | scheduling-and-spec-decode | `llm_base_proposer.py:629-635` | 629: draft_token_ids, draft_probs = self._sample_draft_tokens( // 635: ).contiguous() | `draft_token_ids, draft_probs = self._sample_` | ✅ 命中（区间端点均为代码行） |
| 114 | scheduling-and-spec-decode | `model_runner.py:1636` | self.structured_outputs_worker.apply_grammar_bitmask( | `self.structured_outputs_worker.apply_grammar` | ✅ 命中 |
| 115 | scheduling-and-spec-decode | `rejection_sampler.py:106-121` | 106: def forward( // 121: not provided, which is the case for ngram spec decode. | `def forward` | ✅ 命中（区间端点均为代码行） |
| 116 | scheduling-and-spec-decode | `rejection_sampler.py:487` | target_probs = target_logits.softmax(dim=-1, dtype=torch.float32) | `target_probs` | ✅ 命中 |
| 117 | scheduling-and-spec-decode | `rejection_sampler.py:492-502` | 492: recovered_token_ids = sample_recovered_tokens( // 502: ) | `recovered_token_ids` | ✅ 命中（区间端点均为代码行） |
| 118 | scheduling-and-spec-decode | `rejection_sampler.py:829` | def rejection_random_sample_kernel( | `def rejection_random_sample_kernel` | ✅ 命中 |
| 119 | scheduling-and-spec-decode | `rejection_sampler.py:860-890` | 860: for pos in range(num_draft_tokens): // 890: tl.store( | `for pos in range(num_draft_tokens)` | ✅ 命中（区间端点均为代码行） |
| 120 | scheduling-and-spec-decode | `rejection_sampler.py:864-866` | 864: if draft_token_id < 0: // 866: accepted = False | `if draft_token_id < 0` | ✅ 命中（区间端点均为代码行） |
| 121 | scheduling-and-spec-decode | `rejection_sampler.py:870` | else: | `else` | ✅ 命中 |
| 122 | scheduling-and-spec-decode | `rejection_sampler.py:871-884` | 871: if NO_DRAFT_PROBS: // 884: accepted = draft_prob > 0 and target_prob / draft_prob >= un | `if NO_DRAFT_PROBS` | ✅ 命中（区间端点均为代码行） |
| 123 | scheduling-and-spec-decode | `rejection_sampler.py:881` | ) | `)` | ✅ 命中 |
| 124 | scheduling-and-spec-decode | `rejection_sampler.py:884` | accepted = draft_prob > 0 and target_prob / draft_prob >= uniform_prob | `accepted` | ✅ 命中 |
| 125 | scheduling-and-spec-decode | `rejection_sampler_utils.py:1020-1024` | 1020: def rejection_sample( // 1024: draft_logits: torch.Tensor / None, | `def rejection_sample` | ✅ 命中（区间端点均为代码行） |
| 126 | scheduling-and-spec-decode | `request_queue.py:13-17` | 13: class SchedulingPolicy(Enum): // 17: PRIORITY = "priority" | `class SchedulingPolicy` | ✅ 命中（区间端点均为代码行） |
| 127 | scheduling-and-spec-decode | `request_queue.py:131-159` | 131: class PriorityRequestQueue(RequestQueue): // 159: def prepend_request(self, request: Re | `class PriorityRequestQueue` | ✅ 命中（区间端点均为代码行） |
| 128 | scheduling-and-spec-decode | `sample/rejection_sampler.py:106` | def forward( | `def forward` | ✅ 命中 |
| 129 | scheduling-and-spec-decode | `scheduler.py:1189-1208` | 1189: if ( // 1208: pad_spec_decode = True | `if ( // 1208` | ✅ 命中（区间端点均为代码行） |
| 130 | scheduling-and-spec-decode | `scheduler.py:1649-1692` | 1649: def _preempt_request( // 1692: self.reset_preempted_req_ids.add(request.request_id) | `def _preempt_request` | ✅ 命中（区间端点均为代码行） |
| 131 | scheduling-and-spec-decode | `scheduler.py:1657-1660` | 1657: drop_stale_output: drop (rather than deliver) any in-flight output; used // 1660: whic | `drop_stale_output` | ✅ 命中（区间端点均为代码行） |
| 132 | scheduling-and-spec-decode | `scheduler.py:1671` | request.num_computed_tokens = 0 | `request.num_computed_tokens` | ✅ 命中 |
| 133 | scheduling-and-spec-decode | `scheduler.py:1672-1673` | 1672: if request.spec_token_ids: // 1673: request.spec_token_ids = [] | `if request.spec_token_ids` | ✅ 命中（区间端点均为代码行） |
| 134 | scheduling-and-spec-decode | `scheduler.py:2207` | request.num_computed_tokens -= num_rejected | `request.num_computed_tokens -= num_rejected` | ✅ 命中 |
| 135 | scheduling-and-spec-decode | `scheduler.py:2221-2228` | 2221: adj_draft_tokens = num_draft_tokens // 2228: num_accepted=num_accepted, | `adj_draft_tokens` | ✅ 命中（区间端点均为代码行） |
| 136 | scheduling-and-spec-decode | `scheduler.py:223` | self.waiting = create_request_queue(self.policy) | `self.waiting` | ✅ 命中 |
| 137 | scheduling-and-spec-decode | `scheduler.py:227` | self.kv_holding_waiting = create_request_queue(self.policy) | `self.kv_holding_waiting` | ✅ 命中 |
| 138 | scheduling-and-spec-decode | `scheduler.py:2679` | spec_token_ids = self.structured_output_manager.validate_tokens( | `spec_token_ids` | ✅ 命中 |
| 139 | scheduling-and-spec-decode | `scheduler.py:2679-2686` | 2679: spec_token_ids = self.structured_output_manager.validate_tokens( // 2686: num_invalid_ | `spec_token_ids` | ✅ 命中（区间端点均为代码行） |
| 140 | scheduling-and-spec-decode | `scheduler.py:3058` | num_draft_tokens -= num_invalid_spec_tokens.get(request_id, 0) | `num_draft_tokens -= num_invalid_spec_tokens.` | ✅ 命中 |
| 141 | scheduling-and-spec-decode | `scheduler.py:623-641` | 623: # NOTE(woosuk) on the scheduling algorithm: // 641: token_budget = self.max_num_schedul | `# NOTE(woosuk) on the scheduling algorithm:` | ✅ 命中（显式注释段区间，起行或止行为注释） |
| 142 | scheduling-and-spec-decode | `scheduler.py:641` | token_budget = self.max_num_scheduled_tokens | `token_budget` | ✅ 命中 |
| 143 | scheduling-and-spec-decode | `scheduler.py:643` | draft_slots = spec.max_num_new_slots_for_drafting if spec is not None else 0 | `draft_slots` | ✅ 命中 |
| 144 | scheduling-and-spec-decode | `scheduler.py:644` | input_budget = self.scheduler_config.max_num_batched_tokens | `input_budget` | ✅ 命中 |
| 145 | scheduling-and-spec-decode | `scheduler.py:832-899` | 832: while True: // 899: break | `while True: // 899: break` | ✅ 命中（区间端点均为代码行） |
| 146 | scheduling-and-spec-decode | `spec_decode/utils.py:64` | if not input_batch.has_structured_output_reqs: | `if not input_batch.has_structured_output_req` | ✅ 命中 |
| 147 | scheduling-and-spec-decode | `spec_decode/utils.py:64-68` | 64: if not input_batch.has_structured_output_reqs: // 68: return | `if not input_batch.has_structured_output_req` | ✅ 命中（区间端点均为代码行） |
| 148 | scheduling-and-spec-decode | `spec_decode/utils.py:88` | draft_token_ids = [[-1] * self.num_draft_tokens for _ in self.req_ids] | `draft_token_ids` | ✅ 命中 |
| 149 | scheduling-and-spec-decode | `speculative.py:533` | rejection_sample_method: RejectionSampleMethod = "standard" | `rejection_sample_method` | ✅ 命中 |
| 150 | scheduling-and-spec-decode | `speculative.py:533-547` | 533: rejection_sample_method: RejectionSampleMethod = "standard" // 547: Mutually exclusive  | `rejection_sample_method` | ✅ 命中（区间端点均为代码行） |
| 151 | scheduling-and-spec-decode | `speculative.py:604` | draft_sample_method: DraftSampleMethod = "greedy" | `draft_sample_method` | ✅ 命中 |
| 152 | scheduling-and-spec-decode | `stats.py:367` | num_draft_tokens: Total proposed draft tokens, after the | `num_draft_tokens` | ✅ 命中 |
| 153 | scheduling-and-spec-decode | `stats.py:367-368` | 367: num_draft_tokens: Total proposed draft tokens, after the // 368: grammar-invalidated (` | `num_draft_tokens` | ✅ 命中（区间端点均为代码行） |
| 154 | scheduling-and-spec-decode | `structured_output/__init__.py:455-489` | 455: failed_index: int / None = None // 489: bitmask[cumulative_index].copy_(bitmask[failed_ | `failed_index` | ✅ 命中（区间端点均为代码行） |
| 155 | scheduling-and-spec-decode | `structured_output/utils.py:48-58` | 48: def strip_speculative_padding(token_ids: list[int]) -> list[int]: // 58: return token_id | `def strip_speculative_padding` | ✅ 命中（区间端点均为代码行） |
| 156 | scheduling-and-spec-decode | `structured_outputs.py:195-198` | 195: tl.store( // 198: mask=position_is_active & bitmask & (block_offset < vocab_size), | `tl.store( // 198: mask=position_is_active &` | ✅ 命中（区间端点均为代码行） |
| 157 | scheduling-and-spec-decode | `vllm/v1/core/sched/scheduler.py:1189` | if ( | `if (` | ✅ 命中 |
| 158 | scheduling-and-spec-decode | `vllm/v1/core/sched/scheduler.py:1672` | if request.spec_token_ids: | `if request.spec_token_ids` | ✅ 命中 |
| 159 | scheduling-and-spec-decode | `vllm/v1/core/sched/scheduler.py:1681` | request.drop_stale_output = drop_stale_output or ( | `request.drop_stale_output` | ✅ 命中 |
| 160 | scheduling-and-spec-decode | `vllm/v1/core/sched/scheduler.py:2205-2209` | 2205: if not output_is_stale: // 2209: request.num_output_placeholders -= num_rejected | `if not output_is_stale` | ✅ 命中（区间端点均为代码行） |
| 161 | scheduling-and-spec-decode | `vllm/v1/sample/rejection_sampler.py:487` | target_probs = target_logits.softmax(dim=-1, dtype=torch.float32) | `target_probs` | ✅ 命中 |
| 162 | scheduling-and-spec-decode | `vllm/v1/worker/gpu/model_runner.py:1636` | self.structured_outputs_worker.apply_grammar_bitmask( | `self.structured_outputs_worker.apply_grammar` | ✅ 命中 |

*锚点全表说明：`该行声明的符号` 列由该行原文以 `class/def/赋值/if/assert/raise` 等模式解析得出；区间锚点取起始行。判定为「显式注释段区间」的 5 行，正文均已注明其为注释段，起/止行内容见表。*

*本文完。所有判断仅覆盖上表声明的阅读范围；范围外一律不作结论。*
