# Mooncake：KVCache-centric 服务与 P/D 分离

## 固定来源

- Qin et al., *Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot*, USENIX FAST ’25, 2025-02-25–27, pp. 155–170. [Official paper page](https://www.usenix.org/conference/fast25/presentation/qin), [PDF](https://www.usenix.org/system/files/fast25-qin.pdf).
- 论文 PDF SHA-256 `543e56c541523c5e807d2231370f96749b2294bc901266397a7265b18ae2c130`, cached outside repository in `/tmp/mooncake-paper/`.
- Related preprint: arXiv [`2407.00079v5`](https://arxiv.org/abs/2407.00079v5), title *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving*. This later, longer preprint has different headline claims and additional sections; its numbers are not merged with the FAST ’25 paper.

## System design

Mooncake treats KV as a shared cache resource. The Conductor selects prefill and decode instances using cached-prefix length, queue load, estimated transfer time, and prefill time (§4.1–4.2, Algorithm 1). The cache stores paged blocks with keys incorporating block/prefix identity and deduplicates shared prefixes; policies include LRU eviction for unaccessed blocks and heuristic replication/movement for hot prefixes (§3.1, Figures 2–4).

In the same-request P→D path, prefill builds KV; Mooncake streams layers/chunks into the decode node while prefill runs. The paper describes batch transfer operations such as register local memory, allocate a batch, submit transfer and poll status; the decode request is scheduled after required KV arrives (§3.1–3.2.3). The paper specifies transfer complete/error status, but does not document a cross-node transaction, stale-generation fencing, retry idempotency, or a general request-cancellation contract.

## Evaluation and limits

The main deployment test uses 16 nodes × 8 A800 80GB, four 200-Gbps RDMA NICs per node, LLaMA3-70B dummy model, and vLLM v0.5.1 as baseline (§5.1–5.2.2, pp. 162–164). Workloads include two sampled Kimi traces and a synthetic request stream (Table 2). Effective request capacity is measured against both TTFT and TBT SLOs; TBT uses the average of the longest 10% token intervals. Reported improvements vary by workload and threshold. Prefill compute saved, cache hit-rate increase, and transfer bandwidth are separate experiments (§5.2–5.4); do not combine them into one speedup.

The final conference paper reports deployment history separately from this testbed. It uses sampled/constructed workloads and a dummy model, so the figures illustrate tested system behavior, not independent production replication. High-bandwidth RDMA and workload prefix repetition are important conditions.

**Reading takeaway:** Mooncake combines cross-request KV reuse, remote storage and same-request P/D transfer; these operations share infrastructure but have separate objectives and completion signals. The paper gives a scheduler and transfer design, not a universal atomic cache transaction or cancellation guarantee.
