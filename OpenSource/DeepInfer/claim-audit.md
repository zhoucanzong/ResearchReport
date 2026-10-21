# DeepInfer结论复核与阅读边界

> 对象：`9bd9cf243fc53ef9afbf8f04d391d989117d6ab9`；2026-10-22，`code-researcher deep`。主报告见 [report.md](report.md)，完整覆盖见 [sources/MANIFEST.md](sources/MANIFEST.md)。

## 高影响结论的语义复核

| 结论 | 回到源码检查的关键证据 | 判定/适用范围 |
|---|---|---|
| 本发布是离线内核，不是完整服务 | README明确未提供KV系统/分离服务/DP负载均衡；Engine保留do_save_kvcache等空钩子 | **支持发布范围**，不能推出生产体系的所有组件均已实现 [README.md:38](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/README.md#L38) [deepinfer/engine/llm_engine.py:801](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/engine/llm_engine.py#L801) |
| ZOS隐藏CPU后处理与排批气泡 | Worker在launch当前forward后处理前步，保存当前step；显式event同步仍存在 | **支持机制**，不承诺实际开销为零或本轮测得加速 [deepinfer/worker/worker.py:143](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/worker/worker.py#L143) [deepinfer/worker/worker.py:182](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/worker/worker.py#L182) [deepinfer/worker/worker.py:248](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/worker/worker.py#L248) |
| 抢占并非统一重算恢复 | COMPLETION配置闸门，SO抢占直接FINISHED_PREEMPTED，普通请求reset/requeue | **支持条件化行为**，不称SO可透明恢复 [csrc/engine/scheduler.hpp:98](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/csrc/engine/scheduler.hpp#L98) [csrc/engine/scheduler.hpp:766](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/csrc/engine/scheduler.hpp#L766) |
| 短输出优先不是严格按到达时间LCFS | decode排序键get_output_len，取尾端并抢占另一端 | **按代码限定**；注释LCFS不能独立支撑last-arrival解释 [csrc/engine/scheduler.hpp:622](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/csrc/engine/scheduler.hpp#L622) |
| confidence与proposal q不同 | DFlash分开计算、pool分开保存；验证读取logprobs | **支持角色区分**；不称confidence本身是已校准概率 [deepinfer/model_executor/models/mtp/dflash.py:308](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/models/mtp/dflash.py#L308) [deepinfer/model_executor/layers/sampler.py:446](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/layers/sampler.py#L446) |
| 变长预算有轮次隔离 | N−2决定total_q，较新估计分请求；schedule/process配对断言 | **支持控制路径**；未证明所有随机选择无偏 [csrc/engine/mtp_varlen.hpp:160](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/csrc/engine/mtp_varlen.hpp#L160) [csrc/engine/mtp_varlen.hpp:191](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/csrc/engine/mtp_varlen.hpp#L191) |
| 数值残差不是精确p−q | penalty=5e-5，CUDA减exp(draft_lp−penalty)；源内有界分析 | **支持数值取舍**；本轮未测实际误差或全多步误差界 [deepinfer/model_executor/layers/tilelang_ops/common.py:53](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/layers/tilelang_ops/common.py#L53) [deepinfer/model_executor/layers/tilelang_ops/cuda/fused_sample.py:435](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/layers/tilelang_ops/cuda/fused_sample.py#L435) |
| mask/compact等价不是无截断等价 | 两者共享截断SWA可见域，compact变query布局；部署文档称近似bounded replay | **支持比较边界**；不称截断不损精度 [deepinfer/model_executor/input_metadata/yoco.py:1](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/model_executor/input_metadata/yoco.py#L1) [doc/inference_deployment_qa.md:183](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/doc/inference_deployment_qa.md#L183) |
| 输出/元数据可能下一步复用 | pybind借用vector，RequestOutputPool与API即时clone | **支持寿命约束**，没有本轮原生内存压力测试 [csrc/engine/pybind_scheduler.cpp:34](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/csrc/engine/pybind_scheduler.cpp#L34) [deepinfer/entrypoints/llm.py:175](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/entrypoints/llm.py#L175) |
| batch-invariant测试不能解释成所有自由生成一致 | 单条回放设置golden_token_ids，固定EP8模型case | **保留测试真实强度**；未扩大到所有随机设置 [tests/models/test_batch_invariant.py:91](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/tests/models/test_batch_invariant.py#L91) |

## 工具检查的实际含义

已运行官方`scan_repo.py`、`build_evidence_index.py`和`claim_audit.py`。扫描结果：336文件、63,630文本行，Python54,929行、C++5,909行；这是源码规模，不是阅读覆盖百分比。

三份正文生成时检查了**215处固定SHA的源码行级链接，涉及43文件**：本地对应文件存在、起始行在范围内。该检查没有把“行存在”当成“句子为真”；上表另做语义对账。新增来源manifest和本页的链接同样按固定源码生成。

`claim_audit.py --lang zh`的结果：

| 正文 | 高影响词命中 | 无邻近路径线索 | 人工处置 |
|---|---:|---:|---|
| report.md | 10 | 1 | 命中测试表头“证据的边界”，非独立行为结论 |
| runtime-and-lifetimes.md | 4 | 0 | 运行次序和生命周期仍按上表回源核验 |
| speculation-cache-and-so.md | 9 | 2 | 命中Mermaid节点和“数值取舍”标题；节点证据在图后，标题证据在正文 |

不为清零将源码路径塞进标题、表头或图节点；告警保留为阅读线索。此处报数基于本页生成前的三份正文；后续正文如增删高影响词，应重跑计数。

## 本轮未运行的验证

没有安装DeepInfer依赖、构建扩展、执行pytest、启动设备模型、下载权重、运行benchmark/评测，也没有测试对外HTTP推理服务。主报告的profile HTTP仅指源码中可选的profile控制入口，**不是已交付OpenAI兼容推理API**。[deepinfer/engine/llm_engine.py:235](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/deepinfer/engine/llm_engine.py#L235) [README.md:38](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/README.md#L38)

未完成的深读包括：全部NPU路径、attention/低精度kernel内部、外部FlashMLA/DeepGEMM/DeepEP、EPLB算法、完整CP>1行为与生产存储/路由。现有测试文件和作者报告数字只证明“验证方法/自述存在”，不代表本轮复现通过。
