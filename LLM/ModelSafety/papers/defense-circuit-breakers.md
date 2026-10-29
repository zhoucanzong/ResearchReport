# Circuit Breakers：从拒答输出改为干预有害生成路径

来源：Zou et al., [*Improving Alignment and Robustness with Circuit Breakers*](https://arxiv.org/html/2406.04313v1)，arXiv v1（2024-06-06）。重点阅读 §3–§5、Appendix B–C。

## 为什么输出层拒答会被绕过？

拒答训练通常教模型在危险请求下输出拒绝文本。若攻击绕开这个拒答状态，模型仍可能沿着原本会生成有害内容的内部表示继续计算。Circuit Breakers 提出另一种干预：在内部表示空间把特定有害过程重路由到一个“短路”状态，使生成路径不再继续构造目标输出，而不只是在最终文本上加拒答模板。[§1、§3](https://arxiv.org/html/2406.04313v1)

## Representation Rerouting 改的是什么

论文的 Representation Rerouting（RR）使用 LoRA 参数化的干预，在安全数据上构造 short-circuit 表示，在 retain 数据上约束模型保留正常能力；目标是把有害样本激活映射到一个与有害生成方向分离的表示区域。它不是外部分类器，也不是简单添加一个 refusal token；模型仍然内部计算，但关键表示转入一条不继续生成目标内容的路径。[§3、Algorithm 1](https://arxiv.org/html/2406.04313v1)

作者在文本 LLM、多模态模型和 agent function-calling 场景中测试 RR，并用 harmful compliance、多个攻击类型与常规能力基准检查安全/效用权衡。该证据是特定模型、训练数据、攻击集合和任务设置的报告；例如表中的能力保持不能证明安全表征对分布外攻击普遍有效。论文还指出其方法针对模型产生有害输出这一类攻击，不能覆盖所有系统级攻击目标。[§4、Table 1、Figures 2–4](https://arxiv.org/html/2406.04313v1)

## 与拒答训练和分类器防御对照

- **拒答训练**改变模型输出偏好，训练便宜但可能被输入改写绕过。
- **Circuit Breakers**干预内部表示路径，避免为每种攻击训练一个独立过滤器；它仍依赖训练/保留数据与目标表示的选择，干预泛化需攻击测试验证。
- **Constitutional Classifiers**在输入/输出接口分类或升级审查，不改主模型的生成机制，但引入分类器判错、上下文截断与额外推理环节。

这些路线的位置不同，不能凭“attack success rate 更低”就说机制更根本。拒绝率、正常能力、不同攻击下的有害响应、误拒和多模态副作用应分别评价。Circuit Breakers 的表示干预也不等于已经找到或解释了完整的“有害电路”；成功阻断行为只能支持给定干预和任务下的因果作用。[§4.4–§5](https://arxiv.org/html/2406.04313v1)

**带走的区别**：该工作把防御从特定字符串/分类边界推进到生成过程中间表示的干预；研究问题转为干预是否稳健、是否损害边界附近的良性请求，以及它对不同任务/模态的因果路径是否一致。
