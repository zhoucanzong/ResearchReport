# 投机解码（Speculative Decoding）技术深度调研报告

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、技术博客、开源项目和第三方分析整理生成。部分 2025-2026 年信息可能未经同行评审，建议读者直接查阅原始论文验证。arXiv 预印本论文中的加速比数据受测试条件（模型规模、硬件、任务类型）影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮更新；上一版 2026 年 6 月）
> **覆盖范围**：2023 年 Leviathan/Chen 同期独立提出 draft-then-verify 范式，至 2026 H2 随机采样正确性、级联/异构草稿、端侧与硬件的完整技术谱系
> **本轮更新要点**：新增「技术脉络时间线（2023 → 2026H2）」「指标口径与可比性」两节；把"当前技术瓶颈与优化方向"更新为随机采样正确性 / 草稿质量 / 系统协同 / 端侧约束四条；新增 5 份子报告。**注意：本轮只做"重排"，未按 IEEE 2026 综述把本报告整体重构为"系统协同设计"框架。**

---

## 一、概述与执行摘要

**投机解码（Speculative Decoding）** 是自回归（Autoregressive, AR）大语言模型推理加速领域最具影响力的无损加速范式之一。其核心思想可概括为 **Draft-then-Verify**：用一个轻量级的"草案模型"（Drafter / Draft Model）快速并行生成候选 token 序列，再由目标模型（Target / Verifier）通过单次前向传播验证并修正，从而在保持输出分布与标准自回归解码完全一致的前提下，显著降低 wall-clock 时间。

### 1.1 核心数学原理

投机解码的数学基础是 **修改的接受-拒绝采样（Modified Rejection Sampling）**。设目标模型分布为 $p(x)$，草案模型分布为 $q(x)$，对于每个候选位置 $i$：

1. 从 $q(x_i)$ 采样候选 token $x_i$
2. 计算接受概率 $\alpha_i = \min\left(1, \frac{p(x_i)}{q(x_i)}\right)$
3. 以概率 $\alpha_i$ 接受该 token；若拒绝，则从调整后的分布 $p'(x) \propto \max(0, p(x) - q(x))$ 重新采样

该过程保证最终输出严格服从 $p(x)$，实现**无损加速**。

**加速比公式**：

$$\text{Speedup} = \frac{\tau}{1 + \tau_{\text{draft}} / \tau_{\text{verify}}}$$

其中 $\tau$ 为平均接受长度（accepted tokens per verification），$\tau_{\text{draft}}$ 和 $\tau_{\text{verify}}$ 分别为草案模型和目标模型的单次前向耗时。当草案模型足够快且接受率足够高时，加速比可突破 2-6×。

### 1.2 与标准自回归解码的效率对比

| 维度 | 标准 AR 解码 | 投机解码 | 说明 |
|------|------------|---------|------|
| **输出分布** | 精确 $p(x)$ | 精确 $p(x)$（无损） | 接受-拒绝采样保证等价性 |
| **并行度** | 单 token / forward | 多 token / forward | 验证步可并行处理候选序列 |
| **内存开销** | 仅 target KV Cache | target + draft KV Cache | 草案模型额外显存占用 |
| **适用场景** | 通用 | 草案-目标分布对齐时最优 | 低熵/模板化文本加速更显著 |
| **典型加速比** | 1×（基线） | 2-6× | 取决于接受率与草案速度 |
| **训练需求** | 无 | 部分方法需训练 draft 模型 | 自投机/检索式可免训练 |

### 1.3 2023-2026 技术演进主线

投机解码三年间经历了从"外挂小模型"到"内生自投机"、从"token 级自回归"到"特征级/块级并行"的范式跃迁：

```
2023 经典独立模型 ──→ 2024 自投机多头/顺序头 ──→ 2024-2025 特征级 EAGLE 系列
     │                      │                           │
     ▼                      ▼                           ▼
Leviathan/Chen         Medusa / Hydra / Lookahead    EAGLE-1/2/3 (工业标准)
(独立小模型 draft)     (目标模型自身生成 draft)       (特征级自回归，单层 Transformer)
     │                      │                           │
     └──────────────────────┴───────────────────────────┘
                              │
                              ▼
                    2025-2026 新兴方向
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    块扩散 (DFlash)   多模态投机解码    训练目标优化
    (并行块生成)        (VLM/视频/VLA)   (LK Losses/PPOW/ConFu)
```

---

## 二、技术脉络时间线（2023 → 2026H2）

> 本节为本轮新增。完整文献与证据等级见各子报告。

### 2.1 阶段主线

