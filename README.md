# 📚 ResearchReport · AIGC & LLM 研究报告统一索引

**AI Agent 驱动的中文研究报告聚合仓库（monorepo）** —— 一个仓库，收纳两个调研报告库：生成式 AI（AIGC / 图像 · 视频 · 3D · 音频）方向与**大语言模型（LLM）**方向。

## 本仓库说明

| 项目 | 内容 |
| :-- | :-- |
| **仓库名** | **ResearchReport** |
| **远端（origin）** | <https://github.com/zhoucanzong/ResearchReport.git> |
| **克隆** | `git clone https://github.com/zhoucanzong/ResearchReport.git` |
| **仓库布局** | 根目录 `README.md`（本索引）＋ [`AIGC-Research/`](AIGC-Research/)（16 份报告）＋ [`LLM-Research/`](LLM-Research/)（36 份报告）＋ `.gitignore` |
| **规模** | **52** 份报告 · **55** 个 `.md` · **57** 个跟踪文件 · 工作树约 **1.66 MiB**（不含 `.git`） |
| **仓库类型** | 扁平化 **monorepo**：两个报告库以**普通目录**形式纳入版本管理 |

```bash
# 获取与浏览
git clone https://github.com/zhoucanzong/ResearchReport.git
cd ResearchReport
cat README.md                                   # 本索引
cat AIGC-Research/README.md                     # AIGC 库内索引
cat LLM-Research/README.md                      # LLM 库内索引

# 全域检索（例：找所有提到 DiT 的报告）
grep -r "DiT" --include='*.md' AIGC-Research LLM-Research
```

> **关于结构**：两个报告库在本仓库中是**普通子目录，已移除各自的嵌套 `.git`**，因此仓库内**不存在 gitlink（mode 160000）或 submodule**，`git add -A` 会把所有报告作为普通文件提交。
> 各自的独立仓库（`AIGC-Research`、`LLM-Research`）作为**上游存档**仅保留在 GitHub（完整提交历史在那里）；本地副本 `~/Documents/AIGC-Research`、`~/Documents/LLM-Research` 已按仓主要求于 **2026-10-16 移除**（见 §6.1）。本仓库是二者的**内容快照 + 统一索引**，此后统一在本仓库维护。

**统计口径**：下表的计数与体积是**两个报告库目录本身**的合计（含各自库内 `README.md`，**不含**根目录的 `README.md`、`.gitignore` 与 `.git`）。

| 汇总项（两库目录合计） | 数值 |
| :-- | --: |
| 报告库目录数量 | **2** 个（`AIGC-Research/`、`LLM-Research/`） |
| 报告总数（不含共 3 个 README） | **52** 份 |
| 报告正文（52 份）总量 | **1,683,826 bytes ≈ 1.61 MiB**（30,515 行） |
| `.md` 文件总数（52 份报告 + 3 个 README） | **55** 个 |
| 报告目录数（`*-research/`） | **41** 个（16 + 25） |
| 目录内文件数 / 字节（不含 `.git`） | **56** 个 / **1,703,034 bytes ≈ 1.62 MiB** |
| 磁盘占用（`du -sk`，不含 `.git`） | **1,776 KB ≈ 1.73 MiB** |
| 纳入版本控制的文件（全仓库，含根索引与 `.gitignore`） | **57** 个 |

---

## 1. 两库定位与差异

### 1.1 定位

| | [AIGC-Research](AIGC-Research/) | [LLM-Research](LLM-Research/) |
| :-- | :-- | :-- |
| **一句话定位** | 生成式 AI 多模态内容生成调研（图像 / 视频 / 3D / 音频 / 数字人） | 大语言模型调研（文本、多模态理解、训练与推理基础设施） |
| **核心关注点** | **模型结构演进**：U-Net → DiT → 3D DiT，扩散 / 流匹配与条件注入 | **模型能力与全栈技术**：能力边界、Benchmark、对齐、推理加速、训练与部署 |
| **覆盖对象** | 8 个生成式模型 / 产品系列（Stability AI、OpenAI 生成线、Google、Midjourney、可灵、Runway、字节、阿里万相） | 15 个 LLM 模型 / 系列（Claude、DeepSeek、Qwen、GPT、Gemini、Grok、GLM、Kimi、LLaMA 等） |
| **技术专题数** | 8 个（DiffusionModels、DiT、VideoGen、ControllableGen、3DGen、AudioGen、AvatarGen、ImageEditing） | 10 个（SpeculativeDecoding、LongContext、MoE、ReasoningModels、VLM、Agent、Alignment、TrainingInfra、QuantizationEdge、RAG） |
| **报告粒度** | 每系列 **1 份** 汇总报告（16 份） | 多数系列 1 份；DeepSeek / Qwen / SpeculativeDecoding **分册展开**（36 份） |
| **报告风格** | 架构时间线 → 模型结构详解 → 竞品对比 | 模型列表 → 关键能力 → 生态 → 竞品对比；专题偏论文方法梳理 |
| **上游独立仓库（存档，仅 GitHub）** | `git@github.com:zhoucanzong/AIGC-Research.git`（1 次 commit · `main`） | `git@github.com:zhoucanzong/LLM-Research.git`（7 次 commit · `main`） |
| **在本仓库中的形态** | 普通子目录 `AIGC-Research/`（**无嵌套 `.git`**，不产生 gitlink） | 普通子目录 `LLM-Research/`（同上） |

### 1.2 差异速览

