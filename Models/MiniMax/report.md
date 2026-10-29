---
display_name: MiniMax
---

# MiniMax 系列模型研究报告：混合注意力、后训练与多模态路线

> 撰写时间：2026-06-05 ｜ 研究范围：MiniMax-abab 系列、MiniMax-01（Text/VL）、MiniMax-Speech 与海螺音视频模型、MiniMax-M1/M2/M2.5/M2.7/M3 推理与 Agent 模型、海螺 AI 产品线

---

## 1. 概述与时间线

本报告沿 MiniMax 的公开论文和模型报告梳理稀疏专家、混合注意力、推理后训练、工具任务与多模态生成几条研究线。重点是这些机制解决什么约束、论文用什么设置评估，以及结论能否跨任务外推；不以公司排名、商业策略或产品覆盖面作为技术判断。

**关键时间线**

| 时间 | 模型 / 事件 | 关键技术 / 形态 |
|------|--------------|------------------|
| 2021-12 | MiniMax 成立 | 闫俊杰创立，立足通用大模型 + 多模态 |
| 2022 末 – 2023 初 | abab 早期版本（abab1/2） | 自研稠密 Transformer 基座 |
| 2023-04 | MiniMax 开放平台正式上线 | API 形态对外提供模型能力 |
| 2023 中后期 | abab5 / abab5.5 | 扩规模、强化指令/对话能力 |
| 2024-01 | abab6 | **国内首个 MoE 大语言模型** |
| 2024-04-17 | abab6.5 / abab6.5s | 万亿参数 MoE，**200k token 上下文** |
| 2024 下半年 | 海螺 AI 视频上线（Video-01、I2V-01-Live） | 多模态产品线开始集中爆发 |
| 2024 下半年 – 2025 初 | T2A-01 / T2V-01-Director / I2V-01-Director | 文生音、镜头控制视频 |
| 2025-01-14 | **MiniMax-Text-01 / MiniMax-VL-01** 论文与权重开源（arXiv:2501.08313） | **456B 总参 / 45.9B 激活** MoE + **Lightning Attention + Softmax 混合注意力**，训练 1M、推理 4M token |
| 2025-05-12 | MiniMax-Speech 技术报告（arXiv:2505.07916） | AR Transformer + 可学习 Speaker Encoder + Flow-VAE，32 语种零样本声纹克隆，登顶 Artificial Arena |
| 2025 上半年 | Speech-02-series、MiniMax Music 1.5 / 02 | 文本到音频、音乐生成 |
| 2025-06-16 | **MiniMax-M1**（arXiv:2506.13585） | **首个开源大规模混合注意力推理模型**，1M 上下文，提出 CISPO RL 算法，3 周 / 53.47 万美元完成 RL 训练 |
| 2025-10 | **MiniMax-M2** 开源 | **230B / 10B 激活** MoE，主打 coding + agent，登顶 Artificial Analysis 开源综合榜 |
| 2026-01-23 | **Speech-2.8** | 语音合成重大升级，情感表达与多语种覆盖增强 |
| 2026-01-29 | MiniMax Music 2.5 | 段落级控制、音质与可控性大幅提升 |
| 2026-02-12 | **MiniMax-M2.5** 开源 | **Agent 生产级 LLM**，SWE-Bench Verified 80.2%，速度比 M2.1 快 37%，成本仅 Claude Opus 4.6 的 10% |
| 2026-03-18 | **MiniMax-M2.7** | 递归自我改进（Recursive Self-Improvement）启动 |
| 2026-04 | **Music-2.6** | 音乐生成再升级，纯器乐创作扩展至古典、电子、ambient、电影配乐 |
| 2026-05 | Hailuo-2.3 / 2.3-Fast | 视频生成质量与速度双提升，Fast 版面向实时预览场景 |
| 2026-06-01 | **MiniMax-M3** | 最新 M 系列旗舰，代理推理、工具使用、编码、多模态聊天、长上下文统一 |

整条时间线的演进逻辑可以概括为：**abab 时代押注 MoE → MiniMax-01 时代押注线性注意力 → M1/M2 时代押注 RL + Agent，并把 Lightning Attention 的训练/测试时计算优势迁移到推理模型**。

---

## 2. 基座模型演进：从 abab 到 MiniMax-01 再到 M-series

### 2.1 abab 系列（2022–2024）：押注 MoE 的稠密→稀疏过渡

`abab` 名字来自于 MiniMax 内部对自研基座系列的代号。早期 abab1/2 是常规 Decoder-Only 稠密 Transformer，主要承担产品（Glow / Talkie / 星野）的对话与人设生成能力；abab5 / abab5.5（2023）开始引入更大规模训练数据与强化的对话/指令对齐管线，对中文综合能力做了重点优化。

真正的转折点是 **abab6（2024 年 1 月）**：MiniMax 把 80% 以上的研发精力投在了 MoE 上，发布了**国内首个 MoE 大语言模型**。MoE 的稀疏激活策略让 abab6 在保持单 token 推理成本可控的前提下，把"总知识容量"提升一个数量级。

**abab6.5 / abab6.5s（2024-04-17）** 进一步将 MoE 推到**万亿（trillion）级总参数**，并把上下文窗口扩展到 **200k tokens**：

- `abab6.5`：万亿总参 MoE，官方材料列出 200k 上下文；与 GPT-4、Claude 2.1 的比较和长文档能力描述应限于当时公布的版本与测试，不能由窗口长度推出综合能力。
- `abab6.5s`：相同训练数据与方法，但更轻量，推理更快，**1 秒可处理近 3 万字**，主打高吞吐场景。
- 两者通过 MiniMax 开放平台、海螺 AI 等产品对内对外滚动更新。

标准 Softmax Attention 的计算与 KV 缓存成本会随序列长度增长，使超长上下文训练和推理面临计算与内存压力。MiniMax-01 论文选择混合线性注意力与 Softmax 注意力的方案；这是一种设计取舍，并不意味着所有百万级上下文模型都必须移除 Softmax。

