# UltraFeedback：把多模型回答转成带理由的 AI 偏好反馈

来源：Cui et al., [*UltraFeedback: Boosting Language Models with High-quality Feedback*](https://arxiv.org/html/2310.01377v1)，arXiv v1（2023-10-02）。重点阅读 §3.1–§3.4、§4.1–§4.4、§5.1、Appendix A–B。

## 它合成的不是只有 instruction，而是“回答—评价—批评”结构

UltraFeedback 从多个公开指令集合抽样，按指令关注的能力维度给不同模型生成回答；随后让 GPT-4 对同一指令下的多个回答给出逐维分数、整体偏好和文字 critique。论文围绕 instruction-following、helpfulness、truthfulness、honesty 四个方面构造评分准则；评分说明把每个维度的 1–5 档行为写给标注模型参考。细粒度 critique 不只给 reward model 训练，也用于训练能点评回答的 critique model。[§3.1–§3.2](https://arxiv.org/html/2310.01377v1)

关键设计是**同一 prompt 多回答联合评分**：作者一次把一个 instruction 的多个模型 completions 放进 GPT-4 评分提示，以减小跨多次独立打分时标准漂移。各回答的 critique 则单独生成，因此“成对/组内比较的分数”与“逐回答解释反馈”是不同标注流程，不能把文本 critique 当成严格偏好标签。[§3.2](https://arxiv.org/html/2310.01377v1)

## 指令池、回答池和评价原则共同决定数据分布

论文汇集 TruthfulQA、FalseQA、Evol-Instruct、UltraChat、ShareGPT 和 FLAN 等指令，再从 17 个不同规模/架构的模型池中为每条指令采样四个回答；GPT-4 评估时再按维度提示原则，包含人工起草原则与 GPT-4 扩写的原则集合。[§3.1–§3.2](https://arxiv.org/html/2310.01377v1)

所以 UltraFeedback 的反馈质量不只取决于 GPT-4 judge：指令来源决定任务覆盖，响应模型池决定被比较的风格和能力范围，原则提示决定“好回答”的操作定义，组内评分方式影响偏好标签。某一维度分数高，不表示其它维度也好；judge 的详细解释更不等于真实人类偏好。

## 从数据到 reward model / PPO 的证据要分开读

作者报告在其数据和训练设置下，UltraFeedback 可训练 UltraRM、以 best-of-n 或 PPO 对开源模型进行优化，并可训练 UltraCM critique model。数据集构造结果、reward-model 排名能力、best-of-n 输出质量和 PPO 后模型分数是四个不同层次的证据；若把它们合并为“合成偏好数据提升了模型”，就会忽略下游 reward model 与优化算法的作用。[§3.4、§4.1–§4.4](https://arxiv.org/html/2310.01377v1)

论文承认偏好质量和严格评测仍有挑战，数据以单轮对话为主；它也只对 AlpacaEval、UltraChat test、Evol-Instruct test 等执行了特定 13-gram 污染排查，没有穷尽所有评测集。因此 GPT-4 打分一致或模型在某个 benchmark 表现好，都不是“AI feedback 等于人类偏好”的证明。[§6、Appendix A–B](https://arxiv.org/html/2310.01377v1)

**带走的区别**：UltraFeedback 研究的是“多源 prompt + 多模型回答 + AI 评价”的反馈管线，和 Self-Instruct 的 task bootstrapping、Evol-Instruct 的难度变异不是同一合成数据任务。
