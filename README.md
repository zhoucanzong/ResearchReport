<h1 align="center">AI 论文与技术报告精读</h1>

<p align="center">读懂研究问题与方法机制，按需追踪开源实现</p>

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
[**76** 主报告](index/by-report.md) &nbsp; · &nbsp; [**278** 分册与子文档](INDEX.md) &nbsp; · &nbsp; [**45** 研究专题](index/by-topic.md) &nbsp; · &nbsp; [**9** 研究板块](#研究板块)
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
<p><strong>语言模型方法</strong><br><sub>12 篇主报告 · 语言模型能力、训练数据与技术专题</sub></p>
<p><a href="LLM/ReasoningModels/report.md">推理模型与测试时计算</a> · <a href="LLM/LongContext/report.md">长上下文</a> · <a href="LLM/MoE/report.md">混合专家模型（MoE）</a> · <a href="LLM/TrainingData/report.md">训练数据策展</a></p>
<p><a href="LLM/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>03 · <a href="Agents/README.md">Agents</a></h3>
<p><strong>智能体系统</strong><br><sub>3 篇主报告 · Agent 系统围绕决策闭环展开，覆盖记忆、工具、长程执行、电脑使用与安全</sub></p>
<p><a href="Agents/AgentSystems/report.md">智能体系统</a> · <a href="Agents/ComputerUse/report.md">电脑使用 Agent</a> · <a href="Agents/AgentSecurity/report.md">工具 Agent 安全</a></p>
<p><a href="Agents/README.md"><strong>浏览板块 →</strong></a></p>
</td>
</tr>
<tr>
<td width="33%" valign="top">
<h3>04 · <a href="AIGC/README.md">AIGC</a></h3>
<p><strong>AIGC</strong><br><sub>9 篇主报告 · 图像、视频、音频、3D、数字人生成及相关架构与编辑方法</sub></p>
<p><a href="AIGC/VideoGen/report.md">视频生成</a> · <a href="AIGC/DiT/report.md">扩散 Transformer（DiT）</a> · <a href="AIGC/DiffusionModels/report.md">扩散模型</a></p>
<p><a href="AIGC/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>05 · <a href="WorldModel/README.md">WorldModel</a></h3>
<p><strong>世界模型与具身</strong><br><sub>3 篇主报告 · 世界模型与具身 VLA</sub></p>
<p><a href="WorldModel/WorldModels/report.md">世界模型</a> · <a href="WorldModel/EmbodiedVLA/report.md">机器人视觉语言动作模型（VLA）</a> · <a href="WorldModel/EmbodiedPlanning/report.md">具身预测规划</a></p>
<p><a href="WorldModel/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>06 · <a href="AI4Science/README.md">AI4Science</a></h3>
<p><strong>科学研究应用</strong><br><sub>10 篇主报告 · 科学问题中的 AI 方法与实验闭环</sub></p>
<p><a href="AI4Science/ProteinDesign/report.md">蛋白质与肽结合体设计</a> · <a href="AI4Science/MaterialsDiscovery/report.md">生成式材料设计</a> · <a href="AI4Science/WeatherClimate/report.md">天气与气候预测</a> · <a href="AI4Science/AutonomousLabs/report.md">自主实验室</a></p>
<p><a href="AI4Science/README.md"><strong>浏览板块 →</strong></a></p>
</td>
</tr>
<tr>
<td width="33%" valign="top">
<h3>07 · <a href="Evaluation/README.md">Evaluation</a></h3>
<p><strong>跨领域评测科学</strong><br><sub>2 篇主报告 · 跨领域 AI 评测与测量方法</sub></p>
<p><a href="Evaluation/EvaluationScience/report.md">评测科学</a> · <a href="Evaluation/ScientificDiscovery/report.md">科学发现的评测方法</a></p>
<p><a href="Evaluation/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>08 · <a href="Infra/README.md">Infra</a></h3>
<p><strong>训练与推理系统</strong><br><sub>6 篇主报告 · 推理 / 训练基础设施</sub></p>
<p><a href="Infra/SpeculativeDecoding/report.md">投机解码</a> · <a href="Infra/QuantizationEdge/report.md">模型量化与边缘部署</a> · <a href="Infra/TrainingInfra/report.md">分布式训练基础设施</a> · <a href="Infra/KVCachePD/report.md">KV Cache 与预填充／解码分离</a> · <a href="Infra/MoEExecution/report.md">MoE 执行与专家通信</a> · <a href="Infra/ServingEvaluation/report.md">在线推理服务与评测</a></p>
<p><a href="Infra/README.md"><strong>浏览板块 →</strong></a></p>
</td>
<td width="33%" valign="top">
<h3>09 · <a href="OpenSource/README.md">OpenSource</a></h3>
<p><strong>开源代码深读</strong><br><sub>8 篇主报告 · 开源仓库代码深读</sub></p>
<p><a href="OpenSource/DeepInfer/report.md">DeepInfer</a> · <a href="OpenSource/vllm/report.md">vLLM</a> · <a href="OpenSource/sglang/report.md">SGLang</a></p>
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
| **[GPT](<Models/GPT/report.md>)**<br><sub>Models</sub> | GPT：从生成式预训练到推理与多模态系统 |
| **[推理模型与测试时计算](<LLM/ReasoningModels/report.md>)**<br><sub>LLM</sub> | 推理模型：测试时计算怎样变成更可靠的解题 |
| **[智能体系统](<Agents/AgentSystems/report.md>)**<br><sub>Agents</sub> | Agent 系统综述：从工具调用到可验证的长程闭环 |
| **[视频生成](<AIGC/VideoGen/report.md>)**<br><sub>AIGC</sub> | 视频生成：从图像先验到时空建模 |
| **[世界模型](<WorldModel/WorldModels/report.md>)**<br><sub>WorldModel</sub> | WorldModels 技术专题调研 |
| **[蛋白质与肽结合体设计](<AI4Science/ProteinDesign/report.md>)**<br><sub>AI4Science</sub> | 蛋白质 binder 发现：从复合物生成到候选筛选 |
| **[评测科学](<Evaluation/EvaluationScience/report.md>)**<br><sub>Evaluation</sub> | 评测科学：分数何时支持“模型更好”或“能力泛化” |
| **[投机解码](<Infra/SpeculativeDecoding/report.md>)**<br><sub>Infra</sub> | 投机解码（Speculative Decoding）技术专题 · 深度调研 |
| **[DeepInfer](<OpenSource/DeepInfer/report.md>)**<br><sub>OpenSource</sub> | DeepInfer：离线推理内核、异步调度与状态契约 |
<!-- SCRIPT:highlights END -->

## 最近更新

<!-- SCRIPT:recent START · 报告日期优先，缺失时回退最近提交日 -->
| 日期 | 阅读条目 | 板块 |
| :-- | :-- | :-- |
| 2026-10-28 | [Harness²](<OpenSource/Harness2/report.md>) | OpenSource |
| 2026-10-28 | [REA](<OpenSource/REA/report.md>) | OpenSource |
| 2026-10-26 | [智能体系统](<Agents/AgentSystems/report.md>) | Agents |
| 2026-10-26 | [电脑使用 Agent](<Agents/ComputerUse/report.md>) | Agents |
| 2026-10-26 | [决策模型（Decision Models）](<LLM/DecisionModels/report.md>) | LLM |
<!-- SCRIPT:recent END -->

[查看全部更新 →](index/recent.md)

## 研究专题

<!-- SCRIPT:topics START · 从条目目录生成 -->
| 方向 | 专题入口 |
| :-- | :-- |
| **LLM** | [模型对齐与后训练](<LLM/Alignment/report.md>) · [决策模型（Decision Models）](<LLM/DecisionModels/report.md>) · [扩散语言模型](<LLM/DiffusionLM/report.md>) · [OCR 与文档解析](<LLM/DocumentParsing/report.md>) · [长上下文](<LLM/LongContext/report.md>) · [混合专家模型（MoE）](<LLM/MoE/report.md>) · [大模型辅助运筹建模与求解](<LLM/OperationsResearch/report.md>) · [检索增强生成（RAG）](<LLM/RAG/report.md>) · [推理模型与测试时计算](<LLM/ReasoningModels/report.md>) · [LLM 后训练中的强化学习](<LLM/ReinforcementLearning/report.md>) · [训练数据策展](<LLM/TrainingData/report.md>) · [视觉语言模型（VLM）](<LLM/VLM/report.md>) |
| **Agents** | [智能体系统](<Agents/AgentSystems/report.md>) · [电脑使用 Agent](<Agents/ComputerUse/report.md>) · [工具 Agent 安全](<Agents/AgentSecurity/report.md>) |
| **AIGC** | [3D 生成](<AIGC/3DGen/report.md>) · [音频与音乐生成](<AIGC/AudioGen/report.md>) · [数字人与 Avatar](<AIGC/AvatarGen/report.md>) · [可控生成](<AIGC/ControllableGen/report.md>) · [扩散 Transformer（DiT）](<AIGC/DiT/report.md>) · [扩散模型](<AIGC/DiffusionModels/report.md>) · [图像编辑与修复](<AIGC/ImageEditing/report.md>) · [图像生成](<AIGC/ImageGeneration/report.md>) · [视频生成](<AIGC/VideoGen/report.md>) |
| **WorldModel** | [具身预测规划](<WorldModel/EmbodiedPlanning/report.md>) · [机器人视觉语言动作模型（VLA）](<WorldModel/EmbodiedVLA/report.md>) · [世界模型](<WorldModel/WorldModels/report.md>) |
| **AI4Science** | [抗生素发现](<AI4Science/AntibioticDiscovery/report.md>) · [天文图像异常发现](<AI4Science/Astronomy/report.md>) · [自主实验室](<AI4Science/AutonomousLabs/report.md>) · [化学反应条件优化](<AI4Science/Chemistry/report.md>) · [生成式材料设计](<AI4Science/MaterialsDiscovery/report.md>) · [数学与算法发现](<AI4Science/MathematicalDiscovery/report.md>) · [神经活动表征与解码](<AI4Science/Neuroscience/report.md>) · [蛋白质与肽结合体设计](<AI4Science/ProteinDesign/report.md>) · [单细胞扰动预测](<AI4Science/SingleCellPerturbation/report.md>) · [天气与气候预测](<AI4Science/WeatherClimate/report.md>) |
| **Evaluation** | [评测科学](<Evaluation/EvaluationScience/report.md>) · [科学发现的评测方法](<Evaluation/ScientificDiscovery/report.md>) |
| **Infra** | [KV Cache 与预填充／解码分离](<Infra/KVCachePD/report.md>) · [MoE 执行与专家通信](<Infra/MoEExecution/report.md>) · [模型量化与边缘部署](<Infra/QuantizationEdge/report.md>) · [在线推理服务与评测](<Infra/ServingEvaluation/report.md>) · [投机解码](<Infra/SpeculativeDecoding/report.md>) · [分布式训练基础设施](<Infra/TrainingInfra/report.md>) |
| **分析分册** | [查看 18 篇专题内分析](<index/by-topic.md>) |
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
共 **76** 条，分属 **9** 个板块：Models 23 · LLM 12 · Agents 3 · AIGC 9 · WorldModel 3 · AI4Science 10 · Evaluation 2 · Infra 6 · OpenSource 8。
完整 76 行（条目 | 板块 | 路径）见 **[index/by-report.md](<index/by-report.md>)**；按域 / 主题 / 来源分面见 [index/](<index/>)，总目录见 [INDEX.md](<INDEX.md>)。
<!-- SCRIPT:index END -->

### 目录结构

<!-- SCRIPT:structure START · 来源 scripts/panels.json，配置驱动 -->
```text
ResearchReport/    76 条目 · 45 研究专题 · 9 板块
│
├─ 🧠 Models/        23 条 · 厂商模型 / 系列逐个精读（GPT · Qwen · Gemini …）
├─ 💬 LLM/           12 条 · 语言模型能力、训练数据与技术专题（推理模型与测试时计算 · 长上下文 · 混合专家模型（MoE） …）
├─ 🤖 Agents/         3 条 · Agent 系统围绕决策闭环展开，覆盖记忆、工具、长程执行、电脑使用与安全（智能体系统 · 电脑使用 Agent · 工具 Agent 安全 …）
├─ 🎨 AIGC/           9 条 · 图像、视频、音频、3D、数字人生成及相关架构与编辑方法（视频生成 · 扩散 Transformer（DiT） · 扩散模型 …）
├─ 🌍 WorldModel/     3 条 · 世界模型与具身 VLA（世界模型 · 机器人视觉语言动作模型（VLA） · 具身预测规划 …）
├─ 🧪 AI4Science/    10 条 · 科学问题中的 AI 方法与实验闭环（蛋白质与肽结合体设计 · 生成式材料设计 · 天气与气候预测 …）
├─ 📏 Evaluation/     2 条 · 跨领域 AI 评测与测量方法（评测科学 · 科学发现的评测方法 …）
├─ ⚙️ Infra/          6 条 · 推理 / 训练基础设施（投机解码 · 模型量化与边缘部署 · 分布式训练基础设施 …）
├─ 🔧 OpenSource/     8 条 · 开源仓库代码深读（DeepInfer · vLLM · SGLang …）
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