### 2.2 MiniMax-01：把 Lightning Attention 推到 456B 规模

2025 年 1 月 14 日，MiniMax 发布技术报告 *MiniMax-01: Scaling Foundation Models with Lightning Attention*（arXiv:2501.08313），同步在 GitHub 与 Hugging Face 开源 **MiniMax-Text-01 / MiniMax-VL-01** 两个模型权重，许可使用宽松的 MiniMax 协议。

**MiniMax-Text-01 关键架构参数**（来自官方仓库与论文）：

| 维度 | 数值 |
|------|------|
| 总参数 | **456B** |
| 单 token 激活参数 | **45.9B** |
| 层数 | 80 |
| 注意力头数 | 64 |
| 注意力头维度 | 128 |
| Hidden Size | 6144 |
| 词表 | 200,064 |
| MoE 专家数 | 32（FFN 隐层 9216） |
| 路由策略 | Top-2 |
| 位置编码 | RoPE，base=1e7，仅作用于一半头维度 |
| **混合注意力比例** | **每 7 层 Lightning Attention 后接 1 层 Softmax Attention** |
| 训练上下文长度 | 1,000,000 tokens |
| 推理外推上下文 | **4,000,000 tokens**（NIAH 4M 通过） |

MiniMax-01 论文展示了在 456B 总参数 MoE 与百万级训练上下文下使用混合注意力的一种实现，并公开对应模型权重。其核心组合是：

1. **Lightning Attention（线性注意力高效实现）**——把训练/推理成本从 O(n²d) 降到 O(nd²)，并通过 IO-aware tiling 把常数项压平；
2. **Softmax 兜底**——只在每 8 层中保留 1 层 Softmax，承担长程检索与精确召回任务，弥补线性注意力在"针在干草堆"等任务上的检索弱项；
3. **MoE 稀疏激活**——保证容量与质量，单 token 仅激活 45.9B 参数；
4. **针对 MoE + Lightning Attention 共同优化的并行策略与 communication-overlap 技术**，让百万级序列的训练 / 推理在数千卡集群上可承担。

MiniMax-01 论文在 MMLU、IFEval、Arena-Hard、C-SimpleQA 等基准报告与指定对照模型的结果，并在 RULER、LongBench v2、MTOB 等长上下文任务中作比较。以下数字均为论文报告结果；它们对应不同基准与评测协议，不能合并成统一的“总体同档”或跨模型排名：

- **RULER（1M 长度）**：MiniMax-Text-01 = 0.910；在该论文列出的 1M 对照模型中，它是达到 0.9 以上的模型；
- **LongBench v2 w/ CoT**：56.5（人类 53.7、GPT-4o 51.4、Claude-3.5-Sonnet 46.7）；
- **MTOB 半本书翻译 ChrF Δ**：+45.7；按论文任务构造和指标定义理解，不概括为所有长文档翻译任务的领先。

这些结果说明论文中的混合配置可在指定的长上下文基准上运行。线性注意力部分的渐近复杂度不能直接换算为整套模型在所有序列长度下的实际算力或成本收益；具体收益仍取决于实现、Softmax 注意力层比例、硬件和任务。

### 2.3 MiniMax-M2 / M2.5：编码与 Agent 任务

到了 2025 年 10 月，MiniMax 在 GitHub 开源 **MiniMax-M2**：

- **230B 总参 / 10B 激活**的 MoE 模型；
- 官方定位是"Mini model built for Max coding & agentic workflows"；10B 激活参数说明其稀疏计算配置，但不单独证明端到端 Agent 延迟或并发收益，后者还取决于工具执行、批量、硬件和服务栈；
- MiniMax 的报告列出 SWE-bench Verified = 69.4、Terminal-Bench = 46.3、ArtifactsBench = 66.8、BrowseComp = 44、τ²-Bench = 77.2 等结果；它们是各基准的独立分数，不能合并成跨基准综合排名；
- M2 是**交错思考（interleaved thinking）模型**，输出中保留 `<think>...</think>` 段，多轮历史必须原样回传，否则性能显著下滑；
- 后续推出的 **MiniMax-M2.1（2025-12-22）** 进一步强化多语言编程精通能力，在 LiveCodeBench、FullStackBench 等代码基准上持续提升。

**MiniMax-M2.5（2026-02-12）** 的公开报告补充了 M2 系列在代码与 Agent 任务上的评测结果：

- MiniMax 报告 SWE-Bench Verified 80.2%、Multi-SWE-Bench 51.3%、BrowseComp 76.3%；引用时需保留基准版本、harness 与预算条件，不据此推出模型总体排名；
- M2.5 与 M2.1 的速度对照，以及与 Claude Opus 4.6 的端到端耗时比较，均依赖报告所述任务和执行配置；它们不代表所有 Agent 工作流的固定延迟差异；
- API 定价与托管速度不作为本报告的研究结论；
- 开源权重，**197K 上下文**支持；
- **10+ 语言编程**能力，在 20 万+ 真实软件工程环境中完成 RL 训练；
- 定位"原生 Agent 生产级 LLM"，覆盖编程、工具调用、信息检索与办公场景。

**MiniMax-M2.7（2026-03-18）** 报告了递归自我改进（Recursive Self-Improvement）流程，使用模型生成数据、评价并迭代训练。要判断它是否带来可复现的持续提升，需要检查独立验证、固定评测集以及跨轮次增益；流程描述本身不等于已排除数据污染或自评偏差。

**MiniMax-M3（2026-06-01）** 的公开材料描述了代理推理、工具使用、编码、多模态聊天与长上下文：

- 在 M2.5 的 agentic 基础上进一步扩展至多模态输入（文本 + 图像 + 音频）的端到端 agent 闭环；
- 公开材料描述其使用 Lightning Attention 混合架构；长上下文效率仍需结合论文中的固定负载与对照理解；
- 支持更复杂的 multi-hop 工具调用与跨会话记忆保持；
- 同时提供 API 与开源权重，延续 MiniMax"开源旗舰 + 产品闭环"的双轨策略。

