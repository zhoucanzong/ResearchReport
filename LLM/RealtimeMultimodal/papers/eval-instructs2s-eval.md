# InstructS2S-Eval：语音指令遵循、输出对齐与响应延迟

来源：Fang et al., [*LLaMA-Omni: Seamless Speech Interaction with Large Language Models*](https://arxiv.org/html/2409.06666v1)，arXiv v1（2024-09-10）。重点阅读 §4.1–§4.5，尤其 Datasets、Evaluation、Main Results 与 latency/chunk-size 对照。

## 它测的是“听懂指令并生成语音回答”，不是全双工轮次管理

InstructS2S-Eval 由 Alpaca-Eval 的 helpful_base 与 vicuna 子集构成，剔除数学和代码题后有 199 条指令；作者以 CosyVoice-300M-SFT 合成输入语音，再让模型完成 speech-to-text instruction following（S2TIF）或 speech-to-speech instruction following（S2SIF）。因此它主要控制的是语义任务内容，输入音频并非自然双人对话记录，也没有系统性地标注用户暂停、打断或轮次转移。[§4.1](https://arxiv.org/html/2409.06666v1)

## 几组指标回答不同问题

| 指标 | 原文中的测量方法 | 它不等同于 |
| :-- | :-- | :-- |
| ChatGPT content/style score | GPT-4o 依据指令与转录文本评价内容是否回应问题、表达是否适合语音场景 | 人类用户对完整实时对话的偏好 |
| ASR-WER / ASR-CER | Whisper-large-v3 转写模型语音，再与模型文本回复比较 | ASR 以外的说话自然度、时序和情绪一致 |
| UTMOS | 学得的 MOS 预测器评价语音自然度 | 真人听测的主观质量保证 |
| Response latency | 输入语音进入后，到输出语音开始的时间；并报告开始说话时文本已生成的 lagging words | 对话轮次预测、打断响应和用户感知的全链路延迟 |

论文主表把 S2SIF 的 vocoder chunk size 设为 `Ω=∞`，即等待全部离散语音单位生成后再合成波形；§4.5 才扫不同 chunk size，展示较早输出与语音自然度、文本—语音对齐之间的取舍。这个“streaming”指**输出语音分块播放**；任务仍从一条完整语音指令开始，不是边听用户讲话边决定是否打断或接管话轮。[§4.1–§4.2、§4.5，Table 1–2](https://arxiv.org/html/2409.06666v1)

## 应怎样解读它的证据

作者报告的 226 ms 是其模型、推理配置与 `Ω=10` chunk 条件下，从语音输入到语音响应开始的延迟；相应文本在语音开始时平均领先 1.82 个词，UTMOS 低于一次性完整解码。`Ω=∞` 的延迟约 1.9 秒、UTMOS 更高。它展示的是**首段语音延迟—文本/语音对齐—自然度**的工程取舍，不证明模型具备预测轮次边界或处理用户插话的能力。[§4.5、Table 2](https://arxiv.org/html/2409.06666v1)

另一个边界来自评测数据：合成指令、单轮任务和 GPT-4o transcript scoring 能比较回答内容与风格，却没有测量多人重叠、停顿中的回馈、用户中途纠正、模型是否应继续说话，或真人在交互中的满意度。这些需用专门全双工协议分别测。

**带走的区别**：InstructS2S-Eval 是 speech-instruction following 评测；“首响快、语音文字一致、语音自然”是三个独立构念，仍不能替代 turn-taking 或 interruption success。
