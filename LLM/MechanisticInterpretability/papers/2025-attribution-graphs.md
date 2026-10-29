# On the Biology of a Large Language Model：归因图是机制假说，不是思维转录

来源：Anthropic，[On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)，2025-03-27；以及配套 [Circuit Tracing 方法文档](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)。阅读重点：Method Overview、case studies、Limitations、§7.7 Mechanistic Faithfulness。

## 从 feature catalogue 走向计算图

单独找出 “Texas” feature 只能说明模型在某处保留了与 Texas 有关的表示。要解释回答 “the capital of the state containing Dallas” 时模型为什么输出 Austin，还需追踪：Dallas 如何引出 Texas，Texas 如何影响 Austin 的输出 logit，其他平行路径是否同时参与。

Anthropic 用 cross-layer transcoders 近似原模型 MLP 输入—输出映射，再把某个 prompt 上的中间 feature、边和输出组成 attribution graph。研究者据图提出机制假说，再通过 feature inhibition/excitation 等干预检验。[Method Overview、case studies](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)

## 替换模型使图可读，也引入新的忠实度问题

Circuit tracing 不是直接把原模型内部“照相”出来。它先用可解释的 transcoders 替换部分 MLP 计算，再做归因。替换模型若能重建激活，也未必采用原模型相同的内部机制；因此要分开看：替换模型是否拟合数据、图中的 feature 是否可理解、干预结果是否符合图的预测、图是否能重现原模型的目标行为。

论文指出它没有解释所有注意力计算，图中可能有无法解释的 error nodes；对稀有或分布外概念，替换模型重建更容易失配；未激活和抑制性路径不容易从图中发现；论文展示的图有剪枝和人工标签；某些 perturbation 结果还会与图预测矛盾。[Biology 的 Limitations](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)；[Methods §7.7 Mechanistic Faithfulness](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)

## 能支持什么结论

这些案例支持在 Claude 3.5 Haiku 的特定提示上，研究者能构造可视化中间路径，并用干预测试部分 feature 的行为贡献。它们展示了机制研究可能补充黑盒评测和显式 chain-of-thought 的地方：例如输出前是否形成中间预测、不同路径是否相互竞争、口头解释是否忠实于内部计算。

它们不能证明 attribution graph 是模型完整的推理图、feature 标签就是完整“内部想法”，或被检查的安全行为已被一般性控制。论文自己报告了不忠实例子；因此图应被当作**能产生预测、也能被反例修订的研究对象**，不是供外部观察完整读心的接口。

## 阅读所得

与 SAE feature 研究相比，Circuit Tracing 把研究单位从单个字典方向推进到跨层路径；但路径可视化引入替换模型、边归因、剪枝和可读性筛选等新假设。每个结论都应标明基于原模型直接干预还是替换模型归因，以及 error nodes 占据什么位置。
