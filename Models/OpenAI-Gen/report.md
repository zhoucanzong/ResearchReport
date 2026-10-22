# OpenAI 生成模型系列研究报告

> **原报告日期**：2026年6月6日；**证据复核**：2026年10月23日
> **研究范围**：DALL-E → DALL-E 2 → DALL-E 3 → GPT-4o Image Generation / ChatGPT Images 2.x → Sora → Sora 2
> **核心主题**：架构演进 — 从自回归到扩散，再到原生图像能力与时空 diffusion Transformer

---

## 目录

1. [概述](#1-概述)
2. [发展时间线](#2-发展时间线)
3. [DALL-E](#3-dall-e-2021自回归图像生成)
4. [DALL-E 2](#4-dall-e-2-2022clip--扩散模型)
5. [DALL-E 3：caption 的证据](#5-dall-e-3-2023用详细-caption-改善提示遵循)
6. [OpenAI 图像生成系统的后续边界](#6-gpt-4o-image-generation-2025原生图像生成与未知实现)
7. [Sora 已披露的流程](#7-sora-2024已披露的表示与去噪流程)
8. [Sora 2 与产品状态](#8-sora-2-2025能力发布与产品状态)
9. [技术变量](#9-能比较与不能比较的技术变量)
10. [待补证问题](#10-仍需补证的研究问题)
11. [竞品证据要求](#11-与竞品比较的证据要求)
12. [局限与偏见](#12-局限性与来源偏见)
13. [来源索引](#13-参考链接)

---

## 1. 概述

OpenAI 的生成模型系列是过去五年多模态 AI 领域最具影响力的技术演进路线之一。从 2021 年 DALL-E 将图像生成重新定义为语言建模问题，到 2025 年 GPT-4o 将图像生成内嵌于统一多模态 LLM，OpenAI 的架构选择反映了生成式 AI 从**专用模型**走向**统一模型**的宏观趋势。

本报告系统梳理 OpenAI 生成模型的七代演进，重点关注：

- **模型结构**：dVAE、CLIP、扩散解码、caption 数据工程与时空 patches
- **范式转移**：图像与视频两条研究线，分别核对公开机制
- **工程洞察**：数据质量、条件注入、多模态统一

---

## 2. 发展时间线

| 时间 | 模型 | 核心架构 | 模态 | 关键突破 |
|------|------|----------|------|----------|
| 2021.01 | DALL-E | dVAE + GPT-3 自回归 Transformer | 文本 → 图像 | 首次将图像生成视为语言建模 |
| 2022.04 | DALL-E 2 | CLIP + GLIDE (扩散) | 文本 → 图像 | 抛弃自回归，引入扩散 + CLIP 语义空间 |
| 2023.09 | DALL-E 3 | 详细 caption 数据工程；完整实现未披露 | 文本 → 图像 | 专门训练 captioner 重标数据，见 §5 |
| 2024.02 | Sora | 时空 Patch + DiT (Diffusion Transformer) | 文本/图像 → 视频 | 首次实现高质量长视频生成 |
| 2025.03 | GPT-4o Image Gen | 原生图像能力；具体生成头未披露 | 文本/图像 → 图像 | 统一 LLM 内生图像生成，精确文本渲染 |
| 2025.09 | Sora 2 | 同步音视频；完整内部实现未披露 | 文本 → 视频+音频 | 同步音频、多镜头一致性 |
| 2026.04.26 | Sora 产品状态变更 | 非架构事件 | — | 官方公告后续注记产品不再可用，见 §8 |

> **注**：不同代次完整实现的披露程度不同。不得把前代论文架构未经证据继承给后代。

---

## 3. DALL-E (2021)：自回归图像生成

### 3.1 核心思想

DALL-E 的核心创新在于：**将图像生成重新定义为离散 token 的自回归预测问题**。这一思路直接继承了 GPT-3 在文本生成上的成功，试图证明 "Scaling Law" 不仅适用于语言，也适用于视觉。

### 3.2 架构详解

```
文本输入 → BPE Tokenizer → 文本 Token 序列
                                    ↓
图像输入 → dVAE Encoder → 32×32 离散图像 Token (8192 词表)
                                    ↓
                    ┌─────────────────────────────┐
                    │   GPT-3 风格自回归 Transformer  │
                    │  (64 层，稀疏注意力，~12B 参数) │
                    │                             │
                    │  输入：文本 token + 图像 token │
                    │  输出：自回归预测下一个 token   │
                    └─────────────────────────────┘
                                    ↓
                           dVAE Decoder
                                    ↓
                              256×256 图像
```

#### 3.2.1 dVAE (Discrete VAE)

| 组件 | 配置 |
|------|------|
| 输入分辨率 | 256 × 256 × 3 |
| 输出分辨率 | 32 × 32 × 1 (离散 token) |
| 词表大小 | 8192 |
| 压缩率 | 256×256 → 32×32，空间压缩 8×8 = 64 倍 |
| 通道 | 每像素 1 个离散索引 (logits 过 Gumbel-Softmax) |
| 训练目标 | 重建 + KL 散度 (向先验对齐) |

**关键设计**：dVAE 将连续像素空间映射到离散词表，使得图像和文本可以在同一自回归框架下统一处理。每个 32×32 位置上的 token 从 8192 个可能值中选择，总组合空间为 8192^(32×32)，足以覆盖自然图像分布。

#### 3.2.2 自回归生成过程

DALL-E 的生成严格遵循自回归范式：

1. 文本经过 BPE tokenizer 得到文本 token 序列
2. 图像经过 dVAE encoder 得到 32×32 = 1024 个图像 token
3. 将文本 token 与图像 token 拼接为统一序列
4. Transformer 自回归地预测序列中的下一个 token
5. 生成完成后，dVAE decoder 将 32×32 token 网格解码为 256×256 图像

**条件注入方式**：文本 token 与图像 token 在序列层面拼接，通过 causal attention mask 实现文本到图像的条件生成。没有显式的 cross-attention，条件信息完全通过 token 共现学习。

### 3.3 局限性与遗产

| 局限性 | 说明 |
|--------|------|
| 分辨率低 | 256×256，细节不足 |
| 生成速度慢 | 自回归需 1024 步顺序生成 |
| 组合与多样性 | 需由指定采样和评测实验判断，不能由自回归目标单独推出 mode collapse |
| 文本渲染差 | 离散 token 难以精确控制字符级细节 |

**历史意义**：DALL-E 证明了 "图像 = 语言" 这一范式在工程上的可行性，为后续统一多模态模型奠定了概念基础。但其自回归架构在图像质量上很快被扩散模型超越。

---

## 4. DALL-E 2 (2022)：CLIP + 扩散模型

### 4.1 范式转移

DALL-E 2 标志着 OpenAI 生成模型的**第一次架构范式转移**：从自回归彻底转向扩散模型。核心动机是扩散模型在图像质量、训练稳定性和条件控制上的显著优势。

### 4.2 架构详解

DALL-E 2 采用**两阶段生成架构**：

```
阶段一：先验模型 (Prior)

文本输入 → CLIP Text Encoder → 文本嵌入 (CLIP embedding)
                                    ↓
                         扩散模型先验 (Transformer 或 Diffusion)
                                    ↓
                         CLIP 图像嵌入 (Image Embedding)

阶段二：解码器 (Decoder)

CLIP 图像嵌入 → 投影 + 条件注入
                    ↓
            GLIDE 风格扩散解码器 (U-Net)
                    ↓
            64×64 基础图像 → 两个上采样扩散模型
                    ↓
              256×256 / 1024×1024 最终图像
```

#### 4.2.1 CLIP：语义桥梁

CLIP (Contrastive Language-Image Pre-training) 是 DALL-E 2 的基石。它将文本和图像映射到同一语义嵌入空间：

| 组件 | 配置 |
|------|------|
| 文本编码器 | Transformer；图像侧 ViT 名称标识 CLIP 配套版本，不能把整个 CLIP 参数量当文本编码器参数 |
| 图像编码器 | Vision Transformer (ViT) 或 ResNet |
| 嵌入维度 | 512 (ViT-B) / 768 (ViT-L) |
| 训练数据 | 4 亿图像-文本对 (WebImageText) |
| 训练目标 | 对比学习：最大化匹配对的余弦相似度 |

CLIP 的核心价值在于提供了**语义丰富的条件空间**。文本和图像不再通过离散 token 拼接，而是在连续的语义嵌入空间中交互。

#### 4.2.2 先验模型 (Prior)

先验模型负责将 CLIP 文本嵌入转换为 CLIP 图像嵌入：

- **原始方案**：自回归 Transformer (预测离散化的嵌入 token)
- **更优方案**：扩散模型 (直接在连续嵌入空间去噪)

扩散先验的优势：
- 连续空间操作，无需离散化
- 更好的多样性和采样灵活性
- 与解码器阶段保持生成范式一致

#### 4.2.3 解码器：GLIDE 风格扩散

解码器基于 GLIDE (Guided Language-to-Image Diffusion for Editing)，核心组件：

| 组件 | 说明 |
|------|------|
| 基础模型 | U-Net 架构的扩散模型，输出 64×64 |
| 条件注入 | CLIP **图像**嵌入投影后加入时间步嵌入，并投影为 4 个 context tokens；保留 GLIDE 文本条件路径 [论文 §2.1] |
| 上采样 | 两个级联扩散模型：64→256→1024 |
| 引导方式 | Classifier-Free Guidance (CFG) |
| 时间步 | ~1000 步扩散过程 |

**Classifier-Free Guidance (CFG)**：
[DALL-E 2 原论文](https://arxiv.org/abs/2204.06125) §2.1 分开描述 CLIP 图像嵌入与文本 caption 的条件丢弃；不同条件的比例不同，不能用一个“文本丢弃 10%”概括所有组件。推理时 CFG 可写为以下示意式：

```
ε_guided = ε_uncond + s · (ε_cond - ε_uncond)
```

其中 s 为 guidance scale (通常 3-10)，控制生成图像与文本提示的匹配程度。

### 4.3 关键创新

| 创新点 | 影响 |
|--------|------|
| 语义空间解耦 | CLIP 嵌入作为中间表示，实现文本-图像语义对齐 |
| 两阶段生成 | 先验 + 解码器分离，各自优化 |
| 扩散取代自回归 | 图像质量大幅提升，支持高分辨率 |
| CFG | 精确控制文本-图像一致性 |

### 4.4 局限

- **组合性不足**：复杂空间关系 (如 "一个红色立方体在蓝色球体左侧") 仍易出错
- **文本渲染**：扩散模型在精确字符生成上仍不稳定
- **计算成本**：两阶段 + 级联上采样，推理成本高

---

## 5. DALL-E 3 (2023)：用详细 caption 改善提示遵循

### 5.1 方法与可公开边界

[原论文 *Improving Image Generation with Better Captions*](https://cdn.openai.com/papers/dall-e-3.pdf) 用专门训练的图像描述模型为数据重新标注，再混合原始 caption 训练生成器。它没有证明描述器就是 GPT-4V，也没有披露完整产品实现；不能据 DALL-E 2 的论文把“CLIP prior + GLIDE decoder”整条架构继承给 DALL-E 3。

```text
图像 → 专门训练的图像描述器 → 详细合成 caption
     + 原始 caption 按采样概率混合
     → 文本条件图像扩散模型训练
```

GPT-4 的 prompt upsampling 是把用户/评测的简短提示扩写成详细文字（§3.4），与用图像描述器重标训练图像是不同阶段。两者都改善条件信息，但不能混称“用 GPT-4 Vision 重写全部训练 caption”。

### 5.2 受控实验与产品结果分开解释

| 对象 | 条件和结果 | 结论边界 |
|---|---|---|
| Caption 受控实验 | §3.2 在相同图像数据上训练相同的 T5-conditioned 模型，500,000 步、batch 2048；每个模型生成 50,000 张评测图像；§3.3–3.4 比较 caption 类型和混合比例 | 支持在该受控设定下详细合成 caption 改善提示遵循；累计 1B 是训练图像呈现次数，不能误读为 1B 个互异图像 |
| DALL-E 3 产品训练 | §4 使用 95% 合成、5% 原始 caption；模型是前面实验模型的放大版本且还有其他改进 | 脚注 5 明确说多项改进没有做消融，不能把产品相对 DALL-E 2 的收益全部归因于 caption |
| Drawbench short | 表 1：DALL-E 3 为 70.4%，DALL-E 2 为 49.0%，SDXL 为 46.9%，分数是 GPT-V 判定正确的图像比例 | DALL-E 2 是 2023-09-20 在用版本，SDXL v1.0 开启 Refiner；这是自动评判，不是人类偏好胜率 |
| 人评复查 | §4.2.1 发现 GPT-V 在计数类任务上表现接近随机，另做人工 Drawbench 评价 | 自动模型评判不能覆盖全部提示遵循能力；表 2 的 ELO 也不能直接解释为百分比 |

### 5.3 机制解释与反例

详细 caption 提供更多对象、属性和关系，缓解训练描述缺失导致的条件信号不足。但它也继承描述器的错误。论文 §5.1 指出左右、上下、前后等空间关系仍不可靠，§5.2 列出漏字与多字问题；T5 编码器的影响是作者提出的解释，不能当成已经隔离出的单一原因。

因此，这项工作支持“数据配对质量是重要变量”，不支持原稿的“数据质量大于模型复杂度”“架构不变即可解释整个代际收益”或“与 ChatGPT 共享文本编码器联合训练”。

## 6. GPT-4o Image Generation (2025)：原生图像生成与未知实现

[2025-03-25 官方发布](https://openai.com/index/introducing-4o-image-generation/) 描述原生图像生成、图文联合分布训练和后训练；展示文字渲染、基于上传图像的生成和多轮编辑。它没有给出图像 token 的具体离散/连续形式、扩散头、hidden states 条件注入或图像解码器内部结构。

原稿将“自回归框架 + LLM 内扩散头”写成既定结构，并据此画出逐 token 去噪伪代码，本次撤回该实现结论。产品原生多模态能力与某种内部训练目标之间不构成一一对应关系。

**失效边界**：同一发布页的 Limitations 包括裁剪、幻觉、密集对象的属性绑定、精确作图、多语言文字及编辑精度。这些是具体失败类别，不能把“可生成文字”扩大成“已解决文字渲染”。发布演示是作者选例，本次未进行独立固定提示集实验。

### 6.1 ChatGPT Images 2.0 / 2.5：系统能力有进展，底层生成架构仍未公开

OpenAI 的 [ChatGPT Images 2.0 System Card](https://deploymentsafety.openai.com/chatgpt-images-2-0/chatgpt-images-2-0.pdf)（2026-04-21）把 Thinking mode 描述为在图像生成流程中加入推理与工具调用，可整合实时网页搜索、一次提示生成多张图，并调用 reasoning stack。这说明产品系统能以工具与推理编排扩展生成工作流；它不等同于披露了图像模型的网络架构，也不能证明这些步骤是生成器内部的联合训练目标。

[Images 2.5 System Card](https://deploymentsafety.openai.com/chatgpt-images-2-5/safety-evaluations)（2026-09-08）称 GPT-Image-2.5-Sunburst 与 Flare 使用公开网络、第三方合作及用户/研究人员提供或生成的数据，并描述数据过滤和图像安全评测；没有公开生成器结构、训练配方或可复现的图像质量对照。发布页所称编辑一致性和延迟改善属于产品方描述，本报告不把它们写成已验证的架构进步。

因此，公开证据支持将 2.0 的 Thinking mode 视为**生成系统的推理/工具编排变化**，将 2.5 的模型内部机制继续标为未知。2.5 System Card 的对抗安全测试衡量的是安全栈拦截与残余风险，不是生成质量或模型能力的受控比较。

## 7. Sora (2024)：已披露的表示与去噪流程

[2024-02-15 技术说明](https://openai.com/index/video-generation-models-as-world-simulators/) 明确披露：压缩网络降低视频时空维度，再切成 spacetime patches；Transformer diffusion model 在这些表示上去噪，支持不同分辨率、时长、宽高比，且能联合训练图像和视频。其压缩网络的细节与变分训练目标未公开，不能自动把它指定成某个 3D VAE 配方。

```text
图像 / 视频 → 时空压缩表示 → spacetime patches
          → 文本条件 diffusion Transformer
          → 重建视频的解码网络
```

报告开篇直接声明不包含 model / implementation details。因此，原稿给出的 4×8×8 压缩比、C=16、T5/CLIP 编码器、AdaLN block、10–30B 参数和训练 GPU 小时均没有一手依据，已移除。用假设尺寸可以做容量估算，但必须将其单独作为假设算例，不能称为 Sora 实测配置；token 数也应按 patch 网格计算，而非乘上通道数。

技术说明报告可生成最长一分钟视频，这是研究模型的展示能力，不应把它移植成 Sora App 或 Sora 2 每个套餐的实际接口上限。页面展示计算量增加时样本质量改善，但没有给出可据此写出的通用 `FID ∝ −log(compute)` 视频标度公式。

**训练与评价边界**：页面确认使用图像/视频 captioner 及提示扩写，并展示可变尺寸训练、图像动画、延展和编辑；没有公开完整数据来源配比、训练阶段、位置编码和推理优化实现。定性呈现的三维一致性与物体持续性不是物理仿真精度证明；Discussion 明确指出玻璃破碎、食物状态变化与长片段一致性失败。

## 8. Sora 2 (2025)：能力发布与产品状态

[2025-09-30 官方公告](https://openai.com/index/sora-2/) 报告同步语音与音效、更复杂的多镜头控制及改进的物理表现；同时承认模型仍有大量错误。公告还介绍 iOS 社交应用，人物形象功能基于一次短视频和音频录制，不是仅“上传照片”即可等价得到的身份验证流程。

本次访问时该公告已加注：**自 2026-04-26 起 Sora 产品不再可用**。这是后续编辑加入的产品状态，不能伪装成 2025 年发布时的原句。原稿的“关闭后视频能力集成至 Runway、转向 B2B/API”未由所核官方材料支持，撤回该因果和集成结论。

音视频同步作为功能存在不等于公开了音频编码器或联合建模结构；不能从“方案 A/B/C 都可能”推定某一个实现。Sora 2024 的模型细节也不能未经材料确认整体继承给 Sora 2。

## 9. 能比较与不能比较的技术变量

| 模型 | 有原始材料支持的研究主线 | 不由该材料支持的推断 |
|---|---|---|
| DALL-E | 离散图像表示和自回归预测 | 自回归天然导致 mode collapse |
| DALL-E 2 | CLIP 图像嵌入先验与条件扩散解码 | 全部后继模型沿用相同 prior / decoder |
| DALL-E 3 | 图像描述重标、受控 caption 对照与产品评测 | 全部代际收益由 caption 引起、与 ChatGPT 权重共享 |
| GPT-4o image | 原生图文能力与交互式编辑 | 具体图像 token、扩散头或参数规模 |
| Sora 2024 | 时空压缩 patch 与 diffusion Transformer | 确切压缩率、注意力 block 和训练预算 |
| Sora 2 | 同步音视频和控制能力的发布 | 内部音频生成路径或已达物理模拟可靠性 |

图像和视频模型是并行研究线。Sora 2024 早于 GPT-4o image 2025，不能画成“GPT-4o 的混合架构继续演化为 Sora”的单一时间箭头；产品同属 OpenAI 也不能证明二者是同一权重。

## 10. 仍需补证的研究问题

1. DALL-E / DALL-E 2 的精确配置需要分别对应论文版本、组件参数和条件路径；不能把整个 CLIP 模型的参数记到文本编码器名下。
2. DALL-E 3 的 caption 受控对照需要进一步整理每组混合比例、CLIP-S 曲线与人工评价采样规则，避免只选总分支持预设结论。
3. Sora 的压缩器、位置编码、数据组成、训练预算和音频路径没有在上述材料中披露；这些是未知项，不能用通用 DiT 教程填成产品事实。
4. 后续跨模型比较需固定型号、日期、原始提示、是否扩写、随机种子、步数和评审方式；目前没有统一条件支撑跨产品星级排名。

## 11. 与竞品比较的证据要求

本次移除原稿未给样本集的星级表、跨版本混用的最长视频时长表，以及由未知架构推导的优劣排序。可以采用 DALL-E 3 论文的历史对照作为明确范围的例子，但不能将当时的 Midjourney 5.2 / SDXL 分数升级成 2026 年竞品结论。

比较 prompt following、审美、文字、计数和空间关系时应分别报告；DALL-E 3 论文的人评与自动评判存在差异，就是一个需要保留的反例。服务分发渠道、开放权重和模型生成质量也应分成独立维度。

## 12. 局限性与来源偏见

本报告以模型开发者论文、技术说明和公告为主要证据。本轮核读了 DALL-E 3 原文的 §1–§5 及关键表，Sora 的表示/条件/Discussion 章节，GPT-4o image 与 Sora 2 材料，以及 Images 2.0 / 2.5 System Card 的相关范围；没有运行图像、视频或人评复现实验。作者选例与自建评测存在来源偏向，涉及第三方的跨产品断言仍应独立复查。

不能由当前研究方向推导某年必然达到实时视频、统一 3D 或计算成本降低 10 倍；这些没有实验条件的数值预测不保留为技术结论。后续可验证的问题是：同一任务下，控制表示、数据质量和推理预算后，各因素如何改变提示遵循及失败分布。

---

## 13. 参考链接

本轮证据修订：2026-10-22。DALL-E 3 PDF 直接从官方 CDN 取回并提取正文，位于仓库外 `paper-cache/research-audit-2026-10-22/models/dalle3/`；DALL-E 2 用 `paper-fetcher download` 取回并核读 §2.1，位于相邻 `models/dalle2/`。其他实际阅读的一手来源已在相应段落给出。原始引用表不等同于每篇论文均已完整精读。

### 官方资源

| 资源 | 链接 |
|------|------|
| DALL-E 博客 (2021) | https://openai.com/research/dall-e |
| DALL-E 2 博客 (2022) | https://openai.com/research/dall-e-2 |
| DALL-E 3 论文/博客 (2023) | https://openai.com/research/dall-e-3 |
| Sora 技术报告 (2024) | https://openai.com/research/video-generation-models-as-world-simulators |
| GPT-4o 图像生成公告 (2025-03-25) | https://openai.com/index/introducing-4o-image-generation/ |
| Sora App 公告 (2025) | https://openai.com/sora |

### 关键论文

| 论文 | 作者 | 年份 | 链接 |
|------|------|------|------|
| Zero-Shot Text-to-Image Generation (DALL-E) | Ramesh et al. | 2021 | https://arxiv.org/abs/2102.12092 |
| Hierarchical Text-Conditional Image Generation (DALL-E 2) | Ramesh et al. | 2022 | https://arxiv.org/abs/2204.06125 |
| Improving Image Generation with Better Captions (DALL-E 3) | Betker et al. | 2023 | https://cdn.openai.com/papers/dall-e-3.pdf |
| Diffusion Models Beat GANs on Image Synthesis (ADM) | Dhariwal & Nichol | 2021 | https://arxiv.org/abs/2105.05233 |
| GLIDE: Towards Photorealistic Image Generation | Nichol et al. | 2022 | https://arxiv.org/abs/2112.10741 |
| Learning Transferable Visual Models From Natural Language Supervision (CLIP) | Radford et al. | 2021 | https://arxiv.org/abs/2103.00020 |
| Scalable Diffusion Models with Transformers (DiT) | Peebles & Xie | 2023 | https://arxiv.org/abs/2212.09748 |
| Flow Matching for Generative Modeling | Lipman et al. | 2023 | https://arxiv.org/abs/2210.02747 |
| Stable Diffusion 3 | Esser et al. | 2024 | https://arxiv.org/abs/2403.03206 |
| FLUX.1 技术报告 | Black Forest Labs | 2024 | https://blackforestlabs.ai/ |

### 竞品资源

| 资源 | 链接 |
|------|------|
| Midjourney | https://www.midjourney.com/ |
| FLUX.1 (Black Forest Labs) | https://blackforestlabs.ai/ |
| Stable Diffusion (Stability AI) | https://stability.ai/ |
| 可灵 (Kling) | https://klingai.com/ |
| Runway Gen-3 | https://runwayml.com/ |
| Pika | https://pika.art/ |
| Luma Dream Machine | https://lumalabs.ai/dream-machine |

### 分析与评论

| 资源 | 说明 |
|------|------|
| https://lilianweng.github.io/posts/2024-04-12-diffusion-video/ | Lilian Weng: 扩散模型与视频生成综述 |
| https://sora.com/ | Sora 官方平台 (已重定向) |
| https://platform.openai.com/docs/guides/images | OpenAI API 图像生成文档 |
| https://platform.openai.com/docs/guides/video | OpenAI API 视频生成文档 |

---

## 附录：术语表

| 术语 | 英文 | 解释 |
|------|------|------|
| 自回归 | Autoregressive | 按序列顺序逐个预测下一个元素 |
| 扩散模型 | Diffusion Model | 通过迭代去噪从随机噪声生成数据 |
| DiT | Diffusion Transformer | 基于 Transformer 的扩散模型 |
| dVAE | Discrete VAE | 输出离散 token 的变分自编码器 |
| VAE | Variational Autoencoder | 学习数据压缩表示的生成模型 |
| CLIP | Contrastive Language-Image Pre-training | 对比学习的图文对齐模型 |
| CFG | Classifier-Free Guidance | 无分类器引导，增强条件控制 |
| Cross-Attention | Cross-Attention | 一个序列对另一个序列的注意力机制 |
| AdaLN | Adaptive Layer Normalization | 根据条件动态调整归一化参数 |
| Patchify | Patchify | 将图像/视频切分为小块 (patch) |
| Flow Matching | Flow Matching | 直接学习概率路径的生成模型 |
| Scaling Law | Scaling Law | 模型性能随规模/计算可预测提升的规律 |
| 潜变量 | Latent Variable | 数据的压缩/隐含表示 |
| 去噪 | Denoising | 从含噪信号恢复干净信号 |
| 世界模型 | World Model | 可模拟环境动态的预测模型 |

---

> **报告完成日期**：2026年6月6日  
> **版本**：v1.0  
> **声明**：本报告基于公开信息、技术论文和社区分析整理。公开材料没有给出的实现保持未知，不以通用架构推演填补；本文仍有待补证问题，见 §10。
