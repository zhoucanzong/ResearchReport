# Nemotron-Labs-Diffusion 结构化阅读笔记

> **论文**: Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding
> **作者**: Yonggan Fu et al. (NVIDIA + Georgia Tech + HKU + MIT)
> **日期**: 2026-05-19
> **页数**: 21
> **阅读日期**: 2026-05-27
> **结构化 JSON**: [`papers/nemotron-labs-diffusion.json`](../papers/nemotron-labs-diffusion.json)

---

## 一句话总结
在同一模型里联合训练 AR + Block-wise Diffusion 损失，使其同时获得 AR 精度、Diffusion 并行解码能力和 Self-Speculation 加速能力——证明 diffusion 起草 + AR 验证（self-speculation）比 Eagle3 这类 MTP 方法更有效，且 diffusion 解码本身在 SOL 上还有 76.5% 的并行潜力未释放。

---

## 1. 研究背景与三大问题

AR LM 的串行解码在低 batch 部署下严重欠用 GPU；Diffusion LM 虽能并行解码，但精度落后且训练效率低（不利用左到右先验）。论文围绕：

- **Q1**：AR 与 Diffusion 应该竞争还是融合？
- **Q2**：Diffusion 能否提供比 MTP 更强的加速？
- **Q3**：Diffusion 解码是否值得长期研究（有多大潜力）？

## 2. 训练框架（Sec.2）

### 2.1 联合损失
$$\mathcal{L}(\theta) = \mathcal{L}_{AR}(\theta) + \alpha \cdot \mathcal{L}_{diff}(\theta), \quad \alpha = 0.3$$

- **AR loss**：标准 next-token CE（causal）。
- **Diffusion loss**：block-wise denoising，序列分为 $B$ 个 block，每个 block 内 token 按 noise level $t \in [0,1]$ 被掩码，loss 含 $1/t$ 重权。
- $\alpha=0.3$ 是经过 5 个值（0.1/0.2/0.3/0.5/1.0）扫描后的最优——使两个 loss 的量纲匹配。

### 2.2 注意力与 Dual-Stream
- 训练时把序列复制两份：一份 **clean**（用于 AR loss）、一份 **noisy**（用于 diffusion loss）。
- **Clean→Clean** 严格 causal（与先前 [9,10] 的 block-wise 不同），避免标签泄漏；这样 AR loss 与 diffusion loss 可在同一次 forward-backward 内计算。
- **Noisy→Noisy** intra-block 双向、跨 block causal；**Noisy→Clean** 让 noisy block 看 clean prefix 实现 condition。

### 2.3 关键训练技巧
两个最大单点收益：
- **+AR loss → +7.48%**（diffusion mode 的 avg accuracy）
- **+ two-stage training → +5.74%**

其它技巧：
- **Global Loss Averaging（Eq.5）**：用 batch 内全部 $NL$ token 数归一化（而非 sequence-wise）。原因：diffusion loss 的 $1/t$ 重权 + 每条 sample 不同噪声 token 数，导致 sequence-wise 平均会放大小 $t$ 样本的影响，增大梯度方差。
  - 类比 RL 中 GRPO vs DAPO 的 aggregation 选择。
- **DP-rank varying masking ratios**：不同 data parallel rank 用不同 noise level，进一步降方差。
- **Two-stage**：Stage 1 纯 AR（α=0，1T tokens）建立左到右先验 → Stage 2 联合（α=0.3，300B tokens）。

### 2.4 AR 与 Diffusion 损失互相影响
- **AR loss 提升 diffusion 精度**（+7.48%，最大收益）。
- **Diffusion loss 几乎不损 AR 精度**（base +0.14%，instruct +0.43%）。
- 两者在 α=0.3 同时最优——**不是 zero-sum**。
- 唯一可见的代价：instruct 模型在 IFEval -3.01%、HumanEval -2.44%——说明严格指令遵循略受影响。

## 3. 三模式推理（Sec.3）

### 3.1 Mode 1: AR
标准 left-to-right 解码，适合 **高并发**（compute-bound 场景）。

### 3.2 Mode 2: Block-wise Diffusion
- 按 block 解码，block 内并行 denoise，confidence > 阈值即 commit。
- **可选训练采样器**：把"top-1 是否会被最终 commit"作为分类任务训练一个轻量 head，让 commit 决策从启发式 → 学习到的。
- 在 8B 上把 Pareto frontier 整体上移：相同精度下 +1.3× TPF，或相同 TPF 下 +10.6% 精度。

