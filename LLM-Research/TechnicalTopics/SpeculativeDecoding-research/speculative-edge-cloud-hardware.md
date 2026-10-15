# 投机解码：端侧、边缘与硬件

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、会议 proceedings（ISSCC / ACM Web）、IEEE 期刊页、arXiv 预印本、机构知识库与官方工程博客整理生成。**注意：IEEE Xplore 与 ACM Digital Library 在本次核验时对本环境返回反爬拦截（IEEE HTTP 202 空响应、ACM Cloudflare 挑战页 403），相关条目已改用机构知识库/OpenAlex 元数据 + 官方工程博客交叉确证，并在文中逐条标明核验强度。** 加速比与能效数字受测试条件影响极大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮新增）
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦**端侧内存带宽约束、端云分工、以及硬件加速路线与算法路线的耦合**。它与 [speculative-systems-and-frameworks.md](speculative-systems-and-frameworks.md)（服务端框架生态）、[speculative-multimodal.md](speculative-multimodal.md)（多模态端侧场景）交叉。
> **证据等级约定**：**[精读原文]**、**[摘要级]**、**[二手]**，另加一档 **⚠️[受限核验]**（一手页面被反爬拦截，改由多个二手/元数据来源交叉确证）。
> **等级规则**：每条结论只取**一个主等级**（精读原文 / 摘要级 / 二手 / 受限核验）；**混合来源取最弱等级**并在正文注明来源类型（如 `[精读原文（vLLM 官方文档）]`）；不使用 `A + B`、`A（摘要层）` 这类复合标签。

---

## 1. 本章结论

1. **端侧投机解码的第一约束不是"草稿质量"，而是"内存带宽与专家权重搬运"**。这与服务端（算力/显存、batch 吞吐）的优化目标根本不同——服务端关心吞吐，端侧关心**每次前向的外部内存访问（EMA）与 IO 开销**。 **[精读原文]**
2. **端侧 MoE 与投机解码存在结构性不兼容**：投机解码用"少调用几次 target 换速度"，但**验证被拒 token 时仍然要加载专家**；批量验证又会激活**专家并集**，把稀疏计算重新推回密集内存访问。SS-MoE 与 EdgeXpert 都把这个不兼容点作为核心问题。 **[二手]**
3. **"端云协同"的真实瓶颈是通信，不是算力**。FlexSpec 指出既有框架的根本问题是 draft 与 target **紧耦合**：target 频繁演进 → 反复同步 → 通信开销吃掉加速收益。它的解法是**共享骨干（shared-backbone）**架构，让**单个静态边缘 draft 模型兼容一大族演进的云端 target**，从而免去端侧重训与反复下载，并叠加**信道感知的自适应投机长度**。 **[精读原文]**
4. **硬件侧的"投机解码专用单元"已经出现，并且指标口径与算法论文完全不同**。SMoLPU（ISSCC 2026）是 MoE 投机解码专用 LLM 处理器（NPU-CIM 核心），报的是 **µJ/token、能效倍数、每参数能量下降**，而不是 tokens/s 或接受率。 **[摘要级（⚠️ 受限核验）]**
5. **硬件路线与算法路线正在耦合**：Google TPU 上的扩散式投机（DFlash）之所以能拿到 **3.13×（峰值近 6×）token/s 提升**，关键不只是算法，而是把 proposer 与验证流水线重新映射到 TPU 的 MXU 上（**双缓存架构**解决 DFlash 非因果块扩散与 paged attention/Pallas 内核的不兼容）。 **[精读原文]**
6. **给工程判断的一句话**：端侧选草稿策略时，应先按**内存带宽 / IO 预算**筛掉不可行的方案，再谈接受率；端云分工时，应先算**同步通信量**，再谈草稿模型多强。

---

## 2. FlexSpec：端云协同与"冻结草稿 + 演进目标" **[精读原文]**

**基本信息**：Yuchen Li, Rui Kong, Zhonghao Lyu, Qiyang Li, Xinran Chen, Hengyi Cai, Lingyong Yan, Shuaiqiang Wang, Jiashu Zhao, Guangxu Zhu, Linghe Kong, Guihai Chen, Haoyi Xiong, Dawei Yin；arXiv 2601.00644（2026-01-02）；期刊版本 *IEEE Transactions on Mobile Computing*，DOI `10.1109/tmc.2026.3683574`。

