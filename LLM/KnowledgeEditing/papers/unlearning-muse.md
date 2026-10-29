# MUSE：把遗忘评测扩展到数据拥有者与模型部署者的六项要求

来源：[MUSE: Machine Unlearning Six-Way Evaluation for Language Models](https://arxiv.org/html/2407.06460v2)，固定版本 v2。重点阅读 §2–§5，尤其 §3.1 的指标定义、§4 的方法族和 §5.2–§5.3 的结果。

## 从“答不上来”扩展到完整的删除要求

MUSE 认为，删除请求同时涉及数据拥有者和模型部署者的不同要求。数据拥有者关心：模型是否复述原文、是否仍保留原文事实、是否仍泄漏某条数据曾进入训练集；部署者还要关心保留数据上的任务效用、删除请求扩大时是否可扩展，以及多次顺序请求后效果是否保持。因此它把遗忘评价拆成六项：verbatim memorization、knowledge memorization、privacy leakage、utility preservation、scalability、sustainability。[§1、§3.1](https://arxiv.org/html/2407.06460v2)

数据设计也把“原文记忆”和“知识记忆”分开：News 集合用 BBC 新闻文章；Books 集合以 Harry Potter 原书作 forget set、相关 FanWiki 文本作 retain set；从文本片段生成问答，用于测试模型是否仍能回答其中知识。membership-inference 指标则比较 forget 与 holdout 样本的可辨识性。论文报告两个数据语料中 forget set 为 0.8M 与 3.3M tokens；这些是指定语料构造规模，不等于涵盖了真实用户删除请求的全部规模或结构。[§3.2](https://arxiv.org/html/2407.06460v2)

## 方法为何在不同指标间拉扯

MUSE 比较八种近似遗忘算法，覆盖 Gradient Ascent、Negative Preference Optimization、Task Vector、Who’s Harry Potter，以及对部分方法增加 retain-set 梯度或 KL 正则。设计轴很清楚：对 forget set 降低模型目标知识/复述能力，与 retain set 上保持原模型分布或继续训练之间存在冲突；Task Vector/WHP 用强化模型与原模型的差值来构造删除效果，则另有“强化出来的方向是否只对应目标知识”的问题。[§4](https://arxiv.org/html/2407.06460v2)

论文结果显示，某些方法能让常规逐字复述和知识问答指标很低，却同时破坏保留效用，或仍留下 membership leakage；逐次删除和扩大 forget set 也会带来新的问题。因此一个低 forget score 不能直接解释成隐私信息已删除，必须同时与 retraining 参照、membership test、保留能力和顺序请求一起看。[§5.2–§5.3](https://arxiv.org/html/2407.06460v2)

## MUSE 与 TOFU 测的是不同层面

TOFU 的虚构作者数据适合检查受控、实体级问答知识如何在遗忘时影响相关 retain set；MUSE 用真实新闻/图书语料及衍生 QA 扩展到逐字记忆、会员推断、规模与连续删除请求。前者容易控制知识来源，后者覆盖更广的部署属性；两者都不等于对真实机构数据执行删除并证明法律意义上的完全抹除。

## 证据边界

- MUSE 的案例是 Harry Potter 书籍和 BBC 新闻；不同领域的事实关联、隐私结构和删除请求无法由这两类语料穷尽。
- membership-inference AUC 是特定攻击/判别器下的泄漏测量，不能证明所有攻击者均无法识别成员。
- retraining 是该实验中的参照模型；近似行为接近某个参照并不自动构成对训练过程完全等价的形式化保证。
- 论文测的是给定模型、方法、forget/retain/holdout 划分和训练设置下的性质，不应把某方法在一项指标上的优势概括成“已解决机器遗忘”。

**带走的区别**：MUSE 的核心贡献是提醒评测必须多维且面向利益相关方，而非只问模型是否拒答。六项性质不能压成一个分数；应明确当前任务想保护的是内容不复述、事实不再可答、成员关系不可识别，还是部署效用与顺序请求能力。
