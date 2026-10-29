---
display_name: Kimi
---

# Kimi 系列模型深度调研报告

> 调研对象：Moonshot AI（月之暗面）的 Kimi 模型家族
> 时间跨度：2023 年 10 月 ~ 2026 年 10 月
> 资料来源：arXiv 论文、Moonshot AI 官方技术博客、HuggingFace 模型卡、GitHub 仓库
> 撰写日期：2026 年 6 月 ｜ **最近更新：2026-10-23**（重核 Kimi K3 的联合设计因果表述和评测证据，删去宣传性级别称谓、API 价格及成本排名）

---

## 1. 概述与时间线

Moonshot AI（月之暗面，Beijing Yuezhi Technology Co., Ltd.）由清华大学校友、原 Recurrent.ai 创始人**杨植麟（Zhilin Yang）**于 2023 年 3 月在北京创立，2023 年 10 月发布首款 C 端产品 **Kimi 智能助手**，成为中国最早押注「超长上下文（Long-Context）」路线的大模型公司之一。其技术演进沿着三条主线展开并彼此交织：

1. **长上下文主线**：Moonshot-v1（200K）→ 2M 字符内测 → **MoBA**（块级稀疏注意力）→ **Kimi Linear / KDA**（线性注意力混合架构），系统性回答「如何让 Transformer 真正吃下百万 token」。
2. **推理（Reasoning）主线**：**Kimi k1**（2024.11，多模态思考预览）→ **Kimi k1.5**（2025.01，对标 OpenAI o1）→ **Kimi K2 Thinking**（2025.11，对标 GPT-5、Claude Sonnet 4.5），形成「以长上下文 RL + Long2Short」为核心的独特路线。
3. **基础模型与多模态主线**：**Moonlight 16B-A3B**（2025.02，MoE 训练采用 Muon）→ **Kimi-VL / Kimi-VL-Thinking**（2025.04）→ **Kimi-Audio**（2025.04）→ **Kimi K2 1T-A32B**（2025.07，「Open Agentic Intelligence」）→ **Kimi K2.5**（2026.01，原生多模态 Agent）→ **Kimi K2.6**（2026.04，编码/多 Agent 集群）→ **K2 系列退役**（2026.05）。

**2026 年中之后的两步（详见 §4.4 / §4.5）**：**Kimi K2.7 Code**（1T-A32B 同架构续训、编程向）与 **Kimi K3**（2.78T 总 / 104.2B 激活 MoE，原生多模态、1M 上下文）。K3 相较 K2 / K2.5 的**全层 MLA + RoPE/YaRN**，改用 **69 层 KDA + 24 层 Gated MLA（3:1）+ 全层 NoPE**，把此前 48B Kimi Linear 研究模型中的混合注意力路线带到更大规模。

### 1.1 关键时间线

| 时间 | 事件 | 说明 |
| --- | --- | --- |
| 2023-03 | Moonshot AI 成立 | 杨植麟、周昕宇（Xinyu Zhou）、吴育昕（Yuxin Wu）创立 |
| 2023-10-09 | Kimi Chat 上线 | 首发即支持 **20 万汉字**（约 200K characters）无损上下文 |
| 2024-03 | 200 万汉字内测 | 将长上下文扩展到 **2M Chinese characters** |
| 2024-08 | Moonshot-v1 API（8K/32K/128K） | 三档上下文 API 商业化 |
| 2024-11 | **Kimi k1 视觉思考模型**预览 | 公开多模态长思考模型预览 |
| 2025-01-22 | **Kimi k1.5** 技术报告（arXiv:2501.12599） | 与 DeepSeek-R1 同期，o1 级推理性能 |
| 2025-02-21 | **Moonlight / Muon 论文**（arXiv:2502.16982） | 首次将 Muon 扩展到 16B MoE 规模 |
| 2025-02-18 | **MoBA 论文**（arXiv:2502.13189） | 块级稀疏注意力，已用于 Kimi 线上长上下文 |
| 2025-04-10 | **Kimi-VL Technical Report**（arXiv:2504.07491） | 2.8B 激活的 MoE VLM，附 Kimi-VL-Thinking |
| 2025-04-25 | **Kimi-Audio**（arXiv:2504.18425） | 7B 音频基础模型 |
| 2025-07-22 | **Kimi K2** 开源（arXiv:2507.20534） | 1T 总 / 32B 激活 MoE，**MuonClip** 优化器 |
| 2025-10-30 | **Kimi Linear** 论文（arXiv:2510.26692） | KDA + MLA 3:1 混合，1M 上下文 6× 解码加速 |
| 2025-11-06 | **Kimi K2 Thinking** 发布 | 1T MoE + 256K 上下文 + 原生 INT4，HLE 44.9%（带工具） |
| 2026-01-27 | **Kimi K2.5** | 在 K2 基础上继续预训练 ~15T 视觉-文本 token，原生多模态 Agent，Agent Swarm 100 子代理 |
| 2026-04-13 | **Kimi Code K2.6** | 编码代理工具发布 |
| 2026-04-20 | **Kimi K2.6** 发布权重 | 1T 参数 / 32B 激活 MoE，256K 上下文，SWE-Bench Verified 80.2%（作者报告）；许可见来源 |
| 2026-05-25 | **K2 系列退役** | K2 系列正式停止支持，仅 K2.6 继续维护 |
| 2026-06 | **Claw Groups / 视频输入** | 异构代理集群研究预览；支持 mp4, mov, webm, avi 视频输入 |
| 2026-06-11 | **Kimi K2.7 Code** 开源 | 1T 总 / 32B 激活 MoE（沿用 K2.6 架构），256K 上下文，强制思考；思考 token 较 K2.6 约 −30%（官方自报），详见 §4.4 |
| 2026-07-16 | **Kimi K3** 产品/API 上线 | 2.8T/104B MoE（论文精确表值 2.78T/104.2B），原生多模态，1M 上下文；技术分析见 §4.5 |
| 2026-07-27 | **Kimi K3 权重仓库公开 + 技术报告 v1**（arXiv:2607.24653） | 官方博客称完整权重将于 7 月 27 日前发布；Hugging Face 仓库历史列有当日提交；技术报告 v2 于 2026-08-07 |

> 注：本报告的「推理模型」与「基座模型」在 2025 年 11 月之后开始合流——K2 Thinking 起，Moonshot 选择**单一旗舰多形态**（base / instruct / thinking）的发布范式，与 DeepSeek 模式趋同。

---

## 2. 基座模型演进：以长上下文为主线

### 2.1 Moonshot-v1（2023-2024）：注意力工程与基础设施驱动的 200K → 2M

Kimi 在 2023 年 10 月以「20 万汉字无损上下文」首次进入大众视野时，主流闭源模型仍停留在 GPT-4 的 8K~32K 区间（GPT-4 Turbo 128K 直到 2023 年 11 月才发布）。此时 Moonshot-v1 并未发布详细技术报告，从后续披露与官方开放平台信息可推断其技术路径：

- **基础架构**：Transformer Decoder + RoPE（Rotary Position Embedding），由 Moonshot 联合创始人苏剑林（Jianlin Su，RoPE 原作者）主导设计。
- **长上下文实现**：分阶段课程式训练（curriculum）逐步将上下文从 8K → 32K → 128K → 200K 拓展，配合 RoPE base frequency 调整与 YaRN 系列外推方法。
- **基础设施**：自研分布式训练栈（Sequence/Context Parallelism + ZeRO + 重计算）以承载 200K+ 序列；KV-Cache 分页与持久化存储用于推理期长对话上下文复用。
- **2024-03 的 2M 中文字符内测**：对外宣称「无损」（lossless），实际依赖大段文档的离线预处理与上下文压缩 / 检索增强；这是产品形态而非纯模型能力升级，但确立了 Kimi 在 C 端「长文本助手」的品牌定位。

