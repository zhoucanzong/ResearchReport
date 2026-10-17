---
type: topic-research
domain: Infra
subject: SpeculativeDecoding
date: 2026-10-17
evidence: 精读原文
status: completed
---

# 投机解码（Speculative Decoding）技术专题 · 深度调研

> **声明**：本报告由 AI Agent 自动调研生成，未经官方确认；引用具体参数、日期或 benchmark 前请回溯原始来源。
> **调研日期**：2026-10-17（本轮：**按新标准升级**——新增 `papers/` 8 篇逐篇精读、`topics/` 3 篇横切专题、`sources/` 馆藏清单；`report.md` 重写为入口/结论/判据/总表）。
> **定位**：投机解码 = **用低成本草稿换 target 的并行验证**，在**输出分布可证等价（或明示有界风险）**的前提下降低解码 wall-clock。本条目管的是“**算法 + 验证 + 系统条件**”这一整条链，不把“草稿模型训练”单独抽出去。

**证据等级约定（单一主等级）**：

| 等级 | 含义 | 本轮用法 |
| :-- | :-- | :-- |
| `[精读原文]` | 已抓正文并定位到数值/结论段落；代码类须有 `仓库@commit:文件:行` | 8 篇 `papers/` 全部满足（代码类两篇为代码级） |
| `[摘要级]` | 仅核验官方摘要/会议页/项目页，未通读正文 | 只用于“登记存在”，不进结论数字 |
| `[二手]` | 第三方解读、工程博客、周报 | 只作线索，不入对照表 |
| `[⚠️受限核验]` | 一手对象无法直接抓取，只能经镜像/元数据交叉确证 | 逐条写明“卡在哪” |

**规则**：每条只给**一个主等级**；混合来源取**最弱**等级并在括号里注明来源类型。`[摘要级]` **不许升格**为 `[精读原文]`。

---

## 深度阅读导航

本条目采用三层结构：本页 = 入口 + 结论 + 谱系 + 总表；`papers/` = 逐篇精读；`topics/` = 横切专题。

### 逐篇精读（`papers/`，8 篇）

| # | 分册 | 系统 | 在谱系中的位置 | 行数 |
| --: | :-- | :-- | :-- | --: |
| 1 | [2401.15077-eagle-series.md](papers/2401.15077-eagle-series.md) | EAGLE / EAGLE-2 / EAGLE-3 | 自投机·特征级自回归（工业默认） | 244 |
| 2 | [2401.10774-medusa.md](papers/2401.10774-medusa.md) | Medusa | 自投机·并行头（轻量插件） | 204 |
| 3 | [2402.02057-lookahead.md](papers/2402.02057-lookahead.md) | Lookahead Decoding | 免训练·Jacobi 轨迹 | 202 |
| 4 | [2305.09781-specinfer.md](papers/2305.09781-specinfer.md) | SpecInfer | 独立 draft·树验证系统 | 201 |
| 5 | [2408.11049-magicdec.md](papers/2408.11049-magicdec.md) | MagicDec | 系统条件·长上下文大 batch | 200 |
| 6 | [2609.21827-rheosampling.md](papers/2609.21827-rheosampling.md) | RheoSampling | T>0 动态树的无损修复 | 216 |
| 7 | [vllm-implementation.md](papers/vllm-implementation.md) | vLLM @ 2b85d9cb | 生产框架·draft/verify 两路径 | 218 |
| 8 | [sglang-implementation.md](papers/sglang-implementation.md) | SGLang @ 2a08e261 | 生产框架·topk=1 拒绝采样 | 219 |

### 横切专题（`topics/`，3 篇）

| # | 专题 | 回答什么 | 行数 |
| --: | :-- | :-- | --: |
| 1 | [algorithm-families.md](topics/algorithm-families.md) | 四大家族、五根轴、选型判据 | 164 |
| 2 | [verification-acceptance.md](topics/verification-acceptance.md) | 单链/树/有界风险的无损性准则、top-K 到底改变什么、指标口径 | 216 |
| 3 | [systems-throughput-latency.md](topics/systems-throughput-latency.md) | batch×序列×硬件的相图、吞吐-延迟权衡、上线清单 | 168 |

### 历史素材层（保留的 11 篇横切子文档）

本轮按“**改造，不是从零写**”的要求，保留了 2026-10 之前的 11 篇横切子文档作为素材层，**未重写、未删除**：

`speculative-classical-and-self.md`、`speculative-eagle-series.md`、`speculative-stochastic-verification.md`、`speculative-block-diffusion.md`、`speculative-cascade-heterogeneous.md`、`speculative-draft-training-2026.md`、`speculative-training-optimization.md`、`speculative-edge-cloud-hardware.md`、`speculative-domain-language.md`、`speculative-multimodal.md`、`speculative-systems-and-frameworks.md`。

> **使用规则**：素材层用于查“2026 上半年的横向线索”；**与 `papers/` 冲突时以 `papers/` 为准**（例：素材层里 EAGLE 的 arXiv 编号有一处误写为 `2403.00835`，该编号实际是 CLLMs；正确编号是 **2401.15077**，见 [papers/2401.15077-eagle-series.md](papers/2401.15077-eagle-series.md)）。

---

## 0. 一页结论

