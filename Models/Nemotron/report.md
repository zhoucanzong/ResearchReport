---
display_name: Nemotron
---

# NVIDIA Nemotron 系列研究脉络

> 覆盖范围：NVIDIA Nemotron 系列大语言模型从 2024 年至 2026 年 10 月公开的技术路线与代表性研究。

---

## 一、执行摘要

Nemotron 的研究线包括早期合成数据与对齐、基于 Llama 的压缩/推理后训练，以及 Mamba–Attention–MoE 混合架构。但同一品牌不代表同一训练配方。Nemotron 3 初始 Nano 与 Super / Ultra 的关键区别是：**LatentMoE、MTP 与原生 NVFP4 训练在家族白皮书中归给两个大模型**，不能把它们全部附到 Nano 上。[新增一手来源 N1–N4]

Ultra 的 550B 总参 / 55B 激活可由官方模型卡和技术报告确认；BF16 型号页也列出最长 1M context。现有材料不支持把 BF16 与 NVFP4 的上下文上限说成不同。部署瓶颈还取决于精度、批大小、序列和硬件，不能只凭参数量判断。

性能证据也必须带运行点：Ultra 论文在 GB200、NVFP4、8K 输入/64K 输出的最大吞吐比较中有优势，但同一论文在 prefill-heavy 任务给出反例。因此不应把特定运行点外推成统一速度或成本排名；横向比较需固定模型版本、硬件、精度、输入输出长度与服务栈。

## 二、模型演进时间线

| 时间 | 模型 / 论文 | 核心定位 | 关键创新 |
|------|------------|---------|---------|
| 2024-02 | **Nemotron-4 15B** (arXiv:2402.16819) | 中型 Dense 基座模型 | 预训练数据配方与评估基准 |
| 2024-06 | **Nemotron-4 340B** (arXiv:2406.11704) | 大型合成数据生成器 | 98%+ 合成数据对齐、Reward Model、开放 Pipeline |
| 2025-03 | **Llama 3.1 Nemotron Nano 8B** | 端侧高效推理模型 | 基于 Llama 3.1 蒸馏 + 优化 |
| 2025-03 | **Llama 3.3 Nemotron Super 49B** | 中型推理模型 | 基于 Llama 3.3 改进 |
| 2025-03 | **Llama 3.1 Nemotron 70B Instruct** | 指令遵循模型 | 长上下文、工具使用 |
| 2025-04 | **Llama 3.1 Nemotron Ultra 253B** | 大型推理模型 | 企业级复杂推理 |
| 2025-04 | **Nemotron-H** (arXiv:2504.03624) | 混合架构基座模型 | Mamba + Transformer 混合、FP8 训练、MiniPuzzle 压缩 |
| 2025-05 | **Llama-Nemotron** (arXiv:2505.00949) | 异构推理模型家族 | 动态推理切换、RL 训练、开源 Post-Training Dataset |
| 2025-08 | **Nemotron Nano 2** (arXiv:2508.14444) | 高效推理小模型 | Mamba-2 + Attention、6.3× 吞吐提升、20T tokens 预训练 |
| 2025-08 | **Nemotron Nano 9B v2** | Nano 迭代版 | 知识截止 2024-09，多语言与推理增强 |
| 2025-12 | **Nemotron 3 Nano**（专报2512.20848；家族白皮书2512.20856） | 混合Mamba/MoE基座 | 初始BF16/FP8 checkpoint；不能套用Super/Ultra组件，见§3.4 |
| 2026-03-11 | **Nemotron 3 Super**（120B/12B） | 多agent基座 | 官方确认1M；评测条件待补，见§3.4 |
| 2026-03 | **Nemotron 3 子系列** | 垂直领域扩展 | Speech、RAG、Safety、VoiceChat、Omni |
| 2026-03 | **Nemotron Coalition** | 开放联盟 | 联合 Black Forest Labs、Cursor、LangChain、Mistral 等八大实验室 |
| 2026-06-04 | **Nemotron 3 Ultra**（550B/55B） | 混合Mamba/LatentMoE基座 | BF16模型卡亦列1M；吞吐依工作负载，见§五 |

---

## 三、分代技术详解

### 3.1 第一代：Nemotron-4 系列（2024）—— 合成数据驱动的对齐范式