| 阶段 | 主线 | 代表工作 | 对应子报告 |
|---|---|---|---|
| **2023** | 经典 draft-then-verify、并行采样验证、自投机雏形 | Leviathan et al.；Chen et al. | [classical §3.1](speculative-classical-and-self.md) |
| **2023-2024** | 检索式 / 词表式草稿（低成本、免训练） | Prompt Lookup、REST；2026 年延伸出**非拉丁语系字典法** | [block-diffusion §3.5](speculative-block-diffusion.md) · [domain §2](speculative-domain-language.md) |
| **2024** | 多头草稿与冻结式结构；动态草稿树登场 | Medusa、Hydra、Lookahead、LayerSkip；**EAGLE-1/-2**（动态草稿树） | [classical §3.2](speculative-classical-and-self.md) · [eagle §3.3](speculative-eagle-series.md) |
| **2024-2025** | EAGLE 工业化；草稿侧训练目标与蒸馏 | EAGLE-3；**AdaSPEC**（选择性知识蒸馏，NeurIPS 2025） | [eagle §3.3.3](speculative-eagle-series.md) · [draft-training §2](speculative-draft-training-2026.md) |
| **2025** | 验证侧理论化；层跳过与在线自投机 | **Traversal Verification**（NeurIPS 2025）；**SWIFT**（ICLR 2025）；**CLaSp**（ACL 2025） | [stochastic §3.2](speculative-stochastic-verification.md) · [classical §3.2.5](speculative-classical-and-self.md) |
| **2025-2026** | 走向训练闭环与多模态 | **Adaptive Drafter / TLT**（推理 RL 训练长尾，ASPLOS 2026）；多模态投机解码 | [draft-training §4](speculative-draft-training-2026.md) · [multimodal](speculative-multimodal.md) |
| **2026H1** | 块扩散式草稿与预算感知 | **DFlash**（ICML 2026）、**DSpark**；**BASTION**（预算感知 + 树状块扩散，arXiv 2605.29727）；成本感知建树（ICLR 2026） | [block-diffusion §3.4](speculative-block-diffusion.md) · [cascade §4](speculative-cascade-heterogeneous.md) |
| **2026H2** | **随机采样下的动态树正确性**、风险界定接受、级联/异构、端云与硬件 | **RheoSampling**（arXiv 2609.21827）、**ARC-Decode**（ICML 2026）、**HCSpec / HeteroSpec**（ACL 2026）、**FlexSpec**（端云协同）、端侧 MoE 自投机（ACM Web 2026）、**SMoLPU**（ISSCC 2026）、Google TPU 扩散式 3.13× | [stochastic](speculative-stochastic-verification.md) · [cascade](speculative-cascade-heterogeneous.md) · [edge](speculative-edge-cloud-hardware.md) |
| **2026** | 系统协同设计综述（**本轮未采纳为重构框架**） | IEEE《From Draft-Then-Verify to Systems Co-Design》 | —（见 §2.3） |

**一句话脉络**：从"草稿-验证两段式"→"结构化的树 / 多头草稿"→"草稿模型训练与蒸馏"→"验证理论与正确性（随机采样）"→"扩散 / 块式草稿 + 预算与硬件协同"。

### 2.2 本轮的转折点判断

> **2026H2 的转折点是：随机解码（T>0）下"动态树更优"的既有结论被证伪或需要限定条件。**

四条依据（详细论证见对应子报告）：

1. **T>0 下动态树塌缩为 one-hot**，接受率显著下降，且这是**机制性**的——建树与验证共用了同一个 draft 概率分布。 **[精读原文，见 [stochastic §3.1](speculative-stochastic-verification.md)]**
2. **朴素的"改成采样"修法会破坏无损性**：token 能否在树中存活取决于它自身的取值，对"存活"取条件会扭曲条件分布。 **[精读原文]**
3. **正确解是解耦**：RheoSampling 用"建树 proxy 概率 + 验证真实采样概率"的双身份设计，并给出严格无损性证明。 **[精读原文]**
4. **"草稿 token 越多越好"在系统侧也被推翻**：batch=1（memory-bound）与高并发（compute-bound）下结论相反，不存在适配所有并发度的静态 `num_speculative_tokens`。 **[精读原文，见 [systems §①](speculative-systems-and-frameworks.md)]**

### 2.3 关于 IEEE 2026 综述（原方案 C 未采纳）

检索到 IEEE 2026 综述《From Draft-Then-Verify to Systems Co-Design: A Survey of Speculative Decoding for Autoregressive Large Language Models》（核验页见 §八）。

按任务书口径，**本轮只做"重排"，不按该综述把 report.md 整体重构为"系统协同设计"框架**。该综述在 §八 中作为参考来源列出，"系统协同"作为 §五 的四条瓶颈之一被引用。

