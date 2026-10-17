# Google Gemini系列模型深度调研报告

> 调研日期：2026年6月5日（2026-10-17 增补 §9：Gemini 4 Argon）
> 覆盖范围：从PaLM（2022年）到**Gemini 4 Argon（2026 年 9–10 月）**的完整技术演进  
> 写作原则：以**架构演进路径**为骨架，突出原生多模态、超长上下文、MoE与推理能力四大技术主线

---

## 1. 概述与发展时间线

### 1.1 系列定位

Google的大语言模型系列经历了从PaLM到Gemini的重大战略转型。PaLM（Pathways Language Model）代表了Google在Dense Transformer上的极致scaling探索，而Gemini则标志着Google进入**原生多模态+MoE**的新时代。整个系列的核心设计哲学可归纳为：

1. **原生多模态**：Gemini从1.0开始即在预训练阶段联合训练文本、图像、音频、视频，而非后接多模态适配器
2. **MoE高效scaling**：从1.5代起全面转向Sparse MoE架构，实现计算效率与模型容量的最优平衡
3. **超长上下文**：从32K→1M→10M token，实现近乎完美的长程检索与推理
4. **硬件协同设计**：与TPU（v4→v5e→v6e Trillium）深度协同，从Pathways分布式训练系统到模型架构均针对TPU拓扑优化
5. **从对话到Agent**：Gemini 2.0起明确定位"Agentic Era"，2.5/3代实现原生工具调用与长程自主规划

### 1.2 完整发展时间线（2022–2026）

```
2022年 ── PaLM时代：Dense Transformer极致Scaling
├── 04月  PaLM 540B              首个千亿级Dense模型，6144 TPU v4训练（arXiv:2204.02311）
└── 12月  Flan-PaLM              指令微调版本，显著提升zero-shot性能

2023年 ── PaLM 2与Gemini诞生
├── 05月  PaLM 2                 Gecko/Otter/Bison/Unicorn四档，compute-optimal训练
├── 12月  Gemini 1.0             Ultra/Pro/Nano三档，原生多模态，首次超越GPT-4
└── 12月  Gemini Nano            1.8B/3.25B端侧部署模型（Pixel 8 Pro）

2024年 ── 超长上下文与高效推理
├── 02月  Gemini 1.5 Pro         Sparse MoE + 1M token原生上下文（arXiv:2403.05530）
├── 05月  Gemini 1.5 Flash       轻量MoE，知识蒸馏自1.5 Pro
├── 06月  Gemma 2                2B/9B/27B开源，交替Local/Global注意力
├── 12月  Gemini 2.0 Flash       原生多模态输出（图像+音频）+ 原生工具调用
└── 12月  Gemini 2.0 Flash Thinking   实验性推理模型，显示思考过程

2025年 ── 推理革命与Gemini 3
├── 03月  Gemma 3                1B/4B/12B/27B多模态开源，SigLIP视觉编码器，128K上下文
├── 03月  Gemini 2.5 Pro         首个"Thinking Model"，1M上下文，SOTA推理
├── 06月  Gemini 2.5 Flash       高效Thinking模型，平衡速度与成本
├── 06月  Gemini 2.5 Flash-Lite  最低延迟与成本的2.5系列变体
├── 11月  Gemini 3 Pro           最智能模型，LMArena 1501 Elo，1M/64K输入输出
├── 11月  Gemini 3 Deep Think    增强推理模式，GPQA 93.8%，ARC-AGI-2 45.1%
└── 12月  Gemini 3 Flash         高效旗舰，1M上下文，原生多模态输出

2026年 ── 持续突破
├── 02月  Gemini 3.1 Deep Think  金牌级学术推理，物理/数学奥赛水平
├── 02月  Gemini 3.1 Pro         前沿推理模型，ARC AGI 2 达77.1%
├── 05月  Gemini 3.1 Flash Lite  轻量高效版，1M上下文
├── 05月  Gemini 3.5 Flash       Google I/O发布，编码和代理工作流优化，速度4倍快
├── 05月  Gemini Omni Flash      全模态模型，支持视频输出，集成YouTube Shorts
└── 06月  Gemini 3.5 Pro         发布预告，新一代旗舰
```

### 1.3 技术代际划分

| 阶段 | 时间跨度 | 代表模型 | 核心技术标志 | 战略定位 |
|------|----------|----------|--------------|----------|
| **Dense Scaling期** | 2022.04–2023.05 | PaLM / PaLM 2 | 540B Dense + Pathways训练系统 + compute-optimal | 追赶GPT-3.5水平 |
| **原生多模态期** | 2023.12–2024.01 | Gemini 1.0 Ultra/Pro/Nano | 原生多模态联合训练 + 32K上下文 | 首次多任务超越GPT-4 |
| **长上下文+MoE期** | 2024.02–2024.11 | Gemini 1.5 Pro/Flash | Sparse MoE + 1M→10M上下文 + 高效蒸馏 | 长上下文+效率双突破 |
| **Agentic+推理期** | 2024.12–2025.11 | Gemini 2.0/2.5/3 | Thinking模式 + 原生工具调用 + 多模态输出 | Agent时代到来 |
| **深度推理期** | 2025.11– | Gemini 3/3.1/3.5 Deep Think | Deep Think增强推理 + 长程规划 + 1501 Elo + 全模态输出 | AGI前沿探索 |

---

## 2. 基座模型演进

### 2.1 PaLM（2022年4月）

**论文**：*PaLM: Scaling Language Modeling with Pathways*（arXiv:2204.02311）

PaLM是Google首个真正意义上的超大规模Dense LLM，其核心贡献在于证明了在TPU Pod级别高效训练540B参数模型的可行性。

**架构细节**：
- **模型类型**：Decoder-only Transformer
- **参数规模**：8B / 62B / 540B三个尺度
- **训练数据**：780B tokens（多语言语料，涵盖网页、书籍、代码、对话等）
- **训练基础设施**：6144 TPU v4芯片，使用Pathways系统实现跨Pod分布式训练

**关键架构创新**：

| 组件 | 设计选择 | 说明 |
|------|----------|------|
| 注意力 | Multi-Query Attention (MQA) | 所有头共享同一组K/V投影，显著降低推理延迟 |
| 位置编码 | RoPE | 旋转位置编码 |
| FFN激活 | SwiGLU | Swish(xW) · xV，相比ReLU/GeLU显著提升质量 |
| 层结构 | **Parallel Attention + FFN** | 注意力层与FFN并行计算而非串行，训练吞吐提升15% |
| 归一化 | Pre-RMSNorm | 每层前进行RMSNorm |
| Bias | **无bias** | 全部Dense层和LayerNorm均不使用bias |
| 词表 | 256K SentencePiece | 支持多语言 |
| 上下文长度 | 2048 tokens | 早期模型上下文较短 |

**PaLM 540B关键配置**：
- 118层，d_model = 18432，n_heads = 48
- FFN隐层维度 = 4 × 18432（SwiGLU使实际参数量翻倍）
- 训练使用2-way Pod级数据并行 + 模型并行

**Pathways系统**：Google自研的分布式ML训练框架，核心特点是：
- 单个Python客户端控制所有6144芯片
- 支持异步分布式数据流
- 跨数据中心TPU Pod级别的高效通信
- 为后续Gemini训练奠定基础设施基础

### 2.2 PaLM 2（2023年5月）

**论文**：*PaLM 2 Technical Report*（arXiv:2305.10403）

PaLM 2的核心理念转变为**compute-optimal training**（遵循Chinchilla scaling law），不再单纯追求参数量最大化。

**关键改进**：
- **Compute-Optimal**：相比PaLM使用更多训练数据、相对更小的模型尺寸，实现更好的性能/成本平衡
- **多语言增强**：训练数据中多语言比例大幅提升，覆盖100+语言
- **推理增强**：数据混合中增加科学论文和数学推导内容
- **代码增强**：代码语料占比显著提升

**尺寸分档**：
| 代号 | 定位 | 典型应用 |
|------|------|----------|
| Gecko | 最小，端侧 | 移动设备 |
| Otter | 中小 | 轻量级应用 |
| Bison | 中等 | API标准层 |
| Unicorn | 最大 | 旗舰能力 |

