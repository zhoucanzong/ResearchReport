# Demystifying Synthetic Data：预训练中的合成数据何时有益？

来源：Kang et al., [*Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling Laws, Benefits, and Pitfalls*](https://arxiv.org/html/2510.01631v1)，固定阅读版本 v1（2025-10-02）。重点阅读 §3–§5、§7，尤其是两类生成方式、mixture ratio 搜索和单轮 model-collapse 讨论。

## 研究问题：合成数据不是一种同质材料

论文区分两种预训练数据：**web rephrasing** 以真实网页文本为底稿，让模型改写以期增加表达多样性；**synthetic textbooks** 则由模型直接生成教学式、主题组织的文本。二者的来源、目标和分布范围不同，因此“合成数据有用/有害”的笼统判断会掩盖关键条件。[§3.1–§3.2](https://arxiv.org/html/2510.01631v1)

作者在统一训练协议下比较自然网页文本、不同合成类型及其混合。研究规模包括超过一千个语言模型变体，模型最大 3B、训练数据预算最高 200B tokens；这为其 scaling 分析提供了比小型单任务微调更广的对照，但并未覆盖当前 frontier 模型规模或长期多代自训练。[Abstract、§4.1–§4.1.2](https://arxiv.org/html/2510.01631v1)

## 混合结果：改写与纯生成文本给出不同证据

论文报告在较大数据预算下，约三分之一的改写合成文本与三分之二自然网页文本混合，达到相同验证损失所需的数据量可减少；但**只用改写文本**并不比自然网页更快。纯生成 textbook-style 文本单独预训练时，在若干下游领域出现较高损失，尤其在小预算条件下。[Abstract、§4.2–§4.3](https://arxiv.org/html/2510.01631v1)

作者还搜索不同模型规模和 token 预算下的合成比例，观察到改写数据的“较好配比”在其设置中约向 30% 收敛；QA-style 与 textbook 类型的最佳比例则随规模和预算变化。这里的 30% 是该研究数据类型、CommonCrawl 基线、模型尺度和验证损失定义下的经验结果，**不是可迁移到所有语料的处方**。[§5.1、Figure 4](https://arxiv.org/html/2510.01631v1)

数据贡献不能仅用生成器参数规模解释：作者报告更大的生成器并不必然产出更好的预训练语料；低层统计分析也未能单独解释不同数据的下游效果。这支持读者把生成任务、过滤、真实数据保留和训练预算一起看，而不是用“teacher 更大”替代数据质量分析。[§5.2–§5.3](https://arxiv.org/html/2510.01631v1)

## 它如何限定“模型崩塌”争论

研究只测试**单轮（n=1）**合成数据预训练，而经典递归崩塌研究测试多代模型输出逐步成为后代训练数据。作者在单轮设定下发现：rephrased synthetic data 未显示可预见尺度上的性能退化；textbook-style 纯生成或部分混合则在特定数据预算/下游领域呈现与崩塌预测相符的模式。论文强调这些结果是混合证据，且仅涉及三种生成类型、最多 3B 参数和 200B token。[§7、Limitations](https://arxiv.org/html/2510.01631v1)

因此它的关键贡献是把问题从“合成数据会不会崩塌”细化为：**哪种合成机制、占比多少、与什么真实语料混合、在何种模型和 token 预算下，优化了什么目标？** 论文使用的核心训练指标包括验证损失和 scaling-law 拟合，不能直接代表指令遵循、事实性、安全或分布外推理的全面效用。

## 与递归指令微调的关系

预训练的改写/教科书配比与后训练的自生成指令、回答或推理轨迹不能混成一种“synthetic data ratio”。后者每一代往往以模型能力与验证器共同决定候选，可能产生技能偏置；见[迭代指令调优中的合成数据](feedback-iterative-instruction.md)。

重点定位： [arXiv v1 §3–§5、§7](https://arxiv.org/html/2510.01631v1)，尤其 §5.1 mixture ratio、§5.2 generator capability 与 §7 单轮崩塌范围。