---

## 三、方法级技术演进时间线（v1 保留）

> 本节为 v1 的细粒度方法级时间线；2023 → 2026H2 的概览脉络见 §二，两者互补。

| 阶段 | 代表方法 | 年份 | 核心机制 | 训练需求 | 典型加速比 | 信息可靠性 |
|------|---------|------|---------|---------|-----------|-----------|
| **经典独立模型** | Leviathan et al. / Chen et al. | 2023 | 独立小模型 draft + target 验证 | 无需联合训练 | 2-3× | 高（ICML/NeurIPS 论文） |
| **自投机：并行头** | Medusa | 2024 | 多头并行预测 + 树状注意力 | 需微调 | 2.5-3.5× | 高（ICML 2024） |
| **自投机：顺序头** | Hydra | 2024 | 顺序依赖草案头 | 需微调 | 2.8-3.8× | 高（NeurIPS 2024） |
| **自投机：免训练** | Lookahead | 2024 | Jacobi 迭代 + n-gram 池 | 免训练 | 1.5-2.5× | 高（NeurIPS 2024） |
| **自投机：层跳过** | SWIFT / CLaSp | 2025 | 在线自适应跳过中间层作 draft | 免训练 | 1.3-1.7× | 高（ICLR/ACL 2025） |
| **特征级：单层** | EAGLE-1 | 2024 | 特征自回归，单层 Transformer | 需训练 | 3-4× | 高（ICLR 2024） |
| **特征级：动态树** | EAGLE-2 | 2024 | 动态草案树，上下文感知分支 | 需训练 | 3.5-4.5×（**T=0**）；摘要称 EAGLE-3 相对其约 **1.4×** 提升 | 高（EMNLP 2024） |
| **特征级：多层融合** | EAGLE-3 | 2025 | 多层特征融合 + TTT，工业标准 | 需训练 | 摘要 **up to 6.5×**；特定设定 **4.79×**；SGLang batch=64 吞吐 **1.38×**（**T=0**） | 高（NeurIPS 2025） |
| **块扩散** | DFlash / DSpark / BASTION | 2026 | 块 / 树状块扩散并行 draft | 需训练 | DFlash **>6×**；BASTION 最高 6.61× | 中（ICML 2026 / arXiv 预印本） |
| **块扩散（TPU）** | DFlash on TPU v5p | 2026 | 双缓存 + 流水线重映射 | 需训练 | **3.13×**（峰值近 6×） | 中（官方工程博客） |
| **检索式** | REST / PLD | 2023-24 | 基于检索的候选生成 | 零训练成本 | 1.5-2.5× | 高（NAACL/独立工作） |
| **字典式（低资源语种）** | DictSpec | 2026 | 静态 n-gram 查找表，与 prompt-local 混合 | **零训练** | 验证步最多 1.65×；混合真实服务最高 1.76× | 中（ACL 2026） |

> **加速比说明（本轮重要修订）**：
> 1. 上表典型加速比为**论文报告值**，实际部署受模型规模（7B vs 70B）、硬件（A100 vs H100 vs GB200 vs TPU v5p）、任务类型（代码/数学/开放对话）、**batch / 并发度**影响显著。例如 EAGLE-3 在 LLaMA-3.3-70B 上报告的 4.79× 是**该设定下的表值**；其**摘要口径为 up to 6.5×**（chat + reasoning 模型、五任务的上限），另有 **SGLang batch=64 下 1.38× 吞吐提升**——**6.5× = 摘要上限，4.79× = 特定设定值，两者不矛盾**；在小模型或高熵任务上还可能降至 2-3×。三个数字口径不同（上限 / 特定模型设定 / 特定框架与 batch 吞吐），**不可混用**。
> 2. **EAGLE-2/EAGLE-3 的数字是 greedy（T=0）设定下的报告值**。在 T>0 随机采样下，动态树会塌缩为 one-hot、接受率显著下降——详见 [speculative-stochastic-verification.md](speculative-stochastic-verification.md) 与 [speculative-eagle-series.md](speculative-eagle-series.md) §3.3.5。
> 3. **块扩散方法的收益强依赖 batch**：batch=1（memory-bound）时 draft token 接近免费，高并发（compute-bound）时与真实 token 争夺算力，**结论相反**。详见 [speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md) §①。
> 4. **不同硬件上的同一算法不可直接比较**：DFlash 在 GPU 与 TPU 上的数字来自不同优化路径（见 [speculative-edge-cloud-hardware.md](speculative-edge-cloud-hardware.md) §5）。

---

