# Evol-Instruct：沿难度轴演化指令，再用过滤器阻止无效变异

来源：Xu et al., [*WizardLM: Empowering Large Language Models to Follow Complex Instructions*](https://arxiv.org/html/2304.12244v1)，arXiv v1（2023-04-24）。重点阅读 §3.1–§3.3、§4.3–§4.5。

## 两种演化操作分别改变难度和覆盖

Evol-Instruct 从现有 instruction-response 池出发，每轮取待演化 instruction，用语言模型提示生成变体，再为新指令生成 response。**In-depth evolving** 通过添加限制、深化问题、具体化对象、增加推理步骤、复杂化输入逐步增加难度；**in-breadth evolving** 则从当前 instruction 启发一个新任务，扩展主题和技能覆盖，但目标复杂度大致保持在原水平。[§3.1–§3.2](https://arxiv.org/html/2304.12244v1)

这与 Self-Instruct 的差别不只是 prompt 不同：Self-Instruct 优先从任务池自举新任务；Evol-Instruct 把已有 instruction 当作搜索起点，显式将“难度递增”和“广度扩展”分成两种变换。作者发现每次只“稍微更难”有助于避免难度快速堆积，使训练池缺少普通任务、只剩极难样本。[§3.2，In-Depth Evolving](https://arxiv.org/html/2304.12244v1)

## Elimination Evolving 不是事实验证器

演化失败过滤器把结果判为无效的情形包括：新指令相对原题没有信息增量；模型生成拒答或过短回答；回答只有标点/停用词；或把提示模板内容复制进 instruction。第一项由 LLM 比较两条指令是否具有相同约束、深度和范围；拒答/长度规则则用生成 response 作为可处理性的代理。[§3.2，Elimination Evolving](https://arxiv.org/html/2304.12244v1)

这能筛掉明显的空变异，却不能判断每个复杂任务是否合理、公平或具有训练价值。复杂度过滤依赖同一个模型的可回答性判断：模型觉得难，不代表对人类用户有用；模型能回答，也不保证数据标签正确。过滤规则会把“教师当前可做”悄悄变成训练集可纳入边界。

## 实验比较的是数据路线，不是开放域能力的因果归因

作者以 Alpaca 的 175 个种子指令启动四轮演化，生成约 250K instruction；为与使用 70K ShareGPT 的模型对照，另从 Evol-Instruct 中均匀采样 70K 微调 LLaMA 7B。论文在人工构建的难度均衡测试集上报告该模型相对 Vicuna 的偏好结果（41.3% vs 28.9%）；这是论文特定基座、样本构造、训练与评审设置下的结果，不证明任何模型生成的困难样本都优于人写数据。[§4.2–§4.5](https://arxiv.org/html/2304.12244v1)

尤其要注意：模型自身既是变体生成器，也是 response 生成器；训练又混入所有演化轮次。比较到的是一个完整的“演化 prompt + 过滤 + response generation + 数据混合”配方，不是对五种难度操作逐项做因果归因。作者的难度均衡评测也只覆盖他们构造的任务范围。

**带走的区别**：Evol-Instruct 把数据生成变成带变异操作的搜索过程；复杂度是可控轴，但“更复杂”与“更适合训练”需要独立验证。