1. **投机解码的收益不是“算法属性”，而是“算法 × 负载 × 硬件”的联合属性**。EAGLE 在 SGLang batch=24 就跌破 1.0×（0.93×），EAGLE-3 在 batch=64 仍有 1.38×；同一族、不同版本，拐点不同。`[精读原文]`
2. **“无损”至少要分三档**：严格分布等价（经典单链 / 静态树 / RheoSampling / Traversal Verification）、序列级等价、有界风险（ARC-Decode / Medusa typical acceptance）。混档比较不成立。`[精读原文]`
3. **T>0 是动态树的真实边界**：EAGLE-2/3 的“动态树更优”只在 greedy 下成立；T>0 时按 `q` 建树会塌缩为 one-hot，直接“改成采样”还会破坏无损性。RheoSampling 用 proxy/真实概率双身份修复，但**默认 EAGLE 配置并未启用**。`[精读原文]`
4. **top-K 改变的是接受率，不是无偏性**：单链拒绝采样的 α* = Σ min(p,q) = 1 − TV；top-K 截断只要验证端用同一分布、残差用完整 p，输出仍严格等于 p。把“top-K 有偏”当结论是错的。`[精读原文]`
5. **草稿来源的四族不是代际，而是并存选项**：独立 draft（SpecInfer）、自投机（EAGLE/Medusa）、免训练（Lookahead）、块/扩散（DFlash 一类）。选族先看“有没有 draft / 能不能训 / 输出是否模板化”。`[精读原文]`
6. **高 batch 的结论要加第三维：序列长度**。短序列 + 大 batch 亏（SpecInfer/Medusa/vLLM 口径一致）；长序列 + 大 batch 可能赚（MagicDec：S≥4000 时加速随 batch 上升，最高 2.51×）。`[精读原文]`
7. **指标必须成对**：`draft_acceptance_rate`（分母=提议草稿数）与 `mean_acceptance_length`（分母=验证步数，含 bonus）会反向移动；只报一个会得出相反结论。`[精读原文（vLLM 代码）]`
8. **工程落地已经分叉成两种语义**：vLLM 用 `draft_sample_method ∈ {greedy, probabilistic}`；SGLang 用 `speculative_use_rejection_sampling` + `assert topk == 1`。两者都能把真实 `draft_probs` 传给验证，但适用形状不同。`[精读原文（代码）]`
9. **历史 issue #10308 的准确结论**：issue 以 inactive 关闭、无 linked PR；但它请求的“topk=1 采样验证”能力已在 SGLang 主线以 `draft_probs` + 拒绝采样开关实现，且**硬限制 topk=1**；tree topk>1 仍走 target-only kernel。`[精读原文（代码）]`
10. **证据边界**：本条目 8 篇分册中 6 篇是论文正文精读、2 篇是代码级核验；**未做独立复现**，所有加速比均为论文/官方自报值。

---

## 1. 定义与判据

### 1.1 操作性定义

**投机解码**：给定 target 自回归模型 `p` 与一个更便宜的提议机制 `q`，先并行产生若干候选 token（链/树/块/检索结果），再由 target **一次前向**并行验证，按某个接受规则决定输出；当接受规则满足“输出边缘分布 = p”时称**无损**。

三个必要元素：

| 元素 | 作用 | 缺了会怎样 |
| :-- | :-- | :-- |
| **提议机制 q** | 产生候选，决定 `T_draft/T_target` | 没有 q 就退化为普通解码 |
| **并行验证** | 一次前向验证多个候选 | 退化为逐 token 解码，无加速 |
| **接受规则** | 保证分布/质量，决定接受率 | 无规则 = 直接信草稿，有偏 |

### 1.2 纳入 / 排除

| 类别 | 是否纳入 | 理由 |
| :-- | :-- | :-- |
| 经典 draft-then-verify（Leviathan/Chen） | ✅ | 范式源头 |
| 自投机（Medusa / EAGLE / MTP / 层跳过） | ✅ | 当前工业默认 |
| 免训练（Lookahead / PLD / REST / 字典） | ✅ | 独立一族，端侧/低资源重要 |
| 树验证系统（SpecInfer / Sequoia） | ✅ | 验证侧的基础设施 |
| 块/扩散草稿（DFlash / DSpark / BASTION） | ✅（谱系） | 2026 新方向；本轮未设分册，数字不入表 |
| 纯量化 / 纯剪枝 / 纯 KV eviction | ❌ | 不产生“候选-验证”结构；归 `Infra/QuantizationEdge` |
| 纯 batch 调度 / continuous batching | ❌ | 系统优化但不含投机；归 `Infra/TrainingInfra` 或框架条目 |
| 扩散语言模型（非投机范式） | ❌ | 竞争范式，不是本条目主体；只在谱系里对照 |

### 1.3 无损性三档（引用时必须声明）

| 档 | 定义 | 代表 | 可否写“严格无损” |
| :-- | :-- | :-- | :-- |
| **严格分布等价** | 对任意序列，输出概率 = p(Seq) | 经典单链；静态树；RheoSampling（Theorem 1）；Traversal Verification；HeteroSpec（ACL 2026，`[摘要级]`） | ✅ |
| **序列级等价** | 以整条序列概率判接受（而非逐 token） | Traversal Verification 的视角 | ✅（在其定义域） |
| **有界风险** | 接受放宽到“分布偏移受控” | ARC-Decode（JS 上界，ICML 2026 会议页 `[摘要级]`）；Medusa typical acceptance（[papers/2401.10774-medusa.md](papers/2401.10774-medusa.md) §2.3）；CDSL（NAACL 2025，素材层） | ❌ 只能写“质量近乎不变” |

> **反例**：把 ARC-Decode 的“相对 EAGLE-3 最高 1.6×”（ICML 2026 会议页 `[摘要级]`）与 RheoSampling 的“相对自回归 2.93×”（[papers/2609.21827-rheosampling.md](papers/2609.21827-rheosampling.md) §4）并列，是**量纲 + 基准 + 保证等级**三重错配。

### 1.4 指标口径（工程硬要求）

| 指标 | 定义 | 分母 |
| :-- | :-- | :-- |
| `draft_acceptance_rate` | 被接受草稿 / 提议草稿 | **提议 token 数** |
| `mean_acceptance_length` | 1 + 被接受草稿 / 验证步数 | **验证步数**（含 bonus token） |
| `per_position_acceptance` | 逐位置接受率 | 验证步数 |
| `num_draft_tokens` | 总提议数 | **已扣除结构化约束作废的草稿** |

**必须成对报告**，并同时声明：`(batch, T, 序列长度, 硬件, 树参数, 是否结构化约束)`。

---

## 2. 谱系

### 2.1 四大家族

```mermaid
flowchart LR
    A[投机解码] --> B[I 独立 draft]
    A --> C[II 自投机]
    A --> D[III 免训练]
    A --> E[IV 块/扩散]
    B --> B1[SpecInfer 多 SSM]
    B --> B2[standalone draft]
    C --> C1[并行头 Medusa/Hydra]
    C --> C2[特征级 EAGLE-1/2/3]
    C --> C3[层跳过 SWIFT/CLaSp]
    D --> D1[Lookahead]
    D --> D2[PLD/REST/DictSpec]
    E --> E1[DFlash]
    E --> E2[DSpark]
    E --> E3[BASTION]
```