## 四、指标口径与可比性（本轮新增，必读）

> 完整的字段定义与对账关系见 [speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md) §②。

### 4.1 acceptance rate 与 mean accepted length 必须成对报告

据 vLLM 官方 *Per-Request Acceptance Metrics* 文档（一手来源，本轮已精读）：

| 指标 | 精确分母 | 含义 |
|---|---|---|
| `mean_acceptance_length` | **验证步数**（`num_spec_steps`） | 每次验证步平均产出 token 数，**含必得的 bonus token**，范围 $[1, k+1]$ |
| `draft_acceptance_rate` | **提议草稿 token 数**（`num_draft_tokens`） | 被提议草稿中被接受的比例 |

**两者分母不同，会反向移动**：加深草稿树通常**降低** acceptance rate（多提议了低命中率的 token）却**提高** mean accepted length（一旦命中就一次吃更多）。

> **工程硬要求**：单独报一个数字无法判断系统是变快还是变慢。**必须成对给出**，并同时声明测试的（a）并发度 / batch size，（b）temperature，（c）是否启用结构化输出约束。

### 4.2 三个会改变指标口径的因素

| 因素 | 影响 | 处置 |
|---|---|---|
| **temperature（T=0 vs T>0）** | T>0 下动态树塌缩，接受率显著下降；T 越低越接近确定性 | 必须声明 T；T>0 的结论不可外推到 T=0，反之亦然（见 [stochastic](speculative-stochastic-verification.md)） |
| **batch / 并发度** | batch=1 与高并发下"是否划算"结论相反 | 必须声明并发度；不存在适配所有并发度的静态 `num_speculative_tokens`（见 [systems §①](speculative-systems-and-frameworks.md)） |
| **结构化输出约束** | `num_draft_tokens` **已扣除被约束作废的草稿** → acceptance rate 分母变小 | 必须声明约束类型；有/无约束的实验**不可直接对比**（见 [domain §3.3](speculative-domain-language.md)） |

### 4.3 "无损"不是一个含义统一的词

本轮新增子报告识别出三类**不同等级**的输出分布保证，混用会导致错误结论：

| 等级 | 含义 | 代表方法 | 可否宣称"严格无损" |
|---|---|---|---|
| **严格分布等价** | 输出分布**严格等于** target 分布 $p$ | 经典 draft-then-verify；RheoSampling（Theorem 1）；Traversal Verification；HeteroSpec | ✅ 可以 |
| **序列级等价** | 以**整条序列**的概率而非逐 token 概率判接受 | Traversal Verification 的核心视角 | ✅ 可以（有其自身定义域） |
| **有界风险** | 接受放宽到"分布偏移受控"，**不是**严格等价 | ARC-Decode（JS 散度上界）；CDSL（任务奖励验证） | ❌ **不可**，须写"有界风险 / 质量近乎不变" |

> **推论**：把 ARC-Decode 的"相对 EAGLE-3 最高 1.6×"与 RheoSampling 的"相对自回归 2.93×"放在同一句话里比较是**不成立的**——量纲、基准与保证等级都不同。

### 4.4 跨论文比较的三条禁令

1. **禁止跨硬件比较**：GPU 与 TPU 上的同一算法不可直接比（工程映射不同）。
2. **禁止跨量纲比较**：能效（µJ/token，如 SMoLPU）与吞吐（token/s）不是同一量纲，排成"谁更快"的榜单是方法论错误。
3. **禁止把摘要级数字当已验证事实**：本专题所有子报告均逐条标注证据等级（精读原文 / 摘要级 / 二手 / 受限核验），跨论文引用时须保留该标注。

---

## 五、当前技术瓶颈与优化方向（本轮更新为四条）

> 本轮按任务书口径把 v1 的 6 条瓶颈重排为 **4 条**：随机采样正确性 / 草稿质量 / 系统协同 / 端侧约束。v1 中"与量化兼容性""扩散语言模型竞争"两条并入相应条目或保留在子报告中。

### 5.1 随机采样正确性（本轮新增，最高优先级）

**瓶颈**：投机解码的理论保证建立在"lossless"之上，但**"lossless"在 T>0 下对动态树并不自动成立**。

- 动态树（EAGLE-2/3）的建树与剪枝按 draft 概率 $q$ 排序，而接受判据是 $\min(1, p/q)$ 的**比值**。T>0 时 $q$ 不再是接受率的可靠指标 → 树塌缩为近似 one-hot → 接受率下降。
- 更严重的是：**朴素的"改为采样"修法会破坏无损性**（token 存活依赖自身取值 → 条件分布被扭曲）。
- 因此需要区分三种保证等级：严格分布等价 / 序列级等价 / **有界风险**（见 §4.3）。

