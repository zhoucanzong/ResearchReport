---
type: research
domain: Infra
subject: ServingEvaluation
date: 2026-10-24
evidence: primary-paper-reading-and-existing-fixed-source-reports
status: current
---

# 在线 LLM Serving：SLO、Goodput 与请求完整性

**范围**：解释在线请求负载下如何同时判断交互体验、系统容量和资源代价。重点是 TTFT、token 间延迟、SLO 达成率、goodput，以及被拒绝、失败或取消的请求如何进入统计。它不重述引擎内部请求控制流，也不制定跨模型通用评测规范。

**阅读顺序**：先读 [SLO 与系统指标精读](papers/2410.14257-slo-goodput.md)，理解常用指标的反直觉边界；再读 [DistServe 精读](papers/2401.09670-distserve.md)，看 SLO 如何参与资源划分与容量优化；最后回看本页的请求分母和资源回收核对项。

## 先问清“每秒服务了什么”

离线吞吐回答模型在一段计算中处理多少 token；在线容量回答持续到达请求时，系统能以多大速率提供满足交互约束的服务。两者之间隔着排队、准入、首 token 等待、逐 token 交付、请求终止和状态清理。若只看完成请求的平均 tok/s，拒绝请求和被中途终止的请求可能从统计中消失，资源占用也可能仍在发生。

把每个客户端发起的请求作为一次 offered request，并在压测开始时就纳入队列。至少分别计数：

| 状态 | 含义 | 报告时要保留什么 |
| :-- | :-- | :-- |
| offered | 客户端按负载计划发起 | 到达时间、输入/期望输出分布；这是负载分母 |
| admitted | 服务接受并分配执行机会 | 排队时间、拒绝/超载原因；拒绝不能从 offered 总数中抹掉 |
| completed | 正常生成并结束 | 完成请求数、实际输出 token 数、SLO 是否满足 |
| failed | 服务端错误、超时或基础设施故障 | 失败阶段、错误类、已生成 token、是否触发重试 |
| cancelled | 客户端主动取消与服务端主动终止分别记录 | 谁发起取消、停止生成时间、资源何时可再次使用 |

这是本专题建议的计数账本，不是两篇论文共同采用的标准。对 offered load，容量曲线应同时给出已完成且符合 SLO 的 goodput、SLO attainment 的分母与上述终态计数。外部用户取消是否算服务失败取决于问题定义，但必须单列，不能与服务主动丢弃合并。

## SLO 把延迟拆成用户能感受到的约束

- **TTFT** 从服务收到请求到首个输出 token；它主要反映排队与 prefill，但须写明时钟从客户端发出、入口接收还是准入后开始。
- **TBT** 约束相邻 token 之间的间隔，能发现局部停顿；若只看 P95/P99 TBT，它不一定反映一次早期停顿对后续阅读的影响。
- **TPOT** 通常是首 token 之后的平均每 token 时间。平均值会把长时间卡顿与其他快速 token 抹平，所以要同时报告逐请求尾部、token-gap 分布或明确的交互 SLO。
- **端到端延迟** 从请求提交到最后 token 交付；它能覆盖全程，但同一个总时长可能来自不同的首 token 等待、生成节奏和输出长度。

这些指标不能互相替代。更不能把服务端“已生成”时间直接当成客户端“已收到”时间：缓冲或传输会改变用户观察到的 token 时间线。尾延迟必须给出请求集合、时钟边界、分位数和统计窗口；均值或 P99 单值都不说明拒绝、取消和未完成请求怎样计入。

## SLO attainment 与 goodput 的互补及盲点

SLO attainment 是满足单请求约束的请求占比；goodput 通常是单位时间内满足约束的完成请求量（论文也可能按 token 计权）。给定目标 attainment（例如 90%），goodput 可用于寻找系统在满足尾部体验约束时的最大接入速率。这比饱和吞吐更适合比较在线容量，但数值依赖 SLO、工作负载和计数口径。

Wang 等人指出，基于相邻 token 间隔的 TBT 可以被人为缓冲输出“改善”：前一个 token 送得越晚，后续 token 的间隔测量反而越容易满足阈值。另一个盲点来自二元 SLO：一旦某请求被判定违约，它对 goodput 贡献归零；优化器可能直接终止这类请求，把资源转给新请求。论文提出 smooth goodput，以每个请求生成的 token 数减去用户无 token 可读时长的惩罚来保留部分服务价值。它揭示二元达标指标可能诱发的系统行为，不是已被普遍校准的统一评分标准；惩罚函数、权重和读速设定会改变最优负载点。

由此可见，“失败请求分母”与“好请求吞吐”回答不同问题：前者让读者知道 offered workload 中有多少请求遭拒、出错、超时或被截断；后者刻画系统在指定质量约束内提供服务的速率。建议两者并列，且把失败请求的服务耗时与已消耗资源也保留下来，避免只按成功请求算延迟和 token/s。

## SLO 也是资源分配目标

DistServe 将 prefill 和 decode 分配到不同 GPU 池，分别调节并行度，并把资源方案与 TTFT/TPOT 目标一起优化。动机不是抽象的“拆分更快”：prefill 计算密集、单步较长，可能拖慢 decode 的 token 间隔；两阶段合批又让一阶段的资源配置牵制另一阶段。分离可以针对两种约束配资源，但新增 KV 传输和放置成本必须进入容量估算。