| 族 | 草稿来源 | 额外权重 | 训练 | 典型条件数字 |
| :-- | :-- | :-- | :-- | :-- |
| I 独立 draft | 另一个小模型 | 一个完整模型 | 预训练 | 1.5–2.8×（SpecInfer 分布式） |
| II 自投机 | target 的头/特征/层 | ~7% 或 <1B | 训头/联合 | 2.3–6.5×（EAGLE/Medusa，带条件） |
| III 免训练 | 轨迹/检索/字典 | **无** | **免训练** | 1.5–4×（Lookahead，算力富余） |
| IV 块/扩散 | 块扩散网络 | 一个 draft | 需训练 | 本轮不入表（证据不够） |

详细谱系与选型判据见 [topics/algorithm-families.md](topics/algorithm-families.md)。

### 2.2 时间线（2023 → 2026H2）

| 阶段 | 主线 | 代表 | 本条目证据 |
| :-- | :-- | :-- | :-- |
| 2023 | 经典 draft-then-verify | Leviathan / Chen；SpecInfer | [SpecInfer 分册](papers/2305.09781-specinfer.md) |
| 2024 H1 | 并行头/树验证 | Medusa；Lookahead | [Medusa](papers/2401.10774-medusa.md)、[Lookahead](papers/2402.02057-lookahead.md) |
| 2024 H2 | 特征级自投机 + 动态树 | EAGLE-1 / EAGLE-2 | [EAGLE 分册](papers/2401.15077-eagle-series.md) |
| 2025 | 训练目标 + 数据 scaling | EAGLE-3 | 同上 |
| 2026 H1 | 块扩散/预算感知 | DFlash / DSpark / BASTION | 谱系定位（无分册） |
| 2026 H2 | T>0 正确性 + 系统条件 | RheoSampling；MagicDec | [RheoSampling](papers/2609.21827-rheosampling.md)、[MagicDec](papers/2408.11049-magicdec.md) |
| 2026 | 生产框架落地 | vLLM / SGLang | [vLLM](papers/vllm-implementation.md)、[SGLang](papers/sglang-implementation.md) |

### 2.3 五根可判定的轴

| 轴 | 取值 | 判定方式 |
| :-- | :-- | :-- |
| A 草稿来源 | 独立 / target 自身 / 检索 / 块 | 看是否需要额外权重 |
| B 训练 | 免训练 / 训头 / 训独立模型 | 看训练管线 |
| C 拓扑 | 链 / 静态树 / 动态树 / 块 | 看验证 mask |
| D 接受率上限 | 由 p 与 q 的对齐度决定 | 同条件比 τ 或 acceptance rate |
| E 负载行为 | batch↑ 升/降/反转 | 看 batch×序列扫描 |

---

## 3. 机制（把四族串起来）

### 3.1 单链：draft-then-verify

- 从 `q` 逐 token 采样；以 `min(1, p/q)` 接受；拒绝后从 `norm(max(0, p−q))` 重采。
- 证明见 [topics/verification-acceptance.md](topics/verification-acceptance.md) §2；结论：输出严格等于 `p`。
- 工程前提：采样与验证必须用**同一个 q**；截断（top-K/top-128）必须两端一致。

### 3.2 自投机：并行头 vs 特征自回归

| 维度 | Medusa（并行头） | EAGLE（特征自回归） |
| :-- | :-- | :-- |
| 草稿来源 | target 最后隐藏态 + K 个头 | target 第二层顶层特征 + 单层 decoder |
| 前缀依赖 | ❌ 头之间独立 | ✅ 有 |
| 接受率（同条件参考） | ~0.6 | ~0.8 |
| 训练 | 训头（backbone 可冻结） | 训草稿头（70B 约 0.99B 参数） |
| 树 | 笛卡尔积/搜索树 | 静态→动态树 |
| 典型加速（带条件） | 2.3–2.8×（batch=1） | 3.0–6.5×（五任务） |

### 3.3 树验证：覆盖率 vs 成本

- SpecInfer 的 tree mask + 树形 KV 是公共祖先；EAGLE/Medusa 的树验证复用了同一抽象。
- 树宽不是越大越好：SpecInfer 在 **BS≥4** 时 2–3 最优；EAGLE-2 的动态树按 value 选点；CAST（`[二手]`）进一步把 GPU/batch 纳入成本。
- 树验证的收益来自“一次前向验证多分支”，成本是“验证 token 数 × 每 token 成本”。

### 3.4 免训练：用已有轨迹

- Lookahead：Jacobi 轨迹 + 2D 窗口（W/N/G）+ n-gram 池；贪心草稿 = one-hot，验证仍无损。
- PLD/REST/DictSpec：prompt/语料/字典匹配；收益与重复度/tokenizer fertility 强相关。
- 边界：命中率决定上限；需要剩余算力。

### 3.5 T>0：one-hot 困境与修复

- 动态树按 `q` 排序建树；T>0 时接受取决于 `p/q` 比值，`q` 不再预测接受 → 树塌缩。
- 直接“改成采样”会破坏无损性（存活依赖取值）。
- RheoSampling：前 m 个确定性 + 第 m+1 个残差采样；采样 token 用 proxy 参与排序/剪枝、用真实 `q̃` 验证；OT 重分配残差。
- 修复的代价：每步多一次采样 + OT 验证；**默认 EAGLE 未启用**，线上 T>0 仍需自行标定。

### 3.6 系统调度：从静态到自适应

- 静态 `num_speculative_tokens` 无法覆盖负载区间（vLLM 文档口径）。
- 方向：按 (request, position) 置信度分配验证预算（vLLM adaptive verification）；按上下文裁剪 draft（`draft_context_window`，本 commit 未检出）；变长验证 + ragged verify（SGLang DSpark）。
- 这些是“算法→wall-clock”的关键，见 [topics/systems-throughput-latency.md](topics/systems-throughput-latency.md)。

### 3.7 三次“系统化”转折

