# 跨语言越狱评测：攻击和防御会不会随语言改变？

来源：Atil, Passonneau, and Morstatter, [*Do Methods to Jailbreak and Defend LLMs Generalize Across Languages?*](https://arxiv.org/html/2511.00689v1)，arXiv v1（2025-11-01）。重点阅读 §3–§4、§6，尤其 Safety Evaluation 和 limitations。

## 将 HarmBench/AdvBench 提示迁移到十种语言

该研究在六个模型上评估 HarmBench 与 AdvBench 的有害请求，覆盖高、中、低资源十种语言，并比较标准提示、逻辑表达攻击和优化式 prompt 攻击。其逻辑表达方法将有害问题转成谓词形式，再翻译谓词名称；prompt-based 攻击则把为目标模型优化的提示策略迁移到其他语言。研究对象因而不只是“机器翻译后模型是否拒绝”，还包括攻击形式和防御在语言间的迁移。[§3.1–§3.4](https://arxiv.org/html/2511.00689v1)

论文在其模型、数据集和攻击协议下观察到，不同语言的 unsafe response rate 会随攻击方法改变而重新排序：标准查询下某些高资源语言更安全，但逻辑表达或优化式攻击下未必如此；不存在一个跨模型、跨提示都最安全的语言。这说明“英语安全”不能代替跨语言测试，也说明语言资源等级不是单独、稳定的风险排序。[§4.1–§4.5](https://arxiv.org/html/2511.00689v1)

## Judge 和人工核验也有语言边界

作者用 GPT-4o 将回答标为 safe、unsafe 或 invalid，并报告 unsafe rate 时剔除 invalid；随后每种语言抽样 100 个回答，由可靠母语者核查，报告 Krippendorff’s alpha。由于 “invalid” 不等于安全，排除它会改变分母和观察结果；作者也明确指出低资源语言的人工标注尚不完整，且十种语言不能代表数千种语言。[§3.5、§6](https://arxiv.org/html/2511.00689v1)

这让跨语言安全评测出现两层偏差：一是模型对语言和脚本的支持不均，二是自动裁判及人工标注本身在低资源语言上的可靠性变化。统一翻译回英语并不自动解决测量问题，因为翻译可能抹掉冒犯方式、语用含义和攻击变体；但直接使用多语种 judge 也要报告原生能力、标注覆盖和 invalid-response 处理方法。

## 与单轮误拒和多轮交互评测的关系

本论文关注的是不同语言中的 harmful compliance 和两类攻击/防御迁移，并不测 XSTest 所关注的 benign false refusal；也未构建长对话中的轮次状态或模型自适应攻击预算。多轮 adaptive benchmark 是不同评测构念，见 [MultiBreak arXiv 页面](https://arxiv.org/abs/2605.01687)；这里只把它作为覆盖边界，不据摘要或论文标题推断其评测结果。

**带走的区别**：跨语言稳健性不是把英语 benchmark 逐字翻译后就测出来。数据生成、攻击迁移、模型语言能力、评审器语言覆盖和无效回答处理都会参与分数形成；报告应标明这些协议，而不把十种语言结果外推到未测语言或多轮对话。
