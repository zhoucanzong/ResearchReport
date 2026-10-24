---
display_name: MoE 执行与专家通信
type: repo-research
domain: Infra
subject: MoEExecution
upstream: https://github.com/deepseek-ai/DeepInfer@9bd9cf243fc53ef9afbf8f04d391d989117d6ab9
date: 2026-10-24
evidence: 固定版本源码精读
status: completed
---

# MoE 执行：token 如何抵达专家，又如何回到原序

## 读者先看什么

MoE 的路由不只是“选几个专家”。一个 token 的隐藏向量要被送到持有目标专家的 rank，按本地专家分组后完成两层 MLP，再把结果送回原 rank 并按路由权重合并。这里真正难读的部分，是路由结果、分组布局、跨设备缓冲区和异步事件必须在同一步里保持一致。

本专题精读 DeepInfer 的一条显式 EP 路径：gate 生成 top-k 路由 → DeepEP `EPBuffer.dispatch` → DeepGEMM 分组 GEMM 与 SwiGLU → DeepEP `combine`。先读[执行路径与边界](implementation/deepep-v2-dispatch-compute-combine.md)，再按其中的固定版本链接回源码。

DeepInfer 在满足 NVLink 域和数据类型等条件时还会走 DeepGEMM Mega MoE 融合路径；它不调用这条显式 `dispatch → grouped GEMM → combine` 序列。报告会说明两条路径的分界，但不把专题扩成 GPU kernel 清单。[DeepInfer `mlp.py`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L184-L201) [DeepGEMM `mega/__init__.py`](https://github.com/deepseek-ai/DeepGEMM/blob/1fc9c66975ee322d628b3288534ca0e9ce12a64d/deep_gemm/mega/__init__.py#L18-L76)

## 这条路径的关键认识

- **dispatch 不只是搬运向量，也建立后续布局契约。** DeepEP 返回按本地专家展开的 token、路由权重和 `EPHandle`；handle 保存 combine 逆转路由所需的源 token 元数据、前缀和、扩展布局以及原始 `topk_idx`。DeepInfer 将 handle 的 `psum_num_recv_tokens_per_expert` 直接作为分组 GEMM 的 PSUM 布局输入。[DeepEP `ep.py`](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/buffers/ep.py#L27-L61) [DeepInfer `mlp.py`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L585-L598)
- **专家分组边界不是普通的等长 batch。** DeepInfer 开启 `do_expand=True`，每个专家区域按 DeepGEMM 给出的对齐值留布局间隔；handle 中的 PSUM 前缀和表达真实 token 数与对齐槽位的关系，DeepGEMM 的 `use_psum_layout=True` 据此读写分组矩阵并处理间隔。对齐值和 grouped layout 是两端共享的契约。[DeepInfer `mlp.py`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L469-L488) [DeepEP `EPHandle`](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/buffers/ep.py#L43-L61) [DeepGEMM `gemm.hpp`](https://github.com/deepseek-ai/DeepGEMM/blob/1fc9c66975ee322d628b3288534ca0e9ce12a64d/csrc/apis/gemm.hpp#L181-L233)
- **这条实现把重叠机会放在共享专家与 combine 之间。** dispatch 以异步方式提交通信，但 DeepInfer 随即对该事件调用 `current_stream_wait()`，之后才开始 routed-expert GEMM，因此源码路径没有显示这两者重叠。routed GEMM 后，DeepInfer 捕获当前流事件，计算 shared expert，并把该事件交给 combine；DeepEP 将 combine epilogue 延迟至事件等待后。代码结构允许 combine 通信与 shared-expert 计算交叠，是否获得性能收益仍需设备测量。[DeepInfer `mlp.py`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/v4_modules/mlp.py#L585-L610) [DeepEP `ep.py`](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/buffers/ep.py#L770-L843) [DeepEP `event.py`](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/utils/event.py#L39-L60)
- **buffer 和 handle 的所有权跨越不同层。** DeepInfer 的 `userbuffer` 长期持有 EPBuffer，退出时显式 destroy；一次 dispatch 的 handle 则由 `EPBuffer` 创建，并被本次 combine 消费。handle 持有的 `topk_idx` 按引用保存且在使用期间不得原地修改。异步 event 还持有流依赖和延迟 epilogue；过早丢弃事件或复用路由张量会破坏这个借用期。[DeepInfer `userbuffer.py`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/parallel_utils/userbuffer.py#L55-L95) [DeepInfer `userbuffer.py`](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/parallel_utils/userbuffer.py#L227-L234) [DeepEP `ep.py`](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/buffers/ep.py#L96-L111)

## 适用范围与证据边界

DeepInfer 固定提交 `9bd9cf2…` 的 gitlink 将 DeepEP 固定为 `f6aa38f…`、DeepGEMM 固定为 `1fc9c66…`；这里的库级 API 解释对应这些依赖版本。[DeepInfer 固定版本树](https://github.com/deepseek-ai/DeepInfer/tree/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/vendor) [DeepEP 固定版本](https://github.com/deepseek-ai/DeepEP/tree/f6aa38fe06cd4a0489e7730365d4e0114970a2f3) [DeepGEMM 固定版本](https://github.com/deepseek-ai/DeepGEMM/tree/1fc9c66975ee322d628b3288534ca0e9ce12a64d)

本文聚焦 DeepInfer 显式 EPBuffer 路径，源码阅读覆盖输入/路由交接、专家分组计算、流事件和资源所有权；不推断任意 rank 拓扑、所有 dtype 或硬件均可运行。单机/多机 hybrid 实际通信协议、网络拥塞与超时恢复需要读更深的 C++/CUDA 实现并在目标集群验证，本条目没有将其概括成已经证明的容错或扩展性结论。Mega MoE 路径只用于解释分流边界。[DeepEP `EPBuffer`](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/buffers/ep.py#L208-L288) [DeepEP `EPBuffer` init](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/buffers/ep.py#L298-L363)

**验证状态：** 本条为固定版本静态源码精读；没有在本机安装 DeepEP/DeepGEMM，没有运行多 rank 测试、模型、CUDA kernel 或性能基准。库内存在 dispatch/combine 和 Mega MoE 测试，不代表本次运行通过。[DeepEP EP 测试](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/tests/ep/test_ep.py#L61-L137) [DeepGEMM Mega MoE 测试](https://github.com/deepseek-ai/DeepGEMM/blob/1fc9c66975ee322d628b3288534ca0e9ce12a64d/tests/test_mega_moe.py#L245-L275)
