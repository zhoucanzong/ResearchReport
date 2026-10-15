# 📚 ResearchReport · AIGC & LLM 研究报告统一索引

**AI Agent 驱动的中文研究报告聚合仓库（monorepo）** —— 一个仓库，收纳三份研究资料库：生成式 AI（AIGC / 图像 · 视频 · 3D · 音频）方向、**大语言模型（LLM）**方向，以及**论文 / 开源仓库深度阅读笔记**（Repo-Research）。

## 本仓库说明

| 项目 | 内容 |
| :-- | :-- |
| **仓库名** | **ResearchReport** |
| **远端（origin）** | <https://github.com/zhoucanzong/ResearchReport.git> |
| **克隆** | `git clone https://github.com/zhoucanzong/ResearchReport.git` |
| **仓库布局** | 根目录 `README.md`（本索引）＋ [`AIGC-Research/`](AIGC-Research/)（16 份报告）＋ [`LLM-Research/`](LLM-Research/)（36 份报告）＋ [`Repo-Research/`](Repo-Research/)（2 个深度阅读项目）＋ `.gitignore` |
| **规模** | **52** 份报告 + **8** 份深读笔记 · **63** 个 `.md` · **66** 个跟踪文件 · 工作树约 **1.85 MiB**（不含 `.git`） |
| **仓库类型** | 扁平化 **monorepo**：三个资料库以**普通目录**形式纳入版本管理 |

```bash
# 获取与浏览
git clone https://github.com/zhoucanzong/ResearchReport.git
cd ResearchReport
cat README.md                                   # 本索引
cat AIGC-Research/README.md                     # AIGC 库内索引
cat LLM-Research/README.md                      # LLM 库内索引
# Repo-Research 没有自己的 README —— 见本索引 §4 的逐项索引

# 全域检索（例：找所有提到 DiT 的报告）
grep -r "DiT" --include='*.md' AIGC-Research LLM-Research Repo-Research
```

> **关于结构**：三个资料库在本仓库中都是**普通子目录**。`AIGC-Research/`、`LLM-Research/` 已移除各自的嵌套 `.git`，因此仓库内**不存在 gitlink（mode 160000）或 submodule**，`git add -A` 会把所有内容作为普通文件提交。
> `AIGC-Research`、`LLM-Research` 的独立仓库作为**上游存档**仅保留在 GitHub（完整提交历史在那里）；本地原始目录 `~/Documents/AIGC-Research`、`~/Documents/LLM-Research` 已按仓主要求于 **2026-10-16 移除**（见 §7.1）。
> `Repo-Research` **从来不是 Git 仓库**（无 `.git`、无提交历史、无上游存档），其内容仅存于本仓库；本地原始目录同样于 **2026-10-16 移入废纸篓**（见 §7.4）。

**统计口径**：下表的计数与体积是**三个资料库目录本身**的合计（含 `AIGC-Research/README.md`、`LLM-Research/README.md`；`Repo-Research/` 内无 README），**不含**根目录的 `README.md`、`.gitignore` 与 `.git`。

| 汇总项（三库目录合计） | 数值 |
| :-- | --: |
| 资料库目录数量 | **3** 个（`AIGC-Research/`、`LLM-Research/`、`Repo-Research/`） |
| AIGC / LLM 报告总数（不含 README） | **52** 份 |
| 报告正文（52 份）总量 | **1,683,826 bytes ≈ 1.61 MiB**（30,515 行） |
| Repo-Research 深读文档 | **8** 个 `.md`（1 份深度报告 + 1 个论文精读项目）+ 1 个结构化 `.json` |
| Repo-Research 文档总量 | **172,767 bytes ≈ 168.7 KB**（3,773 行） |
| `.md` 文件总数（三库目录内） | **62** 个（52 份报告 + 8 份深读笔记 + 2 个库内 README） |
| 研究目录数（报告 / 专题 / 项目） | **43** 个（AIGC 16 + LLM 25 + Repo 2 个项目目录） |
| 目录内文件数 / 字节（不含 `.git`） | **65** 个 / **1,892,195 bytes ≈ 1.80 MiB** |
| 磁盘占用（`du -sk`，不含 `.git`） | **1,980 KB ≈ 1.93 MiB** |
| 纳入版本控制的文件（全仓库，含根索引与 `.gitignore`） | **66** 个 |

---

## 1. 三库定位与差异

### 1.1 定位

