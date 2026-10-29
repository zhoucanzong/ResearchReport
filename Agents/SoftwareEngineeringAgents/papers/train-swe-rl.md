# SWE-RL：从软件演化记录学习修复策略，奖励却不执行代码

来源：Wei et al., [*SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software Evolution*](https://arxiv.org/html/2502.18449v1)，固定版本 v1（2025-02-25）。重点阅读 §2.1–§2.3、§3.1–§3.6，尤其 reward ablation 与 out-of-domain evaluation。

## 软件演化记录可以提供什么

一次 GitHub pull request（PR）通常包含 issue、讨论、代码快照、review 和最终 patch。SWE-RL 把这些记录拼成训练任务：从 PR 关联的 bug-fixing issue 得到自然语言需求，提供初始仓库上下文与 oracle patch，让模型生成自己的代码改动，再把改动与 oracle patch 比较形成 RL reward。[§2.1–§2.2](https://arxiv.org/html/2502.18449v1)

这种数据路线不需要为每条历史 PR 重新执行完整软件环境，但要求把多时点 Git 历史和 issue/PR 关系正确关联、去污染、抽取相关代码文件。作者提到先提供完整文件上下文，是为了让模型学会定位而非只仿写变更文件；然而相关文件集合和仓库历史快照的构造也会影响模型看到的问题。

## Patch similarity 是可微弱的 proxy，不是测试通过奖励

SWE-RL 用 Group Relative Policy Optimization 训练策略。对于格式错误输出给负奖励；格式正确时，奖励取生成 patch 与 oracle patch 的字符串相似度（Python `difflib.SequenceMatcher`）。连续相似分数比“patch 必须完全匹配”更能给近似修复提供梯度方向；作者在 reward ablation 中报告连续奖励优于离散 exact-match。[§2.2、§3.6](https://arxiv.org/html/2502.18449v1)

但同一 bug 可能有多种等价修复。与标准测试执行不同，patch 字符串相似度可能惩罚正确但结构不同的实现，也可能给与 oracle 写法相似但行为错误的 patch 一定奖励。它是在大规模历史 PR 上较便宜的优化代理，不等同于单元测试、代码审查或用户需求满足。

## 数据路线和训练目标共同决定证据

作者从大规模软件演化数据中筛出 PR，生成 issue + 代码上下文 + oracle patch 的 seed，再进行 GRPO。其“真实软件演化数据”并非完整交互轨迹：训练对象主要是 issue 到 patch 的映射，模型生成的过程并不需要逐轮使用工具、执行测试、修复报错。论文报告在 SWE-Bench Verified 和若干域外任务上获得结果；这些比较依赖其基座模型、prompt、patch 格式、SFT/RL 数据处理和评测设置。[§2、§3.1–§3.5](https://arxiv.org/html/2502.18449v1)

这与 SWE-Gym 的差别是监督接口而非“真实/合成”二分：SWE-Gym 的核心训练信号来自可执行环境与成功轨迹筛选；SWE-RL 用 PR 历史与 patch similarity 构建可扩展 RL 信号。前者测试的是环境反馈下的完整 Agent trajectory，后者主要优化生成 patch 与历史 oracle 的相似度。两种方法各自省略的部分不同：环境法受仓库安装和测试质量限制，PR 代理奖励则受唯一 oracle 写法限制。[SWE-Gym 对读](train-swe-gym.md)

## 泛化结果应怎样解释

SWE-RL 论文报告其模型在函数级编码、库使用、代码推理、数学与一般语言任务上优于自身基座或相应 SFT 基线；这是作者选择的模型、数据和 zero-shot greedy 设置下的域外评测，不证明 RL 在所有任务分布上都会提高通用推理能力。PR 数据中还含有广泛代码、提交信息和讨论，所谓“只在软件工程数据上训练”仍然依赖作者定义的数据池与去污染范围。[§3.5、Table 3](https://arxiv.org/html/2502.18449v1)

**带走的区别**：SWE-RL 证明了大规模软件演化记录可以支撑 RL 式 patch 学习；它没有把软件 Agent 训练成一个持续观察、执行测试、获取环境奖励并自行修复的交互系统。区分训练数据来源、策略优化目标与推理时 scaffold，才能判断 RL 到底改进了什么。