#### Nemotron-4 15B（2024-02）
- **论文**：*Nemotron-4 15B Technical Report* (arXiv:2402.16819)
- **定位**：中型 Dense Transformer 基座模型，探索预训练数据配方
- **规模**：15B 参数，训练数据细节公开

#### Nemotron-4 340B（2024-06）
- **论文**：*Nemotron-4 340B Technical Report* (arXiv:2406.11704)
- **定位**：大型开源模型家族，核心亮点是**合成数据生成（Synthetic Data Generation, SDG）**
- **模型家族**：
  - **Nemotron-4-340B-Base**：340B 参数，9T tokens 预训练
  - **Nemotron-4-340B-Instruct**：指令遵循版本
  - **Nemotron-4-340B-Reward**：奖励模型，RewardBench 上超越 GPT-4o 和 Gemini 1.5 Pro
- **核心创新**：
  - **98%+ 合成数据对齐**：整个对齐阶段超过 98% 的数据为合成生成，大幅降低人工标注成本
  - **合成数据 Pipeline**：开源完整的 prompt 生成 → response 生成 → 质量过滤 → 偏好排序 pipeline
  - **Iterative Weak-to-Strong**：多轮迭代自增强，用中间模型生成更高质量数据训练下一代
  - **LLM-as-Judge / Reward-Model-as-Judge**：系统比较了两种自动评估策略，最终 Reward Model 在 Chat-Hard 类别上显著优于 LLM（0.87 vs 0.54）
- **许可证**：NVIDIA Open Model License（允许商业应用）
- **影响**：为后续 Nemotron 系列奠定了"合成数据 + 自迭代"的技术基因，也成为社区重要的合成数据生成基座

---

### 3.2 第二代：Llama-Nemotron 系列（2025-03~05）—— 基于 Llama 的高效推理改进

2025 年初，NVIDIA 基于 Meta Llama 3.1/3.3 基座，通过**神经架构搜索（NAS）**、**知识蒸馏**、**持续预训练**和**大规模强化学习**，推出了一系列改进模型：

| 模型 | 发布时间 | 基座 | 规模 | 核心能力 |
|------|---------|------|------|---------|
| Llama-3.1-Nemotron-Nano-8B-v1 | 2025-03-18 | Llama 3.1 8B | 8B | 端侧高效推理 |
| Llama-3.1-Nemotron-70B-Instruct | 2025-03-18 | Llama 3.1 70B | 70B | 指令遵循、长上下文 |
| Llama-3.3-Nemotron-Super-49B-v1 | 2025-03-18 | Llama 3.3 70B | 49B | 中型推理（剪枝后） |
| Llama-3.1-Nemotron-Ultra-253B-v1 | 2025-04-07 | Llama 3.1 405B | 253B | 大型推理（蒸馏后） |

#### Llama-Nemotron（2025-05，arXiv:2505.00949）
- **论文**：*Llama-Nemotron: Efficient Reasoning Models*
- **定位**：首个开源**异构推理模型家族**，支持动态推理模式切换
- **模型规模**：
  - **LN-Nano**：8B（基于 Llama 3.1 8B）
  - **LN-Super**：49B（基于 Llama 3.3 70B 剪枝）
  - **LN-Ultra**：253B（基于 Llama 3.1 405B 蒸馏）
- **核心创新**：
  - **动态推理切换（Dynamic Reasoning Toggle）**：首个开源模型支持通过轻量级 system prompt（"detailed thinking on/off"）在标准聊天模式和深度推理模式间动态切换，无需切换模型或架构
  - **五阶段训练流程**：
    1. NAS + FFN Fusion 优化推理效率
    2. 知识蒸馏 + 持续预训练恢复精度
    3. SFT 混合标准指令数据与 DeepSeek-R1 等强教师的推理轨迹
    4. 大规模 RL 训练（数学/STEM 数据集），LN-Ultra 在 GPQA-D 上超越教师模型
    5. 短对齐阶段优化指令遵循和人类偏好
  - **FP8 生成优化**：为大规模 RL 训练开发自定义框架，支持 FP8 精度生成
  - **开源资源**：完整 Post-Training Dataset、NeMo / NeMo-Aligner / Megatron-LM 训练代码
- **性能**：LN-Ultra 在 2025-04 的 Artificial Analysis Intelligence Index 上被评为"最聪明的开源模型"，在多项推理和非推理基准上领先

