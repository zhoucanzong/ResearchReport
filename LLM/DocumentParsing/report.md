---
display_name: OCR 与文档解析
title: OCR 与文档解析：从字符识别到结构还原
type: research
domain: LLM
subject: DocumentParsing
topic: DocumentParsing
date: 2026-10-25
status: current
---

# OCR 与文档解析：从字符识别到结构还原

把一页文档变成可检索、可计算的内容，不是一次 OCR 调用就能完成。系统要找到文字、表格、公式和图表，判断阅读顺序，保留元素关系，再把结果转成可用结构。任何一步出错，都可能让最终 Markdown 看起来流畅却缺字、串栏、破坏单元格或改错公式。

本专题聚焦这条解析链的设计取舍：模块化流水线如何分工，文档 VLM 怎样共同识别不同元素，粗到细处理怎样分配高分辨率视觉预算，以及不同基准的分数各自在测什么。范围覆盖字符转写、页面结构恢复、图形解析，以及解析结果接入文档检索与问答的边界。[VLM 总览](../VLM/report.md)提供视觉语言建模背景，[输入预算与 grounding 分析](../VLM/topics/evaluation-input-budget.md)补充通用视觉评测方法。

## 推荐阅读路线

先读本页的任务分解与架构比较，再按问题进入精读；每条路线都可独立选读。

| 想理解的问题 | 推荐精读 |
|---|---|
| 一页文档如何拆成区域、恢复顺序并识别内容 | [PaddleOCR-VL](papers/2510.14528-paddleocr-vl.md) → [Dolphin](papers/2505.14059-bytedance-dolphin.md) |
| 高分辨率、视觉压缩和解码预算如何取舍 | [DeepSeek-OCR](papers/2510.18234-deepseek-ocr.md) → [DeepSeek-OCR 2](papers/2601.20552-deepseek-ocr2.md)，再对照 [Coarse-to-Fine](papers/2603.24326-coarse-to-fine.md)、[FastOCR](papers/2605.17447-jd-fastocr.md) |
| 数据和奖励怎样教会模型输出文档结构 | [FireRed-OCR](papers/2603.01840-firered-ocr.md)、[Logics-Parsing](papers/2509.19760-alibaba-logics-parsing.md)、[ABot-OCR](papers/2605.27978-amap-abot-ocr.md)；[HunyuanOCR](papers/2511.19575-hunyuan-ocr.md)与 [1.5](papers/2607.04884-hunyuan-ocr-15.md)展示后续演进 |
| 指标、语言、拍摄条件与逐字忠实度怎样影响结论 | [OmniDocBench](papers/2412.07626-omnidocbench.md) → [MDPBench](papers/2603.28130-mdpbench.md) → [FaithC4](papers/2607.21617-amazon-faithc4.md) |
| 图表结构和多文档证据怎样成为下游可用信息 | [Multimodal OCR / dots.mocr](papers/2603.13032-multimodal-ocr.md)、[Doc-Researcher](papers/2510.21603-huawei-doc-researcher.md) |

## 先看端到端任务怎样分解

可以把文档解析理解为从页面图像到结构树的逐步还原：

```mermaid
flowchart LR
    A[页面图像 / PDF] --> B[版面检测与区域分类]
    B --> C[文字 / 表格 / 公式 / 图表识别]
    C --> D[阅读顺序与跨区域关系]
    D --> E[Markdown / JSON / HTML 等结构输出]
    E --> F[检索、问答、表格计算等下游任务]
```

这几步的误差会串联：漏检区域后，识别器就看不到内容；文字识别对了但多栏顺序错，段落语义仍会混乱；表格单元格全读出但行列关系错，下游计算会得到错误数值。端到端总分方便比较整套系统，却难以单独定位哪一段出了问题。

## 三种架构如何分配工作

