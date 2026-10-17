<div align="center">

# 📚 ResearchReport

**一个仓库收敛 AIGC / LLM / 论文深读全部研究产出**

🌐 **[在线阅读](https://zhoucanzong.github.io/ResearchReport/)** · 📦 [GitHub 仓库](https://github.com/zhoucanzong/ResearchReport)

<!-- SCRIPT:badges START -->
[![Site](https://img.shields.io/badge/Site-在线阅读-3f51b5?style=flat-square)](https://zhoucanzong.github.io/ResearchReport/)
![Entries](https://img.shields.io/badge/Entries-48-5c6bc0?style=flat-square)
![Topics](https://img.shields.io/badge/Topics-21-7986cb?style=flat-square)
![Panels](https://img.shields.io/badge/Panels-6-9fa8da?style=flat-square)
![Updated](https://img.shields.io/badge/Updated-2026--10--17-9e9e9e?style=flat-square)
<!-- SCRIPT:badges END -->

</div>

## 🌳 图书馆结构

<!-- SCRIPT:structure START · 来源 scripts/panels.json（配置驱动，勿手改） -->
```text
ResearchReport/    48 条目 · 21 专题 · 6 板块
│
├─ 🧠 Models/        23 条 · 厂商模型 / 系列逐个精读（GPT · Qwen · Gemini …）
├─ 💬 LLM/            8 条 · 语言模型能力与技术专题（ReasoningModels · LongContext · MoE …）
├─ 🎨 VisualGen/      8 条 · 视觉与多模态生成（VideoGen · DiT · DiffusionModels …）
├─ 🌍 WorldModel/     2 条 · 世界模型与具身 VLA（WorldModels · EmbodiedVLA …）
├─ ⚙️ Infra/          3 条 · 推理 / 训练基础设施（SpeculativeDecoding · QuantizationEdge · TrainingInfra …）
├─ 🔧 OpenSource/     4 条 · 开源仓库代码深读（vllm · sglang · nemotron …）
│
└─ ⚙ 生成管线：scripts/panels.json（单一真值）→ library_index.py
              → README / INDEX.md / index/* / 站点 nav
```
<!-- SCRIPT:structure END -->

## 🗂 六大板块

<!-- SCRIPT:panels START · 来源 scripts/panels.json（配置驱动，勿手改） -->
<table>
<tr>
<td align="center" width="33%"><br>🧠<br><b>Models</b> · <b>23</b> 条<br><sub>厂商模型 / 系列逐个精读</sub><br><sub><a href="Models/GPT/report.md">GPT</a> · <a href="Models/Qwen/report.md">Qwen</a> · <a href="Models/Gemini/report.md">Gemini</a></sub><br><a href="Models/"><b>进入 →</b></a><br><br></td>
<td align="center" width="33%"><br>💬<br><b>LLM</b> · <b>8</b> 条<br><sub>语言模型能力与技术专题</sub><br><sub><a href="LLM/ReasoningModels/report.md">ReasoningModels</a> · <a href="LLM/LongContext/report.md">LongContext</a> · <a href="LLM/MoE/report.md">MoE</a></sub><br><a href="LLM/"><b>进入 →</b></a><br><br></td>
<td align="center" width="33%"><br>🎨<br><b>VisualGen</b> · <b>8</b> 条<br><sub>视觉与多模态生成</sub><br><sub><a href="VisualGen/VideoGen/report.md">VideoGen</a> · <a href="VisualGen/DiT/report.md">DiT</a> · <a href="VisualGen/DiffusionModels/report.md">DiffusionModels</a></sub><br><a href="VisualGen/"><b>进入 →</b></a><br><br></td>
</tr>
<tr>
<td align="center" width="33%"><br>🌍<br><b>WorldModel</b> · <b>2</b> 条<br><sub>世界模型与具身 VLA</sub><br><sub><a href="WorldModel/WorldModels/report.md">WorldModels</a> · <a href="WorldModel/EmbodiedVLA/report.md">EmbodiedVLA</a></sub><br><a href="WorldModel/"><b>进入 →</b></a><br><br></td>
<td align="center" width="33%"><br>⚙️<br><b>Infra</b> · <b>3</b> 条<br><sub>推理 / 训练基础设施</sub><br><sub><a href="Infra/SpeculativeDecoding/report.md">SpeculativeDecoding</a> · <a href="Infra/QuantizationEdge/report.md">QuantizationEdge</a> · <a href="Infra/TrainingInfra/report.md">TrainingInfra</a></sub><br><a href="Infra/"><b>进入 →</b></a><br><br></td>
<td align="center" width="33%"><br>🔧<br><b>OpenSource</b> · <b>4</b> 条<br><sub>开源仓库代码深读</sub><br><sub><a href="OpenSource/vllm/report.md">vllm</a> · <a href="OpenSource/sglang/report.md">sglang</a> · <a href="OpenSource/nemotron/report.md">nemotron</a></sub><br><a href="OpenSource/"><b>进入 →</b></a><br><br></td>
</tr>
</table>
<!-- SCRIPT:panels END -->

## ✨ 亮点推荐

新读者从这里看起（`scripts/panels.json` 的 `highlights` 配置驱动）：

<!-- SCRIPT:highlights START -->
- 🧠 **[GPT](<Models/GPT/report.md>)** — OpenAI GPT 系列模型深度调研报告
- 💬 **[ReasoningModels](<LLM/ReasoningModels/report.md>)** — 推理模型（Reasoning Models）与 Test-Time Compute 研究报告
- 🎨 **[VideoGen](<VisualGen/VideoGen/report.md>)** — 视频生成技术研究报告
- 🌍 **[WorldModels](<WorldModel/WorldModels/report.md>)** — WorldModels 技术专题调研
- ⚙️ **[SpeculativeDecoding](<Infra/SpeculativeDecoding/report.md>)** — 投机解码（Speculative Decoding）技术深度调研报告
- 🔧 **[vllm](<OpenSource/vllm/report.md>)** — vLLM 仓库代码分析报告
<!-- SCRIPT:highlights END -->

## 🏷 专题标签

点击标签直达对应条目：

<!-- SCRIPT:topics START · 从条目目录生成 -->
[`Agent`](<LLM/Agent/report.md>) · [`Alignment`](<LLM/Alignment/report.md>) · [`DecisionModels`](<LLM/DecisionModels/report.md>) · [`LongContext`](<LLM/LongContext/report.md>) · [`MoE`](<LLM/MoE/report.md>) · [`RAG`](<LLM/RAG/report.md>) · [`ReasoningModels`](<LLM/ReasoningModels/report.md>) · [`VLM`](<LLM/VLM/report.md>) · [`3DGen`](<VisualGen/3DGen/report.md>) · [`AudioGen`](<VisualGen/AudioGen/report.md>) · [`AvatarGen`](<VisualGen/AvatarGen/report.md>) · [`ControllableGen`](<VisualGen/ControllableGen/report.md>) · [`DiT`](<VisualGen/DiT/report.md>) · [`DiffusionModels`](<VisualGen/DiffusionModels/report.md>) · [`ImageEditing`](<VisualGen/ImageEditing/report.md>) · [`VideoGen`](<VisualGen/VideoGen/report.md>) · [`EmbodiedVLA`](<WorldModel/EmbodiedVLA/report.md>) · [`WorldModels`](<WorldModel/WorldModels/report.md>) · [`QuantizationEdge`](<Infra/QuantizationEdge/report.md>) · [`SpeculativeDecoding`](<Infra/SpeculativeDecoding/report.md>) · [`TrainingInfra`](<Infra/TrainingInfra/report.md>)
<!-- SCRIPT:topics END -->

## 🕒 最近更新

<!-- SCRIPT:recent START · front-matter date，缺失时回退 git 最近提交日 -->
| 条目 | 板块 | 日期 | 来源 |
| :-- | :-- | :-- | :-- |
| [WorldModels](<WorldModel/WorldModels/report.md>) | WorldModel | 2026-10-17 | front-matter date |
| [DecisionModels](<LLM/DecisionModels/report.md>) | LLM | 2026-10-17 | 最近提交日 |
| [EmbodiedVLA](<WorldModel/EmbodiedVLA/report.md>) | WorldModel | 2026-10-17 | 最近提交日 |
| [sglang](<OpenSource/sglang/report.md>) | OpenSource | 2026-10-16 | front-matter date |
| [this-that-model](<OpenSource/this-that-model/report.md>) | OpenSource | 2026-10-16 | front-matter date |
<!-- SCRIPT:recent END -->

## 📖 怎么用这个图书馆

- **按板块读**：从上面六张卡片进入板块页，每个板块有自己的 README 导览
- **按专题读**：用上面的标签云直达条目，或查 [index/by-topic.md](<index/by-topic.md>) 分面
- **在线阅读**：[站点版](https://zhoucanzong.github.io/ResearchReport/) 有全文搜索、目录树与深/浅色模式
- **找最新**：[index/recent.md](<index/recent.md>) 按日期降序；[index/stale.md](<index/stale.md>) 列出待复核条目

<details>
<summary>📖 <b>完整索引</b>（48 条，点击展开）</summary>

<!-- SCRIPT:index START · 摘要 + 链接（48 行单一真值在 index/by-report.md） -->
共 **48** 条，分属 **6** 个板块：Models 23 · LLM 8 · VisualGen 8 · WorldModel 2 · Infra 3 · OpenSource 4。
完整 48 行（条目 | 板块 | 路径）见 **[index/by-report.md](<index/by-report.md>)**；按域 / 主题 / 来源分面见 [index/](<index/>)，总目录见 [INDEX.md](<INDEX.md>)。
<!-- SCRIPT:index END -->

</details>

<!-- STATIC -->
<sub>索引与统计由 `scripts/library_index.py` 生成（`scripts/panels.json` 驱动板块）；校验与统计见 [docs/](<docs/>)。</sub>
