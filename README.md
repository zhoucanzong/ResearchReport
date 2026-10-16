<div align="center">

# 📚 ResearchReport

**一个仓库收敛 AIGC / LLM / 论文深读全部研究产出**

![Collections](https://img.shields.io/badge/Collections-3-blue?style=flat-square)
![Reports](https://img.shields.io/badge/Reports-46-green?style=flat-square)
![Topic](https://img.shields.io/badge/Topic-21-orange?style=flat-square)
![Markdown](https://img.shields.io/badge/Markdown-83-lightgrey?style=flat-square)
![Updated](https://img.shields.io/badge/Updated-2026--10--16-informational?style=flat-square)

</div>

---

## 🗂 一眼看懂

<table>
<tr>
<td align="center" width="33%">

<b>🎨 AIGC-Research</b>

<br><br>

生成式 AI 多模态调研<br>聚焦 <b>U-Net → DiT → 3D DiT</b> 架构演进

<br><br>

<b>18</b> 份报告<br>8 个模型系列 + 10 个技术专题

<br><br>

<a href="AIGC-Research/">浏览目录</a> · <a href="AIGC-Research/README.md">库内索引</a>

</td>
<td align="center" width="33%">

<b>🤖 LLM-Research</b>

<br><br>

大语言模型全景调研<br>能力边界 · 对齐 · 推理加速 · 训练部署

<br><br>

<b>26</b> 份报告<br>15 个模型系列 + 11 个技术专题

<br><br>

<a href="LLM-Research/">浏览目录</a> · <a href="LLM-Research/README.md">库内索引</a>

</td>
<td align="center" width="33%">

<b>📑 Repo-Research</b>

<br><br>

论文与开源仓库深读<br>源码剖析 + 单论文精读全流程

<br><br>

<b>13</b> 个文件<br>3 个深度阅读项目<br>（非 Git 仓库，无库内 README）

<br><br>

<a href="Repo-Research/">浏览目录</a> · <a href="docs/statistics.md">统计明细</a>

</td>
</tr>
</table>

> **AIGC-Research** 关注「生成」：图像 / 视频 / 3D / 音频 / 数字人。
> **LLM-Research** 关注「理解与推理」：模型能力、Benchmark、训练与部署全栈，其中 DeepSeek、Qwen、SpeculativeDecoding 为多分册展开。
> **Repo-Research** 关注「单个系统」：`mini-swe-agent` 源码级架构报告 + Nemotron-Labs-Diffusion 论文精读（计划、笔记、概念卡、原始提取、结构化 JSON）+ SGLang 推理引擎源码分析（调度器 / 前缀缓存 / 投机解码）。

---

## 🚀 快速开始

```bash
# 克隆
git clone https://github.com/zhoucanzong/ResearchReport.git
cd ResearchReport

# 浏览
cat README.md                       # 本页：统一索引
cat AIGC-Research/README.md         # AIGC 库内索引
cat LLM-Research/README.md          # LLM 库内索引
# Repo-Research 无库内 README —— 逐项索引见下方「完整索引」

# 全域检索（例：找所有提到 DiT 的报告）
grep -r "DiT" --include='*.md' AIGC-Research LLM-Research Repo-Research
```

---

## 📊 统计摘要

| 资料库 | 内容 | 条目（`report.md`） | 子文档 `.md` | 正文字节 | 目录内容字节 | `du -sk` |
| :-- | :-- | --: | --: | --: | --: | --: |
| 🎨 [AIGC-Research](AIGC-Research/) | 8 系列 + 10 专题 | 18 | 1 | 671,827 B | 679,964 B | 704 KB |
| 🤖 [LLM-Research](LLM-Research/) | 15 系列 + 11 专题 | 26 | 33 | 1,695,700 B | 1,710,402 B | 1780 KB |
| 📑 [Repo-Research](Repo-Research/) | 3 个深读项目 | 2 | 10 | 262,771 B | 279,065 B | 300 KB |
| **合计** | **3 个资料库** | **46** | **44** | **2,630,298 B ≈ 2.51 MiB** | **2,669,431 B ≈ 2.55 MiB** | **2,784 KB** |

> 本表数字由 [`scripts/library_index.py`](scripts/library_index.py) 产出，机器可读版见 [`index/stats.json`](index/stats.json)；**条目 = 文件名字面为 `report.md` 的主文档**，同目录其它 `.md`（分册 / `plan.md` / `notes/` / `raw-extracts/` 等）是它的**子文档**。
> **口径细化（2026-10-16 复测）**：本表中「条目数 / 子文档数」取自 `index/stats.json`；「正文字节 / 目录内容字节 / `du -sk`」为**逐库实测**——「正文字节」= 该库内**除 `README.md` 外的全部 `.md`** 的字节和（LLM-Research = 58 份 / 1,695,700 B），「目录内容字节」= 该库目录下全部文件（跳过隐藏目录），`du -sk` 含文件系统块开销。上一版 LLM-Research 的「正文字节」列（1,764,826 B）与同表其它列**不同源**（约多计 6.9 万 B），本次已按上述可复现口径统一重测。
> 各库 `README.md` 与 `docs/*.md` 既不是条目也不是子文档，不计入本表；「目录内容字节」不含 `.git` 且按脚本口径跳过隐藏目录；`du -sk` 含文件系统块开销，故大于字节数之和。
> 全仓库 Markdown 共 **104** 份（`git ls-files '*.md'` 实测；含生成物 8 份，故非生成物 96 份）。各口径的换算关系见 [`docs/statistics.md`](docs/statistics.md) §2。
> **索引入口**：[`INDEX.md`](INDEX.md)（总目录）· [`docs/team.md`](docs/team.md)（团队约定）。
> **逐目录明细**（每个报告的行数 / 字节、统计方法与口径说明）见 **[docs/statistics.md](docs/statistics.md)**。

---

## 📖 完整索引

<details>
<summary><b>🎨 AIGC-Research</b> — 18 份条目（8 模型系列 + 10 技术专题）</summary>

<br>

**模型系列（8 个）**

| # | 系列 | 所属公司 | 亮点 | 报告 |
| :--: | :-- | :-- | :-- | :-- |
| 1 | **StabilityAI** | Stability AI / BFL | SD 1.x→2.x→XL→3→FLUX，U-Net→DiT 架构演进 | [目录](AIGC-Research/ModelSeries/StabilityAI-research/) · [报告](AIGC-Research/ModelSeries/StabilityAI-research/report.md) |
| 2 | **OpenAI-Gen** | OpenAI | DALL-E 2/3 → GPT-4o 图像生成 → Sora，自回归 + 扩散混合架构 | [目录](AIGC-Research/ModelSeries/OpenAI-Gen-research/) · [报告](AIGC-Research/ModelSeries/OpenAI-Gen-research/report.md) |
| 3 | **Google-Gen** | Google / DeepMind | Imagen 2/3 → Veo 2/3/3.1，级联扩散 → DiT 视频生成 | [目录](AIGC-Research/ModelSeries/Google-Gen-research/) · [报告](AIGC-Research/ModelSeries/Google-Gen-research/report.md) |
| 4 | **Midjourney** | Midjourney | V4→V5→V6→V7，闭源标杆的架构推测与美学进化 | [目录](AIGC-Research/ModelSeries/Midjourney-research/) · [报告](AIGC-Research/ModelSeries/Midjourney-research/report.md) |
| 5 | **Kling** | 快手 | 可灵 1.0→2.0→3.0/O1，国产视频生成的 DiT 架构路线 | [目录](AIGC-Research/ModelSeries/Kling-research/) · [报告](AIGC-Research/ModelSeries/Kling-research/report.md) |
| 6 | **Runway** | Runway | Gen-1→Gen-4.5，Latent Diffusion → DiT 视频编辑与生成 | [目录](AIGC-Research/ModelSeries/Runway-research/) · [报告](AIGC-Research/ModelSeries/Runway-research/report.md) |
| 7 | **ByteDance-Gen** | 字节跳动 | Seedance 1.0→2.0，即梦 AI，多模态 cinematic 生成 | [目录](AIGC-Research/ModelSeries/ByteDance-Gen-research/) · [报告](AIGC-Research/ModelSeries/ByteDance-Gen-research/report.md) |
| 8 | **Alibaba-Gen** | 阿里巴巴 | 通义万相 Wan 2.1/2.2/2.6，开源视频生成的 DiT 架构 | [目录](AIGC-Research/ModelSeries/Alibaba-Gen-research/) · [报告](AIGC-Research/ModelSeries/Alibaba-Gen-research/report.md) |

**技术专题（10 个）**

| # | 专题 | 覆盖范围 | 亮点 | 报告 |
| :--: | :-- | :-- | :-- | :-- |
| 1 | **DiffusionModels** | 扩散模型基础 | DDPM→DDIM→LDM→Consistency Models，数学框架与采样加速 | [目录](AIGC-Research/TechnicalTopics/DiffusionModels-research/) · [报告](AIGC-Research/TechnicalTopics/DiffusionModels-research/report.md) |
| 2 | **DiT** | Diffusion Transformer | U-Net→DiT 架构革命，PixArt→SD3→FLUX→Sora 的 Transformer 化 | [目录](AIGC-Research/TechnicalTopics/DiT-research/) · [报告](AIGC-Research/TechnicalTopics/DiT-research/report.md) |
| 3 | **VideoGen** | 视频生成技术 | 时序建模、3D DiT、因果注意力、运动一致性 | [目录](AIGC-Research/TechnicalTopics/VideoGen-research/) · [报告](AIGC-Research/TechnicalTopics/VideoGen-research/report.md) |
| 4 | **ControllableGen** | 可控生成 | ControlNet→IP-Adapter→T2I-Adapter→LoRA，条件注入架构演进 | [目录](AIGC-Research/TechnicalTopics/ControllableGen-research/) · [报告](AIGC-Research/TechnicalTopics/ControllableGen-research/report.md) |
| 5 | **3DGen** | 3D 生成 | DreamFusion→Point-E→Shap-E→Tripo3D，NeRF→3D Gaussian Splatting | [目录](AIGC-Research/TechnicalTopics/3DGen-research/) · [报告](AIGC-Research/TechnicalTopics/3DGen-research/report.md) |
| 6 | **AudioGen** | 音频 / 音乐生成 | AudioLDM→MusicLM→Suno/Udio，扩散 + 自回归 + 流匹配 | [目录](AIGC-Research/TechnicalTopics/AudioGen-research/) · [报告](AIGC-Research/TechnicalTopics/AudioGen-research/report.md) |
| 7 | **AvatarGen** | 数字人 / Avatar 生成 | Wav2Lip→SadTalker→OmniHuman-1，CNN→3DMM→DiT 统一生成 | [目录](AIGC-Research/TechnicalTopics/AvatarGen-research/) · [报告](AIGC-Research/TechnicalTopics/AvatarGen-research/report.md) |
| 8 | **ImageEditing** | 图像编辑与修复 | GAN→InstructPix2Pix→DiT Joint Attention→Agentic 编辑 | [目录](AIGC-Research/TechnicalTopics/ImageEditing-research/) · [报告](AIGC-Research/TechnicalTopics/ImageEditing-research/report.md) |
| 9 | **WorldModels** | 世界模型 | action 条件化的视频 / 3D 生成、潜空间预测（JEPA / Dreamer）、world foundation model 平台；判据 = action 条件化 + 系统可调用 + 动力学自数据学得 | [目录](AIGC-Research/TechnicalTopics/WorldModels-research/) · [报告](AIGC-Research/TechnicalTopics/WorldModels-research/report.md) |
| 10 | **EmbodiedVLA** | 具身 VLA | Vision-Language-Action 策略：判据 = 视觉 + 语言条件化 + 直接输出动作；动作表征三路线 token / flow matching / diffusion head，代表 RT-2 · π0 · OpenVLA · GR00T；与世界模型作为训练环境互引 | [目录](AIGC-Research/TechnicalTopics/EmbodiedVLA-research/) · [报告](AIGC-Research/TechnicalTopics/EmbodiedVLA-research/report.md) |

库内索引：[AIGC-Research/README.md](AIGC-Research/README.md) ｜ 目录：[AIGC-Research/](AIGC-Research/)

</details>

<details>
<summary><b>🤖 LLM-Research</b> — 26 份条目 + 16 份分册（15 模型系列 + 11 技术专题）</summary>

<br>

**模型系列（15 个系列 / 15 份条目 + 5 份分册；分册已标注份数）**

| # | 系列 | 所属公司 | 亮点 | 报告 |
| :--: | :-- | :-- | :-- | :-- |
| 1 | **Claude** | Anthropic | Reasoning、Coding、工具使用能力 | [目录](LLM-Research/ModelSeries/Claude-research/) · [报告](LLM-Research/ModelSeries/Claude-research/report.md) |
| 2 | **DeepSeek**（3 份） | 深度求索 | 文本模型 + 多模态 + 专项能力，分拆详述 | [目录](LLM-Research/ModelSeries/DeepSeek-research/) · [主报告](LLM-Research/ModelSeries/DeepSeek-research/report.md) · [文本模型](LLM-Research/ModelSeries/DeepSeek-research/deepseek-text-models.md) · [多模态与专项](LLM-Research/ModelSeries/DeepSeek-research/deepseek-multimodal-and-specialized.md) |
| 3 | **Doubao-Seed** | 字节跳动 | 豆包大模型 + Seed 系列技术报告 | [目录](LLM-Research/ModelSeries/Doubao-Seed-research/) · [报告](LLM-Research/ModelSeries/Doubao-Seed-research/report.md) |
| 4 | **GLM** | 智谱 AI | ChatGLM 系列演进与技术路线 | [目录](LLM-Research/ModelSeries/GLM-research/) · [报告](LLM-Research/ModelSeries/GLM-research/report.md) |
| 5 | **GPT** | OpenAI | GPT-4 系列能力边界与生态 | [目录](LLM-Research/ModelSeries/GPT-research/) · [报告](LLM-Research/ModelSeries/GPT-research/report.md) |
| 6 | **Gemini** | Google | 多模态理解、长上下文、生态整合 | [目录](LLM-Research/ModelSeries/Gemini-research/) · [报告](LLM-Research/ModelSeries/Gemini-research/report.md) |
| 7 | **Grok** | xAI | 实时 X 数据、超大上下文、Musk 生态绑定 | [目录](LLM-Research/ModelSeries/Grok-research/) · [报告](LLM-Research/ModelSeries/Grok-research/report.md) |
| 8 | **Hunyuan** | 腾讯 | 混元大模型多模态能力 | [目录](LLM-Research/ModelSeries/Hunyuan-research/) · [报告](LLM-Research/ModelSeries/Hunyuan-research/report.md) |
| 9 | **Kimi** | 月之暗面 | 长上下文、联网搜索特色能力 | [目录](LLM-Research/ModelSeries/Kimi-research/) · [报告](LLM-Research/ModelSeries/Kimi-research/report.md) |
| 10 | **LLaMA** | Meta | 开源模型生态与技术架构 | [目录](LLM-Research/ModelSeries/LLaMA-research/) · [报告](LLM-Research/ModelSeries/LLaMA-research/report.md) |
| 11 | **MiMo** | 小米 | 端侧部署与小模型优化方向 | [目录](LLM-Research/ModelSeries/MiMo-research/) · [报告](LLM-Research/ModelSeries/MiMo-research/report.md) |
| 12 | **MiniMax** | MiniMax | 多模态与语音能力 | [目录](LLM-Research/ModelSeries/MiniMax-research/) · [报告](LLM-Research/ModelSeries/MiniMax-research/report.md) |
| 13 | **Mistral** | Mistral AI | 欧洲开源领袖、GDPR 主权、多语言 Tier-1 | [目录](LLM-Research/ModelSeries/Mistral-research/) · [报告](LLM-Research/ModelSeries/Mistral-research/report.md) |
| 14 | **Nemotron** | NVIDIA | 混合 Mamba 架构、合成数据、Agentic 高效推理 | [目录](LLM-Research/ModelSeries/Nemotron-research/) · [报告](LLM-Research/ModelSeries/Nemotron-research/report.md) |
| 15 | **Qwen**（4 份） | 阿里巴巴 | 文本 + VL + Omni + 生态，覆盖面最广 | [目录](LLM-Research/ModelSeries/Qwen-research/) · [主报告](LLM-Research/ModelSeries/Qwen-research/report.md) · [文本模型](LLM-Research/ModelSeries/Qwen-research/qwen-text-models.md) · [VL 模型](LLM-Research/ModelSeries/Qwen-research/qwen-vl-models.md) · [Omni 与生态](LLM-Research/ModelSeries/Qwen-research/qwen-omni-and-ecosystem.md) |

> 国内 8 家 · 海外 6 家 · 欧洲 1 家 · 共 15 个系列

**技术专题（11 个 / 11 份条目 + 11 份分册；分册已标注份数）**

| # | 专题 | 覆盖范围 | 亮点 | 报告 |
| :--: | :-- | :-- | :-- | :-- |
| 1 | **SpeculativeDecoding**（12 份） | 投机解码 | EAGLE / DFlash / **随机采样正确性** / **级联异构** / **草稿训练** / **端侧硬件**，经典方法到系统框架 | [目录](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/) · [主报告](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/report.md) · [经典与自投机](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-classical-and-self.md) · [EAGLE 系列](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-eagle-series.md) · [**随机采样与验证正确性**](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-stochastic-verification.md) · [块扩散与检索式](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-block-diffusion.md) · [**级联与异构草稿**](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-cascade-heterogeneous.md) · [**草稿模型训练新法**](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-draft-training-2026.md) · [训练目标优化](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-training-optimization.md) · [**端侧·边缘·硬件**](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-edge-cloud-hardware.md) · [**领域与语种特化**](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-domain-language.md) · [多模态投机](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-multimodal.md) · [系统与框架](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-systems-and-frameworks.md) |
| 2 | **LongContext** | 长上下文技术 | FlashAttention、Ring Attention、线性注意力、百万 Token 窗口 | [目录](LLM-Research/TechnicalTopics/LongContext-research/) · [报告](LLM-Research/TechnicalTopics/LongContext-research/report.md) |
| 3 | **MoE** | 混合专家架构 | Switch→DeepSeekMoE→Routing-Free，负载均衡与推理优化 | [目录](LLM-Research/TechnicalTopics/MoE-research/) · [报告](LLM-Research/TechnicalTopics/MoE-research/report.md) |
| 4 | **ReasoningModels** | 推理模型 | o1/R1/k1.5，Test-Time Scaling，GRPO/DAPO 训练方法 | [目录](LLM-Research/TechnicalTopics/ReasoningModels-research/) · [报告](LLM-Research/TechnicalTopics/ReasoningModels-research/report.md) |
| 5 | **VLM** | 多模态大模型 | GPT-4o / Qwen3-VL，视觉编码器、模态对齐、长视频理解 | [目录](LLM-Research/TechnicalTopics/VLM-research/) · [报告](LLM-Research/TechnicalTopics/VLM-research/report.md) |
| 6 | **Agent** | Agent 架构 | ReAct/MCP/A2A，多 Agent 系统，工具使用与记忆 | [目录](LLM-Research/TechnicalTopics/Agent-research/) · [报告](LLM-Research/TechnicalTopics/Agent-research/report.md) |
| 7 | **Alignment** | 模型对齐 | RLHF/DPO/GRPO/DAPO，安全对齐与奖励黑客缓解 | [目录](LLM-Research/TechnicalTopics/Alignment-research/) · [报告](LLM-Research/TechnicalTopics/Alignment-research/report.md) |
| 8 | **TrainingInfra** | 训练基础设施 | DeepSpeed/FSDP/Megatron，3D 并行，万卡集群 | [目录](LLM-Research/TechnicalTopics/TrainingInfra-research/) · [报告](LLM-Research/TechnicalTopics/TrainingInfra-research/report.md) |
| 9 | **QuantizationEdge** | 量化与边缘部署 | AWQ/GPTQ/GGUF/FP8，vLLM/Ollama，Jetson 边缘 | [目录](LLM-Research/TechnicalTopics/QuantizationEdge-research/) · [报告](LLM-Research/TechnicalTopics/QuantizationEdge-research/report.md) |
| 10 | **RAG** | 检索增强生成 | RAG 0.0→4.0，GraphRAG，Agentic RAG，混合检索 | [目录](LLM-Research/TechnicalTopics/RAG-research/) · [报告](LLM-Research/TechnicalTopics/RAG-research/report.md) |
| 11 | **DecisionModels** | 决策模型（System One / Typed Decision Model） | 类型化输出（Choice/Score/Noul）、隐藏状态直读、零输出 token、`confidence` 语义；**RLCD 同名消歧**（≠ 2023 Contrastive Distillation）；官方九类 jaggedness；第三方研究地图含**失效与攻击**；**JEV 为主线案例**，同类含 `this-that-model` / `Laya` / `Kev` / `JevLite` | [目录](LLM-Research/TechnicalTopics/DecisionModels-research/) · [报告](LLM-Research/TechnicalTopics/DecisionModels-research/report.md) |

库内索引：[LLM-Research/README.md](LLM-Research/README.md) ｜ 目录：[LLM-Research/](LLM-Research/)

</details>

<details>
<summary><b>📑 Repo-Research</b> — 9 个文件（2 个深度阅读项目）</summary>

<br>

> 本库**没有自己的 `README.md`**，本节即其唯一索引。它**不是 Git 仓库**（无 `.git`、无提交历史、无上游存档），不套用 `ModelSeries/ TechnicalTopics/` 模板，而是按项目建目录。

**① [mini-swe-agent-research/](Repo-Research/mini-swe-agent-research/) — 开源 agent 源码深度剖析**

| 文件 | 大小 / 行数 | 说明 |
| :-- | --: | :-- |
| [mini-swe-agent-deep-report.md](Repo-Research/mini-swe-agent-research/mini-swe-agent-deep-report.md) | 34,490 B / 735 行 | **mini-swe-agent v2.3.0 深度架构报告**（2026-06-06）：Princeton & Stanford SWE-agent 团队的极简 SWE agent（约 5,200 行 Python / 9,100 行测试，唯一工具是 bash、线性消息历史、SWE-bench verified >74%）；含 Codebase Map / Runtime Story / Design Inquiry / Maintainer Notes / Diagrams / Evidence Index 六部分 |

**② [nemotron-tri-mode-diffusion/](Repo-Research/nemotron-tri-mode-diffusion/) — 单论文精读全流程**

论文：**Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding**（Yonggan Fu 等，NVIDIA + Georgia Tech + HKU + MIT，2026-05-19，21 页）

| 文件 | 大小 / 行数 | 说明 |
| :-- | --: | :-- |
| [report.md](Repo-Research/nemotron-tri-mode-diffusion/report.md) | 13,183 B / 206 行 | **中文综述报告**（2026-05-27）：执行摘要 + 核心发现（AR 与 Diffusion 互补、Self-Speculation 优于 MTP/Eagle3、SOL 仍有 76.5% 空间）+ 每条的**个人解读** |
| [plan.md](Repo-Research/nemotron-tri-mode-diffusion/plan.md) | 2,561 B / 28 行 | **研究计划**：核心研究问题、5 个子问题分解（训练框架 / 三模式推理 / SOL 分析 / 实证 / 核心洞见）、搜索策略、范围决策与产出物清单 |
| [knowledge-graph.md](Repo-Research/nemotron-tri-mode-diffusion/knowledge-graph.md) | 10,088 B / 136 行 | **核心概念卡片**（按理解依赖组织）：Tri-Mode Language Model、Block-wise Diffusion、Self-Speculation Decoding 等，每卡含定义 / 类比 / 数学表达 / 关联概念 / 常见误区 |
| [sources-index.md](Repo-Research/nemotron-tri-mode-diffusion/sources-index.md) | 2,363 B / 41 行 | **来源索引**：主论文条目（作者 / 日期 / 页数 / 开源与训练框架）、PDF 提取文件指路、论文重要引用上下文表（SPEED-Bench、LLaDA、Dream、Eagle-3、LoRA 等） |
| [notes/structured-reading.md](Repo-Research/nemotron-tri-mode-diffusion/notes/structured-reading.md) | 10,416 B / 169 行 | **结构化阅读笔记**（中文）：一句话总结 + 逐章节要点（研究背景三问、训练框架、三模式推理、SOL、实验结论），是 `report.md` 的详细底稿 |
| [raw-extracts/nemotron-tri-mode-fulltext.md](Repo-Research/nemotron-tri-mode-diffusion/raw-extracts/nemotron-tri-mode-fulltext.md) | 98,525 B / 2,430 行 | **论文 PDF 全文提取**（21 页，逐页文本，约 96K 字符）—— 本库体积最大的文件，供全文检索与原文核对 |
| [raw-extracts/pdf-fu_等__…dif.md](Repo-Research/nemotron-tri-mode-diffusion/raw-extracts/pdf-fu_%E7%AD%89__nemotronlabsdiffusion_a_trimode_language_model_unifying_autoregressive_dif.md) | 1,141 B / 28 行 | **PDF 提取占位/模板**（脚本自动生成，正文未填入）—— 实际全文见上一条，保留它是为记录提取流程，**勿当作论文全文** |
| [papers/nemotron-labs-diffusion.json](Repo-Research/nemotron-tri-mode-diffusion/papers/nemotron-labs-diffusion.json) | 16,294 B / 47 行 | **结构化阅读 JSON**：基本信息 / 内容摘要 / 研究背景 / 核心方法 / 实验与结果 / 分析与讨论 / 个人评价，含 `relevance: 10`、`quality: 9` 等评分字段，便于检索或二次加工 |

</details>

---

## 🛠 维护速览

- **新增报告**：在 `AIGC-Research/` 或 `LLM-Research/` 的 `ModelSeries/` / `TechnicalTopics/` 下建 `<Name>-research/` 目录，主报告命名为 `report.md`；深挖时用 `<topic>-<sub>.md` 分册。
- **新增深读项目**：在 `Repo-Research/` 下按项目建目录，建议包含 `report.md`、`plan.md`、`knowledge-graph.md`、`sources-index.md`、`notes/`、`raw-extracts/`、`papers/*.json`。
- **更新索引**：同步本页「完整索引」折叠块、顶部徽章计数与 [docs/statistics.md](docs/statistics.md)。
- **与上游同步**：仅 `AIGC-Research`、`LLM-Research` 有 GitHub 存档仓库，用 `rsync` 导入变化（先 `--dry-run`）；`Repo-Research` 无上游，本仓库即权威副本。

完整流程（含提交前检查清单）见 **[docs/maintenance.md](docs/maintenance.md)**。

---

## 📚 文档

| 文件 | 内容 |
| :-- | :-- |
| [docs/statistics.md](docs/statistics.md) | 逐目录 / 逐文件的完整体积与数量统计、统计方法与口径 |
| [docs/verification.md](docs/verification.md) | 全部校验留证：上游仓库最终状态、复制校验、扁平化校验、Repo-Research 复制与移除留证 |
| [docs/maintenance.md](docs/maintenance.md) | 维护流程、提交前检查清单、已知问题与限制 |
| [docs/team.md](docs/team.md) | 团队约定：成员与范围、协作规则、条目定义与统计口径 |

---

<div align="center">

<sub>⚠️ <b>免责声明</b>：本仓库中的调研报告由 <b>AI Agent 自动调研生成</b>，深度阅读笔记为人工 + Agent 整理，均<b>未经官方确认</b>；日期、参数、benchmark 等数据可能过时或存在错误。引用前请回溯各报告内的原始来源。</sub>

<br><br>

<sub>ResearchReport · 最后更新 2026-10-16</sub>

</div>