注意：M2/M2.1/M2.5/M2.7/M3 的命名沿用 M1 系列，但在公开资料中并未强调 M2 及后续版本是否继续使用 hybrid lightning attention（M2 更接近"小激活、强 agent"路线，技术细节官方信息相对克制）；而 M1 则是**MiniMax-Text-01 架构在推理方向上的直接继承者**。

---

## 3. Lightning Attention 核心技术深度解析

Lightning Attention 是 MiniMax-01 / M1 体系的"地基"。它本质上是**线性注意力（Linear Attention）的 IO-aware 高效实现**，由 Zhen Qin 等人提出（TransNormer / TransNormerLLM 系列工作），在 *Various Lengths, Constant Speed: Efficient Language Modeling with Lightning Attention*（ICML 2024，arXiv:2405.17381）中给出完整算法，并被 MiniMax-01 真正大规模工程化。

### 3.1 标准 Softmax Attention 的瓶颈

经典自注意力为：

$$\mathbf{O} = \text{softmax}\!\big(\mathbf{Q}\mathbf{K}^\top / \sqrt{d}\big)\,\mathbf{V}$$

- 时间复杂度 **O(n²d)**，对长序列不友好；
- KV cache 内存随序列线性增长，4M token 级别的 KV cache 几乎无法承受；
- FlashAttention 系列只是**优化常数与 IO**，理论复杂度仍是 n²。

### 3.2 Linear Attention 的核心思想

线性注意力把 Softmax 拆掉，用核函数把 Attention 拆成 Q · (KᵀV)：

$$\mathbf{O} = \phi(\mathbf{Q})\,\big(\phi(\mathbf{K})^\top \mathbf{V}\big)$$

由于矩阵乘满足结合律，可以**先算 KᵀV ∈ ℝ^{d×d}**，复杂度从 O(n²d) 降到 O(nd²)。在递推形式下还能写成：

$$\mathbf{kv}_t = \mathbf{kv}_{t-1} + \mathbf{k}_t\mathbf{v}_t^\top,\quad \mathbf{o}_t^\top = \mathbf{q}_t^\top \mathbf{kv}_t$$

理论上 KV 状态固定为 d×d，**推理时常数空间、常数复杂度**——天生就是给"百万 token 上下文"准备的。

但是在因果（causal）训练时存在两个老问题：

1. **cumsum 瓶颈**：递推形式必须串行扫描所有时间步，每步累加 KᵀV，无法并行，GPU 利用率极低；
2. **精度差距**：朴素 1+elu 等核近似的线性注意力在语言建模上长期落后于 Softmax。

### 3.3 Lightning Attention 的关键贡献

Lightning Attention 的核心 idea 是**用分块 + intra/inter 双路径计算消除 cumsum**，并把整个算法做成 FlashAttention 风格的 IO-aware kernel：

1. **分块（tiling）**：把 Q/K/V 沿序列维切成 T = n/B 块，每块大小 B×d；
2. **块内（intra-block）走 Left Product**：在块内仍然用 [(QKᵀ) ⊙ M] V 这种"先算 QKᵀ"的左乘范式，因为块小、能并行、能放进 SRAM 共享内存；
3. **块间（inter-block）走 Right Product**：维护一个全局 KV ∈ ℝ^{d×d} 累加器，块结束时把 K_tᵀV_t 累加进 KV，下一块只需要做 Q_{t+1}·KV 即可——这一步不需要逐 token cumsum，而是**逐块累加**；
4. **每块输出 = O_intra + O_inter**，等价于完整 causal 线性注意力，**精确而非近似**；
5. **IO 优化**：所有中间量 Q_t、K_t、V_t、KV 都尽量在 on-chip SRAM 上滚动，最大化避免 HBM 读写，用 Triton 写 kernel；
6. **反向传播同样 tiled**：dQ、dK、dV 和 dKV 都分块计算，不再依赖整序列 cumsum，反向也享有 O(nd²) 复杂度与近常数显存。

理论复杂度（论文 Theorem 3.1）：

$$O(nd^2 + nBd),\quad 取\;B \approx d \;\Rightarrow\; O(nd^2)$$

实测中，与 Vanilla Linear Attention 和 FlashAttention-2 对比：

- **训练吞吐**：FlashAttention-2 的耗时仍随序列长度二次增长，Lightning Attention **保持线性增长**，并且**在不同序列长度下保持常数级训练速度**（这是论文标题"Various Lengths, Constant Speed"的来源）；
- **显存**：Vanilla 线性注意力会因为中间矩阵爆显存，Lightning Attention 显存占用与 FlashAttention-2 同级甚至更低；
- **质量**：在 Wikitext-103 / 大规模 LLM 训练上 perplexity 和下游能力**追平甚至超过 Softmax Transformer**（TransNormerLLM 已在 7B/15B 量级验证，MiniMax-01 把验证规模推到 456B）。

### 3.4 与标准 Attention 的复杂度与表达能力对比

| 维度 | Softmax Attention | FlashAttention-2 | Lightning Attention |
|------|--------------------|-------------------|---------------------|
| 训练时间复杂度 | O(n²d) | O(n²d) | **O(nd²)** |
| 训练显存（理论） | O(n²) → 经 Flash 降到 O(n) | O(n) | **O(n)**，常数极小 |
| 推理 KV 状态 | 随序列线性增长 | 同 Softmax | **固定 d×d** |
| 推理时间（每 token） | O(nd) | O(nd) | **O(d²)** |
| 信息容量 | 显式存储所有 token | 同 Softmax | 隐式压缩进 KV 矩阵 |
| 长程检索 | 强 | 强 | 偏弱（信息被压缩） |
| 长上下文成本 | 二次方爆炸 | 二次方爆炸 | **线性** |

这张对比表也直接解释了 MiniMax-01 为什么不是"纯线性注意力"，而是 **Hybrid 混合注意力**。

### 3.5 Hybrid Lightning + Softmax 混合策略

MiniMax-01 / M1 采用的混合方式是：

> **每 7 层 Lightning Attention 后插入 1 层标准 Softmax Attention**（也就是 8 层为一个 block，1/8 的层是 Softmax）。