| | [AIGC-Research](AIGC-Research/) | [LLM-Research](LLM-Research/) | [Repo-Research](Repo-Research/) |
| :-- | :-- | :-- | :-- |
| **一句话定位** | 生成式 AI 多模态内容生成调研（图像 / 视频 / 3D / 音频 / 数字人） | 大语言模型调研（文本、多模态理解、训练与推理基础设施） | **论文与开源仓库的深度阅读笔记**（源码剖析 + 单论文精读） |
| **核心关注点** | **模型结构演进**：U-Net → DiT → 3D DiT，扩散 / 流匹配与条件注入 | **模型能力与全栈技术**：能力边界、Benchmark、对齐、推理加速、训练与部署 | **单个系统的机制细节**：agent 运行时设计、diffusion LM 的训练 / 推理算法 |
| **覆盖对象** | 8 个生成式模型 / 产品系列（Stability AI、OpenAI 生成线、Google、Midjourney、可灵、Runway、字节、阿里万相） | 15 个 LLM 模型 / 系列（Claude、DeepSeek、Qwen、GPT、Gemini、Grok、GLM、Kimi、LLaMA 等） | **2 个具体项目**：`mini-swe-agent` v2.3.0（开源 agent 源码）、Nemotron-Labs-Diffusion（NVIDIA 论文） |
| **技术专题数** | 8 个（DiffusionModels、DiT、VideoGen、ControllableGen、3DGen、AudioGen、AvatarGen、ImageEditing） | 10 个（SpeculativeDecoding、LongContext、MoE、ReasoningModels、VLM、Agent、Alignment、TrainingInfra、QuantizationEdge、RAG） | 无「专题」抽象 —— 按**项目**组织 |
| **文档粒度** | 每系列 **1 份** 汇总报告（16 份） | 多数系列 1 份；DeepSeek / Qwen / SpeculativeDecoding **分册展开**（36 份） | 每项目一整套：**1 份深度报告** + 论文精读全流程材料（计划 / 笔记 / 概念卡 / 来源索引 / 原始提取 / 结构化 JSON） |
| **文档风格** | 架构时间线 → 模型结构详解 → 竞品对比 | 模型列表 → 关键能力 → 生态 → 竞品对比；专题偏论文方法梳理 | 源码地图 → 运行时故事 → 设计追问 → 维护者笔记；论文侧含**个人解读**与开放问题 |
| **上游独立仓库** | `git@github.com:zhoucanzong/AIGC-Research.git`（1 次 commit · `main`） | `git@github.com:zhoucanzong/LLM-Research.git`（7 次 commit · `main`） | **无**（从来不是 Git 仓库，无提交历史） |
| **库内 README** | [有](AIGC-Research/README.md) | [有](LLM-Research/README.md) | **无** —— 本索引 §4 即其唯一索引 |
| **在本仓库中的形态** | 普通子目录 `AIGC-Research/`（**无嵌套 `.git`**，不产生 gitlink） | 普通子目录 `LLM-Research/`（同上） | 普通子目录 `Repo-Research/`（本就不是仓库，无 `.git` 可移除） |

### 1.2 差异速览

| 维度 | AIGC-Research | LLM-Research | Repo-Research |
| :-- | :-- | :-- | :-- |
| 主题域 | **生成**（图像 / 视频 / 3D / 音频 / 数字人） | **理解与推理**（语言 / 多模态理解）＋ 工程全栈 | **源码级 / 单论文级深读** |
| 文档数量 | 16 份报告 | 36 份报告 | 8 个 `.md` + 1 个 `.json` |
| `.md` 文件数 | 17（16 报告 + 1 README） | 37（36 报告 + 1 README） | 8（无 README） |
| 正文字节 | 611,021 B ≈ 596.7 KB | 1,072,805 B ≈ 1,047.7 KB | 172,767 B ≈ 168.7 KB |
| 目录内容字节（不含 `.git`） | 618,256 B ≈ 603.8 KB | 1,084,878 B ≈ 1,059.5 KB | 189,061 B ≈ 184.6 KB |
| 磁盘占用（`du -sk`） | 640 KB | 1,136 KB | 204 KB |
| 上游提交数 | 1 | 7 | —（非 Git 仓库） |
| 上游仓库 `.git`（**不在本仓库内**；本地副本已移除） | 280,333 B ≈ 273.8 KB | 870,445 B ≈ 850.0 KB | — |
| 目录结构约定 | `ModelSeries/<Name>-research/report.md`、`TechnicalTopics/<Topic>-research/report.md` | 同左，另允许 `Topic-research/<topic-sub>.md` 分册 | **无统一约定**：按项目建目录，内部自由使用 `notes/`、`raw-extracts/`、`papers/` |
| 附加文件 | — | `.gitignore`（另有 `.claude/settings.local.json`，被全局 gitignore 忽略、未纳入版本控制） | `papers/nemotron-labs-diffusion.json`（结构化阅读数据） |

### 1.3 共同点与关键差异

**共同点**

- 三库都是**长期积累的研究资料集**，而非一次性产出。
- 内容**以中文为主，关键术语保留英文**。
- 都强调**可追溯**：AIGC / LLM 报告附来源索引与论文引用；Repo-Research 更彻底 —— 直接保留 PDF 全文提取、来源索引与阅读计划。
- `AIGC-Research/README.md`、`LLM-Research/README.md` 均已加入「仓库归属」说明，标注其现归属 monorepo **ResearchReport**，并给出正确的克隆 / 浏览命令。