**架构延续**：保持PaLM的Decoder-only Transformer基本设计（MQA、SwiGLU、RoPE、Parallel层），但具体参数配置未公开。

**与PaLM的关键差异**：
- 训练数据量大幅增加（具体未公布，估计数倍于780B tokens）
- 数据混合比例优化（更多多语言、推理、代码数据）
- 遵循Chinchilla optimal而非单纯scale参数

### 2.3 Gemini 1.0（2023年12月）

**论文**：*Gemini: A Family of Highly Capable Multimodal Models*（arXiv:2312.11805）

Gemini 1.0是Google从"语言模型"向"多模态模型"的战略转型标志，其最核心的突破在于**原生多模态预训练**。

**模型分档**：
| 变体 | 定位 | 参数规模 | 上下文 |
|------|------|----------|--------|
| Ultra | 旗舰，最强能力 | 未公布（推测>1T） | 32K |
| Pro | 生产部署，性能与效率平衡 | 未公布 | 32K |
| Nano-1 | 端侧部署 | 1.8B | 较短 |
| Nano-2 | 端侧部署 | 3.25B | 较短 |

**核心架构**：
- **模型类型**：Decoder-only Transformer
- **多模态输入**：文本、图像、音频、视频均通过编码后的token序列输入共享的Transformer decoder
- **词表**：256K SentencePiece（联合编码文本、代码、图像token）
- **位置编码**：RoPE
- **归一化**：RMSNorm
- **FFN激活**：GeGLU（类似SwiGLU的Gated Linear Unit变体）
- **注意力**：Multi-Head Attention（部分变体使用Multi-Query Attention）

**原生多模态训练**：
与GPT-4V等"先训练语言模型再接视觉编码器"的方案不同，Gemini 1.0从预训练第一步起就在文本+图像+音频+视频的混合数据上联合训练。这意味着：
- 模型内部的表征空间天然融合了多种模态
- 跨模态推理能力更强（如从图像推理出文字含义）
- 不存在"模态对齐"的后训练gap

**训练基础设施**：
- 使用多个4096-chip TPU v4 Pod
- 跨多个数据中心分布式训练
- Pathways系统驱动

**标杆性能**：
- MMLU: 90.0%（首次超越GPT-4的86.4%）
- GSM8K: 94.4%
- HumanEval: 74.4%
- 在30/32个评测任务上达到SOTA

### 2.4 Gemini 1.5 Pro（2024年2月）

**论文**：*Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context*（arXiv:2403.05530）

Gemini 1.5是整个系列的**架构转折点**——从Dense转向Sparse MoE，同时将上下文长度从32K一跃提升至1M（实验性10M）。

**核心架构**：
- **模型类型**：Sparse Mixture-of-Experts (MoE) Transformer
- **路由机制**：Learned routing function，将输入引导至参数子集处理
- **Conditional Computation**：总参数量巨大但每次前向传播仅激活一小部分
- **上下文窗口**：原生支持1M tokens，实验性支持10M tokens
- **多模态**：继承Gemini 1.0的原生多模态能力

**MoE设计（基于Google长期MoE研究）**：
Google在MoE领域有深厚积累：
- Shazeer et al. (2017): 最早的MoE for NLP
- GShard (Lepikhin et al., 2020): 分布式MoE
- Switch Transformer (Fedus et al., 2021): 简化MoE路由
- GLaM (Du et al., 2022): 1.2T参数MoE
- ST-MoE (Zoph et al., 2022): 稳定MoE训练

Gemini 1.5 Pro的MoE是这些研究的集大成者，实现了：
- 模型总参数量远大于激活参数量（估计总参数数千亿，激活参数数百亿级别）
- 训练和推理效率远优于同等能力的Dense模型
- 相比Gemini 1.0 Ultra用更少计算达到相近甚至更优性能

**长上下文能力（详见第5章）**：
- Text Haystack: 1M tokens达到99.7%召回率，10M tokens达到99.2%
- Video Haystack: 10.5小时视频中完美检索
- Audio Haystack: 超过107小时音频
- NLL在1M tokens内持续下降（遵循power-law）

**性能对比**：
- vs Gemini 1.0 Pro: 29/33个benchmark胜出（87.9% win rate）
- vs Gemini 1.0 Ultra: 19/33个benchmark胜出（57.6% win rate），尽管使用的训练计算量显著更少

### 2.5 Gemini 1.5 Flash（2024年5月）

**定位**：高效率部署模型，从Gemini 1.5 Pro知识蒸馏而来。

**关键特点**：
- Sparse MoE架构（同Pro）
- 1M token上下文窗口
- 知识蒸馏：从Pro模型蒸馏核心能力到更小、更快的模型
- 延迟和成本显著低于Pro
- 适合大规模部署和低延迟场景

### 2.6 Gemini 2.0 Flash（2024年12月）

**定位**：Agentic Era的开端模型。

**核心突破**：
- **原生多模态输出**：首次支持原生图像生成和音频输出（不仅是理解）
- **原生工具调用（Native Tool Use）**：模型可直接调用Google搜索、代码执行等工具
- **1M token上下文**
- **多语言原生音频输出**：Text-to-Speech with fine-grained control

**训练基础设施**：
- 使用TPU v6e（Trillium）训练
- Trillium相比v5e：训练性能提升4×，推理提升3×

### 2.7 Gemini 2.5 Pro / Flash（2025年3月/6月）

**论文**：*Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities*（arXiv:2507.06261）

**核心定位**：首代"Thinking Model"，将推理过程显式化。

**架构信息**：
- MoE架构，每次前向传播激活约**40B参数**
- 1M token上下文窗口（2M逐步开放）
- 支持最多3小时视频处理
- 512K text + 多小时音视频混合输入

**Thinking模式**：
- 模型在生成答案前先进行内部"思考过程"
- 显著提升多步推理和规划能力
- 动态思考：根据问题复杂度自动调整思考深度
- 用户可通过参数控制思考token预算

**2.5 Pro关键性能**：
- GPQA Diamond: ~90%+
- Aider Polyglot (coding): 极具竞争力
- Humanity's Last Exam: 领先
- SWE-bench Verified: 强劲
- LMArena: 连续6个月排名第一

**2.5 Flash**：
- 2025年6月17日GA发布
- 设计目标：速度+低成本的Thinking模型
- 内建思考能力
- 相比Pro大幅降低延迟和成本

**2.5 Flash-Lite**：
- 2.5系列中最低延迟和成本
- 面向成本敏感的大规模部署

### 2.8 Gemini 3 Pro / Deep Think / Flash（2025年11月–12月）

**定位**：Google迄今最智能模型系列。

**Gemini 3 Pro（2025-11-18）**：
- **LMArena**: 1501 Elo（突破性分数）
- **GPQA Diamond**: 91.9%（PhD级推理）
- **Humanity's Last Exam**: 37.5%（无工具）
- **MathArena Apex**: 23.4%（数学SOTA）
- **MMMU-Pro**: 81%（多模态推理）
- **Video-MMMU**: 87.6%
- **SimpleQA Verified**: 72.1%（事实准确性）
- **SWE-bench Verified**: 76.2%
- **WebDev Arena**: 1487 Elo
- **Terminal-Bench 2.0**: 54.2%
- **上下文窗口**：1M输入 + 64K输出
- **图像侧衍生产品 Nano Banana Pro**（= Gemini 3 Pro Image，2025-11-20 官方博客口径；arXiv:2604.20329 正文本身只写 "Nano Banana Pro"）被 Google 拿去做 instruction-tuning 得到 Vision Banana，"生成即理解"的精读见 [Google-Gen 分册](../Google-Gen/papers/2604.20329-vision-banana.md)。

**Gemini 3 Flash（2025-12-17）**：
- 高效旗舰变体，1M token上下文窗口
- 原生多模态输出能力
- 在速度和成本上优化，适合大规模部署

**Gemini 3 Deep Think（2026-02-12）**：
- 增强推理模式，比3 Pro更进一步
- Humanity's Last Exam: 41.0%
- GPQA Diamond: 93.8%
- **ARC-AGI-2: 45.1%**（with code execution，验证集）
- 解决高度新颖的挑战

