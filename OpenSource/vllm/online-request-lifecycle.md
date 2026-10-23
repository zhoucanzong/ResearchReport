# vLLM 在线流式请求：从 HTTP 到取消与 KV 回收

> 本文补上主报告明确留出的在线服务入口与异步引擎切面。它追踪一条普通文本 `POST /v1/chat/completions`、`stream=true`、单个 choice 的源码路径，不覆盖多模态请求、全部 runner 变体或运行时性能。

## 固定源码与阅读边界

- 来源：[`vllm-project/vllm@fa75d3456d60a5ffe923818c4b495295675b38e1`](https://github.com/vllm-project/vllm/tree/fa75d3456d60a5ffe923818c4b495295675b38e1)，与[主报告](report.md)使用同一源码快照。
- 这是一条静态源码追踪：未启动 API server、未加载模型、未运行测试或测量背压/延迟。
- EngineCore 到 model executor 的交接可确认；具体 GPU runner 的 forward/sample 路径属于实现分支。主报告尚未确定旧版与模块化 runner 在所有配置下的默认选择，因此本文不把某个 runner 写成通用路径。

## 一条流式请求如何穿过系统

1. `/v1/chat/completions` 路由校验请求并交给 serving handler；流式结果被包装为 `StreamingResponse`，媒体类型为 `text/event-stream`。[路由与响应构造](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/openai/chat_completion/api_router.py#L43-L85)
2. serving 层把消息按 chat template 渲染成 engine 输入，建立 request ID 与采样参数，再调用 `engine_client.generate(...)`。`stream=true` 选择 chat completion 流生成器。[渲染与生成器选择](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/openai/chat_completion/serving.py#L299-L422)
3. `AsyncLLM.generate` 首次被消费时创建请求、经过准入队列、提交给 EngineCore，并为请求注册输出收集器；超出队列上限的请求在准入阶段处理。[准入与提交](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/async_llm.py#L324-L382) · [请求注册与 EngineCore 提交](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/async_llm.py#L480-L535) · [输出收集器](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/async_llm.py#L566-L586)
4. EngineCore 把请求交给 scheduler，再调用 model executor 执行；在常规同步 step 中，执行返回后进入 token sampling。[EngineCore 执行循环](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/core.py#L657-L687)
5. 后台输出处理器消费 EngineCore 结果，将 token ID 解码、检查停止条件并构造 `RequestOutput`，再放入该请求的 collector。[输出处理与投递](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/output_processor.py#L813-L853)
6. chat 流生成器把增量结果序列化为 SSE `data:` 块，按需发送 usage chunk，最后输出 `data: [DONE]`。[SSE 分块](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/openai/chat_completion/serving.py#L750-L816) · [终止标记](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/openai/chat_completion/serving.py#L912-L919)

这条路径把主报告里的 `Scheduler.schedule()` decode step 放回完整服务上下文：HTTP handler 与异步输出队列位于引擎之前/之后，EngineCore 才是把在线请求交给调度和模型执行的边界。它解释控制流与数据交接，不证明端到端队列有界或实际客户端能以某个速率消费。

## 客户端断开后发生什么

路由的取消装饰器说明：在 `StreamingResponse` 返回之前由 handler 侧监听 `http.disconnect`；响应开始发送后，断连监听交给 response 对象。[断连监听边界](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/serve/utils/api_utils.py#L53-L94) 如果响应迭代器因断连而关闭，keep-alive 包装器会取消待取结果的 task 并关闭上游生成器。[生成器关闭传播](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/serve/utils/sse_keep_alive.py#L21-L65) `AsyncLLM.generate` 在收到取消或 `GeneratorExit` 时调用内部 abort，并在 `finally` 中关闭输出 collector。[取消与清理](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/async_llm.py#L795-L803) · [collector 收尾](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/async_llm.py#L840-L842)

abort 从 OutputProcessor 转成 EngineCore 请求，再由 scheduler 标记请求结束、清理 encoder 状态并释放请求持有的 KV blocks。[abort 传递](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/output_processor.py#L599-L660) · [EngineCore 分派](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/core.py#L554-L559) · [scheduler 终止与 KV 清理](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/core/sched/scheduler.py#L2733-L2859) 释放可能被 KV connector 或正在执行的 GPU step 延后；源码不支持“断连即刻归还所有块”的表述。[KV manager 释放边界](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/core/kv_cache_manager.py#L620-L630)

## 取消、过载与错误的边界

这条链的取消保护分两段：`with_cancellation` 只在路由 handler 尚未返回时监听 `http.disconnect`；交出 `StreamingResponse` 后，断连监听由响应对象接管。[`api_utils.py:53-94`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/serve/utils/api_utils.py#L53-L94) 若响应迭代结束，SSE keep-alive 包装器会取消正在等待的 `anext()` 并 `aclose()` chat 流生成器。[`sse_keep_alive.py:36-65`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/serve/utils/sse_keep_alive.py#L36-L65) 这与 `AsyncLLM.generate` 对取消/`GeneratorExit` 调用 abort 的行为相接；但本仓库测试没有模拟真实 ASGI socket 断开，因此从网络事件到 EngineCore abort 的闭环仍是静态推断。正常生成器耗尽或被其 `except Exception` 处理的错误会写 `[DONE]`；cancel/close 属于另一条退出路径，不能假设客户端会收到终止块。[`serving.py:912-919`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/openai/chat_completion/serving.py#L912-L919)

EngineCore 的 step 在提交模型结果前处理已经到达的 abort 队列：模型执行 future 先完成，然后 `_process_aborts_queue()`，再 `scheduler.update_from_output()`。[`core.py:657-687`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/core.py#L657-L687) 因而取消不会证明当前 GPU forward 被中断；若请求块仍可能被执行中的 step 或 connector 使用，scheduler 延后把它们归还 block pool。[`scheduler.py:2843-2859`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/core/sched/scheduler.py#L2843-L2859)

队列准入在 AsyncLLM 侧按未完成请求数和仍在 prefill 的 prompt token 数设置上限，超限抛出 `QueueOverflowError` 或 `MaxQueuedTokensError`；注释把预期响应写作 HTTP 503。[`async_llm.py:324-382`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/async_llm.py#L324-L382) 对这条流式路径，serving 先把惰性 `engine_client.generate()` 交给 `StreamingResponse`，随后才由 SSE 生成器消费；若准入拒绝在首次迭代时发生，serving 层源码会将异常转为流内错误块。于是“配置的队列上限对应 HTTP 503”仍需通过真实 HTTP 路径核验，不能只从 `check_admission()` 的 docstring 推到客户端可见状态。[`serving.py:391-422,523-526,912-919`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/openai/chat_completion/serving.py#L391-L422) [`api_utils.py:70-94`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/serve/utils/api_utils.py#L70-L94)

输出收集器是单个待交付槽：producer 不阻塞；DELTA 输出在消费者落后时合并。因此它会合并待处理增量，但这不足以证明 EngineCore、进程间传输、SSE 与客户端之间存在端到端有界背压。[`output_processor.py:53-103`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/output_processor.py#L53-L103) Worker/output-handler 异常会写入各请求 collector；对每请求普通异常，`generate()` 会 abort 并包装为 `EngineGenerateError`，而 `EngineDeadError` 走引擎死亡分支，不应混称为同一请求级恢复路径。SSE 已开始后，serving 层把错误写进数据流。[`async_llm.py:795-839,924-932`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/async_llm.py#L795-L839) [`output_processor.py:593-597`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/v1/engine/output_processor.py#L593-L597) [`serving.py:912-919`](https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/vllm/entrypoints/openai/chat_completion/serving.py#L912-L919) 本次没有追踪可适用于这条请求的通用生成 deadline，也没有把 worker 故障恢复或网络背压当作已验证行为。

## 代码里有测试，但本次没有运行

- `tests/entrypoints/openai/chat_completion/test_serving_chat.py:1115-1215` 用 mock 输出对 chat SSE generator 做 cancel/close、错误和 usage 边界检查；对取消/关闭断言没有 `[DONE]`，但没有真实 HTTP、AsyncLLM 或 EngineCore。
- `tests/v1/engine/test_async_llm.py:684-730` 直接取消 100 个引擎级生成任务，在输出处理器中检查无未完成请求并复用 request ID；它测试的是 generator/task cancellation，不是浏览器或 socket 断开。
- `tests/v1/engine/test_abort_final_step.py:144-164,265-319` 把 `execute_model` 挂起后发起 abort，验证 abort 在输出更新前获处理、最终状态为 abort、KV connector 收到 `FINISHED_ABORTED` 且没有遗留请求。这覆盖了“取消撞上最后一步”的资源边界，不证明 kernel 会被中止。

这些是源码中的测试定义和断言，不是本次测试结果；本次未启动服务、模型、pytest 或 GPU。SGLang 姊妹稿还显式追踪了等待队列/运行中 abort 与 503 queue-full，但固定 SHA 是 2026-10-23 的另一版本；两文只可对照责任边界，不作同版本优劣结论。[SGLang 生命周期专题](../sglang/online-request-lifecycle.md)

## 未由本次静态追踪确立的行为

- 浏览器/客户端断连是否在特定 ASGI server 与代理配置下可靠触发上述迭代器关闭，需要运行时验证。
- deadline 超时及跨进程/网络背压的完整终止语义未在本专题追踪。
- 没有服务端、模型或 GPU 实验；本文结论是固定源码中可见的控制路径。
