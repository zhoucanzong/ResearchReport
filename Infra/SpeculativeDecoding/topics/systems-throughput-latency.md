# 横切专题③：系统实现与吞吐—延迟权衡

> **定位**：把“为什么同一个算法在 batch=1 快 3×、在 batch=64 只快 1.38×、在 batch=256 可能变慢”拆成可判定的成本模型与负载相图。
> **证据等级**：系统数字均来自本条目分册的 `[精读原文]` 或论文官方表格；未设分册的工程博客数字标 `[二手]`。
> **配套分册**：[EAGLE](../papers/2401.15077-eagle-series.md)、[Medusa](../papers/2401.10774-medusa.md)、[SpecInfer](../papers/2305.09781-specinfer.md)、[MagicDec](../papers/2408.11049-magicdec.md)、[Lookahead](../papers/2402.02057-lookahead.md)、[vLLM](../papers/vllm-implementation.md)、[SGLang](../papers/sglang-implementation.md)。

---

## 1. 成本模型：加速比不是一个数

投机解码一步的期望产出（Leviathan 公式）：

`Ω(γ, α) = (1 − α^(γ+1)) / (1 − α)`

其中 `γ` 是投机 token 数、`α` 是单 token 接受率。端到端加速比近似：

`Speedup ≈ Ω(γ, α) / (1 + T_draft/T_target + T_verify(γ)/T_target)`

三个比值决定一切：

| 比值 | 由什么决定 | 何时有利 |
| :-- | :-- | :-- |
| `Ω(γ, α)` | 草稿质量（α）与草稿长度（γ） | 草稿与 target 对齐、任务模板化 |
| `T_draft/T_target` | draft 模型大小、KV 预算、是否并行 | draft 比 target 小很多 / 只读稀疏 KV |
| `T_verify(γ)/T_target` | batch、序列长度、硬件 FLOPS/带宽比 | 验证与解码共享 KV 加载（长序列） |

**推论**：同一算法在不同 `(batch, 序列长度, 硬件)` 下可以有**相反**的结论；任何“加速比 X×”都必须带这三个坐标。

---

## 2. 三种负载区间

### 2.1 memory-bound：batch=1 / 小 batch

- GPU 算力大量闲置，主要成本是把权重从 HBM 搬到 cache；多验证几个 token 的边际算力成本接近 0。
- 投机解码的“黄金区间”：EAGLE-3 在 SGLang batch=2 时吞吐 **1.81×**；Lookahead 在 A100 上 >50%、RTX 3090 只有 ~30%（后者算力上限低）。
- 失效：草稿太慢（`T_draft/T_target` 高）时，收益被 draft 吃掉。

### 2.2 compute-bound：大 batch / 短序列

- 线性层被 batch 喂饱，验证 token 与真实 token 争同一份算力；每个被拒 token 都是浪费。
- SpecInfer：batch 增大 → 相对收益下降；树宽在 **BS≥4** 时 2–3 最优（更宽反而慢）。
- Medusa：roofline 模拟显示 **batch>32** 后加速下降、甚至为负。
- vLLM 文档口径：batch=256 时“每个被拒 token 都是浪费的算力，够多时吞吐下降”。

### 2.3 KV-bandwidth-bound：长序列 + 大 batch

- KV cache 随 batch×序列线性增长，加载 KV 成为主瓶颈；验证与解码共享同一份 KV 加载，`T_verify/T_target` 趋近 1。
- MagicDec：序列长 **≥4000** 时，加速随 batch **上升**；**<4000** 时随 batch **下降**。临界长度 `S_inflection` 随模型（GQA 更高）与硬件（H100 更低）移动。
- 这是“大 batch 不适合投机”结论的反例区间；但它的前提是**长上下文**。

---

## 3. batch 曲线：同一算法在 2→64 上不是直线

EAGLE-3 论文 Table 3（SGLang、1×H100、LLaMA-3.1-8B、MT-Bench、链长 3、不用树）：

| batch | 2 | 4 | 8 | 16 | 24 | 32 | 48 | 56 | 64 |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| EAGLE | 1.40× | 1.38× | 1.23× | 1.02× | **0.93×** | 0.94× | 0.88× | 0.99× | 0.99× |
| EAGLE-3 | 1.81× | 1.82× | 1.62× | 1.48× | 1.39× | 1.32× | 1.38× | 1.34× | 1.38× |