### 3.3 Mode 3: Linear Self-Speculation
两次 forward：
1. **Drafting (diffusion)**：在 verified prefix 后接 $k$ 个 mask，并行 denoise 得到 $\hat{x}_{n+1}, ..., \hat{x}_{n+k}$。
2. **Verification (AR)**：用 causal AR 跑一次 forward，逐位置匹配；接受最长匹配前缀 + 第一个 reject 位置的 AR token（标准 speculative decoding）。

**LoRA-Drafter 增强**：仅在 attention 的 $o_{proj}$ 加 LoRA（rank=128, α=512，~36M 参 / 0.4% backbone），用 **LK-hybrid distribution-matching loss + token CE** 训练。

关键细节 **"accepted+1" loss mask**：loss 只在接受前缀 + 第一个 reject 位置计算，因为 inference 时验证器 KV cache 会在 reject 点重建——若在更靠后的位置计算 loss，会让 drafter 学到一个 deployment 时永远观察不到的反事实分布。

LK-hybrid loss：
$$\mathcal{L}^{LK}_j = \lambda_j \cdot KL(\tilde{p}_j \| \tilde{q}_j) + (1-\lambda_j) \cdot \frac{1}{2} \sum_v |\tilde{p}_j(v) - \tilde{q}_j(v)|$$
其中 $\lambda_j = \exp(-\eta \cdot \mathrm{sg}[\alpha_j])$ 自适应：训练早期（$\alpha_j$ 小）行为像 KL（强匹配梯度），训练后期（$\alpha_j \to 1$）行为像 TV（直接最小化接受率 gap）。

### 3.4 Variant: Quadratic Self-Speculation
单 forward 内通过结构化 attention mask 同时做 draft + verify——更高的 TPF/step（6.38 vs 6.99），但因 FlexAttention kernel 未充分优化，wall-clock 反而比 Linear SS 慢，默认使用 Linear。

## 4. Speed-of-Light 分析（Sec.4）

### 4.1 SOL 构造
两步定义 oracle：
1. **Serial denoising**：从 all-mask 开始，每步只 commit 当前最大 peak prob 位置的 argmax，跑 $B$ 步得到收敛 target $\mathbf{t}$。这定义了"diffusion 模型在没有任何并行的情况下会收敛到什么"。
2. **Recursive Dynamic Compaction**：并行 commit 时，对当前匹配 serial target 的位置按 confidence 排序，二分搜索能 "safely commit" 的最大前缀。**Safety check** 通过递归 simulate（greedy acceptance，预算 5000 forward）验证：commit 之后剩余位置仍能收敛到 $\mathbf{t}$。

### 4.2 关键数字
- **Diffusion SOL acceptance rate**: 7.60× 平均，BL=32 时 multilingual 11.26×、coding 10.24×、roleplay 仅 3.49×（受 token entropy 限制）。
- **Confidence-based sampling**: 仅 ~3× → 离 SOL 还有大 gap。
- **Linear SS vs SOL**: acceptance rate 仅差 10.3%（6.82× vs 7.60×），但 real TPF 差 76.5%（3.41× vs 6.02×）——因为 Linear SS 双 forward + 只 commit 前缀。

### 4.3 结论
1. Diffusion 解码是高度并行的候选方向，关键在于训练能逼近 SOL 的采样器。
2. AR 验证是逼近 SOL 的有效手段，但 prefix-only + 双 forward 的代价基本封死了它的 real TPF 上限。

## 5. 模型家族（Sec.5）

| 规模 | 训练设置 |
|------|----------|
| Base | 起点 Ministral3，Stage1 1T tokens (α=0)，Stage2 300B tokens (α=0.3)，bs=512、seq=4096，256× H100，WSD 调度，AdamW |
| Instruct | 起点 base，SFT 45B tokens、bs=256、seq=16k、α=0.3、lr 2.5e-6→2.5e-7 |
| VLM | LM 来自 NLD-8B Instruct、vision encoder 来自 Ministral3-8B-Instruct VLM，**Asymmetric Dual-Stream**（noisy 半流去掉 vision token，减少 FLOPs）|

## 6. 实验结果（Sec.6）