设计动机：

1. **质量兜底**：纯线性注意力在 NIAH（Needle-In-A-Haystack）、长程精确检索类任务上的表现不如 Softmax；保留少量 Softmax 层负责"重要 token 的精确召回"；
2. **成本主导 = Lightning**：7/8 的层是 Lightning Attention，长上下文几乎所有计算瓶颈都在 O(nd²) 那一侧，因此推理 4M token 才"可承受"；
3. **混合配置的消融**：MiniMax-01 论文在其模型、训练数据和长上下文评测设置下比较 Hybrid-Lightning + MoE 与纯 Softmax + MoE。该对照支持作者在该设置下的选择，不能推出混合配置在所有模型、任务或上下文长度上都优于纯 Softmax；
4. **长上下文 + 推理时计算（test-time compute）双友好**：M1 后续做 RL 推理时，长 chain-of-thought 不会让显存爆炸——这是 M1 能做 80K thinking budget 的硬件基础。

### 3.6 上下文窗口扩展：1M 训练 → 4M 推理

MiniMax-Text-01 训练阶段直接把上下文拉到 100 万 token，并通过：

- **RoPE base 提升到 1e7**（远高于 LLaMA 的 1e4），缓解长程角度坍缩；
- 仅对一半头维度施加 RoPE，剩余维度保持 NoPE，配合线性注意力的隐式记忆；
- 长上下文阶段的数据 curriculum 与高质量长文档数据；

论文报告训练上下文为 1M，并在该模型的 4M Needle-In-A-Haystack 设置中评估外推能力。该结果说明模型在特定检索任务中能处理 4M 输入；不等于对任意任务都有效利用 4M 上下文，也不需要据此作跨模型“唯一”判断。

### 3.7 训练效率收益

线性注意力的渐近计算量与 Softmax 注意力不同；整套训练栈能获得多少收益还取决于序列长度、线性/Softmax 层比例、内核、通信与硬件。MiniMax-01 技术报告给出了该模型的训练系统案例：

- **FLOPs**：线性注意力在固定特征维度下对序列长度呈线性计算，Softmax 注意力包含二次项；这不是整套模型实际 FLOPs 比例的直接预测。
- **激活 / KV 显存**：线性递推状态避免存储完整注意力矩阵，但混合模型仍保留 Softmax 层，因此内存收益取决于层配置和实现。
- **并行策略**：技术报告描述了为 MoE 与 Lightning Attention 组合设计的并行切分和通信计算重叠；其长序列可行性证据限于论文采用的训练集群与批量配置。
- **RL 训练**：M1 报告了特定规模的强化学习运行。训练费用不用于比较方法能力，且不能由此推断同规模 Softmax 模型无法训练。

---

## 4. 多模态能力：从 VL 到 Speech / Music / Video

本节比较论文报告的模态表示与训练机制；不从产品组合或发布节奏推断 MiniMax 与其它公司的整体多模态战略。

### 4.1 MiniMax-VL-01：把视觉接到 Lightning 基座上

MiniMax-VL-01 在 MiniMax-Text-01 之上**继续训练 5120 亿（512B）视觉-语言 token** 得到，结构是经典的 ViT + MLP Projector + LLM：

- **视觉编码器**：303M 参 ViT，24 层，patch=14，hidden=1024，FFN=4096，16 头 × 64 维；
- **语言主干**：原 MiniMax-Text-01（456B / 45.9B 激活、Hybrid Lightning Attention）；
- 训练做了多阶段：图像描述对齐 → 多任务图文 → 长视觉文档（M-LongDoc）。

**Vision Benchmark 表现**（节选自官方仓库）：

- MMMU = 68.5、MMMU-Pro = 52.7；分数来自材料所列评测版本和协议
- ChartQA = 91.7、DocVQA = 96.4、OCRBench = 865（OCR 与图表是强项）
- M-LongDoc（长视觉文档）= 32.5；该值应与相同版本和协议的对照读取
- MathVista = 68.6、In-house Benchmark = 56.6

VL-01 论文覆盖视觉问答、图表、文档与长视觉输入；其长上下文表现应以所列测试集和上下文构造为边界，不能外推为相对其它 VLM 的普遍优势。

### 4.2 MiniMax-Speech / Speech-02：可学习 Speaker Encoder + Flow-VAE

**MiniMax-Speech**（arXiv:2505.07916，2025-05）的核心系统由三部分构成：

1. **Tokenizer**：文本 BPE + 音频 Encoder-VQ-Decoder（基于 mel-spectrogram，25 token/s，CTC 监督）；
2. **自回归 Transformer**：把文本 token 映射到离散音频 token 序列；
3. **Latent Flow Matching 解码器 + Flow-VAE**：把离散 token 还原成高保真波形。

两项关键创新：

- **Learnable Speaker Encoder（可学习说话人编码器）**：业界主流（CosyVoice2 / Seed-TTS / VALL-E 等）依赖预训练的说话人验证（SV）模型作为冻结的 speaker encoder，而 MiniMax 让 speaker encoder **与 AR Transformer 联合训练**，提取的不是 SV 任务向量，而是真正服务于 TTS 任务的"音色 + 韵律"条件向量。结果是：
  - 严格意义上的 **"intrinsic zero-shot"** 声纹克隆——只需一段无转写参考音频就能克隆说话人；
  - 摆脱对 paired text-audio 的依赖；
  - 论文报告编码器在 32 种语种上联合训练，并在其跨语种声纹测试中评估音色保持；不据此概括为跨语种普遍领先。

- **Flow-VAE**：传统 VAE 假设潜变量符合标准正态，会形成信息瓶颈；MiniMax 在 VAE encoder 输出后再串一个 Normalizing Flow，把潜分布映射到标准正态后才计算 KL，使得 encoder 实际可以输出**任意正态分布**，潜空间表达力显著提升。Flow Matching 解码器在该潜空间上做生成，比"先生成 mel-spectrogram 再 vocoder"的两段式方案保真度更高。

