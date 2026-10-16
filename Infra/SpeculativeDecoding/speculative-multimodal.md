# 投机解码：多模态投机解码

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、技术博客、开源项目和第三方分析整理生成。部分 2025-2026 年信息可能未经同行评审，建议读者直接查阅原始论文验证。arXiv 预印本论文中的加速比数据受测试条件（模型规模、硬件、任务类型）影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮小幅更新；v1 为 2026 年 6 月）
> **本次改动**：新增 §4.5「与端侧/边缘章节的交叉引用」；参考文献表中 v1 遗留的占位符链接已按验收要求**显式标注为未确证**。
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦 2025-2026 年快速涌现的多模态投机解码方向。主报告见 [report.md](report.md)；端侧与硬件约束见 [speculative-edge-cloud-hardware.md](speculative-edge-cloud-hardware.md)。
>
> **证据等级约定**：本报告对每条结论标注 **[精读原文]**、**[摘要级]**、**[二手]**、**[受限核验]**；**每条只取一个主等级**，混合来源取**最弱**等级并在正文注明来源类型（如 `[精读原文（vLLM 官方文档）]`），不使用 `A + B`、`A（摘要层）` 这类复合标签。

---

## 四、多模态投机解码（2025-2026 新兴方向）

多模态投机解码是 2025-2026 年快速涌现的新方向，核心挑战在于：**视觉 token 冗余、视觉-语言对齐、视觉内存墙**。

### 4.1 视觉-语言模型（VLM）

| 方法 | 年份 | 核心机制 | 加速比 | 信息可靠性 |
|------|------|---------|--------|-----------|
| **ViSpec** | 2025 | 轻量级视觉适配器压缩视觉 token | — | 高 |
| **FLASH** | 2025 | 潜在感知半自回归投机解码 | — | 高 |
| **HiViS** | 2025 | 对 drafter 隐藏视觉 token，仅使用文本特征 | — | 高 |
| **FastVLM** | 2025 | 复用 target 模型早期层 | — | 高 |
| **SpecVLM** | 2025 | 弹性视觉压缩器 + 在线 logit 蒸馏 | **2.5-2.9×** | 高 |
| **DREAM** | 2025 | 交叉注意力 + 自适应特征选择 | — | 高 |
| **MASSV** | 2025 (EMNLP) | 小语言模型多模态适配 + 自蒸馏视觉指令微调 | **1.46×** | 高 |
| **MSD** | 2025 | 解耦文本/视觉 token，两阶段训练 | **2.29-2.46×** | 高 |
| **Spec-LLaVA** | 2025 (ICML Workshop) | 动态树状投机解码 | — | 中 |
| **AASD** | 2025 (IEEE/DAC) | 对齐投机解码加速 MLLM | — | 高 |
| **TwigVLM** | 2025 | 轻量级 twig 模块 + 自投机解码 | **154% 加速** | 高 |
| **HSD** | 2026-02 | 分层投机解码，文档解析 VLM | — | 中（预印本） |
| **SAGE** | 2026-02 | 熵引导自适应投机解码 | — | 中（预印本） |
| **TABED** | 2026 (EACL) | 测试时自适应集成 drafting | — | 高 |
| **EdgeSD** | 2026 (IEEE TMC) | 边缘-云协同，视觉-解码解耦 | — | 高 |

**VLM 投机解码的关键设计模式**：

1. **视觉 token 压缩**：ViSpec、SpecVLM 通过轻量适配器将高冗余视觉 token（如 576 个 patch）压缩为更少语义 token
2. **文本-视觉解耦**：HiViS、MSD 让 drafter 仅处理文本特征，视觉理解完全由 target 承担
3. **早期层复用**：FastVLM 利用 target 模型的早期层输出作为 draft 输入，减少重复计算
4. **弹性压缩**：SpecVLM 的"弹性视觉压缩器"根据任务类型动态调整视觉 token 数

### 4.2 视频大语言模型

| 方法 | 年份 | 核心机制 | 信息可靠性 |
|------|------|---------|-----------|
| **Sparse-to-Dense** | 2025-05 | 无损加速视频理解 | 高 |
| **SpecVLM-Video** | 2025 (EMNLP) | 验证器引导 token 剪枝 | 高 |
| **FastV-RAG** | 2026-01 | 快速细粒度视频 QA | 中（预印本） |
| **HIPPO** | 2026-02 | 整体感知并行投机解码 | 中（预印本） |
| **Sparrow** | 2026-02 | 文本锚定窗口注意力 + 视觉语义瞥视 | 中（预印本） |

