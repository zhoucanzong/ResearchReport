# OpenHands：把代码 Agent、事件状态与沙箱运行时拆成平台接口

来源：[OpenDevin: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/html/2407.16741v1)，固定版本 v1（2024-07-23；后续项目更名 OpenHands）。重点阅读 §2.1–§2.4、§4.2.1–§4.2.2、Appendix E。

## 它回答的不是一个修复算法，而是“Agent 系统由哪些可替换部件组成”

OpenDevin（后来的 OpenHands）把平台分成 agent 实现、状态与事件流、runtime 环境、可扩展工具/skills、多 agent 委派和评估框架。某个 Agent 收到状态后产生活动；runtime 在沙箱操作系统、终端、Jupyter 或浏览器中执行；执行结果再转成 observation 并写回 event stream，供下一轮使用。[§2.1–§2.4](https://arxiv.org/html/2407.16741v1)

代码开发由此只是通用 Agent 能力的一种工作流：仓库修复可能调用终端、编辑工具和测试执行；浏览器任务则用不同技能和环境，但可以复用同一类 event/runtime 基础设施。论文的贡献主要是让不同 Agent、工具、环境和 UI 能接入同一平台，不是提出一个固定的仓库 bug 定位算法。

## event stream 怎样支持恢复和人类协作

状态包含按时间顺序记录的 actions、observations、用户指令和反馈等事件；它不只是聊天文本，而是运行时状态的一部分。Action 由 runtime 执行后产生 Observation，并与用户输入、错误信息等统一进入 event stream。UI 可以查看和追加事件，Agent 与执行环境也可替换而维持相同接口。[§2.1–§2.2](https://arxiv.org/html/2407.16741v1)

这种设计使“任务当前走到哪一步、刚才执行了什么、环境返回了什么”较易检查，也为人类反馈、多 Agent 委派与执行回放提供了平台基础。不过事件日志记录完整，不等于 Agent 能正确解释状态；安全沙箱限制了代码执行风险，也不证明运行中的工作流绝无外部副作用。要讨论可靠性，还需看具体 Agent 的策略和 evaluator。

## 论文评测支持什么

论文的平台评估覆盖 SWE-bench、HumanEvalFix、浏览器和其它通用任务，并展示多种 Agent 实现可以使用同一环境与评估入口。[§4.2](https://arxiv.org/html/2407.16741v1)

这些结果支持“平台可以承载多 Agent/多环境研究”这一软件框架主张，不是 OpenHands 某一软件工程 Agent 在所有代码仓库上的胜率保证。若比较软件修复能力，仍需固定 Agent scaffold、模型、容器、工具权限、任务版本、测试反馈和迭代预算；平台支持哪些基准并不等同于每个 Agent 都通过这些基准。

## 与 SWE-agent / Agentless 的关系

- **SWE-agent** 专门研究 ACI 如何改变 LM 的搜索、浏览、编辑和反馈利用；OpenHands 把 Agent—runtime—event 的连接抽象成平台。
- **Agentless** 证明固定的定位、候选 patch、验证管线可以在某些任务中作为强 baseline；OpenHands 则提供可以运行多种执行策略的环境和接口。
- 三者关注点分别是专用操作接口、分阶段 patch 生成/选择、以及可扩展 Agent 平台，不应只把它们按 SWE-bench 分数排序。
