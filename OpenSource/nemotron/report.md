---
display_name: Nemotron-Labs 扩散模型
---

# Nemotron-Labs-Diffusion 阅读报告

> **报告日期**: 2026-05-27
> **论文来源**: Yonggan Fu 等 (NVIDIA + Georgia Tech + HKU + MIT), 2026-05-19
> **结构化数据**: [`papers/nemotron-labs-diffusion.json`](papers/nemotron-labs-diffusion.json)
> **详细笔记**: [`notes/structured-reading.md`](notes/structured-reading.md)
> **概念地图**: [`knowledge-graph.md`](knowledge-graph.md)

> **原文复核（2026-10-22）**：按 `researcher deep` 与 `paper-fetcher` 回取 NVIDIA 2026-05-19 v1 PDF，核对训练消融 Table 1–3、准确率/TPF Table 5–6、SOL §4.2 与 Fig.7、硬件 Fig.9；图表页已渲染复核。后补 arXiv 为 [2607.05722](https://arxiv.org/abs/2607.05722)，首次提交2026-07-07，与5月报告分开记；见 [sources/MANIFEST.md](sources/MANIFEST.md)。

---

## 执行摘要

NVIDIA 提出 **Nemotron-Labs-Diffusion (NLD)**，一个在单一权重内同时支持 **AR、Diffusion、Self-Speculation** 三种解码模式的 LLM 家族（3B/8B/14B，含 base/instruct/VLM）。核心做法是在同一模型上联合优化 AR next-token loss 与 block-wise diffusion denoising loss（$\mathcal{L}=\mathcal{L}_{AR}+0.3\mathcal{L}_{diff}$），并采用 dual-stream attention、global loss averaging、two-stage training 等技巧解决方差与训练稳定性问题。

实证上，**NLD-8B 在 10 个主流基准上的 AR 模式平均精度 63.61%，超过 Qwen3-8B (62.75%)**；Table 5（8B instruct、10项任务）Linear Self-Speculation 的TPF为 **5.99**（AR=1），在 GB200 GPU + SGLang + SPEED-Bench 上 wall-clock 比 AR 加速 **3.3×**（kernel 优化后 3.97×），比 Qwen3-8B-Eagle3 在多硬件上加速 **1.8×~2.4×**。

最值得关注的方法学贡献是 **Speed-of-Light (SOL) 分析**——它通过 oracle 估计 该模型与 serial-denoising 参照下的 oracle 经验上限，发现SOL 的 real TPF 比 Linear Self-Speculation 高 **76.5%**（6.02/3.41−1）；反向说 Linear SS 比 SOL 低约 **43.4%**，为社区设定了清晰的优化目标。

论文最深刻的结论：**AR 与 Diffusion 不是竞争而是互补关系**——它们在本文25B-token配置的有限 α 扫描中同时以0.3最优，相互增强（Table 1的累计加AR loss增量为+7.48个百分点；Table 3的配对比较中加diffusion loss令AR平均分+0.14/+0.43个百分点）。

---

## 数字适用范围与失效边界

| 证据 | 设置与问题 | 可以支持 | 不能外推 |
|---|---|---|---|
| Table 1（p.4） | Ministral3-8B起点，25B-token CPT，逐项累加技巧，diffusion mode 6项任务均值 | 给定顺序下全组合54.23→70.28；AR loss最后一步+7.48个百分点 | 单个技巧独立因果收益、从零训练同样有效 |
| Table 2–3（p.5–6） | α有限网格0.1/0.2/0.3/0.5/1.0，base/instruct配对比较 | 本设置α=0.3平均分最好；平均增益可与个别任务下降并存 | 所有模型/数据上0.3最优、所有任务无退化 |
| Table 5（p.11） | 8B instruct，10任务均值，AR / diffusion / Linear SS / Quad SS | 准确率与每次前向的产出权衡 | TPF等于墙钟加速、单项任务都优于基线 |
| §4.2 / Fig.7（p.9–10） | 713条SPEED-Bench、11类、B=32；SOL参考diffusion自己的serial-denoising输出，SS参考AR验证 | 两种参照的实测oracle比较；real TPF 6.02 vs3.41 | 通用理论上界、相同输出分布的无损速度比较 |
| Fig.9 / §6.5（p.14） | 8B、SGLang、SPEED-Bench四类、生成上限1024、并发1；量化/内核分别列示 | 指定硬件和量化条件下吞吐；GB200优化kernel 1015 tok/s | 高并发也有同一倍数、第三方性能复现 |

SOL递归dynamic compaction每block有5000次模拟forward预算（§4.1）；预算耗尽将候选判为不安全。这是昂贵的oracle分析，不能当成已部署采样器。Table 4里BL=32的平均准确率61.81低于BL=8的65.43，说明追求更高并行率仍有准确率代价。本文未重新训练或跑硬件基准。

## 核心发现

### 发现 1: AR 与 Diffusion 损失是互补而非竞争的

通过 α ∈ {0.1, 0.2, 0.3, 0.5, 1.0} 的扫描（Tab.2）：
- 在 α=0.3 时，AR mode（70.62%）和 Diffusion mode（69.77%）**同时达到最优**。
- 在 [0.1, 0.5] 范围内，**没有任何 α 是以牺牲一方为代价提升另一方**。
- 移除 AR loss（独立的 no-AR 设置，不等于 α=1）会使两种模式都退化，反之亦然。

这是论文最核心的实证：**联合训练不是零和博弈**。Table 1 是逐项累加训练技巧的消融：最后加入 AR loss 从62.80到70.28（+7.48个百分点），加入两阶段训练从57.06到62.80（+5.74个百分点）。它们依赖当时已加入的技巧，不能作为相互独立的因果贡献排序。

> **个人解读**：这点解决了 diffusion LM 社区长期的一个开放问题——"加 AR 监督会不会让 diffusion 模式退化为伪 AR"。论文用 α 扫描 + 消融给了否定答案。这支持在相近训练设置下继续比较联合目标；不能由有限 α 扫描规定所有 diffusion LM 的默认训练目标。

### 发现 2: Self-Speculation 在多个维度优于 MTP/Eagle3

|              | NLD Linear SS | Eagle3 | MTP |
|--------------|---------------|--------|-----|
| 接受长度（avg） | 5.46 / **6.82 (LoRA)** | 2.75 | 4.24 |
| 接受长度（4 类目 avg） | 6.75 / **8.69 (LoRA)** | 2.81 | 4.73 |
| GB200 wall-clock 加速 vs Eagle3 | **2.4×** | 1× | — |

机制上的优势：
1. **无需独立 draft 模型** → 省掉 embedding/LM head 开销
2. **同一 backbone 表达** → drafter 和 verifier 共享语言理解
3. **diffusion 起草更可靠** → 长 horizon 上的草稿质量优于 MTP 的小模型

> **个人解读**：这一发现颠覆了 "推测解码 = 需要独立 draft 模型" 的固有思路。Eagle3 类方案的设计假设是"draft 模型必须更小才能快"，但 NLD 证明同一大模型用不同 attention 模式跑两次也能赢——只要 acceptance length 足够长。

### 发现 3: SOL 在指定参照下比 Linear SS 高 76.5% TPF

SOL 分析（Sec.4）：
- 在 BL=32 时，diffusion mode 的 SOL acceptance rate **7.60×**（multilingual 11.26×、coding 10.24×、roleplay 仅 3.49×）。
- 现有 confidence-based sampling 只能达 ~3×，**离 SOL 仍有大 gap**。
- Linear Self-Speculation 的 acceptance rate 已逼近 SOL（6.82× vs 7.60×，差 10.3%），但 SOL 的 real TPF 为 6.02、Linear SS 为 3.41，即 SOL 比 Linear SS 高 76.5%，Linear SS 比 SOL 低约 43.4%——因为它双 forward + 只 commit 前缀。

> **个人解读**：SOL 分析是本文最有方法学价值的贡献之一。它把模糊的"还能更快多少"问题量化为可测的 oracle 上界。Recursive Dynamic Compaction 的设计也优雅——通过递归 simulate 解决并行 commit 后分布漂移的 safety 问题。这种 framework 可以推广到所有"并行/序列"权衡的问题。

### 发现 4: LoRA-Drafter 用极小成本撬动大幅效率提升

仅在 attention 的 $o_{proj}$ 上加 LoRA（rank=128, α=512, ~36M 参 / 0.4% backbone），在 3B/8B/14B 上分别带来：
- **+14.4% / +32.5% / +27.6% TPF 提升**
- **平均分变化较小，但不等于逐任务不损精度**（差异主要来自 1-token decoding vs multi-token prefilling 的 kernel mismatch）

工程上的精彩细节 **"accepted+1" loss mask**——loss 只在接受前缀和第一个 reject 位置计算，避免训练时学到 inference 永远观察不到的反事实分布。

> **个人解读**：这是把"训练数据分布要匹配 inference 数据分布"做到极致的例子。在所有 drafter/verifier 类工作里，类似的反事实陷阱很常见——通常被忽略或用 dropout 等粗糙方式处理。本文给出了一个干净的解法。

### 发现 5: 不同规模支持多 token 解码，不能据此认定单调 scaling

| 规模 | Linear SS TPF | Quad SS TPF |
|------|---------------|-------------|
| 3B   | 4.36×         | 5.42×       |
| 8B   | 5.99×         | 6.38×       |
| 14B  | 5.96×         | 6.92×       |

论文归因为"更大模型 → 更强的 future-prediction 能力 → 更可靠的 draft 预测"。

> **个人解读**：这与"模型越大越涌现"的现象一脉相承，但是在解码效率维度的体现。这显示 self-speculation 能在这三个规模上工作；Linear SS 的8B为5.99、14B为5.96，并不单调，且基础模型/训练差异未被控制，不能单独归因为参数规模，与"模型越大推理越慢"的常识形成对冲，对超大模型部署非常有吸引力。

---

## 方法学全景

```
┌──────────────────────────────────────────────────────────────────┐
│                    Joint AR-Diffusion Training                   │
│   L = L_AR + 0.3 * L_diff,  Stage1(纯AR 1T) → Stage2(联合 300B)  │
│                                                                  │
│   关键技巧:                                                       │
│   - Dual-Stream Attention (Clean→Clean 严格 causal)              │
│   - Global Loss Averaging (降梯度方差)                            │
│   - DP-rank Varying Masking Ratios (进一步降方差)                 │
└────────────────────────────┬─────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
         Inference 自然涌现三模式             │
              │                             │
   ┌──────────┼──────────┬──────────────────┴──────────┐
   ▼          ▼          ▼                              ▼
┌─────┐  ┌─────────┐  ┌────────────────┐         ┌────────────┐
│ AR  │  │Diffusion│  │ Self-Speculation│        │SOL Analysis│
│Mode │  │  Mode   │  │     Mode        │        │  (oracle)   │
└─────┘  └─────────┘  └────────────────┘         └────────────┘
高并发    Confidence-     Linear: 双forward             ↑
 友好     based +         (diff draft + AR verify)     量化
         Trained          + LoRA Drafter               未释放
         Sampler          + accepted+1 mask            的 76.5%
                          + LK-hybrid loss             headroom
                          Quadratic: 单forward
                          (结构化 mask 同步 draft+verify)
```

---

## 关键数据汇总

### 8B Instruct 性能对比（Tab.5，10 任务平均）

| 模型 | Mode | Avg Acc | TPF | 备注 |
|------|------|---------|-----|------|
| Qwen3-8B | AR | 62.75 | 1.00 | SOTA AR 基线 |
| Ministral3-8B | AR | 58.02 | 1.00 | NLD 训练起点 |
| LLaDA-8B | Diff | 37.24 | 1.00 | SOTA diffusion 基线 |
| Dream-7B | Diff | 40.54 | 1.00 | SOTA diffusion 基线 |
| SDAR-8B | Diff | 50.57 | 1.75 | block-wise diffusion |
| **NLD-8B** | **AR** | **63.61** | **1.00** | 同精度超越 Qwen3 |
| **NLD-8B** | **Diff** | **63.18** | **2.57** | 远超其他 diffusion |
| **NLD-8B** | **Linear SS** | 62.81 | **5.99** | 默认部署模式 |
| **NLD-8B** | **Quad. SS** | **64.04** | **6.38** | 最高 TPF |

### 推理硬件实测（c=1，SPEED-Bench，Fig.9）

| 硬件 | AR (tok/sec) | NLD Linear SS | Eagle3 | NLD vs AR | NLD vs Eagle3 |
|------|--------------|---------------|--------|-----------|---------------|
| GB200 | 256 | **1015** (CUDA-opt) | — | **3.97×** | **2.4×** |
| RTX Pro 6000 (FP8) | 80 | **277** | 137 | 3.46× | 2.0× |
| RTX Pro 6000 (INT4) | 223 | **525** | 211 | 2.35× | 2.5× |
| DGX Spark (FP8) | 24.7 | **77.5** | 43.2 | 3.14× | 1.8× |

### Speed-of-Light 上限（Tab.4，BL=32）

| 类别 | SOL Accept | 备注 |
|------|------------|------|
| Multilingual | **11.26×** | 模板化、低 entropy |
| Coding | 10.24× | 强语法约束 |
| Math | 9.30× | 公式结构性强 |
| STEM | 8.01× | |
| Avg | **7.60×** | |
| Roleplay | 3.49× | 开放式、高 entropy（最低）|

---

## 局限性与未来方向

### 当前局限
1. **强依赖起点模型**：从 Ministral3 进行 1T+300B CPT，没回答"从零联合训练"的最优配方。
2. **采样器仍远低于 SOL**：confidence-based ~3× vs SOL 7.6×，trained sampler 改善有限。
3. **Linear SS 只能 commit 前缀**：丢弃第一个 reject 之后的高置信 token，是 real TPF 的根本瓶颈。
4. **Quad SS 设备效率受 kernel 制约**：FlexAttention 未充分优化。
5. **指令遵循略受影响**：IFEval -3.01个百分点、HumanEval -2.44个百分点（instruct）。
6. **训练成本高**：256× H100、1T+300B+45B token 的训练量。
7. **开放式任务受 token entropy 限制**：roleplay SOL 仅 3.49×，与"模板化任务并行最优"形成对比。

### 论文提出的未来方向
1. **更好的 sampler**：缩小与 SOL 的 gap。
2. **更好的 drafter-verifier alignment**：通过 nested subnets、weight-shared sub-models 降 drafting 成本。
3. **超越 prefix-only verification**：探索 diffusion verifier 验证非连续 tokens。
4. **更高层级的并行**：从 token 级 → segment/paragraph 级。

### 我的额外开放问题
- 若不从 Ministral3 起步而是从零联合训练，α=0.3 是否仍最优？两阶段是否仍必要？
- SOL 上限本身依赖 'serial denoising oracle'——能否设计训练 schedule 提高 SOL 的上限？
- Linear SS 的 prefix-only 限制能否被 diffusion verifier 完全打破？若 verifier 也并行，effective acceptance 的边界在哪？

---

## 结论与个人评价

**评分**：相关度 10/10，质量 9/10。

NVIDIA 这篇技术报告是 "AR + Diffusion 融合" 这一研究方向迄今最完整的工程证明。它做对了三件事：

1. **方法论上**：把"AR/Diffusion 互补"从猜想变成可量化的结论（α 扫描 + 消融 + SOL 三角验证）。
2. **工程上**：交付 3B/8B/14B 文本模型及论文研究的8B视觉语言变体（不按规格笛卡尔积推算发布数量），开源 Megatron Bridge 训练 pipeline 与 HF 权重。
3. **基础设施上**：SOL 分析框架给社区设定了"还有多远"的明确 north star。

最值得借鉴的设计哲学是 **"对 inference 时实际数据分布建模"**——'accepted+1' loss mask、global loss averaging、asymmetric dual-stream 都是这一思想的不同侧面体现。

如果这一 'tri-mode 一站式部署' 范式能工程化稳定，可能会成为下一代 LLM 推理基础设施的默认形态——单模型、按 concurrency 切换模式、不需要维护独立的 draft model。这对模型管理、显存占用、运维复杂度都是结构性简化。

---

## 来源

- **主论文**: Yonggan Fu et al. *Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding*. NVIDIA Technical Report, 2026-05-19. [既有全文文本抽取](raw-extracts/nemotron-tri-mode-fulltext.md)；[官方v1 PDF](https://d1qx31qr3h6wln.cloudfront.net/publications/Nemotron_Diffusion_Tech_Report_v1.pdf?VersionId=db8_EMO8B.vmU26.jr7Le9pN3MqcUDNL)；版本与证据定位见 [来源清单](sources/MANIFEST.md)
- **关键引用**:
  - LLaDA (Nie et al. 2025) — diffusion LM 基线
  - Dream-7B (Ye et al. 2025) — diffusion LM 基线
  - SDAR-8B (Cheng et al. 2025) — diffusion-AR 混合基线
  - Block Diffusion (Arriola et al. 2025) — block-wise 设计起源
  - "Your LLM knows the future" (Samragh et al. 2025) — AR 模型的 lookahead 能力
  - Eagle-3 (Li et al. 2025) — MTP 主要对比对象
  - SPEED-Bench (Abramovich et al. 2026) — 推测解码评测基准
