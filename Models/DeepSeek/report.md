---
display_name: DeepSeek
---

# DeepSeek 系列模型深度调研报告

> 调研范围：DeepSeek 六条模型研究线；历史主体保留至 2026 年 4 月 V4 Preview，近期分批补核到 2026-10-23，涉及 V4.1-Flash-1017 身份、训练/部署证据及分块 KV 压缩相位敏感性；见 §2.8、§11.10。各批只覆盖标明的范围，不代表六条研究线全量新型号扫描。
> 覆盖范围：DeepSeek 系列截至 **2026-10-23（Asia/Shanghai）**可获得的模型与技术材料。
> 历史主体基于两份子报告整合：[纯文本基座模型](deepseek-text-models.md) 与 [多模态与专业模型](deepseek-multimodal-and-specialized.md)，并提炼跨方向的整合性洞察。

---

## 1. 概述与发展时间线

### 1.1 DeepSeek 整体定位：高效开源路线

从公开论文看，DeepSeek 的模型研究反复处理给定计算预算下的能力、推理缓存、专家路由和长序列开销。下面的路线归纳依据所列论文，不代表组织内部的完整战略或未公开的工程实践：

1. **计算与能力的取舍**——DeepSeek-LLM 与 V3 等论文分别分析了模型/数据规模、训练计算和系统设计；这些是论文研究问题，不推断为贯穿所有版本的内部统一目标。
2. **开放范围因模型而异**——部分模型提供权重、论文或训练代码；这些材料有助于检查具体机制，但不等于所有数据、训练过程和复现条件都完整开放。
3. **架构与系统设计的变化**——V2 论文描述 MLA 与 DeepSeekMoE；后续论文分别讨论 FP8、MTP、辅助损失自由负载均衡和稀疏注意力。与其它厂商的总体路线差异不在此作排名判断。
4. **专业任务与通用模型间的公开技术联系**——推理、代码、数学、证明、视觉与生成系列中可见部分机制复用或任务扩展；“分叉—回流”是对这些公开联系的阅读归纳，不等于内部开发流程或每种专用能力都进入了通用主干。

为帮助阅读而作的有限对照。下表只概括若干公开系列/论文中可直接观察的设计，不代表厂商整体能力、训练路线或开放程度的全面比较：

| 维度 | DeepSeek 路线 | Qwen 路线（参考） |
| --- | --- | --- |
| 观察维度 | DeepSeek 公开例子 | Qwen 公开例子 |
| --- | --- | --- |
| 架构 | DeepSeek-V2/V3 报告 MLA 与 MoE 设计 | Qwen2/2.5/3 系列包含稠密与 MoE 等不同规格 |
| 训练证据 | V3 论文报告整套训练流程的计算预算及 MTP 等设计 | 各代报告披露范围与训练设置不同，需按具体模型对读 |
| 推理后训练 | R1-Zero 报告无 SFT 冷启动的 RL 设置 | Qwen 系列报告包含 SFT、偏好优化和 RL 等不同配置 |
| 多模态 | Janus 采用分开的理解与生成视觉表示 | Qwen-VL/Omni 报告不同的多模态接入设计 |
| 长上下文 | DSA 与 token-wise 压缩见 V3.2/V4 相关材料 | YaRN 等扩展设计见各模型论文 |

### 1.2 2024–2026 完整时间线

```text
─────────────────────────  2023  ─────────────────────────
2023-11  DeepSeek-LLM-7B/67B（首发，Dense；4K 上下文）
─────────────────────────  2024  ─────────────────────────
2024-01-05  DeepSeek-LLM (论文 arXiv:2401.02954) — 自研 scaling laws
2024-01-11  DeepSeekMoE (arXiv:2401.06066) — 细粒度专家分割 + 共享专家隔离
2024-01-25  DeepSeek-Coder（1.3B–33B Dense；2T tokens；仓库级 FIM）
2024-02-05  DeepSeekMath（7B；提出 GRPO，arXiv:2402.03300）
2024-03-08  DeepSeek-VL（1.3B/7B；混合视觉编码器）
2024-05-07  DeepSeek-V2（236B/21B MoE；首次引入 MLA + DeepSeekMoE；128K）
2024-05-17  V2-0517（IFEval 63.9 → 77.6）
2024-05-23  DeepSeek-Prover-V1（Lean 4 自动证明；miniF2F 50.0%）
2024-06-17  DeepSeek-Coder-V2（236B/21B MoE；338 种语言；128K）
2024-06-28  V2-0628（HumanEval 84.76）
2024-08-15  DeepSeek-Prover-V1.5（RLPAF + RMaxTS；miniF2F 63.5%）
2024-09-05  DeepSeek-V2.5（V2-Chat ⊕ Coder-V2 合并）
2024-10-17  Janus（1.3B；解耦视觉编码）
2024-11    JanusFlow；R1-Lite-Preview（线上对标 o1-preview）
2024-12-10  V2.5-1210（MATH-500 82.8）
2024-12-13  DeepSeek-VL2（Tiny/Small/Base；动态切片 + DeepSeekMoE + MLA）
2024-12-26  DeepSeek-V3（671B/37B；FP8 + MTP + ALF；14.8T；2.788M H800 GPU-hours）
─────────────────────────  2025  ─────────────────────────
2025-01-20  DeepSeek-R1-Zero / R1（arXiv:2501.12948）— 纯 RL 涌现推理
2025-01-22  R1-Distill × 6（Qwen 1.5/7/14/32B + Llama 8/70B）
2025-01-27  Janus-Pro（1B/7B）— 统一视觉理解与生成模型
2025-03-24  DeepSeek-V3-0324（MMLU-Pro 81.2，AIME 59.4）
2025-04-30  DeepSeek-Prover-V2（7B + 671B；子目标分解 + cold-start RL；miniF2F 88.9%）
2025-05-28  DeepSeek-R1-0528（AIME 2025 70 → 87.5）+ R1-0528-Qwen3-8B
2025-08-21  DeepSeek-V3.1（首个 Hybrid Think / Non-Think 单一 checkpoint）
2025-09-22  V3.1-Terminus（中英混杂修复）
2025-09-29  V3.2-Exp（首次引入 DeepSeek Sparse Attention DSA）
2025-10-20  DeepSeek-OCR（Contexts Optical Compression；96%+ 精度）
2025-11-27  DeepSeekMath-V2（自验证 + 自精炼 + meta-verifier；IMO 金牌级）
2025-12-01  DeepSeek-V3.2 / V3.2-Speciale（GRPO 升级 + 长 CoT；IMO/IOI 双金）
2025-12-31  mHC（研究）— Manifold-Constrained Hyper-Connections
─────────────────────────  2026  ─────────────────────────
2026-01-04  R1 论文 v2（Nature 645:633-638 正式发表）
2026-04-24  DeepSeek-V4 Preview（Pro/Flash；公告日、权重与论文存档分别记录）
2026-07-31  V4-Flash-0731（V4 Flash正式版本；不是4.1）
2026-08-13  V4-Pro-0813（Pro正式版本）
2026-08-21  V4-Flash-Vision-Exp（视觉实验版；本报告不把它作为公开研究权重）
2026-09-10  V4.1-Flash发布（原生图文输入）
2026-09-17  V4.1-Flash论文2609.19969v1（论文提交日，不是模型首次发布日）
2026-10-17  V4.1-Flash-1017（模型卡与权重更新；技术报告未更新）
```

---

## 2. 基座语言模型演进

从公开版本的时间顺序看，基座主线经历了 Dense 到 MoE、BF16 到 FP8，以及更长上下文等变化；这些不是一条严格单向的技术收敛路线，模型规模、训练精度与上下文策略也不能概括成每代都有同一种成本收益。

### 2.1 DeepSeek-LLM (2024-01)：Dense 起跑点

- 7B / 67B 双档 Dense Transformer（67B 上使用 GQA），BBPE 100K 词表（初代口径，不能继承为后续各代词表不变；V4.1 固定配置另见来源清单），4K 上下文，2T tokens 预训练。
- DeepSeek-LLM 论文研究了按 non-embedding FLOPs/token 分配模型与数据规模的 scaling-law 拟合，并在其训练配置与评测基准上报告了与 LLaMA-2 70B、GPT-3.5 的比较。它是该论文提出的训练分析，不是 DeepSeek 唯一的原创机制；跨模型结论应保留对应表格中的模型版本和指标。
- 后训练 = SFT + DPO，对齐路线相对保守。

### 2.2 DeepSeek-V2 (2024-05)：架构革命的起点

V2 技术报告把 MLA 与 DeepSeekMoE 引入该系列公开基座主线，并详细描述其训练与推理配置。后续模型沿用部分组件，但不能由时间先后推断 V2 单篇论文“确立”了全部后续路线：

- **236B 总 / 21B 激活**（V2-Lite 15.7B/2.4B），上下文一举跳到 **128K**（YaRN 扩展）。
- **首次引入 MLA**（攻 KV cache）+ **DeepSeekMoE FFN**（160 routed + 2 shared，激活 6 routed）+ **三层辅助损失负载均衡**（ExpBal/DevBal/CommBal）+ device-limited routing。
- 训练栈：BF16 + 16-way zero-bubble 流水线 + 8-way 专家并行 + ZeRO-1（不使用 tensor 并行），运行在 H800 集群，HAI-LLM 自研框架。
- 8.1T tokens 预训练。GRPO 先于 V2 出现在 DeepSeekMath 论文中，R1 等后续推理模型再将它用于相应的 RL 目标；不把它记作 V2 首次引入。
- 论文报告的训练与推理比较显示，在作者给定的 H800 集群、训练 token 数和推理设置下，V2 相较 DeepSeek 67B 使用更少 GPU-hours/获得更高最大吞吐。节省比例和吞吐比是论文特定对照，不应外推为跨模型、跨硬件的固定成本收益。
- 后续小迭代：V2-0517（IFEval 大幅提升）、V2-0628（HumanEval/MATH/BBH 全面增强）、**V2.5（V2-Chat 与 Coder-V2 合并为单一模型）**、V2.5-1210（MATH-500 进一步推到 82.8）。