| 维度 | AIGC-Research | LLM-Research |
| :-- | :-- | :-- |
| 主题域 | **生成**（图像 / 视频 / 3D / 音频 / 数字人） | **理解与推理**（语言 / 多模态理解）＋ 工程全栈 |
| 报告数量 | 16 份 | 36 份 |
| `.md` 文件数 | 17（16 报告 + 1 README） | 37（36 报告 + 1 README） |
| 报告正文字节 | 611,021 B ≈ 596.7 KB | 1,072,805 B ≈ 1,047.7 KB |
| 目录内容字节（不含 `.git`） | 618,206 B ≈ 603.7 KB | 1,084,828 B ≈ 1,059.4 KB |
| 磁盘占用（`du -sk`） | 640 KB | 1,136 KB |
| 上游提交数 | 1 | 7 |
| 上游仓库 `.git`（**不在本仓库内**；本地副本已移除） | 280,333 B ≈ 273.8 KB | 870,445 B ≈ 850.0 KB |
| 目录命名约定 | `ModelSeries/<Name>-research/report.md`、`TechnicalTopics/<Topic>-research/report.md` | 同左，另允许 `Topic-research/<topic-sub>.md` 分册 |
| 附加文件 | — | `.gitignore`（另有 `.claude/settings.local.json`，被全局 gitignore 忽略、未纳入版本控制） |

### 1.3 共同点

- 报告均由 **AI Agent 自动调研生成**，来源为公开网络搜索、第三方评测、社交媒体与行业媒体；两库 README 均带同名**免责声明**（数据可能错误、过时或未经证实，仅供参考）。
- 内容**以中文为主，关键术语保留英文**。
- 目录结构、命名约定、报告模板高度同构，因此可以合并成统一索引、统一检索。
- 报告都带来源索引 / 论文引用，可追溯。
- 两库 README 均已加入「仓库归属」说明，标注其现归属 monorepo **ResearchReport**，并给出正确的克隆 / 浏览命令。

---

## 2. [AIGC-Research](AIGC-Research/) 逐项索引

库内索引：[AIGC-Research/README.md](AIGC-Research/README.md) · 16 份报告 · 8 个模型系列 + 8 个技术专题

### 2.1 模型系列（8 个，各 1 份，共 8 份）

| # | 模型 / 系列 | 所属公司 | 报告数 | 亮点 | 目录 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 1 | **StabilityAI** | Stability AI / BFL | 1 | SD 1.x→2.x→XL→3→FLUX，U-Net→DiT 架构演进 | [目录](AIGC-Research/ModelSeries/StabilityAI-research/) · [报告](AIGC-Research/ModelSeries/StabilityAI-research/report.md) |
| 2 | **OpenAI-Gen** | OpenAI | 1 | DALL-E 2/3 → GPT-4o 图像生成 → Sora，自回归 + 扩散混合架构 | [目录](AIGC-Research/ModelSeries/OpenAI-Gen-research/) · [报告](AIGC-Research/ModelSeries/OpenAI-Gen-research/report.md) |
| 3 | **Google-Gen** | Google / DeepMind | 1 | Imagen 2/3 → Veo 2/3/3.1，级联扩散 → DiT 视频生成 | [目录](AIGC-Research/ModelSeries/Google-Gen-research/) · [报告](AIGC-Research/ModelSeries/Google-Gen-research/report.md) |
| 4 | **Midjourney** | Midjourney | 1 | V4→V5→V6→V7，闭源标杆的架构推测与美学进化 | [目录](AIGC-Research/ModelSeries/Midjourney-research/) · [报告](AIGC-Research/ModelSeries/Midjourney-research/report.md) |
| 5 | **Kling** | 快手 | 1 | 可灵 1.0→2.0→3.0/O1，国产视频生成的 DiT 架构路线 | [目录](AIGC-Research/ModelSeries/Kling-research/) · [报告](AIGC-Research/ModelSeries/Kling-research/report.md) |
| 6 | **Runway** | Runway | 1 | Gen-1→Gen-4.5，Latent Diffusion → DiT 视频编辑与生成 | [目录](AIGC-Research/ModelSeries/Runway-research/) · [报告](AIGC-Research/ModelSeries/Runway-research/report.md) |
| 7 | **ByteDance-Gen** | 字节跳动 | 1 | Seedance 1.0→2.0，即梦 AI，多模态 cinematic 生成 | [目录](AIGC-Research/ModelSeries/ByteDance-Gen-research/) · [报告](AIGC-Research/ModelSeries/ByteDance-Gen-research/report.md) |
| 8 | **Alibaba-Gen** | 阿里巴巴 | 1 | 通义万相 Wan 2.1/2.2/2.6，开源视频生成的 DiT 架构 | [目录](AIGC-Research/ModelSeries/Alibaba-Gen-research/) · [报告](AIGC-Research/ModelSeries/Alibaba-Gen-research/report.md) |

> 国内 4 家 · 海外 4 家 · 共 8 个系列 ｜ 全部索引目录：[AIGC-Research/ModelSeries/](AIGC-Research/ModelSeries/)

### 2.2 技术专题（8 个，各 1 份，共 8 份）

