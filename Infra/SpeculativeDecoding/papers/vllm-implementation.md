# vLLM 实现核验：投机解码的 draft/verify 两条路径（仓库 @ 2b85d9cb）

> **一手来源**：`vllm-project/vllm` @ **`2b85d9cb65c1f56c347cb7f56f1596a6b8b28373`**（2026-10-17，commit `2b85d9cb`，committed 2026-10-17T02:55:28−07:00），只读快照；license = **Apache-2.0**。｜ **主等级**：`[精读原文]`（代码路径）
> **核验范围**：`vllm/config/speculative.py`、`vllm/v1/spec_decode/llm_base_proposer.py`、`vllm/v1/sample/rejection_sampler.py`、`vllm/v1/spec_decode/metrics.py`、`vllm/v1/worker/gpu_model_runner.py` 的投机相关分支（非全仓库）。
> **一句话定位**：vLLM 把投机解码拆成「**draft 采样**（greedy / probabilistic）」×「**验证规则**（standard / synthetic / block）」两个正交开关；`greedy` 默认把草稿概率当 one-hot，`probabilistic` 才真正把 draft 分布传给拒绝采样。
> **亮点与差异四行**
> - **一句话亮点**：在同一个 proposer 里同时支持 EAGLE/MTP/DFlash/standalone draft，并用 `draft_sample_method` 显式区分“草稿是 one-hot 还是真分布”。
> - **新在哪（相对论文）**：论文里的 `q` 是数学对象；vLLM 把它落成**可配置的运行时字段**，并给出“缺 draft_probs 时回退 legacy 行为”的工程路径。
> - **证据强度**：**代码级**。所有结论都有 `文件:行` 锚点；没有跑端到端 benchmark，因此**不报告加速比**（避免伪造测量）。
> - **值不值得引用**：**值得作为“投机解码在生产框架里如何落地”的一手证据**；引用时钉 commit，不要把行为当成跨版本契约。

---

## 0. 七问速答（代码版一页）

| # | 七问 | 一句话回答 |
| --: | :-- | :-- |
| 1 | 解决什么问题 | 把“draft 怎么采样、验证用不用草稿概率、指标怎么报”变成框架里的显式配置，而不是隐式假设。 |
| 2 | 机制与关键参数 | `draft_sample_method ∈ {greedy, probabilistic}`；`rejection_sample_method ∈ {standard, synthetic, block}`；`num_speculative_tokens`；`parallel_drafting`。 |
| 3 | 覆盖范围 | EAGLE/MTP（`llm_base_proposer`）、DFlash 并行草稿、standalone draft；单请求 + batch 路径；`gpu_model_runner` 负责 draft_probs 装配。 |
| 4 | 带条件的“结果” | 默认 `greedy` + `standard`；`probabilistic` 需要 `standard`；`synthetic` 只用于模拟接受率；`block` 走块验证。**这些是行为契约，不是加速比**。 |
| 5 | 消融/开关 | 打开 `probabilistic` → 保留完整 draft logits、参与 `p/q` 比值检验；保持 `greedy` → 草稿概率按 one-hot 处理。 |
| 6 | 何时失效 | 缺 draft_probs 时回退 legacy；异构词表只支持 greedy；`synthetic` 不保分布；`draft_context_window` 在本 commit **未检出**（PR 未合入）。 |
| 7 | 可判定差异 | vs SGLang：vLLM 用“draft_sample_method”显式建模 one-hot vs 真分布；SGLang 用 `speculative_use_rejection_sampling` 开关 + `draft_probs` 校验。 |

---

## 1. 核验方法与边界

- **版本钉死**：所有 `文件:行` 对应 commit `2b85d9cb`；换 commit 后行号可能漂移，引用时必须带 SHA。
- **只读**：源码快照放在 `/tmp/vllm-src`（仓库外），不构建、不修改；本条目只保留短引用与行号。
- **不跑 benchmark**：本条目没有 GPU 实测，因此**不写加速比**；凡是“性能”字样，均指代码路径/契约，不是测量值。
- **不做全仓库审计**：只覆盖投机解码直接相关的 5 个文件；调度器、attention backend 只在必要时引用。

---

## 2. 代码地图（先看哪几处）