**评测结果**：

- Seed-TTS-eval：论文报告 zero-shot WER（test-zh / test-en）= 0.83 / 1.65，one-shot SIM = 0.799 / 0.738；WER 与 SIM 衡量不同属性，按其样本和协议解释，不将 WER 低于某参考语音写成整体优于参考；
- **多语种**：论文在 Vietnamese、Thai、Cantonese 等语种上报告 WER，并与其列出的系统比较；结果受语种、测试集、转写规范和服务版本影响，不合并成跨语言排名；
- **Artificial Arena（2025-05-12）**：报告记录了 MiniMax-Speech 在当时的 Artificial Arena 人类偏好评测中的 ELO 排名。该读数应按当日参评系统、版本和听测协议理解，不能视为跨服务、跨时段的普遍语音质量排序。

API 与产品落地：

- 平台侧 `Speech-02-HD`（高保真）/ `Speech-02-Turbo`（更快、更便宜）；
- **Speech-2.8（2026-01-23）**：语音合成重大升级，情感表达更细腻自然，多语种覆盖进一步扩展，支持更复杂的语调控制与风格迁移；
- 海螺 AI 文生音支持最长 10000 字符输入；
- 在海螺 Audio、海螺视频配音、Talkie 数字人对话中全面使用。

### 4.3 MiniMax Music：从 Music 1.5 到 Music 2.5+

- **Music 02**：MoE 架构的 text-to-music 模型，支持歌词/段落控制、风格控制；
- **Music 1.5**（2025）：把生成时长扩到 4 分钟级别；
- **Music 2.0 / 2.5（2026-01-29）**：可控性、真实感再一次上台阶，支持**段落级控制**与人声+乐器协作；
- **Music 2.6（2026-04）**：音乐生成再升级，纯器乐创作能力大幅扩展，覆盖古典、电子、ambient、电影配乐等更多风格，音质与结构完整性进一步提升；
- **Music 2.5+**（2026 上半年）：作为 2.6 的前置探索，已扩展到纯器乐创作。

整个 Music 路线和 Speech 共用了**音频 token 化 + AR Transformer + Flow Matching 解码器**这一套基础设施。

### 4.4 海螺视频：Video-01 / T2V-01-Director / I2V-01-Director

视频侧，海螺视频（hailuoai.video）依托：

- **Video-01**：text-to-video 通用模型；
- **T2V-01-Director**：文生视频，支持镜头语言（推拉摇移、运镜节奏、构图）显式控制；
- **I2V-01-Director / I2V-01-Live**：图生视频，支持把静态图人物按导演脚本进行表演；
- **Hailuo-2.3 / 2.3-Fast（2025-10-28）**：视频生成质量与速度双提升，2.3-Fast 面向实时预览与快速迭代场景，在保持画质的同时显著缩短生成时间；

`01-Director` 系列把"专业镜头语言"作为可控属性放到 prompt 里，是海螺视频在 C 端短视频/电影预可视化上的差异化卖点；其海外月访问量已达千万级。

### 4.5 海螺 AI 与 Talkie：双产品矩阵

- **海螺 AI（hailuoai.com / hailuoai.video）**：全面整合文本（基于 abab/MiniMax-01/M-series）、语音（Speech-02）、音乐（Music）、视频（Video-01）、图像；C 端定位"多模态生产力 + 创作力"。
- **Talkie / 星野**：海外/国内的 AI 角色陪伴与创作社区，依托 MiniMax 自研对话与人设模型，海外 Talkie MAU 曾突破 1100 万。
- **MiniMax Open Platform / minimax.io**：B 端 API，提供 ChatCompletion、Realtime、Finetune、T2A、Music、Video 等接口。
- **MiniMax Agent（2025-10 起）**：基于 M2/M2.5 的浏览器/IDE/终端 agent 产品。

商业上，多模态 + 出海是 MiniMax 与国内同行最大的差异。

---

## 5. 推理模型 MiniMax-M1：把 Lightning Attention 扩展到 Test-Time Compute

2025 年 6 月，MiniMax 发布 **MiniMax-M1**（arXiv:2506.13585），副标题直指核心命题：*Scaling Test-Time Compute Efficiently with Lightning Attention*。

### 5.1 模型定位与规模

M1 论文展示了一个开源权重的大规模 hybrid-attention 推理模型：

- 基于 MiniMax-Text-01 继续训练，**456B 总参 / 45.9B 激活**；
- 沿用 Lightning Attention + Softmax + MoE 的混合结构；
- **论文报告 1M token 上下文设置**；与其它模型的窗口长度对照不等同于相同任务下的有效上下文能力比较；
- 提供两个版本：**M1-40K**（思考预算 40K token，相当于 80K 训练的中间版本）、**M1-80K**（80K 思考预算）。

### 5.2 为什么 Lightning Attention 让 M1 成为可能

M1 论文将长 chain-of-thought 作为推理负载之一：随着生成 token 增多，Softmax 注意力的计算和 KV cache 会继续增长。Lightning Attention 在其线性注意力层上提供另一种增长方式，但模型仍保留 Softmax 层，整套系统的收益取决于上下文、生成长度与运行配置：

- 在线性注意力层中，论文给出的注意力计算随序列长度呈线性增长；混合模型的总计算还包括保留的 Softmax 层与其它模块；
- 在该模型的 7/8 Lightning 层中，递推 KV state 的大小不随序列长度线性增长；
- 论文配置了 1M 输入与 80K 思考预算；这描述模型支持的实验设置，不证明所有任务均可同时有效利用这些预算。

M1 论文在 OpenAI-MRCR-1M 与 LongBench-v2 等任务中报告了与 DeepSeek-R1、Qwen3-235B 的对照结果。结果支持作者对所测试长上下文任务的观察，不能仅凭这些分数把优势归因于 Lightning Attention；模型版本、提示、预算和评测协议也会影响比较。

### 5.3 CISPO：为长 RL 训练定制的策略算法

M1 提出 **CISPO**（Clipped Importance Sampling Policy Optimization），核心想法是：