把 2023–2026 的变化按“解决了什么系统问题”重排，比按年份更清楚：

| 转折 | 之前的问题 | 解法 | 代价 | 代表 |
| :-- | :-- | :-- | :-- | :-- |
| **① 从“一个 draft”到“一棵树”**（2023–24） | 单链草稿一错全废，覆盖率低 | token tree + 树形 KV + topology-aware mask | 验证 token 数上升；实现复杂度上升 | SpecInfer |
| **② 从“独立模型”到“自投机”**（2024–25） | 独立 draft 难获取、难对齐、双模型服务贵 | target 特征/头/层跳过做草稿 | 要训草稿头；换 target 要重训 | Medusa / EAGLE |
| **③ 从“静态配置”到“按负载/按温度自适应”**（2025–26） | 一个 `num_speculative_tokens` 适配不了所有 batch/T | 动态树、adaptive verification、变长验证、T>0 解耦 | 系统复杂度上升；默认配置未必开启 | EAGLE-2/3、RheoSampling、vLLM/SGLang |

**读法**：三次转折都不是“算法更准”，而是“**把某个系统约束显式化**”——① 把覆盖率显式化，② 把 draft 获取成本显式化，③ 把负载/温度显式化。这也是为什么同一算法在不同系统里表现差异巨大。

### 3.8 一个请求从进入到返回的投机路径（跨系统抽象；vLLM `llm_base_proposer.py:511` / SGLang `eagle_worker_v2.py:676`）

| 步 | 做什么 | vLLM 对应 | SGLang 对应 |
| --: | :-- | :-- | :-- |
| 1 | 判定是否开投机、开哪种 | `speculative_config` | `get_spec()` |
| 2 | draft 采样 | `_sample_draft_tokens` | `draft_forward` |
| 3 | 组装验证输入 | `propose` + `draft_probs` 装配 | `build_eagle_verify_input` |
| 4 | 并行验证 | `rejection_sample` | `eagle_sample` |
| 5 | 接受/拒绝、写回 KV | `_rejection_*` kernel | `verify_tree_greedy_func` / sampling kernel |
| 6 | 记录指标 | `metrics.py` | 调度侧统计 |

这张表是 [vLLM 分册](papers/vllm-implementation.md) 与 [SGLang 分册](papers/sglang-implementation.md) 的“共同骨架”；两者的差异在第 2/4 步的语义（greedy vs probabilistic、topk=1 vs tree）。

---

## 4. 跨系统对比总表（带条件）

> **读法**：每一行的数字只在“条件”列成立；跨行不可直接排序。空值表示本轮未取得可核验数字，不表示“没有”。

| 系统 | 年份/出处 | 族 | 草稿来源 | 训练 | 拓扑 | 报告加速比 | 条件 | 证据 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Leviathan / Chen | 2023 | I | 独立小模型 | 预训练 | 链 | 2–3× | T5-XXL、同族 draft | 背景（未设分册） |
| **SpecInfer** | 2023–24 | I | 多 SSM | 用现成 | 树 | 分布式 1.5–2.8×；offloading 2.6–3.5× | 单机/多机；A10 24GB | [分册](papers/2305.09781-specinfer.md) |
| **Medusa** | 2024 | II | 并行头 | 训头 | 树 | Medusa-1 >2.2×；Medusa-2 2.3–2.8× | Vicuna-7B/13B、batch=1 | [分册](papers/2401.10774-medusa.md) |
| **Lookahead** | 2024 | III | Jacobi 轨迹 | 免训练 | n-gram | 1.5–2.3×；MT-Bench 7B 1.8×；8 卡 4× | A100/3090、代码任务 | [分册](papers/2402.02057-lookahead.md) |
| **EAGLE-1** | 2024 | II | 特征自回归 | 训头 | 静态树 | LLaMA2-70B 2.7–3.5× | T=0、batch=1 | [分册](papers/2401.15077-eagle-series.md) |
| **EAGLE-2** | 2024 | II | 特征自回归 | 训头 | 动态树 | 3.05–4.26× | T=0、三系列模型、六任务 | 同上 |
| **EAGLE-3** | 2025 | II | 多层特征 + 直接 token | 训头（8× 数据） | 动态树 | 3.0–6.5× | 五任务、chat+reasoning | 同上 |
| **EAGLE-3 @ SGLang** | 2025 | II | 同上 | — | 链（链长 3，不用树） | 1.38× 吞吐（batch=64）；2.36× 吞吐（batch=1） | 1×H100、LLaMA3.1-8B、MT-Bench | 同上（Table 3/4） |
| **MagicDec** | 2024–25 | I/自投机 | 稀疏 KV 自投机 | 免训练 | 链 | 最高 2.51× | 长上下文、batch 32–256、8×H100 | [分册](papers/2408.11049-magicdec.md) |
| **RheoSampling** | 2026 | II+验证 | EAGLE-3 官方 draft | 不重训 | 动态树 | τ 5.04→5.25；加速 2.84→2.93× | T=1.0、单 A6000、树 60/8 | [分册](papers/2609.21827-rheosampling.md) |
| **vLLM** | 2026 | 框架 | EAGLE/MTP/DFlash/standalone | 取决 draft | 链/树 | 本分册不报 | commit 2b85d9cb | [分册](papers/vllm-implementation.md) |
| **SGLang** | 2026 | 框架 | EAGLE/MTP/DFlash | 取决 draft | 链（topk=1）/树 | 本分册不报 | commit 2a08e261 | [分册](papers/sglang-implementation.md) |

### 4.1 三条跨表禁令

1. **禁止跨硬件**：H100 / A100 / L40 / RTX 3090 / TPU v5p 的同一算法不可直接比。
2. **禁止跨量纲**：µJ/token（能效）与 tokens/s（吞吐）不是同一量纲；SMoLPU 一类专用硅的数字不能与算法论文排榜。
3. **禁止把“上限”当“通用值”**：EAGLE-3 的 6.5× 是摘要上限；2.36× 是 SGLang batch=1 的吞吐；1.38× 是 batch=64 的吞吐。三个数字各有条件。

### 4.2 条件数字速查（按“条件”索引，不按“谁更大”）