| # | 专题 | 覆盖范围 | 报告数 | 亮点 | 目录 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 1 | **DiffusionModels** | 扩散模型基础 | 1 | DDPM→DDIM→LDM→Consistency Models，数学框架与采样加速 | [目录](AIGC-Research/TechnicalTopics/DiffusionModels-research/) · [报告](AIGC-Research/TechnicalTopics/DiffusionModels-research/report.md) |
| 2 | **DiT** | Diffusion Transformer | 1 | U-Net→DiT 架构革命，PixArt→SD3→FLUX→Sora 的 Transformer 化 | [目录](AIGC-Research/TechnicalTopics/DiT-research/) · [报告](AIGC-Research/TechnicalTopics/DiT-research/report.md) |
| 3 | **VideoGen** | 视频生成技术 | 1 | 时序建模、3D DiT、因果注意力、运动一致性 | [目录](AIGC-Research/TechnicalTopics/VideoGen-research/) · [报告](AIGC-Research/TechnicalTopics/VideoGen-research/report.md) |
| 4 | **ControllableGen** | 可控生成 | 1 | ControlNet→IP-Adapter→T2I-Adapter→LoRA，条件注入架构演进 | [目录](AIGC-Research/TechnicalTopics/ControllableGen-research/) · [报告](AIGC-Research/TechnicalTopics/ControllableGen-research/report.md) |
| 5 | **3DGen** | 3D 生成 | 1 | DreamFusion→Point-E→Shap-E→Tripo3D，NeRF→3D Gaussian Splatting | [目录](AIGC-Research/TechnicalTopics/3DGen-research/) · [报告](AIGC-Research/TechnicalTopics/3DGen-research/report.md) |
| 6 | **AudioGen** | 音频 / 音乐生成 | 1 | AudioLDM→MusicLM→Suno/Udio，扩散 + 自回归 + 流匹配 | [目录](AIGC-Research/TechnicalTopics/AudioGen-research/) · [报告](AIGC-Research/TechnicalTopics/AudioGen-research/report.md) |
| 7 | **AvatarGen** | 数字人 / Avatar 生成 | 1 | Wav2Lip→SadTalker→OmniHuman-1，CNN→3DMM→DiT 统一生成 | [目录](AIGC-Research/TechnicalTopics/AvatarGen-research/) · [报告](AIGC-Research/TechnicalTopics/AvatarGen-research/report.md) |
| 8 | **ImageEditing** | 图像编辑与修复 | 1 | GAN→InstructPix2Pix→DiT Joint Attention→Agentic 编辑 | [目录](AIGC-Research/TechnicalTopics/ImageEditing-research/) · [报告](AIGC-Research/TechnicalTopics/ImageEditing-research/report.md) |

> 共 8 个专题 ｜ 全部索引目录：[AIGC-Research/TechnicalTopics/](AIGC-Research/TechnicalTopics/)

---

## 3. [LLM-Research](LLM-Research/) 逐项索引

库内索引：[LLM-Research/README.md](LLM-Research/README.md) · 36 份报告 · 15 个模型系列 + 10 个技术专题

### 3.1 模型系列（15 个系列，20 份报告）

| # | 模型 / 系列 | 所属公司 | 报告数 | 亮点 | 目录 / 报告 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 1 | **Claude** | Anthropic | 1 | Reasoning、Coding、工具使用能力 | [目录](LLM-Research/ModelSeries/Claude-research/) · [报告](LLM-Research/ModelSeries/Claude-research/report.md) |
| 2 | **DeepSeek** | 深度求索 | **3** | 文本模型 + 多模态 + 专项能力，分拆详述 | [目录](LLM-Research/ModelSeries/DeepSeek-research/) · [主报告](LLM-Research/ModelSeries/DeepSeek-research/report.md) · [文本模型](LLM-Research/ModelSeries/DeepSeek-research/deepseek-text-models.md) · [多模态与专项](LLM-Research/ModelSeries/DeepSeek-research/deepseek-multimodal-and-specialized.md) |
| 3 | **Doubao-Seed** | 字节跳动 | 1 | 豆包大模型 + Seed 系列技术报告 | [目录](LLM-Research/ModelSeries/Doubao-Seed-research/) · [报告](LLM-Research/ModelSeries/Doubao-Seed-research/report.md) |
| 4 | **GLM** | 智谱 AI | 1 | ChatGLM 系列演进与技术路线 | [目录](LLM-Research/ModelSeries/GLM-research/) · [报告](LLM-Research/ModelSeries/GLM-research/report.md) |
| 5 | **GPT** | OpenAI | 1 | GPT-4 系列能力边界与生态 | [目录](LLM-Research/ModelSeries/GPT-research/) · [报告](LLM-Research/ModelSeries/GPT-research/report.md) |
| 6 | **Gemini** | Google | 1 | 多模态理解、长上下文、生态整合 | [目录](LLM-Research/ModelSeries/Gemini-research/) · [报告](LLM-Research/ModelSeries/Gemini-research/report.md) |
| 7 | **Grok** | xAI | 1 | 实时 X 数据、超大上下文、Musk 生态绑定 | [目录](LLM-Research/ModelSeries/Grok-research/) · [报告](LLM-Research/ModelSeries/Grok-research/report.md) |
| 8 | **Hunyuan** | 腾讯 | 1 | 混元大模型多模态能力 | [目录](LLM-Research/ModelSeries/Hunyuan-research/) · [报告](LLM-Research/ModelSeries/Hunyuan-research/report.md) |
| 9 | **Kimi** | 月之暗面 | 1 | 长上下文、联网搜索特色能力 | [目录](LLM-Research/ModelSeries/Kimi-research/) · [报告](LLM-Research/ModelSeries/Kimi-research/report.md) |
| 10 | **LLaMA** | Meta | 1 | 开源模型生态与技术架构 | [目录](LLM-Research/ModelSeries/LLaMA-research/) · [报告](LLM-Research/ModelSeries/LLaMA-research/report.md) |
| 11 | **MiMo** | 小米 | 1 | 端侧部署与小模型优化方向 | [目录](LLM-Research/ModelSeries/MiMo-research/) · [报告](LLM-Research/ModelSeries/MiMo-research/report.md) |
| 12 | **MiniMax** | MiniMax | 1 | 多模态与语音能力 | [目录](LLM-Research/ModelSeries/MiniMax-research/) · [报告](LLM-Research/ModelSeries/MiniMax-research/report.md) |
| 13 | **Mistral** | Mistral AI | 1 | 欧洲开源领袖、GDPR 主权、多语言 Tier-1 | [目录](LLM-Research/ModelSeries/Mistral-research/) · [报告](LLM-Research/ModelSeries/Mistral-research/report.md) |
| 14 | **Nemotron** | NVIDIA | 1 | 混合 Mamba 架构、合成数据、Agentic 高效推理 | [目录](LLM-Research/ModelSeries/Nemotron-research/) · [报告](LLM-Research/ModelSeries/Nemotron-research/report.md) |
| 15 | **Qwen** | 阿里巴巴 | **4** | 文本 + VL + Omni + 生态，覆盖面最广 | [目录](LLM-Research/ModelSeries/Qwen-research/) · [主报告](LLM-Research/ModelSeries/Qwen-research/report.md) · [文本模型](LLM-Research/ModelSeries/Qwen-research/qwen-text-models.md) · [VL 模型](LLM-Research/ModelSeries/Qwen-research/qwen-vl-models.md) · [Omni 与生态](LLM-Research/ModelSeries/Qwen-research/qwen-omni-and-ecosystem.md) |

