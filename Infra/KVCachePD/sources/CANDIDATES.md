# 候选筛选 — KVCache / Prefill-Decode 分离

筛选日期：2026-10-23。范围刻意限于“一个系统论文对照 + 一条固定代码实现”，回答 KV 如何从模型进程的 cache 变成共享/远端数据，以及 D 端何时真的可读；不做所有缓存厂商的吞吐排名。

| 候选 | 决定 | 理由 |
|---|---|---|
| Mooncake, USENIX FAST ’25 | 精读，系统设计对照 | 统一展示 KV-centric storage、Conductor 与 P/D 生命周期；最终会议版和 arXiv v5 内容/数字不混用。 |
| LMCache, arXiv:2510.09665v2 | 精读，缓存层/PD路径 | 直接讨论 connector、storage manager、chunked transfer、跨请求 cache reuse 与 P/D，并明确了短上下文和低带宽限制。 |
| LMCache `LMCacheConnectorV1Dynamic` + `PDBackendAsync`, commit `ff9185d…` | 固定源码深读 | 用一条 vLLM V1 路径核实 sender、receiver、proxy 与 D-side GPU copy 的状态边界；不扩成全仓架构或性能复现。 |
| Mooncake 当前仓库 Transfer Engine / Store / 多引擎 connector | 延后 | 横跨 C++ Transfer Engine、Store、多个 serving integration；首个专题若同时追，会混淆传输原语与具体 KV admission/ownership。后续可作为独立 repo-research 切面。 |
| 更广泛的 KV serving benchmarks | 暂不纳入 | workload、模型、SLO 与 network 配置差异大；在统一协议卡前不拼成排行榜。 |

主要边界：不把 L1/CPU/L2 命中率等同于端到端命中；不把 receiver key 可见等同 payload complete；不把 transfer complete 等同于 D GPU KV 可用；不同论文 headline 不合并。