| 条件 | 数字 | 出处 |
| :-- | :-- | :-- |
| LLaMA2-Chat 70B、T=0、MT-Bench | EAGLE 2.7–3.5×；EAGLE-2 3.51× | EAGLE / EAGLE-2 |
| LLaMA3-Instruct 8B、T=0、MT-Bench | EAGLE-2 3.46×，τ 4.53 | EAGLE-2 |
| Vicuna-7B、batch=1 | Medusa-1 >2.2×；Medusa-2 2.3–2.8× | Medusa |
| LLaMA-2-7B、MT-Bench、A100、FlashAttention | Lookahead 1.8× | Lookahead |
| 8 卡、ClassEval、强扩展 | Lookahead 4× | Lookahead |
| LLaMA-65B/OPT-30B、单机/多机 | SpecInfer 1.5–2.8× | SpecInfer |
| OPT-13B/30B、单 A10 24GB、vs FlexGen | SpecInfer 2.6–3.5× | SpecInfer |
| LLaMA-3.1-8B、长上下文、batch 32–256、8×H100 | MagicDec 2.51× | MagicDec |
| LLaMA-3.1-8B、S≥4000 | 加速随 batch 上升 | MagicDec |
| LLaMA-3.1-8B、S<4000 | 加速随 batch 下降 | MagicDec |
| 1×H100、LLaMA3.1-8B、MT-Bench、链长 3 | EAGLE b=24 0.93×；EAGLE-3 b=64 1.38× | EAGLE-3 Table 3 |
| 1×H100、batch=1、MT-Bench | 158.34 → 373.25 tokens/s（2.36×） | EAGLE-3 Table 4 |
| T=1.0、单 A6000、树 60/8 | RheoSampling τ 5.04→5.25；2.84→2.93× | RheoSampling |
| T=1.0、Vicuna-13B | Rheo τ 5.75→5.89；3.37→3.43× | RheoSampling |

> 这张表只用于“查条件”，**不能横向排序**。例如 2.51×（MagicDec，长上下文大 batch）与 6.5×（EAGLE-3，五任务上限）不是同一坐标。

---

## 5. 条件化结果读法

### 5.1 温度：T=0 与 T>0 是两条曲线

| 温度 | 动态树行为 | 接受率 | 引用注意 |
| :-- | :-- | :-- | :-- |
| T=0 | 按 q 排序 ≈ 接受顺序 | 高 | EAGLE-2/3 的主表多在此 |
| T>0 | 树塌缩为 one-hot | 显著下降 | 不能把 T=0 数字外推 |
| T→0 | 采样退化为 top token | 上升 | RheoSampling 的收益区间收窄 |

### 5.2 batch：先升后降，拐点随版本移动

- EAGLE：batch=2 1.40× → batch=24 **0.93×** → batch=64 0.99×。
- EAGLE-3：batch=2 1.81× → batch=24 1.39× → batch=64 1.38×。
- SpecInfer：batch 越大，相对收益越小；BS≥4 树宽 2–3。
- Medusa：模拟显示 batch>32 加速可能转负。
- MagicDec：长序列（S≥4000）时加速随 batch 上升；短序列相反。

### 5.3 序列长度与硬件

| 变量 | 影响 | 证据 |
| :-- | :-- | :-- |
| 序列长度 | 短序列 compute-bound；长序列 KV-bound | MagicDec §3 |
| GPU 的 FLOPS/带宽比 | H100 > A100 > L40 | MagicDec Table 1 |
| GQA vs 非 GQA | GQA 临界序列更长 | MagicDec §3 |
| 多卡 | TP/PP 基线可能 0.75–0.82×；LP 强扩展 4× | Lookahead §5 |

### 5.4 指标：两个分母

- `draft_acceptance_rate` 分母是提议 token；`mean_acceptance_length` 分母是验证步。
- 加深树通常降低前者、提高后者；只报一个会得出相反结论。
- 结构化输出会扣除作废草稿，分母变小。

---

## 6. 失效边界综述

### 6.1 算法边界

1. **T>0 动态树塌缩**（EAGLE-2/3；RheoSampling 修复但未默认启用）。
2. **top-K 的接受率上限**：即使 q=p，纯 top-K 也到不了 100%（缺随机 token）。
3. **草稿质量上限**：独立 draft 的容量差（100–1000×）；Medusa 头无前缀依赖；EAGLE-1/2 的特征约束限制数据 scaling。
4. **有界风险不是无损**：Medusa typical acceptance、ARC-Decode、CDSL。
5. **树参数不可移植**：EAGLE-2 的 60/6 与 RheoSampling 的 60/8 不可混用。

### 6.2 系统边界

1. **高 batch + 短序列**：验证成本主导，可能负收益。
2. **长序列显存墙**：KV 随 batch×序列增长；batch 上不去。
3. **draft 上下文失配**：超出训练长度后接受率崩塌；`draft_context_window` 在本轮 vLLM 快照未合入。
4. **静态配置盲区**：不存在适配所有并发度的 `num_speculative_tokens`。
5. **硬件映射**：GPU 与 TPU 的收益不可互推。
6. **量纲混用**：µJ/token 与 tokens/s 不可排榜。

### 6.3 证据边界

1. **未独立复现**：8 篇分册的数字均为论文/官方自报；RheoSampling 无公开代码。
2. **未设分册的 2026 工作**（DFlash/DSpark/BASTION）只作谱系定位，数字不入表。
3. **素材层与分册冲突时以分册为准**（例：EAGLE 的 arXiv 编号）。
4. **代码行为绑定 commit**：vLLM `2b85d9cb`、SGLang `2a08e261`；换版本需重核。

### 6.4 失效边界矩阵（按场景查；依据 [RheoSampling](papers/2609.21827-rheosampling.md) §6、[MagicDec](papers/2408.11049-magicdec.md) §6、[topic 3](topics/systems-throughput-latency.md) §8）