**Gemini 3.1 Pro（2026-02-19）**：
- 前沿推理模型，全面超越3 Pro
- **ARC-AGI-2 达77.1%**，推理能力大幅提升
- 推理、多模态、Agent能力全面提升
- 1M token上下文窗口

**Gemini 3.1 Deep Think（2026年初）**：
- 全面超越3 Pro
- Deep Think Feb 2026变体达到金牌级学术推理
- 2025年国际物理奥林匹克笔试金牌水平

### 2.9 Gemini 3.5系列与Omni Flash（2026年5月–6月）

**Gemini 3.5 Flash（2026-05-19）**：
- **发布场合**：Google I/O 2026
- **定位**：新工作马，编码和代理工作流优化
- **性能**：比Gemini 3.1 Pro在编码和代理基准上更强
- **速度**：4倍快于前代旗舰
- **成本**：1/3 of GPT-5.5
- **上下文窗口**：1M token

**Gemini Omni Flash（2026-05-19）**：
- **定位**：全模态模型
- **关键能力**：支持视频输出（原生视频生成）
- **集成**：已集成到YouTube Shorts
- **上下文窗口**：1M token

**Gemini 3.5 Pro（2026-06 announced）**：
- 6月发布预告，新一代旗舰
- 预计继承3.5 Flash的编码/代理优化并扩展至全能力维度

### 2.10 思考级别与上下文统一

**4个思考级别**：
所有Gemini 3/3.1/3.5系列模型均支持4级思考控制：
- **minimal**：最小思考，最低延迟
- **low**：低思考深度，平衡速度
- **medium**：中等思考深度（默认）
- **high**：最大思考深度，最佳推理质量

**统一1M token上下文**：
从Gemini 3系列开始，所有模型（Pro/Flash/Deep Think/Omni）均标配1M token上下文窗口，实现长文档、长视频、长代码库的统一处理。

### 2.11 跨代架构对比表

| 组件 | PaLM (2022) | PaLM 2 (2023) | Gemini 1.0 (2023.12) | Gemini 1.5 (2024.02) | Gemini 2.0 (2024.12) | Gemini 2.5 (2025.03) | Gemini 3 (2025.11) | Gemini 3.1 (2026.02) | Gemini 3.5 (2026.05) |
|------|-------------|---------------|----------------------|----------------------|----------------------|----------------------|--------------------|----------------------|----------------------|
| 架构 | Dense Decoder | Dense Decoder | Dense Decoder | **Sparse MoE** | MoE/Dense | MoE | MoE | MoE | MoE |
| 注意力 | MQA | MQA | MHA/MQA | MoE+MHA | MoE+MHA | MoE+MHA | MoE+MHA | MoE+MHA | MoE+MHA |
| 位置编码 | RoPE | RoPE | RoPE | RoPE | RoPE | RoPE | RoPE | RoPE | RoPE |
| FFN | SwiGLU | SwiGLU | GeGLU | MoE-GeGLU | MoE-GeGLU | MoE-GeGLU | MoE-GeGLU | MoE-GeGLU | MoE-GeGLU |
| 归一化 | Pre-RMSNorm | Pre-RMSNorm | Pre-RMSNorm | Pre-RMSNorm | Pre-RMSNorm | Pre-RMSNorm | Pre-RMSNorm | Pre-RMSNorm | Pre-RMSNorm |
| 词表 | 256K SP | 256K SP | 256K SP | 256K SP | 256K SP | 256K SP | 256K SP | 256K SP | 256K SP |
| 上下文 | 2K→8K | 8K→32K | 32K | **1M (10M实验)** | 1M | 1M (2M开放) | **1M统一** | **1M统一** | **1M统一** |
| 多模态 | 纯文本 | 纯文本 | **原生多模态** | 原生多模态 | **原生输出** | 原生输出 | 原生输出 | 原生输出 | **原生视频输出** |
| 推理模式 | — | — | — | — | Flash Thinking | **Thinking** | **Deep Think** | **Deep Think** | **4级思考** |
| 训练硬件 | TPU v4 | TPU v4 | TPU v4 | TPU v4 | **TPU v6e** | TPU v6e+ | TPU v6e+ | TPU v7 | TPU v7 |
| 激活参数 | 540B (全量) | 未公布 | 未公布 | 部分激活 | 部分激活 | ~40B | 未公布 | 未公布 | 未公布 |

---

## 3. 多模态架构设计

### 3.1 设计理念：原生多模态 vs 后接多模态

Google Gemini系列的多模态设计理念与其他主流方案有根本区别：

| 方案 | 代表 | 方法 | 局限性 |
|------|------|------|--------|
| 后接编码器 | GPT-4V, Qwen-VL | 先训练LLM，再接视觉编码器 | 模态间存在对齐gap |
| **原生联合训练** | **Gemini** | 从头开始在多模态混合数据上训练 | 训练成本高但效果更好 |

### 3.2 Gemini多模态架构细节

**输入处理**：
- **文本**：256K SentencePiece tokenizer
- **图像**：转换为离散视觉token序列，与文本token交错输入decoder
- **音频**：原生音频理解，转换为audio token序列
- **视频**：按帧采样（如1 FPS），每帧转为视觉token，支持多小时视频

**Decoder统一处理**：
- 所有模态token通过type embedding区分
- 共享同一个decoder-only Transformer处理
- 自注意力机制跨模态建立关联
- 输出通过不同head生成对应模态（文本/图像/音频）

**Gemini 2.0+的原生多模态输出**：
- 不仅能理解多模态输入，还能**原生生成**图像和音频
- Text-to-Speech: 多语言原生语音输出，支持细粒度控制
- Image Generation: 原生图像生成能力

### 3.3 Gemini在不同模态上的表现

**视觉理解**：
- 自然图像、文档、图表、公式OCR
- 空间推理与物体关系理解
- 视频时序理解（精确到秒级时间戳）

**音频理解**：
- 语音识别（ASR）
- 音频事件检测
- 音乐理解

**跨模态推理**：
- 从手绘草图定位长文档中的场景（如Les Misérables中的场景定位）
- 从视频中回答需要推理的问题
- 图文交错理解与生成

---

## 4. 长上下文技术

### 4.1 长上下文发展路径

```
PaLM:       2K tokens
PaLM 2:     8K → 32K tokens
Gemini 1.0: 32K tokens
Gemini 1.5: 1M tokens (10M实验性)
Gemini 2.0+: 1M tokens (标准)
```

### 4.2 Gemini 1.5的长上下文技术实现

Gemini 1.5 Pro在长上下文方面取得了突破性进展，核心技术包括：

**4.2.1 MoE对长上下文的支持**

Sparse MoE架构天然有利于长上下文：
- 每个token仅激活部分参数，降低了序列长度增加带来的计算量增长
- 专家路由可以学习到不同上下文距离的模式
- 总模型容量（记忆能力）远大于激活参数量

**4.2.2 注意力机制优化**

- **层级注意力（Hierarchical Attention）**：结合窗口注意力、全局token和学习压缩
- **Gist Tokens（摘要token）**：学习对旧上下文进行压缩表示，超过一定长度后用learned summary representations替代
- **上下文压缩**：在context compression ratio和retrieval fidelity间做trade-off

**4.2.3 训练与推理的工程优化**

- 使用多个4096-chip TPU v4 Pod跨数据中心训练
- 支持将长序列分布到多个设备上处理
- 推理时支持增量式KV-cache管理

### 4.3 长上下文评估结果

**Needle-in-a-Haystack（文本）**：
| 上下文长度 | 召回率 |
|-----------|--------|
| 200K tokens | 100% |
| 530K tokens | 100% |
| 1M tokens | 99.7% |
| 10M tokens | 99.2% |

**视频检索**：
- 10.5小时视频（37994帧 at 1FPS，9.9M tokens）中检索嵌入信息：完美召回

**音频检索**：
- 107小时音频（9.7M tokens）中检索隐藏关键词：完美召回

**Perplexity曲线**：
- NLL在1M tokens内单调递减（文档数据）
- NLL在2M tokens内单调递减（代码数据）
- 遵循 L(x) = αx^β + γ 的power-law结构
- 证明模型确实能利用数百万token前的信息

### 4.4 vs 竞品对比

