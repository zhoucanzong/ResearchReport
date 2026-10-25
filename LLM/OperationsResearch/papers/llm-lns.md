# LLM-LNS：让 LLM 选择大邻域搜索中的变量

**原文**：[Large Language Model-driven Large Neighborhood Search for Large-Scale MILP Problems, ICML 2025, PMLR 267](https://proceedings.mlr.press/v267/ye25j.html)。阅读 §§3–4.2、Tables 4–5、Appendix C、I。

## LLM 放在启发式决策环节

Large Neighborhood Search (LNS) 保留当前可行解，选择一组变量并暂时放松它们，再让 MILP 子求解器重新优化这个 neighborhood。效果依赖“放开哪些变量”。LLM-LNS 使用内外两层自演化 agent 设计 neighborhood-selection heuristics，并以候选策略运行后的 objective feedback 评价策略。[§3]

分工是：LLM 搜索“当前该改哪些变量”的策略；Gurobi 或 SCIP 处理放松子问题。它不是用 LLM 取代 branch-and-bound，而是让 LLM 产生可嵌入求解流程的启发式组件。

## 作者的比较与适用范围

论文实验包括 online bin packing、TSP，以及 set covering、minimum vertex cover、maximum independent set 和 mixed-integer knapsack 等 MILP 测试。作者用小规模实例训练 neighborhood 策略，再将其用于更大的实例；比较 Random-LNS、ACP、CL-LNS、GNN&GBDT、Light-MILPopt，以及 Gurobi/SCIP。[§4.1–4.2、Tables 4–5]

作者报告，在列出的 MILP 测试和时间限制下，LLM-LNS 的 objective values 与 primal integrals 有竞争力；表中 SC2、MVC2 等指定实例的 primal integral 比最近基线改善超过 20%。这是作者在特定实例、LNS 参数、子求解器和时间预算下的结果，不能表述为“LLM 全面超越传统求解器”。LNS 比较的子问题使用 Gurobi，不等同于同一算法只替换 solver 后的全局结论。[§4.2.1、Table 5、Appendix C]

作者也指出，跨异质问题时对目标值作未归一化平均可能使大数值实例主导 fitness，导致启发式过拟合；当前设计主要面向特定 MILP 场景。[Appendix I]
