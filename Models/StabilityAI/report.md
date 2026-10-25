---
display_name: StabilityAI
---

# Stability AI / Black Forest Labs 图像生成模型系列研究报告

> **覆盖范围**：Stable Diffusion 系列、FLUX 的公开论文、权重与源码，以及仍未公开的模型实现边界。
> 研究范围：Stable Diffusion 1.x → SDXL → SD3 → FLUX → SD3.5 全系列架构演进
> 核心主线：U-Net → DiT → MMDiT → Flow Matching Transformer，并补充 BFL 的跨模态 Self-Flow 训练机制

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
   - 3.6 SD3.5 / 后续迭代 (2024)
   - 3.7 Self-Flow (2026)：流匹配中的自监督表征学习
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
| 2022.08 | **Stable Diffusion 1.4** | LDM (VAE + U-Net + CLIP) | ~860M (U-Net) [论文表 1] | 开源文生图里程碑，消费级 GPU 可运行 |
| 2022.10 | **Stable Diffusion 1.5** | LDM (同上) | ~860M | 社区微调基础模型 |
| 2022.11 | **Stable Diffusion 2.0** | LDM (OpenCLIP) | ~865M | 重新训练，OpenCLIP ViT-H 替代 CLIP |
| 2022.12 | **Stable Diffusion 2.1** | LDM (OpenCLIP) | ~865M | 输出分辨率 768x768 |
| 2023.07 | **SDXL 1.0** | Base + Refiner 两级 U-Net | Base U-Net 2.6B；其余组件另计 | 1024x1024 原生分辨率，双文本编码器 |
| 2023.11 | **SDXL Turbo** | SDXL + Adversarial Distillation | Base U-Net 2.6B | 单步/少步推理，实时生成 |
| 2024.06 | **Stable Diffusion 3 Medium** | MMDiT | 2B | 公开权重发布；区别于论文研究规模 |
| 2024.08 | **FLUX.1 [pro]** | Flow Matching Transformer | 12B | BFL 成立，最强文本渲染 |
| 2024.08 | **FLUX.1 [dev]** | 双流 + 单流 rectified-flow Transformer | 12B | 开放权重；模型为 Non-Commercial License，见 §3.5.4 |
| 2024.08 | **FLUX.1 [schnell]** | Flow Matching Transformer | 12B | 本地极速版，1-4 步 |
| 2024.10 | **FLUX.1.1 [pro]** | Flow Matching Transformer | 12B | 质量与速度双提升 |
| 2024.11 | **FLUX.1 Tools** | 基于 FLUX 的编辑套件 | 12B | Fill、Canny、Depth、Redux |
| 2024.10 | **SD3.5** | MMDiT / MMDiT-X | Large / Turbo 8.1B；Medium 2.5B | 官方发布见 §3.6 |
| 2025.11 / 2026.03 | **FLUX.2 表征分析 / Self-Flow** | FLUX.2 表征比较研究；基于 FLUX 架构的多模态自监督流匹配 | 论文实验模型约 625M（另有 4B 定性样例） | Self-Flow 是训练方法研究，不等于 FLUX.2 产品结构或 FLUX 视频产品披露；详见 §3.7 |

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
│  │                    U-Net (860M)                       │   │
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

U-Net 是 SD 1.x 的去噪骨干网络，参数量约 **860M**（SDXL 论文表 1 的 SD1.4/1.5 口径），结构特点：

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
| U-Net 参数量 | ~860M | ~865M |
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

