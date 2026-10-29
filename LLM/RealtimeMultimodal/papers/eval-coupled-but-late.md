# Coupled but Late：模型互相说话时，轮次时间会怎样演化？

来源：Zhu et al., [*Coupled but Late: Turn-Taking Between Full-Duplex Speech Models in Unscripted Dialogue*](https://arxiv.org/html/2610.08683v1)，arXiv v1（2026-10-06）。重点阅读 §2–§4、Appendix C–H，尤其测量定义、partner re-pairing 与延迟控制。

## 研究单位是两个模型形成的交互回路

论文让两份 PersonaPlex-7B 在共享时钟上直接交换音频 token，进行无脚本对话；没有 ASR/TTS 中间管线把输入变成文字再回传。一个模型的响应时间因此直接变成另一个模型的输入，作者问：这种闭环会稳定在怎样的轮次节奏？这不同于只测单模型对固定录音的事件预测，也不同于只测输入一条语音后生成一条回答的 instruction following。[§1–§2](https://arxiv.org/html/2610.08683v1)

## Floor-transfer offset 是时间统计，不是语义质量

作者把两段相邻 speech spans 合并为 inter-pausal units（IPUs），若下一位说话者在当前 IPU 结束后开始，floor-transfer offset（FTO）为正 gap；重叠为负。主要报告 median、overlap fraction、±120 ms near-zero band 和分布 Wasserstein-1 距离。它们刻画谁何时开始说话、两个说话者的时间分布是否像人类，不直接判断回答内容是否正确或是否遵守指令。[§2、Table 1](https://arxiv.org/html/2610.08683v1)

作者报告在 baseline model-model 配置中，模型 dyad 的 median FTO 为 400–560 ms，而他们的 Switchboard 人类参考为 137 ms；结果由 36 个固定 seed 的 90 秒双人场景产生。重新配对 partner、静音 partner、录音人类 partner 和单向通信延迟控制试图区分模型策略与通道时延。论文据此提出该特定 PersonaPlex 配置更像“听到结束后再反应”，而不是在人类过渡相关位置预测接话。[Abstract、§2–§3、Appendix C–H](https://arxiv.org/html/2610.08683v1)

## 这不是用户面对面的完整交互质量结论

人类基线来自 Switchboard 电话陌生人对话，模型则共享同一场景并用 system prompt 设定 persona；即使时延采用同一抽取规则，场景和话语目标仍不同。论文有额外 recorded-partner 条件，但主要对象仍是 dyadic self-play。FTO、overlap 和 timing distribution 不测回答正确性、用户主观满意度、情绪协调或任务完成；更快接话也不必然更自然，抢话误报会带来另一种失败。

与 [TurnBench](eval-turnbench.md) 对照：TurnBench 固定人类对话环境测 EOT/INT 事件检测，Coupled but Late 观察两个完整生成器互相改变对方输入后形成的动态。它补充了“单边事件预测”看不到的耦合效应，但不能代替人机、多风格和任务质量评测。