**核验说明**：任务书给出的是 IEEE Xplore 页面（`document/11480773`），该页面在本环境**被反爬拦截**（HTTP 202 空响应）；本报告改用 **arXiv 一手页面**（已精读摘要与元数据）+ IEEE 期刊 DOI 元数据交叉确证。

**问题：紧耦合是端云协同的结构性瓶颈**

在移动/边缘环境中部署 LLM 受三重约束：**端侧资源有限、无线带宽稀缺、模型频繁演进**。

端云协同 + 投机解码的既有做法是"端侧跑轻量 draft、云端 target 验证"，能降低端到端延迟——但：

> 既有框架**根本上依赖 draft 与 target 之间的紧耦合**。因此**反复的模型同步引入过量通信开销**，增加了端到端延迟，最终**限制了 SD 在边缘环境中的可扩展性**。

**机制：两个设计**

| 设计 | 内容 | 解决的问题 |
|---|---|---|
| **共享骨干架构**（shared-backbone） | 一个**静态的**边缘侧 draft 模型，可兼容**一大族演进的**云端 target 模型 | 把"边缘部署"与"云端模型更新"解耦 → **免端侧重训、免反复下载** → 大幅降低通信与运维成本 |
| **信道感知自适应投机**（channel-aware adaptive speculation） | 依据**实时信道状态信息**与**设备能量预算**动态调整投机草稿长度 | 适应时变的无线条件与异构设备约束 |

**结果（论文自报）**：在推理效率上优于常规 SD 方案；具体加速比数字本报告未从一手页面取得（arXiv 摘要为定性陈述），故**不列入对比表**。

**与本章其他条目的关联**：FlexSpec 的"冻结 draft 兼容演进 target"与 [speculative-draft-training-2026.md](speculative-draft-training-2026.md) 中 TLT 的"target 演化导致 draft 失配"是**同一个问题的两种场景**（边缘 vs RL 训练），但解法相反：TLT 选择"持续更新 draft"，FlexSpec 选择"冻结 draft 并让它天然兼容一族 target"。

---

## 3. 端侧 MoE 自投机：SS-MoE（ACM Web 2026） **[摘要级]**

**基本信息**：*Self-Speculative Decoding for On-device MoE Acceleration*；ACM Web Conference (WWW) 2026；DOI `10.1145/3774904.3792218`。**核验说明**：ACM DL 页面在本环境被 Cloudflare 拦截（HTTP 403），本报告改用 **OpenAlex 元数据**（DOI/会议/年份与 ACM 一致）获取摘要全文。

**问题**

- 稀疏 MoE 是端侧基础模型的有力骨干，但其**路由专家权重超出内存受限 GPU 的容量**。
- 既有做法是 **CPU 专家卸载（expert offloading）**，面临两个痛点：**预取不准确** + **按需加载延迟**。

**机制：SS-MoE（self-speculative MoE），算法-系统协同设计**

论文的核心 insight 有两条：

1. **"路由专家的一个子集"本身就能当 draft 模型**——对**简单任务**，用被路由的专家子集仍能生成 token。即 draft 不需要额外模型，而是 target MoE 的一个子集。
2. **把内存本身当作专家缓存**，通过更新缓存来削减 IO 开销。

流程：先用较少的专家快速生成 draft token → 再交给完整 MoE 验证。此外引入**基于置信度的自适应策略**，选择性地接受或验证 token，从而**有选择地减少/增加验证步骤**。

**为什么这条设计对端侧特别重要**：它把"draft 模型"从"额外权重"变成了"已有权重的子集"，**端侧不增加任何权重的内存占用**——这是端侧场景与数据中心场景最本质的差别之一。

---

## 4. SMoLPU：MoE 投机解码专用硬件（ISSCC 2026） **[摘要级（⚠️ 受限核验）]**