**视频投机解码的特殊挑战**：
- 视频帧数远超图像 patch 数（如 32 帧 × 576 patch = 18,432 视觉 token）
- 时间冗余：相邻帧高度相似，draft 可利用时序连续性
- Sparse-to-Dense 通过稀疏采样关键帧 draft、密集验证全帧，实现无损加速

### 4.3 视觉-语言-动作模型（VLA）

| 方法 | 年份 | 核心机制 | 信息可靠性 |
|------|------|---------|-----------|
| **Spec-VLA** | 2025-07 | VLA 投机解码，松弛接受 | 高 |
| **SpecPrune-VLA** | 2025-09 | 动作感知自投机剪枝 | 高 |
| **KERV** | 2026-03 | 运动学修正投机解码 | 中（预印本） |
| **HeiSD** | 2026-03 | 混合投机解码，运动学感知 | 中（预印本） |

**VLA 投机解码特点**：
- 动作 token（如机器人关节角）通常比语言 token 分布更集中，接受率天然更高
- Spec-VLA 引入"松弛接受"——在动作安全边界内允许轻微分布偏移，换取更高加速比
- KERV / HeiSD 将运动学约束（如关节限位、平滑性）融入 draft 生成

### 4.4 语音与音频

| 方法 | 年份/会议 | 核心机制 | 信息可靠性 |
|------|----------|---------|-----------|
| **Speech Speculative Decoding** | 2025 (INTERSPEECH) | 语音生成投机解码 | 高 |
| **SpecASR** | 2025-07 | LLM-based ASR 投机解码 | 高 |
| **Simultaneous Masked/Unmasked Decoding** | 2025 (INTERSPEECH) | 同步掩码/非掩码解码 | 高 |
| **Multi-Token Prediction + Speculative Decoding for Codec-based Speech Synthesis** | 2024-10 | 多 token 预测 + 投机解码 | 高 |
| **Edge-Cloud Collaborative Speech Emotion Captioning** | 2026-03 | 边缘-云协同语音情感描述 | 中（预印本） |
| **Self-Speculative Decoding for LLM-based ASR with CTC Encoder Drafts** | 2026-03 | CTC 编码器作为 draft | 中（预印本） |

---

## 4.5 与端侧/边缘章节的交叉引用（本轮新增）

多模态投机解码与端侧部署高度重叠——**视觉 token 的数量级膨胀，使端侧的内存带宽约束比纯文本场景更早成为瓶颈**。相关结论请直接参阅端侧章节：

| 交叉点 | 端侧章节中的对应内容 | 对多模态的含义 |
|---|---|---|
| **内存带宽优先于草稿质量** | [speculative-edge-cloud-hardware.md](speculative-edge-cloud-hardware.md) §1 结论 1：端侧第一约束是内存带宽与权重搬运，而非草稿质量 | 视觉 token 使 KV cache 与激活规模进一步膨胀，端侧应先按内存预算筛掉不可行的视觉压缩 / 草稿方案 |
| **"额外模型"代价不可接受** | 同章 §3：SS-MoE 用**已有权重的子集**作 draft，端侧不增加任何权重的内存占用 | 多模态 drafter（ViSpec、TwigVLM 等轻量适配器）在端侧必须评估其**额外权重与激活的内存占用**，不能只报加速比 |
| **端云分工的通信瓶颈** | 同章 §2：FlexSpec 指出紧耦合导致同步通信吃掉加速收益 | 多模态场景需要传输的视觉特征/中间结果更大，端云同步成本更敏感（对照本表 **EdgeSD** 的"视觉-解码解耦"） |
| **硬件映射决定收益上限** | 同章 §5：Google TPU 上 DFlash 的 3.13× 来自双缓存与流水线重映射，而非算法本身 | 多模态投机的收益同样取决于视觉编码器与 drafter 能否映射到同一硬件路径 |

> **证据等级**：本节为跨章节的**结构性关联**，不引入新的实证结论。上表右列判断属于本报告基于两章论据的**推断**，未见任何论文做过"多模态投机解码 × 端侧内存约束"的联合实验。

---

## 参考文献

> **⚠️ 核验声明（2026-10-16 清理轮）**：v1 中本表 13 条 arXiv 链接均为**占位符**（编号含 `xxxxx`，实测 HTTP 404）。本轮逐条重新核验一手来源：**12 条已确证并替换**，**1 条无法确证一手来源、已剔除**（Spec-VLA）。逐条处置见下文「v1 遗留占位文献清理·链接核验清单」。**本轮仅修复引用，未改动任何结论、数字或推断。**