### 2.3 DeepSeek-V3 (2024-12)：规模训练与系统设计

V3 在 V2 架构骨架上叠加了系统级创新；论文报告其完整训练流程使用 2.788M H800 GPU-hours。该总量涵盖多种训练和系统优化，不能归因于单项技术：

- **671B 总 / 37B 激活**（256 routed + 1 shared，激活 8 routed），61 层中前几层为 dense FFN。
- **Auxiliary-Loss-Free 负载均衡**：用不参与梯度的 per-expert bias 替代主要辅助损失，仅保留极小权重的 sequence-wise 保险损失；V3 论文的消融在其训练设置下报告了负载与主任务指标的改善，不能由此推出所有 MoE 训练都能同时改善两者。
- **Multi-Token Prediction (MTP)**：在主 next-token loss 之外预测未来 token；论文消融报告了训练指标变化，并在指定推理任务与硬件配置中测试其作为投机解码 draft module 的效果（第二 token 接受率约 85–90%、端到端 TPS 约 1.8×）。这些结果不能当作跨硬件、批量和任务的固定收益。
- **FP8 混合精度训练**：671B V3 的主要 Linear GEMM 使用 E4M3 输入、细粒度量化与高精度累加；论文的“相对BF16理论2倍计算速度”不等于训练step实测2倍，8位张量载荷减半也不等于整机显存减半。作者报告14.8T tokens预训练未出现不可恢复的loss spike、未回滚；数字与证据边界见[§3.3](#33-fp8-训练与低成本策略)。
- **DualPipe** 流水线 + 跨节点 all-to-all kernel：MoE 通信开销几乎被完全 overlap。
- 14.8T tokens 预训练，后训练 SFT + RL 并蒸馏部分 R1 知识。
- V3-0324（2025-03）继续推升：MMLU-Pro 75.9 → 81.2，AIME 39.6 → 59.4，LiveCodeBench 39.2 → 49.2。

### 2.4 DeepSeek-V3.1 (2025-08)：从双轨到混合推理

- 架构与 V3 完全一致，**改变的是后训练**：用同一个 checkpoint，通过 chat template 切换 Think / Non-Think 双模式（`deepseek-chat` = 非思考，`deepseek-reasoner` = 思考），CoT 长度比 R1-0528 压缩 20–50%。
- Agent 能力大幅增强：SWE-bench Verified 66.0、SWE-bench Multilingual 54.5、Terminal-bench 31.3。
- V3.1-Terminus（2025-09-22）小修中英混杂、异常字符，并成为 V3.2 的训练 base。

### 2.5 DeepSeek-V3.2 (2025-09 → 2025-12)：稀疏注意力时代

- **V3.2-Exp（2025-09-29）**：在 V3.1-Terminus 之上 continued training，并在该系列公开架构中首次引入 **DeepSeek Sparse Attention (DSA)** —— lightning indexer + token selector（top-k≈2048）。被选择 token 上的 attention 计算量随序列长度和 top-k 改变；该复杂度不等于端到端成本同幅下降，论文效率与质量结果须连同其长上下文设置理解。
- **V3.2（2025-12-01，arXiv:2512.02556）**：架构与 Exp 相同，并报告了 RL 框架、Agentic Task 合成 pipeline、GRPO 更新（按域调权 KL、修正 KL 估计、off-policy 序列掩码、MoE rollout 路由保持等）以及规则/生成式奖励的组合。与 GPT-5 的比较应限定为论文列出的任务、基准与推理预算，不作为一般能力等价结论。
- **V3.2-Speciale**：仅推理数据 RL、放宽长度惩罚的"扩展思考"变体，IMO 2025 与 IOI 2025 双金。

### 2.6 DeepSeek-V4 Preview (2026-04)：历史发布口径

- **双模型策略**：

  | 子模型 | 总参 / 激活 | 定位 |
  | --- | --- | --- |
  | **V4-Pro** | 1.6T / 49B | 旗舰；论文/发布材料在指定 Agentic Coding 基准中与列出的模型比较 |
  | **V4-Flash** | 284B / 13B | 较小激活规模；与 Pro 的能力差异须按具体基准和推理设置阅读 |

- **新型注意力**：*Token-wise 压缩 + DSA*——在 DSA 之上再叠加 token-wise 隐空间压缩；公开技术材料描述了 1M 上下文设置。产品接口的默认窗口与上限应以对应版本文档为准。
- 预览发布材料区分思考 / 非思考模式；后来的思考强度配置需按模型版本与接口分别读取，不把客户端可配置误写成所有 Agent 运行结果已验证。
- **公开范围**：V4-Pro 与 V4-Flash 权重及技术报告采用 MIT 许可发布；这不意味着训练数据、完整训练流程和全部复现条件均已公开。

### 2.7 历史架构对比表（至 V4 Preview）

| 维度 | V1 (2024-01) | V2 (2024-05) | V3 / V3.1 (2024-12 / 2025-08) | V3.2 (2025-12) | V4 (2026-04) |
| --- | --- | --- | --- | --- | --- |
| 模型类型 | Dense | MoE | MoE | MoE + 稀疏注意力 | MoE + 稀疏注意力 |
| 总参 / 激活 | 7B / 67B (Dense) | 236B / 21B（Lite 15.7B/2.4B） | 671B / 37B | 685B / ~37B | Pro 1.6T/49B；Flash 284B/13B |
| 注意力 | MHA / GQA | **MLA** | MLA | MLA + **DSA**（lightning indexer + top-k≈2048） | **Token-wise 压缩 + DSA** |
| FFN | SwiGLU Dense | DeepSeekMoE（160 routed + 2 shared，激活 6） | DeepSeekMoE（256 routed + 1 shared，激活 8） | 同 V3 | 升级版 DeepSeekMoE |
| 负载均衡 | — | ExpBal+DevBal+CommBal 三辅助损失 + device-limited | **Auxiliary-Loss-Free（per-expert bias）** + 极小 seq-wise loss | 沿用 V3 + DSA 友好路由 | 同 V3.x |
| 训练目标 | next-token | next-token | **+ Multi-Token Prediction (D=1)** | + MTP | + MTP（推断） |
| 训练精度 | BF16 | BF16 | **FP8 (E4M3) + 高精度累加 + tile/block 量化** | FP8 | FP8（推断） |
| 流水/通信 | 标准 ZeRO + PP | 16-way zero-bubble PP + 8-way EP + ZeRO-1 | **DualPipe** + 跨节点 all-to-all | 同 V3 | 同 V3.x |
| 上下文 | 4K | 128K（YaRN） | 128K | 128K | **1M 默认** |
| 预训练 tokens | 2T | 8.1T | 14.8T | 14.8T 之上继续训练 | >32T（固定预览模型卡口径） |
| 训练计算量（论文报告） | — | 每 1T tokens 172.8K H800·h | **2.788M H800·h** | 未单独披露 | 未单独披露 |
| 后训练 | SFT + DPO | SFT + GRPO | SFT + RL（含 R1 蒸馏） | RLVR + 生成式 reward + GRPO 升级 | RLVR + Agentic 任务合成 |
| 推理形态 | Base + Chat | Base + Chat | Base + Chat（V3.1 起 hybrid） | hybrid + Speciale 扩展思考 | Pro/Flash + 三档思考 |
| 开源协议 | MIT | MIT | MIT | MIT | **MIT** |

---

### 2.8 DeepSeek-V4.1-Flash：研究版本与技术证据

#### 2.8.1 V4.1-Flash 的论文与版本

| 模型/资料 | 时间 | 对研究的作用 |
|---|---|---|
| V4-Flash-0731、V4-Pro-0813 | 2026-07-31、2026-08-13 | V4正式版阶段的两个模型版本，和4月Preview分开 |
| V4.1-Flash | 2026-09-10 | 本报告用于技术分析的版本，支持图文输入 |
| 技术报告 `2609.19969v1` | 2026-09-17提交 | 晚于模型发布；用于解释方法，不把论文提交日当模型首发日 |
| V4.1-Flash-1017 | 2026-10-17更新 | 后续模型卡沿用同一技术报告，不是新论文 |

固定模型卡与权重索引的具体版本、来源覆盖范围见[来源清单](sources/MANIFEST.md)。静态配置相同不能证明权重或训练过程相同；本文没有权重运行结果。

#### 2.8.2 新架构的证据边界

[4.1 原版技术报告 **2609.19969v1**](https://arxiv.org/abs/2609.19969v1) 的提交日是 **2026-09-17**，晚于 9 月 10 日模型公告；1017 模型卡引用这份既有研究，不代表 10 月 17 日发布了一篇新的独立技术报告。固定 arXiv PDF 与固定 HF revision 内 PDF 是不同文件版本，不能默认视为同一版本。

论文摘要、§2/§4.2.1 和固定的原版模型卡支持以下变化：**552B 是 backbone 参数口径**，另有 196B Engram 条件记忆参数；40 层 Causal Encoder-Decoder 把 prefill 与 decode 的激活参数分别记为 **8B / 16B**。不能把 HF 权重页面的整体规模、backbone 参数和单 token 激活参数放进同一列，也不能由小激活量推出整套权重可装进一张显卡。

CSA2 的跨层 KV/索引复用与 FP4 KV 缓存把**全局 KV**记录为 890 bytes/token、约为旧 V4-Flash 的 1/4；SWA Bounded Replay 针对的是**持久缓存**，作者给出的比例约为 1/8。这两种缓存口径和固定长度下的比较不能改写为整机显存分别下降 4 倍/8 倍，或所有请求时延都同比下降。论文 §6 还指出 CSA2 选择错误、cache 恢复边界上的近似状态重建可能在极端条件下损害能力；这些失效条件没有独立验证。

原版与 1017 两个固定仓库的 `config.json` 字节一致（同为 40 层、词表 129,280），权重索引列出的分片数与映射规模相同；这只确认公开静态配置一致，**不能证明权重相同，也不能证明训练变更全部已披露**。权重分片没有下载或运行推理，因此不能据此确认权重相同或运行效果。

#### 2.8.3 评测、harness 与推理强度不能跨版本继承

1017 固定模型卡与更新日志列出 HLE 无工具 **42.6**（**44.0** 另指纯文本子集）、Terminal-Bench **4.0** 为 **42.3**、DeepSWE **v1.1** 为 **77.0**；后两项分别使用 **Claude Code** 与 **Mini-SWE-V2**。ZeroBench-main 的 **51.0** 是带工具 **Pass@5**。这些均为厂商报告值，未独立复跑。[1017 固定模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/blob/1bae0e1088993b9b82de08f59de5be5a34e42170/README.md)；[官方脚注](https://api-docs.deepseek.com/updates/)

原版 4.1 论文/卡片的代码评测通常用 DeepSeek Harness Minimal，DeepSWE 另用 mini-SWE；不能把旧表到 1017 新表的分差都归因于 checkpoint 更新。现有报告没有提供完整的逐项采样重复、模型预算和失败分布，因此这些数字不足以支持全场景排名，也不能转换成缺少硬件和任务条件的固定速度倍数。

论文报告中的 reasoning-effort 设置属于该论文评测条件；它不代表所有托管产品都采用相同默认推理强度。输入窗口与输出预算也不能替代长上下文准确率评估。

---

## 3. 核心技术创新深度解析

DeepSeek 的差异化几乎完全建立在六项核心技术上——**MLA、DeepSeekMoE、FP8 训练、MTP、ALF、DSA**——其中 MLA 与 DeepSeekMoE 是最具标识性的"DeepSeek 烙印"。

### 3.1 MLA（Multi-head Latent Attention）

**问题背景**：对一个 N 层、$n_h$ 头、每头 $d_h$ 维、序列长度 L 的 MHA，KV cache 大小为 $2 N n_h d_h L$ bytes。在 100B+ 模型 + 128K 上下文场景下，单 batch KV cache 通常以**百 GB**计，是 prefill/decoding 的主导开销。

**历史方案**：

| 方案 | 思路 | 缺点 |
| --- | --- | --- |
| MHA | 每头独立 K/V | KV 巨大 |
| MQA (Shazeer 2019) | 所有头共享一组 K/V | KV 极小但损质量明显 |
| GQA (Ainslie 2023) | 头分 g 组，每组共享 K/V | g 上做权衡，超长上下文仍偏大 |

**MLA 的核心三步**（V2 论文 §2.1）：

1. **Joint low-rank compression**：用降投影 $W^{DKV}$ 把隐状态 $\mathbf{h}_t$ 压成潜向量 $\mathbf{c}_t^{KV} = W^{DKV} \mathbf{h}_t$（V2 中 $d_c = 4d_h$），K 与 V 共用一份压缩潜向量。
2. **延迟上投影 + Absorb 技巧**：$\mathbf{k}_t^C = W^{UK} \mathbf{c}_t^{KV}$，$\mathbf{v}_t^C = W^{UV} \mathbf{c}_t^{KV}$；得益于矩阵结合律，$W^{UK}$ 在推理时可被吸收进 $W^Q$，从而**只需缓存 $\mathbf{c}_t^{KV}$**（每 token 仅一份、不分头）。
3. **解耦 RoPE 通道**：因 RoPE 与低秩压缩不可交换（合并矩阵会被 RoPE 阻断），单独维护一个共享小维度的 RoPE 路径 $\mathbf{k}_t^R$（维度 $d_h^R = d_h/2$），与 query 拼接为 $[q_t^C; q_t^R]$、key 拼接为 $[k_{t,i}^C; k_t^R]$，使位置信息独立维护、不破坏低秩 absorb 优化。

**KV cache 体积对比**（V2 论文 Table 1）：

| 注意力机制 | 每 token KV cache 元素数 | 能力 |
| --- | --- | --- |
| MHA | $2 n_h d_h l$ | Strong |
| GQA (g 组) | $2 n_g d_h l$ | Moderate |
| MQA | $2 d_h l$ | Weak |
| **MLA (DeepSeek-V2)** | $(d_c + d_h^R) l \approx \tfrac{9}{2} d_h l$ | **Stronger** |

MLA 的 KV cache 体积**约等于 GQA 仅 2.25 组**的水平，但效果**强于 MHA**——这是 V2 能把 128K 上下文做到推理可负担的关键。

**信息论视角**：

- GQA 是**结构性容量裁剪**：直接减少 K/V 头数，等价于让所有头共用同一 subspace，损失多视角能力。
- MLA 是**信息论级压缩**：压缩到 $d_c$ 维潜空间，但通过解耦 RoPE 与 absorb 技巧，**模型参数容量与计算能力并未削弱**——KV cache 减少来自"潜空间储存 + 推理时上投回原空间"，类似 LoRA 的 down-project / up-project 之于权重。这也是 V2 论文 Appendix D 中 MLA 在同 KV 体积下质量优于 MHA 的根因。

**演化轨迹**：

- **V2 → V3**：MLA 结构不变，但通过 FP8 + DualPipe 把训练效率推到极致；MLA 的 KV cache 进一步以 6-bit 量化部署。
- **V3 → V3.2**：MLA 之上叠加 DSA，注意力复杂度从 $O(L^2)$ 降到 $O(Lk)$；DSA 的 lightning indexer 直接复用 MLA 已压缩的 key latent，**避免重复缓存**——这是 MLA 与 DSA 协同设计的关键巧思。
- **V3.2 → V4**：在 DSA 之上再引入 token-wise 压缩，把 1M 默认上下文做到可负担。
- **跨方向复用**：DeepSeek-VL2 直接搬用 MLA 来支撑高分辨率长视觉序列；R1 系列继承 V3-Base 的 MLA 处理长 CoT。

### 3.2 DeepSeekMoE 设计哲学与迭代

**标准 MoE 的两个痛点**（GShard / Switch Transformer 时代）：

- **专家专业化不足**：经典做法把 FFN 切成几十到一百多个专家，每个专家仍然学到大量"通用知识"，专家间冗余高。
- **routed 专家承担公共知识** 导致负载更难均衡，且容易出现"路由塌缩"。

**两大设计原则**（DeepSeekMoE 论文 arXiv:2401.06066）：

1. **Fine-grained Expert Segmentation（细粒度专家分割）**：保持 FLOPs 不变，把每个常规专家切成 m 等份的小专家，同时把激活的专家数量也乘以 m。在不增加每 token 计算量的前提下，**专家组合空间从 $\binom{N}{K}$ 扩张到 $\binom{mN}{mK}$**，专业化粒度大幅提升。
2. **Shared Experts Isolation（共享专家隔离）**：拿出极少量（V2 中 2 个、V3 中 1 个）"共享专家"对所有 token 始终激活，承担"公共语言/通用知识"，让 routed experts 把容量留给真正需要专业化的方向。

**V2 阶段：多重辅助损失 + device-limited routing**

- **ExpBal**：基于路由频率 $f_i$ 与平均概率 $P_i$ 的乘积惩罚不均衡。
- **DevBal**：把专家划分为 D 组（每组一台设备），按设备维度计算同样形式的损失。
- **CommBal**：对接收侧通信量做均衡，配合 device-limited routing（每 token 只能落到 ≤ M 台设备）。
- 还引入 **Token-Dropping**：超过设备容量的 token 直接 drop。

**V3 阶段：Auxiliary-Loss-Free Load Balancing**

V2 的辅助损失虽然有效，但**会损害模型主任务性能**——损失函数中加入"平均化"压力会与"语义专精"目标冲突。V3 的解法：

- 用 **per-expert bias term** 替代主要辅助损失：$\tilde{s}_{i,t} = s_{i,t} + b_i$，bias 通过移动平均更新，**不参与梯度反传**——既能调度负载又不污染主任务损失。
- 仅保留极小权重的 **sequence-wise auxiliary loss** 作为防止极端不均衡的保险。
- 这是 V3 同时取得"负载更均衡 + 主任务效果更好"的关键之一。

**路由与并行：从 device-limited 到节点感知**

- V2：device-limited routing（≤ M 设备）。
- V3：node-limited routing + cross-node all-to-all 优化（IB + NVLink 双层 kernel），**MoE 通信开销几乎被 DualPipe 完全 overlap**。
- 推理：MLA 的小 KV + DeepSeekMoE 的稀疏激活，使 671B/37B 这种"低激活高总参"模型可以在远小于其总参的显存下高效部署。

### 3.3 FP8 训练与低成本策略

按固定版 [V3 技术报告 `2412.19437v2`](https://arxiv.org/abs/2412.19437v2)（2025-02-18）§3.3，Linear 的 Fprop/Dgrad/Wgrad 以 FP8 E4M3 为输入，输出为 BF16/FP32。激活1×128、权重128×128分组量化；H800上每128元素（4次WGMMA）提升部分和至FP32累加。embedding、输出头、gating、normalization、attention仍保留原精度；master weights/累积梯度用FP32，AdamW一、二阶矩用BF16，部分缓存激活另用E5M6。

- **存储**：相同元素数的FP8权重/激活载荷为BF16的一半（1对2 bytes/元素，理论格式计算，忽略缩放与副本）；论文未据此给出完整训练峰值显存降低50%的对照。
- **速度**：§3.3.1称相对原BF16方法的计算速度**理论上2倍**。这不是固定矩阵形状、计时方法下的内核实测，也不是完整step或端到端推理速度；量化、缩放、高精度累加、非GEMM与通信仍有开销。
- **质量与完整训练**：附录B.1以约16B/1.33T tokens和约230B/0.9T tokens的MoE做FP8对BF16实验，图10以EMA 0.9平滑loss，作者报告相对loss误差<0.25%（H800训练系统；附录未单列各组卡数/批量）。这不是671B全程BF16对照。V3完整系统使用2048张H800，作者报告未发生**不可恢复的**loss spike、未回滚；总GPU-hours是FP8、并行、通信等联合优化的结果，不能隔离成FP8单项收益。[摘要、§1/Table 1、§3.1、附录B](https://arxiv.org/pdf/2412.19437v2)

附录B.2还报告：将Dgrad相关张量全部改成128×128 block量化会使约16B MoE在约300B tokens时发散。公开仓库的固定revision只提供FP8/BF16推理demo，不能证明原始训练内核吞吐或完整训练显存；详见[文本子报告 §4.3.3](deepseek-text-models.md#433-fp8-混合精度训练)的源码调用链和存储推导。

**配套低成本策略**：

- **DualPipe**：自研流水线算法，让前向和反向同时双向流动，**几乎完全重叠 all-to-all 通信与计算**。
- **HAI-LLM 自研框架**：16-way zero-bubble 流水线 + 8-way 专家并行 + ZeRO-1，**未使用 tensor 并行**（因激活参数少 + 部分算子重计算），定制 CUDA kernel 与改造版 FlashAttention-2。
- **训练成本拆解**（V3 论文摘要原话）：

  | 阶段 | GPU 小时 (H800) |
  | --- | --- | --- |
  | 预训练 | 2.664M |
  | 上下文扩展 | 0.119M |
  | 后训练 | 5K |
  | **总计** | **2.788M** |

- 该GPU小时为论文报告的计算用量，不包含数据、消融、人力等项目，也不能单独归因给FP8。

### 3.4 Multi-Token Prediction (MTP)

**机制**（V3 论文 §2.2）：

- 训练目标在主 next-token loss 之外，**额外预测下一 D 个 token**（V3 中 D=1，即除当前位置外再多预测 1 个 token）。
- 实现上是在主模型之上挂载一个**轻量级 MTP 模块**（一层 transformer + projection），共享主干 embedding/output head，在训练阶段只增加少量 FLOPs。

**两点收益**：

1. **训练信号更密**：主模型本身在所有标准基准上得到稳定提升（论文消融数据均为正向）。
2. **推理时作为投机解码 draft module**：论文报告**第二 token 接受率约 85–90%**，端到端 TPS 大约 ×1.8。

V3 论文展示了 MTP 在大型 MoE 训练中的一种实现，并报告模型消融与投机解码设置下的结果。这是模型训练与推理机制的证据，不足以据此划分其他团队是否达到“工业级落地”。

### 3.5 Auxiliary-Loss-Free 负载均衡

详见 [3.2 节](#32-deepseekmoe-设计哲学与迭代) 的 V3 段落。其核心洞察是：

> 负载均衡是工程目标，不应通过损失函数让模型"妥协"。
> 正确的做法是把它放到优化器旁边——一个**不参与梯度的调度器**——用 bias 移动平均做闭环控制。

这一设计把负载目标与主任务梯度分开处理；跨模型是否借鉴或获得相同效果，需分别依据相关项目文档和实验判断，本报告不从方法相似性推断直接影响关系。

### 3.6 DeepSeek Sparse Attention (DSA)

V3.2-Exp 在该系列中引入 DSA，研究稀疏选择如何降低长序列注意力的计算量，同时尽量保留检索质量。

**两个组件**：

1. **Lightning Indexer**——为每个 query token 计算其对所有历史 token 的"相关度评分"。在 MLA 压缩空间中复用 keys（**避免重复存储**），并使用 ReLU 与 per-head 学习权重的简单形式：
   $$I_{t,s} = \sum_{j=1}^{H^I} w_{t,j}\, \mathrm{ReLU}(q_{t,j} \cdot k_s)$$
   其中 t 是当前 query 位置，s 是历史 token 位置（s<t），j 是 indexer head 索引；keys 直接从 MLA 已压缩并缓存的 latent 取出。

2. **Token Selector**——基于 indexer 分数选 **top-k**（DeepSeek 公开代码中 k=2048），构造稀疏 attention mask，只对被选中的历史 token 计算 attention。

**效果**：

- 对被选中的 token 执行注意力时，计算量随序列长度和 top-k 选择数变化为 $O(L \cdot k)$；索引器本身、KV 访问和其它模型计算仍需计入端到端开销。论文在其长上下文训练/推理设置中报告效率与质量结果，不能把这一项复杂度直接等同于总成本下降。
- 设计目标是在论文所测试的长上下文任务中减少注意力计算，并尽量保持检索质量；这一目标的实现程度以对应模型、负载和对照实验为准。

**V4 升级**：公开材料描述在 DSA 之上使用 **token-wise 压缩**，对 token 序列做隐空间压缩；具体实现细节未完全披露。模型权重、论文实验中的上下文长度和不同产品接口的窗口上限应分别引用，不能由模型能力说明推断所有服务默认值。

---

## 4. 推理模型演进

### 4.1 R1-Lite-Preview (2024-11)：探路

发布形式为 chat.deepseek.com 上线的预览版（未开源 weights，未发表正式论文），是 DeepSeek 第一次正面回应 OpenAI 在 2024 年 9 月发布的 o1-preview。在 AIME、MATH-500 上首次接近 o1-preview 水平，验证了"长思维链 + 强化学习"路径可行。

### 4.2 R1-Zero (2025-01)：纯 RL 涌现推理

**论文**：DeepSeek-AI, *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948（Nature 645:633-638, 2025）。

- **基座**：DeepSeek-V3-Base（671B / 37B 激活）。
- **训练范式**：论文跳过监督微调（SFT）冷启动，直接对 V3-Base 做强化学习。作者在其可验证数学/代码任务与规则奖励设置中观察到自我检查、回溯等输出行为；这说明该配置能够训练出相应轨迹，不证明无需人类推理数据就能在一般任务中稳定获得这些能力。
- **算法**：使用 **GRPO**（Group Relative Policy Optimization，源自 DeepSeekMath）：
  - 去掉 PPO 的 critic value model，改用**组内相对优势**——对同一 prompt 采样 G 条响应，用组内归一化得分作 advantage。
  - 去掉单独价值模型可减少该组件的训练状态与显存需求；总训练开销取决于采样数量、序列长度和实现，不直接等于 PPO 的固定比例。
- **奖励设计**：完全规则化，避免奖励模型 hacking——
  1. *Accuracy reward*：数学题答案匹配、代码题编译/单测通过；
  2. *Format reward*：必须以 `<think>...</think><answer>...</answer>` 包裹推理过程。
- **观察到的 "Aha Moment"**：模型在训练中段自发出现"等等、让我重新检查……"这类自我修正行为，思考长度随训练步数单调上升。
- **缺陷**：可读性差、中英混杂、有时输出冗长重复。

### 4.3 R1 (2025-01)：四阶段管线对标 o1-1217

为缓解 R1-Zero 的可读性问题，DeepSeek 设计了四阶段训练管线：

1. **冷启动 SFT**：用数千条高质量长 CoT 数据（部分由 R1-Zero 生成后人工修订）对 V3-Base 做轻量 SFT，规范输出格式。
2. **面向推理的 RL**：与 R1-Zero 同样的 GRPO + 规则奖励，并加入语言一致性奖励避免中英混杂。
3. **拒绝采样 + SFT**：用阶段 2 收敛模型生成 ~600K 推理数据 + 200K 通用数据（写作、知识问答、自我认知）一起 SFT，让模型在保留推理能力的同时回归通用对齐。
4. **全场景 RL**：最后再做一轮 RL，目标兼顾 helpfulness/harmlessness（用奖励模型）与 accuracy（用规则奖励），完成最终对齐。

- **论文报告结果**：AIME 2024 pass@1 ≈ 79.8%、MATH-500 97.3%、Codeforces 2029 ELO（96.3 percentile）。与 OpenAI o1-1217 的比较只适用于论文所列任务、版本与推理设置，不能概括为整体能力持平或超越。
- **协议**：MIT License；首个面向 LLM 推理的"完全开源 + 完全可商用"前沿模型。

### 4.4 R1-Distill：从 671B 装进小模型

DeepSeek 用 R1 生成 ~80 万条推理样本（≈60 万推理 + 20 万通用），对 6 个开源 dense 基座做单纯 SFT（**故意不做 RL**，旨在测试"知识注入是否足够"）：

| 蒸馏模型 | 基座 | AIME 24 pass@1 | MATH-500 | LiveCodeBench |
| --- | --- | --- | --- | --- |
| R1-Distill-Qwen-1.5B | Qwen2.5-Math-1.5B | 28.9 | 83.9 | 16.9 |
| R1-Distill-Qwen-7B | Qwen2.5-Math-7B | 55.5 | 92.8 | 37.6 |
| R1-Distill-Llama-8B | Llama-3.1-8B | 50.4 | 89.1 | 39.6 |
| R1-Distill-Qwen-14B | Qwen2.5-14B | 69.7 | 93.9 | 53.1 |
| R1-Distill-Qwen-32B | Qwen2.5-32B | **72.6** | 94.3 | 57.2 |
| R1-Distill-Llama-70B | Llama-3.3-70B-Instruct | 70.0 | 94.5 | **57.5** |

**关键结论**：

- **32B 蒸馏版在论文报告的若干数学/编码基准上高于 OpenAI o1-mini 对照值**；这是指定版本和评测设置下的结果，不构成消费级可部署模型的综合排名。
- 论文还比较了 R1 蒸馏的 Qwen-32B 与复用其 RL 管线训练的 Qwen-32B-Base。该实验支持在作者所用数据、训练预算和任务中，蒸馏路线取得更高分；不能推出小模型普遍从蒸馏获益多于 RL。

### 4.5 R1-0528 (2025-05)：思考预算翻倍

- 体量从 671B 微调到 685B（新增 token & 路由专家）。
- **思考预算翻倍**：AIME 题目平均思考 token 12K → 23K，AIME 2025 准确率 70% → 87.5%。
- 幻觉降低 45–50%（改写、摘要、阅读理解任务）。
- 新增 **JSON 输出**与**函数调用**支持；支持 system prompt；不再需要手动塞入 `<think>\n` 触发推理。
- 前端代码 / vibe-coding 显著增强。
- 同步释出 `DeepSeek-R1-0528-Qwen3-8B` 蒸馏版。

### 4.6 GRPO 训练范式深度解析

GRPO 最早由 DeepSeekMath 论文提出，R1 与 V3.2 又在各自训练目标中使用或调整该方法。它在开源 RL 实践中的采用范围不作为本报告结论；与 PPO 相比，其核心设计是：

| 维度 | PPO | GRPO |
| --- | --- | --- |
| Critic / Value Model | 需要单独训练或维护 | 不训练单独的 critic；节省量取决于实现、rollout 与序列长度 |
| Advantage 估计 | GAE（基于 value） | **组内相对优势**：对同 prompt 采样 G 条 rollout，按组内得分归一化 |
| 训练开销 | 受 critic 与 GAE 计算影响 | 少一条价值模型路径，但总开销仍取决于采样数量、长度和实现 |
| 是否兼容规则化奖励 | 兼容 | **天然兼容**（V3.2 进一步引入按域调权 KL） |

V3.2 阶段的 GRPO 升级版：保留 KL（按域调权，数学域近 0）、修正 KL 估计、off-policy 序列掩码、MoE rollout 路由保持、top-p/top-k 采样掩码保持、保留原 GRPO normalization。

### 4.7 "无 SFT 冷启动"路线的意义

R1-Zero 的纯 RL 路线在 LLM 史上有特殊地位：

- **测试无 SFT 冷启动的可行性**：在 R1-Zero 的基座、数学/代码任务和规则奖励条件下，直接 RL 产生了论文描述的推理轨迹；这不等同于证明 SFT 对 RLHF 或通用能力训练并非必要。
- **不使用冷启动推理轨迹**：这是 R1-Zero 该训练配置的特点；对其他任务是否能降低数据需求，需要单独评估可验证奖励的覆盖范围与失败模式。
- **奖励边界**：可验证的答案或单测让这些任务能使用规则奖励，但规则本身仍可能被利用；论文没有据此证明奖励 hacking 已被一般性解决。
- **后续模型形态**：R1、V3.1 与 V4 的公开材料分别呈现独立推理模型、同一 checkpoint 的 Think/Non-Think 模式，以及不同思考强度设置。它们提供模型形态变化的案例，不据此概括为整个开源社区的主流方向或内部路线动机。

一个独立的 2026 年预印本为“基座已有能力与 RL 后训练”的关系提供了可比较的实验视角：Wang 等人在 Olmo-3-7B 与 Qwen3-14B 上发现，固定回复开头 cue 可使若干数学基准成绩接近直接从基座进行的 RL 对照；例如 Qwen3-14B 的 MATH-500 pass@1 从 72% 升到 87%，与其 GRPO 对照相当。作者还在 Olmo 与 SmolLM3 的受控中训练数据改写中改变 cue 行为。该结果不是 DeepSeek 模型实验，也不验证 R1-Zero 的训练因果解释；多阶段后训练和模型间差异仍可能超出 cue 效应。详见[逐篇精读](papers/2610.06851-base-model-cues.md)及[来源记录](sources/MANIFEST.md#9-base-model-cues-preprint-2026-10-23)。

### 4.8 DeepSeek-R2：公开证据边界

本报告未发现可供精读的 DeepSeek-R2 官方技术报告或权重。发布时间、内部测试、训练资源分配和产品路线等说法没有公开一手材料支持，不用于解释研究路线；后续若出现官方原文再补充。

---

## 5. 视觉语言模型演进

### 5.1 DeepSeek-VL (2024-03)：混合视觉编码器

第一代 VL 模型（arXiv:2403.05525），覆盖 1.3B / 7B 两档 dense LLM 基座。三大设计支柱：

1. **数据 (Data)**：覆盖网页截图、PDF、OCR、图表、知识类内容，并基于真实用户场景构建任务分类法（taxonomy）和指令微调集，强化"实战能力"。
2. **混合视觉编码器 (Hybrid Vision Encoder)**：
   - 高分辨率分支：基于 SAM-B（图像分辨率高达 1024×1024）；
   - 低分辨率分支：基于 SigLIP-L（语义浓缩）；
   - 两路特征经独立 MLP 投影后在通道维拼接，再过一个 MLP 进入 LLM。这一设计兼顾文档级细节（小字、表格）和宏观语义。
3. **三阶段训练 + 视觉-语言均衡**：
   - Stage 1：仅训练 vision-language adaptor；
   - Stage 2：联合预训练，从一开始就把 LLM 一起训，并引入精心设计的视觉/语言 token 比例调度，避免视觉训练侵蚀 LLM 能力；
   - Stage 3：监督微调 + 偏好对齐。

### 5.2 DeepSeek-VL2 (2024-12)：动态切片 + DeepSeekMoE + MLA

VL2（arXiv:2412.10302）围绕"高分辨率 + MoE 高吞吐"做两处重大升级：

**视觉侧：动态切片 (Dynamic Tiling)**

- 用一个固定基础分辨率的视觉编码器（SigLIP-SO400M-384）处理任意宽高比、任意分辨率图像。
- 输入图被切片成若干 384×384 patch + 一张 thumbnail，token 序列拼接后送入 LLM。
- 相比 VL 的"双分支固定 1024×1024"，VL2 能处理更长的纵向截图、4K 大图、文档页面，对 OCR/Doc/Chart/Table 任务尤其友好。

**语言侧：DeepSeekMoE + MLA**

- 改用 DeepSeek V2/V3 同款 **DeepSeekMoE** 架构（共享专家 + 细粒度专家）。
- 引入 **MLA**：把 KV cache 压缩到低秩 latent 向量，长上下文推理显存降一个数量级。
- 这是 DeepSeek 主基座技术**首次回流到 VL 子方向**。

**三个尺寸（按激活参数）**：

| 模型 | Activated | Total | 备注 |
| --- | --- | --- | --- |
| DeepSeek-VL2-Tiny | 1.0B | 3.4B | 边缘部署 |
| DeepSeek-VL2-Small | 2.8B | 16.1B | 平衡型 |
| DeepSeek-VL2 | 4.5B | 27.5B | 旗舰 |

**能力**：VQA、OCR、文档/表格/图表理解、视觉定位（grounding）。在同等激活参数下击败大量 dense 与 MoE 开源模型。

### 5.3 DeepSeek-OCR (2025-10)：上下文光学压缩

- 一个 3B VLM（arXiv:2510.18234），主线**不是"OCR 工具"**而是 **Contexts Optical Compression** 的研究：把整页文档压成极少量视觉 token（远少于直接 OCR 后的文本 token），仍保持 96%+ 解码精度。
- 隐含结论：未来可以用"页面图像 → 视觉 token → LLM"的方式**显著压缩**长文本上下文，是 LLM 上下文扩展的潜在新方向，与 V3.2 DSA 形成互补——一个是"在 token 层面稀疏选择"，一个是"在感知层面光学压缩"。

---

## 6. 代码与数学模型演进

### 6.1 DeepSeek-Coder 系列

**DeepSeek-Coder (2024-01-25, arXiv:2401.14196)**：
- 1.3B / 5.7B / 6.7B / 33B 共四档 dense，全部从零训练在 2T token 上（87% 代码 + 13% 自然语言，含中英）。
- **仓库级数据组织**：使用拓扑排序在仓库范围内拼接多文件，让模型理解跨文件依赖；上下文 16K。
- **Fill-in-the-Middle (FIM)**：训练时按比例随机执行"前缀-后缀-中段"重排，使模型同时具备 left-to-right 生成与中段补全能力，是 IDE 内联补全的核心技术。
- **两阶段训练**：通用代码预训练 + 数学/项目级再训练；继之以 instruction tuning 得到 `DeepSeek-Coder-Instruct`。
- 论文报告 33B 版本在 HumanEval、MBPP 和 DS-1000 上高于所列 CodeLlama、Codex 与 GPT-3.5 对照值；这些结果受基准版本、提示和采样设置约束，不概括为“最强开源代码模型”。

**DeepSeek-Coder-V2 (2024-06, arXiv:2406.11931)**：
- 在 **DeepSeek-V2-Base**（MoE）上做"代码继续预训练"，得到 Lite（16B/2.4B 激活）与 V2（236B/21B 激活）两档。
- **支持语言数 86 → 338**；**上下文 16K → 128K**；继续预训练数据 6T token，FIM 策略保留并优化。
- 后训练阶段加入 *DPO* + *GRPO*（数学/代码 RL，与 DeepSeekMath 同源）。
- 论文报告 HumanEval 90.2、MBPP+ 76.2 等结果，并在其列出的基准和协议下与 GPT-4-Turbo、Claude-3-Opus、Gemini-1.5-Pro 对照；不将这些分数扩展成跨基准的整体代码能力判断。

**跨代联系**：V2.5 将 V2-Chat 与 Coder-V2 合并升级；后续 V3 系列论文也报告代码基准结果。这些公开模型与论文之间存在任务和组件上的联系，但不足以还原内部产品决策或证明“专业模型技术必然回流主线”。

### 6.2 DeepSeekMath 系列

**DeepSeekMath (2024-02-05, arXiv:2402.03300)**：
- 7B dense 模型，从 DeepSeek-Coder-Base 7B 出发继续预训练于 120B 数学 token（高质量爬取 Common Crawl + 自训练分类器去噪）。
- 论文报告 MATH 得分为 51.7%（7B），并与该文列出的 GPT-4、Gemini-Ultra 结果比较；这些数值来自不同模型版本与评测口径，不作为跨系统等价能力判断。
- **最大贡献：提出 GRPO**（详见 §4.6）——这篇论文事实上是**后来 R1 训练算法的"前传"**。

**DeepSeekMath-V2 (2025-11-27, arXiv:2511.22570)**：
- 基于 V3.2-Exp-Base 的数学专用模型。
- **目标转向自验证数学推理**：模型除给出答案外，还生成可由模型检查的证明；训练信号从答案匹配扩展到证明质量。该设计针对论文中的数学任务，不能据此声称奖励作弊已被根本消除。
- 两个新方向：
  1. *Process-level verification*：把奖励信号从最终答案搬到推理过程中的每个步骤；
  2. *Theorem-proving 与一般数学推理融合*：吸收 Prover 系列的形式化证明能力。
- **三 LLM 链路**：训练独立的 LLM verifier（LLM 2）对 generator（LLM 1）输出打分，再训练 meta-verifier（LLM 3）评估 verifier；rubric 评分为 1/0.5/0。
- **Self-Refinement**：训练好的 generator 学会按 rubric 对自己的输出迭代修正（最多 8 轮，仍未饱和）。
- 在 IMO 2025、CMO 2024 上取得**金牌级**得分；其能力被并入 V3.2-Speciale。

### 6.3 DeepSeek-Prover 系列：Lean 4 形式化定理证明

| 版本 | 时间 | arXiv | 关键贡献 |
| --- | --- | --- | --- |
| **Prover-V1** | 2024-05-23 | 2405.14333 | 首版：从高中/竞赛题自动 *autoformalize* 为 Lean 4 statement，再用模型生成证明，用 Lean 4 验证作为 ground truth；筛选出 8M 高质量合成证明对 7B 模型做 SFT，miniF2F-test 达 50.0% |
| **Prover-V1.5** | 2024-08-15 | 2408.08152 | 继续预训练 + RLPAF（用 Lean proof-assistant 反馈做 RL）+ **RMaxTS**（Monte-Carlo Tree Search 引入 intrinsic reward 鼓励多样路径）。miniF2F 63.5%，ProofNet 25.3% |
| **Prover-V2** | 2025-04-30 | 2504.21801 | 671B（基于 V3）+ **子目标分解**：先用大模型把非形式化证明拆成 subgoal，再让 7B prover 逐个完成、最后回拼。引入 *cold-start RL*：从一批 high-quality 证明开始，用 GRPO 微调；miniF2F **88.9%**，攻克 PutnamBench 相当一部分题；同时发布 7B 与 671B 双尺寸 |

形式化证明系列与 DeepSeekMath-V2 的"自验证"思想高度一致，可视为 DeepSeek 在"reasoning 可验证化"路径上的两个互补支柱。

---

## 7. 多模态生成（Janus）

### 7.1 解耦视觉编码的设计理念

之前的"Chameleon 路线"用**单一**视觉 tokenizer 同时承担"理解"（需高语义抽象）与"生成"（需细粒度像素级 token），两者目标冲突，导致理解性能下滑。

**Janus 的解法**（arXiv:2410.13848，CVPR 2025）：

| 任务 | 视觉编码器 | 输出空间 |
| --- | --- | --- |
| 多模态理解 | SigLIP-L（连续语义特征） | 投影到 LLM token 空间 |
| 图像生成 | VQ tokenizer（离散像素 token） | 自回归生成离散 image token |

- 两路**分别**编码，但**共享同一个 Transformer 主干**做下游建模。架构因此既统一又解耦。
- 训练分三阶段：adaptor 训练 → 统一预训练 → 指令微调。
- 论文在 GenEval、DPG-Bench 等图像生成基准与 MMBench 等理解基准中报告了相对 Chameleon、Show-o 的结果；需按各自版本、基准和评价协议分别理解，不由此推断架构普遍占优。
- 1.3B 参数（DeepSeek-LLM-1.3B 基座），首次给"统一理解 + 生成"模型一个清晰的架构指引。

### 7.2 JanusFlow (2024-11)：流匹配生成

把生成路径换成 **Rectified Flow**（连续流匹配），抛弃 VQ tokenizer，进一步提升生成质量与采样效率，仍延续解耦视觉编码思路。

### 7.3 Janus-Pro (2025-01)：统一视觉理解与生成

- 1B 与 7B 双尺寸，相对 Janus 三处升级：
  1. **优化训练策略**：调整三阶段时长、视觉 token 比例；
  2. **扩展数据**：理解侧多模态 SFT 数据扩到 ~9000 万样本；生成侧加入 7200 万合成审美数据；
  3. **模型放大**至 7B。
- 论文在 GenEval、DPG-Bench 上报告了相对 SDXL、DALL·E 3 的结果；该比较受模型版本与基准协议限制，不作为跨任务的整体排序。发布后的社区关注度不属于方法证据。
- 与 R1 在同一周发布，构成 DeepSeek **2025 年初的"双爆点"**。

---

## 8. 跨代技术演进总结

### 8.1 核心设计哲学

**一、效率优先（Efficiency-First）**

DeepSeek 的多代研究反复探索如何在给定训练与推理预算下提高能力；具体收益取决于模型、硬件和任务设置，不能把单项机制的理论节省直接外推到完整系统。

- 架构层：MLA 攻 KV cache、DeepSeekMoE 攻 FFN 计算、DSA 攻长上下文 attention、Token-wise 压缩攻 1M 上下文。
- 训练层：FP8（攻显存与 GEMM 算力）、DualPipe（攻流水线气泡）、ALF（攻"为均衡牺牲质量"）、MTP（攻训练信号密度）。
- 后训练层：GRPO（攻 critic 显存）、规则奖励（攻奖励 hacking）、自验证（攻"对答案胡编"）。
- 这种全栈效率路线把架构、训练配方和推理系统一起优化；论文报告的总计算量不应归因给其中某一项。

**二、开源开放（Open & Reproducible）**

- 权重 + 技术报告 + 训练框架 + RL 算法 + 后训练 pipeline 全部公开。
- 关键算法（GRPO、MLA、DeepSeekMoE、ALF、MTP、DSA）均有 arXiv 论文 + 完整数学推导 + 消融实验。
- 全部模型 MIT/宽松商用许可。
- 这种开放程度直接孕育了下游生态：R1-Distill 让 6 个开源 dense 基座（Qwen2.5/Llama-3.x）一夜之间获得 o1-mini 级推理能力，并被 OpenRLHF / TRL / verl 等 RL 框架收编。

**三、分叉—回流（Branch & Merge）**

DeepSeek 的演化模式具有清晰的"分叉—回流"特征：

```text
                 ┌─────────────── DeepSeek-V3-Base (671B MoE) ───────────────┐
                 │                                                            │
                 │         post-train ↓ (RLHF+SFT)        post-train ↓ (RL)   │
                 │                                                            │
        DeepSeek-V3-Chat                                  DeepSeek-R1-Zero / R1
              │                                                  │
   incorporated R1 RL ↓                              distill (SFT) ↓
              │                                                  │
   V3-0324 → V3.1 → V3.1-Terminus → V3.2-Exp → V3.2 → V4   R1-Distill × 6
                                          ⊕                      ↓
                                  DeepSeekMath-V2           V4-Flash Distill
                                          ⊕                      (社区)
                                 (V3.2-Speciale 融合)

   R2 (延迟/未确认) ← 推理能力收编进 V4 Think Max 模式
```

- 公开材料显示 Coder-V2 与 V2.5、R1 与 V3.1、DeepSeekMath-V2 与 V3.2-Speciale 之间存在版本或训练上的联系；这些联系有助于阅读不同目标如何进入后续模型，但不能单凭发布顺序推断完整组织路径或因果关系。
- Prover-V2 报告了 miniF2F 结果；其对其它基准和通用推理能力的意义仍受形式化语言、问题集合和验证流程约束。

### 8.2 关键架构决策演变线索

下表保留至4月V4 Preview的历史脉络。9月4.1改为CED + CSA2、引入Engram，并按prefill/decode分别记激活规模；它不是把末格的旧Flash配置原样扩展，具体新增证据见§2.8。

| 决策维度 | 演化轨迹 | 触发动机 |
| --- | --- | --- |
| 注意力 | MHA/GQA → **MLA** → MLA + **DSA** → **Token-wise + DSA** | KV cache 瓶颈 → 长上下文 attention 复杂度 → 1M 上下文 |
| FFN | Dense SwiGLU → **DeepSeekMoE**（细粒度 + 共享专家） | "低激活高总参"性价比；专家专业化粒度 |
| 负载均衡 | 三层辅助损失 → **Auxiliary-Loss-Free** | 辅助损失伤害主任务质量 |
| 训练精度 | **FP8 E4M3 GEMM输入** + BF16/FP32混合精度 | FP8载荷字节数为BF16的一半；GEMM理论2倍速度不等于端到端实测（见§3.3） |
| 训练目标 | next-token → **+ MTP** | 训练信号密度 + 推理 speculative decoding |
| 流水线 | 标准 PP → **DualPipe** | 跨节点 MoE all-to-all 通信开销 |
| 上下文 | 4K → 128K (YaRN) → **1M** (DSA + Token-wise) | 长文档、Agent、代码仓库 |
| 后训练 | SFT + DPO → **SFT + GRPO** → **RLVR + 规则奖励 + 自验证** | 奖励 hacking 防御；推理可验证化 |
| 推理形态 | Base + Chat 双模 → **R1 推理分叉** → **混合推理（Think/Non-Think）** → **三档思考强度** | 把推理收编进通用基座 |

### 8.3 跨系列比较的边界

本报告只在引出具体机制时比较论文报告的模型、任务和训练设置。不能把若干代公开材料拼成 Qwen、LLaMA 或 DeepSeek 各自固定不变的总体路线，也不从开源材料的多少推出整体开放程度或能力强弱。需要比较时，应固定论文版本、模型尺寸、数据、基准、推理预算和硬件；简介中的代表案例不替代这类受控对照。

从公开论文可以概括出一条可追踪的研究路线：注意力与 MoE 架构、训练系统、推理后训练和专业模型之间出现了多次技术复用。这里的“分叉—回流”是对公开工作关系的阅读归纳；它不等于完整的组织决策史，也不能据此概括其他团队的整体工程文化。跨模型比较应回到相同任务和评测条件，而不是将厂商路线压缩成单一标签。

---

## 9. 关键机制及其证据边界

1. **MLA（Multi-head Latent Attention）**——将多个注意力头的键和值映射到低维潜在表示，以降低 KV cache 的存储开销。V2/V3 论文在各自模型、任务和缓存设置下报告了质量与效率结果；这些结果说明该设计在 DeepSeek 的训练和推理栈中可用，不足以证明它在所有同缓存预算下普遍优于 MHA、GQA 或 MQA。V4 的稀疏索引器复用 MLA latent，是论文所述的组件关系。

2. **DeepSeekMoE（细粒度专家分割 + 共享专家 + 辅助损失自由负载均衡）**——V2 论文通过细粒度专家和共享专家组织路由容量，并以辅助损失自由的偏置更新调节负载。组合空间的扩大是论文给出的设计动机；是否改善质量、负载与训练稳定性，仍要看具体对照和训练条件，不能把不同模型的 MoE 组件视为同一方法。

3. **GRPO**——DeepSeekMath 提出的组相对策略优化方法，不训练单独的价值模型，而以同组采样的相对奖励构造优势估计。R1-Zero 将其用于可验证推理任务并报告了无需冷启动 SFT 的实验结果；这说明该训练路线在论文设定下可行，不意味着所有模型或任务都能由纯 RL 获得同样行为。

4. **R1-Zero 的纯 RL 路线**——论文展示了在规则可验证的数学与代码任务上，从基座模型直接进行强化学习后，模型生成轨迹中出现反思、验证和回溯等行为。应将其理解为该任务、奖励和训练配置下的观察；论文没有证明这些行为在一般任务中都能稳定涌现。

5. **FP8 混合精度训练（V3）**——671B训练结合E4M3 GEMM输入、细粒度量化和FP32累加，并保留敏感算子与状态的高精度。作者报告未发生不可恢复的loss spike、未回滚；小规模BF16对照与完整训练结果的适用范围见[§3.3](#33-fp8-训练与低成本策略)，公开推理demo不等于公开训练实现。

6. **Multi-Token Prediction (MTP)**——V3 论文把多 token 预测作为辅助训练目标，并在特定推理配置中把预测头用于投机解码。论文报告的接受率和端到端速度提升受模型、硬件、批量与任务影响，不能概括为固定部署收益。

7. **DSA (DeepSeek Sparse Attention)**——V4 论文的索引器先选取相关 token，再对选中键值执行注意力；论文据此分析注意力计算随序列长度和选择数量变化的复杂度，并报告其长上下文设置。该分析不涵盖端到端推理的全部开销，也不能单独解释模型长上下文能力。

8. **Janus 解耦视觉编码**——Janus 将视觉理解和图像生成的输入表示分开，再由共享 Transformer 主干处理；这是论文的一种统一理解与生成设计。与其它系统的基准比较需保留各自模型版本和评测协议，不能从单一榜单结果推断架构普遍占优。

9. **DualPipe 流水线 + 跨节点 all-to-all kernel**——让 H800 上的 MoE 通信与计算重叠；V3总GPU-hours还包含FP8、数据处理、上下文扩展等环节，不能归因于DualPipe单项。

10. **自验证 / 形式化奖励（DeepSeekMath-V2 + Prover-V2）**——相关论文研究生成器、证明验证器与元验证器如何共同构成训练或筛选信号。它们提供了可验证推理的一组方法案例，不是覆盖任意数学任务的完整方案；结论要结合证明语言、验证器可靠性和题目分布理解。

11. **R1-Distill 的蒸馏与 RL 对照**——R1 报告在其选定的小模型、数据和训练预算下比较了蒸馏与强化学习路线。结果可帮助理解轨迹监督和在线奖励优化的取舍，不构成对所有小模型与任务的普遍效率结论。

12. **DeepSeek-OCR 的视觉上下文压缩**——论文把页面图像编码为视觉 token，并在给定文档集与压缩设置下报告文本恢复结果。它提出一种以视觉表示替代部分文本 token 的研究假设；与 DSA 的机制和评测问题不同，二者能否组合仍需直接实验。

13. **混合推理架构（V3.1 起）**——同一 checkpoint 通过 chat template 切换 Think/Non-Think，CoT 长度比 R1-0528 压缩 20–50%；V4 进一步演化为三档思考强度（Non-think / Think High / Think Max），是把推理能力收编进通用基座的关键一步。

---

## 10. 生态与平台集成进展（2025–2026）

DeepSeek 的开源策略不仅体现在权重与技术报告上，还体现在与全球主流云平台和推理基础设施的深度集成。

### 10.1 平台集成信息的时间边界

官方材料没有提供各平台接入 V4 的公告，因此不能确认早期上线日期或将其列成统一支持表。上游权重公开不能证明第三方平台已完成适配。

各第三方平台的支持情况仍需其原始说明；本报告不据上游公告推定其部署状态。

### 10.2 开源社区与下游生态

- **框架适配**：vLLM、SGLang、TensorRT-LLM、llama.cpp 均已原生支持 DeepSeek-V3/V4 的 MLA + DeepSeekMoE 架构。vLLM 在 2025-12 版本中加入了对 DSA 稀疏注意力的初步支持。
- **量化与部署**：公开 V4.1 仓库的配置与权重索引显示，激活参数不等于要存储的全部权重；现有证据不支持“V4-Flash 在单卡 H100 80GB 上以 FP8 运行1M”的部署说法，不能从较小激活量推出该结论。
- **Agent 集成**：1017 公告建议使用 DeepSeek Harness 0.2.1-rc.1 或更新版本，并点名 CodeBuddy / WorkBuddy 适配。这是官方建议，不代表所有主流框架都将其设为默认后端，也不等同于这些平台上的独立运行结果。
- **蒸馏生态**：R1-Distill 模式持续扩展，社区基于 V4-Flash 蒸馏出多个 7B–32B 级别的小模型，在数学与代码任务上保持接近原版的性能。

### 10.3 企业采用与行业落地

- **编程工具适配**：V4.1/1017 的官方适配说明见 §2.8。工具可以配置某个 API 后端，但这不能证明每个模型版本都经过独立工程任务评测；现有材料也不足以支持 V4 在 2025 下半年已接入这些工具。

本报告不汇总缺少一手出处的行业采用案例；这些案例也不能替代论文对方法机制和实验条件的证据。

---

## 11. 参考文献

### 11.1 通用基座主线（V Series）

1. DeepSeek-AI. *DeepSeek LLM: Scaling Open-Source Language Models with Longtermism*. arXiv:2401.02954, 2024. https://arxiv.org/abs/2401.02954
2. Dai, D. *et al.* *DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models*. arXiv:2401.06066, 2024. https://arxiv.org/abs/2401.06066
3. DeepSeek-AI. *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*. arXiv:2405.04434, 2024. https://arxiv.org/abs/2405.04434
4. DeepSeek-AI. *DeepSeek-V3 Technical Report*. arXiv:2412.19437, 2024–2025. https://arxiv.org/abs/2412.19437
5. DeepSeek-AI. *DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models*. arXiv:2512.02556, 2025. https://arxiv.org/abs/2512.02556
6. DeepSeek-AI. *DeepSeek-V4 Technical Report*. HuggingFace, 2026. https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf
7. DeepSeek-AI. *mHC: Manifold-Constrained Hyper-Connections*. arXiv:2409.19606（更新版 2025-12-31）。
8. *Hardware-Centric Analysis of DeepSeek's Multi-Head Latent Attention*. arXiv:2506.02523, 2025（第三方 MLA 硬件分析）。

### 11.2 推理模型（R1 Series）

9. DeepSeek-AI. *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948 (2025-01-22; v2 2026-01-04). Nature **645**, 633–638 (2025). DOI: 10.1038/s41586-025-09422-z.
10. DeepSeek-AI. *DeepSeek-R1-0528 Release Notes*. https://api-docs.deepseek.com/news/news250528 (2025-05-28).
11. DeepSeek-AI. *DeepSeek-R1-Lite-Preview Announcement* (2024-11). chat.deepseek.com.

### 11.3 视觉语言（VL Series）

12. Lu H., Liu W., Zhang B., et al. *DeepSeek-VL: Towards Real-World Vision-Language Understanding*. arXiv:2403.05525 (2024-03-08).
13. Wu Z., Chen X., Pan Z., et al. *DeepSeek-VL2: Mixture-of-Experts Vision-Language Models for Advanced Multimodal Understanding*. arXiv:2412.10302 (2024-12-13).
14. DeepSeek-AI. *DeepSeek-OCR: Contexts Optical Compression*. arXiv:2510.18234 (2025-10-20).

### 11.4 代码（Coder Series）

15. Guo D., Zhu Q., Yang D., et al. *DeepSeek-Coder: When the Large Language Model Meets Programming — The Rise of Code Intelligence*. arXiv:2401.14196 (2024-01-25).
16. Zhu Q., Guo D., Shao Z., et al. *DeepSeek-Coder-V2: Breaking the Barrier of Closed-Source Models in Code Intelligence*. arXiv:2406.11931 (2024-06-17).

### 11.5 数学与形式化证明（Math / Prover Series）

17. Shao Z., Wang P., Zhu R., et al. *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models*. arXiv:2402.03300 (2024-02-05).
18. DeepSeek-AI. *DeepSeekMath-V2: Towards Self-Verifiable Mathematical Reasoning*. arXiv:2511.22570 (2025-11-27).
19. Xin H., Guo Z., et al. *DeepSeek-Prover: Advancing Theorem Proving in LLMs through Large-Scale Synthetic Data*. arXiv:2405.14333 (2024-05-23).
20. Xin H., Ren Z., Song J., et al. *DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement Learning and Monte-Carlo Tree Search*. arXiv:2408.08152 (2024-08-15).
21. DeepSeek-AI. *DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition*. arXiv:2504.21801 (2025-04-30).

### 11.6 多模态生成（Janus Series）

22. Wu C., Chen X., Wu Z., et al. *Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation*. arXiv:2410.13848 (2024-10-17). CVPR 2025.
23. Ma Y., Liu X., et al. *JanusFlow: Harmonizing Autoregression and Rectified Flow for Unified Multimodal Understanding and Generation*. arXiv:2411.07975 (2024-11).
24. Chen X., Wu Z., Liu X., et al. *Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling*. arXiv:2501.17811 (2025-01-27).

### 11.7 官方公告与 Changelog

25. DeepSeek API Docs – [Change Log](https://api-docs.deepseek.com/updates/)，动态页面列有截至2026-10-17的条目；页面状态与快照信息见来源清单。
26. DeepSeek API Docs – DeepSeek-V3.1 Release (2025-08-21). https://api-docs.deepseek.com/news/news250821
27. DeepSeek API Docs – DeepSeek-V3.1-Terminus (2025-09-22). https://api-docs.deepseek.com/news/news250922
28. DeepSeek API Docs – Introducing DeepSeek-V3.2-Exp (2025-09-29). https://api-docs.deepseek.com/news/news250929
29. DeepSeek API Docs – DeepSeek-V4 Preview Release (2026-04-24). https://api-docs.deepseek.com/news/news260424

V4.1 更新涉及的一手来源：[V4.1-Flash-1017公告](https://api-docs.deepseek.com/news/news261017/)、[V4.1原版论文2609.19969v1](https://arxiv.org/abs/2609.19969v1)、[1017固定模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/blob/1bae0e1088993b9b82de08f59de5be5a34e42170/README.md)、[原版固定模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/README.md)、[Pro-0813固定模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/blob/72e1d3230f6c080a530b0a1d46f8eb4602340597/README.md)。完整来源身份/论文与权重日期/未解决冲突见 [sources/MANIFEST.md](sources/MANIFEST.md)。

### 11.8 第三方综述与交叉验证

30. Sebastian Raschka. *A Technical Tour of the DeepSeek Models from V3 to V3.2*. Ahead of AI Magazine, 2025-12. https://magazine.sebastianraschka.com/p/technical-deepseek
31. Rohan Paul. *DeepSeek-V3's Architectural Revolution*. https://www.rohan-paul.com/p/deepseek-v3-technical-report-they

### 11.9 代码与权重仓库

- GitHub Org: https://github.com/deepseek-ai （34+ repositories）
- Hugging Face Org: https://huggingface.co/deepseek-ai
- 关键 repo：`DeepSeek-LLM`、`DeepSeek-MoE`、`DeepSeek-V2`、`DeepSeek-V3`、`DeepSeek-V3.2-Exp`、`DeepSeek-R1`、`DeepSeek-VL2`、`DeepSeek-Coder-V2`、`DeepSeek-Prover-V2`、`Janus`、`DeepSeek-OCR`。

### 11.10 新鲜度补核：分块 KV 压缩的相位敏感性（2026-09）

ByteDance Seed 团队于 2026-09-28 发布 [*Periodic Weak Spots: Phase Sensitivity from Chunked KV-Cache Compression*](https://seed.bytedance.com/en/public_papers/periodic-weak-spots-phase-sensitivity-from-chunked-kv-cache-compression) 对 V4 长上下文评测补上了重要限制：分块 KV 压缩会使检索表现依赖信息相对压缩 stride 的 phase。论文在 128K NIAH 设置中报告，DeepSeek-V4-Flash / Pro 基座检查点的最大相位差分别为 **40.23 / 34.77 个百分点**，后训练检查点仍有 **19.14 / 14.84 个百分点**差距；V4.1-Flash 为 **6.09 个百分点**。这些是 2,048 或 20,480 条固定合成 key-value 检索提示上的 residue 组间差，不是产品总体准确率。V4 的八个 modulo-8 residue 组覆盖两个 stride=4 周期，V4.1 覆盖四个 stride=2 周期；目标位置均值、方差及 query 位置配平，但外层 filler 同时移动了干扰记录。受控 Qwen3-0.6B 派生模型的压缩与 full-attention 对照支持压缩 stride 是周期性弱点的来源；KV-head knockout 机制证据来自这些受控模型，DeepSeek-V4 侧的干预是整层 attention 输出替换。该机制证据不等于完整重建 DeepSeek-V4。逐篇精读见[相位敏感性分册](deepseek-phase-sensitivity.md)。

固定版本与锚点：Zhu et al., [arXiv:2609.36322v1](https://arxiv.org/abs/2609.36322v1)，arXiv 显示 v1 于 2026-09-28 21:54 UTC 提交，PDF 首页日期为 2026-09-30；arXiv 版本页链接 CC BY 4.0，本文为预印本。§2、图 1–2、Table 7 报告 V4/V4.1 的周期翻转与 NIAH residue 差；§3.2、图 3 和 Table 8 对比压缩/全注意力与窗口/stride 变体；§4、图 4 分别展示受控模型 KV-head knockout 和 V4 层级 attention-output intervention，图 5 是受控模型 gate 结果。附录 C.1 给出 128K NIAH 提示构造，且说明目标 phase 与干扰项 phase 未独立移动。逐篇证据与七问见[相位敏感性精读](deepseek-phase-sensitivity.md)；来源清单 §8 记录工具使用口径及可复核边界。
- HuggingFace V4 集合：https://huggingface.co/collections/deepseek-ai/deepseek-v4

---

> *本报告基于 [deepseek-text-models.md](deepseek-text-models.md)（纯文本基座模型）与 [deepseek-multimodal-and-specialized.md](deepseek-multimodal-and-specialized.md)（多模态与专业模型）两份子报告整合提炼。如需查看某一方向的更详细技术细节（如训练超参、消融实验、benchmark 完整数值），请回到子报告。*

> **V4.1 更新范围**：本文聚焦 V4 正式版本至 V4.1-Flash-1017 的版本身份及相关主报告结论；原文覆盖范围、固定 revision 与未解决项见来源清单。历史子报告与当前路由映射属于不同证据范围，不应相互替代。
