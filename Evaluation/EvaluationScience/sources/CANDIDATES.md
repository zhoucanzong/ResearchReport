# 候选筛选 — 评测科学

筛选截止：2026-10-23。**候选池 16 项；本专题精读 13 篇；既有条目交叉引用 1 篇；排除 2 项。** 本轮先后补入小样本区间校准、pairwise judge 的近/远差距条件、真实用户来源的长时程任务，以及 agent 重复成功、桌面终态 evaluator 和网页 checker 三个交互评测切面。取舍标准仍是能否支撑“什么推断被测量、哪些假设会断裂、怎样用反例限定分数解释”这条机制线；不按基准数量扩写。

| 候选 | 决定 | 纳入或排除理由 |
|---|---|---|
| The Benchmarking Epistemology: Validity Theory for Evaluating Machine Learning Models, DOI 10.1017/psa.2026.10280 | 精读，主框架 | 最新的出版版本把从分数到推断拆为可检查的效度条件和五类子推断，直接回答本专题核心问题；用 ImageNet 与社会科学案例说明跨领域适用性。 |
| HELM, arXiv:2211.09110v2 | 精读，构念/报告设计 | 用场景分类、多指标和显式缺失项说明 benchmark 设计选择怎样限定它能声称的内容；但不把“holistic”标题当成通用能力效度证明。 |
| A Taxonomy for Data Contamination in Large Language Models, arXiv:2407.08716v1 | 精读，污染机制 | 区分 dataset-level、instance-level 泄露及相关但非污染的先验任务知识；保留其 GPT-2 Large 摘要/QA 实验的模型与任务边界。 |
| LiveBench, arXiv:2406.19314v2 | 精读，动态评测机制 | 近期题目、周期更新、自动客观评分同时针对污染与 judge 噪声；其非英语与开放生成限制使它也是“动态并不等于全面有效”的反例。 |
| Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena, arXiv:2306.05685v4 | 精读，judge 正面与反例 | 有 58 名专家标注者、众包投票、人评一致结果和位置偏差实验；可以说明高 agreement 既是实证支持，也有协议适用范围。 |
| Judging the Judges: A Systematic Study of Position Bias, arXiv:2406.07791v9 | 精读，judge 信度/偏差 | 大规模 position swap、多 judge、不同任务分析可将重复稳定与评判公平分开；比再加入一篇偏差分类综述更直接。 |
| WildClawBench, arXiv:2605.10912v1 | 精读，长时程 agent | 2026 年 native-runtime、多模态、工具交互案例，提供任务筛选、混合评分、跨 harness 对照及明确外推限制；适合作为当前研究线的例子，不作生产部署代表性结论。 |
| Position: Don’t Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints, arXiv:2503.01747v3 | 精读，样本不确定性 | ICML 2025 Spotlight position paper 以覆盖率模拟展示小样本、聚类、配对比较和非均值指标中的区间风险，并比较替代方法；修正报告把点估计分差当作确定提升的倾向。其标题不是固定 N 门槛，结论按所模拟的数据生成与指标条件使用。 |
| Pair Difficulty Matters: Rethinking Pairwise LLM-as-a-Judge Evaluation and Consistency, arXiv:2609.37577v1 | 精读，近差距 judge 评估 | 2026 年原文提出 pair 质量差距会改变逐对错误对 Bradley–Terry 排序的影响；模拟与两个教育文本语料显示聚合一致性代理可能不能预测排序恢复。纳入后补充“近 pair 更易翻转”的已有发现；其新实验仅有 12 个 judge-corpus 点，保留为方向性结果，不作通用效应估计。 |
| RealWebAssist: A Benchmark for Long-Horizon Web Assistance with Real-World Users, AAAI 2026, DOI 10.1609/aaai.v40i40.40742 | 精读，真实用户来源 | AAAI 官方 PDF 报告从真实用户辅助会话收集的连续指令，提供静态单任务 benchmark 的有价值外部效度补充；但后续模型评测是离线动作回放，参与者仅 10 人且不含在线澄清对话，不能作为真实部署评估的替代。 |
| τ-bench, arXiv:2406.12045v1 | 精读，重复交互可靠性 | 给出 `pass^k` 与 `pass@k` 的不同问题定义，并显式含随机用户模拟器；主表每任务至少三次，但 Figure 4 的高阶试次数及区间报告不充分。用于解释重复成功，不将最终状态奖励等同完整政策合规。 |
| OSWorld, arXiv:2404.07972v2；OSWorld-Verified 官方修订公告 | 精读，VM 状态重建与终态评估 | 原论文的 VM 快照、配置化初态和逐任务状态检查说明桌面评测如何降低环境噪声；原分数没有 pass@k/重复方差。2025 修订公告单独作为维护者的基准版本记录，不与原论文表格混排。 |
| WebArena, arXiv:2307.13854v4 | 精读，浏览器状态 checker 与变体一致性 | 自托管容器可重置，操作任务按数据库/API/页面状态判分，信息任务部分依赖 GPT-4 fuzzy match。模板变体表现不能冒充同任务多次运行的方差。 |
| SIMPLER, arXiv:2405.05941v1 | 引用已有专题，不重复精读 | 本库 VLA 专题已有正文精读：sim-real 评测目标是相对排序关联，不是仿真绝对成功率可替代真机；用于补足物理接触环境与软件 agent 的外部效度差异。 |
| Benchmark Data Contamination of Large Language Models: A Survey, arXiv:2406.04244 | 排除 | 综述有助于扩展书目，但本专题已有一手污染分类和动态基准设计案例；再铺一篇调查会扩充覆盖面却不增加核心机制解释。 |
| Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge, arXiv:2410.02736 | 排除 | 系统量化多种 judge 偏差是有价值的后续候选；本次选择含受控人评对照的 MT-Bench 原文，再配大规模位置交换研究，足以支撑“agreement、重复信度、偏差”三者区分。若后续专题扩展到自偏好或 demographic bias，可重开此候选。 |

筛选的主线不是“哪些 benchmark 有新分数”，而是依次追问：测量目标怎样被任务操作化 → 测试暴露如何侵蚀新颖性和独立性 → 评分者的稳定性与无偏性如何分开验证 → 交互环境怎样改变被测系统与部署推断。