| 设计 | 核心做法 | 换来的能力 | 主要依赖/风险 |
|---|---|---|---|
| **模块化流水线** | 检测版面，按元素类型调用 OCR、公式、表格等专用模型，再排序并组装 | 每个组件可独立优化；区域、文本和结构错误较容易分别诊断 | 上游切分和类别错误会传到下游；多个模型及格式接口增加集成成本 |
| **整页端到端 VLM** | 将页面图像与提示一起输入模型，直接生成结构化文本 | 跨区域语义可由同一模型联合处理，减少显式模块边界 | 密集小字要求高分辨率；长输出易漏项或错序；高视觉 token 带来计算成本 |
| **布局引导的紧凑 VLM** | 先预测元素区域与顺序，再用小型视觉语言模型识别裁剪区域 | 把高分辨率计算集中到有效区域，同时保留显式布局信息 | 前级检测与阅读顺序成了关键门槛；裁剪可能丢掉跨区域上下文 |

PaddleOCR-VL 采用第三种结构：PP-DocLayoutV2 检测区域并预测阅读顺序，再用动态分辨率视觉编码器和 0.9B 语言模型识别文本、表格、公式与图表。[PaddleOCR-VL 精读](papers/2510.14528-paddleocr-vl.md) 它不是完全端到端：若布局阶段漏掉或错切区域，元素识别模型拿不到正确输入；但各阶段可分开检查，比从整页生成结果中猜测错误来源更容易。

## 高分辨率不该平均花在每个像素上

细小印刷文字、边注和公式往往需要高分辨率；直接缩小整页会丢掉细节，而把全页升到高分辨率又会显著增加视觉 token。PaddleOCR-VL 的粗到细版本用 VRFM 先定位有效区域及其阅读关系，再将局部交给识别器，减少在背景和空白上的编码开销。[Coarse-to-Fine 精读](papers/2603.24326-coarse-to-fine.md)

论文中的消融支持“结构化选区比单纯裁剪更有用”：在其比较里，朴素区域裁剪减少视觉 token 却降低准确率；加入 VRFM 后，token 数相近而准确率回升。这是特定模型、数据和输入配置下的作者报告结果，说明布局和顺序信息值得保留；它不证明所有页面都能受益。若页面几乎处处有信息，粗检开销、裁切遗漏或跨栏关系损失可能削弱收益。重点应看有效区域召回、细小元素识别和端到端结构，而不是只看 token 数。

## OCR、顺序与结构指标回答不同问题

[OmniDocBench 精读](papers/2412.07626-omnidocbench.md)把页面解析的主要能力拆成 OCR 文本、版面区域检测、阅读顺序、表格和公式结构。归一化编辑距离（NED）适合比较字符/序列差异，mAP 测版面框，TEDS 比较表格树结构，CDM 衡量公式结构相似；这些数值不能互换成一个通用“文档理解分”。阅读顺序分也会被 OCR 漏字和段落合并影响，所以低分未必是排序模块单独出错。

OmniDocBench 的 981 个样本是单页文档，覆盖九类版面和部分语言/扫描条件；它适合诊断页面解析组件，不直接证明多页文档检索、跨页引用或真实业务中的文档问答。页面样本也不是部署业务的自然流量抽样，平均值要结合语言、版式、背景和文字方向切片阅读。

MDPBench 把另一条缺口凸显出来：标准数字文档表现不能代表非拉丁文字或手机实拍页面。其 3,400 张图像覆盖 17 种语言，包含从屏幕或纸张拍摄、倾斜、弯曲、反光和背景变化；作者分别公开与保留测试划分，并报告开源系统在实拍和非拉丁脚本上的明显退化。[MDPBench 精读](papers/2603.28130-mdpbench.md) 这类结果适合说明模型的失效分布，但样本语言和拍摄条件仍不是全球文档的随机样本，不能直接读作现实业务错误率。

## 一个模型分数是怎样被评测代码算出来的

在 VLMEvalKit 的固定 Video-MME 路径中，`Video-MME_8frame + Qwen2.5-VL-7B-Instruct` 将八帧配置交给外部视频预处理器，生成文本后用正则抽取 A–D，解析失败时才尝试 judge 回退。[源码路径精读](../VLM/topics/vlmevalkit-video-mme-path.md) 这条路径说明基准配置、模型接口、输出解析和无效样本处理共同决定最终分数。文档解析评测同样应追踪 PDF 渲染、页面缩放/裁切、元素提取、输出规范化、指标计算和失败分母；若前处理失败被跳过，报告分数就只代表剩下的有效样本。

