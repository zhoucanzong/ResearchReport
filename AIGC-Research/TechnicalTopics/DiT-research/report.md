# Diffusion Transformer (DiT) 架构演进研究报告

> **报告日期**: 2026年6月6日  
> **研究范围**: 从 U-Net 到 DiT 的生成模型架构范式转移（2020–2025）  
> **核心主题**: 模型结构演进、Scaling Law、计算效率优化、多模态扩展

---

## 目录

1. [概述](#1-概述)
2. [发展时间线](#2-发展时间线)
3. [U-Net 时代：扩散模型的卷积基础](#3-u-net-时代扩散模型的卷积基础)
4. [DiT 诞生：Transformer 进入扩散模型](#4-dit-诞生transformer-进入扩散模型)
5. [PixArt-α/Σ：高效训练策略](#5-pixart-ασ高效训练策略)
6. [SD3 / MMDiT：多模态 DiT](#6-sd3--mmdit多模态-dit)
7. [FLUX：Flow Matching + Transformer](#7-fluxflow-matching--transformer)
8. [SANA：Linear DiT 与实时生成](#8-sana-linear-dit-与实时生成)
9. [视频 DiT：从图像到时空生成](#9-视频-dit从图像到时空生成)
10. [架构对比总结](#10-架构对比总结)
11. [Scaling Law 分析](#11-scaling-law-分析)
12. [挑战与未来方向](#12-挑战与未来方向)
13. [参考链接](#13-参考链接)

---

## 1. 概述

Diffusion Transformer（DiT）代表了生成模型领域自 2023 年以来最深刻的架构范式转移之一。在 2020–2022 年间，扩散模型（Diffusion Models）的骨干网络几乎被 U-Net 垄断——从 DDPM、DDIM 到 Stable Diffusion（LDM），对称的编码器-解码器结构配合卷积操作成为标准范式。然而，U-Net 的卷积局部性、感受野限制以及难以随参数量扩展的特性，逐渐成为生成质量进一步提升的瓶颈。

2023 年，Peebles & Xie 在 ICCV 发表的 **DiT（Diffusion Transformer）** 首次系统性地证明了：将 Transformer 作为扩散模型的去噪网络（denoising network），不仅能达到与 U-Net 相当甚至更好的性能，而且展现出清晰的 **Scaling Law**——即模型参数量和数据量的增加能够稳定地提升生成质量。这一发现与 NLP 领域 GPT 系列的成功经验相呼应，标志着生成模型正式迈入"Transformer 时代"。

此后，DiT 架构迅速演化出多个重要分支：
- **PixArt-α/Σ**（华为诺亚，2023–2024）通过解耦文本编码和分阶段训练策略，实现了高效低成本训练；
- **SD3 / MMDiT**（Stability AI，2024）引入多模态 Transformer，让文本和图像 token 在注意力层中深度交互；
- **FLUX**（Black Forest Labs，2024）将 Flow Matching 与 Transformer 结合，以 12B 参数成为开源最强图像生成模型；
- **SANA**（NVIDIA，2025）用 Linear Attention 替代标准二次复杂度注意力，配合深度压缩自编码器（DC-AE），在 0.6B 参数下实现消费级 GPU 实时生成；
- **视频 DiT**（Sora、可灵、Veo、Wan，2024–2025）将 2D 空间注意力扩展为 3D 时空注意力，开启了视频生成的新纪元。

本报告将系统梳理这一架构演进脉络，重点分析每代模型的结构创新、计算复杂度特征以及 Scaling 行为，为理解当前生成模型的技术格局提供参考。

---

## 2. 发展时间线

| 时间 | 模型/工作 | 机构 | 核心架构创新 | 参数量 | 关键意义 |
|------|-----------|------|-------------|--------|----------|
| 2020.06 | DDPM | UC Berkeley | U-Net + ResNet + Time Embedding | ~100M | 扩散模型奠基，U-Net 成为标准骨干 |
| 2020.10 | DDIM | Stanford | DDPM 加速采样，U-Net 结构不变 | ~100M | 确定性采样，50步→20步 |
| 2021.12 | LDM (Stable Diffusion) | LMU Munich | U-Net + 潜空间扩散 (VAE 压缩) | ~890M | 潜空间计算效率突破，开源生态起点 |
| 2022.08 | SD 1.4/1.5 | Stability AI | LDM U-Net + CLIP 文本条件 | ~890M | 文本到图像开源爆发 |
| 2022.11 | SD 2.0 | Stability AI | U-Net + OpenCLIP 文本编码器 | ~890M | 更高分辨率，更强文本理解 |
| 2023.07 | SDXL | Stability AI | 更大 U-Net + 双文本编码器 (CLIP+OpenCLIP) | ~2.6B (Base+Refiner) | U-Net 规模扩展的极限尝试 |
| **2023.12** | **DiT** | **UC Berkeley / Meta** | **Transformer 替代 U-Net，adaLN 条件注入** | **0.6B–7B** | **范式转移起点，Scaling Law 验证** |
| 2023.12 | PixArt-α | 华为诺亚 | DiT + T5 解耦文本编码 + 分阶段训练 | ~0.6B | 10M 数据达到 SDXL 水平 |
| 2024.03 | PixArt-Σ | 华为诺亚 | PixArt-α 升级，更高分辨率，更强细节 | ~0.6B | 高效训练策略的进一步完善 |
| 2024.06 | SD3 | Stability AI | MMDiT (Multimodal DiT)，文本/图像双路注意力 | ~3B | 多模态 DiT 的工业级实现 |
| 2024.08 | FLUX.1 [dev/schnell] | Black Forest Labs | Flow Matching + Transformer，统一文本/图像流 | ~12B | 开源最强图像生成模型 |
| 2024.12 | Sora (推测) | OpenAI | 3D DiT (空间+时序注意力)，大规模视频训练 | ~?B (推测 10B+) | 视频生成里程碑，DiT 扩展至时空 |
| 2025.01 | 可灵 (Kling) | 快手 | 3D DiT + 因果时序注意力，长视频生成 | ~?B | 国产视频 DiT 代表，1080p 长视频 |
| 2025.02 | Wan (万相) | 阿里巴巴 | 3D DiT + 双向时序注意力，开源视频模型 | ~?B | 开源视频 DiT，支持多种分辨率 |
| 2025.03 | Veo 2 | Google | 3D DiT 变体，高质量视频生成 | ~?B | Google 视频生成旗舰 |
| **2025.06** | **SANA** | **NVIDIA** | **Linear DiT + DC-AE (32x 压缩)** | **~0.6B** | **O(n) 复杂度突破，消费级实时生成** |

---

## 3. U-Net 时代：扩散模型的卷积基础

### 3.1 架构结构

在 2020–2022 年间，几乎所有主流扩散模型都采用 **U-Net** 作为去噪网络。其典型结构如下：

```
输入: 噪声潜变量 z_t (4×64×64 或 3×256×256)
        ↓
    ┌─────────────────────────────────────────┐
    │  编码器 (Encoder)                        │
    │  ─────────────────────────────────────   │
    │  Conv-In → ResNet Block ×2 → Downsample │
    │       ↓                                  │
    │  ResNet Block ×2 → Self-Attention → Down │
    │       ↓                                  │
    │  ResNet Block ×2 → Self-Attention → Down │
    │       ↓                                  │
    │  ───────── 瓶颈层 (Bottleneck) ───────── │
    │  ResNet Block ×2 → Self-Attention         │
    │  (Cross-Attention 注入文本条件)            │
    │       ↓                                  │
    │  解码器 (Decoder)                        │
    │  ─────────────────────────────────────   │
    │  ResNet Block ×2 → Self-Attention → Up   │
    │       ↓ (Skip Connection)                │
    │  ResNet Block ×2 → Self-Attention → Up   │
    │       ↓ (Skip Connection)                │
    │  ResNet Block ×2 → Up                    │
    │       ↓                                  │
    └─────────────────────────────────────────┘
输出: 预测噪声 ε_θ(z_t, t, c)
```

### 3.2 核心组件详解

**ResNet Blocks**：
- 由两个 3×3 卷积层组成，中间夹 BatchNorm / GroupNorm 和 SiLU 激活
- 时间步条件通过 **AdaGN (Adaptive Group Normalization)** 注入：将时间步 embedding 投影为缩放参数 γ 和偏移参数 β，对特征图进行逐通道调制
- 数学表达：`AdaGN(h, t) = γ(t) · GroupNorm(h) + β(t)`

**Self-Attention**：
- 在 U-Net 的较低分辨率层（如 16×16、8×8）插入标准 Multi-Head Self-Attention
- 将 2D 特征图展平为 1D token 序列，计算二次复杂度的全局注意力
- 作用：突破卷积的局部感受野限制，建立长距离空间依赖

**Cross-Attention (LDM/SD 引入)**：
- 在 Self-Attention 后增加 Cross-Attention 层，Query 来自图像特征，Key/Value 来自文本编码器（CLIP）的输出
- 实现文本条件到图像特征的精细注入
- 这是文本到图像生成的关键机制

**对称 Skip Connections**：
- 编码器每一层的特征直接连接到解码器对应层，通过通道拼接（concatenation）融合
- 保留高分辨率细节信息，缓解下采样导致的信息损失

### 3.3 条件注入机制

| 机制 | 位置 | 方式 | 代表模型 |
|------|------|------|----------|
| Time Embedding | ResNet Block | 正弦位置编码 → MLP → AdaGN | DDPM, DDIM, LDM |
| AdaIN | 特征图 | 实例归一化参数调制 | 早期 StyleGAN 融合 |
| AdaGN | ResNet Block | 组归一化参数调制 | LDM, SD 1.x/2.x |
| Cross-Attention | 注意力层 | 文本 KV 与图像 Q 交互 | LDM, SD 1.x/2.x, SDXL |

### 3.4 U-Net 的局限性

1. **卷积的局部性**：3×3 卷积核的感受野有限，虽然通过堆叠和 Skip Connection 可以扩大，但本质上仍是局部操作。全局依赖必须依赖少量插入的 Self-Attention 层。

2. **难以 Scale**：U-Net 的参数量增加主要依赖增加通道数或深度，但通道数增加会导致显存消耗呈平方增长（因为特征图是 4D 张量）。SDXL 将 U-Net 扩展到约 2.6B 参数已接近工程极限，训练稳定性和收益都出现明显瓶颈。

3. **计算效率低下**：U-Net 的对称结构意味着大量计算花在编码器-解码器的重复卷积上。Skip Connection 虽然保留细节，但也增加了显存带宽压力。

4. **文本条件融合不够深入**：Cross-Attention 仅在特定层插入，文本信息对浅层特征的影响有限。

---

## 4. DiT 诞生：Transformer 进入扩散模型

### 4.1 核心思想

2023 年，Peebles & Xie 在论文 *"Scalable Diffusion Models with Transformers"* 中提出 DiT，核心思想极其简洁：**用标准的 Vision Transformer (ViT) 替代 U-Net 作为扩散模型的去噪网络**。

这一替换的动机来自两个观察：
- 在 NLP 中，Transformer 的 Scaling Law 已被充分验证（GPT-3/4）
- 在 CV 中，ViT 在分类任务上已证明可以替代 CNN
- 那么，Transformer 是否也能在生成任务中替代 U-Net？

DiT 的答案是肯定的，并且带来了意外的惊喜：**清晰的 Scaling Law**。

### 4.2 架构结构

```
输入: 噪声潜变量 z_t (4×32×32 或 4×64×64，取决于 VAE 压缩率)
        ↓
    [Patchify]
    将空间特征图切分为 p×p 的 patch
    例如: 4×32×32 → 每 patch 4×4×4=64 维 → 8×8=64 个 token
        ↓
    [Patch Embedding]
    Linear 投影到 D 维 (如 768, 1024, 1536)
    + 可学习的位置编码 (Positional Embedding)
        ↓
    ┌─────────────────────────────────────────┐
    │  Transformer Encoder × L 层              │
    │  ─────────────────────────────────────   │
    │  每层结构:                               │
    │    ┌─→ LayerNorm ─→ Multi-Head Self-Attn │
    │    │         (adaLN-Zero 调制)            │
    │    └──────────────────────────────────┘  │
    │    ┌─→ LayerNorm ─→ MLP (Feed-Forward)   │
    │    │         (adaLN-Zero 调制)            │
    │    └──────────────────────────────────┘  │
    │                                          │
    │  关键: 无 Cross-Attention!                │
    │  条件仅通过 adaLN 注入                   │
    └─────────────────────────────────────────┘
        ↓
    [Unpatchify]
    将 token 序列重组为空间特征图
        ↓
    [输出头]
    Linear 投影到原始通道数
        ↓
输出: 预测噪声 ε_θ(z_t, t, c)
```

### 4.3 Patchify：从图像到 Token

Patchify 是 DiT 将 2D 图像转换为 Transformer 可处理的 1D token 序列的关键操作：

- 输入：VAE 编码后的潜变量 `z_t ∈ R^{C×H×W}`（如 C=4, H=W=32）
- Patch 大小：`p × p`（如 p=2 或 p=4）
- Token 数量：`N = (H/p) × (W/p)`（如 32/2 × 32/2 = 256 个 token）
- 每个 token 的维度：`C × p × p`（如 4×2×2 = 16）
- 通过 Linear 层投影到模型维度 D

与 ViT 不同的是，DiT 处理的是**噪声潜变量**而非原始图像，因此 patch 的语义含义较弱，主要作为空间单元参与注意力计算。

### 4.4 Adaptive Layer Norm (adaLN)：条件注入的核心

DiT 最大的架构创新之一是 **adaLN-Zero**（Adaptive Layer Normalization with Zero Initialization）：

**标准 LayerNorm**：
```
LN(x) = γ · (x - μ) / σ + β
```
其中 γ, β 是可学习的固定参数。

**adaLN**：
```
adaLN(x, c) = γ(c) · (x - μ) / σ + β(c)
```
其中 γ(c), β(c) 是由条件 c（时间步 t + 文本条件）通过 MLP 动态生成的。

**adaLN-Zero**（DiT 采用）：
- 在初始化时，将 adaLN 的 γ 参数初始化为 **0**
- 这意味着：训练初期，adaLN 模块相当于恒等映射，Transformer 块的行为接近标准 ViT
- 随着训练进行，条件调制逐渐生效
- 这一技巧显著提升了训练的稳定性，尤其是在深层 Transformer 中

条件编码：
```
c = [embedding(t); embedding(text)]  # 拼接时间步和文本 embedding
γ, β, α = MLP(c)  # 投影为缩放、偏移、门控参数
adaLN-Zero(x, c) = (1 + γ) · LN(x) + β  # 残差前乘以门控 α
```

### 4.5 无 Cross-Attention 的设计选择

DiT 的一个显著特点是**完全摒弃 Cross-Attention**，所有条件信息仅通过 adaLN 注入。这一设计选择的影响：

- **优点**：架构简洁，与标准 ViT 完全一致，易于实现和扩展；注意力计算仅需 Self-Attention，无需处理异构模态的交互
- **局限**：文本条件的信息量受限于 adaLN 的维度（仅通过 γ, β, α 三个向量调制），对于复杂文本描述的精细控制可能不足

后续工作（如 SD3/MMDiT、FLUX）通过重新引入 Cross-Attention 或等效机制解决了这一局限。

### 4.6 Scaling Law：DiT 最重要的发现

DiT 论文的核心贡献不仅是架构本身，更是**验证了扩散模型中的 Scaling Law**：

| 模型规模 | 参数量 | 配置 | FID↓ (ImageNet 256×256) |
|----------|--------|------|------------------------|
| DiT-S | 33M | depth=12, width=384, heads=6 | ~20 |
| DiT-B | 130M | depth=12, width=768, heads=12 | ~15 |
| DiT-L | 458M | depth=24, width=1024, heads=16 | ~12 |
| DiT-XL | 675M | depth=28, width=1152, heads=16 | ~10 |
| DiT-XL/2 | 675M | patch=2 (更多 token) | ~8 |

关键发现：
1. **参数量↑ → 质量↑**：在固定计算预算下，更大的模型 consistently 获得更低的 FID
2. **计算量↑ → 质量↑**：在固定模型大小下，更多的训练步数/数据量 consistently 提升质量
3. **与 GAN 不同**：GAN 的扩展往往不稳定，而 DiT 的扩展呈现平滑的幂律关系
4. **与 NLP 呼应**：DiT 的 Scaling 行为与 GPT 系列类似，暗示生成模型可能遵循统一的 Scaling Law

这一发现为后续 3B (SD3)、12B (FLUX) 甚至更大规模的扩散模型提供了理论信心。

---

## 5. PixArt-α/Σ：高效训练策略

### 5.1 背景与动机

DiT 虽然验证了 Scaling Law，但其训练成本仍然高昂。PixArt 系列（华为诺亚方舟实验室，2023–2024）的核心问题是：**能否用更少的数据和计算资源，训练出与 SDXL 相当的 DiT 模型？**

答案是肯定的。PixArt-α 仅用 **10M 图像-文本对**（相比 LAION-5B 的 5B 规模）就达到了 SDXL 级别的生成质量，其核心在于**训练策略的分解设计**和**文本编码的解耦**。

### 5.2 架构特点

PixArt-α 的骨干是标准 DiT，但做了以下关键修改：

**1. 解耦文本编码 (Decoupled Text Encoding)**：
- 使用 **T5-XXL**（4.3B 参数）作为文本编码器，而非 CLIP
- T5 的文本理解能力显著强于 CLIP，尤其是复杂句法和长文本
- 文本编码与图像生成网络完全解耦：T5 预训练后冻结，仅输出文本 embedding 作为 DiT 的条件输入

**2. 三阶段分解训练 (Decomposed Training)**：

| 阶段 | 目标 | 数据 | 条件 | 作用 |
|------|------|------|------|------|
| Stage 1 | 像素依赖学习 | 无标签自然图像 | 仅时间步 t | 让 DiT 学会图像的统计先验（颜色、纹理、结构） |
| Stage 2 | 文本对齐学习 | 10M 图像-文本对 | 时间步 t + 文本 | 将文本语义与视觉概念关联 |
| Stage 3 | 质量提升 | 高质量图像-文本对 | 时间步 t + 文本 | 微调提升细节和美学质量 |

这一分解的关键洞察：
- 像素依赖（图像本身的统计规律）与文本对齐（跨模态关联）是两种不同性质的学习任务
- 先用无标签数据学习像素依赖，可以大幅减少后续文本对齐所需的配对数据量
- Stage 1 相当于"自监督预训练"，Stage 2 相当于"指令微调"

### 5.3 PixArt-Σ 的改进

PixArt-Σ 在 α 的基础上主要改进：
- **更高分辨率支持**：从 1024×1024 扩展到 2K、4K 分辨率
- **细节增强**：引入更精细的 VAE 和更长的训练时间
- **数据质量筛选**：使用美学评分模型筛选训练数据，提升生成图像的美学质量

### 5.4 效率对比

| 指标 | PixArt-α | SDXL | 比值 |
|------|----------|------|------|
| 训练数据量 | 10M | ~5B (LAION+内部) | **1/500** |
| 训练 GPU 小时 | ~3,000 A100 小时 | ~100,000+ A100 小时 | **1/30** |
| 参数量 | ~0.6B | ~2.6B (Base+Refiner) | 1/4 |
| 生成质量 (FID/人类偏好) | ≈ SDXL | 基准 | 相当 |

PixArt 系列证明：DiT 架构配合聪明的训练策略，可以实现**数据效率和计算效率的双重突破**。

---

## 6. SD3 / MMDiT：多模态 DiT

### 6.1 动机：DiT 的文本条件局限

DiT 的 adaLN 条件注入虽然简洁，但存在明显局限：文本信息仅通过 γ, β, α 三个向量调制每个 Transformer 层，对于复杂文本（如多个对象、空间关系、属性描述）的精细控制能力不足。SD3 的核心目标是：**让文本和图像在 Transformer 中实现更深度的交互**。

### 6.2 MMDiT 架构：Multimodal DiT

SD3 提出了 **MMDiT (Multimodal Diffusion Transformer)**，其核心创新是**文本和图像 token 分别处理，通过注意力机制交互**：

```
文本输入: "a red cat sitting on a blue chair"
        ↓
    [文本编码器]
    CLIP-L (77 token) + T5-XXL (256 token) → 双编码器融合
        ↓
    文本 Token 序列: T = [t_1, t_2, ..., t_M]  (M ≈ 333)
        ↓
    
图像输入: 噪声潜变量 z_t
        ↓
    [Patchify]
    图像 Token 序列: X = [x_1, x_2, ..., x_N]  (N = 16×16=256 for 32×32 latent)
        ↓

    ┌─────────────────────────────────────────┐
    │  MMDiT Transformer × L 层                  │
    │  ─────────────────────────────────────   │
    │                                          │
    │  每层包含两个并行的 Self-Attention:        │
    │                                          │
    │  图像分支:                               │
    │    Q_X, K_X, V_X = Proj(X)               │
    │    X' = Self-Attn(Q_X, K_X, V_X)         │
    │       ↓                                  │
    │    [Cross-Modal Attention]               │
    │    Q_X' 与 K_T, V_T 交互                 │
    │    (图像 Query 关注文本 Key/Value)       │
    │                                          │
    │  文本分支:                               │
    │    Q_T, K_T, V_T = Proj(T)               │
    │    T' = Self-Attn(Q_T, K_T, V_T)         │
    │       ↓                                  │
    │    [Cross-Modal Attention]               │
    │    Q_T' 与 K_X, V_X 交互                 │
    │    (文本 Query 关注图像 Key/Value)       │
    │                                          │
    │  两个分支的输出通过门控机制融合            │
    │                                          │
    └─────────────────────────────────────────┘
        ↓
    图像分支输出 → Unpatchify → 预测噪声
    文本分支输出 → 丢弃（仅用于训练时的交互）
```

### 6.3 双文本编码器

SD3 使用两个文本编码器的组合：

| 编码器 | 参数量 | 最大 token 数 | 特点 | 作用 |
|--------|--------|--------------|------|------|
| CLIP-L | ~400M | 77 | 视觉-语言对齐强，全局语义 | 提供高层语义 embedding |
| T5-XXL | ~4.3B | 256 | 文本理解深，长文本支持 | 提供细粒度文本特征 |

融合方式：将两个编码器的输出拼接后，通过 Linear 投影到统一的文本 token 维度。

### 6.4 与 DiT 的关键差异

| 特性 | DiT (2023) | MMDiT (SD3, 2024) |
|------|-----------|-------------------|
| 模态处理 | 仅图像 token | 图像 + 文本双路 token |
| 注意力类型 | 纯 Self-Attention | Self-Attention + Cross-Modal Attention |
| 条件注入 | adaLN-Zero (γ,β,α) | adaLN + 注意力交互 |
| 文本编码器 | 无（或外部 CLIP） | CLIP-L + T5-XXL 双编码器 |
| 文本 token 参与计算 | 否 | 是，与图像 token 共同进入 Transformer |
| 参数量 | 0.6B–7B | ~3B |
| 文本控制能力 | 中等 | 强（尤其是复杂描述） |

### 6.5 3B 参数规模的意义

SD3 的 ~3B 参数规模在当时是开源扩散模型中最大的之一。这一规模的选择反映了：
- MMDiT 的双路结构增加了参数量（需要两套 Q/K/V 投影矩阵）
- 更大的模型可以更好地利用双文本编码器的丰富信息
- Scaling Law 的延续：从 DiT-XL (675M) 到 SD3 (3B)，质量持续提升

---

## 7. FLUX：Flow Matching + Transformer

### 7.1 背景：从扩散到流匹配

FLUX（Black Forest Labs，2024）代表了 DiT 架构演进的另一个重要分支。其核心创新不仅是架构，更是**将训练目标从扩散（DDPM/DDIM）切换到 Flow Matching**。

Flow Matching 的核心思想：
- 扩散模型学习的是"去噪"（从噪声到数据的逆向过程）
- Flow Matching 学习的是"向量场"（定义从噪声到数据的直线路径上的速度场）
- 数学上，Flow Matching 是扩散模型的推广，但训练更稳定，采样更灵活

FLUX 证明：Flow Matching 与 Transformer 的结合，可以释放出比传统扩散目标更强的生成能力。

### 7.2 架构：统一文本/图像流的 Transformer

FLUX 的架构可以看作是 MMDiT 的进一步演化，但有一个关键区别：**文本和图像 token 不在两个独立分支中处理，而是在同一个统一的 Transformer 中混合处理**。

```
文本输入 → T5 编码 → 文本 Token 序列 T
图像输入 → Patchify → 图像 Token 序列 X

        ↓
    [拼接]
    统一序列: S = [T; X] = [t_1, ..., t_M, x_1, ..., x_N]
    (文本 token 在前，图像 token 在后)
        ↓
    ┌─────────────────────────────────────────┐
    │  Unified Transformer × L 层 (约 19 层双块)│
    │  ─────────────────────────────────────   │
    │                                          │
    │  每层: 所有 token (文本+图像) 共同进入     │
    │  单一的 Multi-Head Self-Attention          │
    │                                          │
    │  Q, K, V = Proj(S)  (统一投影)            │
    │  Attention 计算时:                        │
    │    - 文本 token 之间: 自注意力              │
    │    - 图像 token 之间: 自注意力            │
    │    - 文本 ↔ 图像: 交叉注意力 (隐式)        │
    │                                          │
    │  条件注入: adaLN + 时间步 embedding        │
    │                                          │
    └─────────────────────────────────────────┘
        ↓
    分离图像 token → Unpatchify → 预测速度场 v_θ(z_t, t, c)
    (文本 token 的输出仅用于中间层交互)
```

### 7.3 关键设计细节

**1. 双块结构 (Double Blocks)**：
- FLUX 的 Transformer 由两种块交替组成：
  - **Double Stream Block**：文本和图像 token 分别通过独立的 Q/K/V 投影，但在注意力计算中共享 attention map（即文本和图像的 Key/Value 互相可见）
  - **Single Stream Block**：文本和图像 token 完全混合，通过统一的 Self-Attention 处理
- 这种设计兼顾了模态特异性（双块）和深度融合（单块）

**2. 12B 参数规模**：
- FLUX.1 [dev]：约 12B 参数，开源可商用版本
- FLUX.1 [schnell]：约 12B 参数，4 步快速采样版本
- FLUX.1 [pro]：更大规模（未公开具体参数），API 专用

**3. 文本渲染能力**：
- FLUX 在图像中生成可读文本的能力显著强于 SD3 和之前的模型
- 这得益于：
  - T5 编码器的强文本理解能力
  - 文本 token 在 Transformer 中全程参与计算（而非仅在 Cross-Attention 层）
  - Flow Matching 的训练目标可能更适合学习细粒度结构

### 7.4 FLUX 的性能定位

| 模型 | 参数量 | 开源 | 文本渲染 | 图像质量 | 采样步数 |
|------|--------|------|----------|----------|----------|
| SDXL | ~2.6B | 是 | 差 | 良好 | 20–50 |
| SD3 | ~3B | 是 | 中等 | 良好 | 20–50 |
| DALL-E 3 | ~?B | 否 | 良好 | 优秀 | 未知 |
| Midjourney v6 | ~?B | 否 | 优秀 | 优秀 | 未知 |
| **FLUX.1 [dev]** | **~12B** | **是** | **优秀** | **优秀** | **20–50** |
| **FLUX.1 [schnell]** | **~12B** | **是** | **优秀** | **优秀** | **4** |

FLUX.1 [dev] 被广泛认为是 2024 年开源最强的图像生成模型，其 12B 参数规模和 Flow Matching 训练目标的结合，将 DiT 架构的潜力推向了新的高度。

---

## 8. SANA：Linear DiT 与实时生成

### 8.1 动机：注意力的二次复杂度瓶颈

DiT 及其后续变体（MMDiT、FLUX）的一个共同瓶颈是 **Self-Attention 的二次复杂度 O(N²)**：
- 对于 32×32 的 latent（patch=2），N = 256，N² = 65,536 —— 可接受
- 对于 64×64 的 latent（patch=2），N = 1024，N² = 1,048,576 —— 显著增加
- 对于高分辨率生成或视频（时空 token 数可达 10K+），N² 成为不可承受的负担

SANA（NVIDIA，2025）的核心目标是：**在保持 DiT 生成质量的前提下，将注意力的复杂度从 O(N²) 降低到 O(N)**。

### 8.2 架构创新：Linear DiT

SANA 的架构包含两个核心创新：

**1. Linear Attention (线性注意力)**：

标准 Self-Attention 的计算：
```
Attention(Q, K, V) = softmax(QK^T / √d) · V
复杂度: O(N² · d)  (因为 QK^T 是 N×N 矩阵)
```

Linear Attention 的核心思想：利用矩阵乘法的结合律，改变计算顺序：
```
LinearAttn(Q, K, V) = φ(Q) · (φ(K)^T · V)
                     = φ(Q) · (Σ_i φ(k_i)^T · v_i)
复杂度: O(N · d²)  (先计算 K^T·V 的 d×d 矩阵，再与 Q 相乘)
```

其中 φ(·) 是核函数（如 ReLU、elu+1），将 Q/K 映射到特征空间。

关键性质：
- 当 d << N 时（典型 d=64, N=1024），O(N·d²) << O(N²·d)
- 复杂度与序列长度 N 成**线性关系**，而非二次关系
- 全局感受野仍然保留（所有 token 仍然互相可见）

**2. DC-AE (Deep Compression Autoencoder)**：

标准 VAE（如 SD 使用的）将 512×512 图像压缩到 64×64 latent，压缩率 8×。
SANA 引入 **DC-AE**，将压缩率提升到 **32×**：
- 512×512 图像 → 16×16 latent（而非 64×64）
- Token 数量从 1024 减少到 64
- 即使使用标准注意力，N² 也从 1M 降到 4K

DC-AE 的关键挑战和解决方案：
- 更高压缩率通常导致信息损失和重建质量下降
- SANA 通过更深的编码器-解码器结构和特殊的训练目标（结合感知损失和对抗损失）来缓解

### 8.3 SANA 的架构概览

```
输入图像: 512×512×3
        ↓
    [DC-AE 编码器]
    压缩率 32× → 16×16×(C=32) latent
        ↓
    [Patchify]
    patch=1 (已足够小) → 256 个 token (16×16)
        ↓
    ┌─────────────────────────────────────────┐
    │  Linear DiT Transformer × L 层           │
    │  ─────────────────────────────────────   │
    │  每层:                                   │
    │    ┌─→ LayerNorm ─→ Linear Self-Attention │
    │    │         (adaLN 调制)                 │
    │    └──────────────────────────────────┘  │
    │    ┌─→ LayerNorm ─→ MLP                  │
    │    │         (adaLN 调制)                 │
    │    └──────────────────────────────────┘  │
    │                                          │
    │  复杂度: O(N·d²) ≈ O(256×64²) = 1M      │
    │  对比标准 DiT: O(N²·d) = O(256²×64) = 4M │
    │  (当 N 更大时，差距更显著)                │
    └─────────────────────────────────────────┘
        ↓
    [Unpatchify] → DC-AE 解码器 → 输出图像
```

### 8.4 性能：0.6B 匹敌 12B

SANA 最惊人的结果是：**0.6B 参数的 Linear DiT，在图像质量上匹敌 12B 参数的 FLUX**。

| 模型 | 参数量 | 注意力复杂度 | 单张 512×512 生成时间 (RTX 4090) | 质量 (FID/CLIP) |
|------|--------|-------------|----------------------------------|----------------|
| FLUX.1 [dev] | ~12B | O(N²) | ~15–30 秒 | 优秀 (基准) |
| SD3 | ~3B | O(N²) | ~5–10 秒 | 良好 |
| PixArt-Σ | ~0.6B | O(N²) | ~3–5 秒 | 良好 |
| **SANA** | **~0.6B** | **O(N)** | **~0.5–1 秒** | **≈ FLUX** |

这一结果的启示：
1. **架构效率 > 纯参数量**：通过 Linear Attention 和深度压缩，小模型可以实现大模型的效果
2. **实时生成成为可能**：0.5–1 秒的生成时间使消费级 GPU 实时交互成为现实
3. **O(N) 复杂度是扩展的关键**：对于视频（N 可达 10K+），Linear Attention 几乎是必需的

---

## 9. 视频 DiT：从图像到时空生成

### 9.1 核心挑战：从 2D 到 3D

将 DiT 从图像生成扩展到视频生成，核心挑战是**时序维度的引入**：
- 图像：2D 空间 (H×W)
- 视频：3D 时空 (T×H×W)，其中 T 是帧数
- 如果直接展平为 1D token 序列，N = T × (H/p) × (W/p)
- 对于 1 秒视频（24 帧），512×512，patch=2：N = 24 × 256 × 256 = 1,572,864 个 token
- 标准注意力的 N² 复杂度完全不可行

### 9.2 3D DiT 架构：空间注意力 + 时序注意力

视频 DiT 的通用架构采用**分解的 3D 注意力**：

```
输入: 噪声视频潜变量 z_t ∈ R^{C×T×H×W}
        ↓
    [3D Patchify]
    将时空体切分为 3D patch (t_p × p × p)
    例如: 每帧 4×32×32 latent, 8 帧
    → 8 × 16 × 16 = 2048 个 3D token
        ↓
    ┌─────────────────────────────────────────┐
    │  3D DiT Transformer × L 层               │
    │  ─────────────────────────────────────   │
    │                                          │
    │  每层包含两种注意力（顺序或交替）:         │
    │                                          │
    │  1. 空间注意力 (Spatial Self-Attention)    │
    │     - 同一帧内的 patch 互相注意力         │
    │     - 复杂度: O((H·W/p²)² · d) 每帧      │
    │     - 捕获单帧内的空间关系                │
    │                                          │
    │  2. 时序注意力 (Temporal Self-Attention) │
    │     - 同一空间位置的 patch 跨帧注意力     │
    │     - 复杂度: O(T² · d) 每位置           │
    │     - 捕获帧间的时间动态                  │
    │                                          │
    │  两种注意力可以:                          │
    │    - 顺序执行 (先空间后时序，或反之)      │
    │    - 交替执行 (层间交替)                  │
    │    - 联合执行 (3D 全注意力，但极昂贵)     │
    │                                          │
    └─────────────────────────────────────────┘
        ↓
    [3D Unpatchify] → 预测噪声/速度场
```

### 9.3 时序注意力的变体

| 类型 | 机制 | 复杂度 | 特点 | 代表模型 |
|------|------|--------|------|----------|
| 双向时序注意力 | 所有帧互相可见 | O(T²·d) | 全局时序依赖，适合短视频 | Wan, 部分 Sora 推测 |
| 因果时序注意力 | 仅当前帧及之前帧可见 | O(T²·d) | 适合自回归生成，长视频 | 可灵 (Kling) |
| 滑动窗口时序注意力 | 仅邻近 K 帧可见 | O(T·K·d) | 局部时序依赖，可扩展 | 部分高效视频模型 |
| 线性时序注意力 | 核技巧降复杂度 | O(T·d²) | 可扩展至长视频 | 推测未来方向 |

### 9.4 代表模型分析

**Sora (OpenAI, 2024.12)**：
- 推测架构：3D DiT + 双向时序注意力
- 推测规模：10B+ 参数
- 关键能力：
  - 生成 1 分钟 1080p 视频
  - 物理世界模拟（流体、刚体碰撞）
  - 长时序一致性（角色、场景保持）
- 推测技术：
  - 使用视频-文本对的大规模预训练
  - 可能采用级联生成（低分辨率→高分辨率）
  - 可能结合深度估计或 3D 先验

**可灵 (Kling, 快手, 2025.01)**：
- 架构：3D DiT + 因果时序注意力
- 特点：
  - 支持 2 分钟 1080p 视频生成
  - 因果注意力支持自回归扩展（先生成前 N 帧，再续接）
  - 强大的运动幅度和物理合理性
- 训练策略：
  - 大规模视频-文本对预训练
  - 高质量视频微调

**Wan (万相, 阿里巴巴, 2025.02)**：
- 架构：3D DiT + 双向时序注意力
- 特点：
  - 开源视频生成模型
  - 支持多种分辨率（480p, 720p, 1080p）
  - 支持文本到视频、图像到视频
- 意义：开源社区的视频 DiT 基准

**Veo 2 (Google, 2025.03)**：
- 架构：3D DiT 变体（具体细节未公开）
- 特点：
  - 高质量视频生成
  - 与 Google 生态深度整合

### 9.5 视频 DiT 的计算挑战

| 场景 | 帧数 T | 空间 token/帧 | 总 token N | 标准注意力 N² | 可行性 |
|------|--------|--------------|-----------|--------------|--------|
| 图像 | 1 | 256 (32×32) | 256 | 65K | ✓ |
| 短视频 (2s @ 8fps) | 16 | 256 | 4,096 | 16.7M | 勉强 |
| 中视频 (5s @ 24fps) | 120 | 256 | 30,720 | 943M | ✗ |
| 长视频 (10s @ 24fps) | 240 | 256 | 61,440 | 3.77B | ✗ |
| 长视频 (60s @ 24fps) | 1,440 | 256 | 368,640 | 136B | ✗ |

上表说明：对于超过几秒的视频，标准二次注意力的计算量完全不可行。解决方案包括：
1. **分解注意力**（空间+时序分离）：将 O(N²) 降为 O((HW)² + T²)
2. **Linear Attention**：将时序注意力降为 O(T·d²)
3. **稀疏注意力**：仅计算关键帧或采样帧的注意力
4. **级联生成**：先生成低帧率/低分辨率，再插帧/超分
5. **潜空间压缩**：使用 3D VAE 进一步压缩时空维度

---

## 10. 架构对比总结

### 10.1 U-Net vs DiT：核心差异

| 维度 | U-Net (DDPM/LDM/SD) | DiT (及其变体) |
|------|----------------------|----------------|
| **骨干网络** | 卷积编码器-解码器 | Transformer Encoder |
| **基本操作** | 3×3 卷积, ResNet | Self-Attention, MLP |
| **感受野** | 局部（卷积核大小）+ 少量全局注意力 | 全局（每层的 Self-Attention） |
| **条件注入** | AdaGN / Cross-Attention | adaLN-Zero / Cross-Modal Attention |
| **对称结构** | 是（Skip Connections） | 否（纯编码器结构） |
| **参数量扩展** | 困难（通道数↑→显存平方↑） | 容易（与 NLP Transformer 相同） |
| **Scaling Law** | 不明显（SDXL 2.6B 接近极限） | 清晰（0.6B→12B+ 持续提升） |
| **训练稳定性** | 较好（归纳偏置强） | 需要技巧（adaLN-Zero, 初始化） |
| **归纳偏置** | 强（平移等变性来自卷积） | 弱（需从数据学习空间关系） |
| **数据效率** | 较高（卷积的局部先验） | 较低（需更多数据学习空间关系） |
| **文本控制** | Cross-Attention（特定层） | adaLN（全层）或 Cross-Modal（全层） |
| **典型参数量** | 100M–2.6B | 0.6B–12B+ |

### 10.2 DiT 变体对比

| 模型 | 年份 | 核心变体 | 注意力类型 | 条件注入 | 文本编码器 | 参数量 | 关键创新 |
|------|------|----------|-----------|----------|-----------|--------|----------|
| DiT | 2023 | 标准 DiT | Self-Attention | adaLN-Zero | 无/外部 | 0.6B–7B | Scaling Law 验证 |
| PixArt-α/Σ | 2023–24 | 标准 DiT | Self-Attention | adaLN | T5-XXL | ~0.6B | 分阶段训练，数据效率 |
| SD3 / MMDiT | 2024 | 多模态 DiT | Self + Cross-Modal | adaLN + 注意力 | CLIP+T5 | ~3B | 文本-图像深度交互 |
| FLUX | 2024 | 统一流 Transformer | 统一 Self-Attention | adaLN | T5-XXL | ~12B | Flow Matching + 统一处理 |
| SANA | 2025 | Linear DiT | Linear Self-Attention | adaLN | T5-XXL | ~0.6B | O(N) 复杂度，实时生成 |
| Sora (推测) | 2024 | 3D DiT | 空间+时序注意力 | adaLN | 推测 T5/CLIP | 10B+ | 视频生成，物理模拟 |

### 10.3 计算复杂度对比

| 操作 | 标准 U-Net | 标准 DiT | MMDiT | Linear DiT (SANA) |
|------|-----------|----------|-------|-------------------|
| 卷积/投影 | O(C²·H·W) | O(D·C·p²·N) | O(D·C·p²·N + D·M) | O(D·C·p²·N) |
| 注意力 | O((H·W)²·d) (仅低层) | O(N²·D) | O((N+M)²·D) | O(N·D²) |
| 总复杂度 (512×512, 32×32 latent) | ~O(10⁸) | ~O(10⁸) | ~O(10⁸–10⁹) | ~O(10⁷) |
| 总复杂度 (视频, 120帧) | 不适用 | O(10¹²) | O(10¹²) | O(10⁹) |
| 显存占用 | 中等 | 高 (N² 注意力矩阵) | 更高 (双路) | 低 (线性核) |

注：N = token 数量, D = 模型维度, d = 头维度, M = 文本 token 数, C = 通道数, H,W = 空间尺寸, p = patch 大小

---

## 11. Scaling Law 分析

### 11.1 扩散模型中的 Scaling Law

DiT 论文首次系统验证了扩散模型中的 Scaling Law，其形式与 NLP 中的类似：

```
Loss ∝ C^(-α)  或  FID ∝ C^(-β)
```

其中 C 是计算量（FLOPs），α, β 是幂律指数。

**关键观察**：
1. **模型大小 Scaling**：固定训练步数，增加模型参数量 → Loss 平滑下降
2. **数据 Scaling**：固定模型大小，增加训练数据 → Loss 平滑下降
3. **计算 Scaling**：同时增加模型大小和数据量（遵循 Chinchilla 最优比例）→ 最优效率

### 11.2 从 DiT 到 FLUX 的 Scaling 轨迹

| 模型 | 参数量 | 估计训练数据量 | 估计计算量 (FLOPs) | 质量指标 |
|------|--------|---------------|-------------------|----------|
| DiT-S | 33M | ImageNet (1.3M) | ~10¹⁸ | FID ~20 |
| DiT-XL | 675M | ImageNet (1.3M) | ~10²⁰ | FID ~8 |
| PixArt-α | 0.6B | 10M | ~10²¹ | ≈ SDXL |
| SD3 | 3B | ~?M (推测 100M+) | ~10²² | 优于 SDXL |
| FLUX | 12B | ~?M (推测 1B+) | ~10²³ | 开源最优 |

### 11.3 Scaling 的边界与挑战

1. **数据瓶颈**：高质量图像-文本对的数量可能不如文本数据丰富，数据 Scaling 可能先于模型 Scaling 触及天花板
2. **计算成本**：12B 模型的训练成本已达数百万美元，100B 规模可能需要数十亿美元
3. **推理成本**：大模型的推理延迟是部署瓶颈，SANA 的 Linear DiT 路线可能是解决方案
4. **质量饱和**：FID 等指标可能饱和，人类偏好的提升更难量化

---

## 12. 挑战与未来方向

### 12.1 当前挑战

**1. 计算效率**：
- 标准 DiT 的二次注意力复杂度限制了高分辨率和长视频生成
- Linear Attention 是 promising 方向，但需验证在长序列上的稳定性

**2. 训练稳定性**：
- 大 Transformer 的训练需要精细的初始化（adaLN-Zero）和学习率调度
- 视频 DiT 的 3D 注意力引入额外的稳定性挑战

**3. 数据质量**：
- 生成质量的提升越来越依赖高质量训练数据，而非仅模型规模
- 视频-文本对的标注质量远低于图像-文本对

**4. 可控性**：
- 文本到生成的对齐仍有提升空间（复杂空间关系、数量、属性绑定）
- 细粒度控制（如精确的姿势、布局）需要额外的条件机制

**5. 物理一致性**：
- 视频生成中的物理规律（重力、碰撞、流体）仍难以稳定学习
- 可能需要结合物理引擎或 3D 先验

### 12.2 未来方向

**1. 更高效的注意力机制**：
- **Linear Attention** 的进一步优化（如 SANA 的后续工作）
- **Mamba / State Space Models**：将线性复杂度的序列模型引入生成任务
- **混合注意力**：全局线性注意力 + 局部精确注意力

**2. 多模态统一生成**：
- 图像、视频、音频、3D 的统一 DiT 架构
- 任意模态到任意模态的生成（如文本→视频→3D）

**3. 世界模型 (World Models)**：
- DiT 作为世界模型的生成组件，与强化学习结合
- 可交互的生成环境（如游戏场景生成）

**4. 端侧部署**：
- 模型压缩（量化、剪枝、蒸馏）使 DiT 可在手机端运行
- SANA 已证明 0.6B 模型可实现高质量，端侧 1B 模型可能成为现实

**5. 自回归 vs 扩散的融合**：
- 自回归模型（如 GPT-4o 的图像生成）与扩散模型的优劣比较
- 可能的融合：自回归生成 token，扩散细化细节

---

## 13. 参考链接

### 核心论文

1. **DDPM**: Ho, Jain & Abbeel. "Denoising Diffusion Probabilistic Models." NeurIPS 2020.  
   https://arxiv.org/abs/2006.11239

2. **DDIM**: Song et al. "Denoising Diffusion Implicit Models." ICLR 2021.  
   https://arxiv.org/abs/2010.02502

3. **LDM**: Rombach et al. "High-Resolution Image Synthesis with Latent Diffusion Models." CVPR 2022.  
   https://arxiv.org/abs/2112.10752

4. **DiT**: Peebles & Xie. "Scalable Diffusion Models with Transformers." ICCV 2023.  
   https://arxiv.org/abs/2212.09748

5. **PixArt-α**: Chen et al. "PixArt-α: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis." ICLR 2024.  
   https://arxiv.org/abs/2310.00426

6. **PixArt-Σ**: Chen et al. "PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation." arXiv 2024.  
   https://arxiv.org/abs/2403.04692

7. **SD3 / MMDiT**: Esser et al. "Scaling Rectified Flow Transformers for High-Resolution Image Synthesis." arXiv 2024.  
   https://arxiv.org/abs/2403.03206

8. **FLUX**: Black Forest Labs. "FLUX.1: State-of-the-Art Image Synthesis." 2024.  
   https://blackforestlabs.ai/flux-1/

9. **SANA**: Xia et al. "SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformer." arXiv 2025.  
   https://arxiv.org/abs/2410.10629

10. **Flow Matching**: Lipman et al. "Flow Matching for Generative Modeling." ICLR 2023.  
    https://arxiv.org/abs/2210.02747

### 视频生成相关

11. **Sora (技术报告)**: OpenAI. "Video Generation Models as World Simulators." 2024.  
    https://openai.com/research/video-generation-models-as-world-simulators

12. **Wan (万相)**: Alibaba. "Wan: Open Video Generation Model." 2025.  
    https://github.com/Wan-Video/Wan2.1

13. **Latte**: Ma et al. "Latte: Latent Diffusion Transformer for Video Generation." arXiv 2024.  
    https://arxiv.org/abs/2401.03048

### 技术博客与资源

14. **DiT GitHub**: https://github.com/facebookresearch/DiT
15. **PixArt GitHub**: https://github.com/PixArt-alpha/PixArt-alpha
16. **FLUX GitHub**: https://github.com/black-forest-labs/flux
17. **SANA GitHub**: https://github.com/NVlabs/Sana
18. **Hugging Face Diffusers**: https://github.com/huggingface/diffusers

### 综述与教程

19. **Diffusion Models Survey**: Yang et al. "Diffusion Models: A Comprehensive Survey of Methods and Applications." ACM Computing Surveys 2023.  
    https://arxiv.org/abs/2209.00796

20. **Flow Matching Survey**: Tong et al. "Flow Matching Tutorial." 2024.  
    https://flow-matching.github.io/

---

> **报告结语**: 从 2020 年 U-Net 垄断扩散模型，到 2023 年 DiT 开启 Transformer 时代，再到 2025 年 Linear DiT 实现实时生成，DiT 架构的演进展现了生成模型领域"架构创新 + Scaling Law + 效率优化"的三重驱动。未来，随着视频生成、多模态统一和世界模型的需求增长，DiT 及其变体将继续扮演核心角色，而 Linear Attention 等效率突破将是扩展至更长序列、更高分辨率的关键。

---

*报告完成日期: 2026年6月6日*
