# DeepInfer来源与阅读覆盖

- **固定对象**：[deepseek-ai/DeepInfer @ 9bd9cf243fc53ef9afbf8f04d391d989117d6ab9](https://github.com/deepseek-ai/DeepInfer/tree/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9)。2026-10-22通过`git ls-remote --symref … HEAD`解析到main及该SHA，再按完整SHA下载codeload tarball。
- **源码包**：[固定SHA tarball](https://codeload.github.com/deepseek-ai/DeepInfer/tar.gz/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9)，2,329,121字节；SHA-256 `0a4a1e96d48594f1e63dd7c4bb276a12e80d6efe5cf9adcbd295788bcb693406`。没有把移动main链接当版本身份；未取得提交时间，因此不虚构发布时间或commit标题。
- **许可证/包版本**：Apache-2.0；项目元数据version0.1.0。[pyproject.toml:9](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/pyproject.toml#L9) [LICENSE:1](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/LICENSE#L1)
- **仓库外阅读位置**：`/tmp/research-deepinfer-20261022/src`；源码、源码包与临时笔记未入研究仓库，不保证临时路径长期存在。GitHub API提交元数据请求遇rate-limit403，使用已解析SHA的codeload成功，不据API失败推断项目状态。
- **指纹**：[三份正文被引用文件SHA-256](READ_FILES_SHA256SUMS.txt)，43文件；清单自身SHA-256 `a2817fe9699eef77467b7051035ba002864c89ab9a835f546ae76f6ed52449a7`。这是引文所覆盖文件的指纹，非完整源码树Git身份的替代。

## 方法与报告结构

使用本地`/Users/zhoucanzong/Documents/codes/code-researcher/skills/code-researcher/SKILL.md`的deep路径：先跑`scan_repo.py`，再读research-method、runtime-story、report-planning、module-investigation、visual-reporting、evidence-quality、reading-coverage和claim-audit。问题选为“公开引擎怎样把离线请求变成token，以及异步、草稿和缓存共同要求什么状态契约”。据此安排主报告、运行专题和机制专题，不按文件目录堆摘要。

本轮实际运行skill扫描、`build_evidence_index.py`与`claim_audit.py`；局部脚本只检查报告链接、源码行范围、指纹和数据格式，**未执行DeepInfer构建、模型、pytest或GPU/NPU算子**。本文“traced”指静态追过调用边，未冒称运行trace。

## 阅读覆盖

| 区域/文件 | 等级 | 实际支撑 | 尚未覆盖 |
|---|---|---|---|
| `entrypoints/llm.py`、`examples/_config.py`、`examples/offline_inference.py` | Traced | 输入参数、设备初始化顺序、入队/聚合/clone/解码 | 所有非法参数组合、示例实际运行 |
| `engine/llm_engine.py` | Traced +关键段Audited | 初始化block/state、add_request、step、process_MTPInfo→process_outputs→build_request_outputs、DeferredRelease、集成空钩子 | 全模型加载、profile HTTP行为、所有shutdown竞态 |
| `csrc/engine/scheduler.hpp` | Traced +关键段Audited | DP步型投票、decode资源不足、元数据、在途与抢占、接受前缀回填、MTP信息移位 | 全prefill预算求解、fork/split和所有abort组合 |
| `sequence.hpp`、`block_manager.hpp`、`pybind_scheduler.cpp`、`zos.cpp` | 关键段Audited | KV/在途账本、块引用、借用vector、相邻batch输入准备 | 所有对象池异常路径、native内存安全穷举 |
| `worker/worker.py` | Traced | forward→前轮post-process→sample→延迟当前回填、remap、event边界 | 真实设备流时序与延迟 |
| `worker/model_runner.py`、`worker/base.py` | 代表方法Traced | forward/sample发射、guard、prewarm性能曲线 | 完整CUDA graph捕获/内存profile与CP follower所有分支 |
| `models/mtp/dflash.py`、`layers/mtp_info_pool.py` | Traced | 特征→draft→confidence/logprobs→pool、DSpark字段与DFlash类名对应 | head训练数据/目标、所有量化head实现 |
| `csrc/engine/mtp_varlen.hpp`、`tilelang_ops/schedule_mtp_varlen.py` | Audited | 时序分离的预算目标、CPU/GPU两阶段、参考算法及测试存在 | 设备对拍、校准/收益测量、全分布因果证明 |
| `layers/sampler.py`、`sampler_utils.py`、`tilelang_ops/{common,fused_sample,cuda/fused_sample}.py` | 关键路径Traced/Audited | SO先mask、proposal logprobs对齐、比值判据、5e-5残差penalty与源内解释 | 所有kernel/backend数值、全step误差累积 |
| `worker/cache_engine.py`、`input_metadata/yoco.py`、`models/deepseek.py`、`prepare_tensor_input_v4.cpp` | 关键段Traced | block/state布局、stored/dropped、consumer视图、keep与回退闸门 | 所有attention低精度布局、CP>1边界端到端对拍 |
| `structure_output/so_matcher_builder.py`及Sampler使用方 | Traced | future→pump→入队、临时draft推进/rollback、请求级失败 | XGrammar内部、所有timeout/cache/取消路径 |
| `parallel_state.py`、`v4_modules/moe.py`、runtime_config | Skimmed | DP/CP/EP分组及MoE调用/平台开关 | DeepEP/EPLB算法内部、跨机性能与容错 |
| 表内测试、YoCo等价脚本说明 | 有目的抽读 | 明确测试输入、断言和限制；区分golden轨迹、统计检验与运行证据 | 没有运行结果、无CI健康结论 |
| 其余336文件 | Scanned或未读 | 仅目录/语言/大小分类 | 不把扫描命中作为行为证据 |

## 引文等级

- **源码事实**：固定SHA实现直接支持的状态、调用、分支和接口，文中有文件:行。
- **仓库文档自述**：README发布边界、部署问答的线上结构/数字；作者是一手来源，但静态读取不等于独立运行验证。
- **研究解读**：性能/维护后果根据实现形态推导，明确标“设计解读”“维护推断”；不推测未见的设计意图。
- **受限核验**：真实GPU/NPU运行、性能、权重、外部KV服务、全采样正确性与容错；不并入“精读源码”已证实行为范围。

部署问答涉及3FS、路由、TTL、集群规模等内容；README同时明确其中若干服务未提供。本文仅在解释发布边界与某项机制时引用，不移植生产数字到本机/开源性能结论。[README.md:38](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/README.md#L38) [doc/inference_deployment_qa.md:124](https://github.com/deepseek-ai/DeepInfer/blob/9bd9cf243fc53ef9afbf8f04d391d989117d6ab9/doc/inference_deployment_qa.md#L124)