比较文档解析结果时，至少记录：页面来源与语言、数字生成或实拍、页数/图像分辨率、裁切和动态分辨率策略、OCR/布局组件、视觉 token 或计算预算、输出格式，以及各任务的指标和失败计数。需要解释端到端差异时，再拆出布局检测、文字识别、阅读顺序、表格/公式结构和人工审查样本。跨系统比较须说明预算是否一致；论文原文没有报告的量应标为未知，不以模型规模或营销描述代替。

这些论文展示了文档解析从识别单个字符走向结构恢复、从整页密集编码走向元素选择，以及从规整数字页面走向多语言实拍测试的几条研究线。还缺少跨系统、同页集、统一分辨率/token预算和可审计失败分母的控制比较；本专题没有运行模型或基准，也不据此判定哪种架构总体最佳。

## 哪些团队也在做 OCR 与文档解析

这里列的是截至 2026-10-24 能找到的一手公开证据代表，不是厂商普查或性能榜。研究论文和产品文档回答的问题不同：前者能读方法、数据和实验条件；后者主要说明可用能力与接口，不能据此推断内部模型机制。

| 团队 | 可追溯的一手材料 | 研究问题/路线 | 阅读状态 |
|---|---|---|---|
| 百度 PaddleOCR | [PaddleOCR-VL](papers/2510.14528-paddleocr-vl.md)、[PaddleOCR 3.0 技术报告](https://arxiv.org/abs/2507.05595) | 传统 OCR、版面分析与小型 VLM 逐步整合；布局检测先行，再识别文本、表格、公式等元素 | PaddleOCR-VL 已精读；报告摘要与题录已核 |
| 百度千帆 | [Qianfan-OCR](https://arxiv.org/abs/2603.13398) | 单个端到端模型联合文档解析和理解；可选的 Layout-as-Thought 阶段显式输出框、类别和阅读顺序 | 已核官方论文，尚未精读 |
| 字节跳动 | [Dolphin 精读](papers/2505.14059-bytedance-dolphin.md)（[原文](https://arxiv.org/abs/2505.14059)） | “先分析、后解析”：先生成带阅读顺序的异构版面锚点，再并行识别各区域，尝试在整页生成和多专家流水线间折中 | v1 已精读 |
| 阿里巴巴通义实验室「读光」OCR Team | [Advanced Literate Machinery 官方仓库](https://github.com/AlibabaResearch/AdvancedLiterateMachinery) | 仓库明确由通义实验室语言技术实验室 OCR Team 维护，汇集文档理解、Platypus 通用文字识别和 CC-OCR 评测等公开项目 | 已核对团队归属和项目入口，具体论文尚未精读 |
| 阿里巴巴 Logics Team / Qwen 产品 | [Logics-Parsing 精读](papers/2509.19760-alibaba-logics-parsing.md)（[原文](https://arxiv.org/abs/2509.19760)）、[Qwen OCR 文档](https://docs.modelstudio.console.alibabacloud.com/zh/model-studio/qwen-vl-ocr) | Logics-Parsing 用布局感知奖励训练端到端解析；Qwen OCR 文档说明有专门产品接口，但不公开足够细节来替代论文 | Logics-Parsing v1 已精读；产品文档只作产品证据 |
| 阿里巴巴高德 AMAP CV Lab | [ABot-OCR 精读](papers/2605.27978-amap-abot-ocr.md)（[原文](https://arxiv.org/abs/2605.27978)）、[官方代码仓库](https://github.com/amap-cvlab/ABot-OCR) | 2B VLM 从页面直接生成 Markdown；训练先分阶段建立文字、公式、表格与布局能力，再用感知奖励和结构奖励优化输出 | v1 已精读 |
| DeepSeek | [DeepSeek-OCR](papers/2510.18234-deepseek-ocr.md)、[DeepSeek-OCR 2](papers/2601.20552-deepseek-ocr2.md) | 把页面视觉编码作为上下文压缩路径；第二版改变视觉 token 的顺序建模，关注长文档解析与生成效率的关系 | 两篇已精读 |
| 小红书 | [FireRed-OCR](papers/2603.01840-firered-ocr.md)、[Multimodal OCR / dots.mocr](papers/2603.13032-multimodal-ocr.md) | 一条路线把通用 VLM 专门化为文档解析器；另一条把图表、示意图等图形也变成可解析的结构内容 | 两篇已精读 |
| 腾讯混元 | [HunyuanOCR](papers/2511.19575-hunyuan-ocr.md)、[HunyuanOCR-1.5](papers/2607.04884-hunyuan-ocr-15.md) | 以小型端到端 OCR VLM 统一识别、结构解析和语义抽取；后续报告进一步讨论训练与推理加速 | 两篇已精读 |
| 腾讯微信 WXG | [微信 OCR 图片文字提取技术介绍](https://developer.cloud.tencent.com/article/1798403) | WXG 工程师明确称微信客户端长按提取文字使用微信自研 OCR；文章描述文字存在性/语种检测、文本图像分类、通用或垂类识别，再做版面重排 | 2021 年工程文章，非近期论文；直接证明微信团队有 OCR 研发与产品实践，不能代表当前模型结构 |
| 智谱 | [GLM-OCR](https://arxiv.org/abs/2603.10910) | 视觉编码器与小型语言解码器组合，配合版面分析及区域级识别，并用多 token 预测处理 OCR 的确定性输出 | 已核官方报告 v2 的架构和限制章节，尚未精读 |
| 小米 | [Xiaomi-OCR-0](https://arxiv.org/abs/2609.36136) | 将文档解析与 OCR 问答/信息抽取放进统一小模型训练；报告强调文本锚定、分阶段训练和混合任务强化学习 | 已检索到技术报告，尚未精读 |
| 华为 | [Doc-Researcher 精读](papers/2510.21603-huawei-doc-researcher.md)（[原文](https://arxiv.org/abs/2510.21603)） | 把版面和视觉语义保留、多粒度切分、跨模态检索接到多文档研究流程，关注解析质量如何影响证据检索 | v1 已精读；系统范围超出 OCR 模型 |
| Amazon / AWS AI Labs | [FaithC4 精读](papers/2607.21617-amazon-faithc4.md)（[原文 v2](https://arxiv.org/abs/2607.21617v2)）、[DocVLM](https://arxiv.org/abs/2412.08746)、[TAP-VL](https://www.amazon.science/publications/tap-vl-text-layout-aware-pre-training-for-enriched-vision-language-models) | FaithC4 研究模型会否按语言先验改写可见错字；DocVLM/TAP-VL 则研究将 OCR 文字与版面压缩后接入 VLM | FaithC4 v2 已精读；其余两篇尚未精读 |
| Meta AI | [Nougat](https://arxiv.org/abs/2308.13418)、[Rosetta](https://ai.meta.com/research/publications/rosetta-large-scale-system-for-text-detection-and-recognition-in-images/) | Nougat 把学术 PDF 页转换为结构化标记语言；Rosetta 是面向海量社交图片的文字检测/识别系统 | 研究与系统论文，分别代表文档转写和场景 OCR；尚未精读 |
| NAVER CLOVA | [Donut](https://arxiv.org/abs/2111.15664)、[CLOVA OCR 文档](https://guide.ncloud-docs.com/docs/en/clovaocr-document) | Donut 直接从文档图像生成结构化答案，绕过独立 OCR 引擎；CLOVA OCR 则是文档/证件识别产品 | Donut 是较早且有影响的论文，尚未精读；产品文档只说明公开能力 |
| JD.com 与清华 | [FastOCR 精读](papers/2605.17447-jd-fastocr.md)（[原文](https://arxiv.org/abs/2605.17447)） | 针对文档图像视觉 token 不能被永久丢弃的问题，按解码步骤动态选择注意区域并跨步复用焦点 | v1 已精读 |
| IBM Research | [Docling 技术报告](https://research.ibm.com/publications/docling-technical-report)、[Granite-Docling](https://www.ibm.com/new/announcements/granite-docling-end-to-end-document-conversion) | Docling 是组合版面、表格和 OCR 组件的解析工具链；Granite-Docling 进一步用紧凑 VLM 直接输出结构化文档 | 官方技术报告与产品/模型说明已检索，尚未精读 |
| JPMorgan AI Research | [DocLLM](https://aclanthology.org/2024.acl-long.463/) | 用 OCR 提取的文字框坐标编码版面关系，不依赖视觉编码器，研究表单、收据等视觉文档推理 | ACL 2024 论文，尚未精读 |
| Mistral | [OCR 4 技术介绍](https://mistral.ai/news/ocr-4/) | 产品路线输出文本框、区块类别和置信信息，面向后续搜索与文档工作流；这是厂商发布材料，不是同行评审论文 | 官方产品材料已检索 |
| Upstage | [Document Parse](https://www.upstage.ai/products/document-parse) | 商业解析服务输出 HTML/Markdown、表格和图表结构；现有公开材料主要说明产品能力 | 产品材料已检索，暂未找到足以作为其独立模型研究的公开论文 |
| Google | [Gemini 文档理解说明](https://ai.google.dev/gemini-api/docs/document-processing) | 直接用通用多模态模型读取 PDF 的文本、图表、表格和版式，并支持结构化抽取；文档描述产品能力，不揭示专用 OCR 模型训练机制 | 官方文档已检索 |
| Microsoft | [Azure OCR / Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-ocr)、[模型选择说明](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept/choose-model-feature) | 将 OCR、字段抽取、文档专用模型与生成式内容理解分层提供，体现生产级 IDP 的任务拆分 | 官方文档已检索 |
| Adobe | [Acrobat AI Assistant 文档问答](https://experienceleague.adobe.com/en/docs/document-cloud-learn/acrobat-learning/get-started/ai/ai-assistant) | 以 PDF 阅读、来源定位和多文档问答为产品入口；这说明文档理解应用方向，不等同于公开 OCR 研究 | 官方产品文档已检索 |

阿里至少能确认三条团队/产品线：通义实验室「读光」团队维护 OCR 研究项目，高德 AMAP CV Lab 发布 ABot-OCR，Alibaba Group 的 Logics 团队发布 Logics-Parsing；Qwen OCR 文档则只确认产品能力，不足以据此认定其背后的论文团队。微信也确有腾讯 WXG 工程团队的自研 OCR 公开记录，说明它参与了实际 OCR 研发与产品落地；这篇 2021 年文章不是新模型论文，不能和当前 HunyuanOCR 研究线混为一谈。

其他公司也覆盖了从经典 OCR 到文档 VLM 的不同层次：Amazon 研究 OCR 表征如何补充 VLM，并关注转写的逐字忠实度；Meta 有海量图片 OCR 系统与学术 PDF 转写模型；NAVER 的 Donut 是较早的 OCR-free 文档理解路线；IBM 同时维护解析工具链和紧凑文档 VLM；JD 与清华的 FastOCR 研究如何减少每个生成步骤实际关注的视觉区域。它们不全是近期 OCR 专用模型发布，但都能提供清晰的研究问题或系统路线。

整体上，行业研究不只是在发布“识字模型”：还包括版面和阅读顺序恢复、OCR 文字与视觉信息融合、结构化文档重建、长上下文检索、逐字转写忠实度和解码期计算优化。新增精读覆盖了字节、阿里两支团队、华为、JD/清华和 Amazon 五个研究组织；这些路线的输入、输出和目标任务不同，不能只按“OCR”名称或单个总分横向排名。下一步更值得追问的是，在固定页面集、语言、分辨率、输出协议和计算预算下，布局分解、整页生成和动态注意各自在哪些页面类型上占优；其他产品资料仍只作应用背景，未读论文也保持待精读标记。