| 模型 | 最大上下文 | 1M tokens召回 |
|------|-----------|--------------|
| Gemini 1.5 Pro | 10M | 99.7% |
| Claude 2.1 | 200K | 98%（at 200K） |
| GPT-4 Turbo | 128K | 支持 |
| Gemini 2.5 Pro | 1M (2M rolling) | — |
| Gemini 3/3.1/3.5 系列 | **1M统一** | — |
| Gemini Omni Flash | **1M + 视频输出** | — |

---

## 5. 推理能力演进

### 5.1 推理能力发展路径

```
Gemini 1.0/1.5:    标准自回归生成（无显式推理）
Gemini 2.0 Flash Thinking (2024.12):  实验性Thinking模式
Gemini 2.5 Pro/Flash (2025.03/06):    正式Thinking Model
Gemini 3 Pro (2025.11):               SOTA推理 + Deep Think模式
Gemini 3.1 Pro (2026.02):             前沿推理，ARC AGI-2 77.1%
Gemini 3.5 Flash (2026.05):           4级思考控制（minimal/low/medium/high）
```

### 5.2 Gemini 2.0 Flash Thinking

- 2024年12月发布的实验性模型
- 基于Gemini 2.0 Flash的速度和性能
- 训练使用"思考"来增强推理
- 生成过程包含模型的思考过程（thinking trace）
- 由Jeff Dean发布，标志Google正式进入reasoning model竞赛

### 5.3 Gemini 2.5: 正式Thinking Model

**设计理念**：
- Thinking model = 在回答前进行内部推理过程
- 与OpenAI o1/o3、DeepSeek-R1类似的思考链方法
- 但集成于Gemini的原生多模态框架中

**技术特点**：
- **动态思考（Dynamic Thinking）**：模型根据问题复杂度自动调整推理深度
- **思考预算控制**：开发者可设置最大思考token数
- **多模态推理**：思考过程可以涉及视觉、音频等多模态信息

**性能突破（Gemini 2.5 Pro）**：
- 连续6个月LMArena第一
- 编码、数学、推理benchmark全面领先
- SoTA级别的Aider Polyglot编码评测
- GPQA Diamond和Humanity's Last Exam极具竞争力

### 5.4 Gemini 3 Deep Think

**Deep Think vs Standard Thinking**：
- Deep Think是比标准Thinking更深层的推理模式
- 允许模型在更长时间内进行更深入的推理链
- 类似于"extended thinking"但更注重推理深度和准确性

**代表性成就**：
- 2025年国际数学奥林匹克金牌（Gemini 2.5 Deep Think阶段，2025年7月）
- 2025年国际编程竞赛金牌（2025年9月）
- 2025年国际物理奥林匹克笔试金牌水平（Gemini 3.1 Deep Think）
- ARC-AGI-2: 45.1%（含代码执行，前所未有的新颖问题解决能力）

**Deep Think技术方向**（基于公开信息推断）：
- Parallel-thinking tree search（并行思考树搜索）
- Adversarial self-critique（对抗性自我批评）
- Neuro-symbolic verification（神经符号验证）
- 长程推理链中的一致性维护

---

## 6. Gemma开源系列

### 6.1 系列概览

Gemma是Google基于Gemini研究和技术开发的开源小模型系列，目标是将Gemini的核心架构创新以开源形式带给社区。

| 版本 | 发布时间 | 参数规模 | 多模态 | 上下文 | 关键特性 |
|------|----------|----------|--------|--------|----------|
| Gemma 1 | 2024.02 | 2B, 7B | 否 | 8K | 基础开源LLM |
| CodeGemma | 2024.06 | 2B, 7B | 否 | 8K | 代码专用 |
| Gemma 2 | 2024.06 | 2B, 9B, 27B | 否 | 8K | 架构创新 |
| Gemma 3 | 2025.03 | 1B, 4B, 12B, 27B | **是** | **128K** | 多模态+长上下文 |

### 6.2 Gemma 1（2024年2月）

**论文**：*Gemma: Open Models Based on Gemini Research and Technology*（arXiv:2403.08295）

**架构**：
- Decoder-only Transformer
- 继承Gemini Pro/Ultra的核心架构motif
- Multi-Head Attention
- RoPE位置编码
- GeGLU激活函数
- RMSNorm

**训练**：
- 从Gemini训练流程中衍生
- 使用高质量预训练数据
- SFT + RLHF后训练

**性能**：
- Gemma 7B在MMLU达到64.3%
- HumanEval pass@1: 32.3%
- 同规模开源模型中最佳

### 6.3 Gemma 2（2024年6月）

**论文**：*Gemma 2: Improving Open Language Models at a Practical Size*（arXiv:2408.00118）

**核心架构创新**：

**1. 交替Local/Global注意力（Alternating Local-Global Attention）**：
- **Local Attention层**：滑动窗口大小4096 tokens
- **Global Attention层**：全注意力范围8192 tokens
- 两种层交替排列，兼顾效率与全局信息
- 减少了全序列注意力的计算开销

**2. Logit Soft-Capping**：
- 在attention logits上应用soft-capping（tanh压缩）
- 防止attention分数过大导致的数值不稳定
- 提升训练稳定性

**3. 知识蒸馏（Knowledge Distillation）**：
- 从更大的Gemini模型蒸馏知识
- 蒸馏作为核心训练信号（而非可选增强）
- 实现了小模型超越同规模独立训练模型的性能

**配置详情**：
| 模型 | 层数 | d_model | n_heads | KV_heads | FFN | 参数量 |
|------|------|---------|---------|----------|-----|--------|
| Gemma 2 2B | 26 | 2304 | 8 | 4 | 9216 | 2.6B |
| Gemma 2 9B | 42 | 3584 | 16 | 8 | 14336 | 9.2B |
| Gemma 2 27B | 46 | 4608 | 32 | 16 | 36864 | 27.2B |

### 6.4 Gemma 3（2025年3月）

**论文**：*Gemma 3 Technical Report*（arXiv:2503.19786）

**关键突破**：Gemma系列首次引入**多模态能力**。

**多模态架构**：
- **视觉编码器**：定制SigLIP（Sigmoid Loss for Image-text Pre-training）
- 4B/12B/27B模型共享同一SigLIP编码器
- 1B模型为纯文本
- 视觉token通过cross-attention或prefix方式注入decoder
- 支持Pan & Scan策略处理不同分辨率图像

**其他关键特性**：
- **128K token上下文**（4B/12B/27B）
- **32K token上下文**（1B）
- **140+语言支持**
- **开放权重 + 商用许可**

**训练方法**：
- 知识蒸馏作为**核心预训练信号**（而非后训练增强）
- 从Gemini大模型蒸馏
- Pre-trained和Instruction-tuned版本均显著超越Gemma 2

**性能**：
- 27B模型在多项benchmark上与更大模型竞争
- 视觉理解能力在同规模开源模型中领先
- 多语言能力覆盖140+语言

---

## 7. 跨代技术演进分析

### 7.1 从Dense到MoE的架构转型

| 维度 | Dense时代 (PaLM) | MoE时代 (Gemini 1.5+) |
|------|-------------------|------------------------|
| 参数效率 | 所有参数每次都激活 | 仅激活部分参数 |
| Scaling策略 | 增大模型尺寸 | 增加专家数量 |
| 计算成本 | 与参数量成正比 | 与激活参数量成正比 |
| 训练效率 | 较低 | 显著更高 |
| 推理延迟 | 与参数量成正比 | 可控（与激活量相关） |

**转型动因**：
- Chinchilla scaling law表明需要更多数据+适当模型尺寸
- MoE允许在固定计算预算下拥有更大的"知识容量"
- Google在MoE领域有7年以上研究积累（GShard→Switch→GLaM→ST-MoE→Gemini 1.5）

### 7.2 多模态能力的深化

```
PaLM/PaLM2:         纯文本
Gemini 1.0:          原生多模态理解（文本+图像+音频+视频输入）
Gemini 1.5:          原生多模态 + 超长多模态上下文
Gemini 2.0:          原生多模态输入 + 原生多模态输出（图像/音频生成）
Gemini 2.5/3:        全模态理解+生成 + 工具调用
Gemini 3.5/Omni:     全模态理解+生成 + 原生视频输出 + YouTube集成
```

