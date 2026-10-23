# 预训练数据配比：从稳健重加权到代理回归

训练数据“配比”回答的是不同语料池在固定训练 token 预算里各占多少；它和删掉单篇低分文档的样本级过滤不是同一个决策。把网页、书籍、论文、代码等域的采样概率改掉，即使 token 总数、模型和优化器相同，也会改变模型看到的知识、写作风格与任务分布。DoReMi 和 RegMix 给出两种有代表性的自动选配比方式：前者提高 proxy 模型尚未学会、但基准模型认为可学习的域的权重；后者从许多小模型的混合实验拟合性能面，再预测大模型该用哪组配比。

## DoReMi：用“相对可学习性”给域重加权

DoReMi 不直接追求一组下游 benchmark 的最优分数。它先训练一个 reference model，作为各域难度的基线；然后训练 proxy 模型，按域比较两者的 token-level loss 差值。某个域上 proxy 比 reference 仍差很多、而 reference 本身又已能较好预测该域时，该域有较大的“可改善空间”，Group DRO 就逐步增加该域权重。最终用整段训练过程中权重的平均值，重采样训练更大的主模型。减去 reference loss 是关键：若只挑 loss 最高的域，可能只是在追逐本质熵很高、难以学好的材料。[DoReMi §2]

在 The Pile 实验中，作者用 280M 参数的 reference/proxy 为 8B 主模型选配比，主模型从头训练；比较中每个主模型处理相同 token 数，Pile 训练 200k steps，batch size 512、最大序列长 1024，one-shot generative 评测覆盖 TriviaQA、NaturalQuestions、WebQuestions、SQuADv2 和 LAMBADA。DoReMi 相对 The Pile 默认权重的平均准确率提升 6.5 个百分点，并以约 2.6 倍更少的主模型训练步数达到基线准确率；选配比所用 reference 与 proxy 训练约占主模型计算量的 8%。这是论文在其语料和五项任务上的结果，不是所有领域都可同时提升的保证。[DoReMi Abstract, §3.1–3.2]

一个有解释力的结果是：DoReMi 即使降低某域在训练分布中的权重，仍报告 8B 模型在 The Pile 各域上的验证困惑度均优于默认权重模型。它说明某个域原有采样比例可能造成整体训练效率损失；不代表被降权的域不重要，也不表示面向每类用户的公平性、覆盖率或长尾能力已经被照顾。方法优化的是所选域划分下的整体/最坏域目标，域定义本身决定了“谁被保护”。[DoReMi Abstract, §3.2]

## RegMix：从小模型混合实验预测大模型

RegMix 把每个语料域的混合权重当作回归特征，把训练后的目标验证损失当作标签。它先从许多候选混合中训练小模型、拟合 ridge 或 LightGBM 等回归器，再在混合空间中预测表现较好的配比，并用较大模型验证。作者在 17 个 Pile 子集上研究混合；模型使用 GPT-NeoX tokenizer（50,432 词表），代理训练设为 1M/60M 参数、每个候选 1B tokens；大模型实验是 1B 参数、25B tokens、cosine 学习率。训练配比预测的关键假设是：不同模型规模和训练 token 数下，混合方案的相对名次大体保持不变。[RegMix §3–4, Appendix E]

对 1M 参数代理，作者训练 512 种混合、每种 1B tokens；其总 FLOPs 估计接近单个 1B 参数模型训练的 2%。回归器预测之后，作者以 64 个不同配比训练 1B/25B-token 模型作检验。论文 Table 4 中 RegMix 的 14 项任务平均分为 47.3，The Pile 人工设定权重为 45.1；RegMix 也并非逐项第一。附录 J 又在 7B/100B-token 设定比较 RegMix 与人工配比，报告 13 项任务平均为 56.5 vs 54.5；其中一些任务仍无改善。这里验证的是 RegMix 选出的一个配比优于人工基线，不等于在 7B 上系统验证了 64 个混合的相对排名。结果支撑“同一语料池内配比足以造成可观测的能力差异”，不支撑“代理回归找到普遍最优配方”。RegMix 选择 Pile-CC 验证损失作为代理目标，是因为小模型实验发现它与多数下游任务相关性较强；因此这条验证损失不是完全独立于任务分析的盲选指标。[RegMix §4–5.3, Table 4, Appendix E, J]