**突破方向**：

| 方向 | 代表工作 | 关键结果 |
|---|---|---|
| **建树 / 验证解耦** | **RheoSampling**（arXiv 2609.21827） | 双概率身份（proxy 建树 + 真实采样概率验证）；Theorem 1 证明严格无损；Llama-3.1-8B 接受长度 5.04→**5.25**，加速 2.84×→**2.93×** |
| **换验证的遍历与粒度** | **Traversal Verification**（NeurIPS 2025） | 叶到根遍历 + 序列级接受判据；证明无损且单链最优；平均接受长度 **+2.2%~5.7%** |
| **放宽为有界风险** | **ARC-Decode**（ICML 2026） | JS 散度上界 + Local Tolerance Score 软接受；相对 EAGLE-3 最高 **1.6×**（**摘要级**） |
| **指标口径修正** | vLLM 官方文档 | acceptance rate 与 mean accepted length **必须成对报告** |

→ 详见 [speculative-stochastic-verification.md](speculative-stochastic-verification.md)；对 EAGLE 的限定见 [speculative-eagle-series.md](speculative-eagle-series.md) §3.3.5。

### 5.2 草稿质量（含训练目标、表征、时机三个子问题）

**瓶颈**：高质量 drafter 获取困难；且即使获得了，**接受率也不等于"学得像 target"**。

- **训练目标错位**：经典 KD 最小化所有 token 上的 KL 散度，而 SD 的目标是最大化接受率。
- **表征缺陷**：**Attention Drift**——drafter 隐藏状态幅值随链深单调增长，注意力从 prompt 漂移到自身近期输出；该现象在 **EAGLE-3 drafter 与 MTP head 上都存在**。
- **训练时机**：RL 训练中 target 持续演化，离线训一次的 drafter 会对不上。

**突破方向**：

| 方向 | 代表工作 | 关键结果 |
|---|---|---|
| **选择性蒸馏** | **AdaSPEC**（NeurIPS 2025） | 用 reference model 过滤难拟合 token，接受率最高 **+15%**（优于 DistillSpec） |
| **表征归一化** | **Attention Drift**（arXiv 2605.09992） | Post-norm + per-hidden-state RMSNorm；接受长度最高 **2×**（模板扰动）/1.18×（长上下文）/1.10×（7 benchmark） |
| **在线持续训练** | **Adaptive Drafter / TLT**（ASPLOS 2026） | 利用长尾生成期间的空闲 GPU 持续训 drafter；RL 训练 **>1.7×**，draft 模型为免费副产品 |
| **表述层修正旧路线** | **SWIFT**（ICLR 2025）/ **CLaSp**（ACL 2025） | 免训练在线层跳过；**1.3×~1.7×**，保持原始分布 |
| **训练框架工程化** | **SpecForge**（ICML 2026, arXiv 2603.18567） | target-draft 解耦 + 混合并行；EAGLE-3 训练最高 **9.9× 加速**，发布 SpecBundle |

→ 详见 [speculative-draft-training-2026.md](speculative-draft-training-2026.md)、[speculative-training-optimization.md](speculative-training-optimization.md)、[speculative-classical-and-self.md](speculative-classical-and-self.md) §3.2.5。

### 5.3 系统协同（本轮从"批量推理效率"扩展而来）

**瓶颈**：**投机解码的收益随负载恶化**——这是结构性的，不是调参问题。

- batch=1 时 GPU 是 **memory-bound**，额外 draft token 接近免费；
- batch=256 时 draft token **与真实 token 争夺同一份算力**，每个被拒 token 都是浪费的算力，够多时**吞吐下降**；
- **不存在适配所有并发度的静态 `num_speculative_tokens`**；
- 成本感知建树（CAST）实测 **EAGLE-2 在 batch=8 的 CNN/DM 上降到 0.84×（比原始自回归还慢）**。

**突破方向**：

| 方向 | 代表工作 | 关键结果 |
|---|---|---|
| **按置信度分配验证预算** | vLLM **adaptive verification**；**DSpark**（SGLang 集成） | 逐 (request, position) 打分准入 + 启动时 profiled 成本模型；**一套配置覆盖整个负载区间**；DSpark 半自回归块草稿 + 变长验证 |
| **预算感知的树扩张** | **BASTION**（arXiv 2605.29727） | 接受代理 + 在线延迟估计 + best-first 扩张；最高 **6.61×**，优于 SOTA 块扩散基线 39% |
| **成本感知建树** | **CAST**（ICLR 2026） | 把 GPU 型号与 batch 纳入效用最大化；**最高 5.2×** |
| **分层 / 级联草稿** | **HCSpec**（ACL 2026）/ **HeteroSpec**（ACL 2026） | HCSpec 两级水平级联，相对 EAGLE-3 **+15~30%**；HeteroSpec 按不确定性分配验证算力，平均 **4.24×** 且保持精确分布 |
| **上下文窗口界限** | vLLM PR #61261 | `draft_context_window` 把"超出训练长度后接受率崩塌"变成可配置项 |

