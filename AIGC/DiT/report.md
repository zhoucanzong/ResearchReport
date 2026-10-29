---
display_name: 扩散 Transformer（DiT）
---

# Diffusion Transformer (DiT) 架构演进研究报告

> **报告日期**: 2026年10月25日
> **研究范围**: 从 U-Net 到 DiT 的生成模型架构范式转移（2020–2025）  
> **核心主题**: 去噪骨干、条件交互、训练目标与视频时空扩展

> **本报告的职责**：聚焦扩散模型中的 Transformer 去噪骨干、条件交互及其视频扩展；生成目标、噪声路径与采样器的基础机制见[扩散模型报告](../DiffusionModels/report.md)，不同图像生成路线之间的关系、任务能力与评测边界见[图像生成综述](../ImageGeneration/report.md)。适合在了解扩散基本过程后阅读，也可作为综述中 DiT 路线的机制分册。

跨媒介的表示与评测路线见 [AIGC 学习地图](../../docs/aigc-learning-path.md)；本篇只说明 Transformer 如何实现扩散去噪，不将 DiT 当成独立生成目标。

---

## 目录

1. [概述](#1-概述)
2. [发展时间线](#2-发展时间线)
3. [U-Net 时代：扩散模型的卷积基础](#3-u-net-时代扩散模型的卷积基础)
4. [DiT：潜变量 patch Transformer](#4-dit潜变量-patch-transformer)
5. [PixArt-α/Σ：训练分解与文本条件](#5-pixart-ασ训练分解与文本条件)
6. [SD3 / MMDiT：多模态 DiT](#6-sd3--mmdit多模态-dit)
7. [FLUX：Rectified Flow 与多模态 Transformer](#7-fluxrectified-flow-与多模态-transformer)
8. [SANA：压缩、注意力与采样协同](#8-sana压缩注意力与采样协同)
9. [视频生成：时空表示与生成顺序的不同选择](#9-视频生成时空表示与生成顺序的不同选择)
10. [架构对比总结](#10-架构对比总结)
11. [扩展性：当前证据能说明什么](#11-扩展性当前证据能说明什么)
12. [挑战与未来方向](#12-挑战与未来方向)
13. [参考链接](#13-参考链接)

---

## 1. 概述

DiT（Diffusion Transformer）不是一种新的生成目标，而是把扩散模型的去噪网络从卷积 U-Net 换成处理潜变量 patch 的 Transformer。理解这条路线要分开三个问题：**去噪骨干如何扩展**（DiT、PixArt、SANA），**文本与图像条件如何交互**（adaLN、cross-attention、MMDiT），以及**训练目标和采样路径如何选择**（扩散、rectified flow）。这些维度经常一起出现，但并非同一项创新。

DiT 原论文在类别条件 ImageNet 的 256²/512² 设置中，系统比较网络深度、宽度、patch size 与前向 FLOPs，并观察到所测模型 FLOPs 增大时 FID 通常下降。它证明 Transformer 去噪器在该实验范围内可扩展；它没有建立跨数据集、跨目标或无限规模成立的普遍 scaling law，也没有证明 U-Net 已到上限。

后续研究回答的是不同瓶颈：PixArt 把训练拆成图像先验、文本对齐和美学质量阶段，并加入文本 cross-attention；SD3/MMDiT 让文本和图像 token 在共享注意力计算中交互；FLUX 将 rectified-flow 目标与双流/单流 Transformer 组合；SANA 同时压缩视觉 latent、替换注意力并改造文本编码与采样。视频工作则不能简单理解为把图像 DiT 的 token 轴加上帧数：潜空间压缩、时空注意力的分解、因果性和长程状态管理共同决定可扩展性。

以下按“骨干—条件—目标—时空扩展”梳理代表论文，重点区分作者实验直接支持的结论与尚未公开的工业模型内部设计。建议先读第 3–4 节理解 U-Net 与 DiT 的差异，再读第 5–8 节追踪文本条件、训练目标和效率取舍，最后用第 9–11 节对照视频扩展及证据边界。

## 2. 发展时间线

| 路线 | 代表工作 | 主要解决的问题 | 阅读时应区分 |
|---|---|---|---|
| 潜空间扩散 + U-Net | LDM / Stable Diffusion（2021–22） | 将高分辨率像素扩散改在压缩 latent 上进行，以卷积多尺度骨干建模 | 潜空间计算收益来自表示压缩，不能全归因于 U-Net |
| Transformer 去噪器 | DiT（2022 预印本；ICCV 2023） | 在类别条件 ImageNet 上比较 patch、深度/宽度、FLOPs 与质量 | 原论文的 scaling 证据来自特定数据集、分辨率和训练设置 |
| 高效训练与文本条件 | PixArt-α/Σ（2023–24） | 数据标注密度、训练阶段分解、T5 与 cross-attention | 它不是“完全无 cross-attention 的标准 DiT” |
| 多模态注意力 | SD3 / MMDiT（2024） | 让不同模态有专属投影，同时在联合注意力中交换信息 | 架构变化针对文本图像交互，不等同于更好的所有生成能力 |
| 流目标 + Transformer | Rectified Flow / FLUX（2024） | 以流匹配训练路径与 Transformer 共同实现高分辨率生成 | 训练目标、骨干和模型规模是不同设计轴；闭源部分以公开材料为限 |
| 视觉 token 效率 | SANA（2024 预印本，后续版本） | 32× 压缩 AE、Linear DiT、文本编码器与采样共同降成本 | 论文报告的速度/质量比较依赖具体分辨率、硬件、采样和基线 |
| 视频时空建模 | Latte、CogVideoX、HunyuanVideo、Wan 等 | 在压缩视频 latent 中处理空间细节、运动与长程一致性 | 不同论文采用不同骨干/注意力设计，不能概括成一种“通用 3D DiT” |

此时间线刻画公开研究问题的转移，不按厂商产品发布顺序排列。

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

2. **难以 Scale**：U-Net 的参数量增加主要依赖增加通道数或深度，但通道数增加会导致显存消耗呈平方增长（因为特征图是 4D 张量）。SDXL 展示了更大 U-Net 的工程路线；但 DiT 论文没有通过 SDXL 规模比较来证明 U-Net 存在参数或质量上限。卷积特征图的显存/带宽开销与注意力 token 代价不同，实际取舍取决于分辨率、实现和训练预算。

3. **计算效率低下**：U-Net 的对称结构意味着大量计算花在编码器-解码器的重复卷积上。Skip Connection 虽然保留细节，但也增加了显存带宽压力。

4. **文本条件融合不够深入**：Cross-Attention 仅在特定层插入，文本信息对浅层特征的影响有限。

---

## 4. DiT：潜变量 patch Transformer

### 4.1 核心思想

2022 年预印本、后发表于 ICCV 2023 的 Peebles & Xie 论文 *"Scalable Diffusion Models with Transformers"* 中提出 DiT，核心思想极其简洁：**用标准的 Vision Transformer (ViT) 替代 U-Net 作为扩散模型的去噪网络**。

论文的问题是：将 latent patch 输入标准 Transformer 去噪器后，质量是否会随模型计算量扩展？作者在类别条件 ImageNet 上回答了这个问题；结果支持该实验范围内的扩展性，并不依赖“GPT 的 scaling law 可直接迁移”这一前提。

### 4.2 架构结构

```
输入: 噪声潜变量 z_t (原论文使用 4×32×32 latent)
        ↓
    [Patchify]
    将空间特征图切分为 p×p 的 patch
    例如: 4×32×32 latent、patch=2 → 4×2×2=16 维输入 patch，16×16=256 个 token
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
    │  类别条件通过 adaLN-Zero 注入；类别条件不是文本条件 │
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
其中 γ(c), β(c) 是由条件 c（原论文为类别标签与时间步）通过 MLP 动态生成的。

**adaLN-Zero**（DiT 采用）：
- 在初始化时，将 adaLN 的 γ 参数初始化为 **0**
- 这意味着：训练初期，adaLN 模块相当于恒等映射，Transformer 块的行为接近标准 ViT
- 随着训练进行，条件调制逐渐生效
- 这一技巧显著提升了训练的稳定性，尤其是在深层 Transformer 中

条件编码：
```
c = embedding(t) + embedding(class label)  # 原论文的类别条件设置
γ, β, α = MLP(c)  # 投影为缩放、偏移、门控参数
adaLN-Zero 对注意力与 MLP 子层的调制量及残差门控均零初始化
```

### 4.5 条件注入的设计选择

原论文以类别标签与扩散时间步作为条件，通过 adaLN-Zero 调制 Transformer 块。它没有对文本条件做对照，因而不能据此断言 adaLN 必然不适合文本，也不能把 PixArt 或 SD3 的改进单独归结为“修复 DiT 的文本缺陷”。PixArt 的 cross-attention 是文本到图像特征交互的显式通道；SD3 则令两种模态的 token 在联合注意力中双向交换信息，选择取决于条件信息量、计算开销和训练目标。

### 4.6 计算扩展证据的范围

DiT 论文的核心实验贡献之一，是在类别条件 ImageNet 上系统改变 DiT 的规模与 patch 设置，研究计算量和样本质量之间的关系：

按[DiT v2 §§4–5、表2及附录](https://arxiv.org/html/2212.09748v2)拆开：

| 模型与条件 | FID-50K↓ | 比较解释 |
|---|---:|---|
| DiT-XL/2，ImageNet 256²，adaLN-Zero，400K steps，无CFG | 19.47 | 模型约675M参数；不能与7M steps的结果直接比较架构 |
| 同模型，7M steps，无CFG | 9.62 | 增加训练预算后的结果 |
| 同模型，7M steps，CFG=1.50 | 2.27 | 表2的有引导结果；不应称为无引导FID |

论文扫描深度/宽度与patch大小后，发现前向Gflops较大通常对应更低FID；**参数量并不是唯一解释变量**，减小patch也会在参数基本不变时增加计算与质量。这里是所测架构和预算中的经验关系，不是任意固定算力预算下“大模型必胜”的定理，也没有据此证明所有GAN都不能稳定扩展。

---

## 5. PixArt-α/Σ：训练分解与文本条件

### 5.1 背景与动机

DiT 的证据来自类别条件 ImageNet，而文本到图像还需要学习图文对齐。PixArt 系列（华为诺亚方舟实验室，2023–2024）的核心问题是：**能否用更少的数据和计算资源，训练出与 SDXL 相当的 DiT 模型？**

PixArt-α 把问题拆成模型结构、训练阶段与数据标注三部分。论文报告其在 10M 图文对训练后，在其选用的基准与评测中达到有竞争力的结果；这不能概括为仅以 1/500 数据普遍复现 SDXL，也不表示只靠数据量解释质量。

### 5.2 架构特点

PixArt-α 沿用 Transformer 去噪器思路，但不是原论文类别条件 DiT 的简单标准配置：它加入文本 cross-attention，并使用 T5 文本表示。

**1. 解耦文本编码 (Decoupled Text Encoding)**：
- 使用 **T5-XXL**（4.3B 参数）作为文本编码器，而非 CLIP
- T5-XXL 提供较长文本序列表示；其与 CLIP 的能力差异不能只由编码器规模概括
- 文本编码与图像生成网络完全解耦：T5 输出文本表示供生成网络使用；报告比较需同时考虑文本编码、cross-attention、数据和训练阶段

**2. 三阶段分解训练 (Decomposed Training)**：

| 阶段 | 目标 | 数据 | 条件 | 作用 |
|------|------|------|------|------|
| Stage 1 | 像素依赖学习 | 无标签自然图像 | 仅时间步 t | 让 DiT 学会图像的统计先验（颜色、纹理、结构） |
| Stage 2 | 文本对齐学习 | 10M 图像-文本对 | 时间步 t + 文本 | 将文本语义与视觉概念关联 |
| Stage 3 | 质量提升 | 高质量图像-文本对 | 时间步 t + 文本 | 微调提升细节和美学质量 |

这一分解的关键洞察：
- 像素依赖（图像本身的统计规律）与文本对齐（跨模态关联）是两种不同性质的学习任务
- 先用无标签数据学习像素依赖，可以大幅减少后续文本对齐所需的配对数据量
- 这些阶段分别针对无条件视觉分布、图文对齐和美学质量；类比“指令微调”会掩盖其图像生成目标与文本指令微调的差异

### 5.3 PixArt-Σ 的改进

PixArt-Σ 在 α 的基础上主要改进：
- **更高分辨率支持**：从 1024×1024 扩展到 2K、4K 分辨率
- **细节增强**：引入更精细的 VAE 和更长的训练时间
- **数据质量筛选**：使用美学评分模型筛选训练数据，提升生成图像的美学质量

### 5.4 比较的适用范围

PixArt-α 论文给出数据、训练成本与基准结果，并报告在若干文本到图像评测上具竞争力。此处不将其与 SDXL 的训练数据量、GPU 小时和质量并排换算比例：两者内部数据、训练目标、分辨率、评测协议与算力口径并不完全一致。学习重点是其分解训练和密集 caption 的机制，以及这些组件各自的消融，而不是把单个总指标理解成数据缩减的因果结果。

---

## 6. SD3 / MMDiT：多模态 DiT

### 6.1 从条件调制到 token 交互

原始 DiT 的实验使用类别条件；文本到图像模型需要把较长的文本序列与图像 latent 对齐。SD3 的 MMDiT 让文本和图像保留各自的特征投影，但在每个 joint-attention 层中允许图像 token 读取文本 token、文本 token 读取图像 token。与把文本压成少量全局调制向量相比，这能提供逐 token 的交互路径；代价是更长的联合序列和更多多模态计算。

### 6.2 结构与设计取舍

SD3 使用 CLIP 与 T5 等文本编码器形成文本表示。MMDiT 为图像、文本模态分别设置 attention 投影参数，再把两侧的 Q/K/V 组合进行联合注意力计算；两个分支的输出再各自经过相应变换。它不是“先各做 self-attention、再串接两个 cross-attention”的普通双塔结构，也不是完全共享一套投影的普通 self-attention。

| 设计 | 对读者意味着什么 | 代价或边界 |
|---|---|---|
| 模态专属投影 | 模型可保留文本和视觉特征空间差异 | 参数量和实现复杂度增加 |
| 联合注意力 | 双向跨模态信息可在多层传播 | 序列长度增加带来注意力开销；交互能力不等于空间关系必然正确 |
| 多文本编码器 | 兼顾图文对齐与更丰富的语言表示 | 编码器成本较高，实际能力仍取决于训练数据和任务 |

该机制是架构设计，不是质量保证。论文的文本理解、排版和人类偏好结果是在其训练数据、模型规模、采样配置和评测协议下获得；不能将单项能力提升解释为“联合注意力已解决组合绑定”。后续编辑、参考图和空间控制还需独立条件路径。

### 6.3 与 DiT 的关系

| 维度 | DiT 原论文 | SD3 / MMDiT |
|---|---|---|
| 主要实验任务 | 类别条件 ImageNet | 文本到图像 |
| 条件表示 | 类别与时间步的 adaLN-Zero | 文本/图像 token 与模态专属投影 |
| 模态交互 | 原论文未研究图文 token 交互 | 联合注意力中的双向交互 |
| 可比较结论 | 去噪 Transformer 在 ImageNet 设定中的计算扩展 | 多模态表示与高分辨率 T2I 训练设计 |

任务与训练规模不同，所以不能把两篇论文当成只改变条件模块的严格对照实验。

## 7. FLUX：Rectified Flow 与多模态 Transformer

### 7.1 背景：从扩散到流匹配

FLUX（Black Forest Labs，2024）代表了 DiT 架构演进的另一个重要分支。其核心创新不仅是架构，更是**将训练目标从扩散（DDPM/DDIM）切换到 Flow Matching**。

Flow Matching 的核心思想：
- 扩散模型学习的是"去噪"（从噪声到数据的逆向过程）
- Flow Matching 学习的是"向量场"（定义从噪声到数据的直线路径上的速度场）
- 数学上，Flow Matching 是扩散模型的推广，但训练更稳定，采样更灵活

Flow Matching 是生成轨迹/训练目标的选择；Transformer 是去噪网络骨干。FLUX 将二者组合，但现有跨模型质量比较混有数据、模型容量、编码器与采样等差异，不能把质量差异单独归因于 Flow Matching。

### 7.2 架构：统一文本/图像流的 Transformer

FLUX 的公开实现采用双流块与单流块：前者保持文本/图像各自的投影路径并进行联合注意力，后者进一步合并 token 流。细节依据公开实现与相关技术材料；不据此推断 FLUX [pro] 等未公开版本的内部结构。

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

**3. 能力归因边界**：公开评测显示 FLUX 在若干文字渲染与提示遵循测试中表现较强，但数据、架构、规模、训练及采样同时变化，不能从这些观察识别出 T5、双流/单流结构或 Flow Matching 各自的因果贡献。

### 7.4 阅读结果时的比较边界

FLUX 的公开报告展示了其在文本对齐、排版和人类偏好等方面的结果；这些结果应结合论文评测协议、公开模型版本、硬件和采样步数阅读。与 SD3、SDXL、DALL·E 或 Midjourney 的跨报告排名表无法控制训练数据、版本、评测器与推理预算，因此不用于判断哪种架构或训练目标单独更优。此处保留的结论是机制层面的：多模态 token 路径与 rectified-flow 训练共同构成系统设计，现有对照并未隔离其各自贡献。

---

## 8. SANA：压缩、注意力与采样协同

### 8.1 它要解决的不是单一的注意力问题

SANA 面向高分辨率图像生成的计算与延迟。其论文把 **32× Deep Compression Autoencoder（DC-AE）**、Linear DiT、文本编码器、数据筛选和少步采样组合起来。因此实验中的吞吐收益不能只归因于 Linear Attention；更高 latent 压缩会减少 token 数，采样器减少去噪步数，文本编码器与数据策略也会影响质量。

### 8.2 线性注意力与表示压缩的作用

标准注意力构造 token 两两交互，主要注意力项随序列长度 $N$ 二次增长。SANA 使用 ReLU linear attention 共享键值聚合项，并以 Mix-FFN 的深度卷积补足局部信息；其分析在固定特征维度下将注意力复杂度对 $N$ 的增长降至线性。论文也报告线性注意力收敛更慢，说明效率优势伴有优化代价。其 NoPE 设计利用 Mix-FFN 注入局部位置信息。DC-AE 则通过更高压缩率降低 latent token 数，但压缩率增大也会提高重建损失风险，需要在 tokenizer/decoder 质量与 transformer 开销之间权衡。

这组机制也包括 Mix-FFN 与 NoPE，不能简化为“Linear Attention + AE”两项。改动互补而非互相替代：压缩 AE 减少要处理的 token；Linear Attention 降低每 token 数变大时的注意力成本；Mix-FFN 用深度卷积聚合邻近 token 的局部信息。论文报告 SANA-0.6B 在其文本到图像基准、硬件和采样配置下相对 FLUX-12B 具有竞争力且推理更快。它不是跨任务“0.6B 等于 12B”的结论，也没有证明 Linear Attention 是长视频生成的必要条件。

### 8.3 适用边界

| 阅读角度 | 可支持的结论 | 不应外推的结论 |
|---|---|---|
| 压缩表示 | 高压缩 AE 可显著减少图像 latent token | 压缩不会损害细节或可控性 |
| 注意力 | 线性注意力可作为长序列效率方案 | 它在所有质量、分辨率和任务上都优于标准注意力 |
| 端侧推理 | 论文展示特定 SANA 配置可在有限显存设备生成 | 任意 0.6B DiT 都能在消费级设备实时运行 |
| 模型比较 | 论文报告其指定基准上的竞争力、吞吐和质量 | 跨论文分数/时间直接可比或模型规模单独决定胜负 |



## 9. 视频生成：时空表示与生成顺序的不同选择

图像 DiT 的结论不能直接移植到视频。视频先经时空 VAE 压缩，再由模型处理具有空间、时间和动作关系的 latent。帧数只是成本的一部分：空间/时间压缩率、patch 形状、注意力连接方式、是否双向生成、是否要流式输出都会影响质量和延迟。把原始像素帧数直接乘上图像 token 数会严重高估实际序列长度，也无法比较不同论文。

### 9.1 代表路线与取舍

| 工作 | 表示/机制 | 它解决的问题 | 证据边界 |
|---|---|---|---|
| [Latte](https://arxiv.org/html/2401.03048) §3–4 | 在视频 latent 中构造时空 token，并比较空间/时间维度分解的 Transformer 变体 | 将图像 DiT 扩展到视频，同时控制 token 交互成本 | 论文在 FaceForensics、SkyTimelapse、UCF101、Taichi-HD 等数据集研究，不能直接代表开放域商业 T2V |
| [CogVideoX](https://arxiv.org/html/2408.06072) §§2–4 | 3D causal VAE 压缩时空信息；DiT 中结合 expert AdaLN 与 3D RoPE | 让长时间与空间位置在压缩 latent 中建模，改善文本视频生成 | 结论针对公开模型/版本及论文评测设置；不是所有视频 DiT 的模板 |
| [HunyuanVideo](https://arxiv.org/html/2412.03603) §§4.1–4.4 | 公开的 13B 视频 DiT 采用双流到单流的多模态 Transformer，联合文本/视频 token，并使用 3D RoPE | 统一多模态交互，并在视频生成任务中扩展模型容量 | 作者报告的基准和偏好评测属于其特定数据、模型和评测协议 |
| [Wan](https://arxiv.org/html/2503.20314) §§4–5 | 时空 VAE、视频 DiT、数据/训练与推理优化共同组成开放视频模型 | 关注高压缩表示、较大规模训练及图像转视频、编辑等任务 | 技术报告覆盖多组件，质量和效率不能单独归因于 Transformer block |
| [CausVid](https://arxiv.org/html/2412.07772) §§4–5 | 将双向视频扩散模型蒸馏为因果生成器，并使用 KV cache | 将一次性整段生成改成低延迟、可流式生成 | 论文在其模型上做双向教师→因果学生蒸馏；存在逐步误差积累与教师能力继承边界 |

这些路线体现两个相互关联的问题。第一，**全局一致性与流式响应之间有冲突**：双向 attention 可让整段视频共同去噪，但生成下一段前要看未来帧；因果模型能边生成边响应输入，却要控制历史条件和误差累积。第二，**压缩和运动细节之间有冲突**：时空 VAE 减少 token，但过度压缩会损失纹理、细动作和时间边界信息。将生成结果称为“物理模拟”也需要谨慎：论文中的连贯运动或特定物理场景样例并不等于显式物理状态建模或稳定规律保证。

### 9.2 闭源系统的证据范围

Sora 技术报告用时空 patches 描述视频表示和训练方式，但未公开完整网络与训练配方；其展示的模拟能力不等于物理一致性保证。Veo、可灵等系统若没有公开一手技术材料，内部骨干、注意力形式和参数规模仍未知，不能由生成样例或产品规格反推。

### 9.3 读论文时关注的评测

视频论文通常分别评估文本对齐、单帧视觉质量、运动幅度/连贯性和人类偏好；单一聚合分数可能掩盖镜头运动、主体身份、短时细节或长时间一致性退化。阅读结果时需同时记录数据集、视频长度/帧率、分辨率、采样步数、评测器和比较基线。当前公开基准仍难充分测量长程因果、物体持续性和物理规律，因此展示样例不应替代系统评测。



## 10. 架构对比总结

### 10.1 U-Net 与 DiT 的取舍

| 维度 | 卷积 U-Net | Transformer 去噪器 |
|---|---|---|
| 空间归纳偏置 | 多尺度卷积提供局部与平移等变先验 | 全局 token 交互更直接，但需学习空间关系 |
| 条件路径 | 时间调制、跨注意力、跳连等可组合 | adaLN、cross-attention、joint attention 均可用，取决于具体模型 |
| 高分辨率成本 | 特征图卷积与 skip connection 占用较多激活/带宽 | 注意力对 token 数敏感，patch 与 latent 压缩决定成本 |
| 证据 | 长期用于扩散并可形成高质量系统 | DiT 在类别条件 ImageNet 上给出受控扩展实验；T2I 发展需另看 PixArt、SD3 等 |

不存在基于这些论文即可宣布的单一胜者或 U-Net 的统一规模上限。

### 10.2 代表模型的机制对照

| 工作 | 去噪骨干/条件路径 | 训练或效率侧重点 | 关键边界 |
|---|---|---|---|
| DiT | latent patch Transformer；类别/时间步 adaLN-Zero | 在 ImageNet 研究 FLOPs、深度/宽度和 patch | 类别条件结果不能直接解释开放文本生成 |
| PixArt-α | T2I Transformer + 文本 cross-attention + T5 | 训练分解、密集 caption 与高效数据/训练流程 | 其对照涉及训练配方与数据，非单变量架构比较 |
| SD3 / MMDiT | 模态专属投影 + 文本/图像 joint attention | 多模态交互和高分辨率 rectified-flow 训练 | joint attention 不自动保证准确计数/空间绑定 |
| FLUX | 双流/单流 Transformer；rectified-flow 目标 | 模态交互与采样/训练路径 | 不能从模型总体表现拆出目标函数的单独贡献 |
| SANA | Linear DiT + 高压缩 AE | 减少 token 与注意力成本，并调整编码/采样 | 多项改动共同贡献效率 |
| Latte / CogVideoX / HunyuanVideo / Wan | 视频 latent 上的不同空间、时间或多模态 token 交互 | 建模时序、压缩与视频任务扩展 | “视频 DiT”不是单一架构，按论文与版本比较 |



### 10.3 计算量的主要来源

- U-Net 的卷积开销随特征图空间尺寸、通道数和层数增长；多尺度下采样能控制部分高分辨率计算，但 skip feature 需要额外存储/带宽。
- 标准 Transformer 的注意力项约随 token 数 (N) 的平方增长，MLP 与投影则随 (N) 线性增长并依赖隐藏维度。减小 patch 会增加 token 数，即使参数量变化不大，也会显著改变注意力成本。
- MMDiT 把文本 token 与图像 token 纳入联合注意力，计算取决于两种 token 总长度及模态投影；多模态表示能力需与这笔开销一起衡量。
- Linear DiT 改变注意力计算形式；SANA 同时降低视觉 token 数，所以不能把其效率简单归因于线性注意力一项。
- 视频模型需将时空 VAE 压缩率、空间/时间 token 数、注意力图样及去噪步数一起纳入；不能用原始像素帧数直接宣称统一的 FLOPs 数值。

这些复杂度关系适合解释设计动机，不代替针对具体实现、分辨率、精度和硬件的实测。

## 11. 扩展性：当前证据能说明什么

### 11.1 DiT 的受控结果

DiT 原论文在类别条件 ImageNet 256²/512² 比较不同深度、宽度、patch size 和训练计算。其观察是：在报告的模型集合与训练设定内，更高前向 FLOPs 通常伴随更低 FID；减少 patch size 会增加 token 和计算，即使参数量相近也可改变质量。作者没有建立跨数据规模、文本条件、视频任务和无限计算范围的通用幂律，也没有从 DiT 与 PixArt/SD3/FLUX 的跨论文数字推导一条可比的“规模轨迹”。

FID 还会受采样器、引导强度、训练步数、VAE 和评测实现影响。DiT 论文表格中的训练预算与 CFG 设置不同，因而直接并列单个 FID 会混合架构、训练时长和推理条件；引用时必须保留条件。

### 11.2 结构扩展与任务扩展

对 T2I，增加参数只是因素之一；更丰富的 caption、文本编码器、模态交互、图像 latent 质量和偏好优化都可能改变结果。对视频，数据筛选、时空 VAE、视频长度、运动覆盖、时空注意力与推理缓存同样重要。跨论文模型规模表通常无法控制这些条件，因此不应将未知训练数据量、估算 FLOPs 或未经统一评测的质量排名拼成 scaling law。

更有解释价值的研究问题是：固定数据与训练预算时，哪项改变提高目标能力；在质量相当时，哪项改变降低采样成本；压缩或因果化引入的失败是否可检测并纠正。当前报告以论文各自的 ablation 和测试条件回答这些问题，不做跨系统重算。



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
- **生成即理解（统一接口）**：Vision Banana（arXiv:2604.20329）把语义/实例/指代分割与度量深度、表面法向的输出全部参数化成可反解回指标的 RGB 图像、由同一个图像生成器按 prompt 生成，说明生成器的输出空间本身就能充当跨任务的统一接口而无需专用头（[精读分册](../../Models/Google-Gen/papers/2604.20329-vision-banana.md)；该论文未披露基座 NBP 架构，此处不假定其为 DiT）。

**3. 世界模型 (World Models)**：
- DiT 作为世界模型的生成组件，与强化学习结合
- 可交互的生成环境（如游戏场景生成）

**4. 端侧部署**：
- 模型压缩（量化、剪枝、蒸馏）使 DiT 可在手机端运行
- SANA 已证明 0.6B 模型可实现高质量，端侧 1B 模型可能成为现实

**5. 自回归 vs 扩散的融合**：
- 比较架构已公开的自回归图像生成路线（如早期 DALL-E、Janus）与扩散 / 流匹配路线；GPT-4o 图像生成的具体实现未披露，不能归为自回归模型
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

14. **CogVideoX**: Yang et al. "CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer." arXiv 2024.
    https://arxiv.org/abs/2408.06072

15. **HunyuanVideo**: Kong et al. "HunyuanVideo: A Systematic Framework For Large Video Generation Model." arXiv 2024.
    https://arxiv.org/abs/2412.03603

16. **Wan**: Wan Team. "Wan: Open and Advanced Large-Scale Video Generative Models." arXiv 2025.
    https://arxiv.org/abs/2503.20314

17. **CausVid**: Yin et al. "From Slow Bidirectional to Fast Autoregressive Video Diffusion Models." arXiv 2024.
    https://arxiv.org/abs/2412.07772

### 技术博客与资源

18. **DiT GitHub**: https://github.com/facebookresearch/DiT
19. **PixArt GitHub**: https://github.com/PixArt-alpha/PixArt-alpha
20. **FLUX GitHub**: https://github.com/black-forest-labs/flux
21. **SANA GitHub**: https://github.com/NVlabs/Sana
22. **Hugging Face Diffusers**: https://github.com/huggingface/diffusers

### 综述与教程

23. **Diffusion Models Survey**: Yang et al. "Diffusion Models: A Comprehensive Survey of Methods and Applications." ACM Computing Surveys 2023.
    https://arxiv.org/abs/2209.00796

24. **Flow Matching Survey**: Tong et al. "Flow Matching Tutorial." 2024.
    https://flow-matching.github.io/

---

> **报告结语**：这条路线不是 U-Net 被 Transformer 线性替代的单向故事。DiT 提供了特定图像任务中的计算扩展证据；PixArt、SD3、FLUX 和 SANA 分别改变数据/条件交互、模态注意力、训练目标和 token 效率；视频论文又将时空压缩、长程一致性与因果生成带入问题。比较工作时先分清目标、表示、条件机制和评测范围，才能判断一项改动解决了什么问题、付出了什么代价。

---
