# 运筹建模与求解评测：正确性、反馈与基准边界

> 本篇把 NL4Opt、OptiMUS、LLM-LNS、LLM4Branch 与 MIPLIB-NL 放到同一评测框架里。它们回答的问题不同，报告的“准确率”“胜场”“求解时间”不能直接合成一个总排名。

## 先拆成五个判断

| 层 | 要回答的问题 | 可用证据 | 不能据此推出 |
|---|---|---|---|
| **语义解析** | 文本里的实体、变量、目标和约束是否抽取正确？ | 实体识别、子句映射；需说明是否给了 gold entities | 完整数学模型已正确 |
| **模型忠实度** | 数学模型是否表达了原问题和隐含假设？ | 独立等价检查、专家核查、模型与需求逐条对照 | 代码可以运行就代表模型忠实 |
| **实现有效性** | 代码能否在指定 solver 和数据上正确实例化模型？ | parser/runtime 状态、约束构造审阅、solver 日志 | 求解器找到的最优解对应业务真实目标 |
| **决策质量** | 给定模型后，算法在预算内能找到怎样的解与 bound？ | incumbent、best bound、gap、可行性、时间、primal integral | 一个小 benchmark 的平均值代表工业总体 |
| **算法发现** | 搜索出的算法能否在独立问题实例上重现收益？ | held-out instances、独立 runs、预算匹配、人工/solver baseline | 一次找到新最优值就证明通用算法优越 |

这些层之间可以串成闭环，但证据不能越级。求解器状态是强反馈，却只针对给定的形式化模型和数据。模型漏了业务约束时，solver 仍可能正确地给出一个不满足实际需求的“最优解”。

## 现有工作的反馈环位置不同

* **NL4Opt** 把任务拆成实体抽取和 formulation generation； formulation 子任务使用标注实体，单独分数不等于原始自然语言到求解器的完整成功率。[NL4Opt, §2、§2.1–2.3](../papers/2022-nl4opt.md)
* **OptiMUS** 的 evaluator 执行生成代码、定位运行错误并触发 programmer/formulator 修正。其失败分析包含漏约束、模型结构错误和代码错误，说明“solver feedback”不应简化成代码编译错误。[OptiMUS, §§3.2–3.3、§4.5](../papers/2402.10172-optimus.md)
* **FunSearch / EoH** 的 external evaluator 运行候选程序，再把分数用于种群选择；性能信号是候选在特定组合优化实例上的启发式质量，不是 MIP solver 的最优性证明。[FunSearch, Methods；EoH, §4](../papers/funsearch.md) · [EoH](../papers/2401.02051-eoh.md)
* **LLM-LNS / LLM4Branch** 把整段 solver 的结果当评价信号：前者演化 LNS neighborhood，后者在 branch-and-bound 中替换 branching policy。指标由 gap/节点/时间等端到端 solver 行为构成，而不是生成代码与专家模板的相似度。[LLM-LNS, §4、Tables 4–5](../papers/llm-lns.md) · [LLM4Branch, §5、Tables 1–2](../papers/2605.10401-llm4branch.md)

## 三类基准暴露的盲区

### 小型自然语言建模题

NL4Opt 收录 1,101 条线性规划文字题，用不同子任务测实体抽取和逻辑表示生成。其 formulation 子任务的输入含标注的 optimization entities，因此适合隔离公式生成能力，却低估了真实系统还须从开放描述自行判断变量、单位、量词、目标方向和约束条件的难度。[NL4Opt, §2、§3]

OptiMUS 所用 NLP4LP 有 67 个问题；论文还用 NL4Opt 和 ComplexOR 等不同集合。ComplexOR 当时公开数据不完整，作者用合成数据补足 21 个问题。数据版本、补数来源和是否提供结构化提示都会改变结果含义，引用成绩时应保留这些设置。[OptiMUS, §4.1]

### 从已有 MIP 反向生成的规模基准

MIPLIB-NL 从 MIPLIB 2017 选取现成的 MIP 模型，抽取循环结构，再生成自然语言、数值文件和规范数学模型。论文公布 223 个一一对应实例；245 个候选进入验证，163 个通过最多 8 次独立 reconstruction 尝试，另外 60 个由专家和 LLM 检视、修订后保留，22 个被剔除。这个设计既测试模型结构与大数据绑定，也让标准答案来自已有 solver-verified 模型。[MIPLIB-NL, §3.2–3.5]

它不等于“真实业务人员写下的 223 个需求”：自然语言是从已有模型反向生成、被约束为能表达被选中的模型结构。8 次尝试中只要有一次 solver outcome 对上就算主验证通过；测试失败也不会单独证明 benchmark 错误，需人工核查。8 个 infeasible 和 15 个 open 实例也不能参加要求参考最优值的定量比较。[MIPLIB-NL, §3.4–3.5]

### 算法与求解器比较

LLM-LNS 在论文所选的六类 MILP 实例规模、LNS 设计和相同时间限制下，与 ACP、CL-LNS、GNN&GBDT、Gurobi、SCIP 等作比较；其 LNS neighbourhood subproblems 使用 Gurobi。作者报告在所测大型实例上 objective/primal-integral 表现较强。这个证据支持的是给定 benchmark 和时间预算下的 LLM-guided LNS workflow，不支持“LLM 普遍全面超越商用 solver”。[LLM-LNS, §4.2、Tables 4–5、Appendix C]

LLM4Branch 的主张也需要完整条件：它把策略限为 91 维输入上的轻量可执行打分程序，固定在 SCIP 8.0.0 中评估；标准问题用 Easy/Medium/Hard 规格，挑战问题使用 Item Placement 与 neural-network verification；每个实例最多一小时。胜场仅在 CPU-based methods 之间统计，GPU 方法仅作参考；因此“CPU 分支策略中的胜场”不能写成“胜过所有现代求解器”。[LLM4Branch, §§4–5、Tables 1–2]

## 读结果前的条件清单

比较两篇工作时，逐项问这些问题即可；不需要为每篇论文重算全部指标。

1. **问题和数据**：LP/MILP/NLP？实例来自真实模型、人工写题、合成，还是反向生成？NL 是否披露全部约束？数值数据是否分离？
2. **模型接口**：只评 entity extraction，还是给了 gold entities？要求数学 formulation、可执行代码、最终可行解，还是完整闭环？
3. **solver 配置**：同一 solver/version、gap tolerance、预处理、随机种子、并行线程和 time limit 吗？不一致要说明。
4. **结果分母**：未解、超时、不可行和代码失败如何计入？最优性 gap 与仅有 incumbent 的目标值是否区分？
5. **搜索预算**：LLM queries、program evaluations、solver calls、墙钟时间和硬件分别是多少？这些预算不能用同一个“迭代次数”替代。
6. **泛化**：哪些实例参与 prompt、heuristic evolution、参数调优、模板设计？评测问题和随机生成分布是否独立？

把这些条件写清之后，“模型给出了可执行模型”“策略让 solver 在这个基准中跑得更好”和“系统能可靠处理业务需求”才不会被同一个准确率或 gap 混为一谈。
