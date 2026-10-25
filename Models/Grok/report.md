---
display_name: Grok
---

# xAI Grok 系列模型深度调研报告

> **证据范围**：Grok-1 有公开权重与技术报告；后续型号的公开材料主要是官方模型卡、API 文档和发布记录。官方尚未披露 Grok 4+ 的参数规模与完整训练配方，架构和训练过程不能由产品接口或社区推测补足。

> **覆盖范围**：Grok 系列自 2023 年 11 月 Grok-1 至 2026 年 9 月 Grok 4.7 的公开研究与技术材料

---

## 一、研究路线：公开权重、推理后训练与工具系统

Grok 系列的研究证据在不同阶段并不连续：Grok-1 是公开权重的自回归 Transformer，Grok 2 引入官方描述的 Aurora 自回归图像生成模型；Grok 3/4 的公开研究叙述开始强调强化学习、测试时计算与工具使用；Grok 4.1 Fast 进一步报告长时程工具交互训练；Grok 4.20 system card 则把安全/双重用途评估和单/多 agent 部署作为主要公开材料。后续 4.7 API 页披露输入接口与 reasoning effort，但没有完整训练配方。

这条路线可以拆成三个问题：

| 研究问题 | 代表阶段 | 公开材料支持的判断 | 证据边界 |
|---|---|---|---|
| 语言模型如何从基座走向推理模型？ | Grok-1 → Grok-3/4 | Grok-1 model card 说明自回归 Transformer 预训练；Grok-3/4 官方文章描述大规模 RL 和更长 test-time reasoning | Grok 2–4 架构与训练数据/参数均未完整披露，不由 Grok-1 外推 |
| 多模态生成与理解如何并入 Grok？ | Grok-1.5V、Grok-2/Aurora、后续 API | 官方公告确认图像输入，Aurora 被描述为自回归 MoE 图像生成模型 | Aurora 与 Grok 语言模型的参数共享/联合训练关系未公开 |
| 能力何时来自模型、何时来自 agent 系统？ | Grok 4 Heavy、4.1 Fast、4.20 | 官方材料分别描述并行 test-time compute、长时程工具调用训练、multi-agent 部署 | 产品并行协作、模型训练和 API 工具调用是不同层级，不能统称为模型架构 |

因此，Grok 的公开研究史更适合读成“模型能力训练”与“工具/部署系统”两条线逐渐交织，而不是简单的参数规模或生态扩张。xAI 未公开 Grok 4+ 的完整模型结构；本报告将发布材料直接说明的训练目标与接口写作厂商披露，将内部网络和训练细节保留为未知。

---

## 二、版本变化与证据类型

| 阶段 | 代表工作 | 研究变化 | 可读材料 |
|---|---|---|---|
| 开放基座 | Grok-1 (2023) | 自回归文本生成；权重公开，模型卡描述训练数据时间范围和能力限制 | model card + 权重；无完整训练代码/语料 |
| 视觉输入与生成分支 | Grok-1.5V、Grok-2/Aurora (2024) | 图像理解进入聊天模型；Aurora 以自回归 MoE 生成图像 | 官方公告给出模型类型与能力，内部连接关系未披露 |
| RL 推理与 test-time compute | Grok-3/4 (2025) | RL 训练推理；Grok 4 扩大可验证训练数据范围，并加入原生工具使用；Heavy 使用并行 test-time compute | 发布文章给出方法概述和作者 benchmark，未给架构/训练配方 |
| 对话偏好与长时程工具使用 | Grok 4.1/4.1 Fast (2025) | 一支以 AI reward models 优化非可验证偏好；另一支在模拟环境训练多轮工具调用 | 官方发布材料；4.1 与 Fast 是不同产品/模型配置 |
| 系统部署与安全评估 | Grok 4.20/4.7 (2026) | 4.20 system card 区分 single/multi-agent 部署；4.7 API 描述模型输入、工具接口与 reasoning effort | 安全卡 / API 文档；不公开完整网络结构 |

