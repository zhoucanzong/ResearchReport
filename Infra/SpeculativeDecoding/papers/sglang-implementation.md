# SGLang 实现核验：EAGLE 草稿链与 topk=1 的拒绝采样（仓库 @ 2a08e261）

> **一手来源**：`sgl-project/sglang` @ **`2a08e261ecd4cdfb04ec354f9005f18b88108b7d`**（2026-10-16），只读快照；license = **Apache-2.0**。｜ **主等级**：`[精读原文]`（代码路径）
> **核验范围**：`python/sglang/srt/speculative/eagle_worker_v2.py`、`eagle_utils.py`、`eagle_info.py`、`runtime_context.py` 的投机相关分支。
> **一句话定位**：SGLang 的 EAGLE 路径把“贪心验证”和“采样验证”彻底分开；2026-10 的主线已支持 **topk=1 链式草稿 + 真 draft 概率 + 拒绝采样**，并用 `speculative_use_rejection_sampling` 开关与一条 `assert topk == 1` 把适用范围钉死。
> **亮点与差异四行**
> - **一句话亮点**：在 `eagle_sample` 里按 `use_rejection_sampling` 选择不同的验证 kernel；topk=1 链式草稿可以拿到真实 `draft_probs`，不再把草稿概率当 one-hot。
> - **新在哪（相对 2026 年初）**：历史 issue #10308 描述的“tree attention 把 draft 概率置 1”在 **topk=1 链式路径**上已有对应实现（`draft_probs` 字段 + `chain_speculative_sampling_triton` + 严格校验）；但**不是通过该 issue 的 linked PR 合入**。
> - **证据强度**：**代码级**。所有结论有 `文件:行`；没有跑 benchmark，因此**不报告 SGLang 的加速比**（只引用 EAGLE-3 论文里 SGLang 团队给出的官方吞吐表，并标注来源）。
> - **值不值得引用**：**值得作为“生产框架如何处理 topk=1 采样无损性”的一手证据**；引用必须钉 commit，并说明“tree topk>1 仍走 target-only kernel”。

---

## 0. 七问速答（代码版一页）

| # | 七问 | 一句话回答 |
| --: | :-- | :-- |
| 1 | 解决什么问题 | 在 EAGLE 草稿链上同时支持 greedy 与 sampling；sampling 时把草稿真实概率传给验证，避免“one-hot 提议”带来的接受率损失。 |
| 2 | 机制与关键参数 | `speculative_use_rejection_sampling` 开关；`speculative_eagle_topk`（开启拒绝采样时必须 **1**）；`speculative_num_steps`、`speculative_num_draft_tokens`；`draft_probs` 字段。 |
| 3 | 覆盖范围 | EAGLE-2/3 草稿（`EagleWorkerV2`）、MTP、DFlash；topk=1 链式草稿；非 greedy 请求。 |
| 4 | 带条件的“结果” | 开启拒绝采样 → 断言 topk=1；非 greedy 且开启 → 构造 `draft_probs` 并走 `chain_speculative_sampling_triton`；否则走 `tree_speculative_sampling_target_only`（`draft_probs` 置零）。 |
| 5 | 消融/开关 | 开/关 `use_rejection_sampling` 改变验证 kernel；greedy 批跳过 draft_probs 构造（`is_all_greedy`）。 |
| 6 | 何时失效 | topk>1 不适用（断言失败）；`draft_probs` 缺失/词表不匹配 → 抛 `ValueError`；greedy 路径不需要也不读 draft_probs。 |
| 7 | 可判定差异 | vs vLLM：SGLang 把“topk=1 链式 + 拒绝采样”做成硬约束；vLLM 用 `draft_sample_method` 区分 greedy/probabilistic，且不要求 topk=1。 |

---

## 1. 核验方法与边界

- **版本钉死**：所有行号对应 commit `2a08e261`（2026-10-16）；换版本行号会漂移。
- **只读**：快照在 `/tmp/sglang-src` + 按文件抓取的 raw 副本，位于仓库外；不构建、不修改。
- **不跑 benchmark**：本分册不报告 SGLang 的加速比；唯一引用的吞吐数字来自 EAGLE-3 论文 Table 4（SGLang 团队提供），并明确标注。
- **不做全仓库审计**：只看投机路径直接相关文件；attention backend、CUDA graph 细节不展开。

---

## 2. 代码地图