**关键差异（Repo-Research 与另两库的根本不同）**

| 方面 | AIGC-Research / LLM-Research | Repo-Research |
| :-- | :-- | :-- |
| 组织结构 | 统一模板：`ModelSeries/` + `TechnicalTopics/`，主报告固定 `report.md` | 按项目自由组织，无模板 |
| 库内索引 | 各有自己的 `README.md` | **没有自己的 README**（索引即本文件 §4） |
| 版本历史 | 有上游 Git 仓库与提交历史（存于 GitHub 存档） | **从来没有 Git 仓库**，无任何提交历史 |
| 内容性质 | 面向「模型 / 技术全景」的成品综述报告 | 面向「单个系统」的**研究过程留痕**：计划、原始提取、笔记、结构化 JSON、个人解读 |
| 覆盖广度 | 广（数十个模型 / 专题） | 窄而深（仅 2 个项目，但含 21 页论文全文与源码级分析） |
| 机器可读性 | 纯 Markdown | 兼有结构化 `JSON`（`papers/nemotron-labs-diffusion.json`） |

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

## 4. [Repo-Research](Repo-Research/) 逐项索引

> ⚠️ **本库没有自己的 `README.md`，本节即它唯一的索引。** 结构与其他两库不同：不是 Git 仓库（无 `.git`、无提交历史、无上游存档），不套用 `ModelSeries/ TechnicalTopics/` 模板，而是**按项目建目录**，目录内自由使用 `notes/`、`raw-extracts/`、`papers/` 等子目录。
> 共 **2 个项目目录 / 8 个 `.md` / 1 个 `.json`**，合计 **189,061 bytes**（`du -sk` 204 KB）。

### 4.1 [mini-swe-agent-research/](Repo-Research/mini-swe-agent-research/) —— 开源 agent 源码深度剖析（1 个文件）

| 文件 | 大小 / 行数 | 一句话说明 |
| :-- | --: | :-- |
| [mini-swe-agent-deep-report.md](Repo-Research/mini-swe-agent-research/mini-swe-agent-deep-report.md) | 34,490 B / 735 行 | **mini-swe-agent v2.3.0 深度架构报告**（分析日期 2026-06-06）：Princeton & Stanford SWE-agent 团队的极简 SWE agent（约 5,200 行 Python / 9,100 行测试，**唯一工具是 bash**、线性消息历史、SWE-bench verified >74%）；含 Codebase Map / Runtime Story / Design Inquiry / Maintainer Notes / Diagrams / Evidence Index 六大部分 |

### 4.2 [nemotron-tri-mode-diffusion/](Repo-Research/nemotron-tri-mode-diffusion/) —— 单论文精读全流程（8 个文件）

论文：**Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding**（Yonggan Fu 等，NVIDIA + Georgia Tech + HKU + MIT，2026-05-19，21 页）

| 文件 | 大小 / 行数 | 一句话说明 |
| :-- | --: | :-- |
| [report.md](Repo-Research/nemotron-tri-mode-diffusion/report.md) | 13,183 B / 206 行 | **中文综述报告**（2026-05-27）：执行摘要 + 核心发现（AR 与 Diffusion 互补、Self-Speculation 优于 MTP/Eagle3、SOL 仍有 76.5% 空间）+ 每条的**个人解读** |
| [plan.md](Repo-Research/nemotron-tri-mode-diffusion/plan.md) | 2,561 B / 28 行 | **研究计划**：核心研究问题、5 个子问题分解（训练框架 / 三模式推理 / SOL 分析 / 实证 / 核心洞见）、搜索策略、范围决策与产出物清单 |
| [knowledge-graph.md](Repo-Research/nemotron-tri-mode-diffusion/knowledge-graph.md) | 10,088 B / 136 行 | **核心概念卡片**（按理解依赖关系组织）：Tri-Mode Language Model、Block-wise Diffusion、Self-Speculation Decoding 等，每张卡含定义 / 类比 / 数学表达 / 关联概念 / 常见误区 |
| [sources-index.md](Repo-Research/nemotron-tri-mode-diffusion/sources-index.md) | 2,363 B / 41 行 | **来源索引**：主论文条目（作者 / 日期 / 页数 / 开源与训练框架）、PDF 提取文件指路、论文中重要引用上下文表（SPEED-Bench、LLaDA、Dream、Eagle-3、LoRA 等） |
| [notes/structured-reading.md](Repo-Research/nemotron-tri-mode-diffusion/notes/structured-reading.md) | 10,416 B / 169 行 | **结构化阅读笔记**（中文）：一句话总结 + 逐章节要点（研究背景三问、训练框架 Sec.2、三模式推理 Sec.3、SOL、实验结论），是 `report.md` 的详细底稿 |
| [raw-extracts/nemotron-tri-mode-fulltext.md](Repo-Research/nemotron-tri-mode-diffusion/raw-extracts/nemotron-tri-mode-fulltext.md) | 98,525 B / 2,430 行 | **论文 PDF 全文提取**（21 页，逐页文本，约 96K 字符）—— 本库体积最大的文件，供全文检索与原文核对 |
| [raw-extracts/pdf-fu_等__…dif.md](Repo-Research/nemotron-tri-mode-diffusion/raw-extracts/pdf-fu_%E7%AD%89__nemotronlabsdiffusion_a_trimode_language_model_unifying_autoregressive_dif.md) | 1,141 B / 28 行 | **PDF 提取占位/模板**（脚本自动生成，正文未填入）—— 实际全文见上一条，保留它是为记录提取流程 |
| [papers/nemotron-labs-diffusion.json](Repo-Research/nemotron-tri-mode-diffusion/papers/nemotron-labs-diffusion.json) | 16,294 B / 47 行 | **结构化阅读 JSON**：基本信息 / 内容摘要 / 研究背景 / 核心方法 / 实验与结果 / 分析与讨论 / 个人评价，含 `relevance: 10`、`quality: 9` 等评分字段，便于后续检索或二次加工 |

