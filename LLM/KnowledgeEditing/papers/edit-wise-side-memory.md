# WISE：为持续知识编辑增加可路由的 side memory

来源：Wang et al., [*WISE: Rethinking the Knowledge Memory for Lifelong Model Editing of Large Language Models*](https://arxiv.org/html/2405.14768v2)，arXiv v2（2024-10-07）。建议读 §2.1–§2.3、§3.1–§3.3、§5 与 Appendix B.1。

## 为什么单事实编辑的成功不足以说明可持续更新？

模型在多次知识更新中需要同时做到：新事实可被回忆（reliability）、同义问法能泛化（generalization）、无关旧知识不被改变（locality）。直接改主权重可能与预训练参数及旧编辑冲突；纯外部检索又可能让模型只复制相关文本，难以泛化。WISE 把“编辑知识存在哪里”作为长期编辑的核心设计问题。

论文所称 reliability/generalization/locality 的“impossible triangle”是对其 benchmark、模型和连续编辑协议的实验观察与研究假设，不是普遍数学不可能性证明。[§2.2、Figure 1](https://arxiv.org/html/2405.14768v2)

## 方法：保留 main memory，单独编辑 side memory

WISE 在目标 FFN 的 value matrix 上建立 side memory 副本，主模型参数保留预训练 memory；查询时计算一个 activation-based routing signal，在主记忆与侧记忆之间选择。多批编辑通过 knowledge sharding 放入不同的参数子空间，再按规则 merge，以降低新旧编辑冲突。[§2.3.1–§2.3.2](https://arxiv.org/html/2405.14768v2)

它不是普通 RAG：侧记忆仍以参数矩阵形式参与 FFN 计算，而非仅将文档追加到 prompt；同时也不是直接覆盖主模型权重。这个隔离结构让编辑更容易被禁用、回滚或合并，但仍要求路由器识别编辑适用的语义范围。

## 作者证据与已知边界

论文在 ZsRE、CounterFact、hallucination 和 temporal 设置中测试持续编辑，并报告 LLaMA-2-7B 上 100 次连续编辑的 reliability、generalization 与 locality 对照。适读结论是：在这些实验协议下，主记忆/侧记忆分离和路由可缓和部分连续编辑冲突；不同任务、模型和评价器并不等同于开放世界更新。[§3.1–§3.3](https://arxiv.org/html/2405.14768v2)

作者指出 side-memory retrieval 还未达到 oracle，且 WISE-Retrieve 的推理时间会随编辑流增长。[§5](https://arxiv.org/html/2405.14768v2) 因而“可撤销”不意味着“检索一定正确”，也不消除路由错误、重复事实、冲突事实和内存规模带来的代价。side memory 的撤下也不同于从预训练参数中删除某个样本的影响。

## 与 ROME、MEMIT、MEND 的关系

| 路线 | 编辑位置/更新 | 适合解释的问题 | 典型边界 |
| :-- | :-- | :-- | :-- |
| [ROME](edit-rome-local-weight.md) | 直接改一层 MLP 的 rank-one 方向 | 单事实如何局部写入 | 定位假设和邻近事实影响 |
| [MEMIT](edit-memit-mass.md) | 多层批量残差写入 | 多条事实如何共同更新 | 冲突与多跳传播未自动解决 |
| [MEND](edit-mend-hypernetwork.md) | 学习 gradient-to-update 编辑器 | 如何由单个新样本快速生成更新 | 需预训练 editor、locality 依赖近似样本 |
| WISE | 主模型 + 可路由侧记忆 | 如何隔离、持续管理更新 | 路由准确、编辑容量与长期检索成本 |

这些方法的共同目标是修改推理行为；要声称模型“忘记”了某项训练知识，还需规定删除对象和可验证的遗忘标准，不能将编辑 benchmark 成绩当作 unlearning 保证。