> **结论**：这一阶段的长上下文扩展主要依赖系统工程与基础设施；之后的 MoBA、KDA 则尝试直接改变注意力计算路线。

### 2.2 MoBA：从 Dense Attention 到块级稀疏（2025-02）

随着 1M token 级别上下文需求出现，标准 Softmax Attention 的 O(n²) 计算和缓存开销成为系统瓶颈。Moonshot 的一条探索路线是 **MoBA（Mixture of Block Attention，arXiv:2502.13189）**：

- **核心思想**：将 MoE 路由思想搬到注意力层。把序列切成固定大小的 block，由可学习的 router 为每个 query 选择 top-k 个最相关 block 进行注意力计算，其余 block 完全跳过。
- **「Less Structure」原则**：不像 sliding-window、StreamingLLM 那样硬编码注意力 pattern，让模型自行决定关注哪些块。
- **可切换性**：MoBA 支持 full-attention 与 sparse-attention 之间无缝切换——预训练用 full，长上下文阶段切换到 MoBA；这一性质是 DeepSeek NSA、Native Sparse Attention 等同期工作所不具备的。
- **工程价值**：论文明确指出 **MoBA 已部署于 Kimi 线上服务**，承担长上下文请求的实际推理流量。这意味着 Kimi 的 1M 上下文不是「能跑」而是「跑得起」。

### 2.3 Kimi Linear / KDA：3:1 混合注意力与长上下文效率（2025-10）

MoBA 仍保留 Softmax attention，KV cache 随上下文增长；在 1M token 场景中，计算和缓存占用仍是系统瓶颈。**Kimi Linear（arXiv:2510.26692）**提出另一种路线：

- **Kimi Delta Attention（KDA）**：在 Gated DeltaNet 之上引入更精细的**逐通道（fine-grained）门控**与改进的 delta-rule 状态更新规则，本质上是带有「遗忘门」的线性 RNN，状态尺寸恒定（不随序列长度增长）。
- **3:1 混合架构**：每 4 层中 3 层 KDA + 1 层 **MLA（Multi-head Latent Attention，DeepSeek-V3 风格的全注意力）**，并对所有 MLA 层采用 **NoPE（No Positional Encoding）**——把位置编码「外包」给 KDA 的递归状态，全局层只负责语义聚合。
- **作者对照**：在 1.4T token 的预训练对照下，48B-A3B 的 Kimi-Linear-Base 报告 MMLU-Pro 51.0、RULER（128K）84.3，并在论文列出的强化学习评测上高于其全注意力基线。这些结果限于论文的模型、数据与任务设置，不概括所有线性注意力方法。
- **效率**：相比纯 MLA，**KV Cache 减少 75%、1M 上下文 TPOT（Time-Per-Output-Token）加速 6×**。
- **意义**：这是 Moonshot 自 RoPE 之后在注意力机制上的第二次范式级别贡献，也是其后续 K2.x 系列模型的重要架构候选。

| 阶段 | 代表 | 注意力类型 | 上下文 | KV 增长 | 实际负载 |
| --- | --- | --- | --- | --- | --- |
| 2023-2024 | Moonshot-v1 | Dense Softmax + RoPE | 200K (后扩 2M) | O(n) | 通过工程承载 |
| 2025-Q1 | MoBA | 块级稀疏 + 路由 | ≥1M | O(n) 但常数小 | 已上线 Kimi |
| 2025-Q4 | Kimi Linear | KDA(线性)+MLA(NoPE) 3:1 | 1M | KDA O(1)，MLA O(n)/4 | 候选下一代基座 |

### 2.4 MoE 探索：从 Moonlight 到 K2 的稀疏化路径

Moonshot 在 2025 年完整跑通了 MoE：

- **Moonlight 16B-A3B（2025-02）**：3B 激活 / 16B 总参数，5.7T token 训练；架构沿用 DeepSeek-V3 family（细粒度专家 + 共享专家 + MLA），训练采用 Muon 优化器。论文在匹配算力下报告相对 AdamW 约 2× token 效率，机制与条件见 §6.1。
- **Kimi K2 1T-A32B（2025-07）**：61 层、384 路由专家 + 1 共享专家 + 64 注意力头 + MLA。沿 DeepSeek-V3 蓝图但做出三个关键差异化选择：
  1. **稀疏度提升至 48**（DeepSeek-V3 为 32）：8/384 激活，论文给出「sparsity scaling law」证明在固定 FLOPs 下稀疏度越高 loss 越低；
  2. **注意力头减半**（64 vs 128）：以略微 loss 退化（0.5–1.2%）换取长上下文推理速度；
  3. **取消 expert grouping**：换更小 EP=16 配合 1F1B，避免 DualPipe 的额外内存。
- **Kimi-VL 16B-A3B（2025-04）** 复用 Moonlight 架构作为语言塔；**Kimi-Linear 48B-A3B（2025-10）**则是更新一代稀疏度更高的 MoE。

| 模型 | 总参数 | 激活参数 | 路由专家数 | 共享专家 | 稀疏度 | Attention | 优化器 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Moonlight | 16B | 3B (2.8B) | — | — | 中等 | MLA | Muon |
| Kimi-VL | 16B | 2.8B + 0.4B ViT | — | — | 中等 | MLA | Muon (enhanced) |
| Kimi K2 | 1.04T | 32.6B | 384 | 1 | 48 | MLA, 64 heads | **MuonClip** |
| Kimi-Linear | 48B | 3B | — | — | 16 | KDA + MLA(NoPE) 3:1 | Muon |
| Kimi K2.5 | 1T 级 | 32B 激活 | 沿用 K2 | 1 | 48 | MLA | MuonClip + 续训 |
| **Kimi K2.6** | **1T** | **32B** | **沿用 K2** | **1** | **48** | **MLA** | **MuonClip + 续训** |

---

## 3. 推理模型：Kimi k1 / k1.5 与 K2 Thinking

### 3.1 Kimi k1（2024-11）：多模态长思考模型预览

Kimi k1 是 OpenAI o1 公布（2024-09）后业界最早的对标产品之一，与 DeepSeek-R1-Lite-Preview 同期。官方未发独立论文，从 k1.5 报告与博客可拼出技术骨架：

- 多模态原生（图像 + 文本同栈），AIME / MathVista 等多任务超越 GPT-4o；
- 长 CoT 由 SFT「激活」+ 简单 RL 强化得到；
- 这一版的最大价值是建立了**长上下文 + RL** 的研究 hypothesis，为 k1.5 铺路。

### 3.2 Kimi k1.5（2025-01-22）：长上下文 RL 的成功实践

Kimi k1.5（arXiv:2501.12599）与 DeepSeek-R1 同日（2025-01-20）开放，是 2025 年开源/半开源推理模型最重要的两份报告之一。其核心论点是：**长上下文是 RL 的另一条 scaling axis，不依赖 MCTS / Value Function / PRM 也能逼近 o1**。

#### 3.2.1 关键技术

| 技术 | 描述 | 与 R1 / o1 对比 |
| --- | --- | --- |
| **Long Context Scaling** | RL 上下文窗口扩到 **128K**，长 CoT 自然涌现规划、反思、回溯 | R1 同样长 CoT，但更强调 GRPO；o1 未公开 |
| **Partial Rollout** | 复用前次 trajectory 的大段，仅采样新 token，避免完整重算 | 创新点；R1 / o1 未公开类似机制 |
| **Online Mirror Descent (变体)** | 不用 PPO 的 clip ratio，用相对熵 KL 正则的策略镜像下降 | 与 R1 的 GRPO 不同路线，更接近经典 RLHF |
| **Length Penalty** | 显式惩罚冗余长度，缓解 overthinking | R1 让模型自发收敛；k1.5 显式约束 |
| **Curriculum + Prioritized Sampling** | 用难度标签与每实例成功率聚焦「中等难度」样本 | 类似 OpenAI o1 的样本难度策划 |
| **拒绝复杂结构** | 不用 MCTS / Value Function / Process Reward Model | 与 R1 一致：只用最终结果奖励 |

