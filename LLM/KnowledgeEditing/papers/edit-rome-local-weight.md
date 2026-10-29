# ROME：把一条事实写入 MLP 的 key–value 关联

来源：Meng et al., [*Locating and Editing Factual Associations in GPT*](https://arxiv.org/html/2202.05262v3)，arXiv v3（2022-06-01），ICLR 2023。建议读 §2.1–§2.3、§3.1–§3.6、Appendix B 与 E.5。

## 研究问题：能否只改主体—关系—宾语中的一个关联？

对提示 “The Space Needle is in …” 而言，模型需要把主体与关系映射到宾语。若原答案过时，直接微调整个模型可能同时改变同义问法和无关事实。ROME 将问题拆成两个可检验假设：事实回忆是否通过 subject token 进入中层 MLP；若是，能否对该 MLP 的权重做一次定向更新来改变这个关联？

## Causal tracing 提供候选位置，不等于证明知识只存于此

作者先给主体 token 加噪，使目标答案概率下降，再把干净运行中的某个中间激活替换回受噪运行。目标概率的恢复量用来估计这个状态对该预测的间接因果作用。论文在 GPT-2 XL 的事实样本上观察到，主体位置的中层 MLP 状态对答案恢复较关键；随后以 GPT-J 等模型检查相似模式。[§2.1–§2.3、Appendix B](https://arxiv.org/html/2202.05262v3)

这种实验定位的是给定提示、模型和干预中的信息路径，不是读取权重后直接看到“知识地址”。后续研究发现 Causal Tracing 的峰值层不一定是编辑成功的最佳层，甚至二者相关性很弱；所以定位实验应作为提出编辑假说的依据，而非该编辑方法的正确性证明。[Does Localization Inform Editing? §4–§6](https://arxiv.org/html/2301.04213v1)

## 方法：优化新 value，再以 rank-one 更新写入

ROME 把 MLP 看作线性联想记忆：输入主体的隐藏状态经过第一矩阵形成 key (k_*)，第二矩阵 (W_{mathrm{proj}}) 将 key 映射为 value。编辑时先优化目标向量 (v_*)，再求一个 rank-one 矩阵改变量，使 (W_{mathrm{proj}}k_*=v_*)；经验协方差项用于尽量减少对其它输入方向的改变。[§3.1、Figure 4、Appendix A](https://arxiv.org/html/2202.05262v3)

这条路线的优点是更新小、对象明确；其代价是必须选择层、目标表示和协方差近似，并假设该事实能被局部化为一个 key–value 关联。若答案依赖多跳推理、分布式表示或多个互相牵制的关联，单次 rank-one 写入未必能同步更新后果。

## 编辑效果不能只看原始提示是否答对

论文分别评估目标提示的 efficacy、改写提示的 generalization、相邻主体的 specificity，以及流畅度和语义一致性。CounterFact 的反事实问题比“改写成模型本来就较相信的答案”更严格；论文报告 ROME 在其 GPT-2 XL/GPT-J 设置下可在目标事实改对和保留邻近事实之间取得一定平衡。[§3.2–§3.6、Table 2](https://arxiv.org/html/2202.05262v3)

这不表示对任意事实、任务或持续更新流都能保持同样性质。MQuAKE 后来将评测扩展到编辑事实带来的多跳推论，发现局部事实可回忆并不保证相关 belief 一起更新；这说明“编辑成功”必须绑定到明确的能力测量。[MQuAKE §1、§3–§5](https://arxiv.org/html/2305.14795v1)

## 与相邻编辑方法的关系

- [MEMIT](edit-memit-mass.md) 扩展了关联记忆写入：把多条更新分配到一组 MLP 层，而不是逐事实单层写入。
- [MEND](edit-mend-hypernetwork.md) 不假设固定的事实存储位置，而训练编辑网络将新样本梯度转成更新。
- [WISE](edit-wise-side-memory.md) 把编辑知识隔离在可路由的 side memory，重心转向连续更新和回滚。

ROME 改的是基座权重，通常是持久更新；它既不是按请求 reset 的测试时适应，也不自动提供隐私删除或“遗忘某条训练数据”的保证。