| 场景 | 最可能踩的坑 | 先查哪篇 |
| :-- | :-- | :-- |
| 线上 T=1.0 开 EAGLE-3 | 动态树 one-hot 塌缩，接受率低于离线测 | [RheoSampling](papers/2609.21827-rheosampling.md)、[topic 2](topics/verification-acceptance.md) |
| batch 从 1 扩到 64 | 收益从 1.81× 掉到 1.38×，甚至更低 | [topic 3](topics/systems-throughput-latency.md)、[EAGLE 分册](papers/2401.15077-eagle-series.md) §4.4 |
| 长上下文 + 大 batch | 用短序列结论会误判；KV 才是主瓶颈 | [MagicDec](papers/2408.11049-magicdec.md) |
| 端侧 / 单卡小显存 | 内存带宽与权重搬运优先于接受率 | [topic 3](topics/systems-throughput-latency.md) §7、素材层 edge 文档 |
| 结构化输出（JSON/SQL） | acceptance rate 分母被扣除，跨实验不可比 | [topic 2](topics/verification-acceptance.md) §7 |
| 缺少 draft_probs | vLLM 整批回退 legacy；SGLang 直接报错 | [vLLM](papers/vllm-implementation.md) §5、[SGLang](papers/sglang-implementation.md) §5 |
| 换 target 模型 | 草稿头/独立 draft 都要重训或重新适配 | [topic 1](topics/algorithm-families.md) §4 |
| 想宣称“无损” | 误把 typical acceptance / ARC 当严格无损 | [topic 2](topics/verification-acceptance.md) §6 |

---

## 7. 与相邻条目的边界

### 7.1 `OpenSource/vllm`

- **vLLM 条目**回答“vLLM 这个系统整体怎么工作”（调度、PagedAttention、分布式）。
- **本条目**只取“投机解码在 vLLM 里怎么落地”这一条路径（`draft_sample_method`、`rejection_sample_method`、`draft_probs` 生命周期）。
- 交叉点：[papers/vllm-implementation.md](papers/vllm-implementation.md) 是本条目对 vLLM 的**单点核验**，不替代 vLLM 条目。

> 任务书写的是 `Infra/vllm`；本仓库实际路径是 `OpenSource/vllm`（同一对象，按实际路径引用）。

### 7.2 `OpenSource/sglang`

- **SGLang 条目**回答“SGLang 的调度/前缀缓存/结构化解码”。
- **本条目**只取 EAGLE 草稿路径与 `speculative_use_rejection_sampling` 这一条；历史 issue #10308 的处置写在本条目 [SGLang 分册](papers/sglang-implementation.md) §6。
- 交叉点：SGLang 的 EAGLE-3 吞吐（batch=64 1.38×、batch=1 2.36×）属于**本条目**的系统条件证据，不重复进 SGLang 条目的架构叙述。

### 7.3 `Infra/QuantizationEdge`

- 量化/边缘部署回答“权重/激活怎么压”。
- 投机解码回答“怎么用草稿换并行验证”。
- 交叉点：QSpec（量化 + 投机）一类工作属于“两者交叉”，本条目只在谱系里提，不展开量化细节。

### 7.4 `Infra/TrainingInfra`

- 训练基础设施回答“怎么训 target / 怎么做 RL rollout”。
- 本条目只在“drafter 训练时机”“RL 长尾（TLT）”处交叉；不展开训练系统。
- 交叉点：EAGLE-3 的 8× 数据、Medusa 的头训练、SpecInfer 的 SSM 预训练都属于“训练成本”，本条目只给成本数字，不给训练配方。

### 7.5 `LLM/*` 与 `Models/*`

- 模型条目回答“这个模型是什么/能力如何”。
- 本条目回答“怎么加速任意自回归模型”；不绑定具体模型家族。
- 交叉点：EAGLE 的实验覆盖 Vicuna/LLaMA/Mixtral，但结论是“方法”的，不是“模型”的。

---

## 8. 两条历史未核验项的处理结果

### 8.1 EAGLE 官方代码对 top-K 下 draft 概率的处理

**结论**：在 `SafeAILab/EAGLE` @ **`cb7e0841fe0c206c6ed74a197ad5e2a1f13f5a2b`**（2026-02-20，commit patch 的 `Date:` 头）中：

- 官方 **tree / EA 评估路径**把草稿概率按 **1.0** 处理：`eagle/model/utils.py:398` 为 `qx = 1.0`，`:399` 为 `acp = px / qx`；即接受概率退化为 `p(x)`，草稿分布被当作 one-hot。
- 调用点：`eagle/model/ea_model.py:270`、`:452`；`eagle/evaluation/gen_ea_alpha_llama2chat.py:87`、`gen_ea_alpha_vicuna.py:93`（本轮按文件行号复核）。
- **边界（不夸大）**：同仓库另有 HF 风格实现 `eagle/modeling_eagle.py`，其 `evaluate_posterior` 在 `:1427` 使用 `qx = cart_candidates_prob[batch, j, i]`，即**保留真实草稿概率**。因此“置 1”是**官方 tree/EA 评估路径**的事实，**不是仓库内所有路径**的共性。
- **影响**：这为“T>0 下按 q 建树 + one-hot 验证导致接受率下降”提供了实现层证据；也说明“无损≠高效”——one-hot 提议仍可无损，但接受率低。

**证据等级**：`[精读原文]`（代码级，仓库 @ commit + 文件:行）。

### 8.2 SGLang #10308 后续 PR 是否合入

**结论（准确表述）**：

1. issue `sgl-project/sglang#10308` **真实存在**：标题 *[Feature] Speculative sampling supports passing the predicted probability of the draft model and sample token for verification when **topk=1***；2025-11-03 开立、指派 `hnyls2002`；**2026-01-03 被 github-actions 以 inactive 自动关闭**；页面 timeline **未观察到 linked / merged PR**。
2. **能力已在主线**（`sgl-project/sglang` @ `2a08e261`，2026-10-16）：
   - `eagle_worker_v2.py:178–180`：开启 `speculative_use_rejection_sampling` 时 `assert self.topk == 1`；
   - `eagle_worker_v2.py:727–733`：非 greedy 且开启拒绝采样 → 构造 `draft_probs`；
   - `eagle_info.py:35`/`:162`：`EagleVerifyInput` / `EagleDraftInput` 均有 `draft_probs` 字段；
   - `eagle_utils.py:947`：选 `chain_speculative_sampling_triton`；
   - `eagle_utils.py:1000–1013`：`draft_probs` 缺失/词表不匹配 → **硬报错**；
   - `eagle_utils.py:1030–1044`：`target_probs`、`draft_probs`、`uniform_samples` 一起传入 kernel。
