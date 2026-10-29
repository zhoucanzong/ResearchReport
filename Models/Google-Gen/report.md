---
display_name: Google 生成模型
---

# Google / DeepMind 生成模型系列研究报告

> **范围**：比较 Google / DeepMind 公开论文中的图像与视频生成机制，并用官方产品资料补充论文未覆盖的产品线。Imagen、Phenaki、VideoPoet、Lumiere 有论文或技术报告；产品资料的公开粒度各异。Veo 3 模型卡只确认 latent diffusion 等高层信息，没有公开足以还原骨干网络、注意力布局或训练配方的细节。因此本文不把产品发布顺序写成一条已证实的架构演进链。

---

## 目录

1. [概述](#1-概述把研究路线和产品系列分开读)
2. [发展时间线](#2-发展时间线)
3. 模型架构详解
   - 3.1 [Imagen (2022)](#31-imagen-2022)
   - 3.2 [Imagen 2 (2023)](#32-imagen-2-2023)
   - 3.3 [Imagen 3 (2024)](#33-imagen-3-2024)
   - 3.4 [Phenaki / VideoPoet (2022-2023)](#34-phenaki--videopoet-2022-2023)
   - 3.5 [Lumiere (2024)](#35-lumiere-2024)
   - 3.6 [Veo 系列：公开机制到哪里为止](#36-veo-系列公开机制到哪里为止)
4. [架构演进对比](#4-架构演进对比)
5. [Veo 的证据边界与研究问题](#5-veo-的证据边界与研究问题)
6. [与其他研究路线比较时的边界](#6-与其他研究路线比较时的边界)
7. [开放问题：从公开材料缺口出发](#7-开放问题从公开材料缺口出发)
8. [参考链接](#8-参考链接)
9. [Vision Banana（2026-04）：把图像生成器当视觉骨干](#9-vision-banana2026-04把图像生成器当视觉骨干)
10. [Nano Banana 2.1（2026-10）：生成与编辑型号更新](#10-nano-banana-212026-10生成与编辑型号更新)

---

## 1. 概述：把研究路线和产品系列分开读

这组工作不是一条从 Imagen 自然“演进到 Veo”的单一架构谱系。图像生成论文 Imagen 展示级联扩散与强文本编码器如何配合；视频论文 Phenaki、VideoPoet 和 Lumiere 分别探索离散 token 自回归、多任务自回归、时空联合扩散。它们研究的问题和表示方式不同，适合比较设计选择，而不是拼成同一模型的代际。

Google 2024 年的 Veo 发布说明将其放在 GQN、DVD-GAN、Imagen-Video、Phenaki、WALT、VideoPoet、Lumiere 等既有研究积累之上。这支持“前序研究经验汇入产品线”，不代表公开了具体模块继承关系。Veo 3 模型卡把架构概括为 latent diffusion，并称扩散作用于时空视频 latent 与时间音频 latent；公开资料没有说明具体去噪骨干是否为 DiT，也没有披露注意力布局、tokenizer 或分阶段采样流程。本文因此以论文机制为分析主线，把 Veo 作为“产品资料能支持到哪里”的案例，不用常见实现替未公开细节补空。

推荐先读 Imagen 理解文本条件与级联生成，再对照 Phenaki / VideoPoet 的离散自回归路线和 Lumiere 的时空联合去噪；最后读 Veo 模型卡，观察产品资料给出的机制边界。图像生成方法的横向问题地图见[图像生成综述](../../AIGC/ImageGeneration/report.md)。

---

## 2. 发展时间线

| 时间 | 模型/产品 | 模态 | 核心架构 | 关键特性 |
|------|-----------|------|----------|----------|
| 2022.05 | **Imagen** | 图像 | 级联扩散 (Cascade Diffusion) | T5-XXL 文本编码器，64→256→1024 三级超分 |
| 2022.10 | **Phenaki** | 视频 | 自回归 Transformer (C-ViViT) | 文本/图像引导的长视频生成，可变长度 |
| 2023.05 | **Imagen 2** | 图像 | 产品发布；公开架构细节有限 | 文本渲染、编辑等产品能力更新 |
| 2023.12 | **VideoPoet** | 视频 | LLM 风格自回归 | 多任务统一：生成/编辑/风格化/音频 |
| 2024.01 | **Lumiere** | 视频 | 时空 U-Net (STUNet) | 一次生成完整视频，非逐帧拼接 |
| 2024.05 | **Imagen 3** | 图像 | 有官方技术报告；不以产品代际推断骨干变化 | 报告训练、评测与安全设计 |
| 2024.05 | **Veo** | 视频 | 产品发布；后续 Veo 3 模型卡披露 latent diffusion | 官方说明其建立在多条既有视频研究线上 |
| 2025.05 | **Veo 3** | 视频+音频 | 模型卡称 latent diffusion；骨干等细节未披露 | 同时生成视频与音频；细节见模型卡 |
| 2025.11 | **Nano Banana Pro**（Gemini 3 Pro Image） | 图像生成/编辑 | 未公开（产品级模型，无技术报告） | 2025-11-20 官方博客发布；本报告新增 §9：它被 Google 自己用作「生成即理解」的基座（Vision Banana） |
| 2026.04 | **Veo 3.1 Lite** | 视频+音频 | 官方模型卡称基于 Veo 3 | 产品变体信息不披露具体加速机制 |
| 2026.10 | **Nano Banana 2.1** | 图像生成/编辑 | Gemini 3.6 Flash 衍生型号；公开模型卡不披露生成图像的内部解码架构 | Thinking / No Thinking 分项评测，图像质量与限制见 §10；不能据此替换 Imagen / Veo 架构描述 |

> **注**：以上时间线基于公开论文、技术博客和产品发布信息整理。Google 部分模型的确切发布时间可能存在内部迭代与公开披露的时间差。

---

## 3. 模型架构详解

### 3.1 Imagen (2022)

Imagen 是 Google Research 于 2022 年提出的文本到图像生成模型，其核心创新在于**级联扩散架构（Cascade Diffusion）**和**文本编码器规模优先策略**。

#### 3.1.1 级联扩散架构

Imagen 采用三级级联 pipeline，逐步从低分辨率向高分辨率提升：

```
文本输入 → T5-XXL 编码 → [64x64 基础扩散] → [256x256 超分] → [1024x1024 超分] → 最终图像
```

**第一级：64×64 基础扩散模型**
- 基于 U-Net 架构的条件扩散模型
- 输入：T5-XXL 输出的文本嵌入（text embeddings）
- 输出：64×64 的噪声图像，经去噪后得到低分辨率图像
- 这是整个 pipeline 的"语义核心"，负责理解文本并生成对应的视觉内容

**第二级：64×64 → 256×256 超分扩散模型**
- 同样基于 U-Net 的条件扩散模型
- 输入：64×64 图像 + 文本嵌入
- 输出：256×256 高分辨率图像
- 负责在保持语义一致性的同时增加空间细节

**第三级：256×256 → 1024×1024 超分扩散模型**
- 最后一级超分，专注于纹理和边缘细节的精细化
- 输出 1024×1024 的最终图像

#### 3.1.2 文本编码器：T5-XXL

Imagen 最引人注目的设计选择是**使用 T5-XXL（约 4.6B 参数）作为文本编码器，且不冻结其参数，参与端到端训练**。

这一选择与同期模型形成鲜明对比：
- DALL·E 2 使用冻结的 CLIP 文本编码器
- Stable Diffusion 使用冻结的 CLIP 或 OpenCLIP

Google 在论文中提出了一个关键发现：**更大的文本编码器比更大的图像扩散模型对生成质量的提升更显著**。具体而言：
- 将文本编码器从 T5-XXL 降级到 T5-Large，即使保持图像模型规模不变，生成质量也会显著下降
- 反之，增大图像模型而保持文本编码器较小，收益相对有限

这一发现深刻影响了后续生成模型的设计方向，促使社区重新审视文本理解在视觉生成中的核心地位。

#### 3.1.3 关键技术与限制

**关键技术**：
- 动态阈值化（Dynamic Thresholding）：解决高分辨率扩散中的饱和问题
- 无分类器引导（Classifier-Free Guidance, CFG）：提升文本-图像对齐度
- 级联训练策略：各级模型独立训练，通过噪声条件化实现稳定级联

**限制**：
- 级联 pipeline 推理成本高，需要多次前向传播
- 文本渲染能力有限（后续 Imagen 2/3 重点改进）

---

### 3.2 Imagen 2 (2023)

Imagen 2 是 Imagen 的迭代版本，于 2023 年随 Google Cloud Vertex AI 发布。虽然 Google 未公开完整技术细节，但从产品特性和技术博客中可以推断其改进方向。

#### 3.2.1 已知改进

**图像质量提升**：
- 更好的细节保留和纹理生成
- 改进的光照和阴影处理
- 更自然的肤色和材质表现

**文本渲染能力**：
- 显著改进的文本生成能力（Imagen 的已知短板）
- 支持图像中的可读文本生成

**编辑能力扩展**：
- **Inpainting**：对图像局部区域进行重绘，保持上下文一致性
- **Outpainting**：扩展图像边界，生成超出原始画面的内容
- **Mask-based editing**：基于掩码的精细编辑

#### 3.2.2 公开信息的边界

Imagen 2 的产品资料可以说明发布场景和对外提供的图像生成、编辑能力，但不足以还原网络骨干、基础分辨率、文本编码器或条件注入方式。Imagen 论文中的架构不能自动外推到后续产品版本；本报告将 Imagen 2 作为产品演进记录，不把未披露实现写成架构结论。

---

### 3.3 Imagen 3 (2024)

Imagen 3 于 2024 年 5 月在 Google I/O 大会上发布，代表了 Google 图像生成技术的最新水平。

#### 3.3.1 核心改进

**视觉质量**：
- 显著改进的细节层次（fine-grained details）
- 更自然的光照模型和全局光照一致性
- 更合理的构图和透视关系
- 减少伪影和失真

**文本理解**：
- 更精确的复杂提示词理解
- 更好的属性绑定（attribute binding，如"一只红色的狗和蓝色的猫"）
- 支持更长的描述性文本

**产品集成**：
- 集成到 Gemini 多模态对话中
- Google Search 中的图像生成功能
- Google Workspace 中的创意工具

#### 3.3.2 可用的一手材料

Imagen 3 有 Google DeepMind 技术报告，适合据其方法、训练与评测章节讨论公开设计；不能依据行业趋势猜测未写出的骨干或文本编码器变化。报告摘要指出默认配置生成 1024×1024 图像并可接后续 2×、4×、8×上采样；这是该技术报告所述配置，不外推到所有 Imagen 产品部署。来源：[Imagen 3 技术报告](https://storage.googleapis.com/deepmind-media/imagen/imagen_3_tech_report_update_dec2024_v3.pdf)，§1 与后续方法章节。

---

### 3.4 Phenaki / VideoPoet (2022-2023)

在视频生成领域，Google 早期探索了**自回归（Autoregressive）**路线，与图像生成的扩散路线形成有趣的对照。Phenaki 和 VideoPoet 代表了这一方向的两个重要里程碑。

#### 3.4.1 Phenaki (2022)

Phenaki 是 Google Research 提出的**首个能够从文本生成可变长度视频**的模型。

**核心架构：C-ViViT (Causal ViViT)**

Phenaki 的视频生成 pipeline 包含以下关键组件：

```
文本输入 → 编码器 → 视频 Tokenizer (C-ViViT) → 自回归 Transformer → 视频解码
```

**C-ViViT 视频 Tokenizer**：
- 基于 ViViT（Video Vision Transformer）的因果变体
- 将输入视频编码为离散的时空 token 序列
- "因果"意味着 token 生成仅依赖于过去的 token，支持自回归生成
- 采用 3D CNN 或时空 patch embedding 提取视频特征

**自回归 Transformer**：
- 接收文本嵌入和已生成的视频 token
- 逐个预测下一个视频 token
- 支持双向条件：文本描述 + 关键帧图像

**关键特性**：
- **可变长度**：能够生成从几秒到数分钟的视频
- **双向引导**：支持文本 + 图像联合条件
- **计算效率**：自回归生成在推理时逐 token 进行，但训练相对高效

#### 3.4.2 VideoPoet (2023)

VideoPoet 是 Google Research 于 2023 年底提出的**多任务视频生成模型**，其最大特色是采用类似 LLM 的自回归框架统一多种视频任务。

**核心设计：LLM 风格的自回归视频生成**

VideoPoet 将视频生成重新框架为**语言建模问题**：
- 使用 tokenizer 将视频（和音频）转换为离散 token
- 使用自回归 Transformer（类似 LLM 的 decoder-only 架构）建模 token 序列
- 统一处理多种模态和任务

**多任务统一能力**：

| 任务类型 | 描述 |
|----------|------|
| 文本到视频 (T2V) | 从文本描述生成视频 |
| 图像到视频 (I2V) | 从静态图像生成动态视频 |
| 视频编辑 | 基于文本指令编辑已有视频 |
| 风格化 | 将视频转换为指定艺术风格 |
| 视频到音频 (V2A) | 为视频生成匹配的音频 |
| 视频修复/扩展 | 视频 inpainting 和 outpainting |

**架构特点**：
- **Decoder-only Transformer**：与 GPT 系列类似的纯解码器架构
- **多模态 token 统一**：视频、音频、文本统一表示为 token 序列
- **任务提示（Task Prompting）**：通过特殊 token 或前缀区分不同任务
- **自回归生成**：逐 token 生成视频和音频内容

**VideoPoet 的意义**：
- 证明了自回归框架在视频生成中的可行性
- 展示了多任务统一建模的潜力
- 为后续多模态 LLM（如 Gemini）的视频理解能力奠定了基础

---

### 3.5 Lumiere (2024)

Lumiere 是 Google Research 于 2024 年 1 月提出的文本到视频生成模型。其核心设计是用**时空 U-Net（STUNet）**让基础模型一次生成完整时间范围的低分辨率视频片段；高分辨率阶段仍使用窗口式空间超分。

#### 3.5.1 为什么把整段视频放进一个生成过程

Lumiere 针对一类常见方案提出问题：先生成稀疏关键帧，再用多个时间超分模型补帧。关键帧采样会丢掉快速运动信息，后续时间窗口的上下文有限，且超分模型训练时看到的真实帧与推理时生成帧之间存在分布差异。作者把这些视为全局时间一致性的限制。

其 Space-Time U-Net 同时在空间和时间维度下采样、上采样，并在紧凑时空表示中完成主要计算。基础模型直接生成完整时间范围、全帧率但低空间分辨率的视频片段；论文报告其设置为 80 帧、16fps，即约 5 秒。高分辨率输出再由空间超分模块处理重叠窗口，并使用 MultiDiffusion 融合窗口预测。因此，“整段一次生成”准确地说是基础生成阶段不采用关键帧加时间超分级联；高分辨率阶段仍有窗口处理。

#### 3.5.2 设计取舍与适用边界

这种设计把时间一致性问题放进基础模型：时间维度也参与压缩和特征计算，模型不必依赖多个局部时间超分模块事后补齐运动。代价是时空信号仍有显著计算与显存成本，因而作者在紧凑时空表征上处理主要计算，并将高分辨率空间超分拆到后续模块。

论文明确的边界是它不面向多镜头视频或镜头转场；作者将其列为开放挑战。更重要的是，这是一篇关于短片段生成机制的论文，不足以证明所有联合时空建模都优于级联生成，也不揭示 Veo 使用了同一设计。

来源：[Lumiere 原文](https://arxiv.org/abs/2401.12945)，摘要、§1、§3、§6；联合时空下采样与 80 帧/16fps 设置见摘要与 §1，窗口式空间超分和 MultiDiffusion 见 Fig. 3 与 §3，镜头边界见 §6。

### 3.6 Veo 系列：公开机制到哪里为止

Veo 是 Google DeepMind 的视频生成系统。Google 2024 年的发布说明把 Veo 建立在多条既有视频研究线上；这能支持研究积累与产品线有关联，却不能证明 Veo 直接继承某一篇论文的具体架构。

Veo 3 模型卡将其架构描述为 **latent diffusion**：扩散作用于时空视频 latent 与时间音频 latent；音视频数据由多个 Gemini 模型生成不同细节层级的字幕。Veo 3.1 Lite 模型卡称其基于 Veo 3。公开资料没有给出足以确认 DiT 的骨干结构、patch/token 方案、注意力分解方式或各代训练改动。产品页的分辨率、时长、音频等能力描述也不能推出实现它们的具体算子或模型拓扑。

因此，以下只把模型卡明确披露的 latent diffusion 和音视频 latent 作为高层事实。关于 Veo 1/2/3 的具体架构演进，除非对应版本的论文或技术报告直接说明，否则保持未知。

来源：Google DeepMind，[Veo 3 Model Card](https://storage.googleapis.com/deepmind-media/Model-Cards/Veo-3-Model-Card.pdf)（Architecture、Model Data）；[Veo 3 Tech Report](https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf)（安全与责任评估，不是架构技术报告）；[Google I/O 2024 发布说明](https://blog.google/innovation-and-ai/products/google-generative-ai-veo-imagen-3/)（Veo 的前序研究背景）。

#### 产品版本与研究问题

Veo 不同版本的公开发布信息可以帮助读者理解任务范围如何扩展，例如从文本/图像条件的视频生成扩展到音频输出和视频延展；但这些产品能力并不等于架构披露。Veo 3 模型卡给出的关键机制线索是 latent diffusion，并明确区分时空视频 latent 与时间音频 latent。它没有说明视频与音频是否使用共享骨干、如何对齐两路潜变量、使用何种去噪网络或采样方案。

这留下几个值得关注、但当前公开材料尚不能回答的问题：视频和音频的同步采用什么训练目标？输入图像如何影响后续帧？长片段扩展怎样避免身份与运动漂移？低延迟版本通过模型结构、采样步骤还是服务系统获得速度？这些问题需要技术论文、模型卡更新或可审读源码回答，不能仅凭产品名称或业界常见做法推断。

---

## 4. 架构演进对比

### 4.1 机制比较：表示、生成顺序与时间建模

| 工作 | 主要研究问题 | 视频/图像表示与生成方式 | 读者应关注的取舍 |
|---|---|---|---|
| Imagen | 怎样让文本描述更充分地进入图像生成？ | T5 文本表示条件化扩散；级联模型逐步提升空间分辨率 | 级联便于把低分辨率语义生成和高分辨率细节处理分开，但引入多阶段模型与误差传递 |
| Phenaki | 如何从开放域文本生成可变长视频？ | C-ViViT 将视频压为因果离散 token，再由 Transformer 自回归生成 | 可变长度与序列建模相容；视频 tokenizer 的压缩与重建质量成为关键瓶颈 |
| VideoPoet | 能否用统一的 token 生成器覆盖多类视频任务？ | 将文本、图像、视频、音频任务组织为 token 序列，以自回归 Transformer 建模 | 任务统一带来迁移与复用机会，也要求 token 设计和任务条件足以区分不同输入输出关系 |
| Lumiere | 如何在视频生成时直接建模整段的时空结构？ | 时空 U-Net 在视频 latent 上进行联合去噪，采用 Space-Time U-Net 处理时空特征 | 减少对关键帧后插值/拼接的依赖；联合处理高维时空体积带来计算与长度限制 |
| Veo 3 | 产品级视频与音频生成系统公开了哪些机制？ | 模型卡称 latent diffusion，涉及时空视频 latent 与时间音频 latent | 足以确认大类生成范式，不足以判断去噪骨干、模态融合方式和具体训练目标 |

表中论文描述依据各自原文；Veo 行只依据模型卡。产品能力和论文实验不是同一证据口径，不能把厂商展示与不同论文基准拼成统一性能排名。

### 4.2 研究路线：分叉而非单线收敛

    图像生成：Imagen 的文本条件级联扩散

    视频生成：
      离散 token 自回归：Phenaki → VideoPoet（可变长度 / 多任务建模）
      时空扩散：Lumiere（整段视频的联合时空去噪）
      产品系统：Veo（吸收多条既有研究积累；Veo 3 卡片确认 latent diffusion）

Google 将多项前序工作列作 Veo 的研究基础，说明这些成果构成组织内的研究积累。它不能证明 Veo 逐代从 Phenaki、VideoPoet 或 Lumiere 继承某个模块，也不能证明公司整体“最终选择”某一唯一范式。更准确的阅读方式是把这些路线当作针对不同瓶颈的并行探索：离散 token 关注序列化与多任务复用，时空扩散关注整段联合生成，产品模型卡则只透露有限的实现概貌。

### 4.3 为什么不能从“DiT 更可扩展”推断 Veo 采用 DiT

DiT 论文研究的是 Transformer 去噪骨干如何扩展；Lumiere 论文公开描述的是 Space-Time U-Net；Veo 3 模型卡只写 latent diffusion。三者可以作为架构问题的参照，却没有证据支持“Google 选择 DiT 的原因是 scaling law、多模态统一或全局注意力”，也没有证据支持 Veo 3 用 DiT。把一般架构优点说成特定模型的设计动机，会把文献综述变成猜测。

具体比较应回到论文能回答的问题：自回归模型的序列化能否保留足够运动信息；空间与时间分开或联合建模如何改变一致性；条件信号怎样进入去噪过程；输出时长、分辨率和任务覆盖如何影响成本。各论文的基准、任务与数据不同，结论应限定在各自实验中。

## 5. Veo 的证据边界与研究问题

Veo 是本报告中“产品资料不能替代架构论文”的案例。公开材料分工不同：Google DeepMind 的产品页面描述能力；Veo 3 Model Card 给出 latent diffusion、训练数据类别与已知限制；Veo 3 Tech Report 讨论安全责任评估、风险与缓解措施，其主体不是模型结构说明。

模型卡称 Veo 3 的训练数据包括音频、视频和图像；视频与音频数据由多个 Gemini 模型生成不同细节层级的文字字幕，并经过安全、质量、隐私处理及语义去重。这个信息让读者可以提出研究问题：字幕粒度会怎样影响提示遵循？音频与视频 latent 如何同步？图像条件如何约束动作连续性？长片段延展怎样保持主体和运动稳定？但公开卡片没有训练目标、损失分解或对应控制实验，不能据此给出机制结论。

Veo 3 模型卡也记录了限制和风险评估，例如模型生成文本能力不足、具有电影化镜头偏好，以及未指明人口属性时的表现分布偏差。这些限制适合用来理解生成质量与安全评测的边界；它们不能替代对用户任务中提示遵循、运动稳定或真实物理一致性的专门评测。

适合继续追问的方向包括：跨模态同步如何测量；输入图像与文本发生冲突时模型如何处理；长视频延展如何避免漂移；较快变体通过模型结构、采样步骤还是系统调度获得速度。当前材料能建立问题清单，但不足以回答内部实现。

## 6. 与其他研究路线比较时的边界

本报告不做 Google、OpenAI、快手或 Runway 的能力排行榜。不同产品公开的任务、分辨率、时长和评价方式并不一致；“物理一致性强”“中文场景更好”“生成质量领先”这类未附同条件实验的概括，不能作为研究结论。

若要做机制比较，建议从论文入手：将 Imagen 与其他文本到图像扩散工作比较文本编码、条件注入和级联策略；将 Phenaki / VideoPoet 与视频 tokenization、长序列建模工作比较离散表示和自回归生成；将 Lumiere 与时空扩散工作比较完整片段联合去噪与分段生成。Veo 可依据模型卡描述其公开机制和限制，但除非比较方也有同一协议下的可比资料，否则只做任务设定和证据类型的定性对照。

## 7. 开放问题：从公开材料缺口出发

1. **时空一致性如何测量？** Lumiere 通过空间与时间联合去噪改变生成过程，但“整段一起生成”并不自动保证物体身份、因果关系或长时运动正确。需要把短片段视觉质量与跨帧状态保持分开评测。
2. **视频 tokenization 的压缩边界在哪里？** Phenaki、VideoPoet 将视频变成离散序列，压缩率、重建损失和序列长度共同影响模型可学到的运动细节。理解这条路线需要同时看 tokenizer 和生成器，而不是只比较生成样例。
3. **联合音视频模型怎样实现同步？** Veo 3 模型卡确认视频与音频 latent 都参与 diffusion，但未披露共享表示、同步目标或音画错位评测。哪些机制真正保证语义与时间对齐仍是开放问题。
4. **长视频与高分辨率如何扩展？** 产品能力说明无法回答这类扩展依赖分段、层级生成、latent 压缩、采样加速还是服务侧拼接。需要公开架构与对照实验才能把产品能力归因到模型机制。
5. **生成模型何时表现出可迁移的视觉理解？** Vision Banana 将图像生成输出空间用于视觉任务，但它是独立论文研究线，不应与 Imagen/Veo 的产品代际混同。理解它需要比较任务输出编码、逆解码器及对生成能力的影响。

---

## 8. 参考链接

### 论文与技术报告

1. **Imagen** (2022)  
   Saharia et al., "Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding"  
   https://arxiv.org/abs/2205.11487

2. **Phenaki** (2022)  
   Villegas et al., "Phenaki: Variable Length Video Generation From Open Domain Textual Description"  
   https://arxiv.org/abs/2210.02399

3. **Imagen 3** (2024)
   Google DeepMind, *Imagen 3 Technical Report*, arXiv:2408.07009；方法、训练与评测见正文各节。
   https://arxiv.org/abs/2408.07009

4. **VideoPoet** (2023)  
   Kondratyuk et al., "VideoPoet: A Large Language Model for Zero-Shot Video Generation"  
   https://arxiv.org/abs/2312.14125

5. **Lumiere** (2024)  
   Bar-Tal et al., "Lumiere: A Space-Time Diffusion Model for Video Generation"  
   https://arxiv.org/abs/2401.12945

6. **DiT (Diffusion Transformer)** (2023)  
   Peebles & Xie, "Scalable Diffusion Models with Transformers"  
   https://arxiv.org/abs/2212.09748

7. **Veo 技术博客** (2024-2025)  
   Google DeepMind 官方博客  
   https://deepmind.google/technologies/veo/
8. **Veo 3 Model Card** (2025-05-23)
   Architecture 与 Model Data 小节用于本文对 latent diffusion 和数据处理的描述。
   https://storage.googleapis.com/deepmind-media/Model-Cards/Veo-3-Model-Card.pdf
9. **Veo 3 Tech Report** (2025)
   安全与责任评估材料，不是模型架构报告。
   https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf

### 产品页面与演示

8. **Google Veo 官方页面**  
   https://deepmind.google/technologies/veo/veo-3/

9. **Google Imagen 3 官方页面**  
   https://deepmind.google/technologies/imagen-3/

10. **Google AI Studio / Vertex AI**  
    https://aistudio.google.com/  
    https://cloud.google.com/vertex-ai

11. **Nano Banana 2.1 Model Card**（Google DeepMind，2026-10-06；2026-10-23 核查）
    https://deepmind.google/models/model-cards/nano-banana-2-1/
12. **Google DeepMind Model Cards**（2026-10-23 核查；用于确认当前公开 Veo / Imagen 型号目录）
    https://deepmind.google/models/model-cards/

13. **Adobe Firefly + Veo 集成**
    https://www.adobe.com/products/firefly.html

### 相关综述与分析

12. **Google I/O 2024 生成 AI 发布汇总**  
    https://blog.google/technology/ai/google-io-2024-keynote-sundar-pichai/

13. **Google I/O 2025 生成 AI 发布汇总**  
    https://blog.google/technology/ai/google-io-2025-keynote-sundar-pichai/

14. **Video Generation Survey (2024)**  
    视频生成领域综述论文（建议搜索最新版本）

---

## 9. Vision Banana（2026-04）：把图像生成器当视觉骨干

> 本节为**增量新增**（2026-10-17），只写一手可核验内容；逐项数字、逐表条件、失效边界与未确证清单见专册 [`papers/2604.20329-vision-banana.md`](papers/2604.20329-vision-banana.md)。主等级 `[精读原文]`（arXiv:2604.20329 **v3**，2026-06-03）。

### 9.1 它是什么

**Vision Banana** 是 Google 把自家图像生成/编辑模型 **Nano Banana Pro（NBP）** 拿来做**视觉理解**的产物：在 NBP 的原训练混合里**以极低比例**掺入少量视觉任务数据做 instruction-tuning，得到**一套权重**的单一模型；任务只靠 prompt 切换。关键设计是把**视觉任务的输出空间参数化为 RGB 图像**，再对每种任务配一个"轻薄"的逆解码器：

| 任务 | 模型生成什么 | 怎么变回可打分的量 |
| :-- | :-- | :-- |
| 语义分割 | 按"类→颜色"映射上色的整幅图（含图中不存在的类） | 每像素取 RGB 最近的目标色 → mIoU |
| 实例分割 | 只给目标类 + 背景色，模型自己给每个实例分配不同颜色 | 多阶段连通域聚类（τ=14、16-连通、面积 2×10⁻⁴、3×3 腐蚀、γ=5.0） → cgF1 |
| 指代分割 | 按指代描述上色的 mask | 最近色/阈值 → cIoU / gIoU |
| 度量深度 | 一张与米制**严格双射**的假彩色深度图 | 投影到 RGB 立方体棱 + 反 power transform（λ=−3、c=10/3） → δ₁ / AbsRel |
| 表面法向 | camera-space 单位向量直写 R/G/B | 逐通道反解 → 平均角度误差 |

### 9.2 关键数字（**必须带条件**，否则不可引）

| 能力 | 基准（口径） | Vision Banana | 论文认定的最强对手 | 引用时必须带走的前提 |
| :-- | :-- | --: | --: | :-- |
| 语义分割 | Cityscapes val（mIoU） | 69.9 | 65.2（SAM 3，零样本） | 零样本、开放词表、19 类全量颜色映射；闭集 SegMan-L 84.2 仍远高 |
| 指代分割 | RefCOCOg UMD val（cIoU） | 73.8 | 73.4（SAM 3 Agent） | **+0.4 属边际**；对手也接了 Gemini 2.5 Pro |
| 指代分割 | ReasonSeg val（gIoU） | 79.3 | 77.0（SAM 3 + Gemini 2.5 Pro） | 查询经 **Gemini 2.5 Pro 转写**，管线贡献未分离 |
| 实例分割 | SA-Co/Gold（cgF1） | 47.5 | 24.6（OWLv2，零样本） | **存在性判定外包给 Gemini 3.1 Flash-Lite**；**输给**训练内 SAM 3 的 54.1 |
| 度量深度 | 6 数据集平均（δ₁） | 0.882 | 0.918（DA3，仅 4 集） | 平均值分母不同不可横比；NYU 0.948 / KITTI 0.915 / nuScenes 0.643 **均落后专家** |
| 表面法向 | 室内 3 集平均（mean°） | 15.549 | 16.558（Lotus-2） | 室外 VKitti 29.063° **略差于** Lotus-2 28.894° |
| 生成保持 | GenAI-Bench / ImgEdit（对基座胜率） | 53.5% / 47.8% | 46.5% / 52.2%（NBP） | 人评，**无评审人数/样本量/置信区间**；编辑侧字面 −2.2 点 |

### 9.3 与本报告既有内容的关系（三点，均为"关系"而非"校正"）

1. **不是本生成谱系的"下一代"，而是生成模型用于理解的另一项研究**。本文比较 Imagen 级联扩散、Lumiere 时空 U-Net 等公开机制，并将 Veo 3 限定为 latent diffusion 的模型卡描述；Vision Banana 不引入上述模型的代际关系，也不能被写成 Imagen/Veo 的后继。
2. **它补上了本报告一个长期缺口：Nano Banana Pro 此前完全没有条目**。NBP 是产品级模型（2025-11-20 官方博客发布），Google 至今没有为它发布技术报告，论文正文也只以 "Nano Banana Pro" 指称它、**未披露参数量/架构/训练细节**。本报告据此**不推测**其架构；"它属 Gemini 3 Pro 图像侧"这一归属的证据来自官方博客而非论文正文（另见 `Models/Gemini/report.md` 的一行指向）。
3. **它连接生成与理解，但不是产品架构披露**。Vision Banana 将图像生成输出空间用于视觉任务；这与第 7 节提出的“生成器何时能支持视觉理解”问题相连，但不能据此推断 Imagen 或 Nano Banana 产品内部使用相同训练设计。

### 9.4 本条目视角下的引用注意

- **不要**把 Vision Banana 写进"Google 生成模型代际演进"叙事（它不是 Imagen/Veo 的后续版本，也不是新架构）。
- **不要**把"平均 δ₁ 0.882 最好"外推成"逐数据集超过 Depth Anything 3"——论文自己的表里 NYU 与 KITTI 两列是输的；**不要**把 SA-Co/Gold 的 47.5 说成"超过 SAM 3"（训练内 SAM 3 是 54.1，论文正文写明 "we still lag behind"）。
- **可以**引用的是方法论观察：① 生成目标对多模态输出歧义的处理优于判别式回归（与附录 C 的定性观察一致）；② 保留原训练混合的低比例掺数据，是"理解对齐但不遗忘生成"的可行做法（**幅度不可引**，人评协议未披露）。
- 成本侧只有一句定性（"显著高于跑轻量专门模型"），**没有任何延迟/算力数字**，因此"生成器可替代轻量专家"的成本论不被本文支持。

### 9.5 导航与一手来源

- **逐篇精读（本报告新增分册）**：[`papers/2604.20329-vision-banana.md`](papers/2604.20329-vision-banana.md)（423 行 / 30.2k 字符；七问速答、带条件对照表、失效边界 12 条、引用注意、未确证清单）。
- 一手来源：arXiv 正文 **v3**（<https://arxiv.org/abs/2604.20329>）、项目页 <https://vision-banana.github.io/>、官方博客 <https://blog.google/innovation-and-ai/products/nano-banana-pro/>（2025-11-20）。
- **未确证项**（不在本节展开）：NBP 的架构与参数、instruction-tuning 的数据比例/步数/分辨率、人评协议、网页抓取图与 COCO 系基准的图像级重叠是否被排除。

---

## 附录：术语表

| 术语 | 英文 | 解释 |
|------|------|------|
| 级联扩散 | Cascade Diffusion | 多级扩散模型串联，逐步提升分辨率 |
| 扩散模型 | Diffusion Model | 通过逐步去噪生成数据的生成模型 |
| DiT | Diffusion Transformer | 使用 Transformer 替代 U-Net 的扩散模型 |
| 自回归 | Autoregressive | 逐 token 顺序生成的模型范式 |
| 时空注意力 | Spatio-Temporal Attention | 同时在空间和时间维度上执行的注意力机制 |
| STUNet | Spatio-Temporal U-Net | 时空联合的 U-Net 架构 |
| Tokenizer | Tokenizer | 将连续数据（图像/视频/音频）编码为离散 token 的模型 |
| 超分 | Super-Resolution | 从低分辨率图像/视频生成高分辨率版本 |
| 无分类器引导 | Classifier-Free Guidance (CFG) | 通过条件/无条件联合采样提升生成质量的技术 |
| 流匹配 | Flow Matching | 一种改进的生成模型训练框架，与扩散相关 |
| 因果注意力 | Causal Attention | 仅关注过去位置的自注意力变体 |
| 世界模型 | World Model | 能够模拟环境动态并预测未来的模型 |

---

本报告对未披露的产品实现保留未知，不以行业常见做法补写其架构。产品页和模型卡用于说明公开能力与限制，论文结论则限定在原文实验条件内。

---

## 10. Nano Banana 2.1（2026-10）：生成与编辑型号更新

Google DeepMind 于 2026-10-06 发布 Nano Banana 2.1 模型卡。卡片将其描述为 **Gemini 3.6 Flash 的衍生型号**，支持文本和图像输入，图像及文本输出；模型卡列出最高 1M 输入上下文。该归属是目前可确认的公开模型依赖关系，但卡片没有给出图像生成模块的具体网络结构、参数量、扩散/自回归机制或独立训练数据配方，因此不能把它的实现细节写成 Imagen 4 或 Veo 系列的架构证据。

评测分 Thinking / No Thinking 两种设置，分别报告文本生成图像与图像编辑能力。模型卡使用成对人评 Elo 比较总体偏好、信息图设计和编辑能力，并以自动评分器评估信息图事实性；这些测试是 Google 公布的内部评测结果，模型卡没有提供独立复现。卡片指出的限制包括小字与长段落渲染、输入输出人物一致性、编辑指令遵循、姿态保留、左右定位以及高级世界知识、3D 推理和事实性。

对本报告架构主线的影响有限：Nano Banana 2.1 扩展了 Gemini 派生图像生成与编辑的产品支线，但公开资料尚不足以解释其图像生成器如何构造、与 Imagen 4 有何模块关系，或是否继承 Vision Banana 论文的训练设计。Vision Banana（§9）是另一项研究工作，不能由相似命名推断为 Nano Banana 2.1 的实现说明。

一手来源：[Nano Banana 2.1 模型卡](https://deepmind.google/models/model-cards/nano-banana-2-1/)，[Google DeepMind 模型卡目录](https://deepmind.google/models/model-cards/)，核查日期：2026-10-23。目录截至本次核对仍列 Veo 3（2026-01-13 更新）与 Veo 3.1 Lite（2026-04-08 更新）为该谱系的当前公开型号；这仅表示目录中可查到的模型卡范围，不证明其内部不存在未披露研发型号。