---

### 3.3 第三代：Nemotron-H / Nano 2（2025-04~08）—— 混合 Mamba-Transformer 架构

#### Nemotron-H（2025-04，arXiv:2504.03624）
- **论文**：*Nemotron-H: A Family of Accurate and Efficient Hybrid Mamba-Transformer Models*
- **定位**：探索 Mamba 线性复杂度与 Transformer 精确注意力融合的混合架构
- **模型规模**：
  - **Nemotron-H-8B**：8B 参数
  - **Nemotron-H-56B-Base**：56B 参数（FP8 训练）
  - **Nemotron-H-47B-Base**：56B 经 MiniPuzzle 压缩后，推理速度再提升 20%
- **架构设计**：
  - 用 **Mamba 层**替换大部分自注意力层（约 8% 层保留注意力）
  - 保留少量注意力层用于精确长程依赖建模
  - 无位置编码，使用 RMSNorm，独立嵌入/输出层权重
- **核心创新**：
  - **MiniPuzzle 压缩技术**：结合剪枝与知识蒸馏，将 56B 模型压缩至 47B，精度几乎无损，推理更快
  - **FP8 训练方案**：证明 FP8 训练可达到与 BF16 相当的精度，降低训练成本
  - **视觉语言扩展**：Nemotron-H-8B/56B-VLM，采用 NVLM-D 架构，用于 Cosmos-Reason1 等物理 AI 推理
  - **性能**：论文在指定模型、精度、硬件与长度设置中比较同规模 Transformer（Qwen-2.5、Llama-3.1），并报告了最高 3 倍推理速度；这是该报告测试范围内的结果，不代表任意部署设置都能达到该倍数。

#### Nemotron Nano 2（2025-08，arXiv:2508.14444）
- **论文**：*NVIDIA Nemotron Nano 2: An Accurate and Efficient Hybrid Mamba-Transformer Reasoning Model*
- **定位**：Nemotron-H 的推理专用增强版，面向端侧和高效推理场景
- **基座**：Nemotron-Nano-12B-v2-Base（62 层：6 注意力 + 28 FFN + 28 Mamba-2）
- **核心改进**：
  - **20 万亿 tokens 预训练**：使用 Warmup-Stable-Decay 学习率调度，FP8 精度
  - **128K 长上下文扩展**：持续预训练阶段扩展上下文长度，不损害其他基准
  - **数据集升级**：Nemotron-CC-v2（新增 8 组 CommonCrawl 快照、15 语言合成 QA）、Nemotron-CC-Math-v1（133B 数学 tokens）
  - **剪枝与对齐**：从 12B Base 剪枝得到 9B 模型，再经对齐训练
- **性能**：与 Qwen3-8B 相比，在 1k input / 8k output 或 8k input / 16k output 等生成重载场景下，**吞吐量提升 3×–6.3×**，精度相当或更优

---

### 3.4 Nemotron 3：Nano、Super 与 Ultra 分开取证

#### 3.4.1 初始 Nano 与家族规划

NVIDIA 2025-12-15 家族页发布 Nano，并把 Super / Ultra 列为后续计划；`2512.20856` 是**家族白皮书**，Nano 专门技术报告是 **`2512.20848`**。前者的未来配置不能当作 Nano 已采用的组件清单。[N1,N2]

Nano 专门报告写 25T tokens 预训练，后训练包括 SFT、RLVR、RLHF；公开初始 checkpoint 为 BF16 及由 BF16 经 PTQ 得到的 FP8。家族白皮书把 LatentMoE、MTP、NVFP4 训练分配给 Super / Ultra；因此，不能把“原生NVFP4训练 + LatentMoE + MTP”组合归给 Nano。后续另有 NVFP4 推理权重，不等于初代用了同样精度预训练。[N1 Abstract/§2.2–2.4；N2 §1、§4]

参数也有口径差异：模型卡的产品规格是30B总 / 3.5B激活，家族页细分为31.6B总 / 3.2B激活（含embeddings为3.6B）。引用应标明出处与是否含嵌入，不能把不同四舍五入值当作不同checkpoint。[N1官方家族页；N3 Nano Model Description]

#### 3.4.2 Super