三条读法：

1. **EAGLE 在 batch=24 跌破 1.0×**：不是偶发，而是“验证成本 > 省下的解码步”的结构性结果。
2. **EAGLE-3 把曲线整体抬高，但形状仍递减**：2→4 最高，16 之后稳定在 1.3–1.4×。
3. **batch=1 的吞吐**：无投机 158.34 → EAGLE-2 244.10 → EAGLE-3 373.25 tokens/s（约 **2.36×**）；这是**吞吐**，不是单请求延迟。

---

## 4. 硬件：换卡会改变结论

| 硬件/条件 | 观察 | 来源 |
| :-- | :-- | :-- |
| A100 vs RTX 3090（Lookahead） | A100 >50%、3090 ~30% | Lookahead §5 |
| H100 vs A100 vs L40（MagicDec） | 同设置 H100 加速最高；L40 最低 | MagicDec §5 |
| 8×A100 8-way TP（MagicDec） | 长序列大 batch 下 2.51× | MagicDec §5 |
| 8 卡强扩展（Lookahead LP） | ClassEval 4×；TP/PP 基线反而 0.75–0.82× | Lookahead §5 |
| TPU v5p + DFlash | 平均 3.13×、峰值近 6×（官方工程博客） | `[二手]`，本条目未设分册 |

**规则**：跨硬件不可直接比。同一算法在 GPU 与 TPU 上的收益来自不同工程路径（paged attention vs 双缓存），不是“算法更强”。

---

## 5. 系统杠杆：从静态配置到在线自适应

| 杠杆 | 做法 | 代表 | 解决什么 |
| :-- | :-- | :-- | :-- |
| **静态 `num_speculative_tokens`** | 按部署手动调 | 早期 vLLM/SGLang | 简单，但无法覆盖整个负载区间 |
| **按 batch 调树宽/深度** | 小 batch 宽树、大 batch 窄树 | SpecInfer（BS≥4 用 2–3） | 验证成本与覆盖率的平衡 |
| **按负载调验证预算** | 逐 (request, position) 置信度打分，跨请求竞争 | vLLM adaptive verification | 一套配置覆盖整个负载区间 |
| **按上下文裁剪 draft** | `draft_context_window` 限制 draft 只看最近 N 个 token | vLLM PR #61261（本 commit 未检出） | 解决“超出训练长度后接受率崩塌” |
| **变长验证 + ragged verify** | 置信度驱动裁剪，重放更小的 CUDA graph | SGLang DSpark | 把调度变成 wall-clock |
| **成本感知建树** | 把 GPU 型号、batch 纳入效用最大化 | CAST（ICLR 2026，`[二手]`） | EAGLE-2 在 batch=8 的 CNN/DM 上 0.84× 的反例 |

---

## 6. 延迟 vs 吞吐：不要混着报

| 指标 | 定义 | 投机解码的影响 |
| :-- | :-- | :-- |
| **单请求延迟** | 一个请求从开始到结束的 wall-clock | batch=1 时通常下降；高 batch 时可能上升 |
| **吞吐** | 单位时间产出的 token 数 | batch=1 时可能下降（验证开销）；高 batch 时可能上升（KV 带宽区间） |
| **每 token 延迟** | 总时间 / 输出 token 数 | SpecInfer offloading 用它做指标（2.6–3.5×） |
| **接受长度 τ** | 每验证步平均 token 数 | 只反映草稿质量，不反映墙钟 |
| **acceptance rate** | 被接受草稿 / 提议草稿 | 与 τ 分母不同，会反向移动 |

**报告纪律**：至少给 `(吞吐|延迟, batch, T, 序列长度, 硬件, 树参数)` 六元组；只给“最高 X×”无法判断是否适用于你的负载。

---

## 7. 负载相图（把结论落到可操作的格子）

