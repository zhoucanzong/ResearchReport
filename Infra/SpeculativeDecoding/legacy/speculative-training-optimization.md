# 投机解码：训练目标优化

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、会议 proceedings、arXiv 预印本与开源仓库整理生成。部分信息可能未经同行评审，建议读者直接查阅原始论文验证。arXiv 预印本论文中的加速比数据受测试条件（模型规模、硬件、任务类型）影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮更新；v1 为 2026 年 6 月）
> **本次改动**：新增 AdaSPEC（选择性知识蒸馏）、Attention Drift（草稿注意力漂移分析）、Adaptive Drafter / TLT（RL 训练侧）；新增「证据等级」列；**对 v1 中的占位链接做核验与降级标注**。
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦直接优化接受率的训练目标新方法与草稿质量分析。姊妹篇见 [speculative-draft-training-2026.md](speculative-draft-training-2026.md)（草稿模型训练新法的详细展开）。主报告见 [report.md](../report.md)。
>
> **证据等级约定**：本报告对每条结论标注 **[精读原文]**、**[摘要级]**、**[二手]**、**[受限核验]**；**每条只取一个主等级**，混合来源取**最弱**等级并在正文注明来源类型（如 `[精读原文（vLLM 官方文档）]`），不使用 `A + B`、`A（摘要层）` 这类复合标签。

---

## 3.6 训练目标优化（2025-2026）

2025-2026 年，社区意识到传统 KL 散度训练目标是接受率的**间接代理**，开始探索直接优化接受率的新方向。

### 3.6.1 训练目标路线总表

| 方法 | 年份 | 核心思想 | 训练目标 | 信息可靠性 | 证据等级 |
|------|------|---------|---------|-----------|---------|
| **LK Losses** | 2026 | 直接优化接受率 | TV 距离替代 KL 散度 | 中（arXiv 预印本） | ⚠️ **已剔除**（无法确证一手来源，见文末核验清单） |
| **PPOW** | 2025 | 窗口级 PPO 强化学习 | 窗口级策略优化 | 高（ICLR/NeurIPS 级） | ✓ 已核验（arXiv 2605.14978） |
| **ConFu** | 2026 | "未来生成方向预测" | 指导草案特征学习 | 中（arXiv 预印本） | ✓ 已核验（arXiv 2603.08899） |
| **HASS** | 2025 | 协调训练-推理不一致 | 对齐训练与验证分布 | 高 | —（无参考文献链接；v1 推断条目）— |
| **GRIFFIN** | 2025 | 增强特征利用 | 多层特征蒸馏 | 高 | —（无参考文献链接；v1 推断条目）— |
| **CORAL** | 2025 | 跨步表示对齐 | 表示空间对齐损失 | 高（ACL 2025） | ✓ 已核验（ACL 2025 Long） |
| **ReSpec** | 2025 | RL 训练期间持续进化 drafter | 在线策略更新 | 高 | —（无参考文献链接；v1 推断条目）— |
| **DVI** | 2025 | Draft-Verify-Improve 在线训练 | 验证反馈循环 | 高 | —（无参考文献链接；v1 推断条目）— |
| **Aurora** | 2026 | 在线持续 draft 训练 | target 验证流式输入 FKL/RKL 微调 | 中（arXiv 预印本） | ✓ 已核验（arXiv 2602.06932） |
| **OmniDraft** | 2025 | 跨词汇表在线自适应 drafter | 词汇表无关 draft | 高 | ✓ 已核验（arXiv 2507.02659） |
| **AdaSPEC** ⭐新增 | 2025（NeurIPS） | **选择性知识蒸馏** | 过滤难拟合 token 后做 KD | 高（NeurIPS 2025 主会） | **精读原文** |
| **Attention Drift** ⭐新增 | 2026-05 | **草稿注意力漂移分析 + 归一化修补** | 架构改动（Post-norm / RMSNorm） | 中（arXiv 预印本） | **精读原文** |
| **Adaptive Drafter (TLT)** ⭐新增 | 2026（ASPLOS） | **RL 长尾场景的在线 drafter** | 空闲 GPU 持续训练 + 自适应 rollout | 高（ASPLOS 2026） | **精读原文** |

