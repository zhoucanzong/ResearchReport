---
display_name: MoE 执行与专家通信
type: repo-research
domain: Infra
subject: MoEExecution
upstream: https://github.com/deepseek-ai/DeepInfer@9bd9cf243fc53ef9afbf8f04d391d989117d6ab9
date: 2026-10-24
evidence: fixed-version-source-study
status: current
---

# MoE 执行：从专家路由到跨设备回收

**范围**：本专题不再讲一遍 MoE 的 router 如何训练，而是解释训练好的 top-k 路由如何变成设备上的执行路径：token 如何按目标专家分组、跨 rank 交换、由分组 GEMM 处理，再恢复原 token 顺序并合并权重。源码案例固定为 DeepInfer `9bd9cf243fc53ef9afbf8f04d391d989117d6ab9` 及其 DeepEP、DeepGEMM gitlink 依赖；这是一条具体实现路径，不代表所有 MoE 框架。[DeepInfer 固定版本树](https://github.com/deepseek-ai/DeepInfer/tree/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9)

## 先把问题说清：条件计算把算术变稀疏，却把数据移动变动态

普通稠密 FFN 对一个 batch 中的每个 token 应用同一组权重。MoE router 为每个 token 选少数专家；如果专家分散在多张卡上，执行器必须先根据每个 token 的目标专家重新分组，并把向量送到对应设备。计算后还要把结果送回源位置，按 router 权重合并。于是 MoE 的运行成本不只来自专家 MLP 的 FLOPs，还来自路由不均、两次跨设备交换、布局转换、buffer 容量和同步等待。

这与模型层面的“激活参数更少”不是同一个问题。稀疏路由减少每 token 需要执行的专家矩阵，却不会自动减少所有专家权重的驻留或传输；batch 内专家负载均衡也不自动等于设备延迟均衡。DeepSeek-V3 将专家路由、节点拓扑和通信重叠一起设计，正说明 MoE 的计算与集群通信要联合考虑；其训练数字只支持论文报告的模型、精度与集群条件，不能由 active parameter count 单独推出。[DeepSeek-V3 技术报告 §2–3](https://arxiv.org/html/2412.19437v2)

## 一次专家路由在执行器里要经历什么

```mermaid
flowchart LR
    A[hidden states] --> B[router: top-k 索引与权重]
    B --> C[按目标专家分组]
    C --> D[dispatch: 发往专家所在 rank]
    D --> E[本地 grouped GEMM 与激活]
    E --> F[combine: 逆路由并加权求和]
    F --> G[恢复源 token 顺序]
```

显式 EP（Expert Parallelism）路径至少有四个相互耦合的对象：路由索引/权重、按专家分组的 token 缓冲区、记录通信和布局信息的 handle、以及两次交换之间执行的专家矩阵乘法。若只看到“all-to-all + FFN”，就会漏掉最重要的实现契约：dispatch 的输出布局必须与 grouped GEMM 读取的行边界一致；combine 又必须拿同一条路由计划还原结果。

### dispatch 产生布局，也产生逆路由凭证

在 DeepInfer 固定版本中，`DeepseekMoE.forward` 根据路径条件分流：一类进入显式 gate → EPBuffer dispatch → routed experts → combine；满足相应设备域与数据类型条件时，另一类进入 DeepGEMM Mega MoE 调用。[DeepInfer `mlp.py:184–201`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L184-L201) [显式路径 `mlp.py:565–610`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L565-L610)

显式路径把 `topk_idx`、`topk_weights`、本地专家接收计数、token cap 和 expert alignment 传给 `EPBuffer.dispatch`。设置 `do_expand=True` 后，逻辑上的散列路由被展开成每个专家的连续 token 区间。实际有效 token 数和为了 kernel 对齐保留的行间隙不是同一概念；DeepEP 返回的 prefix sums 描述这层分组布局，`EPHandle` 还保存源 token 元数据、目标 buffer slot、拓扑和原始索引，供后续 GEMM 与 combine 使用。[DeepInfer `mlp.py:461–490`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L461-L490) [DeepEP `EPHandle`](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/buffers/ep.py#L27-L111)

这意味着 handle 不是可随意重建的“辅助信息”：dispatch 到 combine 期间，路由索引必须与其保持一致。DeepInfer 当前调用设置 `do_handle_copy=False`，所以张量生命周期和调用顺序就是接口契约的一部分。布局对齐值也从 DeepGEMM 查询后传给 DeepEP；只改一端的对齐或 prefix-sum 解释，可能让 grouped GEMM 读错专家行段。[DeepInfer `userbuffer.py:55–95`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/parallel_utils/userbuffer.py#L55-L95) [DeepInfer grouped GEMM `mlp.py:109–138`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L109-L138) [DeepGEMM PSUM layout](https://github.com/deepseek-ai/DeepGEMM/blob/1fc9c66975ee322d628b3288534ca0e9ce12a64d/csrc/apis/gemm.hpp#L181-L233)

### 分组 GEMM 不等于普通 batch GEMM

收到本 rank 的专家 token 后，DeepInfer 对同一套 expert prefix sum 做 gate/up grouped GEMM，再做 SwiGLU 和路由加权，最后执行 down grouped GEMM。BF16 与 FP8 activation 走不同 DeepGEMM API；FP8/FP4 权重、scale factor 布局和 SM90/SM100 kernel 分支也影响实际计算形态。所谓“分组”不是把变长专家 batch pad 成等长后即可忽略边界，DeepGEMM 的 PSUM layout 会显式消费每组前缀和，并在 scale-factor packing 时跳过对齐 gap。[DeepInfer `mlp.py:406–459`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L406-L459) [DeepGEMM grouped API](https://github.com/deepseek-ai/DeepGEMM/blob/1fc9c66975ee322d628b3288534ca0e9ce12a64d/csrc/apis/gemm.hpp#L181-L248)

专家接收 token 数差异很大时，一批 grouped GEMM 的可用工作量就不均匀；如果有少数专家 token 过多，忙 rank 可能成为本层临界路径。对齐间隙换来 kernel 可执行的连续布局，但会产生 padding/空隙开销；小 batch 时，通信和分组调度占总工作量的比例也可能上升。这些是从布局和执行序列得到的系统性后果，源码本身没有提供跨 batch、dtype 或设备的性能对比，不能把它们写成已经测出的延迟数字。

### combine 恢复顺序，异步事件只提供交叠机会

Combine 使用 dispatch 的 handle 和路由元数据，把专家输出映射回原 token，并按 gate 权重求和。DeepInfer 将 shared expert 的输出作为 combine bias；代码在 routed GEMM 后捕获 CUDA event，再执行 shared expert，并把事件交给延迟 combine epilogue。这样安排给 shared expert 计算与 combine 通信提供了重叠机会。

但 dispatch 返回异步 event 后，DeepInfer 立即在当前流等待，再开始 routed-expert GEMM；所以至少在这条代码路径中，不能声称 dispatch 通信与该 GEMM 已经重叠。`async_with_compute_stream=True` 也不等于所有后续算子自动并行：实际 overlap、等待位置和收益要在目标设备上用 profiler 或测量确认。[DeepInfer `mlp.py:574–610`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L574-L610) [DeepEP `EventOverlap`](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/utils/event.py#L39-L60) [DeepEP combine](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/buffers/ep.py#L770-L843)

## 显式 dispatch 与融合入口是在解决不同问题

固定源码显示，`DeepseekMoE.forward` 先按设备域与输入类型分流。显式 EPBuffer 路径把 dispatch、routed-expert grouped GEMM 和 combine 分成可见调用；调用方因此能安排 shared expert、量化转换与异步 epilogue，但必须维护 handle、专家布局、事件顺序和 buffer 所有权的一致性。[DeepInfer `mlp.py:184–201, 461–511`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L184-L201) [DeepInfer `mlp.py:406–459`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L406-L459) [DeepInfer `mlp.py:493–511`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L493-L511)

满足其 NVLink domain 与数据类型条件时，另一分支将 MoE 路径交给 DeepGEMM Mega MoE API；它把 gate/top-k、缓冲布局和 MoE 计算收进专用入口，减少调用侧显式管理的中间契约，但也受该路径支持的硬件条件约束，内部阶段更难独立安排和观测。[DeepInfer `mlp.py:184–201`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L184-L201) [DeepGEMM Mega MoE API](https://github.com/deepseek-ai/DeepGEMM/blob/1fc9c66975ee322d628b3288534ca0e9ce12a64d/deep_gemm/mega/__init__.py#L18-L76)

这两种接口不能简单概括为“通用版”和“快速版”：一条强调显式的通信与计算编排，另一条优先融合特定设备域内的执行。这个比较是对固定调用结构的设计解读；源码支持分流条件和入口差异，不证明任一路径在任意拓扑、dtype、batch 或模型上更快。[DeepInfer `mlp.py:184–201, 461–511`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L184-L201) [DeepGEMM Mega MoE API](https://github.com/deepseek-ai/DeepGEMM/blob/1fc9c66975ee322d628b3288534ca0e9ce12a64d/deep_gemm/mega/__init__.py#L18-L76)

## 训练侧均衡不是运行时负载的完整答案

MoE 训练会约束每个 expert 收到的 token 数，以减少 token dropping 或明显过载；DeepSeek-V3 的 batch-level bias 更新与轻量 sequence-level balance loss，是把跨 batch 和单序列热点分别处理的例子。[DeepSeek-V3 技术报告 §2.1.2–2.1.3](https://arxiv.org/html/2412.19437v2)

执行系统还要关心另一层：负载落在哪个 rank、节点间发送多少字节、每组 token 是否足以摊薄 GEMM 开销，以及哪张设备最后完成。专家 token 数相同，不代表字节数、计算量或链路距离相同；训练时全局均匀，也不保证在线请求里每个 batch 都均匀。node-limited routing 可以控制一个 token 跨越的节点数，却可能把路由选择限制在较小设备集合。它体现了“路由质量—通信局部性—负载平衡”的联合取舍，不只是路由器超参数。[DeepSeek-V3 技术报告 §2.1.3、§3](https://arxiv.org/html/2412.19437v2)

因此，研究或报告 MoE 执行性能时，至少要把模型/总专家数、每 token 激活专家数、EP/TP/DP 拓扑、每设备 token 分布、dtype、batch、prefill/decode 阶段、节点互联、buffer/对齐策略和计时边界放在一起。单报“激活参数量”不能解释通信，单报“all-to-all 带宽”也不能解释端到端 token 延迟。

## 读者应如何继续阅读

1. 先读[MoE 总览](../../LLM/MoE/report.md)中路由、负载均衡和专家并行部分，建立 token-choice / expert-choice、路由权重、辅助损失与通信的概念框架。
2. 再读 DeepInfer 的[主报告](../../OpenSource/DeepInfer/report.md)，理解一次请求的调度、状态和模型执行边界；本专题只放大其中的 MoE 专家通信路径。
3. 逐段读[DeepEP V2 dispatch–compute–combine 实现追踪](implementation/deepep-v2-dispatch-compute-combine.md)，关注 `EPHandle`、prefix sums、grouped GEMM 与 event 顺序如何形成跨库契约。
4. 最后回到 DeepInfer 固定版本 `mlp.py` 的显式 EP 和 Mega MoE 分支，判断具体硬件、dtype、并行组落在哪条路径。

本专题的研究范围是 DeepInfer 一个固定版本调用 DeepEP/DeepGEMM 的源码行为。它不证明所有 MoE 框架使用相同 buffer 协议、拓扑或 overlap；没有运行多 rank 通信、kernel、模型和性能测试，也没有从静态调用关系推断真实集群的速度、扩展效率或故障恢复。