---

## 5. 目录结构

本仓库为**扁平化 monorepo**：`AIGC-Research/`、`LLM-Research/`、`Repo-Research/` 都是仓库内的**普通目录**（内部**没有** `.git`），统一由根目录的 `.git` 管理。

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
├── LLM-Research/                            ← 普通目录（上游 LLM-Research 仓库的内容快照）
│   ├── .gitignore
│   ├── README.md
│   ├── ModelSeries/                         # 15 个模型系列 / 20 份报告
│   │   ├── Claude-research/report.md
│   │   ├── DeepSeek-research/               #   3 份（主报告 + 2 分册）
│   │   ├── Doubao-Seed-research/report.md
│   │   ├── GLM-research/report.md
│   │   ├── GPT-research/report.md
│   │   ├── Gemini-research/report.md
│   │   ├── Grok-research/report.md
│   │   ├── Hunyuan-research/report.md
│   │   ├── Kimi-research/report.md
│   │   ├── LLaMA-research/report.md
│   │   ├── MiMo-research/report.md
│   │   ├── MiniMax-research/report.md
│   │   ├── Mistral-research/report.md
│   │   ├── Nemotron-research/report.md
│   │   └── Qwen-research/                   #   4 份（主报告 + 3 分册）
│   └── TechnicalTopics/                     # 10 个技术专题 / 16 份报告
│       ├── SpeculativeDecoding-research/    #   7 份（主报告 + 6 分册）
│       ├── LongContext-research/report.md
│       ├── MoE-research/report.md
│       ├── ReasoningModels-research/report.md
│       ├── VLM-research/report.md
│       ├── Agent-research/report.md
│       ├── Alignment-research/report.md
│       ├── TrainingInfra-research/report.md
│       ├── QuantizationEdge-research/report.md
│       └── RAG-research/report.md
│
└── Repo-Research/                           ← 普通目录（非 Git 仓库，无上游存档；无自身 README）
    ├── mini-swe-agent-research/
    │   └── mini-swe-agent-deep-report.md    # 源码级深度架构报告（735 行）
    └── nemotron-tri-mode-diffusion/
        ├── report.md                        # 中文综述报告
        ├── plan.md                          # 研究计划
        ├── knowledge-graph.md               # 核心概念卡片
        ├── sources-index.md                 # 来源索引
        ├── notes/structured-reading.md      # 结构化阅读笔记
        ├── raw-extracts/
        │   ├── nemotron-tri-mode-fulltext.md   # PDF 全文提取（2,430 行）
        │   └── pdf-fu_等__…dif.md              # PDF 提取占位模板
        └── papers/nemotron-labs-diffusion.json # 结构化阅读 JSON