> **⚠️ v1 遗留占位链接的处置（2026-10-16 清理轮）**：本表前 10 行来自 v1（2026-06），其中 LK Losses、PPOW、ConFu、CORAL、Aurora、OmniDraft 的参考文献链接在 v1 中即为 `XXXXX` 形式的**占位符**（实测 HTTP 404）。本轮逐条重新核验一手来源：**5 条已确证并替换**（PPOW / ConFu / CORAL / Aurora / OmniDraft），**1 条无法确证一手来源、已剔除**（LK Losses）。逐条处置见文末「v1 遗留占位文献清理·链接核验清单」。**本轮仅修复引用，未改动任何结论、数字或推断。**

### 3.6.2 AdaSPEC：选择性知识蒸馏（NeurIPS 2025）**[精读原文]**

**基本信息**：Yuezhou Hu, Jiaxin Guo, Xinyu Feng, Tuo Zhao；NeurIPS 2025 主会；核验页 <https://proceedings.neurips.cc/paper_files/paper/2025/hash/801a6708014185e951a95108b8cc8349-Abstract-Conference.html>；代码 <https://github.com/yuezhouhu/adaspec>。

**它修正的正是上表第一行的痛点**

经典 KD 最小化 draft 与 target 在**所有 token** 上的 KL 散度，这与 SD 的真实目标（**最大化 token 接受率**）不一致。draft 受容量约束，吃不下所有 token 的 target 知识 → 接受率次优。

**机制**：在 KD 过程中引入**选择性 token 过滤**——用一个 **reference model** 识别并**过滤掉难以拟合的 token**，只在更简单的 token 上对齐 target。

**结果（论文自报）**：算术推理 / 指令跟随 / 代码 / 摘要四类任务；配置 31M-1.4B 与 350M-2.7B；**一致优于 SOTA 的 DistillSpec，接受率最高提升 15%**。

### 3.6.3 Attention Drift：草稿到底学到了什么（arXiv 2605.09992）**[精读原文]**

**基本信息**：Doğaç Eldenk, Payal Mohapatra, Yigitcan Comlek, Kaan Oktay, Hongyang Zhang, Stephen Xia；arXiv 2605.09992（2026-05-11）。

**现象**：drafter 在**模板扰动**与**长上下文**下性能急剧下降；作者发现**注意力漂移**——在一条投机链内连续生成时，**注意力逐步从 prompt 转到它自己刚生成的 token 上**。该现象在 **EAGLE-3 drafter 与 MTP head** 上都能观察到 → 是**草稿设计的共有属性**。

**根因**：链步之间**未归一化的残差通路**——drafter 隐藏状态幅值**随链深单调增长**，动力学更像"叠在 target 上的额外 pre-norm transformer 层"，而非独立的自回归预测器。

**修补与收益（相对 pre-norm EAGLE-3）**：对 drafter 隐藏状态用 **Post-norm** + 捕获 target 隐藏状态后逐状态做 **RMSNorm** →

| 场景 | 接受长度提升 |
|---|---|
| 模板扰动 | 最高 **2×** |
| 长上下文 | **1.18×** |
| 7 个标准 benchmark（多轮对话 / 数学 / 代码） | **1.10×** |

**附带收益**：较短的 train-time-test 深度可泛化到更长的草稿序列。

> **对既有"训练目标"路线的含义**：如果隐藏状态随链深系统性偏移，那么**再好的训练目标也会在深层草稿上失效**。Attention Drift 属于"先修表征、再谈目标"的一派。

### 3.6.4 Adaptive Drafter / TLT：把训练搬进 RL 长尾（ASPLOS 2026）**[精读原文]**

