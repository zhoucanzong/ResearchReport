# Constitutional Classifiers：从规则生成到上下文分类级联

来源：Sharma et al., [*Constitutional Classifiers: Defending against Universal Jailbreaks across Thousands of Hours of Red Teaming*](https://arxiv.org/html/2501.18837v1)，arXiv v1（2025-01-31）；Cunningham et al., [*Constitutional Classifiers++*](https://arxiv.org/html/2601.04603v1)，arXiv v1（2026-01-08）。分别阅读原文 v1，重点看防护机制、red-teaming protocol、生产误拒率和局限。

## 原始 Classifiers：用规则合成训练数据与输入/输出检查器

原始 Constitutional Classifiers 从自然语言“constitution”描述允许/限制内容，用 LLM 生成合成攻击/良性样本来训练分类器；部署时分类器检查输入或输出是否涉及受限制内容。论文关注“统一越狱”对多轮有害协助的风险，并以长时间人工红队、held-out 攻击和生产流量误拒来评估鲁棒性与可部署性。[原始论文 §2–§6](https://arxiv.org/html/2501.18837v1)

这一结构不修改主语言模型的表示或训练目标，风险识别发生在生成接口周围。若分类器只看用户输入或只看最终输出，便可能漏掉跨轮累计、从上下文重构的攻击、或“输入看似无害但答案与其组合后危险”的情形。

## Classifiers++：交换上下文、分级审查和线性探针

Constitutional Classifiers++ 报告了两类旧分类器漏洞：攻击者把危险内容拆分到较长上下文里重组，或对输出编码/混淆以绕过只看输出的检查。它改用 **exchange classifier**，联合输入与响应判断对话是否危险；再用两阶段 cascade 先由轻量检查器筛选，只把可疑交互升级给更强分类器；线性 probe 与外部 classifier ensemble 则进一步降低计算开销。[Classifiers++ §2–§6](https://arxiv.org/html/2601.04603v1)

级联不是“第一层判定即拒绝”：第一层可以高召回筛查，后续分类器再评估，避免第一层误报直接造成误拒。完整系统在 Anthropic 的特定 production shadow traffic 和红队协议中报告低 flag/refusal rate 与更低计算开销；这些不是所有模型、部署流量或未来攻击下的通用安全保证。论文使用的统一越狱目标也比“阻止任意有害内容”窄。[§4、§6](https://arxiv.org/html/2601.04603v1)

## 一条方法路线上的两个改进点

| 版本 | 检查什么 | 主要盲点/设计变化 | 需要同时查看的效用指标 |
| :-- | :-- | :-- | :-- |
| 原始 Classifiers | 输入/输出分类器；规则合成训练集 | 单侧观察可能漏掉输入—响应组合和跨片段重构 | 良性流量误拒、攻击成功与生产样本分布 |
| Classifiers++ exchange | 带对应输入的完整交互 | 更能识别输出混淆，但全量运行更贵 | 误拒率、全量/升级比例、人工红队发现攻击的协议 |
| Classifiers++ cascade + probes | 轻量筛查再升级；内部激活 probe 与外部分类器结合 | 成本和误报的控制来自多层阈值，仍可能被新攻击绕过 | 生产 flag/refusal、阈值校准、held-out/adaptive attack 与良性任务 |

论文中报告的红队小时数描述投入的攻击搜索量，不是概率意义的安全证明；production flag rate 是相应影子流量中的拦截比例，不等同为所有用户请求的 false-refusal rate。比较两代系统时还需注意旧版基线、分类任务、部署流量和 red-team protocol 是否同口径。[原始论文 §4–§5；++ §4–§6、Appendix B–F](https://arxiv.org/html/2501.18837v1) [Classifiers++](https://arxiv.org/html/2601.04603v1)

**带走的区别**：classifier 防御强化的是输入/输出的风险测量与拦截；相较训练期 refusal，它更易独立更新，但也新增分类边界、上下文完整性、阈值与级联策略等失效点。它与 [Circuit Breakers](defense-circuit-breakers.md) 的内部表示干预、[Instruction Hierarchy](defense-instruction-hierarchy.md) 的模型训练行为并非同一层。