```

**命名约定**

- `AIGC-Research/`、`LLM-Research/`：`ModelSeries/<Name>-research/` 与 `TechnicalTopics/<Topic>-research/`，主报告固定名为 `report.md`；未单独展开的系列 / 专题**只有** 1 份 `report.md`，需要深挖时才在目录内新增 `<topic>-<sub>.md` 分册（如 `speculative-eagle-series.md`）。
- `Repo-Research/`：**无统一模板**，以「一个项目一个顶层目录」组织，目录内按用途自由分层（`notes/` 笔记、`raw-extracts/` 原始提取、`papers/` 结构化数据）。

> `.claude/settings.local.json`（本地工具配置）不在此树中：它被全局 gitignore 规则忽略，**未纳入版本控制**。

---

## 6. 报告数量与体积统计

> 统计范围 = **三个资料库目录本身**（`AIGC-Research/`、`LLM-Research/`、`Repo-Research/`），已**不含**任何 `.git`。其中「报告正文」指 AIGC / LLM 的 52 份报告文件（不含 3 个 `README.md`）；Repo-Research 的 8 个 `.md` 单列为「深读文档」。

### 6.1 按库汇总

| 指标 | AIGC-Research | LLM-Research | Repo-Research | 合计 |
| :-- | --: | --: | --: | --: |
| 模型系列目录数 | 8 | 15 | — | 23 |
| 技术专题目录数 | 8 | 10 | — | 18 |
| 项目目录数 | — | — | 2 | 2 |
| 报告数 / 文档数（不含 README） | 16 份报告 | 36 份报告 | 8 个 `.md` + 1 个 `.json` | **52 份报告 + 8 份深读文档** |
| ├ 文件名字面为 `report.md` | 16 | 25 | 1（`nemotron-tri-mode-diffusion/report.md`） | 42 |
| └ 其他 `.md`（分册 / 辅文档 / 深度报告） | 0 | 11 | 7 | 18 |
| 正文字节 | 611,021 | 1,072,805 | 172,767 | **1,856,593** |
| 正文行数 | 12,733 | 17,782 | 3,773 | **34,288** |
| `.md` 文件数（含库内 README） | 17 | 37 | 8（无 README） | **62** |
| 目录内文件数（全部类型） | 17 | 39 | 9 | 65 |
| 目录内容字节（不含 `.git`） | 618,256 | 1,084,878 | 189,061 | **1,892,195** |
| 磁盘占用 `du -sk` | 640 KB | 1,136 KB | 204 KB | **1,980 KB** |
| 纳入版本控制的文件 | 17 | 38 | 9 | 64 |

> 全仓库口径（含根目录 `README.md`、`.gitignore`）：**66** 个跟踪文件 · 工作树 **约 1.85 MiB**（≈ 1.94 MB）· `du -sk`（不含 `.git`）**约 2,040 KB**（`.git` 另计，约 1.2 MB）。
> 上述体积随本索引更新而小幅浮动，故取约值。
> LLM-Research 目录内 39 个文件中，`.claude/settings.local.json` 被全局 gitignore 忽略，故跟踪 38 个。

### 6.2 逐目录分布

**AIGC-Research**（报告正文字节与行数）

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

**Repo-Research**（按文件；`.md` 计入行数，`.json` 不计行数口径）

| 文件 | 类型 | 行数 | 字节 |
| :-- | :-- | --: | --: |
| mini-swe-agent-research/mini-swe-agent-deep-report.md | 深度报告 | 735 | 34,490 |
| nemotron-tri-mode-diffusion/report.md | 综述报告 | 206 | 13,183 |
| nemotron-tri-mode-diffusion/notes/structured-reading.md | 阅读笔记 | 169 | 10,416 |
| nemotron-tri-mode-diffusion/knowledge-graph.md | 概念卡片 | 136 | 10,088 |
| nemotron-tri-mode-diffusion/sources-index.md | 来源索引 | 41 | 2,363 |
| nemotron-tri-mode-diffusion/plan.md | 研究计划 | 28 | 2,561 |
| nemotron-tri-mode-diffusion/raw-extracts/nemotron-tri-mode-fulltext.md | 原始提取 | 2,430 | 98,525 |
| nemotron-tri-mode-diffusion/raw-extracts/pdf-fu_等__…dif.md | 提取占位 | 28 | 1,141 |
| nemotron-tri-mode-diffusion/papers/nemotron-labs-diffusion.json | 结构化数据 | 47 | 16,294 |

---

## 7. 校验结果

### 7.1 上游原始仓库最终状态（本地副本已于 2026-10-16 移除）

复制与校验阶段（见 §7.2）两库**只读、全程未改动**，其最终状态如下。仓主随后指示「以后统一维护新仓库」，两个本地原始目录已于 **2026-10-16** 移入废纸篓（`~/.Trash/AIGC-Research`、`~/.Trash/LLM-Research`），可从废纸篓恢复，直至清空废纸篓。

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

### 7.2 复制阶段校验（扁平化前，历史留证）

`cp -a <src> Research/<name>`（保留权限、时间戳与 `.git`）。当时两副本各含完整 `.git`，校验结论如下（该 `.git` 现已按计划删除，见 §7.3）：

| 校验项 | AIGC-Research | LLM-Research |
| :-- | :-- | :-- |
| 工作区 `.md` 数量（源 → 副本） | 17 → **17** | 37 → **37** |
| `report.md` 数量（源 → 副本） | 16 → **16** | 25 → **25** |
| 全部普通文件数（源 → 副本） | 80 → **80** | 206 → **206** |
| 工作区文件 SHA-256 逐文件比对 | ✅ 全部一致（18 个非 `.git` 文件） | ✅ 全部一致（42 个非 `.git` 文件） |
| `.git` 内文件 SHA-256 比对 | ⚠️ 仅 `.git/index` 不同（stat cache） | ⚠️ 仅 `.git/index` 不同（stat cache） |
| HEAD tree（源 = 副本） | ✅ `ca974128baf589ecbaf2ed4d9af2bee1b18f2852` | ✅ `fd6ccaf955341f9b7e28de5443862cb578f4eff9` |
| `git fsck --full --strict` | ✅ exit 0，无输出 | ✅ exit 0，无输出 |

### 7.3 扁平化与新仓库校验（当前状态）

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
> `Repo-Research` 无需此步骤：它**本来就不是 Git 仓库**，直接以普通文件纳入。

**② 仓库结构校验**

| 检查项 | 结果 |
| :-- | :-- |
| 根目录是否为 Git 仓库 | ✅ 是（`.git` 仅存在于 `/Users/zhoucanzong/Documents/Research/.git`） |
| 是否存在嵌套 `.git` | ✅ 不存在（三个子目录均为普通目录） |
| 缺失模式检查 `git ls-files -s \| awk '{print $1}' \| sort \| uniq -c` | ✅ **仅 `66 100644`**，gitlink（`160000`）计数 **0** |
| 是否存在 submodule | ✅ 无 `.gitmodules` |
| `git ls-files \| wc -l` | ✅ **66** |
| `git ls-files '*.md' \| wc -l` | ✅ **63**（52 份报告 + 8 份 Repo 深读 + 3 个 README） |
| AIGC / LLM 报告是否全部被跟踪 | ✅ AIGC 16/16 + LLM 36/36 = **52/52** |
| Repo-Research 文件是否全部被跟踪 | ✅ **9/9**（8 个 `.md` + 1 个 `.json`） |
| `git status --short`（提交后） | ✅ **空**（干净；`.claude/settings.local.json` 被全局 gitignore 忽略，不产生噪声） |
| 提交者身份 | `zhoucanzong <zhoucanzong@gmail.com>`（来自全局 `~/.gitconfig`，未设置任何 BotHarness 身份） |
| GPG 签名 | 未启用（`commit.gpgsign` 未设置） |
| 最近提交 SHA / 分支 / remote | 见 `git log -1`、`git branch --show-current`、`git remote -v`（本索引随该提交一同发布，故不内嵌自身 SHA） |

### 7.4 Repo-Research 复制与移除校验（2026-10-16）

来源 `/Users/zhoucanzong/Documents/Repo-Research`（**非 Git 仓库**，无 `.git`）→ 目标 `Research/Repo-Research/`。**先复制、校验通过后才移除原位**。

| 校验项 | 结果 |
| :-- | :-- |
| 复制方式 | `cp -a`（目标不存在时执行；执行前已确认目标不存在） |
| 源 / 副本文件数（排除 `.DS_Store`） | 9 → **9** ✅ |
| 源 / 副本总字节（排除 `.DS_Store`） | 189,061 B → **189,061 B** ✅ |
| **逐文件 SHA-256 比对** | ✅ **9/9 完全一致**，无差异、无缺失 |
| 副本内 `.DS_Store` | 🗑️ 已删除（源含 1 个 `.DS_Store`，按仓主要求不复制/不提交） |
| 副本 `du -sk` | 204 KB（源 212 KB；差额来自已删除的 `.DS_Store`） |
| 移除前 `realpath` 确认 | ✅ `/Users/zhoucanzong/Documents/Repo-Research`（与目标路径完全一致） |
| 移除前废纸篓冲突检查 | ✅ `~/.Trash/Repo-Research` 当时不存在，无需改用时间戳名 |
| 原位处置方式 | `mv`（**不是 `rm -rf`**）→ `~/.Trash/Repo-Research` |
| 移除后确认 | ✅ `~/Documents/Repo-Research` 已不存在；`~/.Trash/Repo-Research` 存在，`du -sk` = **212 KB**、10 个文件（含 `.DS_Store`），与源一致 |
| 备份状况 | ⚠️ Repo-Research **没有上游 Git 存档**，仓库内副本是主副本，废纸篓副本是**唯一**可恢复的旧位置（清空废纸篓后不可恢复） |

逐文件 SHA-256（源 = 副本）：

```
e2e60cc59547de1209aa773abea8e8a39ee78ba8181c42e040a771073d51d0a3  mini-swe-agent-research/mini-swe-agent-deep-report.md
d6ed2728b89cd3c0df175589442b0bee5dccb867558b54612fb5fe9d82289b4a  nemotron-tri-mode-diffusion/report.md
84132eaf20f60a97cb884739565c5ddcd628634faff7ae684c1a8ac64a64d58d  nemotron-tri-mode-diffusion/plan.md
433f81d51cc7376c032bc134dc220f0cef639607d95a02c81cdaeffd711aa354  nemotron-tri-mode-diffusion/knowledge-graph.md
160cf5b3218345e2fa4d492c5c51807044cea1e5a1eb0e5d8391fb767c109d5b  nemotron-tri-mode-diffusion/sources-index.md
91700645a85dc9b1b3183fb7948552a11a6667f225506478d98397f078a24f76  nemotron-tri-mode-diffusion/notes/structured-reading.md
add59912f210a242d8cd988d54303dac8cabefc78ce94d55008c5b26e8e5d710  nemotron-tri-mode-diffusion/raw-extracts/nemotron-tri-mode-fulltext.md
82c0c591022421004c40ed26239206da1369d3172dad2332f11d90d784f626bb  nemotron-tri-mode-diffusion/raw-extracts/pdf-fu_等__…dif.md
1faa4df3e1123a026e085d91f02ddf7f5ce290d8291b8c0fb4e819e9e199f985  nemotron-tri-mode-diffusion/papers/nemotron-labs-diffusion.json
```

---

## 8. 后续如何更新

### 8.1 拉取与推送（顶层即可，不存在 submodule 语境）

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

### 8.2 新增 / 修改报告

```bash
cd ResearchReport/LLM-Research                     # 或 AIGC-Research