2026-03-11 官方公告确认 Super 为 **120B 总参 / 12B 激活、1M context**，定位在多 agent 工作负载；LatentMoE、MTP 与 NVFP4 配方需以对应技术报告为界。[N4] 公开公告确认 Super 的参数与定位，但缺少完整技术报告和评测 harness 的 SWE-bench 60.47% 与无日期的 Intelligence Index 36 不作为可比较成绩；Nano 的后训练细节也不能逐项继承给 Super。

#### 3.4.3 Ultra

官方 BF16 模型卡列出 **550B总 / 55B激活、最长1M context、Hugging Face发布日2026-06-04**。arXiv 专门报告 `2606.15007v1` 的提交日是 **2026-06-12**；两个日期是模型发布与论文存档，不相互替代。技术报告的 arXiv 提交日为 2026-06-12，晚于模型卡公布日 2026-06-04；引用时应分别注明模型发布与论文存档日期。[N5,N6][N5,N6]

Ultra 使用 Mamba-2、MoE 与少量 Attention 交错，并带 LatentMoE 和共享权重的 MTP。原文表1给出108层、64个Q heads、2个KV heads、每层512 experts选22、latent维2048、2个共享权重MTP层；这些是 **Ultra 的配置**，不统称整个 Nemotron 家族固定规格。[N6 §2.1–2.2、表1]

## 四、训练和量化：区分阶段与模型

| 对象 | 公开训练与量化信息 | 不应混淆的模型边界 |
|---|---|---|
| 初始 Nano | 25T预训练；后训练后BF16→FP8 PTQ；选择性保留敏感层较高精度 | 不等同于全程NVFP4预训练，也不能将Ultra的20T训练数字套给Nano [N2] |
| Super | 家族白皮书和发布公告支持原生NVFP4、LatentMoE与MTP方向 | 具体优化器和训练token数未在这些来源中披露 [N1,N4] |
| Ultra | 20T预训练，**15T + 5T**两阶段；NVFP4采用混合精度，部分网络保留高精度 | 不能与“前20T+后5T”或全系列共用同一优化器/学习率表混为一谈 [N6 §1、§2.2] |

Ultra 的NVFP4不是所有张量都四位。原文保留末段网络和若干敏感投影等高精度。§2.2 / 图3从5T、10T、16T检查点分支切BF16再训练74B tokens，比较训练loss gap；作者给出平均低于0.4%的差距。这是分支训练损失代理，**不是所有任务准确率损失<1%**。原文还明确切BF16没有解决所讨论的训练发散，不能据小loss gap声称低精度不会发散。

Nano 的FP8也有任务差异。表4的MMLU-Pro从78.30到78.10，TauBench V2 airline从48.00到44.79；总体约99%的中位数恢复不能改成逐任务无损。§4.3和图11对attention、Mamba层与KV cache做选择性量化，体现的是精度与可用batch的取舍。[N2]

## 五、效率证据：保留运行条件与失败运行点

### 5.1 Nano 的吞吐不是裸 tok/s

Nano专门报告图1的比较是**单H200、8K输入/16K输出**，每个模型在vLLM与TRT-LLM中取较好实现。Nano与Qwen3使用FP8权重/激活，GPT-OSS使用mxfp4权重、BF16激活；作者报告相对Qwen3-30B-A3B-Thinking-2507为3.3倍，相对GPT-OSS-20B为2.2倍。不同精度与引擎选择必须伴随引用，不能称为单一架构的隔离增益。[N2 图1、§1]

### 5.2 Ultra 最大吞吐与单用户延迟分开

Ultra报告图1在 **GB200、NVFP4、8K输入/64K输出、最大吞吐** 条件下，相对GLM-5.1、Kimi-K2.6、Qwen3.5分别为5.9/4.8/1.6倍；Ultra用TRT-LLM、对手用vLLM，各自有无投机解码取较优。它是整套部署的比较，不能解释为相同引擎下纯网络提升，也不能用它给出“DeepInfra 300+ tok/s”的服务承诺。[N6 图1与图注]

**需要保留的反例**：§5 / 图15另测关闭投机解码的GB200 NVL72吞吐，比较8K/64K与 **50K输入/2K输出**。后者偏prefill，Ultra相对Qwen3.5的激活参数更多，MoE GEMM成为主要开销，因而落后；“所有长上下文都更快”的结论不成立。