> **裁剪重要性采样权重，而非裁剪 token 级 update**，绕开传统 PPO/GRPO 中由于策略漂移导致的不稳定。

M1 论文在其 RL 任务和训练设置中将 CISPO 与 GRPO、Dr. GRPO、DAPO 等变体作比较，并报告相应结果；这支持作者对该训练配置的选择，不证明 CISPO 在不同任务或预算下普遍占优。

- 论文描述了 512 张 H800 上的 RL 训练运行。硬件规模和训练时长用于理解实验条件，不在此换算成方法成本排名。

### 5.4 训练数据与任务

M1 的 RL 任务覆盖：

- 数学推理（AIME 2024/2025、MATH-500）
- 代码（LiveCodeBench、FullStackBench）
- **真实软件工程（SWE-bench，沙盒化的真实仓库）**
- 工具使用（TAU-bench airline / retail）
- 长上下文（OpenAI-MRCR 128k/1M、LongBench-v2）

### 5.5 评测结果（节选）

下表是 M1 报告列出的模型分数。各列版本、提示、采样和执行环境需按报告说明理解；不同基准分别测量不同任务，不构成统一的模型排名。

| 任务 | M1-80K | DeepSeek-R1-0528 | Qwen3-235B-A22B | Claude 4 Opus | Gemini 2.5 Pro | OpenAI-o3 |
|------|--------|------------------|------------------|----------------|------------------|-----------|
| AIME 2024 | 86.0 | 91.4 | 85.7 | 76.0 | 92.0 | 91.6 |
| AIME 2025 | 76.9 | 87.5 | 81.5 | 75.5 | 88.0 | 88.9 |
| MATH-500 | 96.8 | 98.0 | 96.2 | 98.2 | 98.8 | 98.1 |
| LiveCodeBench | 65.0 | 73.1 | 65.9 | 56.6 | 77.1 | 75.8 |
| **SWE-bench Verified** | **56.0** | 57.6 | 34.4 | 72.5 | 67.2 | 69.1 |
| **OpenAI-MRCR (128k)** | **73.4** | 51.5 | 27.7 | 48.9 | 76.8 | 56.5 |
| **OpenAI-MRCR (1M)** | **56.2** | -- | -- | -- | 58.8 | -- |
| LongBench-v2 | 61.5 | 52.1 | 50.1 | 55.6 | 65.0 | 58.8 |
| **TAU-bench airline** | **62.0** | 53.5 | 34.7 | 59.6 | 50.0 | 52.0 |

在论文报告的对照范围内，M1 的结果集中在以下方向：

- **长上下文推理**（MRCR 128k/1M、LongBench-v2）；
- **软件工程 / Agent 工具使用**（SWE-bench Verified、TAU-bench airline）；
- **训练机制**（hybrid attention 与 CISPO）。

在论文所列数学/AIME 对照中，M1 的分数低于 DeepSeek-R1-0528 与 Gemini 2.5 Pro。该观察不能单独归因于 hybrid attention；模型训练数据、奖励、预算和推理设置均可能影响结果。

### 5.6 从 M1 到 M2 / M2.5：方向收敛到 Agent

从公开报告比较，M1 侧重长上下文推理训练，M2 则把重点放在代码与工具任务；这是论文/报告公开目标的变化，不推断为产品战略或内部研发路线切换：

- 使用 **10B 激活参数**；该规模本身不能证明 Agent 闭环延迟或总成本必然降低；
- 在 SWE-bench、Terminal-Bench、BrowseComp、τ²-Bench 等 Agent 基准报告结果，按各基准协议分别理解；
- M2 是 **interleaved thinking 模型**，思考与工具调用交错；
- MiniMax 报告 Artificial Analysis Intelligence 综合分为 61；该分数受榜单版本、任务组合和评测日期影响，不在这里作为模型总体排名。

M2 对开发者最大的吸引力是 **"前沿 agent 能力 + 8% Sonnet 成本"** 这条性价比曲线——这与 M1 强调"长上下文推理"是不同的子目标。从 M1 到 M2，MiniMax 完成了一次"从研究展示到产品化 Agent"的姿态切换。**M2.5** 进一步把 M2 推进为生产级 Agent 模型，覆盖编程 / 工具调用 / 信息检索 / 办公场景。

---

## 6. 跨代技术演进分析

把 abab → MiniMax-01 → M1/M2/M3 放在同一张表里，可以按注意力、训练目标和任务交付物观察公开工作的变化。这个时间线是阅读组织方式，不代表每一代都由前一代机制直接导致，也不证明公司预先规划了单一路线：

| 维度 | abab6.5（2024-04） | MiniMax-01（2025-01） | MiniMax-M1（2025-06） | MiniMax-M2（2025-10） | MiniMax-M2.5（2026-02） | MiniMax-M3（2026-06） |
|------|---------------------|------------------------|------------------------|------------------------|------------------------|------------------------|
| 总参 / 激活 | ~1T MoE | 456B / 45.9B | 456B / 45.9B（同 01） | **230B / 10B** | 230B / 10B（同 M2） | （未公布） |
| 注意力 | Softmax | **Hybrid Lightning + Softmax (7:1)** | Hybrid（同 01） | （未公开混合细节） | （未公开混合细节） | Hybrid Lightning + Softmax |
| 上下文 | 200k | **训练 1M / 推理 4M** | **原生 1M**（thinking 80K） | 长上下文 + agent | **197K** | 长上下文 + 多模态 agent |
| 训练目标 | 通用基座 + 对话对齐 | 通用基座 + VL 继续训练 | **RL + CISPO** | Agent 任务后训练 | Agent 任务后训练 | 多模态 Agent / RSI 研究 |
| 多模态 | 文本主导 | 文本 + ViT 视觉 | 文本推理 | Coding / Agent / 工具 | Coding / Agent / 工具 | 文本 + 图像 + 音频 + Agent |
| 研究焦点 | 稀疏专家模型 | 混合注意力与长上下文 | 推理后训练 | 工具使用与代码任务 | Agent 任务训练 | 多模态 Agent |