| 关注点 | 文件 | 行号（本 commit） | 说明 |
| :-- | :-- | :-- | :-- |
| 配置字段 | `vllm/config/speculative.py` | `533` | `rejection_sample_method` 默认 `standard` |
| 配置字段 | 同上 | `604` | `draft_sample_method` 默认 `greedy`；注释明确“greedy 时草稿概率按 one-hot 处理” |
| 配置校验 | 同上 | `1809–1840` | `synthetic` 需要 rates/length；异构词表只允许 greedy |
| 基类 proposer | `vllm/v1/spec_decode/llm_base_proposer.py` | `73` | `class SpecDecodeBaseProposer` |
| 概率草稿开关 | 同上 | `257–261` | `_enable_probabilistic_draft_probs = (rejection_sample_method == "standard" and draft_sample_method == "probabilistic")` |
| 草稿采样 | 同上 | `449–475` | `_sample_from_logits`：非 probabilistic 或全 greedy → argmax |
| 草稿 token 生成 | 同上 | `477–506` | `_sample_draft_tokens`；probabilistic 时返回 `(ids, probs)` |
| 取回 draft_probs | 同上 | `508–509` | `take_last_draft_probs()` |
| 拒绝采样入口 | `vllm/v1/sample/rejection_sampler.py` | `410` | `rejection_sample(...)`，`draft_probs: Tensor | None` |
| 贪心路径 | 同上 | `445–480` | `target_argmax` + `_rejection_greedy_sample`；全 greedy 直接返回 |
| 采样路径 | 同上 | `487–520` | `target_probs = softmax`，`sample_recovered_tokens` + `_rejection_random_sample` |
| 无 draft_probs 分支 | 同上 | `949` / `1128` | Triton kernel 的 `NO_DRAFT_PROBS=draft_probs is None` |
| 指标 | `vllm/v1/spec_decode/metrics.py` | `107–122` | acceptance rate、mean acceptance length、逐位置接受率 |
| draft_probs 装配 | `vllm/v1/worker/gpu_model_runner.py` | `4714–4741` | `_get_spec_decode_draft_probs`；缺失 → `None` |
| draft_probs 缓存 | 同上 | `4987–4990` | 从 drafter 的 `take_last_draft_probs()` 取 |

---

## 3. draft 侧：greedy 与 probabilistic 是两种语义，不是两种优化（`vllm/config/speculative.py:604`）

### 3.1 `greedy`（默认）

- `draft_sample_method="greedy"`（`speculative.py:604`）时，`_sample_draft_tokens` 直接走 `_greedy_sample`（`llm_base_proposer.py:477–486`），返回 `(ids, None)`。
- 配置注释写得很直白：**“greedy always picks the argmax token, and the draft probabilities are treated as one-hot during rejection sampling”**（`speculative.py:604` 的 docstring）。
- 数学含义：草稿分布 `q` 退化为 one-hot（在该 token 上概率 1，其余 0）。这与 Lookahead 的“贪心草稿”是同一语义（见 [papers/2402.02057-lookahead.md](2402.02057-lookahead.md) §2.3）。
- 代价：T>0 时 one-hot 提议的接受率低于真实分布提议；好处：不需要存整个词表的 `q`，显存与传输成本低。

### 3.2 `probabilistic`

- `_enable_probabilistic_draft_probs` 只在 `rejection_sample_method == "standard"` **且** `draft_sample_method == "probabilistic"` 时为真（`llm_base_proposer.py:257–261`）。
- 打开后：
  - `_sample_from_logits` 用 `compute_probs_and_sample_next_token` 真正按采样参数抽样（`llm_base_proposer.py:449–475`）；
  - `_sample_draft_tokens` 返回 `(draft_token_ids, draft_probs)`（`:487–506`）；
  - `take_last_draft_probs()` 把 `draft_probs` 交给 runner（`:508–509`），runner 再按请求拼成扁平张量（`gpu_model_runner.py:4714–4741`）。
- 配置注释明确代价：**“This comes at the cost of additional GPU memory usage”**（`speculative.py:604` docstring）——要存 `num_spec_tokens × vocab` 的概率。

### 3.3 为什么 `probabilistic` 必须配 `standard`

- `synthetic` 是“按预设接受率衰减”的模拟模式（`speculative.py:533` 的 docstring），它不需要真实 `q`；`block` 是块验证（同处）。
- 因此 `_enable_probabilistic_draft_probs` 把条件写死为 `standard`；其他模式即使开了 probabilistic 也不会走完整 `p/q` 比值检验。**这是一个容易踩的配置坑**：用户以为开了 `probabilistic` 就一定无损，实际上还要 `standard`。

### 3.4 一个“把开关打开”的配置长什么样

按本 commit 的字段名，打开 probabilistic 需要**同时**满足两个条件；示意（字段名以代码为准）：

```json
{
  "method": "eagle",
  "model": "<eagle-draft>",
  "num_speculative_tokens": 3,
  "rejection_sample_method": "standard",
  "draft_sample_method": "probabilistic"
}
```

- 只写 `draft_sample_method="probabilistic"` 而 `rejection_sample_method` 仍是 `synthetic`/`block` 时，`_enable_probabilistic_draft_probs` 为假，**不会**走完整 `p/q` 检验。
- 反过来，只写 `rejection_sample_method="standard"` 而 `draft_sample_method` 保持默认 `greedy`，则草稿概率按 one-hot 处理——这是默认且免费（显存）的路径。

