---
display_name: Gemini
date: 2026-10-29
---

# Google Gemini系列模型深度调研报告

> 覆盖范围：以 PaLM、Gemini 1.0/1.5 技术报告为研究证据主线，延伸到 Gemini 4 Argon 的公开模型卡；Gemma 开放权重系列单列为相关生态，不能据此推断 Gemini 闭源模型的内部架构。产品与模型卡信息更新至 2026-10-29。
> 阅读重点：理解多模态训练、长上下文、稀疏计算和推理/Agent 能力分别解决什么问题，以及现有公开证据能支持到哪里；不把不同代产品拼成单一排行榜。

---

## 1. 概述与发展时间线

### 1.1 系列定位

Google 的公开模型研究可以沿几条互相交叉、但不适用于每个型号的路线来理解：PaLM 研究大规模稠密语言建模与分布式训练；Gemini 1.0 报告多模态联合训练；Gemini 1.5 披露稀疏 MoE 与长上下文实验；后续模型卡更多描述推理、工具使用和多模态输入输出。它们是公开材料呈现的研究线索，不足以证明所有 Gemini 型号共享同一架构或训练配方。

1. **原生多模态**：Gemini 1.0 论文确认文本、图像、音频和视频联合训练，同时保留视觉编码与 USM 音频特征处理；“原生”不等于没有模态编码器，也不证明不存在对齐问题（[固定 v1，§2、§4](https://arxiv.org/html/2312.11805v1#S2)）。
2. **稀疏计算**：Gemini 1.5 技术报告描述了稀疏 MoE；不能据此把后续所有 Gemini 型号都归为 MoE，也不能推断未披露的专家数和路由设计。
3. **长上下文**：Gemini 1.5 报告了百万级上下文及更长序列实验。针对此类合成检索任务的结果，不能等同任意长文档上的可靠推理。
4. **训练与硬件**：Google 的论文和模型卡提到 Pathways、TPU、JAX 等基础设施；具体型号的硬件协同细节并未全部公开。
5. **推理与工具使用**：后续报告和模型卡呈现更强的推理预算、工具接口与多步任务评测；产品能力说明不自动揭示内部推理机制。

### 1.2 完整发展时间线（2022–2026）

```
2022年 ── PaLM时代：Dense Transformer极致Scaling
├── 04月  PaLM 540B              首个千亿级Dense模型，6144 TPU v4训练（arXiv:2204.02311）
└── 12月  Flan-PaLM              指令微调版本，显著提升zero-shot性能

2023年 ── PaLM 2与Gemini诞生
├── 05月  PaLM 2                 Gecko/Otter/Bison/Unicorn四档，compute-optimal训练
├── 12月  Gemini 1.0             Ultra/Pro/Nano三档；MMLU比较须区分5-shot与CoT@32（见§2.3）
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

2026年下半年 ── Gemini 3.6–4更新
├── 07–09月 Gemini 3.6 / 3.7 / 3.8 Flash  多轮迭代；3.8 Flash 模型卡将其描述为基于 3.7 Flash，支持多模态输入、最高 1M 上下文及可调 effort
├── 09月  Gemini 3.8 Audio      Live、Live Extended Thinking、Flash TTS 与 Flash-Lite TTS 型号组
└── 09–10月 Gemini 4 Argon      新一代前沿型号；官方模型卡披露多领域评测，但不披露权重规模或完整架构
```

### 1.3 技术代际划分

| 阶段 | 时间跨度 | 代表模型 | 核心技术标志 | 战略定位 |
|------|----------|----------|--------------|----------|
| **稠密模型与训练系统** | 2022–2023 | PaLM / PaLM 2 | 大规模稠密 Transformer、Pathways 与规模化训练 | 读 PaLM 论文中的并行策略、数据与 scaling 实验 |
| **多模态联合训练** | 2023–2024 | Gemini 1.0 | 论文描述文本、图像、音频、视频等混合训练；同时使用模态处理组件 | “原生多模态”指训练路线，不等于没有编码器或模态边界 |
| **长上下文与稀疏计算** | 2024 | Gemini 1.5 | 稀疏 MoE、百万级上下文与长序列检索实验 | 区分可用上下文长度、合成检索表现和真实任务推理 |
| **推理与多步任务** | 2024–2026 | Gemini 2.x–4 | 思考预算、工具接口和多步任务评测逐步出现在公开材料中 | 公开产品能力与未披露的内部实现分开阅读 |
| **开放权重支线** | 2024–2026 | Gemma 系列 | 面向不同资源、模态和任务的开放权重模型 | 作为独立模型家族比较，不将其架构外推到 Gemini |

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

**固定来源**：*Gemini: A Family of Highly Capable Multimodal Models*，[arXiv:2312.11805v1](https://arxiv.org/abs/2312.11805v1)，提交于 **2023-12-19**（UTC）。[官方发布文章](https://blog.google/innovation-and-ai/technology/ai/google-gemini-ai/)日期为 **2023-12-06**；发布日与 arXiv 提交日分别记录。这里采用历史 v1，不以未注明版本的链接混入后续修订或后代模型规格。

**模型分档**（v1 §2、表1）：

| 变体 | 定位 | 参数规模 | 上下文口径 |
|------|------|----------|------------|
| Ultra | 高复杂度任务 | 本篇未公布；不保留“>1T”估计 | 家族训练长度32,768，逐产品API限额未由本表给出 |
| Pro | 成本、延迟与能力平衡 | 本篇未公布 | 同上，不视为服务的输入/输出配额 |
| Nano-1 | 低内存端侧 | 1.8B | 论文未单列其部署上下文，因此不应将其概括为“较短” |
| Nano-2 | 较高内存端侧 | 3.25B | 同上 |

**架构能确认到哪一层**（[v1 §2](https://arxiv.org/html/2312.11805v1#S2)、[§4](https://arxiv.org/html/2312.11805v1#S4)）：

- **骨干**：基于 Transformer decoder，采用高效注意力，原文举例 MQA；没有按变体列出完整层结构，不能据此把 Ultra/Pro/Nano 的注意力配置写死。
- **分词**：确认 SentencePiece，并以大样本训练语料训练分词器；**论文未给词表大小**，也没有说明文本、代码和图像共用 256K 词表。
- **视觉与音频输入**：支持图文、音频、视频帧交错；视觉编码参考 Flamingo、CoCa、PaLI，输入分辨率可变，音频使用16kHz的USM特征。**离散图像token是原文对图像输出的说明**，不能反推所有视觉输入也经离散量化或SentencePiece编码。
- **上下文**：[§5.1.5](https://arxiv.org/html/2312.11805v1#S5.SS1.SSS5)给出训练序列长度 **32,768 tokens**。这是训练/论文评测口径，不是当前API规格，也不单独证明所有长文档推理可靠。
- **未披露项**：RoPE、RMSNorm、GeGLU、各变体Dense/MoE细分、type embedding与模态输出head布局，**Gemini 1.0 原文未披露**，不能从PaLM或后代模型补推。

**联合训练的边界**：原文确认多模态联合训练与交错输入，未提供“原生训练消除了模态对齐gap”的受控证据。它也描述分阶段调整训练数据混合，不能把“从一开始是多模态模型”扩写为全部组件都从随机初始化、每一步各模态比例固定。[v1 §2、§4]

**训练基础设施**：Gemini 1.0 论文没有披露多个4096-chip TPU v4 Pod、跨数据中心或由Pathways驱动等具体配置；下述实验结果不能确认这些说法。

**MMLU：90.0%与86.4%不属于同一推理设置**。v1表2与[附录§9.1](https://arxiv.org/html/2312.11805v1#S9.SS1)分别列出：

| 设置 | Gemini Ultra | GPT-4 | 条件与来源 |
|------|-------------:|------:|------------|
| 表2的高分配置 | 90.04% | 87.29% | Ultra为带不确定性路由的CoT@32；GPT-4为作者经API采集的CoT@32值（2023-11），不是86.4%的来源 |
| 表2的5-shot | 83.7% | 86.4% | GPT-4值是转引的reported结果；不能把两行拼成同设置比较 |
| 附录普通CoT、32样本 | 85.0% | 87.3% | 未加不确定性路由；不可与上一行5-shot混用 |
| 附录带不确定性路由、32样本 | 90.0% | 87.3% | 置信共识不足则回退greedy；阈值分别在各模型validation split选择 |

官方发布文章的90.0%是发布口径的圆整数；这里保留论文表格与附录各自精度。这些是作者自测或转引，未独立复跑；**不能把90.0−86.4解释为同预算下裸模型普遍领先3.6个百分点**，也不能从MMLU一项推出所有任务超越GPT-4。

同表的其他历史结果也需连设置引用：GSM8K **94.4%（Maj1@32）**、HumanEval **74.4%（0-shot、instruction-tuned）**；“30/32个基准达当时SOTA”是作者对所选基准的报告，不代表所有任务或现行产品表现。

### 2.4 Gemini 1.5 Pro（2024年2月）

**论文**：*Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context*（arXiv:2403.05530）

Gemini 1.5 是公开研究材料中一个清楚的转折点：技术报告介绍了 **Sparse MoE**，并报告百万级上下文与更长序列实验。这里的“转折”只描述可见证据，不意味着 Gemini 2 之后的每个型号都沿用同一实现；报告也未披露可据以确认总参数量、激活参数量和专家路由细节的数据。

**核心架构**：
- **模型类型**：Sparse Mixture-of-Experts (MoE) Transformer
- **路由机制**：Learned routing function，将输入引导至参数子集处理
- **Conditional Computation**：总参数量巨大但每次前向传播仅激活一小部分
- **上下文窗口**：原生支持1M tokens，实验性支持10M tokens
- **多模态**：继承Gemini 1.0的原生多模态能力

**它回答了什么问题**：在维持大容量模型的同时，让每个 token 只经由部分专家计算，以缓解稠密模型的计算成本。Google 报告称 Gemini 1.5 Pro 相比 Gemini 1.0 Ultra 使用更少训练计算量并在其所选基准上取得相近或更好结果；这是作者对该代训练和评测设置的报告，不足以单独证明同等能力下普遍更高效，也不能把效果归因给 MoE 一个因素。相关背景可读 GShard、Switch Transformer、GLaM 与 ST-MoE；这些是技术谱系，不是 Gemini 1.5 未公开实现细节的证据。

**长上下文能力（详见第5章）**：技术报告用合成检索任务测试文本、视频和音频中的定位能力，并报告在长序列训练上的损失趋势。这些实验说明模型可在特定设置中利用远距离上下文；不等同于对自然长文档、长视频或多步推理达到“近乎完美”。数值与实验协议见第 4、5 章及固定版本技术报告。

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

### 2.10 思考设置和上下文上限：按具体型号阅读

模型卡/API 文档中的 thinking level、effort 或上下文上限是**具体型号和接口的设置**，并非整个 Gemini 家族共享的架构属性。某个型号支持更高 effort，只能说明接口允许分配不同推理预算；公开接口不揭示模型内部如何产生或筛选思考过程。上下文窗口也是输入、思考和输出预算的组合，具体限制要回到对应版本的模型卡/API 文档，不能概括为“Gemini 3 起全系列统一 1M”。

### 2.11 跨代材料实际披露了什么

| 研究对象 | 公开材料能支持的机制判断 | 关键未知项 / 阅读边界 |
|---|---|---|
| PaLM | 技术论文描述稠密 Transformer、并行注意力与 FFN 的实现选择，以及大规模 TPU 训练 | 单一训练配置的效率结果不能直接外推到后续 Gemini 系列 |
| Gemini 1.0 | v1 技术报告描述多模态联合训练、Transformer decoder 骨干和模态输入处理 | 不能从模型家族总称推出每个产品型号的完全相同实现 |
| Gemini 1.5 | 技术报告明确描述 Sparse MoE、长上下文训练和多模态检索实验 | 参数总量、激活规模和完整长上下文推理实现未披露 |
| Gemini 2.x–4 | 以产品文档、模型卡和部分技术报告为主，可查各型号输入/输出、上下文与公开评测 | 多数型号缺少足够的结构细节；不应填入推测的 RoPE、FFN、路由或硬件参数 |
| Gemma | 独立技术报告和模型卡给出具体开放权重型号的架构与任务信息 | Gemma 规格不代表闭源 Gemini 实现 |

本表刻意不把分散的产品规格拼成“跨代内部架构表”。每项技术结论应以对应技术报告、模型卡版本及具体型号为准。

---

## 3. 多模态架构设计

### 3.1 设计理念：联合训练与模态编码分别看待

Gemini 1.0的原生多模态指多模态联合训练与交错输入/输出能力；它仍有视觉编码和音频特征处理。不能仅凭“原生/后接”标签断言某类方案效果更好、没有模态对齐问题，或还原GPT-4V、Qwen-VL等竞品未在本篇披露的训练流程。[固定v1 §2、§4](https://arxiv.org/html/2312.11805v1#S2)

### 3.2 Gemini 1.0多模态架构的披露边界

| 环节 | v1直接支持 | 不据本篇补推的部分 |
|------|------------|------------------|
| 文本 | SentencePiece分词器 | 256K词表，以及图像也由同一分词器处理 |
| 图像输入 | 视觉编码；分辨率可变；与文本/音频交错 | 视觉输入一定离散量化、视觉码本大小 |
| 视频输入 | 编码为帧序列置入上下文 | 固定1 FPS、所有型号支持多小时的上限 |
| 音频输入 | 使用16kHz的USM特征 | 统一离散audio token词表或具体量化流程 |
| 模型骨干与输出 | Transformer decoder；可输出交错图文；图像输出使用离散image tokens | 所有模态共用一个embedding矩阵、type embedding实现、不同模态head的数量与连接方式 |

因此可以说“decoder骨干支持多模态交错序列”，不能把这句话补画成已公开的逐模块实现图。[v1 §2、图2](https://arxiv.org/html/2312.11805v1#S2)的研究性图像输出也不等于2023年所有产品端点已开放生图或音频生成。

**后代型号边界**：Gemini 2.0+ 的原生音频/图像输出、TTS控制及视频时长，应依据各自版本的模型卡或 API 文档；Gemini 1.0 论文不披露这些型号的输出 head 或推理实现。

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

### 4.2 Gemini 1.5 的长上下文机制与公开边界

Gemini 1.5 报告把长上下文能力与稀疏 MoE、多模态长序列训练和大规模 TPU 训练联系起来，但并未给出足够细节来重建完整注意力结构或推理缓存实现。尤其不能把其他论文中的层级注意力、Gist token 或摘要压缩机制移植为 Gemini 1.5 的已确认设计。

阅读时应把三个成本分开：MoE 控制每个 token 使用多少前馈参数；长上下文本身仍增加注意力、存储与通信负担；跨模态长输入还受分辨率、帧率和音频切片策略影响。论文在受控的 needle retrieval / perplexity 设置下展示模型利用长输入的能力，并讨论训练与推理配置；这类证据支持“模型能在特定条件下检索远处线索”，不支持“MoE 自动解决长序列成本”或“真实资料里普遍完美召回”。

原文阅读入口：Gemini 1.5 技术报告 [§2（架构）](https://arxiv.org/html/2403.05530v1#S2)、[§3（训练）](https://arxiv.org/html/2403.05530v1#S3)、[§5（评测）](https://arxiv.org/html/2403.05530v1#S5)。

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

### 6.5 2025–2026：Gemma 开放权重分出生成、扩散与表示学习路线

Google 近期新增的开放模型不是一串同构的“Gemma 新版本”。其中既有通用生成基座，也有任务专门化微调、文本扩散模型和非生成式 embedding 模型。比较它们时先看**输出对象**和**系统中承担的环节**，不要把基准分数或参数规模拼成单一排行榜。

截至 2026-10-29，Google DeepMind [官方模型卡目录](https://deepmind.google/models/model-cards/)在 Gemma 的开放模型栏目列出 EmbeddingGemma 2（10 月 6 日更新）、DiffusionGemma（6 月 10 日）和 Gemma 4（4 月 2 日）为最近的系列发布。下表按学习主线挑选代表性分支，并非 Google 所有开源项目的全量清单；例如模型卡目录按专门用途分组的机器人模型不自动等同于开放权重。

| 型号 / 发布节点 | 模型类型与主要用途 | 公开机制或规格 | 证据性质 |
|---|---|---|---|
| **Gemma 4**（2026-04-02） | 开放权重通用模型家族 | E2B、E4B、26B A4B MoE、31B Dense；小型型号强调端侧多模态，较大型号面向推理和微调；官方称 Apache 2.0 | 发布博客和模型卡自述；不等于训练数据和所有模型组件均开源。[发布说明](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/) |
| **Gemma 4 12B**（2026-06-03） | Gemma 4 的中型多模态变体 | 官方发布稿称视觉和音频输入直接接入 LLM 主干，不使用传统独立多模态编码器；这是发布稿层级的结构描述 | Google 发布博客；Apache 2.0。[发布说明](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/) |
| **Gemma 4 QAT checkpoints**（2026-06） | 既有型号的量化感知训练变体 | 训练时模拟量化，以降低端侧压缩后的质量损失 | 检查点与部署变体，不是新的模型架构代际。[QAT 发布说明](https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/) |
| **FunctionGemma**（2025-12-18） | 270M 级函数调用专门模型 | 基于 Gemma 3 270M 微调，把自然语言映射为结构化 API / OS 动作；官方示例强调还需针对应用微调 | Google 发布博客和模型卡；属于边缘 Agent 的专用分支，不代表通用 Gemma 指令模型天然具备相同工具可靠性。[官方说明](https://blog.google/innovation-and-ai/technology/developers-tools/functiongemma/) |
| **TranslateGemma**（2026-01-15） | 翻译专门模型系列 | 4B / 12B / 27B，基于 Gemma 并经翻译任务定向训练 | Google 发布说明与官方权重；报告结果是厂商指定评测上的作者数据。[官方说明](https://blog.google/innovation-and-ai/technology/developers-tools/translategemma/) |
| **MedGemma 1.5**（2026-01-15） | 医学文本 / 影像专门模型 | 4B；官方发布范围包括 CT/MRI 体数据、病理切片、纵向 X 光分析与报告抽取 | 属 HAI-DEF 开放模型生态，使用条款不同于通用 Gemma Apache 2.0；属于下游开发起点，不是临床诊断系统。[官方说明](https://blog.google/intl/en-in/company-news/from-seed-to-scale-partnering-with-indias-startups-to-build-the-ai-future/) |
| **DiffusionGemma 26B A4B**（2026-06-10） | 实验性文本扩散生成模型 | 26B 总参数 / 3.8B 激活；自回归 encoder 处理 prompt 并缓存 KV，双向 denoiser 迭代修订 256-token canvas，定稿块再作为下一块上下文 | Google 官方博客、开发指南与模型卡；Apache 2.0。模型卡称整体输出质量低于标准 Gemma 4；“最高 4×”是低批量、指定 GPU 配置下的作者报告，不能泛化到高并发服务。[DiffusionGemma 模型卡](https://ai.google.dev/gemma/docs/diffusiongemma/model_card) · [扩散语言模型专题](../../LLM/DiffusionLM/report.md) |
| **EmbeddingGemma 2**（2026-10-06 发布；arXiv v1 于 10-27 提交） | 多模态 embedding 模型，输出向量而非生成文本 | 文本、代码、图像、视频、音频映射到共享空间；论文报告约 744M 参数，官方模型卡四舍五入为 740M；支持模块化编码器和 Matryoshka 向量截断 | 官方模型卡称 Apache 2.0；技术报告已做[逐篇精读](papers/2610.37364-embeddinggemma2.md)。它属于检索 / 表征线，不能当成 Gemma 生成模型能力的证据。[官方发布说明](https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/) |

这些分支至少分成三类：**生成模型**回答或生成内容；**DiffusionGemma**研究并行去噪、块提交与自修订；**EmbeddingGemma 2**学习跨模态检索表示。它们共享 Gemma 家族背景，但任务目标、训练损失、输出接口和评测集都不同。Function/Translate/Med 等专用模型则主要体现对数据和目标任务的定向适配。许可证也应按各模型卡逐一确认，不能用“Gemma”这个家族名推断所有模型条款一致。

---

## 7. 跨代技术演进：公开证据呈现的几条路线

### 7.1 从规模化训练到多模态训练

PaLM 的研究问题是如何把稠密语言模型扩展到大规模 TPU 系统；Gemini 1.0 报告将重点转向多模态混合训练。两者并非简单的“旧架构被新架构替代”：训练数据、模型接口、并行系统与评测目标都发生变化。Gemini 1.0 论文可支持联合多模态训练的判断，但没有证明这种训练消除了模态间的对齐问题，也没有公开所有产品变体的具体结构。

### 7.2 Gemini 1.5：长上下文不只是扩大窗口

Gemini 1.5 的研究将稀疏计算、多模态长序列训练和检索评测放在一起。读这一代时要拆开看：MoE 影响每 token 激活哪些前馈参数；长序列增加注意力与缓存成本；needle retrieval 只测特定位置线索能否被找回。窗口上限、每 token 计算量和任务质量属于不同问题，不能把一个实验的高召回率解释成“长上下文已经解决”。

### 7.3 后续 Gemini：从推理接口看系统，而非猜内部算法

Gemini 2.5 及之后的报告与模型卡越来越强调 thinking / effort 设置、工具调用、多步任务和多模态生成。对学习者而言，值得比较的是模型得到多少推理预算、能否调用哪些工具、任务如何判定成功，以及结果来自模型卡自测还是独立评测。产品接口中可见的“思考级别”不是内部推理算法的完整描述；“Agent”也需拆成规划、状态观察、工具执行和错误恢复等可测环节。

### 7.4 Gemma：开放权重带来的另一种研究可见性

Gemma 支线提供可下载权重及各型号自己的模型卡、技术报告，因而读者可直接学习小模型、专用模型、扩散解码与多模态 embedding 的设计。它与 Gemini 同属 Google 研究生态，但可见的开源权重不能补足 Gemini 闭源型号未披露的架构细节。近期分支见 §6.5。

### 7.5 读技术与硬件协同的证据

PaLM/Gemini 论文和 Google 的基础设施材料说明 TPU、JAX、Pathways 在大规模训练中的作用；但“某型号在某代 TPU 上训练”不足以证明模型结构已经针对某硬件做了特定联合优化。除非论文披露并比较并行策略、通信瓶颈或硬件消融，报告应把训练平台和架构协同分开写。

---

## 8. 关键创新点总结

### 8.1 这条研究线目前能支持的综合判断

1. **多模态首先是训练与接口问题，不是一个标签。** Gemini 1.0 技术报告描述联合多模态训练，但也公开视觉与音频的输入处理组件；后代产品支持更多输入/输出，公开材料并未因此揭示同一套内部实现。
2. **长上下文能力必须连同任务协议阅读。** Gemini 1.5 的合成检索结果展示远距离线索可被利用，但上下文窗口上限、needle recall 与真实长文档推理是不同问题；不能把定点检索分数概括成普遍“近乎完美”。
3. **稀疏计算与长上下文是两条相交的成本轴。** MoE 主要改变每 token 激活的参数子集，序列长度仍影响注意力、缓存与通信；公开材料没有证明一个机制消除了另一类成本。
4. **推理与 Agent 能力应按可观察的任务和预算分析。** 模型卡提供的 effort、工具配置和 benchmark 条件可用于理解系统行为；它们不等同于已披露的内部思维算法或通用自主规划机制。
5. **Gemma 是相邻的开放权重研究线。** Gemma 技术报告和模型卡能讨论具体模型的训练、结构与适用边界；不能将其规格泛化到闭源 Gemini。

### 8.2 跨厂商比较的读法

| 比较问题 | 建议比较的证据 | 不宜直接得出的结论 |
|---|---|---|
| 多模态路线 | 具体技术报告对训练目标、输入编码和生成接口的描述 | 不能仅凭“原生”一词判定不存在编码器或对齐阶段 |
| 上下文能力 | 同一任务协议、输入长度、检索位置和推理预算下的结果 | 不能把产品上下文窗口当成真实长文档推理质量 |
| 推理与 Agent | 明确工具、预算、成功判据和独立评测条件的任务结果 | 不能把 thinking 档位或厂商演示直接解释成通用自主规划算法 |
| 开放程度 | 权重、数据、代码和许可分别检查 | 不能用“开源 / 闭源”一个标签概括整个模型生态 |

跨厂商比较的单位应是具体模型、版本、任务与协议，而不是公司路线概述。Gemini、GPT 与 Llama 的开放方式、模态接口和推理系统都随型号变化；表格只给出比较维度，不把异质结果强行排位。

---

## 9. Gemini 4 Argon（2026-09/10）：稀疏 MoE、长解码与评测边界

> 模型以 stable ID `gemini-4-argon` 提供；本节依据 Google 官方模型卡、Gemini API 模型说明和官方发布公告。官方来源没有公开权重 revision 或完整参数规模，本节不推断这些数值。

### 9.1 发布和研究对象

Google DeepMind 于 2026-09-30 宣布 Gemini 4 Argon 向 Fairwind 网络安全合作方有限开放；2026-10-13 的公告再称向开发者、企业和订阅用户全球开放。两日表示分阶段发布，不是日期冲突。API 模型页标注模型 ID `gemini-4-argon`，stable，页面最近更新于 2026-10-14。

### 9.2 可确认的技术特征

- **架构**：Google 模型卡称 Argon 是基于 Transformer 的稀疏 MoE，支持文本、视觉和音频输入；参数总量、专家数和路由细节未披露。模型卡提及用强化学习训练多步推理、问题求解和定理证明数据，但未给这些环节的完整消融，因此不能把能力提升归因给某一训练步骤。
- **输入与上下文**：Gemini API 模型页列出文本、图像、视频、音频和 PDF 输入，文本输出；统一上下文预算为 1,048,576 tokens。同步请求的最大输出为 65,536 tokens；长解码模式可继续到 1M 上限减去输入占用。thinking level 提供 low、medium、high。
- **训练实现**：模型卡披露训练使用 TPU、JAX 与 ML Pathways；没有披露参数规模、集群规模或训练算力，不能据此比较训练效率。

这组披露显示研究重点放在稀疏模型、多步推理与长生成，但目前公开材料没有给出专家路由、训练阶段消融或同算力对照；这是一项证据缺口，不能用 MoE 的一般理论替代该模型的实验证据。

### 9.3 评测结果应如何读

Google 模型卡给出若干结果。下表只保留能帮助理解任务范围的代表性数据；它们都是厂商公布的评测结果，本报告没有独立复跑。

| 能力 | 结果 | 条件与边界 |
|---|---:|---|
| 长上下文 GraphWalks | 84.2 F1 | 200 道 256K–1M tokens 的 BFS 题；Google 自行运行。分数不等于对任意百万 token 文档都能可靠检索。 |
| DeepSWE v1.1 | 77.9% | Gemini 结果使用 mini-swe agent harness；竞品结果来自各自公开榜单或系统卡，不能当作完全相同的运行环境。 |
| Terminal-Bench 4.0 | 57.4% | Gemini 结果由 Google 自行运行；其他模型按公开榜单报告。 |
| Vals Index | 68.9% | 取自 Vals AI；属于该套知识工作任务的结果，不代表通用能力总分。 |

Google 的评测方法说明：除特别注明外，Argon 结果为 pass@1，并使用最高 thinking setting；小规模基准会对多次试验取平均。其他模型结果除特别注明外多数来自厂商自报。因而这些数字适合了解 Argon 在指定任务和设置下的表现，不能直接读成同条件排行榜。GraphWalks 的百万级长上下文结果覆盖 200 道题，仍需与真实长文档和跨文档任务分开判断。

### 9.4 尚不能确认的结论

- 官方材料没有披露总参数、激活参数、专家数量、路由机制或训练算力；不写“超大规模”具体数字。
- 官网支持视频等输入模态，但没有披露各模态的内部编码器、训练混合比例或逐模态消融；产品输入能力不能还原模型结构。
- Vals Index 等厂商页面及模型卡给出的分数没有在本研究中独立复现。Google 内部工程任务结果也不等于外部仓库的可复现实验。
- 1M 是统一输入/思考/输出预算，长解码也会消耗同一预算；它是接口上限，不代表模型在满长度时保持相同准确率或延迟。

本节依据的固定页面和读取范围见[官方 Gemini 4 Argon API 模型页](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon)、[Google DeepMind 模型卡](https://deepmind.google/models/model-cards/gemini-4-argon/)、[模型评测方法](https://deepmind.google/models/evals-methodology/gemini-4-argon)、[9 月 30 日有限开放公告](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)及[10 月 13 日全球开放公告](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/)。

---


### 9.5 2026-07–10 更新：Flash 迭代与 Gemini 4 Argon 的披露边界

截至 2026-10-23，Google DeepMind 的模型卡目录新增 Gemini 3.6、3.7、3.8 Flash 与 Gemini 3.8 Audio。Gemini 3.8 Flash 模型卡将其明确描述为基于 Gemini 3.7 Flash，支持文本、图像、音频和视频输入、最高 1M token 上下文与 64K 输出；卡片说明可调 effort 用于控制质量、成本与延迟。该卡提供若干 agentic coding、knowledge work、computer-use、长上下文等基准结果，但指出部分安全自动评估已更新、不可直接与旧卡分数比较。此证据支持产品级能力与评测口径，不能推出 3.8 的全新底层架构或训练配方。

Gemini 4 Argon 的官方模型卡（2026-10-13）公布 2026 年 10 月多项软件工程、知识工作、科学、长上下文、计算机使用和多模态评测，并链接到单独的方法说明。其结果在同一张表中列出对手，但比较仍受各基准的工具、预算、版本和评分条件约束；不能简化为单一“总排名”。官方卡没有公开 Argon 参数规模、权重、专家数或完整训练流程。本节 §9.1–§9.4 的发布信息与架构限制仍适用。

本条目所称“Gemini 系列”也包括 §6 的 Gemma 开放模型支线。官方模型卡目录将 Gemma 列为开放模型，并列出 Gemma 4（2026-04）、DiffusionGemma（2026-06）与 EmbeddingGemma 2（2026-10）；它们与 Gemini 4 Argon 属不同发布线，不能用 Gemma 模型卡推断闭源 Gemini 的架构。

一手材料：[Gemini 3.8 Flash 模型卡](https://deepmind.google/models/model-cards/gemini-3-8-flash/)、[Gemini 4 Argon 模型卡](https://deepmind.google/models/model-cards/gemini-4-argon/)、[Google DeepMind 模型卡目录](https://deepmind.google/models/model-cards/)。

## 10. 参考文献

1. Chowdhery, A., et al. (2022). **PaLM: Scaling Language Modeling with Pathways.** arXiv:2204.02311. JMLR 2023.

2. Anil, R., et al. (2023). **PaLM 2 Technical Report.** arXiv:2305.10403.

3. Gemini Team (2023). **Gemini: A Family of Highly Capable Multimodal Models.** [arXiv:2312.11805v1](https://arxiv.org/abs/2312.11805v1)，2023-12-19；相关方法与评测定位见 §2、§4、§5.1.1、§5.1.5 和附录 §9.1。

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

19. Google DeepMind (2026). *Gemini 4 Argon Model Card* and *Model evaluation: Approach, methodology & results*, checked 2026-10-22.

20. Google AI for Developers (2026). *Gemini 4 Argon model documentation*, model ID `gemini-4-argon`, page last updated 2026-10-14.

21. Google Blog (2026). *Gemini 4 Argon* (limited rollout, 2026-09-30; global availability, 2026-10-13).
22. Google DeepMind (2026). *Gemini 3.8 Flash Model Card*, published 2026-09-02; *Gemini 4 Argon Model Card*, published 2026-10-13; model card catalogue checked 2026-10-23.

19. Google Cloud Blog (2024). *Trillium TPU is GA.* cloud.google.com/blog, 2024.

20. Google DeepMind (2026). **Gemini 3.1 Pro / Deep Think Model Card.** deepmind.google/models.

21. Google Blog (2026). *Gemini 3.5 Flash: Our fastest model for coding and agents.* blog.google, May 2026.

22. Google Blog (2026). *Gemini Omni Flash: Native video generation comes to YouTube Shorts.* blog.google, May 2026.

23. Hassabis, D. (2025). *Our vision for building a universal AI assistant.* blog.google/technology/google-deepmind.

---

*本报告基于公开论文、技术报告、博客文章及API文档撰写。由于Google对Gemini部分架构细节（如精确参数量、专家数量等）未完全公开，相关推断均已标注。*
