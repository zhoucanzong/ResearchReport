# FunSearch：固定语言模型，演化被评价的程序

**原文**：[Mathematical discoveries from program search with large language models, Nature 2024](https://doi.org/10.1038/s41586-023-06924-6)。阅读主文 Introduction、Methods “Implementation details / Prompt building / Evolutionary method and program selection” 及 cap-set、online bin-packing 两个示例。

## 搜索对象是程序，不是完整解

FunSearch 将预训练 LLM、程序数据库和可执行评价器组合在一起：研究者提供问题规范、初始程序或 skeleton，LLM 只编辑关键函数；评价器执行候选并评分。高分程序回到 programs database，后续 sampler 再从库中抽取历史程序组装提示。多个岛并行维护不同的候选群体，并可异步运行 sampler 和 evaluator。

这一区别对理解“LLM 发现算法”很关键。模型不必直接写出某个实例的最终解；它要找到一段能够反复构造好解的规则。外部 evaluator 检查具体输入输出，搜索过程在程序空间累计改进。

## 纠正“无跨代学习”的说法

FunSearch 使用固定的预训练 LLM、没有针对搜索结果进行模型参数微调。这一点容易被误述为“每个候选完全独立生成、没有跨代反馈”。Nature 原文明确说明：提示由数据库抽取的高分程序构建；候选被评价后存入数据库，之后继续进入 prompt；岛模型维护并演化群体。[Methods: Prompt building; Evolutionary method and program selection]

准确区分是：**没有权重层面的训练，但有搜索状态层面的跨代反馈。** EoH 的变化在于把 thought 作为显式个体表示与代码共同进化，而不是它才第一次让系统复用历史候选。

## 论文支持到什么程度

作者在 cap-set 构造中报告超过此前已知构造的结果；online bin packing 实验中，FunSearch 演化用于决策的 priority function。Nature 论文说明使用较快推理的 LLM，总样本规模约为百万量级，并强调 evaluator、程序 skeleton、多样种群和异步并行等设计。[Abstract、Methods、Results]

这不应简化为“LLM 独立提出超人类解”或“FunSearch 每个候选从零生成”。数学构造的新颖性依赖对构造本身的组合数学检查；启发式性能则依赖装箱 benchmark。百万级样本是该论文所报告的实验规模，不与另一任务或另一系统的 LLM query 数直接构成通用效率比。
