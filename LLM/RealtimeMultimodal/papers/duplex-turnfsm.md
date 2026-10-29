# TurnFSM：把语义端点检测和输入拒绝写成状态转移

来源：[TurnFSM for Full-Duplex Dialogue System](https://arxiv.org/html/2609.04240v1)，固定版本 v1（2026-08-05）。重点读 §II–§III，特别 II-B/II-C、III-B/III-C。

## 它不是另一个语音生成器，而是全双工系统的输入控制器

全双工系统持续监听时，语音可能是用户真正的话语、背景说话、噪声、回声，也可能是还没说完的句子。外置音频 VAD 只判断是否有人声，不能决定一段语义是否完整；系统若过早提交，会截断用户，若太晚则增加等待。提交后还需要判断这段内容是否是有意图的有效输入。

TurnFSM 把这两个决定分开：**Semantic VAD** 决定何时提交音频片段，**Utterance-level rejection** 决定提交内容是否应该交给对话模型。它以 Qwen2.5-7B-Instruct 为 LLM 骨干，使用流式音频编码器与 adapter；输出离散控制状态，不负责产生助手语音。[§I–§II-A](https://arxiv.org/html/2609.04240v1)

## 机制：把级联系统的状态机内化，而不是平行加两个分类头

模型按前一状态和当前音频前缀预测状态：`Start → Silence → Listen → Submit → Accept/Reject`。处于 `Listen` 时主要判断语义是否完整，达到提交条件后再判断有效意图。作者认为这种串行状态分解比共享表示上同时预测两个标签，降低了不同决策任务之间的表征/梯度竞争。

状态历史被限制为一阶依赖 (p(S_tmid A_{leq t},S_{t-1}))，而不是把所有旧状态 token 持续累积进上下文。论文通过修改训练 mask 和位置绑定教模型这种状态转移，推理时可用标准因果 mask 与原始 LLM 位置编码。[§II-B–II-C](https://arxiv.org/html/2609.04240v1)

与 BayLing-Duplex 的对照：BayLing 用状态 token 直接决定语音对话中的静音、开口、文本完成和语音结束；TurnFSM 只解决输入何时提交、是否拒绝，后续语义理解和语音生成仍由下游系统完成。它减少了手工状态机/额外推理阶段，但没有把完整的 speak/listen/interrupt 对话建模统一进一个语音生成器。[BayLing-Duplex 对读](duplex-bayling.md)

## 评测：端点判定与拒绝要分开报告

论文分别报告 early-cut rate、timeout rate、success rate、成功样本延迟、含超时惩罚的整体延迟，以及 rejection 的 false rejection/false acceptance。它还在语义 VAD 的 EasyTurn 测试集上报告完整句与未完成句分类准确率。TurnFSM 在其测试设置下与单任务基线保持相近表现，并优于共享 LLM 的双二分类头；不同指标不能合成单一的“对话质量”。[§III-B–III-D，Tables I–IV](https://arxiv.org/html/2609.04240v1)

论文把超时样本记为 2000 ms，因此“overall latency”部分由超时率和惩罚协议共同决定；成功样本的延迟、过早截断和完整语句超时也应分开读。语义 VAD 模型的成功率不直接评价回复是否有帮助，也不证明真实用户在对话中感觉自然。

## 证据边界

- TurnFSM 把级联流水线中的控制逻辑内化为一个有状态模型，不等于系统再也不需要音频编解码、下游 LLM 或 TTS。
- 论文将 rejection 与 semantic VAD 纳入同一状态序列，但对真实用户意图、多人重叠、长时间 backchannel 和情绪交互的覆盖仍有限。
- 作者使用的数据、模型初始化、状态定义与延迟惩罚规则限定结论；其工程意义是特定控制模块的可学习化，不是全双工自然对话的完整解决方案。

**带走的区别**：TurnFSM 关注“什么时候把音频交给系统、哪些输入不应提交”；这与“模型如何同时听和说”相关，但不是同一个生成机制。
