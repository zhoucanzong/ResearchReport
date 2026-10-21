# 知识图谱：Nemotron-Labs-Diffusion 核心概念

> 概念卡片按理解依赖关系组织。先理解上层 → 再深入下层。

---

## 顶层概念

### Tri-Mode Language Model
- **定义**：在单一模型权重内同时支持 AR、Diffusion、Self-Speculation 三种解码模式的语言模型。
- **类比**：一个会同时使用 "口述、写字、看图速记" 三种笔记方式的人——根据场景选最快的那种，无需切换大脑。
- **直观理解**：训练时把 AR 和 Diffusion 两种损失加权求和，不需要架构特化；推理时通过切换 attention mask（causal/bidirectional）和输入方式（带或不带 mask token）就能进入不同模式。
- **关联概念**：[[joint-ar-diffusion-training]]、[[block-wise-diffusion]]、[[self-speculation-decoding]]
- **典型应用**：单模型部署、按 concurrency 切换推理策略（高并发用 AR、低并发用 SS、高潜力场景用 Diffusion）
- **常见误区**：以为需要训三个独立模型并 ensemble；其实是同一权重 + 切换 attention 模式

### Block-wise Diffusion
- **定义**：把序列分成 $B$ 个连续 block，block 内 token 双向 attention 并行 denoise，block 间 causal——使其能复用 KV cache 又保留并行解码能力。
- **类比**：写小说时按 "段落" 为单位，先框定段内骨架（双向脑暴），段间按时间顺序推进。
- **数学表达**: $\mathcal{L}_{diff}(\theta) = \mathbb{E}\big[-\frac{1}{t}\sum_{b=1}^B \log p_\theta(x^b | \tilde{x}^b_t, x^{<b})\big]$
- **直观理解**：纯 diffusion 没法用 KV cache（双向 attention 每步重算），block-wise 让 cross-block 的 prefix 部分得以复用，是工程可行的关键。
- **关联概念**：[[joint-ar-diffusion-training]]、[[confidence-based-sampling]]、[[kv-cache-reuse]]
- **典型应用**：所有现代 diffusion LM（Block Diffusion、SDAR、Dream、NLD）

### Self-Speculation Decoding
- **定义**：用同一个模型的 Diffusion 模式起草多 token 草稿、AR 模式验证草稿，不需要额外的 draft 模型。
- **类比**：左手画草图（粗但快）、右手用尺子量（慢但准）——同一个人就完成 draft + verify。
- **直观理解**：替代 Eagle3 这类需要训独立小模型的 MTP 方案；优势是 (1) 接受长度更高（diffusion 草稿更可靠），(2) 不引入额外 embedding/LM head 开销，(3) 整体共享 backbone 表达。
- **关联概念**：[[speculative-decoding]]、[[multi-token-prediction]]、[[lora-drafter]]、[[accepted-plus-one-mask]]
- **典型应用**：低并发、单流推理加速（GB200/RTX Pro 6000/DGX Spark 上均比 Eagle3 快 1.8×~2.4×）
- **常见误区**：以为还需要外挂"小模型"——其实就是同一个权重切到 diffusion mode 跑一次

---

## 训练相关概念

### Joint AR-Diffusion Training
- **定义**：用加权 $\mathcal{L} = \mathcal{L}_{AR} + 0.3 \cdot \mathcal{L}_{diff}$ 同时优化两个目标。
- **直观理解**：AR loss 锚定语言的左到右先验，diffusion loss 解锁前瞻规划与并行解码。两者在 α=0.3 同时最优，**不是 zero-sum**。
- **关键发现**：加 AR loss 让 diffusion 精度 +7.48%（消融最大单项）；加 diffusion loss 几乎不损 AR 精度（+0.14% ~ +0.43%）。
- **关联概念**：[[two-stage-training]]、[[global-loss-averaging]]、[[dual-stream-attention]]

