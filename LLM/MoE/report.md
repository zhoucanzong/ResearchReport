---
display_name: 混合专家模型（MoE）
---

# 混合专家模型：路由、负载均衡与系统通信

混合专家模型（Mixture of Experts, MoE）将 Transformer 中的一部分稠密前馈层替换成多个专家子网络，并让每个 token 只激活其中一部分。它试图把**模型总容量**与**每 token 计算**部分解耦：更多参数可作为候选知识存储，但单个 token 只经过少数专家。

这并不意味着 MoE 自动更便宜或更快。总专家权重仍需存储或分片到设备上；路由会产生 token 分发与回收通信；负载不平衡会让最忙专家决定整步延迟。理解 MoE 的研究主线，需把三个层面放在一起看：路由怎样选择专家，负载目标怎样影响训练形成的专家分工，分布式系统如何为这种稀疏访问付通信成本。

## 目录

1. [MoE 层与计算账目](#1-moe-层与计算账目)
2. [路由方向和容量管理](#2-路由方向和容量管理)
3. [专家粒度与知识分工](#3-专家粒度与知识分工)
4. [负载均衡](#4-负载均衡任务目标与路由目标如何相互作用)
5. [路由怎样落到设备上](#5-路由怎样落到设备上)
6. [实验如何比较与开放问题](#6-实验如何比较与开放问题)

---

## 1. MoE 层与计算账目

典型 MoE 层由路由器 $G$ 和 $N$ 个专家 FFN 组成。对 token 表示 $x$，路由器计算专家 affinity，选择 Top-$K$ 个专家并归一化权重，输出可简写为：

```text
y = x + Σ(i ∈ TopK(x)) g_i(x) · E_i(x)
```

其中残差项 $x$ 保留该层输入，$g_i(x)$ 是所选专家权重，$E_i$ 是专家网络；具体实现还包括层归一化、容量缓冲和 dispatch。由于每个 token 只经过 $K$ 个专家，前馈层不必对所有专家做矩阵乘法。这是 MoE 的**条件计算**来源。

理解资源时必须区分：

- **总参数量**：所有专家和共享模块的参数，主要影响模型容量与权重存储。
- **激活参数量**：每个 token 实际经过的参数，近似反映部分算术量，但不包含所有注意力、路由和通信成本。
- **部署资源**：专家权重是否全部驻留、跨设备传输与 all-to-all 通信、KV cache、batch、量化和并发共同决定显存、吞吐和延迟。

所以“激活参数只有 X”不能单独推出“推理成本只有 X”或“消费级设备可运行”。不同层的专家可能分散在多卡；一次生成也要为每个 token 找到对应专家、交换隐藏状态并回收输出。

MoE 通常替换 Transformer 的 FFN，而不是整个 block。注意力仍处理序列信息；MoE 条件计算主要发生在 token-wise FFN。扩大专家容量不会自动改善长上下文位置利用、视觉感知或推理监督，这些问题需要与本层路由机制分别研究。

## 2. 路由方向和容量管理

### 2.1 Token-choice：token 选 Top-K 专家

Shazeer 等人 2017 年提出的 sparsely-gated MoE layer 用可学习门控网络为每个输入计算专家权重，并以 noisy Top-K 只激活少数专家。训练噪声帮助路由探索，辅助负载损失则鼓励专家收到较均衡的 token。其挑战并非只有路由器 FLOPs：离散 Top-K 不便直接反向传播，专家利用不均会自我强化，路由又要把输入/输出在专家设备之间搬运。论文指出，小批次、分布式网络带宽和专家负载会让理论稀疏计算难以转成墙钟速度。[Shazeer et al. §2–4、Appendix A](https://arxiv.org/html/1701.06538)

后续 Transformer MoE 常使用 **capacity factor** 限定每个专家在一个 token group 中的缓冲容量。它给设备内存和计算上限，却带来新的分配结果：专家满载后，多余 token 可能被丢弃、路由到次选专家或由实现采用其他溢出策略。训练时被丢弃的 token 仍计入输入，但其 MoE 层不再获得正常的专家变换；评估 token dropping 时需区分训练/推理策略和模型检查点。

### 2.2 GShard 与 Switch：Top-2 的组合能力与 Top-1 的简化

GShard 将 Top-2 门控扩展到大规模 Transformer 和 TPU 设备集群。作者报告训练一个 600B 参数的 seq2seq Transformer，并在 2,048 个 TPU v3 上训练多语言到英语的翻译模型；这个结果同时依赖 Top-2 稀疏层、自动 sharding、设备并行策略和该翻译数据/目标。一个 token 的两个 gate 权重经归一化后组合两个专家输出；为了控制每组 token 的容量，论文使用 group-level gating、容量上限、辅助负载损失，并对次选专家采用按 gate 强度的随机 dispatch。路由实现与模型并行一起考虑，SPMD sharding 把高层张量表达映射为跨设备通信。其 600B 参数模型和 100 语言机器翻译实验展示了规模可扩展性，但证据来自论文定义的翻译目标、数据与 TPU 训练系统，不意味着任意自然语言任务都按同样比例获益。[GShard §2–5](https://arxiv.org/html/2006.16668)

Switch Transformer 提出简化到 Top-1：每个 token 仅路由一个专家，减少专家组合和通信步骤。它同时研究 router softmax 稳定性、专家容量、bfloat16 和负载损失；容量不足时依然可能出现 token dropping。论文在 T5 系列预训练条件中报告速度与质量收益，例如同等计算资源下相对其强基线的 time-to-quality 提升；结果必须跟具体 T5 模型、数据、硬件和目标质量一起读，不能把“Top-1 更快”写成通用定律。[Switch §2–5](https://arxiv.org/html/2101.03961v3)

这两条路线的差别是计算和调度取舍：Top-2 让一个 token 合并多个专家输出，增加组合表达但要执行更多专家 dispatch；Top-1 简化每个 token 的路由路径，却把所有信息压进单专家输出。效果还依赖模型如何训练、是否丢 token、专家容量和设备拓扑。

| 路由设计 | 谁选专家/Token | 负载如何控制 | 主要改变 | 关键风险 |
|---|---|---|---|---|
| Noisy Top-K | token 选 K 个专家 | importance/load 辅助损失 | 用噪声鼓励探索、软 gate 聚合 | 负载损失与任务损失竞争 |
| GShard Top-2 | token 选两个专家 | 分组容量、辅助损失 | 两个 expert 的 gate 加权融合 | 溢出 token 与跨设备 dispatch |
| Switch Top-1 | token 选一个专家 | capacity factor、负载损失 | 降低路由和通信复杂度 | 单专家容量限制表达/溢出风险 |
| Expert Choice | 专家选固定 bucket 的 tokens | 每专家 bucket size | 专家侧负载固定，token 路由数异构 | token 可能收到零个或多个专家 |
| DeepSeek-V3 | token 选 routed experts | batch bias 更新 + 小 sequence loss | 将 batch 均衡与任务 gate 解耦 | 单序列热点、节点通信仍需处理 |

### 2.3 Expert Choice：专家选 token

Expert Choice 将“每个 token 选择固定个数的专家”反过来，改成每个专家从 token 集合中选固定容量的 bucket。这样专家负载通过分配规则变得可控，但每个 token 最终被零个、一个或多个专家选择，计算量按 token 而异；需要保证每个 token 都收到专家输出时，还要加额外约束。

它说明负载均衡可以写进路由拓扑，而不只作为训练损失；代价是改变 token 覆盖和路由语义，并要在批次内对 token 做专家侧排序/选择。原论文在 T5 设置下与 Switch Top-1、GShard Top-2 比较预训练速度、语言理解微调和不同专家数；其报告的收敛时间与任务分数限定于这些实验设置。[Expert Choice §3–4](https://arxiv.org/html/2202.09368)

## 3. 专家粒度与知识分工

### 3.1 DeepSeekMoE：细粒度专家与共享专家

传统 MoE 专家通常是较宽的 FFN。若一个专家接收多种 token，它可能要把多类模式压在同一组参数里；若不同专家都学到常见知识，也会造成重复。DeepSeekMoE 针对这两个问题提出两种结构变化：

1. **细粒度切分**：将每个专家 FFN 的中间维度拆成更小的 FFN，并按比例增加每 token 激活的小专家数，使总专家参数与激活计算保持可比。路由器由此能组合更细的知识单元。
2. **共享专家隔离**：让所有 token 都经过少量 shared experts，处理共同知识；其余 routed experts 则更集中学习有条件的模式，试图减少通用参数在路由专家间重复。

论文用组合数说明路由空间的变化：16 个专家 Top-2 有 $\binom{16}{2}=120$ 种组合；把每个 FFN 切为 4 份后，64 个细粒度专家 Top-8 的可能组合数为 $\binom{64}{8}$。这是组合空间的理论计数，不等于训练后实际出现或有用的专业分工。论文通过保持总参数和激活参数相同的消融比较细粒度与共享专家，提供的是特定训练和模型设置下的结构证据，而非“越细越强”的规律。[DeepSeekMoE §3–4](https://arxiv.org/html/2401.06066)

Mixtral 8×7B 是较直接的 Top-2 MoE 实例：每个 token 经 router 选择 8 个标准 FFN 专家中的两个，输出按 gate 权重合并。它帮助解释总参数与 per-token active 参数的差异；论文还明确给出 32K context 和模型/训练结构。Mixtral 的能力比较对应论文当时选用的语言基准、prompt 和检查点；其 active 参数量不能单独解释实际显存、并发和速度。[Mixtral §2–5](https://arxiv.org/html/2401.04088v1)

### 3.2 PEER：把“专家”变成可检索的微型参数块

PEER（Parameter Efficient Expert Retrieval）探索百万级微型专家。若直接对每个 token 与百万个独立键打分，路由开销会很大；PEER 使用 product-key retrieval，将 key 拆成两个低维子空间，分别检索候选后组合专家索引，避免对所有完整 key 作穷举比较。其专家可由单神经元式 FFN 构成，因此它更像动态组合参数单元的层设计，而不是传统的宽 FFN 专家集合。

论文在语言建模 isoFLOP 对照和专家数量/活跃专家数消融中研究 performance–compute tradeoff。它支持“更高专家粒度可能扩展容量”的研究方向；实际系统仍要解决百万级权重的存储、embedding lookup 局部性、专家融合 kernel 和优化稳定性，不能把论文层结构当成已被验证的百万专家生产模型。[PEER §2–3](https://arxiv.org/html/2407.04153)

## 4. 负载均衡：任务目标与路由目标如何相互作用

辅助负载损失把专家使用率加进训练目标，直观且有效，但它可能与语言建模目标竞争：路由器需要按内容选择专家，均匀分配则推动 token 分散。移除辅助项可以减少这种目标干扰，却不保证系统负载自动合理。

DeepSeek-V3 的 DeepSeekMoE 路由对每个 token 与 routed expert 计算 sigmoid affinity，再选 Top-$K$，并在 gate 中加入 per-expert bias。训练时监控一个 batch 内专家负载；过载专家的 bias 按固定 update speed 下调，欠载者上调。bias **只影响 Top-K 路由选择**，最终与专家输出相乘的 gate 仍来自原始 affinity，因此这个 bias 不是由语言建模损失直接学习的普通门控参数。

“Auxiliary-loss-free”描述其主要 batch-wise 均衡机制，但报告也保留一个系数很小的 sequence-wise balance loss，用来防止单条序列内部极端失衡。可以把路由选择概括成 $g^{\prime}_{i,t}=\mathrm{TopK}(\sigma(u_t^T e_i)+b_i)$，随后用于专家输出的 gate $g_{i,t}$ 仍由原始 affinity 归一化；batch 结束后，过载专家 bias 按步长下调、欠载专家 bias 上调。bias 是负载反馈控制量，不是通过语言损失反向传播学习的参数。batch 均衡允许不同序列/领域在不同专家上呈现不同模式；sequence 均衡则可能在单样本层面施加更强约束。DeepSeek-V3 还使用 node-limited routing 限制一个 token 分发到的节点数，以控制跨节点通信；其路由和负载机制必须与分布式训练拓扑一起理解。[DeepSeek-V3 §2.1.2–2.1.3](https://arxiv.org/html/2412.19437v2)

这组设计揭示负载均衡至少有三层：每专家 token 数是否过载；单个 sequence 中路由是否极端集中；跨设备节点间通信是否均匀。一个 batch 的专家计数均衡，不能推出每条请求尾延迟均衡；专家计数接近，也不能推出专家承载的计算量相等。

## 5. 路由怎样落到设备上

专家并行（Expert Parallelism, EP）将不同专家分片到 GPU/TPU。一个典型 MoE 层的执行链是：

```text
router 打分/选专家 → 按专家重排 token → all-to-all 发送 → 专家 FFN → all-to-all 回传 → gate 加权合并
```

稀疏性减少了专家 FFN 的算术量，却引入不规则通信。路由结果决定同一设备接收多少 token；热点专家可能使某些设备比其他设备更晚完成；若 token 的目标专家跨越多个节点，网络传输和同步会成为延迟瓶颈。batch 增大可以摊销权重读取和通信，但交互式小批次与在线并发的路由分布可能不同于预训练批次。

DeepSeek-V3 技术报告把专家路由、节点拓扑和通信重叠一并设计：其特定配置将 routed experts 部署到 8 个节点、64 张 GPU，并限制每 token 最多发往 4 个节点；DualPipe 与通信实现尝试重叠计算和 all-to-all。论文报告的训练成本/吞吐来自整套架构、精度、集群和并行实现，不能归因于“MoE 激活参数少”一个因素。[DeepSeek-V3 §3](https://arxiv.org/html/2412.19437v2)

从部署角度，MoE 还有一个常见误区：未激活专家不做这一步的 FFN 计算，但它的权重仍需存放在 GPU、CPU 或远端节点；量化、卸载和 expert caching 会改变内存带宽、专家加载和尾延迟。性能报告至少要区分 prefill/decode、吞吐/单请求延迟、batch、模型权重常驻策略、KV cache、量化和互联，不能用 active parameter count 替代这些指标。

本节给出路由与 EP 的概念执行链；并行训练中 DP、TP、PP 与 FSDP 如何切分状态和安排通信，见[训练基础设施](../../Infra/TrainingInfra/report.md)。固定版本的 dispatch → grouped GEMM → combine、运行时负载迁移及 DeepEP 数据面见 [MoE 执行与专家通信](../../Infra/MoEExecution/report.md)。三者分别讨论模型路由、训练状态并行和固定执行实现，不能把各自论文的吞吐数字拼成横向排名。

## 6. 实验如何比较与开放问题

| 对比问题 | 必须对齐/报告的条件 | 避免的误读 |
|---|---|---|
| 路由结构能否改善质量？ | 总/激活参数、训练 tokens、数据、损失、基线架构 | 将更大总参数或更多训练数据误归因于 router |
| 负载损失是否伤害任务目标？ | 负载定义（expert/batch/sequence/device）、损失系数、容量与 token drop | 把“无辅助损失”写成“完全无负载约束” |
| MoE 是否更快？ | GPU/TPU、节点互联、并行配置、batch、prompt/output 长度 | 用理论 active FLOPs 代替端到端 latency/throughput |
| 专家是否形成分工？ | 路由统计、同预算消融、专家替换/行为分析 | 把不同 gate 频率直接解释成有意义的语义专家 |
| PEER 的高基数设计是否有效？ | isoFLOP 对照、专家检索成本、存储与内核设置 | 把层设计论文当作生产规模模型评测 |

开放问题包括：负载均衡怎样避免抹平有用专业化；不同 sequence/domain 的负载应如何适配线上并发；专家路由能否在分布变化和持续学习时保持稳定；百万级微专家在真实硬件上的检索、存储与稀疏执行成本是否仍优于粗粒度 FFN；如何让“专家专业化”通过行为干预验证，而不是只从激活可视化推断。

### 推荐阅读顺序

1. [Shazeer et al.](https://arxiv.org/html/1701.06538) §2–4：Top-K 门控、噪声探索和负载损失。
2. [GShard](https://arxiv.org/html/2006.16668) §2–3 与 [Switch Transformers](https://arxiv.org/html/2101.03961v3) §2：Top-2/Top-1、capacity 和设备分片。
3. [Expert Choice Routing](https://arxiv.org/html/2202.09368) §3–4：反转路由方向后的异构 token 计算。
4. [DeepSeekMoE](https://arxiv.org/html/2401.06066) §3–4：等参数/激活预算下的 expert granularity 与 shared expert 消融。
5. [DeepSeek-V3](https://arxiv.org/html/2412.19437v2) §2–3：bias 均衡、sequence loss、node-limited routing 与通信协同。
6. [PEER](https://arxiv.org/html/2407.04153) §2–3：product-key 与百万级微型专家的设计边界。

### 主要原文

- [Outrageously Large Neural Networks](https://arxiv.org/html/1701.06538)：稀疏门控、负载崩塌和分布式带宽约束。
- [GShard](https://arxiv.org/html/2006.16668)、[Switch Transformers](https://arxiv.org/html/2101.03961v3)、[Expert Choice](https://arxiv.org/html/2202.09368)：token-choice 与 expert-choice 路由。
- [Mixtral of Experts](https://arxiv.org/html/2401.04088v1)、[DeepSeekMoE](https://arxiv.org/html/2401.06066)：Top-2 宽专家与等预算的细粒度/共享专家方案。
- [DeepSeek-V3](https://arxiv.org/html/2412.19437v2)：负载偏置、辅助损失范围、节点路由和系统实现。
- [Mixture of A Million Experts](https://arxiv.org/html/2407.04153)：product-key 专家检索层。
