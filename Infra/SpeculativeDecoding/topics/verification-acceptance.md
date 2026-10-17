# 横切专题②：验证—接受准则与无损性

> **定位**：把“投机解码为什么无损”“T>0 下哪里会坏”“top-K 到底改变了什么”讲成一套可判定的准则，而不是一句“lossless”。
> **证据等级**：数学部分为教科书级推导 + 本条目分册正文；方法级结论标 `[精读原文]`；ARC-Decode 只有会议页，标 `[摘要级]`。
> **配套分册**：[EAGLE](../papers/2401.15077-eagle-series.md)、[Lookahead](../papers/2402.02057-lookahead.md)、[Medusa](../papers/2401.10774-medusa.md)、[RheoSampling](../papers/2609.21827-rheosampling.md)、[vLLM](../papers/vllm-implementation.md)、[SGLang](../papers/sglang-implementation.md)。

---

## 1. 先把符号钉死

| 符号 | 含义 | 备注 |
| :-- | :-- | :-- |
| `p(x)` | target 模型在当前位置的分布 | 我们最终要采样的分布 |
| `q(x)` | draft/草稿模型在同一位置的分布 | 可以是模型、one-hot、top-K 截断、或残差分布 |
| `α` | 接受率 | 单 token 的接受概率；不是“整步接受长度” |
| `τ` | 平均接受长度（mean acceptance length） | 每次验证步平均产出 token 数，含 bonus token |
| `K` / `k` | top-K 的 K / 草稿 token 数 | 注意两个 K 在不同论文里含义不同 |
| one-hot | `q` 只在某个 token 上为 1 | 贪心草稿的极端形态 |

> **第一个坑**：很多材料把 `α`（单 token 接受率）与 `τ`（每步接受长度）混写。两者量纲不同，不能互相替代。

---

## 2. 单链无损性：修改的拒绝采样

### 2.1 算法（Leviathan / Chen 2023）

对每个候选位置：

1. 从 `q` 采一个 token `x`；
2. 以概率 `α(x) = min(1, p(x)/q(x))` 接受；
3. 若拒绝，从残差分布 `p'(x) = norm(max(0, p(x) − q(x)))` 重采一个 token；
4. 接受/重采后，继续下一个位置。

### 2.2 为什么输出严格等于 p

对任意 token `x`：

`Pr(output = x) = q(x)·α(x) + [1 − Σ_y q(y)α(y)]·p'(x)`

第一项 `q(x)·min(1, p/q) = min(p(x), q(x))`；第二项的系数是 `1 − Σ_y min(p(y), q(y))`，而 `p'(x) ∝ max(0, p(x) − q(x))`，归一化常数正好是 `Σ_y max(0, p−q) = 1 − Σ_y min(p,q)`。两项相加：

`min(p,q) + max(0, p−q) = p(x)`

**结论**：只要 `q` 的计算与采样一致、残差用 `p` 而不是截断后的 `p`，单链拒绝采样**严格无损**。

### 2.3 两个容易忽略的前提

1. **q 必须是“实际采样用的分布”**：如果采样时用了 top-K/top-p 截断，验证时也必须用同一截断分布；否则 `q` 与采样不符。
2. **残差必须用完整的 p**：即使 `q` 是 top-K 截断的，残差 `max(0, p−q)` 里的 `p` 仍是完整 target 分布——这正是 top-K 草稿仍能无损的原因（见 §3）。

---

## 3. top-K 到底改变了什么：接受率，不是无偏性

### 3.1 接受率的精确表达

单 token 的接受率（在标准拒绝采样下）：

`α* = Σ_x min(p(x), q(x)) = 1 − TV(p, q)`

其中 `TV` 是总变差距离。也就是说：**接受率 = p 与 q 的重叠面积**。RheoSampling 论文明确写了这个等式（§3.1、图 1）。

- 若 `q = p`：`α* = 1`（单链下每个草稿都被接受）。
- 若 `q` 是 top-1（one-hot 在 `x_top1 = argmax q`）：`α* = p(x_top1)`——只是 target 在该点的概率质量，通常远小于重叠面积。
- 若 `q` 是 top-K 截断并重归一化：`α* = Σ_{x∈TopK} min(p(x), q_K(x))`；截断丢掉的尾部质量会降低重叠。

### 3.2 无偏性：top-K 草稿仍然无损

关键点：**“q 是截断的”不等于“输出有偏”**。因为拒绝后的残差用的是完整 `p`，`q` 没覆盖的尾部会通过 `max(0, p−q)` 被补回来。所以：

| 草稿形式 | 输出分布 | 接受率 |
| :-- | :-- | :-- |
| 完整 q | 严格 p | `1 − TV(p,q)` |
| top-K 截断 q | **严格 p** | 更低（尾部质量丢失） |
| top-1（one-hot） | **严格 p** | `p(argmax q)`（很低） |
| 动态树 top-K 选择 + 按 q 排序 | 取决于建树是否与取值耦合 | T>0 下显著下降 |

