# LMCache：把 KV 搬运做成引擎外的分层存储

## 固定来源

- Liu et al., *LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference*, arXiv [`2510.09665v2`](https://arxiv.org/html/2510.09665v2), revised 2025-12-05. The checked arXiv record is a preprint; this audit found no proceedings/journal version.
- Paper Fetcher PDF SHA-256 `a1b6a90258c7e9091f24603ca4cff85f9f47410be10f5de89b7f902a2d3f641`, temporary `/tmp/lmcache-paper/`; shared `paper-cache` had no matching file.
- The paper evaluates LMCache v0.3.6. Current MP documentation and the fixed 2026 source snapshot are separate evidence and must not inherit the paper’s performance numbers.

## Connector, cache engine and storage manager

The connector reports externally matched prefix tokens to the scheduler, prepares request/page metadata, and invokes layer hooks for load/save (§4, §6). The token processor identifies hit prefix and unmatched suffix. A storage manager selects backend(s), while the cache engine handles keys, token chunks and layout conversion. On load, storage objects are gathered and returned to the model runner; on store, paged GPU KV is packed into contiguous streaming buffers before lower-tier transfer (§5.1–5.3).

The described default transfer chunk is 256 tokens, an I/O packing size formed from multiple engine pages/layers; it is not a semantic text chunk or tokenizer unit. Chunking permits DMA, batching and overlap with model work. Current MP configuration can round chunk size upward to satisfy KV geometry, so do not assume the paper’s 256-token default is a universal current runtime value.

## Distinguish cache reuse from P/D disaggregation

- **Context caching:** later requests may reuse a previously stored prefix, skipping some prefill; hit ratio depends on prompt repetition and cache capacity.
- **PD transfer:** one live request produces KV on P and sends it to D. It does not depend on a later request having a repeated prompt.

The paper evaluates both kinds of use. Cross-request cache experiments and PD transfer experiments have different request patterns, hardware/storage conditions and endpoints; “up to 15×” refers to particular repeated-document workloads, not a generic PD or cache speedup.

## Evaluation boundaries

The paper’s repeated-document test uses LMCache v0.3.6, an 8×H100 host, up to 500GB CPU-cache capacity, roughly 10K input tokens (20K for one model), at most 100 output tokens, and baseline vLLM versions 0.10.2/0.11.0 (§8.1–8.2). The remote-store experiment uses 15Gbps and TriviaQA/LongBench (§8.4). The PD experiment uses synthetic 8K input/200 output requests with NVLink-connected P and D (§8.5). The paper also notes that for short contexts or low bandwidth, loading cached KV can be slower than recomputing (§8.4, §8.7).

It does not specify a complete stable wire format, full cache-key namespace for model/tenant/layout isolation, or a universal retrieval error contract. Current MP docs say tags/TTL are metadata and do not automatically enforce cache identity/isolation. Use the code-trace note for one pinned V1 integration path; neither the paper nor this note validates every current backend.
