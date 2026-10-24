---
display_name: 神经活动表征与解码
type: research
domain: AI4Science
subject: Neuroscience
date: 2026-10-23
evidence: fixed-primary-papers
status: completed
---

# 神经活动到运动行为：跨记录会话的表征与解码

> **范围**：聚焦侵入式皮层电生理中一个具体问题：每次记录得到不同神经元集合时，模型能否把群体脉冲活动映射到运动行为，并迁移到未参与模型训练的记录会话、个体或物种？本文比较多会话预训练 NDT2、配对神经—行为的大规模解码器 NDT3，以及以行为事件切分群体状态的 TWS。范围不包含 EEG/fMRI 全景、语言解码、脑疾病诊断或通用神经回路建模。

## 先给判断

目前的关键障碍不只是数据量，而是**不同会话里“一个神经 token 指什么”**。NDT2 和 NDT3 用时间分箱与神经元/电极 patch 构造序列，并通过实验情境嵌入、通道映射或目标会话微调适应分布差异。TWS 提出另一个方案：以任务事件之间的群体活动几何作为 token，丢掉神经元身份；它在 2026 年 10 月的 arXiv v1 中报告了跨会话与跨数据集行为解码结果。

证据支持三个有限结论：

1. **预训练能减少目标行为数据需求，但收益有条件。** NDT2 的多会话自监督预训练提高新上下文拟合并能做小样本/无监督适配；NDT3 在 8 个运动任务、约 2,000 小时预训练数据的评测中，目标任务数据少于约 1.5 小时最容易看见收益，目标数据增加后从头训练与预训练差距趋近。跨个体的“泛化”仍通常包含目标数据微调。
2. **token 化和数据划分决定迁移结论。** NDT3 明确发现通道维度/patch 顺序变化会破坏迁移；TWS 在其 IBL 评测里强调不使用 held-out 会话标签，但试验边界会泄露部分标签信息。它的 IBL movement 标签由首动时间定义，而仅用该时间就得到 MCC 0.908；在去掉边界信息或跨到其他任务的对照中，神经表征才更能单独接受检验。
3. **这些模型是预测器与表征学习器，不是因果回路发现工具。** 它们拟合的是特定实验设置下的神经活动—行为关系。潜空间中可解码的行为或跨数据集迁移，既没有识别哪条生物回路产生行为，也没有证明改变该回路会改变行为。

因此，研究问题宜从“做一个统一大脑模型”缩小为：**哪些不依赖神经元身份的群体统计量，能在神经元周转后仍保留可迁移的行为信息；行为事件先验在什么任务下有帮助，又何时造成目标泄漏？**

## 先分清四种主张

| 主张 | 这组论文实际提供的证据 | 尚不能推出 |
| :-- | :-- | :-- |
| 表征 | NDT2 的掩码重建表示、NDT3 的时空 patch 表示、TWS 的每个行为 regime 群体几何 token；可用神经重建或行为线性探针检查 | 表征等于真实脑回路、单神经元功能或生物学因果变量 |
| 预测 | 给定一段神经活动预测运动学、反应时间、选择或运动状态；在特定 held-out 轴、指标和数据量下比较分数 | 未见实验室、传感器、任务、行为范围全都泛化，或在线临床有效 |
| 因果 | 本文三条主线均没有做随机化神经干预或正式因果识别 | “神经活动预测行为”不等于估计神经活动对行为的因果效应 |
| 生物发现 | TWS 检验哪些行为变量跨随机神经元子集仍可解码，属于关于信息可迁移性的分析 | 找到承载行为的细胞类型、突触连接、调控路径或可操纵机制 |

若要声称回路发现，至少还需要明确干预目标、反事实/识别假设、时间与空间特异性，以及刺激、抑制、病灶或救援实验等正交验证；本文中的 decoder 指标不满足这些条件。

## 问题机制：跨会话变动为何难

皮层电极记录不是对同一批神经元的稳定连续采样。探针重新插入、阻抗变化、单元分选和电极阵列位置都会改变可见神经元及其排序。于是，一个按“第 17 个单元”学习到的嵌入可能只对应训练会话中的那个单元；对新会话，它可能指向完全不同的信号。

