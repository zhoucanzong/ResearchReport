# MiniCPM-OCR：1.3B 只做区域转写，2B 专门判"这段要不要复核"

> 面壁智能（OpenBMB）2026-10-27 开源，Apache-2.0（代码、文档、权重；见仓库 `LICENSE` 与 README 末段）。**没有 arXiv 论文**：2026-10-28 以 `"MiniCPM-OCR" arxiv` 等词检索未见条目，一手材料只有仓库文档与模型卡。依据：仓库 [README](https://github.com/OpenBMB/MiniCPM-OCR) 与 `docs/` 下四份文档（`minicpm_ocr_1dot0_en.md`、`minicpm_ocr_jev_en.md`、`benchmark_reproduction_en.md`、`faq_en.md`，下文以文件名:行号引用）、[MiniCPM-OCR-1.0 模型卡](https://huggingface.co/openbmb/MiniCPM-OCR-1.0)、[Jev 模型卡](https://huggingface.co/openbmb/MiniCPM-OCR-Jev)、[JevOCRBench 数据集卡](https://huggingface.co/datasets/openbmb/JevOCRBench)。证据等级为**官方发布稿/文档**，低于论文级：机制段落有多处是官方自己承认"无材料可证"，本文逐处标出；未独立运行模型、未重算任何指标。

## 先把"系统"和"模型"分开，否则 93.68 会被误读

MiniCPM-OCR 1.0 是 1.3B 的**区域识别器**，不是整页端到端模型。整页解析由 SDK 串起来（`minicpm_ocr_1dot0_en.md:45,53-56`）：PDF 光栅化 → **PP-DocLayoutV3 检测区域与读序并裁剪** → 区域并发送识别服务 → 按读序拼 Markdown，表格 OTSL 转 HTML、公式保留 LaTeX。SDK 与推理服务是两个 Python 环境，可以分机器跑。

这决定了三件事：

1. 榜上的分数是**系统分**：版面与读序由 PP-DocLayoutV3（paddle 生态）提供，不经与 1.3B 模型。讨论"1.3B 能到多少"时必须带这个前提。
2. 模型只回答**短程转写**：输入是按区域类型裁好的图，prompt 也按类型切（`Text/Table/Formula/Seal Recognition:`、`Chart to Table:`，`minicpm_ocr_1dot0_en.md:64-70`）。五类区域共用一个权重，任务靠 prompt 分流。
3. 视觉预算走切片路线：4× 压缩、`scale_resolution` 448、最多 9 切片（模型卡 Architecture 表）；评测侧 `max_slice_nums` 9、`max_model_len` 40960（`benchmark_reproduction_en.md:37-39`）。

## 1.3B 为什么还够用：能证到哪一步

底子是 MiniCPM-V 4.6，组件为 **SigLIP 视觉编码器 + Qwen3.5 语言模型**（`minicpm_ocr_1dot0_en.md:38`）。但"为什么是 1.3B 就够"这件事，官方**明确不给结论**——模型指南里有一行 HTML 注释：初始 checkpoint、原始训练数据、训练阶段"尚未有可核实材料支持，也不据架构名反推"（`:47`）。所以任何"用 XX 数据训出来的"说法都缺一手依据。

能证的只有三条可观察事实：

- **区域级裁剪替代整页长生成**：一页被切成若干区域，每块输出很短。生成长度按区域类型设上限——纯文本 4096、表格 8192、独立公式 2048、行内公式 1024（`benchmark_reproduction_en.md:22-31`）。8192 就是复杂表格的硬天花板。
- **高分辨率靠切片而非单图放大**：`max_slice_nums 9` 让一块区域最多切成 9 片加一张缩略图；`downsample_mode 4x` 压视觉 token。这是"小模型 + 富视觉细节"的常见权衡。
- **"文本为中心"落在可观察的任务面**：官方表述是 text-centric document understanding，覆盖文本、表格、公式、图表、印章 + KIE（`:7`）；KIE 是直接问字段返回 JSON，不走整页 Markdown（`:78-86`）。这是 prompt 层面的证据，不是训练数据层面的证据。

**我们的推断（标为推断）**：短输出把语言模型要承担的推理压得很短，全局版面问题外包给外部布局模型，因此参数量不必大。这条能解释"为什么够用"，但不能证明官方就是这么设计的。

## Jev：把"对不对"改成二元分类

MiniCPM-OCR Jev 2B，从 **Qwen3.5-2B** 训起，保留视觉编码器与语言主干，把语言模型输出头 `lm_head` **换成二分类头**，学"这个候选是否正确"（`minicpm_ocr_jev_en.md:16`）。注意官方紧接着的注释：保留架构**不等于训练时冻结参数**（`:18`）。

输入是**三件套**：区域原裁剪图 + 候选 OCR 文本 + **由该文本渲染出来的图**，外加区域类别（`text`/`formula`/`table`），输出 0–1 分（`:22-29`；数据集卡"Evaluation"段要求三个输入按此顺序）。渲染由服务端完成，SDK 不带渲染器时调用方要自备渲染图。

训练信号是**块级、人工审过**的正确/错误标签；JevOCRBench 负样本取自前沿 OCR 模型的真实错误输出（`minicpm_ocr_jev_en.md:57,65`；数据集卡："Negatives come from real error outputs of frontier OCR models"）。

**为什么 2B 能超过 35B 的通用模型**——最硬的证据是同一张表里的同尺度对照：通用 Qwen3.5-2B 在 JevOCRBench 只有 **50.6**（AUROC×100，≈随机），而 Jev 2B 是 **93.6**（README 的 Jev 结果表图）。同样的 2B 参数，差别只在任务与训练信号，所以这不是"小模型更强"，而是**窄任务 + 专用训练信号**把可分性从近随机拉到 93.6。

**但 README 的口径收窄了两行**：正文只写"超过 JEV-35B-A3B（90.1）、接近 Qwen3.5-397B-A17B（93.8）"（`jev_en.md:11`）。同一张表里还有 **JEV-VL 27B 94.0、Qwen3.7-Plus 94.3、Kimi K3 96.9、Gemini 3.8 Flash 97.1** 都在 Jev 之上。结论应写成"赢同尺度通用 VLM 与 35B 的 JEV，但 27B 的 JEV-VL 仍高 0.4 分"，不能写成"小模型判别 SOTA"。

**推断（标为推断）**：加入"候选文本的渲染图"是关键设计——它把判断题从"这段文字像不像真的"变成"两个视觉结构是否一致"，表格的合并单元格、公式的符号位置在渲染图上更容易对不上；纯文本里也只是给了一个同分布参照。官方未解释动机，只规定输入顺序。

## 三个数字的口径

| 数字 | 基准 | 条件 | 谁测的 | 能不能跨来源比 |
|---|---|---|---|---|
| **93.68** | Real5-OmniDocBench | 复用 **OmniDocBench v1.5 的 GT 与评分**；Scanning/Warping/Screen-Photography/Illumination/Skew 五场景各 1,355 页；综合分 = 五场景 Overall 的**等权平均**（`benchmark_reproduction_en.md:50`） | 官方自测 | 只能与同表 Real5 列比（PaddleOCR-VL-1.6 93.19、Xiaomi-OCR-0 92.73） |
| **96.51** | OmniDocBench v1.6 | `quick_match`；temp 0.01 / top_p 0.001 / top_k 1 / `enable_thinking: false`；4× 压缩、9 切片、`max_model_len` 40960（`:11-39,49`） | 官方自测 | 同表可比；**与 94.74 同类**——94.74 是 HunyuanOCR-1.5 在 v1.6 的自报，本表给同值 |
| **54.7** | OCRBench v2 | 写入 `predict` 字段，`eval_scripts/eval.py` 按任务计分、`get_score.py` 聚合中英（`:53`） | 官方自测 | 仅同表 |
| **93.6** | JevOCRBench | 2,267 条中英块级样本，AUROC×100；作者自建集（数据集卡） | 官方自测 | 仅该表 |

任何文档解析综合分都要先看定义：`Overall = ((1 - TextEdit) × 100 + FormulaCDM + TableTEDS) / 3`（`benchmark_reproduction_en.md:61`）——三项等权、不含读序，所以它既不是字符准确率，也不能单独归因于识别或版面。

**两处必须纠正的地方**（都是官方自家材料内部不一致）：

1. **"v1.6 与 olmOCR 领先"站不住**。指南写"在 OmniDocBench v1.6、Real5、Wild、olmOCR-Bench 上综合表现最高"（`minicpm_ocr_1dot0_en.md:124`），但自家完整结果图里 v1.6 是 96.51，低于 **TeleOCR 96.91、Xiaomi-OCR-0 96.83、Ovis-OCR2 96.58**；olmOCR-Bench 82.7，低于 **chandra-ocr-2 85.8、LightOnOCR-3-1B 84.5、Surya OCR 2 83.3**。真正在比选集合中最高的是 **Real5 93.68、Wild 92.39、CHAOS-Bench 29.78、OCRBench v2 54.7** 四列。若"领先"指某个未声明的开源子集，文档没说。
2. **93.68 与 94.74 不是同一把尺**。前者是 Real5（v1.5 GT，五场景平均），后者是 OmniDocBench v1.6；同表可见 1.0 的 v1.6 是 96.51。把 93.68 和 [HunyuanOCR-1.5 精读](2607.04884-hunyuan-ocr-15.md) 的 94.74 并表相减是错的；要同基准比就用 v1.6：**96.51 vs 94.74**。

跨模型列的数字**来源未说明**：文档没有写对手分数是自己重跑还是转引论文（HunyuanOCR-1.5 的 94.74 与论文自报完全一致，倾向于转引）。这一列按"作者汇编"读，不能当独立复现。

## DSpark 与那个 55%

DSpark 是**主模型 + 配套草稿模型（sampling head）**的推测解码组合；权重表里主模型与 DSpark head 分开发布，官方强调"两者必须同发布批次配套，不能混用"（`minicpm_ocr_1dot0_en.md:99`；模型卡"Related checkpoints"段）。普通解码不需要草稿模型。

**55% 的条件是官方自己承认不完整的**：文档只规定"比 DSpark 与不启用 DSpark，必须同主权重、同数据集、同硬件、同 SDK 配置，只切 DSpark 开关"，随后写"完整的对比命令与日志仍待补充"（`benchmark_reproduction_en.md:112`），且强调这 55% 只描述 DSpark 的收益、不能替代与其他系统的吞吐比较（`:116`）。所以 55% 只能作为官方声明引用，复现路径目前不存在。

**吞吐数字是可自查的**：1.217 pages/s（RTX 5090、全部 1,651 张图、**图级**并发 1、各系统开加速配置，`minicpm_ocr_1dot0_en.md:151,157-173`）。表内 1.49× PaddleOCR-VL-1.6 = 1.217/0.818，3.62× MinerU2.5-Pro = 1.217/0.336，两处都对得上。注意"图级并发 1"不等于页内串行——页内区域仍并发，这是它吞吐高的一半原因（`benchmark_reproduction_en.md:105`）。

顺带一句与库内条目的关系：DSpark 与 [HunyuanOCR-1.5 精读](2607.04884-hunyuan-ocr-15.md) 的 DFlash 是同一路线（草稿模型加速 OCR 长输出），但**口径不同不可相减**——DFlash 报的是 vLLM 下单请求延迟 2.14×（3.032→1.408 秒/页），DSpark 报的是端到端效率 +55%。

## 与库内两篇怎么摆

| 场景 | 更合适 | 依据 |
|---|---|---|
| 单页/多栏/表格公式精度（同基准同表） | **MiniCPM-OCR 1.0** | OmniDocBench v1.6 **96.51** vs HunyuanOCR-1.5 94.74、Unlimited-OCR2 94.02、MinerU2.5-Pro 95.75（同一张 OpenBMB 结果图） |
| 多语言长尾（149 语种、古文字） | **HunyuanOCR-1.5** | [HunyuanOCR-1.5 精读](2607.04884-hunyuan-ocr-15.md)；MiniCPM 官方只声明中英，其他语言要 SFT |
| 超长文档（40+ 页连续、恒定 KV cache） | **Unlimited OCR** | [Unlimited OCR 精读](2606.23050-unlimited-ocr.md)；MiniCPM 按区域识别、页间无状态，也没有长文档实验 |
| 批量吞吐（同表同硬件） | **MiniCPM-OCR 1.0** | 1.217 vs Unlimited-OCR2 0.246 pages/s（同表 RTX 5090 条件），约 4.9× |
| 判断"哪些区域要人复核" | **Jev** | 库内无同类条目；它不取代解析模型，只在候选之间打分 |

MiniCPM 的定位可以概括为"**把长序列生成的责任拆走**"：版面交给 PP-DocLayoutV3、区域输出压在 1k–8k token、页内并发拉吞吐。代价是系统复杂度（两个环境、布局模型依赖 `pypdfium2` 与 paddle，见 `faq_en.md:130-131`）与页间无状态。

## 失效边界

- **语言**：官方只声明中英文（`minicpm_ocr_1dot0_en.md:43`）。官方给的法语教程是**手写文本行 SFT 示例**（README Fine-Tuning 段），反证开箱不支持更多语言。
- **Wild 场景需要旋转校正**：报告的 Wild 分数是**经 SDK 旋转校正后**的结果，原始图与校正图被当作两个 track 分别归档（`benchmark_reproduction_en.md:51,89`）。不加预处理直接拍的照片，对应的是较低的那一列。
- **复现材料不全**：评估脚本、精确版本、计时边界"仍待补充"（`:5`）；55% 的复现命令与日志同样缺失（`:112`）。
- **超长输入**：`max_model_len` 40960，区域生成上限见上表；输出被截断时 `finish_reason` 会是 `length`（`minicpm_ocr_1dot0_en.md:72`）。OOM 时官方建议降到 16384（`faq_en.md:124`）。
- **Jev 的三条使用边界**：AUROC 高**不等于**可以直接选阈值，官方明确"现有 AUROC 结果不支持任何通用默认阈值"，必须用本域样本标定（`jev_en.md:83`）；它只能在**已有候选**里挑，最终质量受候选覆盖限制（`:47`）；返回里只有 `verdict == scored` 才是模型分，`precheck`/渲染/前向失败返回的是**固定值**，不能当"低分"处理（`:107`）——这条在流水线里最容易出错。
- **许可要分开看**：仓库、两份权重与文档均 Apache-2.0；但 **JevOCRBench 是 `license: other`**——因为数据取自 OmniDocBench（上游研究用途、非商用）、Real5 与 olmOCR-Bench，数据集卡明确写了派生材料的条款各自延续。用 Jev 做商用评估前先读 `DATA_LICENSE.md`。
- **未能确证**：训练数据构成与训练阶段；竖排、低质扫描、手写各自的量化表现（官方只有"示例里包含手写"这类展示，没有分项分数）；对手列数字的来源（转引或重跑）；DSpark 55% 的复现条件。

## 读法

先读 `minicpm_ocr_1dot0_en.md` 的流水线四步（`:53-56`）与区域 prompt 表（`:64-70`），把"系统分"的来源固定下来；再打开完整结果图（`assets/minicpm-ocr/ocr-benchmarks.png`）逐列看，别只读正文那三个数字——v1.6 与 olmOCR 两列的排名和正文说法不一致，就在这张图上；然后读 `minicpm_ocr_jev_en.md` 的三件套输入（`:22-29`）与阈值章节（`:75-83`）；最后回到 `benchmark_reproduction_en.md` 的 Settings 表，任何跨系统比较都从那张表开始读，先确认并发、硬件、GT 版本与综合分定义。
