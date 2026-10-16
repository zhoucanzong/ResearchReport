<div align="center">

# 🤖 LLM Research Reports

**AI Agent 驱动的中文大语言模型深度调研报告集**

> ⚠️ **重要声明**：本知识库所有报告均由 AI Agent 自动调研生成，信息来源于公开网络搜索、第三方评测站点、社交媒体及行业媒体报道。由于大模型厂商官方披露程度不一，部分日期、参数、benchmark 数据可能存在错误、过时或未经证实的情况。**所有内容仅供参考，不构成权威结论，建议读者直接查阅各厂商官方渠道获取最新准确信息。**

覆盖 **15 个主流模型 / 系列 + 11 个技术专题** · 持续更新中

[![Monorepo](https://img.shields.io/badge/monorepo-ResearchReport-6f42c1?style=flat-square)](https://github.com/zhoucanzong/ResearchReport)
[![Reports](https://img.shields.io/badge/Reports-43-blue?style=flat-square)](.)
[![Files](https://img.shields.io/badge/Files-43-green?style=flat-square)](.)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

> 📦 **仓库归属**：本报告集现归属 monorepo **[ResearchReport](https://github.com/zhoucanzong/ResearchReport.git)**，在统一仓库中位于根目录 [`LLM-Research/`](https://github.com/zhoucanzong/ResearchReport/tree/main/LLM-Research)，**库内相对路径保持不变**（如 `ModelSeries/Qwen-research/report.md`）。
>
> ```bash
> git clone https://github.com/zhoucanzong/ResearchReport.git
> cd ResearchReport/LLM-Research
> ```
>
> 独立仓库 **LLM-Research** 作为**上游存档仅保留在 GitHub**（`git@github.com:zhoucanzong/LLM-Research.git`），本地副本已于 2026-10-16 移除；本目录内容与其一致，后续更新请以统一仓库 ResearchReport 为准。

---

## 📊 总览

| #  | 图标 | 模型 / 系列                                   | 所属公司  | 报告数 | 亮点                                     |
| -- | :--: | --------------------------------------------- | --------- | :----: | ---------------------------------------- |
| 1  | 🇺🇸 | [**Claude**](./ModelSeries/Claude-research/)           | Anthropic |   1   | Reasoning、Coding、工具使用能力调研      |
| 2  | 🇨🇳 | [**DeepSeek**](./ModelSeries/DeepSeek-research/)       | 深度求索  |   3   | 文本模型 + 多模态 + 专项能力，分拆详述   |
| 3  | 🇨🇳 | [**Doubao-Seed**](./ModelSeries/Doubao-Seed-research/) | 字节跳动  |   1   | 豆包大模型 + Seed 系列技术报告           |
| 4  | 🇺🇸 | [**Gemini**](./ModelSeries/Gemini-research/)           | Google    |   1   | 多模态理解、长上下文、生态整合           |
| 5  | 🇺🇸 | [**Grok**](./ModelSeries/Grok-research/)               | xAI       |   1   | 实时X数据、超大上下文、Musk生态绑定       |
| 6  | 🇨🇳 | [**GLM**](./ModelSeries/GLM-research/)                 | 智谱 AI   |   1   | ChatGLM 系列演进与技术路线               |
| 7  | 🇺🇸 | [**GPT**](./ModelSeries/GPT-research/)                 | OpenAI    |   1   | GPT-4 系列能力边界与生态                 |
| 8  | 🇨🇳 | [**Hunyuan**](./ModelSeries/Hunyuan-research/)         | 腾讯      |   1   | 混元大模型多模态能力调研                 |
| 9  | 🇨🇳 | [**Kimi**](./ModelSeries/Kimi-research/)               | 月之暗面  |   1   | 长上下文、联网搜索特色能力               |
| 10 | 🇺🇸 | [**LLaMA**](./ModelSeries/LLaMA-research/)             | Meta      |   1   | 开源模型生态与技术架构                   |
| 11 | 🇨🇳 | [**MiMo**](./ModelSeries/MiMo-research/)               | 小米      |   1   | 端侧部署与小模型优化方向                 |
| 12 | 🇨🇳 | [**MiniMax**](./ModelSeries/MiniMax-research/)         | MiniMax   |   1   | 多模态与语音能力调研                     |
| 13 | 🇫🇷 | [**Mistral**](./ModelSeries/Mistral-research/)         | Mistral AI|   1   | 欧洲开源领袖、GDPR主权、多语言Tier-1     |
| 14 | 🇺🇸 | [**Nemotron**](./ModelSeries/Nemotron-research/)       | NVIDIA    |   1   | 混合Mamba架构、合成数据、Agentic高效推理 |
| 15 | 🇨🇳 | [**Qwen**](./ModelSeries/Qwen-research/)               | 阿里      |   4   | 文本 + VL + Omni + 生态，覆盖面最广      |

> **🇨🇳 国内 8 家** &nbsp;|&nbsp; **🇺🇸 海外 6 家** &nbsp;|&nbsp; **🇫🇷 欧洲 1 家** &nbsp;|&nbsp; 共 **15 个** 模型系列

### 技术专题

| #  | 图标 | 专题                                          | 覆盖范围  | 报告数 | 亮点                                     |
| -- | :--: | --------------------------------------------- | --------- | :----: | ---------------------------------------- |
| 1  | 🔬 | [**SpeculativeDecoding**](./TechnicalTopics/SpeculativeDecoding-research/) | 投机解码 |   **12**   | EAGLE/DFlash/**随机采样正确性**/**级联异构**/**草稿训练**/**端侧硬件**，经典方法到系统框架 |
| 2  | 🔬 | [**LongContext**](./TechnicalTopics/LongContext-research/) | 长上下文技术 |   1   | FlashAttention、Ring Attention、线性注意力、百万Token窗口 |
| 3  | 🔬 | [**MoE**](./TechnicalTopics/MoE-research/)                 | 混合专家架构 |   1   | Switch→DeepSeekMoE→Routing-Free，负载均衡与推理优化 |
| 4  | 🔬 | [**ReasoningModels**](./TechnicalTopics/ReasoningModels-research/) | 推理模型 |   1   | o1/R1/k1.5，Test-Time Scaling，GRPO/DAPO训练方法 |
| 5  | 🔬 | [**VLM**](./TechnicalTopics/VLM-research/)                 | 多模态大模型 |   1   | GPT-4o/Qwen3-VL，视觉编码器、模态对齐、长视频理解 |
| 6  | 🔬 | [**Agent**](./TechnicalTopics/Agent-research/)             | Agent架构   |   1   | ReAct/MCP/A2A，多Agent系统，工具使用与记忆 |
| 7  | 🔬 | [**Alignment**](./TechnicalTopics/Alignment-research/)     | 模型对齐    |   1   | RLHF/DPO/GRPO/DAPO，安全对齐与奖励黑客缓解 |
| 8  | 🔬 | [**TrainingInfra**](./TechnicalTopics/TrainingInfra-research/) | 训练基础设施 |   1   | DeepSpeed/FSDP/Megatron，3D并行，万卡集群 |
| 9  | 🔬 | [**QuantizationEdge**](./TechnicalTopics/QuantizationEdge-research/) | 量化与边缘部署 |   1   | AWQ/GPTQ/GGUF/FP8，vLLM/Ollama，Jetson边缘 |
| 10 | 🔬 | [**RAG**](./TechnicalTopics/RAG-research/)                 | 检索增强生成 |   1   | RAG 0.0→4.0，GraphRAG，Agentic RAG，混合检索 |
| 11 | 🔬 | [**DecisionModels**](./TechnicalTopics/DecisionModels-research/) | 决策模型（System One / Typed Decision Model） |  **17**   | Choice/Score/Noul 类型化输出、隐藏状态直读、零输出 token、`confidence` 语义；**RLCD 同名消歧**（≠ 2023 Contrastive Distillation）；官方九类 jaggedness；第三方研究地图含**失效与攻击**；**JEV 为主线案例**，同类含 `this-that-model` / `Laya` / `Kev` / `JevLite`；**第二批新增逐篇论文提取 12 篇（`papers/`）与开源实现情报（`open-implementations.md`）** |

> **🔬 技术专题 11 个** &nbsp;|&nbsp; 共 **46 份** Markdown 报告
>
> **DecisionModels 条目已升格为领域研究（第一批·结构层）**：主文档 `report.md` + 三份子文档 [`taxonomy.md`](./TechnicalTopics/DecisionModels-research/taxonomy.md)（边界 / 接口谱系 / 训练目标谱系 + Mermaid 分类图）、[`calibration.md`](./TechnicalTopics/DecisionModels-research/calibration.md)（ECE / Brier / 可靠性曲线的跨域-跨语言-不平衡-OOD 证据链）、[`experiments.md`](./TechnicalTopics/DecisionModels-research/experiments.md)（§八 复核清单的可执行实验协议）。
>
> **第二批·证据层（2026-10-16）**：新增 [`papers/`](./TechnicalTopics/DecisionModels-research/papers/)（**12 篇逐篇结构化提取**，统一 方法 / 实验 / 数字+条件 / 失效边界 / 关联本条目结论 模板，每条数字附可 grep 的 `find:` 串）与 [`open-implementations.md`](./TechnicalTopics/DecisionModels-research/open-implementations.md)（`this-that-model` / `Laya` / `Kev` / `JevLite` / `Visual Jev` 的 readout 实现路径、权重与许可、接口依赖与模型卡口径，外链全部实测状态码）。

---

## 📁 仓库结构

```
LLM-research/
├── ModelSeries/                    # 模型系列报告（15 个主流模型 / 系列）
│   ├── Claude-research/            #   Anthropic Claude 系列
│   │   └── report.md
│   ├── DeepSeek-research/          #   深度求索 DeepSeek 系列
│   │   ├── report.md               #     主报告
│   │   ├── deepseek-text-models.md #     文本模型专题
│   │   └── deepseek-multimodal-... #     多模态与专项能力
│   ├── Doubao-Seed-research/       #   字节跳动豆包 / Seed
│   ├── GLM-research/               #   智谱 GLM 系列
│   ├── GPT-research/               #   OpenAI GPT 系列
│   ├── Gemini-research/            #   Google Gemini 系列
│   ├── Grok-research/              #   xAI Grok 系列
│   ├── Hunyuan-research/           #   腾讯混元系列
│   ├── Kimi-research/              #   月之暗面 Kimi 系列
│   ├── LLaMA-research/             #   Meta LLaMA 系列
│   ├── MiMo-research/              #   小米 MiMo 系列
│   ├── MiniMax-research/           #   MiniMax 系列
│   ├── Mistral-research/           #   Mistral AI 系列
│   ├── Nemotron-research/          #   NVIDIA Nemotron 系列
│   └── Qwen-research/              #   阿里通义千问系列
│       ├── report.md               #     主报告
│       ├── qwen-text-models.md     #     文本模型专题
│       ├── qwen-vl-models.md       #     视觉语言模型专题
│       └── qwen-omni-and-ecosystem.md  #     Omni 模型与生态
│
└── TechnicalTopics/                # 技术专题报告（11 个核心技术方向）
    ├── SpeculativeDecoding-research/   # 投机解码技术专题（12 份）
    │   ├── report.md                       #   主报告：技术脉络、指标口径、四条瓶颈、框架、QwenAccel-Train
    │   ├── speculative-classical-and-self.md   #   经典方法与自投机（Medusa/Hydra/Lookahead/SWIFT/CLaSp）
    │   ├── speculative-eagle-series.md         #   EAGLE 系列（含 T>0 下动态树塌缩的限定）
    │   ├── speculative-stochastic-verification.md #  随机采样与验证正确性（RheoSampling/Traversal Verification/ARC-Decode）
    │   ├── speculative-block-diffusion.md        #   块扩散与检索式（DFlash/DSpark/BASTION/CAST/REST/PLD）
    │   ├── speculative-cascade-heterogeneous.md #   级联与异构草稿（HCSpec/HeteroSpec）
    │   ├── speculative-draft-training-2026.md   #   草稿模型训练新法（AdaSPEC/Attention Drift/TLT）
    │   ├── speculative-training-optimization.md #   训练目标优化（部分链接为未确证占位符）
    │   ├── speculative-edge-cloud-hardware.md   #   端侧·边缘·硬件（FlexSpec/SS-MoE/SMoLPU/TPU）
    │   ├── speculative-domain-language.md       #   领域与语种特化（DictSpec/CDSL）
    │   ├── speculative-multimodal.md           #   多模态投机解码（VLM/视频/VLA/语音）
    │   └── speculative-systems-and-frameworks.md #   系统级优化与框架生态（vLLM/SGLang/llama.cpp）
    ├── LongContext-research/             # 长上下文技术专题
    │   └── report.md                     #   FlashAttention、Ring Attention、线性注意力、百万Token窗口
    ├── MoE-research/                     # 混合专家架构专题
    │   └── report.md                     #   Switch→DeepSeekMoE→Routing-Free，负载均衡与推理优化
    ├── ReasoningModels-research/         # 推理模型专题
    │   └── report.md                     #   o1/R1/k1.5，Test-Time Scaling，GRPO/DAPO训练方法
    ├── VLM-research/                     # 多模态大模型专题
    │   └── report.md                     #   GPT-4o/Qwen3-VL，视觉编码器、模态对齐、长视频理解
    ├── Agent-research/                   # Agent架构专题
    │   └── report.md                     #   ReAct/MCP/A2A，多Agent系统，工具使用与记忆
    ├── Alignment-research/               # 模型对齐专题
    │   └── report.md                     #   RLHF/DPO/GRPO/DAPO，安全对齐与奖励黑客缓解
    ├── TrainingInfra-research/           # 训练基础设施专题
    │   └── report.md                     #   DeepSpeed/FSDP/Megatron，3D并行，万卡集群
    ├── QuantizationEdge-research/        # 量化与边缘部署专题
    │   └── report.md                     #   AWQ/GPTQ/GGUF/FP8，vLLM/Ollama，Jetson边缘
    └── RAG-research/                     # 检索增强生成专题
        └── report.md                     #   RAG 0.0→4.0，GraphRAG，Agentic RAG，混合检索
    └── DecisionModels-research/          # 决策模型（System One）专题 · JEV 为主线案例
        └── report.md                     #   类型化输出/零输出token/RLCD 消歧/失效与攻击地图
```

---

## 🔍 使用方式

```bash
# 克隆统一仓库并进入本报告集
git clone https://github.com/zhoucanzong/ResearchReport.git
cd ResearchReport/LLM-Research

# 浏览某份报告（库内相对路径不变）
cat ModelSeries/Qwen-research/report.md

# 全文搜索（例：搜索所有提到 "MoE" 的报告）
grep -r "MoE" --include="*.md" .
```

---

## ✨ 特色

- 🧠 **AI Agent 生成** — 所有报告由 Claude / DeepSeek / Kimi 等 Agent 自动调研撰写
- 📊 **结构化内容** — 统一模板：模型列表 → 关键能力 → 生态 → 竞品对比
- 🌐 **中英双语** — 报告内容以中文为主，关键术语保留英文
- 🔗 **可追溯** — 部分报告附带来源索引、论文原文、阅读笔记

---

## 🤝 贡献

欢迎提交 PR 补充新的模型调研、更新过时内容或修正错误。

---

<div align="center">

*Made with ❤️ by AI Agents & [zhoucanzong](https://github.com/zhoucanzong)*

</div>
