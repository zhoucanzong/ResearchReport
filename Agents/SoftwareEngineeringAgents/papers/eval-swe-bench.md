# SWE-bench：把 GitHub issue 变成 patch 与测试通过任务

来源：Jimenez et al., [*SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*](https://arxiv.org/html/2310.06770v2)，arXiv v2（2024-04-05）。重点阅读 §2、Appendix A.2–A.5，尤其 Execution-Based Validation 与 Evaluation Procedure。

## 它测量的不是短代码补全

HumanEval 一类基准给出相对封闭的函数规格，模型生成函数后可以直接跑输入输出测试。SWE-bench 把任务换成真实仓库中的 issue：模型看到问题描述和提交前的代码快照，需要产生一个 patch。问题可能要求跨函数或跨文件理解，测试则来自解决原 issue 的 pull request（PR）。因此任务单位是 **issue + 基础仓库状态 + 测试**，不是从零生成一个孤立代码片段。[§1–2](https://arxiv.org/html/2310.06770v2)

原论文从已合并 PR 构造候选：PR 必须关联一个或多个 issue，并新增测试。模型看到的是 PR 初始提交前的 issue 标题、描述和评论；代码状态锁定在 PR 的 base commit。测试 patch 与 gold patch 分开保存，避免把正确解直接给模型。[Appendix A.1–A.2](https://arxiv.org/html/2310.06770v2)

## harness 如何把“修好 issue”变成可重放判据

每个实例对应一个仓库 release context，而不是一个不分版本的通用 Python 环境。论文选择 release 级环境作为折中：实例级环境更贴合依赖，但人工维护量大；仓库当前版本又常与旧 PR 的 Python/依赖不兼容。每次评价时，harness 清理上一次文件变更，检出 base commit，激活相应执行环境、安装仓库、打上 test patch，再应用模型 patch 并执行测试脚本。[Appendix A.3–A.4](https://arxiv.org/html/2310.06770v2)

原文把测试结果整理成四类状态：`FAIL_TO_PASS` 是 gold 修复后新通过的测试；`PASS_TO_PASS` 是修复前后都应保持通过的测试；另有 `FAIL_TO_FAIL` 与 `PASS_TO_FAIL` 记录失败或回归。模型 patch 必须成功应用，而且所有 `FAIL_TO_PASS` 与 `PASS_TO_PASS` 测试通过，才记作该实例 resolved；自动修复 patch 格式失败只限于移除不必要上下文和重算 hunk header，仍失败则计零。[Appendix A.2–A.4](https://arxiv.org/html/2310.06770v2)

这不是要求预测 patch 与 gold patch 文本相同。不同 patch 只要满足 harness 指定的测试映射，都可能通过；因此分数是**在该测试集上的 resolved rate**，不是代码与人工 gold patch 的相似度，也不是 GitHub 维护者接受 patch 的概率。

## SWE-bench Verified 改善的是筛选，不是形式正确性

SWE-bench Verified 是原测试集的人工筛选子集。OpenAI 与 SWE-bench 作者合作，由 93 位有 Python 经验的开发者审阅 1,699 个随机样本，按 issue 是否欠明确、`FAIL_TO_PASS` 测试是否会错拒合理实现等标准，筛出 500 条任务。它降低了一部分可预见的题目/测试问题，**不是形式验证，也不保证余下测试完全充分**。[OpenAI 官方说明（2024）](https://openai.com/index/introducing-swe-bench-verified/)

后续官方复审进一步说明这个边界仍重要：OpenAI 抽查 o3 在 64 次独立运行中不稳定解决的 138 条 Verified 任务，报告其中 59.4% 有影响判定的测试或问题描述问题，并指出公开 GitHub 任务还存在训练污染风险。该审计针对一个按“模型不稳定解决”筛出的子集与其复审流程；它不意味着 Verified 全部 500 条都有问题。[OpenAI 官方复审说明（2026）](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)

## 这项判据能证实什么，不能证实什么

- `FAIL_TO_PASS` 通过说明 patch 满足了这批针对 issue 的新测试；`PASS_TO_PASS` 通过说明已保留这批回归测试所检查的行为。
- 它不能证明所有未测输入都正确，也不能证明非功能目标、性能、代码风格、兼容性或维护者意图都满足。
- 基准从公开 issue/PR 建构，带来时间切分、重复描述与预训练污染的可能；“issue 发生在 cutoff 之后”也需看具体语料和模型训练数据，不能靠日期字段一概排除。
- 通过率依赖 patch 生成格式、自动修补、环境版本、任务预算和 agent scaffold；比较时要把这些条件一起说明。

与 [Terminal-Bench](eval-terminal-bench.md) 相比，SWE-bench 的问题语义来自 issue、主要产物是仓库 patch；与 [SWE-Proof](eval-swe-proof.md) 相比，它以有限测试验收，不要求给 patch 建立形式规格。三者的容器和测试相似，但任务构念与正确性主张不同。

**带走的区别**：引用 SWE-bench 成绩时，说清楚它是哪个子集/版本、什么 harness、模型与 scaffold、尝试预算，以及通过了哪一组测试；“resolved”不自动等于 patch 完全实现需求或可直接合并上线。

## 固定源码的交叉定位

为区分论文中的评测定义与当前 runner 实现，另抽查官方 SWE-bench 仓库 `v5.0.1`（commit `87ab1f6ced28f75ba73ca899dc759b019310944a`）。该版本 [`run_evaluation.py`](https://github.com/SWE-bench/SWE-bench/blob/87ab1f6ced28f75ba73ca899dc759b019310944a/swebench/harness/run_evaluation.py#L280-L338) 在容器内尝试应用模型 patch，并保留失败日志；[`grading.py`](https://github.com/SWE-bench/SWE-bench/blob/87ab1f6ced28f75ba73ca899dc759b019310944a/swebench/harness/grading.py#L195-L258) 将 FAIL_TO_PASS 的 resolution 与 PASS_TO_PASS 的 maintenance 分开统计。这个 SHA 是当前源码交叉阅读版本，不应倒写成 arXiv v2 论文的原始实现版本。