**基本信息**：Sangwoo Ha, Jingu Lee, Youngjin Moon, Sunjoo Whang, Wooyoung Jo, Gwangtae Park, Sangjin Kim, Soyeon Um, Junha Ryu, Yurim Jo, Hoi-Jun Yoo（KAIST SSL + MIT，资深作者 Hoi-Jun Yoo）；*SMoLPU: 122.1 µJ/Token Sparse MoE-Based Speculative Decoding Language Processing Unit with Adaptive-Offload NPU-CIM Core*；**ISSCC 2026**，Digest of Technical Papers vol. 69, pp. 312–314；DOI `10.1109/ISSCC49663.2026.11409285`。

**核验说明与任务书链接异常**：任务书给出的是 <https://ieeexplore.ieee.org/document/11678131>（标题为 "SMoLPU: An Energy-Efficient Sparse Mixture-of-Experts-Based Speculative Decoding Language Processing Unit"）。本次核验发现：

- IEEE 在本环境返回 202 空响应，**两个 IEEE 页面均无法直接读取**；
- 通过 KAIST 官方实验室页面与 KAIST Pure 知识库确证，ISSCC 2026 版本的正确收录号为 **DOI `10.1109/ISSCC49663.2026.11409285`**，标题为带 `122.1µJ/Token ... Adaptive-Offload NPU-CIM Core` 的长标题；
- 任务书链接的 **11678131 很可能是同一工作的另一版本/另一条收录**（标题措辞不同），本报告**无法确证二者关系**，故按后者处理并在 §7 显式标注。

**三个设计特征（来自 KAIST Pure 的官方摘要引用）**

| # | 特征 | 论文自报指标 |
|---|---|---|
| 1 | **Token-adaptive expert refinement**：移除冗余专家激活并调度专家加载顺序 | prefill / decode 能效分别提升 **2.3× / 4.2×** |
| 2 | **Adaptive-offload NPU-CIM 核心 + 顶层调度单元**：在动态 INT–FP 比例下维持硬件利用率 | 延迟降低 **3.3×** |
| 3 | **可重构的 DRAM-based LUT-CIM**：降低加法树功耗/面积，并支持动态输入尺寸 | 相比此前 SOTA，**每参数能量降低 43.5%** |

**为什么单列一条**：这是本专题中**少见的"为投机解码 + MoE 定制硅"**的工作。它的指标口径（µJ/token、能效倍数、每参数能量）与算法论文（tokens/s、接受率）不可直接换算——把两者放在同一张表里排序是**方法论错误**。

---

## 5. Google TPU 上的扩散式投机：算法-硬件耦合的范例 **[精读原文]**

**基本信息**：Google Developers Blog，2026-05-04，*Supercharging LLM inference on Google TPUs: Achieving 3X speedups with diffusion-style speculative decoding*；作者 Weiren Yu（PM）、Yarong Mu（Senior Staff SWE）、Lihao Ran（SWE）、Zhaoxiang Feng（UCSD）、Yiming Zhao（UCSD）、Hao Zhang（UCSD 助理教授，paged attention 与 prefill/decode 分离服务的共同发明人）。

**核验页**：<https://developers.googleblog.com/supercharging-llm-inference-on-google-tpus-achieving-3x-speedups-with-diffusion-style-speculative-decoding/>

**背景：为什么自回归 draft 会成为天花板**

> 自回归投机解码要求 **K 次串行前向才能产出 K 个候选 token**。逐步依赖迫使系统等每个 token 预测完才能开始下一个，**在结构上限制了起草阶段的速度上限**。

突破方式是块扩散（block diffusion）：**单次前向 O(1) 生成整个候选块**。

**成果（工程博客自报）**

| 指标 | 数值 | 条件 |
|---|---|---|
| token/s 提升 | **平均 3.13×** | TPU v5p |
| 峰值提升 | **接近 6×** | 复杂数学任务 |
| 与 EAGLE-3 的端到端服务对比 | **DFlash 2.29× vs EAGLE-3 1.30×** | TPU v5p |

**工程实施的三道坎（这才是本条目的价值所在）**

