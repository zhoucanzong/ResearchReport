# Terminal-Bench 2.0：命令行任务的最终状态怎样验收？

来源：Merrill et al., [*Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces*](https://arxiv.org/html/2601.11868v1)，arXiv v1（2026-01-17）。重点阅读 §2.1–2.3、§3.1–3.4、§4.3–4.5 与 Appendix B/C。

## 任务不是仓库 issue，而是带状态的 terminal 工作流

Terminal-Bench 任务由自然语言指令、Docker 环境、测试、人工写的参考解和时间上限组成。Agent 获得容器后可探索状态并调用 shell/工具；tests 检查**最终容器状态中的目标属性**，不要求复刻参考解的命令序列或 console output。这样设计允许多条合法执行路径，也把验收目标从 patch 相似度转为“任务说明的结果是否发生”。[§2.1](https://arxiv.org/html/2601.11868v1)

Terminal-Bench 2.0 的 89 项任务来自 93 名贡献者提交的 229 个候选，再由经验审阅者筛选。论文定义三项主要准入标准：

1. **Specificity**：tests 对指令描述的可接受终态既不能漏测，也不该误拒。
2. **Solvability**：oracle/reference solution 能在环境中完成任务并通过 tests。
3. **Integrity**：不能通过真实部署中不存在的捷径“作弊”，例如读取 git 历史中的未来修复。[§2.2–2.3](https://arxiv.org/html/2601.11868v1)

质量控制还包含自动运行 oracle、检查 no-op 是否失败、任务检查清单、LLM 辅助检查、模型试跑、adversarial exploit agent 和人工复审。作者报告平均每项最终任务约三小时审阅；这提高任务质量，但不是对所有有效解的数学证明。[§2.3、Appendix B](https://arxiv.org/html/2601.11868v1)

## “terminal benchmark”不等于“纯代码 benchmark”

Terminal-Bench 包含软件工程，也包含构建/运行系统、数据处理、视频处理、个人助理等 shell 工作流。Agent 不被强制只能使用一种命令；关键是在给定容器中通过可用接口完成状态变更。论文还允许把已有 benchmark 经 adapter 转成兼容格式，说明它既是任务集合，也是可扩展的评测框架。[§2.1、§2.4、Appendix D](https://arxiv.org/html/2601.11868v1)

这与 [SWE-bench](eval-swe-bench.md) 的任务单位不同：SWE-bench 从 GitHub issue 出发，验收仓库 patch 的测试结果；Terminal-Bench 从工作流指令出发，验收最终容器状态。相邻的 [TUA-Bench](https://arxiv.org/html/2606.28480v1) 将 terminal-use 扩到文档编辑、邮件、网页信息搜寻及科学/工程任务；它测的是更通用的 terminal 计算机使用能力，不应把其分数解读成仓库级代码修复能力。

## harness 让什么变成可比，什么仍混在一起

任务以 Harbor 格式定义并由 Harbor harness 执行；论文的比较矩阵包含不同模型与 agent scaffold，例如 Claude Code、Codex CLI、OpenHands、Mini-SWE-Agent 和作者的 Terminus 2。作者至少运行五次各受支持组合，并为可配置推理力度的模型使用提供方默认设置。由于同一个模型配不同 scaffold、同一 scaffold 配不同模型都会改变完成率，结果属于**模型 × scaffold × 任务容器 × 预算**，不是裸模型能力。[§3.1–3.4](https://arxiv.org/html/2601.11868v1)

Terminal-Bench 测的是是否达到终态属性；它不要求 Agent 使用唯一正确的命令路径，也不自动判断中间命令是否“像专业工程师”。测试质量的核心是“指令包含的所有重要结果是否被覆盖、是否容许所有正确实现”，而不是日志文本和参考命令是否相同。失败轨迹分析可以进一步诊断执行、连贯性、验证等问题，但这是独立的轨迹标注层，不能取代最终状态测试。[§2.1–2.3、§4.4、Appendix C](https://arxiv.org/html/2601.11868v1)

## 证据边界

- 作者为任务列出的 expert/junior completion time 是人的估计，不是模型运行预算或环境时钟的替代指标。
- 每项任务有 time limit，实际运行还涉及 agent scaffold、工具权限和容器 sandbox；换了时间上限或 scaffold，结果构念就变了。
- tests 检查被写明的最终状态；未写进 instruction/test 的质量、额外副作用或软约束不自动计分。
- 多次试验的成功率描述该模型与 agent 配置在该任务集上的表现，不能与只测 patch acceptance 的 SWE-bench 直接排成一个榜。

**带走的区别**：Terminal-Bench 的核心问题是“Agent 能否在一个可重置的终端容器里达到指令定义的最终状态”；它比仓库 issue 修复更宽，但也更依赖测试是否完整表达了可接受结果。