论文使用 ShareGPT、HumanEval、LongBench 工作负载，从 Poisson 到达率生成请求时序；主要容量点要求超过 90% 请求满足 TTFT 和 TPOT SLO，另外报告 99% attainment。实验在 4 节点、32 张 A100-80GB GPU 的集群上完成，OPT 13B–175B、FP16，跨节点链路 25 Gbps；不同任务设置不同 SLO。因此其“最高 7.4× 请求率”是特定基线、工作负载、模型与门槛下的结果，不能当作任意现代引擎或生产负载的通用加速比。

## 请求结束不等于资源已归还

一个请求可能已经对客户端报错或停止输出，执行 step、KV connector、异步传输或缓存层仍可能持有它的状态。把取消时间戳当成资源释放时间会高估系统恢复容量；反过来，缓存保留的 prefix KV 也不一定是泄漏，需区分请求私有占用和可复用缓存。

本库已有固定源码切面可供继续追读： [vLLM 在线请求生命周期](../../OpenSource/vllm/online-request-lifecycle.md)记录取消如何传至 scheduler、KV block 回收可能等待 GPU step/connector；[SGLang 在线请求生命周期](../../OpenSource/sglang/online-request-lifecycle.md)说明运行请求 abort 可能越过一个 decode forward 才进入清理；[KV Cache 与 P/D](../KVCachePD/report.md)区分传输完成和引擎 KV 可读。它们是各自源码版本的路径证据，不是同一版本性能比较，也没有证明客户端断连、deadline、负载和资源回收的端到端实测。

因此容量测试至少应分别观测：请求对客户端结束的时间、scheduler/worker 不再执行它的时间、KV 私有块可复用的时间，以及缓存保留量。对取消/失败后的资源复用，应把释放延迟和后续请求受影响情况纳入测试，而非从一条静态清理路径推出负载下的回收性能。

## 读者可以怎样比较两项 serving 结果

先对齐模型和量化、输入/输出长度分布、请求到达过程、warm/cold cache、GPU 与并行配置、SLO 定义、SLO attainment 目标、计时边界和失败策略。然后逐项回答：

1. 速率是 offered、admitted 还是 completed？失败和主动取消是否进入总请求数？
2. TTFT/TPOT/TBT 是从哪个时钟点测起，是否含入口和排队；报告的是均值还是逐请求尾部？
3. SLO 约束每个 token、首尾 token，还是整条请求？超标请求是继续生成、被拒绝还是中断？
4. goodput 按满足 SLO 的请求数还是 token 数计？系统是在固定 GPU 预算下比容量，还是固定负载下比资源？
5. 请求失败后，执行和 KV 状态何时释放？结果是论文报告、源码推断还是本次压测观测？

通用 benchmark 工具和跨领域效度见[评测科学](../../Evaluation/EvaluationScience/report.md)。引擎如何具体处理准入、流式响应、错误和取消，见上述 vLLM/SGLang 源码精读；本专题聚焦跨实现的负载、SLO、结果分母和资源账，不替它们写第二份实现报告。

### GuideLLM 中两个常被混为一谈的分母

以固定 GuideLLM v0.8.1 源码为例，报告的 `request_totals.total` 将 measurement window 内的 successful、incomplete（例如取消）和 errored 请求相加；SLO attainment 使用不同分母：已得到足够 objective 数据的成功请求，加上所有错误请求；被测量时长边界截断的取消及无法计算目标指标的成功请求不计入该分母。因而“请求总数”“可判定的 SLO 样本数”和“合规请求数”是不同数值，不能从一个总请求字段反推出 SLO 达标率。[分母实现见固定源码定位](sources/MANIFEST.md)

该版本从发送请求时开始记录时钟，基于客户端接收到并解析的流式内容事件计算首 token 与 inter-token latency；若单个 SSE chunk 含多个模型 token，chunk 时间戳并不能揭示每个 token 的单独间隔。profile 也定义不同负载形状：串行同步、固定并发、恒定请求率和 Poisson 到达不可互称为“不同负载强度”。这些是 GuideLLM 的特定实现定义，用来说明压测工具会怎样塑造统计对象，并非通用协议标准。[计时、profiles 与来源定位](sources/MANIFEST.md)

## 证据边界与开放问题

两篇论文展示了 SLO 约束如何影响资源架构，以及 goodput/SLO 指标可能如何诱发不符合用户体验的策略。它们没有形成统一的失败/取消分类标准；DistServe 的主评测也不是逐个剖析 HTTP 错误、客户端取消和释放延迟。对这些边界，本库当前依据是 vLLM、SGLang 与 LMCache 的固定版本静态源码阅读，缺少真实 socket 断连、deadline、过载阶跃和 GPU 资源回收联合实验。

本专题的 serving 性能数字均引用论文作者报告，没有在本机复跑。GuideLLM 部分只用固定源码解释指标与请求分母，不提供真实引擎 benchmark 或性能结论；静态源码中的时钟与清理定义不能替代目标负载下的端到端测量。

下一步若做运行研究，优先在一个固定引擎上构造闭环：open-loop 到达率扫描与突发负载；同时记录所有 offered request 的终态和端到端时间；注入超载、超时、客户端取消及执行错误；核对请求退出后 KV blocks / worker slots 何时重新可用。再与一个不同策略引擎比较时，应固定相同模型、硬件、工作负载和统计口径。没有该实测前，本文不宣称哪种引擎有更好的尾延迟或回收效率。

**本条目与相邻专题的关系**：这是 Infra 中关于在线容量、交互 SLO 和请求结果完整性的独立学习入口；评测科学负责更一般的效度和 benchmark 解释，vLLM/SGLang 报告负责代码路径，KVCachePD 负责缓存/传输状态。已有 backlog 中的机器可读跨引擎协议和压测工具校准仍是后续工作，不由本报告假定已经完成。
