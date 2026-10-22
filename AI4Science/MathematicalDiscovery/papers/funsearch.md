# 精读：FunSearch——LLM 引导的组合构造与算法搜索

## 亮点与差异

- **一句话亮点**：将语言模型放进可执行 evaluator 与进化种群之间，搜索生成数学构造或算法启发式的短程序。
- **新在哪**：搜索对象不是几十万项的完整解，而是控制 greedy constructor 的 priority/heuristic 函数；骨架、岛模型、程序聚类和最佳程序提示共同改变候选搜索分布。
- **证据强度**：cap-set/admissible-set 构造可推出新的容量下界；在线装箱结果是指定模拟分布、有限实例规模上的指标比较。补充材料显示组件在 5 个随机种子下结果不稳定，8 维 cap-set 的新纪录仅出现在 140 次运行中的 4 次。
- **值不值得引用**：适合研究 program-space search、人机共同解释以及可执行验证器的作用；不能当定理自动证明系统，也不能把特定分布的装箱优势写成普遍最优。

## 文献信息

- Bernardino Romera-Paredes et al., “Mathematical discoveries from program search with large language models,” *Nature* 625, 468–475 (2024), DOI [10.1038/s41586-023-06924-6](https://doi.org/10.1038/s41586-023-06924-6)。2023-12-14 online，version of record 2024-01-11，CC BY 4.0。无 arXiv 身份经 PaperFetcher 核实；固定阅读 Nature 正文与官方 Supplementary Information。Supplementary Data 提供演化代码与发现函数；本文未下载其 ZIP、未克隆或运行代码。

## 1. 解决什么问题

不少组合问题“容易给候选打分、难以搜索到高分候选”：一个 evaluator 可以快速检查集合是否满足条件或 heuristic 用了多少箱，但候选空间极大。FunSearch 试图利用 LLM 代码生成能力，持续提出可执行程序，由 evaluator 筛掉错误/低分候选，并让进化搜索积累有用的局部代码结构（Nature 正文 Abstract、§§“FunSearch”“Evaluation”）。适合的问题需要高效 evaluator、细粒度分数和可用程序骨架；无稳定分数反馈的普遍定理证明不属于本文展示的强项。

## 2. 核心方法

以 cap set 为例，人工给出 `solve` 骨架，从空集开始逐步添加候选点，并在加入前检验是否破坏“三个不同点不共线”约束；LLM 只演化 `priority`，即候选点顺序。在线装箱中，人工固定 solve 流程，LLM 演化给箱子打分的 heuristic（Fig. 2）。这种人为限定把搜索集中在决定结果的一个函数，代价是解空间也受骨架限制。

每轮程序经过语法/运行检查和 evaluator 执行；合法程序按得分、跨输入表现签名形成 cluster，并存放在多个 island。采样偏向高分 cluster，同时按程序长度偏向简短样本，再以多个已选程序组成 prompt 供预训练 LLM 提议新实现。岛间定期淘汰低分区域以维持多样性（正文 Fig. 1、Methods “Programs database”；Supplementary §§A.1、F.3、F.3.1–F.3.2）。主论文用未微调的 Codey，报告总样本量级约 `10^6`；常见分布式设置为 15 个 samplers、150 个 CPU evaluators（正文 “Pretrained LLM”、Methods “Implementation details”）。

## 3. 数据与规模

- **Cap set**：在 `Z_3^n` 中选点，任意三个不同点不组成直线。精确最大值只知到 `n≤6`；论文指出 `n=8` 的原始空间约 `3^1600`。报告的直接构造为 8 维、512 点（正文 §“Cap sets”、Fig. 3；Supplementary §E.2）。
- **Admissible sets**：从小维构造诱导 cap-set 容量下界。论文搜索 `I(12,7)`、对称 `I(15,10)` 全尺寸集合和 `A(24,17)` 部分集合；补充统计包括 `n=12,w=7` 的 5 次无显式对称约束运行、`I(15,10)` 的 5 次对称运行和 `A(24,17)` 的 5 次运行（Supplementary §§A.1、A.3、C.2、D）。
- **Online bin packing**：在生成的 OR1 规模实例训练，再测试 OR-Library OR1–OR4；另在 5k 件 Weibull 实例训练、10k/100k 件实例测跨规模泛化。指标为相对离线下界的超额用箱比例（正文 §“Bin packing”、Table 1；Supplementary §§E.4、A.3）。补充常见规模为 15 LLM samplers 与 150 CPU evaluators；这不是与一个单机/同预算 baseline 的硬件速度对照。

## 4. 主要结果（带条件）

**数学构造**：FunSearch 找到 `I(12,7)` 结构后，研究者检查程序输出并观察到坐标三元组对称性，再把该对称性明确纳入后续搜索。`I(15,10)` 诱导 `C ≥ 2.219486`；`A(24,17)` 的 237,984 元素部分集合诱导容量下界 `C ≥ 2.2202`（正文 §“Cap sets”、Fig. 5）。这是下界提升，不是容量的精确值或证明其最优。

**算法启发式**：OR1–OR4 上论文报告优于 first fit / best fit；Weibull 100k 件实例距离离线最优下界 0.03%（正文 Table 1）。多次运行的补充统计给出更易复核的另一口径：10 次 Weibull 10k 评估的超额箱比例为 FunSearch `0.44% ± 0.11%`，first fit `4.20%`，best fit `3.90%`（Supplementary Fig. A.3c、§A.3）。后一个数字对应 10k Weibull 数据，不能与 100k 离线下界结果混为一项。

**随机性**：cap set 8 维的 140 次实验中仅 4 次达到 512；`I(15,10)` 对称搜索 5 次中 2 次发现全尺寸集合；`I(12,7)` 不显式约束对称的 5 次中 3 次发现全尺寸集合（Supplementary Fig. A.3、§A.3）。所以代表性最好结果不能当典型单次命中率。

## 5. 消融 / 对照说明了什么

Nature Supplementary §A.1 在 `I(15,10)` 上做 5 随机种子组件消融，分别移除程序骨架、提示进化、跨岛多样性或 prompt 合并多个程序。报告总体 FunSearch 5 次中 2 次得到全尺寸集合，平均找到的集合也大于其他配置；不使用 skeleton、evolution 或 diversity 的配置没有完整解；不合并 prompt 的 `k=1` 变体 5 次中 1 次完整解。结论是骨架与演化对效果尤其关键，但样本数为 5 的小实验不支持精确估计这些模块的因果效应（Supplementary Fig. A.1、§A.1）。

另有模型/搜索对照：Codey 在 `I(15,10)` 五次中两次找到完整集，StarCoder 五次均未找到完整集但仍改善旧容量下界；手工设计随机代码变异比两者差且需要人工添加新操作。随机变异即便生成超过 5,000 万程序仍停在较差分数（Supplementary Fig. A.2、§A.2）。这些结果支持 LLM 提议器在该任务与该配置上的优势，不证明任意模型、任务或预算下 LLM 必然胜过传统变异。

**对照口径**：SAT/CP-SAT 在小中型 admissible-set 规模可用；加 FunSearch 从输出中识别的对称性后，能达到更大 `I(15,10)` 实例（Supplementary Fig. A.4、§A.4）。SAT 运行还包含 210 路并行、对 10 个二进制变量固定赋值、每个 solver instance 至少运行 50 小时等设置；这不是直接的相同算力速度赛。方法差异在于 FunSearch 可搜索短生成程序、再利用观察到的结构缩小空间，SAT formulation 直接求大型变量赋值。

## 6. 失效条件与边界

- **依赖 evaluator 与骨架**：问题要可高效评分并提供有信息量的连续/等级分数；骨架能把逻辑隔离出来，但也排除了骨架本身之外的策略空间（正文 “When does FunSearch work?”；Supplementary §A.1）。
- **不是定理证明器**：evaluator 可检查 cap-set/packing 候选，但算法本身没有 Lean 式完整证明验证；评分更高不意味着达到组合问题最优。
- **搜索不稳定**：512 cap set 仅在 140 次中出现 4 次；报告最好一次会掩盖多数运行未达到记录这一事实（Supplementary §A.3）。
- **尺度依赖评测**：online packing 优势针对 OR-Library 和 Weibull 生成分布、指定实例规模及其下界指标；其他输入分布、真实调度系统或硬件时间没有被这些数字证明。
- **训练数据污染风险**：后续作者指出原论文发布的 512 构造可能进入后续 LLM 预训练语料，故后来重现该程序不能仅凭得分判定独立发现（见[复现精读](funsearch-reproducibility.md)）。

## 7. 与同类系统的可判定差异

相对传统遗传编程，FunSearch 用 LLM 作为程序提议/变异机制，不必为每个任务手写一套精细 mutation primitive；但具体 `solve` 骨架、约束和 evaluator 仍由研究者设计，LLM 没有接管整个发现问题。相对 SAT/CP-SAT，它优先搜索程序描述而非枚举大量变量赋值，且输出可读函数能被数学家观察并发现对称。相对 AlphaProof，它的真实性闸门是任务 evaluator，不是对形式命题 proof term 的 Lean kernel 验证。

## 原文定位

- 机制：Nature 正文 Figs. 1–2、§§“FunSearch”“Evaluation”；Supplementary §§A.1、F.1–F.3。
- Cap-set 构造与下界：正文 §“Cap sets”、Figs. 3–5；Supplementary §§C.1–C.2、D、E.2–E.3。
- Bin packing 与口径：正文 §“Bin packing”、Table 1、Fig. 6；Supplementary §§A.3、E.4–E.5。
- 组件消融与模型对照：Supplementary Figs. A.1–A.2、§§A.1–A.2。
- 运行随机性：Supplementary Fig. A.3、§A.3。
- SAT 差异：Supplementary Fig. A.4、§A.4。
