# vllm 源码证据与复核边界

- 复核：2026-10-22，使用 `code-researcher deep`（evidence-quality、runtime-story、reading-coverage、claim-audit），重新运行官方 `scan_repo.py`。
- 固定来源：[vllm-project/vllm@fa75d3456d60a5ffe923818c4b495295675b38e1](https://github.com/vllm-project/vllm/tree/fa75d3456d60a5ffe923818c4b495295675b38e1)；[源码tarball](https://codeload.github.com/vllm-project/vllm/tar.gz/fa75d3456d60a5ffe923818c4b495295675b38e1)。
- 仓库外临时阅读目录：`/tmp/research-code-audit-20261022/vllm`；上游源码未入库，未构建或执行上游系统。临时目录不是长期保存承诺，可按固定SHA重新取源。
- 本轮核验的是下列强结论和运行切面，**不是全上游仓库逐行读完、测试全通过或所有配置行为已证实**。旧报告的机械零告警不代表语义通过。

- Traced/Audited：`vllm/v1/core/sched/scheduler.py:588-596,1014-1022,1649-1692`，KV不足/抢占与重新准入；`core/kv_cache_manager.py:264-325`、`core/block_pool.py:666-804`、`core/single_type_kv_cache_manager.py:735-875`，查表/引用释放/淘汰及细粒度匹配。
- Traced/Audited：旧runner `v1/worker/gpu_model_runner.py:3432-3462,4329-4335` → `v1/sample/rejection_sampler.py:450-522,829-890,1003-1085`，grammar、接受与残差。
- Audited：新runner `v1/worker/gpu/model_runner.py:1633-1667` → `worker/gpu/spec_decode/rejection_sampler.py:418-452`；仅确认调用边与invalid_drafts，没有复现分布。
- Audited：`worker/block_table.py:114-153`、`config/speculative.py:604-609`；“append-only”与greedy草稿语义。
- 不作结论：GPU运行/性能、所有attention内核、所有connector、Mamba/SWA分支、新旧runner全配置等价。

### 在线流式请求生命周期补充

- 同一固定来源 `vllm-project/vllm@fa75d3456d60a5ffe923818c4b495295675b38e1`；本次扩核静态追踪 `api_utils.py:53-94`、`sse_keep_alive.py:36-65`、chat serving `:299-422,469-526,912-919`、`async_llm.py:324-382,795-842,924-947`、`output_processor.py:53-103,593-661`、EngineCore `:554-559,657-687`、scheduler abort/释放 `:2733-2859` 与 KV manager `:620-630`。
- 阅读了测试定义但未执行：`tests/entrypoints/openai/chat_completion/test_serving_chat.py:1115-1215`（mock stream cancel/close/error）、`tests/v1/engine/test_async_llm.py:684-730`（引擎级取消与请求清理）、`tests/v1/engine/test_abort_final_step.py:144-164,265-319`（执行中最后一步 abort、connector 状态及清理）。它们没有端到端模拟 HTTP socket 断连。
- 覆盖单 choice 文本 SSE 的路由、准入、EngineCore 执行边界、输出 collector、错误块、SSE 结束和条件性断连清理。没有运行服务/模型/pytest/GPU；真实 ASGI disconnect 传播、用户可见 queue-full 状态码、deadline 与端到端背压仍未验证。KV connector 和执行中 GPU step 可延后 block 归还。阅读稿：[online-request-lifecycle.md](../online-request-lifecycle.md)。这不是整份仓库或所有 runner 配置的重新审计。

引用格式：本条目的简写 `文件:行` 均相对上述固定源码根；回源使用 `https://github.com/vllm-project/vllm/blob/fa75d3456d60a5ffe923818c4b495295675b38e1/<path>#L<line>`。保留旧阅读记录不将其覆盖等级自动升级成本轮已核。
