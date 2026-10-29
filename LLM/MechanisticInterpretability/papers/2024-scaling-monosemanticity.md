# Scaling Monosemanticity：大字典提取出什么，又还缺什么

来源：Anthropic，[官方 2024 原文](https://transformer-circuits.pub/2024/scaling-monosemanticity/)，发布于 2024-05-21。阅读重点：§1–2、§4、§6–7。

## 从 toy SAE 到中型生产模型

SAE 将模型某处激活编码为稀疏系数，再用学到的字典向量重建激活。Anthropic 将此方法用于 Claude 3 Sonnet 中间层 residual stream，训练宽度不同的字典。论文展示了语言、多模态、代码和抽象主题等特征，也研究把这些 feature 作为计算中间变量以及干预它们时的行为变化。[§1–2、§4](https://transformer-circuits.pub/2024/scaling-monosemanticity/)

作者报告的工程与特征统计说明大字典并非“算力越多，就得到一份完备概念表”：34M feature SAE 的 dead feature 比例较高；一个粗特征在更宽字典里可能拆成多个近邻子特征；有些概念在较小字典中则没有明显对应。改变字典宽度，会改变可见特征的粒度和覆盖范围。[§1.2、§3.1–3.2](https://transformer-circuits.pub/2024/scaling-monosemanticity/)

## 从激活样例到行为干预，证据增加但仍非充分

论文用最大激活样例和自动评分检查特征描述的 specificity，再通过改变 feature activation 观察模型输出是否按解释方向变化。作者展示了若干安全相关和抽象特征，并明确提醒：激活代表“模型在表示或讨论某概念”，不自动表示模型具有相应意图或会在真实场景执行相关行为。即便干预改变输出，也只说明在选定 prompt 和模型位置下存在影响，不能替代对更大机制或其他路径的完整解释。[§2、§4、§6](https://transformer-circuits.pub/2024/scaling-monosemanticity/)

更关键的限制是论文承认 SAE feature suite 不完整，且缺少严格方法测量 feature 是否忠实捕捉原模型计算。重建损失和一组可读示例都是代理；低重建误差不保证解码字典与原模型执行的是同一种机制。论文中的 steering 案例也不等于已解释完整电路。[Abstract、§7](https://transformer-circuits.pub/2024/scaling-monosemanticity/)

## 与 neuron-basis circuit tracing 的关系

2026 年的[神经元基底电路研究](https://arxiv.org/html/2601.22594v2)挑战“必须先训练 SAE 才能得到稀疏电路”的预设。作者在 Llama 3.1 8B-Instruct 的 subject–verb agreement 任务和一个多跳地名任务中，比较 MLP activation basis 与 SAE feature basis，并报告在其 attribution 方法和评估设置下，MLP activations 也能构成稀疏且有干预效果的电路。这不是对 SAE 的普遍否定，而是说明分析基底、归因算法、数据和任务都会改变“可解释单位”。

## 阅读所得

SAE 扩大了研究者可以检索和干预的内部坐标，但“可命名”“与行为相关”“干预有用”和“忠实复现原机制”是不同证据要求。学到更多 feature 有价值，仍要把它们放回计算图、用干预测试路径，并报告未覆盖的 error/residual 部分。