mkdir -p TechnicalTopics/NewTopic-research
$EDITOR TechnicalTopics/NewTopic-research/report.md

cd ..                                              # 回到仓库根目录
git add -A
git commit -m "新增 NewTopic 技术专题调研"
git push origin main
```

`AIGC-Research/`、`LLM-Research/` 的约定：

1. 目录名用 `<Name>-research`（模型系列放 `ModelSeries/`，技术专题放 `TechnicalTopics/`）。
2. 主报告固定命名 `report.md`；深挖分册用 `<topic>-<sub>.md`（全小写连字符）。
3. 报告内容**中文为主、关键术语保留英文**，并附来源索引以便追溯。
4. 沿用统一模板，便于跨库检索与对比。

`Repo-Research/` 的约定（结构自由，但建议沿用既有组织方式）：

```bash
cd ResearchReport/Repo-Research
mkdir -p <new-project>/notes <new-project>/raw-extracts <new-project>/papers
# 每个项目建议产出：report.md（综述）、plan.md（计划）、knowledge-graph.md（概念卡）、
#   sources-index.md（来源）、notes/、raw-extracts/、papers/*.json（结构化数据）
cd .. && git add -A && git commit -m "新增 XXX 深度阅读" && git push origin main
```

### 8.3 与上游独立仓库同步（仅适用于 AIGC-Research / LLM-Research）

**三个子目录中，只有 `AIGC-Research/`、`LLM-Research/` 是上游 GitHub 仓库的内容快照**，不带 Git 历史；本地已无上游仓库副本（2026-10-16 移除，见 §7.1）。如需从上游导入提交，先把存档仓库克隆到本仓库之外，再复制变化：

```bash
# 例：从 GitHub 取上游 AIGC-Research 存档
git clone https://github.com/zhoucanzong/AIGC-Research.git /tmp/AIGC-Research
rsync -a --delete --exclude '.git' --exclude '.DS_Store' \
  /tmp/AIGC-Research/ ResearchReport/AIGC-Research/

