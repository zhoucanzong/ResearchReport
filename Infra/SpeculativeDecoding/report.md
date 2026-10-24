---
display_name: 投机解码
type: topic-research
domain: Infra
subject: SpeculativeDecoding
date: 2026-10-22
evidence: 精读原文
status: needs-review
---

# 投机解码（Speculative Decoding）技术专题 · 深度调研

> **声明**：本报告由 AI Agent 自动调研生成，未经官方确认；引用具体参数、日期或 benchmark 前请回溯原始来源。
> **资料核查**：截至 2026-10-23；新增 HSD、Delayed Tree Expansion、CaDDTree 与 TLAR 四篇精读，补齐严格无损序列验证、分支时机、树预算成本和轨迹检索价值四条机制线。论文与源码固定版本及证据范围见[来源清单](sources/MANIFEST.md)。
> **定位**：投机解码 = **用低成本草稿换 target 的并行验证**，在**输出分布可证等价（或明示有界风险）**的前提下降低解码 wall-clock；定义与保证边界见[验证专题](topics/verification-acceptance.md)。本条目管的是“**算法 + 验证 + 系统条件**”这一整条链，不把“草稿模型训练”单独抽出去。

**证据等级约定（单一主等级）**：

| 等级 | 含义 | 本轮用法 |
| :-- | :-- | :-- |
| `[精读原文]` | 固定论文版本并定位到支撑结论的正文；代码类须有 `仓库@commit:文件:行` | 每篇分册标出具体阅读范围；代码实现另标静态核验范围 |
| `[摘要级]` | 仅核验官方摘要/会议页/项目页，未通读正文 | 只用于“登记存在”，不进结论数字 |
| `[二手]` | 第三方解读、工程博客、周报 | 只作线索，不入对照表 |
| `[⚠️受限核验]` | 一手对象无法直接抓取，只能经镜像/元数据交叉确证 | 逐条写明“卡在哪” |

**规则**：每条只给**一个主等级**；混合来源取**最弱**等级并在括号里注明来源类型。`[摘要级]` **不许升格**为 `[精读原文]`。

---

> **补充核验（2026-10-22）**：已重新核对有限分布拒绝采样、截断的接受率反例，以及固定 vLLM 源码中的 point-mass 恢复分支；其余论文实验和 legacy 素材尚未逐项重验，不能将此记录解释为整篇验收通过。

## 深度阅读导航

本条目采用三层结构：本页 = 入口 + 结论 + 谱系 + 总表；`papers/` = 逐篇精读；`topics/` = 横切专题。

### 分册（`papers/`，14 篇论文笔记覆盖 16 篇论文，另有 2 份框架代码核验）