### 7.3 推理能力的跃迁

| 阶段 | 模型 | 推理方式 | 代表能力 |
|------|------|----------|----------|
| 基线推理 | Gemini 1.0/1.5 | 标准自回归 | 遵循指令、基本CoT |
| 显式推理 | 2.0 Flash Thinking | Thinking trace | 可见思考过程 |
| 深度推理 | 2.5 Pro | Dynamic Thinking | 自适应推理深度 |
| 专家推理 | 3 Deep Think | Extended Deep Think | 奥赛金牌级 |
| 前沿推理 | 3.1 Pro | ARC AGI-2 77.1% | 接近人类水平 |
| 工作马优化 | 3.5 Flash | 4级思考 + 编码/代理优化 | 速度4×，成本1/3 GPT-5.5 |

### 7.4 从对话到Agent

```
Gemini 1.0/1.5:   被动响应式对话
Gemini 2.0:       原生工具调用 → "Agentic Era"开端
Gemini 2.5:       长程规划 + 持续推理
Gemini 3:         自主多步骤任务执行（SWE-bench 76.2%）+ Vending-Bench长程规划SOTA
Gemini 3.5 Flash: 编码和代理工作流优化，比3.1 Pro在编码/代理基准上更强
```

### 7.5 TPU硬件协同演进

| TPU版本 | 时间 | 关键特性 | 对应模型 |
|---------|------|----------|----------|
| TPU v4 | 2022 | 4096-chip Pod，ICI互连 | PaLM, Gemini 1.0/1.5 |
| TPU v5e | 2023 | 2.5×吞吐/美元(vs v4) | 推理优化 |
| TPU v6e (Trillium) | 2024 | 4×训练/3×推理(vs v5) | Gemini 2.0+ |
| TPU v7+ | 2025-2026 | 下一代 | Gemini 3/3.1 |

**协同设计**：
- Pathways系统针对TPU Pod拓扑优化通信模式
- MoE路由与TPU chip间通信带宽匹配
- 模型并行策略与TPU互连拓扑适配
- 长序列训练的KV-cache分布策略与TPU HBM匹配

---

## 8. 关键创新点总结

### 8.1 十大核心创新

1. **原生多模态预训练**：Gemini系列从1.0起就在多模态混合数据上从头联合训练，避免了"先语言后多模态"的对齐gap，是其区别于GPT-4V等模型的根本性设计差异

2. **Sparse MoE大规模化**：Gemini 1.5将Google近十年MoE研究（GShard/Switch/GLaM/ST-MoE）工程化落地，实现了超大容量模型的高效训练与推理

3. **1M→10M超长上下文**：通过MoE+层级注意力+Gist Tokens等技术组合，实现10M token级别的近乎完美检索，且遵循context-length power law

4. **Pathways分布式训练系统**：单Python客户端控制数千TPU芯片，跨数据中心的异步分布式数据流，为超大规模模型训练提供了工程基础

5. **PaLM的Parallel Attention+FFN**：将注意力层和FFN并行化而非串行，在不损失质量的前提下提升15%训练吞吐

6. **Dynamic Thinking Mode**：Gemini 2.5引入的自适应推理深度机制，模型根据问题难度自动决定"思考多久"

7. **原生多模态输出**：Gemini 2.0首次实现文本→图像/音频的原生生成（非外接生成模型），使模型成为真正的"全模态"系统

8. **Gemma知识蒸馏方法论**：将蒸馏作为核心预训练信号（而非后训练增强），使开源小模型显著超越同规模独立训练模型

9. **Gemma 2的Local/Global交替注意力**：交替使用4096窗口滑动注意力和8192全局注意力，在效率和全局信息获取间取得平衡

10. **TPU-Model协同设计**：模型架构（MoE专家数/路由/并行策略）与TPU硬件拓扑（Pod互连/HBM带宽）深度匹配

### 8.2 Google路线 vs OpenAI/Meta路线对比

| 维度 | Google (Gemini) | OpenAI (GPT) | Meta (LLaMA) |
|------|----------------|--------------|--------------|
| 多模态方式 | 原生联合训练 | 后接编码器 | 后接编码器(LLaMA 3.2) |
| 规模策略 | MoE (1.5起) | Dense→MoE(??) | Dense为主 |
| 长上下文 | 1M-10M原生 | 128K-200K | 128K |
| 硬件 | 自研TPU | NVIDIA GPU | NVIDIA GPU |
| 推理方法 | Dynamic Thinking | o1/o3 CoT | 无显式推理(开源) |
| 开源策略 | Gemma系列(小模型) | 不开源 | 全面开源 |

---

## 9. 新模型补录（2026-10）：Gemini 4 Argon

> **本节的定位**：原报告写于 2026-06-05，覆盖到 Gemini 3.5（2026-05）。本节只做**增量补录**，不改写前八章的既有结论；凡与前文冲突处，本节注明冲突并给出依据。
> **证据等级**：`[摘要级]`（官方博客／官方推文／评测平台页面直接可读）；`[二手]`（媒体转述）；`[未确证]`（找不到一手来源）。
> **检索日期**：2026-10-17。

### 9.1 发布与可得性

| 项 | 内容 | 证据等级 |
|---|---|---|
| 模型名 | **Gemini 4 Argon**（官方路由名 `gemini-4-argon`） | `[摘要级]`（官方博客标题）|
| 官方发布口径 | Google 官方账号 2026-10-13 宣布"rolling out now in the Gemini app" | `[摘要级]`（官方推文）|
| 评测平台标注 | Artificial Analysis 页面标注 **Released September 2026** | `[摘要级]`（平台页面）|
| **日期冲突** | 官方推文 10-13 与平台标注 "September 2026" 不一致 → **本报告以"2026 年 9–10 月"区间记录，不单选** | `[未确证]` |
| 可得渠道 | Gemini App（AI Ultra / Pro 订阅）、Google AI Studio、Gemini API、Google Antigravity（含 CLI） | `[摘要级]`（媒体转述官方说明）|
| 开源 | **无**（闭源；权重未公开） | `[摘要级]` |

### 9.2 规格与定价

| 维度 | 数值 | 条件 / 口径 |
|---|---|---|
| 架构 | **原生多模态 Sparse MoE**（媒体称"ground-up，非前代微调"）| `[二手]`；官方未公开专家数/总参数量 |
| 上下文 | **1M tokens**（输入+输出合计上限，平台口径）| Artificial Analysis 页面；官方"long decode（1M output）"指南佐证输出侧可长 |
| 输入模态 | **文本 + 高分辨率图像 + 音频 + 视频** | `[二手]`（媒体转述）；AA 页面只标 text+image，**二者口径不一致，需以 API 文档复核** |
| 输出模态 | **文本** | Artificial Analysis 页面 |
| 推理形态 | **有 reasoning 变体**（AA 页面标注 "High" 档为推理版）| AA 页面 |
| 价格（输入）| **\$2.00 / 1M tokens** | AA 页面 + 媒体一致 |
| 价格（输出）| **\$10.00 / 1M tokens** | 同上 |
| 缓存折扣 | **95%**（命中缓存的输入 token）| AA 页面 |
| 单任务成本 | **\$1.99 / 次**（在 AA Intelligence Index 上的加权成本）| AA 页面测算，非厂商报价 |

> **定价读法**：`\$2 / \$10` 属于"前沿能力 + 中位价格"组合（AA 给出的同价位中位数恰为 \$2 / \$10）。**不要**把它读成"便宜"——它只是**没有对旗舰能力加价**；对长上下文、长输出任务，成本仍随 token 线性上升。

### 9.3 评测（必须带条件读）

