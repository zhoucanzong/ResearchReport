# 草稿位置与验证上下文为何需要不同预算

投机解码常把“多生成候选”视为一个统一的预算问题，但不同位置、不同上下文的边际收益并不相同。HCSpec 与 HeteroSpec 分别从草稿内部的位置差异和运行时上下文差异入手，给出两种不同的预算重分配方式。

## 两种异质性，两种调度层

| 阅读问题 | 代表工作 | 系统看见的信号 | 改动落在哪层 |
| :-- | :-- | :-- | :-- |
| 草稿链前后位置的收益是否相同？ | [HCSpec](../papers/2026.acl-long.353-hcspec.md) | 从当前位置起可连续接受的未来长度 | 前段用双层、双路 draft；后段切换轻量 draft |
| 某个上下文是否值得扩展当前候选树？ | [HeteroSpec](../papers/2026.acl-long.589-heterospec.md) | 最高置信路径的累计 Top-K 熵，经浅层 CART 分区 | 按复杂度区间调整 draft depth、Top-N 与运行图 |
| 已生成的分支中哪条更像 target greedy 路径？ | [ValuSpec](../papers/2610.31338-valuspec.md) | calibration 数据上 target greedy 轨迹的分支估值 | target 验证前筛除低分枝，最后仍由 target 判定 |

HCSpec 是**训练后固定的模块分工**：它重塑 drafter，不是候选树的 verifier。HeteroSpec 是**按上下文在线选策略**：它没有重新训练 target/draft LLM，但会从轨迹拟合一个辅助分层器，也不等于 ValuSpec 的逐分支轨迹估值。三个方法看起来都在省计算，实际操作的阶段和信息不同。

可用这条链理解设计位置：

```text
预算在哪些 token 位置更值？ ── HCSpec：重分配 drafter 容量
当前上下文是否适合多草拟？ ── HeteroSpec：运行时调整树预算
现成树里的哪些分支值得验证？ ─ ValuSpec：验证前估值筛枝
target 最终如何接受/回补？ ─── HSD / 标准 verifier / 具体接受规则
```

最后一步必须与前三步分开：HCSpec 采用既有 EAGLE-2 验证；HeteroSpec 依赖 EAGLE-3 verifier 条件并声明保留严格接受；ValuSpec 的 output-identical 结论限定在 greedy。需要序列级概率保持证明时看 [HSD](../papers/2601.05724-hsd.md)；要问 greedy / top-m 等局部规则在什么 KL 条件下会接受，看 [When Is a Draft Accepted?](../papers/2606.30265-when-is-draft-accepted.md)。它们解决的不是“如何分配 draft 预算”。

## 论文之间能比较什么，不能比较什么

HCSpec 把 early-position fidelity 与后段低成本连接起来，研究的是模型结构、状态传递和阶段训练；HeteroSpec 用目标候选路径的累计熵和历史接受排名决定深度/Top-N，研究的是系统策略与运行时图；ValuSpec 用独立 calibration split 的 target-greedy 轨迹训练轻量估值器，研究的是候选价值预测。三者形成**位置容量 → 上下文策略 → 候选筛选**的学习路线。

不能据各自摘要的速度数字排榜：基线、模型、任务、硬件、温度和 candidate budget 不同。更有解释力的对照是各机制拿什么信号、何时作决策、改变了哪个成本项、以及正确性由谁兜底。HCSpec 的切换点经验设定；HeteroSpec 的跨框架泛化仍待验证；ValuSpec 的校准分布和 greedy 条件限制了迁移范围。若将这些模块组合，必须重新测端到端成本并逐项确认 verifier 的接受/回补语义，当前论文没有共同组合实验。

## 推荐阅读顺序

先读 [HCSpec](../papers/2026.acl-long.353-hcspec.md)，理解为何 draft chain 早段和尾段可以用不同容量；再读 [HeteroSpec](../papers/2026.acl-long.589-heterospec.md)，看上下文复杂度怎样触发深度、候选数与计算图变化；最后读 [ValuSpec](../papers/2610.31338-valuspec.md)，对比 target greedy 轨迹如何估值已构造候选。若读者需要判定这些提速改动的正确性，再接 HSD 和 When-Is；不要把预算策略本身误读成 verifier 的数学证明。
