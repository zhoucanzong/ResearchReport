# EAGLE-4：用「按实测成本调树」把自回归草稿做成一个通用 drafter

> **一手来源**：EAGLE-4 Team《EAGLE-4: One Flexible Drafter for All Batch Sizes and Hardware》（Eagle AI，**预印本 PDF**，2026；仓库 `github.com/eagle-hq/EAGLE-4`）。本文按该 PDF 的 Abstract/§1/Table 1–3 与仓库 `docs/architecture.md`、`docs/known-limits.md` 读取；**未在 arXiv 检索到该文**（arXiv `all:"EAGLE-4"` 返回 0 条），故不标 arXiv 号。
> **证据类型**：论文 PDF 已读（方法、条件数字）+ 官方实现文档已读（机制细节、限制）；**未独立运行**任何 EAGLE-4 实验。
> **一句话**：EAGLE-4 没有换草稿形态（仍是 EAGLE 的单层自回归 drafter），而是**把"这次该草稿多深/多宽"交给一个按硬件与 batch 实测成本算出来的控制器**——于是同一个 drafter 覆盖 batch=1 到 512、GPU/CPU/手机三种平台。

---

## 1. 它要解决的是"草稿预算"问题，不是"草稿质量"问题

EAGLE 系此前的已知短板是**高 batch 下验证成本反超**（本条目 §4 记过：EAGLE 在 SGLang batch=24 已跌破 1.0×）。EAGLE-4 的立论正是这一点：

- **并行块草稿（DFlash 2、DSpark）把 block size 当超参**，必须先定死；而"最优块长随 batch 增大而缩短"（PDF §1：极大队列时最优推测长度可能只剩 1–2 个 token），于是大 batch 下大量草稿 token 被丢弃——**草稿算力白烧**。
- **自回归草稿天然支持"随时停"**：EAGLE-4 用 **EAGLE-Harness** 在推理时决定树宽、树深与验证预算；判据是**草稿成本 vs 草稿置信度**的权衡。
- 配套的第二件是 **EAGLE Efficient LM Head**：低秩候选检索先在小候选集上算，再用完整 LM head 精确重算选中项，论文称把草稿模型开销降 **>40%**。

## 2. 机制：三处可控点

| 环节 | 做法（依据） |
|---|---|
| **草稿模型本身** | 仍是**单层** Transformer：每草稿位置 **0.44B** 层参数；对比 DFlash 2 **1.66B**、DSpark 1.65B（Table 1）——论文算得每草稿 token 的 FLOPs 约少 **3.8×**，大 batch 下矩阵乘变 compute-bound 时这一项最要紧 |
| **候选打分（Efficient LM Head）** | rank-r 估计先在词表分片上挑少量候选，只对候选做全 LM head 行精确打分（`architecture.md`：`low-rank candidate head`） |
| **树与验证预算（EAGLE-Harness）** | 预演一次轻量 warm-up，刻画当前硬件成本；SGLang 上**每两个草稿层**判断"再深一层是否值回草稿时间"，并按各验证宽度的实测成本选本轮验证宽度；vLLM 上验证宽度由调度器按 batch 固定，于是**每轮只决定草稿深度**（`architecture.md` 第 3 步） |

**接口形态**（对我们是可复用的一条工程经验）：`eagle-harness` **不 patch 引擎**，通过各引擎插件入口注册（SGLang `sglang.srt.plugins` / vLLM `vllm.general_plugins` / TokenSpeed `tokenspeed.plugins`），并在注册前**校验宿主 hook 是否齐全**——缺一个就"什么都不注册 + 打一条错误"，引擎照常跑。

## 3. 已报告的条件数字（全部来自论文与官方支持矩阵，非本次复现）

| 场景 | 结果 | 条件 |
|---|---|---|
| SPEED-Bench 定性集，Qwen 3.8 27B | **863.8 tok/s**，为 DFlash 2（672.6）的 **1.28×**、DSpark（618.6）的 **1.40×** | 4×NVIDIA B300，并发 1，T=0 |
| 同上 | **3.59×** 于 vanilla | 同上，并发 1 |
| 同上 | **1.70×** / **1.99×** 于 DFlash 2 / DSpark | 同上，**并发 512**（两并行草稿在此跌破 vanilla）|
| Nemotron-3.5-Super-VL-120B-A12B | **2.0×** 于 vanilla | 并发 512，HumanEval |
| AWS c5.xlarge（4 vCPU/8GB） | **2.71×**（四基准平均） | 单请求，T=0，4-bit Gemma-4-E2B-it |
| Motorola Razr 70 Ultra（8 CPU 核） | **3.62×** | HumanEval 单请求，T=0，热降频前测量 |
| 官方实现文档（SGLang，4×B300） | **3.42× / 2.09× / 1.39×** | 并发 1 / 8 / 64 |