| 指标 | 数值 | 条件 / 口径 | 证据等级 |
|---|---|---|---|
| **AA Intelligence Index** | **53**（**#8 / 217**）| AA v4.3.2，10 项评测：AA-Briefcase v1.1、GDPval-AA v2.1、AutomationBench-AA、Terminal-Bench 4.0、SciCode、Humanity's Last Exam、GDP.pdf、CritPt、AA-Omniscience、AA-LCR v1.1；**推理档（High）** | `[摘要级]` |
| 成本效率 | \$1.99 / 任务；**#83 / 114**（成本维度）| 同一 AA Index 口径 | `[摘要级]` |
| 输出冗长度 | **110M tokens**（AA 中位 85M）| 跑完整 Index 的累计输出 token，越高越"啰嗦" | `[摘要级]` |
| **Vals Index** | **#1**（经济场景精度：企业财务/企业编码/法律取证/税务合规）| 媒体转述官方口径，**未见榜单原始快照** | `[二手]` |
| **ERQA（具身推理）** | **87%** | 媒体转述官方口径，**未给样本数与评分脚本** | `[二手]` |
| 内部工程收益 | agentic code 提交 **+35%**；post-submit 回滚 **−30%** | Google/Antigravity 自报，**在自家 Chromium 6M 行遗留目录重构任务上** | `[二手]`（官方推文转述）|

**三条必须一起读的条件**：
1. **AA 53 分是"推理档（High）"**——非推理档若不是同一模型，不能直接拿 53 与别家非推理档比；
2. **Vals/ERQA 都是厂商口径**，且 ERQA 87% 没有样本数与评分脚本，**只能当"作者声称的上界"**；
3. **+35% / −30% 是内部任务**（Chromium 重构），与公开基准不可混算。

### 9.3b 成本模型（用 §9.2 的报价复算，不给结论只给算式）

单价：输入 **\$2.00/1M**、输出 **\$10.00/1M**、缓存命中折扣 **95%**（即缓存输入按 \$0.10/1M 计，若折扣作用于全部输入；**折扣适用范围未确证**，见 §9.7）。

| 负载形态 | 输入 tokens | 输出 tokens | 未命中缓存成本 | 全命中缓存成本 | 说明 |
|---|---:|---:|---:|---:|---|
| 单轮长文档问答（RAG） | 100,000 | 2,000 | \$0.22 | \$0.03 | 输入主导；缓存收益极大 |
| Agent 单任务 20 轮（每轮输入 30,000、输出 800） | 600,000 | 16,000 | \$1.36 | \$0.10 | 多轮下**缓存是否跨轮生效未确证**，上界按下界算 |
| 一次满额长解码 | 20,000 | 1,000,000 | \$10.04 | \$10.00 | 输出主导；**"1M 输出"不便宜** |
| 批量评测（AA Index 口径） | — | 110,000,000 | 约 \$1.10k（仅输出） | — | 对应 AA 的"110M 输出 token"冗长度口径 |

> **读法**：这三档说明 4 Argon 的**成本结构由输出 token 主导**；对"读长文档、写短答案"的任务便宜，对"长解码/长报告"的任务昂贵。任何"降价 X 倍"的说法都必须先说明参照物与缓存命中率。

### 9.3c 评测方法学（AA Index v4.3.2 的构成与限制）

AA Intelligence Index v4.3.2 记录的 10 项：**AA-Briefcase v1.1、GDPval-AA v2.1、AutomationBench-AA、Terminal-Bench 4.0、SciCode、Humanity's Last Exam、GDP.pdf、CritPt、AA-Omniscience、AA-LCR v1.1**。

| 维度 | 这套题覆盖什么 | 不覆盖什么（因此不能外推） |
|---|---|---|
| 经济/办公 | Briefcase、GDPval、GDP.pdf | 行业专有流程、合规审计 |
| 编码/终端 | Terminal-Bench 4.0、SciCode | 大型遗留仓库重构（即 §9.3 提到的 Chromium 那类任务）|
| 科学/推理 | HLE、CritPt | 长程多轮实验设计 |
| 长上下文 | AA-LCR v1.1 | 1M 满额检索、跨文档一致性 |
| 检索/知识 | AA-Omniscience | 时敏事实（榜单有版本滞后）|

**结论**：53 分是"在这 10 项上的加权结果"，**不含多模态、不含 agent 长程、不含 1M 满额**——这正是我们把 ERQA/Vals 单列的原因。

### 9.3d 与同价位模型的位置（只看 AA 给出的相对位置，不做跨榜排名）

AA 页面同时给出：同价位（\$2 输入 / \$10 输出）的中位数为 **27 分**、中位冗长度 **85M tokens**、中位成本 **\$1.99/任务**。

| 维度 | Gemini 4 Argon (High) | 同价位中位 | 相对位置 |
|---|---:|---:|---|
| AA Index | 53 | 27 | 约 2× 中位（**同价位内**）|
| 输出冗长 | 110M | 85M | 偏啰嗦（+29%）|
| 单任务成本 | \$1.99 | \$1.99 | 持平 |

> **边界**：这是**同价位分层内**的比较，不是"总体第一梯队"的证明；跨价位比较要另做加权。

### 9.2b 架构主张的可判定含义（只写能被现有一手材料支持的部分）

媒体的"原生多模态 Sparse MoE"是一句**架构类别**描述，不是可复核的细节。把它拆成能判与不能判两部分：

| 主张 | 可判定性 | 依据/缺口 |
|---|---|---|
| Sparse MoE（稀疏激活）| **不可判定** | 官方未公开专家数、激活参数、路由策略；媒体转述无出处 |
| 原生多模态（同一模型处理多模态）| **弱可判定** | AA 页面只列 text+image 输入；媒体称含音频/视频 → 冲突 |
| 1M 上下文 | **可判定（平台口径）** | AA 与官方指南一致，但""合计上限""与""输入上限""是两回事 |
| 长输出（1M output）| **可判定（有指南）** | 官方 long-decode 指南存在；**无公开延迟/成本实测** |
| 推理增强（High 档）| **可判定（有档位）** | AA 标明 High 为推理版；低档是否存在、是否同权重未确证 |

> **写法纪律**：本节及后续引用一律写"**官方/媒体口径**"，不写"其架构为……"这种把转述当事实的句式。

### 9.5b 迁移与集成检查清单（不知道的写"未确证"，不猜）

| 检查项 | 状态 | 说明 |
|---|---|---|
| API 名称与版本字段 | 未确证 | 需查 Gemini API 文档的 model id |
| 与 3.5 的请求/响应 schema 变化 | 未确证 | 迁移指南链接存在（官方推文），未逐条核对 |
| 定价的 cache 作用范围 | 未确证 | 95% 折扣是按"输入全量"还是"命中部分"计，未写明 |
| 1M 上下文的实际可用长度 | 未确证 | "合计上限"意味着输入+输出共享 1M，长输入会挤占输出预算 |
| 多模态输入的格式与限制 | 未确证 | 音频/视频若支持，需采样率/时长限制说明 |
| 速率限制与配额 | 未确证 | 与订阅档（Ultra/Pro）相关，需查官方配额表 |

**可执行动作**：以上六项**任一项未查清前，不在报告里写"支持"或"兼容"**；若业务需要，先小样本实测再落结论。

### 9.6b 适用/不适用决策矩阵

| 任务形态 | 是否适合 4 Argon | 理由（带条件）|
|---|---|---|
| 长文档理解 → 短答案 | **适合** | 输入便宜（\$2/1M）+ 缓存 95% 折扣；输出短则总成本低 |
| 代码库级重构/迁移 | **视 harness** | 内部 +35%/−30% 是 Google 自家 Chromium 任务；换成你的仓库需重测 |
| 超长报告/长解码（>200k 输出）| **不适合**（默认）| 输出 \$10/1M，满额 1M 输出 ≈ \$10/次；除非质量收益明确 |
| 需要多模态输入（音频/视频）| **待核** | 模态口径冲突，未查清前不要依赖 |
| 低延迟交互 | **未确证** | 官方未给 tokens/s；AA 页面 Speed 为 N/A |
| 严格可复现评测 | **不适合做基准锚** | 厂商口径多、平台口径不一致 |

### 9.9 对既有章节的交叉修改建议（不改原文，只记"该改哪里"）

| 既有位置 | 建议修改 | 类型 |
|---|---|---|
| 文首"覆盖范围" | 已改为「到 Gemini 4 Argon（2026 年 9–10 月）」| 已执行 |
| §1.2 时间线块 | 可补一行：`2026-09/10  Gemini 4 Argon  原生多模态 Sparse MoE（媒体口径），1M 上下文，\$2/\$10，AA Index 53` | 未执行（本节已记录）|
| §4.4 vs 竞品对比 | "1M"表述改为"1M（输入+输出合计）" | 未执行（口径修正）|
| §7 跨代演进分析 | 结论需限定为"3.x 期间偏轻量化"；4 Argon 回到旗舰路线 | 未执行（结论限定）|
| §8 关键创新点 | 可加一条"缓存 95% 折扣 + 长输出显式化" | 未执行 |