| # | 分册 | 系统 | 在谱系中的位置 | 行数 |
| --: | :-- | :-- | :-- | --: |
| 1 | [2401.15077-eagle-series.md](papers/2401.15077-eagle-series.md) | EAGLE / EAGLE-2 / EAGLE-3 | 自投机·特征级自回归（工程实现代表） | 244 |
| 2 | [2401.10774-medusa.md](papers/2401.10774-medusa.md) | Medusa | 自投机·并行头（轻量插件） | 204 |
| 3 | [2402.02057-lookahead.md](papers/2402.02057-lookahead.md) | Lookahead Decoding | 免训练·Jacobi 轨迹 | 202 |
| 4 | [2305.09781-specinfer.md](papers/2305.09781-specinfer.md) | SpecInfer | 独立 draft·树验证系统 | 201 |
| 5 | [2408.11049-magicdec.md](papers/2408.11049-magicdec.md) | MagicDec | 系统条件·长上下文大 batch | 200 |
| 6 | [2609.21827-rheosampling.md](papers/2609.21827-rheosampling.md) | RheoSampling | T>0 动态树的无损修复 | 216 |
| 7 | [2610.08678-secure-sd.md](papers/2610.08678-secure-sd.md) | SecureSD | 有损验证的安全—效用不对称；早期位置校正 | 55 |
| 8 | [2608.13524-dartree.md](papers/2608.13524-dartree.md) | DARTree | 扩散草稿 + 分支条件校正 + 延迟剪枝 | 31 |
| 9 | [2609.33184-specstream.md](papers/2609.33184-specstream.md) | SpecStream | 历史 KV 流式 offload 与共卡草稿调度 | 44 |
| 10 | [2610.23787-dlite.md](papers/2610.23787-dlite.md) | DLite | 复用 target hidden states 的无历史 draft KV | 48 |
| 11 | [2601.05724-hsd.md](papers/2601.05724-hsd.md) | HSD | 分层概率质量平衡的严格无损验证 | 84 |
| 12 | [2602.16994-delayed-tree.md](papers/2602.16994-delayed-tree.md) | Delayed Tree Expansion | 选择分支时机，调整多路径草稿树拓扑 | 83 |
| 13 | [2606.01813-caddtree.md](papers/2606.01813-caddtree.md) | CaDDTree | 按实测验证成本逐轮选择扩散草稿树预算 | 53 |
| 14 | [2610.07350-tlar.md](papers/2610.07350-tlar.md) | TLAR | 复用当前生成轨迹，并按验证收益调度检索 | 54 |
| 15 | [vllm-implementation.md](papers/vllm-implementation.md) | vLLM @ 2b85d9cb | 生产框架·draft/verify 两路径 | 220 |
| 16 | [sglang-implementation.md](papers/sglang-implementation.md) | SGLang @ 2a08e261 | 生产框架·topk=1 拒绝采样 | 219 |

### 横切专题（`topics/`，3 篇）

| # | 专题 | 回答什么 | 行数 |
| --: | :-- | :-- | --: |
| 1 | [algorithm-families.md](topics/algorithm-families.md) | 四大家族、五根轴、选型判据 | 164 |
| 2 | [verification-acceptance.md](topics/verification-acceptance.md) | 单链/树/有界风险的无损性准则、top-K 到底改变什么、指标口径 | 216 |
| 3 | [systems-throughput-latency.md](topics/systems-throughput-latency.md) | batch×序列×硬件的相图、吞吐-延迟权衡、上线清单 | 168 |

### 历史素材层（legacy 素材，未按新标准校验）

本轮按“**改造，不是从零写**”的要求，保留了 2026-10 之前的 11 篇横切子文档作为素材层，**未重写、未删除**，并已整体移入 [`legacy/`](legacy/)（内容未改，仅修正指向主报告的相对链接）：

[`speculative-classical-and-self.md`](legacy/speculative-classical-and-self.md)、[`speculative-eagle-series.md`](legacy/speculative-eagle-series.md)、[`speculative-stochastic-verification.md`](legacy/speculative-stochastic-verification.md)、[`speculative-block-diffusion.md`](legacy/speculative-block-diffusion.md)、[`speculative-cascade-heterogeneous.md`](legacy/speculative-cascade-heterogeneous.md)、[`speculative-draft-training-2026.md`](legacy/speculative-draft-training-2026.md)、[`speculative-training-optimization.md`](legacy/speculative-training-optimization.md)、[`speculative-edge-cloud-hardware.md`](legacy/speculative-edge-cloud-hardware.md)、[`speculative-domain-language.md`](legacy/speculative-domain-language.md)、[`speculative-multimodal.md`](legacy/speculative-multimodal.md)、[`speculative-systems-and-frameworks.md`](legacy/speculative-systems-and-frameworks.md)。

> **使用规则**：素材层用于查“2026 上半年的横向线索”；**与 `papers/` 冲突时以 `papers/` 为准**（例：素材层里 EAGLE 的 arXiv 编号有一处误写为 `2403.00835`，该编号实际是 CLLMs；正确编号是 **2401.15077**，见 [papers/2401.15077-eagle-series.md](papers/2401.15077-eagle-series.md)）。

---

## 0. 一页结论

