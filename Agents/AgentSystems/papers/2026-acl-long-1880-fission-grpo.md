# Fission-GRPO：把在线工具错误变成恢复训练信号

> Zhang et al., *Robust Tool Use via Fission-GRPO: Learning to Recover from Execution Errors*, ACL 2026, pp. 40477–40491. [论文页](https://aclanthology.org/2026.acl-long.1880/) · [PDF](https://aclanthology.org/2026.acl-long.1880.pdf)

## 问题：负奖励说“错了”，但没有教模型怎样修正

工具调用出错后，小模型可能重复提交同一无效参数。常规 outcome-only RL 通常只给整条失败轨迹负奖励；离线纠错样本又可能跟不上当前策略正在犯的新错误。Fission-GRPO 要把训练期间采到的错误反馈回同一策略的恢复训练中（§1–2）。

## 机制：从当前策略错误上采样修正尝试

流程分三步：先用标准 GRPO 采样并更新一般工具调用能力；再由 Error Simulator 为失败调用生成诊断反馈；将原请求、失败调用和反馈组成纠正上下文，从当前策略重新采样多条恢复轨迹，再做 corrective GRPO 更新（§3.3）。新鲜失败样本进入 LIFO buffer，目的是让训练信号更贴近当前策略的错误分布。

训练数据来自 11 个工具 schema 域的合成轨迹，经分层过滤后从约 2,000 条初始轨迹中保留 630 条。对 Error Simulator 的抽样人工评估中，96% 的反馈被判断为不泄漏答案，评估者一致性 κ=0.71；这评价的是模拟诊断反馈，不等于真实 API 错误的分布已被覆盖（§4.1、Table 3）。

## 结果与边界

在 BFCL v4 Multi-Turn 的 Qwen3-8B 设置中，论文报告错误恢复率平均提高 5.7 个百分点，总体准确率从 GRPO 的 42.75% 升至 46.75%（Table 1、§4.3）。消融中，Fission-Static 的总体准确率为 44.00%，带上下文诊断的 Fission-Dynamic 为 46.75%，支持“失败后增加恢复尝试有用，具体反馈还能带来额外收益”的解释（Table 2）。作者还报告计算量匹配时保留收益，但该方法对每个被拦截的错误增加恢复 rollouts。

评测限于有错误反馈和重试机制的工具调用基准，尚未覆盖浏览器、代码修改或产生真实外部副作用的服务。Fission-GRPO 学会在反馈后修正策略，但不回滚已经改变的环境状态；每个失败都增加恢复 rollout，也带来训练开销（Limitations）。