奖励目标：

$$\max_{\theta}\mathbb{E}_{(x,y^*)\sim\mathcal{D}}\Big[\mathbb{E}_{(y,z)\sim\pi_{\theta}}[r(x,y,y^*)] - \tau\,\mathrm{KL}(\pi_{\theta}(x)\,\|\,\pi_{\theta_i}(x))\Big]$$

其中 $r\in\{0,1\}$ 仅依据最终答案 $y$ 与 ground truth $y^*$ 是否一致，$\pi_{\theta_i}$ 是上一轮迭代策略，本轮目标是相对它做 KL 受限的 mirror descent。

#### 3.2.2 Long2Short：把长 CoT 蒸馏回短 CoT

k1.5 提出 **long2short** 范式来兼顾推理质量与推理成本：

- **Model Merging**：直接对 long-CoT 和 short-CoT 模型做权重平均；
- **Shortest Rejection Sampling**：多次采样取最短正确答案；
- **DPO**：以「长正确 vs 短正确」对作为 chosen，「冗长错误」作为 rejected；
- **Long2Short RL**：把 short-CoT 模型在长 CoT 数据上做带显式长度奖励的二阶段 RL。

最终 short-CoT 版本：AIME 60.8 / MATH500 94.6 / LiveCodeBench 47.3，超越 GPT-4o、Claude 3.5 Sonnet **最高 +550%**。

#### 3.2.3 多模态原生

k1.5 不是「文本模型 + 视觉适配器」，而是**文本与视觉数据联合 RL 训练**，MathVista 74.9 与 o1 持平。这一选择直接孕育了 §4 的 Kimi-VL-Thinking。

### 3.3 Kimi K2 Thinking（2025-11-06）：开源对标 GPT-5

K2 Thinking 是在 Kimi K2（base / instruct）之上做进一步的「思考态 RL」，并面向工具调用与多步任务使用：

- **架构**：1T MoE / 32B 激活，**256K 上下文窗**（K2 base 是 128K，K2 Thinking 进一步扩展并配合 YaRN）；
- **原生 INT4 推理**：在 post-training 阶段用 **Quantization-Aware Training（QAT）**对 MoE 部分做 INT4 weight-only 量化，所有公开 benchmark 均在 INT4 精度下报告，推理速度~2×；
- **Interleaved Thinking + 多步工具调用**：可在多达 **200~300 次顺序工具调用**之间穿插 thinking token，是首批具备这种能力的开源模型（同期为 MiniMax M2 2025-11-03）；
- **关键 benchmark**（INT4，官方）：
  - Humanity's Last Exam（HLE，with tools）：**44.9%**
  - BrowseComp：**60.2%**
  - SWE-Bench Verified（base K2 已达 65.8%）等。

### 3.4 与 DeepSeek-R1 的异同

| 维度 | Kimi k1.5 / K2 Thinking | DeepSeek-R1 / R1-Zero |
| --- | --- | --- |
| RL 算法 | Online Mirror Descent + KL 正则 | GRPO（Group Relative Policy Optimization） |
| 长上下文 | **核心维度**，RL 阶段直接扩到 128K-256K | 长 CoT 自然涌现，未把 context 当 scaling axis |
| 价值函数 / PRM | 不使用 | 不使用 |
| Long2Short | **显式系统化方法**（merge / DPO / 长度奖励 RL） | 主要靠 R1 → 蒸馏小模型 |
| 多模态原生 | **是**（文本+视觉联合 RL） | R1 仅文本 |
| 架构 | k1.5 多模态稠密 → K2 Thinking 1T MoE+MLA | R1 用 V3 671B MoE+MLA |
| 优化器 | Muon → MuonClip | AdamW |
| 量化 | K2 Thinking 原生 INT4 QAT | 后置量化 |

> **结论**：k1.5 与 R1 是 2025 年 1 月开源推理模型的「双子星」。R1 重在 RL 算法（GRPO + R1-Zero 纯 RL 路线）；Kimi 重在**长上下文 RL + 多模态 + Long2Short 工程闭环**。两条技术线后续相互渗透——K2 Thinking 已经在算法上吸收了部分 GRPO 思想，DeepSeek 后续模型也开始重视长上下文与稀疏注意力。

---

## 4. 多模态模型：Kimi-VL / Kimi-VL-Thinking / Kimi-Audio

### 4.1 Kimi-VL（2025-04）：高效 MoE 视觉语言模型

Kimi-VL（arXiv:2504.07491）是 Moonshot 第一份正式的 VLM 技术报告，使用 2.8B+0.4B 激活参数的 MoE 结构，并报告与 GPT-4o-mini、Qwen2.5-VL-7B、Gemma-3-12B-IT 的比较结果。

#### 4.1.1 架构三件套

```
图像  →  MoonViT (400M, native resolution)  →  Pixel-Shuffle 2×2  →  2-layer MLP  →  Moonlight MoE (16B/2.8B-A3B)
```

- **MoonViT（原生分辨率视觉编码器）**：吸收 NaViT 的 packing 思想——将不同分辨率的图像切 patch、展平、序列拼接，因此可与 LLM 共享 FlashAttention 这类变长序列注意力 kernel。**不需要 LLaVA-OneVision 风格的 sub-image 切块/拼接**。
- **MLP Projector**：先 pixel-shuffle 把 2×2 空间维度折到通道维（特征数 ×4，序列长度 ÷4），再两层 MLP 映射到 LLM hidden。
- **Moonlight MoE 解码器**：16B/2.8B-A3B，结构同 DeepSeek-V3 family；从 Moonlight 中间 checkpoint（5.2T token、8K 上下文）继续训。

> **MoE 应用于 VLM 是 Kimi-VL 的关键差异点**：相比同期主流 dense VLM（Qwen2.5-VL-7B、Gemma-3-12B），它在 24 个 benchmark 中 19 项超越 Qwen2.5-VL-7B（后者激活 2.59× 参数），证明 MoE 路线在 VLM 上同样有效。

#### 4.1.2 训练策略：四阶段共 4.4T token

| 阶段 | 数据 | 序列长度 | 可训练 |
| --- | --- | --- | --- |
| ViT 训练 | Alt-text + 合成 caption + grounding + OCR (2.1T) | 8192 | 仅 ViT |
| 联合预训练 | + 文本/知识/交错图文/视频/Agent (1.4T) | 8192 | ViT + LLM |
| 联合 cooldown | + 高质量文本与多模态、学术语料 (0.6T) | 8192 | ViT + LLM |
| **联合长上下文激活** | 长文本/长视频/长文档 + 25% 长 + 75% 短 (0.3T) | **32K → 128K** | ViT + LLM |

最后一阶段把 RoPE base 从 50,000 → 800,000，分两段 4× 扩展。NIAH（Needle-in-a-Haystack）测试在 128K 文本/视频上检索准确率仍 ≥87%/91.7%。

#### 4.1.3 Kimi-VL-Thinking：原生多模态思考

在 Kimi-VL 之上：
1. **Long-CoT SFT**：用长链思考监督微调，激活长思考能力；
2. **RL（同 k1.5）**：online mirror descent + KL 正则 + 长度奖励 + 课程/优先级采样；最终在 MMMU 61.7、MathVision 36.8、MathVista 71.3 全面对标更大模型。

这是与「外接 reasoning 模块」截然不同的范式：**视觉与思考过程在同一个模型内端到端 RL 训练**，与 OpenAI o1（视觉版）思路一致，但开源、且只用 2.8B 激活参数。

### 4.2 Kimi-Audio（2025-04）

Kimi-Audio（arXiv:2504.18425）是 Moonshot 的音频基础模型，7B 参数，基于 Qwen2.5-7B 并融合 Whisper 编码思路，统一支持 ASR、AQA（音频问答）、TTS、音频对话等。它与 Kimi-VL 同月发布，构成 Moonshot 多模态矩阵的语音侧。

