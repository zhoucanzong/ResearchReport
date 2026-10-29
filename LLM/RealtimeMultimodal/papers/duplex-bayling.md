# BayLing-Duplex：用交织通道和状态 token 学会何时听、何时说

来源：[BayLing-Duplex: Native Full-Duplex Speech Dialogue with a Single Autoregressive LLM](https://arxiv.org/html/2606.14528v1)，固定版本 v1（2026-06-12）。重点读 §2.1–§2.3、§3、§4.2–§4.4。

## 研究问题：能否把 turn-taking 从外部 VAD 搬进模型决策

许多端到端语音模型仍然先判断用户结束，再把完整话语交给模型生成回复；外置 VAD 一旦误判，可能截断用户或拖慢响应。BayLing-Duplex 想从一个已经具备语音输入/输出的 GLM-4-Voice 检查点出发，用少量全双工对话微调，让同一个自回归 LLM 决定持续听、开始说、继续输出或结束发言。

它不另加轮次分类器，而是为用户语音、助手文本、助手语音建立对齐的三通道 interleaved sequence。每个 block 放入固定数量的用户语音 token、文本 token 和助手语音 token；文本通道加入 `[SILENCE]`、`[ASSISTANT]`、`[PAD]`、`[EPAD]` 四个状态标记。模型因此把“保持静音/开始回答/文本已完但语音继续/回复完全结束”化为普通 next-token prediction。[§2.1](https://arxiv.org/html/2606.14528v1)

与 Moshi 共享“同时看用户流和发助手流”的目标，但序列实现不同：Moshi 直接建模用户与助手的两个音频流，加文本内省通道；BayLing-Duplex 用块级对齐组织两个音频轨和一个文本状态轨，并显式编码对话状态 token。它从回合制 checkpoint 出发的路径，也不同于从头构建 full-duplex 基座。[Moshi 对读](duplex-moshi.md)

## 设计取舍：block 越小，响应更及时但文本预算更紧

音频 tokenizer 将 16 kHz 波形编码为 12.5 Hz token（每个 token 对应 80 ms）；论文选用 (N=10, M=5)，使每个 block 代表 0.8 秒，并提供平均约 6.25 个文本 token。较大 block 给文本通道更多子词空间，却把最早响应粒度推迟；较小 block 可以更频繁做轮次决策，但每块文本预算较少，容易产生不稳定/抖动的说话节奏。作者明确说没有对 block size 做系统性 sweep，所以 0.8 秒是他们实验配置，不是普适最优时延。[§2.1，Block Size / Causal Shift](https://arxiv.org/html/2606.14528v1)

另一个关键步骤是 Causal Shift：训练时把助手文本与语音目标向后移一个 block，使它们对应已经观察到的用户音频之后的时间窗；推理时再加上同一偏移。这是输入可见历史与目标音频时间对齐的接口约束，不等同于保证交互在这个窗口后一定自然接话。[§2.1，Causal Shift](https://arxiv.org/html/2606.14528v1)

## 训练和论文证据

作者使用 GLM-4-Voice 的公开检查点，先对 400K 全双工样本做 SFT，再用轻量 DPO 优化轮次和插话时机。论文在 InstructS2S-Eval 报告：DPO 版本 Turn-Taking SR@3s 为 92%，ISR@2s 为 100%；同一表格中基线 Moshi 为 71.9% 与 81.9%，而 BayLing SFT 版本是 88.9% 与 91.4%。它还报告了人工语音响应评分和口语问答结果。数值只适用于该 benchmark、语料、GLM-4-Voice 初始化与 DPO 配置。[§3、§4.2–§4.4，Tables 1–5](https://arxiv.org/html/2606.14528v1)

一个重要消融显示，若对静音 token 使用不合适的统一损失权重，模型可能长期不说话；这时 ISR@2s 会因为“几乎不讲话就不被打断”而显得很高。作者通过单独加权角色/静音 token 和 DPO 改善轮次行为。**打断成功率必须和是否及时开口、响应内容质量一起读**，不能孤立作为交互自然度指标。[§4.4，Tables 3–4](https://arxiv.org/html/2606.14528v1)

## 失效边界

- 论文关注 turn-taking 与 interruption；backchannel、多人对话和 emotion-aware turn-taking 明确未研究。[§5](https://arxiv.org/html/2606.14528v1)
- Block size 固定而未全面搜索，响应粒度和文本预算的权衡仍需其它语速、语言和编解码速率的验证。
- 该模型在口语 QA 任务上的结果表明全双工微调未必损害所测文本任务，但不证明所有复杂推理、长任务或工具使用都不受语音对齐影响。
- 与基于独立 VAD/ASR/LLM/TTS 的级联系统相比，论文报告的是一个特定基线集合；不能将其泛化成“移除任何外部模块都一定更自然/更快”。

**带走的区别**：BayLing-Duplex 让对话状态成为模型 token；设计关键不是“有四个特殊 token”，而是 block 时序、静音/语音损失权重和 DPO 共同决定何时轮到系统发言。