MTP同样不是固定30–50%延迟收益：小batch时权重读取占主导，多draft可能划算；大batch计算和验证开销增大，较短draft甚至关闭MTP可能更优。论文把draft长度当部署参数，并指出Mamba状态回滚需要额外snapshot，不等同于普通KV截断。[N6 §5 Inference Efficiency / 图15–16]

### 5.3 推理预算的质量代价

Ultra §3.5的medium-effort模式平均生成token约少2.5倍，作者同时报告约7%的准确性下降。这是其AA Intelligence Index V4任务组合上的相对取舍，不是无成本压缩。这些结果对应 AA Intelligence Index V4 的特定任务组合，不足以支持“Index 48 即美国开源第一”的无条件排名；比较还需固定榜单版本、模式与 token 归一化方式。

## 六、上下文、开放资源与许可

Ultra BF16模型卡直接列最长1M，因此“BF16 262K / NVFP4 1M”不是该型号的上下文口径。量化能降低特定部署内存压力，但context上限、某硬件装不装得下和长任务正确率是不同问题。部署仍要固定checkpoint、运行引擎、GPU、并行方式、batch与输入/输出长度。[N5 Model Summary]

开放范围也需区分。官方家族页承诺发布**有权再分发的数据**；Ultra模型卡说披露全部数据来源、发布其中重要部分。不能写成所有预训练/后训练数据和完整旗舰复现条件无缺开放。模型权重可得、训练recipe可读与能复现全部训练是不同级别。

Nano模型卡标注 `nvidia-nemotron-open-model-license`，Ultra BF16卡标注 `openmdw-1.1`；这些 checkpoint 的许可标识不能推广到整个 Nemotron 家族。模型、数据、软件各自的许可证也不能合并；NeMo、TensorRT-LLM、NIM 的许可也应按各项目分别判断，不能统称为专有软件。

## 七、生态事件与仍需补证的范围

NVIDIA 2026-03-16官方新闻稿确认Nemotron Coalition，列出8个创始成员，并称首个NVIDIA/Mistral协作基座将支撑Nemotron4。[N7] 这是一项合作计划，不能作为未发布模型架构或能力的实测证据。下载量、榜单热度和企业业务效果不属于该合作公告可支持的技术结论。

本报告引用的推理效率、量化和训练数字均为论文或官方材料报告值，没有独立下载权重、运行推理或重训验证；跨模型结果须保留原文给出的硬件、精度、输入输出长度和服务栈条件。

仍有若干证据缺口：早期模型原论文、98%合成数据的分母与 RewardBench 比较、Llama-Nemotron 的压缩/蒸馏条件、Nemotron-H/Nano2 速度协议、Super 的完整评测表，以及 Ultra 主评测逐项 harness 与采样预算。相关结论应按来源披露程度谨慎引用。

## 九、主要来源与原文定位