**演进逻辑梳理：**

1. **密集模型到 MoE（abab 系列）**：研究重点由稠密容量扩展转到稀疏专家路由；总参数与激活参数的区别决定了参数规模不等于单 token 计算量。
2. **全注意力到混合注意力（MiniMax-01）**：论文研究 Lightning Attention 与 Softmax Attention 的层级组合，并报告长序列设置下的训练与评测结果。其结论受层比例、模型、数据和上下文设置限制。
3. **基座到推理后训练（M1）**：论文把大规模强化学习和 CISPO 用于推理模型训练，适合与其它 RL 后训练方案对比其重要性权重裁剪与优化稳定性。
4. **推理到工具任务（M2/M2.5）**：训练对象扩展到代码与 Agent 任务。论文报告的 SWE-Bench Verified 结果应结合任务版本、执行环境、采样与修复预算阅读；托管服务价格不作为模型能力证据。
5. **Agent 到多模态与自改进研究（M2.7/M3）**：后续公开材料提出递归自我改进和多模态 Agent 方向。应区分已公开论文/模型报告中的机制与产品路线表述，不能把研究设想直接写成已验证能力。

这条组织方式提示读者分别追问：新增的计算结构解决什么约束，训练目标改变了什么行为，评测是否覆盖了真实的闭环任务。跨代共用组件本身不能证明它导致了后续能力变化。

---

## 7. 关键创新点（特别突出线性注意力的贡献）

### 7.1 Lightning Attention 的工程突破

MiniMax-01 的设计重点是把因果线性注意力组织成适合 GPU 并行的计算路径，并与 Softmax Attention 混合。应从论文中的算法、内核和模型实验分别理解其贡献：

1. **算法层 cumsum 消除**：tiling + intra/inter 双路径让因果线性注意力既保留了 O(nd²) 的理论复杂度，又获得了 GPU 友好的并行度，**精确等价于完整线性注意力，而非近似**。
2. **系统层 IO-aware kernel**：Triton 实现 + on-chip SRAM 滚动 KV，使前向/反向都接近 FlashAttention 级常数项，但在长序列下时间近似线性增长（"Various Lengths, Constant Speed"）。
3. **混合架构（Hybrid Lightning + Softmax）**：论文将大部分注意力层设为 Lightning、保留一部分 Softmax 层，并在 MiniMax-01 的模型和训练设置中与纯 Softmax 基线比较。该消融支持这一配置在论文条件下的可行性，不意味着该层比例是普遍最优，也不单独证明线性注意力在所有长上下文任务上优于全注意力。

### 7.2 长上下文能力与机制

MiniMax-01 报告了长上下文训练和推理设置，并研究混合注意力如何支撑长序列建模。上下文窗口是模型配置，不等同于长上下文任务中的有效检索能力；其对后续 M1/M2 的作用需要由各自论文的实验确认，不能仅凭系列时间线推断。

### 7.3 多模态多产品同基座

公开资料分别描述了文本、视觉、语音、音乐和视频模型的架构。各条路线可以比较其 token 表示、自回归建模与 Flow Matching 解码的组合，但“共用一套基座/训练栈”需要逐篇核对，不能从同一公司或模型系列名称推断。

### 7.4 语音（TTS / 声纹克隆）的差异化

MiniMax-Speech 的论文可作为 Speaker Encoder 与 Flow-VAE 组合的案例。其主观听感结果应按论文的听测样本、评价协议和对照版本理解；这里不据此给跨服务商做普遍排名。

### 7.5 RL 算法（CISPO）

CISPO 的关键设计是裁剪重要性采样权重，而非直接裁剪 token 级策略更新；M1 论文据此讨论长链策略优化中的更新稳定性。具体收益需结合论文的训练预算、奖励与基准结果阅读，训练费用不作为方法结论。

---

## 8. 仍待回答的问题

1. **混合注意力的适用条件**：在什么上下文长度、检索任务与硬件下，Lightning/线性层和 Softmax 层的比例能兼顾状态压缩与精确召回？MiniMax-01 的消融给出一个具体模型设置，尚需其它任务与系统条件的对照。
2. **训练机制能否解释能力变化**：CISPO、RL 环境规模和工具轨迹同时变化时，哪些因素分别改善代码任务与 Agent 闭环？需看消融是否固定模型、数据、采样和执行环境。
3. **基准成绩如何转成真实工作流能力**：SWE-Bench 类任务的通过判据、补丁测试和预算，与浏览器、终端或多模态工作流不同，不能合并成一个 Agent 能力分数。
4. **多模态系统的共享边界**：不同模态模型共享 tokenization、主干或训练栈的程度各异；需要由对应论文或配置说明，不能由产品家族关系推断统一模型。
5. **RSI 的证据要求**：模型生成数据并参与评估还不等于自我改进成立；需要独立验证器、固定评测集和可重复的跨轮次增益，排除数据污染与评价器自偏。

---

## 9. 参考文献

### 核心论文

1. MiniMax et al. *MiniMax-01: Scaling Foundation Models with Lightning Attention*. arXiv:2501.08313, 2025-01-14. <https://arxiv.org/abs/2501.08313>
2. MiniMax et al. *MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention*. arXiv:2506.13585, 2025-06-16. <https://arxiv.org/abs/2506.13585>
3. Z. Qin, W. Sun, D. Li, X. Shen, W. Sun, Y. Zhong. *Various Lengths, Constant Speed: Efficient Language Modeling with Lightning Attention*. ICML 2024 / arXiv:2405.17381. <https://arxiv.org/abs/2405.17381>
4. MiniMax. *MiniMax-Speech: Intrinsic Zero-Shot Text-to-Speech with a Learnable Speaker Encoder*. arXiv:2505.07916, 2025-05-12. <https://arxiv.org/abs/2505.07916>

### 官方仓库与权重

