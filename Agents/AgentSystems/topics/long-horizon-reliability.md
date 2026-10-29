# 长程 Agent 可靠性：从看见状态到保留经过验证的进展

一个 Agent 连续运行几个小时或几百步，并不自动意味着它“有长程能力”。长任务至少有四个可分开研究的问题：Agent 有没有把关键环境状态取进上下文；它写下的计划有没有转成后续动作；中断或遇错后，系统能不能恢复；跨任务留下的记忆、技能和目标修订是否通过适当证据审查。

**CivBench** 和 **Argus** 分别照亮这条链的两侧。前者是长时间交互基准，将信息是否被主动查询、短期承诺是否兑现变成可观察行为；后者是多任务研究 runtime，将持久化状态、权限分工、review 和验证门控作为系统机制。它们不是同一任务上的两种方法，不能按分数横比，也不能合并成“长程 Agent 已解决”的证据。

## 先拆开四类可靠性构念

| 环节 | 问题 | 可观察证据 | 当前两篇工作的覆盖边界 |
|---|---|---|---|
| 状态监控 | 关键信息存在时，Agent 是否知道去查询？ | 工具查询轨迹、查询时机、可识别的漏检后果 | CivBench 明确区分信息可查询与被观察；Argus 管项目进展和证据，但未使用 PMR 这类应用内监控指标 |
| 计划兑现 | Agent 的明确意图是否变成目标动作？ | 带对象/目标的承诺与之后的执行记录 | CivBench 的 RAG@10 检查有界承诺；Argus 的任务交接、review 与 verifier 记录跨 mission 完成与修订 |
| 失败恢复 | 出错后能否定位、重试或撤销副作用？ | 故障定位、状态快照、重试差异、外部副作用 | 两篇不替代[长程执行恢复专题](long-horizon-execution-recovery.md)中的诊断、回滚与训练修正机制 |
| 经验持续 | 哪些经过验证的状态可用于下一个 mission？ | 带来源的 checkpoint、审查记录、可复用技能与后续任务表现 | Argus 把提交权限和证据门控纳入 runtime；跨状态更新的因果效应尚未通过 frozen-state replay 确认 |

这些指标互相影响，但不能互相替代：查询得多不代表查询正确；计划兑现率高不保证计划本身合理；恢复成功不证明记忆被正确保留；跨 mission 持续状态也不保证状态对新任务仍然有效。

## CivBench：让“没看见”成为可测的接口行为

CivBench 将 Civilization VI 包装成 MCP 工具环境，完整游戏有 300 多回合；结构化 narration layer 只返回 Agent 主动查询的状态。设计重点不是游戏分数，而是借助“存在但必须显式查询”的状态，观察长程监控行为。[论文 §3.2–3.3](../papers/2609.02459-civbench.md)

作者提出 PMR（Proactive Monitoring Rate）作为监控查询占工具调用的比例，并提出 Reflection–Action Gap @10：从 playbook diary 提取具体计划，检查 10 回合内是否执行。RAG 是该文对“反思—行动差距”的缩写，不是检索增强生成。它测的是明确的短期承诺兑现，不代表完整规划质量。[论文 §4.1–4.4、§6.1–6.2](../papers/2609.02459-civbench.md)

在 23 场可用游戏、四个模型家族的 pilot 中，作者报告多个家族普遍较少主动查询全局胜利状态，并出现明确计划未在后续行动中兑现的情况。作者将结果定位为固定 playbook 和少量运行下的描述性行为证据，而非模型排行榜；监控集合和 diary 解析方法本身也定义了这些指标能看见什么。[论文 §5.1–5.2、§6](../papers/2609.02459-civbench.md)

## Argus：把跨 session 连续性放进有权限的 runtime 状态

Argus 将长程工作切为 bounded missions，保持一个持久 campaign state，并由 Manager、Planner、Engineer、Reviewer 分担目标、任务、执行和验收。用户意图与当前 operational objective 分开；证据支持的目标修订要经过授权，memory、skill、verifier、routing 等可复用状态则由对应角色在 task-native evidence 后提交。[论文 §3.1–3.3、§4.1–4.4](../papers/2608.05144-argus.md)

它比 CivBench 更直接讨论跨 mission 状态、回滚和 review ownership；但其部署/工作流架构不能直接推导为所有任务都更可靠。论文的 benchmark 结果分属不同原生度量；SWE-Bench 长序列上的 token/time 变化是同一顺序任务轨迹中的观察，没有匹配的 frozen-state replay，作者也将其作为非因果的 longitudinal evidence。[论文 §5–6、§8](../papers/2608.05144-argus.md)

## 两类证据如何互补，哪些地方仍空着

| 设计问题 | CivBench 提供的证据 | Argus 提供的证据 | 还需要怎样的研究 |
|---|---|---|---|
| 关键状态是否被获取 | 可见的状态查询是否发生，以及漏查是否与失败相连 | 持久项目记录和 mission handoff 中有哪些状态和证据 | 同一 Agent 是否能在真实工具/GUI 任务中维持注意点，而不是只在 game API 结构里查询 |
| 计划是否落地 | diary commitments 与未来短窗口动作可对齐 | Planner 任务、Engineer artifacts、Reviewer verdict 可跨 mission 记录 | 把用户目标、计划子目标和副作用验证对齐，处理目标变化与环境改变 |
| 经验是否改善下一轮 | 在单 episode 内测轨迹行为，不测跨 campaign 学习 | 运行状态随着 campaign 更新，案例展示持久状态的可能价值 | 固定后续任务、冻结运行时状态作对照，测哪些 memory/skill/verifier 真正带来复用收益 |
| 验收是否可信 | 计划标签由 rubric/LLM pipeline 产生，外部游戏状态可检查 | Reviewer 与官方 verifier 的职责来源被记录 | 分别测试环境错误、规格错误与 judge 错误，避免 Agent 只学会满足当前 checker |

下一步更有价值的评测不只是延长轨迹：它应能回放或扰动关键状态，检验 Agent 是否及时获取；明确标注承诺、时间窗口和更新条件；追踪失败后的副作用与恢复；并用独立、任务原生检查判断状态是否可安全地延续到后续任务。若仅将任务步数加长，仍可能测到环境复杂度，却没有分辨监控、承诺、恢复和持久化的具体机制。

## 阅读路线

1. 先读主报告[Agent 系统综述](../report.md)中的长程记忆、工具生命周期和失败恢复，明确这篇分册补的是“监控/兑现/跨任务状态验证”。
2. 精读 [CivBench](../papers/2609.02459-civbench.md)，重点看 MCP narration、PMR、Reflection–Action Gap 以及样本与 playbook 限制。
3. 精读 [Argus](../papers/2608.05144-argus.md)，重点看 mission boundary、状态/角色权限和 verification-gated updates；只把纵向结果视作论文在该任务序列中的观察。
4. 回到[长程执行恢复](long-horizon-execution-recovery.md)比较诊断、回滚与训练期修正，再读[电脑使用 Agent](../../ComputerUse/report.md)和[评测科学](../../../Evaluation/EvaluationScience/report.md)理解环境状态与验收标准。