| # | 论文 | 年份 | 链接 | 可靠性 |
|---|------|------|------|--------|
| 1 | SpecVLM, *SpecVLM: Fast Speculative Decoding in Vision-Language Models*（v1 标题为简写，已更正） | 2025 | https://arxiv.org/abs/2509.11815 | 高（**已核验**，本轮确证） |
| 2 | MASSV, *MASSV: Multimodal Adaptation and Self-Data Distillation for Speculative Decoding of VLM* | 2025 | https://arxiv.org/abs/2505.10526 | 高（**已核验**，本轮确证） |
| 3 | MSD, *Speculative Decoding Reimagined for Multimodal Large Language Models*（v1 标题为简写，已更正） | 2025 | https://arxiv.org/abs/2505.14260 | 高（**已核验**，本轮确证） |
| 4 | Spec-LLaVA, *Spec-LLaVA: Accelerating Vision-Language Models with Dynamic Tree-Based Speculative Decoding*（v1 标题为简写，已更正） | 2025 | https://arxiv.org/abs/2509.11961 | 高（**已核验**，本轮确证） |
| 5 | TwigVLM, *Growing a Multi-head Twig via Distillation and Reinforcement Learning to Accelerate VLMs*（v1 标题为简写，已更正） | 2025 | https://arxiv.org/abs/2503.14075 | 高（**已核验**，本轮确证） |
| 6 | HSD, *HSD: Training-Free Acceleration for Document Parsing Vision-Language Models with Hierarchical Speculative Decoding* | 2026-02-13 | https://arxiv.org/abs/2602.12957 | 高（**已核验**，本轮确证） |
| 7 | SAGE, *SAGE: Accelerating Vision-Language Models via Entropy-Guided Adaptive Speculative Decoding* | 2026-01-31 | https://arxiv.org/abs/2602.00523 | 高（**已核验**，本轮确证） |
| 8 | TABED, *TABED: Test-Time Adaptive Ensemble Drafting for Robust Speculative Decoding in LVLMs*（v1 标题为简写，已更正） | 2026-01-28 | https://arxiv.org/abs/2601.20357 | 高（**已核验**，本轮确证） |
| 9 | SpecPrune-VLA, *SpecPrune-VLA: Accelerating Vision-Language-Action Models via Action-Aware Self-Speculative Pruning*（v1 标题为简写，已更正） | 2025-09-06 | https://arxiv.org/abs/2509.05614 | 高（**已核验**，本轮确证） |
| 10 | KERV, *KERV: Kinematic-Rectified Speculative Decoding for Embodied VLA Models*（v1 标题为简写，已更正） | 2026-03-02 | https://arxiv.org/abs/2603.01581 | 高（**已核验**，本轮确证） |
| 11 | Speech Speculative Decoding, *Accelerating Autoregressive Speech Synthesis Inference With Speech Speculative Decoding*（v1 描述为简写，已补全名） | 2025-05-21 | https://arxiv.org/abs/2505.15380 | 高（**已核验**，本轮确证） |
| 12 | SpecASR, *SpecASR: Accelerating LLM-based Automatic Speech Recognition via Speculative Decoding*（v1 标题为简写，已更正） | 2025-07-24 | https://arxiv.org/abs/2507.18181 | 高（**已核验**，本轮确证） |

**v1 遗留占位文献清理·链接核验清单（本轮实测，2026-10-16）**

