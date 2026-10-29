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
| 一页文档如何拆成区域、恢复顺序并识别内容 | [PaddleOCR-VL](papers/2510.14528-paddleocr-vl.md) → [Dolphin](papers/2505.14059-bytedance-dolphin.md)；同骨架换解码策略（外置版面 + 多 token 预测）见 [GLM-OCR](papers/2603.10910-glm-ocr.md)；把版面分析做成可选"思维"阶段的端到端做法见 [Qianfan-OCR](papers/2603.13398-qianfan-ocr.md) |
| 高分辨率、视觉压缩和解码预算如何取舍 | [DeepSeek-OCR](papers/2510.18234-deepseek-ocr.md) → [DeepSeek-OCR 2](papers/2601.20552-deepseek-ocr2.md)，再对照 [Coarse-to-Fine](papers/2603.24326-coarse-to-fine.md)、[FastOCR](papers/2605.17447-jd-fastocr.md)；长时程解码见 [Unlimited OCR](papers/2606.23050-unlimited-ocr.md)；按区域类型提示做短程转写、并用专用 draft head 加速见 [MiniCPM-OCR](papers/20261027-minicpm-ocr.md) |
| 数据和奖励怎样教会模型输出文档结构 | [FireRed-OCR](papers/2603.01840-firered-ocr.md)、[Logics-Parsing](papers/2509.19760-alibaba-logics-parsing.md)、[ABot-OCR](papers/2605.27978-amap-abot-ocr.md)；[HunyuanOCR](papers/2511.19575-hunyuan-ocr.md)与 [1.5](papers/2607.04884-hunyuan-ocr-15.md)展示后续演进；把增益全押在数据与分阶段训练上见 [MinerU2.5-Pro](papers/2604.04771-mineru2-5-pro.md)，文本锚定预训练 + 混合任务 RL 见 [Xiaomi-OCR-0](papers/2609.36136-xiaomi-ocr-0.md) |
| 指标、语言、拍摄条件与逐字忠实度怎样影响结论 | [OmniDocBench](papers/2412.07626-omnidocbench.md) → [MDPBench](papers/2603.28130-mdpbench.md) → [FaithC4](papers/2607.21617-amazon-faithc4.md)；v1.6 的 MGAM 匹配与 Base/Hard/Full 三层协议由 [MinerU2.5-Pro](papers/2604.04771-mineru2-5-pro.md) 定义，引用 v1.6 分数前先读其 §5 |
| 图表结构和多文档证据怎样成为下游可用信息 | [Multimodal OCR / dots.mocr](papers/2603.13032-multimodal-ocr.md)、[Doc-Researcher](papers/2510.21603-huawei-doc-researcher.md) |
| 不换解析器时，怎样自动判断这份 OCR 结果准不准 | [JEV 判别线](papers/jev-decision-line.md)（判别模型与解析器的分工、概率如何进阈值策略）→ 同思路的小模型实例见 [MiniCPM-OCR Jev](papers/20261027-minicpm-ocr.md) |

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

## 路线分歧的核心：结构信息放在哪里

“端到端”与“模块化”不是唯一的架构选择。更有解释力的问题是：页面结构由独立模型预测、由同一个模型写成中间表示，还是只在训练奖励里作为目标约束？三种做法把错误和计算成本放在不同位置。