1. **投机解码的收益不是“算法属性”，而是“算法 × 负载 × 硬件”的联合属性**。EAGLE 在 SGLang batch=24 就跌破 1.0×（0.93×），EAGLE-3 在 batch=64 仍有 1.38×；同一族、不同版本，拐点不同。`[精读原文]`
2. **“无损”须按保证与算法形式区分**：严格分布保持与贪心等价需要各自证明；逐 token / 序列级是验证形式，不能另当正确性等级；typical acceptance 的经验质量也不能直接升级为分布偏移有界。新近 SecureSD 还测到：对有损 verifier，jailbreak/prompt-injection 指标可能比通用 utility 更早退化；这不推翻严格无损方法的等价证明。详见 [验证专题 §6](topics/verification-acceptance.md#6-无损需要区分保证与经验)与[SecureSD 精读](papers/2610.08678-secure-sd.md)。`[精读原文]`
3. **T>0 的动态树必须分析候选选择条件**：不能从贪心 benchmark 推出所有采样配置的收益。对按 `q` 排序/剪枝的随机候选，需核对存活条件和实际提议分布；RheoSampling 给出一种特定构造。未核版本的默认配置不在此断言。`[精读原文]`
4. **top-K 改变的是接受率，不是无偏性**：单链拒绝采样的 α* = Σ min(p,q) = 1 − TV；top-K 截断只要验证端用同一分布、残差用完整 p，输出仍严格等于 p。把“top-K 有偏”当结论是错的。`[精读原文]`
5. **草稿来源的四族不是代际，而是并存选项**：独立 draft（SpecInfer）、自投机（EAGLE/Medusa）、免训练（Lookahead）、块/扩散（DFlash 一类）。选族先看“有没有 draft / 能不能训 / 输出是否模板化”。`[精读原文]`
6. **高 batch 的结论要加第三维：序列长度**。短序列 + 大 batch 亏（SpecInfer/Medusa/vLLM 口径一致）；长序列 + 大 batch 可能赚（MagicDec：S≥4000 时加速随 batch 上升，最高 2.51×）。`[精读原文]`
7. **指标必须成对**：`draft_acceptance_rate`（分母=提议草稿数）与 `mean_acceptance_length`（分母=验证步数，含 bonus）会反向移动；只报一个会得出相反结论。`[精读原文（vLLM 代码）]`
8. **工程落地已经分叉成两种语义**：vLLM 用 `draft_sample_method ∈ {greedy, probabilistic}`；SGLang 用 `speculative_use_rejection_sampling` + `assert topk == 1`。两者都能把真实 `draft_probs` 传给验证，但适用形状不同。`[精读原文（代码）]`
9. **历史 issue #10308 的准确结论**：issue 于 2025-09-11 开立、2026-01-03 以 `state_reason=completed` 由 `github-actions[bot]` 关闭，timeline 无 linked PR/commit；但它请求的“topk=1 采样验证”能力已在 SGLang 主线以 `draft_probs` + 拒绝采样开关实现，且**硬限制 topk=1**；tree topk>1 仍走 target-only kernel。`[精读原文（代码）]`
10. **新近工作解决不同瓶颈**：HSD 改严格无损的序列级概率恢复；Delayed Tree 改分支时机；CaDDTree 改树预算的成本目标；DARTree 改扩散候选树路径；DLite 改草稿历史表征；SpecStream 改 KV 生命周期与数据移动；TLAR 改候选来源和检索调度。它们不是一条能按单一加速比排名的算法线，见 §2.4。
11. **证据边界**：专题现含 [16 篇学术论文与 5 个固定版本代码快照](sources/MANIFEST.md)（含参考实现）；各新分册均记录固定版本、阅读锚点与实验范围。没有独立复现实验，性能数字均为作者或官方报告值。

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
| 自投机（Medusa / EAGLE / MTP / 层跳过） | ✅ | 当前工程实现代表 |
| 免训练（Lookahead / PLD / REST / 字典） | ✅ | 独立一族，端侧/低资源重要 |
| 树验证系统（SpecInfer / Sequoia） | ✅ | 验证侧的基础设施 |
| 块/扩散草稿（DFlash / DSpark / BASTION） | ✅（谱系） | 扩散模型为自回归 target 生成待验证草稿；本专题只讨论该交叉机制，独立 diffusion LM 见 [LLM/DiffusionLM](../../LLM/DiffusionLM/report.md) |
| 纯量化 / 纯剪枝 / 纯 KV eviction | ❌ | 不产生“候选-验证”结构；归 `Infra/QuantizationEdge` |
| 纯 batch 调度 / continuous batching | ❌ | 系统优化但不含投机；归 `Infra/TrainingInfra` 或框架条目 |
| 扩散语言模型（非投机范式） | ❌ | 独立生成范式不是本条目主体；训练目标与去噪机制见 [LLM/DiffusionLM](../../LLM/DiffusionLM/report.md) |

### 1.3 无损性三档（引用时必须声明）

| 档 | 定义 | 代表 | 可否写“严格无损” |
| :-- | :-- | :-- | :-- |
| **严格分布等价** | 对任意序列，输出概率 = p(Seq) | 经典单链；静态树；HSD；RheoSampling（Theorem 1）；Traversal Verification；HeteroSpec（ACL 2026，`[摘要级]`） | ✅ |
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
| 2026 H2 | T>0 正确性、安全边界与新系统瓶颈 | RheoSampling；SecureSD；SpecStream | [RheoSampling](papers/2609.21827-rheosampling.md)、[SecureSD](papers/2610.08678-secure-sd.md)、[SpecStream](papers/2609.33184-specstream.md) |
| 2026 新近结构线 | 扩散草稿的分支校正；Agent 场景下复用 target 上下文 | DARTree；DLite | [DARTree](papers/2608.13524-dartree.md)、[DLite](papers/2610.23787-dlite.md) |
| 2026 | 生产框架落地 | vLLM / SGLang | [vLLM](papers/vllm-implementation.md)、[SGLang](papers/sglang-implementation.md) |

### 2.3 五根可判定的轴

| 轴 | 取值 | 判定方式 |
| :-- | :-- | :-- |
| A 草稿来源 | 独立 / target 自身 / 检索 / 块 | 看是否需要额外权重 |
| B 训练 | 免训练 / 训头 / 训独立模型 | 看训练管线 |
| C 拓扑 | 链 / 静态树 / 动态树 / 块 | 看验证 mask |
| D 接受率上限 | 由 p 与 q 的对齐度决定 | 同条件比 τ 或 acceptance rate |
| E 负载行为 | batch↑ 升/降/反转 | 看 batch×序列扫描 |

> 本节依据 [DARTree](papers/2608.13524-dartree.md)、[SpecStream](papers/2609.33184-specstream.md) 与 [DLite](papers/2610.23787-dlite.md) 的固定版本原文。

### 2.4 投机解码方向的新近工作

截至 2026-10-23，投机解码的进展不只是“更高接受率”。下面的判断来自近期固定版本精读；这些工作分别改变不同层：

| 工作 | 它改变什么 | 读它时先问什么 |
| :-- | :-- | :-- |
| [DARTree](papers/2608.13524-dartree.md)（8 月） | 对扩散草稿沿多条候选分支分别做因果校正，并把建树与全局 top-B 剪枝分离 | 树验证预算与候选宽度固定时，批量建树是否在目标模型/硬件上减少真实 draft wall-clock？ |
| [SpecStream](papers/2609.33184-specstream.md)（9 月） | 按 target commit 边界 offload 历史 KV、流式验证、共享 KV 读取，并在传输等待时共卡运行 draft | PCIe 数据搬运能否被 overlap 隐藏到足以补偿每轮全历史传输？它明确显示长输入仍慢于全驻 GPU。 |
| [DLite](papers/2610.23787-dlite.md)（10 月） | 把 target 多层 hidden states 当作紧凑上下文，草稿器仅做局部预测，不保存 draft 历史 KV | 免去的是 draft KV 和重复历史建模；target KV 仍在，收益目前由 Qwen3-4B/8B 证据支撑。 |
| [HSD](papers/2601.05724-hsd.md)（3 月） | 在可访问树分支间平衡概率过剩/不足，做严格分布保持的序列级验证 | EAGLE-3 等概率槽位实验不能单独证明 HSD 提升了接受率；其吞吐结果也受 verifier 实现路径影响。 |
| [Delayed Tree Expansion](papers/2602.16994-delayed-tree.md)（2 月） | 先走 trunk，再由 selector 决定分支深度、宽度和数量 | 三模型平均吞吐略高于 Traversal，但 Llama 子项回退；selector 依赖离线轨迹与目标硬件延迟测量。 |
| [CaDDTree](papers/2606.01813-caddtree.md)（6 月） | 将扩散草稿树目标从最大接受长度改为每轮时间归一化收益，按边际验证成本选节点预算 | 停止保证依赖单调凸验证成本；当前主证据仅覆盖 Qwen3-4B/8B + DFlash 与 8×A800。 |
| [TLAR](papers/2610.07350-tlar.md)（10 月） | 检索当前生成轨迹，以此前 target 验证收益调节检索频率与宽度 | B200 上长代码输出有吞吐收益，512-token 短输出略亏；轨迹来源的价值随模型与任务而变。 |

我的阅读判断：它们分别对应**候选覆盖效率、系统内存/数据移动、草稿表征与训练**三类问题；不能把 DARTree/DLite 的 `τ` 或 AR-relative speedup 与 SpecStream 的并发服务 throughput 横向排名。若继续扩展本专题，优先追 DLite 的其它 target/训练可迁移性、SpecStream 的真实源码与不同互联拓扑，再看 lossless 与高并发共存的条件。

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
- [Delayed Tree Expansion](papers/2602.16994-delayed-tree.md) 将分叉点延后并按硬件/模型代价选择；[CaDDTree](papers/2606.01813-caddtree.md) 则直接把每轮验证成本纳入树预算。前者改变**分支何时出现**，后者改变**每轮扩多少节点**；机制与 DARTree 的候选校正不同。

### 3.4 免训练：用已有轨迹

- Lookahead：Jacobi 轨迹 + 2D 窗口（W/N/G）+ n-gram 池；贪心草稿 = one-hot，验证仍无损。
- PLD/REST/DictSpec：prompt/语料/字典匹配；收益与重复度/tokenizer fertility 强相关。
- 边界：命中率决定上限；需要剩余算力。

### 3.5 T>0：one-hot 困境与修复

- 动态树按 `q` 排序建树；T>0 时接受取决于 `p/q` 比值，`q` 不再预测接受 → 树塌缩。
- 直接“改成采样”会破坏无损性（存活依赖取值）。
- RheoSampling：前 m 个确定性 + 第 m+1 个残差采样；采样 token 用 proxy 参与排序/剪枝、用真实 `q̃` 验证；OT 重分配残差。
- 修复的代价：每步多一次采样 + OT 验证；默认值必须按具体版本核对，线上 T>0 应同时核正确性和效率。

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

### 3.8 一个请求从进入到返回的投机路径（跨系统抽象；vLLM `llm_base_proposer.py:511` / SGLang `eagle_worker_v2.py:671`）

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
| **DARTree** | 2026 | IV+校正 | DFlash/扩散块 + Domino correction | 不重训 | 路径校正树 | GSM8K 9.73×；τ=12.97 | Qwen3-4B、T=0、batch=1、RTX 6000 Ada、B=64 | [分册](papers/2608.13524-dartree.md) |
| **DLite** | 2026 | II/IV 交叉 | target hidden-state + 局部块草稿 | 两段蒸馏 | 块 + 顺序头 | SWE-Bench 2.74×；τ=3.19 | Qwen3-8B、H800、K=7、相对本地 AR | [分册](papers/2610.23787-dlite.md) |
| **SpecStream** | 2026 | serving 系统 | Draft 与 Target 共卡 | 使用现成模型 | 流式多-query 验证 | vs TriForce 1.41×/1.32×；vs SD+Offload 1.44×/1.62× | 2×A800 PCIe、8 并发汇总；长输入仍逊于 GPU-resident SGLang | [分册](papers/2609.33184-specstream.md) |
| **HSD** | 2026 | verifier | 现有 draft | 不改 draft | 分层序列验证 | 32.52 / 27.48 / 12.33 tokens/s | Qwen2.5-72B/0.5B、1×H20、T=1；GSM8K/HumanEval/CNN-DM；相对 tokenwise +3.3–4.4% | [分册](papers/2601.05724-hsd.md) |
| **Delayed Tree Expansion** | 2026 | tree 拓扑 | 独立 i.i.d. draft | selector 需训练 | trunk 后动态分支 | 平均 16.69 vs 15.89 tokens/s | 三模型、五数据集、八采样设置；2×A100；Llama 子项回退 | [分册](papers/2602.16994-delayed-tree.md) |
| **CaDDTree** | 2026 | 成本感知树预算 | DFlash 块草稿 | 不新增训练 | 每轮按成本选树大小 | 不报单一加速倍数；多数配置贴近/优于 DDTree 网格 oracle | Qwen3-4B/8B、8×A800；PyTorch tree attention 与快速 AR/DFlash kernel 条件不同 | [分册](papers/2606.01813-caddtree.md) |
| **TLAR** | 2026 | 检索式候选来源 | 当前生成历史 + SmallDraft | 免训练控制器 | 匹配后缀并入 target 验证树 | Qwen B=1/32 +8.3%/+7.6%；Mistral +4.1%/+3.5% | 单张 B200、1024 输出 token、代码任务；Qwen 512-token 输出略慢 | [分册](papers/2610.07350-tlar.md) |
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
| Qwen3-4B、T=0、batch=1、RTX 6000 Ada、GSM8K | DARTree τ=12.97；9.73× vs local AR | DARTree Table 1 |
| Qwen3-8B、T=0、H800、K=7、SWE-Bench | DLite τ=3.19；2.74× vs local AR；DSpark 1.60× | DLite Table 3 |
| Qwen3/InternLM2.5、2×A800 PCIe、8 并发、CPU KV offload | SpecStream vs TriForce 1.41×/1.32×；vs SD+Offload 1.44×/1.62× | SpecStream §5.2.2 |

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

1. **T>0 动态树塌缩**（EAGLE-2/3；RheoSampling 给出特定构造，是否启用需查具体配置）。
2. **top-K 的接受率上限**：即使 q=p，纯 top-K 也到不了 100%（缺随机 token）。
3. **草稿质量上限**：独立 draft 的容量差（100–1000×）；Medusa 头无前缀依赖；EAGLE-1/2 的特征约束限制数据 scaling。
4. **有界风险不是无损**：Medusa typical acceptance、ARC-Decode、CDSL。
5. **宽松验证的任务风险不只看准确率**：SecureSD 在所测设置中发现 jailbreak 和 prompt-injection PRR 早于 HumanEval/GSM8K 退化；详见 [SecureSD 精读](papers/2610.08678-secure-sd.md)。
5. **树参数不可移植**：EAGLE-2 的 60/6 与 RheoSampling 的 60/8 不可混用。

### 6.2 系统边界

1. **高 batch + 短序列**：验证成本主导，可能负收益。
2. **长序列显存墙**：KV 随 batch×序列增长；batch 上不去。
3. **draft 上下文失配**：超出训练长度后接受率崩塌；`draft_context_window` 在本轮 vLLM 快照未合入。
4. **静态配置盲区**：不存在适配所有并发度的 `num_speculative_tokens`。
5. **硬件映射**：GPU 与 TPU 的收益不可互推。
6. **量纲混用**：µJ/token 与 tokens/s 不可排榜。

### 6.3 证据边界

1. **未独立复现**：所有论文分册数字均为论文/官方自报；RheoSampling 无公开代码。
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
- **影响**：这为“T>0 下按 q 建树 + one-hot 验证导致接受率下降”提供了实现层证据；也说明“无损≠高效”——one-hot 提议仍可无损，其接受率为 p(候选)，是否更低须按实际分布比较。

**证据等级**：`[精读原文]`（代码级，仓库 @ commit + 文件:行）。

### 8.2 SGLang #10308 后续 PR 是否合入

**结论（准确表述）**：

1. issue `sgl-project/sglang#10308` **真实存在**：标题 *[Feature] Speculative sampling supports passing the predicted probability of the draft model and sample token for verification when **topk=1***；**2025-09-11 开立**（API `created_at=2025-09-11T08:20:37Z`；2025-11-03 指派 `hnyls2002`，为另一里程碑）；**2026-01-03 关闭（API `state_reason=completed`，`closed_by=github-actions[bot]`）**；页面 timeline **无 linked PR/commit，无法确证由哪个变更关闭**。
2. **能力已在主线**（`sgl-project/sglang` @ `2a08e261`，2026-10-16）：
   - `eagle_worker_v2.py:178–180`：开启 `speculative_use_rejection_sampling` 时 `assert self.topk == 1`；
   - `eagle_worker_v2.py:727–733`：非 greedy 且开启拒绝采样 → 构造 `draft_probs`；
   - `eagle_info.py:35`/`:162`：`EagleVerifyInput` / `EagleDraftInput` 均有 `draft_probs` 字段；
   - `eagle_utils.py:947`：选 `chain_speculative_sampling_triton`；
   - `eagle_utils.py:1000–1013`：`draft_probs` 缺失/词表不匹配 → **硬报错**；
   - `eagle_utils.py:1032–1038`：`uniform_samples`（1032–1033）、`target_probs`（1034）、`draft_probs`（1035）一起传入 kernel；
   - `eagle_utils.py:951–959`：`use_rejection_sampling=False` 时走 `tree_speculative_sampling_target_only`（tree topk>1 的 target-only 依据）。
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

## 9. 阅读范围与证据状态

本专题汇总 12 篇学术论文（10 个论文分册，EAGLE 分册覆盖三篇）与 5 个固定版本代码快照：vLLM/SGLang 两个框架、DARTree/DLite 两个论文实现，以及 EAGLE 官方参考切面。逐篇版本、选择与排除理由见 [来源清单](sources/MANIFEST.md) 和 [选文记录](sources/CANDIDATES.md)。本轮新增 SecureSD、DARTree、SpecStream、DLite；阅读范围和代码可得性按论文分别注明，其他 legacy 素材未随本次补核升级。没有独立性能复现，所有加速数字仍应按原论文的硬件、batch、温度和序列条件理解。

## 10. 引用时的边界

- 引用加速比：必须带 `(batch, T, 序列长度, 硬件, 树参数)`。
- 引用“无损”：说明是严格分布等价、序列级保证，还是有界风险（定义见 [验证专题 §6](topics/verification-acceptance.md#6-无损需要区分保证与经验)）。
- 引用 EAGLE-3：6.5× 是论文上限，1.38× 是 batch=64 的吞吐，2.36× 是 batch=1 的吞吐。
- 引用 RheoSampling：2.93× 是相对自回归，不是相对 EAGLE-3。
- 引用 SecureSD：PRR 是 draft-to-target 指标差距的归一化保留率；`ΔPRR` 不是攻击成功率百分点。
- 引用 DARTree：9.73× 是 Qwen3-4B/T=0/GSM8K/batch=1/RTX 6000 Ada 的结果，不是 7 任务平均。
- 引用 DLite：2.74× 是 Qwen3-8B/SWE-Bench/H800/K=7 相对作者本地 AR；不是跨家族速度承诺。仓库 benchmark 不核对输出 token ID。
- 引用 SpecStream：分别说明 TriForce 与 SD+Offload 的比较；offload 释放显存、提升并发的同时仍承担每轮 PCIe 历史传输。

### 10.1 术语对照

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
| 有界风险 | risk-bounded | 分布偏移受控但非严格等价（见 [验证专题 §6](topics/verification-acceptance.md#6-无损需要区分保证与经验)） |
| 稀疏 KV | sparse KV | 只保留部分 KV 做 draft |
| 临界序列长度 | critical/inflection sequence length | 投机收益随 batch 反转的分界 |
| 逐位置接受率 | per-position acceptance rate | 第 j 个草稿位置的历史接受率 |

---

## 附录 A：历史素材层（11 篇）的定位（legacy 素材，未按新标准校验）

| 素材文档 | 保留原因 | 与新结构的关系 |
| :-- | :-- | :-- |
| [`speculative-classical-and-self.md`](legacy/speculative-classical-and-self.md) | 经典/自投机的时间线 | 被 `papers/` 1–3 覆盖，保留作素材 |
| [`speculative-eagle-series.md`](legacy/speculative-eagle-series.md) | EAGLE 细节（含一处错误 ID） | 以 `papers/2401.15077-eagle-series.md` 为准 |
| [`speculative-stochastic-verification.md`](legacy/speculative-stochastic-verification.md) | T>0 的首轮分析 | 被 `topics/verification-acceptance.md` + RheoSampling 分册升级 |
| [`speculative-block-diffusion.md`](legacy/speculative-block-diffusion.md) | 块扩散/检索式线索 | 谱系 IV 的素材；本轮未设分册 |
| [`speculative-cascade-heterogeneous.md`](legacy/speculative-cascade-heterogeneous.md) | 级联/异构 | 系统条件的补充素材 |
| [`speculative-draft-training-2026.md`](legacy/speculative-draft-training-2026.md) | 训练目标新法 | 与 EAGLE-3/Medusa 训练章节交叉 |
| [`speculative-training-optimization.md`](legacy/speculative-training-optimization.md) | 训练目标优化 | 同上 |
| [`speculative-edge-cloud-hardware.md`](legacy/speculative-edge-cloud-hardware.md) | 端侧/硬件 | 系统条件补充 |
| [`speculative-domain-language.md`](legacy/speculative-domain-language.md) | 领域/语种 | 检索式/结构化输出的补充 |
| [`speculative-multimodal.md`](legacy/speculative-multimodal.md) | 多模态 | 本轮未覆盖的方向 |
| [`speculative-systems-and-frameworks.md`](legacy/speculative-systems-and-frameworks.md) | 系统/框架 | 被 vLLM/SGLang 分册 + topic 3 升级 |

---

## 来源

- 论文（均经 arXiv 元数据逐条核验）：EAGLE 2401.15077v3；EAGLE-2 2406.16858v2；EAGLE-3 2503.01840v3；Medusa 2401.10774v3；Lookahead 2402.02057v1；SpecInfer 2305.09781v4；MagicDec 2408.11049v5；DARTree 2608.13524v1；SpecStream 2609.33184v1；RheoSampling 2609.21827v1；SecureSD 2610.08678v1；DLite 2610.23787v1。
- 代码：`SafeAILab/EAGLE` @ `cb7e0841`；`VILA-Lab/DARTree` @ `5bb3240e`；`SJTU-DAI-Sys/DLite` @ `e0aa3d55`；`vllm-project/vllm` @ `2b85d9cb`；`sgl-project/sglang` @ `2a08e261`。SpecStream 未找到作者代码链接。
- 清单：[sources/MANIFEST.md](sources/MANIFEST.md)、[sources/CANDIDATES.md](sources/CANDIDATES.md)。
