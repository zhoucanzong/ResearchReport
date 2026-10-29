# MEND：学习把编辑梯度变成局部权重更新

来源：Mitchell et al., [*Fast Model Editing at Scale*](https://arxiv.org/html/2110.11309v2)，arXiv v2（2022-06-13）。建议读 §2–§3、§5.1–§5.4 与 Appendix C.2。

## 问题：单个新答案的微调为什么会改坏其它回答？

模型编辑输入通常只有一对“问题—新答案”，但编辑希望模型在等价问法上也更新，同时保留无关输入的行为。普通微调只看编辑样本，容易把这个提示过拟合；KL 等 locality 正则可约束输出变化，却仍要反复计算完整模型梯度。MEND 把“如何更新权重”本身交给一个小型编辑网络学习。

## 方法：低秩梯度分解与双层训练

给定编辑样本，先照常对基座模型做前向/反向，取得可编辑权重矩阵的梯度。MEND 以低秩分解压缩高维梯度结构，再由每层的小网络变换激活与梯度，产出一个近似 rank-one 的权重改变量。编辑器本身先在编辑数据集上训练；其训练损失同时奖励编辑输入及改写成功，并以 locality 样本上的预测分布 KL 约束无关行为。[§3、Algorithm 1–2](https://arxiv.org/html/2110.11309v2)

这和 ROME 不同：ROME 为“事实在哪里”提出结构假设并构造解析式更新；MEND 学“面对编辑梯度时怎样改参数”，无需假定每条知识都存放在同一特定层。它也不同于一次性 fine-tuning：部署时的更新由预先训练的 editor 生成，但最终改动仍落在基座模型的权重上。

## 快速编辑不等于零训练成本或零副作用

作者在 GPT-Neo、GPT-J、T5-XL、T5-XXL 等编辑设置中评估 MEND，并报告对参数量 11B 的 T5-XXL 仍能应用其编辑方法；这受其 NQ/QA、Wikitext 等任务、训练好的 editor、硬件精度与数据协议限定。[§5.1、Table 3、Appendix C.3](https://arxiv.org/html/2110.11309v2)

编辑器需要先从代表性 edit/locality 数据中学到更新规律，因此“测试时只给一对编辑输入”不代表无需训练数据、无需预先训练 editor 或可直接迁移到任意领域。Locality 项也用数据集样本近似模型输出分布 KL，而不是对模型全部可能输入做穷举；原文明确这是计算近似。[Appendix C.2](https://arxiv.org/html/2110.11309v2)

## 与其他编辑和记忆路线的关系

- [ROME](edit-rome-local-weight.md) 将 subject key 映射到新 value；MEND 则用学出的变换器处理编辑梯度。
- [MEMIT](edit-memit-mass.md) 把许多事实同时作为矩阵写入目标；MEND 的关键贡献是编辑器可以快速为新 edit pair 预测权重更新。
- [WISE](edit-wise-side-memory.md) 把编辑放入可独立选择的 side memory，以便管理长期更新；MEND 的普通形式修改被选中的主模型权重，撤销仍需要保留/恢复参数状态。

MEND 的编辑成功、locality 和规模指标都依赖其任务定义。局部单事实更新成功不等于多跳后果正确，也不等于满足训练数据删除、用户隐私删除或法律意义上的 machine unlearning。
