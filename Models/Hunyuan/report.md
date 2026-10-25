---
display_name: Hunyuan
---

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
- [7. 音频、语音与机器翻译](#7-音频语音与机器翻译)
- [8. 跨方向综合：容量、序列状态与生成表示是不同设计轴](#8-跨方向综合容量序列状态与生成表示是不同设计轴)
- [9. 技术阅读要点](#9-技术阅读要点)
- [10. 比较边界](#10-比较边界)
- [11. 参考文献](#11-参考文献)

---

## 1. 概述与时间线

腾讯混元（Hunyuan）是腾讯自研的基础模型系列，涵盖语言、图像、视频、3D/世界、OCR、视觉理解和音频等方向。自 2024 年起，团队陆续公开论文、代码或权重；不同项目的开放范围和技术体系并不相同，不能从产品覆盖面推断为统一架构或全部开源。

### 1.1 主要发布时间线（精选）

| 时间 | 模型 | 类别 | 关键定位 |
|---|---|---|---|
| 2023.09 | Hunyuan-LLM（闭源 1T MoE） | 语言 | 元宝/腾讯内部业务起家的旗舰 MoE LLM |
| 2024.02 | Hunyuan trillion-parameter MoE 升级 | 语言 | Yuanbao 全面切换至 MoE 架构 |
| 2024.05 | **Hunyuan-DiT** (arXiv:2405.08748v1) | 图像 | 中英文文本条件 DiT；多分辨率生成与多轮编辑 |
| 2024.11 | **Hunyuan-Large** (arXiv:2411.02265) | 语言 | 389B 总参 / 52B 激活 MoE |
| 2024.11 | Hunyuan3D 1.0 (arXiv:2411.02293) | 3D | 文/图到 3D 的统一两阶段框架 |
| 2024.12 | **HunyuanVideo** (arXiv:2412.03603) | 视频 | 13B 双流→单流 DiT，3D Causal VAE，MLLM 文本编码 |
| 2025.01 | **Hunyuan3D 2.0** (arXiv:2501.12202) | 3D | Shape-VAE + Hunyuan3D-DiT + Hunyuan3D-Paint |
| 2025.03 | **Hunyuan-T1** | 语言推理 | Mamba+Transformer Hybrid MoE |
| 2025.03 | HunyuanVideo-I2V | 视频 | 图生视频扩展 |
| 2025.03 | **Hunyuan-TurboS** | 语言 | 快思考模型，Mamba2-Transformer Synergy + 自适应 CoT |
| 2025.05 | **Hunyuan-T1-Vision** | 多模态推理 | 视觉深度推理模型 |
| 2025.05 | **Hunyuan-Voice** | 语音 | 语音通话模型 |
| 2025.05 | HunyuanVideo-Avatar (arXiv:2505.20156)，HunyuanCustom，HunyuanPortrait | 视频 | 数字人/可控/肖像视频 |
| 2025.06 | HunyuanGameCraft (arXiv:2506.17201) | 视频 | 交互式无限长游戏视频 |
| 2025-06-26 | **Hunyuan-A13B** 权重及技术报告开放 | 语言 | 官方仓库当日公告开放 Pretrain、Instruct、FP8、GPTQ-Int4；后续 arXiv v1 于 2026-09-23 提交 |
| 2025.07 | HunyuanWorld 1.0 | 3D 世界 | 交互式 3D 世界生成系统 |
| 2025.09 | **HunyuanImage-2.1** | 图像 | 17B DiT，原生 2K，单/双流混合，Glyph-Aware |
| 2025-09-28 | **HunyuanImage-3.0**（base） | 图像 | 约 80B 总参 / 13B 每 token 激活；文本自回归、图像扩散的原生多模态混合架构 |
| 2025.10 | **Hunyuan-Vision-1.5** | VLM | Mamba-Transformer 混合 VLM，A56B/4B，"Thinking on Image" |
| 2025.11 | **HunyuanVideo-1.5** | 视频 | 8.3B 高效视频基模，SSTA 稀疏注意力 |
| 2025.11 | **HunyuanOCR** (arXiv:2511.19575) | VLM-OCR | 1B OCR-VLM |
| 2025.12 | **混元 2.0** | 语言 | 推理模型系列；具体能力比较需按评测设置核查 |
| 2026-01-26 | HunyuanImage-3.0-Instruct / Instruct-Distil | 图像 | 独立衍生权重；推理增强与图像编辑 / 少步蒸馏 |
| 2026.04 | **HY 2.0 Think** | 语言推理 | 深度推理模型，128K上下文 |
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
│   ├── 混元 2.0 (2025.12，推理模型系列)
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

最早披露于 2023 年下半年，作为支撑腾讯元宝助手的核心 LLM；腾讯于 **2024 年 2 月** 宣布产品切换至 trillion 级 MoE 架构。该阶段没有公开技术报告，因此无法据此还原训练细节、产品能力变化或后续各模型的架构沿革。

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

- **参数口径**：技术报告给出 **80B 总参数、每个输入激活 13B 参数**。报告 §2.2（PDF 第 2 页）说明每层含 1 个始终激活的共享专家和 64 个细粒度非共享专家，其中每次同时激活 8 个非共享专家；表 1 列出 32 层、32 个 attention heads、8 个 KV heads。公开报告没有提供“含共享专家时为 26.5B 激活”的另一口径，因此不能据社区推算替代作者给出的数字。
- **训练与上下文**：论文描述训练长度逐步扩至 256K。模型卡也宣称支持 256K，但默认配置是 32K；启用完整窗口要改配置，厂商给出的 BF16 部署建议为 4 张 H20 96GB。训练目标、默认设置和部署条件不能混为一谈，这些资料也不证明所有任务在 256K 下都保持稳定效果。
- **部署边界**：13B 是每个输入的激活参数口径，不等同于 80B 权重占用或整机显存需求。不同官方部署说明给出的硬件条件不同，长上下文部署尤其依赖配置和显存；对应版本与部署材料见来源清单。
- **当前可确认的架构**：fine-grained MoE、GQA、RoPE，以及快/慢思考两种模式见技术报告。该报告和模型卡未证明 A13B 是 Hunyuan-Large 的同一架构来源，也未证明它被 TurboS/T1 作为 backbone；这两项关系不在本节作事实陈述。

**版本与日期**：权重及官方仓库技术报告于 2025-06-26 发布；arXiv v1 到 2026-09-23 才提交，PDF 首页标注 2025-06-27。发布日期和论文收录日分别列出；权重与仓库 revision 见来源清单。

### 2.4 Hunyuan-TurboS：Mamba-Transformer Synergy + 自适应 CoT

> 论文：*Hunyuan-TurboS: Advancing Large Language Models through Mamba-Transformer Synergy and Adaptive Chain-of-Thought*，arXiv:2505.15431，2025-05。

- **核心思想**：将 **Mamba2（线性时序状态空间模型）与 Transformer 注意力融合在 MoE 框架内**，目标是同时具备：
  - 长序列亚二次复杂度下的低成本高吞吐（Mamba 优势）；
  - 强语义建模与精细推理（Transformer 优势）。
- **自适应 CoT（Adaptive Chain-of-Thought）**：根据 prompt 难度动态决定是否进入"慢思考"模式，简单问题快速直答，复杂问题自动展开多步推理；通过 Hunyuan-T1 监督信号生成自适应思考的训练数据。
- **效果（作者报告）**：论文列出 MATH=81.4 等结果，但缺少与 Qwen3 对照所需的完整评测实现、提示集和检查点信息；这些数字不能单独支持同档结论，也不能推出平均推理成本优势。

### 2.5 Hunyuan-T1：Mamba-Transformer 混合推理模型

> 官方页：tencent.github.io/llm.hunyuan.T1。
> 发布时间：2025-03-21

- **公开定位**：Hybrid-Transformer-Mamba MoE 的推理模型，强调长上下文和强化学习驱动的思考模式。
- **关系边界**：TurboS 技术报告包含 Adaptive CoT 和其训练数据/推理配置；T1 的官方页面披露较少。现有来源不能确认二者共享 checkpoint、前后级蒸馏关系或相同的 RL 配方，因此本报告将它们视作相关但独立公开的路线。

- **混元 2.0 / HY 2.0 Think、Instruct**：官方材料说明推理/指令模型系列及部分接口；目前公开技术披露未达到 Hunyuan-Large、A13B 或 TurboS 报告的细节程度，不从发布时间或产品描述补推架构、训练链路或基准胜负。
- **Hunyuan-T1-Vision / Hunyuan-Voice**：可确认的材料主要描述视觉推理与语音交互能力；在没有独立技术报告时，不据“继承 T1”推断其和 T1 共享同一视觉/语音 backbone。

就语言模型支线而言，能够逐篇比较方法的材料目前主要是 Hunyuan-Large、A13B 和 TurboS：前两者均以稀疏专家扩大模型容量，但专家粒度和路由负担不同；TurboS 把线性序列状态模型与 attention 结合，重点转向长序列效率。Hunyuan-T1 与更晚的混元 2.0/HY 2.0 系列可用于追踪能力方向，当前公开文档不足以纳入同等深度的机制对照。

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
- **评估协议与结果（作者报告）**：团队使用 50+ 名评审和 3,000+ 个提示词，按文本图像一致性、AI 瑕疵、主体清晰度、美学四维评分。按该文 Table 1 的所列开源对照（Playground 2.5、PixArt-α、SDXL），Hunyuan-DiT 四项分数均最高（74.2 / 74.3 / 95.4 / 86.6）；overall pass rate 为 59.0%，在表中全部七个模型里排第三，低于 DALL·E 3 的 71.0% 和 MidJourney v6 的 63.3%。用于“Comparison with SOTA”的权重仅覆盖表 2 中列出的类别（合计 90%）；多轮生成的 10% 权重只用于作者内部评测，不包含在该跨模型比较中。表 1 将 SD 3 归为闭源模型，Stable Cascade 未列入比较；因此这些表格不支持“超越 SD3、Stable Cascade 等开源模型”的说法。结果受作者自建提示集、评审与聚合规则约束，且未将每个对照权重/API revision 固定到可复现身份。来源：[§3.1–3.3、§4.1 Table 1、Appendix A Table 2](https://arxiv.org/html/2405.08748v1)。
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
- **模型与版本**：base ID `tencent/HunyuanImage-3.0`，Hugging Face revision `36f21fe74b65614451cc50ffd8a35a5f662dac70`（页面 `lastModified` 2026-01-28）；代码/README 对应 `Tencent-Hunyuan/HunyuanImage-3.0@6e9113a692a27a0751d82aba3b2015a876646c03`（commit date 2026-06-23）。base 权重使用 Tencent Hunyuan Community License；Instruct 与 Instruct-Distil 是不同 checkpoint，官方公告日为 2026-01-26，HF revision 分别见来源清单。
- **能力**：
  - 超长文本指令遵循（"长 prompt 不丢细节"）；
  - 与 HunyuanImage-3.0-Instruct（2026-01）扩展为推理增强提示与 Image-to-Image；
  - 自然支持图像理解 ↔ 生成的统一对话。
- **研究解读**：它将理解与生成放入一个原生多模态模型序列，但图像生成模块仍使用扩散预测。arXiv v3 与官方仓库提供的体量和性能排名属于厂商报告，不能视作独立比较；可用于机制分析的是公开的结构、参数和版本信息。

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

腾讯混元基础模型团队提出的 13B 视频生成模型，支持文生视频；后续版本扩展图生视频。技术报告描述 720p、129 帧（约 5 秒）的生成设置。这里记录模型规模与任务范围，不据未固定的跨系统设置作质量排序。

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
| **HunyuanVideo-1.5** | 2025.11，技术报告与 HF | **8.3B DiT**；SSTA 将动态选出的时空块与局部滑动窗口掩码结合，减少长序列注意力计算；作者在限定推理配置中报告了加速，见[技术报告 §3.1、§6](https://arxiv.org/abs/2511.18870v2) |

> 技术报告的对照是 HunyuanVideo-1.5 自身启用与未启用稀疏注意力：10 秒、720p 文生视频、241 帧的 CFG 蒸馏模型，在 8 张 H800 上每步时间由 5.507 秒降至 2.9475 秒（约 1.87×，不含工程级加速；§6/Table 7）。这说明该设置下 SSTA 降低了推理时间；报告没有证明它与旧版 13B HunyuanVideo 达到相同生成质量，也不能把这组硬件结果直接外推为消费级 GPU 的速度。

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

### 6.2 Hunyuan-Vision-1.5（2025.10 公布）

> GitHub：[`Tencent-Hunyuan/HunyuanVision`](https://github.com/Tencent-Hunyuan/HunyuanVision/tree/61895cecc18a2ede2c8f8c921b9bec26130625f8)。该固定 README 仍把论文、权重和推理支持列在“Open-source Plan”中。

- **架构**：采用 **Mamba-Transformer 混合 VLM**。现有材料不足以判断其吞吐、理解质量，或是否与 TurboS/T1 共享骨干；这些关系需要固定实现和同条件实验才能比较。
- **规格**：MoE 版本 **A56B**（约 56B 激活）+ **4B** 轻量版；含 Hunyuan-ViT-V1 视觉编码器；将提供 TRT 推理与 vLLM 支持。
- **关键能力**：
  - **"Thinking on Image"（图上思考）**：在推理过程中主动调用 crop/zoom-in、画点/线/框等"图像操作工具"，并可调用网络检索补充知识，类似 OpenAI o3 的 visual chain-of-thought；
  - **3D 空间推理**、视频理解、多语种鲁棒。

> 官方 README 提及 2025-10-06 的 LMArena 排名，但未提供榜单快照、任务类型和对照模型版本；该说法不足以支持可复核的横向比较。

### 6.3 HunyuanOCR：1B OCR-VLM

> 报告：arXiv:2511.19575，2025-11。

- **目标**：把 OCR/文档/版面/公式/手写等多任务统一进一个 1B VLM，在边缘/CPU 端落地；开源同时商用授权。
- **意义**：补齐 Tencent 多模态家族的"轻量端侧 OCR 入口"，与 Hunyuan-Vision-1.5 形成"重型理解 + 轻型 OCR"双线。

---

## 7. 音频、语音与机器翻译

腾讯混元在音频侧的开源更聚焦"视频生态闭环"，而非纯 TTS：

- **HunyuanVideo-Foley**（2025.08）：端到端的 Video-to-Audio 模型，根据画面与文本生成与时间精准对齐的音效/环境声，并配合 HunyuanVideo 输出"带声"视频；
- **HunyuanVideo-Avatar**：在视频侧支持音频驱动数字人语音口型同步（输入语音→驱动头像视频）。
- **Hunyuan-MT-7B / Hunyuan-MT-Chimera-7B**（2025.09）：前者是 7B 翻译模型，后者把同一模型在不同设置下生成的多个译文融合为一个输出。技术报告分别使用 Flores-200、WMT24pp 开发集和普通话—少数民族语言测试集，并报告自动指标和专家评分；这些结果不应与 WMT25 竞赛排名混为一谈。见[技术报告 §4](https://arxiv.org/html/2509.05209v2)。

  WMT25 中，Tencent 技术报告称其参赛系统在 31 个语言方向里有 30 个“排名第一”。组织方的结果论文将参赛系统标为 **Shy-hunyuan-MT**，并指出 30/31 是自动排名：该系统在人评中明显低于部分高排名系统，但仍是受限赛道表现最好的系统，在 11 个方向进入该赛道的胜出组；总体人评中 Gemini 2.5 Pro 在 14 个方向进入顶端组。因而 30/31 不能写成“人评赢 30 个语种”，也不能不加区分地归到基础 Hunyuan-MT-7B 检查点。来源：[WMT25 结果论文 §7.2](https://www2.statmt.org/wmt25/pdf/2025.wmt-1.22.pdf)、[Shy-hunyuan-MT 系统论文](https://aclanthology.org/2025.wmt-1.36.pdf)。
- 截至公开信息，腾讯尚未发布与 GPT-4o-Voice / CosyVoice / Step-Audio 同档位的端到端语音 LLM；其语音/TTS 能力主要内嵌于元宝助手与企业 API。

---

## 8. 跨方向综合：容量、序列状态与生成表示是不同设计轴

混元家族看上去覆盖许多模态，但这些支线不是同一个基础模型逐代加入工具。论文显示的是几类不同的技术问题：语言模型控制参数容量和推理计算；图像/视频生成压缩视觉序列并决定去噪过程；3D生成从几何表示到纹理渲染分阶段构造；视觉理解模型则要在图像输入和语言推理间分配容量。

### 8.1 语言线：MoE 扩展容量，Mamba-T 混合改变序列建模

[Hunyuan-Large](https://arxiv.org/abs/2411.02265v3) 与 [Hunyuan-A13B](https://arxiv.org/abs/2609.27284v1) 都用 MoE 将总参数规模与每 token 激活计算分开，但专家数量、共享/路由策略、上下文训练和模型规模并不相同。Large 重点研究共享专家、Recycle Routing、KV 压缩和专家专属学习率；A13B 使用更细粒度的路由专家，并以 13B 激活配置兼顾开放部署。两篇论文的共同问题是：扩大参数容量时，怎样避免推理显存、路由负载和长上下文 KV 状态成为瓶颈；不能据“都叫 MoE”推断两者共享 backbone 或能直接互换部署。

[Hunyuan-TurboS](https://arxiv.org/abs/2505.15431) 把问题进一步转为序列处理成本：在混合专家体系里交替布置 Mamba2、attention 和 FFN，目标是在长序列上利用 Mamba 的状态传递效率，同时保留 attention 对上下文关系的直接访问。其 Adaptive CoT 则把模型计算预算按任务难度变化，面向简短回答与复杂推理两类输出。T1 和 TurboS 的公开材料均描述混合序列模块与推理增强，但没有证明其训练配方、检查点和部署成本完全相同；应分别阅读架构图、token/attention 细节与采样条件。

这一语言路线的变化可概括为“稀疏容量”与“序列计算”两个不同轴：MoE 减少激活 FFN 计算但仍需管理全量专家权重；Mamba-T 试图降低长序列计算/状态成本，但不能由架构名称直接推出长上下文的检索质量。对报告中的效率数字，应回到它所比较的 baseline、硬件和 batch 设定。

### 8.2 生成线：连续视觉 latent 扩散，到几何/纹理和交互世界

[Hunyuan-DiT](https://arxiv.org/abs/2405.08748v1) 解决中文/英文提示如何进入高分辨率图像扩散：CLIP 与 mT5 组合处理图文语义，2D RoPE 支持多分辨率，多轮对话编辑则增加上下文式条件。HunyuanImage-2.1 仍沿图像 DiT 方向，重点放在 2K 生成、VAE token 压缩和文字渲染；[HunyuanImage-3.0](https://arxiv.org/abs/2509.23951v3) 把文本 next-token prediction 与图像 latent diffusion 放入同一多模态序列框架。这几代有可比较的表示路线，但 3.0 的公开材料并未证明它是 2.1 主干简单放大，也没有统一实验把质量变化归因到单一机制。

[HunyuanVideo](https://arxiv.org/abs/2412.03603) 将图像生成扩展到时空 latent：3D causal VAE 降低帧序列长度并用时间因果卷积保持过去/未来方向，视频 DiT 的 dual-stream 阶段分开处理文本和视频特征，single-stream 阶段再做融合；3D RoPE 表示时空坐标，完整时空 attention 直接建模跨帧关系。核心取舍是时序一致性与注意力成本：full attention 能建立全局时间关系，却会扩大序列计算；VAE 压缩节省计算，也会成为可恢复细节的上限。[HunyuanVideo-1.5](https://arxiv.org/abs/2511.18870v2) 的 SSTA 则用选择性时空块和局部窗口减少注意力负担；论文只支持给定 8×H800、10 秒 720p 配置下的推理加速，不能推出与旧 13B 模型质量等价。

[Hunyuan3D 2.0](https://arxiv.org/abs/2501.12202) 将生成对象变为可编辑的 3D 资产：shape diffusion 与 texture paint 分成两个基础模型，几何先满足输入图像约束，纹理阶段再处理材质与多视角外观。2.5 沿两阶段结构扩大 shape 模型，并加入 PBR 纹理路线。[HunyuanWorld](https://arxiv.org/abs/2507.21809) 则关注场景而非单件资产，使用可探索的场景表示、语义分层网格及视点/动作条件。三者分别对应单图像、资产表面和持续世界状态，不能把“从图到3D”与“可交互 world model”视作同一能力连续升级。

### 8.3 理解线：通用 VLM 与专用 OCR 的任务边界

[Hunyuan-Vision-1.5](https://github.com/Tencent-Hunyuan/HunyuanVision) 将视觉编码器与语言/序列模型结合，并使用推理阶段的裁剪、放大、标注和检索等工具处理图像任务；这是一条以视觉推理/交互为目标的路线。[HunyuanOCR](https://arxiv.org/abs/2511.19575) 则用约 1B 参数的 ViT + LLM + MLP adapter 处理文字定位、文档解析、信息抽取和翻译等 OCR 任务，强调端到端架构以减少传统 OCR 流水线中间步骤的误差传播。

两者不构成简单的“通用模型比专用模型强”关系：Vision 的测试应覆盖图像推理、视频、GUI、空间理解等开放任务；OCR 应覆盖文字检测/识别、版面、表格、文档问答、印刷/手写等任务。HunyuanOCR 论文报告其在部分文档与 OCR benchmark 上表现突出，但这些是作者报告的特定任务结果；不能直接据此推导其通用视觉推理能力，也不能用 VLM 总分替代 OCR 任务评测。

### 8.4 跨线连接：可确认的依赖与不可确认的“统一”

| 连接点 | 公开材料支持什么 | 还不能推出什么 |
|---|---|---|
| 语言模型作为条件/重写组件 | HunyuanVideo 论文用大语言/多模态模型处理文本描述和 prompt；HunyuanImage 的数据/文本编码线也强调文本条件质量 | 不能据此认为视频、图像系统共享同一文本编码器或联合预训练 |
| 混合专家与混合序列模块 | Large/A13B 用 MoE；TurboS 和 Vision-1.5 提及 Mamba-Transformer 混合 | 同一团队使用相同术语不代表专家数、层布局、训练目标或参数可继承 |
| 生成与理解并置 | HunyuanImage-3.0 报告了文本自回归与图像扩散的混合路线；Hunyuan-Vision/OCR 分别提供视觉理解模型 | 不能把“统一架构”推广为所有 Hunyuan 模态已共用一个模型或共享参数 |
| 文本到视频、3D 与世界建模 | Video 生成时空像素序列，3D 资产生成 mesh，World 生成可探索场景 | 视频逼真度、单资产几何质量和交互世界一致性是不同评测对象，不能合并成“世界模型能力” |
| 音频与语言服务 | Video-Foley 研究视频条件音效；Hunyuan-MT/Chimera 研究翻译与多候选融合，属于各自任务的专门处理 | 公开材料没有证明它们使用同一语音—视频模型，竞赛系统也不能等同于基础 MT 检查点 |

最有价值的跨线观察并不是“混元覆盖得很全”，而是表示和反馈随任务而变：语言序列可走稀疏 FFN 专家或 Mamba/attention 混合；图像生成用连续 latent 扩散；视频需要时间因果压缩；3D 需要把形状与材质分离；OCR 则把任务限制在文字/文档理解。后续如果出现模型间共享 encoder、joint training 或 distillation 的直接报告，才可以把这种并行路线改写成因果关系。

### 8.5 阅读路线与未闭合问题

建议围绕三个比较问题阅读：先对照 Hunyuan-Large/A13B/TurboS 的稀疏容量、KV cache 与长序列设计；再读 Hunyuan-DiT、HunyuanVideo、Hunyuan3D 2.0，比较图像/视频/几何表示及生成目标；最后读 Hunyuan-Vision-1.5 与 HunyuanOCR，区分工具化视觉推理和专用文档感知。

仍未闭合的问题包括：Mamba-T 混合结构是否在推理质量/延迟上优于同预算 attention-only 或 Mamba-only baseline；HunyuanVideo full attention 与 Video-1.5 SSTA 在固定版本、同质量设置下如何取舍；Image-3.0 的理解与生成任务是否互相促进；世界模型的长时几何一致性如何在多轮交互而非单帧视觉质量上度量。现有不同论文和模型卡未形成这些问题的同协议对照。

---

## 9. 技术阅读要点

以下归纳聚焦本报告已介绍、适合进一步阅读的技术设计，不构成创新性或行业排名：

1. **Hunyuan-Large 的 MoE 与注意力设计**
   - 共享 + 路由专家、Recycle Routing、Expert-Specific LR；GQA+CLA 的“近95%”只指论文以 BF16、原始 MHA 为基线的 KV-cache 张量字节数（§2.2.2，Table 2）；MoE compute-budget 式 (2) 的定义、拟合区间与外推边界见 §2.3.1。

2. **TurboS / T1 的 Mamba-Transformer 混合路线**
   - 相关技术报告描述了 Mamba 与 Transformer 的组合，并讨论自适应 CoT。该设计的质量、速度和成本收益需要按对应实验设置分别判断。

3. **中文原生 DiT 文生图（Hunyuan-DiT）**
   - 双语 CLIP + 多语 T5 + 2D RoPE + MLLM Captioner + 多轮多模态对话生图；其作者报告的对照范围和评分结论见上文评测段落。

4. **HunyuanVideo 的"Dual→Single Stream DiT + Causal 3D VAE + MLLM 文本编码 + 3D RoPE + Full Attention"五件套**
   - 这些组件构成该报告描述的视频生成架构；不同组件的独立贡献和社区采用范围需要分别验证。

5. **HunyuanImage-3.0 的原生多模态混合生成**
   - 文本 token 自回归、图像 latent 扩散；论文 v3 报告总参超过80B、每token激活13B。不同任务路径与 checkpoint revision 的参数口径应分别理解；单个厂商报告不足以建立跨模型规模排名。

6. **HunyuanVideo-1.5 的 SSTA**
   - SSTA 把按块相似度/冗余度筛选出的注意力区域与局部滑动窗口结合；论文在 8×H800 的 10 秒 720p T2V 设置中报告相对 FlashAttention-3 约 1.87× 的端到端加速。它支持“特定配置下降低推理耗时”，不支持与旧版 13B 模型质量等同的结论。

7. **Hunyuan3D 2.0 的 "Shape-DiT + Texture-Paint" 解耦**
   - 把"几何"与"纹理"作为两个独立可扩展的扩散问题分别训练，配合 ShapeVAE；后续 Studio 报告扩展到从概念图到游戏资产的多个生产阶段；该报告没有提供端到端耗时测量。

8. **HunyuanWorld：3D 世界 + 可交互**
   - 将场景生成与交互式世界探索结合；具体输入条件、生成流程和可控性应以对应版本的技术材料为准。

9. **Hunyuan-Vision-1.5 的 "Thinking on Image"**
   - 报告将其描述为结合视觉工具与检索的推理路线；不以未固定日期、版本和评测设置的榜单成绩作结论。

---

## 10. 比较边界

本报告覆盖混元公开论文与模型材料中的语言模型、图像/视频生成、3D/世界建模、VLM、OCR 和翻译。这个范围图描述的是研究主题，不是模型能力排行榜或市场覆盖排名。不同论文采用不同提示集、基线、评审方式和推理预算；未固定同一任务与版本时，不将各方向的分数放在一张横向总表里。

跨厂商比较只在具体论文的实验条件范围内成立。比如 Hunyuan-DiT 的自建人评、Hunyuan-Large 的语言 benchmark、HunyuanVideo 的视频人评、Hunyuan3D 的几何/纹理评价分别测量不同目标，不能合并成一个“混元整体领先”结论。产品名相似、同一发布平台或相同公司归属，也不能证明共享参数、训练数据或推理系统。

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