---

## 4. 验证侧：贪心与采样走两条不同的 kernel 路径

`rejection_sample`（`rejection_sampler.py:410`）的入口参数里，`draft_probs` 是 **Optional**：

> 下表对应 `vllm/v1/sample/rejection_sampler.py` 的三条 kernel 路径。

| 条件 | 路径（`vllm/v1/sample/rejection_sampler.py`） | 关键代码 |
| :-- | :-- | :-- |
| `sampling_metadata.all_greedy` | 纯贪心：`target_argmax` 对比草稿 token，接受前缀 | `:445–480`，`_rejection_greedy_sample` |
| 混合 batch（部分 greedy） | 先对 greedy 请求做拒绝，再对随机请求做概率拒绝 | `:455–480` 后继续 `:487` |
| 随机采样 | `target_probs = target_logits.softmax(...)`；`draft_probs` 可为 `None` | `:487–520` |
| `draft_probs is None` | Triton kernel 走 `NO_DRAFT_PROBS=True` 分支 | `:949`、`:1128` |

**关键语义**：`draft_probs is None` 不等于“无损”——它表示 kernel 按 **one-hot 提议**处理（即假定草稿是 argmax，`vllm/v1/sample/rejection_sampler.py:949`）。这正是 `greedy` 默认路径的数学基础，也是“缺 draft_probs 时回退 legacy 行为”的原因（见 §5，`vllm/v1/worker/gpu_model_runner.py:4714–4741`）。

### 4.1 两条路径的接受判据（代码对照）

| 路径 | 接受条件 | 拒绝后 | 代码 |
| :-- | :-- | :-- | :-- |
| greedy | 草稿 token == `target_argmax` | 用 target 的 argmax 作为修正 token | `_rejection_greedy_sample`（`:811`） |
| random + draft_probs | `u ≤ p(x)/q(x)` | 从 `norm(max(0, p−q))` 采恢复 token | `sample_recovered_tokens`（`:678`）、`_rejection_random_sample`（`:934`） |
| random、无 draft_probs | 按 one-hot 提议的等价规则 | 同上，但 `q` 视为 one-hot | `NO_DRAFT_PROBS`（`:949`/`:1128`） |

这张表解释了为什么“greedy 不需要 draft_probs 也能无损”：one-hot 提议下 `q(x)=1`，`p/q` 退化为 `p`，接受规则与 target argmax 一致。

---

## 5. draft_probs 的生命周期与回退

`gpu_model_runner._get_spec_decode_draft_probs`（`gpu_model_runner.py:4714–4741`）：

1. 如果 `self._draft_probs` 为空 → 返回 `None`；
2. 按 `req_id` 找每行的 draft 概率，截到 `num_draft`；
3. 任何一个请求找不到 → **打 warning 并返回 `None`**（整批回退 legacy 行为）；
4. 全部找到 → `torch.cat` 成 `[total_draft_tokens, vocab]` 的连续张量。

这段代码说明两件事：

- **draft_probs 是“按请求缓存、按批拼装”的**，不是随 token 流式传递；
- **失败是整批回退**，不是逐请求降级——这对排查“为什么开了 probabilistic 但接受率没变”很关键（可能是某一行缺失导致整批回退；`vllm/v1/worker/gpu_model_runner.py:4714–4741`）。

---

## 6. 配置面：三个 rejection 模式 + 并行草稿

| 模式 | 语义 | 是否保分布 | 备注 |
| :-- | :-- | :-- | :-- |
| `standard` | 概率拒绝采样（`p/q` 比值 + 残差重采样） | ✅ 严格（在 `q` 正确传递时） | 默认；支持 greedy 与 probabilistic |
| `synthetic` | 按 `synthetic_acceptance_rates` / `synthetic_acceptance_length` 衰减接受 | ❌ 不保分布 | 用于模拟/压测；参数必须单调不增（`speculative.py:533–553`） |
| `block` | 块验证（Sun et al.） | 取决于实现 | 与“逐 token 验证”相对 |

- **`enable_adaptive_verification`**（`speculative.py:555`）：按请求置信度自适应验证预算，注释写明“currently only supported for method='dspark'”——这与 [papers/2408.11049-magicdec.md](2408.11049-magicdec.md) 的“按负载选 γ”同源。
- **`parallel_drafting`**（`llm_base_proposer.py:112–114`）：DFlash 一类并行草稿一次出 `num_speculative_tokens` 行；`_sample_from_logits` 里专门处理“logits 行数 = batch×K、sampling metadata 是 per-request”的广播（`:459–472`）。

---

## 7. 指标实现：分母写死在代码里

`vllm/v1/spec_decode/metrics.py:107–122`：