### 4.3 Kimi K2.5 / K2.6：原生多模态 Agent

- **Kimi K2.5（2026-01-27）**：在 K2（纯文本）基础上做约 **15T 视觉 + 文本混合 token 的 continual pretraining**，定义「Visual Agentic Intelligence」——同一个 1T MoE 同时承担文本推理、视觉理解、多步 Agent 执行；强调视觉编码（screenshots、UI、图表）下的 Agent 行为。支持 **Agent Swarm 100 子代理** 协同。
- **Kimi K2.6（2026-04-20）**：开源发布，1T 参数 / 32B 激活 MoE，**256K 上下文**，采用 **Modified MIT License**。关键指标：
  - **SWE-Bench Verified 80.2%**（作者报告）；
  - **SWE-Bench Pro 58.6%**——与 GPT-5.5 持平；
  - **Agent Swarm 300 子代理 / 4000 步**——面向超长程软件工程任务；
  - 官方披露可**连续编码 13 小时**；
- **Kimi Code K2.6（2026-04-13）**：编码代理工具，面向 IDE 集成与自动化软件工程。
- **视频输入支持**：新增 mp4、mov、webm、avi 格式视频输入能力。
- **Claw Groups（研究预览）**：异构代理集群（Heterogeneous Agent Cluster），支持不同类型 Agent 协同完成复杂任务。

至此，Moonshot 的多模态路线呈现「**小而强（VL/Audio 单独发版）→ 大而全（K2.5 单一旗舰原生多模态）→ 开源旗舰（K2.6 开源 + 编码工具）**」的演进。

### 4.4 Kimi K2.7 Code（2026-06-11）：编程向旗舰，K2.6 之上继续训练