| 关注点 | 文件 | 行号（本 commit） | 说明 |
| :-- | :-- | :-- | :-- |
| 顶层开关 | `eagle_worker_v2.py` | `178–180` | `self.topk = get_spec().speculative_eagle_topk`；开启拒绝采样时 `assert self.topk == 1` |
| 步数/草稿数 | 同上 | `184–186` | `speculative_num_steps`、`speculative_num_draft_tokens` |
| 草稿输出 | 同上 | `648–657` | CUDA graph 输出 `draft_probs`，并 `clone()` 出图内存池 |
| 构造验证输入 | 同上 | `676–681` | `build_eagle_verify_input(..., draft_probs, topk=...)` |
| 何时需要 draft_probs | 同上 | `727–733` | `needs_draft_probs = speculative_use_rejection_sampling and not is_all_greedy` |
| 树构造 | `eagle_utils.py` | `157` | `build_tree_kernel_efficient(...)` |
| 贪心验证 | 同上 | `384` | `verify_tree_greedy_func(...)` |
| 统一验证入口 | 同上 | `741` | `eagle_sample(...)` |
| 读开关 | 同上 | `860` | `use_rejection_sampling = get_spec().speculative_use_rejection_sampling` |
| 贪心分支 | 同上 | `862–916` | `_verify_uses_greedy(...)` → `verify_tree_greedy_func` |
| 采样分支 | 同上 | `947–1030` | 选 `chain_speculative_sampling_triton` 或 `tree_speculative_sampling_target_only` |
| draft_probs 校验 | 同上 | `1000–1013` | 拒绝采样时检查 `draft_probs` 存在且词表匹配，否则 `ValueError` |
| 传入 kernel | 同上 | `1030–1044` | `target_probs`、`draft_probs`、`uniform_samples` 一起传 |
| 字段定义 | `eagle_info.py` | `35`、`162` | `EagleVerifyInput.draft_probs`、`EagleDraftInput.draft_probs` |

---

## 3. 一次 EAGLE 迭代的控制流

按 `eagle_worker_v2.py` 的顺序：

1. **draft 前向**：跑 `speculative_num_steps` 步草稿；CUDA graph 路径返回 `(parent_list, top_scores_index, draft_tokens, draft_probs)`（`:648–657`）。
2. **draft_probs 出池**：CUDA graph 的 `draft_probs` 指向图私有内存池，必须 `clone()`（`:650–657` 的注释明确写了池会被 DSA top-k mask 复用，不 clone 会读到 `-inf`）。
3. **组装验证输入**：`build_eagle_verify_input(..., draft_probs, topk=self.topk, ...)`（`:676–681`）。
4. **验证**：`eagle_sample` 按 greedy / sampling 分流（`eagle_utils.py:860`）。
5. **写回**：接受路径写 KV / 序列；被拒位置由 target 采样补 token。

关键：整条链路只在“**非 greedy 且开启拒绝采样**”时才构造 `draft_probs`（`python/sglang/srt/speculative/eagle_worker_v2.py:727–733`）。greedy 批不构造，因为 `verify_tree_greedy_func` 只比较 argmax，不读分布。

---

## 4. `draft_probs` 的出现条件：一条 assert 定边界（`python/sglang/srt/speculative/eagle_worker_v2.py:178–180`）

`eagle_worker_v2.py:178–180`：

```
self.topk = get_spec().speculative_eagle_topk
if get_spec().speculative_use_rejection_sampling:
    assert self.topk == 1, "Chain speculative sampling supports only topk=1"
```

这条 assert 信息量很大：

- SGLang 的“拒绝采样”实现是 **chain speculative sampling**，只支持 **topk=1**（单链草稿），不支持 topk>1 的树；
- 因此它**不是**对 EAGLE-3 动态树的全面修复；树路径仍走另一套 kernel；
- 这也解释了为什么 `draft_probs` 只在链式路径被需要：树路径的候选来自 top-k 分支，逐分支传 `q` 的成本与接口都不同。

---

## 5. 验证的三条分支

`eagle_sample`（`eagle_utils.py:741`）在 `860` 之后分流：