另一方面，并非所有行为变量都以同一种方式分布在神经群体里。TWS 论文把变量操作性分成两类：Type A 是换一批神经元后群体统计仍保留较多解码信息的变量；Type B 是解码方向随会话变化、丢失身份后不保证保留的变量。论文在 IBL 数据中比较随机神经元两半的可解码性：movement 跨半群体指标为 0.59，choice 为 0.25；Gallego macaque reach direction 只有 0.12。该指标是“身份无关摘要保留了多少原可解码信号”的比率，不是目标在个体内有多强，也不能说明单个细胞不重要。[TWS §3.1、Appendix E Table 5](https://arxiv.org/html/2610.03001v1)

| 变量 / 数据 | 全神经元 MCC | 随机半群体统计 MCC | 保留比例 | 解释边界 |
| :-- | --: | --: | --: | :-- |
| IBL movement | 0.524 | 0.308 | 0.59 | 具有较强跨神经元群体信息；该实验的行为标签还受事件时间定义影响 |
| IBL choice | 0.624 | 0.155 | 0.25 | 去掉神经元身份后信息损失较多 |
| NLB movement | 0.663 | 0.234 | 0.35 | 部分群体信息保留；NLB 伪会话共享神经元，不能把它当跨真实会话证据 |
| Gallego reach direction | 0.952 | 0.112 | 0.12 | 个体内全神经元容易解码，但 identity-free 跨群体方向很弱 |

这个差异解释了为何统一 token 可能迁移某些状态或运动变量，却未必能迁移选择、方向等所有行为。任务定义、动物、阵列、神经元采样和评价切分都决定了所谓的“可迁移”。

## 三种建模路线

### NDT2：先学脉冲序列，再用新上下文校准

NDT2 是 NeurIPS 2023 的多上下文脉冲序列 Transformer。它在同一掩码自编码框架下，以时空注意力、情境嵌入和非对称 encoder-decoder 处理上下文差异；目标包括神经脉冲重建与运动学解码。论文测试跨会话、跨受试者和跨任务数据的预训练价值。[论文 §3、Fig. 2–4](https://papers.neurips.cc/paper_files/paper/2023/file/fe51de4e7baf52e743b679e3bdba7905-Paper-Conference.pdf)

它的重要设计不是假设所有记录已经同分布，而是把“上下文”显式作为输入，并检验相关数据与远距数据的迁移差异。NDT2 在 sorted RTT 脉冲实验中报告，预训练模型优于单会话和 rEFH 基线；混合跨受试者数据也能带来收益，跨任务数据还可进一步改善。unsorted、具有同一受试者电极物理位置的设置达到超过 0.7 的运动学 R²，作者同时提醒 sorted/unsorted 设置的输入和 split 不同。[§4.1、Fig. 3](https://papers.neurips.cc/paper_files/paper/2023/file/fe51de4e7baf52e743b679e3bdba7905-Paper-Conference.pdf)

论文展示一名 iBCI 使用者的在线 cursor-control proof of principle，但具体结果要求仔细读：在有监督 calibration 数据时，线性 OLE 控制优于 NDT2；作者解释离线到在线的分布差异会暴露脉冲式 “pulsar” 失败模式，并提出闭环调整或开环增强作为后续方向。[§4.4、§5](https://papers.neurips.cc/paper_files/paper/2023/file/fe51de4e7baf52e743b679e3bdba7905-Paper-Conference.pdf)

所以 NDT2 证明的是：规模不大的跨上下文预训练可以成为下游解码初始化，并能参与实时控制原型；它没有证明无需校准即可跨记录日或跨个体直接工作，也没有证明自监督表示就是生物机制。官方实现还显式支持 session、subject、task、array embedding，和之后“去掉 identity、寻找公共 token”的路线形成可判定差异。[代码 `model.py` 中 `bind_io`：会话/受试者/任务嵌入，约 L171–258；固定仓库版本见 MANIFEST](https://github.com/joel99/context_general_bci)

### NDT3：把神经与行为放进同一自回归序列

NDT3 将问题从“只预训练脉冲活动”扩展到成对的脉冲与行为协变量：每 20 ms 统计脉冲，通常每 32 通道组成空间 patch；行为变量逐维作为 token，同一因果 Transformer 预测序列。预训练可含运动学、EMG、力、iBCI phase/return 等信息；推理时移除辅助 token，并遮蔽行为输入，输出行为预测。[NeurIPS 2025 §2、Fig. 2](https://papers.neurips.cc/paper_files/paper/2025/file/a00000e6a2208172700510bcd69d48e9-Paper-Conference.pdf)

数据量写作“约 2,000 小时”，正文说明原始总量约 1,750 小时后四舍五入；数据来自 30 多只猴和人类 iBCI 的多种运动任务。论文在 8 个 motor datasets 上评测，并以 held-out subject 作为主要外推轴：所有下游猴子都未进入预训练；少于 2k 小时模型的人类受试者也留出，但最大数据模型有人类预训练重叠，作者报告该重叠并分析未发现它带来优势。[§2.1–2.3、Appendix A.2.5](https://papers.neurips.cc/paper_files/paper/2025/file/a00000e6a2208172700510bcd69d48e9-Paper-Conference.pdf)

论文的汇总结论是，在目标数据约少于 1.5 小时时预训练更可能提升解码；高于该范围，预训练与从头训练差距消失。要把预训练数据从 200 h 扩到约 2,000 h，也需要模型从 45M 增至 350M 参数，否则异质数据可能干扰目标任务。训练 2k h、350M 模型约需 20,000 A100 GPU 小时。[§3.1、Fig. 3](https://papers.neurips.cc/paper_files/paper/2025/file/a00000e6a2208172700510bcd69d48e9-Paper-Conference.pdf)

更关键的是，NDT3 自己报告了泛化失败：通道顺序、输入维度或 token 组成变化会损害迁移；在一个 8 方向等长用力任务中，训练只见 3 个方向、测试留 5 个方向时，预训练没有解决角度外推，预测仍趋向最近的训练方向。线性 Wiener Filter 在降维后反而可以在展示条件下粗略外推。[§3.2、Fig. 4](https://papers.neurips.cc/paper_files/paper/2025/file/a00000e6a2208172700510bcd69d48e9-Paper-Conference.pdf)

实现代码也能看见这种取舍：脉冲数据先由任务管线编码，再和其他 modality 按时间、空间位置打包排序送入 Transformer；新增数据集仍需要登记 context、task、subject、配置和预处理。开源仓库说明实验配置需连同 checkpoint/W&B 记录读取，且提示某些较新 commit 存在复现回退。因此，复现和迁移依赖预处理、模型配置与代码状态，不只是下载权重。[代码 `model.py`、`ndt3_slim.py`、README 和 `model_card.md`；commit 见 MANIFEST](https://github.com/joel99/ndt3)

### TWS：以行为事件间的群体几何做 token

TWS（Tokenization with States）是 2026-10-02 发布的 arXiv v1。对每个 trial，它在已记录的事件（如 stimulus onset、movement onset）附近学习共享边界偏移，把 trial 分为 `K=3` 个 regime；每个 regime 中先对单元活动做时间加权摘要，再以跨单元共享的 attention 和 Gram–Schmidt 产生 2 个维度为 256 的向量。每条 trial 因而得到 6 个不依赖神经元排序的 token，输入 backbone 与行为探针。[§3.1–3.2、Algorithm 1、Fig. 1](https://arxiv.org/html/2610.03001v1)

这一路线把泛化假设放在输入单位上：同一行为 regime 中群体活动形成低维几何，不同会话即使记录了不同细胞，也可能拥有可比较的分布式状态。它不是显式拟合神经元对应关系，省掉每会话 unit alignment；代价是必须拥有任务事件时间，并把 regime 内的时间顺序压缩掉。作者把适用对象限定为可事件化的受控电生理实验，而非自由行为自动发现状态。[§1、§2、§3.2](https://arxiv.org/html/2610.03001v1)

IBL Brain Wide Map 评测含 243 个 Neuropixels sessions、109 只小鼠；每个 held-out IBL 模型测试 53 个会话（49 随机留出、4 个 NEDS test sessions），TWS 训练时排除这些 session。跨会话评估使用冻结表征，在其他会话拟合 Ridge probe，不给 test session 行为标签；不过无标签神经样本用于每会话 z-score，连续目标还按每个 session 统计量标准化。文章报告 TWS from scratch 对 IBL movement 的 MCC 为 0.565 ± 0.006，RT 的 R² 为 0.402 ± 0.003（5 seeds）。[§4.1–4.2、Table 1](https://arxiv.org/html/2610.03001v1)

这组数字必须与事件时间基线同读。IBL 的 movement 定义是 stimulus 后 2 秒内是否发生首动；同一首动边界单独解码 movement 的 MCC 为 0.908，RT 的 R² 为 0.443。作者进一步指出，TWS 对 movement/RT 在多数 held-out sessions 并未显著超过事件时间本身。因此 IBL 的高 movement 分数不能作为神经信号改善的独立证明。[§4.3、Appendix V、Appendix Y Table 27](https://arxiv.org/html/2610.03001v1)

更直接检验神经活动的结果来自跨数据集任务：IBL 训练表征冻结后，仅训练线性 probe。对 Gallego macaque/Utah array reach direction（边界时间本身 MCC 0.010），TWS from scratch 报告 MCC 为 0.232 ± 0.010；随机初始化为 0.128 ± 0.002，aligned PCA 为 0.090。此迁移仍然让目标数据的其他 sessions 及标签用于训练 probe，因此可称“冻结表征的跨数据集迁移”，不能称零样本行为预测。NLB 有共享神经元的伪会话，不能提供独立的跨会话验证。[§4.5、Table 4；Appendix V Table 23](https://arxiv.org/html/2610.03001v1)

TWS 的额外机制证据来自边界消融：边界整体偏移 100/200 ms 会降低 movement 解码；以每 trial 固定/随机分割会更大幅降低。另一方面，时间顺序打乱后自监督预训练迁移不降，提示这一配置中 regime 内时间动态未被证明是主要增益来源；效果可能更多来自事件边界与分布式群体摘要。[§4.3、Appendix U、Appendix W](https://arxiv.org/html/2610.03001v1)

## 比较时不能混成一个排行榜

| 维度 | NDT2 | NDT3 | TWS |
| :-- | :-- | :-- | :-- |
| 研究对象 | 多上下文脉冲建模与 motor decoding | 多物种/多任务 motor decoder | 事件 regime 间群体状态表征与跨 session probe |
| 神经 token | 20ms 脉冲 patch；context / neuron 信息保留 | 20ms 脉冲 patch，通常 32 channels；配对行为 token | 事件切段后每 regime 的 order-invariant population geometry |
| 训练信号 | 掩码神经活动重建；下游监督微调 | 神经与行为自回归联合预训练，再微调 | masked state-summary/几何自监督；行为训练/线性探针分开评估 |
| 泛化轴 | 会话、受试者、任务；目标会话常需校准/微调 | held-out individuals + 新任务数据微调；设备 token 结构影响迁移 | IBL held-out sessions；冻结表征迁移到其他实验数据，仍用目标数据拟合 probe |
| 能支持的最强判断 | 广泛预训练有助于神经建模和数据效率，可做在线原型 | 大规模联合模型对低数据 motor decoding 有用，但受传感器与行为范围限制 | 无神经元 ID 的群体状态 token 在若干受控行为任务里可迁移 |
| 关键限制 | 在线 supervised baseline 可更好；跨物种结果不确定 | 2k 小时扩展需大幅扩模；行为/传感器变化下失效 | 需事件时间；IBL 标签泄漏显著；2026 arXiv 单篇预印本，尚未独立复现 |

表中任务、拆分和指标不相同，不能据各自 MCC/R² 排名。NDT2/NDT3 有高维行为预测、闭环或多人群任务；TWS 把任务边界知识作为输入、主要验证冻结 embedding 的线性可解码性。它们回答不同问题。

## 目前最值得相信与最需要验证的部分

**相对稳固的部分**：神经记录中的传感器差异使跨会话复用变难；显式预训练能减少部分下游标签量；target data、session split、行为标签定义和通道映射都会改变测得的 transfer。NDT3 的 token-order 与 held-out behavior 失败实验，以及 TWS 的 event-time control 和固定边界跨数据集实验，提供了比单纯 leaderboard 更有用的机制对照。

**尚未证成的部分**：是否存在统一的、物种不变的行为神经几何；是否能在新实验室完全无需标签工作；TWS 是否较现有全新多会话模型更稳健；人口几何 token 是否对应生物学回路；预训练是否能带来稳定闭环控制收益。TWS v1 说服力主要来自作者提供的对照与消融，目前没有独立重跑，且其 IBL 主任务首动边界强烈预测标签这一事实降低了主分数的解释力。

**因果边界**：用神经活动预测行为，只说明记录信号中包含对行为有用的信息，并不估计对这些神经元或通路实施干预会怎样改变行为。模型的注意力权重、probe direction 或 manifold basis 也不能直接当作生物功能定位。若用于神经科学发现，后续应提出可证伪的回路假说，再用靶向刺激/抑制、时间锁定干预或闭环操纵验证。

## 下一轮实验判据

1. 预先按 session、subject、probe、实验室、任务分层留出；结果明确说明 held-out session 是否也曾用于自监督预训练或无标签归一化。
2. 分别报告冻结表征 linear probe、只用少量目标标签拟合 decoder、端到端微调、真正无目标标签的 zero-shot；不要混写成“跨个体泛化”。
3. 每个行为目标都提供 label-only baseline、event-time-only baseline、shuffle/control，以及简单 population summary / linear decoder。若边界能直接编码标签，应另设事件不含标签的任务。
4. 对跨阵列结果同时验证通道空间位置、通道顺序、单元数变动与记录质量变化；对行为外推单独留出训练范围外的动作方向或速度。
5. 将生物机制目标与 decoder benchmark 分开：若目的是发现回路，先明确 intervention unit 和可检验方向，再新增干预数据，不以行为解码分数代替因果证据。

## 选文说明

候选池 10 项，入选 3 项作为主证据。NDT2 为共享的多上下文脉冲预训练基线，NDT3 说明成对神经—行为大规模模型的实际收益与外推失败，TWS 聚焦 token 单位以及边界先验的检验。候选发现、排除理由、精读等级和来源核验方式见 [CANDIDATES.md](sources/CANDIDATES.md)；版本、图表锚点、许可证、代码提交及 skill 使用证据见 [MANIFEST.md](sources/MANIFEST.md)。
