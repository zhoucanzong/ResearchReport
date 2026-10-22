# Hunyuan系列模型深度调研报告

> 对腾讯（Tencent）混元（Hunyuan）大模型家族——基座语言、图像生成、视频生成、3D生成、多模态理解与音频/世界模型——的技术路线、架构演进与开源生态的系统性梳理。所有结论均基于已公开的论文、技术报告和官方仓库。

---

## 目录

- [1. 概述与时间线](#1-概述与时间线)
- [2. 基座语言模型演进：Hunyuan-LLM → Hunyuan-Large → A13B → TurboS → T1](#2-基座语言模型演进hunyuan-llm--hunyuan-large--a13b--turbos--t1)
- [3. 图像生成模型：Hunyuan-DiT 系列与 HunyuanImage](#3-图像生成模型hunyuan-dit-系列与-hunyuanimage)
- [4. 视频生成模型：HunyuanVideo 与衍生家族](#4-视频生成模型hunyuanvideo-与衍生家族)
- [5. 3D生成模型：Hunyuan3D 与 HunyuanWorld](#5-3d生成模型hunyuan3d-与-hunyuanworld)
- [6. 多模态理解：Hunyuan-VL / Hunyuan-Vision-1.5 / HunyuanOCR](#6-多模态理解hunyuan-vl--hunyuan-vision-15--hunyuanocr)
- [7. 音频/语音相关模型](#7-音频语音相关模型)
- [8. 跨方向技术演进分析](#8-跨方向技术演进分析)
- [9. 关键创新点](#9-关键创新点)
- [10. 与其他国产模型的差异化定位](#10-与其他国产模型的差异化定位)
- [11. 参考文献](#11-参考文献)

---

## 1. 概述与时间线

腾讯混元（Hunyuan）是腾讯自研的全栈式基础大模型矩阵，起步于内部支撑 Yuanbao（元宝）助手与微信、QQ、广告等业务的闭源 LLM，自 2024 年中起进入"高频开源 + 多模态"阶段。其特点是：**同时覆盖语言、图像、视频、3D、世界、OCR、视觉理解、音频** 全模态，形成纵向开源、横向统一的生态。

### 1.1 主要发布时间线（精选）

| 时间 | 模型 | 类别 | 关键定位 |
|---|---|---|---|
| 2023.09 | Hunyuan-LLM（闭源 1T MoE） | 语言 | 元宝/腾讯内部业务起家的旗舰 MoE LLM |
| 2024.02 | Hunyuan trillion-parameter MoE 升级 | 语言 | Yuanbao 全面切换至 MoE 架构 |
| 2024.05 | **Hunyuan-DiT** (arXiv:2405.08748v1) | 图像 | 中英文文本条件 DiT；多分辨率生成与多轮编辑 |
| 2024.11 | **Hunyuan-Large** (arXiv:2411.02265) | 语言 | 389B 总参 / 52B 激活 MoE，开源最大 Transformer-MoE |
| 2024.11 | Hunyuan3D 1.0 (arXiv:2411.02293) | 3D | 文/图到 3D 的统一两阶段框架 |
| 2024.12 | **HunyuanVideo** (arXiv:2412.03603) | 视频 | 13B 双流→单流 DiT，3D Causal VAE，MLLM 文本编码 |
| 2025.01 | **Hunyuan3D 2.0** (arXiv:2501.12202) | 3D | Shape-VAE + Hunyuan3D-DiT + Hunyuan3D-Paint |
| 2025.03 | **Hunyuan-T1** | 语言推理 | Mamba+Transformer Hybrid MoE，首个 Mamba 超大推理模型 |
| 2025.03 | HunyuanVideo-I2V | 视频 | 图生视频扩展 |
| 2025.03 | **Hunyuan-TurboS** | 语言 | 快思考模型，Mamba2-Transformer Synergy + 自适应 CoT |
| 2025.05 | **Hunyuan-T1-Vision** | 多模态推理 | 视觉深度推理模型 |
| 2025.05 | **Hunyuan-Voice** | 语音 | 语音通话模型 |
| 2025.05 | HunyuanVideo-Avatar (arXiv:2505.20156)，HunyuanCustom，HunyuanPortrait | 视频 | 数字人/可控/肖像视频 |
| 2025.06 | HunyuanGameCraft (arXiv:2506.17201) | 视频 | 交互式无限长游戏视频 |
| 2025-06-26 | **Hunyuan-A13B** 权重及技术报告开放 | 语言 | 官方仓库当日公告开放 Pretrain、Instruct、FP8、GPTQ-Int4；后续 arXiv v1 于 2026-09-23 提交 |
| 2025.07 | HunyuanWorld 1.0 | 3D 世界 | 首个开源交互式 3D 世界生成 |
| 2025.09 | **HunyuanImage-2.1** | 图像 | 17B DiT，原生 2K，单/双流混合，Glyph-Aware |
| 2025-09-28 | **HunyuanImage-3.0**（base） | 图像 | 约 80B 总参 / 13B 每 token 激活；文本自回归、图像扩散的原生多模态混合架构 |
| 2025.10 | **Hunyuan-Vision-1.5** | VLM | Mamba-Transformer 混合 VLM，A56B/4B，"Thinking on Image" |
| 2025.11 | **HunyuanVideo-1.5** | 视频 | 8.3B 高效视频基模，SSTA 稀疏注意力 |
| 2025.11 | **HunyuanOCR** (arXiv:2511.19575) | VLM-OCR | 1B 商用级开源 OCR-VLM |
| 2025.12 | **混元 2.0** | 语言 | 推理能力与效率国内领先 |
| 2026-01-26 | HunyuanImage-3.0-Instruct / Instruct-Distil | 图像 | 独立衍生权重；推理增强与图像编辑 / 少步蒸馏 |
| 2026.04 | **HY 2.0 Think** | 语言推理 | 深度推理旗舰，128K上下文，分段定价 |
| 2026.04 | **HY 2.0 Instruct** | 语言 | 指令遵循旗舰 |

> 提示：阶段时间以 arXiv 提交或官方仓库 README 公示日期为准；部分模型存在多版本迭代（如 Hunyuan3D 2.0 → 2.1/2.5）。

### 1.2 体系结构

```
Hunyuan 总平台
├── 基座 LLM 线
│   ├── Hunyuan-LLM (闭源 trillion MoE)
│   ├── Hunyuan-Large (389B/52B MoE)
│   ├── Hunyuan-A13B (80B/13B MoE)
│   ├── Hunyuan-TurboS (Mamba+Transformer Hybrid MoE)
│   ├── Hunyuan-T1 (Hybrid MoE 推理强化)
│   ├── 混元 2.0 (2025.12，推理能力与效率国内领先)
│   ├── HY 2.0 Think (2026.04，深度推理旗舰)
│   └── HY 2.0 Instruct (2026.04，指令遵循旗舰)
├── 图像生成
│   ├── Hunyuan-DiT (中文原生 DiT)
│   ├── HunyuanImage-2.1 (17B DiT, 2K)
│   └── HunyuanImage-3.0 (约80B MoE；文本自回归 + 图像latent扩散)
├── 视频生成
│   ├── HunyuanVideo (13B Dual→Single DiT)
│   ├── HunyuanVideo-I2V / Avatar / Portrait / Custom / GameCraft / Foley
│   └── HunyuanVideo-1.5 (8.3B 高效)
├── 3D 与世界
│   ├── Hunyuan3D 1.0 / 2.0 / 2.1 / 2.5
│   ├── Hunyuan3D Studio
│   └── HunyuanWorld 1.0 / 1.5（HY-WorldPlay）
├── 多模态理解
│   ├── Hunyuan-VL (闭源)
│   ├── Hunyuan-Vision-1.5 (Mamba-T 混合 VLM)
│   ├── HunyuanOCR (1B)
│   └── Hunyuan-T1-Vision (2025.05，视觉深度推理)
└── 音频/翻译/语音
    ├── HunyuanVideo-Foley (V2A)
    ├── Hunyuan-MT-7B (翻译)
    └── Hunyuan-Voice (2025.05，语音通话模型)
```

---

## 2. 基座语言模型演进：Hunyuan-LLM → Hunyuan-Large → A13B → TurboS → T1

### 2.1 Hunyuan-LLM（早期闭源 MoE 旗舰）

最早披露于 2023 年下半年，作为支撑腾讯元宝助手的核心 LLM，于 **2024 年 2 月** 全面切换至 MoE 架构（trillion 级总参规模），驱动元宝在阅读、写作和搜索能力上的产品升级。该阶段为闭源，没有公开技术报告，但在后续 Hunyuan-Large 论文中作为系列前身被引用，奠定了"全员 MoE"的工程路线。

### 2.2 Hunyuan-Large：389B 总参 / 52B 激活

> 论文：*Hunyuan-Large: An Open-Source MoE Model with 52 Billion Activated Parameters by Tencent*，[arXiv:2411.02265v3](https://arxiv.org/abs/2411.02265v3)。首次提交 2024-11-04，v3 更新于 2024-11-06。

- **整体规模**：389B 总参数、52B 激活参数；64 层；hidden=6400；80 attention heads；KV heads=8（GQA）；词表 128K；7T tokens 预训练；上下文 256K。
- **MoE 结构**：1 共享专家 + 16 路由（specialized）专家，每 token 激活 1 个共享 + 1 个路由专家。激活函数 SwiGLU，位置编码 RoPE。
- **三大核心创新**：
  1. **KV Cache 压缩（GQA + CLA）**：Hunyuan-Large 使用 80 个 attention heads、8 个 KV groups，CLA 每 2 层共享 KV。技术报告 §2.2.2 的 Table 2 以 BF16 KV 张量字节数对比：MHA 为 `4 n_h d_h l`，GQA+CLA 为 `2 n_g d_h l`，据此比例是 `(2×8)/(4×80)=5%`，作者称相对原始 MHA 节省近 95%。这是给定 MHA 基线与 BF16 下的 KV-cache 张量估算，不代表整机显存或端到端推理内存必然下降 95%。
  2. **Recycle Routing（回收式路由）**：传统 Top-k 中超过专家容量的 token 会被丢弃；Hunyuan-Large 将这些"溢出"的 token 随机重路由到其他专家，避免丢 token 造成的信息损失，与共享专家协同提升训练效率。
  3. **Expert-Specific Learning Rate Scaling**：基于 Adam-style 最优学习率与 batch 之间的关系，对共享专家与路由专家分别匹配各自有效 batch 的最优学习率，缓解 MoE 中"专家梯度异质"的优化痛点。
- **MoE Scaling Law 与训练**：技术报告 §2.3.1 式 (2) 给出作者的 MoE compute-budget 估算 `C ≈ 9.59ND + 2.3×10⁸D`，其中 `N` 为激活参数数、`D` 为训练 token 数；作者以 10M–1B 激活参数及 10B–100B token 范围的实验拟合 isoFLOPs 关系，外推最优点约 58.1B/5.6T，再基于曲线平缓等考虑选择 52B/约 7T。该外推不是在 52B、7T 附近直接穷举的实验，也不等同硬件实测吞吐或训练墙钟时间。学习率采用 warmup → 长缓降 → annealing 三阶段；长上下文阶段渐进 32K→256K，将 RoPE base 频率扩至 1B（均为论文设置）。
- **数据**：约 **1.5T 高质量合成数据**（指令生成→指令进化→响应生成→响应过滤四步法），数学/代码/低资源场景占比显著提升。
- **后训练**：≥1M 条 SFT 数据 + DPO（offline+online 单阶段融合，配 SFT loss 项与 EMA 防 reward hacking）。
- **效果**：在 MMLU=88.4、CMMLU=90.2、C-Eval=91.9、MATH=69.8、HumanEval=71.4 等指标上全面超越 LLaMA3.1-70B，与 LLaMA3.1-405B 持平或在中文/数学/代码维度反超。

### 2.3 Hunyuan-A13B：轻量级 MoE 路线

腾讯于 2025-06-26 开放 Hunyuan-A13B-Pretrain、Instruct、Instruct-FP8 和 Instruct-GPTQ-Int4 权重，并发布技术报告与训练、推理说明。这里的版本范围是官方仓库在该发布中介绍的 Hunyuan-A13B；基准结果仅代表报告所列模型版本和实验设置。

- **参数口径**：技术报告将模型定义为 **80B 总参数、每个输入激活 13B 参数**。报告 §2.2（PDF 第 2 页）说明每层含 1 个始终激活的共享专家和 64 个细粒度非共享专家，其中每次同时激活 8 个非共享专家；表 1 列出 32 层、32 个 attention heads、8 个 KV heads。报告没有给出“含共享专家时为 26.5B 激活”的第二套口径，故删除此前依据社区分析的推算。
- **训练与上下文**：论文描述训练长度逐步扩至 256K。模型卡也宣称支持 256K，但默认配置是 32K；启用完整窗口要改配置，厂商给出的 BF16 部署建议为 4 张 H20 96GB。训练目标、默认设置和部署条件不能混为一谈，这些资料也不证明所有任务在 256K 下都保持稳定效果。
- **部署边界**：13B 是每个输入的激活参数口径，不等同于 80B 权重占用或整机显存需求。不同官方部署说明给出的硬件条件不同，长上下文部署尤其依赖配置和显存；具体来源版本与条件见来源清单。
- **当前可确认的架构**：fine-grained MoE、GQA、RoPE，以及快/慢思考两种模式见技术报告。该报告和模型卡未证明 A13B 是 Hunyuan-Large 的同一架构来源，也未证明它被 TurboS/T1 作为 backbone；这两项关系不在本节作事实陈述。

**版本与日期**：权重及官方仓库技术报告于 2025-06-26 发布；arXiv v1 到 2026-09-23 才提交，PDF 首页标注 2025-06-27。发布日期和论文收录日分别记录；精确权重、仓库 revision 与核查范围见来源清单。

### 2.4 Hunyuan-TurboS：Mamba-Transformer Synergy + 自适应 CoT

> 论文：*Hunyuan-TurboS: Advancing Large Language Models through Mamba-Transformer Synergy and Adaptive Chain-of-Thought*，arXiv:2505.15431，2025-05。

- **核心思想**：将 **Mamba2（线性时序状态空间模型）与 Transformer 注意力融合在 MoE 框架内**，目标是同时具备：
  - 长序列亚二次复杂度下的低成本高吞吐（Mamba 优势）；
  - 强语义建模与精细推理（Transformer 优势）。
- **自适应 CoT（Adaptive Chain-of-Thought）**：根据 prompt 难度动态决定是否进入"慢思考"模式，简单问题快速直答，复杂问题自动展开多步推理；通过 Hunyuan-T1 监督信号生成自适应思考的训练数据。
- **效果**：在 MATH=81.4 等基准上保持与 Qwen3 等顶级模型可比，同时显著降低慢思考类模型的平均推理成本，落地 Tencent Cloud `hunyuan-turbo-*` 系列商用 API。

### 2.5 Hunyuan-T1：首个 Mamba 驱动的超大推理模型

> 官方页：tencent.github.io/llm.hunyuan.T1。
> 发布时间：2025-03-21

- **架构**：超大规模 **Hybrid-Transformer-Mamba MoE**（在 TurboS 基础上加深推理优化层），公开为腾讯首个具备"深度推理"能力的旗舰模型。
- **能力**：长文本理解（继承 TurboS 的长上下文捕获能力）+ 强化学习驱动的链式推理；与 DeepSeek-R1、OpenAI o1 同梯队对标。
- **关系**：T1 在 TurboS 之上提供"思考型"推理；TurboS 反向用 T1 的推理输出做自适应 CoT 蒸馏。

### 2.6 混元 2.0（2025-12-08）

- **定位**：推理能力与效率国内领先的基座模型
- **能力**：在中文推理、数学、代码等维度达到国内第一梯队
- **后续**：为2026年HY 2.0系列奠定基础

### 2.7 HY 2.0 Think / Instruct（2026-04-27）

**HY 2.0 Think**：
- **定位**：深度推理旗舰
- **上下文窗口**：128K
- **能力**：继承并超越T1的深度推理能力，在数学、代码、逻辑推理等基准上达到新高度

**HY 2.0 Instruct**：
- **定位**：指令遵循旗舰
- **能力**：在复杂指令遵循、长文本理解、多轮对话等场景优化

### 2.8 Hunyuan-T1-Vision / Voice（2025-05）

**Hunyuan-T1-Vision**：
- **定位**：视觉深度推理模型
- **能力**：继承T1的推理能力，扩展至视觉理解领域，支持图像分析、图表推理、文档理解等

**Hunyuan-Voice**：
- **定位**：语音通话模型
- **能力**：端到端语音交互，支持实时语音对话、语音指令遵循等场景

### 2.9 语言模型对比表

| 模型 | 总参/激活 | 架构 | 上下文 | 训练 token | 主要场景 | 开源 |
|---|---|---|---|---|---|---|
| Hunyuan-LLM (2024.02) | trillion / – | MoE Transformer | – | – | 元宝助手 | ❌ |
| Hunyuan-Large | 389B / 52B | MoE Transformer + GQA + CLA | 256K | 7T | 通用旗舰 | ✅ |
| Hunyuan-A13B | 80B / 13B per input | Fine-grained MoE；1 shared + 8/64 routed experts | 256K | >20T | 通用/推理 | ✅ |
| Hunyuan-TurboS | – | Mamba2 + Transformer Hybrid MoE | 长上下文 | – | 通用 + 自适应 CoT | API |
| Hunyuan-T1 | – | Hybrid Mamba-Transformer MoE | 长上下文 | – | 深度推理 | API |
| 混元 2.0 (2025.12) | – | – | – | – | 推理与效率旗舰 | API |
| HY 2.0 Think (2026.04) | – | – | 128K | – | 深度推理旗舰 | API |
| HY 2.0 Instruct (2026.04) | – | – | 128K | – | 指令遵循旗舰 | API |

---

## 3. 图像生成模型：Hunyuan-DiT 系列与 HunyuanImage

### 3.1 Hunyuan-DiT

> 论文：*Hunyuan-DiT: A Powerful Multi-Resolution Diffusion Transformer with Fine-Grained Chinese Understanding*，[arXiv 2405.08748v1](https://arxiv.org/abs/2405.08748v1)，首次提交 2024-05-14。模型权重/API revision 未在本批固定。

- **研究定位**：v1 提出面向中文与英文文本的多分辨率 Diffusion Transformer，并报告多轮对话编辑能力。论文支持“在其自建中文评测协议中领先所列开源对照”；不据此声称“首个双语开源 DiT”或“国内最早将 DiT 做成 SOTA”。
- **架构骨架**：
  - **Backbone**：Diffusion Transformer，基于 SD3-style 设计但重写自适应层归一化与位置编码。
  - **VAE**：在潜空间压缩图像（沿用 SD-VAE 结构再训练）。
  - **文本编码器组合（双重）**：
    - **双语 CLIP**（Tencent 自研，覆盖中英）——提供细粒度跨模态语义。
    - **多语言 T5 Encoder（mT5-XXL）**——提供长描述、细节属性的强语义对齐。
  - **位置编码**：**2D RoPE**，支持任意宽高比与多分辨率；多分辨率训练时通过 2D RoPE 自然外推。
- **数据管线（自建）**：
  - 全自研图文数据管线，迭代清洗与重新生成 caption。
  - 训练专用 **多模态大模型 (MLLM) Captioner**：用于 caption refine，把短描述扩成层次化、多视角描述，显著提升细粒度语义对齐。
- **多轮多模态对话**：在 Hunyuan-DiT 基础上加入 multi-turn dialog 微调，使模型能够基于上下文反复修改图像（"对话式生图"）。
- **评估协议与结果（作者报告）**：团队使用 50+ 名评审和 3,000+ 个提示词，按文本图像一致性、AI 瑕疵、主体清晰度、美学四维评分。按该文 Table 1 的所列开源对照（Playground 2.5、PixArt-α、SDXL），Hunyuan-DiT 四项分数均最高（74.2 / 74.3 / 95.4 / 86.6）；overall pass rate 为 59.0%，在表中全部七个模型里排第三，低于 DALL·E 3 的 71.0% 和 MidJourney v6 的 63.3%。用于“Comparison with SOTA”的权重仅覆盖表 2 中列出的类别（合计 90%）；多轮生成的 10% 权重只用于作者内部评测，不包含在该跨模型比较中。表 1 将 SD 3 归为闭源模型，Stable Cascade 未列入比较，因此不再写成“超越 SD3、Stable Cascade 等开源模型”。该结果受作者自建提示集、评审与聚合规则约束，且未将每个对照权重/API revision 固定到可复现身份。来源：[§3.1–3.3、§4.1 Table 1、Appendix A Table 2](https://arxiv.org/html/2405.08748v1)。
- **开源生态**：GitHub 仓库 `Tencent-Hunyuan/HunyuanDiT`，集成至 Diffusers/ComfyUI/Replicate；后续社区在其基础上做 LoRA/ControlNet 等延伸。

### 3.2 HunyuanImage-2.1：高效 2K 文生图

- **规模**：17B 参数 DiT；原生支持 2K（2048×2048）输出，单卡 24GB 显存即可生成 2K 图（2025.09 发布）。
- **架构亮点**：
  - **多模态单/双流 DiT 混合骨架**（吸收了 HunyuanVideo 的 dual→single stream 设计）；
  - **高表达力 VAE**：32×32 空间压缩比，大幅减少 token 数量；
  - **Glyph-Aware 处理**：对中文字符与文字渲染做专门 tokenization 与训练，缓解 DiT 对汉字结构的弱点；
  - **两阶段管线**：第 1 阶段 base T2I + 第 2 阶段 refine（双文本编码器联合）。
- **意义**：是 Hunyuan-DiT 的工业级升级版，主打"高分辨率 + 文字 + 中文"三大刚需。

### 3.3 HunyuanImage-3.0：混合多模态生成架构

> 技术报告：arXiv `2509.23951v3`（v1 首次提交 2025-09-28；v3 更新 2026-06-26）。base 代码与权重于 2025-09-28 公布；Instruct 与 Instruct-Distil 分别于 2026-01-26 公告，具体 checkpoint 版本见[来源清单](sources/MANIFEST.md)。

- **生成路径**：论文 v3 描述的是**混合离散—连续建模**：文本 token 采用自回归 next-token prediction，图像 latent 由扩散式预测生成，再与多模态序列交互。因此这是统一多模态架构中的混合生成，不是纯自回归图像生成。
- **规模**：论文报告总参数**超过 80B**、推理时每 token 激活 **13B**；base 模型卡/代码仓库将总规模标作 80B。
- **模型与版本**：base ID `tencent/HunyuanImage-3.0`，本次检查 HF revision `36f21fe74b65614451cc50ffd8a35a5f662dac70`（页面 `lastModified` 2026-01-28）；代码/README 固定到 `Tencent-Hunyuan/HunyuanImage-3.0@6e9113a692a27a0751d82aba3b2015a876646c03`（commit date 2026-06-23，2026-10-22 查询为 HEAD）。base 权重使用 Tencent Hunyuan Community License；Instruct 与 Instruct-Distil 是不同 checkpoint，官方公告日为 2026-01-26，HF revision 分别见来源清单。
- **能力**：
  - 超长文本指令遵循（"长 prompt 不丢细节"）；
  - 与 HunyuanImage-3.0-Instruct（2026-01）扩展为推理增强提示与 Image-to-Image；
  - 自然支持图像理解 ↔ 生成的统一对话。
- **研究解读**：它将理解与生成放入一个原生多模态模型序列，但图像生成模块仍使用扩散预测。arXiv v3 与官方仓库仍使用营销式体量/性能排名表述；本报告不把该排名当作独立结论，只保留可复核的结构、参数和版本信息。

### 3.4 图像生成模型对比

| 模型 | 范式 | 骨架 | 文本编码器 | 关键能力 |
|---|---|---|---|---|
| Hunyuan-DiT (2024.05) | Diffusion | DiT (UNet→Transformer) | 双语 CLIP + mT5-XXL | 中文原生、多分辨率、多轮对话生图 |
| HunyuanImage-2.1 (2025.09) | Diffusion | Single+Dual Stream DiT | 多文本编码器 | 17B、2K 原生、Glyph-aware、高效 |
| HunyuanImage-3.0 (2025.09) | Hybrid native multimodal | 论文报告 >80B MoE；文本自回归 + 图像latent扩散 | 内置 Hunyuan-A13B base | 统一理解+生成 |

---

## 4. 视频生成模型：HunyuanVideo 与衍生家族

### 4.1 HunyuanVideo：13B 开源视频基础模型

> 论文：*HunyuanVideo: A Systematic Framework For Large Video Generative Models*，arXiv:2412.03603，2024-12。

#### 4.1.1 总体定位

腾讯混元基础模型团队推出，**目标是缩小开源与闭源视频生成（Sora、Gen-3、Kling 等）的差距**，13B 参数规模，具备文生视频与（衍生）图生视频能力，单视频可达 720p × 129 帧（约 5 秒，且可外推），是 2024 年开源视频模型的最强代表之一。

#### 4.1.2 数据系统

- **PySceneDetect + Transnet v2** 进行场景分割；
- **VideoCLIP 嵌入**做去重 + k-means 概念聚类（≈10K 概念中心），实现概念再采样与平衡；
- **Dover** 评估美学/技术质量、optical-flow 过滤静态视频、OCR 移除字幕过载样本、YOLOX 检测水印/边框/Logo；
- 分级（hierarchical）数据漏斗：256p → 360p → 540p → 720p 共 4 级训练子集 + 1M 人工精标 SFT 子集；
- **结构化 caption** + 14 类摄像机运动分类（zoom、pan、tilt、around、static、handheld 等），便于精细控制。

#### 4.1.3 架构核心

1. **Causal 3D VAE**
   - 全自训（不从 image VAE 初始化）；
   - 时空压缩比 *cₜ=4, c_s=8, C=16*；用 CausalConv3D 同时支持图像与视频；
   - Loss = L1 + 0.1·LPIPS + 0.05·GAN + 1e-6·KL；
   - 训练采用 spatial-temporal tiling + 微调消除 inference 不一致；ImageNet PSNR=33.14（>FLUX-VAE/CogVideoX-1.5/Cosmos-VAE）。

2. **Diffusion Backbone（13B）**：**Dual-Stream → Single-Stream Hybrid DiT**
   - **Dual-Stream 阶段**：视频 token 与文本 token 分别穿过 20 个 Transformer block，各自学习独立的调制机制（避免相互干扰）；
   - **Single-Stream 阶段**：将视频/文本 token 拼接，进入 40 个 Transformer block 做深度多模态融合；
   - 配置：hidden=3072、FFN=12288、24 heads、head dim=128；
   - 全局采用 **Full Attention** 替代 divided spatiotemporal attention（论文给出三大理由：性能更优、统一支持图像/视频、可复用 LLM 加速生态）；
   - **3D RoPE**：将旋转频率矩阵分别作用于 (T, H, W) 三个轴的特征通道分段（dt=16, dh=56, dw=56）；
   - 训练目标：**Flow Matching**（v-prediction），推理用一阶 Euler ODE 求解器。

3. **文本编码器**
   - **MLLM Decoder-only LLM 作为主文本编码器**（替代 T5-XXL）：作者论证 instruction-guided MLLM 在文本-视觉对齐与可控指令理解上优于 T5；
   - **CLIP-Large pooled token** 作为全局 guidance 注入 dual/single-stream 块。

4. **Scaling Laws**：构建 DiT-T2X 家族（92M–6.6B），分别对图像与视频拟合 *Nopt = a₁C^b₁, Dopt = a₂C^b₂*；先求 T2I scaling，再外推 T2V scaling，指导 13B 主模型的最终规模选择。

5. **训练阶段（curriculum）**
   - Image stage 1（256px 多宽高比）；
   - Image stage 2（512px）；
   - 视频低分辨率短片段 → 低分辨率长片段 → 高分辨率长片段；
   - 全程视频/图像 4:1 混训以防止图像语义灾难性遗忘。

6. **Prompt Rewrite**
   - 用 **Hunyuan-Large** 直接做 prompt rewriter（多语适配 / 标准化结构 / 简化术语）；
   - 后期 LoRA 微调出小型 rewriter 加速推理。

7. **加速**
   - Time-step shifting（极少步 10-step 也能保质）；
   - Text-guidance distillation（CFG 蒸馏）；
   - **AngelPTM** + Tencent **XingMai 网络**做 13B 大规模分布式训练 + 自动容错。

### 4.2 HunyuanVideo 衍生家族

| 模型 | 论文/时间 | 能力 |
|---|---|---|
| **HunyuanVideo-I2V** | 2025.03，GitHub | 图生视频，720p × 129 帧；Day-1 ComfyUI 支持 |
| **HunyuanVideo-Avatar** | arXiv:2505.20156 | 高保真音频驱动数字人；以 I2V 为底模，两阶段训练（音视频 + 身份保持） |
| **HunyuanCustom** | arXiv:2505.04512 | 多模态条件（文本/图/视频/参考身份）的可控视频定制 |
| **HunyuanPortrait** | 2025 | 隐式条件控制肖像动画，处理身份保真与表情同步 |
| **HunyuanGameCraft** | arXiv:2506.17201 | 连续动作信号驱动的无限长游戏视频生成 |
| **HunyuanVideo-Foley** | 2025.08 | 端到端视频→音效生成（Video-to-Audio） |
| **HunyuanVideo-1.5** | 2025.11，HF | **8.3B 高效新基模**；引入 **SSTA（Selective and Sliding Tile Attention）** 剪枝冗余时空 KV 块，显著降部署门槛 |

> HunyuanVideo-1.5 把"通用视频生成"从 13B 时代压到 8B 级别，使消费级显存可用，成为腾讯视频家族新的"轻量主力"。

---

## 5. 3D生成模型：Hunyuan3D 与 HunyuanWorld

### 5.1 Hunyuan3D 1.0：统一文/图到 3D

> 论文：*Hunyuan3D 1.0: A Unified Framework for Text-to-3D and Image-to-3D Generation*，arXiv:2411.02293，2024-11。

- **范式**：典型"二阶段" 3D 生成——多视图扩散 + sparse-view 重建。
- **能力**：同时支持文本到 3D 与单图/多图到 3D；输出带纹理 mesh。
- **意义**：是 Tencent 对 3D 基础生成的首次系统化开源尝试，铺路 2.0。

### 5.2 Hunyuan3D 2.0：可扩展 3D 资产生成系统

> 论文：*Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation*，arXiv:2501.12202，2025-01（v5 已升级到 2026-05）。

- **架构**（两大基础组件）：
  1. **Hunyuan3D-DiT（形状）**：基于可扩展 **flow-based diffusion transformer**，输入条件图像，输出与之严格对齐的几何形状（mesh）；底层用 **ShapeVAE** 把 3D 几何压到 latent。
  2. **Hunyuan3D-Paint（纹理）**：基于强几何先验和扩散先验的纹理合成模型，可对生成或手工 mesh 涂上高分辨率纹理图。
- **配套 Hunyuan3D-Studio**：面向专业/业余用户的端到端 3D 创作平台（修改、动画化、回退编辑）。
- **后续**：Hunyuan3D 2.1/2.5 之后，Tencent 于 2025-09-16 提交了 *Hunyuan3D Studio* 技术报告（arXiv `2509.12815v1`）。该文描述从概念图到游戏可用资产的集成流程，包含可控图像生成、高保真几何、部件级生成、低多边形建模、Semantic UV、纹理和动画模块（§2）。该固定版本未提到 FlashVDM，也没有“数周到数分钟”的计时，因此不把该时间收益挂在这篇论文名下；见[来源清单](sources/MANIFEST.md)。

### 5.3 HunyuanWorld 1.0 / 1.5：3D 世界与可交互场景

- **HunyuanWorld 1.0**（2025.07 开源）：从文本/单图生成可探索、沉浸式的 3D 场景，使用层次化 3D 网格。
- **HunyuanWorld 1.5（HY-WorldPlay）**：把"世界生成"扩展为**可交互的 3D 世界游玩**，结合 HunyuanVideo 的视频先验和 HunyuanWorld-Mirror 的图像→3D 转换，目标是"用文字/照片生成能进去玩的世界"。
- **意义**：把 3D 生成从静态资产推到"沉浸 + 可交互"领域，是与 Hunyuan3D 资产线并行的高维探索。

---

## 6. 多模态理解：Hunyuan-VL / Hunyuan-Vision-1.5 / HunyuanOCR

### 6.1 Hunyuan-VL（早期闭源 VLM）

腾讯云上 `hunyuan-vision-*` API（含 `hunyuan-t1-vision-*`）从 2024 年起提供视觉问答、OCR、图文检索、文档解析等能力，作为内部业务和云客户的多模态接口；该阶段未开源。

### 6.2 Hunyuan-Vision-1.5（2025.10 公布、计划开源）

> GitHub：`Tencent-Hunyuan/HunyuanVision`。

- **架构亮点**：业内首批 **Mamba-Transformer 混合 VLM**，原生兼具高吞吐与强语义；与 LLM 端的 TurboS/T1 共用混合骨干哲学。
- **规格**：MoE 版本 **A56B**（约 56B 激活）+ **4B** 轻量版；含 Hunyuan-ViT-V1 视觉编码器；将提供 TRT 推理与 vLLM 支持。
- **关键能力**：
  - **"Thinking on Image"（图上思考）**：在推理过程中主动调用 crop/zoom-in、画点/线/框等"图像操作工具"，并可调用网络检索补充知识，类似 OpenAI o3 的 visual chain-of-thought；
  - **3D 空间推理**、视频理解、多语种鲁棒。
- **成绩**：2025-10-06 在 LMArena 中 `hunyuan-vision-1.5-thinking` 排第 3，国内最佳 VLM。

### 6.3 HunyuanOCR：1B 商用级开源 OCR-VLM

> 报告：arXiv:2511.19575，2025-11。

- **目标**：把 OCR/文档/版面/公式/手写等多任务统一进一个 1B VLM，在边缘/CPU 端落地；开源同时商用授权。
- **意义**：补齐 Tencent 多模态家族的"轻量端侧 OCR 入口"，与 Hunyuan-Vision-1.5 形成"重型理解 + 轻型 OCR"双线。

---

## 7. 音频/语音相关模型

腾讯混元在音频侧的开源更聚焦"视频生态闭环"，而非纯 TTS：

- **HunyuanVideo-Foley**（2025.08）：端到端的 Video-to-Audio 模型，根据画面与文本生成与时间精准对齐的音效/环境声，并配合 HunyuanVideo 输出"带声"视频；
- **HunyuanVideo-Avatar**：在视频侧支持音频驱动数字人语音口型同步（输入语音→驱动头像视频）。
- **Hunyuan-MT-7B**（2025.09）：7B 翻译模型，在 WMT2025 拿下 30/31 语言 SOTA，Flores200 上与 GPT-4.1 持平，腾讯把翻译作为"语言侧"专项小模型补强。
- 截至公开信息，腾讯尚未发布与 GPT-4o-Voice / CosyVoice / Step-Audio 同档位的端到端语音 LLM；其语音/TTS 能力主要内嵌于元宝助手与企业 API。

---

## 8. 跨方向技术演进分析

### 8.1 从"独立模型"到"统一平台"的整合路径

腾讯混元的发布并非各自孤立，而是呈现出**横向技术复用 + 纵向能力堆栈**的两条主线：

**(1) 横向：相同的"工程基线"在多模态间复用**

- **MoE 策略**：Hunyuan-Large 的"共享 + 路由专家 + recycle routing + KV 压缩"成为 Hunyuan-A13B、TurboS、Vision-1.5 的共同 backbone 设计语言。
- **Mamba-Transformer 混合**：先在 LLM（TurboS、T1）验证，再迁移至 VLM（Hunyuan-Vision-1.5）。
- **Dual-Stream → Single-Stream DiT**：HunyuanVideo 的范式直接被 HunyuanImage-2.1 借用做"高分辨率 T2I 主骨架"，证实视频→图像的反哺。
- **3D RoPE / Flow Matching**：HunyuanVideo、Hunyuan3D-DiT 共享同一类 flow-based diffusion transformer 训练范式与 RoPE 扩展技巧。
- **MLLM Captioner / Hunyuan-Large Prompt Rewriter**：Hunyuan-DiT、HunyuanVideo 都用自家 LLM 做 caption 重写与 prompt 改写——LLM 直接成为生成模型的"前端语义模块"。

**(2) 纵向：从生成到理解再到世界**

- **生成线（生成像素/几何）**：Hunyuan-DiT → HunyuanImage-2.1/3.0 → HunyuanVideo → Hunyuan3D → HunyuanWorld；
- **理解线**：Hunyuan-VL → Hunyuan-Vision-1.5 → HunyuanOCR；
- **理解 ↔ 生成 融合点**：HunyuanImage-3.0 在原生多模态 backbone 中结合自回归文本与扩散图像生成；Hunyuan-Vision-1.5 则把“生图编辑动作”作为推理工具。两者是不同的多模态整合路径。

### 8.2 时间维度上的三个阶段

| 阶段 | 时间 | 标志 | 主线 |
|---|---|---|---|
| Phase 1：闭源旗舰 | 2023–2024.04 | Hunyuan-LLM trillion MoE | 业务 LLM |
| Phase 2：开源全栈爆发 | 2024.05–2025.06 | DiT/Large/3D/Video 同期开源 | "造各赛道开源 SOTA" |
| Phase 3：架构融合 + 生态平台化 | 2025.05–2026.04 | TurboS/T1/Vision-1.5/Image-3.0/Video-1.5/HunyuanWorld | "Mamba-Transformer 混合 + 多模态统一 AR + 世界化" |
| Phase 4：推理旗舰迭代 | 2025.12–2026.04 | 混元 2.0 → HY 2.0 Think/Instruct | 以推理和指令能力为主的产品迭代 |

### 8.3 与 LLM、生成线的相互增强

- **LLM → 生成**：报告记录 Hunyuan-Large 用于 caption/prompt 重写；HunyuanImage-3.0 则将文本自回归建模与图像扩散预测整合进原生多模态序列；
- **生成 → LLM**：HunyuanVideo 的多模态结构启发了 Vision-1.5 的"图像思考"行为；MLLM Captioner 在视频/图像数据上获得的细粒度对齐，又反哺 LLM 的视觉指令训练。

---

## 9. 关键创新点

按"对中国/全球开源社区最具增量价值"维度归纳：

1. **首个开源 trillion-级 Transformer-MoE（Hunyuan-Large）**
   - 共享 + 路由专家、Recycle Routing、Expert-Specific LR；GQA+CLA 的“近95%”只指论文以 BF16、原始 MHA 为基线的 KV-cache 张量字节数（§2.2.2，Table 2）；MoE compute-budget 式 (2) 的定义、拟合区间与外推边界见 §2.3.1。

2. **首个 Mamba-Transformer 超大 LLM（Hunyuan-T1 / TurboS）**
   - 把 SSM 引入 80B+ 级别推理 LLM，同时引入自适应 CoT，在"成本/质量/响应速度"三角上提供新解。

3. **中文原生 DiT 文生图（Hunyuan-DiT）**
   - 双语 CLIP + 多语 T5 + 2D RoPE + MLLM Captioner + 多轮多模态对话生图，成为开源中文 T2I 标杆。

4. **HunyuanVideo 的"Dual→Single Stream DiT + Causal 3D VAE + MLLM 文本编码 + 3D RoPE + Full Attention"五件套**
   - 是开源视频生成最完整的工程报告之一，被广泛复用（HunyuanImage-2.1、社区微调如 SkyReels）。

5. **HunyuanImage-3.0 的原生多模态混合生成**
   - 文本 token 自回归、图像 latent 扩散；论文 v3 报告总参超过80B、每token激活13B。不同任务路径和 checkpoint revision 应分开核查，不据单个厂商自述给出跨模型规模排名。

6. **HunyuanVideo-1.5 的 SSTA**
   - Selective and Sliding Tile Attention 在视频 DiT 中剪枝时空 KV 块，使 8.3B 模型即可达到原 13B 体验，是开源视频部署的工程拐点。

7. **Hunyuan3D 2.0 的 "Shape-DiT + Texture-Paint" 解耦**
   - 把"几何"与"纹理"作为两个独立可扩展的扩散问题分别训练，配合 ShapeVAE；后续 Studio 报告扩展到从概念图到游戏资产的多个生产阶段，但本报告未核验端到端耗时。

8. **HunyuanWorld：3D 世界 + 可交互**
   - 站在 Hunyuan3D + HunyuanVideo 的肩膀上，把生成内容从"图/视频/资产"推到"可游玩 3D 世界"。

9. **Hunyuan-Vision-1.5 的 "Thinking on Image"**
   - VLM 主动调用图像操作工具 + 网络检索做视觉链式推理，是国产开源 VLM 在 LMArena 的最佳成绩之一。

---

## 10. 与其他国产模型的差异化定位

| 维度 | Hunyuan | Qwen（阿里） | DeepSeek | GLM/智谱 | Kimi（月之暗面） |
|---|---|---|---|---|---|
| LLM 旗舰路线 | Trillion MoE 起家 → Large/A13B 双开源 | Qwen2.5/3 + Qwen3-MoE | V2/V3/R1 强稀疏 MoE | GLM-4 / GLM-4.5 | K1.5 长上下文 |
| 推理模型 | T1 + TurboS（**Mamba-Transformer 混合**） | QwQ / Qwen3-Thinking | R1 / R1-Distill | GLM-Z1 | k1.5/k2-thinking |
| 文生图 | Hunyuan-DiT、HunyuanImage-2.1/3.0（3.0为文本自回归 + 图像latent扩散的多模态混合架构） | Wan-Image、Qwen-Image | Janus-Pro | CogView-3 | – |
| 视频 | **HunyuanVideo（开源 13B）+ 1.5（8B 高效）+ Avatar/I2V/GameCraft** | Wan2.1/2.2 | – | CogVideoX | – |
| 3D | **Hunyuan3D 1/2/2.5 + Studio + World** | – | – | – | – |
| VLM | Hunyuan-Vision-1.5（Mamba-T 混合）、HunyuanOCR | Qwen2.5-VL/Qwen3-VL | DeepSeek-VL2 | GLM-4V/4.5V | k1.5-vl |

**差异化要点（研究归纳，非横评）**：
- **当前报告覆盖语言、图像、视频、3D/世界、OCR 与 V2A**，体现了腾讯已公开研究方向的跨度；本报告没有对全市场覆盖率或各方向的同协议模型质量做完整盘点，故不据此声称“国内覆盖最宽”或“视频与 3D/世界最强 SOTA”。
- **架构哲学上"押注 Mamba-Transformer 混合 + MoE"**，与 DeepSeek（纯 MoE+MLA）、Qwen（密集+MoE 双线）、Kimi（强 attention 注意力优化）形成路线分化。
- **大量复用业务侧 LLM（Hunyuan-Large）当 caption/prompt rewriter**，把 LLM 的"语义先验"显式注入到生成模型，是其内容质量明显高于同等开源模型的工程秘密。
- **腾讯把 3D 与世界生成单独立项**（Hunyuan3D Studio、HunyuanWorld、GameCraft），与游戏/广告/影视产业链高度绑定，这是其他几家暂未规模化覆盖的赛道。

---

## 11. 参考文献

> 论文与官方资源（按出现顺序）

1. Tencent Hunyuan Team. *Hunyuan-Large: An Open-Source MoE Model with 52 Billion Activated Parameters by Tencent.* [arXiv:2411.02265v3](https://arxiv.org/abs/2411.02265v3), first submitted 2024-11-04; v3 updated 2024-11-06.
2. Tencent Hunyuan Team. *Hunyuan-DiT: A Powerful Multi-Resolution Diffusion Transformer with Fine-Grained Chinese Understanding.* arXiv:2405.08748v1, submitted 2024-05-14. https://arxiv.org/abs/2405.08748v1
3. Hunyuan Foundation Model Team. *HunyuanVideo: A Systematic Framework For Large Video Generative Models.* arXiv:2412.03603, 2024. https://arxiv.org/abs/2412.03603
4. Tencent Hunyuan 3D Team. *Hunyuan3D 1.0: A Unified Framework for Text-to-3D and Image-to-3D Generation.* arXiv:2411.02293, 2024. https://arxiv.org/abs/2411.02293
5. Tencent Hunyuan 3D Team. *Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation.* arXiv:2501.12202, 2025. https://arxiv.org/abs/2501.12202
6. Tencent Hunyuan Team. *Hunyuan-TurboS: Advancing Large Language Models through Mamba-Transformer Synergy and Adaptive Chain-of-Thought.* arXiv:2505.15431, 2025. https://arxiv.org/abs/2505.15431
7. Tencent Hunyuan Team. *HunyuanImage 3.0 Technical Report.* arXiv:2509.23951v3; v1 submitted 2025-09-28, v3 revised 2026-06-26. https://arxiv.org/abs/2509.23951v3
8. Tencent Hunyuan Team. *HunyuanOCR Technical Report.* arXiv:2511.19575, 2025. https://arxiv.org/abs/2511.19575
9. Tencent Hunyuan Team. *HunyuanVideo-Avatar: High-Fidelity Audio-Driven Human Video Generation.* arXiv:2505.20156, 2025.
10. Tencent Hunyuan Team. *HunyuanCustom: A Multimodal-Driven Architecture for Customized Video Generation.* arXiv:2505.04512, 2025.
11. Tencent Hunyuan Team. *Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation.* arXiv:2506.17201, 2025.
12. Tencent Hunyuan Team. *Hunyuan3D Studio: End-to-End AI Pipeline for Game-Ready 3D Generation.* arXiv:2509.12815, 2025.
13. *Hunyuan-T1 Official Page.* https://tencent.github.io/llm.hunyuan.T1/README_EN.html
14. *Tencent Hunyuan Team. Hunyuan-A13B Technical Report.* arXiv:2609.27284v1, submitted 2026-09-23; PDF cover date 2025-06-27. §2.2–2.3, Tables 1 and 4. https://arxiv.org/abs/2609.27284v1
15. *Tencent-Hunyuan/Hunyuan-A13B (official repository).* https://github.com/Tencent-Hunyuan/Hunyuan-A13B
16. *tencent/Hunyuan-A13B-Instruct model card.* https://huggingface.co/tencent/Hunyuan-A13B-Instruct
17. *Tencent-Hunyuan/HunyuanDiT (GitHub).* https://github.com/Tencent-Hunyuan/HunyuanDiT
18. *Tencent-Hunyuan/HunyuanVideo (GitHub).* https://github.com/Tencent-Hunyuan/HunyuanVideo
19. *Tencent-Hunyuan/HunyuanVideo-I2V (GitHub).* https://github.com/Tencent-Hunyuan/HunyuanVideo-I2V
20. *tencent/HunyuanVideo-1.5 (Hugging Face).* https://huggingface.co/tencent/HunyuanVideo-1.5
21. *Tencent-Hunyuan/HunyuanImage-2.1 (GitHub).* https://github.com/Tencent-Hunyuan/HunyuanImage-2.1
22. *tencent/HunyuanImage-3.0 (Hugging Face).* https://huggingface.co/tencent/HunyuanImage-3.0
23. *Tencent-Hunyuan/HunyuanVision (GitHub).* https://github.com/Tencent-Hunyuan/HunyuanVision
24. *Tencent-Hunyuan/Hunyuan3D-2 (GitHub).* https://github.com/Tencent-Hunyuan/Hunyuan3D-2
25. *Tencent-Hunyuan/HY-WorldPlay (GitHub).* https://github.com/Tencent-Hunyuan/HY-WorldPlay
26. *Tencent Hunyuan 3D 官网.* https://3d-models.hunyuan.tencent.com/
27. *Hunyuan AI 视频项目官网.* https://aivideo.hunyuan.tencent.com/
28. *Tencent Hy Research.* https://hy.tencent.com/

> 报告完成时间：2026-06-05（基于截至该时间公开的论文与官方信息）。