3. **因此**：
   - 说“#10308 已修复”**不准确**（无 linked PR，issue 未 reopen）；
   - 说“完全没处理”**也不准确**（能力已在 topk=1 路径）；
   - **准确说法**：issue 未被正式关联；其请求的 topk=1 采样验证能力已在主线实现，**硬限制 topk=1**；tree topk>1 仍走 `tree_speculative_sampling_target_only`（`draft_probs` 置零），不是 p/q 拒绝采样。

**证据等级**：`[精读原文]`（代码级）；issue 状态为页面级核验。

### 8.3 两条的“卡在哪”

| 项 | 卡点 | 处置 |
| :-- | :-- | :-- |
| EAGLE 代码 | 只能证明该 commit 的行为，不能证明未来版本 | 钉 commit；标注“tree/EA 路径”边界 |
| SGLang #10308 | 无法把“能力存在”等同于“issue 已修复” | 分开写“issue 状态”与“代码能力”；给出剩余缺口 |

---

## 9. 选文说明

### 9.1 候选池 / 入选 / 排除

- **候选池 N = 22**（论文/系统/代码仓库；含本轮新增与素材层已出现的工作）。
- **入选 M = 8**（6 篇论文分册 + 2 篇代码核验）。
- **排除 14**，逐条理由见 [sources/CANDIDATES.md](sources/CANDIDATES.md)；**排除项不编造 ID**。

### 9.2 为什么是这 8 篇

| 入选 | 理由（一句话） |
| :-- | :-- |
| EAGLE 系列 | 工业默认；三代演进把“特征级/动态树/TTT”这条主线讲全 |
| Medusa | 并行头代表；typical acceptance 是“有界风险”的早期样本 |
| Lookahead | 免训练代表；one-hot 草稿无损性的关键论据 |
| SpecInfer | 树验证系统源头；多 SSM/树宽/batch 依赖 |
| MagicDec | 系统条件代表；临界序列长度把“大 batch 不划算”证伪一半 |
| RheoSampling | T>0 动态树的无损修复；本轮“转折点”的核心证据 |
| vLLM | 生产框架一手代码；greedy/probabilistic 语义分叉 |
| SGLang | 生产框架一手代码；#10308 的处置对象 |

### 9.3 没选的（以及为什么）

- **DFlash / DSpark / BASTION**：2026 预印本/工程博客，正文与复现条件不稳定；本轮只做谱系定位，数字不入表。列为下一轮候选。
- **HASS**：与 EAGLE-3 同属“训练目标/上下文对齐”线，但 EAGLE-3 论文已直接对照 HASS；单独设册会重复。
- **Hydra / SWIFT / CLaSp / LayerSkip**：自投机子型，机制已被 Medusa/EAGLE 覆盖；在素材层保留。
- **Sequoia / TriForce / Mirror-SD**：系统优化，部分与 MagicDec/SpecInfer 重叠；本轮不设册。
- **QSpec / HiSpec**：量化/分层交叉，归 `Infra/QuantizationEdge` 更合适。
- **多模态/端侧/领域特化**：素材层已有横切文档；本轮篇幅优先给“验证 + 系统”两条主线。

### 9.4 候选池统计（可逐条核对）

| 项 | 数 | 说明 |
| :-- | --: | :-- |
| 候选池 N | 22 | 论文 14 + 系统/框架 5 + 代码仓库 3 |
| 入选 M | 8 | 6 论文 + 2 代码 |
| 排除 | 14 | 8 条带已核实 ID；6 条类别性排除 |
| 未设分册但进谱系 | 3+ | DFlash / DSpark / BASTION（只定位，不入表） |
| 素材层保留 | 11 | 未重写、未删除；冲突以分册为准 |

> 排除项的具体 ID 与理由见 [sources/CANDIDATES.md](sources/CANDIDATES.md)；**没有核实 ID 的排除项只写类别，不编号**。

---

## 10. skill 使用证据

| skill | 用在哪 | 证据 |
| :-- | :-- | :-- |
| `researcher`（deep） | 论文筛选、正文精读、七问抽取 | 8 篇分册均有 `arXiv ID + 版本日期`；每篇「亮点四行」+ 七问 + 失效边界；`claim_audit` 报数见 §11 |
| `code-researcher`（trace/deep） | vLLM / SGLang / EAGLE 代码核验 | 全部分册使用 `仓库@commit:文件:行`；vLLM/SGLang 分册含代码地图与调用链 |
| `paper-fetcher` | arXiv 元数据/版本/license 核验 | `sources/MANIFEST.md` 的 ID/版本/日期/标题/作者/license 均逐条回查；本地缓存不依赖 |

### 10.1 三个 skill 的具体落点

- `researcher`（deep）：先用 arXiv API 回查候选的标题/作者/版本/日期，再抓 HTML 正文逐节读；产出模板统一为「亮点四行 + 七问 + 带条件表 + 失效边界」。
- `code-researcher`（trace）：先定位入口（`eagle_sample` / `rejection_sample`），再沿调用链追到 kernel；每个强结论必须有 `文件:行`，否则降级为“推断”。
- `paper-fetcher`：只用于元数据/引用，不把摘要当正文；无正文的条目（ARC-Decode、CAST）标 `[摘要级]`/`[二手]`，不升格。

---

## 11. 复现与核验记录

| 项 | 结果 |
| :-- | :-- |
| 论文元数据 | 9 个 arXiv ID 经 `export.arxiv.org` 逐条回查（标题/作者/版本/日期/license） |
| EAGLE 代码 | @ `cb7e0841`（2026-02-20），`utils.py:398–399`、`modeling_eagle.py:1427` |
| vLLM 代码 | @ `2b85d9cb`（2026-10-17），5 个文件的行号锚点 |
| SGLang 代码 | @ `2a08e261`（2026-10-16），4 个文件的行号锚点 |
| issue #10308 | 页面 timeline：assigned / comment / closed(inactive) / labeled；无 linked PR |
| 独立复现 | ❌ 未做；所有性能数字为论文/官方自报 |
| `claim_audit` | 见交付说明（`--lang zh` 报数） |