> 国内 8 家 · 海外 5 家（含 NVIDIA）· 欧洲 1 家 · 共 15 个系列 / 20 份报告 ｜ 全部索引目录：[LLM-Research/ModelSeries/](LLM-Research/ModelSeries/)

### 3.2 技术专题（10 个，16 份报告）

| # | 专题 | 覆盖范围 | 报告数 | 亮点 | 目录 / 报告 |
| :--: | :-- | :-- | :--: | :-- | :-- |
| 1 | **SpeculativeDecoding** | 投机解码 | **7** | EAGLE / DFlash / 多模态投机，经典方法到系统框架 | [目录](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/) · [主报告](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/report.md) · [经典与自投机](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-classical-and-self.md) · [EAGLE 系列](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-eagle-series.md) · [块扩散与检索式](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-block-diffusion.md) · [训练目标优化](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-training-optimization.md) · [多模态投机](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-multimodal.md) · [系统与框架](LLM-Research/TechnicalTopics/SpeculativeDecoding-research/speculative-systems-and-frameworks.md) |
| 2 | **LongContext** | 长上下文技术 | 1 | FlashAttention、Ring Attention、线性注意力、百万 Token 窗口 | [目录](LLM-Research/TechnicalTopics/LongContext-research/) · [报告](LLM-Research/TechnicalTopics/LongContext-research/report.md) |
| 3 | **MoE** | 混合专家架构 | 1 | Switch→DeepSeekMoE→Routing-Free，负载均衡与推理优化 | [目录](LLM-Research/TechnicalTopics/MoE-research/) · [报告](LLM-Research/TechnicalTopics/MoE-research/report.md) |
| 4 | **ReasoningModels** | 推理模型 | 1 | o1/R1/k1.5，Test-Time Scaling，GRPO/DAPO 训练方法 | [目录](LLM-Research/TechnicalTopics/ReasoningModels-research/) · [报告](LLM-Research/TechnicalTopics/ReasoningModels-research/report.md) |
| 5 | **VLM** | 多模态大模型 | 1 | GPT-4o / Qwen3-VL，视觉编码器、模态对齐、长视频理解 | [目录](LLM-Research/TechnicalTopics/VLM-research/) · [报告](LLM-Research/TechnicalTopics/VLM-research/report.md) |
| 6 | **Agent** | Agent 架构 | 1 | ReAct/MCP/A2A，多 Agent 系统，工具使用与记忆 | [目录](LLM-Research/TechnicalTopics/Agent-research/) · [报告](LLM-Research/TechnicalTopics/Agent-research/report.md) |
| 7 | **Alignment** | 模型对齐 | 1 | RLHF/DPO/GRPO/DAPO，安全对齐与奖励黑客缓解 | [目录](LLM-Research/TechnicalTopics/Alignment-research/) · [报告](LLM-Research/TechnicalTopics/Alignment-research/report.md) |
| 8 | **TrainingInfra** | 训练基础设施 | 1 | DeepSpeed/FSDP/Megatron，3D 并行，万卡集群 | [目录](LLM-Research/TechnicalTopics/TrainingInfra-research/) · [报告](LLM-Research/TechnicalTopics/TrainingInfra-research/report.md) |
| 9 | **QuantizationEdge** | 量化与边缘部署 | 1 | AWQ/GPTQ/GGUF/FP8，vLLM/Ollama，Jetson 边缘 | [目录](LLM-Research/TechnicalTopics/QuantizationEdge-research/) · [报告](LLM-Research/TechnicalTopics/QuantizationEdge-research/report.md) |
| 10 | **RAG** | 检索增强生成 | 1 | RAG 0.0→4.0，GraphRAG，Agentic RAG，混合检索 | [目录](LLM-Research/TechnicalTopics/RAG-research/) · [报告](LLM-Research/TechnicalTopics/RAG-research/report.md) |