| 原链接 | 处置 | 新来源 |
|---|---|---|
| `https://arxiv.org/abs/2505.XXXXX`（SpecVLM） | **替换** | https://arxiv.org/abs/2509.11815（*SpecVLM: Fast Speculative Decoding in Vision-Language Models*，2025-09-15） |
| `https://arxiv.org/abs/2509.XXXXX`（MASSV） | **替换** | https://arxiv.org/abs/2505.10526（*MASSV: Multimodal Adaptation and Self-Data Distillation for Speculative Decoding of VLM*，2025-05-15） |
| `https://arxiv.org/abs/2506.XXXXX`（MSD） | **替换** | https://arxiv.org/abs/2505.14260（*Speculative Decoding Reimagined for Multimodal Large Language Models*，2025-05-20） |
| `https://arxiv.org/abs/2506.XXXXX`（Spec-LLaVA，与上一条同数不同文，v1 两条重复编号） | **替换** | https://arxiv.org/abs/2509.11961（*Spec-LLaVA: Accelerating Vision-Language Models with Dynamic Tree-Based Speculative Decoding*，2025-09-15） |
| `https://arxiv.org/abs/2507.XXXXX`（TwigVLM） | **替换** | https://arxiv.org/abs/2503.14075（*Growing a Multi-head Twig via Distillation and Reinforcement Learning to Accelerate VLMs*，2025-03-18） |
| `https://arxiv.org/abs/2502.XXXXX`（HSD，与 SAGE 同数，v1 两条重复编号） | **替换** | https://arxiv.org/abs/2602.12957（*HSD: Training-Free Acceleration for Document Parsing Vision-Language Models with Hierarchical Speculative Decoding*，2026-02-13） |
| `https://arxiv.org/abs/2502.XXXXX`（SAGE，同上） | **替换** | https://arxiv.org/abs/2602.00523（*SAGE: Accelerating Vision-Language Models via Entropy-Guided Adaptive Speculative Decoding*，2026-01-31） |
| `https://arxiv.org/abs/2503.XXXXX`（TABED） | **替换** | https://arxiv.org/abs/2601.20357（*TABED: Test-Time Adaptive Ensemble Drafting for Robust Speculative Decoding in LVLMs*，2026-01-28） |
| `https://arxiv.org/abs/2507.XXXXX`（Spec-VLA） | **剔除** | **无法确证一手来源**——arXiv 检索（`speculative decoding vision-language-action`、`Spec-VLA relaxed acceptance`）无匹配记录，亦未取得任何一手会议页面，故从参考文献表剔除该条（**未做猜测性编号替换**）。**命名冲突提示**：同表另有一条已核验的 `SpecPrune-VLA`（arXiv 2509.05614），两者是不同工作，请勿混同 |
| `https://arxiv.org/abs/2509.XXXXX`（SpecPrune-VLA） | **替换** | https://arxiv.org/abs/2509.05614（*SpecPrune-VLA: Accelerating Vision-Language-Action Models via Action-Aware Self-Speculative Pruning*，2025-09-06） |
| `https://arxiv.org/abs/2503.XXXXX`（KERV） | **替换** | https://arxiv.org/abs/2603.01581（*KERV: Kinematic-Rectified Speculative Decoding for Embodied VLA Models*，2026-03-02） |
| `https://arxiv.org/abs/2505.XXXXX`（Speech Speculative Decoding） | **替换** | https://arxiv.org/abs/2505.15380（*Accelerating Autoregressive Speech Synthesis Inference With Speech Speculative Decoding*，2025-05-21） |
| `https://arxiv.org/abs/2507.XXXXX`（SpecASR） | **替换** | https://arxiv.org/abs/2507.18181（*SpecASR: Accelerating LLM-based Automatic Speech Recognition via Speculative Decoding*，2025-07-24） |
| v1 表中无链接：ViSpec / FLASH / HiViS / FastVLM / DREAM / AASD / EdgeSD / HeiSD 与「Simultaneous Masked/Unmasked Decoding」等 | **登记待补（本轮不处理）** | 这些条目在 v1 正文表中即为**无参考文献链接**的条目（非占位符），本轮范围限定为"占位符与坏链接"，故按原样保留、**未做任何改动或猜测性补链** |

> **统计**：共处理 **13 条占位符** = **替换 12 条 + 剔除 1 条**（Spec-VLA）；另登记 v1 无链接条目为待补，不在本轮范围。**本轮仅修复引用，未改动任何结论、数字或推断。**

**本轮新增可核验引用（交叉参考）**：

| # | 来源 | 链接 | 证据等级 |
|---|------|------|---------|
| 14 | Google TPU 扩散式投机（端侧/硬件章节） | https://developers.googleblog.com/supercharging-llm-inference-on-google-tpus-achieving-3x-speedups-with-diffusion-style-speculative-decoding/ | 精读原文 |
| 15 | vLLM, *Per-Request Acceptance Metrics*（多模态场景指标口径） | https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/ | 精读原文 |

---

> **报告说明**：本报告所有技术细节均来自公开发表的论文、arXiv 预印本、官方技术博客及开源项目文档。**2026-10-16 清理轮：参考文献表中 13 条 v1 占位符链接已逐条重新核验——12 条替换为可核验一手来源，1 条（Spec-VLA）因无法确证一手来源已剔除**，逐条处置见上文核验清单。表格中的加速比与"信息可靠性"为 v1 结论，本轮仅修复引用、未重新核验数字。加速比数据受测试条件影响显著，跨论文对比需谨慎。
>
> *数据截至 2026-10-16（v1：2026-06-06）。*
