<div align="center">

# 📚 ResearchReport

**一个仓库收敛 AIGC / LLM / 论文深读全部研究产出**

<!-- SCRIPT:badges START -->
![Entries](https://img.shields.io/badge/Entries-47-green?style=flat-square)
![Topics](https://img.shields.io/badge/Topics-21-orange?style=flat-square)
![Markdown](https://img.shields.io/badge/Markdown-108-lightgrey?style=flat-square)
![Updated](https://img.shields.io/badge/Updated-2026--10--16-informational?style=flat-square)
<!-- SCRIPT:badges END -->

</div>

---

## 🗂 一眼看懂

> 5 个板块 = **逻辑视图**（按主题归类，跨物理目录）；物理目录仍是 `AIGC-Research/`、`LLM-Research/`、`Repo-Research/` 三个库（见文末）。

<!-- SCRIPT:panels START · 来源 scripts/panels.json -->
| 板块 | 条目 | 里面有什么 | 代表条目 |
| :-- | --: | :-- | :-- |
| 🧠 **Models** | 23 | 厂商模型/系列逐个精读：Alibaba-Gen、ByteDance-Gen、Google-Gen、Kling、Midjourney、OpenAI-Gen、Runway、StabilityAI、Claude、DeepSeek、Doubao-Seed、GLM… | [GPT](<LLM-Research/ModelSeries/GPT-research/report.md>) · [Qwen](<LLM-Research/ModelSeries/Qwen-research/report.md>) · [Gemini](<LLM-Research/ModelSeries/Gemini-research/report.md>) |
| 💬 **LLM** | 8 | 语言模型能力与技术专题：Agent、Alignment、DecisionModels、LongContext、MoE、RAG、ReasoningModels、VLM | [ReasoningModels](<LLM-Research/TechnicalTopics/ReasoningModels-research/report.md>) · [LongContext](<LLM-Research/TechnicalTopics/LongContext-research/report.md>) · [MoE](<LLM-Research/TechnicalTopics/MoE-research/report.md>) |
| 🎨 **VisualGen** | 8 | 视觉与多模态生成：3DGen、AudioGen、AvatarGen、ControllableGen、DiT、DiffusionModels、ImageEditing、VideoGen | [VideoGen](<AIGC-Research/TechnicalTopics/VideoGen-research/report.md>) · [DiT](<AIGC-Research/TechnicalTopics/DiT-research/report.md>) · [DiffusionModels](<AIGC-Research/TechnicalTopics/DiffusionModels-research/report.md>) |
| 🌍 **WorldModel** | 2 | 世界模型与具身 VLA：EmbodiedVLA、WorldModels | [WorldModels](<AIGC-Research/TechnicalTopics/WorldModels-research/report.md>) · [EmbodiedVLA](<AIGC-Research/TechnicalTopics/EmbodiedVLA-research/report.md>) |
| ⚙️ **Infra** | 6 | 推理/训练基础设施与开源仓库深读：QuantizationEdge、SpeculativeDecoding、TrainingInfra、nemotron-tri-mode-diffusion、sglang、vllm | [SpeculativeDecoding](<LLM-Research/TechnicalTopics/SpeculativeDecoding-research/report.md>) · [vllm](<Repo-Research/vllm-research/report.md>) · [sglang](<Repo-Research/sglang-research/report.md>) |
<!-- SCRIPT:panels END -->

<details>
<summary>🏷 <b>21 个技术专题标签</b>（点击展开）</summary>

<!-- SCRIPT:topics START · 从条目目录生成 -->
`3DGen` · `AudioGen` · `AvatarGen` · `ControllableGen` · `DiT` · `DiffusionModels` · `ImageEditing` · `VideoGen` · `EmbodiedVLA` · `WorldModels` · `Agent` · `Alignment` · `DecisionModels` · `LongContext` · `MoE` · `RAG` · `ReasoningModels` · `VLM` · `QuantizationEdge` · `SpeculativeDecoding` · `TrainingInfra`
<!-- SCRIPT:topics END -->

</details>

## 🕒 最近更新

<!-- SCRIPT:recent START · front-matter date，缺失时回退 git 最近提交日 -->
| 条目 | 板块 | 日期 | 来源 |
| :-- | :-- | :-- | :-- |
| [sglang](<Repo-Research/sglang-research/report.md>) | Infra | 2026-10-16 | front-matter date |
| [vllm](<Repo-Research/vllm-research/report.md>) | Infra | 2026-10-16 | front-matter date |
| [Alibaba-Gen](<AIGC-Research/ModelSeries/Alibaba-Gen-research/report.md>) | Models | 2026-10-16 | 最近提交日 |
| [ByteDance-Gen](<AIGC-Research/ModelSeries/ByteDance-Gen-research/report.md>) | Models | 2026-10-16 | 最近提交日 |
| [Google-Gen](<AIGC-Research/ModelSeries/Google-Gen-research/report.md>) | Models | 2026-10-16 | 最近提交日 |
<!-- SCRIPT:recent END -->

<details>
<summary>📖 <b>完整索引</b>（47 条，点击展开）</summary>

<!-- SCRIPT:index START · 摘要 + 链接（47 行单一真值在 index/by-report.md） -->
共 **47** 条，分属 5 个板块：**Models** 23 · **LLM** 8 · **VisualGen** 8 · **WorldModel** 2 · **Infra** 6。
完整 47 行（条目 | 板块 | 路径）见 **[index/by-report.md](<index/by-report.md>)**（单一真值，由 `scripts/panels.json` 驱动）；按库 / 专题 / 领域的分面见 [index/](<index/>)，总目录见 [INDEX.md](<INDEX.md>)。
<!-- SCRIPT:index END -->

</details>

---

## 📚 三个研究库（物理目录，库内索引保持原结构）

<!-- STATIC: 静态文案；计数与板块名由脚本校准 -->
- **[AIGC-Research](AIGC-Research/README.md)** — 生成式 AI 多模态：18 个条目（8 模型系列 + 10 技术专题）
- **[LLM-Research](LLM-Research/README.md)** — 大语言模型全景：26 个条目（15 模型系列 + 11 技术专题）
- **[Repo-Research](Repo-Research/)** — 开源仓库深读：3 个条目（vLLM / SGLang / Nemotron）+ 1 份无主文档的深读（mini-swe-agent，无 `report.md`）

<!-- STATIC -->
<sub>索引与统计由 `scripts/library_index.py` 生成；总目录 [`INDEX.md`](INDEX.md)，分面索引 [`index/`](index/)，校验与统计 [`docs/`](docs/)，板块配置 [`scripts/panels.json`](scripts/panels.json)。</sub>