### 6.1 8B Instruct 结果（Tab.5）
| 模型 | Mode | Avg Acc (%) | TPF |
|------|------|--------|------|
| Qwen3-8B | AR | 62.75 | 1.00 |
| LLaDA-8B | Diff | 37.24 | 1.00 |
| Dream-7B | Diff | 40.54 | 1.00 |
| SDAR-8B | Diff | 50.57 | 1.75 |
| **NLD-8B** | AR | **63.61** | 1.00 |
| **NLD-8B** | Diff | 63.18 | 2.57 |
| **NLD-8B** | Linear SS | 62.81 | **5.99** |
| **NLD-8B** | Quad. SS | **64.04** | 6.38 |

NLD-8B 各模式精度均高于或匹敌 Qwen3-8B，且 self-speculation 把 TPF 拉到 6×。

### 6.2 规模扩展（3B/14B，Tab.7）
- NLD-3B Quad SS: 55.80% acc / 5.42× TPF（超过 Qwen3-4B 的 53.23%）。
- NLD-14B Quad SS: 68.15% acc / 6.92× TPF（超过 Qwen3-14B 的 65.17%）。
- 越大模型越能解锁并行：3B → 14B 的 Linear SS TPF 从 4.36× 涨到 5.96×。

### 6.3 Base Models（Tab.8）
- NLD-8B base AR: 71.89%（vs Qwen3-8B 71.58%、Ministral3-8B 66.75%）。
- NLD-8B Diff: 比 LLaDA-8B +17.21%、比 Dream-7B +6.83%。
- Quad SS 达 7.04× TPF。

### 6.4 VLM（Tab.9）
- NLD-VLM-8B AR: 59.5%（比 LLaDA-V-8B +1.3%）。
- Linear SS 在 > 200 token 长回答时 TPF 7.45×——**长回答场景优势最大**。

### 6.5 推理效率（Fig.9）
- GB200 上 Linear SS 比 AR 加速 **3.3×**（CUDA kernel 优化后 3.97×，1015 tok/sec）。
- 相比 Qwen3-8B-Eagle3：GB200 2.4×、RTX Pro 6000 2.3×、DGX Spark 1.8×。
- **接受长度对比**（Tab.10，draft length 31）：
  - NLD Native 5.46 / LoRA 6.82
  - Eagle3 2.75 / MTP 4.24
  - diffusion-friendly 4 类（coding/math/reasoning/multilingual）差距进一步拉大到 6.75/8.69 vs 2.81/4.73

## 7. 关键洞见（Sec.8）

1. **三模式自然涌现**：仅靠联合训练，不需架构特化。
2. **AR 与 Diffusion 互补**：在 α=0.3 同时最优，非 zero-sum。
3. **Self-Speculation > MTP**：用同一模型起草 + 验证，省掉外挂 draft 模型。
4. **方差缩减对 diffusion 训练关键**：global loss avg、two-stage、DP-rank 等都是降方差手段。
5. **Linear SS 当前最实用**；Quadratic SS 在 kernel 优化后更有潜力。
6. **Diffusion mode 仍有 76.5% 的 SOL headroom**——是未来重点方向。

未来方向：
- 缩小 sampler 与 SOL 的 gap。
- 改进 drafter-verifier alignment（如 nested subnets）。
- 探索 non-prefix verification（diffusion verifier）。
- 推动 segment-level / paragraph-level 并行。

## 8. 我的思考

- **'accepted+1' loss mask** 是反事实分布管理的精彩工程实践——值得在所有 drafter/verifier 训练里借鉴。
- **Global loss averaging** 的方差分析揭示了一类隐藏陷阱：含可变 token 权重的 loss 一定要看 aggregation 选择。
- **Speed-of-Light 框架** 给社区设定了清晰的 north star——我们离最优还有多远是 quantifiable 的。
- **Asymmetric Dual-Stream** 体现了'按 token 是否进入目标计算分配 attention 资源'的优化空间，未来多模态/工具调用混合训练可借用。

开放问题：
- 若不从 Ministral3 起步而是从零联合训练，α=0.3 是否仍最优？两阶段是否仍必要？
- SOL 上限依赖 'serial denoising oracle'，若改 diffusion 训练 schedule 能否解锁更高的 SOL？
- Linear SS 的 prefix-only 限制能否被 diffusion verifier 完全打破？
