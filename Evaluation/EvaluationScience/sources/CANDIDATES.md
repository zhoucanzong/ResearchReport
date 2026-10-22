# 候选筛选 — 评测科学

筛选截止：2026-10-23。**候选池 10 项；本专题精读 7 篇；既有条目交叉引用 1 篇；排除 2 项。** 取舍标准是能否支撑“什么推断被测量、哪些假设会断裂、怎样用反例限定分数解释”这条机制线；不按基准数量扩写。

| 候选 | 决定 | 纳入或排除理由 |
|---|---|---|
| The Benchmarking Epistemology: Validity Theory for Evaluating Machine Learning Models, DOI 10.1017/psa.2026.10280 | 精读，主框架 | 最新的出版版本把从分数到推断拆为可检查的效度条件和五类子推断，直接回答本专题核心问题；用 ImageNet 与社会科学案例说明跨领域适用性。 |
| HELM, arXiv:2211.09110v2 | 精读，构念/报告设计 | 用场景分类、多指标和显式缺失项说明 benchmark 设计选择怎样限定它能声称的内容；但不把“holistic”标题当成通用能力效度证明。 |
| A Taxonomy for Data Contamination in Large Language Models, arXiv:2407.08716v1 | 精读，污染机制 | 区分 dataset-level、instance-level 泄露及相关但非污染的先验任务知识；保留其 GPT-2 Large 摘要/QA 实验的模型与任务边界。 |
| LiveBench, arXiv:2406.19314v2 | 精读，动态评测机制 | 近期题目、周期更新、自动客观评分同时针对污染与 judge 噪声；其非英语与开放生成限制使它也是“动态并不等于全面有效”的反例。 |
| Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena, arXiv:2306.05685v4 | 精读，judge 正面与反例 | 有 58 名专家标注者、众包投票、人评一致结果和位置偏差实验；可以说明高 agreement 既是实证支持，也有协议适用范围。 |
| Judging the Judges: A Systematic Study of Position Bias, arXiv:2406.07791v9 | 精读，judge 信度/偏差 | 大规模 position swap、多 judge、不同任务分析可将重复稳定与评判公平分开；比再加入一篇偏差分类综述更直接。 |
| WildClawBench, arXiv:2605.10912v1 | 精读，长时程 agent | 2026 年 native-runtime、多模态、工具交互案例，提供任务筛选、混合评分、跨 harness 对照及明确外推限制；适合作为当前研究线的例子，不作生产部署代表性结论。 |
| SIMPLER, arXiv:2405.05941v1 | 引用已有专题，不重复精读 | 本库 VLA 专题已有正文精读：sim-real 评测目标是相对排序关联，不是仿真绝对成功率可替代真机；用于补足物理接触环境与软件 agent 的外部效度差异。 |
| Benchmark Data Contamination of Large Language Models: A Survey, arXiv:2406.04244 | 排除 | 综述有助于扩展书目，但本专题已有一手污染分类和动态基准设计案例；再铺一篇调查会扩充覆盖面却不增加核心机制解释。 |
| Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge, arXiv:2410.02736 | 排除 | 系统量化多种 judge 偏差是有价值的后续候选；本次选择含受控人评对照的 MT-Bench 原文，再配大规模位置交换研究，足以支撑“agreement、重复信度、偏差”三者区分。若后续专题扩展到自偏好或 demographic bias，可重开此候选。 |

筛选的主线不是“哪些 benchmark 有新分数”，而是依次追问：测量目标怎样被任务操作化 → 测试暴露如何侵蚀新颖性和独立性 → 评分者的稳定性与无偏性如何分开验证 → 交互环境怎样改变被测系统与部署推断。
