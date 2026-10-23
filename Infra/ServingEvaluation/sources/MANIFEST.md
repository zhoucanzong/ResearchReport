# 在线 Serving 来源与代码定位

| 来源 | 固定版本与阅读位置 | 在报告中的用途及边界 |
|---|---|---|
| Wang et al., *Revisiting Service Level Objectives and System Level Metrics in Large Language Model Serving* | [arXiv HTML v2](https://arxiv.org/html/2410.14257v2), §§2–5、§6.1–6.2 | SLO attainment、goodput、TBT 缓冲反例与 smooth-goodput。论文提出的具体公式和权重依赖其用户效用设定，不作为统一服务评分。 |
| Zhong et al., *DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving* | [arXiv HTML v3](https://arxiv.org/html/2401.09670v3), §§2–4、§6.1–6.4 | SLO 约束如何进入 P/D 资源配置和容量评测。7.4× 属于论文给定模型、工作负载、A100 集群和 SLO 条件。 |
| `vllm-project/GuideLLM` | [release v0.8.1](https://github.com/vllm-project/guidellm/tree/v0.8.1), commit `597bc014ef78daeb11312374022430939b611f11`。Profiles: `src/guidellm/benchmark/profiles/{synchronous,concurrent,asynchronous}.py`; stream timing: `src/guidellm/backends/openai/http.py:347–393`; TTFT/ITL/TPOT: `src/guidellm/schemas/base/request_stats.py:262–354`; request totals and SLO denominator: `src/guidellm/benchmark/schemas/metrics.py:1158–1352`; status classification: `src/guidellm/scheduler/worker.py:445–549`; accumulator: `src/guidellm/benchmark/schemas/accumulator.py:393–401`. | **[固定源码阅读]** 说明一个实际工具如何定义 arrival profile、客户端流事件计时、请求终态和 SLO 分母；不代表其他工具采用相同口径。固定版本 CLI `run` 未能通过本机最小环境的 `datasets` import，故未取得 GuideLLM runtime result。 |
| 本地 CPU mock protocol probe | 一次 stdlib `http.client` 对本机 mock SSE endpoint 的观察；无模型、GPU或外网。预设正常流、HTTP 429 和 HTTP 200 后提前 EOF 三种响应。临时执行记录不作为 benchmark 附件。 | **[本次局部实验]** 只确认客户端观察到的 SSE chunk 时序含本机调度/HTTP开销，且拒绝与提前 EOF 在 HTTP 层表现不同；不验证 GuideLLM 如何分类、不验证真实 serving 或引擎性能。 |

源码的请求分母、SLO 样本分母、计时起点和 duration-window 过滤规则有实现细节，引用时以该固定 commit 行号为准；换版本须重查。
