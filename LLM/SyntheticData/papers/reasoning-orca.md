# Orca：以分阶段教师轨迹教学生解释复杂答案

来源：[Orca: Progressive Learning from Complex Explanation Traces of GPT-4](https://arxiv.org/html/2306.02707v1)，固定版本 v1。重点阅读 §3.1–§3.2、§4、§6–§8 与 case studies。

## 研究问题：小模型能否学会解题过程，而不只学老师的回答风格？

早期指令微调常用单轮问答或较浅的教师输出。Orca 把监督目标扩展到包含解释过程的回答（explanation tuning），并使用 FLAN-v2 等异质任务模板扩大任务覆盖。数据不是单一 teacher 输出表：作者先从多源任务取样并加入 system instruction，再用 ChatGPT 生成第一阶段 5M responses，并从中采样 1M 给 GPT-4 生成更强的解释，最后按 ChatGPT→GPT-4 阶段训练学生。[§3.1、§3.2](https://arxiv.org/html/2306.02707v1)

这一渐进安排把教师能力差距分成两步：中间教师先覆盖大量指令和任务样式，较强教师再为一个子集补更复杂的解释。它和纯粹增加最终教师答案数不同；作者报告 FLAN-5M 的 ChatGPT 阶段与 FLAN-1M 的 GPT-4 阶段分别承担训练覆盖与提升推理信号的角色。

## 合成解释带来什么，又没有直接证明什么

GPT-4 的 explanation traces 为学生提供比最终答案更丰富的监督，模型可以拟合中间步骤。论文在 BBH、AGIEval、专业考试等多个基准报告结果，讨论其对小模型推理的作用；这些数字是 13B Orca 在作者所构造的 FLAN 子集、系统提示和 zero-shot 评测条件下的结果，不能推为所有 teacher rationale 都能转化为可迁移推理能力。[摘要、§4–§7](https://arxiv.org/html/2306.02707v1)

最重要的评测边界来自作者对自动评价的批评：GPT-4 judge 容易偏好更长的回答，且结果受候选展示顺序影响；小模型可能学会模仿解释风格，却没有同等的理解/推理能力。其自身使用的 teacher-generated explanations 也可能传递教师错误、幻觉或模板偏差；评测分数与解释是否忠实仍要拆开看。

论文把中间 ChatGPT 教师加入训练的消融，报告在该 AGIEval 聚合设置下优于只用 GPT-4 数据的变体；作者将其解释为能力差距较小的中间教师能够桥接学习。该对照同时改变了 5M 与 1M 数据规模及教师分布，不能独立证明“课程顺序”或“更弱教师”是全部收益的因果来源。[§6、Table 10](https://arxiv.org/html/2306.02707v1)

## 与 STaR 和在线 RL 的区别

- [Orca](reasoning-orca.md) 本身是外部教师生成 explanation 的 SFT，样本由任务池、system prompts 和教师调用构造。
- [STaR](reasoning-star.md) 让学生从少量 rationale 示例开始自生成，再用数据标签过滤答案，并对失败问题做 rationalization。
- [ReST](reasoning-rest.md) 按 reward 对当前策略 rollout 进行 Grow–Improve，训练期反馈来自奖励模型，不是固定 teacher trace。
- 在线 RL 会持续针对更新后的策略重新采样；离线合成 SFT 样本静态复用，不代表策略已经通过环境或验证器试错。

Orca 的“复杂解释轨迹”是一种训练信号，不自动证明模型内部采用了相同推理算法。要评价合成推理数据，需分别检查教师监督质量、学生答案正确性、理由忠实度、任务迁移与评估器偏差。