### 9.10 引用注意（能引/不能引）

**可以引**（带出处）：\$2/\$10 定价、95% 缓存折扣、1M 上下文、AA Index 53（须注明 v4.3.2 与 High 档）、AA 成本 \$1.99/任务、110M 冗长度、官方发布日期区间（9–10 月，含冲突说明）。

**不能引**（或必须降级）：总参数量/专家数、"原生视频输入"、"#1 综合能力"、"比 3.5 强 X%"、任何未给样本数的 ERQA/Vals 具体分数。

**引用句式建议**：「据 Artificial Analysis v4.3.2（推理档），Gemini 4 Argon 得分 53（#8/217）」——**版本、档位、名次三要素缺一不可**。

### 9.2c "1M 合计上限"的工程含义（输入与输出抢同一个预算）

平台口径是**输入 + 输出合计 1M**。这意味着"能塞 1M 输入"和"能出 1M 输出"**不能同时成立**。按 \$2/\$10 计价，几种边界的成本：

| 输入 | 输出 | 是否可行 | 估算成本（未命中缓存）|
|---:|---:|---|---:|
| 990,000 | 10,000 | 可行 | \$1.98 + \$0.10 = **\$2.08** |
| 900,000 | 100,000 | 可行 | \$1.80 + \$1.00 = **\$2.80** |
| 500,000 | 500,000 | 可行（但输出极长）| \$1.00 + \$5.00 = **\$6.00** |
| 10,000 | 990,000 | 可行（长解码）| \$0.02 + \$9.90 = **\$9.92** |
| 1,000,000 | 100,000 | **不可行**（超合计上限）| — |

**工程结论**：把 4 Argon 当"长输入引擎"用时，**必须给输出预留预算**；否则请求会在边界处失败（具体失败形态未确证，见 §9.5b）。

### 9.11 常见误读（10 条，逐条给纠正）

| # | 误读 | 纠正 |
|---|---|---|
| 1 | "1M 上下文 = 能有效检索 1M" | 上下文窗口是**能塞进去**，不是**能检索准**；有效长度需独立测（AA-LCR 只是其中一项）|
| 2 | "缓存 95% 折扣 = 省 95% 钱" | 折扣只作用于**输入侧**，且是否作用于"命中部分"未写明；输出仍是 \$10/1M |
| 3 | "AA #8/217 = 综合第八" | 是**AA 那 10 项题**上的第 8；多模态/agent/长解码都不在 | 
| 4 | "得分 53 是模型级能力" | 是 **High 推理档**的分数；低档若存在，分数会不同 |
| 5 | "Vals #1 = 各行业最准" | 厂商口径，且行业覆盖仅财务/编码/法务/税务四类 |
| 6 | "ERQA 87% = 具身智能可用" | 单一基准、厂商口径、无样本数；真实机器人闭环未验证 |
| 7 | "+35% 代码提交 = 产能提升 35%" | 是 Google 内部 Chromium 重构任务的 agentic code 提交量，非人均产能 |
| 8 | "定价 \$2/\$10 = 便宜" | 是**同价位中位价**，不是低价；长解码满额 ≈ \$10/次 |
| 9 | "9 月发布 / 10-13 发布" | 两个来源冲突，**只能写"9–10 月"并注明冲突** |
| 10 | "支持音频/视频输入" | 媒体称支持，平台页面只标 text+image；**未查清前不得写"支持"** |

### 9.12 复检清单（可直接执行）

| # | 触发 | 动作 | 完成判据 |
|---|---|---|---|
| 1 | 官方 model card 发布 | 补参数/模态/评测三节 | 引用 model card 链接 |
| 2 | API 文档更新定价 | 重算 §9.2/§9.3b 四档成本 | 表格数字与文档一致 |
| 3 | AA 升级 Index 版本 | 记录新版号与新分数 | 53 分旁标版本 |
| 4 | 有独立第三方复现 ERQA/Vals | 把 `[二手]` 升为 `[独立评测]` | 指出来源与样本 |
| 5 | 出现 1M 输出的公开延迟数据 | 补延迟表并重算"长解码"决策 | 有 tokens/s 与 p99 |
| 6 | 竞品同口径发布 | 做"同价位同档位"对照 | 只比同口径列 |

### 9.13 时间线补丁（可直接粘贴，未改动原文）

若要把 §1.2 的时间线块补全，建议插入下面这一行（保持原有缩进与格式）：

```text
├── 09/10月 Gemini 4 Argon        原生多模态 Sparse MoE（媒体口径），1M 上下文（合计），\$2/\$10 定价，AA Index 53（High 档，#8/217）
```

**为什么不直接改原块**：原块是叙述性时间线，改它会牵动上下文排版；**在 §9 记录 + 给出补丁片段**，既保留可追溯性，也不破坏既有阅读顺序。

### 9.3f "内部工程收益"该怎么读

媒体给出的两个数字——**agentic code 提交 +35%**、**post-submit 回滚 −30%**——来自 Google 在自家 **Chromium 约 4000 万行代码、其中 600 万行遗留目录**上的重构任务。要让这个结果对你成立，至少需要同构四个前提：

| 前提 | Google 的情况 | 你的情况（需自测）|
|---|---|---|
| 任务形态 | 大规模、可机械分解的重构 | 是否同构？|
| harness | 内部 agent 框架 + 完整测试套件 | 有无等价测试网？|
| 评审闭环 | 内部 code review + 回滚统计 | 有无同口径回滚指标？|
| 基线 | 上一代模型（未披露具体版本）| 基线是否同一？|

**缺任一项，+35%/−30% 都不能直接引用**。可引用的表述是："据 Google 自报，在其 Chromium 重构任务上 agentic code 提交提升 35%、回滚下降 30%（未披露基线与 harness 细节）。"

### 9.5c 产品线位置（对既有"轻量化"叙事的修正）

| 线索 | 说明 |
|---|---|
| 渠道 | Gemini App（Ultra/Pro）、AI Studio、Gemini API、Antigravity（含 CLI）——**同时覆盖消费/开发者/agent IDE 三类入口** |
| 订阅分层 | 官方推文点名 Ultra 订阅优先获得；Pro 订阅者也可见 → **旗舰不再只服务企业 API** |
| 战略含义 | 3.x 阶段"Flash 提速 + 轻量化"的叙事需要限定：**4 Argon 把旗舰能力重新放回消费入口**，这不是"退回大模型"，而是"旗舰与轻量并行" |
| 待核 | 是否替代 3.5 Pro 的默认档位、旧模型下线时间表 → 均未确证 |

### 9.6c 合规与数据风险（企业采用前的必查项）

| 项 | 状态 | 影响 |
|---|---|---|
| 权重闭源 | 已确证（无开源发布）| 无法本地部署/微调 |
| 数据留存与训练使用 | **未确证** | 企业数据是否进入训练需查条款 |
| 缓存（95% 折扣）的数据位置 | **未确证** | 缓存是否跨租户、是否持久化未写明 |
| 区域可用性 | **未确证** | 官方博客有区域化页面，但未给完整可用区列表 |
| 审计与日志 | **未确证** | 合规场景需 API 侧的日志/审计接口说明 |

> 这五项**任何一项不明确，都不应把 4 Argon 放进"可直接上生产"的结论里**。

### 9.7b 未确证清单（扩充版，16 条）