- **独立版面阶段：PaddleOCR-VL。** PP-DocLayoutV2 先用检测器找元素，再用 pointer network 预测元素间阅读顺序；VLM 接收裁剪区域并识别内容。显式的框、类别和顺序使错序、漏检相对容易定位，也避免把整页都变成很长的生成输入。代价是检测与顺序阶段成为硬接口：上游漏掉元素，后级没有机会恢复；两阶段输出还需可靠地合并为 Markdown/JSON。[PaddleOCR-VL 精读](papers/2510.14528-paddleocr-vl.md)，§2.1.1–2.1.2、Fig. 2–4
- **模型内锚点：Dolphin。** 同一个 encoder-decoder VLM 先生成带类别、坐标和阅读顺序的元素序列，再把这些序列作为异构锚点，以元素类型提示并行解析裁剪内容。它在“多个专用模型”和“整页一次性生成”之间折中：共享权重保留跨模态特征，而第一阶段输出提供了显式结构，第二阶段降低了每次识别所需的页面上下文。错误仍可能在锚点阶段固化；裁剪也可能切断图注、跨栏或表格与正文之间的关系。[Dolphin 精读](papers/2505.14059-bytedance-dolphin.md)，§3.1–3.3、Fig. 2
- **结构奖励：Logics-Parsing。** 它保留单一 LVLM 输出 HTML 的路径，却在 SFT 后增加 layout-centric RL。作者的理由是 next-token 交叉熵只逐 token 对齐标签，未直接表达段落阅读顺序或框坐标差错的严重度；RL 阶段将输出解析成文字、框与段落顺序，分别用字符相似度、定位准确度和 pairwise order inversion 组成奖励。训练用约 8,000 个由 SFT 错误挖掘出的难例，减少 RL 计算集中在已容易样本上的浪费。它免去了独立检测器，但 reward 的归一化、权重和解析器共同定义了“结构正确”，不等于有独立人工真值。[Logics-Parsing 技术报告](https://arxiv.org/html/2509.19760)，§2.2–2.4、§3.1–3.3

这三种路线的区别不是“旧 OCR”到“新 VLM”的单向替代：它们分别把结构约束放在**前置模块**、**可见的中间序列**和**训练时奖励**中。显式阶段利于定位错误和扩展元素类型，但造成串联依赖；模型内锚点在共享表示和并行识别间折中，但锚点错误会向后传播；奖励直接优化输出属性，却需要可信的解析与奖励函数，并可能让模型迎合代理指标。

DeepSeek-OCR 则以不同目标组织架构：重点不是怎样重建页面树，而是“给定有限视觉 token，文字还可解码到什么程度”。DeepEncoder 将局部感知、全局语义与 token 压缩串联，后接 MoE 解码器；论文在 Fox 基准研究文本 token/视觉 token 比率与 OCR 精度，显示压缩继续增大时识别精度会下降。这个实验把视觉 token 视作上下文压缩预算的证据，不能替代对阅读顺序、表格关系或复杂页面结构的评估。[DeepSeek-OCR 精读](papers/2510.18234-deepseek-ocr.md)，§3.1–3.3、§4.1–4.2

从评测角度看，LogicsParsingBench 在其 1,078 页测试集上把文字、公式、表格、阅读顺序和化学结构拆开，作者报告 Logics-Parsing 在多项指标上表现领先；这能支持其特定复杂布局目标下的结果，不能证明 RL 优于模块化检测，因为模型、数据、评测集和训练预算并未被统一控制。需要回答“哪条路线最好”时，必须固定输入页、分辨率/token预算、输出结构、训练数据和计算成本，再同时观察页面级与元素级错误。[Logics-Parsing §3.1–3.3]

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

一个具体例子说明“同名基准”也可能换了尺子：OmniDocBench v1.6 不是官方仓库的补丁版，而是 [MinerU2.5-Pro](papers/2604.04771-mineru2-5-pro.md) 提出的协议——用多粒度自适应匹配（MGAM）消除“语义正确但切分粒度不同”的扣分，并新增 296 页 Hard 子集，形成 Base 1,355 / Hard 296 / Full 1,651 三层（§5）。两件事方向相反：匹配放宽会抬分，加入难样本会压分，所以 v1.5 与 v1.6 的分数不能相减成“提升”。引用 v1.6 分数时必须写层，并注意第三方汇总表里的对手列可能混用自报数与重跑数（如 Xiaomi-OCR-0 的 Real5 自报 95.24、第三方重跑 92.73）。

这些论文展示了文档解析从识别单个字符走向结构恢复、从整页密集编码走向元素选择，以及从规整数字页面走向多语言实拍测试的几条研究线。还缺少跨系统、同页集、统一分辨率/token预算和可审计失败分母的控制比较；本专题没有运行模型或基准，也不据此判定哪种架构总体最佳。

## 哪些团队也在做 OCR 与文档解析

这里列的是截至 2026-10-28 能找到的一手公开证据代表，不是厂商普查或性能榜。研究论文和产品文档回答的问题不同：前者能读方法、数据和实验条件；后者主要说明可用能力与接口，不能据此推断内部模型机制。

| 团队 | 可追溯的一手材料 | 研究问题/路线 | 阅读状态 |
|---|---|---|---|
| 百度 PaddleOCR | [PaddleOCR-VL](papers/2510.14528-paddleocr-vl.md)、[PaddleOCR 3.0 技术报告](https://arxiv.org/abs/2507.05595) | 传统 OCR、版面分析与小型 VLM 逐步整合；布局检测先行，再识别文本、表格、公式等元素 | PaddleOCR-VL 已精读；报告摘要与题录已核 |
| 上海人工智能实验室 / OpenDataLab | [MinerU2.5-Pro 精读](papers/2604.04771-mineru2-5-pro.md)（[原文 v2](https://arxiv.org/abs/2604.04771v2)） | 1.2B 解耦架构不动，只做数据引擎与三阶段训练；同时提出 OmniDocBench v1.6 的 MGAM 匹配与 Base/Hard/Full 三层协议 | v2 已精读 |
| 百度千帆 | [Qianfan-OCR 精读](papers/2603.13398-qianfan-ocr.md)、[原文](https://arxiv.org/abs/2603.13398) | 单个端到端模型联合文档解析和理解；可选的 Layout-as-Thought 阶段先输出框、类别和阅读顺序，再出正文 | v1 已精读 |
| 字节跳动 | [Dolphin 精读](papers/2505.14059-bytedance-dolphin.md)（[原文](https://arxiv.org/abs/2505.14059)） | “先分析、后解析”：先生成带阅读顺序的异构版面锚点，再并行识别各区域，尝试在整页生成和多专家流水线间折中 | v1 已精读 |
| 阿里巴巴通义实验室「读光」OCR Team | [Advanced Literate Machinery 官方仓库](https://github.com/AlibabaResearch/AdvancedLiterateMachinery) | 仓库明确由通义实验室语言技术实验室 OCR Team 维护，汇集文档理解、Platypus 通用文字识别和 CC-OCR 评测等公开项目 | 已核对团队归属和项目入口，具体论文尚未精读 |
| 阿里巴巴 Logics Team / Qwen 产品 | [Logics-Parsing 精读](papers/2509.19760-alibaba-logics-parsing.md)（[原文](https://arxiv.org/abs/2509.19760)）、[Qwen OCR 文档](https://docs.modelstudio.console.alibabacloud.com/zh/model-studio/qwen-vl-ocr) | Logics-Parsing 用布局感知奖励训练端到端解析；Qwen OCR 文档说明有专门产品接口，但不公开足够细节来替代论文 | Logics-Parsing v1 已精读；产品文档只作产品证据 |
| 阿里巴巴高德 AMAP CV Lab | [ABot-OCR 精读](papers/2605.27978-amap-abot-ocr.md)（[原文](https://arxiv.org/abs/2605.27978)）、[官方代码仓库](https://github.com/amap-cvlab/ABot-OCR) | 2B VLM 从页面直接生成 Markdown；训练先分阶段建立文字、公式、表格与布局能力，再用感知奖励和结构奖励优化输出 | v1 已精读 |
| DeepSeek | [DeepSeek-OCR](papers/2510.18234-deepseek-ocr.md)、[DeepSeek-OCR 2](papers/2601.20552-deepseek-ocr2.md) | 把页面视觉编码作为上下文压缩路径；第二版改变视觉 token 的顺序建模，关注长文档解析与生成效率的关系 | 两篇已精读 |
| 小红书 | [FireRed-OCR](papers/2603.01840-firered-ocr.md)、[Multimodal OCR / dots.mocr](papers/2603.13032-multimodal-ocr.md) | 一条路线把通用 VLM 专门化为文档解析器；另一条把图表、示意图等图形也变成可解析的结构内容 | 两篇已精读 |
| 腾讯混元 | [HunyuanOCR](papers/2511.19575-hunyuan-ocr.md)、[HunyuanOCR-1.5](papers/2607.04884-hunyuan-ocr-15.md) | 以小型端到端 OCR VLM 统一识别、结构解析和语义抽取；后续报告进一步讨论训练与推理加速 | 两篇已精读 |
| 腾讯微信 WXG | [微信 OCR 图片文字提取技术介绍](https://developer.cloud.tencent.com/article/1798403) | WXG 工程师明确称微信客户端长按提取文字使用微信自研 OCR；文章描述文字存在性/语种检测、文本图像分类、通用或垂类识别，再做版面重排 | 2021 年工程文章，非近期论文；直接证明微信团队有 OCR 研发与产品实践，不能代表当前模型结构 |
| 面壁智能 OpenBMB | [MiniCPM-OCR 精读](papers/20261027-minicpm-ocr.md)（[仓库](https://github.com/OpenBMB/MiniCPM-OCR)、[1.0 模型卡](https://huggingface.co/openbmb/MiniCPM-OCR-1.0)、[Jev 模型卡](https://huggingface.co/openbmb/MiniCPM-OCR-Jev)、[DSpark 草稿头](https://huggingface.co/openbmb/MiniCPM-OCR-1.0-DSpark)） | 1.3B 只做**区域识别**（版面与读序由外置 PP-DocLayoutV3 提供，故 93.68 是系统分）；2B Jev 把"这段识别对不对"做成**二分类头**；另有 **≈0.3B DSpark 推测解码草稿头**（5 层、每前向 15 token、草稿词表裁至 114,688，必须配 1.0 用），官方 +55% 效率来自这条 draft 路径 | 官方发布稿级（无 arXiv）；1.0、Jev、DSpark 与量化形态均已整理 |
| 智谱 | [GLM-OCR 精读](papers/2603.10910-glm-ocr.md)（[原文 v2](https://arxiv.org/abs/2603.10910)） | 0.4B CogViT + 0.5B GLM 解码器，外置 PP-DocLayout-V3 两阶段；MTP 用共享参数多头，训 10 token/步、推理约 5.2 | v2 已精读 |
| 小米 | [Xiaomi-OCR-0 精读](papers/2609.36136-xiaomi-ocr-0.md)（[原文](https://arxiv.org/abs/2609.36136)） | 0.8B 从 Qwen3.5-0.8B 起，Q-Mask 文本锚定 + CPT + Mix-RL；同一套权重同训解析与 OCR 理解，版面仍外置 | v1 已精读 |
| AutoTrust（JEV 系列） | [JEV 判别线](papers/jev-decision-line.md)（[官方模型卡 JEV-35B](https://huggingface.co/autotrust/JEV-35B)） | 不做解析，做判别：把“问题 + 至多 256 个候选”压成一次前向的概率分布，用按类型标定的温度出概率，用于解析结果质检与多解析器仲裁 | 判别线已整理；无 arXiv 论文可确证，证据等级为官方发布稿 |
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

整体上，这不是一个“哪个 OCR 模型总分最高”的单一竞赛，而是几条互相连接的研究轴：布局结构由外置检测器、模型内锚点还是训练奖励承担；视觉预算是整页投入还是按区域/解码步动态分配；数据与奖励怎样影响结构正确性；最后，解析置信度怎样进入人工复核或下游问答。近期精读已覆盖字节、阿里多个团队、华为、百度、面壁、智谱、小米、JD/清华等不同路线，但它们的输入、输出和评测条件并不统一。下一步更有价值的比较是在固定页面集、语言、分辨率、输出协议和计算预算下，观察布局分解、端到端生成与动态注意分别在哪些页面类型上奏效；产品文档和未精读论文仍只作为来源线索，不与论文证据混排。
