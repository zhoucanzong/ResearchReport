# sglang 源码证据与复核边界

- 复核：2026-10-22，使用 `code-researcher deep`（evidence-quality、runtime-story、reading-coverage、claim-audit），重新运行官方 `scan_repo.py`。
- 固定来源：[sgl-project/sglang@2a08e261ecd4cdfb04ec354f9005f18b88108b7d](https://github.com/sgl-project/sglang/tree/2a08e261ecd4cdfb04ec354f9005f18b88108b7d)；[源码tarball](https://codeload.github.com/sgl-project/sglang/tar.gz/2a08e261ecd4cdfb04ec354f9005f18b88108b7d)。
- 仓库外临时阅读目录：`/tmp/research-code-audit-20261022/sglang`；上游源码未入库，未构建或执行上游系统。临时目录不是长期保存承诺，可按固定SHA重新取源。
- 本轮核验的是下列强结论和运行切面，**不是全上游仓库逐行读完、测试全通过或所有配置行为已证实**。旧报告的机械零告警不代表语义通过。

- Traced/Audited：`python/sglang/srt/mem_cache/registry.py:89-146,191`（默认实现）；`unified_radix_cache.py:585-659,1132-1248`（match/touch/insert/evict交接）；`radix_cache.py:345-351,419-426,582-611,650-690`（遗留root/锁/helper）。
- Audited：`python/sglang/srt/speculative/eagle_utils.py:980-1014` → `python/sglang/kernels/jit/include/sgl_kernel/speculative/sampling.cuh:72-150`，目标-only缓冲、接受、残差与CDF。
- Traced：scheduler overlap及EAGLE draft→verify→publish→draft_extend的报告调用链；只读，不把线程/GPU异步路径画成已观测时序。
- 未闭合：EAGLE上游拒绝分支、Rust与Python对拍、topk>1/阈值变化的分布证明、完整HTTP入口和真实性能。

引用格式：本条目的简写 `文件:行` 均相对上述固定源码根；回源使用 `https://github.com/sgl-project/sglang/blob/2a08e261ecd4cdfb04ec354f9005f18b88108b7d/<path>#L<line>`。保留旧阅读记录不将其覆盖等级自动升级成本轮已核。