SDXL 的扩容并非增加到“6 个下采样阶段”。[论文表 1 与 §2.1](https://arxiv.org/abs/2307.01952) 给出 **U-Net 2.6B** 参数（文本编码器另计 817M），channel multiplier 为 `[1,2,4]`，Transformer blocks 分布为 `[0,2,10]`；去掉旧 U-Net 最低的一个分辨率层，把更多 Transformer 计算放到较低分辨率特征上。

[官方 Base 配置](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/unet/config.json) 的 `block_out_channels=[320,640,1280]`、三个 down blocks 与该解释相符。该配置不支持“3.5B U-Net、6 阶段、最大通道 2560、QK-Norm”的说法；3.5B级整体打包规模不能改称为 U-Net 参数量。3.5B 级的整体打包口径不能被改称为 U-Net 参数量。

两个文本编码器是 CLIP ViT-L 与 OpenCLIP ViT-bigG，将倒数第二层特征沿**通道维**拼接，得到 `(77,2048)` 而非 `(77+77,2048)`。此外还输入 pooled text embedding；原图尺寸、裁剪位置、目标尺寸作为 micro-conditioning。尺寸条件是在训练/生成接口中缓解分布不匹配的设计，不是人体重复等所有瑕疵的充分解法。[论文 §2.1–2.3、表 1]

Refiner 是可选的低噪声细化阶段。论文 §2.5 描述在 Base 潜空间输出上进行 SDEdit 式加噪/去噪，并专门训练低噪声区间；实现流水线的步数切分依推理方案而定。不能把后期去噪写为“高噪声阶段”，也不能不经兼容性检查就宣称可用于任意其他模型。

**实验与边界**：论文 §2.5、图 1 的四选一用户研究中，SDXL+refiner、SDXL base、SD1.5、SD2.1 分别获得 48.44%、36.93%、7.91%、6.71% 的偏好选择份额。这不是两两对战胜率。作者同时指出 FID / CLIP score 没有反映同样的改善（附录 F），因此不能用单一指标替代人评结论。§3 列出两模型显存/速度成本、文字生成与增大的推理开销等未解决问题。

SDXL Turbo 的 ADD 蒸馏见 [原论文](https://arxiv.org/abs/2311.17042)；其具体速度需附硬件、尺寸与步数。具体速度必须带硬件、尺寸与步数条件；没有这些条件的延迟数字不能作为该论文的性能结果。

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
- 采样：使用与对应 flow 参数化兼容的 ODE 求解器，不能直接照搬其他噪声参数化的采样器
- 优势：
  - 训练仍需选择时间步分布、路径与损失加权；flow matching 不等于无需调度设计
  - 更少的采样步数（10-20 步即可高质量）
  - 与 Rectified Flow、Consistency Model 等理论统一

**SD3 的具体实现**：
- 使用 **Rectified Flow** 变体
- 时间步 t ∈ [0, 1]，t=0 为噪声，t=1 为数据
- 线性路径可写为 x_t = t·x_1 + (1-t)·x_0；该式不规定训练时间步必须均匀采样，具体分布需回查论文 recipe
- 目标：v_θ(x_t, t, c) ≈ x_1 - x_0

#### 3.4.5 论文规模与发布规格

[Stable Diffusion 3 Medium 官方发布页](https://stability.ai/news-updates/stable-diffusion-3-medium) 明确对应 **2B** 模型。将 Small/Medium/Large 排为 2B/4B/8B 并附带层数、头数，混淆了论文研究规模与正式发布名称；不同权重和服务的参数应分别查模型卡，不能据论文 scaling 实验补出产品矩阵。不同权重和服务的参数应分别查模型卡，不能据论文的 scaling 实验补出产品矩阵。

#### 3.4.6 VAE 改进

SD3 使用改进的 VAE：
- 16 通道潜空间（vs SD 1.x 的 4 通道）
- 更好的细节保留和重建质量
- 与 SD 1.x/SDXL 的 VAE **不兼容**

---

### 3.5 FLUX (2024, Black Forest Labs)

#### 3.5.1 背景：Black Forest Labs 的成立

2024 年，原 Stability AI 核心研究团队出走，成立 **Black Forest Labs (BFL)**：

- **创始人**：Robin Rombach、Andreas Blattmann、Patrick Esser 等；具体论文作者角色应分别核对，不能把 LDM 与 MMDiT 一作合并
- **定位**：延续 Stability AI 的开源精神，但独立运营
- **融资**：种子轮 3100 万美元（[官方成立公告](https://bfl.ai/blog/24-08-01-bfl)），Andreessen Horowitz (a16z) 领投
- **使命**：推动开源多模态生成模型（图像 + 视频）

#### 3.5.2 整体架构：双流与单流混合

FLUX.1 并非全程“无模态边界的单流 Transformer”。[BFL 发布说明](https://bfl.ai/blog/24-08-01-bfl) 明确描述为 multimodal 与 parallel diffusion Transformer blocks 的混合结构；[官方实现 `Flux.forward`](https://github.com/black-forest-labs/flux/blob/802fb4713906133fcbd0d8dc5351620ca4773036/src/flux/model.py#L99) 先循环 `double_blocks` 更新图像与文本，再拼接序列送入 `single_blocks`，最终截取图像部分输出。

```text
图像 / 文本各自投影
  → DoubleStreamBlock：保留各自表示并进行联合注意力
  → 拼接文本与图像序列
  → SingleStreamBlock
  → 截取图像部分 → 输出层 → 后续潜变量解码
```

#### 3.5.3 可直接核对的配置

[固定提交的 `util.py`](https://github.com/black-forest-labs/flux/blob/802fb4713906133fcbd0d8dc5351620ca4773036/src/flux/util.py) 中 `flux-dev` / `flux-schnell` 的配置为 `depth=19`、`depth_single_blocks=38`、hidden size 3072、24 heads；因此不能把它简写为“约 50 层、全单流”。配置是当前固定代码快照的证据，未等同于训练历史审计。

FLUX.1-dev [模型卡](https://huggingface.co/black-forest-labs/FLUX.1-dev) 标示 12B rectified-flow Transformer，使用 guidance distillation；schnell 是另一个少步分支。论文/模型卡未给出可复查训练数据总量时，不估计“数十亿图文对”作为事实。文本到图像质量还受到提示词、步数、guidance 与分辨率影响，不能仅由“统一序列更简洁”推导更好性能。

#### 3.5.4 三个版本

| 版本 | 参数量 | 开源 | 许可证 | 定位 | 典型步数 |
|------|--------|------|--------|------|----------|
| FLUX.1 [pro] | 12B | 否 | API 商用 | 最高质量，API 服务 | 20-50 |
| FLUX.1 [dev] | 12B | 开放权重 | FLUX.1 [dev] Non-Commercial License | guidance-distilled；模型商用另查授权 | 依配置 |
| FLUX.1 [schnell] | 12B | **是** | Apache 2.0 | 本地极速，1-4 步 | 1-4 |

- **[pro]**：仅通过 API/BFL 平台提供，质量最高
- **[dev]**：可下载权重，但模型受 [FLUX.1 [dev] Non-Commercial License](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md) 约束；模型使用授权与生成输出的条款分开，不得用 schnell 的 Apache 2.0 推广到 dev
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

#### 3.5.6 FLUX.1 Tools (2024.11)

BFL 发布基于 FLUX 的图像编辑工具套件：

| 工具 | 功能 | 技术要点 |
|------|------|----------|
| **FLUX Fill** | 图像修复/外扩 | Inpainting/Outpainting，保持风格一致 |
| **FLUX Canny** | Canny 边缘控制 | 结构保持的图像生成/编辑 |
| **FLUX Depth** | 深度图控制 | 3D 结构保持的生成 |
| **FLUX Redux** | 图像变体/重绘 | 保持内容，改变风格/构图 |

这些工具展示了 FLUX 架构的**可控性**和**扩展性**。

---

### 3.6 SD3.5 / 后续迭代 (2024)

#### 3.6.1 SD3.5 的发布

[官方公告](https://stability.ai/news-updates/introducing-stable-diffusion-3-5) 在 **2024-10-22** 发布 Large / Large Turbo，Medium 于 **2024-10-29** 发布。规格分别为 Large 8.1B、同规模蒸馏 Turbo，以及 Medium 2.5B（MMDiT-X）；Turbo 给出的少步配置为 4 步。因此，发布日期和规格不支持“2025 年初、2B/4B/8B”的说法。

公告给出的具体训练设计包括 Query-Key Normalization；更多自定义空间伴随种子间风格/质量差异，模糊提示可能产生较不稳定的结果。作者性能图属于官方自评，尚无独立复现；“更好的人体/手部”不能推广为所有任务的结论。

#### 3.6.2 社区生态适配

SD3.5 面临的主要挑战是**社区生态**：

- SD3 的许可证争议（早期限制商用）导致社区信任受损
- FLUX dev 的权重可获取性与其非商业模型许可证是两个维度；schnell 才是 Apache 2.0
- SD3.5 需要重建 LoRA、ControlNet 等插件生态
- ComfyUI、Stable Diffusion WebUI 等工具已支持 SD3.5

#### 3.6.3 Stability AI 与 BFL 的竞争格局

| 维度 | Stability AI | Black Forest Labs |
|------|-------------|-------------------|
| 核心团队 | 新团队 | 原 SD 核心团队 |
| 最新架构 | MMDiT (SD3.5) | Flow Matching Transformer (FLUX) |
| 开放策略 | 权重开放，按 Community License 等具体版本核对 | schnell 为 Apache 2.0；dev 为非商业模型许可证；pro 为 API |
| 社区生态 | 历史积累深厚，但信任受损 | 新兴，快速增长 |
| 商业模式 | API + 企业授权 | API + 开源 |
| 技术路线 | 延续 MMDiT | 统一序列 Transformer |
| 视频生成研究 | Stable Video Diffusion | BFL 以 FLUX 架构开展 Self-Flow 的视频与联合模态实验；不据此推断 FLUX 产品已有视频版本 |

#### 3.7 Self-Flow (2026)：流匹配中的自监督表征学习

Chefer et al., [Self-Supervised Flow Matching for Scalable Multi-Modal Synthesis, arXiv:2603.06507v1](https://arxiv.org/abs/2603.06507)，2026-03-06，提出 **Dual-Timestep Scheduling + Self-Flow**。动机是外部表征对齐（如 REPA）在模型变大时可能出现反常缩放，而且迁移到视频、音频时可能不如 vanilla flow matching。它不是新的商业 FLUX 版本，而是 BFL 团队提出、以约 625M 参数 FLUX-2 风格 Transformer 为主实验骨干的训练方法。

**机制**：对 token 序列抽取两个噪声时间步，将随机比例 token 加噪到较高时间步、其余 token 保持在较低时间步；学生需从混合噪声输入预测流场，同时匹配 EMA teacher 在较干净输入下的中间表征。联合目标是标准 flow-matching 生成损失与余弦表征匹配损失之和。作者把这种信息不对称视为迫使模型利用较干净上下文推断较噪 token 的方式，以同一生成模型的内部表征替代冻结外部编码器。[论文 §3.1–3.4、式 4–7]

**作者实验与条件**：文本到图像实验使用 Stable Diffusion VAE、2,000 万图文对；视频实验使用 Wan 2.2 VAE、600 万视频；FLUX.2 骨干的单模态实验约 625M 参数，评测集来自相应训练集的 holdout。表 2（§4.1）同为 1M 步时，Self-Flow 的文本图像 FID 为 3.61，vanilla flow 为 4.08、REPA 为 3.92；作者称这一文本图像设置相对 REPA 约 2.8 倍收敛速度。表 3（600K 步）视频 FVD 为 47.81，vanilla flow 50.95，DINOv2 对照 49.59，使用 V-JEPA2 / Depth Anything 3 的对照更差。作者另报告 ImageNet 类条件设置中，4M 步 Self-Flow FID 5.70、REPA 5.89；这组 ImageNet 数字不能与前述 FLUX.2 骨干文本图像结果混为同一实验。多模态 §4.2 还在 RT-1 的 73.5K 轨迹上微调视频-动作模型，并于 SIMPLER 仿真中报告复杂多物体顺序任务的成功率优势。[表 1–4、图 6–8]

**消融与边界**：图 11 显示移除表征损失带来最大退化（ImageNet FID 超过 4 点），移除 mask 或让第二时间步只略微更干净也显著变差；附录 H 显示 student / teacher 层位选择过浅或过深会伤害效果。代价是每步额外一次 teacher 前向，噪声时间步分布也需按任务调参。论文中的跨模态结论限于特定数据、编码器、模型规模和 holdout 评测；没有独立复现，也尚不能推出该目标在生产级 FLUX 权重上带来相同增益。论文附录给出学生/教师层配置、掩码率与推理评测条件，方便复核。[§4.4–5、附录 A.3–A.5、H]

---

## 4. 架构演进对比

### 4.1 骨干网络演进

| 模型 | 骨干网络 | 参数量 | 核心设计 | 模态交互方式 |
|------|----------|--------|----------|--------------|
| SD 1.x | U-Net | 860M（SDXL 论文表 1） | ResNet + Self-Attn + Cross-Attn | Q 为图像特征，K/V 为文本特征 |
| SD 2.x | U-Net | 865M | 同 SD 1.x，更大 | 同 SD 1.x |
| SDXL | Base U-Net + 可选 Refiner | Base U-Net 2.6B | 三个尺度层级，双文本编码器 | Cross-Attention + Micro-Conditioning |
| SD3 Medium | MMDiT | 2B | 双流 Transformer，Joint Attention | Joint Self-Attention (文本+图像 QKV 融合) |
| FLUX.1 | rectified-flow Transformer | 12B | 双流 blocks 后接单流 blocks | 先保留模态表示，再拼接序列 |

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
- dev 与 schnell 权重可获取，但两者许可证不同，不能全家族统称 Apache 2.0
- LoRA、ControlNet、IP-Adapter 适配迅速
- ComfyUI 工作流丰富
- 成为 2024-2025 年开源社区的新焦点

---

## 6. 与竞品对比

### 6.1 开源 vs 闭源图像生成模型

| 维度 | FLUX [dev] | SD3.5 | Midjourney v6 | DALL-E 3 | Ideogram | Imagen 3 |
|------|------------|-------|---------------|----------|----------|----------|
| **权重/许可** | 开放权重；非商业模型许可证 | Community License | 闭源 | 闭源 | 闭源 | 闭源 |
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
- BFL 在 [2024-08-01 成立公告](https://bfl.ai/blog/24-08-01-bfl) 中预告后续 text-to-video 研究；不能由此推导某个图像型号就是视频模型
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
- FLUX schnell 的 Apache 2.0 与 dev 的非商业模型许可证并存；生态影响要区分可获取性与授权范围
- 社区驱动的模型改进（如 LLM 领域的 Llama 生态）
- 去中心化训练和模型共享

---

## 8. 参考链接

证据主要来自 SDXL 原文、固定版本 FLUX.1 源码、SD3/SD3.5 官方材料与 Self-Flow 论文；报告中架构结论以对应版本的原文和源码为界。性能图均按作者报告结果引用，未独立运行权重推理或复现实验。

新增一手来源：[BFL 成立公告](https://bfl.ai/blog/24-08-01-bfl)、[FLUX.1-dev 许可证](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md)、[SD3 Medium 发布](https://stability.ai/news-updates/stable-diffusion-3-medium)、[SD3.5 发布](https://stability.ai/news-updates/introducing-stable-diffusion-3-5)、[SD3.5 代码发布记录](https://github.com/Stability-AI/sd3.5)、[FLUX Tools 公告](https://bfl.ai/blog/24-11-21-tools)、[BFL Self-Flow 研究页](https://bfl.ai/research/self-flow)。

仍待复核：SD1.x 训练配置的统一口径、SD3 目标函数与三编码器具体张量路径、工具支持版本及竞品星级表。后者未附固定提示集或盲评样本，不能当作量化性能证据。

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
| Self-Flow | *Self-Supervised Flow Matching for Scalable Multi-Modal Synthesis*, arXiv:2603.06507v1 (2026-03-06) | https://arxiv.org/abs/2603.06507 |
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