> 共 10 个专题 / 16 份报告 ｜ 全部索引目录：[LLM-Research/TechnicalTopics/](LLM-Research/TechnicalTopics/)

---

## 4. 目录结构

本仓库为**扁平化 monorepo**：`AIGC-Research/` 与 `LLM-Research/` 是仓库内的**普通目录**（**不再是**独立 Git 仓库，内部**没有** `.git`），统一由根目录的 `.git` 管理。

```
ResearchReport/                              ← 本仓库根目录（Git 仓库，.git 仅在根目录）
├── .git/                                    ← 唯一的 Git 目录（管理全部内容）
├── .gitignore                               ← 忽略 macOS 元数据等
├── README.md                                ← 本文件：统一顶层索引
│
├── AIGC-Research/                           ← 普通目录（上游 AIGC-Research 仓库的内容快照）
│   ├── README.md
│   ├── ModelSeries/                         #  8 个生成式模型系列
│   │   ├── StabilityAI-research/report.md
│   │   ├── OpenAI-Gen-research/report.md
│   │   ├── Google-Gen-research/report.md
│   │   ├── Midjourney-research/report.md
│   │   ├── Kling-research/report.md
│   │   ├── Runway-research/report.md
│   │   ├── ByteDance-Gen-research/report.md
│   │   └── Alibaba-Gen-research/report.md
│   └── TechnicalTopics/                     #  8 个生成技术专题
│       ├── DiffusionModels-research/report.md
│       ├── DiT-research/report.md
│       ├── VideoGen-research/report.md
│       ├── ControllableGen-research/report.md
│       ├── 3DGen-research/report.md
│       ├── AudioGen-research/report.md
│       ├── AvatarGen-research/report.md
│       └── ImageEditing-research/report.md
│
└── LLM-Research/                            ← 普通目录（上游 LLM-Research 仓库的内容快照）
    ├── .gitignore
    ├── README.md
    ├── ModelSeries/                         # 15 个模型系列 / 20 份报告
    │   ├── Claude-research/report.md
    │   ├── DeepSeek-research/               #   3 份（主报告 + 2 分册）
    │   ├── Doubao-Seed-research/report.md
    │   ├── GLM-research/report.md
    │   ├── GPT-research/report.md
    │   ├── Gemini-research/report.md
    │   ├── Grok-research/report.md
    │   ├── Hunyuan-research/report.md
    │   ├── Kimi-research/report.md
    │   ├── LLaMA-research/report.md
    │   ├── MiMo-research/report.md
    │   ├── MiniMax-research/report.md
    │   ├── Mistral-research/report.md
    │   ├── Nemotron-research/report.md
    │   └── Qwen-research/                   #   4 份（主报告 + 3 分册）
    └── TechnicalTopics/                     # 10 个技术专题 / 16 份报告
        ├── SpeculativeDecoding-research/    #   7 份（主报告 + 6 分册）
        ├── LongContext-research/report.md
        ├── MoE-research/report.md
        ├── ReasoningModels-research/report.md
        ├── VLM-research/report.md
        ├── Agent-research/report.md
        ├── Alignment-research/report.md
        ├── TrainingInfra-research/report.md
        ├── QuantizationEdge-research/report.md
        └── RAG-research/report.md
```

**命名约定**：`ModelSeries/<Name>-research/` 与 `TechnicalTopics/<Topic>-research/`，主报告固定名为 `report.md`；未单独展开的系列 / 专题**只有** 1 份 `report.md`，需要深挖时才在目录内新增 `<topic>-<sub>.md` 分册（如 `speculative-eagle-series.md`）。

> `.claude/settings.local.json`（本地工具配置）不在此树中：它被全局 gitignore 规则忽略，**未纳入版本控制**。

---

## 5. 报告数量与体积统计

> 统计范围 = **两个报告库目录本身**（`AIGC-Research/`、`LLM-Research/`），已**不含**任何 `.git`（两个嵌套 `.git` 已删除）。其中「报告正文」指 52 份报告文件，不含 3 个 `README.md`。

### 5.1 按库汇总

| 指标 | AIGC-Research | LLM-Research | 合计 |
| :-- | --: | --: | --: |
| 模型系列目录数 | 8 | 15 | 23 |
| 技术专题目录数 | 8 | 10 | 18 |
| 报告数（不含 README） | 16 | 36 | **52** |
| ├ `report.md` 主报告 | 16 | 25 | 41 |
| └ 分册 `.md` | 0 | 11 | 11 |
| 报告正文字节 | 611,021 | 1,072,805 | **1,683,826** |
| 报告正文行数 | 12,733 | 17,782 | **30,515** |
| `.md` 文件数（含库内 README） | 17 | 37 | **54** |
| 目录内文件数（全部类型） | 17 | 39 | 56 |
| 目录内容字节（不含 `.git`） | 618,206 | 1,084,828 | **1,703,034** |
| 磁盘占用 `du -sk` | 640 KB | 1,136 KB | **1,776 KB** |
| 纳入版本控制的文件 | 17 | 38 | 55 |

> 全仓库口径（含根目录 `README.md`、`.gitignore`）：**57** 个跟踪文件 · 工作树 **约 1.66 MiB**（≈ 1.74 MB）· `du -sk`（不含 `.git`）**约 1,816 KB**（`.git` 另计：首次提交后约 1.1 MB）。
> 上述体积随本索引更新而小幅浮动，故取约值。
> LLM-Research 目录内 39 个文件中，`.claude/settings.local.json` 被全局 gitignore 忽略，故跟踪 38 个。