| 区间 | 典型 batch / 序列 | 是否开投机 | 建议配置 |
| :-- | :-- | :-- | :-- |
| 低延迟单请求 | batch=1、短-中序列 | **开** | EAGLE-3 / Medusa-2；树宽 60、深度 6–8；T=0 优先 |
| 高吞吐短序列 | batch≥32、序列<4000 | **谨慎** | 窄树（2–3）、短 γ；或不开；用 adaptive verification |
| 高吞吐长序列 | batch 32–256、序列≥4000 | **开** | 稀疏 KV 自投机（MagicDec 类）；draft KV 预算 512–2049 |
| 端侧/单卡 | 小显存、batch=1 | 视内存而定 | 免训练（Lookahead/PLD）或层跳过；先算内存带宽预算 |
| RL 训练 rollout | 长尾、target 演化 | 开（有条件） | 在线 drafter（TLT 类）；空闲 GPU 训练 |
| 结构化输出 | JSON/SQL/语法约束 | 开但需重标定 | 语法感知草稿；`num_draft_tokens` 扣除后重算 acceptance rate |

---

## 8. 失效边界（系统级）

1. **静态配置无法覆盖负载区间**：交叉点随负载与接受率移动；固定 `num_speculative_tokens` 必然在某些 batch 上亏。
2. **高 batch + 短序列**：验证成本主导，可能负收益（SpecInfer、Medusa、vLLM 文档口径一致）。
3. **长序列的显存墙**：KV 随 batch×序列增长；batch 上不去，投机的并行度也无从谈起。
4. **draft 上下文失配**：drafter 超出训练长度后接受率崩塌；需要 `draft_context_window` 一类显式参数（本 commit 未检出，说明尚未普遍可用）。
5. **硬件映射**：GPU 与 TPU 的收益不可互推；同一算法在不同卡上可能是不同工程路径。
6. **量纲混用**：µJ/token（能效）与 tokens/s（吞吐）不是同一量纲；SMoLPU 一类专用硅的数字不能与算法论文排榜。
7. **指标只报一个**：acceptance rate 与 τ 反向移动；只报一个会得出相反结论。
8. **T 未声明**：T=0 的 batch 曲线不能外推到 T>0；动态树在 T>0 下会额外损失接受率。

---

## 9. 上线前的测量清单

| # | 要测什么 | 怎么测 |
| --: | :-- | :-- |
| 1 | 负载分布 | batch、输入/输出长度、并发；至少覆盖 P50/P99 |
| 2 | 三个区间 | batch=1、目标 batch、超目标 batch 各一组 |
| 3 | 两个指标 | acceptance rate + mean acceptance length 成对 |
| 4 | 墙钟 | 端到端延迟与吞吐分开报；不要用 τ 代替 |
| 5 | 温度 | T=0 与线上 T 各一组；动态树在 T>0 要重标定 |
| 6 | 约束 | 有无结构化输出各一组；分母会变 |
| 7 | 硬件 | 至少目标卡型；跨卡不互推 |
| 8 | 回退 | draft_probs 缺失、树参数越界、上下文超长时的行为 |

---

## 10. 一页纸总结

- 加速比 = `Ω(γ,α) / (1 + T_D/T_T + T_V/T_T)`；三个比值随负载移动。
- 三个区间：memory-bound（batch=1，最赚）、compute-bound（大 batch 短序列，可能亏）、KV-bound（长序列大 batch，可能反转）。
- EAGLE 在 SGLang batch=24 跌破 1.0×、EAGLE-3 在 batch=64 仍 1.38×——**拐点随算法版本移动**。
- 硬件换卡会改变结论；GPU 与 TPU 不可互推。
- 静态配置必然有盲区；方向是“按请求/位置/上下文自适应”，但 `draft_context_window` 在本轮 vLLM 快照尚未合入。
- 指标必须成对、条件必须六元组；否则“最高 X×”没有工程意义。

---

## 来源

- 成本模型与 batch 曲线：EAGLE-3 arXiv:2503.01840v3 Table 3/4（SGLang 团队）；MagicDec arXiv:2408.11049v5 §3–§5；SpecInfer arXiv:2305.09781v4 §6.6；Lookahead arXiv:2402.02057v1 §5。
- 框架行为：vLLM @ `2b85d9cb`（`speculative.py:533/604`、`llm_base_proposer.py:257–261`）；SGLang @ `2a08e261`（`eagle_worker_v2.py:178–180`、`eagle_utils.py:947–1044`）。
- 二手来源：CAST（ICLR 2026 解读页）、TPU v5p + DFlash（Google 工程博客）、SMoLPU（KAIST Pure，`[⚠️受限核验]`）。
