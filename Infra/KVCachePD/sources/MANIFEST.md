# KVCachePD — 来源清单

核查截止：2026-10-23。原文、官方文档与源码 revision 分开记录；不同版本的 benchmark 数字不合并。论文 PDF/仓库 checkout 均位于仓库外临时目录，未加入共享 paper-cache 或本仓库。

| ID | 固定来源 | 关键定位 | 本专题使用范围 |
|---|---|---|---|
| S1 | Qin et al., *Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot*, USENIX FAST ’25, pp.155–170, 2025-02-25–27. | [USENIX paper/PDF](https://www.usenix.org/conference/fast25/presentation/qin)；§3.1–3.2/Figs.2–4（KV 层次与传输）；§4.1–4.2/Alg.1（Conductor scheduling）；§5.1–5.4, Table 2, Figs.1/8（分离报告的基准/传输结果）。 | **[精读原文]** 最终会议版作为主要系统证据。arXiv `2407.00079v5` 是更长的后续预印本，标题、内容与部分 headline 数字不同；不把其扩展模拟/75% claim 混入 FAST ’25。PDF SHA-256 `543e56c541523c5e807d2231370f96749b2294bc901266397a7265b18ae2c130`，临时 `/tmp/mooncake-paper/`。 |
| S2 | Liu et al., *LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference*, arXiv `2510.09665v2`, revised 2025-12-05. | [官方 HTML v2](https://arxiv.org/html/2510.09665v2)：§4 connector/manager；§5.1–5.3 chunking/buffer；§6 vLLM hooks；§8.1–8.7 workloads、cache、remote store 与 PD evaluations。 | **[精读原文]** 系统论文，当前记录未发现会议/期刊版；实验使用 LMCache v0.3.6。跨请求 context caching 与同一请求 PD transfer 分开解释。“up to 15×”限论文指定重复文档工作负载、硬件、容量和吞吐设置。PDF SHA-256 `a1b6a90258c7e9091f24603ca4cff85f9f47410be10f5de89b7f902a2d3f641`，临时 `/tmp/lmcache-paper/`。 |
| S3 | `LMCache/LMCache@ff9185d419e1ce55c9f4f1ad84a4f4f1f06af7be`, 2026-10-23, `[Perf][MP] Callback-driven LookupState for scheduler lookups (#5960)`. | [固定仓库 tree](https://github.com/LMCache/LMCache/tree/ff9185d419e1ce55c9f4f1ad84a4f4f1f06af7be)：`config.py:297–305`（PD async 默认）、`storage_backend/__init__.py:132–143`（factory 后端选择）；其余 connector/adapter/cache/storage/NIXL/proxy 锚点见[实现追踪](../implementation/lmcache-vllm-v1.md)。 | **[固定源码深读]** 只追 `LMCacheConnectorV1Dynamic` + `lmcache.inprocess.v1` + 默认 `PDBackendAsync`。覆盖 scheduler lookup、block allocation、connector metadata、async sender、receiver allocation/key登记、NIXL DONE、proxy gate、D-side lookup/copy/layer wait、部分 miss、rollback 和 abort。没有运行 server/GPU/测试；未见可取消已提交 NIXL coroutine 的 handle，不能宣称 abort 可中断 RDMA。 |
| S4 | LMCache live MP docs, read 2026-10-23. | [MP configuration](https://docs.lmcache.ai/mp/configuration.html)、[L2 storage](https://docs.lmcache.ai/mp/l2_storage.html)、[metrics](https://docs.lmcache.ai/mp/observability/metrics.html). | **[官方动态文档，当前状态快照]** 仅支撑当前配置/指标边界：request tags/TTL 属元数据，不自动成为 cache identity/tenant isolation；L1/L2 与论文 v0.3.6 路径分开标注。文档是 live URL，不当作不可变版本或回溯论文证据。 |

## 既有专题的关系

- [vLLM](../../../OpenSource/vllm/report.md) 与 [SGLang](../../../OpenSource/sglang/report.md) 已解释各自引擎内 block/radix 前缀复用；本专题不重写本地 APC 数据结构。
- [DeepInfer](../../../OpenSource/DeepInfer/report.md) 的固定发布说明明确没有提供完整 KV 服务与 PD 分离；其空 hooks 不作为远端存储实现证据。

## 审核与限制

- 本次 code-researcher 静态追踪限定在 LMCache 单一 commit/配置切面；未运行服务、测试、NIXL transfer 或 GPU copy。
- 固定 commit 源码锚点检查 13 组路径/行区间，全部在本地 checkout 存在且不越界；渲染站点的链接/锚点检查无失效。
- Canonical `claim_audit.py`：主报告 8 条高影响候选/2 条机械提示（frontmatter evidence 和 §4 标题）；实现追踪 2/0。该脚本只做邻近路径提示，不代替对代码路径含义和论文实验条件的语义核查。
- 论文实验数字均为作者报告；本专题没有复现实验，也未将 FAST ’25、arXiv v5 与 LMCache v0.3.6/2026 dev 源码的结果拼接比较。
