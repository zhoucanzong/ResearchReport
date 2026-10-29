# SWE-Gym：把可执行仓库环境变成 Agent 的训练反馈

来源：Pan et al., [*Training Software Engineering Agents and Verifiers with SWE-Gym*](https://arxiv.org/html/2412.21139v1)，固定版本 v1（2024-12-30）。重点阅读 §2.1、§3.1–§3.3、§4.1–§4.2 和 Appendix B.3–B.5。

## 问题：代码任务有答案文件，却未必有可学习的环境

SWE-Bench 的训练 split 提供 GitHub issue 和修复 patch，但 patch 本身不是交互奖励：模型在仓库里搜索、改文件、运行命令后，训练器还需要知道这条轨迹是否真的修好了问题。若缺少依赖齐全的运行环境、可复现测试和任务初态，测试结果就很难作为稳定反馈。

SWE-Gym 把任务组织为自然语言 issue、代码快照、预装依赖的可执行环境和单元测试。论文从真实 Python 仓库的 issue/PR 记录抽取任务；原始集覆盖的仓库比最终可执行环境多，最后的 2,438 个环境经过了额外的人工安装和测试验证。关键并不是样本数，而是让同一个 Agent 轨迹包含观察（issue、命令输出、错误）与动作（搜索、编辑、执行），并可在任务终态运行测试。[§2.1–§2.3](https://arxiv.org/html/2412.21139v1)

## 训练反馈：成功轨迹筛选是 SFT，不等同在线 RL

论文的通用 OpenHands 配置以更强模型或当前学生采样 Agent 轨迹，只保留测试成功的轨迹，再用负对数似然训练学生模仿它们。这是 rejection-sampling fine-tuning / filtered behavior cloning：环境测试给轨迹成败信号，训练更新本身是监督模仿，不是根据每步奖励在线做 policy-gradient RL。[§3.1–§3.2](https://arxiv.org/html/2412.21139v1)

这条流程把“代码能否运行”变成可监督的轨迹筛选，但成功/失败标签仍受测试覆盖限制：通过测试不保证修复了所有真实需求，失败也可能来自环境初始化、测试脆弱、工具使用或时间预算，而非代码推理本身。于是环境构造、测试质量和 Agent scaffold 一起决定训练信号。

论文还报告一个重要负例：通用提示 Agent 从成功 off-policy 轨迹训练后继续采自己的 on-policy 轨迹，简单重采样微调并未持续改善；限制了动作空间的 Moatless 工作流配置却出现一定的自改进。这个差异提示，数据可以是成功的，但当前策略是否能在自己的交互分布中采到可学习的新成功轨迹，是另一问题；“加上 on-policy 轨迹”不自动等于有效 RL。[§3.2–§3.3](https://arxiv.org/html/2412.21139v1)

## Verifier：测试可以筛选，也可以学成轨迹评分器

SWE-Gym 用已执行的测试给轨迹构造成功/失败标签，再训练 outcome reward model 对候选轨迹估计成功概率；推理时采样多条修复轨迹，由 verifier 排序。这是把**训练环境中可执行的单测反馈**蒸馏成**推理时可用的轨迹排序器**，所以 verifier 训练数据要覆盖不同 Agent scaffold 和成功/失败轨迹。[§4.1](https://arxiv.org/html/2412.21139v1)

作者的消融发现，把 off-policy 教师轨迹与 on-policy 学生轨迹混合，对其 verifier 比只用单一来源更有帮助；但该结论限定在 Qwen2.5-Coder、OpenHands/Moatless scaffold、其轨迹采样和 SWE-Bench 评测设置。verifier 学的是“根据看到的轨迹预测测试成功”，并不证明它理解用户意图或能识别测试漏测的缺陷。

## 阅读边界

- **环境既是数据工厂，也是测试假设。** 最终训练环境集中在 11 个 Python 仓库，且环境安装和测试验证需要人工工作；不能从该集合推断任意语言/仓库都能同样自动化。
- **轨迹数、成功率和策略更新是三件事。** 成功轨迹 SFT 证明能模仿筛选出的行为，不等于在线 RL 收敛或自动自我改进。
- **Verifier 是二级模型。** 它从测试执行标签中学成功预测；若测试不完整或轨迹分布变化，其概率未必等于真实软件正确性。
- **分数属于完整系统。** Qwen 模型、OpenHands 或 Moatless scaffold、任务集、交互预算与执行环境共同影响 resolve rate，不能只归因于基座权重。

带走的设计原则是：Repository-level agent 训练需要一个可重复、能执行的任务环境；但“测试 pass”只是奖励接口，测试覆盖质量决定了它能代表多少真实需求。