| # | 事项 | 状态 |
|---|---|---|
| 1 | 精确发布日（09 vs 10-13）| 未确证 |
| 2 | 总参数量 / 专家数 / 激活参数 | 官方未公开 |
| 3 | 是否原生支持音频、视频输入 | 口径冲突 |
| 4 | Vals Index 分数与榜单快照 | 未确证 |
| 5 | ERQA 87% 的样本数/评分脚本/对照模型 | 未确证 |
| 6 | 与 3.5 Pro 的同口径能力差 | 未确证 |
| 7 | 满额 1M 输出的延迟与成本实测 | 未确证 |
| 8 | 是否有非推理档及其价格 | 未确证 |
| 9 | 缓存折扣的作用范围（全量/命中部分）| 未确证 |
| 10 | 1M"合计上限"的失败形态（报错 or 截断）| 未确证 |
| 11 | 数据留存与训练使用条款 | 未确证 |
| 12 | 区域可用性清单 | 未确证 |
| 13 | 速率限制与配额（Ultra/Pro 差异）| 未确证 |
| 14 | 旧模型（3.5 Pro 等）下线时间表 | 未确证 |
| 15 | 音频/视频输入的格式与时长限制 | 未确证 |
| 16 | tokens/s 延迟数据 | 未确证（AA 页面为 N/A）|

### 9.14 三句话结论

1. **能力**：在 AA 那 10 项题、High 推理档上得 53（#8/217）——**是"前沿但不是第一"的位置**，且这个分数不含多模态/agent/长解码。
2. **成本**：\$2/\$10 + 95% 缓存折扣的结构**偏"长输入、短输出"**；长解码（1M 输出）满额约 \$10/次，**不能用"便宜"概括**。
3. **可信度**：可确认的是**产品线定位与定价口径**；不可确认的是**架构细节、多模态范围、跨代能力增幅**——这三类必须留在"未确证"里，等 model card 或 API 文档。

### 9.4 与前代（Gemini 3.5 系列）的差异

| 维度 | Gemini 3.5（2026-05，本报告 §2.9）| Gemini 4 Argon（2026-09/10）| 可判定性 |
|---|---|---|---|
| 定位 | 编码/Agent 工作流优化，速度 4× | 前沿推理 + 原生多模态 + 长解码（1M 输出）| 官方向定位不同，**表述可判** |
| 上下文 | 1M（Flash 侧）| 1M（输入+输出合计）| 数量级相同，**"合计上限"是新口径** |
| 价格 | 未在本节对照（前文未列 3.5-Pro 定价）| \$2 / \$10、缓存 95% | **缺 3.5 对照报价 → 无法算倍数，标未确证** |
| 基准 | 前文引 ARC AGI 2 77.1%（3.1 Deep Think）等 | AA 53、Vals #1、ERQA 87% | **两代评测口径不同，禁止直接相减** |

> **结论**：可以确定的是"**产品线定位上移 + 长输出能力显式化 + 定价未加价**"；**不能**确定"综合能力提升 X%"——因为两代可用的一手数字口径不同。

### 9.5 对既有结论的影响

1. §1.2 时间线应补一行：`2026-09/10  Gemini 4 Argon  原生多模态 Sparse MoE，1M 上下文，\$2/\$10 定价，AA Index 53`（本节已记录，**时间线块本身未改**）；
2. §7 跨代演进分析中"Gemini 在 3.x 之后转向 Flash 提速"的判断**需要限定**：4 Argon 重新回到"旗舰 + 长输出"路线，**不是**只往轻量走；
3. §4 长上下文一章的"1M"表述应改为"**1M（输入+输出合计）**"这一更准确的平台口径——**这是口径修正，不是能力变化**。

### 9.6 失效边界（独立段）

- **榜单替代性**：AA Index 的 10 项评测覆盖有限；Vals/ERQA 均为厂商口径。**"#8/217"只能说明在 AA 这套题上排第 8**，不能外推为"综合第 8"。
- **多模态口径不一致**：媒体称支持音频/视频输入，AA 页面只标 text+image。**在拿到 API 文档前，不得声称"原生视频输入"**。
- **长输出成本**：1M 输出 token 的官方指南存在，但**无公开的单次长解码报价**；按 \$10/1M 输出粗算，一次满额长解码 ≈ \$10，**与"廉价"叙事相反**。
- **内部收益不可外推**：+35%/−30% 来自 Chromium 重构这一特定任务与 Google 内部 harness，**换团队换任务不保证复现**。
- **日期不确定性**：官方推文 10-13 vs 平台标注 2026-09，**任何"某月某日发布"的断言都应带这个区间**。
- **媒体口碑分化**：有媒体以"苦等七个月、刚发布就打折"为标题批评其相对竞品优势不足（`[二手]`，仅记录观点，不采信为结论）。

### 9.7 未确证清单

| # | 事项 | 状态 |
|---|---|---|
| 1 | 精确发布日（09 还是 10-13）| 未确证 |
| 2 | 总参数量 / 专家数 / 激活参数 | 官方未公开 |
| 3 | 是否原生支持音频、视频输入 | 口径冲突，未确证 |
| 4 | Vals Index 具体分数与榜单快照 | 未确证（仅"#1"转述）|
| 5 | ERQA 87% 的样本数、评分脚本、对照模型列表 | 未确证 |
| 6 | 与 Gemini 3.5 Pro 的同口径能力差 | 未确证（两代评测不可比）|
| 7 | 满额 1M 输出的实际延迟与成本 | 未确证 |
| 8 | 是否提供非推理（low/standard）档及其价格 | 未确证 |

### 9.8 复检触发条件

- Google 发布 **Gemini 4 系列模型卡（model card）** → 补参数/模态/评测；
- **Gemini API 文档**更新定价或模态 → 重核 9.2 与 9.6 的口径冲突；
- **AA 更新 Index 版本**（v4.3.2 → 新版）→ 53 分需重算并标版本；
- 出现**第三方独立复现**（非厂商、非平台）→ 才可把 ERQA/Vals 从"厂商口径"升为"独立评测"。

---

## 10. 参考文献

1. Chowdhery, A., et al. (2022). **PaLM: Scaling Language Modeling with Pathways.** arXiv:2204.02311. JMLR 2023.

2. Anil, R., et al. (2023). **PaLM 2 Technical Report.** arXiv:2305.10403.

3. Gemini Team (2023). **Gemini: A Family of Highly Capable Multimodal Models.** arXiv:2312.11805.

4. Gemini Team (2024). **Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context.** arXiv:2403.05530.

5. Gemini Team (2025). **Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities.** arXiv:2507.06261.

6. Gemma Team (2024). **Gemma: Open Models Based on Gemini Research and Technology.** arXiv:2403.08295.

7. Gemma Team (2024). **Gemma 2: Improving Open Language Models at a Practical Size.** arXiv:2408.00118.

8. Gemma Team (2025). **Gemma 3 Technical Report.** arXiv:2503.19786.

9. CodeGemma Team (2024). **CodeGemma: Open Code Models Based on Gemma.** arXiv:2406.11409.

10. Shazeer, N., et al. (2017). **Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer.** ICLR 2017.

11. Lepikhin, D., et al. (2020). **GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding.** arXiv:2006.16668.

12. Fedus, W., et al. (2021). **Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity.** arXiv:2101.03961.

13. Du, N., et al. (2022). **GLaM: Efficient Scaling of Language Models with Mixture-of-Experts.** ICML 2022.

14. Zoph, B., et al. (2022). **ST-MoE: Designing Stable and Transferable Sparse Expert Models.** arXiv:2202.08906.

15. Barham, P., et al. (2022). **Pathways: Asynchronous Distributed Dataflow for ML.** MLSys 2022.

16. Google Blog (2024). *Introducing Gemini 2.0: our new AI model for the agentic era.* blog.google, December 2024.

17. Google Blog (2025). *Gemini 2.5: Our most intelligent AI model.* blog.google, March 2025.

18. Google Blog (2025). *A new era of intelligence with Gemini 3.* blog.google, November 2025.

19. Google Cloud Blog (2024). *Trillium TPU is GA.* cloud.google.com/blog, 2024.

20. Google DeepMind (2026). **Gemini 3.1 Pro / Deep Think Model Card.** deepmind.google/models.

21. Google Blog (2026). *Gemini 3.5 Flash: Our fastest model for coding and agents.* blog.google, May 2026.

22. Google Blog (2026). *Gemini Omni Flash: Native video generation comes to YouTube Shorts.* blog.google, May 2026.

23. Hassabis, D. (2025). *Our vision for building a universal AI assistant.* blog.google/technology/google-deepmind.

---

*本报告基于公开论文、技术报告、博客文章及API文档撰写。由于Google对Gemini部分架构细节（如精确参数量、专家数量等）未完全公开，相关推断均已标注。*