→ 详见 [speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md) §①、[speculative-cascade-heterogeneous.md](speculative-cascade-heterogeneous.md)、[speculative-block-diffusion.md](speculative-block-diffusion.md) §3.4。

### 5.4 端侧约束（本轮新增）

**瓶颈**：端侧的**第一约束是内存带宽与权重搬运，而非草稿质量**；且**投机解码与 MoE 在端侧存在结构性不兼容**——验证被拒 token 时仍要加载专家，批量验证会激活**专家并集**，把稀疏计算推回密集内存访问。

**突破方向**：

| 方向 | 代表工作 | 关键结果 |
|---|---|---|
| **用已有权重的子集作 draft** | **SS-MoE**（ACM Web 2026） | 路由专家子集作 draft + 内存作专家缓存 + 置信度自适应接受；端侧**不增加额外权重内存** |
| **冻结草稿兼容演进 target** | **FlexSpec**（arXiv 2601.00644 / IEEE TMC） | 共享骨干架构 + 信道感知自适应草稿长度；免端侧重训与反复下载 |
| **专用硅** | **SMoLPU**（ISSCC 2026） | MoE 投机解码专用 LPU；**2.3×/4.2×** 能效、**3.3×** 延迟、每参数能量 **−43.5%**（**受限核验**） |
| **硬件映射** | Google **TPU v5p + DFlash** | 双缓存 + 流水线重映射；平均 **3.13×**、峰值近 **6×** tokens/s |
| **视觉/多模态端侧** | 多模态投机解码 | 见 [speculative-multimodal.md](speculative-multimodal.md) §4.5 |

→ 详见 [speculative-edge-cloud-hardware.md](speculative-edge-cloud-hardware.md)。

### 5.5 v1 其他条目的去向

| v1 条目 | 本轮处置 |
|---|---|
| 5.1 草案模型训练难题 | → 并入 §5.2 草稿质量 |
| 5.2 接受率优化困难 | → 并入 §5.2 草稿质量 |
| 5.3 与量化兼容性（QSpec / HierSpec） | → 保留在 [speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md) 系统表；**其原始链接为未确证占位符** |
| 5.4 批量推理效率 | → **扩展为 §5.3 系统协同** |
| 5.5 扩散语言模型的竞争 | → 保留在 [speculative-block-diffusion.md](speculative-block-diffusion.md) §5.5（并已更新 I-DLM / NLD 的可核验链接） |

---

## 六、框架与工具生态

| 框架/工具 | 支持情况 | 备注 |
|----------|---------|------|
| **vLLM** | 原生 EAGLE-1 / EAGLE-3 支持（v0.8.5+） | 最广泛部署的开源推理框架 |
| **SGLang** | SpecForge 训练框架集成 | 高性能推理 runtime |
| **TensorRT-LLM** | NVIDIA 推理优化，支持投机解码 | 闭源，针对 NVIDIA 硬件优化 |
| **SpecBundle** | 生产级 EAGLE-3 草案模型集合 | SpecForge 发布，覆盖主流模型 |
| **Red Hat AI** | 发布 Qwen3-8B-speculator.eagle3 | 企业级部署方案 |

**生态趋势**：
- vLLM 的 EAGLE-3 支持使投机解码从研究工具变为生产默认选项
- SpecBundle 降低 draft 模型获取门槛，类似 HuggingFace 模型库的"draft 模型专区"
- Red Hat AI 等厂商开始发布官方 speculator 模型，标志投机解码进入商业化阶段

---

## 七、QwenAccel-Train 框架设计

QwenAccel-Train 是一个面向投机解码的模块化训练框架，包含 **10 个可开关创新模块**：

