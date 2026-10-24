---
display_name: 图像编辑与修复
---

# 图像编辑与修复技术研究报告

> **报告日期**：2026年6月6日  
> **研究范围**：从 GAN-based 编辑到扩散模型编辑到 DiT 统一编辑到 Agentic 编辑的完整技术演进  
> **语言**：中文为主，关键英文术语保留

---

## 目录

1. [概述](#1-概述)
2. [发展时间线](#2-发展时间线)
3. [GAN 时代 (2016–2021)](#3-gan-时代-20162021)
4. [扩散模型早期编辑 (2021–2022)](#4-扩散模型早期编辑-20212022)
5. [指令驱动编辑 (2023)](#5-指令驱动编辑-2023)
6. [MLLM 增强编辑 (2024)](#6-mllm-增强编辑-2024)
7. [DiT 统一编辑时代 (2025–2026)](#7-dit-统一编辑时代-20252026)
8. [方法论分类与对比](#8-方法论分类与对比)
9. [RL 对齐与 Agentic 编辑](#9-rl-对齐与-agentic-编辑)
10. [架构演进总结](#10-架构演进总结)
11. [评测基准](#11-评测基准)
12. [应用场景](#12-应用场景)
13. [挑战与未来方向](#13-挑战与未来方向)
14. [参考链接](#14-参考链接)

---

## 1. 概述

图像编辑（Image Editing）与修复（Inpainting/Restoration）是计算机视觉与生成式 AI 交叉领域的核心任务。过去十年间，该领域经历了从**像素级操作**到**语义级理解**再到**推理级规划**的三次范式跃迁：

- **GAN 时代（2016–2021）**：以对抗训练为核心，针对特定任务（风格迁移、图像翻译）设计专用网络，泛化能力受限。
- **扩散模型时代（2021–2024）**：以 Denoising Diffusion Probabilistic Models（DDPM）及其变体为 backbone，通过噪声空间中的逆向过程实现高质量生成与编辑，逐步从 task-specific 走向 general-purpose。
- **DiT 统一时代（2025–2026）**：Diffusion Transformer（DiT）取代 U-Net 成为主流 backbone，Joint Attention 机制将图像 token 与文本指令 token 统一处理，实现生成与编辑的架构统一。
- **Agentic 时代（2025–2026）**：多模态大语言模型（MLLM）作为 planner，结合 Chain-of-Thought（CoT）推理与强化学习（RL）对齐，将编辑从"单次生成"升级为"多步规划+执行"。

本报告系统梳理上述演进脉络，重点分析模型架构变迁（U-Net Cross-Attention → DiT Joint Attention）、方法论分类（Training-Based / Testing-Time Finetuning / Training-Free）、以及 RL 对齐与 Agentic 编辑的最新进展。

---

## 2. 发展时间线

| 年份 | 里程碑工作 | 核心贡献 | 架构特点 | 代表模型/方法 |
|:---|:---|:---|:---|:---|
| 2016 | Neural Style Transfer | 优化-based 风格迁移 | 优化 Gram Matrix | Gatys et al. |
| 2017 | pix2pix / CycleGAN | 有监督/无监督图像翻译 | Encoder-Decoder + GAN | Isola et al. |
| 2018 | StarGAN / GauGAN | 多域翻译 / 语义图像合成 | 条件 GAN | StarGAN, SPADE |
| 2020 | DDPM / Score-Based | 扩散模型奠基 | U-Net + Time Embedding | Ho et al., Song et al. |
| 2021 | SDEdit | SDE-based 图像编辑 | 加噪到中间 timestep 再去噪 | SDEdit |
| 2022 | DiffEdit / Prompt-to-Prompt | Mask guidance / 文本驱动编辑 | 注意力图替换 / Mask 引导 | DiffEdit, P2P |
| 2022 | Stable Diffusion | Latent Diffusion Model (LDM) | U-Net + VAE + CLIP | Rombach et al. |
| 2023 | InstructPix2Pix | 端到端指令驱动编辑 | 微调 U-Net，文本+图像条件 | Brooks et al. (CVPR) |
| 2023 | MasaCtrl | 无需训练的一致性编辑 | Mutual Self-Attention Control | ICCV 2023 |
| 2023 | MagicBrush | 高质量手动标注数据集 | 更强基线与评测标准 | MagicBrush |
| 2023 | ImageReward | 人类偏好奖励模型 | 奖励模型用于 RL 对齐 | ImageReward |
| 2024 | MGIE | MLLM 扩展指令为 latent guidance | 多模态 LLM + 扩散模型 | MGIE |
| 2024 | UltraEdit / SmartEdit / HQ-Edit | 更大规模数据与更强模型 | 数据驱动 scaling | UltraEdit, SEED-Data-Edit |
| 2024 | Emu-Edit | Meta 多任务编辑框架 | 多任务训练 + 指令遵循 | Meta |
| 2024 | BrushNet | Mask-conditioned editing | 独立分支注入 mask 条件 | BrushNet |
| 2024 | FLUX.1-Fill | Inpainting / Outpainting | Flow Matching + Mask | Black Forest Labs |
| 2024 | Qwen-Image-Edit | Flow-matching diffusion | 50 steps, CFG=4.0 | Alibaba |
| 2025 | FLUX.1-Kontext / FLUX-Kontext | In-context editing | 图像+文本 token 拼接 → Joint Attention | Black Forest Labs |
| 2025 | BAGEL | DiT-class editor | 纯 Transformer 编辑 backbone | BAGEL |
| 2025 | OmniGen2 | 统一生成+编辑 | 单一模型处理多种视觉任务 | OmniGen2 |
| 2025 | Step1X-Edit | 高效编辑模型 | 优化采样效率 | Step1X-Edit |
| 2025 | Qwen-2511 | 升级版本 | 40 steps，效率提升 | Alibaba |
| 2025 | Flow-GRPO / Dance-GRPO | RL 对齐扩散模型 | 随机探索逃离局部最优 | Flow-GRPO |
| 2025 | Edit-R1 / Agentic-Retoucher | CoT 推理融入编辑 | Agentic 规划+生成 | Edit-R1 |
| 2026 | FireRed 1.1 | Distilled transformer | 4 steps，无 CFG | FireRed |
| 2026 | FLUX 2 | 9B rectified-flow transformer | 4 steps, KV cache | Black Forest Labs |
| 2026 | SpatialReward | 显式空间推理的在线 RL | 空间感知奖励函数 | SpatialReward |
| 2026 | DraCo | Draft-as-CoT | 分层子任务规划 | DraCo |

---

## 3. GAN 时代 (2016–2021)

### 3.1 Neural Style Transfer (2016)

Gatys et al. 提出的 Neural Style Transfer 是深度学习图像编辑的开山之作。其核心思想是：

- **内容表示**：使用预训练 VGG 网络的高层特征图（如 `conv4_2`）捕获图像语义内容。
- **风格表示**：使用 Gram Matrix 统计多层特征图的通道间相关性，捕获纹理风格。
- **优化过程**：随机初始化目标图像，通过梯度下降最小化内容损失与风格损失的加权和。

**局限**：优化-based，单张图像编辑需数百次迭代，速度慢；无法处理复杂语义编辑。

### 3.2 pix2pix / CycleGAN (2017)

Isola et al. 提出的 pix2pix 将有监督图像翻译框架化：

```
输入图像 x → [U-Net Encoder] → Bottleneck → [U-Net Decoder] → 输出图像 y
                          ↓
                    Skip Connections
                          ↓
                    保留高频细节
```

- **pix2pix**：需要成对训练数据（paired data），使用 Conditional GAN 框架，L1 损失保证像素级相似性。
- **CycleGAN**：引入 Cycle Consistency Loss，实现无监督（unpaired）图像翻译，无需成对数据。

**局限**：
- 特定任务训练（如 horse↔zebra、summer↔winter），换任务需重新训练。
- 泛化能力差，无法处理开放式文本指令。
- 模式崩溃（mode collapse）问题严重，生成多样性不足。

### 3.3 GAN 时代总结

GAN-based 编辑的核心特征是**任务专用性**：每个模型针对特定域转换设计，网络结构（Encoder-Decoder、Generator-Discriminator）与训练数据强耦合。这一时期的编辑操作停留在**像素/特征空间映射**，缺乏对高层语义的理解能力。

---

## 4. 扩散模型早期编辑 (2021–2022)

### 4.1 SDEdit (2021)

SDEdit（Stochastic Differential Editing）是扩散模型用于图像编辑的早期代表：

**架构流程**：
```
源图像 x_0 → 前向加噪 → 中间噪声 x_t (t ~ 0.3T-0.7T)
                                    ↓
              条件（文本/草图/mask）→ 逆向去噪 → 编辑后图像 x'_0
```

- **核心思想**：将源图像加噪到中间 timestep，再使用条件扩散模型去噪，噪声强度控制编辑程度。
- **优点**：无需训练，直接利用预训练扩散模型。
- **缺点**：控制精度低，编辑区域与保留区域难以精确分离；文本条件与图像条件融合粗糙。

### 4.2 DiffEdit (2022)

DiffEdit 引入 **mask guidance** 实现语义编辑：

1. **自动 Mask 生成**：比较源文本与目标文本的注意力图差异，自动生成编辑区域 mask。
2. **Masked Diffusion**：在 mask 区域内进行扩散编辑，mask 外区域保持原图内容。

**特点**：首次实现无需用户手动标注 mask 的语义编辑，但 mask 精度依赖注意力图质量，边界处理仍有瑕疵。

### 4.3 Prompt-to-Prompt (2022)

Prompt-to-Prompt 通过**注意力图替换**实现文本驱动编辑：

- **Cross-Attention 替换**：在去噪过程中，将源文本的 cross-attention map 替换为目标文本的对应 map。
- **Self-Attention 保持**：保留 self-attention 以维持图像结构一致性。

**局限**：仅适用于文本 token 级别的简单替换（如 "cat" → "dog"），复杂指令无法处理。

### 4.4 MasaCtrl (ICCV 2023)

MasaCtrl 提出 **Mutual Self-Attention Control**，实现无需训练的一致性编辑：

```
源图像去噪路径:  x_t → [Self-Attn_s] → x_{t-1}
                          ↓ 共享 K, V
目标图像去噪路径:  x'_t → [Self-Attn_t] → x'_{t-1}
```

- **Mutual Self-Attention**：在编辑路径与源图像路径之间共享 Key 和 Value，强制结构一致性。
- **特点**：无需训练、无需 mask、无需 inversion，实现 zero-shot 图像编辑。

---

## 5. 指令驱动编辑 (2023)

### 5.1 InstructPix2Pix (CVPR 2023, Brooks et al.)

InstructPix2Pix 是**端到端指令驱动编辑**的里程碑工作。

#### 5.1.1 数据构建

```
GPT-3 生成编辑指令（如 "make it snowy"）
           ↓
Prompt-to-Prompt 生成编辑前后图像对 (x, x')
           ↓
过滤低质量样本 → 合成数据集 ~500K 对
```

#### 5.1.2 模型架构

基于 Stable Diffusion U-Net 微调，条件注入方式：

```
输入条件:
  - 源图像 latent z_0（通过 VAE 编码）
  - 文本指令 embedding（通过 CLIP 编码）

条件注入:
  - 图像条件: 与噪声 latent 在通道维度拼接（channel-wise concatenation）
  - 文本条件: 通过 Cross-Attention 注入 U-Net 各层

U-Net 结构:
  Input: [z_t; z_0]  (噪声 + 源图像 latent 拼接)
    ↓
  Down Blocks + Cross-Attention(文本) + Time Embedding
    ↓
  Mid Block
    ↓
  Up Blocks + Cross-Attention(文本) + Skip Connections
    ↓
  Output: 预测噪声 ε_θ(z_t, t, text, z_0)
```

#### 5.1.3 训练与推理

- **训练目标**：标准扩散损失，但条件包含源图像与文本指令。
- **推理**：Classifier-Free Guidance（CFG）同时应用于文本与图像条件，平衡编辑强度与源图保留。

#### 5.1.4 局限

- **局部编辑泄漏**：全局条件注入导致编辑区域外内容被意外修改。
- **数据质量**：合成数据存在 domain gap，复杂指令遵循能力不足。
- **结构保持**：大幅编辑时源图结构难以保持。

### 5.2 MagicBrush (2023)

MagicBrush 构建了**高质量手动标注数据集**：

- **数据规模**：约 10K 高质量编辑对，涵盖多样化指令类型。
- **标注方式**：人工标注编辑指令与编辑区域 mask。
- **评测标准**：引入 L1, L2, CLIP-I, DINO, CLIP-T 等多维度指标，成为后续工作的标准评测基准。

---

## 6. MLLM 增强编辑 (2024)

### 6.1 MGIE (2024)

MGIE（Multimodal Guided Image Editing）引入 MLLM 增强指令理解：

```
用户短指令: "make it better"
           ↓
[MLLM, e.g., LLaVA] → 扩展为丰富 latent guidance
  "增加饱和度，提亮阴影，增强对比度，使天空更蓝"
           ↓
Latent Guidance → 注入扩散模型进行编辑
```

- **核心创新**：MLLM 将模糊短指令扩展为详细的 latent-level 操作描述。
- **架构**：两阶段框架，MLLM 生成 guidance → 扩散模型执行编辑。

### 6.2 UltraEdit / SmartEdit / HQ-Edit / SEED-Data-Edit (2024)

2024 年涌现大量数据驱动编辑工作：

| 工作 | 核心特点 |
|:---|:---|
| UltraEdit | 超大规模合成数据集（>1M 编辑对），Scaling Law 验证 |
| SmartEdit | 智能数据过滤与质量提升策略 |
| HQ-Edit | 高质量编辑数据构建 pipeline |
| SEED-Data-Edit | 系统性数据标注与评测协议 |

共同趋势：**数据规模与质量成为编辑模型性能的关键决定因素**。

### 6.3 Emu-Edit (2024, Meta)

Emu-Edit 是 Meta 提出的**多任务编辑框架**：

- **任务覆盖**：风格迁移、对象替换、背景修改、局部编辑、全局调整等 8+ 任务类型。
- **训练策略**：多任务联合训练 + 任务类型标签，提升模型泛化能力。
- **特点**：首次在单一模型中实现多种编辑任务的统一处理。

### 6.4 BrushNet (2024)

BrushNet 提出 **Mask-Conditioned Editing with Independent Branch**：

```
源图像 → VAE Encoder → Latent z_0
Mask  → 独立分支编码 → Mask Feature m

U-Net 主路径:  z_t → [Down] → [Mid] → [Up] → Output
Mask 分支:    m   → [Down] → [Mid] → [Up] → Feature
                          ↓ 特征融合
                    精确控制编辑区域
```

- **独立分支**：mask 条件通过独立编码分支处理，避免与主路径干扰。
- **精确控制**：实现像素级精确的局部编辑，解决 InstructPix2Pix 的泄漏问题。

### 6.5 FLUX.1-Fill (2024)

Black Forest Labs 推出的 FLUX.1-Fill 专注于 **Inpainting / Outpainting**：

- **架构**：基于 Flow Matching，将 mask 作为额外条件通道输入。
- **特点**：高质量填充与扩展，成为 2024 年 inpainting 领域的 SOTA。

---

## 7. DiT 统一编辑时代 (2025–2026)

### 7.1 架构演进：从 U-Net Cross-Attention 到 DiT Joint Attention

2025 年起，图像编辑 backbone 发生根本性变革：

```
U-Net 时代 (2021-2024):
  ┌─────────────────────────────────────────┐
  │  图像 Latent: z ∈ R^(C×H×W)              │
  │  文本 Embedding: e ∈ R^(L×D)             │
  │                                         │
  │  U-Net: Conv + ResBlock + Cross-Attn     │
  │  图像通过卷积处理，文本通过 Cross-Attention│
  │  注入，两种模态交互有限                   │
  └─────────────────────────────────────────┘

DiT 时代 (2025-2026):
  ┌─────────────────────────────────────────┐
  │  图像 Tokens: t_img ∈ R^(N_img × D)      │
  │  文本 Tokens: t_txt ∈ R^(N_txt × D)       │
  │                                         │
  │  拼接: [t_img; t_txt] ∈ R^((N_img+N_txt)×D)│
  │                                         │
  │  DiT: 多层 Transformer + Joint Attention  │
  │  图像与文本在统一 token 空间中交互         │
  │  信息融合更充分，编辑更精准                │
  └─────────────────────────────────────────┘
```

**关键变化**：
- **Backbone**：从 1B 参数 U-Net 到 multi-billion 参数 DiT。
- **模态交互**：从 Cross-Attention（文本→图像单向查询）到 Joint Attention（图像+文本 token 互相查询）。
- **条件形式**：从 channel-wise concatenation / cross-attention 到 token-level concatenation。

### 7.2 关键模型详解

#### 7.2.1 FLUX.1-Kontext / FLUX-Kontext (2025)

FLUX-Kontext 是 Black Forest Labs 推出的 **In-Context Editing** 模型：

**架构**：
```
输入序列:
  [IMG_START] 图像 Token 1 ... 图像 Token N [IMG_END]
  [TXT_START] 文本指令 Token 1 ... [TXT_END]
  [IMG_START] 参考图像 Token ... [IMG_END]  (可选 in-context 示例)

处理:
  所有 token 拼接 → Joint Attention Transformer
  每层的 Self-Attention 同时作用于图像与文本 token
  无需显式 Cross-Attention 层

输出:
  图像 token 部分 → VAE Decoder → 编辑后图像
```

**特点**：
- **In-Context Learning**：支持多示例编辑（few-shot editing），提供参考图像即可学习新编辑风格。
- **Flow Matching**：基于 rectified flow，采样步数少（4–50 steps）。
- **统一框架**：同一模型处理生成、编辑、inpainting、outpainting。

#### 7.2.2 BAGEL (2025)

BAGEL 是专为编辑设计的 **DiT-class Editor**：

- **纯 Transformer**：完全摒弃卷积，所有操作在 token 空间完成。
- **编辑专用设计**：针对编辑任务优化 attention pattern，强化源图像与目标图像 token 的对应关系。
- **高效性**：通过 attention 优化实现高质量编辑的实时推理。

#### 7.2.3 OmniGen2 (2025)

OmniGen2 追求 **统一生成+编辑** 的终极愿景：

- **单一模型**：同一 DiT 处理文本生成图像、图像编辑、图像翻译、多图融合等所有视觉任务。
- **统一输入格式**：所有任务表示为 [图像 token; 文本 token] 序列，无需任务专用 head。
- **Scaling**：验证 DiT 在视觉任务中的 Scaling Law，更大模型带来更优编辑质量。

#### 7.2.4 Step1X-Edit (2025)

Step1X-Edit 专注于 **高效编辑**：

- **步数优化**：通过蒸馏与采样策略优化，减少推理步数。
- **质量保持**：在加速的同时保持编辑质量与结构一致性。

#### 7.2.5 Qwen-Image-Edit (2024) / Qwen-2511 (2025)

阿里巴巴推出的系列编辑模型：

| 版本 | 年份 | 架构 | 采样步数 | CFG |
|:---|:---|:---|:---|:---|
| Qwen-Image-Edit | 2024 | Flow-matching Diffusion | 50 steps | CFG=4.0 |
| Qwen-2511 | 2025 | 升级 Flow Matching | 40 steps | 优化 CFG |

- **特点**：中文指令支持优秀，在中文场景下编辑质量领先。
- **演进**：从 50 步到 40 步，效率持续提升。

#### 7.2.6 FireRed 1.1 (2026)

FireRed 1.1 是 **Distilled Transformer** 的代表：

- **超快推理**：仅需 **4 steps**，无 CFG（Classifier-Free Guidance）。
- **蒸馏技术**：通过对抗蒸馏与一致性蒸馏，将多步模型压缩为少步模型。
- **适用场景**：实时编辑应用（如移动端、Web 实时预览）。

#### 7.2.7 FLUX 2 (2025)

FLUX 2 是 Black Forest Labs 的旗舰模型：

- **规模**：9B 参数 Rectified-Flow Transformer。
- **效率**：4 steps 采样，KV Cache 加速。
- **能力**：生成与编辑的统一 SOTA，支持高分辨率（4K+）编辑。

### 7.3 从 Mask-Based 到 Mask-Free

DiT 时代出现 **Mask-Free 编辑** 趋势：

- **Region-Aware Adapter**：通过 attention 机制隐式感知编辑区域，无需显式 mask。
- **BRIDGE**：双向区域感知机制，自动定位语义编辑区域。
- **优势**：用户只需文本指令，无需手动绘制 mask，降低使用门槛。
- **挑战**：复杂场景下区域定位精度仍有提升空间。

---

## 8. 方法论分类与对比

### 8.1 三大类方法论

图像编辑方法按训练需求分为三大类：

#### (1) Training-Based

需要在大规模编辑数据集上训练或微调模型。

**代表工作**：
- InstructPix2Pix (2023)
- MagicBrush (2023)
- UltraEdit (2024)
- SmartEdit (2024)
- Emu-Edit (2024)
- AnyEdit (2024)
- Step1X-Edit (2025)
- FLUX-Kontext (2025)
- BAGEL (2025)
- OmniGen2 (2025)

**优点**：编辑质量高，指令遵循能力强，端到端优化。
**缺点**：需要大量训练数据，计算成本高，模型泛化受数据分布限制。

#### (2) Testing-Time Finetuning

在推理阶段对模型进行少量步数的微调或优化。

**子类型**：
- **Denoising Model Finetuning**：针对特定图像微调去噪模型参数（如 Imagic）。
- **Embeddings Finetuning**：优化文本 embedding 或图像 inversion 编码（如 Textual Inversion）。
- **Hypernetworks**：训练小型网络生成编辑条件（如 HyperDreamBooth）。
- **Latent Optimization**：在 latent 空间直接优化目标图像（如 SDEdit 的进阶版本）。

**优点**：无需预训练编辑模型，可处理训练时未见过的编辑类型。
**缺点**：每张图像需额外优化时间（分钟级），不适合实时应用。

#### (3) Training-Free

直接利用预训练扩散模型，无需任何训练或微调。

**子类型**：
- **Text Refinement**：通过改写、扩展文本指令提升编辑效果（如 MGIE 的 lightweight 版本）。
- **Inversion / Sampling Modification**：修改采样过程（如 DDIM Inversion、Null-Text Inversion）。
- **Attention Modification**：操纵 attention map（如 MasaCtrl、Prompt-to-Prompt、Attention Refinement）。
- **Mask Guidance**：使用显式或隐式 mask 控制编辑区域（如 DiffEdit、BrushNet 的 testing-time 版本）。
- **Multi-Noise Redirection**：在噪声空间重定向编辑方向（如 Noise Collage）。

**优点**：零成本，即插即用，灵活性强。
**缺点**：编辑质量通常低于 training-based 方法，复杂编辑难以实现。

### 8.2 方法论对比表

| 维度 | Training-Based | Testing-Time Finetuning | Training-Free |
|:---|:---|:---|:---|
| **训练成本** | 高（需大规模数据+GPU 集群） | 中（单图/小批量微调） | 无 |
| **推理成本** | 低（单次前向） | 高（每图需优化） | 低（单次/少次采样） |
| **编辑质量** | 高 | 中高 | 中 |
| **泛化能力** | 受训练数据限制 | 强（针对单图优化） | 强（依赖预训练模型能力） |
| **实时性** | 是 | 否 | 是 |
| **用户门槛** | 低（端到端） | 高（需等待优化） | 低（即插即用） |
| **代表模型** | InstructPix2Pix, FLUX-Kontext | Imagic, Textual Inversion | MasaCtrl, DiffEdit |
| **适用场景** | 产品级应用、批量编辑 | 高精度单图编辑 | 快速原型、研究实验 |

---

## 9. RL 对齐与 Agentic 编辑

### 9.1 人类偏好对齐 (2023–2024)

#### 9.1.1 ImageReward (2023)

ImageReward 是首个大规模 **人类偏好奖励模型**：

- **数据**：收集大量人类对生成图像的偏好对比数据。
- **模型**：训练奖励模型预测人类偏好分数。
- **应用**：用于 RLHF（Reinforcement Learning from Human Feedback）优化扩散模型。

#### 9.1.2 DDPO / D3PO (2023–2024)

直接优化扩散模型的 RL 方法：

- **DDPO（Denoising Diffusion Policy Optimization）**：将扩散采样视为策略，通过策略梯度直接优化奖励。
- **D3PO（Direct Diffusion Policy Optimization）**：改进 DDPO，提升训练稳定性与样本效率。

**核心挑战**：扩散采样链长，信用分配困难；奖励模型偏差导致优化不稳定。

### 9.2 高级 RL 方法 (2025)

#### 9.2.1 Flow-GRPO / Dance-GRPO (2025)

针对扩散模型的 **Group Relative Policy Optimization**：

- **随机探索**：通过组内采样对比，逃离局部最优。
- **Flow Matching 兼容**：适配 rectified flow 的连续时间框架。
- **效果**：显著提升编辑结果的人类偏好分数，减少模式崩溃。

### 9.3 空间感知 RL (2026)

#### 9.3.1 SpatialReward (2026)

SpatialReward 提出 **显式空间推理的在线 RL**：

- **空间奖励函数**：不仅评估整体图像质量，还评估编辑区域的空间位置准确性、边界一致性、结构保持度。
- **在线学习**：在编辑过程中实时收集反馈，动态调整策略。
- **突破**：解决传统 RL 对空间关系理解不足的问题。

### 9.4 Agentic 编辑 (2025–2026)

Agentic 编辑是 2025–2026 年的新兴范式，将编辑从"单次生成"升级为"多步规划+执行"。

#### 9.4.1 RPG (Recaption, Plan, Generate)

RPG 框架引入 **LMM 作为 Planner**：

```
用户指令: "让这张照片更有夏日氛围"
           ↓
[Recaption] LMM 分析图像内容，生成详细描述
  "海滩照片，蓝天，棕榈树，人物穿着冬装"
           ↓
[Plan] LMM 制定编辑计划
  Step 1: 将人物服装改为夏装
  Step 2: 增强天空饱和度
  Step 3: 添加阳光光效
           ↓
[Generate] 执行每步编辑，迭代优化
           ↓
最终输出: 夏日海滩照片
```

#### 9.4.2 DraCo (Draft-as-CoT)

DraCo 提出 **分层子任务规划**：

- **Draft 阶段**：LMM 生成编辑草图（layout / mask / 中间结果）。
- **Chain-of-Thought**：将复杂编辑分解为可验证的子任务链。
- **执行**：每步子任务由专用模块（生成、修复、融合）执行。

#### 9.4.3 Edit-R1 / Agentic-Retoucher (2025–2026)

将 **CoT 推理融入编辑循环**：

- **Edit-R1**：基于 R1 推理框架，在编辑过程中显式生成推理链（"我需要先修改背景，再调整人物，最后统一色调"）。
- **Agentic-Retoucher**：多 agent 协作系统，不同 agent 负责不同编辑子任务，通过消息传递协调。

**Agentic 编辑核心优势**：
- **可解释性**：编辑步骤透明，用户可审查每步操作。
- **复杂任务处理**：分解-执行策略可处理传统端到端模型无法完成的复杂编辑。
- **错误恢复**：某步失败可重试或调整计划，系统鲁棒性更强。

---

## 10. 架构演进总结

图像编辑架构的十年演进可概括为五个阶段：

```
┌─────────────────────────────────────────────────────────────────────┐
│  Stage 1: GAN 特定任务 (2016-2021)                                   │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                        │
│  │ 风格迁移 │    │ 图像翻译 │    │ 人脸编辑 │  ← 每个任务一个模型     │
│  │  (专用)  │    │  (专用)  │    │  (专用)  │                        │
│  └─────────┘    └─────────┘    └─────────┘                        │
│  特征: 像素操作，任务专用，泛化差                                    │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 2: 扩散通用生成+编辑 (2021-2023)                              │
│  ┌─────────────────────────────────────────┐                        │
│  │         预训练扩散模型 (通用)            │                        │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐  │                        │
│  │  │ SDEdit  │ │ DiffEdit│ │ MasaCtrl│  │  ← 同一模型，不同技巧   │
│  │  └─────────┘ └─────────┘ └─────────┘  │                        │
│  └─────────────────────────────────────────┘                        │
│  特征: 噪声空间操作，通用 backbone，技巧驱动                         │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 3: 指令驱动端到端 (2023-2024)                                 │
│  ┌─────────────────────────────────────────┐                        │
│  │  源图像 + 文本指令 → [InstructPix2Pix] → 目标图像                 │
│  │  端到端训练，数据驱动 scaling          │                        │
│  └─────────────────────────────────────────┘                        │
│  特征: 语义理解，端到端优化，数据为王                                │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 4: DiT 统一 Joint Attention (2025-2026)                      │
│  ┌─────────────────────────────────────────┐                        │
│  │  [图像 Token; 文本 Token] → [DiT Joint Attn] → 输出            │
│  │  生成与编辑统一架构，mask-free         │                        │
│  └─────────────────────────────────────────┘                        │
│  特征: 架构统一，模态深度融合，Scaling Law                          │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 5: Agentic 规划+生成 (2025-2026)                               │
│  ┌─────────────────────────────────────────┐                        │
│  │  用户指令 → [LMM Planner] → 子任务链 → [DiT 执行] → 结果       │
│  │  CoT 推理，多步规划，错误恢复          │                        │
│  └─────────────────────────────────────────┘                        │
│  特征: 推理规划，可解释，复杂任务处理                                │
└─────────────────────────────────────────────────────────────────────┘
```

**本质跃迁**：
- 从 **"像素操作"**（GAN 时代的卷积特征映射）
- 到 **"语义理解"**（扩散时代的文本-图像条件融合）
- 再到 **"推理规划"**（Agentic 时代的多步分解与执行）

---

## 11. 评测基准

### 11.1 MagicBrush 评测体系

MagicBrush 建立了图像编辑的标准评测框架：

| 指标 | 类型 | 含义 | 计算方式 |
|:---|:---|:---|:---|
| **L1** | Pixel Distance | 像素级绝对差异 | \|x - x'\|_1 |
| **L2** | Pixel Distance | 像素级平方差异 | \|x - x'\|_2^2 |
| **CLIP-I** | Visual Similarity | 编辑前后图像的语义一致性 | CLIP 图像 embedding 余弦相似度 |
| **DINO** | Visual Similarity | 结构保持度 | DINO-ViT 特征相似度 |
| **CLIP-T** | Text-Image Alignment | 文本-图像对齐度 | CLIP 文本与目标图像 embedding 相似度 |

**评测逻辑**：
- **L1/L2**：衡量编辑强度（越低表示编辑越保守）。
- **CLIP-I / DINO**：衡量源图结构保持度（越高越好）。
- **CLIP-T**：衡量指令遵循度（越高越好）。
- **理想编辑**：L1/L2 适中（足够编辑），CLIP-I/DINO 高（结构保持），CLIP-T 高（指令遵循）。

### 11.2 EditEval_v1

EditEval_v1 是综合性编辑评测基准：

- **任务覆盖**：对象替换、风格迁移、属性修改、背景替换、局部编辑等。
- **评测维度**：编辑质量、指令遵循、结构保持、自然度。
- **自动指标 + 人类评估**：结合定量指标与定性人类偏好。

### 11.3 2026 VLM-Judge Protocols

2026 年兴起的 **VLM-as-Judge** 评测范式：

- **评测者**：多模态大语言模型（如 GPT-4V、Qwen-VL）。
- **输入**：源图像、编辑指令、目标图像。
- **输出**：细粒度评分与文字评价（如"编辑区域准确，但边界有轻微伪影"）。
- **优势**：可评估传统指标无法捕捉的语义级质量（如"夏日氛围"是否到位）。
- **挑战**：VLM 自身偏见，评分一致性需校准。

---

## 12. 应用场景

图像编辑技术的成熟催生了丰富的应用场景：

### 12.1 消费级应用

| 场景 | 描述 | 代表产品/功能 |
|:---|:---|:---|
| 智能修图 | 一键美颜、肤色调整、瑕疵修复 | 美图秀秀、Adobe Photoshop AI |
| 风格迁移 | 照片转油画、漫画、水彩 | Prisma、Lensa |
| 背景替换 | 证件照背景、产品图背景 | Remove.bg、Canva |
| 对象增删 | 移除路人、添加元素 | Adobe Generative Fill |

### 12.2 专业创作

| 场景 | 描述 | 技术要求 |
|:---|:---|:---|
| 广告设计 | 快速生成多版本广告图 | 高分辨率、品牌一致性 |
| 影视后期 | 场景扩展、特效预演 | 时序一致性、4K+ 分辨率 |
| 游戏美术 | 概念图迭代、资产变体 | 风格控制、批量生成 |
| 建筑可视化 | 方案修改、氛围调整 | 结构保持、精确控制 |

### 12.3 工业与科研

| 场景 | 描述 | 技术要求 |
|:---|:---|:---|
| 医学影像 | 病灶标注、图像增强 | 高精度、可解释性 |
| 遥感图像 | 地物变化检测、图像修复 | 大规模、地理一致性 |
| 文物保护 | 古画修复、缺损填补 | 可逆性、历史真实性 |
| 自动驾驶 | 场景编辑、数据增强 | 物理一致性、安全性 |

---

## 13. 挑战与未来方向

### 13.1 当前挑战

#### (1) 精确控制与泛化的矛盾

- **问题**：Training-based 方法泛化受数据限制，Training-free 方法质量不足。
- **表现**：复杂场景下（如"将左边穿红衣服的人改为穿蓝衣服"）编辑失败率高。

#### (2) 结构保持与编辑强度的平衡

- **问题**：大幅编辑时源图结构易被破坏，保守编辑则效果不明显。
- **表现**：人脸编辑中身份保持与表情/妆容修改难以兼顾。

#### (3) 高分辨率与实时性

- **问题**：4K+ 分辨率编辑计算成本高，实时应用（如视频编辑）困难。
- **表现**：当前 SOTA 模型在 4K 分辨率下推理时间以分钟计。

#### (4) 评测的局限性

- **问题**：传统指标（L1/L2/CLIP）无法全面反映人类感知质量。
- **表现**：VLM-Judge 虽更贴近人类判断，但一致性与可重复性待提升。

#### (5) 安全与伦理

- **问题**：深度伪造（Deepfake）、隐私侵犯、版权争议。
- **表现**：人脸替换技术被滥用，生成内容溯源困难。

### 13.2 未来方向

#### (1) 统一多模态编辑

- **方向**：将图像、视频、3D、音频编辑统一于单一 DiT 框架。
- **趋势**：OmniGen2 已迈出第一步，未来将出现真正的"全能视觉编辑器"。

#### (2) 实时交互式编辑

- **方向**：用户通过画笔、语音、手势实时交互，模型即时响应。
- **技术**：FireRed 1.1 的 4-step 推理、KV Cache 优化、模型量化。

#### (3) 物理一致性编辑

- **方向**：编辑结果符合物理规律（光照、阴影、反射、重力）。
- **技术**：结合物理引擎与神经渲染，实现"真实世界"级编辑。

#### (4) 个性化与少样本学习

- **方向**：用户仅需提供 1–3 张参考图，模型即可学习个人风格。
- **技术**：In-Context Learning（FLUX-Kontext）、Meta-Learning、Adapter 微调。

#### (5) 可解释与可控 Agentic 编辑

- **方向**：用户可审查、修改、回滚编辑计划的每一步。
- **技术**：CoT 可视化、人机协作规划、编辑操作日志。

#### (6) 安全与溯源技术

- **方向**：编辑内容自动加水印/签名，AI 生成内容可溯源。
- **技术**：C2PA 标准、神经水印、区块链溯源。

---

## 14. 参考链接

### 14.1 经典论文

| 论文 | 作者 | 年份 | 链接 |
|:---|:---|:---|:---|
| Image Style Transfer Using Convolutional Neural Networks | Gatys et al. | 2016 | [CVPR](https://www.cv-foundation.org/openaccess/content_cvpr_2016/html/Gatys_Image_Style_Transfer_CVPR_2016_paper.html) |
| Image-to-Image Translation with Conditional Adversarial Networks | Isola et al. | 2017 | [CVPR](https://openaccess.thecvf.com/content_cvpr_2017/html/Isola_Image-To-Image_Translation_With_CVPR_2017_paper.html) |
| Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks | Zhu et al. | 2017 | [ICCV](https://openaccess.thecvf.com/content_iccv_2017/html/Zhu_Unpaired_Image-To-Image_Translation_ICCV_2017_paper.html) |
| Denoising Diffusion Probabilistic Models | Ho et al. | 2020 | [NeurIPS](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html) |
| Score-Based Generative Modeling through Stochastic Differential Equations | Song et al. | 2021 | [ICLR](https://openreview.net/forum?id=PxTIG12RRHS) |
| SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations | Meng et al. | 2021 | [ICLR](https://openreview.net/forum?id=aBsCjcGa_1a) |
| DiffEdit: Diffusion-based semantic image editing with mask guidance | Couairon et al. | 2022 | [arXiv](https://arxiv.org/abs/2210.11427) |
| Prompt-to-Prompt Image Editing with Cross Attention Control | Hertz et al. | 2022 | [ICLR](https://openreview.net/forum?id=_6vIbF8L6J) |
| High-Resolution Image Synthesis with Latent Diffusion Models | Rombach et al. | 2022 | [CVPR](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html) |
| InstructPix2Pix: Learning to Follow Image Editing Instructions | Brooks et al. | 2023 | [CVPR](https://openaccess.thecvf.com/content/CVPR2023/html/Brooks_InstructPix2Pix_Learning_To_Follow_Image_Editing_Instructions_CVPR_2023_paper.html) |
| MasaCtrl: Tuning-Free Mutual Self-Attention Control for Consistent Image Synthesis and Editing | Cao et al. | 2023 | [ICCV](https://openaccess.thecvf.com/content/ICCV2023/html/Cao_MasaCtrl_Tuning-Free_Mutual_Self-Attention_Control_for_Consistent_Image_Synthesis_ICCV_2023_paper.html) |
| MagicBrush: A Manually Annotated Dataset for Instruction-Guided Image Editing | Zhang et al. | 2023 | [arXiv](https://arxiv.org/abs/2306.10012) |
| ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation | Xu et al. | 2023 | [NeurIPS](https://arxiv.org/abs/2304.05977) |
| MGIE: Guiding Image Editing via Multimodal Instruction | Fu et al. | 2024 | [CVPR](https://openaccess.thecvf.com/content/CVPR2024/html/Fu_MGIE_Guiding_Image_Editing_via_Multimodal_Instruction_CVPR_2024_paper.html) |
| UltraEdit: Instruction-based Fine-grained Image Editing at Scale | Zhang et al. | 2024 | [arXiv](https://arxiv.org/abs/2407.03162) |
| Emu Edit: Precise Image Editing via Recognition and Generation Tasks | Sheynin et al. | 2024 | [arXiv](https://arxiv.org/abs/2311.10071) |
| BrushNet: A Plug-and-Play Image Inpainting Model with Decomposed Dual-Branch Diffusion | Zhang et al. | 2024 | [ECCV](https://arxiv.org/abs/2403.06976) |
| Scaling Rectified Flow Transformers for High-Resolution Image Synthesis | Esser et al. | 2024 | [arXiv](https://arxiv.org/abs/2403.03206) (Stable Diffusion 3，不能当作FLUX技术报告) |
| Flow-GRPO: Training Flow Matching Models via Online RL | Jie Liu et al. | 2025 | [arXiv](https://arxiv.org/abs/2505.05470)（本轮核题录/摘要，未重做实验精读） |
| FLUX.1-Kontext: In-Context Editing with Flow Matching | Black Forest Labs | 2025 | [BFL](https://blackforestlabs.ai/) |
| OmniGen2: Towards Instruction-Aligned Multimodal Generation | Chenyuan Wu et al. | 2025首发，v4于2026 | [arXiv v4](https://arxiv.org/abs/2506.18871v4)（题录已核，旧版题名Exploration to Advanced Multimodal Generation） |
| FireRed: Distilled Real-Time Image Editing | (2026) | 2026 | [arXiv](https://arxiv.org/) |

### 14.2 开源项目与工具

| 项目 | 描述 | 链接 |
|:---|:---|:---|
| Stable Diffusion | 开源 Latent Diffusion Model | [GitHub](https://github.com/Stability-AI/stablediffusion) |
| InstructPix2Pix | 官方实现 | [GitHub](https://github.com/timothybrooks/instruct-pix2pix) |
| Diffusers | Hugging Face 扩散模型库 | [GitHub](https://github.com/huggingface/diffusers) |
| ComfyUI | 节点式扩散模型工作流 | [GitHub](https://github.com/comfyanonymous/ComfyUI) |
| FLUX | Black Forest Labs 官方 | [GitHub](https://github.com/black-forest-labs/flux) |
| BrushNet | 官方实现 | [GitHub](https://github.com/TencentARC/BrushNet) |
| MasaCtrl | 官方实现 | [GitHub](https://github.com/TencentARC/MasaCtrl) |

### 14.3 数据集

| 数据集 | 规模 | 特点 | 链接 |
|:---|:---|:---|:---|
| MagicBrush | ~10K | 高质量手动标注 | [项目页](https://magicbrush.github.io/) |
| InstructPix2Pix Dataset | ~500K | 合成数据，GPT-3 + P2P | [HuggingFace](https://huggingface.co/datasets/timbrooks/instructpix2pix-clip-filtered) |
| UltraEdit | >1M | 大规模合成 | [HuggingFace](https://huggingface.co/datasets/) |
| SEED-Data-Edit | 大规模 | 系统性标注 | [项目页](https://github.com/) |
| EditEval | 评测集 | 多任务评测基准 | [项目页](https://github.com/) |

---

## 附录：DiT 编辑架构对比表

| 模型 | 年份 | Backbone | 参数量 | 注意力机制 | 条件注入 | 采样步数 | CFG | 核心特点 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| InstructPix2Pix | 2023 | U-Net | ~1B | Cross-Attention | Channel concat + Cross-Attn | 50 | 7.5 | 端到端指令编辑 |
| MGIE | 2024 | U-Net + MLLM | ~1B+7B | Cross-Attention | MLLM latent guidance | 50 | 7.5 | MLLM 增强指令 |
| Emu-Edit | 2024 | U-Net | ~1B | Cross-Attention | 多任务标签 + Cross-Attn | 50 | 7.5 | 多任务统一 |
| BrushNet | 2024 | U-Net + Branch | ~1B | Cross-Attention | 独立 Mask 分支 | 50 | 7.5 | 精确局部编辑 |
| FLUX.1-Fill | 2024 | Flow Matching | ~12B | Joint Attention | Mask channel concat | 4-50 | 无/可选 | Inpainting SOTA |
| Qwen-Image-Edit | 2024 | Flow Matching | ~3B | Joint Attention | Token concat | 50 | 4.0 | 中文优化 |
| FLUX.1-Kontext | 2025 | Flow Matching DiT | ~12B | Joint Attention | Token concat | 4-50 | 无/可选 | In-Context 编辑 |
| BAGEL | 2025 | DiT | ~3B | Joint Attention | Token concat | 20-50 | 可选 | 纯 Transformer 编辑 |
| OmniGen2 | 2025 | DiT | ~7B | Joint Attention | Token concat | 20-50 | 可选 | 统一生成+编辑 |
| Step1X-Edit | 2025 | DiT | ~3B | Joint Attention | Token concat | 10-20 | 可选 | 高效编辑 |
| Qwen-2511 | 2025 | Flow Matching DiT | ~5B | Joint Attention | Token concat | 40 | 优化 | 效率提升 |
| FireRed 1.1 | 2026 | Distilled DiT | ~2B | Joint Attention | Token concat | 4 | 无 | 超实时编辑 |
| FLUX 2 | 2025 | Rectified-Flow DiT | 9B | Joint Attention + KV Cache | Token concat | 4 | 无 | 旗舰统一模型 |

---

> **报告结语**：图像编辑技术正经历从"工具"到"助手"再到"代理"的深刻变革。DiT 统一架构解决了生成与编辑的 backbone 分裂问题，Agentic 编辑则赋予模型规划与推理能力。未来，随着实时性、物理一致性、安全性的进一步提升，图像编辑将成为人机协作创作的核心基础设施。

---

*报告完成日期：2026年6月6日*
