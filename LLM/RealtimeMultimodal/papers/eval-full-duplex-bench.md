# Full-Duplex-Bench：把暂停、回馈、接管和打断拆开测

来源：Lin et al., [*Full-Duplex-Bench: A Benchmark to Evaluate Full-duplex Spoken Dialogue Models on Turn-taking Capabilities*](https://arxiv.org/html/2503.04721v1)，arXiv v1（2025-03-06）。重点阅读 §3.2–§3.4、§5 与 limitation。

## 一个 “takeover rate” 在不同情境里方向相反

论文把模型是否发出非静音、非 backchannel 的语音定义为二元 takeover（TO），并在样本上求 TOR。这个定义简单、可自动算，却要结合任务理解：

- **用户在自然停顿中仍持有话轮**：过早接管有害，TOR 越低越好。
- **平滑轮次转换**：在用户结束后及时接话，TOR 应较高；响应时延只在模型确实接管时计算。
- **用户主动打断模型**：模型应在新的用户输入后接管，TOR 应较高；另测打断后的响应延迟和 GPT-4o 对回复连贯性、相关性、适应性的 0–5 评分。
- **Backchanneling**：不抢话地给出“嗯/对”等倾听信号，测事件频率和与人类回馈时序分布的 Jensen–Shannon divergence；这两项只在未接管的条件下解释。

因此，不能把不同场景下的 TOR 高低直接合成一个“互动性”总分。一个总是立即发声的模型会在平滑接话场景看似及时，却可能在自然停顿中频繁打断。

## 评测数据和任务并非同一个自然对话基准

Full-Duplex-Bench 将四类构念拼成一个评测框架，但使用不同素材：pause handling 与部分 interruption 使用 GPT-4o 生成的文本情境，再由 ChatTTS 合成语音；pause handling 有 137 个样本、用户打断有 200 个样本；backchannel 来自 ICC 语料；smooth turn-taking 从 CANDOR 双通道自然对话中筛出满足预设 gap 的样本。数据来源、语言、场景与操作定义不同，因而结果应按维度读取，而不是当成同一分布下的四个子分数。[§3.4、Table 2](https://arxiv.org/html/2503.04721v1)

自动评分能扩大可重复比较，但每项仍是代理测量：TOR 只看是否出现接管行为；JSD 比较回馈时序分布，不评价语义是否合适；响应延迟不说明答案内容质量；GPT-4o 评分依赖自动裁判。论文数据主要为英语，作者也将语言与场景覆盖列为限制。[§3.3、§5–§6](https://arxiv.org/html/2503.04721v1)

## 与 InstructS2S-Eval、TurnBench 的边界

[InstructS2S-Eval](eval-instructs2s-eval.md)重点是单条语音指令的内容/风格回答、文本—语音对齐和首响延迟；Full-Duplex-Bench 的目标是轮次控制和打断行为。[TurnBench](eval-turnbench.md) 则将端点/中断事件检测定义为一个跨会话风格的事件预测任务，计 recall、FPR 和签名延迟。即使三者都提到“latency”，测量的时间区间与系统行为也不同。

**带走的区别**：Pause handling、backchannel、smooth floor transfer 和 user interruption 是相关但不等价的交互行为。Full-Duplex-Bench 的价值在于把它们放在同一设计框架里；它的多来源合成协议并不能代替真实、跨文化、多轮对话验证。
