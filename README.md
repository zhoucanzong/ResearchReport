<h1 align="center">ResearchReport</h1>

<p align="center">AI 研究图书馆 · 连接论文、方法与开源实现</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme-cover-dark.svg">
  <img src="assets/readme-cover-light.svg" alt="从论文，读到实现。模型原理、技术专题与开源代码。" width="1280">
</picture>

<p align="center">
  <a href="https://zhoucanzong.github.io/ResearchReport/"><strong>在线阅读 ↗</strong></a>
  &nbsp; · &nbsp;
  <a href="INDEX.md">完整索引</a>
  &nbsp; · &nbsp;
  <a href="docs/research-method.md">阅读与证据说明</a>
</p>

<div align="center">

<!-- SCRIPT:badges START -->
[**62** 主报告](index/by-report.md) &nbsp; · &nbsp; [**163** 分册与子文档](INDEX.md) &nbsp; · &nbsp; [**33** 技术专题](index/by-topic.md) &nbsp; · &nbsp; [**8** 研究板块](#研究板块)
<!-- SCRIPT:badges END -->

</div>

---

## 先选一条阅读路线

| 你想了解什么 | 从哪里开始 |
| :-- | :-- |
| 一个模型或系列的机制与演进 | [模型系列](Models/README.md) → 目标报告 → 论文与来源 |
| 一类方法解决了什么问题 | [技术专题](index/by-topic.md) → 方法对照 → 实验条件与失效边界 |
| 开源系统究竟怎样运行 | [代码深读](OpenSource/README.md) → 运行路径 → 固定版本的源码证据 |

## 研究板块

<!-- SCRIPT:panels START · 来源 scripts/panels.json，配置驱动 -->
<table>
<tr>
<td width="33%" valign="top">
<h3>01 · <a href="Models/README.md">Models</a></h3>
<p><strong>模型系列</strong><br><sub>23 篇主报告 · 厂商模型 / 系列逐个精读</sub></p>
<p><a href="Models/GPT/report.md">GPT</a> · <a href="Models/Qwen/report.md">Qwen</a> · <a href="Models/Gemini/report.md">Gemini</a></p>
<p><a href="Models/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>02 · <a href="LLM/README.md">LLM</a></h3>
<p><strong>语言模型方法</strong><br><sub>9 篇主报告 · 语言模型能力与技术专题</sub></p>
<p><a href="LLM/ReasoningModels/report.md">ReasoningModels</a> · <a href="LLM/LongContext/report.md">LongContext</a> · <a href="LLM/MoE/report.md">MoE</a></p>
<p><a href="LLM/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>03 · <a href="VisualGen/README.md">VisualGen</a></h3>
<p><strong>视觉与多模态</strong><br><sub>8 篇主报告 · 视觉与多模态生成</sub></p>
<p><a href="VisualGen/VideoGen/report.md">VideoGen</a> · <a href="VisualGen/DiT/report.md">DiT</a> · <a href="VisualGen/DiffusionModels/report.md">DiffusionModels</a></p>
<p><a href="VisualGen/README.md"><strong>浏览板块 →</strong></a></p>
</td>
</tr>
<tr>
<td width="33%" valign="top">
<h3>04 · <a href="WorldModel/README.md">WorldModel</a></h3>
<p><strong>世界模型与具身</strong><br><sub>2 篇主报告 · 世界模型与具身 VLA</sub></p>
<p><a href="WorldModel/WorldModels/report.md">WorldModels</a> · <a href="WorldModel/EmbodiedVLA/report.md">EmbodiedVLA</a></p>
<p><a href="WorldModel/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>05 · <a href="AI4Science/README.md">AI4Science</a></h3>
<p><strong>科学研究应用</strong><br><sub>10 篇主报告 · 科学问题中的 AI 方法与实验闭环</sub></p>
<p><a href="AI4Science/ProteinDesign/report.md">ProteinDesign</a> · <a href="AI4Science/MaterialsDiscovery/report.md">MaterialsDiscovery</a> · <a href="AI4Science/WeatherClimate/report.md">WeatherClimate</a> · <a href="AI4Science/AutonomousLabs/report.md">AutonomousLabs</a></p>
<p><a href="AI4Science/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>06 · <a href="Evaluation/README.md">Evaluation</a></h3>
<p><strong>跨领域评测科学</strong><br><sub>1 篇主报告 · 跨领域 AI 评测与测量方法</sub></p>
<p><a href="Evaluation/EvaluationScience/report.md">EvaluationScience</a></p>
<p><a href="Evaluation/README.md"><strong>浏览板块 →</strong></a></p>
</td>
</tr>
<tr>
<td width="33%" valign="top">
<h3>07 · <a href="Infra/README.md">Infra</a></h3>
<p><strong>训练与推理系统</strong><br><sub>3 篇主报告 · 推理 / 训练基础设施</sub></p>
<p><a href="Infra/SpeculativeDecoding/report.md">SpeculativeDecoding</a> · <a href="Infra/QuantizationEdge/report.md">QuantizationEdge</a> · <a href="Infra/TrainingInfra/report.md">TrainingInfra</a></p>
<p><a href="Infra/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>08 · <a href="OpenSource/README.md">OpenSource</a></h3>
<p><strong>开源代码深读</strong><br><sub>6 篇主报告 · 开源仓库代码深读</sub></p>
<p><a href="OpenSource/DeepInfer/report.md">DeepInfer</a> · <a href="OpenSource/vllm/report.md">vllm</a> · <a href="OpenSource/sglang/report.md">sglang</a></p>
<p><a href="OpenSource/README.md"><strong>浏览板块 →</strong></a></p>
</td>
</tr>
</table>
<!-- SCRIPT:panels END -->

## 从这些报告开始

每个方向选一篇入口报告，沿着其中的分册与引用继续阅读。

<!-- SCRIPT:highlights START -->
| 阅读入口 | 报告内容 |
| :-- | :-- |
| **[GPT](<Models/GPT/report.md>)**<br><sub>Models</sub> | OpenAI GPT 系列模型深度调研报告 |
| **[ReasoningModels](<LLM/ReasoningModels/report.md>)**<br><sub>LLM</sub> | 推理模型（Reasoning Models）与 Test-Time Compute 研究报告 |
| **[VideoGen](<VisualGen/VideoGen/report.md>)**<br><sub>VisualGen</sub> | 视频生成技术研究报告 |
| **[WorldModels](<WorldModel/WorldModels/report.md>)**<br><sub>WorldModel</sub> | WorldModels 技术专题调研 |
| **[ProteinDesign](<AI4Science/ProteinDesign/report.md>)**<br><sub>AI4Science</sub> | 蛋白质 binder 发现：从复合物生成到候选筛选 |
| **[EvaluationScience](<Evaluation/EvaluationScience/report.md>)**<br><sub>Evaluation</sub> | 评测科学：分数何时支持“模型更好”或“能力泛化” |
| **[SpeculativeDecoding](<Infra/SpeculativeDecoding/report.md>)**<br><sub>Infra</sub> | 投机解码（Speculative Decoding）技术专题 · 深度调研 |
| **[DeepInfer](<OpenSource/DeepInfer/report.md>)**<br><sub>OpenSource</sub> | DeepInfer：离线推理内核、异步调度与状态契约 |
<!-- SCRIPT:highlights END -->

## 最近更新

<!-- SCRIPT:recent START · 报告日期优先，缺失时回退最近提交日 -->
| 日期 | 阅读条目 | 板块 |
| :-- | :-- | :-- |
| 2026-10-23 | [AntibioticDiscovery](<AI4Science/AntibioticDiscovery/report.md>) | AI4Science |
| 2026-10-23 | [Astronomy](<AI4Science/Astronomy/report.md>) | AI4Science |
| 2026-10-23 | [AutonomousLabs](<AI4Science/AutonomousLabs/report.md>) | AI4Science |
| 2026-10-23 | [Chemistry](<AI4Science/Chemistry/report.md>) | AI4Science |
| 2026-10-23 | [MaterialsDiscovery](<AI4Science/MaterialsDiscovery/report.md>) | AI4Science |
<!-- SCRIPT:recent END -->

[查看全部更新 →](index/recent.md)

## 按问题查找

<!-- SCRIPT:topics START · 从条目目录生成 -->
| 方向 | 专题入口 |
| :-- | :-- |
| **LLM** | [Agent](<LLM/Agent/report.md>) · [Alignment](<LLM/Alignment/report.md>) · [DecisionModels](<LLM/DecisionModels/report.md>) · [LongContext](<LLM/LongContext/report.md>) · [MoE](<LLM/MoE/report.md>) · [RAG](<LLM/RAG/report.md>) · [ReasoningModels](<LLM/ReasoningModels/report.md>) · [ReinforcementLearning](<LLM/ReinforcementLearning/report.md>) · [VLM](<LLM/VLM/report.md>) |
| **VisualGen** | [3DGen](<VisualGen/3DGen/report.md>) · [AudioGen](<VisualGen/AudioGen/report.md>) · [AvatarGen](<VisualGen/AvatarGen/report.md>) · [ControllableGen](<VisualGen/ControllableGen/report.md>) · [DiT](<VisualGen/DiT/report.md>) · [DiffusionModels](<VisualGen/DiffusionModels/report.md>) · [ImageEditing](<VisualGen/ImageEditing/report.md>) · [VideoGen](<VisualGen/VideoGen/report.md>) |
| **WorldModel** | [EmbodiedVLA](<WorldModel/EmbodiedVLA/report.md>) · [WorldModels](<WorldModel/WorldModels/report.md>) |
| **AI4Science** | [AntibioticDiscovery](<AI4Science/AntibioticDiscovery/report.md>) · [Astronomy](<AI4Science/Astronomy/report.md>) · [AutonomousLabs](<AI4Science/AutonomousLabs/report.md>) · [Chemistry](<AI4Science/Chemistry/report.md>) · [MaterialsDiscovery](<AI4Science/MaterialsDiscovery/report.md>) · [MathematicalDiscovery](<AI4Science/MathematicalDiscovery/report.md>) · [Neuroscience](<AI4Science/Neuroscience/report.md>) · [ProteinDesign](<AI4Science/ProteinDesign/report.md>) · [SingleCellPerturbation](<AI4Science/SingleCellPerturbation/report.md>) · [WeatherClimate](<AI4Science/WeatherClimate/report.md>) |
| **Evaluation** | [EvaluationScience](<Evaluation/EvaluationScience/report.md>) |
| **Infra** | [QuantizationEdge](<Infra/QuantizationEdge/report.md>) · [SpeculativeDecoding](<Infra/SpeculativeDecoding/report.md>) · [TrainingInfra](<Infra/TrainingInfra/report.md>) |
<!-- SCRIPT:topics END -->

## 阅读与引用

- **先看条件，再看数字**：模型版本、数据集、指标、硬件和对照方法决定结论适用于哪里。
- **区分来源与验证**：论文作者自报、源码观察、研究推断与独立复现分别说明；精读不等于实验已经复现。
- **保留不确定性**：待核项目和受限证据连同边界一起引用，不把缺失信息补成确定结论。

详见 [阅读与证据说明](docs/research-method.md) · [待复核条目](index/stale.md)。

<details>
<summary><strong>展开完整索引与目录结构</strong></summary>

### 完整索引

<!-- SCRIPT:index START · 条目单一真值在 index/by-report.md -->
共 **62** 条，分属 **8** 个板块：Models 23 · LLM 9 · VisualGen 8 · WorldModel 2 · AI4Science 10 · Evaluation 1 · Infra 3 · OpenSource 6。
完整 62 行（条目 | 板块 | 路径）见 **[index/by-report.md](<index/by-report.md>)**；按域 / 主题 / 来源分面见 [index/](<index/>)，总目录见 [INDEX.md](<INDEX.md>)。
<!-- SCRIPT:index END -->

### 目录结构

<!-- SCRIPT:structure START · 来源 scripts/panels.json，配置驱动 -->
```text
ResearchReport/    62 条目 · 33 专题 · 8 板块
│
├─ 🧠 Models/        23 条 · 厂商模型 / 系列逐个精读（GPT · Qwen · Gemini …）
├─ 💬 LLM/            9 条 · 语言模型能力与技术专题（ReasoningModels · LongContext · MoE …）
├─ 🎨 VisualGen/      8 条 · 视觉与多模态生成（VideoGen · DiT · DiffusionModels …）
├─ 🌍 WorldModel/     2 条 · 世界模型与具身 VLA（WorldModels · EmbodiedVLA …）
├─ 🧪 AI4Science/    10 条 · 科学问题中的 AI 方法与实验闭环（ProteinDesign · MaterialsDiscovery · WeatherClimate …）
├─ 📏 Evaluation/     1 条 · 跨领域 AI 评测与测量方法（EvaluationScience …）
├─ ⚙️ Infra/          3 条 · 推理 / 训练基础设施（SpeculativeDecoding · QuantizationEdge · TrainingInfra …）
├─ 🔧 OpenSource/     6 条 · 开源仓库代码深读（DeepInfer · vllm · sglang …）
│
└─ ⚙ 生成管线：scripts/panels.json（单一真值）→ library_index.py
              → README / INDEX.md / index/* / 站点 nav
```
<!-- SCRIPT:structure END -->

</details>

## 维护与贡献

新增和修订报告请遵循 [研究约定](docs/team.md)，维护步骤见 [维护指南](docs/maintenance.md)，校验要求见 [核验记录](docs/verification.md)。

<!-- STATIC -->
<sub>板块、条目、推荐与统计统一生成，研究正文保留为可阅读、可追溯的 Markdown。</sub>