| 分支 | 条件 | kernel | 是否用 draft_probs |
| :-- | :-- | :-- | :-- |
| **贪心** | `_verify_uses_greedy(...)` 为真 | `verify_tree_greedy_func`（`:384`） | ❌ 不需要（比较 argmax） |
| **稀疏 UNO 采样** | `_can_use_sparse_uno_tree_target_sampling(...)` | `sample_uno_tree_target_tokens` | ❌ 目标侧 top-k 采样 |
| **一般采样 + 拒绝采样开** | `use_rejection_sampling` | `chain_speculative_sampling_triton`（`:947`） | ✅ **必须**，校验后传入 |
| **一般采样 + 拒绝采样关** | 否则 | `tree_speculative_sampling_target_only` | ❌ `draft_probs` 置 `zeros_like`（`:1002–1003`） |

### 5.1 拒绝采样路径的校验（防御性）

`eagle_utils.py:1000–1013`：

- 取 `verify_input.draft_probs`；
- 若为 `None` 或最后一维与 `target_probs` 词表不匹配 → 抛 `ValueError`：
  > "Rejection sampling requires a target-vocab draft proposal distribution; the current speculative algorithm/draft worker does not produce one (draft_probs missing or vocab-mismatched)."

这不是“尽量兼容”，而是**硬失败**：宁可报错，也不静默退化成 one-hot。这一点比 vLLM 的“整批回退 legacy”更严格。

### 5.2 树路径为什么不传 draft_probs

`tree_speculative_sampling_target_only` 从名字看就是“只用 target 概率”的采样验证；代码在非拒绝采样时把 `draft_probs` 置为零张量（`:1002–1003`）。它**不是** EAGLE 论文里 `p/q` 比值那套，而是 SGLang 自己的目标侧采样方案。因此：

- **不要把 SGLang 的 tree 路径当成“已实现 p/q 拒绝采样”**；
- 也不要说它“有损”——它是另一套接受规则，需按该 kernel 的语义单独论证（本分册不展开）。

---

## 6. 历史未核验项 #10308 的处理结论

### 6.1 issue 的事实状态

| 项 | 核验结果 |
| :-- | :-- |
| issue | `sgl-project/sglang#10308`，标题：*[Feature] Speculative sampling supports passing the predicted probability of the draft model and sample token for verification when **topk=1*** |
| 开立 | 2025-11-03，指派 `hnyls2002` |
| 关闭 | **2026-01-03 被 github-actions 以 inactive 自动关闭**（"automatically closed due to inactivity"） |
| linked PR | **未观察到 linked / merged PR**（issue 页面 timeline 只有 assigned / comment / closed / labeled） |

### 6.2 当前主线是否已具备该能力

**是，但限于 topk=1 链式路径**，证据链：

1. `eagle_worker_v2.py:178–180`：开启 `speculative_use_rejection_sampling` 时断言 `topk == 1`；
2. `eagle_worker_v2.py:727–733`：非 greedy 且开启拒绝采样 → 构造 `draft_probs`；
3. `eagle_info.py:35`/`162`：`EagleVerifyInput` / `EagleDraftInput` 都有 `draft_probs` 字段；
4. `eagle_utils.py:947`：选择 `chain_speculative_sampling_triton`；
5. `eagle_utils.py:1000–1013`：`draft_probs` 缺失/词表不匹配 → 硬报错；
6. `eagle_utils.py:1030–1044`：`target_probs`、`draft_probs`、`uniform_samples` 一起传入采样 kernel。

**结论（可引用）**：issue 本身**没有 linked PR**、以 inactive 关闭；但**它请求的能力在 2026-10 的主线代码中以“topk=1 + 拒绝采样开关”的形式存在**。因此：

- 说“#10308 已修复”**不准确**（没有 linked PR，issue 也没 reopen）；
- 说“#10308 完全没被处理”**也不准确**（能力已在代码里）；
- 准确表述：**“issue 未被正式关联/关闭为已修复；其请求的 topk=1 采样验证能力已在主线以 `speculative_use_rejection_sampling` + `draft_probs` 实现，且硬限制 topk=1；tree topk>1 仍走 target-only kernel。”**

### 6.3 剩余缺口

| 缺口 | 说明 |
| :-- | :-- |
| topk>1 树 + 真 draft 概率 | 当前 assert 禁止；树路径仍 target-only |
| 默认开关 | `speculative_use_rejection_sampling` 的默认值未在本分册核验的文件中定位（`get_spec()` 的配置对象来自运行时上下文，未逐一展开） |
| 与结构化输出约束的耦合 | 未核验 `num_draft_tokens` 扣除逻辑（对照 `python/sglang/srt/speculative/eagle_utils.py:1000–1013` 的校验路径） |
| 性能影响 | 未跑 benchmark；拒绝采样的额外开销未知 |