### 5.2 逐目录分布（报告正文字节与行数）

**AIGC-Research**

| 目录 | 分类 | 报告数 | 行数 | 字节 |
| :-- | :-- | --: | --: | --: |
| StabilityAI-research | 模型 | 1 | 873 | 48,275 |
| OpenAI-Gen-research | 模型 | 1 | 859 | 36,915 |
| Google-Gen-research | 模型 | 1 | 826 | 33,598 |
| Alibaba-Gen-research | 模型 | 1 | 803 | 36,092 |
| Runway-research | 模型 | 1 | 732 | 33,709 |
| ByteDance-Gen-research | 模型 | 1 | 711 | 41,175 |
| Midjourney-research | 模型 | 1 | 587 | 35,037 |
| Kling-research | 模型 | 1 | 537 | 28,134 |
| ControllableGen-research | 专题 | 1 | 923 | 43,040 |
| AudioGen-research | 专题 | 1 | 913 | 41,460 |
| 3DGen-research | 专题 | 1 | 898 | 46,655 |
| VideoGen-research | 专题 | 1 | 898 | 34,716 |
| DiT-research | 专题 | 1 | 892 | 45,829 |
| DiffusionModels-research | 专题 | 1 | 855 | 36,106 |
| ImageEditing-research | 专题 | 1 | 834 | 42,897 |
| AvatarGen-research | 专题 | 1 | 592 | 27,383 |

**LLM-Research**（多分册目录单独标注）

| 目录 | 分类 | 报告数 | 行数 | 字节 |
| :-- | :-- | --: | --: | --: |
| Qwen-research | 模型（4 分册） | 4 | 2,513 | 124,106 |
| DeepSeek-research | 模型（3 分册） | 3 | 1,525 | 116,669 |
| Gemini-research | 模型 | 1 | 788 | 34,614 |
| GPT-research | 模型 | 1 | 759 | 57,261 |
| Doubao-Seed-research | 模型 | 1 | 643 | 27,470 |
| Claude-research | 模型 | 1 | 611 | 47,565 |
| Hunyuan-research | 模型 | 1 | 525 | 36,518 |
| GLM-research | 模型 | 1 | 523 | 39,747 |
| MiniMax-research | 模型 | 1 | 517 | 41,290 |
| MiMo-research | 模型 | 1 | 510 | 34,754 |
| Mistral-research | 模型 | 1 | 495 | 29,259 |
| LLaMA-research | 模型 | 1 | 483 | 42,535 |
| Grok-research | 模型 | 1 | 469 | 32,612 |
| Nemotron-research | 模型 | 1 | 465 | 32,700 |
| Kimi-research | 模型 | 1 | 431 | 33,338 |
| RAG-research | 专题 | 1 | 851 | 44,423 |
| QuantizationEdge-research | 专题 | 1 | 777 | 34,205 |
| TrainingInfra-research | 专题 | 1 | 720 | 31,849 |
| Agent-research | 专题 | 1 | 698 | 31,433 |
| ReasoningModels-research | 专题 | 1 | 681 | 34,752 |
| SpeculativeDecoding-research | 专题（7 分册） | 7 | 680 | 42,898 |
| LongContext-research | 专题 | 1 | 608 | 30,373 |
| Alignment-research | 专题 | 1 | 588 | 35,712 |
| VLM-research | 专题 | 1 | 517 | 28,916 |
| MoE-research | 专题 | 1 | 405 | 27,806 |

---

## 6. 校验结果

### 6.1 上游原始仓库最终状态（本地副本已于 2026-10-16 移除）

复制与校验阶段（见 §6.2）两库**只读、全程未改动**，其最终状态如下。仓主随后指示「以后统一维护新仓库」，两个本地原始目录已于 **2026-10-16** 由本 Bot 移入废纸篓（`~/.Trash/AIGC-Research`、`~/.Trash/LLM-Research`），可从废纸篓恢复，直至清空废纸篓。

| 校验项 | AIGC-Research | LLM-Research |
| :-- | :-- | :-- |
| 原路径 | `/Users/zhoucanzong/Documents/AIGC-Research`（已移除） | `/Users/zhoucanzong/Documents/LLM-Research`（已移除） |
| `rev-parse HEAD` | `101ae640ea043572f2c6dc64742eb520394c1d3e` | `7deacb5b841c0b0925e1ac024323255b1b7eaf58` |
| `log -1` | `初步调研AIGC` · zhoucanzong \<zhoucanzong@gmail.com\> · 2026-06-07 23:19:52 +0800 | `修正readme` · zhoucanzong \<zhoucanzong@gmail.com\> · 2026-06-07 01:18:47 +0800 |
| `status --short` | `?? .DS_Store`（未跟踪，来源既有状态） | （空 → 干净） |
| `remote -v` | `origin  git@github.com:zhoucanzong/AIGC-Research.git`（fetch/push） | `origin  git@github.com:zhoucanzong/LLM-Research.git`（fetch/push） |
| 提交数 / 分支 | 1 · `main` | 7 · `main` |
| 本地目录处置 | 🗑️ 2026-10-16 移入废纸篓 | 🗑️ 2026-10-16 移入废纸篓 |
| 历史留存位置 | GitHub 存档仓库，删除前核对 `refs/heads/main` = `101ae64…` ✅ | GitHub 存档仓库，删除前核对 `refs/heads/main` = `7deacb5…` ✅ |