树参数（论文 Table 2 脚注）：并发 1 用 **12-4-16**（深 12、宽 4、最多验 16），并发 512 用 **15-1-16**。

## 4. 边界：官方文档自己写下了"什么时候不如不开"

这部分比加速比更值得记，因为它把"EAGLE-4 = 永远更快"直接否掉：

- **SGLang 默认命令在单卡上高并发会倒退**：并发 64 实测 **0.73×**、256 实测 **0.59×**（相对同引擎不开投机）。原因三条：radix cache 与"切回普通解码"的交互、默认树把四卡服务器**运行请求数上限压到 32**、单卡按每个已接纳请求预留验证状态（只能接纳普通解码约 1/4 的请求）。
- **四卡默认配置同样会跌**：`--tp-size 4` 实测并发 64 **0.80×**、128 **0.48×**、256 **0.37×**、512 **0.32×**；官方给的是**另一套 high-load recipe**（四卡专用），热身期 0.95×/0.97×，重启后 1.01×/1.00×。
- **vLLM / TokenSpeed 目前不会自动回退普通解码**：并发 >64 可能比不开投机更慢，官方建议"先别在这些负载上开"。
- **单卡高负载尚不支持**；`--disable-radix-cache` 的官方建议只对四卡成立（单卡会卡在草稿图捕获）。
- **正确性口径是"批不变性"问题**：官方承认普通解码自身就随 batch 变化（512 并发下有 1–3 条 prompt 超出 2-ULP 规则）；开确定性推理后 token 级一致，但**此时 EAGLE-4 在高并发直接退回普通解码、没有加速**。
- **许可证**：EAGLE-4 是 **source-available**，不是 OSI 开源；商用有年营收 2,000 万美元等条件（仓库 README/License）。引用其工程结论时要带这条。

## 5. 与同族、与并行草稿的关系

- **对 EAGLE-1/2/3**：草稿形态不动（单层、特征级自回归、树验证），改的是**"预算控制器"**——把 EAGLE-2 的静态/动态树参数，变成按当前 batch×硬件的实测成本现算。所以它更像**系统层工作**而不是新的草稿架构。
- **对 MTP（DeepSeek-V4 / GLM-5 / Kimi K3 / Qwen3 / Gemma 4 的内置头）**：论文明确说这些 MTP 沿用 EAGLE 的核心形态（target hidden + token embedding 拼进轻量 drafter），EAGLE-4 的优势在**小 batch 吞吐**与**自适应**，而不在"另一种机制"。
- **对 DFlash 2 / DSpark（并行/扩散式草稿）**：争的是"固定块长 vs 自适应长度"。EAGLE-4 的论点是**大 batch 下块草稿会算废**；反过来，块草稿在小 batch 时延上有自己的位置。

## 6. 读后的三个判断（研究推断，非论文主张）

1. **这条线的竞争点已经从"接受率"转向"算力预算分配"**：论文自己说"不接受只看接受长度（acceptance length）作为评价指标"，因为动态验证的收益不在接受率里。评估 EAGLE-4 必须看端到端吞吐。
2. **"一个 drafter 通吃"是工程卖点，也是评估陷阱**：它把复杂度从"训多个 drafter"转移到"为每种硬件/形状标定成本表"。成本表不匹配时性能会掉（官方文档：换模型/draft/TP/精度/attention backend/引擎都要重测）。
3. **对我们既有结论的影响**：本条目 §4 那条"EAGLE 高 batch 跌破 1.0×"不是被推翻，而是被**收窄**为"默认配置 + 单卡/未用 high-load recipe 时成立"；EAGLE-4 在四卡 high-load recipe 下能撑到 512 并发不被普通解码反超。

## 7. 未能确证

- 论文未给**独立的第三方复现**；所有数字来自作者团队与官方支持矩阵。
- 论文 PDF 中未见 "Limitations" 独立章节（搜索未命中），边界主要来自仓库 `docs/known-limits.md`（更新于 2026-10-23）。
- EAGLE-4 与 **CAST**（arXiv 2510.26577，成本感知动态树）的关系：CAST 的官方代码库路径写作 `EAGLE-Research/sglang-eagle4`，暗示同源，但**本文未确认二者是否为同一方法的论文/工程两面**。
