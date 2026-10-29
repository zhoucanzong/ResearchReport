# TurnBench：把话轮边界预测与对话内容质量分开

来源：Jiang et al., [*TurnBench: A Multi-Domain Benchmark for Turn-Taking Dynamics in Spoken Dialogue*](https://arxiv.org/html/2608.25218v1)，arXiv v1（2026-08-25）。重点阅读 III–V、VI–VIII，尤其 annotation、scoring 和 Full-Duplex Models 段。

## 它测的是系统何时预测事件，不是回复得多好

TurnBench 用 30 小时双人真实对话，覆盖六种交谈风格；每段由三位标注者按统一 conversation-analysis taxonomy 标注 end-of-turn（EOT）、floor transition、interruption 和 backchannel。与 InstructS2S-Eval 的 instruction-response 质量不同，TurnBench 的提交对象是时间戳：模型在什么时候判定说话者让出了话轮，或听者开始真正的中断。[Abstract、§III–IV](https://arxiv.org/html/2608.25218v1)

它的金标把两名以上标注者在事件类别一致且端点相差不超过 200 ms 的片段做 consensus；没有共识的区间会作为 excluded intervals，不会被算成正例或负例。相同的谈话事件先定义 gold，再对各种系统使用统一 scorer，减少不同系统自定义 interruption/backchannel 语义导致的不可比性。[§IV-A、§V](https://arxiv.org/html/2608.25218v1)

## Recall、误报和签名时延必须一起读

对每个 gold event，系统在事件前 250 ms 到事件后 3 秒的窗口中匹配预测；报告 recall、负区间上的 false-positive rate，以及 matched true positives 的 signed latency 分位数。负 latency 表示系统在金标边界前预测；排行榜先限制 dev FPR，再在测试集按 recall 排序。这样可以暴露“永远抢答”的系统：它可能很早检测到边界，但会在真实停顿或 backchannel 处误报。[§V-C](https://arxiv.org/html/2608.25218v1)

这一协议测的是预测器或声音输出产生的**事件时机**，不测模型是否给出语义正确、对用户有帮助的完整回复。论文将全双工生成模型的音频输出送入同一事件流程，但因全双工模型不一定在中断事件发生时正处于说话状态，只对它们测 EOT，不测 INT。因此“在 TurnBench 上的 EOT recall”不能写作“中断处理能力”。[§VI-D、§VII](https://arxiv.org/html/2608.25218v1)

## 多域和人类基线各自带来什么

六种交谈风格包括 argument、casual、collaborative、instructional、narrative 与 task-oriented。论文发现 EOT recall 对风格相对稳定，但 interruption FPR 在 backchannel 密集的随意对话中更高；这提示一个总 recall 可能遮住不同会话风格里的误报风险。其 Switchboard 人类参考数据是电话对话、TurnBench 则有六类共同场景，两者不能当完全同分布的“人类标准”。[§IV–§VII](https://arxiv.org/html/2608.25218v1)

**带走的区别**：TurnBench 更接近 turn manager / semantic VAD / event predictor 的测量；它不是端到端语音助手的综合质量分。Full-Duplex-Bench 把多个互动行为放入自动基准，Coupled but Late 则分析两个完整模型互相反馈后的时间动态，三者研究对象不同。
