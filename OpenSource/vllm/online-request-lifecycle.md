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

## 未由本次静态追踪确立的行为

- 浏览器/客户端断连是否在特定 ASGI server 与代理配置下可靠触发上述迭代器关闭，需要运行时验证。
- worker 错误、deadline 超时及跨进程背压的完整终止语义未在本专题追踪。
- 没有服务端、模型或 GPU 实验；本文结论是固定源码中可见的控制路径。

与 [SGLang 在线请求专题](../sglang/online-request-lifecycle.md)可按责任边界对照；两个专题固定源码日期不同，比较不构成同版本实现或性能评测。
