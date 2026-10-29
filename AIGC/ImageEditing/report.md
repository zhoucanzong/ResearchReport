---
display_name: 图像编辑与修复
---

# 图像编辑与修复：让目标变化与原图保留同时成立

> 图像编辑是一个受约束的生成问题：模型既要改变用户指定的内容，也要保留与指令无关的区域和属性。关键问题包括编辑任务形式、控制信号、源图保真、评测证据与开放边界；U-Net、DiT 或 MLLM 是可选的实现骨干，不代表编辑能力已统一。

跨媒介学习路线见 [AIGC 学习地图](../../docs/aigc-learning-path.md)；本篇重点解释图像编辑中“改动目标”和“输入保留”的权衡，不替代一般图像生成综述。

---

## 目录

1. [概述](#1-概述)
2. [发展时间线](#2-发展时间线)
3. [GAN 时代 (2016–2021)](#3-gan-时代-20162021)
4. [扩散模型早期编辑 (2021–2022)](#4-扩散模型早期编辑-20212022)
5. [指令驱动编辑 (2023)](#5-指令驱动编辑-2023)
6. [MLLM 增强编辑 (2024)](#6-mllm-增强编辑-2024)
7. [DiT 与统一多模态模型中的编辑 (2024–2025)](#7-dit-与统一多模态模型中的编辑20242025)
8. [方法论分类与对比](#8-方法论比较把训练方式和编辑接口分开)
9. [奖励优化与多步编辑](#9-奖励优化与多步编辑生成器评分不等于编辑目标)
10. [编辑机制综合](#10-研究主线编辑机制如何安排改动与保留)
11. [编辑评测](#11-评测编辑成功与源图保留分开报告)
12. [应用场景](#12-应用场景)
13. [挑战与开放问题](#13-挑战与开放问题)
14. [参考链接](#14-参考链接)

---

## 1. 概述

图像编辑要同时回答两个问题：**目标变化有没有发生**，以及**无关内容有没有保留**。如果背景被改成雪景，目标变化是天气/地面/光照按指令改变；若没有要求改变人物身份和服装，它们就属于需要保留的内容。只比较输出图像与源图，可能奖励“什么也没改”的失败结果；只比较编辑文本与生成图，又可能奖励“目标改对了但整张图都被重画”的结果。因此，编辑成功和源图保真必须分开观察。

| 评价轴 | 判断的问题 | 可用信号 | 常见误判 |
|---|---|---|---|
| 编辑成功 | 指令要求的对象、属性、动作或场景是否真的变化？ | 目标区域语义对齐、编辑前后差异、人工/多模态评审 | 整图 CLIP 相似度高，不代表细节编辑成功 |
| 编辑定位 | 变化是否出现在该改变的对象/区域？ | 显式 mask、物体/区域定位、region-aware judge | 文本相关度高，但改错对象或范围太大 |
| 非目标保真 | 未要求变化的区域和身份属性是否保持？ | mask 外像素/特征差异、区域/身份一致性 | 全图特征相似度可能被大面积背景主导 |
| 编辑自然度 | 边界、光照、纹理及整体结构是否协调？ | 局部/全局画质指标和人评 | 真实但不遵循指令，或符合指令但有拼接伪影 |

编辑任务还分为不同约束：SDEdit 从粗略 guide 出发，主要在真实性与忠实度间选噪声强度；DiffEdit/P2P 尝试不显式画 mask 也定位或保留结构；InstructPix2Pix 学习自然语言动作；inpainting 以 mask 直接给定修改区域；MLLM/多模态模型可先理解指令、参考图和场景，再由生成器执行。这里的训练范式与 backbone 不是同一分类轴：训练式、训练免方法都可运行在 U-Net 或 Transformer 上，统一多模态模型也不自动解决未编辑区域保真。

GAN 翻译、扩散编辑、指令模型、mask 修复、DiT 和 MLLM 分别回应不同任务约束。可先读第 3–7 节理解机制演进，再用第 8–11 节比较方法分类、改动/保留机制与评测，最后读第 13 节开放问题。U-Net→DiT 改变的是生成骨干；指令编辑、区域修复和源图保真仍需分别分析。多模态模型同时支持生成与编辑，也不意味着二者由同一架构自动解决。

---

## 2. 发展时间线

| 时间 | 代表工作 | 主要约束 | 机制路线 | 阅读重点 |
|---|---|---|---|---|
| 2016–2021 | Neural Style Transfer、pix2pix/CycleGAN | 指定外观或输入—输出域映射 | 特征优化、配对/非配对 GAN | 专用任务效果好；编辑范围由网络任务预先限定 |
| 2021 | SDEdit | 粗略 guide 如何变成逼真图像 | 对输入加噪到 $t_0$ 后按扩散先验去噪 | $t_0$ 控制真实性与 guide 忠实度的取舍 |
| 2022 | DiffEdit、Prompt-to-Prompt | 目标区域不明确、改词会让整图重采样 | 噪声预测差异生成 mask；共享 cross-attention 保持布局 | 自动定位和重用注意力并不等于保证局部编辑 |
| 2023 | InstructPix2Pix、MagicBrush | 自然语言指令及真实编辑数据稀缺 | 合成 instruction pair、人工标注基准 | 数据噪声/benchmark 偏差影响结果和保真评估 |
| 2023 | MasaCtrl、MGIE | 复杂非刚性变化、指令含混 | 源图 attention 交互；MLLM 生成更具表达力的指导 | 需要分别看内容变化和源图结构保留 |
| 2024 | BrushNet | mask 区域细节与目标外保留 | 双分支 mask 特征注入 | mask 提供边界，但不冻结最终输出的 mask 外像素 |
| 2025 | Qwen-Image-Edit、Step1X-Edit | 复杂指令、语义与外观控制 | 多模态理解条件 + 图像 diffusion decoder | 作者结果须限定到模型版本和 benchmark |
| 2025 | BAGEL、OmniGen2 | 多模态输入、复杂真实指令、多任务复用 | 统一预训练或理解器 + 生成 decoder | 编辑能力是统一模型的任务能力，不等于 edit-specific preservation 已解决 |
| 2023–2025 | EditVal、GEdit-Bench、BPM | 单一相似度分数不能同时衡量编辑与保留 | 分任务/区域的自动指标、人评校准 | benchmark 的标注器、judge 与目标图来源也有边界 |

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

**特点**：提出无需用户手动绘制 mask 的文本编辑路径；其自动定位仍依赖噪声预测差异，mask 边界与语义定位会影响编辑结果。

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

- **训练目标**：标准扩散噪声预测损失，条件包含源图像 latent 与文本指令；训练数据由 GPT-3 生成“输入图说明—编辑指令—目标图说明”，再由 Stable Diffusion / Prompt-to-Prompt 构造前后图像对并筛选。
- **推理**：模型分别对图像条件与文本条件使用 classifier-free guidance。图像 guidance 越强通常越保留源图，文本 guidance 越强则更强调指令；两者是两个可调轴，增大编辑强度可能损害源图结构，增强源图条件又可能令编辑不足。[原文 §3.1–3.2；InstructPix2Pix arXiv v2](https://arxiv.org/html/2211.09800v2)

#### 5.1.4 局限

- **局部编辑定位**：无显式 mask 时，模型需从自然语言推断该改哪里；改变一项全局语义可能波及编辑区域外的对象或布局。
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
| UltraEdit | 大规模合成编辑数据集 | 数据规模本身不构成 scaling law 证据；需看论文消融与评测条件 |
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
- **控制边界**：mask 提供明确的编辑区域，分支提取被遮挡图像特征并注入预训练扩散模型；这适合局部修复/替换，但 mask 外保真仍受采样、融合和解码影响，不能因有 mask 就视为严格不变。它研究的是带 mask 的 inpainting，不是直接解决无 mask 的自然语言编辑定位。[BrushNet §4–5](https://arxiv.org/html/2403.06976)

### 6.5 FLUX.1-Fill (2024)

Black Forest Labs 发布了 FLUX.1 Fill 作为 mask-based inpainting/outpainting 系统。公开页面介绍了其功能，但没有足够的完整技术报告支持这里写出精确的内部 mask 注入方式，或把它称为统一 SOTA；因此只把它作为可用模型路线记录，不由功能文案反推架构。

---

## 7. DiT 与统一多模态模型中的编辑（2024–2025）

### 7.1 骨干变化与编辑目标是两条不同的轴

U-Net 与 DiT 描述去噪网络的结构；编辑任务还要决定源图如何进入模型、哪些信息要改变、哪些信息要保持。把文本/图像 token 放入 joint attention 能增强跨模态交互，但不会自动提供编辑区域、不保证 mask 外像素不动，也不解决“指令成功但背景被改坏”的评价问题。反过来，基于 U-Net 的编辑模型也可以通过区域条件和注意力操作获得良好编辑效果。

因此，把 2025 以后直接称为“DiT 统一编辑时代”会混淆架构与任务。更准确的观察是：一批开放模型开始把 MLLM 理解、图像条件编码与 DiT/flow decoder 组合在同一系统中；同时，in-context 与训练免编辑仍然存在。统一的是输入/输出接口或模型服务能力，编辑成功与非目标保真仍须单独测试。

### 7.2 已公开模型路线：用模型结构解释条件分工

**Step1X-Edit** 将输入图像与自然语言编辑指令交给多模态理解组件，得到编辑语义 latent，再由扩散图像 decoder 合成目标图。其研究贡献还包括数据构造/筛选 pipeline 与 GEdit-Bench：这个 benchmark 以真实用户编辑请求为主，并分别报告编辑内容、感知质量及整体分数；作者报告的基线比较只适用于该版 benchmark、有效响应子集和所用 GPT-4.1/Qwen2.5-VL judge，不是独立人评的普遍排名。[原文 §3、§4.1–4.2；Step1X-Edit arXiv v1](https://arxiv.org/html/2504.17761v1)

**BAGEL** 不是专门训练的图像编辑 DiT。论文提出 unified multimodal pretraining，采用理解与生成专家分工的 Mixture-of-Transformers，共享多模态 self-attention；文本走自回归 next-token prediction，视觉 token 的生成采用 rectified flow。图像编辑是其统一预训练后的一个能力，论文在 GEdit-Bench 上评测编辑能力并讨论跨模态数据对其表现的作用。这个例子说明“统一模型能执行编辑任务”，但不能据此说图像编辑的控制/保真机制已收敛成一种架构。[原文 §2、§3、§7.3；BAGEL arXiv v3](https://arxiv.org/html/2505.14683v3)

**OmniGen2** 将多模态 LLM 的图像理解与 diffusion transformer decoder 分开设计，并把 MLLM 的条件 hidden states交给图像生成分支。作者明确将 source/target image 的局部坐标和 sequence/modality 标识纳入位置编码，鼓励对应位置保持一致；编辑数据还利用同场景视频帧对构造局部变化样本。它是一个具体的多模态 DiT 系统，不是“Joint Attention 天生解决保真”的证据；论文 limitations 仍需结合其数据生成协议与 benchmark 读。[原文 §2、§3.2–3.3、§4–6；OmniGen2 arXiv v1](https://arxiv.org/html/2506.18871v1)

**Qwen-Image-Edit** 是 2025 年发布的 Qwen-Image 编辑版本，不应放在 2024 时间线上。官方技术报告描述了一种语义/外观双路条件：输入图像同时进入 Qwen2.5-VL 以提供语义理解，并经 VAE encoder 保留视觉外观，再与 MMDiT 图像生成路径联合训练。作者加入 image-to-image reconstruction 等任务以对齐视觉语言条件与生成 latent。这个设计把“改什么”和“保留源图细节”交给不同条件路径，但效果仍受训练数据、编辑类型和评测协议制约。[原文 §2.1–2.4、§4；Qwen-Image Technical Report arXiv (2025)](https://arxiv.org/html/2508.02324)

**FLUX.1 Kontext** 的官方说明确认它接受文本与图像上下文进行 in-context generation/editing，但公开说明并未提供足以还原完整训练架构与采样器的技术细节。报告仅把它作为 in-context 编辑系统的能力例子，不把模型内部 tokenizer、精确 attention layout、参数量或产品采样步数从展示推断出来。[官方模型说明](https://bfl.ai/models/flux-kontext)

### 7.3 Mask 与 mask-free 是控制接口的选择

显式 mask 直接告诉模型“允许哪里变化”，适合局部替换、修补和扩展；它把区域定位交给用户/上游模型，mask 边界质量就成为重要条件。mask-free instruction editing 则让模型从指令与图像判断目标对象和区域，更易用，但目标定位不确定时可能误改邻近物体或全局风格。两者不是先后替代关系：有些工作允许 mask 可选，模型也可先由 MLLM/检测器推断区域，再交给局部生成器。

BrushNet 展示的是显式 mask inpainting 路线：把 masked image feature 与 noisy latent 分成两个支路，通过层级特征注入保留已知区域信息；其 benchmark 包含不同 mask 大小及 segmentation-based inpainting。结果支持特定 mask/inpainting设置下的质量和保真改进，不意味着它解决无 mask 指令定位，也不意味着所有 mask 外像素都被严格冻结。[BrushNet §3–5；arXiv 2403.06976](https://arxiv.org/html/2403.06976)

### 7.4 这些工作之间的关系

| 系统/方法 | 编辑信号怎么表示 | 哪部分专门处理“改什么” | 非目标保真依赖什么 |
|---|---|---|---|
| Prompt-to-Prompt | 目标文本 + 源/目标 cross-attention maps | token 对齐后替换、保留或重加权 cross-attention | 共享 token 的注意力图、相同噪声初始化和注入步数；注入太久会压制新指令 |
| InstructPix2Pix | 源图 latent + 编辑指令 token | 训练好的 conditional diffusion 从合成 instruction pairs 学动作 | 图像 CFG 与文本 CFG 的平衡；合成训练分布对真实编辑的覆盖 |
| MGIE | 图像/指令经 MLLM 生成 concise expressive instruction 与 latent imagination | 将短、含混命令转成更明确语义，扩散 decoder 执行编辑 | 源图条件及具体编辑目标；MLLM 改写可能遗漏或扩展原意 |
| BrushNet | masked image features + text condition | 显式 mask 指定 edit region | 双分支注入的已知区域特征、mask 准确度和融合过程 |
| Step1X-Edit / Qwen-Image-Edit | MLLM 语义条件 + 图像外观/latent 条件 | MLLM/条件 latent 与 diffusion decoder 协作 | 数据配对和外观路径；需分别报告语义编辑、视觉质量、非目标区保持 |
| BAGEL / OmniGen2 | 多模态交错输入和 unified/in-context conditions | 统一模型从预训练/任务微调中学习编辑行为 | 由特定数据和评测设定决定；统一模型本身不保证区域保持 |

表中方法同时跨越 backbone 和训练范式：Prompt-to-Prompt 是训练免 attention 操作，InstructPix2Pix/BrushNet 是训练式条件模型，MGIE/Step1X/Qwen 用 MLLM 增强指令和视觉条件。读论文时应追问每项控制信息是在哪层进入模型、有没有显式区域、评测有没有对非目标区域单独计分。

## 8. 方法论比较：把训练方式和编辑接口分开

“训练式 / test-time optimization / training-free”描述方法获得能力的途径；“instruction / mask / attention / reference image”描述编辑信号接口。它们是两个交叉轴，而非三类互斥模型。例如 Masked inpainting 既可使用训练好的专用模型，也可在采样时通过遮罩重用通用扩散先验；MGIE 的 MLLM 指令生成与 diffusion decoder 则分别承担理解和渲染。

| 轴 | 主要选项 | 代表机制 | 比较时要保留的边界 |
|---|---|---|---|
| 能力如何获得 | 专用数据训练、微调、推理期反演/优化、训练免采样操作 | InstructPix2Pix、MagicBrush fine-tuning、Imagic、Prompt-to-Prompt | 每图优化时间、训练分布与推理流程不同，不能只按模型名比质量 |
| 编辑信号 | 文本指令、source/target prompt、mask/region、参考图、结构图 | instruction diffusion、attention map reuse、masked inpainting、image prompt | 各输入对 edit success / preservation 的约束不同 |
| 修改范围 | 全局语义、软定位、硬 mask、逐像素编辑强度 | SDEdit、DiffEdit、BrushNet、Differential Diffusion | mask 或噪声强度决定允许的变化范围，但也可能限制真实结构变化 |
| 是否迭代执行 | 单次去噪、反演+编辑、多轮指令或工具链 | InstructPix2Pix、Null-text inversion、multi-turn MagicBrush | 多步编辑需测累计漂移、步骤依赖和是否保留早先目标 |

SDEdit 的噪声强度 $t_0$ 明确展示 realism–faithfulness trade-off：提高 $t_0$ 增强生成先验的重绘能力，同时降低对 guide 的忠实度；P2P 则固定随机种子、在若干去噪步替换/注入共享 token 的 cross-attention map，注入时间过长会锁住旧几何，阻碍新指令。两者都说明“编辑力度”和“保留输入”不是同一标量。[SDEdit §3.2–3.4；P2P §3](https://arxiv.org/html/2208.01626v1)

## 9. 奖励优化与多步编辑：生成器评分不等于编辑目标

### 9.1 生成偏好奖励与编辑奖励不是一回事

ImageReward 使用专家偏好比较训练文本到图像 reward model；DDPO 将扩散去噪链视为多步决策过程，并在论文中优化可计算的人类偏好代理目标（审美、可压缩性、VLM 提示对齐）。这为生成模型后训练提供了方法，但这些论文的主要实验不是图像编辑。若把奖励直接移植到编辑，只有“图片好看”或“目标文本相似”可能鼓励整图重绘；只有输入/输出相似又可能偏向不执行指令。将这些工作称为“编辑 RL 已解决”会把生成奖励与编辑任务目标混为一谈。[ImageReward §2–4；DDPO arXiv v4 §4–6](https://arxiv.org/html/2304.05977v4) / [DDPO arXiv v4 §4–6](https://arxiv.org/html/2305.13301v4)

编辑特定的奖励至少应拆开：目标内容是否被改到指定位置/区域、未编辑区域是否保留、编辑边界/全局画质是否自然、身份/文本等关键属性是否保持。每项奖励都依赖标注、mask、识别器或人评；奖励模型的定位和理解误差会继续传递到训练结果。ControlNet++ 的一致性反馈是空间条件一致性的一种训练反馈例子，但它用预训练条件提取器评估边缘/深度/分割等控制，适用范围受这些提取器和基准限制。

### 9.2 MLLM 理解、指令改写与 Agentic 流程需要区分

MGIE 的机制是让 MLLM 结合输入图和短指令生成更具体但精简的 expressive instruction，并生成视觉 latent guidance，再交给扩散编辑模型；它处理的是理解与表达桥接，不是自动多步编辑 agent。Step1X-Edit 等系统也把 MLLM 条件表示和图像 decoder 结合，但其单次编辑成功仍要由 benchmark 分项测量。

真正的多步编辑系统还要解决规划与执行间的状态传递：第一步的结果是否是第二步应当使用的源图？某步失败如何回滚？若后续步骤破坏了前面保留的属性，系统如何检测？把 LLM 生成 plan、mask 和多次 inpainting 串起来，可以形成有用的工具链，但不能直接推断某个图像生成骨干具备稳定的 reasoning 或错误恢复。现有研究需要分别公开计划成功率、单步编辑成功、非目标保真、累计多轮漂移与人工评审。

---

## 10. 研究主线：编辑机制如何安排“改动”与“保留”

| 路线 | 编辑信息从哪里来 | 如何限制无关变化 | 代表机制与未解决问题 |
|---|---|---|---|
| guide/noise based | 草图、低频图、输入图及文本 | 从输入图加噪再去噪，噪声时刻控制允许重绘幅度 | SDEdit 把真实性—忠实度显式呈为取舍；高噪声可重绘更多，也更容易偏离原图 |
| attention-based reuse | source/target prompt，源图 cross/self attention | 复用共享词语或局部区域的注意力/特征 | P2P 保持布局但可能锁住旧结构；MasaCtrl 取源图局部外观改善一致性，但目标的非刚性变化仍可能受源图特征约束 |
| learned instruction editing | 源图 + 自然语言操作 | 通过训练数据学习常见操作和变化范围 | InstructPix2Pix 方便单次指令但合成数据有 domain gap；MagicBrush 人工数据显示真实多轮编辑仍具挑战 |
| mask-aware inpainting | 源图、mask、文本 | 显式限定生成区域，并将已知图像特征送入去噪器 | BrushNet 分离 masked image features 与 noisy latent；mask 外保真还受融合、VAE、采样影响 |
| MLLM + image decoder | 图像理解、指令改写/解析、视觉 latent | MLLM 解释“要改什么”，decoder 实际渲染 | MGIE、Step1X、Qwen-Image-Edit 提升复杂指令处理，但理解正确不保证像素区间保真 |
| unified multimodal model | interleaved image/text/context | 通过统一预训练或多模态序列共同处理输入 | BAGEL、OmniGen2 展示编辑作为统一模型能力；其任务覆盖和 edit-specific 保真仍应按各自 benchmark 判断 |

这些方法回答的是不同问题。将编辑从 U-Net 迁移到 DiT，会改变 token 化、跨模态交互和计算路径；将单次编辑扩成 agent workflow，会增加指令解析、区域定位和步骤状态管理。二者都不自动提高“该变的变对了、其他部分保持不变”这一双重目标。模型参数、采样步数或“统一生成编辑”标签本身，不能证明编辑忠实度或源图保留。

## 11. 评测：编辑成功与源图保留分开报告

图像编辑的自动评测至少应回答四个问题：目标变化是否发生、变化是否定位正确、非目标内容是否保持、合成是否自然。用全图单一相似度很容易混淆这些目标：不改图可能看起来高度保真，整图重画则可能更像目标文本，却破坏未要求修改的人物、构图或背景。

| 评测轴 | 常见测量 | 主要局限 |
|---|---|---|
| 编辑语义成功 | CLIP-T、directional similarity、编辑专用 VLM judge、人类任务判断 | 全局文字相似度可能忽略改错对象、位置或编辑范围 |
| 编辑定位/范围 | 用户 mask、检测/分割得到的编辑区域、region-aware judge | 无 mask 时自动定位器本身有误差；编辑边界是软的 |
| 源图/非目标保留 | mask 外 L1/LPIPS/DINO/身份相似，或编辑相关/无关区域的分开评分 | 全图 CLIP-I/DINO 容易被大面积静态背景主导，不能证明未编辑区未变 |
| 目标区域自然度 | mask 内画质、边缘融合、局部纹理/光照与人评 | 只看目标区域可能漏掉与周围上下文不协调 |
| 人类综合判断 | 成对偏好或按维度打分 | 样本、评审者、问题措辞和任务分布会影响结论 |

**MagicBrush** 提供超过 10K 的人工标注编辑 turns，含 mask / mask-free 以及最多三轮的多轮编辑；不过源图来自 COCO，标注者借助 DALL-E 2 制作目标图，因此目标图并非每项编辑都由独立人工像素级绘制。benchmark 继承了标注工具和目标生成模型的偏好。它报告 L1/L2、CLIP-I、DINO、CLIP-T 等指标；mask 提供的设置会对 mask 内区域计算目标相似/文本指标，不能把这些数字笼统解释为全图未编辑区域保持度。[原文 §3.1–3.3、§4；MagicBrush arXiv v2](https://arxiv.org/html/2306.10012v2)

**EditVal** 对 13 类编辑做分项评估，并配合大规模人评；作者报告方法在不同编辑类型上排名不同，没有单一模型在所有任务都胜出，空间操作（如对象位置变化）尤其困难。这说明结果必须按任务类别展开。[原文摘要、§4–5；EditVal arXiv](https://arxiv.org/abs/2310.02426)

**GEdit-Bench** 用真实用户指令覆盖增删/替换对象、背景、颜色、材质、动作、文字等编辑任务。Step1X-Edit 报告的 G_SC（生成内容）、G_PQ（生成感知质量）和 G_O 等分数由 GPT-4.1/Qwen2.5-VL judge 评定，来自论文发布的数据划分和有效响应子集；它比合成短提示更贴近真实请求，但仍是自动 judge 分数，不等同于独立人类偏好或对 mask 外区域的直接像素检验。[Step1X-Edit §4.1–4.2、表 2](https://arxiv.org/html/2504.17761v1)

**BPM（Balancing Preservation and Modification）** 专门把图像拆成编辑相关区域与无关区域：Region-Aware Judge 检查目标区域位置/大小，Semantic-Aware Judge 分别测目标内容服从和非目标内容保留。作者在其基准上报告了与人类评审的较高对齐。这一方向正面回应了全图相似指标的盲区，但仍需关注编辑区域自动定位、judge 模型和人评数据覆盖带来的偏差。[BPM §3–4；ICML 2025](https://arxiv.org/html/2506.13827)

评测记录应包含：编辑类型、源图和目标/参考是否存在、mask 是否提供、是否多轮、目标区域与非目标区域各自使用的指标、自动 judge 版本或人评问题。跨 benchmark 的总分不宜拼接排名。

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

## 13. 挑战与开放问题

### 13.1 多目标如何联合建模与评价

高质量编辑需要目标区域发生足够变化，同时保持无关内容不变。训练数据中的 mask/目标图是否真实体现这个边界、奖励模型是否分别对两者负责，是架构之外的重要问题。BPM、GEdit-Bench 等工作开始把区域定位、指令内容与非目标保留拆开，但评测模型和区域提取仍会引入误差。

### 13.2 空间关系、数量和多对象编辑

“把红衣服改蓝”与“把左边的人移到右边、但保留另外两人”需要不同程度的空间推理。指令编辑器可能读懂语义，却定位错对象或意外重绘背景。未来数据与基准需包含对象级关系、数量变化、遮挡、局部/全局联动，并把成功与保留按对象和区域分别计分。

### 13.3 多轮编辑和状态保持

用户常在前次结果上继续修改。每一轮都可能累积颜色、纹理、身份或布局偏差；若模型每次重新从随机噪声生成，错误更容易叠加。需要研究来源状态如何被保留、目标修改如何继承、失败如何回滚，并在多轮 benchmark 上追踪身份和非目标区域漂移。

### 13.4 MLLM 与图像 decoder 的分工边界

MGIE 等系统让 MLLM 将短指令改写成视觉相关的明确条件；Step1X-Edit/Qwen-Image-Edit 等组合视觉理解与 diffusion decoder；BAGEL/OmniGen2 则探索统一多模态预训练。需要分别测指令解析、目标定位、图像合成和非目标保真，才能知道提升来自哪个模块。模型能解释一条编辑计划，不代表最终输出执行无误。

### 13.5 可复现性、偏差与安全

合成训练数据可能将上游生成器的偏差传给编辑器；人工编辑集也会继承标注工具和编辑者偏好。人脸、文本、品牌与敏感属性编辑还涉及身份冒用和来源标识。论文应报告数据来源、目标图生成/标注方法、编辑区域定义和 judge 设置，并将可编辑能力与可安全部署的结论分开。

## 14. 参考链接

### 14.1 关键原文与定位

| 论文 / 官方说明 | 原文定位 | 支撑的分析 |
|---|---|---|
| [SDEdit, arXiv](https://arxiv.org/html/2108.01073) | §3–5 | guide 加噪、反向去噪及真实性—忠实度取舍 |
| [DiffEdit, arXiv](https://arxiv.org/html/2210.11427) | §3–4 | 文本条件噪声预测差异如何生成编辑 mask |
| [Prompt-to-Prompt, arXiv v1](https://arxiv.org/html/2208.01626v1) | §3、图 6 | 共享 cross-attention 图保布局与新指令之间的权衡 |
| [InstructPix2Pix, arXiv v2](https://arxiv.org/html/2211.09800v2) | §3–5 | 合成 instruction pairs、双条件 CFG 与指令编辑边界 |
| [MagicBrush, arXiv v2](https://arxiv.org/html/2306.10012v2) | §3–4、表 2–3 | 手工标注多轮编辑数据与 mask / mask-free 评测设置 |
| [EditVal, arXiv](https://arxiv.org/abs/2310.02426) | 摘要、§4–5 | 13 类编辑、人评相关性及不同编辑类型的模型排序差异 |
| [MasaCtrl, ICCV 2023](https://openaccess.thecvf.com/content/ICCV2023/html/Cao_MasaCtrl_Tuning-Free_Mutual_Self-Attention_Control_for_Consistent_Image_Synthesis_ICCV_2023_paper.html) | 方法与实验 | mutual self-attention 重用源图外观、mask 引导减少前景/背景混淆 |
| [MGIE, arXiv v2](https://arxiv.org/html/2309.17102v2) | §3–4 | MLLM 生成 concise instruction 与视觉 latent guidance |
| [ImageReward / ReFL, arXiv v4](https://arxiv.org/html/2304.05977v4) | §2–4 | 通用 T2I 偏好奖励；不等同编辑区域/非目标保真奖励 |
| [DDPO, arXiv v4](https://arxiv.org/html/2305.13301v4) | §4–6 | 优化一般 T2I 下游奖励；非编辑专用 success/preservation 目标 |
| [BrushNet, arXiv](https://arxiv.org/html/2403.06976) | §4–5 | mask features 与 noisy latent 双支路的 inpainting 机制 |
| [ControlNet++, arXiv v2](https://arxiv.org/html/2404.07987v2) | §3–5 | 对输入结构条件做 cycle-consistency feedback |
| [BPM, arXiv](https://arxiv.org/html/2506.13827) | §3–4 | 分开评估编辑相关区域与非目标区域的区域/语义 judge |
| [Step1X-Edit, arXiv v1](https://arxiv.org/html/2504.17761v1) | §3–4、表 2 | MLLM 与 diffusion decoder 分工、GEdit-Bench 自动评测条件 |
| [BAGEL, arXiv v3](https://arxiv.org/html/2505.14683v3) | §2–3、§7.3 | unified multimodal pretraining 中的 MoT 结构与图像编辑结果 |
| [OmniGen2, arXiv v1](https://arxiv.org/html/2506.18871v1) | §2–5、§6 | MLLM 与 diffusion decoder 分支、图像编辑数据及限制 |
| [Qwen-Image Technical Report, arXiv](https://arxiv.org/html/2508.02324) | §2、§4 | Qwen-Image-Edit 的语义/外观条件与 I2I consistency training |
| [FLUX.1 Kontext, 官方模型说明](https://bfl.ai/models/flux-kontext) | 官方公开说明 | 可确认 text+image in-context editing 功能；未据此推断内部架构 |

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

### 14.3 数据集与基准

| 资源 | 主要内容 | 阅读时注意 |
|---|---|---|
| [MagicBrush](https://arxiv.org/html/2306.10012v2) | 真实源图、编辑指令和目标图；含多轮与 mask / mask-free 设置 | 目标图由标注者借助 DALL-E 2 编辑，benchmark 会继承工具和标注流程的偏好 |
| [InstructPix2Pix 数据](https://huggingface.co/datasets/timbrooks/instructpix2pix-clip-filtered) | GPT-3/Stable Diffusion 合成的指令编辑 pair | 规模大但存在合成数据与真实请求之间的 domain gap |
| [EditVal](https://arxiv.org/html/2310.02426) | 多种细粒度编辑属性和人工评估 | 论文发现结果按编辑类型而变，不能只看跨任务平均排名 |
| [GEdit-Bench](https://arxiv.org/html/2504.17761v1) | Step1X-Edit 构建的真实用户编辑指令评测 | G_SC/G_PQ 等结果采用模型 judge，并非直接人工评分 |
| [BPM evaluation](https://arxiv.org/html/2506.13827) | 区域相关/非相关内容及编辑语义的分层评测 | 区域定位与评审模型自身也需要验证 |

---