> **证据等级：精读原文（官方模型卡 + 官方产品页原文）**。本节所有数字均来自 [HuggingFace 模型卡 `moonshotai/Kimi-K2.7-Code`](https://huggingface.co/moonshotai/Kimi-K2.7-Code) 与 [kimi.com 官方资源页](https://www.kimi.com/resources/kimi-k2-7-code)（页面标注「更新于 2026-10-08」），属**厂商自报**，非第三方复现。

**发布信息**

- **日期**：HuggingFace 仓库 `createdAt = 2026-06-11`、`lastModified = 2026-06-15`（取 HF API 元数据）；官方产品页仅给「更新于 2026-10-08」，未给首发日，故本节以 HF 仓库创建日 2026-06-11 作为可核验的最早公开时间点。
- **命名与形态**：`Kimi K2.7 Code`，**开源权重**（license 为 *Modified MIT*，HF `license_name: modified-mit`）。
- **与 K2.6 的关系（官方原文）**：「a coding-focused agentic model built upon Kimi K2.6」，且「has the same architecture as Kimi-K2.5/Kimi-K2.6, and the deployment method can be directly reused」——即**同架构、纯后训练/续训产物**，不是新基座。

**规格（官方模型卡，逐项）**

| 项 | 取值 |
| --- | --- |
| 架构 | MoE |
| 总参数 / 激活参数 | 1T / 32B |
| 层数（含稠密层） | 61（稠密层 1） |
| 注意力 | MLA，hidden 7168，64 头 |
| MoE | 每专家 hidden 2048，384 专家，每 token 选 8，共享专家 1 |
| 词表 / 上下文 | 160K / 256K |
| 激活函数 | SwiGLU |
| 视觉编码器 | MoonViT，400M |
| 量化 | 原生 INT4（沿用 Kimi-K2-Thinking 的方法） |

**能力与基准（官方自报，附条件）**

评测条件（模型卡脚注 1 原文要点）：K2.7 Code 与 K2.6 均以 **Kimi Code CLI、开启思考模式、`temperature=1.0`、`top_p=0.95`、262,144 token 上下文**评测；GPT-5.5 在 **Codex（xhigh）**、Claude Opus 4.8 在 **Claude Code（xhigh）**；除上述差异外各基准条件一致。

| 基准 | Kimi K2.6 | **Kimi K2.7 Code** | GPT-5.5 | Claude Opus 4.8 | 基准性质 |
| --- | --- | --- | --- | --- | --- |
| Kimi Code Bench v2 | 50.9 | **62.0** | 69.0 | 67.4 | Moonshot 内部基准 |
| Program Bench | 48.3 | **53.6** | 69.1 | 63.8 | 公开（200 任务，248k+ fuzz 行为测试） |
| MLS Bench Lite | 26.7 | **35.1** | 35.5 | 42.8 | 公开（官方 30 任务子集） |
| Kimi Claw 24/7 Bench | 42.9 | **46.9** | 52.8 | 50.4 | Moonshot 内部（17 场景 / 610 评分点） |
| MCP Atlas | 69.4 | **76.0** | 79.4 | 81.3 | 公开（500 任务子集，100 次工具调用预算） |
| MCP Mark Verified | 72.8 | **81.1** | 92.9 | 76.4 | 公开（人工核验版，100 步预算） |

**与前代的可判定差异**

1. **编码基准全面上移**：Kimi Code Bench v2 +21.8%（50.9→62.0）、Program Bench +11.0%、MLS Bench Lite +31.5%——三者均为官方同条件对照，可判定。
2. **Agent 基准约 +10%**：Kimi Claw 24/7、MCP Atlas、MCP Mark Verified 三处同向提升（官方口径「约提升 10%」）。
3. **推理效率**：思考 token 用量较 K2.6 **平均减少约 30%**（官方自报；同一或更高得分配更少 token，属可判定的效率变化，但**未给出 token 计数的绝对测量口径**）。
4. **强制思考**：不支持非思考模式，`thinking` 与 `preserve_thinking` 均强制为 True；在 Kimi Code 里若请求关闭思考，**会自动改由 K2.6 提供服务**。

**失效边界**

- **定位是编程专用**：官方明确「对于写作、分析、对话等通用场景，我们推荐能力更均衡的 K2.6」——用 K2.7 Code 做通用对话不是它的设计目标。
- **仍落后闭源前沿**：MLS Bench Lite 35.1 vs Opus 4.8 的 42.8；Kimi Code Bench v2 62.0 vs GPT-5.5 69.0；MCP Mark Verified 81.1 vs GPT-5.5 92.9。
- **视频输入受限**：模型卡注明「Chat with video content is an experimental feature and is only supported in our official API for now」——第三方 vLLM/SGLang 部署下视频输入不可用（或仅实验）。
- **无独立技术报告**：截至 2026-10-17，未检索到 K2.7 Code 的 arXiv 技术报告，架构层面的解释只能回落到 K2.6 的公开信息（见 §4.3）。

上下文窗口为 262,144 tokens。

### 4.5 Kimi K3：KDA、AttnRes 与 Stable LatentMoE 的旗舰级组合

> **证据等级：精读原文（技术报告全文 + 官方模型卡 + 官方博客）**。arXiv:2607.24653 正文（HTML 全文 38 张表/图）已逐节读取；所有评测数字来自报告 §6/模型卡，属**厂商自报**，第三方结论单列为转引。

技术报告固定引用 arXiv `2607.24653v2`；论文表格给出的精确规模是 **2.78T 总参数、104.2B/token 激活**，摘要与模型卡将其四舍五入为 2.8T/104B。产品/API 于 2026-07-16 上线，官方博客称完整权重于 7 月 27 日前发布；权重仓使用名为 **Kimi K3 License** 的许可，具体条款未逐条核验（见 §4.6）。[技术报告 v2](https://arxiv.org/abs/2607.24653v2) · [官方发布说明](https://www.kimi.com/en/blog/kimi-k3)

模型卡列出的 modality 为 Text、Image；官方博客还称模型可处理 video，但本次来源未确认该能力在模型卡/API 的完整开放范围。论文报告的预训练上下文窗口为 **1,048,576 tokens**。

**规格（K3 模型卡，与 K2 的官方对照见表内「K2」列，数据出自技术报告 Table 1）**

| 项 | Kimi K2 | **Kimi K3** | 变化 |
| --- | --- | --- | --- |
| 层数 | 61 | **93** | +52% |
| 总参数 | 1.04T | **2.78T** | +167% |
| 激活参数 | 32.6B | **104.2B** | +220% |
| Hidden | 7,168 | 7,168 | 不变 |
| Latent MoE 维度 | — | **3,584（0.5×）** | 新增 |
| 每专家 MoE hidden | 2,048 | **3,072** | +50% |
| 路由专家 / 每 token 激活 / 共享专家 | 384 / 8 / 1 | **896 / 16 / 2** | +133% / +100% / +100% |
| 注意力头 | 64 | **96** | +50% |
| 注意力层构成 | MLA 全层 | **69 KDA + 24 Gated MLA**（3:1） | 架构变更 |
| 预训练上下文 | 128K | **1M** | 8× |
| 视觉编码器 | MoonViT 400M | **MoonViT-V2 401M**（27 层） | 从零训练 |
| 激活函数 | SwiGLU | **SiTU-GLU**（β₁=4, β₂=25） | 架构变更 |
| 量化 | — | **MXFP4 权重 / MXFP8 激活**（QAT 自 SFT 起） | 新增 |
| 词表 | 160K | 160K | 不变 |
| 位置编码 | RoPE/YaRN | **NoPE（全 MLA 层）** | 架构变更 |

**四项架构改动（逐项可判定，非营销口径）**

1. **KDA 的下界衰减（lower-bounded decay）**：Kimi Linear 用无界负 Softplus `g = −e^A·Softplus(z)`，导致 chunk 内倒数累积衰减 `1/Γ` 可能溢出，对角线 tile 只能用逐 position-pair 计算。K3 改为 `g = g_min·Sigmoid(e^A z)`、固定 `g_min = −5`，使每个保留因子 `α > e^{-5} ≈ 6.7×10^{-3}`、16-token tile 的累积 log-decay 落在 `(−80, 0)`、倒数缩放因子 `< e^80` **留在 BF16 动态范围内**——于是对角线与非对角线 tile 都能走 Tensor Core 稠密矩阵乘，**彻底移除 position-pair 路径**。这是「数学上改一处参数化，工程上拿掉一类 kernel」的典型案例。
2. **Attention Residuals（AttnRes，深度方向的注意力）**：把 residual 从「累加」改成「对 embedding + 所有前序层输出做注意力」。K3 用 **Block AttnRes**：93 层切成 8 个 12 层 block（+ embedding 共 9 个源），块内求和、跨块做全注意力；显存/通信从 `O(Ld)` 降到 `O(Nd)`，推理期可借 online softmax 把「并行块间结果」与「串行块内部分和」合并。
3. **Stable LatentMoE（896 专家 / 16 激活，稀疏度 56）**：三件套解决极端稀疏的两个失效模式——① routed 分支 `W↓ → 门控专家 FFN → W↑` 近似四次连乘导致激活爆炸 → 在 up-projection 前插 **RMSNorm** 并换 **SiTU-GLU**（`β tanh(x/β)` 软钳位，输出满足 `|f(x)| ≤ β₁β₂ = 100`，而 SwiGLU 无界）；② 896 专家的负载均衡超出 aux-loss-free 固定步长 bias 更新的稳定区间 → 换 **Quantile Balancing（QB）**：直接按 router score 分位数设 bias（`−quantile_{1−k/n}(s_{:,j} − α)`），并用**直方图估计**把全 batch 分位数的通信成本压到每专家几百个 bin。
4. **Per-Head Muon**：把 Q/K/V 投影的动量矩阵按 head 分块做 Newton–Schulz 正交化，避免大尺度 head 主导共享更新方向；官方称训练更稳、且优化器开销略降。

**预训练与其可迁移结论**

- **数据**：Web Text / Code / Mathematics / Knowledge 四域 + 大规模视觉语料（caption、图文交错、OCR、感知、视频、**视觉编程数据**：SVG / 3D 资产 / Webpage / Game / CAD）；沿用 K2 的 rephrase 配方（风格/视角多样化 prompting + chunk-wise 自回归 + 对源文档的保真校验）。
- **Scaling law 结论（可直接引用的一条）**：在**各自独立重调超参**（batch size、LR、TPP、model shape）后，**cosine decay 一致优于 WSD**；官方特别指出「用同一套超参比较两种 schedule 会不公平地偏向某一方」。这条对做训练 recipe 选择的人有直接价值。
- **相对 K2 的 scaling 效率约 2.5×**（held-out OOD 验证集上的拟合曲线）。
- **上下文课程（四阶段）**：预训练 8K → 64K；cooldown 阶段 256K → 1M。因全程 **NoPE**，扩到 1M **不需要**改 RoPE 基频、不需要 YaRN 类插值——这是与 K2 长上下文扩展路径的**结构性差别**（K2 依赖 YaRN）。
- **长上下文数据不是「拼长」**：官方承认长文档/长视频质量低（近似重复、二进制块、截断文件、无效日志），因此做去重 + 帧级感知哈希 + 结构校验；并**合成「只有跨 1M 全窗口取信息才能解」的置换拼接任务**，防止注意力退化成局部模式。

**后训练（三段式，架构差异之外的关键）**

`SFT（XTML 模板 + QAT）→ RL（3 域 × 3 档 effort = 9 个专家模型）→ multi-teacher on-policy distillation（MOPD）合并为单一模型`。

- **3 域**：general（经验/视觉/推理/忠实性/搜索/知识工作）、general agents（长程助手/深度研究/段落级写作）、coding agents（SWE/编码体验/kernel/Web 开发）。
- **effort 控制**：给每题一个由 cold-start 模型估计的 token 预算 `b₀(x)`，超 `τ·b₀(x)` 直接给 −1 奖励；先训大 τ 的 max 档，再退火 τ 得 high/low 档。**注意**：发布时 low/high 档尚未上线（官方博客原文「low- and high-effort modes to be introduced in subsequent updates」）。
- **RL 环境侧的新东西**：统一白盒 RL 环境（把 harness 拆成工具接口/系统提示/上下文管理/skills/memory/subagent 等可配置模块，可实例化 Kimi Code、Claude Code、Codex、OpenClaw、Hermes 等）以**防止对单一 harness 过拟合**；知识图谱驱动的任务合成；kernel 优化任务（含**反 reward hacking 检测**，惩罚 CUDA graph replay / 输入缓存 / 降精度）；mock 版 Gmail/Notion/Slack/Canvas 的个人助理长程任务；**AET（Autonomous Execution Tasks）**——奖励只认 verifier 对最终环境状态的判定，不认模型自述完成。

**基础设施（三条，与「3T + 1M + agentic」一一对应）**

1. **KDA 的算法-系统协同**：融合 kernel、**KDA Context Parallelism**（跨设备切序列）、**state-aware prefix caching**（KDA 是递推状态，常规 prefix cache 不适用）；已向 vLLM 社区提交对应实现。
2. **MoonEP**（独立仓库 `MoonshotAI/MoonEP`，2026-07-24 创建）：静态计算形状 + 零拷贝通信的**完全均衡**专家并行，关键路径上无主机同步。
3. **1M agentic RL**：partial rollout + 外部 KV-cache 保留 + 自适应限流 + **可恢复 microVM 沙箱**，让单条长轨迹跨多个训练迭代而不丢状态。

**部署侧**：MXFP4/MXFP8 QAT（从 SFT 起，rollout 与训练同量化，消除训练-推理失配）；把预训练的 MTP 层微调成 **EAGLE-3 draft**，直接用**接受率的负对数（LK loss）**优化而非 KL 代理；融合 1st / 4th / 末个 AttnRes block 的低/中/高层特征做 draft 输入。官方建议部署在 **64 卡以上的 supernode** 配置上。

**评测（厂商自报；条件决定分数含义）**

模型卡报告的 K3 结果统一使用 **max reasoning effort、`temperature = 1.0`**；单步任务 `top_p=0.95`，agentic 任务 `top_p=1.0`。各基准使用 Kimi Code、Claude Code 或 Codex 等不同 harness，因此数字反映模型、运行器和基准协议的组合，不是纯架构测量。代表性结果包括 GPQA Diamond 93.5、HLE-Full 无工具/带工具 43.5/56.0、DeepSWE 67.5（Kimi Code；mini-SWE-agent 下 67.3）和 SWE-Marathon 42.0（H20 校准分支）。MLS-Bench-Lite 的 48.3 来自 H20 上 3 次运行，而官方设定为 H100；Kimi Code Bench 2.0 是内部基准，换 Claude Code harness 后为 73.7。最能说明协议影响的是 BrowseComp：300K 触发上下文压缩时为 91.2，完整 1M 不压缩时为 90.4。其余主表、对照模型和成本比较不纳入本报告的技术结论；逐项条件见 [K3 精读分册](papers/2607.24653-kimi-k3.md)。

**失效边界（官方明示 + 本报告判断）**

1. **对 thinking history 高度敏感（官方明示）**：K3 在 *preserved thinking history* 模式下训练。harness 若未按要求回传全部历史思考内容，或把别的模型正在进行的会话中途切到 K3，**生成质量会高度不稳定**。官方建议只用已验证兼容的 harness（如 Kimi Code），且不要中途切换。
2. **过度主动（excessive proactiveness，官方明示）**：长程任务训练导致模型遇到小问题/歧义意图时**替用户做决定**。需要边界严格的应用应在 system prompt / AGENTS.md 中显式约束。
3. **规模与复现门槛**：权重公开不等于个人可部署。技术报告推荐 ≥64 加速器 supernode 配置；完整 2.78T 参数规模与 MXFP4 权重仍带来很高的硬件门槛，复现实验需记录具体集群配置。
4. **effort 档位不完整**：模型卡评测使用 max 档；这些数字不能外推到 low/high effort 或默认产品设置。

### 4.6 未确证与待跟踪（2026-06 以来）

以下条目**未进入正文**，仅登记待核：

| 事项 | 现状 | 处置 |
| --- | --- | --- |
| Kimi K3 License 具体条款 | 模型卡只给「Kimi K3 License」名称，未列条款 | 待读 LICENSE 原文；在读到前不称「OSI 许可」/「可商用」 |
| K3 视频输入的产品化范围 | 博客称同一模型理解视频；模型卡 `Modality` 仅列 Text, Image | 正文已按「模型卡列 Text/Image」表述，视频部分标注未确认 |
| K3 第三方评测原始记录 | AA 57.1 / Vals 74.7% 仅有官方技术报告的转述 | 需直接抓 AA / Vals 页面；未抓到前按二手处理 |
| K3 的 low / high effort 档 | 官方称「后续更新引入」 | 待官方上线后补数字 |
| K2.7 Code 的思考 token −30% | 只有相对百分比，无绝对 token 计数口径 | 待官方补测量方法（当前无法自行复现） |
| Complex KDA（arXiv:2609.24797，2026-09-21） | 独立团队（OpenEuroLLM）对 KDA 表达力的改进：把门控放开到 `[−1,1]`、`β ∈ [0,2]`，使单个 delta-rule 转移实现 2D 旋转，声称达到 DeltaProduct₂ 的状态跟踪表达力 | **不是 Moonshot 的模型发布**，故不写入正文；仅登记为 KDA 路线的外部研究跟进 |
| K3 的 MoE 负载均衡收益在推理期的表现 | 技术报告给出训练侧 QB 机制与证明，推理期 bias 冻结 | 推理期是否仍需调 bias、对吞吐的影响未披露 |

---

## 5. 跨代技术演进分析

### 5.1 三条主线的合流

```
长上下文        2023.10 200K  →  2024.03 2M  →  2025.02 MoBA  →  2025.10 KDA
                                   │                │              │
                                   └──── 共享 Infra ─┴──────────────┤
                                                                    │
推理            2024.11 k1  →  2025.01 k1.5  →  2025.11 K2 Thinking ┤
                              (RL+128K)         (1T MoE+256K+INT4) ─┤
                                                                    │
基座 / MoE      2025.02 Moonlight  →  2025.07 K2  →  2026.01 K2.5 ──┘
                (16B-A3B, Muon)     (1T-A32B,        (原生多模态)
                                     MuonClip)
```

至 K2 Thinking / K2.5 阶段，三条主线收敛于同一个 1T MoE backbone：长上下文（256K）、推理（thinking）、多模态（K2.5）皆基于同一架构。

### 5.2 注意力机制演进

| 时代 | 模型 | 注意力 | 位置编码 | KV 复杂度 |
| --- | --- | --- | --- | --- |
| 2023-2024 | Moonshot-v1 | 多头全注意力 | RoPE | O(n) |
| 2024-2025 | Moonlight / Kimi-VL / K2 | **MLA** (DeepSeek-V3 风格) | RoPE | O(n)，但 latent 压缩 |
| 2025-Q1 | Kimi 线上长上下文 | **MoBA** | RoPE | O(n)，常数小 |
| 2025-Q4 | Kimi-Linear | **KDA(3) + MLA-NoPE(1)** 混合 | KDA 内禀位置 + MLA NoPE | KDA O(1)，混合显著低于 MLA |

这些工作显示 Moonshot 作者参与了不同注意力路线的研究：Moonlight/K2 使用 MLA，MoBA 探索块级稀疏注意力，Kimi Linear 研究 KDA 与 MLA 的混合。作者重叠能说明研究之间存在人员联系，但不能据此推断它们构成一条统一规划的“完整谱系”；具体机制和实验结论仍应分别按各论文阅读。

### 5.3 训练优化器：Muon → MuonClip

Moonlight 论文研究了 Muon 在 16B-A3B 模型训练中的使用，K2 论文则讨论了 MuonClip 对注意力 logit 稳定性的处理。两项工作提供了从优化器缩放实验到大规模 MoE 训练的案例；它们不足以把规模化归功于单一团队或单一优化器，机制与实验条件见 §6.1–§6.2。

### 5.4 后训练范式

| 代际 | SFT | RL | 偏好 / 自评 | 工具 / Agent |
| --- | --- | --- | --- | --- |
| Moonshot-v1 | 标准指令 SFT | RLHF (PPO 类) | RM | 简单工具 |
| k1.5 / Kimi-VL-Thinking | 长 CoT SFT | **Online Mirror Descent + KL** + Length Penalty | 结果奖励 (0/1) | 多模态 |
| K2 (Instruct) | 大规模 Agentic SFT（合成 20K+ 工具，多 Agent 轨迹） | **Verifiable Rewards Gym + Self-Critic Rubric** | 自评成对比较 | **20K+ 合成工具**，K8s sandbox 1 万并发 |
| K2 Thinking | + Long-CoT thinking SFT | + Interleaved-thinking RL | + Faithfulness Judge | **200-300 步顺序工具调用** |
| K2.5 / K2.6 | + 视觉 Agent SFT | + 多 Agent 协同 RL | — | **300 子 Agent 集群、13h 连续编码、SWE-Bench 80.2%** |

后训练每代迭代的「门」是 Agent / 工具调用复杂度的指数级增长。

---

## 6. 关键创新点详述

### 6.1 Muon 优化器：从 100M 玩具到 16B MoE（Moonlight 论文）

**Muon**（Jordan 等，2024）原本是基于 Newton-Schulz 矩阵正交化的小规模优化器。Moonlight 论文（arXiv:2502.16982）做了三项关键工作把它推上主流：

1. **加权重衰减（Weight Decay）**：原始 Muon 不带 weight decay，scaling 到 800M+ 时观察到权重 RMS 持续增长甚至超出 bf16 高精度区间；引入 AdamW 风格 $\mathbf{W}_t = \mathbf{W}_{t-1} - \eta_t(\mathbf{O}_t + \lambda\mathbf{W}_{t-1})$ 后既稳定又能在 over-train regime 优于 AdamW。
2. **一致性 Update RMS**：证明对 $[A,B]$ 形状参数 Muon 理论 update RMS 为 $\sqrt{1/\max(A,B)}$，提出乘以 $\sqrt{\max(A,B)}$ 修正，并整体缩放至 0.2 与 AdamW 匹配——使 Muon 可**直接复用 AdamW 调好的学习率与 weight decay**，不需重新调参。
3. **分布式 Muon**：基于 ZeRO-1 分片，引入 DP-Gather 收集完整梯度矩阵 → Newton-Schulz 迭代 → 丢弃非本地分片；通信开销仅为 AdamW 的 1×~1.25×，实际训练里几乎无显著 overhead；BF16 通信进一步省 50%。

Scaling-law 实验显示 **Muon 仅需 ~52% AdamW 的 FLOPs 即可达到等效性能**。Moonlight 16B-A3B 用 Muon 训 5.7T token，在 MMLU、HumanEval、GSM8K 等推到当时同档 Pareto 前沿。

### 6.2 MuonClip：QK-Clip 解决万亿规模注意力 Logit 爆炸

K2 论文（arXiv:2507.20534）发现：在 9B-A53B 的 MoE 中训练时 Muon 仍会让 attention logits 爆到 1000+，而 AdamW 不会；这说明 Muon 的「token efficiency 优势」与「logit 不稳定」相伴而生。

**MuonClip = Muon + QK-Clip**：

1. 每步前向算每头最大 logit $S_{\max}^h = \frac{1}{\sqrt{d}}\max_{X\in B}\max_{i,j}\mathbf{Q}_i^h\mathbf{K}_j^{h\top}$；
2. 若 $S_{\max}^h > \tau$（K2 用 $\tau=100$），按 $\gamma_h = \tau/S_{\max}^h$ 对 $\mathbf{W}_q^h, \mathbf{W}_k^h$ 做权重重缩放（**逐头**而非全局，干预最小化）；
3. 对 MLA 的特殊情况：
   - 头特定的 $q^C, k^C$：各乘 $\sqrt{\gamma_h}$
   - 头特定的旋转 $q^R$：乘 $\gamma_h$
   - **共享 rotary $k^R$ 不动**（避免跨头串扰）

K2 在此基础上 15.5T token 全程**零 loss spike**——这是 1T 级开源 MoE 训练史上最干净的 loss 曲线之一，也是 MuonClip 最重要的产业级证明。

### 6.3 Kimi K2 的 Agentic 数据合成与 RL

K2 的非思考态 SoTA（SWE-Bench Verified 65.8、Tau2-Bench 66.1、ACEBench-EN 76.5）主要来自三方面：

#### 6.3.1 大规模 Agentic 数据合成

- **工具规格生成**：3000+ 真实 MCP 工具（GitHub） + 通过 hierarchical domain evolution 合成 **20,000+ 合成工具**；t-SNE 显示二者在工具空间互补覆盖；
- **Agent 多样化**：上千 system prompt × 工具组合 = 数千 agent；
- **Rubric-based 任务生成**：每个任务带显式 rubric（成功标准、期望工具调用 pattern、检查点）；
- **多轮轨迹生成**：LLM 模拟用户 + LLM 模拟工具执行环境（带状态、有控制随机性的成功/部分失败/边界）；
- **质量过滤**：LLM-as-judge 按 rubric 筛选高质量轨迹用于 SFT。

#### 6.3.2 通用 RL：Verifiable Rewards Gym + Self-Critic Rubric

- **可验证奖励**（数学/STEM/编程）：用 SFT 模型 pass@k 选「中等难度」样本，避免太易 / 太难产生稀疏信号；
- **复杂指令遵循**：双路径——代码执行验证 + LLM-as-judge + hack-check 防伪；
- **Faithfulness Judge**：句子级事实核查 reward model；
- **Self-Critic Rubric Reward**：对创意写作 / 开放问答这类没有 ground truth 的任务，让模型自己做成对比较打分；
- **统一 Gym-like 框架**：一套 RL 框架同时容纳数学、代码、SWE、指令遵循、创意写作。

#### 6.3.3 训练 Recipe（K2 Pre-train）

- 4096 token 上下文 + WSD（warm-stable-decay）学习率，500 步 warmup → 10T token 恒定 2e-4 → 5.5T token cosine decay 到 2e-5；
- 长上下文激活：4K → 32K → **YaRN 扩到 128K**；
- 16-way PP + 16-way EP + ZeRO-1 DP + 选择性重计算 + FP8 存储非敏感激活 + Activation CPU Offload；H800 集群。

### 6.4 Kimi K2 Thinking 的原生 INT4 QAT

K2 Thinking 在后训练阶段对 MoE 部分做 **INT4 weight-only QAT**，所有公开 benchmark 直接报告 INT4 数字。这一点的工程意义大于学术意义：

- **公平性**：用户看到的就是部署版本性能；
- **训练 RL 长序列友好**：INT4 让 thinking RL 在长 trace 上的显存压力减半；
- **2× 推理加速** + 无明显精度损失，进一步扩大开源模型在「免费 + 廉价部署」上的优势。

### 6.5 Kimi Linear / KDA 的细节亮点

- **更细粒度门控**：Gated DeltaNet 是「per-channel scalar gate」，KDA 进一步引入 row-wise / column-wise / element-wise 多层次门控；
- **delta-rule 改进**：在原 delta 规则基础上增加 forget term，避免长序列下 key-state 退化；
- **NoPE for MLA**：取消 MLA 层的 RoPE，把位置编码完全交给 KDA 的递归状态——这背后假设是：**全局层只需要做内容聚合，位置由局部递归层负责**，与早期「Hybrid Mamba」思想类似但更彻底；
- **3:1 比例并非随意**：消融实验显示 3:1 是性能/效率 Pareto 最优。

---

## 7. 与同期对手的横向比较

| 维度 | Kimi (Moonshot) | DeepSeek | Qwen (阿里) | OpenAI | Anthropic |
| --- | --- | --- | --- | --- | --- |
| 最大开源旗舰 | **K2 / K2 Thinking 1T MoE**；2026-07 起为 **K3 2.8T MoE（104B 激活）** | DeepSeek-V3 / R1 671B MoE | Qwen3-MoE 系列 | gpt-oss | 不开源 |
| 推理模型路线 | **长上下文 RL + Mirror Descent** | GRPO + R1-Zero | QwQ / Qwen3-Thinking | o1/o3/o4/GPT-5 | Claude with Extended Thinking |
| 长上下文创新 | **MoBA + KDA**（K3 起 KDA 全面替代 MLA 主体，仅保留 24 层 Gated MLA） | NSA / DeepSeek-V3.2 sparse | Dual-Chunk / YaRN 扩展 | 未公开 | 内部技术 |
| 优化器创新 | **Muon → MuonClip → Per-Head Muon** | AdamW | AdamW | 未公开 | 未公开 |
| 多模态 | Kimi-VL（MoE 2.8B-A3B）+ Audio + K2.5（原生）+ **K3（原生，从零训练 MoonViT-V2）** | DeepSeek-VL2 | Qwen-VL / Qwen2.5-VL（强力） | GPT-4o / GPT-5 | Claude 3.5 Sonnet+ |
| 量化 | **K2 Thinking 原生 INT4 QAT**；**K3 为 MXFP4 权重 / MXFP8 激活 QAT（自 SFT 起）** | 后置量化 | GPTQ / AWQ | 黑盒 | 黑盒 |

从公开论文看，Moonshot 的工作分别涉及优化器（Muon/MuonClip）、注意力（MoBA/KDA）和长上下文推理。它们可作为不同问题线的研究案例；现有公开材料不足以据此给公司整体技术路线排位，也不能把不同团队概括成单一“工程文化”。

---

## 8. 跨论文综合与阅读路径

公开工作可以沿三条问题线理解，但不能将时间上的连续性直接当作统一的团队计划或因果关系：

1. **长上下文形成一条可读的技术线索**——公开工作从 RoPE 外推、MoBA 块级稀疏注意力延伸到 KDA 与 MLA 的混合设计；这说明团队持续研究长序列的计算与缓存约束，但不能仅由产品窗口推断每代机制都以相同目标优化。
2. **训练效率需要拆成不同问题**——Muon 论文研究优化器的训练计算预算，MuonClip 处理大规模训练中的 logit 稳定性，K2 的数据重写则改变训练样本组织。它们的收益指标与实验条件不同，不宜合并成单一“token 利用率”结论。
3. **推理与 Agent 训练的接口**——k1.5 的强化学习、K2 的 Agentic 数据、K2 Thinking 的 interleaved tool-use、K2.5 的视觉 Agent 分别涉及不同训练与任务设置。把它们串读有助于比较训练轨迹、工具反馈和多模态观测如何进入模型；现有跨代材料不足以证明这些组件始终作为同一联合目标优化。

这条技术路线从长上下文产品工程扩展到稀疏注意力、KDA、Muon 系列优化器和 agentic 后训练。本报告将这些机制按其对应论文和模型实验分别讨论；跨论文出现相同组件，不单独证明其贡献可迁移或解释整代模型收益。

---

## 9. 参考文献

### 9.1 Moonshot AI 一作论文（核心）

1. **Kimi k1.5: Scaling Reinforcement Learning with LLMs**, Kimi Team, arXiv:2501.12599 (2025-01).
2. **Kimi-VL Technical Report**, Kimi Team, arXiv:2504.07491 (2025-04).
3. **Kimi K2: Open Agentic Intelligence**, Kimi Team, arXiv:2507.20534 (2025-07).
4. **Muon is Scalable for LLM Training (Moonlight)**, Liu et al. (Kimi Team), arXiv:2502.16982 (2025-02).
5. **MoBA: Mixture of Block Attention for Long-Context LLMs**, Lu et al. (Kimi Team), arXiv:2502.13189 (2025-02).
6. **Kimi Linear: An Expressive, Efficient Attention Architecture**, Zhang et al. (Kimi Team), arXiv:2510.26692 (2025-10).
7. **Kimi-Audio Technical Report**, Kimi Team, arXiv:2504.18425 (2025-04).
8. **Kimi K2.5: Visual Agentic Intelligence**, Kimi Team, arXiv:2602.02276 (2026-01).
9. **Kimi K2.6: Open Agentic Intelligence v2**, Kimi Team, arXiv:2604.20534 (2026-04).
10. **Kimi Code K2.6 Technical Report**, Kimi Team, arXiv:2604.18425 (2026-04).
11. **Kimi K3: Open Frontier Intelligence**, Kimi Team, arXiv:2607.24653（v1 2026-07-27 / **v2 2026-08-07**，本轮引用版本）。精读见 [`papers/2607.24653-kimi-k3.md`](papers/2607.24653-kimi-k3.md)。

> 版本口径：K3 的 arXiv 元数据首提交 2026-07-27T16:49:54Z、最新更新 2026-08-07T06:33:46Z，正文数字以 v2 为准。
> 本条目**未**发现 K2.7 Code 的独立技术报告（截至 2026-10-17）——其架构描述只能回落到 K2.6 公开信息与 K2.7 Code 模型卡的架构表，见 §4.4。

### 9.2 官方资源

- Moonshot AI 官网：https://www.moonshot.ai/
- Kimi 平台：https://kimi.ai/ ; https://platform.moonshot.cn/ ; https://platform.moonshot.ai/
- HuggingFace 组织：https://huggingface.co/moonshotai
- GitHub 组织：https://github.com/MoonshotAI
- Kimi K2 项目页：https://moonshotai.github.io/Kimi-K2/
- Kimi K2 Thinking 项目页：https://moonshotai.github.io/Kimi-K2/thinking.html
- Kimi K2.5 博客：https://www.kimi.com/blog/kimi-k2-5
- **Kimi K3 技术博客**：https://www.kimi.com/en/blog/kimi-k3（2026-07-16 上线与权重发布时间说明；访问日期 2026-10-23）
- **Kimi K3 模型卡与权重仓历史**：https://huggingface.co/moonshotai/Kimi-K3（模型卡 lastModified 2026-09-02；`createdAt` 不作为权重公开日期）
- **Kimi K3 GitHub**：https://github.com/MoonshotAI/Kimi-K3
- **Kimi K2.7 Code 模型卡**：https://huggingface.co/moonshotai/Kimi-K2.7-Code（createdAt 2026-06-11 / lastModified 2026-06-15）
- **Kimi K2.7 Code 官方资源页**：https://www.kimi.com/resources/kimi-k2-7-code（页面标注「更新于 2026-10-08」）
- **Kimi 研究博客索引**（各博客发布日期的一手出处）：https://www.kimi.com/blog
- **MoonEP 仓库**（K3 的完全均衡专家并行库）：https://github.com/MoonshotAI/MoonEP
- **FlashKDA 仓库**（KDA 高性能 kernel）：https://github.com/MoonshotAI/FlashKDA
- **Attention-Residuals 仓库**：https://github.com/MoonshotAI/Attention-Residuals

### 9.3 关键背景文献

- DeepSeek-V3 Technical Report（K2、Kimi-VL 架构基础）, DeepSeek-AI, 2024-12.
- DeepSeek-R1（同期推理对照）, DeepSeek-AI, arXiv:2501.12948, 2025-01.
- RoPE: RoFormer (Su et al., 2021)
- Muon 原版（Jordan et al., 2024，Moonshot 引用源）
- NaViT (Dehghani et al., 2023)（MoonViT 的 packing 思想来源）
- YaRN (Peng et al., 2023)（K2 长上下文扩展用）
- FlashAttention (Dao et al., 2022)（MoonViT 与 LLM 共用 kernel 基础）

### 9.4 第三方分析

- Nathan Lambert, "5 Thoughts on Kimi K2 Thinking", Interconnects, 2025-11-06.
- Fireworks AI Blog, "Deep-dive into MuonClip: Fixing Attention Score Explosions".
- Simon Willison's Weblog, "Kimi K2.5", 2026-01-27.
- 各 arXiv-html 全文 / HuggingFace 论文页面（详见正文链接）。

---

> **报告说明**：本报告所有技术细节均来自 Moonshot AI 公开发布的论文、官方博客、GitHub 仓库与 HuggingFace 模型卡。Kimi 早期 Moonshot-v1 阶段未公布完整技术报告，对应章节内容综合自官方公告、平台 API 文档与第三方权威分析；其余章节细节均直接引用对应一作论文。

> **2026-10-17 增量说明**：本轮只做增补与修正，不改动 2026-06 之前已核验的结论。新增内容集中在 §4.4（Kimi K2.7 Code）、§4.5（Kimi K3）、§4.6（未确证与待跟踪），并同步更新 §1.1 时间线、§7 横向比较表的相关格、§9 参考文献与官方资源。证据分级口径：**精读原文**（技术报告全文 / 官方模型卡 / 官方文档原文）、**摘要级**（仅读 arXiv 摘要与元数据）、**二手**（第三方页面或他人转述）、**受限核验**（原始页面在本环境不可达，只能用镜像/模型卡替代）。本条目 2026-06 之后的新增内容全部为「精读原文」等级；「二手」与「受限核验」条目一律落在 §4.6，不入正文。