### 11.1 本轮自检清单

| # | 检查 | 结果 |
| --: | :-- | :-- |
| 1 | `papers/` 篇数 6–8 | **8** |
| 2 | 每篇 ≥200 行 | 200–244 行（全部达标） |
| 3 | 每篇四行亮点 | 8/8 |
| 4 | 每篇七问 | 8/8 |
| 5 | 每篇 ≥5 处带条件数字 | 论文类均满足；代码类以 `文件:行` + 版本为条件锚点，**不伪造 benchmark** |
| 6 | 每篇 ≥1 张带条件列对照表 | 8/8 |
| 7 | 每篇独立失效边界段 | 8/8 |
| 8 | `topics/` 3 篇 × 150–300 行 | 164 / 216 / 168 |
| 9 | `report.md` ≥600 行 | 见文件行数 |
| 10 | `sources/MANIFEST.md` + `CANDIDATES.md` | 已建 |
| 11 | 两条历史未核验项 | 均已给结论/边界（§8） |
| 12 | 论文全文不入库 | ✅ 只有清单与分册 |
| 13 | 代码不入库 | ✅ 只有 `文件:行` 短引用 |
| 14 | 价格类 `$` 转义 | 本条目未使用价格数字；公式用 `$...$` 包裹 |

---

## 12. 引用注意（一句话版）

- 引用加速比：必须带 `(batch, T, 序列长度, 硬件, 树参数)`。
- 引用“无损”：必须说明是严格 / 序列级 / 有界风险（三档定义见 [topics/verification-acceptance.md](topics/verification-acceptance.md) §6）。
- 引用 EAGLE-3：6.5× 是上限，1.38× 是 batch=64 吞吐，2.36× 是 batch=1 吞吐。
- 引用 RheoSampling：2.93× 是相对自回归，不是相对 EAGLE-3。
- 引用 SGLang #10308：分开写“issue 状态”与“代码能力”。

### 12.1 术语对照（中英）

| 中文 | 英文/缩写 | 一句话解释 |
| :-- | :-- | :-- |
| 投机解码 | speculative decoding (SD) | 草稿 + 并行验证的加速范式 |
| 草稿模型 | draft model / drafter | 产生候选的便宜模型 |
| 目标模型 | target model / verifier | 做最终验证的大模型 |
| 接受率 | acceptance rate | 被接受草稿 / 提议草稿 |
| 平均接受长度 | mean acceptance length (τ) | 每验证步平均产出 token 数 |
| 拒绝采样 | rejection sampling | `min(1,p/q)` 接受 + 残差重采 |
| 典型接受 | typical acceptance | Medusa 的阈值接受（有损） |
| 动态草稿树 | dynamic draft tree | 按上下文/置信度建树 |
| 树注意 | tree attention | 一次前向验证整棵树 |
| 前缀依赖 | prefix dependency | 草稿是否依赖前一个草稿 token |
| 有界风险 | risk-bounded | 分布偏移受控但非严格等价（见 [topic 2 §6](topics/verification-acceptance.md)） |
| 稀疏 KV | sparse KV | 只保留部分 KV 做 draft |
| 临界序列长度 | critical/inflection sequence length | 投机收益随 batch 反转的分界 |
| 逐位置接受率 | per-position acceptance rate | 第 j 个草稿位置的历史接受率 |

### 12.2 维护约定

- 新增论文分册时：先回查 arXiv 元数据（ID/版本/日期/license），再抓正文；没有正文的只进 `CANDIDATES`，不进 `papers/`。
- 新增代码核验时：必须钉 commit，并给 `文件:行`；跨版本行为变化要在分册里写“绑定 commit”。
- 修改 `report.md` 的数字时：同步对应分册与 `sources/MANIFEST.md`；**分册是数字的唯一主写处**，report 只做汇总。
- 生成物（`INDEX.md` / `index/*`）由脚本产出，不手改。

---

## 附录 A：历史素材层（11 篇）的定位

| 素材文档 | 保留原因 | 与新结构的关系 |
| :-- | :-- | :-- |
| `speculative-classical-and-self.md` | 经典/自投机的时间线 | 被 `papers/` 1–3 覆盖，保留作素材 |
| `speculative-eagle-series.md` | EAGLE 细节（含一处错误 ID） | 以 `papers/2401.15077-eagle-series.md` 为准 |
| `speculative-stochastic-verification.md` | T>0 的首轮分析 | 被 `topics/verification-acceptance.md` + RheoSampling 分册升级 |
| `speculative-block-diffusion.md` | 块扩散/检索式线索 | 谱系 IV 的素材；本轮未设分册 |
| `speculative-cascade-heterogeneous.md` | 级联/异构 | 系统条件的补充素材 |
| `speculative-draft-training-2026.md` | 训练目标新法 | 与 EAGLE-3/Medusa 训练章节交叉 |
| `speculative-training-optimization.md` | 训练目标优化 | 同上 |
| `speculative-edge-cloud-hardware.md` | 端侧/硬件 | 系统条件补充 |
| `speculative-domain-language.md` | 领域/语种 | 检索式/结构化输出的补充 |
| `speculative-multimodal.md` | 多模态 | 本轮未覆盖的方向 |
| `speculative-systems-and-frameworks.md` | 系统/框架 | 被 vLLM/SGLang 分册 + topic 3 升级 |

---

## 来源

- 论文（均经 arXiv 元数据逐条核验）：EAGLE 2401.15077v3；EAGLE-2 2406.16858v2；EAGLE-3 2503.01840v3；Medusa 2401.10774v3；Lookahead 2402.02057v1；SpecInfer 2305.09781v4；MagicDec 2408.11049v5；RheoSampling 2609.21827v1。
- 代码：`SafeAILab/EAGLE` @ `cb7e0841`；`vllm-project/vllm` @ `2b85d9cb`；`sgl-project/sglang` @ `2a08e261`。
- 清单：[sources/MANIFEST.md](sources/MANIFEST.md)、[sources/CANDIDATES.md](sources/CANDIDATES.md)。