**结论**：top-K 的问题是**接受率**，不是**无偏性**。把“top-K 草稿有偏”写成结论是错的；它只是“更保守的提议”。

### 3.3 为什么“top-K 即使 q=p 也到不了 100%”

RheoSampling 指出的一个反直觉事实：纯 top-K 选择即使 draft 与 target 完全一致，也**不能达到 100% 接受率**。原因是候选池里没有“随机采样 token”，验证算法缺少重新分配概率质量的操作空间；要突破这一点，必须在候选集中注入至少一个**随机采样**的 token（RheoSampling 的 `m+1` 槽）。

这条结论对理解“为什么需要随机探针”很关键：不是“采样更随机所以更好”，而是**没有随机 token，验证算法就无法做最优传输/残差重分配**。

---

## 4. 贪心 vs 采样：两条判据、两种 q 需求

| 维度 | 贪心（T=0） | 采样（T>0） |
| :-- | :-- | :-- |
| 接受判据 | 草稿 token == target argmax | `u ≤ min(1, p(x)/q(x))` |
| 需要 q 吗 | **不需要**（one-hot 即可） | **需要**（真实采样分布） |
| 拒绝后 | 用 target argmax 修正 | 从 `norm(max(0,p−q))` 重采 |
| 无损性 | 是（argmax 等价） | 是（拒绝采样证明） |
| 框架实现 | `verify_tree_greedy_func` / `_rejection_greedy_sample` | `chain_speculative_sampling_triton` / `_rejection_random_sample` |
| 常见坑 | 把贪心结论外推到 T>0 | 缺 `draft_probs` 时静默退化成 one-hot |

**框架对照**：

- vLLM：`draft_sample_method="greedy"` 时草稿概率按 one-hot 处理；`probabilistic` 才保留完整 `q`（`vllm/config/speculative.py:604`；`llm_base_proposer.py:257–261`）。
- SGLang：开启 `speculative_use_rejection_sampling` 时断言 `topk == 1`，并强制校验 `draft_probs`（`eagle_worker_v2.py:178–180`；`eagle_utils.py:1000–1013`）。

---

## 5. 树验证：路径级接受与 T>0 塌缩

### 5.1 静态树：拓扑与取值无关，天然无损

静态树（EAGLE-1、Medusa 的固定树）在**建树时**就固定了拓扑，不依赖“采样到哪个 token 才决定是否保留”。因此验证时按路径逐节点套用单链拒绝采样即可，T>0 下仍严格无损（前提是每个节点的 `q` 正确）。

### 5.2 动态树：建树与验证共用 q，T>0 下塌缩

EAGLE-2/3 的动态树按 `q` 排序、扩张、剪枝；T>0 时接受判据变成 `p/q` 比值，`q` 的大小不再预测接受。结果：

- 树收敛到少数高 `q` 分支（近似 one-hot）；
- 随机性丢失，接受率下降；
- 若“直接改成采样后仍按 q 排序”，token 的存活依赖自身取值 → 条件分布被扭曲 → 无损性被破坏。

### 5.3 RheoSampling 的修复条件

| 条件 | 作用 |
| :-- | :-- |
| proxy 与采样 token 取值无关 | 存活与取值独立，保住无损性 |
| proxy ≥ `q(x_{m+1})` | Lemma 1 的排序下界；否则存活 token 被强制成某个固定值 |
| 验证用真实 `q̃` | 接受判据的基准正确 |
| 验证用同一 top-128 截断 | 采样/验证分布一致 |

这三条缺一不可；只满足“proxy 独立”而不满足排序下界，仍然会破坏分布（论文给了 `{A,B,C}` 的反例）。

### 5.4 Traversal Verification：换遍历顺序

Traversal Verification（NeurIPS 2025）把验证从“自顶向下逐 token”改成“叶到根、序列级接受”。它不改建树、不改采样语义，因此：

- 仍然严格无损（论文证明输出分布等于 target）；
- 与 RheoSampling 正交，可叠加；
- 收益是“同样树结构下接受长度 +2.2%~5.7%”（论文自报）。

---

## 6. “无损”的三个等级（不要混用）

| 等级 | 含义 | 代表 | 能否宣称“严格无损” |
| :-- | :-- | :-- | :-- |
| **严格分布等价** | 输出分布严格等于 p | 经典单链、静态树、RheoSampling（Theorem 1）、Traversal Verification、HeteroSpec | ✅ |
| **序列级等价** | 以整条序列概率判接受，而非逐 token | Traversal Verification 的视角 | ✅（有其定义域） |
| **有界风险** | 接受放宽到“分布偏移受控” | ARC-Decode（JS 散度上界）、Medusa typical acceptance、CDSL（任务奖励） | ❌ 只能说“质量近乎不变” |