---

## 7. 与 vLLM 的实现对照

| 维度 | SGLang @ 2a08e261 | vLLM @ 2b85d9cb |
| :-- | :-- | :-- |
| 开关命名 | `speculative_use_rejection_sampling` | `rejection_sample_method` + `draft_sample_method` |
| one-hot 草稿 | 未开拒绝采样时，树路径 `draft_probs` 置零 | `draft_sample_method="greedy"`（默认） |
| 真 draft 概率 | topk=1 链式 + 拒绝采样 | `probabilistic` + `standard` |
| 约束 | **assert topk==1** | 不要求 topk=1；异构词表只允许 greedy |
| 缺概率时 | **硬报错**（ValueError） | 整批回退 legacy（warning + None） |
| 树路径 | `tree_speculative_sampling_target_only` | `_rejection_random_sample` / `NO_DRAFT_PROBS` |
| 指标 | 未见独立 metrics 文件；接受长度由调度侧统计 | `metrics.py:107–122` 显式两个分母 |

**可判定差异一句话**：SGLang 把“topk=1 链式 + 真概率”做成**强约束的专用路径**；vLLM 把它做成**可配置的正交开关**。两者都在 2026-10 具备“把 draft 概率传给验证”的能力，但适用形状不同。

---

## 8. SGLang 上的官方吞吐数字（来自 EAGLE-3 论文，非本分册实测）

EAGLE-3 论文 Table 4（SGLang 团队在 1×H100、LLaMA-3.1-8B、MT-Bench 上测）：

| 配置 | 吞吐（tokens/s） | 相对无投机 |
| :-- | --: | --: |
| SGLang 无投机 | 158.34 | 1.00× |
| SGLang + EAGLE-2 | 244.10 | **1.54×** |
| SGLang + EAGLE-3 | 373.25 | **2.36×** |

> 这是**论文里 SGLang 团队提供的数字**，不是本分册跑出来的；引用时保留“1×H100 / batch=1 / MT-Bench / 链长 3、不用树”的条件。

---

## 9. 失效边界（代码层）

1. **topk>1 不支持拒绝采样**：`assert self.topk == 1`，开开关 + topk>1 会直接失败。
2. **draft_probs 缺失即报错**：词表不匹配或算法不产出概率时，`ValueError` 而不是降级。
3. **树路径不是 p/q 拒绝采样**：`tree_speculative_sampling_target_only` + 零 `draft_probs`，语义需单独核对。
4. **CUDA graph 内存池陷阱**：`draft_probs` 必须 clone 出池；否则可能读到被复用的 `-inf`（代码注释已警告）。
5. **默认开关未确认**：本分册没有定位 `speculative_use_rejection_sampling` 的默认值；不要假设“默认开启”。
6. **无 benchmark**：所有性能结论只能引用论文/官方文档，不能由代码推出。
7. **版本漂移**：行号与字段名绑定 commit；SGLang 迭代快，跨版本引用需重新核验。

---

## 10. 交付核验清单

| 检查项 | 结果 |
| :-- | :-- |
| 仓库/commit | `sgl-project/sglang` @ `2a08e261ecd4cdfb04ec354f9005f18b88108b7d`（2026-10-16） |
| 代码是否入库 | ❌ 未入库；只留 `文件:行` 短引用 |
| 引用长度 | 每条 ≤ 3 行语义锚点 |
| 是否跑 benchmark | ❌ 未跑；吞吐数字来自 EAGLE-3 论文 |
| #10308 | issue 无 linked PR、inactive 关闭；能力已在主线 topk=1 路径实现 |
| 已知限制 | topk>1 不支持；默认开关未确认 |

---

## 来源

- 仓库：`https://github.com/sgl-project/sglang` @ `2a08e261`（Apache-2.0）。
- 文件：`python/sglang/srt/speculative/eagle_worker_v2.py`、`eagle_utils.py`、`eagle_info.py`、`runtime_context.py`。
- issue：`https://github.com/sgl-project/sglang/issues/10308`（2025-11-03 开，2026-01-03 inactive 关闭，无 linked PR）。
- 吞吐数字：EAGLE-3 论文 arXiv:2503.01840v3 Table 4（SGLang 团队提供）。