1. **"双缓存"解决注意力不兼容**：TPU 高性能服务走 **paged attention + Pallas 内核**（固定页大小的内存切分）；而 DFlash 的**非因果块扩散**与标准 paged attention **根本性不兼容**。解法是双缓存：**target 模型继续用 paged KV cache**（保住 Pallas 内核的性能），**draft 模型走专用的静态 on-device JAX 数组**路径。
2. **把 proposer 与验证流水线映射到 TPU**：目标是让内存带宽与矩阵乘法单元（MXU）都跑满，最小化起草阶段开销、最大化 target 并行验证吞吐。
3. **从 PyTorch/GPU 迁移到 JAX/TPU 不是代码翻译**，需要按 TPU 的架构强项重新设计。

**结论性判断**：DFlash 的 3.13× **不能仅归因于算法**——同一算法在 GPU 上的报告值与在 TPU 上的工程收益来自不同的优化路径。**"算法路线的上限由硬件映射决定"** 是本条目要传达的核心。

---

## 6. 硬件/边缘路线总表（含口径警示）

| 工作 | 场景 | 关键机制 | 论文自报指标 | 口径 | 证据等级 |
|---|---|---|---|---|---|
| **FlexSpec** | 端云协同（移动/边缘） | 共享骨干（静态边缘 draft 兼容演进云端 target）+ 信道感知自适应草稿长度 | 定性优于常规 SD | 推理效率 | 精读原文 |
| **SS-MoE** | 端侧 MoE（内存受限 GPU） | 路由专家子集作 draft + 内存作专家缓存 + 置信度自适应接受 | 未在本报告取得量化值 | — | 摘要级 |
| **SMoLPU** | MoE 投机解码专用芯片 | token 自适应专家精炼 / adaptive-offload NPU-CIM / DRAM LUT-CIM | 2.3×/4.2× 能效、3.3× 延迟、43.5% 每参数能量 | **µJ/token、能效** | ⚠️受限核验 |
| **TPU + DFlash** | 云端加速器（TPU v5p） | 块扩散 draft + 双缓存 + 流水线重映射 | 3.13× 平均、近 6× 峰值、2.29× vs EAGLE-3 1.30× | **token/s、端到端服务** | 精读原文 |

> **⚠️ 口径警示**：上表四行的指标**不是同一量纲**。SMoLPU 报的是能效（µJ/token），TPU 条目报的是吞吐（token/s），FlexSpec/SS-MoE 报的是端到端效率。把它们排成"谁更快"的榜单是错的。跨口径比较必须回到统一的端到端 wall-clock 与能耗计量。

---

## 7. 尚未确证 / 待跟踪

| 项 | 状态 | 说明 |
|---|---|---|
| 任务书 SMoLPU 链接（`document/11678131`）与 DOI `11409285` 是否为同一工作 | **未确证** | IEEE 页面被拦截；两标题措辞不同，本报告按已知 DOI 处理并标注 |
| FlexSpec 的具体加速比数字 | **未验证** | arXiv 摘要为定性陈述；期刊版本正文未获取 |
| SS-MoE 的量化收益 | **未验证** | 本报告仅取得摘要，未见具体加速/内存节省数字 |
| SS-MoE 在「非简单任务」上的退化幅度 | **未验证** | 论文承认子集专家只对"easy tasks"够用，未在摘要中量化难任务的回退 |
| TPU 条目是否已并入 vLLM TPU 主线 | **未验证** | 博客称已集成进 vLLM TPU inference ecosystem，未核验代码位置 |
| SMoLPU 是否可用于非 MoE 模型 | **未验证** | 设计围绕 MoE 专家调度，通用性未知 |

---

## 8. 链接核验清单（本轮实测，2026-10-16）