| 模块类别 | 模块名称 | 功能描述 |
|---------|---------|---------|
| **自投机 draft** | TiDAR | 自投机解码，目标模型自身生成 draft |
| **高效 draft 架构** | MambaDraft | 线性注意力 draft 模型，O(1) 内存复杂度 |
| **KV 缓存优化** | AnchorKV | 复用 target 模型 KV 缓存，减少重复计算 |
| **条件机制** | MultiScaleConditioner | 多尺度条件注入，融合不同层级的 target 特征 |
| **条件机制** | CrossAttnConditioner | 交叉注意力条件，增强 draft-target 交互 |
| **动态调度** | AdaptiveBlockSizer | 自适应块大小调整，根据上下文熵动态选择 draft 长度 |
| **验证优化** | TreeVerifyEngine | 树状验证引擎，优化树状注意力的 GPU 利用率 |
| **训练策略** | OPDTrainer | On-Policy Distillation，在线策略蒸馏 |
| **训练策略** | ExposureBiasReducer | 曝光偏差削减，缓解训练-推理分布偏移 |
| **架构适配** | MoEAwareDraft | MoE 感知 draft，针对稀疏激活模型优化 |
| **系统协调** | PDCoordinator | Draft-Verify 流水线协调器，优化异构设备调度 |

**框架设计哲学**：
- **模块化**：每个组件可独立开关，支持从经典 EAGLE 到 DFlash 的多种变体
- **硬件感知**：TreeVerifyEngine 和 PDCoordinator 针对实际 GPU/CPU 异构环境优化
- **训练-推理一致性**：OPDTrainer 和 ExposureBiasReducer 直接针对投机解码的训练-推理不一致问题

---

## 子报告导航索引

本报告按技术方向拆分为以下 **12 份**子报告，供深入阅读：

| # | 子报告 | 一句话摘要 | 文件 |
|---|--------|-----------|------|
| 1 | **经典方法与自投机** | 从 2023 年 Leviathan/Chen 的独立小模型 draft 到 2024-2025 年 Medusa、Hydra、Lookahead、LayerSkip、**SWIFT、CLaSp** 的自投机路线演进 | [speculative-classical-and-self.md](speculative-classical-and-self.md) |
| 2 | **EAGLE 系列** | 特征级自回归 draft 从 EAGLE-1 到 EAGLE-3 的工业标准形成，以及 SpecForge 训练框架；**含 T>0 下动态树塌缩的限定条件** | [speculative-eagle-series.md](speculative-eagle-series.md) |
| 3 | **随机采样与验证正确性** ⭐本轮新增 | T>0 下动态树 one-hot 塌缩、建树与验证解耦、无损性边界、三种"无损"口径的区分 | [speculative-stochastic-verification.md](speculative-stochastic-verification.md) |
| 4 | **块扩散与检索式方法** | DFlash / **DSpark** / **BASTION** 块（树状）扩散、成本感知建树、TPU 扩散式投机、REST/PLD 检索方法与扩散语言模型竞争 | [speculative-block-diffusion.md](speculative-block-diffusion.md) |
| 5 | **级联与异构草稿** ⭐本轮新增 | HCSpec 两级水平级联、HeteroSpec 按验证异构性分配算力；与 EAGLE 动态树、CAST 成本感知的对照 | [speculative-cascade-heterogeneous.md](speculative-cascade-heterogeneous.md) |
| 6 | **草稿模型训练新法（2026）** ⭐本轮新增 | AdaSPEC 选择性蒸馏、Attention Drift 表征修补、Adaptive Drafter / TLT 在线训练 | [speculative-draft-training-2026.md](speculative-draft-training-2026.md) |
| 7 | **训练目标优化** | LK Losses、PPOW、ConFu 等直接优化接受率的新型训练目标与在线适应方法（**部分链接为未确证占位符，已标注**） | [speculative-training-optimization.md](speculative-training-optimization.md) |
| 8 | **端侧、边缘与硬件** ⭐本轮新增 | FlexSpec 端云协同、SS-MoE 端侧 MoE 自投机、SMoLPU 专用硅、Google TPU 扩散式投机 | [speculative-edge-cloud-hardware.md](speculative-edge-cloud-hardware.md) |
| 9 | **领域与语种特化** ⭐本轮新增 | DictSpec 非拉丁语系字典法、CDSL 受限解码投机、结构化输出下的指标口径 | [speculative-domain-language.md](speculative-domain-language.md) |
| 10 | **多模态投机解码** | VLM、视频 LLM、VLA、语音音频等 2025-2026 新兴多模态方向的投机加速方案；含与端侧章节的交叉引用 | [speculative-multimodal.md](speculative-multimodal.md) |
| 11 | **系统级优化与框架生态** | SpecInfer、Sequoia、Mirror-SD 等系统级优化；**验证预算/上下文窗口调度**；**指标口径**；vLLM、SGLang、llama.cpp 等框架支持 | [speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md) |
| 12 | （本报告） | 上述子报告的导航与主线整合 | [report.md](report.md) |

**推荐阅读路径**：

