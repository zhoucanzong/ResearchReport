# KITE：迭代指令调优中的合成数据怎样避免技能极化？

来源：Luo et al., [*Learning from Synthetic Data without Model Collapse in Iterative Instruction Tuning*](https://arxiv.org/html/2607.17043v1)，固定阅读版本 v1（2026-07-19）。重点读 §2–§4.6、§6，特别是失败诊断、候选生成、数据筛选、长程演化和限制。

## 问题：综合分数看似稳定，弱技能却可能持续退化

论文研究模型生成的指令被筛选后用于下一代指令微调时，模型能力怎样演化。作者不把 model collapse 只定义成总体分数下降，而观察到一种**技能极化**：合成数据可能继续强化已经较强的技能，同时削弱原本较弱的技能。用一个平均分衡量迭代结果，可能看不到这种相反变化。[Abstract、§1](https://arxiv.org/html/2607.17043v1)

这与从头预训练中真实/合成数据比例问题不同：KITE 研究的是按模型当前能力轮流生成和训练的 self-improving instruction-tuning 回路；合成指令分布直接受到模型已会什么、在哪些题上失败的影响。[§1–§2](https://arxiv.org/html/2607.17043v1)

## 两阶段方法：先找弱项，再选边界附近的数据

**第一阶段**从模型失败中建立候选任务库：用 DINA 类技能诊断估计能力画像，并以 failure-guided 提示生成候选指令；rank-based noise injection 把采样分布从模型最偏好的容易模式拉开。**第二阶段**使用 Kernel Boundary Uncertainty (KBU)，根据模型对候选答案的语义不确定度及 likelihood weighting，筛选更可能提供有效学习信号的样本。[§3.1–§3.3](https://arxiv.org/html/2607.17043v1)

这设计不等于“最高不确定样本最有价值”：高不确定可能来自噪声或不可解问题，低不确定也可能表示数据太容易。KITE 试图在模型现有能力边界附近挑数据；它的有效性依赖技能标注、生成分布、answer verification 和数据筛选信号。

## 论文报告的结果与适用条件

论文在多个开源模型和数学推理基准上报告，KITE 相比其合成数据基线能够更稳定地逐代提升；其九代 Llama-3.2-3B-Instruct 实验中，所测基准分数逐步提升并趋于饱和，没有出现该实验中的反转式退化。[§4.2、§4.4](https://arxiv.org/html/2607.17043v1)

非推理 WikiText 实验进一步显示，高温采样生成的数据在迭代自训练中使测试 perplexity 逐代上升，而 KITE 在其设置下保持稳定。[§4.5](https://arxiv.org/html/2607.17043v1) 这支持“生成策略和数据筛选会改变退化形态”，不能推广为 KITE 已解决所有模型崩塌：论文的 limitation 指出流程使用 GPT-5-mini 验证/归一化答案，因此更准确地说是**受强外部验证器辅助的自生成数据研究**，不是完全闭环、无外部教师的自我改进。[§6](https://arxiv.org/html/2607.17043v1)

## 与其它反馈循环研究的关系

- [The Curse of Recursion](feedback-recursive-model-collapse.md) 解释逐代模型输出怎样导致真实分布尾部丢失；它的核心情境和 KITE 的选择性指令迭代不同。
- [大规模预训练合成数据配比](feedback-pretraining-mixtures.md) 比较单轮预训练中改写/教科书数据与真实网页混合；它不测多代指令自训练。
- KITE 主要处理后训练中“当前策略会生成什么样的学习样本”；系统需要报告外部验证器、数据保留比例、迭代次数及跨技能变化。

重点定位： [arXiv v1 §3–§4](https://arxiv.org/html/2607.17043v1) 与 §6 Limitations。作者报告的性能只适用于论文所选模型、指令数据、验证器和迭代协议；本精读未复现或重算指标。
