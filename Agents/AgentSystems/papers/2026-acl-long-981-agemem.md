# AgeMem：让策略本身管理长短期记忆

> Yu et al., *Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents*, ACL 2026, pp. 21457–21483。 [论文页](https://aclanthology.org/2026.acl-long.981/) · [PDF](https://aclanthology.org/2026.acl-long.981.pdf)

## 问题：两套记忆通常各自优化

作者把 Agent 记忆区分为长期记忆（LTM，跨轮保存的用户或任务信息）与短期记忆（STM，当前上下文）。既有方案常让摘要/RAG 管 STM，让另一个记忆管理器维护 LTM；两者彼此分开，容易发生重复、丢失或无法协调。AgeMem 的研究问题是：能否把两者统一成同一策略可选择的显式操作？（§1–3.1）

## 机制：六种工具动作，三阶段训练

AgeMem 把 `ADD`、`UPDATE`、`DELETE` 用于 LTM；把 `RETRIEVE`、`SUMMARY`、`FILTER` 用于从长期库取回信息和控制当前上下文（Table 1）。执行轨迹分三阶段：先在会话中学习哪些信息值得写入 LTM，再在干扰内容下学习 STM 管理，最后联合两类操作完成任务（§3.2–3.3）。训练采用 progressive RL 和 step-wise GRPO：最终任务结果可以把奖励传回较早的记忆决策，针对记忆操作带来延迟、稀疏奖励的问题设计。奖励同时考虑任务得分、上下文管理、记忆质量，以及超出交互/上下文限制的惩罚（§3.4–3.5）。

关键变化不是“再加一个记忆数据库”，而是让模型策略能决定记忆何时写、何时取、何时更新或压缩。这样可学习跨阶段的协调，但也把错误记忆操作纳入策略本身，要求评测检查长期污染与纠错能力。

## 实验：收益来自长短期操作与训练的组合

论文在 ALFWorld、SciWorld、PDDL、BabyAI、HotpotQA 五个任务上评估，并与无记忆、LangMem、A-Mem、Mem0 等比较（§4.1、Table 2）。在 Qwen2.5-7B-Instruct 上，AgeMem 平均分为 41.96，对应无记忆基线 28.05；Qwen3-4B-Instruct 上为 54.31，对应 43.97。作者的消融显示，仅加入长期记忆和 RL 已有提升，完整 LTM+STM+RL 组合在三个展示任务上优于分步变体（Figure 4）。

Table 2 的两个 backbone、五个任务结果不能视为跨任务通用成功率；控制任务和评分方式也限制外推。论文训练过程以 HotpotQA 产生三阶段轨迹，虽报告跨域任务，但不等于在用户长期在线使用中验证了稳定记忆。

作者另以 HotpotQA 的平均提示 token 数测 STM 压缩：Qwen2.5-7B 为 2,117，对照 AgeMem-RAG 为 2,186；Qwen3-4B 为 2,191，对照 2,310（§4.3）。这说明该设置下 prompt 较短；token 数本身不代表记忆无损或任务质量提高。

## 阅读时重点留意

- 复现基线时分清同 backbone 比较与不同 backbone 对比；Memory baseline 的训练和参数设置会影响结果。
- 奖励中的记忆质量和相关性部分使用 LLM judge / 自动评价信号。评估器误差会传入训练目标，需结合消融阅读，而不能把复合奖励直接视作客观记忆质量。
- 作者明确列出三个限制：记忆操作集合是固定的；长程交互仍比真实开放部署受控；三阶段训练目前依赖 HotpotQA 来源轨迹（Limitations）。
- 方法是在 Agent 内学会调用记忆接口。若底层存储未保留来源、时间和覆盖关系，模型的 `UPDATE` / `DELETE` 决策依旧可能损害可追溯性；这是部署设计问题，不是论文结果已证明解决的问题。