### 6.2 复制阶段校验（扁平化前，历史留证）

`cp -a <src> Research/<name>`（保留权限、时间戳与 `.git`）。当时两副本各含完整 `.git`，校验结论如下（该 `.git` 现已按计划删除，见 6.3）：

| 校验项 | AIGC-Research | LLM-Research |
| :-- | :-- | :-- |
| 工作区 `.md` 数量（源 → 副本） | 17 → **17** | 37 → **37** |
| `report.md` 数量（源 → 副本） | 16 → **16** | 25 → **25** |
| 全部普通文件数（源 → 副本） | 80 → **80** | 206 → **206** |
| 工作区文件 SHA-256 逐文件比对 | ✅ 全部一致（18 个非 `.git` 文件） | ✅ 全部一致（42 个非 `.git` 文件） |
| `.git` 内文件 SHA-256 比对 | ⚠️ 仅 `.git/index` 不同（stat cache） | ⚠️ 仅 `.git/index` 不同（stat cache） |
| HEAD tree（源 = 副本） | ✅ `ca974128baf589ecbaf2ed4d9af2bee1b18f2852` | ✅ `fd6ccaf955341f9b7e28de5443862cb578f4eff9` |
| `git fsck --full --strict` | ✅ exit 0，无输出 | ✅ exit 0，无输出 |

### 6.3 扁平化与新仓库校验（当前状态）

**① 嵌套 `.git` 已删除（依据：内容完全由上游保留，删除不丢失任何历史）**

删除前逐项留证，证明两个嵌套 `.git` 与上游仓库**逐字节等价**（仅 `index` 这个 stat cache 文件不同），且**副本中的每一个对象都能在上游仓库中按同一 SHA 找到**：

| 证据 | AIGC-Research | LLM-Research |
| :-- | :-- | :-- |
| `rev-parse HEAD`（副本 = 上游） | `101ae64…` = `101ae64…` ✅ | `7deacb5…` = `7deacb5…` ✅ |
| `show-ref` 校验和（副本 = 上游） | `0ed5835…` ✅ | `4b14806…` ✅ |
| `count-objects`（副本 = 上游） | 37 objects ✅ | 136 objects ✅ |
| 副本对象是否存在于上游 | ✅ 37/37 命中，无缺失 | ✅ 113/113 可达对象命中，无缺失 |
| 全量 `.git` 文件 SHA-256 比对 | 62 个文件，仅 `index` 不同 | 164 个文件，仅 `index` 不同 |
| `git fsck --full --strict`（删除前） | exit 0，无输出 | exit 0，无输出 |
| 已删除路径（绝对路径已实时校验） | `/Users/zhoucanzong/Documents/Research/AIGC-Research/.git` | `/Users/zhoucanzong/Documents/Research/LLM-Research/.git` |

> 结论：这两个 `.git` 只是上游仓库的同构副本，**没有任何仅存于副本的提交、分支、tag 或对象**；其历史仍完整保存在上游独立仓库（`AIGC-Research` 1 次 commit、`LLM-Research` 7 次 commit，均可 `git log` 追溯）。因此删除它们是安全的，也是让本仓库能扁平推送的**必要步骤**——保留嵌套 `.git` 会使 `git add` 只记录一个 gitlink（mode 160000），推送后目录内容为空。

**② 仓库结构校验**

| 检查项 | 结果 |
| :-- | :-- |
| 根目录是否为 Git 仓库 | ✅ 是（`.git` 仅存在于 `/Users/zhoucanzong/Documents/Research/.git`） |
| 是否存在嵌套 `.git` | ✅ 不存在（子目录均为普通目录） |
| 缺失模式检查 `git ls-files -s \| awk '{print $1}' \| sort \| uniq -c` | ✅ **仅 `57 100644`**，gitlink（`160000`）计数 **0** |
| 是否存在 submodule | ✅ 无 `.gitmodules` |
| `git ls-files \| wc -l` | ✅ **57** |
| `git ls-files '*.md' \| wc -l` | ✅ **55**（52 份报告 + 3 个 README） |
| 52 份报告是否全部被跟踪 | ✅ AIGC 16/16 + LLM 36/36 = **52/52** |
| `git status --short`（提交后） | ✅ **空**（干净；`.claude/settings.local.json` 被全局 gitignore 忽略，不产生噪声） |
| 提交者身份 | `zhoucanzong <zhoucanzong@gmail.com>`（来自全局 `~/.gitconfig`，未设置任何 BotHarness 身份） |
| GPG 签名 | 未启用（`commit.gpgsign` 未设置） |
| 首次提交 SHA / 分支 / remote | 见 `git log -1`、`git branch --show-current`、`git remote -v`（本索引随该提交一同发布，故不内嵌自身 SHA） |

---

## 7. 后续如何更新

### 7.1 拉取与推送（顶层即可，不存在 submodule 语境）

```bash
cd ResearchReport

# 拉取远端最新内容
git pull --ff-only

# 提交并推送本地改动
git add -A
git commit -m "更新报告与索引"
git push origin main

# 查看状态与远端
git status --short
git remote -v
```

> 本仓库是普通 monorepo：**所有内容都在同一个仓库内**，因此不需要（也不存在）`git submodule update`、`git submodule foreach` 之类操作。

### 7.2 新增 / 修改报告