5. MiniMax-AI. *MiniMax-01* GitHub Repository. <https://github.com/MiniMax-AI/MiniMax-01>
6. MiniMax-AI. *MiniMax-M1* GitHub Repository. <https://github.com/MiniMax-AI/MiniMax-M1>
7. MiniMax-AI. *MiniMax-M2* GitHub Repository. <https://github.com/MiniMax-AI/MiniMax-M2>
8. Hugging Face. *MiniMaxAI/MiniMax-Text-01*. <https://huggingface.co/MiniMaxAI/MiniMax-Text-01>
9. Hugging Face. *MiniMaxAI/MiniMax-VL-01*. <https://huggingface.co/MiniMaxAI/MiniMax-VL-01>
10. Hugging Face. *MiniMaxAI/MiniMax-M1-40k / MiniMax-M1-80k*. <https://huggingface.co/MiniMaxAI>

### 官方博客与发布

11. MiniMax. *MiniMax-01 is Now Open-Source: Scaling Lightning Attention for the Era of Foundation Models*. <https://www.minimax.io/news/minimax-01-series-2>
12. MiniMax. *The General Large Language Model abab6.5 Series*. <https://www.minimax.io/news/abab65-series>
13. MiniMax. *Speech-02-series: The Next Leap in Text-to-Audio and AI Voice Cloning*. <https://www.minimax.io/news/speech-02-series>
14. MiniMax. *MiniMax-M1 Technical Seminar: Deep Dive into RL, Hybrid Attention*. <https://www.minimax.io/news/minimax-m1-technical-seminar-2>
15. MiniMax. *Hailuo AI Advances Cinematic Storytelling with T2V-01-Director and I2V-01-Director*. <https://www.minimax.io/news/01-director>
16. MiniMax 官方中文站. *MiniMax 通用大模型 abab 6.5 系列*. <https://www.minimaxi.com/news/通用大模型abab65系列>
17. MiniMax 开放平台 API 文档. <https://platform.minimax.io/docs>

### 技术解读与第三方分析

18. Neurohive. *MiniMax-01: 4M Context Length Benchmark Leader Powered by Lightning Attention*. <https://neurohive.io/en/state-of-the-art/minimax-01-4m-context-length-benchmark-leader-powered-by-lightning-attention/>
19. QED42. *MiniMax-01: Long-context and Multimodal AI Insights*. <https://www.qed42.com/insights/comprehensive-analysis-of-minimax-01-advancements-in-long-context-processing-and-multimodal-ai>
20. Yacine Mahdid. *How Minimax-01 Achieves 1M Token Context Length with Linear Attention*. <https://www.yacinemahdid.com/p/how-minimax-01-achieves-1m-token>
21. 知乎专栏. *大模型结构基础（八）：MiniMax-01 精读之 Hybrid Lightning Attention*. <https://zhuanlan.zhihu.com/p/19522287467>
22. BAAI Hub. *让百万级长文本只用 1/2700 算力——对话 MiniMax-01 架构负责人钟怡然*. <https://hub.baai.ac.cn/view/44961>
23. 知乎. *[论文速看] MiniMax-M1: CISPO-截断重要性采样权重策略优化*. <https://zhuanlan.zhihu.com/p/1922497761967858562>

### 公司与产品

24. Turing Post. *Yan Junjie and MiniMax: Inside China's AGI Startup Story*. <https://www.turingpost.com/p/minimax>
25. The Wire China. *MiniMax's Moment*. <https://www.thewirechina.com/2025/07/20/minimaxs-moment/>
26. 人民网. *海外月访问量达千万级，MiniMax 海螺 AI 加速视频生成行业发展*.
27. 财联社. *MiniMax 海螺 AI 爆火 海外国产 AI 开启出海掘金之路*. <https://www.cls.cn/detail/1833833>
28. 海螺 AI 视频. <https://hailuoai.video/>
29. Hailuo AI（海螺中文站）. <https://hailuoai.com/>
30. MiniMax Agent 入口. <https://agent.minimax.io/>

### 评测与外部基准

31. Hugging Face Papers 讨论页. *MiniMax-01: Scaling Foundation Models with Lightning Attention*. <https://huggingface.co/papers/2501.08313>

32. Hugging Face Papers. *MiniMax-M1*. <https://huggingface.co/papers/2506.13585>
33. Artificial Analysis Intelligence Benchmark Methodology. <https://artificialanalysis.ai/methodology/intelligence-benchmarking>
34. Artificial Analysis Text-to-Speech Arena. <https://artificialanalysis.ai/text-to-speech/arena>

---

> 本报告依据公开资料、官方技术报告、官方仓库 README 与第三方解读整理；基准数据均引自官方发布版本。MiniMax 系列后续可能持续迭代，最新动态请以 minimax.io / minimaxi.com 与官方 GitHub 为准。

## 新鲜度补核（截至 2026-10-23）：MiniMax M3.1 Flash

MiniMax 于 2026-10-19 发布 M3.1 Flash，官方称其为新一代 Agent / coding Flash 模型，并表示其推理稀疏性更激进。发布页报告 BankerToolBench 76.2、DeepSWE v1.1 73.7%、OSWorld V2 61.7、Agents' Last Exam 29.6 与 CyberGym 82%；官方集成指南另报 AutomationBench-AA 62.2。这些均为厂商自报结果；公开页面未提供足够的完整 harness、数据切分和复现细节，不能作为跨模型受控比较。官方发布页说明权重稍后发布，当前没有可读的 M3.1 Flash 技术报告，因而具体架构、训练配方和独立复现仍未核实。

来源与锚点：MiniMax Research，[MiniMax M3.1 Flash: Redefining Agent Performance and Cost](https://www.minimax.io/blog/minimax-m31f)，2026-10-19，正文“Stronger Capabilities Across the Board”“Coding and Software Engineering”“Computer Use”“Cybersecurity”及末段权重说明；[MiniMax M3.1 Flash GA / integration guide](https://agent.minimax.io/tools/m3.1-flash)，FAQ benchmarks 段报告 AutomationBench-AA 62.2。仅据官方发布与集成页面，不推断未公开架构细节。现有公开材料为官方发布与集成页面，未提供可用于机制分析的 M3.1 独立技术论文。
