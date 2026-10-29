---
display_name: 可控生成
---

# 可控生成（Controllable Generation）技术研究报告

> 研究领域：Diffusion Model / Controllable Image & Video Generation
> 核心问题：控制信号如何表示、注入，以及多条件怎样共同作用

跨媒介条件控制的阅读入口见 [AIGC 学习地图](../../docs/aigc-learning-path.md)；本专题聚焦空间图、参考内容和多路条件如何进入图像/视频生成器。

---

## 目录

1. [概述](#1-概述)
2. [发展时间线](#2-发展时间线)
3. [核心方法架构详解](#3-核心方法架构详解)
4. [控制信号与条件冲突](#4-控制信号如何进入模型何时会冲突)
5. [方法设计的跨论文比较](#5-方法设计的跨论文比较)
6. [控制信号进入 DiT / Flow Matching](#6-控制信号进入-dit--flow-matching)
7. [工具实现与研究边界](#7-工具实现与研究边界)
8. [挑战与开放问题](#8-挑战与开放问题)
9. [参考原文](#9-参考原文与工具)

---

## 1. 概述

“可控”不是一种单独的模型结构。不同工作向生成过程提供不同信号：文本说明语义，边缘/深度/姿态提供空间布局，参考图像提供外观或主体线索；LoRA 则通常修改模型参数以适应风格/概念，并不等同于推理时输入的结构条件。方法之间最关键的差异是：信号如何表达、注入到哪一层、哪些原模型权重被冻结、以及多个信号同时出现时是否有机制处理冲突。

路线围绕这些问题展开：从 ControlNet 的冻结主干与旁路残差，到 T2I-Adapter 的多尺度特征、IP-Adapter 的图像 cross-attention、LoRA 的参数偏移、Uni-ControlNet 的局部/全局分组，再到 ControlNet++ 的控制反馈与 DiT 上的 OminiControl。它们不是一条“外挂逐步被原生统一取代”的线性进化链；新骨干改变条件注入的接口，但并不自动解决空间对齐、条件冲突或输出是否服从条件的问题。

理解一个可控系统时，至少分开看：**条件可读性**（信号是否准确表达想要的内容）、**注入/学习机制**（模型能否从信号中抽取相应信息）、**输出忠实度**（结果是否跟随条件）、**非目标保持**（未要求改变的区域/属性是否保留）。控制权重调高，只是改变条件影响强度，并不等于解决了条件互相矛盾。建议先按第 3 节逐篇读懂控制模块，再用第 4–6 节比较条件接口、冲突和 DiT 迁移；第 7 节介绍常见工作流的实现边界。

---

## 2. 发展时间线

| 时间 | 代表工作 | 条件类型 / 方法变化 | 学习问题 |
|---|---|---|---|
| 2021 | LoRA | 对预训练参数加低秩偏移 | 如何以较少可训练参数适配任务/概念 |
| 2023.02 | ControlNet、T2I-Adapter | 边缘、深度、姿态等空间信号；旁路残差 vs 多尺度特征注入 | 怎样保持大型文本到图像主干，同时注入空间结构 |
| 2023.05 | Uni-ControlNet | 将多种局部控制与全局图像条件归为两类共享 adapter | 如何共享控制分支并提高局部/全局条件组合能力 |
| 2023.08 | IP-Adapter | 参考图经 CLIP 编码，单独 cross-attention 注入 | 怎样让图像条件与原文本条件并存 |
| 2023.11 | AnimateAnyone / ReferenceNet | 参考外观、姿态序列和时序模块分别处理 | 视频中如何拆分外观保持、动作控制和时间连续 |
| 2024.04 | ControlNet++ | 用生成后条件提取器形成一致性反馈 | 结构控制模型为何仍会偏离输入条件，如何再校准 |
| 2024.08 | ControlNeXt | 简化控制模块并提出 Cross Normalization | 如何减小控制支路训练/推理成本，兼顾图像与视频 |
| 2025 | OminiControl / OminiControl2 | 在 DiT 中重用视觉编码与 token 序列，并压缩/复用条件特征 | Transformer 条件控制的参数与长条件处理如何设计 |

---

## 3. 核心方法架构详解

### 3.1 ControlNet (2023.02, Zhang et al.)

ControlNet 是可控生成领域的重要工作，由 Lvmin Zhang 等人提出。它提出一种可复用的设计：冻结预训练扩散主干，在对应 block 建立可训练副本，通过零初始化卷积逐步注入空间条件残差。

#### 3.1.1 核心思想

ControlNet 的核心思想是：**冻结预训练主干，在需要接入条件的 block 旁建立对应的可训练副本，通过 zero convolution 将旁路残差逐步注入主网络**。Stable Diffusion 实例中，副本覆盖编码器与中间层；不能简化为“完整复制 U-Net 后只相加最终输出”。

这一设计的精妙之处在于：
- **训练初期**：zero convolution 的输出为零，副本残差不改变冻结主网络 block 的输出
- **训练后期**：旁路学习到条件控制信息，逐步影响主网络的生成过程
- **始终冻结主网络**：保留预训练模型的生成先验知识

零初始化的两个 1×1 卷积分别把条件写入副本输入，并把副本输出形成的残差接回主路径。训练初期该残差为零，之后才逐渐影响主干特征。这能降低直接微调产生遗忘的风险，但代价是训练/部署仍需运行相应的可训练副本。[原文 §3.1–3.2；ControlNet arXiv v3](https://arxiv.org/html/2302.05543v3)

#### 3.1.2 架构结构

```
输入：噪声 latent、文本 token、空间条件图
  ├─ 文本 ─→ 原文本编码器 ──────────────┐
  ├─ 噪声 latent ─→ 冻结主 U-Net block ─┼─→ 原去噪预测
  └─ 空间条件 ─→ 0 初始化投影 ─┐       │
                              ↓       │
       主干 block 的冻结副本接收隐特征 + 条件特征
                              ↓
              zero conv residual ────→ 加回主路径
```

控制信号的作用位置与主文本条件并不相同：文本经原有 cross-attention 提供语义，边缘/姿态/深度等条件由旁路特征逐层注入。论文还讨论把条件信号放入有条件分支、无条件分支或两者对 classifier-free guidance 的影响，因此“多条件相加”不应理解为有优先级的硬约束。[原文 §3.2、§3.4](https://arxiv.org/html/2302.05543v3)

#### 3.1.3 关键组件

**旁路 block**
- 结构：对选定主干 block 建立可训练副本；Stable Diffusion 实现对编码路径/中间层进行复制并以零卷积连接
- 输入：条件图（canny edge、depth map、normal map、human pose、semantic segmentation 等）
- 输出：多尺度特征图，通过 zero convolution 后加到主网络对应层

**Zero Convolution**
- 形式：1×1 卷积层
- 初始化：权重和偏置全部初始化为 0
- 作用：训练初期旁路输出为 0，不影响主网络；随着训练进行，逐步学习到非零权重

**连接方式**
- 旁路每个 block 的输出 → zero convolution → 与主网络对应 block 的输出相加（element-wise addition）
- 连接层级：通常在每个 ResNet block 之后、Attention 之前注入

#### 3.1.4 训练细节

- **可训练参数**：条件 embedding、ControlNet 的副本 block 和 zero convolution 层；原模型对应权重保持冻结
- **冻结参数**：预训练 U-Net 全部参数（包括 Encoder、Middle、Decoder、Attention）
- **训练数据**：条件图-目标图配对数据（如 canny edge → 原图、depth map → 原图）
- **损失函数**：与标准扩散模型相同，预测噪声的 MSE 损失
- **证据边界**：冻结主干可保留其预训练权重并限制遗忘，但不意味着训练成本或显存减半；实际开销取决于复制了哪些 block、模型版本和训练配置。

#### 3.1.5 条件类型支持

ControlNet 支持多种条件输入，每种条件训练独立的模型权重：

| 条件类型 | 输入形式 | 典型应用 |
|----------|----------|----------|
| Canny Edge | 边缘检测图 | 线稿上色、结构保持 |
| Depth (MiDaS) | 深度图 | 3D 感生成、空间布局 |
| Normal Map | 法线图 | 表面细节控制 |
| Human Pose (OpenPose) | 骨骼关键点图 | 人物姿态控制 |
| Semantic Segmentation | 语义分割图 | 场景布局控制 |
| HED Boundary | 软边缘图 | 更自然的边缘控制 |
| Scribble | 涂鸦/手绘 | 快速草图生成 |
| M-LSD | 直线检测 | 建筑/室内设计 |

#### 3.1.6 影响与局限

**影响**：
- 开源社区最广泛使用的可控生成工具
- 催生了 Stable Diffusion WebUI、ComfyUI 等工具链的 ControlNet 插件生态
- 成为后续所有可控生成工作的基准对比方法

**局限**：
- 可训练分支仍然较大；参数比例依采用的 U-Net 版本和复制范围而变
- 每种条件需要独立训练模型
- 多条件组合需要多个 ControlNet 并行，显存开销大
- 仅适用于 U-Net 架构，不直接适配 DiT

---

### 3.2 T2I-Adapter (2023, Tencent ARC Lab)

T2I-Adapter 由腾讯 ARC Lab 提出，研究问题是如何用小型 adapter 把条件图与预训练 T2I 模型已经学到的结构知识对齐；它减少额外参数，但不是不改变画面的“安全附件”。生成时，条件特征会直接改变 U-Net 多尺度中间表示，因此控制强度、条件质量和文本语义仍会相互影响。

#### 3.2.1 核心思想

T2I-Adapter 的核心思想是：**不复制整个 U-Net 编码器，而用小型卷积网络提取不同尺度的条件特征，并加到冻结 U-Net 对应的编码器特征上**。相较 ControlNet，它把更大的、与条件相关的去噪能力留给原主干；adapter 主要负责把外部条件编码成可被主干利用的特征。[原文 §3.2–3.4；T2I-Adapter arXiv v2](https://arxiv.org/html/2302.08453v2)

#### 3.2.2 架构结构

```
输入侧：
  条件图 (Condition Image, 如 canny/depth/pose)
       │
       ↓
  T2I-Adapter Network (四个特征提取块 + 多尺度下采样)
       │
       ├──→ 特征图 Level 1 (高分辨率) ──→ 注入 U-Net Encoder Block 1
       ├──→ 特征图 Level 2 (中分辨率) ──→ 注入 U-Net Encoder Block 2
       ├──→ 特征图 Level 3 (低分辨率) ──→ 注入 U-Net Encoder Block 3
       └──→ 特征图 Level 4 (最低分辨率) ──→ 注入 U-Net Middle Block

注入方式：
  U-Net Block 输入 = 原输入 + Adapter 特征图 (通过 1×1 conv 对齐通道数后相加)
```

#### 3.2.3 关键组件

**Adapter Network**
- 结构：4 个下采样卷积块（每个块包含 2-3 个卷积层 + ReLU）
- 参数量：原文报告约77M参数；若仅作77M/860M的算术比较约为9.0%，不是1%（分母需固定为对应SD U-Net）[T2I-Adapter v2 §1](https://arxiv.org/html/2302.08453v2)
- 输入：条件图（与目标图相同分辨率）
- 输出：4 个尺度的特征图

**特征注入**
- 通过简单的 1×1 卷积对齐通道数
- 与 U-Net 对应层输入相加
- 主干权重冻结不等于注入特征不会扰动输出；训练仍需通过去噪目标学习有效的控制特征。是否采用零初始化要看具体实现，不能由“从头训练”推出

#### 3.2.4 多 Adapter 组合

T2I-Adapter 的一个重要特性是**可组合性**：

```
多个条件同时控制：
  Canny Adapter ──→ 特征图 ──┐
  Depth Adapter ──→ 特征图 ──┼──→ 特征相加 ──→ 注入 U-Net
  Pose Adapter ───→ 特征图 ──┘
```

- 论文展示为不同结构/颜色条件分别训练 adapter，并研究多种 adapter 的组合。
- 多个特征可相加接入冻结 U-Net，但组合后的条件可能互相支持，也可能不一致；该加法本身不包含自动检测冲突或决定条件优先级的逻辑。
- 对照 Uni-ControlNet 的实验时要区分预训练的独立 adapter 直接组合，与联合训练的 adapter/fuser 组合；两种设置的结果不能混称“无需修改且总能组合”。[原文 §4.3](https://arxiv.org/html/2302.08453v2)

#### 3.2.5 与 ControlNet 对比

| 维度 | ControlNet | T2I-Adapter |
|------|------------|-------------|
| 比较点 | ControlNet | T2I-Adapter |
|---|---|---|
| 条件表征 | 空间条件图进入零初始化连接的可训练 block 副本 | 条件图编码为四尺度特征，与冻结 U-Net encoder 特征相加 |
| 可训练部分 | 复制的主干 block 与零卷积；冻结原模型 | 轻量卷积 adapter；冻结原模型 |
| 论文报告参数 | 取决于复制的底模和 block 范围 | adapter 约 77M 参数；相对占比须给出明确底模分母 |
| 多条件方式 | 多个已训练 ControlNet 的输出叠加 | 不同 adapter 特征组合；组合效果取决于条件及训练设定 |
| 主要设计取舍 | 表达力较大的深层旁路带来额外参数与计算 | 更小的特征对齐模块降低开销，但可控制的关系受其特征注入方式限制 |

---

### 3.3 IP-Adapter (2023, Tencent ARC Lab)

IP-Adapter（Image Prompt Adapter）同样由腾讯 ARC Lab 提出，解决的是与 ControlNet/T2I-Adapter 不同的控制问题：它从参考图像提取全局语义/外观提示，适合提供主体或风格线索；边缘、姿态等空间对齐关系仍主要由其他空间条件方法承担。它不承诺像素级复制人物或无冲突地服从所有其他条件。

#### 3.3.1 核心思想

IP-Adapter 的核心创新是**解耦 Cross-Attention（Decoupled Cross-Attention）**：

传统扩散模型的 Cross-Attention 只接收文本提示：
```
Attention(Q, K_text, V_text)  ← 文本条件
```

IP-Adapter 将其扩展为文本 + 图像双路径：
```
Attention(Q, K_text, V_text) + Attention(Q, K_image, V_image)  ← 文本 + 图像条件
```

#### 3.3.2 架构结构

```
图像提示路径：
  参考图像 (Reference Image)
       │
       ↓
  CLIP Image Encoder (冻结)
       │
       ↓
  全局图像 embedding
       │
       ↓
  Image Projection Network (可训练，映射为 N 个图像提示 token；论文设置 N=4)
       │
       ↓
  新增的图像 Cross-Attention 分支

文本提示路径（原有，冻结）：
  文本提示词 ──→ CLIP Text Encoder ──→ Text Embedding ──→ Cross-Attention

解耦 Cross-Attention 结构：
  Query: 来自 U-Net 特征图
  Key/Value_text: 来自文本 Embedding (原有，冻结)
  Key/Value_image: 来自图像 Projection Network (新增，可训练)
  
  Output = Softmax(Q·K_text^T / √d)·V_text + Softmax(Q·K_image^T / √d)·V_image
         = 文本 Cross-Attention 输出 + 图像 Cross-Attention 输出
```

#### 3.3.3 关键组件

**CLIP Image Encoder**
- 使用预训练 CLIP ViT-H/14 的图像编码器
- 提取全局图像 embedding
- **冻结**，不参与训练

**Image Projection Network**
- 结构：轻量级 MLP（2-3 层线性变换 + LayerNorm）
- 作用：将 CLIP 图像特征投影到与文本 embedding 相同维度
- 输出：论文设置为 4 个图像提示 token，由 projection network 从 CLIP 全局图像 embedding 映射得到；它们不是视觉 encoder 的局部 patch token

**解耦 Cross-Attention Layer**
- 在 U-Net 的每个 Cross-Attention 层中新增一个并行的图像 Cross-Attention
- 文本 Cross-Attention 保持原有权重冻结
- 图像 Cross-Attention 使用新的可训练权重
- 输出：文本 attention 输出 + 图像 attention 输出（相加）

#### 3.3.4 应用场景

| 场景 | 说明 | 效果 |
|------|------|------|
| 风格迁移 | 输入风格参考图，生成相同风格的新内容 | 风格一致性高 |
| 角色一致性 | 输入角色参考图，生成同一角色的不同姿态/场景 | 面部/服装一致性 |
| 概念学习 | 输入新概念参考图，生成包含该概念的图像 | 概念保持 |
| 图像变体 | 输入原图，生成结构相似但细节不同的变体 | 内容保持，风格变化 |

#### 3.3.5 与 ControlNet 的区别

| 维度 | ControlNet | IP-Adapter |
|------|------------|------------|
| 控制目标 | 空间结构（pose/depth/edge） | 风格/内容/角色 |
| 注入位置 | U-Net Encoder 各层 | Cross-Attention 层 |
| 条件输入 | 条件图（与生成图同分辨率） | 参考图像（任意分辨率） |
| 连接方式 | 特征图相加 | 解耦 Attention |
| 是否修改模型结构 | 旁路注入 | 新增 Attention 路径 |
| 可组合性 | 多 ControlNet 并行 | 与 ControlNet 可同时使用 |

---

### 3.4 LoRA / LyCORIS：权重适配不是一种空间条件

LoRA（Low-Rank Adaptation）最初是参数高效微调方法，不应与边缘图、深度图或参考图这样的推理时条件等同。它把训练得到的参数偏移压缩为低秩矩阵，适用于把底模适配到特定风格、人物或视觉域；除非配合额外输入/模型机制，LoRA 本身不表示“把目标姿态/布局作为输入并严格遵循”。它与 ControlNet、IP-Adapter 更常互补：一个改变模型参数，一个在推理时额外提供条件。

#### 3.4.1 核心思想

LoRA 的核心思想是：**在冻结预训练权重 W 的基础上，引入低秩矩阵 B 和 A 进行微调，使得 W' = W + BA**。

其中：
- W ∈ R^{d×k}：预训练权重矩阵（冻结）
- B ∈ R^{d×r}：可训练矩阵
- A ∈ R^{r×k}：可训练矩阵
- r ≪ min(d, k)：低秩约束（通常 r = 4, 8, 16, 32, 64, 128）

#### 3.4.2 架构结构

```
标准线性层：
  h = W · x

LoRA 适配后：
  h = W · x + (B · A) · x
      ↑           ↑
   冻结权重    可训练低秩矩阵
      │           │
      │           └── 参数量 = d×r + r×k = r×(d+k)
      │
      └── 参数量 = d×k

当 r ≪ d, k 时，可训练参数量远小于原权重参数量。
```

#### 3.4.3 在扩散模型中的应用

LoRA 通常应用于扩散模型的以下层：

| 目标层 | 可能影响的生成行为 | rank 设定 |
|--------|------|-----------|
| U-Net Cross-Attention Q/K/V 投影 | 可能改变文本/条件与视觉特征的关联 | 由底模、目标域和训练预算决定 |
| U-Net Self-Attention Q/K/V 投影 | 可能改变视觉 token 间的信息流 | 同上 |
| U-Net ResNet / 其他线性层 | 可能改变外观、纹理或领域特征 | 同上 |
| Text Encoder 线性层 | 可能改变文本表征与生成的对应关系 | 同上 |

#### 3.4.4 LyCORIS 扩展

LyCORIS（LoRA beYond Conventional methods, Other Rank adaptation Implementations for Stable diffusion）是 LoRA 的扩展框架，支持更多分解形式：

| 方法 | 公式 | 特点 |
|------|------|------|
| LoRA | W' = W + BA | 最基础，最广泛 |
| LoHa | W' = W + (B₁A₁) ⊙ (B₂A₂) | Hadamard 积，更低秩 |
| LoKr | W' = W + Kronecker 积分解 | 适合大矩阵 |
| DyLoRA | 动态 rank 选择 | 训练时自动选择最优 rank |
| Diag-OFT | 正交微调 | 保持权重正交性 |

#### 3.4.5 与 ControlNet 的本质区别

| 维度 | LoRA | ControlNet |
|---|---|---|
| 适配方式 | 将训练得到的低秩权重偏移加到选定层 | 冻结主干，旁路网络把输入条件转换为逐层残差 |
| 是否是推理时输入控制图 | 否；通常承载训练时学到的风格/概念/身份偏移 | 是；条件图在推理时输入 |
| 典型适用问题 | 底模向特定域或概念适配 | 用结构条件约束当前生成任务 |
| 可组合边界 | 多个权重偏移可能叠加或冲突，效果依训练组合 | 多条件旁路可合成，但输出残差不提供逻辑冲突消解 |
| 推理行为 | 权重可合并，具体开销依实现 | 要运行控制支路，额外计算依底模和控制配置 |

**关键区别**：LoRA 的输入信息主要体现在训练好的权重偏移中，不能把“加载了一个风格 LoRA”当成“模型读懂并遵循了空间控制图”。ControlNet 将条件图显式映射成去噪残差；两种方法的成功标准、训练数据和组合风险都不同。

---

### 3.5 Reference-Only / ReferenceNet (2023-2024)

Reference-Only 和 ReferenceNet 解决的是"参考图像特征如何有效注入生成过程"的问题，在角色一致性、风格一致性、视频生成等场景中至关重要。

#### 3.5.1 Reference-Only (社区方案)

**核心思想**：不训练任何新参数，通过 Attention 机制将参考图像的特征直接注入生成过程。

**实现方式**：
```
1. 将参考图像通过 U-Net Encoder 提取特征
2. 在生成过程中，将参考特征与生成特征进行 Attention 交互
3. 通常通过 Self-Attention 的扩展实现：
   - 将参考图像的 Key/Value 与生成图像的 Key/Value 拼接
   - 生成图像的 Query 同时 attend 到生成特征和参考特征
```

**特点**：
- 无需训练，即插即用
- 效果依赖预训练模型的先验知识
- 控制精度有限

#### 3.5.2 ReferenceNet：外观条件要与动作信号分工

AnimateAnyone 面向图像到视频角色动画，而不是一般 T2I 空间控制。它把参考图像的外观编码、姿态序列、视频时间连续拆成 ReferenceNet、Pose Guider、Temporal Layer 三条职责：ReferenceNet 通过 spatial attention 融入参考细节，Pose Guider 处理动作控制，Temporal Layer 建模帧间连续。该例说明“参考图”与“空间控制图”虽然都是图像输入，但表达的约束不同：前者主要保留人物外观，后者主要指定生成的几何布局/动作。[AnimateAnyone §3.2–3.3；arXiv v3](https://arxiv.org/html/2311.17117v3)

ReferenceNet 不是一个跨任务统一的通用插件，也不能仅凭名称就推出其身份保真效果。需看具体系统怎样将参考特征与去噪 latent 融合、Pose Guider 如何提供运动、Temporal Layer 的窗口和训练设置如何约束跨帧漂移；有关视频角色一致性的精读可在 [数字人与 Avatar 专题](../AvatarGen/report.md) 延伸阅读。

#### 3.5.3 与前述条件接口的关系

| 条件 | 代表性输入表示 | 解决的主要问题 | 不应默认推断 |
|---|---|---|---|
| 边缘/深度/分割/姿态 | 与目标画面对齐的空间图或关键点 | 约束几何、布局、轮廓或姿势 | 条件像素与目标一定一致，或模型会自行校正错误条件 |
| 参考图像 | 全局图像 embedding、参考特征图或参考 token | 提供外观、身份/风格的提示 | 精确复制局部像素、严格保持未提示区域 |
| 文本指令 | token embedding / cross-attention | 提供语义与属性说明 | 精确描述对象位置、数量和优先级 |
| LoRA 等权重适配 | 低秩权重偏移或模块参数 | 适配风格/域/概念先验 | 等价于显式的空间条件输入 |

---

### 3.6 多条件组合：并联并不等于化解冲突

推理时并联多个 ControlNet 是一种组合工程方式：各分支分别将条件图转成主干残差，最终相加。它避免为“姿态+边缘”专门训练一个新主干，但各支路通常独立学习；若条件本身不一致（例如姿态暗示手臂在前，深度图把该手臂放到后景），相加不会自动推理出哪个条件应该优先。手动调低某一支路权重能改变影响强度，却不是冲突消解器。[ControlNet §3.4](https://arxiv.org/html/2302.05543v3)

**Uni-ControlNet** 把条件分为两类，并据此只训练两个 adapter：local controls（边缘、姿态、深度、分割等空间对齐条件）进入多尺度局部路径；global control（论文示例为 CLIP 图像 embedding）通过全局图像条件路径参与生成。它的目标是让不同任务的控制可以组合，并减少每增加一种条件就新增整套支路的需求；论文实验只支持其测试的条件类型、组合和数据设置，不能概括为“任意条件数量都能无冲突统一”。[原文 §3.2–3.3、§4；Uni-ControlNet arXiv v3](https://arxiv.org/html/2305.16322v3)

**ControlNet++** 则针对另一件事：已有图像控制模型在输出端仍会偏离输入条件。它用预训练判别器从生成图中重新提取控制（例如分割、边缘或深度），对输入条件与重提取条件做 cycle-consistency 反馈，再用单步近似去噪降低反向传播穿过完整采样链的成本。它主要改进训练目标/反馈，不是新一代 U-Net 旁路结构；作者分别在分割 mIoU、线稿 SSIM 和深度 RMSE 的指定基准报告相对 ControlNet 的提升，不能由此推出所有控制种类都获得同等收益。原文也讨论某些控制类型的可用性限制。[原文 §3、§4、§5；ControlNet++ arXiv v2](https://arxiv.org/html/2404.07987v2)

**ControlNeXt** 面向图像和视频控制，以轻量控制模块与 Cross Normalization 替代部分旁路/Zero Convolution 设计。作者在所测模型和任务中报告可训练参数最多减少约 90%；幅度取决于比较配置，不能解释为固定参数占比或外推到所有视频 DiT。[原文 §3–4；ControlNeXt arXiv v3](https://arxiv.org/html/2408.06070v3)

## 4. 控制信号如何进入模型、何时会冲突

把方法只按模型名排列，会掩盖它们控制的对象不同。可以先问两件事：条件描述的是**什么**，以及模型在**哪一处**接收它。

| 条件 / 参数化 | 典型表示 | 注入位置 | 擅长控制 | 主要限制 |
|---|---|---|---|---|
| 语义提示 | 文本 token / embedding | 原模型 cross-attention、adaLN 或联合 token attention | 类别、属性、场景语义 | 多对象绑定、精确位置/数量/先后关系仍可能不稳 |
| 空间结构 | 边缘、深度、姿态、分割图 | ControlNet 残差、T2I-Adapter 多尺度特征 | 布局、轮廓、姿势等与像素对齐的内容 | 预处理误差会成为条件误差；空间图并不告诉模型纹理/语义 |
| 参考图像 | CLIP embedding、参考特征/token | IP-Adapter 独立 cross-attention，或 ReferenceNet 空间 attention | 外观、风格、主体线索 | 全局图像提示不等于精确身份锁定；与结构条件可能拉扯 |
| 参数适配 | LoRA / LyCORIS 权重偏移 | 选定的线性层/注意力/卷积层 | 训练域、风格或概念的适配 | 通常不是逐样本空间控制输入；不同 adapter 相加可能互相干扰 |

因此，“多条件”至少有三种含义：同时接入多个信号、在训练中让一个网络覆盖多类条件、以及推理时将多个控制结果组合。三者不等价。组合前应检查条件在语义、空间坐标、时间或对象层级上是否一致；冲突时更需要澄清目标或修改输入，而非假设网络会自动判断优先级。

注入位置也决定信息瓶颈：ControlNet/T2I-Adapter 提供多尺度局部特征，适合空间结构；IP-Adapter把图像特征放到额外 cross-attention 路径，适合与文本并存的参考提示；LoRA 改的是模型映射本身，提供的是任务/风格偏移。没有哪一种仅凭架构标签就能保证条件忠实度。条件强度（如 conditioning scale、CFG scale）、训练条件 dropout、预处理器和任务数据都会影响结果。[ControlNet §3.4；IP-Adapter §3.2–3.3；T2I-Adapter §3.2–3.4]

---

## 5. 方法设计的跨论文比较

### 5.1 核心方法综合对比表

| 工作 | 条件类型 | 注入/适配机制 | 主要设计取舍 |
|---|---|---|---|
| [ControlNet](https://arxiv.org/html/2302.05543v3) | 空间对齐条件图 | 冻结主干块的可训练副本、zero-conv residual | 条件解释能力强；副本增加训练和推理成本；并联输出不解决冲突 |
| [T2I-Adapter](https://arxiv.org/html/2302.08453v2) | 空间图、颜色布局等 | 四尺度 CNN 特征加到 U-Net encoder features | 额外网络更小；条件—主干知识对齐是核心学习目标 |
| [IP-Adapter](https://arxiv.org/html/2308.06721v1) | 参考图像 | 另加 image cross-attention，与 text cross-attention 解耦 | 文本和图像提示可并存；全局图像 embedding 不是像素级锁定 |
| [LoRA](https://arxiv.org/abs/2106.09685) / LyCORIS | 训练数据中体现的域/概念 | 低秩权重偏移 | 适合底模个性化；不等于逐样本结构条件 |
| [Uni-ControlNet](https://arxiv.org/html/2305.16322v3) | 多种 local controls + global image condition | 两个 adapter 分别承担局部与全局条件 | 共享条件类别减少逐条件复制；组合结论依其训练和测试设置 |
| [ControlNet++](https://arxiv.org/html/2404.07987v2) | 已有条件模型的输出 | 通过生成结果重提取条件，优化 cycle consistency | 直接监督输出控制忠实度；依赖预训练条件提取器覆盖目标条件 |
| [ControlNeXt](https://arxiv.org/html/2408.06070v3) | 图像/视频控制信号 | 精简控制模块、选择性训练及 Cross Normalization | 针对论文所测基座降低额外参数；不等于所有基座上的固定比例 |
| [OminiControl](https://openaccess.thecvf.com/content/ICCV2025/papers/Tan_OminiControl_Minimal_and_Universal_Control_for_Diffusion_Transformer_ICCV_2025_paper.pdf) / [OminiControl2](https://arxiv.org/html/2503.08280) | 对齐/非对齐图像条件 | DiT token 序列复用；后续用条件 token 压缩与缓存 | 针对指定 DiT 和多条件图像任务验证，不能视为“DiT 原生已解决控制” |

### 5.2 方法不是单一路线上的替代关系

这些工作分别回答不同问题，而非按发表年份互相替代：ControlNet/T2I-Adapter 对空间图条件编码；IP-Adapter 对图像语义提示与文本并存；LoRA 学习底模的参数偏移；ReferenceNet 让参考外观进入视频生成；Uni-ControlNet 共享局部/全局条件通路；ControlNet++ 用输出反馈检查输入条件是否落实；OminiControl 则探索将图像条件 token 直接纳入特定 DiT。一个工作可组合多种机制，单个系统是否“更可控”应按条件类型、目标区域和评测任务来判断。

### 5.3 条件注入接口对照

| 接口 | 信号流 | 通常在什么情况下更合适 | 需单独验证 |
|---|---|---|---|
| 特征残差注入 | condition encoder → 多尺度/逐层 residual → denoiser | 控制图与目标空间对齐、需要保留底模生成先验 | 残差权重、条件图误差与文本条件冲突 |
| 多尺度特征相加 | condition adapter → encoder feature maps | 轻量结构/颜色提示 | 多 adapter 简单相加是否仍保持每个条件 |
| 独立 cross-attention | 图像 prompt → image K/V，与 text K/V 分路 | 参考图提供外观/内容语义 | 能否保住身份细节、与空间条件如何组合 |
| 权重偏移 | LoRA / LyCORIS ΔW | 适配风格/概念/特定领域 | 多个权重偏移叠加后的退化与底模兼容 |
| 局部/全局条件分组 | local features 与 global tokens 两路 | 同时需要布局约束与整体参考 | 两种条件编码的作用范围是否清楚 |
| DiT 序列条件 | condition token 与 image token 联合建模 | token 对齐可定义，或 condition 可压缩/复用 | 序列长度、位置编码、不同模态间干扰 |

### 5.4 综合判断：先辨信号，再看注入，最后检查冲突

跨论文比较可归结为三个连续问题。第一，信号表达什么：边缘、深度、姿态和分割是带坐标的局部约束；参考图通常给全局外观或语义线索；LoRA 则改变底模对一类概念的参数化倾向。第二，信号在哪里进入生成器：ControlNet/T2I-Adapter 将空间信息变成多尺度特征，IP-Adapter 将参考图特征放入独立注意力路径，LoRA 修改权重，OminiControl 探索在 DiT token 序列中复用条件表示。注入位置决定模型能够读取什么信息，也决定额外计算与组合方式。

第三，条件冲突如何处理：大多数并联注入机制提供的是多路信息入口，并不自带语义优先级仲裁。Uni-ControlNet 的局部/全局分组有助于组织条件，ControlNet++ 的输出重提取反馈可检查特定条件是否落实，但都不能推出任意冲突已解决。实践上应先检查信号的坐标、目标对象和作用范围是否相容；冲突可见时，调整条件或任务定义，再分别评估各信号的遵循度与非目标保持。ComfyUI 等工具可把这些条件组合成可复查配置，属于实验与工作流载体；节点连接成功本身不是方法证据，详见第 7 节。

---

## 6. 控制信号进入 DiT / Flow Matching

### 6.1 骨干改变，不等于条件问题消失

DiT 把去噪 latent 切成 patch token，用 Transformer block 处理；U-Net 中“对齐分辨率的特征图相加”不再是唯一直接接口。条件可以变成额外 token、经 cross-attention 读取、调制 adaLN，或经小型条件 encoder 与主 token 交互。但 DiT 不会自动知道一张图是姿态、边缘还是身份参考，条件类型、坐标系和训练目标仍需由具体架构定义。

同样，Flow Matching 改变的是从噪声到数据的概率路径与模型预测参数化（例如学习速度场），不是一类独立的空间控制结构。文字/图像/姿态可以通过 token 或特征进入 vector-field 网络；控制忠实度仍取决于条件表示、模型注入和训练/反馈损失。因此不把“Flow-Control”当作一种已统一的、独立于架构的控制方法。[Rectified Flow §3；SD3 §2–4](https://arxiv.org/html/2403.03206)

### 6.2 DiT 条件注入的已公开实例

OminiControl 在 ICCV 2025 论文中研究图像条件如何进入预训练 DiT：它复用底模的 VAE encoder 与 transformer blocks，将条件 token 与图像 token 组成统一序列，并以动态位置索引区分空间对齐条件与主体/外观类非对齐条件。作者报告额外参数占比约 0.1%，但这对应 FLUX.1 基座、论文任务和实现设置。其意义是给出一种具体的 DiT 条件接口，不是证明所有 DiT 都能不经专门训练直接接受任意控制图。[原文 §2–4；OminiControl ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Tan_OminiControl_Minimal_and_Universal_Control_for_Diffusion_Transformer_ICCV_2025_paper.pdf)

OminiControl2 处理的则是条件输入较长时，token 数和跨 denoising steps 重复编码的开销：论文提出动态保留更有语义信息的条件 token，以及缓存/复用条件特征；作者在其多条件 image-conditioned 任务报告处理开销和推理速度改善。它是在具体 OminiControl/DiT 路线上对条件处理做效率优化，不是已解决不同模态冲突的通用“原生控制”。[原文 §3–4；OminiControl2 arXiv](https://arxiv.org/html/2503.08280)

ControlNeXt 是另一个对照：它研究轻量 control module、选择性训练主干层与 Cross Normalization，并在论文测试的图像/视频基座上评估。ControlNet++ 则把优化目标放在生成结果反提取出的边缘/深度/分割条件是否与输入一致。两者说明“条件架构怎么做”和“输出怎样反馈校正条件忠实度”是不同轴；参数更少不等同控制更准，DiT token 化也不自动带来控制一致性。[ControlNeXt §3–4；ControlNet++ §3–5](https://arxiv.org/html/2408.06070v3)

### 6.3 读 DiT 控制论文时保留的对照维度

| 维度 | 需要确认的问题 |
|---|---|
| 底模与任务 | 文生图、图生图、视频、主体一致性还是局部几何控制？基座及 VAE 是否相同？ |
| 条件表示 | 图像被编码成 feature map、patch token、全局 embedding 还是逐像素条件？是否保留坐标对应？ |
| 注入层级 | input concat、cross-attention、joint attention、adapter residual 或 adaLN 调制？ |
| 条件冲突 | 文本、主体参考、边缘/深度相互矛盾时如何训练、调权或评估？ |
| 评价目标 | 只报告画质，还是分开衡量文本遵循、条件一致、编辑强度和非目标区域保持？ |

目前公开证据覆盖的模型、条件和数据仍有限。对商业系统，如果未公开技术报告或固定源码，只能将其模型结构标为未知，不从产品控制面板或生成效果推断具体 attention、tokenizer 或训练路径。

---

## 7. 工具实现与研究边界

本节是机制主线之后的实现补充，不代表新的控制方法路线。ComfyUI、Diffusers 等工具把预处理器、控制分支和采样过程连成工作流，便于记录和试验条件组合；工作流“能连线运行”不等于组合后的约束一致，也不等于论文所声称的控制能力已被独立验证。理解方法时以第 3–6 节的论文机制与跨论文比较为主，工具材料用于看机制如何被组织成实验配置。

### 7.1 ComfyUI 中的可控生成节点

| 节点类别 | 在工作流中负责什么 | 研究解释时要分开的东西 |
|---|---|---|
| 条件预处理 | 从源图生成边缘、深度、关键点或分割图 | 预处理器预测错误会成为条件误差，不是去噪器本身的能力 |
| 空间条件模型 | 将结构图编码后注入 denoiser | 需观察目标条件是否满足、主体/风格是否仍合理 |
| 参考图 adapter | 把参考图编码为外观或语义提示 | 不能仅凭参考相似度推断细节完全保持 |
| LoRA/权重模块 | 改变底模在某个域或概念上的生成倾向 | 这属于参数适配，不是逐样本结构输入 |

### 7.2 典型工作流示例

一个常见组合是“文本 + 姿态/边缘 + 参考图”：文本提供语义，空间条件给位置/形状，IP-Adapter 提供参考外观，LoRA 调整风格先验。要判断这条工作流是否有效，需分别比较：去掉各条件后的输出、每个条件自己的遵循度，以及条件之间矛盾时哪一项被牺牲。节点图只是实验配置的可视化，不是条件正确性证据。

---

## 8. 挑战与开放问题

### 8.1 当前挑战

| 挑战 | 为什么难 | 如何验证进步 |
|---|---|---|
| 条件冲突 | 文本、参考外观、姿态/深度可能约束不同对象、坐标或尺度；叠加残差不定义逻辑优先级 | 构造冲突对照，报告每路条件分别遵循程度，并记录条件权重 |
| 条件输入噪声 | 控制图由估计器生成，误差会传到生成模型 | 对条件加噪、遮挡或替换预处理器，测控制忠实度对输入质量的敏感性 |
| 控制与非目标保持 | 强调条件可能改变未要求的区域；整体 CLIP 相关度掩盖局部偏差 | 同时报条件成功、编辑强度、非目标区域/身份保持与整体图像质量 |
| 模块开销 | 额外分支或多组 condition tokens 增加计算；减小模块又可能丢低层细节 | 在相同底模、条件集、分辨率和硬件上比较参数、延迟和条件保真 |
| 架构迁移 | U-Net feature maps 与 DiT tokens 的尺度和接口不同 | 对每种迁移方案说明底模、VAE、tokenizer、训练集和条件编码，不把个别成功推广成通用原生控制 |

### 8.2 开放问题

| 开放问题 | 需要回答的问题 | 现有证据边界 |
|---|---|---|
| 条件可靠度 | 条件抽取器的错误如何在图像里显现；模型何时应当拒绝不可信条件？ | ControlNet++ 在特定可提取条件上优化 cycle consistency，不能覆盖所有语义条件 |
| 组合泛化 | 一个模型在不同条件单独训练后，是否仍能处理未见组合？ | 多条件 benchmark 和训练/测试组合定义不统一，报告需分开 single-condition 与 compositional results |
| 局部控制与全局语义 | 如何保证空间条件不遮蔽文本对象属性，同时外观参考不覆盖姿态/布局？ | Uni-ControlNet 和 IP-Adapter 解决不同子问题，不存在由单一架构自动保证的优先级 |
| 跨骨干接口 | 不同 VAE/patch/token 表示如何复用控制信号？ | OminiControl 仅覆盖其论文的 DiT 与任务，尚未证明跨架构无损迁移 |
| 面向编辑的评测 | 如何分别评价目标变化是否成功、未编辑区域是否保持？ | 条件生成 benchmark 常以条件一致性为主，编辑/重建必须增加非目标保持指标 |

---

## 9. 参考原文与工具

### 9.1 核心论文

| 论文/报告 | 版本与定位 | 阅读重点 |
|---|---|---|
| [ControlNet](https://arxiv.org/html/2302.05543v3) | arXiv v3，§3.1–3.4 | 冻结网络块、zero-conv residual、CFG 与并联条件 |
| [T2I-Adapter](https://arxiv.org/html/2302.08453v2) | arXiv v2，§3.2–3.4、§4.3 | 多尺度条件特征对齐与多 adapter 组合 |
| [IP-Adapter](https://arxiv.org/html/2308.06721v1) | arXiv v1，§3.2–3.3 | 全局图像 embedding、投影 token、解耦 cross-attention |
| [LoRA](https://arxiv.org/abs/2106.09685) | arXiv (2021)，§4–5 | 低秩权重偏移及其作为参数适配而非空间输入条件 |
| [Uni-ControlNet](https://arxiv.org/html/2305.16322v3) | arXiv v3，§3–4 | local/global 控制分组及其组合消融 |
| [AnimateAnyone](https://arxiv.org/html/2311.17117v3) | arXiv v3，§3.2–3.3 | ReferenceNet、Pose Guider 和时间模块的职责拆分 |
| [ControlNet++](https://arxiv.org/html/2404.07987v2) | arXiv v2，§3–5 | 用输出条件重提取与一致性反馈训练 |
| [ControlNeXt](https://arxiv.org/html/2408.06070v3) | arXiv v3，§3–4 | 图像/视频控制模块、Cross Normalization 和指定设置下的效率 |
| [DiT](https://arxiv.org/html/2212.09748v2) | arXiv v2，§3–5 | ImageNet latent patch、adaLN 设计及测量到的 FLOPs/FID 关系 |
| [SD3 / Rectified Flow Transformer](https://arxiv.org/html/2403.03206) | arXiv HTML，§3–5 | Flow Matching 目标与多模态 transformer 表示 |
| [OminiControl](https://openaccess.thecvf.com/content/ICCV2025/papers/Tan_OminiControl_Minimal_and_Universal_Control_for_Diffusion_Transformer_ICCV_2025_paper.pdf) | ICCV 2025，方法与实验 | DiT 自身 VAE/Transformer 复用和图像条件 token 接入 |
| [OminiControl2](https://arxiv.org/html/2503.08280) | arXiv HTML，§3–4 | 长条件 token 压缩与跨采样步特征复用 |
| [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) | arXiv (2022)，§2–3 | 生成目标/路径参数化与条件注入是不同设计轴 |

### 9.2 开源项目与工具

| 项目 | 说明 | 链接 |
|------|------|------|
| ControlNet (官方实现) | ControlNet 原始实现 | https://github.com/lllyasviel/ControlNet |
| ControlNet-for-Diffusers | HuggingFace Diffusers 集成 | https://github.com/huggingface/diffusers |
| IP-Adapter (官方实现) | IP-Adapter 原始实现 | https://github.com/tencent-ailab/IP-Adapter |
| ComfyUI | 节点式工作流平台 | https://github.com/comfyanonymous/ComfyUI |
| Stable Diffusion WebUI (A1111) | 最早的 SD 图形界面 | https://github.com/AUTOMATIC1111/stable-diffusion-webui |
| sd-webui-controlnet | WebUI 的 ControlNet 插件 | https://github.com/Mikubill/sd-webui-controlnet |
| ComfyUI-Manager | ComfyUI 插件管理器 | https://github.com/ltdrdata/ComfyUI-Manager |
| ComfyUI-Advanced-ControlNet | ComfyUI 高级 ControlNet 节点 | https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet |
| CivitAI | 模型分享平台 | https://civitai.com/ |
| HuggingFace Diffusers | 扩散模型工具库 | https://github.com/huggingface/diffusers |

### 9.3 条件预处理工具

| 工具 | 功能 | 链接 |
|------|------|------|
| OpenPose | 人体姿态估计 | https://github.com/CMU-Perceptual-Computing-Lab/openpose |
| MiDaS | 单目深度估计 | https://github.com/isl-org/MiDaS |
| Canny Edge Detector | 边缘检测 | OpenCV 内置 |
| HED (Holistically-Nested Edge Detection) | 软边缘检测 | https://github.com/s9xie/hed |
| M-LSD | 直线段检测 | https://github.com/navervision/mlsd |
| Segment Anything (SAM) | 语义分割 | https://github.com/facebookresearch/segment-anything |
| Depth Anything | 更鲁棒的深度估计 | https://github.com/LiheYoung/Depth-Anything |
| DWPose | 改进的人体姿态估计 | https://github.com/IDEA-Research/DWPose |

### 9.4 综述与博客

| 资源 | 说明 | 链接 |
|------|------|------|
| ControlNet 论文解读 | 知乎/博客园多篇解读 | 搜索 "ControlNet 论文解读" |
| IP-Adapter 技术解析 | 腾讯 ARC Lab 官方博客 | https://arc.tencent.com/en/ai-demos/faceRestoration |
| ComfyUI 工作流教程 | 官方文档 | https://docs.comfy.org/ |
| Stable Diffusion 技术演进 | HuggingFace Blog | https://huggingface.co/blog |
| 扩散模型综述 | 多篇 arXiv 综述论文 | 搜索 "diffusion models survey" |
| 可控图像生成综述 | 中文综述 | 搜索 "可控图像生成综述" |

---

## 附录：术语表

| 术语 | 英文 | 解释 |
|------|------|------|
| 扩散模型 | Diffusion Model | 通过逐步去噪生成数据的生成模型 |
| U-Net | U-Net | 编码器-解码器结构的 CNN，带跳跃连接 |
| Transformer | Transformer | 基于 Self-Attention 的神经网络架构 |
| DiT | Diffusion Transformer | 使用 Transformer 作为骨干的扩散模型 |
| Flow Matching | Flow Matching | 直接学习数据分布间向量场的生成模型训练方法 |
| Cross-Attention | Cross-Attention | Query 来自一个序列，Key/Value 来自另一个序列的注意力机制 |
| Self-Attention | Self-Attention | Query/Key/Value 来自同一序列的注意力机制 |
| Zero Convolution | Zero Convolution | 权重初始化为 0 的 1×1 卷积层 |
| 低秩适配 | Low-Rank Adaptation (LoRA) | 使用低秩矩阵分解进行高效微调的方法 |
| 条件图 | Condition Image | 用于控制生成结果的结构化输入图像（如边缘图、深度图） |
| 文本嵌入 | Text Embedding | 文本经过编码器后的向量表示 |
| 图像嵌入 | Image Embedding | 图像经过编码器后的向量表示 |
| 分类器自由引导 | Classifier-Free Guidance (CFG) | 通过结合有条件和无条件预测来增强控制强度的技术 |
| AdaLN | Adaptive Layer Normalization | 根据条件动态调整 LayerNorm 参数的技术 |
| 旁路网络 | Side Network / Bypass Network | 与主网络并行运行的辅助网络 |
| 解耦注意力 | Decoupled Attention | 将不同类型的条件通过独立的 Attention 路径注入 |

---