cd ResearchReport && git add -A && git commit -m "同步上游 AIGC-Research"
```

> ⚠️ `rsync --delete` 会删除目标端多余文件，执行前请先 `--dry-run` 预览。

> `Repo-Research/` **不适用本节**：它从来不是 Git 仓库，没有任何上游存档；本仓库内的 `Repo-Research/` 就是**唯一权威副本**，直接在其中增删改即可。

> 上游存档仓库（`AIGC-Research`、`LLM-Research`）是否继续保留由仓主决定；此后 **ResearchReport 是唯一在维护的仓库**。

### 8.4 同步更新本索引

新增 / 删除 / 重命名报告、项目或文件后，请回来更新本文件：

1. 更新「本仓库说明」与「汇总项」表的计数与体积；
2. 在 §2 / §3 / §4 对应表格中增删行，并**链接到子目录或具体文件**（多分册目录同时列出各分册文件的链接；Repo-Research 的每个文件都要有链接与一句话说明）；
3. 更新 §6 的按库汇总表与逐目录分布表；
4. 需要时按 §7 的方式重跑校验（`git ls-files -s | awk '{print $1}' | sort | uniq -c`、`git ls-files | wc -l`、`git ls-files '*.md' | wc -l`、`git status --short`、`du -sk`）并更新 §7。

### 8.5 一句话速查

```bash
# 全部 .md 总数 → 63（= 52 份报告 + 8 份 Repo 深读 + 3 个 README）
git ls-files '*.md' | wc -l
# 仅 AIGC/LLM 报告数 → 52
git ls-files 'AIGC-Research/*.md' 'LLM-Research/*.md' | grep -vc 'README\.md$'
# 各库体积
du -sh AIGC-Research LLM-Research Repo-Research
# 全域搜索（例：找所有提到 DiT 的报告）
grep -r "DiT" --include='*.md' AIGC-Research LLM-Research Repo-Research
```

---

## 9. 已知问题与备注

1. **AIGC / LLM 上游 README 的自报计数与实际不一致**（只修引用、未改动其统计数字，在此备注）：
   - `LLM-Research/README.md` 正文写「覆盖 16 个主流模型 / 系列」、徽章写 `Reports-32`，但实际为 **15 个模型系列目录** 与 **36 份报告**（表格行数也只有 15 行）。本索引以**实际文件系统内容**为准。
   - `AIGC-Research/README.md` 的「仓库结构」代码块注释写「技术专题报告（6 个）」，但实际列出并存在 **8 个**专题目录。
2. **`.DS_Store` 已清理**：本仓库内所有 `.DS_Store` 已删除（包括本次纳入的 `Repo-Research/`），并由根目录 `.gitignore` 覆盖（macOS 之后重新生成也不会进入提交）。已移入废纸篓的本地副本（`AIGC-Research`、`LLM-Research`、`Repo-Research`）中仍带着未跟踪的 `.DS_Store`，属其既有状态，未去改动。
3. **License：三库均无 `LICENSE` 文件**。`LLM-Research/README.md` 徽章宣称 MIT，其原 `./LICENSE` 死链已改为**无链接文本徽章**；`Repo-Research/` 同样没有任何许可证声明。若要以 MIT 等许可公开发布本仓库，建议补上统一的许可证文件。
4. **本仓库不含 AIGC-Research / LLM-Research 的 Git 提交历史**：为支持扁平推送，嵌套 `.git` 已移除（见 §7.3）。需要逐次提交历史 / blame 时，请使用上游独立仓库 `AIGC-Research`、`LLM-Research`。`Repo-Research` 本来就没有历史。
5. **内容性质与准确性**：`AIGC-Research/`、`LLM-Research/` 的报告均为 **AI Agent 自动调研生成、未经官方确认**，引用具体参数 / 日期 / benchmark 前请回溯原始来源；`Repo-Research/` 是**人工 + Agent 的阅读笔记**，其中的「个人解读 / 个人评价」带有主观判断（例如 `papers/nemotron-labs-diffusion.json` 中的评分字段），引用时请区分事实与观点。
6. `LLM-Research/.claude/settings.local.json` 被**全局** gitignore 规则（`~/.config/git/ignore`：`**/.claude/settings.local.json`）忽略，因此不在版本控制内；如需强制纳入，使用 `git add -f`。
7. **三个本地原始目录已于 2026-10-16 移除**：按仓主要求「以后统一维护新的」，`~/Documents/AIGC-Research`、`~/Documents/LLM-Research`、`~/Documents/Repo-Research` 均已移入废纸篓（`~/.Trash/`，可恢复直至清空）。其中前两者在移除前已确认：内容 100% 收录于本仓库（§7.2 逐文件 SHA-256 一致），且两个 GitHub 存档仓库的 `refs/heads/main` 与本地 HEAD 完全一致（`101ae64…` / `7deacb5…`）；`Repo-Research` 无上游存档，但已确认 9 个文件 SHA-256 全部一致（§7.4）。因此**未丢失任何报告内容或提交历史**。此后统一维护本仓库 ResearchReport。
8. **`Repo-Research/` 中残留机器相关的绝对路径**：`raw-extracts/nemotron-tri-mode-fulltext.md`、`raw-extracts/pdf-fu_等__…dif.md`、`plan.md`、`sources-index.md` 共 4 个文件、5 处引用了本机的 Zotero 路径 `/Users/zhoucanzong/Zotero/storage/VZ5BMRZW/…pdf`（原始论文 PDF 位置）。这些路径**在其他机器上不可用**，也指向仓库之外的文件；本索引与仓库均未包含该 PDF 本体。若需要跨机使用，建议把这些引用改为相对路径或补充论文公开链接。（本次只做收录与记录，未改动 `Repo-Research/` 内容。）
9. **`Repo-Research/raw-extracts/pdf-fu_等__…dif.md` 是未完成的提取占位**：其正文仅为脚本生成的模板与待办清单（1,141 B），实际全文在同目录的 `nemotron-tri-mode-fulltext.md`。保留它是为了记录提取流程，**不要误当作论文全文**。

---

*索引更新时间：2026-10-16 · 仓库：ResearchReport（已接手统一维护；三个本地上游副本同日移除）· 数据来源：本仓库实际文件系统内容*