- `draft_acceptance_rate = num_accepted_tokens / num_draft_tokens × 100`（分母是**提议草稿数**）；
- `mean_acceptance_length = 1 + num_accepted_tokens / num_drafts`（分母是**验证步数**，含 bonus token）；
- `acceptance_rates = sum(pos_matrix, axis=0) / num_drafts`（逐位置接受率）。

这正好对应 [topics/verification-acceptance.md](../topics/verification-acceptance.md) §2 的“两个指标分母不同、必须成对报告”：代码层面它们就是两个不同的除法，不能互相推导。

---

## 8. 与论文的对照（可判定差异）

| 论文概念 | vLLM 对应 | 差异/注意 |
| :-- | :-- | :-- |
| 经典 `q` 分布 | `draft_probs`（probabilistic）或 one-hot（greedy） | 框架把“q 是什么”变成显式配置 |
| EAGLE 草稿头 | `llm_base_proposer` + `EagleProposer` 子类 | 草稿头由 HF checkpoint 提供，框架只负责调度 |
| Medusa 树 | 树验证路径 + `num_speculative_tokens` | vLLM 没有 Medusa 头训练，只做推理 |
| Lookahead one-hot | `greedy` + `NO_DRAFT_PROBS` | 语义一致：argmax 提议按 one-hot 处理 |
| MagicDec 的“按负载选 γ” | `enable_adaptive_verification`（仅 dspark） | 目前是受限能力，不是通用开关 |

---

### 8.1 指标只覆盖“接受”，不覆盖“墙钟”

`metrics.py` 统计的是 token 级接受/提议计数与逐位置接受率；它**不记录**端到端延迟、batch 形状、GPU 型号。因此：

- 用 metrics 可以判断“草稿质量是否变化”，但不能单独判断“系统是否变快”；
- 变快/变慢要结合外部 benchmark（吞吐、延迟、batch）与 [topics/systems-throughput-latency.md](../topics/systems-throughput-latency.md) 的条件表；
- 这也是为什么报告加速比时必须同时给 acceptance rate 与 mean acceptance length（两者分母不同，见 §7）。

---

## 9. 失效边界（代码层）

1. **`draft_context_window` 不在本 commit**：PR #61261 声称给 DFlash/DSpark 加“draft 只看最近 N 个 token”的字段，但在 `2b85d9cb` 的 `speculative.py` 里**检索不到**该字段。结论：**该 PR 在本快照未合入**（或尚未进该分支）；不能把“已有该能力”写成既成事实。
2. **`probabilistic` 必须配 `standard`**：配 `synthetic`/`block` 时不会走完整 `p/q` 检验；这是配置语义，不是 bug。
3. **缺 draft_probs 整批回退**：任一请求缺概率 → 返回 `None` → legacy 行为；线上表现为“开了开关但没效果”。
4. **异构词表只支持 greedy**：`speculative.py:1836–1841` 明确拒绝 `use_heterogeneous_vocab` + probabilistic。
5. **`synthetic` 不保分布**：它按预设接受率模拟，不能用于对外宣称“无损”。
6. **默认 greedy 不是“无损”的充分条件**：T=0 下 one-hot + 拒绝采样可无损；T>0 下 one-hot 提议仍无损（数学上），但**接受率低**——不要把“无损”误读成“高效”。
7. **快照限制**：只读 5 个文件，未覆盖 attention backend、CUDA graph、调度器；跨版本行为可能变化。

---

## 10. 交付核验清单

| 检查项 | 结果 |
| :-- | :-- |
| 仓库/commit | `vllm-project/vllm` @ `2b85d9cb65c1f56c347cb7f56f1596a6b8b28373`（2026-10-17） |
| 代码是否入库 | ❌ 未入库；快照在 `/tmp`，仓库只留 `文件:行` 短引用 |
| 代码引用长度 | 每条 ≤ 3 行，均为语义锚点，不贴整段 |
| 是否跑 benchmark | ❌ 未跑；本分册不报告加速比 |
| 与论文数字的关系 | 只做语义对照，不做数值对齐 |
| 已知未合入项 | `draft_context_window`（PR #61261）在本 commit 未检出 |

---

## 来源

- 仓库：`https://github.com/vllm-project/vllm` @ `2b85d9cb`（Apache-2.0）。
- 文件：`vllm/config/speculative.py`、`vllm/v1/spec_decode/llm_base_proposer.py`、`vllm/v1/sample/rejection_sampler.py`、`vllm/v1/spec_decode/metrics.py`、`vllm/v1/worker/gpu_model_runner.py`。
- 对照论文：[papers/2401.15077-eagle-series.md](2401.15077-eagle-series.md)、[papers/2402.02057-lookahead.md](2402.02057-lookahead.md)、[papers/2408.11049-magicdec.md](2408.11049-magicdec.md)。