| # | 来源 | 链接 | 核验结果 |
|---|---|---|---|
| 1 | FlexSpec, IEEE TMC | https://ieeexplore.ieee.org/document/11480773 | ❌ **HTTP 202 空响应（IEEE 反爬拦截）** |
| 2 | FlexSpec, arXiv:2601.00644 | https://arxiv.org/abs/2601.00644 | ✅ HTTP 200，标题/14 位作者/日期（2026-01-02）与期刊 DOI 元数据一致 |
| 3 | SS-MoE, ACM DL | https://dl.acm.org/doi/abs/10.1145/3774904.3792218 | ❌ **HTTP 403（Cloudflare 挑战页）** |
| 4 | SS-MoE，经 OpenAlex 元数据 | https://doi.org/10.1145/3774904.3792218 | ✅ 元数据一致（ACM Web Conference 2026），摘要已取得 |
| 5 | SMoLPU，任务书链接 | https://ieeexplore.ieee.org/document/11678131 | ❌ **HTTP 202 空响应**；且标题与已知 DOI 版本的措辞不同 → 存疑 |
| 6 | SMoLPU，KAIST Pure 知识库 | https://pure.kaist.ac.kr/en/publications/smolpu-1221%CE%BCjtoken-sparse-moe-based-speculative-decoding-language/ | ✅ HTTP 200，作者/ISSCC 2026/pp. 312–314/DOI `10.1109/ISSCC49663.2026.11409285`/摘要一致 |
| 7 | SMoLPU，KAIST SSL 实验室页 | https://ssl.kaist.ac.kr/bbs/board.php?bo_table=Conference&wr_id=488&sca=2026 | ✅ HTTP 200，作者名单与会议（ISSCC 2026）一致 |
| 8 | Google TPU 扩散式投机 | https://developers.googleblog.com/supercharging-llm-inference-on-google-tpus-achieving-3x-speedups-with-diffusion-style-speculative-decoding/ | ✅ HTTP 200，日期 2026-05-04、作者、3.13×/近 6×/2.29× vs 1.30× 数字一致 |

> **IEEE/ACM 拦截说明**：本环境对 `ieeexplore.ieee.org` 的请求返回 HTTP 202 且响应体为空（反爬），对 `dl.acm.org` 返回 Cloudflare 挑战页（HTTP 403）。这不是链接失效，而是**本环境无法完成直接核验**。凡涉及这两个来源的条目，本报告均通过**机构知识库（KAIST Pure/SSL）、OpenAlex 元数据或 arXiv 镜像**交叉确证，并逐条标注核验强度。

---

## 参考文献

| # | 论文 / 来源 | 年份 / 出处 | 链接 | 证据等级 |
|---|---|---|---|---|
| 1 | FlexSpec, *Frozen Drafts Meet Evolving Targets in Edge-Cloud Collaborative LLM Speculative Decoding* | arXiv 2601.00644（2026-01-02）；IEEE TMC | https://arxiv.org/abs/2601.00644 | 精读原文 |
| 2 | SS-MoE, *Self-Speculative Decoding for On-device MoE Acceleration* | ACM Web Conference 2026 | https://dl.acm.org/doi/abs/10.1145/3774904.3792218 | 摘要级 |
| 3 | SMoLPU, *122.1 µJ/Token Sparse MoE-Based Speculative Decoding Language Processing Unit with Adaptive-Offload NPU-CIM Core* | ISSCC 2026, pp. 312–314 | https://pure.kaist.ac.kr/en/publications/smolpu-1221%CE%BCjtoken-sparse-moe-based-speculative-decoding-language/ | ⚠️受限核验（二手交叉确证） |
| 4 | Google Developers Blog, *Achieving 3X speedups with diffusion-style speculative decoding* | 2026-05-04 | https://developers.googleblog.com/supercharging-llm-inference-on-google-tpus-achieving-3x-speedups-with-diffusion-style-speculative-decoding/ | 精读原文 |
| 5 | DFlash（TPU 条目的算法基础） | ICML 2026, arXiv 2602.06036 | https://arxiv.org/abs/2602.06036 | 精读原文 |
| 6 | CAST（成本感知建树，端侧/批处理约束的另一面） | ICLR 2026 | https://papernotes.org/ICLR2026/llm_efficiency/inference-cost-aware_dynamic_tree_construction_for_efficient_inference_in_large_/ | 二手 |

---

> **报告说明**：本报告结论按证据等级标注，并额外区分了「本环境无法直接核验」的情况。IEEE Xplore 与 ACM Digital Library 的反爬拦截已如实记录，相关条目改用机构知识库与元数据来源交叉确证。所有数字为论文/机构自报值，**不同指标口径（µJ/token vs token/s vs 端到端效率）不可直接比较**。
>
> *数据截至 2026-10-16。*