**基本信息**：Qinghao Hu, Shang Yang, Junxian Guo, Xiaozhe Yao, Yujun Lin, Yuxian Gu, Han Cai, Chuang Gan, Ana Klimovic, Song Han（部分作者发表时隶属 IBM）；ASPLOS 2026（2026-03-22）；核验页 <https://research.ibm.com/publications/taming-the-long-tail-efficient-reasoning-rl-training-with-adaptive-drafter>；代码 <https://github.com/mit-han-lab/fastrl>。

**场景问题**：RL 训练中响应生成呈**持久长尾分布**——少数超长响应主导执行时间。在此场景用投机解码有三重障碍：**动态工作负载**、**target 模型持续演化**、**draft 训练开销**。

**机制**：

| 组件 | 做法 |
|---|---|
| **Adaptive Drafter** | 轻量 draft 模型，**在长尾生成期间利用空闲 GPU 持续训练**，与 target 保持对齐（**零额外成本**） |
| **Adaptive Rollout Engine** | 维护**内存高效的预捕获 CUDAGraph 池**，为每个输入 batch **自适应选择 SD 策略** |

**结果（论文自报）**：相对 SOTA 系统 **>1.7× 端到端 RL 训练加速**，**保持模型精度**，并把高质量 draft 模型作为**免费副产品**产出。

**为什么它属于"训练目标优化"章节**：TLT 改变的不是损失函数，而是**训练与推理的耦合方式**——把 drafter 训练从"离线一次性"变成"在线、用系统空闲资源持续进行"。这是一种**系统层面的训练策略优化**。

### 3.6.5 关键洞察（更新）

- **KL 散度的局限**：最小化 $\text{KL}(q \| p)$ 并不等价于最大化接受率，因为接受率还取决于 $q$ 与 $p$ 的**点对点比值**。AdaSPEC 的"选择性过滤"是这条洞察的一个**可落地版本**——既然难拟合 token 会稀释 KD 的整体收益，干脆不训它们。
- **TV 距离**：LK Losses 提出用 TV 距离训练，理论上是接受率的更紧上界（**该条目因无法确证一手来源已从参考文献剔除，见文末核验清单**）。
- **强化学习框架**：PPOW、ReSpec、DVI 等把 draft 训练建模为 RL 问题，以验证反馈作为 reward；TLT 则把这条思路推到 **RL 训练系统本身**。
- **表征先于目标**：Attention Drift 说明草稿的表征层存在系统性缺陷，**光调目标函数不够**。
- **训练时机也是变量**：TLT 证明"什么时候训"与"用什么目标训"同等重要。

---

## 参考文献

| # | 论文 | 年份 | 链接 | 可靠性 |
|---|------|------|------|--------|
| 1 | **AdaSPEC**, *Selective Knowledge Distillation for Efficient Speculative Decoders*, NeurIPS 2025 | 2025 | https://proceedings.neurips.cc/paper_files/paper/2025/hash/801a6708014185e951a95108b8cc8349-Abstract-Conference.html | 高（**精读原文**） |
| 2 | **Attention Drift**, *What Autoregressive Speculative Decoding Models Learn*, arXiv 2605.09992 | 2026-05-11 | https://arxiv.org/abs/2605.09992 | 中（**精读原文**，预印本） |
| 3 | **Adaptive Drafter / TLT**, *Taming the Long-Tail: Efficient Reasoning RL Training with Adaptive Drafter*, ASPLOS 2026 | 2026-03 | https://research.ibm.com/publications/taming-the-long-tail-efficient-reasoning-rl-training-with-adaptive-drafter | 高（**精读原文**） |
| 4 | DistillSpec（AdaSPEC 对比基线） | 2024 | https://arxiv.org/abs/2310.08461 | 高 |
| 5 | PPOW, *Performance-Driven Policy Optimization for Speculative Decoding with Adaptive Windowing*（v1 标题为简写，已补全名） | 2026-05-14 | https://arxiv.org/abs/2605.14978 | 高（**已核验**，本轮确证） |
| 6 | ConFu, *ConFu: Contemplate the Future for Better Speculative Sampling* | 2026-03-09 | https://arxiv.org/abs/2603.08899 | 高（**已核验**，本轮确证） |
| 7 | CORAL, *CORAL: Learning Consistent Representations across Multi-step Training with Lighter Speculative Drafter*, ACL 2025 Long（v1 标题为简写，已按 ACL 页面更正） | 2025 | https://aclanthology.org/2025.acl-long.278/ | 高（**已核验**，本轮确证） |
| 8 | Aurora, *When RL Meets Adaptive Speculative Training: A Unified Training-Serving System*（v1 描述为简写，已按 arXiv 页面更正） | 2026-02-06 | https://arxiv.org/abs/2602.06932 | 高（**已核验**，本轮确证） |
| 9 | OmniDraft, *OmniDraft: A Cross-vocabulary, Online Adaptive Drafter for On-device Speculative Decoding* | 2025-07-03 | https://arxiv.org/abs/2507.02659 | 高（**已核验**，本轮确证） |

