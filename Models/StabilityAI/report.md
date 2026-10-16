# Stability AI / Black Forest Labs 图像生成模型系列研究报告

> 报告日期：2026年6月6日
> 研究范围：Stable Diffusion 1.x → SDXL → SD3 → FLUX → SD3.5 全系列架构演进
> 核心主线：U-Net → DiT → MMDiT → Flow Matching Transformer 的结构范式迁移

---

## 目录

1. [概述](#1-概述)
2. [发展时间线](#2-发展时间线)
3. [每代模型架构详解](#3-每代模型架构详解)
   - 3.1 Stable Diffusion 1.x (2022)
   - 3.2 Stable Diffusion 2.x (2022)
   - 3.3 SDXL (2023)
   - 3.4 Stable Diffusion 3 (2024)
   - 3.5 FLUX (2024, Black Forest Labs)
   - 3.6 SD3.5 / 后续迭代 (2025)
4. [架构演进对比](#4-架构演进对比)
5. [开源生态与工具链](#5-开源生态与工具链)
6. [与竞品对比](#6-与竞品对比)
7. [挑战与未来方向](#7-挑战与未来方向)
8. [参考链接](#8-参考链接)

---

## 1. 概述

Stability AI 是开源图像生成领域的奠基者之一。自 2022 年发布 Stable Diffusion 1.x 以来，其模型族经历了从 **U-Net-based LDM** 到 **Transformer-based Diffusion** 再到 **Flow Matching Transformer** 的深刻范式转变。2024 年，原 Stability AI 核心研究团队（Robin Rombach、Andreas Blattmann、Dominik Lorenz 等）出走成立 **Black Forest Labs (BFL)**，并推出 FLUX 系列模型，标志着开源文生图技术进入新的竞争格局。

本报告系统梳理 Stability AI / BFL 模型族的架构演进脉络，重点分析：

- **骨干网络**：U-Net → DiT → MMDiT → Flow Matching Transformer
- **条件注入机制**：AdaGN → Cross-Attention → 统一多模态注意力
- **文本编码器**：CLIP → OpenCLIP → CLIP + T5 双/三编码器
- **生成框架**：DDPM → LDM → Flow Matching
- **开源生态**：ComfyUI、LoRA、ControlNet、IP-Adapter 等插件体系

---

## 2. 发展时间线

| 时间 | 模型/事件 | 核心架构 | 参数量 | 关键特性 |
|------|-----------|----------|--------|----------|
| 2022.08 | **Stable Diffusion 1.4** | LDM (VAE + U-Net + CLIP) | ~890M (U-Net) | 开源文生图里程碑，消费级 GPU 可运行 |
| 2022.10 | **Stable Diffusion 1.5** | LDM (同上) | ~890M | 社区微调基础模型 |
| 2022.11 | **Stable Diffusion 2.0** | LDM (OpenCLIP) | ~865M | 重新训练，OpenCLIP ViT-H 替代 CLIP |
| 2022.12 | **Stable Diffusion 2.1** | LDM (OpenCLIP) | ~865M | 输出分辨率 768x768 |
| 2023.07 | **SDXL 1.0** | Base + Refiner 两级 U-Net | Base 3.5B + Refiner 1.3B | 1024x1024 原生分辨率，双文本编码器 |
| 2023.11 | **SDXL Turbo** | SDXL + Adversarial Distillation | Base 3.5B | 单步/少步推理，实时生成 |
| 2024.06 | **Stable Diffusion 3** | MMDiT (Multimodal Diffusion Transformer) | 2B / 4B / 8B | 彻底抛弃 U-Net，Flow Matching |
| 2024.08 | **FLUX.1 [pro]** | Flow Matching Transformer | 12B | BFL 成立，最强文本渲染 |
| 2024.08 | **FLUX.1 [dev]** | Flow Matching Transformer | 12B | 开源可商用，Apache 2.0 |
| 2024.08 | **FLUX.1 [schnell]** | Flow Matching Transformer | 12B | 本地极速版，1-4 步 |
| 2024.10 | **FLUX.1.1 [pro]** | Flow Matching Transformer | 12B | 质量与速度双提升 |
| 2024.10 | **FLUX.1 Tools** | 基于 FLUX 的编辑套件 | 12B | Fill、Canny、Depth、Redux |
| 2025.01 | **SD3.5** | MMDiT 改进版 | 2B / 4B / 8B | Stability AI 后续迭代，社区适配 |
| 2025.03 | **FLUX.2 [pro]** | Flow Matching Transformer | 未公开 | BFL 下一代，视频生成扩展 |

---

## 3. 每代模型架构详解

### 3.1 Stable Diffusion 1.x (2022)

#### 3.1.1 整体架构：Latent Diffusion Model (LDM)

SD 1.x 的核心架构为 **Latent Diffusion Model**，将扩散过程从像素空间迁移到潜空间（Latent Space），大幅降低计算成本。整体由三个模块组成：

```
┌─────────────────────────────────────────────────────────────┐
│                    Stable Diffusion 1.x                      │
├─────────────────────────────────────────────────────────────┤
│  Text Prompt                                                │
│      │                                                      │
│      ▼                                                      │
│  ┌──────────────┐    Text Embedding (77, 768)              │
│  │ CLIP Text    │─────────────────────┐                      │
│  │ Encoder      │                     │                      │
│  │ (ViT-L/14)   │                     │                      │
│  └──────────────┘                     │                      │
│                                       ▼                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    U-Net (890M)                       │   │
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐         │   │
│  │  │ Down    │───▶│ Mid     │───▶│ Up      │         │   │
│  │  │ Blocks  │    │ Blocks  │    │ Blocks  │         │   │
│  │  │(ResNet+ │    │(ResNet+ │    │(ResNet+ │         │   │
│  │  │ SelfAttn│    │ SelfAttn│    │ SelfAttn│         │   │
│  │  │+CrossAttn│   │+CrossAttn│   │+CrossAttn│        │   │
│  │  └─────────┘    └─────────┘    └─────────┘         │   │
│  │       ▲                              │               │   │
│  │       └────── Latent (64, 64, 4) ────┘               │   │
│  └──────────────────────────────────────────────────────┘   │
│       ▲                              │                       │
│       │                              ▼                       │
│  ┌──────────────┐              ┌──────────────┐              │
│  │ VAE Encoder  │              │ VAE Decoder  │              │
│  │  (KL-f8)     │              │  (KL-f8)     │              │
│  │  512x512x3   │              │  512x512x3   │              │
│  └──────────────┘              └──────────────┘              │
│       ▲                              │                       │
│  Input Image                    Output Image                 │
└─────────────────────────────────────────────────────────────┘
```

#### 3.1.2 VAE：KL-f8 潜空间编码器

- **编码器**：将 512×512×3 的 RGB 图像压缩为 64×64×4 的潜变量（下采样因子 f=8）
- **解码器**：将潜变量还原为像素空间图像
- **损失函数**：KL 散度约束 + 感知损失（LPIPS）+ 像素级 MSE
- **关键设计**：潜空间通道数仅 4，相比像素空间 3 通道 RGB，信息密度更高

#### 3.1.3 U-Net：去噪核心网络

U-Net 是 SD 1.x 的去噪骨干网络，参数量约 **890M**，结构特点：

**下采样路径（Encoder）**：
- 4 个下采样阶段（64×64 → 32×32 → 16×16 → 8×8）
- 每个阶段包含 2 个 ResNet block
- 自注意力（Self-Attention）仅在 16×16 和 8×8 分辨率插入
- 交叉注意力（Cross-Attention）在每个 ResNet block 后插入，Q/K 来自文本 embedding，V 来自图像特征

**中间层（Bottleneck）**：
- 2 个 ResNet block + Self-Attention + Cross-Attention
- 最低分辨率 8×8，通道数 1280

**上采样路径（Decoder）**：
- 4 个上采样阶段，与下采样路径对称
- Skip Connection 将同层编码器特征直接连接到解码器

**条件注入机制**：
- **时间步编码**：通过正弦/余弦位置编码（Sinusoidal Embedding）将离散时间步 t 编码为连续向量
- **AdaGN（Adaptive Group Normalization）**：时间步 embedding 通过 MLP 生成缩放和平移参数，注入到 GroupNorm 中
- **Cross-Attention**：文本条件通过 Transformer-style 交叉注意力注入，Q 来自图像特征，K/V 来自文本 embedding

#### 3.1.4 文本编码器：CLIP ViT-L/14

- 使用 OpenAI 的 **CLIP ViT-L/14** 文本编码器
- 最大 token 长度：77
- 输出维度：768
- 文本 embedding 通过 Cross-Attention 注入 U-Net 的每一层

#### 3.1.5 训练数据与配置

- **数据集**：LAION-5B 子集（LAION-2B-en 等），约 23 亿图文对
- **分辨率**：512×512
- **优化器**：AdamW，学习率 1e-4
- **训练硬件**：256 张 A100，约 15 万 GPU 小时
- **许可证**：CreativeML Open RAIL-M（允许商用，有限制条款）

---

### 3.2 Stable Diffusion 2.x (2022)

#### 3.2.1 主要改进

SD 2.x 并非 SD 1.x 的增量更新，而是**完全重新训练**的模型，核心变化：

| 维度 | SD 1.x | SD 2.x |
|------|--------|--------|
| 文本编码器 | CLIP ViT-L/14 | **OpenCLIP ViT-H/14** |
| 文本维度 | 768 | **1024** |
| U-Net 参数量 | ~890M | ~865M |
| 原生分辨率 | 512×512 | **512×512 / 768×768** |
| 训练数据 | LAION-2B-en | LAION-5B 过滤子集 |
| NSFW 过滤 | 较弱 | **增强过滤** |

#### 3.2.2 OpenCLIP 替代 CLIP 的影响

- OpenCLIP 使用 **LAION 数据训练**，与 SD 的训练数据分布更一致
- 文本理解能力显著提升，特别是**艺术风格描述**和**复杂构图指令**
- 负面效应：与 SD 1.x 的 LoRA、Textual Inversion 等社区模型**不兼容**
- 社区生态分裂：SD 1.5 成为微调生态的事实标准，SD 2.x 生态相对薄弱

#### 3.2.3 架构本质

SD 2.x 的 U-Net 结构、VAE、扩散框架与 SD 1.x **基本一致**，无本质架构创新。主要改进在于：
- 更大的文本编码器（ViT-H vs ViT-L）
- 更严格的训练数据过滤
- 更高分辨率版本（768 模型）

---

### 3.3 SDXL (2023)

#### 3.3.1 整体架构：Base + Refiner 两级流水线

SDXL 是 SD 系列首次重大架构升级，引入**两级模型流水线**和**多条件注入机制**：

```
┌─────────────────────────────────────────────────────────────┐
│                      SDXL 1.0 Pipeline                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Text Prompt ──▶ OpenCLIP ViT-bigG (1280d)                  │
│              ──▶ CLIP ViT-L (768d)                           │
│                      │                                       │
│                      ▼                                       │
│              ┌───────────────┐                               │
│              │ Text Embed    │ (77+77, 2048)                 │
│              │ Concatenation │                               │
│              └───────┬───────┘                               │
│                      │                                       │
│                      ▼                                       │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ SDXL Base (3.5B U-Net)                              │    │
│  │  - 输出：1024×1024 潜空间 (128×128×4)                │    │
│  │  - 去噪步数：20-40 步（主要去噪阶段）                │    │
│  │  - Micro-Conditioning：原始尺寸、裁剪参数注入        │    │
│  └────────────────────┬─────────────────────────────────┘    │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ SDXL Refiner (1.3B U-Net)                           │    │
│  │  - 输入：Base 输出潜变量（去噪后期，高噪声水平）     │    │
│  │  - 专门优化细节：纹理、边缘、高频信息                │    │
│  │  - 去噪步数：5-10 步（精细化阶段）                   │    │
│  └────────────────────┬─────────────────────────────────┘    │
│                       │                                      │
│                       ▼                                      │
│                  VAE Decoder                                 │
│                       │                                      │
│                       ▼                                      │
│                 1024×1024 Image                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 3.3.2 SDXL Base：3.5B 参数 U-Net

SDXL Base 的 U-Net 相比 SD 1.x 有显著扩大：

- **参数量**：3.5B（约 4× SD 1.x）
- **下采样阶段**：从 4 阶段增加到 **6 阶段**（128×128 → 64×64 → 32×32 → 16×16 → 8×8 → 4×4）
- **通道数**：最大通道数从 1280 增加到 **2560**
- **注意力机制**：
  - Self-Attention 在 32×32 及以下分辨率插入
  - Cross-Attention 保持每个 block 后插入
  - 引入 **QK-Normalization** 稳定大模型训练
- **输出分辨率**：1024×1024 原生（潜空间 128×128×4）

#### 3.3.3 SDXL Refiner：1.3B 参数专用细化模型

Refiner 是 SDXL 的创新设计，专门处理去噪**后期阶段**（高噪声水平 → 低噪声水平）：

- **参数量**：1.3B，结构类似 SD 1.x U-Net 但更大
- **输入**：Base 模型去噪后期的潜变量（约最后 20% 去噪步数）
- **功能**：专门优化图像细节、纹理质量、边缘锐度
- **可独立使用**：也可用于其他模型输出的图像细化
- **设计动机**：大模型擅长整体结构，小模型擅长局部细节，分工协作

#### 3.3.4 双文本编码器

SDXL 引入**双文本编码器**机制，增强文本理解能力：

| 编码器 | 模型 | 输出维度 | 最大 Token | 作用 |
|--------|------|----------|------------|------|
| 编码器 1 | OpenCLIP ViT-bigG | 1280 | 77 | 主要语义理解 |
| 编码器 2 | CLIP ViT-L | 768 | 77 | 补充细节、风格 |
| 融合 | Concatenation | 2048 | 77 | 拼接后输入 U-Net |

- 两个编码器的输出在通道维度拼接（1280 + 768 = 2048）
- 拼接后的 embedding 通过 Cross-Attention 注入 U-Net
- 相比单编码器，对**复杂描述**、**多主体场景**、**风格修饰词**理解更强

#### 3.3.5 Micro-Conditioning：元数据条件注入

SDXL 引入 **Micro-Conditioning** 机制，将图像元数据作为额外条件注入：

- **原始图像尺寸**：训练时记录原始图像的宽高，作为条件向量注入
- **裁剪参数**：记录中心裁剪的偏移量，避免训练-推理的裁剪分布不一致
- **目标分辨率**：指定生成图像的目标尺寸
- **注入方式**：通过 AdaGN 或独立 MLP 映射为 embedding，与时间步 embedding 拼接

这一设计解决了 SD 1.x/2.x 的**裁剪伪影**问题（如人物头部被截断、重复肢体等）。

#### 3.3.6 SDXL Turbo：实时生成

2023 年 11 月，Stability AI 发布 SDXL Turbo，通过 **Adversarial Diffusion Distillation (ADD)** 实现单步/少步推理：

- **蒸馏目标**：学生网络（SDXL Turbo）在单步内匹配教师网络（SDXL Base）多步去噪结果
- **对抗损失**：引入判别器区分真实图像和生成图像，提升单步质量
- **推理速度**：A100 上约 0.2 秒生成 512×512 图像
- **质量权衡**：相比 50 步 Base，单步质量有所下降，但可用性大幅提升

---

### 3.4 Stable Diffusion 3 (2024)

#### 3.4.1 整体架构：MMDiT — 彻底抛弃 U-Net

SD3 是 Stability AI 的里程碑式更新，**彻底抛弃 U-Net**，全面转向 Transformer 架构：

```
┌─────────────────────────────────────────────────────────────┐
│                 Stable Diffusion 3 (MMDiT)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Text Prompt ──▶ CLIP-L (768d)                               │
│              ──▶ CLIP-G (1280d)                              │
│              ──▶ T5-XXL (4096d)  ──▶ 文本 Token (77, 4096) │
│                      │                                       │
│                      ▼                                       │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              MMDiT (Multimodal DiT)                  │    │
│  │                                                      │    │
│  │   文本流 (Text Tokens)        图像流 (Image Patches) │    │
│  │        │                              │              │    │
│  │        ▼                              ▼              │    │
│  │   ┌─────────┐                   ┌─────────┐          │    │
│  │   │ Text    │                   │ Image   │          │    │
│  │   │ Embed   │                   │ Embed   │          │    │
│  │   │ (4096)  │                   │ (patch) │          │    │
│  │   └────┬────┘                   └────┬────┘          │    │
│  │        │                              │              │    │
│  │        ▼                              ▼              │    │
│  │   ┌─────────────────────────────────────────┐        │    │
│  │   │      MMDiT Block × N (N≈24-48)         │        │    │
│  │   │  ┌─────────┐    ┌─────────┐            │        │    │
│  │   │  │ 文本    │◀──▶│ 图像    │            │        │    │
│  │   │  │ SelfAttn│    │ SelfAttn│            │        │    │
│  │   │  │ + FFN   │    │ + FFN   │            │        │    │
│  │   │  └────┬────┘    └────┬────┘            │        │    │
│  │   │       │              │                  │        │    │
│  │   │       └──────┬───────┘                  │        │    │
│  │   │              ▼                           │        │    │
│  │   │      Joint Attention (QKV 融合)          │        │    │
│  │   │      文本 Q/K/V + 图像 Q/K/V 交互       │        │    │
│  │   │              │                           │        │    │
│  │   │              ▼                           │        │    │
│  │   │      文本输出 ◀──▶ 图像输出             │        │    │
│  │   └─────────────────────────────────────────┘        │    │
│  │                                                      │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  图像输出 ──▶ VAE Decoder ──▶ 1024×1024 Image               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 3.4.2 MMDiT：Multimodal Diffusion Transformer

MMDiT 是 SD3 的核心创新，基于 DiT (Diffusion Transformer) 扩展为多模态版本：

**核心思想**：
- 文本 token 和图像 patch 分别通过独立的 embedding 层映射
- 进入共享的 Transformer block 序列
- 通过**联合注意力（Joint Attention）**实现文本-图像交互
- 两种模态的 Q/K/V 在注意力层融合计算

**MMDiT Block 结构**：

```
输入: 文本特征 x_t (seq_t, dim) + 图像特征 x_i (seq_i, dim)

1. 模态内 Self-Attention:
   - 文本流: x_t → LayerNorm → Self-Attention → Residual
   - 图像流: x_i → LayerNorm → Self-Attention → Residual

2. Joint Cross-Modal Attention:
   - 拼接 [x_t; x_i] → LayerNorm
   - 计算联合 QKV: Q = [Q_t; Q_i], K = [K_t; K_i], V = [V_t; V_i]
   - Attention(Q, K, V) = softmax(QK^T/√d) V
   - 分离输出: 文本部分 + 图像部分
   - 分别残差连接

3. FFN (Feed-Forward Network):
   - 文本流: x_t → LayerNorm → MLP → Residual
   - 图像流: x_i → LayerNorm → MLP → Residual

4. 时间步/条件注入:
   - AdaLN-Zero: 时间步 embedding 通过 MLP 生成 γ, β, α
   - γ, β 注入 LayerNorm; α 作为残差缩放
```

**与 DiT 的区别**：
- DiT (Peebles & Xie, 2023) 仅处理图像 patch，文本条件通过 AdaLN 注入
- MMDiT 同时处理文本 token 和图像 patch，通过注意力层深度交互
- 文本不再只是"外部条件"，而是与图像平等的"内部模态"

#### 3.4.3 三文本编码器

SD3 引入**三文本编码器**机制，是开源模型中文本理解能力最强者之一：

| 编码器 | 模型 | 输出维度 | 最大 Token | 作用 |
|--------|------|----------|------------|------|
| 编码器 1 | CLIP ViT-L | 768 | 77 | 基础语义、视觉对齐 |
| 编码器 2 | OpenCLIP ViT-bigG | 1280 | 77 | 增强语义、风格理解 |
| 编码器 3 | T5-XXL | 4096 | 77 | 深层语言理解、复杂推理 |
| 融合 | 投影 + 拼接 | 4096 | 77 | T5 主导，CLIP 辅助 |

- T5-XXL (11B 参数) 提供强大的**语言理解能力**，对复杂句法、逻辑关系、细节描述理解深刻
- CLIP-L + CLIP-G 提供**视觉-语言对齐**，确保生成内容与文本语义一致
- 实际推理时，T5-XXL 可省略（CLIP-only 模式），但质量下降

#### 3.4.4 Flow Matching 框架

SD3 从 DDPM/LDM 框架迁移到 **Flow Matching**，这是生成模型领域的重要范式转变：

**DDPM/LDM 回顾**：
- 定义前向过程：x_t = √(α_t) x_0 + √(1-α_t) ε
- 训练目标：预测噪声 ε_θ(x_t, t, c)
- 采样：迭代去噪，步数 20-50

**Flow Matching 核心**：
- 定义概率流 ODE：dx_t/dt = v_θ(x_t, t, c)
- 训练目标：回归向量场 v_θ，使其匹配真实流
- 采样：ODE 求解器（Euler、Heun、DPM-Solver++）直接积分
- 优势：
  - 更稳定的训练（无需噪声调度设计）
  - 更少的采样步数（10-20 步即可高质量）
  - 与 Rectified Flow、Consistency Model 等理论统一

**SD3 的具体实现**：
- 使用 **Rectified Flow** 变体
- 时间步 t ∈ [0, 1]，t=0 为噪声，t=1 为数据
- 训练时采样 t ~ Uniform(0, 1)，计算 x_t = t·x_1 + (1-t)·x_0
- 目标：v_θ(x_t, t, c) ≈ x_1 - x_0

#### 3.4.5 多规格模型

SD3 提供三种参数规模：

| 模型 | 参数量 | MMDiT 层数 | 注意力头数 | 适用场景 |
|------|--------|------------|------------|----------|
| SD3 Small | 2B | 24 | 16 | 消费级 GPU，快速推理 |
| SD3 Medium | 4B | 36 | 24 | 平衡质量与速度 |
| SD3 Large | 8B | 48 | 32 | 最高质量，专业创作 |

#### 3.4.6 VAE 改进

SD3 使用改进的 VAE：
- 16 通道潜空间（vs SD 1.x 的 4 通道）
- 更好的细节保留和重建质量
- 与 SD 1.x/SDXL 的 VAE **不兼容**

---

### 3.5 FLUX (2024, Black Forest Labs)

#### 3.5.1 背景：Black Forest Labs 的成立

2024 年，原 Stability AI 核心研究团队出走，成立 **Black Forest Labs (BFL)**：

- **创始人**：Robin Rombach（LDM/MMDiT 一作）、Andreas Blattmann、Dominik Lorenz、Patrick Esser 等
- **定位**：延续 Stability AI 的开源精神，但独立运营
- **融资**：A 轮 3100 万美元，Andreessen Horowitz (a16z) 领投
- **使命**：推动开源多模态生成模型（图像 + 视频）

#### 3.5.2 整体架构：Flow Matching + Transformer

FLUX 是 BFL 的首个模型系列，架构上延续并超越了 SD3 的 MMDiT：

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUX.1 Architecture                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Text Prompt ──▶ CLIP-L (768d)                               │
│              ──▶ T5-XXL (4096d)  ──▶ 文本 Token (512, 4096) │
│                      │                                       │
│                      ▼                                       │
│  ┌──────────────────────────────────────────────────────┐    │
│  │           FLUX Transformer (12B, 约 50 层)            │    │
│  │                                                      │    │
│  │   文本流 + 图像流 ──▶ 统一 Transformer Block          │    │
│  │                                                      │    │
│  │   ┌─────────────────────────────────────────────┐    │    │
│  │   │         FLUX Block × 50                      │    │    │
│  │   │                                              │    │    │
│  │   │   输入: 拼接 [文本 tokens; 图像 patches]     │    │    │
│  │   │                                              │    │    │
│  │   │   1. LayerNorm + AdaLN (时间步/条件注入)     │    │    │
│  │   │                                              │    │    │
│  │   │   2. 统一 Self-Attention                     │    │    │
│  │   │      - 文本和图像在同一个序列中                │    │    │
│  │   │      - 无显式 Cross-Attention                │    │    │
│  │   │      - 通过位置编码区分模态                  │    │    │
│  │   │                                              │    │    │
│  │   │   3. FFN (SwiGLU, 大扩展比)                  │    │    │
│  │   │                                              │    │    │
│  │   │   4. 输出: 统一序列 [文本; 图像]             │    │    │
│  │   │                                              │    │    │
│  │   └─────────────────────────────────────────────┘    │    │
│  │                                                      │    │
│  │   关键设计: 文本和图像完全统一处理，无模态边界       │    │
│  │                                                      │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  图像部分 ──▶ VAE Decoder ──▶ 1024×1024 / 2048×2048 Image   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 3.5.3 核心架构特点

**统一序列处理（Unified Sequence）**：
- FLUX 将文本 token 和图像 patch **拼接为单一序列**
- 通过**模态特定的位置编码**区分文本和图像
- 无显式的模态间 Cross-Attention，所有交互通过 Self-Attention 自然发生
- 相比 MMDiT 的"双流"设计，FLUX 的"单流"设计更简洁、交互更深度

**12B 参数规模**：
- 约 **12B 参数**，是开源图像生成模型中最大之一
- 约 50 层 Transformer block
- 隐藏维度大，FFN 扩展比高（SwiGLU 激活）
- 训练数据量巨大（未公开具体规模，估计数十亿图文对）

**文本编码器**：
- CLIP-L + T5-XXL（与 SD3 类似，但 T5 序列长度扩展到 **512 token**）
- 长文本理解能力显著增强，可处理复杂段落描述

**Flow Matching + 改进采样**：
- 基于 Flow Matching，但使用更先进的 ODE 求解器
- 支持 **Guided Distillation**：在训练时引入 CFG（Classifier-Free Guidance）信号
- 推理时可用少量步数（4-20 步）获得高质量结果

#### 3.5.4 三个版本

| 版本 | 参数量 | 开源 | 许可证 | 定位 | 典型步数 |
|------|--------|------|--------|------|----------|
| FLUX.1 [pro] | 12B | 否 | API 商用 | 最高质量，API 服务 | 20-50 |
| FLUX.1 [dev] | 12B | **是** | Apache 2.0 | 开源可商用，质量接近 pro | 20-50 |
| FLUX.1 [schnell] | 12B | **是** | Apache 2.0 | 本地极速，1-4 步 | 1-4 |

- **[pro]**：仅通过 API/BFL 平台提供，质量最高
- **[dev]**：开源可下载，社区生态核心，**Apache 2.0 许可证**允许自由商用
- **[schnell]**：蒸馏版本，1-4 步即可生成可用图像，本地运行友好

#### 3.5.5 文本渲染能力

FLUX 的文本渲染能力是**行业最强**（截至 2024 年底）：

- 可生成**清晰可读**的英文、数字、符号
- 支持**指定文本内容**（如招牌、书籍封面、UI 元素）
- 对**复杂排版**、**多行文本**、**混合字体**有良好支持
- 原理：
  - T5-XXL 的强语言理解能力
  - 长序列（512 token）支持详细文本描述
  - 大规模训练数据中包含大量带文本的图像
  - 统一序列设计使文本和图像特征深度融合

#### 3.5.6 FLUX.1 Tools (2024.10)

BFL 发布基于 FLUX 的图像编辑工具套件：

| 工具 | 功能 | 技术要点 |
|------|------|----------|
| **FLUX Fill** | 图像修复/外扩 | Inpainting/Outpainting，保持风格一致 |
| **FLUX Canny** | Canny 边缘控制 | 结构保持的图像生成/编辑 |
| **FLUX Depth** | 深度图控制 | 3D 结构保持的生成 |
| **FLUX Redux** | 图像变体/重绘 | 保持内容，改变风格/构图 |

这些工具展示了 FLUX 架构的**可控性**和**扩展性**。

---

### 3.6 SD3.5 / 后续迭代 (2025)

#### 3.6.1 SD3.5 的发布

2025 年初，Stability AI 发布 **SD3.5**，作为 SD3 的改进版本：

- **架构**：MMDiT 改进版，细节优化
- **规格**：2B / 4B / 8B 多规格延续
- **改进点**：
  - 更好的**人体解剖**准确性
  - 改进的**手部生成**
  - 更强的**风格一致性**
  - 优化的**推理效率**

#### 3.6.2 社区生态适配

SD3.5 面临的主要挑战是**社区生态**：

- SD3 的许可证争议（早期限制商用）导致社区信任受损
- FLUX [dev] 的 Apache 2.0 许可证更具吸引力
- SD3.5 需要重建 LoRA、ControlNet 等插件生态
- ComfyUI、Stable Diffusion WebUI 等工具已支持 SD3.5

#### 3.6.3 Stability AI 与 BFL 的竞争格局

| 维度 | Stability AI | Black Forest Labs |
|------|-------------|-------------------|
| 核心团队 | 新团队 | 原 SD 核心团队 |
| 最新架构 | MMDiT (SD3.5) | Flow Matching Transformer (FLUX) |
| 开源策略 | 部分开源，许可证复杂 | 完全开源，Apache 2.0 |
| 社区生态 | 历史积累深厚，但信任受损 | 新兴，快速增长 |
| 商业模式 | API + 企业授权 | API + 开源 |
| 技术路线 | 延续 MMDiT | 统一序列 Transformer |
| 视频生成 | Stable Video Diffusion | FLUX 视频扩展（预告） |

---

## 4. 架构演进对比

### 4.1 骨干网络演进

| 模型 | 骨干网络 | 参数量 | 核心设计 | 模态交互方式 |
|------|----------|--------|----------|--------------|
| SD 1.x | U-Net | 890M | ResNet + Self-Attn + Cross-Attn | Cross-Attention (Q/K text, V image) |
| SD 2.x | U-Net | 865M | 同 SD 1.x，更大 | 同 SD 1.x |
| SDXL | U-Net (Base+Refiner) | 3.5B+1.3B | 6 阶段下采样，双编码器 | Cross-Attention + Micro-Conditioning |
| SD3 | MMDiT | 2B/4B/8B | 双流 Transformer，Joint Attention | Joint Self-Attention (文本+图像 QKV 融合) |
| FLUX | Flow Matching Transformer | 12B | 统一序列 Transformer | 统一 Self-Attention (单流，无显式模态边界) |

### 4.2 条件注入机制演进

| 模型 | 时间步注入 | 文本条件注入 | 其他条件 | 机制总结 |
|------|------------|--------------|----------|----------|
| SD 1.x | AdaGN (正弦编码) | Cross-Attention | 无 | 时间步调制归一化，文本通过注意力注入 |
| SD 2.x | AdaGN (正弦编码) | Cross-Attention | 无 | 同 SD 1.x |
| SDXL | AdaGN + 独立 MLP | Cross-Attention (双编码器) | Micro-Conditioning (尺寸、裁剪) | 多条件并行注入 |
| SD3 | AdaLN-Zero | Joint Attention (三编码器) | 无 | 时间步通过 AdaLN，文本通过联合注意力 |
| FLUX | AdaLN | 统一 Self-Attention (双编码器) | 无 | 时间步通过 AdaLN，文本作为序列一部分 |

### 4.3 文本编码器演进

| 模型 | 编码器 1 | 编码器 2 | 编码器 3 | 总维度 | 最大 Token |
|------|----------|----------|----------|--------|------------|
| SD 1.x | CLIP ViT-L (768d) | 无 | 无 | 768 | 77 |
| SD 2.x | OpenCLIP ViT-H (1024d) | 无 | 无 | 1024 | 77 |
| SDXL | OpenCLIP ViT-bigG (1280d) | CLIP ViT-L (768d) | 无 | 2048 | 77 |
| SD3 | CLIP ViT-L (768d) | OpenCLIP ViT-bigG (1280d) | T5-XXL (4096d) | 4096 | 77 |
| FLUX | CLIP ViT-L (768d) | T5-XXL (4096d) | 无 | 4096 | **512** |

### 4.4 生成框架演进

| 模型 | 框架 | 前向过程 | 训练目标 | 采样方式 | 典型步数 |
|------|------|----------|----------|----------|----------|
| SD 1.x | DDPM + LDM | x_t = √α_t x_0 + √(1-α_t) ε | 预测噪声 ε_θ | DDIM/PLMS | 20-50 |
| SD 2.x | DDPM + LDM | 同 SD 1.x | 预测噪声 ε_θ | DDIM/DPM++ | 20-50 |
| SDXL | DDPM + LDM | 同 SD 1.x | 预测噪声 ε_θ | DPM++ 2M/Euler | 20-40 |
| SD3 | **Flow Matching** | dx_t/dt = v_θ(x_t, t) | 回归向量场 v_θ | ODE 求解器 | 10-20 |
| FLUX | **Flow Matching** | 同 SD3 | 回归向量场 v_θ | 改进 ODE 求解器 | 4-20 |

### 4.5 VAE 演进

| 模型 | 潜空间通道 | 下采样因子 | 输入分辨率 | 重建质量 | 兼容性 |
|------|------------|------------|------------|----------|--------|
| SD 1.x | 4 | 8 | 512×512 | 中等 | 与 SD 2.x 兼容 |
| SD 2.x | 4 | 8 | 512/768 | 中等 | 与 SD 1.x 兼容 |
| SDXL | 4 | 8 | 1024×1024 | 较好 | 独立 |
| SD3 | **16** | 8 | 1024×1024 | 好 | 独立 |
| FLUX | 16 | 8 | 1024/2048 | 好 | 独立 |

---

## 5. 开源生态与工具链

### 5.1 推理框架

| 工具 | 支持模型 | 特点 | 社区活跃度 |
|------|----------|------|------------|
| **ComfyUI** | SD 1.x/2.x, SDXL, SD3, FLUX | 节点式工作流，最灵活 | 极高 |
| **Stable Diffusion WebUI (A1111)** | SD 1.x/2.x, SDXL, SD3, FLUX | 插件丰富，易用 | 高 |
| **Forge** | SD 1.x/2.x, SDXL | A1111 分支，性能优化 | 中 |
| **Fooocus** | SDXL, FLUX | 极简界面，一键生成 | 中 |
| **InvokeAI** | SD 1.x/2.x, SDXL, SD3, FLUX | 专业创作工具 | 中 |
| **Diffusers (Hugging Face)** | 全系列 | Python 库，开发友好 | 高 |

### 5.2 微调与适配技术

| 技术 | 原理 | 适用模型 | 参数量 | 效果 |
|------|------|----------|--------|------|
| **LoRA** | 低秩适配，冻结主模型，训练低秩矩阵 | SD 1.x/2.x, SDXL, SD3, FLUX | 4-100M | 风格/角色/概念定制 |
| **DreamBooth** | 稀有 token + 类别先验保持 | SD 1.x/2.x, SDXL | 全参数或 LoRA | 新主体学习 |
| **Textual Inversion** | 优化新 token 的 embedding | SD 1.x/2.x, SDXL | ~10K | 新概念嵌入 |
| **ControlNet** | 可训练副本 + 零卷积，条件控制 | SD 1.x/2.x, SDXL, SD3, FLUX | ~400M | 姿态/深度/边缘控制 |
| **IP-Adapter** | 解耦的图像特征交叉注意力 | SD 1.x/2.x, SDXL, SD3, FLUX | ~100M | 图像风格/内容参考 |
| **T2I-Adapter** | 轻量级适配器，空间条件控制 | SD 1.x/2.x, SDXL | ~70M | 草图/语义分割控制 |
| **InstantID** | 基于 IP-Adapter 的人脸保持 | SDXL | ~100M | 单图人脸身份保持 |

### 5.3 社区生态现状（2025）

**SD 1.5 生态**：
- 最成熟的微调生态，Civitai 上数十万 LoRA/Checkpoint
- ControlNet 模型最丰富（OpenPose, Canny, Depth, Scribble 等）
- 插件和工具链最完善

**SDXL 生态**：
- 官方和社区 LoRA 丰富
- ControlNet 支持完善
- 成为 1024×1024 生成的标准

**SD3 生态**：
- 早期许可证问题导致社区犹豫
- LoRA 和 ControlNet 支持逐步完善
- 生态规模小于 SD 1.5 和 SDXL

**FLUX 生态**：
- 快速增长，Apache 2.0 许可证吸引开发者
- LoRA、ControlNet、IP-Adapter 适配迅速
- ComfyUI 工作流丰富
- 成为 2024-2025 年开源社区的新焦点

---

## 6. 与竞品对比

### 6.1 开源 vs 闭源图像生成模型

| 维度 | FLUX [dev] | SD3.5 | Midjourney v6 | DALL-E 3 | Ideogram | Imagen 3 |
|------|------------|-------|---------------|----------|----------|----------|
| **开源** | ✅ Apache 2.0 | ✅ 部分 | ❌ | ❌ | ❌ | ❌ |
| **可本地部署** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **参数量** | 12B | 8B | 未知 | 未知 | 未知 | 未知 |
| **文本渲染** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **图像质量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **语义理解** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **人体/手部** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **推理成本** | 高 | 中 | API | API | API | API |
| **社区生态** | 快速增长 | 中等 | 无 | 无 | 无 | 无 |
| **可控性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |

### 6.2 架构范式对比

| 模型 | 骨干网络 | 生成框架 | 文本编码 | 核心优势 |
|------|----------|----------|----------|----------|
| **FLUX** | Flow Matching Transformer | Flow Matching | T5-XXL + CLIP | 开源最强，文本渲染，可控性 |
| **SD3.5** | MMDiT | Flow Matching | T5-XXL + CLIP×2 | 开源，多规格 |
| **Midjourney v6** | 未知（推测 U-Net/Transformer 混合） | 未知 | 未知 | 美学质量，用户体验 |
| **DALL-E 3** | 未知（推测 Diffusion Transformer） | 未知 | GPT-4 级文本理解 | 语义理解，与 ChatGPT 集成 |
| **Imagen 3** | 未知 | 未知 | T5-XXL 级 | 细节质量，Google 生态 |

### 6.3 关键差异分析

**开源 vs 闭源**：
- 开源模型（FLUX、SD3.5）优势：可控性（ControlNet、LoRA）、本地部署、隐私、定制性
- 闭源模型（Midjourney、DALL-E 3）优势：开箱即用质量、用户体验、无需硬件投资

**文本渲染**：
- FLUX 和 Ideogram 是文本渲染最强的模型
- 这得益于 T5-XXL 级文本编码器和大量带文本的训练数据

**人体生成**：
- Midjourney v6 和 DALL-E 3 在人体解剖准确性上仍领先
- 开源模型通过社区 LoRA 和专用训练数据逐步追赶

---

## 7. 挑战与未来方向

### 7.1 当前挑战

**计算成本**：
- FLUX 12B 参数需要 24GB+ VRAM（FP16），消费级 GPU 压力大
- 量化技术（INT8/INT4/FP8）和蒸馏是降低门槛的关键
- schnell 版本 1-4 步生成是重要进步，但质量仍有妥协

**训练数据与版权**：
- 大规模图像数据集（LAION 等）的版权争议持续
- 艺术家抗议和诉讼影响开源模型声誉
- 合成数据训练、授权数据采购是可能方向

**安全性与滥用**：
- 开源模型难以限制 NSFW、深度伪造等滥用
- 水印技术（如 Stable Signature）是缓解方案
- 平衡开放与安全是持续挑战

**人体与细节生成**：
- 手部、面部、复杂人体姿态仍是难点
- 需要更好的训练数据和架构改进

### 7.2 未来方向

**视频生成扩展**：
- BFL 已预告 FLUX 视频扩展（2025）
- Stability AI 的 Stable Video Diffusion 是现有基础
- 3D 一致性、时序连贯性是视频生成的核心挑战

**更高效架构**：
- 混合专家（MoE）降低推理成本
- 线性注意力、状态空间模型（Mamba）替代标准 Transformer
- 一步/零步生成（Consistency Model、GAN 回归）

**多模态统一**：
- 图像 + 视频 + 音频 + 3D 的统一生成模型
- 与 LLM 的深度集成（如 GPT-4o 的原生多模态）

**个性化与交互**：
- 实时交互式生成（用户边画边生成）
- 更强的概念组合和逻辑推理能力
- 长上下文理解（生成系列图像、故事板）

**开源生态演进**：
- FLUX 的 Apache 2.0 模式可能成为开源生成模型的新标准
- 社区驱动的模型改进（如 LLM 领域的 Llama 生态）
- 去中心化训练和模型共享

---

## 8. 参考链接

### 8.1 论文与技术报告

| 模型 | 论文/报告 | 链接 |
|------|-----------|------|
| LDM (SD 基础) | *High-Resolution Image Synthesis with Latent Diffusion Models* (CVPR 2022) | https://arxiv.org/abs/2112.10752 |
| SD 2.x | Stability AI Blog | https://stability.ai/blog/stable-diffusion-v2-release |
| SDXL | *SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis* | https://arxiv.org/abs/2307.01952 |
| SDXL Turbo | *Adversarial Diffusion Distillation* | https://arxiv.org/abs/2311.17042 |
| DiT | *Scalable Diffusion Models with Transformers* (ICCV 2023) | https://arxiv.org/abs/2212.09748 |
| SD3 | *Scaling Rectified Flow Transformers for High-Resolution Image Synthesis* | https://arxiv.org/abs/2403.03206 |
| Flow Matching | *Flow Matching for Generative Modeling* (ICLR 2023) | https://arxiv.org/abs/2210.02747 |
| Rectified Flow | *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow* | https://arxiv.org/abs/2209.03003 |
| FLUX | Black Forest Labs Blog | https://blackforestlabs.ai/ |
| FLUX.1 [dev] | Hugging Face Model Card | https://huggingface.co/black-forest-labs/FLUX.1-dev |
| FLUX.1 [schnell] | Hugging Face Model Card | https://huggingface.co/black-forest-labs/FLUX.1-schnell |
| FLUX.1 Tools | BFL Tools Announcement | https://blackforestlabs.ai/flux-1-tools/ |
| T5 | *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer* | https://arxiv.org/abs/1910.10683 |
| CLIP | *Learning Transferable Visual Models From Natural Language Supervision* | https://arxiv.org/abs/2103.00020 |
| LoRA | *LoRA: Low-Rank Adaptation of Large Language Models* (ICLR 2022) | https://arxiv.org/abs/2106.09685 |
| ControlNet | *Adding Conditional Control to Text-to-Image Diffusion Models* (ICCV 2023) | https://arxiv.org/abs/2302.05543 |
| IP-Adapter | *IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models* | https://arxiv.org/abs/2308.06721 |

### 8.2 官方资源

| 资源 | 链接 |
|------|------|
| Stability AI 官网 | https://stability.ai/ |
| Stability AI GitHub | https://github.com/Stability-AI |
| Black Forest Labs 官网 | https://blackforestlabs.ai/ |
| BFL GitHub | https://github.com/black-forest-labs |
| Hugging Face - Stability AI | https://huggingface.co/stabilityai |
| Hugging Face - BFL | https://huggingface.co/black-forest-labs |
| ComfyUI | https://github.com/comfyanonymous/ComfyUI |
| Stable Diffusion WebUI | https://github.com/AUTOMATIC1111/stable-diffusion-webui |
| Diffusers | https://github.com/huggingface/diffusers |
| Civitai (社区模型) | https://civitai.com/ |

### 8.3 技术博客与解读

| 文章 | 链接 |
|------|------|
| Lilian Weng - Diffusion Models | https://lilianweng.github.io/posts/2021-07-11-diffusion-models/ |
| Papers with Code - Diffusion | https://paperswithcode.com/task/image-generation |
| AssemblyAI - Stable Diffusion 3 | https://www.assemblyai.com/blog/stable-diffusion-3/ |
| Replicate - FLUX Guide | https://replicate.com/blog/flux-state-of-the-art-image-generation |
| Reddit r/StableDiffusion | https://www.reddit.com/r/StableDiffusion/ |

---

## 附录：术语表

| 术语 | 英文 | 解释 |
|------|------|------|
| LDM | Latent Diffusion Model | 潜空间扩散模型，将扩散过程在压缩潜空间执行 |
| VAE | Variational Autoencoder | 变分自编码器，用于图像压缩和重建 |
| U-Net | U-Shaped Network | 编码器-解码器结构，带跳跃连接，用于去噪 |
| DiT | Diffusion Transformer | 基于 Transformer 的扩散模型骨干 |
| MMDiT | Multimodal Diffusion Transformer | 多模态扩散 Transformer，SD3 核心架构 |
| Flow Matching | Flow Matching | 通过回归向量场学习概率流的生成框架 |
| AdaGN | Adaptive Group Normalization | 自适应组归一化，条件注入机制 |
| AdaLN | Adaptive Layer Normalization | 自适应层归一化，Transformer 中的条件注入 |
| Cross-Attention | Cross-Attention | 交叉注意力，Q 来自一个模态，K/V 来自另一个模态 |
| Self-Attention | Self-Attention | 自注意力，Q/K/V 来自同一序列 |
| CFG | Classifier-Free Guidance | 无分类器引导，通过条件/无条件预测差值控制生成 |
| LoRA | Low-Rank Adaptation | 低秩适配，高效微调大模型的方法 |
| ControlNet | ControlNet | 通过可训练副本实现条件控制的插件架构 |
| IP-Adapter | Image Prompt Adapter | 图像提示适配器，通过解耦注意力实现图像条件 |
| ODE | Ordinary Differential Equation | 常微分方程，Flow Matching 中的采样过程 |
| NSFW | Not Safe For Work | 不适宜工作场所的内容，通常指成人内容 |

---

> **报告声明**：本报告基于公开论文、技术博客和官方文档整理，仅供学术研究和技术参考。模型性能评价基于公开基准和社区反馈，可能存在主观性。报告日期为 2026 年 6 月 6 日，后续模型更新请以官方发布为准。

---

*报告完成日期：2026-06-06*
