---
display_name: 扩散模型
---

# 扩散模型（Diffusion Models）基础框架与架构演进研究报告

> **研究范围**：从 DDPM（2020）到 Flow Matching（2023）及后续采样加速技术的核心架构演进  
> **阅读目标**：理解扩散模型的噪声路径、网络参数化和采样器各自解决什么问题，以及它们如何与潜空间表示和 Transformer 骨干组合。

---

## 目录

1. [概述](#1-概述)
2. [发展时间线](#2-发展时间线)
3. [核心架构详解](#3-核心架构详解)
   - 3.1 DDPM：奠基之 U-Net
   - 3.2 DDIM：非马尔可夫确定性采样
   - 3.3 LDM / Stable Diffusion：潜空间扩散
   - 3.4 Classifier-Free Guidance：条件采样范式
   - 3.5 Consistency Models：单步一致性映射
   - 3.6 Flow Matching：速度场回归框架
4. [数学框架对比](#4-数学框架对比)
5. [采样加速技术](#5-采样加速技术)
6. [代表性模型架构对比表](#6-代表性模型架构对比表)
7. [挑战与未来方向](#7-挑战与未来方向)
8. [参考链接](#8-参考链接)

---

## 1. 概述

扩散模型（Diffusion Models）是近年来生成式 AI 领域最具影响力的范式之一。其核心思想源于非平衡热力学：通过定义一个前向（Forward）过程逐步向数据添加高斯噪声，直至数据分布退化为纯噪声；再训练一个神经网络学习逆向（Reverse）过程，从噪声中逐步恢复出真实数据。

自 2020 年 DDPM（Denoising Diffusion Probabilistic Models）重新点燃该方向以来，扩散模型经历了从像素空间到潜空间、从数百步迭代到单步生成、从概率建模到确定性流匹配的深刻架构演进。本报告系统梳理这一演进脉络，重点剖析每一代模型的结构差异、数学本质与工程权衡，为理解 Stable Diffusion、SD3、FLUX 等现代系统的底层设计提供完整知识框架。

---

## 2. 发展时间线

| 时间 | 模型/技术 | 作者/团队 | 核心贡献 | 架构关键词 |
|------|-----------|-----------|----------|------------|
| 2015 | **Diffusion / NCSN** | Sohl-Dickstein et al. | 首次提出扩散概率模型概念 | 原始扩散框架 |
| 2020.06 | **DDPM** | Ho et al. (OpenAI) | 将扩散模型与 U-Net 结合，实现高质量图像生成 | U-Net + ResNet + Self-Attention |
| 2020.10 | **DDIM** | Song et al. | 提出非马尔可夫采样，实现确定性、少步生成 | 共享 DDPM 网络，改进采样过程 |
| 2021 | **ADM / Guided Diffusion** | Dhariwal & Nichol | 引入 Classifier Guidance，提升条件生成质量 | U-Net + 外部分类器梯度 |
| 2022.04 | **LDM / Stable Diffusion** | Rombach et al. (LMU Munich) | 在潜空间（Latent Space）执行扩散，计算量降低 48x | VAE + U-Net + Cross-Attention |
| 2022.07 | **Classifier-Free Guidance (CFG)** | Ho & Salimans | 无需外部分类器的条件引导，成为文生图标配 | 条件/无条件联合训练 |
| 2023.03 | **Consistency Models** | Song et al. (OpenAI) | 从扩散模型蒸馏出单步/少步一致性映射 | 一致性蒸馏 + 跳步生成 |
| 2023.10 | **Flow Matching / Rectified Flow** | Lipman et al.; Liu et al. | 直接回归速度场，用直线插值替代曲线扩散 | 速度场 v_t + 直线路径 |
| 2024 | **SD3 / FLUX** | Stability AI / Black Forest Labs | 采用 Flow Matching 框架的大规模文生图系统 | Flow Matching + Transformer |

> **注**：时间线用于定位代表性机制，不代表某条路线取代其他路线；重点是不同路径、目标与采样器的关系。

---

## 3. 核心架构详解

### 3.1 DDPM（2020, Ho et al.）

#### 3.1.1 整体架构

DDPM 是扩散模型现代复兴的奠基之作。其核心网络是一个**U-Net**，输入为带噪图像 `x_t` 和时间步 `t`，输出为预测噪声 `ε_θ(x_t, t)`。

```
输入: x_t (噪声图像, 3×H×W) + t (时间步标量)
        │
        ▼
┌─────────────────────────────────────────┐
│           U-Net Backbone                │
│  ┌─────────┐    ┌─────────┐    ┌─────┐ │
│  │Encoder  │───▶│Bottleneck│───▶│Decoder│ │
│  │(Down)   │    │         │    │(Up) │ │
│  └─────────┘    └─────────┘    └─────┘ │
│       │ Skip Connections │              │
└─────────────────────────────────────────┘
        │
        ▼
输出: ε_θ(x_t, t) (预测噪声, 3×H×W)
```

#### 3.1.2 关键模块

**（1）ResNet Block**

每个下采样/上采样阶段包含多个 ResNet Block，结构如下：

```
输入: feature map f
        │
        ├──▶ GroupNorm ──▶ SiLU ──▶ Conv3×3 ──┐
        │                                      │
        │    时间步嵌入 t_emb 注入 ────────────▶ (+) ──▶ GroupNorm ──▶ SiLU ──▶ Conv3×3 ──▶
        │                                      │
        └──────────────────────────────────────▶ (残差连接)
```

时间步嵌入 `t_emb` 通过**正弦位置编码（Sinusoidal Positional Encoding）**生成，与 Transformer 中的编码方式一致：

```
t_emb = [sin(t/10000^(0/d)), cos(t/10000^(1/d)), ..., sin(t/10000^(d-2/d)), cos(t/10000^(d-1/d))]
```

随后通过 MLP 映射到与特征图通道数相同的维度，以**逐元素相加（element-wise addition）**或**AdaGN（Adaptive Group Norm）**方式注入。

**（2）Self-Attention Block**

在 U-Net 的较低分辨率层（如 16×16 或 32×32）插入 Self-Attention，以捕获全局依赖关系：

```
输入: feature map f (B×C×H×W)
        │
        ▼ Reshape to (B×HW×C)
        │
        ├──▶ Q = f·W_q ──┐
        ├──▶ K = f·W_k ──┼──▶ Attention(Q,K,V) = softmax(QK^T/√d)·V ──┐
        └──▶ V = f·W_v ──┘                                              │
        │                                                              │
        └──────────────────────────────────────────────────────────────▶ (+) ──▶
```

**（3）下采样与上采样**

- **Encoder（下采样路径）**：通过 `Conv2d(stride=2)` 逐步降低空间分辨率（如 256→128→64→32→16），同时增加通道数（如 128→256→512→1024）。
- **Decoder（上采样路径）**：通过 `Upsample + Conv2d` 恢复分辨率，并与 Encoder 对应层的特征通过 Skip Connection 拼接（Concatenate）。

#### 3.1.3 训练目标

DDPM 的训练目标为预测噪声的均方误差（MSE）：

```
L_simple = E_{x_0, ε, t} [ ||ε - ε_θ(x_t, t)||² ]
```

其中 `x_t = √(ᾱ_t)·x_0 + √(1-ᾱ_t)·ε`，`ε ~ N(0, I)`，`t ~ Uniform({1, ..., T})`。

#### 3.1.4 采样过程

训练完成后，采样通过迭代去噪实现：

```
x_T ~ N(0, I)
for t = T, T-1, ..., 1:
    ε_θ = model(x_t, t)
    x_{t-1} = (x_t - √(1-ᾱ_t)·ε_θ) / √ᾱ_t  + σ_t·z   (z ~ N(0,I) if t>1, else z=0)
return x_0
```

原始 DDPM 需要 **T = 1000** 步迭代，生成一张图像需要调用模型 1000 次，速度极慢。

---

### 3.2 DDIM（2020, Song et al.）

#### 3.2.1 核心洞察

DDIM（Denoising Diffusion Implicit Models）的关键发现是：**前向过程的马尔可夫假设并非必要**。只要边缘分布 `q(x_t|x_0)` 保持不变，逆向过程可以定义为一族非马尔可夫过程。

#### 3.2.2 架构关系

DDIM **完全复用 DDPM 训练好的网络**，不做任何架构修改。其创新完全在于**采样算法**：

```
DDPM 训练 ──▶ 得到 ε_θ(x_t, t)
                │
                ├──▶ DDPM 采样: 马尔可夫链, 1000 步, 随机性高
                │
                └──▶ DDIM 采样: 非马尔可夫, 10-50 步, 确定性（σ=0）
```

#### 3.2.3 确定性采样公式

DDIM 定义了如下采样过程：

```
x_{t-1} = √ᾱ_{t-1} · x̂_0(x_t) + √(1-ᾱ_{t-1} - σ_t²) · ε_θ(x_t, t) + σ_t · z_t

其中 x̂_0(x_t) = (x_t - √(1-ᾱ_t)·ε_θ(x_t, t)) / √ᾱ_t   (预测的原始图像)
```

当 `σ_t = 0` 时，采样变为**完全确定性**：给定相同的 `x_T`，总是生成相同的 `x_0`。这使得 DDIM 成为后续一致性蒸馏、反演（Inversion）等技术的基础。

#### 3.2.4 加速效果

| 采样步数 | DDPM (FID) | DDIM (FID) | 备注 |
|----------|------------|------------|------|
| 1000 | ~3.17 | ~3.17 | 基准 |
| 100 | ~10+ | ~4.0 | DDPM 质量急剧下降 |
| 50 | 不可用 | ~4.5 | DDIM 仍可用 |
| 20 | 不可用 | ~5.5 | DDIM 快速采样 |
| 10 | 不可用 | ~7.0 | 牺牲部分质量 |

---

### 3.3 LDM / Stable Diffusion（2022, Rombach et al.）

#### 3.3.1 核心动机

DDPM 直接在像素空间（如 256×256×3）执行扩散，存在两个致命问题：
1. **计算量巨大**：像素空间去噪要处理更多空间位置；若在H×W位置上做同宽全局自注意力，该子操作为O((HW)²)，不能用它代表所有U-Net层。
2. **冗余度高**：图像像素空间存在大量感知冗余（Perceptually Redundant）。

LDM（Latent Diffusion Model）的核心创新是：**将扩散过程从像素空间迁移到潜空间（Latent Space）**。

#### 3.3.2 整体架构

```
文本输入: "a photo of a cat"
        │
        ▼
┌─────────────────┐
│ CLIP Text Encoder│  ──▶ 文本特征 c (77×768)
└─────────────────┘
        │
        │         图像输入: x_0 (3×512×512)
        │                │
        │                ▼
        │       ┌─────────────────┐
        │       │  VAE Encoder    │  下采样 8x: 512×512 → 64×64
        │       │  (冻结权重)     │  通道扩展: 3 → 4
        │       └─────────────────┘
        │                │
        │                ▼
        │         z_0 = E(x_0)  (4×64×64)
        │                │
        │                ▼ 在潜空间执行扩散
        │       ┌─────────────────────────────────────────┐
        │       │         Latent Space U-Net               │
        │       │  输入: z_t (4×64×64) + t + 文本条件 c     │
        │       │                                          │
        │       │  时间步注入: AdaGN (Adaptive Group Norm) │
        │       │  条件注入: Cross-Attention (Q=图像, K/V=文本)│
        │       │                                          │
        │       │  输出: ε_θ(z_t, t, c) (4×64×64)          │
        │       └─────────────────────────────────────────┘
        │                │
        │                ▼
        │         z_0 (去噪后的潜变量)
        │                │
        │                ▼
        │       ┌─────────────────┐
        │       │  VAE Decoder    │  上采样 8x: 64×64 → 512×512
        │       │  (冻结权重)     │  通道收缩: 4 → 3
        │       └─────────────────┘
        │                │
        ▼                ▼
     文本条件 c      输出图像 x̂_0 (3×512×512)
```

#### 3.3.3 VAE（变分自编码器）

LDM 使用预训练的 VAE 将图像压缩到低维潜空间：

- **Encoder** `E`: `x ∈ R^(3×H×W) → z ∈ R^(4×H/8×W/8)`
- **Decoder** `D`: `z ∈ R^(4×H/8×W/8) → x̂ ∈ R^(3×H×W)`
- **KL 约束**：用KL正则使编码分布接近先验；这不等于每个图像的潜码严格服从标准高斯

VAE 在 LDM 训练期间**完全冻结**，不参与扩散过程的训练。这带来了巨大的计算节省：

以图示 SD-style `f=8,c=4` 为例，下面只计算表示大小，不把它冒充实测速度：

| 量 | 像素空间 | 潜空间 | 像素/潜空间比（计算值） |
|---|---:|---:|---:|
| 空间位置数 | 512² | 64² | 64 |
| 标量个数（含通道） | 3×512² | 4×64² | 48 |
| 假设对全部位置做同宽全局自注意力时的配对数 | (512²)² | (64²)² | 4096 |

**48倍是标量个数比，64倍是位置数比，4096倍是指定注意力子操作的配对数比；三者都不是整个U-Net的FLOPs或端到端加速倍数。** 实际代价还包含多尺度卷积、通道宽度、注意力位置与VAE编解码。LDM原文研究多个压缩因子，图示不能代表所有LDM。[原文v2 §3.1、§4.1及效率附录](https://arxiv.org/html/2112.10752v2)

#### 3.3.4 U-Net 结构改进

LDM 的 U-Net 在 DDPM 基础上做了以下关键改进：

**（1）Cross-Attention 注入文本条件**

```
图像特征 f_img (B×HW×C) ──▶ Q = f_img · W_q ──┐
                                               │
文本特征 f_txt (B×77×768) ──▶ K = f_txt · W_k ──┼──▶ Attention(Q,K,V) ──▶ 条件化特征
                                               │
                              V = f_txt · W_v ──┘
```

- `Q` 来自图像特征（查询"图像需要什么信息"）
- `K/V` 来自 CLIP 文本编码器的输出（提供"文本描述的信息"）
- 文本序列长度固定为 77（CLIP 的 token 上限）
- 文本特征维度 768（CLIP ViT-L/14）

**（2）AdaGN（Adaptive Group Norm）**

LDM 使用 AdaGN 替代简单的时间步嵌入相加，将时间步和条件信息更优雅地注入特征：

```
输入: feature map f (B×C×H×W)
        │
        ├──▶ GroupNorm(f) ──┐
        │                    │
        │    t_emb ──▶ MLP ──▶ γ (scale) ──┐
        │    c_emb ──▶ MLP ──▶ β (shift)  ──┼──▶ γ · GroupNorm(f) + β ──▶
        │                                  │
        └──────────────────────────────────┘
```

其中 `γ` 和 `β` 是逐通道的缩放和平移参数，由时间步嵌入和/或条件嵌入通过 MLP 生成。

**（3）Attention 层级分布**

LDM 的 Self-Attention 和 Cross-Attention 主要分布在 U-Net 的较低分辨率层（16×16 和 32×32），高分辨率层（64×64）以卷积为主，平衡了计算效率与全局建模能力。

#### 3.3.5 Stable Diffusion 的工程实现

Stable Diffusion 是 LDM 的开源工程实现，核心架构完全一致，增加了：
- **文本编码器**：CLIP ViT-L/14（后续版本支持 OpenCLIP、T5 等）
- **安全过滤器**：NSFW 内容检测
- **社区生态**：LoRA、ControlNet、IP-Adapter 等插件体系

---

### 3.4 Classifier-Free Guidance（CFG, 2022, Ho & Salimans）

#### 3.4.1 背景问题

早期的 Classifier Guidance 需要训练一个额外的噪声图像分类器，并在采样时将其梯度注入去噪过程：

```
ε_guided = ε_uncond - √ᾱ_t · w · ∇_x log p_classifier(y|x_t)
```

这种方法存在明显缺陷：
1. 需要额外训练分类器，成本高
2. 分类器在噪声图像上训练，泛化性差
3. 梯度可能不稳定，导致生成样本失真

#### 3.4.2 CFG 的核心思想

CFG（Classifier-Free Guidance）提出了一种**无需外部分类器**的条件引导方法：

**训练阶段**：以 10% 的概率将条件 `c` 替换为空条件 `∅`（如空字符串），联合训练条件分支和无条件分支：

```
L = E_{x_0, c, ε, t} [ ||ε - ε_θ(x_t, t, c)||² ]   (90% 概率，条件训练)
L = E_{x_0, ε, t} [ ||ε - ε_θ(x_t, t, ∅)||² ]      (10% 概率，无条件训练)
```

**采样阶段**：通过线性外推增强条件响应：

```
ε_cfg = ε_θ(x_t, t, ∅) + w · (ε_θ(x_t, t, c) - ε_θ(x_t, t, ∅))
```

其中 `w` 为 guidance scale：
- `w = 1`：无条件生成（相当于不使用 CFG）
- `w = 7-10`：文生图的标准设置（高保真、高文本对齐）
- `w > 15`：可能出现过饱和、模式崩溃

#### 3.4.3 架构影响

CFG 不改变模型架构，但要求：
1. **推理时每次需要两次前向传播**（条件 + 无条件），计算量翻倍
2. **Batch 推理优化**：将条件/无条件输入拼接为同一 Batch，利用并行计算减少开销
3. **负向提示（Negative Prompt）**：将 `∅` 替换为用户指定的负面描述，成为社区标准实践

---

### 3.5 Consistency Models（2023, Song et al.）

#### 3.5.1 核心思想

Consistency Models 试图回答一个根本问题：**能否跳过迭代采样，实现单步生成？**

其核心洞察是：对于同一条概率流 ODE（Probability Flow ODE）轨迹上的任意两点 `x_t` 和 `x_{t'}`，它们应该映射到同一个最终解 `x_0`。即存在一个**一致性函数（Consistency Function）** `f`：

```
f: (x_t, t) → x_ε    (对所有 t ∈ [ε, T]，f(x_t, t) = x_ε)
```

其中 `x_ε` 是接近最终解的"一致性输出"（通常 `ε` 取很小的值，如 0.002）。

#### 3.5.2 架构设计

Consistency Models 的架构是一个**独立的神经网络**，可以直接从预训练的扩散模型蒸馏得到：

```
输入: x_t (噪声/中间状态) + t (时间步)
        │
        ▼
┌─────────────────────────────────────────┐
│      Consistency Model Network           │
│  (通常基于 U-Net 或改进的 ResNet 结构)   │
│                                          │
│  关键约束: 时间步 t=ε 时，f(x_ε, ε) = x_ε │
│  (边界条件: 当噪声极小时，输出等于输入)    │
│                                          │
│  时间步注入: 傅里叶特征 + MLP             │
│  跳过连接: 支持多尺度特征融合             │
└─────────────────────────────────────────┘
        │
        ▼
输出: x_ε (预测的最终解，可直接解码为图像)
```

#### 3.5.3 训练方法：一致性蒸馏

**第一阶段**：预训练一个标准的扩散模型（如 EDM 框架）。

**第二阶段**：蒸馏一致性模型，目标函数为：

```
L = E [ d(f_θ(x_{t_{n+1}}, t_{n+1}), f_θ^-(x_{t_n}, t_n)) ]
```

其中：
- `f_θ` 为在线网络（Online Network）
- `f_θ^-` 为目标网络（Target Network），通过 EMA 更新：`θ^- ← μ·θ^- + (1-μ)·θ`
- `d(·,·)` 为距离度量（如 LPIPS 感知损失或 L2 损失）
- `t_n` 和 `t_{n+1}` 为从同一 ODE 轨迹上采样的相邻时间步

#### 3.5.4 采样过程

一致性模型的采样极为简洁：

```
x_T ~ N(0, I)
x_ε = f_θ(x_T, T)    # 单步！直接得到最终输出
return x_ε
```

也可以进行多步采样以提升质量：

```
x_T ~ N(0, I)
for n = N, N-1, ..., 1:
    x_{t_{n-1}} = f_θ(x_{t_n}, t_n) + (t_{n-1} - t_n) · 可选的修正项
return x_{t_0}
```

#### 3.5.5 与扩散模型的关系

| 特性 | 扩散模型 (DDPM/DDIM) | Consistency Models |
|------|---------------------|-------------------|
| 采样步数 | 10-1000 步 | 1-4 步 |
| 单次前向计算量 | 与步数成正比 | 固定（单网络前向） |
| 训练方式 | 直接训练 | 从扩散模型蒸馏 |
| 质量-速度权衡 | 步数越少质量越差 | 单步即可达到较好质量 |
| 条件生成 | 直接支持 CFG | 需要额外适配 |
| 零样本编辑 | 支持（DDIM Inversion） | 原生支持一致性轨迹 |

---

### 3.6 Flow Matching 与 Rectified Flow（2022–2023）

#### 3.6.1 核心思想

Flow Matching（FM）首先是一种**按指定概率路径训练速度场**的方式：路径可以取自扩散过程，也可以是非扩散路径；Conditional Flow Matching（CFM）通过条件路径构造可直接计算的训练目标。Rectified Flow 则以噪声和数据之间的直线耦合为出发点，学习相应 ODE 速度场，并可通过 reflow 使轨迹逐步变直。二者相关但不是同义词：**FM/CFM 是路径匹配训练框架，直线路径是可选设计之一；Rectified Flow 专门研究直线路径、rectification 与数值求解误差之间的关系。**[Flow Matching §§3–4](https://arxiv.org/html/2210.02747v1) · [Rectified Flow §§2–3](https://arxiv.org/html/2209.03003v1)

#### 3.6.2 数学框架

**扩散模型的视角**：

扩散模型通过噪声调度定义扰动路径；连续时间表述可写成 SDE 及对应的 probability-flow ODE：

```
dx = [f(x,t) - ½·g²(t)·∇_x log p_t(x)] dt + g(t) dw   (SDE)
dx = [f(x,t) - ½·g²(t)·∇_x log p_t(x)] dt             (Probability Flow ODE)
```

**Flow Matching 的视角**：

以 CFM 原论文的噪声到数据时间方向为例，令 `x_noise ~ N(0,I)`、`x_data ~ p_data`，忽略终点处很小的方差下限后，条件直线路径可写为：

```
x_t = (1-t)·x_noise + t·x_data,   t ∈ [0, 1]
```

路径上的速度场为：

```
v_t = dx_t/dt = x_data - x_noise
```

训练目标是让神经网络 `v_θ(x_t, t)` 回归这个真实速度场：

```
L = E_{x_noise, x_data, t} [ ||v_t - v_θ(x_t, t)||² ]
    = E [ ||(x_data - x_noise) - v_θ((1-t)·x_noise + t·x_data, t)||² ]
```

#### 3.6.3 与扩散模型的关系

Flow Matching（FM）描述的是如何为一条选定的概率路径回归速度场；扩散模型通常从噪声扰动路径、score 或反向 SDE/ODE 来表述生成过程。Lipman 等人的 conditional flow matching（CFM）可使用高斯条件路径，其中包含特定的扩散路径，也允许选用非扩散路径，例如最优传输位移插值。[原文 §§3–4](https://arxiv.org/html/2210.02747v1)

| 视角 | 路径 / 训练对象 | 需要区分的部分 |
|------|----------------|----------------|
| 扩散模型 | 由噪声调度定义概率路径，常用 score 或噪声预测目标；对应的 probability-flow ODE 可作确定性采样 | 随机过程、训练参数化和确定性 ODE 采样器彼此相关，但并非同一对象 |
| Flow Matching | 先选概率路径，再回归生成该路径的向量场；CFM 用每个数据样本的条件路径构造可训练目标 | 可沿扩散路径训练，也可选非扩散路径；路径选择与网络骨干是独立设计 |

因此准确说法是：**FM/CFM 提供了比特定扩散路径更灵活的向量场训练表述；部分扩散路径可以嵌入这一表述，非扩散路径则打开额外选择。**这不是说所有扩散模型在每个训练和采样细节上都只是同一类 FM 模型的别名。原论文证明 FM 与 CFM 目标在其条件路径构造下具有相同梯度，并给出可恢复扩散路径及 OT 路径的例子。[原文 §3.2、§4.1](https://arxiv.org/html/2210.02747v1)

#### 3.6.4 路径、预测量与采样器

Flow Matching 是训练目标/路径构造，不是单独规定一种网络架构。它可以使用 U-Net、Transformer 等骨干；与扩散系统对照时，应分开看路径、模型预测量和数值积分器。

**（1）时间参数**
- 离散 DDPM 常把时间步写成 `1...T`；score/SDE 与 probability-flow ODE 可采用连续时间。
- CFM 原论文将时间归一化到 `[0,1]`，这是一种记号与路径设定，不是 FM 独有的计算优势。

**（2）网络预测量**
- 扩散模型可预测噪声、score、数据或等价的速度参数化，具体取决于训练目标和调度。
- CFM 训练网络预测指定概率路径的向量场 `v_θ(x_t,t)`。

**（3）采样器**
- 概率流 ODE 和 FM 向量场都可交给数值 ODE 求解器；Euler 只是一个低阶选项。
- 步数—质量—计算开销由路径曲率、网络误差、条件引导、求解器阶数和容差共同决定，不能仅凭目标名称推断。

以 CFM 原论文的 noise-to-data 时间方向为例，忽略路径末端的微小方差下限，令 `x_noise` 位于 `t=0`、`x_data` 位于 `t=1`，直线路径可写为 `x_t=(1-t)x_noise+t x_data`，其条件速度为 `x_data−x_noise`。若用 Euler 求解，生成时从噪声向数据方向更新：

```text
x ← x_noise
for t = 0, Δt, 2Δt, ..., 1−Δt:
    x ← x + Δt · v_θ(x, t)
return x
```

这里的直线路径是解释 CFM 的一个选择，不代表所有 Flow Matching 模型都使用同一路径或固定步数。[CFM 原文 §4.1](https://arxiv.org/html/2210.02747v1)

#### 3.6.5 SD3 / FLUX 中的应用

SD3 与 FLUX 说明，FM/Rectified Flow 可以和 Transformer/MMDiT 类骨干组合；这仍是“生成目标/路径”与“网络骨干”两项选择。不能据“采用 Flow Matching”推出模型必然更稳定、可用固定少步数达到同等质量，或其 Transformer 结构与其他系统相同。具体的 SD3、FLUX 架构与论文报告结果见[DiT 报告](../DiT/report.md)及[模型系列报告](../../Models/README.md)。本节只保留机制关系，不把产品级推理配置当作 FM 的普遍性质。

---

## 4. 数学框架对比

### 4.1 统一视角

很多扩散与流模型都可用“路径—预测量—训练目标—采样器”这组问题对照。下式是常见的高斯噪声到数据路径示意，不表示所有模型使用同一噪声调度或插值式路径：

```
路径构造（噪声到数据）:  x_t = a_t·x_noise + b_t·x_data
                            │
                            ▼
网络预测:                  y_θ = model(x_t, t)     (y 可以是 ε, x_0, v, 或 score)
                            │
                            ▼
训练目标:                  L = E[ ||y_true - y_θ||² ]
                            │
                            ▼
采样过程:                  从 x_T ~ N(0,I) 出发，通过迭代/ODE 积分恢复 x_0
```

### 4.2 各框架的数学公式

#### DDPM（噪声预测）

```
前向:  x_t = √ᾱ_t·x_0 + √(1-ᾱ_t)·ε,    ε ~ N(0,I)
网络:  ε_θ(x_t, t)
目标:  L = E[ ||ε - ε_θ(x_t, t)||² ]
采样:  x_{t-1} = (x_t - √(1-ᾱ_t)·ε_θ) / √ᾱ_t + σ_t·z
```

#### DDIM（非马尔可夫采样）

```
共享 DDPM 的网络 ε_θ(x_t, t)
采样:  x_{t-1} = √ᾱ_{t-1}·x̂_0 + √(1-ᾱ_{t-1})·ε_θ    (确定性版本, σ=0)
      其中 x̂_0 = (x_t - √(1-ᾱ_t)·ε_θ) / √ᾱ_t
```

#### LDM（潜空间扩散）

```
前向:  z_t = √ᾱ_t·z_0 + √(1-ᾱ_t)·ε,    z_0 = E(x_0)
网络:  ε_θ(z_t, t, c)    (c 为文本条件)
目标:  L = E[ ||ε - ε_θ(z_t, t, c)||² ]
采样:  z_{t-1} = ... (同 DDPM/DDIM)
输出:  x̂_0 = D(z_0)
```

#### Consistency Models（一致性函数）

```
一致性函数:  f: (x_t, t) → x_ε,    满足 f(x_t, t) = f(x_{t'}, t') 对同一轨迹
边界条件:   f(x_ε, ε) = x_ε
训练目标:   L = E[ d(f_θ(x_{t_{n+1}}, t_{n+1}), f_θ^-(x_{t_n}, t_n)) ]
采样:       x_ε = f_θ(x_T, T)    (单步)
```

#### Flow Matching（速度场回归）

```
路径:  x_t = (1-t)·x_noise + t·x_data,  x_noise ~ N(0,I),  t ∈ [0,1]
速度场: v_t = dx_t/dt = x_data - x_noise
网络:  v_θ(x_t, t)
目标:  L = E[ ||v_t - v_θ(x_t, t)||² ]
采样:  x_{t+Δt} = x_t + Δt · v_θ(x_t, t)    (noise→data 的 Euler 积分)
```

### 4.3 参数化方式对比

扩散模型有多种网络输出参数化方式，本质等价但训练稳定性不同：

| 参数化 | 网络输出 | 训练目标 | 特点 |
|--------|---------|---------|------|
| **Noise Prediction** | `ε_θ(x_t, t)` | `||ε - ε_θ||²` | DDPM 默认，简单直接 |
| **x0 Prediction** | `x_0^θ(x_t, t)` | `||x_0 - x_0^θ||²` | 直接预测干净图像，适合小 t |
| **v-Prediction** | `v_θ(x_t, t)` | `||v - v_θ||²` | `v = α_t·ε - σ_t·x_0`，训练更稳定 |
| **Score Matching** | `s_θ(x_t, t)` | `||∇log p_t(x) - s_θ||²` | 理论优雅，与 SDE 直接对应 |

> **注**：v-Prediction 由 Salimans & Ho (2022) 提出，已成为现代扩散模型（如 Imagen、SDXL）的标准选择，因为它在信噪比（SNR）极端情况下更稳定。

---

## 5. 采样加速技术

### 5.1 Progressive Distillation（渐进蒸馏, Salimans & Ho, 2022）

#### 原理

通过迭代蒸馏，将 `N` 步的采样过程压缩为 `N/2` 步：

```
教师模型: 需要 2N 步生成高质量样本
        │
        ▼ 蒸馏
学生模型: 仅需 N 步，输出与教师 2N 步结果一致
        │
        ▼ 再次蒸馏
学生模型: 仅需 N/2 步
        │
        ▼ ...
最终: 仅需 4-8 步
```

#### 蒸馏目标

```
L = E[ ||student(x_t, t, t') - teacher^N(x_t, t)||² ]
```

其中 `teacher^N` 表示教师模型执行 `N` 步 DDIM 采样的结果。

#### 特点
- 需要多轮蒸馏，每轮计算成本高
- 最终模型可以实现 4-8 步高质量采样
- 被 Imagen 等系统采用

---

### 5.2 DPM-Solver / DPM-Solver++（Lu et al., 2022）

#### 原理

DPM-Solver 是一族**专为扩散模型设计的高阶 ODE 求解器**。其核心洞察是：

扩散模型的概率流 ODE 可以写成：

```
dx_t/dt = f(t)·x_t - ½·g²(t)·s_θ(x_t, t)
```

其中 `s_θ(x_t, t) = -ε_θ(x_t, t) / √(1-ᾱ_t)` 为估计的 score 函数。

通过变量替换 `y_t = x_t / √ᾱ_t`，可以将 ODE 转化为**半线性形式**，从而应用高阶数值方法（如 Runge-Kutta 的变体）。

#### DPM-Solver 算法族

| 方法 | 阶数 | 每步函数评估次数 | 适用场景 |
|------|------|-----------------|---------|
| DPM-Solver-1 | 1 | 1 | 最快，质量一般 |
| DPM-Solver-2 | 2 | 2 | 平衡速度和质量 |
| DPM-Solver-3 | 3 | 3 | 高质量，步数极少 |
| DPM-Solver++ | 1-3 | 1-3 | 改进版，支持 noise/x0/v 预测 |

#### 采样效果

| 步数 | DDIM | DPM-Solver++(2M) | DPM-Solver++(3) |
|------|------|-----------------|-----------------|
| 10 | FID ~7 | FID ~4 | FID ~3.5 |
| 20 | FID ~5 | FID ~3.5 | FID ~3.0 |
| 50 | FID ~4 | FID ~3.0 | FID ~2.8 |

DPM-Solver++ 已成为 Stable Diffusion WebUI、ComfyUI 等工具的默认采样器之一。

---

### 5.3 Flow-DPM-Solver（Zheng et al., 2023）

#### 原理

将 DPM-Solver 的思想扩展到 Flow Matching 框架。在 Flow Matching 中，采样 ODE 为：

```
dx_t/dt = v_θ(x_t, t)
```

Flow-DPM-Solver 利用速度场的**时间导数信息**，构造高阶积分公式：

```
x_{t_{n-1}} = x_{t_n} + Δt·v_θ(x_{t_n}, t_n) + ½·Δt²·(dv/dt) + ...
```

通过自动微分或有限差分估计 `dv/dt`，实现 3-5 步的高质量采样。

#### 特点
- 专为 Flow Matching 设计
- 3-5 步即可达到 20-50 步 Euler 采样的质量
- 被 SD3、FLUX 等系统采用

---

### 5.4 加速技术对比总结

| 技术 | 类型 | 是否需要重新训练 | 采样步数 | 质量损失 | 代表应用 |
|------|------|-----------------|---------|---------|---------|
| DDIM | 采样器改进 | 否 | 10-50 | 小 | 通用 |
| DPM-Solver++ | 高阶 ODE 求解器 | 否 | 10-20 | 极小 | Stable Diffusion |
| Progressive Distillation | 模型蒸馏 | 是（多轮） | 4-8 | 中 | Imagen |
| Consistency Models | 一致性蒸馏 | 是（单轮） | 1-4 | 中 | Consistency Model |
| Flow-DPM-Solver | 高阶流求解器 | 否 | 3-5 | 极小 | SD3, FLUX |
| LCM (Latent Consistency Model) | 一致性蒸馏+潜空间 | 是 | 1-4 | 中 | LCM-LoRA |

---

## 6. 代表性模型架构对比表

| 维度 | DDPM | DDIM | LDM / SD 1.x | SDXL | Consistency Models | SD3 / FLUX (Flow Matching) |
|------|------|------|-------------|------|-------------------|---------------------------|
| **年份** | 2020 | 2020 | 2022 | 2023 | 2023 | 2024 |
| **空间** | 像素空间 | 像素空间 | 潜空间 (8×) | 潜空间 (8×) | 像素/潜空间 | 潜空间 (8×/16×) |
| **骨干网络** | U-Net | U-Net (共享) | U-Net + Cross-Attn | U-Net + Cross-Attn | U-Net/ResNet | Transformer (DiT) |
| **条件注入** | 时间步嵌入 | 时间步嵌入 | AdaGN + Cross-Attn | AdaGN + Cross-Attn | 时间步嵌入 | AdaLN + Cross-Attn |
| **文本编码器** | 无 | 无 | CLIP ViT-L/14 | CLIP + OpenCLIP | 可选 | CLIP + T5-XXL / T5 |
| **网络输出** | 噪声 ε | 噪声 ε | 噪声 ε | v-Prediction | 一致性输出 x_ε | 速度场 v |
| **训练目标** | MSE(ε) | MSE(ε) | MSE(ε) | MSE(v) | 一致性损失 | MSE(v) |
| **采样步数** | 1000 | 10-50 | 20-50 | 20-50 | 1-4 | 4-8 |
| **CFG 支持** | 有限 | 有限 | 原生支持 | 原生支持 | 需适配 | 原生支持 |
| **计算量** | 极高 | 高 | 中 | 中 | 低 | 中 |
| **分辨率** | 32×32-256×256 | 同 DDPM | 512×512 | 1024×1024 | 同教师模型 | 1024×1024+ |
| **开源** | 部分 | 部分 | 完全开源 | 完全开源 | 部分 | 部分 |
| **核心创新** | U-Net + 扩散框架 | 非马尔可夫采样 | 潜空间扩散 | 双阶段 U-Net | 单步一致性 | 速度场 + Transformer |

---

## 7. 挑战与未来方向

### 7.1 当前挑战

**（1）推理速度仍是瓶颈**

即使采用 Flow Matching + 4 步采样，生成一张 1024×1024 图像仍需要数秒（A100 上约 1-2 秒）。相比之下，GAN 可以实现毫秒级生成。一致性模型和对抗蒸馏（Adversarial Distillation）是潜在的解决方向。

**（2）文本-图像对齐的精细控制**

现有模型在复杂空间关系（如"左边是 A，右边是 B"）、数量一致性（"三只猫"）、和精细属性控制上仍有明显缺陷。架构层面的改进（如更强的文本编码器、布局条件注入）是活跃研究方向。

**（3）视频与 3D 生成**

将扩散框架扩展到时间维度（视频）和三维空间（3D/NeRF）面临巨大的计算和内存挑战。当前方案（如 Sora、VideoLDM）主要依赖时空分解和潜空间压缩，但长视频的一致性和物理合理性仍是开放问题。

**（4）可解释性与可控性**

扩散模型的生成过程缺乏显式的语义控制。虽然 ControlNet、T2I-Adapter 等插件提供了部分解决方案，但底层的"黑箱"特性限制了其在高风险场景（如医疗、自动驾驶）的应用。

### 7.2 未来方向

**（1）单步/实时生成**

- **对抗一致性模型**：结合 Consistency Models 和 GAN 的对抗训练，实现单步高质量生成
- **蒸馏技术演进**：从 Progressive Distillation 到 Guided Distillation（如 FLUX 的 Guidance Distillation）

**（2）架构统一：Transformer 化**

- **DiT（Diffusion Transformer）**：用 Vision Transformer 替代 U-Net，在潜空间 patch 上执行 attention
- **Scaling Law**：验证扩散模型是否遵循类似 LLM 的 scaling law（参数量 ↑ → 质量 ↑）
- **SD3 / FLUX**：已验证 Transformer 在扩散/流模型中的有效性

**（3）多模态与世界模型**

- **统一生成框架**：文本、图像、视频、音频、3D 的统一生成模型
- **世界模型（World Models）**：将扩散模型作为物理世界的生成式模拟器
- **与 LLM 结合**：如 GPT-4o 的原生多模态生成，或扩散模型作为 LLM 的"视觉解码器"

**（4）效率优化**

- **量化与剪枝**：INT8/INT4 量化、结构化剪枝，降低部署成本
- **专用硬件**：针对扩散/流模型的 attention 模式和 ODE 求解设计 AI 加速器
- **缓存与复用**：如 TeaCache（特征缓存）、CFG-Zero（无需无条件前向）等推理优化

---

## 8. 参考链接

### 核心论文

1. **DDPM**: Ho, J., Jain, A., & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. *NeurIPS 2020*.  
   https://arxiv.org/abs/2006.11239

2. **DDIM**: Song, J., Meng, C., & Ermon, S. (2020). Denoising Diffusion Implicit Models. *ICLR 2021*.  
   https://arxiv.org/abs/2010.02502

3. **LDM / Stable Diffusion**: Rombach, R., Blattmann, A., Lorenz, D., Esser, P., & Ommer, B. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. *CVPR 2022*.  
   https://arxiv.org/abs/2112.10752

4. **Classifier-Free Guidance**: Ho, J., & Salimans, T. (2022). Classifier-Free Diffusion Guidance. *NeurIPS 2021 Workshop*.  
   https://arxiv.org/abs/2207.12598

5. **Consistency Models**: Song, Y., Dhariwal, P., Chen, M., & Sutskever, I. (2023). Consistency Models. *ICML 2023*.  
   https://arxiv.org/abs/2303.01469

6. **Flow Matching (CFM)**: Lipman, Y., Chen, R. T., Ben-Hamu, H., Nickel, M., & Le, M. (2023). Flow Matching for Generative Modeling. *ICLR 2023*.  
   https://arxiv.org/abs/2210.02747

7. **Rectified Flow**: Liu, X., Gong, C., & Liu, Q. (2023). Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow. *ICLR 2023*.  
   https://arxiv.org/abs/2209.03003

### 采样加速

8. **Progressive Distillation**: Salimans, T., & Ho, J. (2022). Progressive Distillation for Fast Sampling of Diffusion Models. *ICLR 2022*.  
   https://arxiv.org/abs/2202.00512

9. **DPM-Solver**: Lu, C., Zhou, Y., Bao, F., Chen, J., Li, C., & Zhu, J. (2022). DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps. *NeurIPS 2022*.  
   https://arxiv.org/abs/2206.00927

10. **DPM-Solver++**: Lu, C., Zhou, Y., Bao, F., Chen, J., Li, C., & Zhu, J. (2022). DPM-Solver++: Fast Solver for Guided Sampling of Diffusion Probabilistic Models. *NeurIPS 2022*.  
    https://arxiv.org/abs/2211.01095

11. **Flow-DPM-Solver**: Zheng, K., Lu, C., Chen, J., & Zhu, J. (2023). Improved Convergence for Consistency Models with Flow Matching.  
    https://arxiv.org/abs/2310.03294

### 现代系统

12. **Stable Diffusion**: https://github.com/Stability-AI/stablediffusion
13. **SDXL**: Podell, D., et al. (2023). SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis. *ICLR 2024*.  
    https://arxiv.org/abs/2307.01952
14. **SD3**: Esser, P., et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis. *ICML 2024*.  
    https://arxiv.org/abs/2403.03206
15. **FLUX**: https://github.com/black-forest-labs/flux
16. **DiT**: Peebles, W., & Xie, S. (2023). Scalable Diffusion Models with Transformers. *ICCV 2023*.  
    https://arxiv.org/abs/2212.09748

### 综述与教程

17. **Diffusion Models Survey**: Yang, L., et al. (2023). Diffusion Models: A Comprehensive Survey of Methods and Applications. *ACM Computing Surveys*.  
    https://arxiv.org/abs/2209.00796
18. **Score-Based Generative Modeling**: Song, Y. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. *ICLR 2021*.  
    https://arxiv.org/abs/2011.13456
19. **Flow Matching Tutorial**: https://flow-matching.github.io/
20. **Lilian Weng's Blog**: What are Diffusion Models?  
    https://lilianweng.github.io/posts/2021-07-11-diffusion-models/

---