- **只想看本轮变化** → §二（技术脉络）→ §四（指标口径）→ **子报告 3**（随机采样正确性）→ §五（四条瓶颈）
- **要做工程选型** → §四（指标口径）→ **子报告 11**（系统协同与框架）→ **子报告 8**（端侧）→ **子报告 9**（领域/语种）
- **要做研究** → **子报告 3**（验证理论）→ **子报告 6**（草稿训练）→ **子报告 5**（级联/异构）

---

## 八、参考文献

各方向详细参考文献见上述子报告。以下为分类汇总索引：

| 分类 | 所在子报告 |
|------|-----------|
| 基础方法（Leviathan, Chen） | [speculative-classical-and-self.md](speculative-classical-and-self.md) |
| 自投机方法（Medusa, Hydra, Lookahead, LayerSkip, SWIFT, CLaSp） | [speculative-classical-and-self.md](speculative-classical-and-self.md) |
| EAGLE 系列（EAGLE-1/2/3, SpecForge） | [speculative-eagle-series.md](speculative-eagle-series.md) |
| **随机采样与验证正确性（RheoSampling, Traversal Verification, ARC-Decode）** | [speculative-stochastic-verification.md](speculative-stochastic-verification.md) |
| 块扩散与检索式方法（DFlash, DSpark, BASTION, CAST, REST, PLD, SAM） | [speculative-block-diffusion.md](speculative-block-diffusion.md) |
| **级联与异构草稿（HCSpec, HeteroSpec）** | [speculative-cascade-heterogeneous.md](speculative-cascade-heterogeneous.md) |
| **草稿训练新法（AdaSPEC, Attention Drift, Adaptive Drafter/TLT, SpecForge）** | [speculative-draft-training-2026.md](speculative-draft-training-2026.md) |
| 训练目标优化（LK Losses, PPOW, ConFu, HASS 等，**部分未确证**） | [speculative-training-optimization.md](speculative-training-optimization.md) |
| **端侧与硬件（FlexSpec, SS-MoE, SMoLPU, TPU+DFlash）** | [speculative-edge-cloud-hardware.md](speculative-edge-cloud-hardware.md) |
| **领域与语种（DictSpec, CDSL）** | [speculative-domain-language.md](speculative-domain-language.md) |
| 多模态投机解码（ViSpec, FLASH, SpecVLM, Spec-VLA 等） | [speculative-multimodal.md](speculative-multimodal.md) |
| 系统优化与框架生态（Sequoia, Mirror-SD, TriForce, vLLM, SGLang, llama.cpp） | [speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md) |
| 扩散语言模型竞争/合流（I-DLM, Nemotron-Labs-Diffusion） | [speculative-block-diffusion.md](speculative-block-diffusion.md) |
| 指标口径（vLLM Per-Request Acceptance Metrics / Adaptive Verification） | [speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md) §② |
| 构建"系统协同设计"框架的综述（**本轮未采纳为重构框架**） | [IEEE 2026 Survey](https://ieeexplore.ieee.org/document/11719495)（⚠️ 本环境 IEEE 页面被反爬拦截（HTTP 202 空响应），未能直接核验内容，仅登记标题；同名的 [preprints.org 版本](https://www.preprints.org/manuscript/202608.0746/v1) 亦返回 HTTP 403，**两处均未确证正文**） |

---

> **报告说明**：本报告所有技术细节均来自公开发表的论文、arXiv 预印本、官方技术博客及开源项目文档。2023-2025 年方法的信息可靠性普遍较高（经同行评审）；2026 年方法（DFlash、BASTION、HeiSD、HSD、SAGE、RheoSampling、HCSpec、HeteroSpec 等）多为 arXiv 预印本或当期会议论文，建议读者直接查阅原始论文验证。
>
> **本轮质量说明**：新增的 5 份子报告与改写的 6 份既有子报告均按「结论—证据—来源」组织，并逐条标注**证据等级**（精读原文 / 摘要级 / 二手 / 受限核验）。任务书中被核验为**失效或受限**的链接已在对应子报告中显式列出并处置；v1 遗留的**占位符链接**（实测 HTTP 404 或指向无关论文）已在 `speculative-training-optimization.md`、`speculative-systems-and-frameworks.md`、`speculative-multimodal.md`、`speculative-eagle-series.md`、`speculative-classical-and-self.md` 中逐条标注或更正。
>
> 加速比数据受测试条件显著影响，**跨论文、跨硬件、跨量纲不可直接比较**；报告加速比时须同时给出 acceptance rate 与 mean accepted length，并声明 temperature、并发度与是否启用结构化输出约束。
>
> *数据截至 2026-10-16（上一版：2026-06-06）。*