表中的同名相邻版本不表示同一底座连续微调。只在官方材料明确说明时，才将训练路线连接起来；例如 Grok 4 官方文章明确将其 RL 工作与 Grok 3 Reasoning 的训练经验相连，而 4.20/4.7 没有提供同等详细的机制说明。

---

## 三、分代详细分析

### 3.1 Grok-1（2023-11）：首发与差异化定位

Grok-1 是这条模型线中少数可检查权重的版本。官方 [Grok-1 Model Card](https://x.ai/news/grok/model-card) 将它描述为自回归 Transformer：以 next-token prediction 预训练，再通过人类与早期 Grok-0 模型反馈微调；发布版训练数据覆盖至 2023 年第三季度，并由公开互联网数据及 AI tutors 提供的数据组成。模型卡同时指出，Grok-1 本身不能独立搜索网络；需要外部搜索工具时，实时信息能力来自部署系统而非基础模型权重。

2024 年开放权重使研究者可以检查该版本，但没有公开完整训练代码和数据。它不能用于反推 Grok-2 以后封闭型号的专家数、参数量、数据来源或训练目标。早期宣传语和社区逆向分析不作为这一综述的架构证据。

---

### 3.2 Grok-1.5 / 1.5V（2024-03~04）：补齐基础能力

Grok-1.5 的[官方公告](https://x.ai/blog/grok-1.5)强调数学/代码推理提升和 128K 上下文，Grok-1.5V 的[公告](https://x.ai/blog/grok-1.5-vision)再将图像输入加入模型接口。公开材料报告了能力变化，但没有技术论文说明视觉编码器、图文对齐、训练集或对长上下文的独立消融。因而这组版本可确认的是输入长度和模态范围变化，而不是从 Grok-1 推导出的架构连续性。

---

### 3.3 Grok-2（2024-08）：图像生成与实时数据深化

Grok-2 公告的一项重要研究变化是图像生成分支 Aurora。xAI 将 [Aurora](https://x.ai/news/grok-image-generation-release) 描述为自回归 MoE 图像生成网络，以交错文本/图像数据训练，并支持以用户图像为条件进行生成或编辑。这是目前 Grok 相关材料中较明确的一次生成机制披露：它使图像生成不只是把文本回答模型外接一个未说明的 API。但公告未公开视觉 tokenizer、模型规模、联合训练方式或与 Grok-2 文本模型是否共享参数；“同在 Grok 对话中调用”不等于同一模型。

Grok-2 同期也接入 X 搜索等实时工具。这个能力应与 Aurora 区分：前者改变系统检索知识的时间边界，后者是视觉内容生成模型；平台入口的集成并不意味着它们由同一套训练目标获得。

---

### 3.4 Grok-3（2025-01）：推理能力加入

**定位**：xAI 首款"推理模型"，对标 OpenAI o1、DeepSeek-R1、Claude 3.5 Sonnet (Thinking)。

**已知信息**：
- xAI [Grok 3 发布材料](https://x.ai/blog/grok-3)将 Grok 3 Think 描述为通过大规模强化学习优化推理策略，可在数学问题上回溯、检查不同解法，并根据任务投入几秒至几分钟的推理时间。
- 官方发布区分基础模式和 Think 模式。Think 模式评估示例报告最高 compute 设置下的 AIME/GPQA 等成绩；因此，作者报告结果必须保留测试时 compute 与是否使用工具的条件。
- 官方材料没有披露参数量、具体 RL objective、奖励模型、rollout 数量或推理过程是否使用显式搜索树。公开演示中的长思考不等于机制已知。

从研究路线看，Grok 3 是从“预训练知识增加”转向“RL 学习推理策略”的可见节点；xAI 后续公告称 Grok 4 的 RL 规模是沿 Grok 3 Reasoning 观察到的 scaling 趋势继续扩大。这个连续性来自官方方法叙述，但详细训练配方仍未公开。

---

### 3.5 Grok 4（2025-07-09）：推理评测与多 Agent 产品

**关键升级**：
- **Grok 4 Heavy**：作为独立多 Agent 产品提供并行协作；这说明系统部署形态，不揭示 Grok 4 底层模型的专家路由结构
- **ARC-AGI v2**：xAI 发布时报告的得分为 **15.9%**；这是特定 benchmark 与测试配置下的作者结果，不等于广义抽象推理能力，也不等于 AGI 判据。
- **256K 上下文**：长文档、代码库处理能力大幅提升
**Grok 4 Heavy**：
- 多 Agent 并行协作架构，面向复杂研究、编程、数据分析任务

xAI [Grok 4 发布材料](https://x.ai/news/grok-4)称该代继续扩大 RL 训练，将可验证训练数据从主要数学/代码扩展到更多领域，并训练原生工具使用；发布文章报告训练过程中性能随 RL compute 提升。其 ARC-AGI v2 结果来自作者报告；HLE 的说明区分使用 Python/Internet tools 与 text-only 子集；Grok 4 Heavy 则使用 parallel test-time compute。三者分别测训练后的模型、带工具系统和并行推理配置，不能汇总成单个“模型分数”，也不能把 Heavy 的并行 Agent 产品形态写成基础网络结构。

Grok 4 公告描述的是训练路径与benchmark表现，并没有公开参数规模、完整网络结构或 RL 奖励的构造细节。它能支持“xAI 将可验证反馈、工具使用和 test-time compute 作为公开研究方向”的判断，不支持更具体的关于 verifier、搜索树或专家结构推断。

---

### 3.6 Grok 4.1 与 4.1 Fast（2025-11）：偏好对齐与工具训练的分叉

Grok 4.1 将后训练目标从数学/代码等可验证任务扩展到对话风格、帮助性与偏好。xAI [发布页](https://x.ai/news/grok-4-1)称它使用 Grok 4 同类 RL 基础设施，并让 agentic reasoning models 承担非可验证 reward 的评分与迭代。发布页报告了 2025-11-01 至 14 日的 silent rollout：对真实生产流量做盲测成对比较，4.1 相对前一生产模型获选率为 64.78%；这是该流量和评测问题集合上的作者报告，不等于任意用户群体偏好比例。幻觉评估使用分层抽样的生产信息查询和 FActScore 500 条人物简介问题；页面注明评估非 reasoning 型号并启用 web search。

两天后发布的 [Grok 4.1 Fast](https://x.ai/news/grok-4-1-fast) 是面向工具调用的独立 API 型号。xAI 描述它用模拟环境执行长时程 RL，训练多轮、多工具交互，并设计为 2M context。相关 benchmark 结果同时依赖 Agent Tools API、模型 reasoning/non-reasoning 配置、运行成本和任务环境；所以可作为“长时程工具使用被纳入训练目标”的证据，不能把它当成 4.1 消费端模型的架构或通用能力。

---

### 3.7 Grok 4.20 / 4.3（2026-03~04）：多 Agent 部署与证据边界

官方 API 更新记录显示 Grok 4.20 与 4.20 Multi-agent 于 2026-03-10 上线。Grok 4.20 System Card（2026-04-07）提供该型号的风险与双重用途能力评估；官方模型页列出文本/图像输入、文本输出、1M 上下文和工具调用。现有一手材料没有说明所谓“Beta 2 指令、LaTeX、图像搜索改进”对应的模型机制，因此不将这些描述作为技术结论。

2026-05-15 的 API 迁移指南记录旧型号转向 Grok 4.3，并列出其 1M 上下文和 reasoning effort 等接口特征。迁移指南描述接口变更，不解释模型架构；也不能将 Grok 4.1 Fast 的 2M API 配置视为 Grok 4.3 或消费端型号的性能变化。
---

### 3.8 Grok 4.7（2026-09）：当前公开型号的技术边界

xAI API 官方发布说明将 Grok 4.7 定位于 coding、agentic tasks 与 knowledge work，列出 500K 上下文、文本和图像输入、文本输出，以及 low / medium / high / xhigh 四档 reasoning effort。此信息足以描述接口能力，不足以推出模型规模、MoE 结构、训练数据组成或推理算法。官方说明还指出，特定 Fast 部署与公开 API 可用性不同；因此应避免将专用产品入口的行为推广为模型本身的普遍能力。

xAI 的 Grok 4.20 System Card（2026-04-07）补充了另一类一手证据：安全评估按恶意使用与失控风险组织，并覆盖 CBRN、网络安全和有害操纵能力。卡片描述 Grok 4.20 可在 single-agent 与 multi-agent 模式部署；除特别说明外，其评测使用 single-agent 模式。它概述训练流程为公开/第三方/内部数据预训练、定向 mid-training，以及结合监督微调和人类/合成奖励信号的后训练，但没有披露模型参数、完整数据配比或优化细节。多 Agent 产品模式不能被解释成底层模型的专家路由架构。

一手来源：[xAI API Release Notes](https://docs.x.ai/developers/release-notes)、[Grok 4.7 API 模型页](https://docs.x.ai/developers/models/grok-4.7)、[Grok 4.20 System Card](https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf)、[Grok 4.20 API 模型页](https://docs.x.ai/developers/models/grok-4.20)。

---

## 四、研究线如何交叉：推理、工具和多模态各有独立机制

Grok 的公开证据更适合按能力机制分线，而非按 X、Grok.com、API 和订阅入口分产品线：

| 研究线 | 代表材料 | 机制变化 | 与相邻路线的区别 |
|---|---|---|---|
| 文本基座 | Grok-1 Model Card | 自回归 Transformer 预测下一个 token，监督反馈微调 | 有一手模型卡和公开权重；它只描述 Grok-1 |
| 图像生成 | Aurora 公告 | 官方称自回归 MoE，使用交错文本/图像数据；支持图像条件编辑 | 是图像生成模型分支，不能推断与 Grok 对话模型共享全部权重 |
| 推理训练 | Grok-3 → Grok-4 公告 | Grok-3 强化学习学习更长推理；Grok-4 将 RL 规模扩到预训练规模，并扩展可验证任务范围 | 属于模型后训练和推理时计算，不等于多 Agent |
| Agent 工具使用 | Grok-4、4.1 Fast 公告 | RL 学习工具调用；Fast 在模拟环境训练长时程、多轮工具操作 | 结果依赖 Agent Tools、工具协议、环境和交互预算，不只是语言模型输出 |
| 多 Agent 部署 | Grok 4 Heavy、4.20 System Card | 多模型/多 Agent 并行属于系统运行模式；4.20 卡片分 single-agent 与 multi-agent | 系统编排模式不证明单个模型用了 MoE 专家或并行推理模块 |

其中最清楚的训练变化是从 Grok-3/4 的可验证推理到 Grok 4.1 的非可验证偏好：数学/代码可直接用结果或任务通过情况构造 reward；对话风格与帮助性则需要偏好比较或 agentic model-as-judge。Fast 再把训练目标移到多轮工具任务。公开材料说明了训练方向，但未公开奖励模型、rollout 数据规模、训练损失和内部检索策略；这些都应作为未闭合问题。

## 五、系统卡、API 页和论文分别能支持什么

Grok-1 的 model card 给出基础模型定位、训练数据时间范围、next-token objective 和能力限制；其开放权重允许读者检查该 checkpoint。Grok-3/4 发布页提供强化学习、工具使用和作者 benchmark 的概述；Grok 4.1 发布页报告生产流量盲测与事实性评估；Grok 4.20 System Card 按风险域说明评估方法和部署模式；Grok 4.7 API 文档只确认当前可调用的模态、上下文和 reasoning effort 接口。

因此证据应分成四类：基础模型卡、能力发布材料、System Card 和 API 接口文档。接口参数不能补足训练细节；安全评估不能解释架构；发布页中的榜单结果不能自动成为独立复现。Grok 4.20 System Card 覆盖恶意使用、失控风险、CBRN、网络安全与有害操纵评估，且通常在 single-agent 模式测试；这能支持部署风险描述，不能推广成所有 multi-agent 应用的安全结论。

## 六、跨版本综合与仍未解决的问题

Grok 的公开路线包含三种“扩展计算”的方式：扩大预训练获得更广知识；增加 RL 与 reasoning time 让单次回答投入更多计算；接入搜索、代码执行或并行 agent 让模型可以从环境获取外部信息。它们解决的分别是知识覆盖、可验证任务的多步推理和交互式任务执行，benchmark 必须按这些条件拆开。

多模态也分成理解和生成两条路径。Grok-1.5V 将图像输入加入对话模型；Aurora 单独公开为自回归图像生成 MoE；Grok-4.20 System Card 描述文本/图像输入，但图像生成和视频分析通过 grok.com/x.com 的工具实现。故“支持图像”不自动意味着同一模型能生成图像，“产品中可调用 Aurora”也不等于 Grok LLM 内部统一多模态训练。

当前未闭合的核心问题：

- **Grok-4+ 主干是什么？** 未公开参数规模、注意力结构、专家数量和具体模型融合方式。
- **RL 的边际收益如何测？** 官方材料报告训练计算与 benchmark 改善，但缺少完整的算法、奖励模型、数据配比和可重跑基线。
- **工具使用与多 Agent 的收益来自哪里？** 需要将模型版本、工具集合、agent 数量、预算和 scaffold 固定后做消融；System Card 中 single-agent 评估不能代替 multi-agent 实验。
- **Aurora 与 Grok 的模型关系怎样？** 已知 Aurora 的公开描述和 Grok 产品集成，未知共享表征、共同预训练或权重连接。
- **时效信息如何进入答案？** Grok-1 model card 明确说基础模型自身不能独立联网；实时信息来自部署的搜索工具。将平台联网能力写成“模型实时训练/实时知识”会混淆权重知识与检索增强。

本报告不做跨厂商排行榜。ARC-AGI、AIME、FActScore、Arena 和 tool-agent benchmark 的版本、预算、工具和评审协议不同；比较时要分别报告作者结果与独立评测，不将不同设置合并成单一能力排名。

## 七、参考文献

### 7.1 xAI 一手材料

1. xAI, [Grok-1 Model Card](https://x.ai/news/grok/model-card), 2023-11：训练目标、数据范围和能力限制。
2. xAI, [Grok Image Generation / Aurora](https://x.ai/news/grok-image-generation-release), 2024-12：官方称 Aurora 为 autoregressive MoE 图像生成模型。
3. xAI, [Grok 3 Beta — The Age of Reasoning Agents](https://x.ai/blog/grok-3), 2025-02-19：RL 推理、test-time compute 和工具使用的发布描述。
4. xAI, [Grok 4](https://x.ai/news/grok-4), 2025-07-09：RL 扩展、verifiable data、native tool use 和 Heavy 的并行 test-time compute。
5. xAI, [Grok 4.1](https://x.ai/news/grok-4-1), 2025-11-17；[Grok 4.1 Model Card](https://data.x.ai/2025-11-17-grok-4-1-model-card.pdf)：非可验证偏好奖励、生产流量盲测与安全评估。
6. xAI, [Grok 4.1 Fast and Agent Tools API](https://x.ai/news/grok-4-1-fast), 2025-11-19：模拟环境长时程 RL、多轮工具交互与 2M API 配置。
7. xAI, [Grok 4.20 System Card](https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf), 2026-04-07：single-agent / multi-agent 部署定义、风险评估和训练概述。
8. xAI, [Grok API Release Notes](https://docs.x.ai/developers/release-notes)、[Grok 4.7 model page](https://docs.x.ai/developers/models/grok-4.7) 与 [Grok 4.20 model page](https://docs.x.ai/developers/models/grok-4.20)：模型接口、模态和 reasoning effort。API 规格不作为内部架构证据。
