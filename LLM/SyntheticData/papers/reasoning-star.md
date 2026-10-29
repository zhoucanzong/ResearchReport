# STaR：正确答案过滤与答案提示下的 rationale bootstrapping

来源：[STaR: Self-Taught Reasoner](https://arxiv.org/html/2203.14465v1)，固定版本 v1。重点阅读 §3.1–§3.2、§4.1–§4.4、§5 与 Appendix A。

## 研究问题：没有大规模人工 rationale，模型怎样学会逐步推理？

早期 chain-of-thought 微调依赖人工或模板化推理过程；few-shot rationale 可以诱发中间步骤，但通常弱于训练样本充足的微调模型。STaR 的出发点是利用现有模型的部分推理能力：模型先给无 rationale 数据生成解释和答案，再利用数据自带的正确答案筛选训练信号。

## 机制：生成—筛选—重训，并对失败题做 rationalization

STaR 每轮包含两个数据来源：

1. **自举生成**：给基座模型少量示例，对训练问题生成 rationale 与最终答案；只保留最终答案匹配数据集标签的样本。
2. **Rationalization**：对于模型答错的问题，把正确答案作为提示，让模型反向构造能导出该答案的 rationale；过滤后训练时去掉答案提示，再与第一类数据合并。

这样，原本“模型答不出来就没有监督”的问题，变为“标签给答案，模型尝试补出可学习解释”。原论文每轮从原始预训练模型重新开始微调，而非在上轮 finetuned checkpoint 上无限追加训练，意在缓解对不断缩小数据子集的过拟合。[§3.1–§3.2、Algorithm 1–2](https://arxiv.org/html/2203.14465v1)

它不是在线 RL：正确答案标签提供的是外部筛选判据，训练阶段用过滤后的 rationale 做监督微调；也不是完全无教师，少量 rationale 示例仍给出格式与推理样式。相较通用教师数据蒸馏，STaR 的大部分 rationale 由学生自身生成，答案标签决定哪些轨迹进入训练集。

## 答案正确不保证 rationale 忠实或有效

标签过滤只验证最终答案，不检查每个中间推理步骤是否真实支持答案。论文列出的错误案例中，有些答案正确但理由循环、把题目本身当证据，或用了不成立的常识连接；多选题还可能存在多个技术上可行的答案。Rationalization 的答案提示能增加困难题的训练覆盖，但它也可能让模型事后拼接一条看似合理的解释，而非暴露模型原先的求解过程。[§4.4、§5、Appendix A](https://arxiv.org/html/2203.14465v1)

作者在 GPT-J 6B 上测试算术和 CommonsenseQA，并报告迭代 STaR 相较直接答案微调和 few-shot rationale 设置有改进；结果只支持这些基座、任务、提示和过滤协议，不证明所有正确答案筛选得到的 rationale 都有因果效用。作者也指出，rationalization 的数据扩增与反向求解能力各自贡献难以完全隔离。[§4、§5](https://arxiv.org/html/2203.14465v1)

## 与教师蒸馏和 ReST 的关系

- [Orca](reasoning-orca.md) 让外部较强模型提供丰富 explanation traces；STaR 则主要让学生生成轨迹，用题目答案过滤并为失败样本补 rationalization。
- [ReST](reasoning-rest.md) 生成候选后用 reward model 排序/过滤，再反复 Improve；它是偏好对齐中的离线 Grow–Improve 循环，不等同于 STaR 的真值答案筛选。
- 现代推理模型的可验证奖励训练进一步把奖励连接到策略更新；具体 RL 回路见[强化学习专题](../../ReinforcementLearning/report.md)和 [DeepSeek-R1 报告](../../../Models/DeepSeek/report.md)。

**带走的判断**：STaR 关键贡献是把“答案标签”和“解释轨迹”拆成不同监督来源，让标签负责筛选、模型负责补出 rationale。评估学习收益时应同时检查答案准确率与解释忠实度，不能只因 CoT 样本变多就推断推理过程变可靠。