### Two-stage Training
- **定义**：Stage 1 纯 AR（α=0，1T tokens）→ Stage 2 联合（α=0.3，300B tokens）。
- **直观理解**：先把左到右先验打牢、再让 diffusion 在此基础上添加并行能力；从已 pretrained 的 AR 模型（Ministral3）出发更高效。
- **累计消融增量**：57.06→62.80，+5.74个百分点；依赖前面的技巧组合。
- **关联概念**：[[joint-ar-diffusion-training]]

### Global Loss Averaging
- **定义**：用 batch 总 token 数 $NL$ 归一化 loss，而非 sequence-wise 平均。
- **类比**：班级总分用全班所有题目数平均，而不是每位学生题目数不同还按每人 1 票算。
- **数学**：$\mathcal{L}_{global} = \frac{1}{NL}\sum_{n,i}\ell_{n,i}$ vs $\mathcal{L}_{seq} = \frac{1}{N}\sum_n (\frac{1}{L}\sum_i \ell_{n,i})$
- **直观理解**：Diffusion loss 含 $1/t$ 重权且 noisy token 数随 sample 变化；sequence-wise 平均会让"小 t 但 token 少"的样本占过大权重，方差大。Global 平均按 token 数权重正比分配，更稳定。
- **直接类比**：RL 里 GRPO vs DAPO 的 aggregation 选择。
- **关联概念**：[[variance-reduction]]、[[dp-rank-varying-masking]]

### Dual-Stream Attention
- **定义**：训练时把序列复制为 clean + noisy 两份并连接，结构化 mask 让两者在同 forward 内计算 AR loss 与 diffusion loss 互不干扰。
- **关键创新**：Clean→Clean **严格 causal**（区别于 Block Diffusion 的 block-wise），保证 AR loss 计算无 label leakage。
- **关联概念**：[[asymmetric-dual-stream-vlm]]、[[joint-ar-diffusion-training]]

### Asymmetric Dual-Stream (VLM)
- **定义**：VLM 设置下，noisy 半流剥离所有 vision token（因 vision 永不被 mask），减少 attention FLOPs。
- **直观理解**：vision token 在 noisy 半流里既不会被 mask 也不参与 diffusion loss，但会消耗 attention 计算；剥离它们是纯收益。FLOPs 节省与 $N_{vis}/L$ 成正比。
- **关联概念**：[[dual-stream-attention]]、[[vlm]]

---

## 推理相关概念

### Confidence-based Sampling
- **定义**：diffusion 解码时每步对 mask 位置取置信度 > 阈值的并行 commit。
- **直观理解**：纯启发式的"觉得有把握就 commit"；本文证明它远低于 SOL（约 3× vs 7.6×），还有大量并行空间未利用。

### Trained Sampler
- **定义**：一个轻量分类器，预测当前 top-1 token 是否会和 serial denoising 收敛 token 一致；超过阈值即 commit。
- **直观理解**：把"何时 commit"从启发式 → 学习问题；可同精度 +1.3× TPF 或同 TPF +10.6% 精度。
- **关联概念**：[[confidence-based-sampling]]、[[sol-analysis]]

### Linear Self-Speculation
- **定义**：双 forward 版 SS——一次 diffusion 起草 k 个 token、一次 AR 验证最长前缀。
- **关联概念**：[[self-speculation-decoding]]、[[lora-drafter]]、[[quadratic-self-speculation]]

### Quadratic Self-Speculation
- **定义**：单 forward 版 SS——通过结构化 attention mask 同时做 draft + verify，每步固定产出 k 个候选。
- **直观理解**：论文设置下 TPF 更高（6.38 vs 5.99），但 FlexAttention kernel 未充分优化，wall-clock 反而慢于 Linear。
- **关联概念**：[[linear-self-speculation]]