```bash
cd ResearchReport/LLM-Research                     # 或 AIGC-Research

mkdir -p TechnicalTopics/NewTopic-research
$EDITOR TechnicalTopics/NewTopic-research/report.md

cd ..                                              # 回到仓库根目录
git add -A
git commit -m "新增 NewTopic 技术专题调研"
git push origin main
```

约定：
1. 目录名用 `<Name>-research`（模型系列放 `ModelSeries/`，技术专题放 `TechnicalTopics/`）。
2. 主报告固定命名 `report.md`；深挖分册用 `<topic>-<sub>.md`（全小写连字符）。
3. 报告内容**中文为主、关键术语保留英文**，并附来源索引以便追溯。
4. 沿用统一模板，便于跨库检索与对比。

### 7.3 与上游独立仓库同步（可选，历史只存在 GitHub）

两个子目录是**内容快照**，不带 Git 历史；本地已无上游仓库副本（2026-10-16 移除，见 §6.1）。如需从上游导入提交，先把存档仓库克隆到本仓库之外，再复制变化：

```bash
# 例：从 GitHub 取上游 AIGC-Research 存档
git clone https://github.com/zhoucanzong/AIGC-Research.git /tmp/AIGC-Research
rsync -a --delete --exclude '.git' --exclude '.DS_Store' \
  /tmp/AIGC-Research/ ResearchReport/AIGC-Research/

cd ResearchReport && git add -A && git commit -m "同步上游 AIGC-Research"
```

> 上游存档仓库（`AIGC-Research`、`LLM-Research`）是否继续保留由仓主决定；此后 **ResearchReport 是唯一在维护的仓库**。

> ⚠️ `rsync --delete` 会删除目标端多余文件，执行前请先 `--dry-run` 预览。

### 7.4 同步更新本索引

新增 / 删除 / 重命名报告或专题后，请回来更新本文件：

1. 更新「本仓库说明」与「汇总项」表的计数与体积；
2. 在 §2 / §3 对应表格中增删行，并**链接到子目录**（多分册目录同时列出各分册文件的链接）；
3. 更新 §5 的统计表与逐目录分布表；
4. 需要时按 §6 的方式重跑校验（`git ls-files -s | awk '{print $1}' | sort | uniq -c`、`git ls-files | wc -l`、`git status --short`、`du -sk`）并更新 §6。

### 7.5 一句话速查

```bash
# 全部 .md 总数 → 55（= 52 份报告 + 3 个 README）
git ls-files '*.md' | wc -l
# 仅报告数 → 52
git ls-files '*.md' | grep -vc 'README\.md$'
# 各库体积
du -sh AIGC-Research LLM-Research
# 全域搜索（例：找所有提到 DiT 的报告）
grep -r "DiT" --include='*.md' AIGC-Research LLM-Research
```

---

## 8. 已知问题与备注

1. **上游 README 的自报计数与实际不一致**（本次只修引用、未改动其统计数字，在此备注）：
   - `LLM-Research/README.md` 正文写「覆盖 16 个主流模型 / 系列」、徽章写 `Reports-32`，但实际为 **15 个模型系列目录** 与 **36 份报告**（表格行数也只有 15 行）。本索引以**实际文件系统内容**为准。
   - `AIGC-Research/README.md` 的「仓库结构」代码块注释写「技术专题报告（6 个）」，但实际列出并存在 **8 个**专题目录。
2. **`.DS_Store` 已清理**：本仓库内所有 `.DS_Store` 已删除，并由根目录 `.gitignore` 覆盖（macOS 之后重新生成也不会进入提交）。已移入废纸篓的本地上游副本 AIGC-Research 中仍带着未跟踪的 `.DS_Store`（属其既有状态，未去改动）。
3. **License 徽章死链已修复**：`LLM-Research/README.md` 原 `./LICENSE` 链接不存在，现已改为**无链接文本徽章**。注意：本仓库与两个上游仓库**均无 `LICENSE` 文件**，若要以 MIT 等许可公开发布，建议补上许可证文件。
4. **本仓库不含两个子库的 Git 提交历史**：为支持扁平推送，嵌套 `.git` 已移除（见 §6.3）。需要逐次提交历史 / blame 时，请使用上游独立仓库 `AIGC-Research`、`LLM-Research`。
5. 两库内容均为 **AI Agent 生成、未经官方确认**，引用具体参数 / 日期 / benchmark 前请回溯原始来源；两库 README 顶部均有对应免责声明。
6. `LLM-Research/.claude/settings.local.json` 被**全局** gitignore 规则（`~/.config/git/ignore`：`**/.claude/settings.local.json`）忽略，因此不在版本控制内；如需强制纳入，使用 `git add -f`。
7. **两个本地原始仓库已于 2026-10-16 移除**：按仓主要求「以后统一维护新的」，`~/Documents/AIGC-Research` 与 `~/Documents/LLM-Research` 已移入废纸篓（`~/.Trash/`，可恢复直至清空）。移除前已确认：其内容 100% 收录于本仓库（§6.2 逐文件 SHA-256 一致），且两个 GitHub 存档仓库的 `refs/heads/main` 与本地 HEAD 完全一致（`101ae64…` / `7deacb5…`），因此**未丢失任何报告内容或提交历史**。此后统一维护本仓库 ResearchReport。

---

*索引更新时间：2026-10-16 · 仓库：ResearchReport（已接手统一维护，两个本地上游副本同日移除）· 数据来源：本仓库实际文件系统内容*