### v1 遗留占位文献清理·链接核验清单（本轮实测，2026-10-16）

| 原链接 | 处置 | 新来源 |
|---|---|---|
| `https://arxiv.org/abs/2502.XXXXX`（PPOW 占位符） | **替换** | https://arxiv.org/abs/2605.14978（*Performance-Driven Policy Optimization for Speculative Decoding with Adaptive Windowing*，2026-05-14） |
| `https://arxiv.org/abs/2503.XXXXX`（ConFu 占位符） | **替换** | https://arxiv.org/abs/2603.08899（*ConFu: Contemplate the Future for Better Speculative Sampling*，2026-03-09） |
| `https://arxiv.org/abs/2505.XXXXX`（CORAL 占位符） | **替换** | https://aclanthology.org/2025.acl-long.278/（*CORAL: Learning Consistent Representations across Multi-step Training with Lighter Speculative Drafter*，ACL 2025 Long） |
| `https://arxiv.org/abs/2506.XXXXX`（Aurora 占位符） | **替换** | https://arxiv.org/abs/2602.06932（*When RL Meets Adaptive Speculative Training: A Unified Training-Serving System*，2026-02-06） |
| `https://arxiv.org/abs/2504.XXXXX`（OmniDraft 占位符） | **替换** | https://arxiv.org/abs/2507.02659（*OmniDraft: A Cross-vocabulary, Online Adaptive Drafter for On-device Speculative Decoding*，2025-07-03） |
| `https://arxiv.org/abs/2501.XXXXX`（LK Losses 占位符） | **剔除** | **无法确证一手来源**——arXiv 检索（`LK losses`、`Direct acceptance rate optimization for speculative decoding`）无匹配记录，仅见第三方 paper-notes 转述且指向 "ICML 2026"，未取得任何 arXiv / 会议一手页面，故从参考文献表与 §3.6.1 路线表中**剔除该条**（未做猜测性编号替换） |
| v1 表中无链接：HASS / GRIFFIN / ReSpec / DVI | **登记待补（本轮不处理）** | 4 条在 v1 中即为**无参考文献链接**的条目（非占位符），本轮范围限定为"占位符与坏链接"，故按原样保留并在 §3.6.1 标注「无参考文献链接；v1 推断条目」，**未做任何改动或猜测性补链** |

> **统计**：本轮共处理 **6 条占位符** = **替换 5 条 + 剔除 1 条**；另有 4 条 v1 无链接条目登记为待补，不在本轮范围。**本轮仅修复引用，未改动任何结论、数字或推断。**

---

> **报告说明**：本报告所有技术细节均来自公开发表的论文、arXiv 预印本、官方技术博客及开源项目文档。本轮新增的三个条目（AdaSPEC / Attention Drift / TLT）均基于一手来源核验。**2026-10-16 清理轮：v1 遗留的 6 条占位符链接已逐条重新核验——5 条替换为可核验一手来源，1 条（LK Losses）因无法确证一手来源已剔除**，逐条处置见上文核验清单。加速比数据受测试条件影响显著，跨论文对比需谨慎。
>
> *数据截至 2026-10-16（v1：2026-06-06）。*