### LoRA Drafter
- **定义**：在 attention 的 $o_{proj}$ 上加 LoRA（rank=128, α=512, ~36M 参 / 0.4% backbone），仅微调 diffusion 起草路径，让其与 AR 验证更对齐。
- **效果**：3B/8B/14B 上分别 +14.4% / +32.5% / +27.6% TPF，几乎不损精度。
- **关联概念**：[[self-speculation-decoding]]、[[lk-hybrid-loss]]、[[accepted-plus-one-mask]]

### Accepted+1 Loss Mask
- **定义**：训练 LoRA drafter 时只在"接受前缀 + 第一个 reject 位置"计算 loss，更靠后的位置完全 mask 掉。
- **直观理解**：inference 时验证器 KV cache 在 reject 点重建，更靠后的位置在 deployment 中永远观察不到，对其训练会让 drafter 学到反事实分布。
- **类比**：射击训练只记录第一次脱靶之前的精度——之后的弹道在比赛里不会出现。
- **关联概念**：[[lora-drafter]]、[[lk-hybrid-loss]]

### LK-hybrid Loss
- **定义**：在 top-K=200 union 支撑集上 KL 与 TV 的自适应加权 + token-level CE：
  $$\mathcal{L}^{LK}_j = \lambda_j \cdot KL(\tilde{p}\|\tilde{q}) + (1-\lambda_j) \cdot \frac{1}{2}\|\tilde{p}-\tilde{q}\|_1$$
  其中 $\lambda_j = \exp(-\eta \cdot \mathrm{sg}[\alpha_j])$，$\alpha_j$ 是 speculative decoding 的接受概率。
- **直观理解**：训练早期（drafter 差，$\alpha_j$ 小）行为像 KL，提供强匹配梯度；训练后期（$\alpha_j \to 1$）行为像 TV，直接最小化接受率 gap。
- **关联概念**：[[lora-drafter]]

---

## 分析框架

### Speed-of-Light (SOL) Analysis
- **定义**：用 oracle 评估 diffusion 解码在"理想采样器"下每个 forward 能 commit 的最大 token 数。
- **构造**：
  1. **Serial denoising oracle**：每步只 commit 当前最高 peak prob 位置 → 得到收敛 target $\mathbf{t}$。
  2. **Recursive Dynamic Compaction**：并行 commit 时对匹配位置按 confidence 排序，二分搜索能"safely commit"的最大前缀。Safety check 通过递归 simulate（greedy acceptance）验证。
- **关键发现**：Diffusion SOL acceptance 7.60× vs Linear SS real TPF 3.41× → **以 Linear SS 为分母高约76.5%；反向以SOL为分母差约43.4%**。
- **意义**：为社区设定 "north star"——清晰告诉我们当前 sampler 离最优有多远。
- **关联概念**：[[trained-sampler]]、[[self-speculation-decoding]]

### Acceptance Rate vs Real TPF
- **区别**：acceptance rate 是"接受步里平均 commit 多少 token"，real TPF 是"每个 forward 平均产出多少 token"。
- **关键差异**：SOL 仅一次 forward 即 commit 多位置（real TPF ≈ acceptance rate）；Linear SS 需要 draft + verify 两次 forward，real TPF ≈ acceptance / 2。
- **意义**：仅对比 acceptance rate 会掩盖真实硬件代价，必须看 real TPF。

---

## 对比基线

### MTP (Multi-Token Prediction) / Eagle3
- **定义**：用小型独立 draft 模型预测未来多 token，大 AR 模型一次 forward 验证。
- **本文对 MTP 的批评**：(1) draft 模型容量有限，远场预测不可靠；(2) 即使 draft 模型小，仍背负 embedding + LM head 开销；(3) 接受长度低（NLD 6.82 vs Eagle3 2.75）。
- **关联概念**：[[self-speculation-decoding]]、[[speculative-decoding]]

### Speculative Decoding (Leviathan et al.)
- **定义**：draft + verify 的经典框架——任何 SS/MTP 都是它的特例。
- **NLD 的位置**：把 draft 和 verify 都内化在同一个模型的不同 mode 内。