**常见错误**：把 ARC-Decode 的“相对 EAGLE-3 最高 1.6×”与 RheoSampling 的“相对自回归 2.93×”放在同一句比较——基准、量纲、保证等级都不同。

---

## 7. 指标口径：两个分母、一个 bonus

vLLM `metrics.py:107–122` 的定义：

| 指标 | 公式 | 分母 |
| :-- | :-- | :-- |
| `draft_acceptance_rate` | `num_accepted / num_draft_tokens` | **提议草稿数** |
| `mean_acceptance_length` | `1 + num_accepted / num_drafts` | **验证步数**（含 bonus token） |
| `per_position_acceptance` | `sum(pos_matrix, axis=0) / num_drafts` | 验证步数 |

**为什么必须成对报告**：加深草稿树通常**降低** acceptance rate（多提议了低命中 token），却**提高** mean accepted length（一旦命中吃更多）。只看一个会得出相反结论。

**其他会改变分母的因素**：

- **结构化输出约束**：`num_draft_tokens` 会扣除被约束作废的草稿，分母变小；
- **n>1 请求**：逐请求 metrics 只在 n=1 时出现（vLLM 文档口径）；
- **流式响应**：metrics 挂在最后一个 usage chunk 上。

---

## 8. 判定一张“无损”声明是否可信的清单

| # | 要问的问题 | 不合格的表现 |
| --: | :-- | :-- |
| 1 | 有没有给出输出分布等于 p 的证明/定理？ | 只说“experimentally lossless” |
| 2 | T>0 是否单独验证？ | 只报 T=0，或把 T=0 结论外推 |
| 3 | 草稿 q 与验证 q 是否同一分布？ | 采样用 top-K、验证用完整分布 |
| 4 | 截断（top-K/top-128）是否在验证端复现？ | 只截断采样端 |
| 5 | 树的建树是否与 token 取值耦合？ | 动态树 + 按 q 排序 + 声称无损 |
| 6 | 指标是否成对报告？ | 只报 acceptance rate 或只报 τ |
| 7 | 是否声明 batch/T/树参数？ | 只给一个“最高 X×” |

---

## 9. 失效边界（准则级）

1. **数值精度**：`p/q` 在极低概率 token 上会有数值问题；框架通常用 float32/float64 的 kernel（vLLM `USE_FP64_GUMBEL` 分支）。
2. **top-K 截断不一致**：采样端截断、验证端不截断 → 无损性破。
3. **温度极低**：T→0 时任何概率采样都退化为 top token，RheoSampling 的随机探针失去作用；方法价值集中在“温度不是极低”的区间。
4. **动态树 + T>0**：不做解耦就会塌缩；做了解耦（RheoSampling）也要满足 proxy 的排序下界。
5. **结构化输出**：约束会改变 `num_draft_tokens` 与候选集，跨实验不可直接比。
6. **混合 batch**：greedy 与 sampling 请求混在一个 batch 时，验证路径要 per-request 分支；框架实现错误会导致部分请求走错判据。
7. **“有界风险”被写成“无损”**：这是最常见的传播错误（Medusa typical acceptance、ARC-Decode）。

---

## 10. 一页纸总结

- 单链无损 = `min(p,q)` + 残差重采；证明只需一行代数。
- top-K 改变的是**接受率**（`1 − TV`），不是无偏性；残差用完整 p 就仍无损。
- 贪心不需要 q；采样必须用真实 q；两者不能互相外推。
- 动态树在 T>0 下的问题不是“采样不够随机”，而是**建树/验证共用 q**；修复要 proxy 与取值独立 + 排序下界 + 真实 q 验证。
- “无损”分严格/序列级/有界风险三档；跨档比较不成立。
- 指标必须成对：acceptance rate（提议 token 分母）+ mean acceptance length（验证步分母）。

---

## 来源

- 单链拒绝采样：Leviathan et al. 2023 / Chen et al. 2023（背景，本条目未单设分册）。
- 接受率 `Σ min(p,q)`、top-K 的固有上限、proxy 条件：RheoSampling arXiv:2609.21827v1 §3–§4、附录 B–D（`[精读原文]`）。
- 贪心/采样分支与指标：vLLM @ `2b85d9cb`（`rejection_sampler.py:410–520`、`metrics.py:107–122`）；SGLang @ `2a08e261`（`eagle_utils.py:860–1044`）。
- 有界风险：ARC-Decode ICML 2026 会议页（`[摘要级]`）；Medusa typical acceptance（`[精读原文]`，见 [papers/2401.10774-medusa.md](../papers/2401.10774-medusa.md)）。
