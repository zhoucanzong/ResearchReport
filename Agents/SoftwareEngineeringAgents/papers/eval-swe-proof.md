# SWE-Proof：测试全通过，离实现真正正确还有多远？

来源：Ma et al., [*SWE-Proof: Can Language Models Resolve Real-World Issues with Machine-Checked Proofs?*](https://arxiv.org/html/2609.21190v1)，arXiv v1（2026-09-18）。重点阅读 §2–§4、Appendix A–F，特别 specification、correctness gates、environment 与 budget。

## 一个过关 patch 未必与任务真正需要的行为等价

在 SWE-bench 类任务中，patch 通过隐藏测试就记为 resolved。这个判据可扩展，但有限测试只覆盖有限输入：错误实现可能对测试样例答对，却在未覆盖输入上偏离需求；测试写得过度具体也可能拒绝合理替代实现。SWE-Proof 将问题改写为：能否为真实 issue 建立可机检的规格，并验证 patch 是否满足该规格？[§1–§2](https://arxiv.org/html/2609.21190v1)

作者的 Benchproofer 从已知 gold patch 出发：为新行为构造 specification；为依赖但未改动的函数建立 axioms；通过机械检查和对抗审计后才将实例纳入 SWE-Proof。Agent 看到 issue、基础仓库和指定可见信息，在容器中修改代码并可运行公开 tests；形式 verifier 检查实现是否满足规格，另有审计者检查被验证实现是否与提交 patch 对应。[§2–§3、Appendix E–F](https://arxiv.org/html/2609.21190v1)

这比“跑一组隐藏 tests”增加了形式规格证据，但验证的是**给定规格与环境公理下的实现**，不是自动验证原始自然语言 issue。规格若遗漏要求，证明仍可能严格地证明了一个不完整的问题。对外部副作用、重命名或内部状态变化等行为，不同形式化后端能表达的语义也不同；论文报告有些任务无法被某些后端合理刻画。[§3.2–3.4、Appendix A/D](https://arxiv.org/html/2609.21190v1)

## 测试、规格和自写规格是不同的评测条件

论文在 SWE-bench Verified 上区分数种设置：只测官方 tests；对测试通过的 patch 再做对抗反例审计；允许 Agent 编写并验证自己的规格；或直接提供 ground-truth specification。作者报告，在其 500 个任务与两类模型的协议下，一部分只通过 tests 的 patch 会被额外反例推翻；提供正确规格能显著改善验证条件，而让 Agent 自己写规格并不稳定有益，因为规格可能遗漏需求或不忠于 issue 意图。[§4.1–4.6、Table 2](https://arxiv.org/html/2609.21190v1)

Table 2 的 tests-only 与 baseline+audit 对照显示，该结果依赖模型：Opus 4.8 在 500 个 SWE-bench Verified 实例上的分辨率从 85.0% 降至 58.2%（相差 26.8 个百分点）；GPT-5.5 从 81.2% 降至 33.4%。因此，正文所说的 26.8% 只对应 Opus 4.8 这一行，不能概括成所有模型的统一被推翻比例。审计通过构造“Agent patch 与参考 patch 输出不同”的输入来判定反例；它揭示测试未覆盖参考 patch 与候选 patch 的差异，不等同于对真实用户意图或所有合法替代修复的完备判决。[§4.2、Table 2](https://arxiv.org/html/2609.21190v1)

这组实验揭示四层不同主张：

1. **tests passed**：实现通过给定样例；
2. **specification verified**：实现满足形式化规格；
3. **specification faithful**：规格忠实包含 issue 要求；
4. **user need satisfied**：实际交付符合用户未必写全的意图和运行环境。

下层证据不能自动推出上层结论。形式证明能加强特定规格下的保证，但它也把问题移到规格是否完整、忠实和可审计。

## 和 SWE-bench、Terminal-Bench 的关系

[SWE-bench](eval-swe-bench.md) 用 `FAIL_TO_PASS` 和 `PASS_TO_PASS` 测试定义 issue 是否解决；[Terminal-Bench](eval-terminal-bench.md) 用任务测试检查最终容器状态，允许多种工具路径；SWE-Proof 在此基础上增加形式规格和 verifier。三者都可用容器与执行式判定，但测量强度与正确性主张不同。一个有缺陷的测试 suite 可能拒绝合理 patch，也可能接受满足测试但不满足需求的 patch；一个不忠实的 specification 也同样会给错误目标提供严格证明。

## 仍待解决的问题

- 如何从自然语言 issue 生成既完整又忠实的规格，而不要求用户预先写形式化需求？
- 规格需要对正确性、性能、安全、兼容行为分别约束到什么范围？
- 隐藏测试、形式证明和真实用户验收怎样共同覆盖不同错误？
- 当 issue 描述、现有行为、gold patch 和规格彼此冲突时，应如何确定 authoritative intent？

**带走的区别**：patch acceptance、tests passed、specification verified 和用户需求满足是不同层级。测试通过有实用价值但不证明完整正确；形式验证增强某项规格下的保证，但其力度取决于规格质量。