论文观察到 Pile-CC（Common Crawl 网页域）验证损失与多数下游任务表现有较强相关，而“感知上质量更高”的 Wikipedia 并没有表现为更强的正向相关；线性代理模型也把 PhilPapers 与多个其他域的收益联系起来。后一个结果更应当作需要进一步验证的域交互假设，而非哲学论文对所有任务的因果增益证明。回归系数、样本量和候选混合分布限制了可以从相关性中读出的因果解释。[RegMix §5.2, §5.4]

## 两种方法的共同点与推断边界

| | DoReMi | RegMix |
|---|---|---|
| 优化信号 | proxy 相对 reference 的域级 excess loss，以 Group DRO 最大化最差域权重 | 小模型混合的目标验证损失，拟合回归后搜索配比 |
| 主要直觉 | 给尚有可学习空间的域更多训练质量 | 用许多便宜实验近似昂贵的大模型混合搜索 |
| 关键依赖 | 域划分、reference 的难度校准、proxy 诱导的权重 | 代理候选覆盖、目标验证集与 mixture rank invariance |
| 规模证据 | 280M proxy 为 8B 主模型选权重；论文也做其他尺度分析 | mixture rank 跨规模系统核验至 1B；另报告 7B/100B-token 的 RegMix-vs-human 比较 |

两项研究共同把“配比”从定性经验变成可比较的训练干预，但都在有限域划分、英文语料和特定模型/评测协议内成立。DoReMi 选择最坏域的相对可学习性，RegMix 预测某一目标损失；这不是同一目标的两种等价求解器。若目标由某个 benchmark、域损失或开发集决定，反复据此挑配比会让该信号逐渐成为策展目标，也可能牺牲未被该信号代表的领域。小模型能不能可靠预测规模扩展仍是关键条件：RegMix 明确把 mixture rank invariance 的系统验证限制在 1M–1B 参数；其附录虽报告 7B/100B-token 模型对比，但那一实验只比较 RegMix 配比和人工基线，没有重做多候选的排名检验。DoReMi 也观察到 proxy 规模变化时 The Pile 权重会改变（280M 倾向 Pile-CC，1B 倾向 OpenWebText2）。

## 放回筛选与去重的完整链路

样本级过滤（DataComp-LM）改变“池内选哪些文档”，分域配比（DoReMi、RegMix）改变“各池抽取多少 token”，去重（FineWeb、Deduplicating Training Data）改变“哪些重复片段/文档仍然存在”。它们作用于不同层级，且顺序可能交互：先过滤会改变每个池的数据规模和组成；再采样配比会改变训练 token 在域间的分配；跨快照去重还可能重排保留下来的时间与质量分布。固定训练 token 只控制总训练量，不会自动固定语言、领域、时间、文档质量或重复程度。

因此，读配比论文时至少同时问：模型和 tokenizer 是否固定、训练 token 预算是否一致、域如何定义、优化目标是哪一个、proxy/search 成本有没有计入、最终是否用较大模型验证，以及未被优化目标覆盖的能力是否评测。DataComp-LM 的人工可读质量标签不等价于训练效用，FineWeb 的全局去重反例说明较少重复也不自动意味着更好样本；DoReMi/RegMix 则进一步表明，即使语料内容池不变，样本池之间的 token 分配也会显著改变最终模型。

## 来源与阅读范围

- Xie et al., *DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining*, arXiv [`2305.10429v3`](https://arxiv.org/html/2305.10429v3), 2023-10-24。重点读 §2、§3.1–3.2、§4 与 Appendix C；本文只摘取 Pile/8B 结果和有助理解机制的权重分析。
- Liu et al., *RegMix: Data Mixture as Regression for Language Model Pre-training*, arXiv [`2407.01492v2`](https://arxiv.org/html/2407.01492v2), 2025-01-23。重点读 §3–5.4、Appendix B、E、J；表格按论文报告引用，未独立复算训练或统计显著性。

上述结果均为作者报告。本次没有训练模型、重跑评测或验证 proxy-to-large 的排序假设。