- **N1** [Nemotron 3 家族页](https://research.nvidia.com/labs/nemotron/Nemotron-3/)，初发2025-12-15；及 [家族白皮书2512.20856v1](https://arxiv.org/abs/2512.20856v1)，2025-12-24；相关定位为 Abstract、§1、§2.2–2.4。
- **N2** [Nano技术报告2512.20848](https://arxiv.org/abs/2512.20848)：图1说明计时协议，§4.3/表4/图11说明量化对照；该报告与家族白皮书是不同文档。
- **N3** [Nano BF16模型卡](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16)：Model Description/Design、许可与训练阶段。
- **N4** [NVIDIA Super发布公告](https://blogs.nvidia.com/blog/nemotron-3-super-agentic-ai/)，2026-03-11：参数、1M上下文与发布时间。
- **N5** [Ultra BF16模型卡](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16)：参数、context、Release Date、Model Design与许可标识。
- **N6** [Ultra技术报告2606.15007v1](https://arxiv.org/abs/2606.15007v1)，2026-06-12提交；相关定位包括§1/图1、§2.1–2.2/表1/图3、§3.5/图11、§5推理效率/图15–16。PDF页眉日期为2026-06-16，与arXiv提交日不同。
- **N7** [NVIDIA Coalition新闻稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Launches-Nemotron-Coalition-of-Leading-Global-AI-Labs-to-Advance-Open-Frontier-Models/default.aspx)，2026-03-16：成员、协作方式和未来模型计划。

## 十、参考来源

| # | 论文 / 报告 | 时间 | 链接 |
|---|------------|------|------|
| 1 | Nemotron-4 15B Technical Report | 2024-02 | https://arxiv.org/abs/2402.16819 |
| 2 | Nemotron-4 340B Technical Report | 2024-06 | https://arxiv.org/abs/2406.11704 |
| 3 | Nemotron-H: Hybrid Mamba-Transformer | 2025-04 | https://arxiv.org/abs/2504.03624 |
| 4 | Llama-Nemotron: Efficient Reasoning Models | 2025-05 | https://arxiv.org/abs/2505.00949 |
| 5 | Nemotron Nano 2 | 2025-08 | https://arxiv.org/abs/2508.14444 |
| 6 | Nemotron 3 Nano | 2025-12 | https://arxiv.org/abs/2512.20856 |
| 7 | NVIDIA Nemotron 3 Ultra Review (BuildFastWithAI) | 2026-06 | https://www.buildfastwithai.com/blogs/nvidia-nemotron-3-ultra-review-2026 |
| 8 | NVIDIA GTC Taipei 2026 解析 (AIPostHub) | 2026-06 | https://www.aiposthub.com/nvidia-gtc-taipei-2026-enterprise-ai-agent-nemotron-3-ultra/ |
| 9 | NVIDIA Nemotron 3 Ultra Review (AIToolsRecap) | 2026-06 | https://aitoolsrecap.com/Blog/nvidia-nemotron-3-ultra-550b-computex-2026 |

| 10 | Nemotron Coalition 宣布 (GetAIBook) | 2026-03 | https://getaibook.com/news/nvidia-launches-nemotron-coalition-at-gtc-2026/ |
| 11 | NVIDIA Nemotron 官方页面 | — | https://research.nvidia.com/labs/nemotron/ |
| 12 | Hugging Face Nemotron 模型集合 | — | https://huggingface.co/nvidia |

---

*报告由 AI Agent 自动调研生成，基于公开论文、技术博客、官方发布信息和第三方评测整理。数据截至 2026-06-06。*

## 新鲜度补核（截至 2026-10-23）：Nemotron 3.5 Super 与 Lightning

NVIDIA 于 **2026-10-14/15** 公布 **Nemotron 3.5 Super / Lightning** 模型及材料：Nemotron 项目页标注 10 月 14 日，项目目录标注 10 月 15 日；固定阅读的技术报告首页日期为 **2026-10-21**。这是 6 月版报告之后的实质性训练和推理更新。Super 为 120B 总 / 12B 激活的多模态模型，Lightning 为 30B / 3B 激活的文本模型。新机制主要包括：Super 先延伸至 1M 长上下文，再以 256K 的 agentic 软件工程 mid-training，并用 9B token recovery stage 恢复长上下文；SFT、RLVR、RLHF、专用教师与 MOPD 合并能力；递归 MTP speculative decoding，并对 Super 使用 hidden-state mixing 缓解训练—推理条件分布不匹配。论文报告 Super 在 SWE-bench Pro 为 51.78%；agentic mid-training 受控设置下 DeepSWE pass@1 从 6.4% 到 10.4%，Codex harness 上 SWE-bench Verified 从 48.4% 到 61.8%；并行 agent 执行加自验证则是 test-time scaling 组合设置，在 Terminal-Bench 2.1 从 62.7% 到 71.9%、DeepSWE 从 24.6% 到 34.5%。后两类增益来自不同实验，不能彼此混同或当作单组件消融。量化与服务数字也依赖具体 GPU、工作负载、采样和 harness，详见原文方法。

来源与锚点：NVIDIA Nemotron Research，[Nemotron 3.5 Super and Lightning](https://research.nvidia.com/labs/nemotron/Nemotron-3.5-Super-and-Lightning/)，页面标注发布日 2026-10-14；[NVIDIA Nemotron 项目目录](https://research.nvidia.com/labs/nemotron/projects/)标注 2026-10-15；[技术报告 PDF](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3.5-Super-and-Lightning-Technical-Report.pdf)，封面日期 2026-10-21，§2 预训练 / MTP / 长上下文，§3 后训练与评测（尤其表 10 及 parallel agent + self-verification 对照），§4 量化，§5 推理。该报告以 NVIDIA 官方 PDF 发布，封面日期为 2026-10-21；§2–§5 分别讨论训练、后训练、评测、量化与推理。
