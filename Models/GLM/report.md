# GLM 系列模型深度调研报告

> 调研对象：智谱 AI（Zhipu AI / Z.ai）与清华大学 KEG 实验室（THUDM）联合研发的 GLM/ChatGLM/CogVLM/CogVideoX/GLM-Z1/GLM-4.5 等模型家族
> 时间跨度：2021 年 CogView 至 2026 年 8 月 GLM-5.3 / GLM-5.3-Flash
> 调研日期：2026-06-05 ｜ **最近更新：2026-10-17**（增量增补 GLM-5.2 / GLM-5.3 / GLM-5.3-Flash 三个新版本，新增 §2.9、§2.10；并据官方发布记录校正 GLM-5.1 上线日期；既有结论未改动）
> 资料来源：arXiv 论文、Z.ai 官方博客与文档（z.ai / bigmodel.cn）、GitHub（THUDM、zai-org）、Hugging Face、ICLR/NeurIPS/ACL 等会议论文

---

## 一、概述

智谱 AI（前身：清华大学 KEG 实验室孵化的中国 AI 独角兽）是国内最早系统性自研基础大模型并开源的机构之一。其模型家族覆盖：

- **基座语言模型**：GLM (2021/22) → GLM-130B (2022) → ChatGLM-6B / ChatGLM2-6B / ChatGLM3-6B (2023) → GLM-4 / GLM-4-9B / GLM-4-32B-0414 (2024–2025) → GLM-4.5 / GLM-4.5-Air / GLM-4.6 / GLM-4.7 / GLM-5 (2025–2026)
- **推理（深度思考）模型**：GLM-Z1-9B/32B-0414、GLM-Z1-Rumination-32B、GLM-4.5 Thinking Mode (2025)
- **视觉语言模型 (VLM)**：CogVLM-17B (2023) → CogVLM2 / CogVLM2-Video (2024) → GLM-4V-9B (2024) → GLM-4.1V-Thinking (2025) → GLM-4.5V / GLM-4.6V / GLM-5V-Turbo (2025–2026)
- **图像生成**：CogView (NeurIPS 2021) → CogView2 (NeurIPS 2022) → CogView3 / CogView-3-Plus (2024) → CogView4 (2025)
- **视频生成**：CogVideo (2022) → CogVideoX-2B/5B (ICLR 2025)

GLM 系列的独特之处在于：早期（2021–2023）坚持自主路线 —— 采用 **Prefix LM + 自回归填空 (Autoregressive Blank Infilling)** 的混合预训练目标，与 GPT 风格 Causal LM 截然不同；从 ChatGLM2 开始逐步收敛到主流 Causal LM 范式（RoPE + RMSNorm + SwiGLU + GQA），并在 GLM-4.5 转向 MoE 与 Hybrid Reasoning 路线。本报告以"架构演进 + 关键创新"双线索梳理这一脉络。

### 1.1 时间线总览

| 时间 | 模型 | 关键特征 |
|---|---|---|
| 2021-05 | CogView | 4B 参数，Transformer + dVAE，文本→图像生成（NeurIPS 2021） |
| 2021-12 | GLM (论文 v1) | 提出"自回归填空"预训练目标；2D 位置编码；ACL 2022 |
| 2022-04 | CogView2 | 层次化生成 + Cross-modal General LM，10× 加速 |
| 2022-05 | CogVideo | 9B，首个开源大规模文生视频模型，多帧生成 |
| 2022-08 | GLM-130B | 1300 亿参数双语模型；INT4 量化首次在百亿级实现（ICLR 2023） |
| 2023-03 | ChatGLM-6B | 首个对外开源的中文对话模型，6.2B，GLM 架构 + SFT/RLHF |
| 2023-06 | ChatGLM2-6B | 切换到 GLM 混合目标 + FlashAttention + Multi-Query Attention，32K 上下文 |
| 2023-10 | ChatGLM3-6B | 3D-RoPE / MQA / Causal-only mask；支持工具调用与代码解释器 |
| 2023-11 | CogVLM-17B | "Visual Expert"机制：在每层 Attention/FFN 中并行视觉专家 |
| 2024-01 | GLM-4 (闭源旗舰) | 对标 GPT-4；GLM-4 All Tools |
| 2024-05 | CogVLM2 / GLM-4V-9B | 切换到 LLaMA3-8B 底座；图像 1344×1344；19B 总参 |
| 2024-06 | GLM-4-9B 开源 + ChatGLM 综述论文 (arXiv 2406.12793) | 10T tokens 预训练 |
| 2024-08 | CogVideoX (2B/5B) | 3D Causal VAE + Expert Transformer + Expert AdaLN |
| 2024-09 | CogView3 / CogView-3-Plus | Relay Diffusion（级联扩散），DiT 路线 |
| 2025-03 | CogView4-6B | 进一步扩展到中文原生 DiT |
| 2025-04 | GLM-4-32B-0414 + GLM-Z1-32B + GLM-Z1-Rumination-32B | 首个开源旗舰级稠密模型 + 深度思考 + 反刍模型 |
| 2025-07 | GLM-4.1V-9B-Thinking | VLM 引入 RL 训练的"Thinking"链 |
| 2025-07 | **GLM-4.5 / GLM-4.5-Air** | MoE 355B/A32B 与 106B/A12B；Hybrid Reasoning；slime RL 框架 |
| 2025-08 | GLM-4.5V | 基于 GLM-4.5-Air 的 106B MoE VLM |
| 2025-09 | GLM-4.6 | 357B MoE，200K 上下文，Agent/Coding 强化 |
| 2025-12 | GLM-4.7 | "Preserved Thinking"，专注自主编程 |
| 2025-12 | GLM-4.6V-Flash | 9B 端侧 VLM |
| 2025-12-20 | **智谱 AI 香港上市 (IPO)** | 港股主板挂牌，募资约 30 亿港元 |
| 2026-01-12 | **GLM-4.7 正式发布** | 官方正式版上线 bigmodel.cn 与 Z.ai |
| 2026-02 | **GLM-5** | 744B MoE，SWE-bench 77.8%，继续基于 slime RL 框架 |
| 2026-03-04 | **API 价格大幅上调** | 全线 API 价格上涨 30–100% |
| 2026-04 | **GLM-5V-Turbo** | 基于 GLM-5 底座的旗舰视觉模型，多模态推理增强（官方上线日 2026-04-02） |
| 2026-04-07 | **GLM-5.1** 上线 | 长程任务强化，单次任务可持续自主工作约 8 小时；官方称综合能力对齐 Claude Opus 4.6（日期取自官方发布记录，详见 §2.8 校正说明） |
| 2026-05 | **API 调用量翻倍** | 官方披露日调用量较 2025 年底翻倍 |
| 2026-06-16 | **GLM-5.2** 上线 | 1M 上下文；IndexShare 跨层复用 indexer；MIT 许可。HF 权重仓库 `createdAt` 同为该日（详见 §2.9.1） |
| 2026-08-19 | **GLM-5.3** 上线 | 与 GLM-5.2 **同一基座**，全部增益来自后训练（IndexShare + SAO + slime）；编码与网络安全能力大幅提升。详见 §2.9.2 |
| 2026-08-25 | **GLM-5.3 / 5.3-Flash 的 HF 仓库创建** | 官方称「发布两周后开放模型权重」，此前需完成安全评估与模型加固；HF 仓库 `createdAt` 为 2026-08-25（权重实际开放时点未在官方记录中单列） |
| 2026-08-26 | **GLM-5.3-Flash / FlashX** 上线 | GLM-5 系列首个**原生多模态**成员：320B 总 / 18B 激活，稀疏+线性注意力混合架构，mHC。详见 §2.9.3 |

> 注：智谱 2025 年起将海外品牌名启用 **Z.ai**，开源仓库迁至 **github.com/zai-org**（原 THUDM 仓库部分仍保留）。

---

## 二、基座语言模型演进

### 2.1 GLM（General Language Model，2021–2022）

**核心论文**：Du et al., *GLM: General Language Model Pretraining with Autoregressive Blank Infilling*, ACL 2022（arXiv:2103.10360）。

**动机**：当时主流预训练范式分为三类——自编码（BERT，擅长 NLU）、自回归（GPT，擅长生成）、Encoder-Decoder（T5/BART，擅长 Seq2Seq）。GLM 旨在用一个统一架构同时适配三类下游任务。

**核心设计**：

1. **自回归填空 (Autoregressive Blank Infilling)**：从输入序列中随机采样若干 span 用 `[MASK]` 替换，剩余部分构成 Part A（双向可见），被 mask 的 spans 拼成 Part B（自回归生成）。模型在 Part A 上做双向编码，在 Part B 上做自回归解码——这本质上是一种 **Prefix LM**（Part A 全可见 + Part B 因果可见）。
2. **2D Positional Encoding**：每个 token 用 (position1, position2) 双坐标编码 —— position1 是其在原文中的绝对位置（被 mask 的 span 共享同一个位置 id），position2 是 span 内部的相对位置。这一设计使被填充内容的长度对模型不可见（避免信息泄漏）。
3. **Span 顺序随机化**：训练时打乱 spans 的预测顺序，强迫模型学习双向依赖。
4. **多任务预训练**：短 span（句中 mask，类 BERT）+ 长 span（句尾 mask，类 GPT）联合训练，使同一参数体可在 NLU、有条件/无条件生成任务上微调。

**模型规模**：GLM-Base (110M)、GLM-Large (335M)、GLM-XL (10B)、GLM-XXL (515M+)。

**架构细节**：基于 Transformer，但相比原始 BERT 做了两点改动：(a) 重排 LayerNorm 与残差连接的顺序（Post-LN→Pre-LN 思路）；(b) 输出 token 预测使用单层线性层；(c) 用 GeLU 替换 ReLU。

### 2.2 GLM-130B（2022-08，ICLR 2023）

**核心论文**：Zeng et al., *GLM-130B: An Open Bilingual Pre-Trained Model*, ICLR 2023（arXiv:2210.02414）。

**目标**：训练一个达到 GPT-3 (davinci, 175B) 水平的双语（中英）开源百亿级模型，并公开训练日志。

**架构选择**（与 GLM-Base 相同的预训练目标，但工程上做了多项关键决定）：

| 设计点 | GLM-130B 选择 | 备注 |
|---|---|---|
| 主架构 | GLM 自回归填空（Prefix LM） | 沿用 GLM 论文 |
| 层数 / 隐藏维度 | 70 层 / 12,288 hidden / 96 heads | 130B 参数 |
| 上下文长度 | 2,048 | 当时主流 |
| 位置编码 | **RoPE (Rotary Positional Embedding)** | 已抛弃 GLM-Base 的 2D learnable PE |
| 激活函数 | **GeGLU** | GLU 家族 |
| LayerNorm | **DeepNorm**（自研） | 解决 100B 级训练发散 |
| 训练精度 | FP16 主体 + 梯度累加 FP32 | FlashAttention 之前的方案 |
| 推理量化 | **INT4**（无后训练） | 首个达到 INT4 几乎无损的 100B+ 模型，可在 4×RTX 3090 上推理 |

**训练**：在 96×A100 集群上耗时 60 天，预训练 400B tokens（200B 中文 + 200B 英文）。论文重点报告了训练稳定性（loss spike 与 divergence）的工程经验：嵌入梯度收缩 (Embedding Gradient Shrink, EGS)、混合精度策略调整、DeepNorm 替换 Pre/Post-LN 等。

**评测**：在 MMLU、LAMBADA、BIG-bench-Lite 上接近或超过 GPT-3 davinci；在中文 CLUE/FewCLUE 上显著超过 ERNIE-Titan-3.0 260B。

> **重要**：GLM-130B 是该家族**仍然采用 Prefix LM 双向+单向混合**的最后一代百亿级模型。下一代 ChatGLM 系列在工程上继续兼容 GLM 目标，但从 ChatGLM3 开始已逐步向标准 Causal LM 收敛。

### 2.3 ChatGLM-6B / ChatGLM2-6B / ChatGLM3-6B（2023）

| 维度 | ChatGLM-6B (2023.03) | ChatGLM2-6B (2023.06) | ChatGLM3-6B (2023.10) |
|---|---|---|---|
| 参数 | 6.2B（28 GLM Block） | 6.2B | 6.2B |
| 预训练目标 | **GLM 自回归填空（Prefix LM）** | GLM 混合目标，1.4T 双语 tokens | 与 ChatGLM2 类似，更大规模数据 |
| 位置编码 | RoPE | RoPE（单维改造） | RoPE |
| Attention | 标准 MHA | **Multi-Query Attention (MQA)** | MQA |
| 激活 | GeLU | **SwiGLU**（部分版本仍 GeLU；社区资料口径不一） | SwiGLU |
| LayerNorm | RMSNorm | RMSNorm | RMSNorm |
| 上下文 | 2K | **32K**（FlashAttention） | **128K**（ChatGLM3-6B-128K） |
| 对齐 | SFT + RLHF（小规模） | SFT + Human Preference Alignment | SFT + DPO 风格对齐 |
| 工具能力 | — | — | **原生 Function Call / Code Interpreter / Agent** Prompt |
| 开源 | 首发开源，引爆国内开源浪潮 | 推理速度提升 42%，KV cache 显存降至 1/8 | 兼容三种 prompt：chat、tool、code |

**关键演进**：

1. ChatGLM2 引入 **MQA**（所有 head 共享同一组 K/V，仅 Query 多头）大幅压缩 KV cache，显存占用降为 MHA 的约 1/N；为后来 GQA 在国产大模型中的普及打下工程基础。
2. ChatGLM2 启用 **FlashAttention**（v1）+ 上下文从 2K→32K。
3. ChatGLM3 重点布局**工具能力（Tools）**：模板支持 system / user / assistant / observation / tool 多角色，可被视为后续 GLM-4 All Tools 的前身。
4. 三代 ChatGLM-6B 在 Hugging Face 累计下载量在 2023 年突破千万，是中文开源生态的标志性模型。

### 2.4 GLM-4（2024）

**官方综述**：Team GLM, *ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools*, arXiv:2406.12793 (2024-06)。

**模型矩阵**：

| 模型 | 类型 | 上下文 | 备注 |
|---|---|---|---|
| GLM-4 | API 旗舰（闭源） | 128K | 对标 GPT-4 |
| GLM-4-Air | API 轻量 | 128K | 高性价比 |
| GLM-4-9B | 开源 base | 8K | 2024-06 开源 |
| GLM-4-9B-Chat | 开源 chat | 128K / 1M | 长上下文版本 |
| GLM-4V-9B | 开源 VLM | 8K | 见第三章 |

**训练规模**：GLM-4 系列预训练 **10T tokens**（中英为主，少量 24 语种），多阶段后训练（SFT + 来自人类反馈的强化学习/偏好对齐）。

**评测**（论文摘要）：
- **MMLU / GSM8K / MATH / BBH / GPQA / HumanEval**：与 GPT-4 持平或略优；
- **IFEval（指令跟随）**：接近 GPT-4-Turbo；
- **AlignBench（中文对齐）**：超过 GPT-4。

**GLM-4 All Tools**：模型自主决定何时调用 web browser / Python interpreter / Text-to-Image / 用户自定义函数，在线访问与数学求解上匹敌 GPT-4 All Tools。这是国内最早系统化 Function-Calling Agent 化的旗舰模型之一。

### 2.5 GLM-4-32B-0414 与 GLM-Z1（2025-04）

2025-04-14 智谱发布 **GLM-4-0414 系列**，将开源主线从 9B 跳到 32B，并首次系统性开源推理模型。

| 模型 | 类型 | 上下文（YaRN 扩展） | 说明 |
|---|---|---|---|
| GLM-4-32B-Base-0414 | Base | 32K → 128K | 32B 稠密底座 |
| GLM-4-32B-0414 | Chat | 32K → 128K | 通用对话/Agent |
| GLM-Z1-32B-0414 | Reasoning | 32K → 128K | "深度思考"模型 |
| GLM-Z1-Rumination-32B-0414 | Deep Research | 128K | "反刍/沉思"模型，对标 OpenAI Deep Research |
| GLM-4-9B-0414 | Chat | 32K → 128K | 轻量批量任务 |
| GLM-Z1-9B-0414 | Reasoning | 32K → 128K | 9B 推理"惊喜版" |

特性：
- **YaRN RoPE Scaling**：当输入 + 输出超过 32K 时启用 `factor=4.0` 的 YaRN，扩展到 128K；
- **GLM-4-32B-0414 函数调用 / Agent**：在 BFCL-v3 (69.6)、TAU-Bench Retail (68.7)、Airline (51.2)、IFEval (87.6) 等指标上反超 DeepSeek-V3-0324 与 GPT-4o-1120；
- **SWE-bench Verified**：搭配 Moatless 框架达到 33.8（同等规模开源 SOTA）；
- 推理速度（在线）最高达 **200 tokens/s**。

详见第五章"推理模型"。

### 2.6 GLM-4.5 / GLM-4.5-Air（2025-07）—— MoE 与 Hybrid Reasoning

**核心论文**：*GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models*, arXiv:2508.06471 (2025-08)。

**架构关键参数**：

| 模型 | 总参数 | 激活参数 | 上下文 | 最大输出 |
|---|---|---|---|---|
| GLM-4.5 | 355B | 32B | 128K | 96K |
| GLM-4.5-Air | 106B | 12B | 128K | 96K |
| GLM-4.5-X / AirX / Flash | API 变体（速度/价格不同档） | — | 128K | 96K |

**架构设计要点**（与 DeepSeek-MoE 同源、有所改造）：
1. **Mixture-of-Experts**：每层多个 FFN 专家，每 token 动态路由到 Top-K；
2. **Loss-free Balance Routing**：替代经典的 auxiliary load-balancing loss，避免对主任务 loss 的负面干扰；
3. **Sigmoid 路由 + 共享专家**（部分细节与 DeepSeek 相似）；
4. **Hybrid Reasoning**：模型同时支持 Thinking Mode（带显式 reasoning_content）与 Non-Thinking Mode，通过 API 参数 `thinking.type = enabled / disabled` 切换；
5. **训练管线**：15T tokens 通用预训练 → 代码/推理/Agent 任务定向后训练 → RL（slime 框架）增强；技术报告中的总训练 token 数为 **23T**（含后训练 RL rollout）。

**slime（强化学习框架）**：智谱自研、开源（github.com/THUDM/slime），是 GLM-4.5/4.6/4.7/5/5.1 系列共同的 RL 后训练基础设施。核心特性：
- **Hybrid 同步/异步训练架构**：支持 sync 与 fully-asynchronous decoupled rollouts；
- 把 RL rollout 视为"在线数据集生成器"，rollout 与 trainer 解耦扩缩容；
- 支持百亿级 MoE 的大规模 RL。

**性能**（来自官方与第三方报告）：
- 在 **MMLU Pro / AIME24 / MATH 500 / SciCode / GPQA / HLE / LiveCodeBench / SWE-Bench Verified / Terminal-bench / TAU-Bench / BFCL-v3 / BrowseComp** 12 项基准的综合平均分，**全球排名第 2、开源第 1**；
- GLM-4.5-Air（106B/A12B）在多项推理基准上**超越 Gemini 2.5 Flash、Qwen3-235B、Claude 4 Opus**；
- API 价格：输入 \$0.2 / M tokens、输出 \$1.1 / M tokens；高速版生成速度 100+ tokens/s。

### 2.7 GLM-4.6（2025-09）

**架构**：MoE，**357B 总参 / 32B 激活**（与 GLM-4.5 同代但参数微调），**上下文 200K**（GLM-4.5 为 128K），最大输出 131K。

**重点改进**（来自 Hugging Face zai-org/GLM-4.6 与第三方评测）：
- 推理性能显著提升，并支持**推理过程中调用工具**（thinking + tool use 交错）；
- Coding（特别是 Agentic Coding）相对 GLM-4.5 大幅提升；
- 在 8 项公开 Agent / Reasoning / Coding 基准上系统性优于 GLM-4.5；
- 与 Claude Sonnet 4.5 在编码与推理上"近平价"，但成本显著更低。

### 2.8 GLM-4.7 与 GLM-5（2025-12 起）

- **GLM-4.7**（2025-12 预览，2026-01-12 正式发布）：定位**自主编程**，引入 *Preserved Thinking* —— 在多轮工具调用之间保留思考链，避免 reasoning 被截断；在 SWE-bench 等编程基准上较 GLM-4.6 进一步提升；
- **GLM-5**（2026-02）：智谱新一代旗舰基座模型，**744B MoE / 40B 激活**（官方技术博客确认），继续基于 slime RL 框架训练。关键指标：
  - **SWE-bench Verified 77.8%**（开源模型最高水准之一）；
  - 在 MMLU Pro、AIME 2025、GPQA、LiveCodeBench 等 12 项综合基准上保持全球前 3；
  - 上下文 200K，最大输出 131K；
  - API 价格随 2026-03 调价上涨，但性价比仍优于同性能闭源竞品；
- **GLM-5.1**（**2026-04-07 上线**，本轮据官方发布记录校正）：GLM-5 的迭代版本，强化 Agent 与长程任务能力。官方口径：单次任务可持续自主工作约 **8 小时**；综合与 Coding 能力**整体对齐 Claude Opus 4.6**。带条件数字见 §2.9.0。
- **GLM-5V-Turbo**（2026-04）：基于 GLM-5 底座的旗舰视觉语言模型，继承 GLM-4.5V/4.6V 的 Encoder + Projector + LLM 架构，在多模态推理与长视频理解上进一步突破。技术报告见 arXiv:2604.26752（v3 2026-05-12）。

> **校正说明（本轮）**：原文写作「GLM-5.1（2026 初）」。智谱官方发布记录给出 **GLM-5.1 上线日期为 2026-04-07**（`docs.bigmodel.cn/cn/update/new-releases`），HuggingFace 仓库 `zai-org/GLM-5.1` 的 `createdAt` 为 2026-04-03。此处以官方发布记录为准。同理，GLM-4.7 官方记录为 **2025-12-22 上线**（原文记「2026-01-12 正式发布」，两者可能分别指 API 上线与正式版发布，本轮**不改原文**，仅在此标注口径差异）。

### 2.9 GLM-5.2 / GLM-5.3 / GLM-5.3-Flash（2026-06 起）

> **证据等级：精读原文（HuggingFace 官方模型卡 + 智谱官方文档原文 + 官方发布记录）**。z.ai / docs.z.ai 在本环境 **TLS 不可达**（`web_fetch` 与 `curl` 均失败），因此本节全部数字改用 **HF 官方模型卡**与 **docs.bigmodel.cn 官方文档**核验，均为**厂商自报**；依赖 z.ai 博客原文的项一律标注「核验受限」。

#### 2.9.0 GLM-5.1 的带条件数字（为 §2.9 的对照基线）

来源：[HF 模型卡 `zai-org/GLM-5.1`](https://huggingface.co/zai-org/GLM-5.1)（MIT 许可）。官方自报，同表内 9 个模型同条件对照：

| 基准 | GLM-5.1 | GLM-5 | Claude Opus 4.6 | Gemini 3.1 Pro | 条件/说明 |
| --- | --- | --- | --- | --- | --- |
| SWE-Bench Pro | **58.4** | 55.1 | 57.3 | 54.2 | 官方称「刷新全球最佳表现」 |
| NL2Repo | 42.7 | 35.9 | **49.8** | 33.4 | 仓库生成 |
| Terminal-Bench 2.0 (Terminus-2) | 63.5 | 56.2 | 65.4 | **68.5** | 同 harness |
| CyberGym | **68.7** | 48.3 | 66.6 | 38.8 | 漏洞发现 |
| BrowseComp（带上下文管理） | 79.3 | 75.9 | 84.0 | **85.9** | 两个口径分列（无/有上下文管理） |
| τ³-Bench | 70.6 | 69.2 | 72.4 | 67.1 | 工具/agent 场景 |

另（官方 docs 表述，带条件）：**KernelBench Level 3** 上经千轮工具调用优化真实 ML 负载，实现 **3.6× 几何平均加速**，对比 `torch.compile` max-autotune 的 **1.49×**；典型案例中 8 小时内从零构建完整 Linux 桌面系统、或在向量数据库上完成 655 轮迭代把查询吞吐提到初始正式版的 **6.9×**。这些是**官方选取的案例**，不是基准分布。

#### 2.9.1 GLM-5.2（2026-06-16 上线并开源）

**发布信息**

- **日期**：官方发布记录 **2026-06-16**；HuggingFace 仓库 `zai-org/GLM-5.2` 的 `createdAt` 同为 **2026-06-16**（两条一手源互证）。
- **形态**：**开源权重，MIT 许可**（模型卡 `license: mit`，官方称「Pure Open — no regional limits, technical access without borders」）。前代 GLM-5.1 的模型卡同为 `license: mit`；**MIT 状态维持到 GLM-5.2 为止，GLM-5.3 起改为自定义许可**（见 §2.9.2）。
- **上下文**：**1M tokens**（官方称「solid 1M context」）；文档口径最大输出 128K。
- **与前代的定位差**：从 GLM-5.1 的「200K + 8 小时长程」推到「**1M + 项目级工程上下文**」。

**新增架构：IndexShare（跨层复用稀疏注意力索引）**

- 官方模型卡表述：提出 **IndexShare**，**在每 4 层稀疏注意力之间复用同一个 indexer**，在 1M 上下文下把**每 token FLOPs 降低 2.9×**。
- 模型卡把 IndexShare 链接到 **arXiv:2603.12201**，该论文题目为 *IndexCache: Accelerating Sparse Attention via Cross-Layer Index Reuse*（v1 2026-03-12）。论文侧的数字与模型卡不同口径，须并列记录：**在 30B DSA 模型上移除 75% 的 indexer 计算**、质量退化可忽略，**prefill 1.82× / decode 1.48× 加速**（相对标准 DSA），并在**生产级 GLM-5** 上做了初步验证。→ 引用时务必区分「论文的 30B 实验数字」与「GLM-5.2 模型卡的 1M 上下文 2.9× FLOPs」。
- 另一项改动：改进 **MTP（multi-token prediction）层**用于投机解码，**接受长度提升最多 20%**。

**能力与基准（官方模型卡，全表 8 模型同条件）**

| 基准 | **GLM-5.2** | GLM-5.1 | DeepSeek-V4-Pro | Claude Opus 4.8 | GPT-5.5 | Gemini 3.1 Pro | 条件（官方脚注要点） |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HLE | 40.5 | 31 | 37.7 | 49.8\* | 41.4\* | 45 | temp 1.0 / top_p 0.95，最大生成 163,840；默认 text-only 子集，\* 为全量集 |
| HLE (w/ Tools) | 54.7 | 52.3 | 48.2 | 57.9\* | 52.2\* | 51.4\* | 最大上下文 300K，**不做上下文管理** |
| GPQA-Diamond | 91.2 | 86.2 | 90.1 | 93.6 | 93.6 | 94.3 | 同上采样参数 |
| SWE-bench Pro | 62.1 | 58.4 | 55.4 | 69.2 | 58.6 | 54.2 | OpenHands；temp 1 / top_p 1 / max_new 32k / **400K 上下文** |
| NL2Repo | 48.9 | 42.7 | 35.5 | 69.7 | 50.7 | 33.4 | temp 1.0 / top_p 1.0 / max_new 48k / 400K 上下文 + 反作弊（规则 + LLM 判定） |
| DeepSWE | 46.2 | 18 | 8 | 58 | 70 | 10 | 官方 pier 框架 + **mini-swe-agent**；temp 1.0 / top_p 1.0 / timeout 2h / **400K 上下文**；每任务隔离容器 2 CPU / 8GB / 无网 |
| ProgramBench | 63.7 | 50.9 | 47.8 | 71.9 | 70.8 | 39.5 | Claude-Code 2.1.156；max_tokens 64k / max_turns 2000 / sample_timeout 6h / reasoning_effort=max / 400K 上下文 |
| Terminal Bench 2.1 (Terminus-2) | 81.0 | 63.5 | 64 | 85 | 84 | 74 | Terminus-2：parser=json / timeout 4h / max_new 48k / max_episodes 500 / **256K 上下文** |
| Terminal Bench 2.1 (Best Harness) | 82.7 | 69 | — | 78.9 | 83.4 | 70.7 | Claude Code 2.1.167；max_new_tokens 131,072、5 次平均、取消 wall-clock 限制 |
| FrontierSWE (Dominance) | 74.4 | 30.5 | 29.0 | 75.1 | 72.6 | 39.6 | **第三方 Proximal 评测**，1M 上下文 / max effort / 128K 输出，**分数截至 2026-06-16** |
| PostTrainBench | 34.3 | 20.1 | — | 37.2 | 28.4 | 21.6 | **第三方 PostTrainBench 评测**，1M 上下文 / max effort / 128K 输出 |
| SWE-Marathon | 13.0 | 1.0 | — | 26.0 | 12.0 | 4.0 | **第三方 Abundant AI 评测**，同 1M/max/128K 设定 |
| MCP-Atlas (Public Set) | 76.8 | 71.8 | 73.6 | 77.8 | 75.3 | 69.2 | 500 任务公开子集，think 模式，每任务 10 分钟超时，**Gemini-3.0-Pro 作裁判** |
| Tool-Decathlon | 48.2 | 40.7 | 52.8 | 59.9 | 55.6 | 48.8 | 官方评测服务，max_token 128K |

**与前代的可判定差异（GLM-5.1 → GLM-5.2）**

1. **上下文 200K → 1M**，且官方文档给了「累计处理 **>85 万 tokens**、接近用满 1M 窗口」的实际案例（一次连续长程任务完成 Web/移动端/小程序交付）——这是**上下文能力的可用性证据**，不是基准分数。
2. **DeepSWE 18 → 46.2、FrontierSWE 30.5 → 74.4、SWE-Marathon 1.0 → 13.0、PostTrainBench 20.1 → 34.3**：官方表内同条件对照，可判定。
3. **effort 可调**：官方称提供**多档 thinking effort**以平衡性能与延迟（GLM-5.3 起进一步固化为 `low/high/max`）。
4. **许可**：旗舰线维持 **MIT**（GLM-5.3 起改自定义许可，是该系列的一次转向）。

**失效边界**

- **仍落后最强闭源**：SWE-Marathon 13.0 vs Claude Opus 4.8 的 26.0；NL2Repo 48.9 vs 69.7；Terminal Bench 2.1 81.0 vs 85。
- **部分指标靠第三方评测**：FrontierSWE / PostTrainBench / SWE-Marathon 三行明确写「evaluation was conducted by …」，其口径（1M 上下文 / max effort / 128K 输出）与官方自跑项**不同**，不能与其他行混算平均。
- **IndexShare 的收益是分层的**：模型卡的 **2.9× FLOPs（1M）** 与论文的 **75% indexer 计算移除 / 1.82× prefill（30B）** 是**不同模型、不同口径**的两个结论，互相不能替代。
- **核验受限**：官方 `z.ai/blog/glm-5.2` 原文本环境不可达，模型卡中「Check out the GLM-5.2 blog」的链接目标内容未直读；模型卡内的 `bench_52.png`（另一张基准图）为图片，未做 OCR 取值。

#### 2.9.2 GLM-5.3（2026-08-19 上线 / 2026-08-25 权重）

**发布信息**

- **日期**：官方发布记录 **2026-08-19**（「GLM-5.3 新一代旗舰模型上线」）；HuggingFace 仓库 `zai-org/GLM-5.3` 的 `createdAt` 为 **2026-08-25**，与官方「发布两周后开放模型权重（此前完成安全评估与模型加固）」的表述一致。
- **形态**：开源权重，但许可**不再是 MIT**——模型卡 `license: other` / `license_name: glm-5.3`（自定义许可）。对比：同期的 GLM-5.3-Flash 是 **MIT**。
- **上下文**：官方文档 **1M 上下文窗口，最大输出 128K**；仅支持文本模态。
- **思考模式**：**始终启用**，`reasoning_effort` 三档 `low/high/max`（默认 `max`）；**不再支持禁用思考**。迁移提示（官方原文）：若应用原先用 `thinking.type: "disabled"`，必须先改为 `enabled` 并把 `reasoning_effort` 设为 `low`，否则请求失败。

**最关键的一条：与 GLM-5.2 同一基座，全部增益来自后训练**

官方中英文口径一致——「GLM-5.3 uses the same base model as GLM-5.2 — every gain comes from post-training」。相对 GLM-5.2 的后训练改动是：**更大的任务环境规模化**（数十倍的长程任务环境、更多环境类型、更长后训练时间）、**IndexShare + SAO（结合上下文压缩）+ 持续演进的新一代 Slime 框架**。

- **任务环境规模化（官方描述，可迁移的方法论）**：训练任务不再是「编程题」，而是**接近专家真实工作单元的完整环境**（例如给模型计算集群、存储、内部文档、代码库与实验结果，要求定位训练栈瓶颈、实施优化、跑实验、在保证正确性前提下拿到可量化端到端加速）。难点从模型转移到**环境**：环境必须可执行、可验证、贴近真实工作。为此他们建了**端到端合成任务环境**的流水线，并为部分任务**自动生成 RL 奖励信号**；验证器在**不访问参考解法**的前提下生成，并用求解轨迹识别、消除 reward shortcut；**只有同时通过 Oracle / 空操作 / 未解决状态三类检查的验证器**，其二值奖励才允许用于训练。

**能力与基准（官方模型卡，全表 9 模型同条件）**

| 基准 | **GLM-5.3** | GLM-5.2 | Kimi K3 | Claude Opus 4.8 | Claude Fable 5 (w/ fallback) | GPT-5.6 Sol | 条件（官方脚注要点） |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Terminal Bench 2.1 | 88.2 | 81.0 | 88.3 | 85.0 | 88.0 | **88.8** | Claude Code 2.1.207；temp 1.0 / top_p 1 / max_new 65,536；**6h 超时** |
| Terminal Bench 3.0 | 28.3 | 4.6 | 17.4 | 21.1 | 33.7 | **34.6** | Claude Code 2.1.207，max effort，**400K 上下文 / 128K 输出**，**avg@3**；每 rollout 独立容器、600 agent turns、10h 超时；关闭 Tool Search，由任务官方 verifier 打分 |
| DeepSWE (v1.1) | 66.9 | 46.2 | 67.5 | 58.0 | 69.7 | **72.7** | mini-swe-agent；temp 0.95 / top_p 1.0 / timeout **6h** / 400K 上下文 |
| NL2Repo | 58.0 | 48.9 | 58.0 | **69.7** | — | — | temp 1.0 / top_p 1.0 / max_new 64k / **1M 上下文** + 反作弊 |
| ProgramBench (Almost Solved) | 19.0 | 9.5 | 17.5 | 15.5 | **33.0** | 23.0 | 「Almost Solved」子集口径（与 GLM-5.2 卡的 63.7 不是同一个指标） |
| FrontierSWE | 78.1 | 67.5 | — | 66.5 | **88.2** | — | 第三方 Proximal，1M / max effort / 128K 输出，**分数截至 2026-08-14** |
| SWE-Marathon (v1.1) | 42.5 | 19.4 | 48.1 | **48.8** | 33.1 | 42.5 | Claude Code 2.1.207，1M 上下文 / 128K 输出；官方说明修改了 2 处过严反作弊/镜像构建问题 |
| PostTrainBench | 39.8 | 31.7 | 32.0 | 32.9 | **41.8** | 36.2 | Claude Code 2.1.207，1M 上下文，3 次加权平均；失败运行回落到官方 zero-shot 基线分 |
| CyberGym | **84.5** | 77.2 | 80.0 | 78.1 | 83.8 | 83.6 | Claude Code 2.1.207，max effort，**无 web 工具**，temp 1.0 / top_p 1.0 / max_new 128,000；**不限超时**，1,507 任务单次 pass@1；agent 置于任务容器内，**移除全部 Git 信息 + 域名白名单**防作弊 |
| ExploitGym (2h / 6h) | 105 / 130 | 29 / 39 | 36 / 70 | 80 / 120 | 181 / 247 | **216 / 293** | 869 任务单次 pass@1；**按各模型 TPS 折算 API 推理时间**（GLM-5.3 115 TPS / K3 40 TPS / Qwen3.8 Max 47 TPS）+ 非 API 开销 |
| ExploitBench | 54.4 | 24.4 | 32.2 | 40.0 | **78.0** | 76.5 | 41 任务 3 轮，最多 300 轮交互，取覆盖能力并集后平均 |
| Toolathlon Verified | 73.0 | 59.9 | **76.5** | 76.2 | 74.7 | 74.9 | 官方评测服务，pass@1 三次平均 |
| AutomationBench (v1.0.6) | **48.2** | 26.2 | 46.7 | 41.0 | 46.2 | 45.8 | v1.0.6（含修复 `null` 类型处理的 PR #13） |
| Agents' Last Exam (ALE-CLI) | 28.5 | 23.8 | 27.6 | 25.7 | 23.8 | **28.6** | 官方协议，Claude Code harness，max effort，**1M 上下文 / 64K 输出**；105 任务，隔离 Docker，默认 4h 超时（个别最长 8h），关闭 Tool Search |
| HLE w/ Tools | 62.5 | 54.7 | 59.8 | 57.9 | 63.9 | **64.5** | temp 1.0 / top_p 0.95，最大生成 163,840；**300K 上下文 + 上下文管理策略**；裁判 GPT-5.6-luna (medium) |
| GDPval-AA v2 (Elo) | **1769** | 1508 | 1682 | 1588 | 1743 | 1730 | **由 Artificial Analysis 评测**（非厂商自跑） |

**与 GLM-5.2 的可判定差异（同基座、纯后训练，因此归因最干净）**

因为**基座相同**，这一组对比是本次更新里**归因最干净的 A/B**——同一基座、同一 harness、同一采样参数，差异只来自后训练：

1. **Terminal Bench 3.0：4.6 → 28.3**（+23.7 分，约 6 倍）。这是本轮最大的单点跃迁。
2. **DeepSWE v1.1：46.2 → 66.9**；**ALE-CLI：23.8 → 28.5**（官方文档另给 23.8→28.5，模型卡同）。
3. **网络安全能力是「涌现」而非定向优化**（官方原话承认「我们原本预计……令人意外的是，随着训练规模持续扩大，这项能力也迅速演进」）：CyberGym **77.2 → 84.5**（官方称该基准当前最佳，超过 Mythos 5 的 83.8 与 GPT-5.6 Sol 的 83.6）；ExploitBench **24.4 → 54.4**（翻倍以上）；ExploitGym 2h/6h **29/39 → 105/130**。官方给出的规律：**漏洞利用链越往深处，相对 GLM-5.2 的提升越大，同时与闭源前沿的差距也越大**。
4. **真实场景侧证**：官方称自 GLM-5.2 起与中国多家安全团队合作，在 **269 个项目**中发现 **2,436 个漏洞**（其中 **1,097 个中高危**），涵盖内核、操作系统、浏览器引擎、开源基础设施、Web 应用与网络协议；存在时间最长的漏洞在代码库中约 **40 年**。
5. **Token 效率同时改善**（官方内部 Z.ai Code Bench）：Max 档准确率 **34.5%**（GLM-5.2 为 **23.4%**），而每任务平均输出约 **7.5 万** token（GLM-5.2 约 **9.6 万**）——**分更高、token 更少**。

**失效边界**

- **编程之外不一定同向**：官方自己给的对照中说，Max 档准确率 34.5% **仍低于 Claude Fable 5 的 39.5%**；ExploitBench 54.4% 远低于 Mythos 5 的 78.0% 与 GPT-5.6 Sol 的 76.5%。
- **部分基准的「提升」口径要小心**：GLM-5.2 卡里的 ProgramBench 是 **63.7**，GLM-5.3 卡里的 ProgramBench 是「**Almost Solved** 19.0」——**不是同一子集/指标**，两者不能相减。
- **`license_name: glm-5.3` 是自定义许可**，条款未逐条核验 → 不能默认等同 MIT 使用范围（见 §2.10）。
- **代码安全能力的双面性（官方自述）**：官方在 GLM-5.3 中文稿中说明开源权重前需「完成必要的安全加固，尽可能限制其潜在攻击能力，保留其防御价值」——这意味着**发布版与内部版在攻击性上存在人为差异**，复现「未加固」表现不可行。
- **核验受限**：`z.ai/blog/glm-5.3` 原文本环境不可达；官方中文研究页（`zhipuai.cn/zh/research/161`）可读，作为中文侧补充源。

#### 2.9.3 GLM-5.3-Flash / FlashX（2026-08-26 上线）：GLM-5 系列首个原生多模态

**发布信息**

- **日期**：官方发布记录 **2026-08-26**（「GLM-5.3-Flash 原生多模态模型上线」）；HuggingFace 仓库 `createdAt` 为 **2026-08-25**。
- **形态**：**开源权重，MIT 许可**（模型卡 `license: mit`）；**原生多模态**（输入 视频 / 图像 / 文本 / 文件；输出文本）——GLM-5 系列第一个原生多模态成员。
- **规模**：**320B 总参数 / 18B 激活参数**。
- **上下文**：**1M**；最大输出 **128K**。
- **推理档位**：`reasoning_effort` `low/high/max`（默认 `max`），`thinking.type` **仅支持 enabled**。
- **Flash vs FlashX**：`glm-5.3-flash` / `glm-5.3-flashx` 两个模型 ID；**FlashX 推理速度 200 tokens/s**（官方文档）。Coding Plan 当前**未开放 FlashX**。

**关键架构变化（与前两代不是同一基座）**

官方模型卡明确：GLM-5.3-Flash **starts from a newly trained base model**（新训基座），架构与训练配方围绕能力与效率重设计。三项：

1. **稀疏注意力 + 线性注意力的混合架构**——官方称是「**首个采用该混合架构的开源前沿模型**」；相比 GLM-5.3，**注意力计算量降低 3.01×、KV cache 降低 4.44×**。
2. **mHC（Manifold-Constrained Hyper-Connections）**——用于进一步提升 scaling 效率。
3. **30T token 多模态预训练语料**。

> ⚠️ 与 GLM-5.3 的关系要说清：**GLM-5.3 是「同一基座 + 后训练」；GLM-5.3-Flash 是「新基座 + 新架构」**。两者只共享「后训练方法论（SAO / slime / 任务环境规模化）」与命名，**不是同一模型的蒸馏版**。

**能力与基准**

官方文档给出的带条件数字/表述：

- **Artificial Analysis Intelligence Index：57 分**，**超过 GLM-5.2**，与 **Claude Opus 4.8 持平**（官方自报，非第三方直读）。
- **Z.ai Code Bench**：编程表现与 **Claude Opus 4.8 相当**（官方自报，非公开基准）。
- **价格**：**GLM-5.3 的 1/10**（限时折扣内 **1/20**；为 Opus 4.8 的 **1/40**）——这是官方主打的性价比论点。
- 官方还宣称拓展到 Office 文档与金融研究工作流，可交付 PPTX / PDF / DOCX / XLSX。

**失效边界**

- **基准表是图片**：模型卡只嵌了 `bench_53.png`，**未提供可解析的基准表**；官方文档也只给「AA II 57 / Z.ai Code Bench 与 Opus 4.8 相当」这类表述。因此本条目**不列 GLM-5.3-Flash 的逐项基准数字**——图片未做 OCR 取值，属**核验受限**。
- **「与 Opus 4.8 持平」是官方口径**，且是在 **AA Index（单一综合分）** 上的持平，不等于逐任务持平。
- **原生多模态的评测覆盖未知**：文档只提到视觉 coding 与 Office/金融场景，**未见多模态基准的逐项分数**。
- **FlashX 的 200 tokens/s** 是官方给出的推理速度，**未说明测量条件**（batch / 硬件 / 上下文长度 / 输出长度），不可直接与别家吞吐对比。

### 2.10 未确证与待跟踪（2026-06 以来）

以下条目**未进入正文**，仅登记待核：

| 事项 | 现状 | 处置 |
| --- | --- | --- |
| GLM-5.3 的自定义许可 `glm-5.3` 条款 | HF 仅标 `license: other` / `license_name: glm-5.3` | 待读 LICENSE 原文；在读到前不称「可商用等同于 MIT」 |
| z.ai 官方博客原文（glm-5.2 / glm-5.3 / glm-5.3-flash） | 本环境 TLS 不可达（`web_fetch` + `curl` 均失败） | 数字改用 HF 模型卡与 bigmodel 官方文档核验；博客原话未逐字核对 |
| GLM-5.2 / 5.3 的精确总参/激活参 | 官方文档与模型卡**均未给** GLM-5.2、GLM-5.3 的参数量 | 不沿用此前「744B/40B 属 GLM-5」以外的推测；待官方披露 |
| GLM-5.3-Flash 的逐项基准 | 模型卡只有 `bench_53.png` 图片 | 待从可解析来源取得后再入表 |
| GLM-5.3-Flash 的 mHC 细节 | 官方只给名称与「提升 scaling 效率」 | 是否有独立技术报告待跟踪（检索到 `Manifold-Constrained Hyper-Connections` 方向的论文，但未确认与 GLM 实现的对应关系） |
| GLM-5.3-FlashX 的 200 tokens/s | 无测量条件 | 待官方补 benchmark 口径 |
| GLM-OCR / GLM-Image / GLM-TTS / GLM-5-Turbo | 分别于 2026-02-03 / 2026-01-14 / 2025-12 / 2026-03-15 上线，**早于本轮「2026-06 起」窗口**，且本条目此前未覆盖 | 本轮不补写（避免超出「增量补充 2026-06 起」的范围）；若协调者要求扩容再另立一段 |
| 智谱「IndexShare」与论文「IndexCache」的命名对应 | 模型卡用 IndexShare，链接指向 arXiv:2603.12201 *IndexCache* | 正文已并列标注两种名称与各自数字口径；名称是否等价未获官方文字确认 |

---

## 三、视觉语言模型 (VLM) 演进

### 3.1 CogVLM（2023-11）—— Visual Expert 机制

**核心论文**：Wang et al., *CogVLM: Visual Expert for Pretrained Language Models*, NeurIPS 2024（arXiv:2311.03079）。

**核心动机**：当时主流多模态范式（BLIP-2、LLaVA、MiniGPT-4）多采用 **shallow alignment**——把图像特征通过 Q-Former / 简单 MLP 投到 LLM 的输入 embedding 空间，LLM 主体冻结。CogVLM 团队认为这种"浅对齐"会损害视觉细节（OCR、grounding、细粒度物体）。

**架构**（CogVLM-17B = ViT 4.4B + LLM 7B + Visual Expert ~5B）：

```
                ┌─────────────────────────────┐
                │      ViT (EVA-CLIP-E/14)    │
                └──────────────┬──────────────┘
                               │ patch tokens
                ┌──────────────▼──────────────┐
                │  MLP Adapter (2-layer)       │
                └──────────────┬──────────────┘
                               │ visual tokens (concat with text)
   ┌───────────────────────────▼───────────────────────────┐
   │  每一层 Transformer Block (Vicuna-7B 主干)              │
   │  ┌───────────────────────────────────────────────┐    │
   │  │   Self-Attention                              │    │
   │  │   Q/K/V = [Q_text/K_text/V_text  ‖            │    │
   │  │            Q_visual/K_visual/V_visual]        │    │
   │  │   注意力矩阵跨 modality 共享                    │    │
   │  └───────────────────────────────────────────────┘    │
   │  ┌───────────────────────────────────────────────┐    │
   │  │   FFN_text  (frozen LLM expert)               │    │
   │  │   FFN_visual (Visual Expert，trainable)        │    │
   │  │   token 是 visual 走 FFN_visual，否则 FFN_text  │    │
   │  └───────────────────────────────────────────────┘    │
   └────────────────────────────────────────────────────────┘
```

**关键点**：
1. **每一层都注入"视觉专家" QKV+FFN**，参数数量约等于该层原本的 QKV+FFN，相当于在每层并行一个"视觉副本"；
2. **token 路由**：text token 走 LLM 原参数，visual token 走视觉专家；attention 层跨模态共享 Q/K/V 计算（拼接后 softmax）；
3. **冻结 LLM 主参数**，只训练 Visual Expert + ViT + MLP adapter，**完全不损害原 LLM 的纯文本性能**（这是与 LLaVA 等"开放 LLM 训练"路线的最大区别）；
4. **深度融合（Deep Fusion）**：与浅对齐相比，视觉信号在每一层都参与 attention，提升 OCR / grounding / 细粒度推理。

**评测**：CogVLM-17B 在 NoCaps、Flickr30k captioning、RefCOCO/+/g、Visual7W、GQA、ScienceQA、VizWiz VQA、TDIUC 共 **10 个跨模态基准上达到 SOTA**，并在 VQAv2、OKVQA、TextVQA、COCO captioning 上仅次于 PaLI-X 55B（参数量约为 1/3）。

### 3.2 CogVLM2 / CogVLM2-Video / GLM-4V-9B（2024-05 / 08）

**核心论文**：Hong et al., *CogVLM2: Visual Language Models for Image and Video Understanding*, arXiv:2408.16500 (2024-08)。

CogVLM2 家族继续采用 **Visual Expert 架构**，但做了多项工程升级：

| 维度 | CogVLM-17B | CogVLM2-19B (llama3-chat-19B) | GLM-4V-9B |
|---|---|---|---|
| LLM 底座 | Vicuna-7B | **Meta-Llama-3-8B-Instruct** | **GLM-4-9B** |
| 视觉编码器 | EVA-CLIP-E/14 | **SigLIP / EVA-CLIP** 改造版 | 同 CogVLM2 |
| MLP Adapter | 2 层 MLP | **2×2 卷积 + SwiGLU** | 同 CogVLM2 |
| 图像分辨率 | 490² | **1344×1344** | 1120/1344 |
| 上下文 | 2K | **8K** | 8K |
| 总参 | 17B | 19B（8B LLM + 11B 视觉专家） | 13B 级 |
| 中文 | — | cogvlm2-llama3-chinese-chat-19B | 原生中英 |

**CogVLM2-Video**（2024-07）：
- 在 CogVLM2 基础上增加**时间 grounding** 数据构建管线，自动生成 30K 时间相关 QA；
- 支持分钟级视频理解；
- 在多项 video QA 基准上 SOTA（同期开源）。

**GLM-4V-9B**：作为 GLM-4 主线的视觉版本，继承 CogVLM2 的视觉专家结构，绑定 GLM-4-9B 文本基座，是 ChatGLM 综述论文中正式列入的开源 VLM。

### 3.3 GLM-4.1V-Thinking / GLM-4.5V / GLM-4.6V（2025）

**核心论文**：*GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with a Family of VLMs*, arXiv:2507.01006 (2025-07，多次修订至 v6 含 GLM-4.6V)。

**统一架构**（三代共享）：

```
Vision Encoder  →  MLP Projector  →  LLM (GLM-4-9B / GLM-4.5-Air / GLM-4.6 base)
```

变化要点：
1. **抛弃 Visual Expert**：从 GLM-4.1V 开始回归到主流 **vision encoder + projector + LLM** 结构，更易复用 LLM 基座的 RL 后训练成果；
2. **强化学习"Thinking"链**：大量使用强化学习 + curriculum 教模型在视觉推理上"显式思考"；GLM-4.1V-9B-Thinking 用 RL 让 9B 模型在复杂多模态推理基准上击败 72B 量级闭源模型；
3. **GLM-4.5V (2025-08)**：基于 **GLM-4.5-Air (106B/A12B)** 底座，继承 4.1V 思路；在 **42 项公开视觉-语言基准上达到同规模 SOTA**；支持图像、视频、长文档与 GUI Agent；
4. **GLM-4.6V**（2025 Q4）：升级到 GLM-4.6 底座，进一步扩展多模态推理与长视频；
5. **GLM-4.6V-Flash 9B**（2025-12）：端侧/低成本版本；
6. **GLM-5V-Turbo**（2026-04）：基于 **GLM-5 (744B/40B)** 底座的旗舰 VLM，在多模态推理、长文档理解、GUI Agent 与视频分析上达到新高度，是智谱视觉模型线的最新旗舰。

---

## 四、视觉生成模型

### 4.1 CogView 系列（图像生成）

| 模型 | 时间 | 关键技术 | 参数 |
|---|---|---|---|
| **CogView** | 2021-05 (NeurIPS 2021) | dVAE 离散 token + 4B GPT-style Transformer 自回归生成；首个开源中文文生图大模型 | 4B |
| **CogView2** | 2022-04 (NeurIPS 2022) | **Cross-modal General LM (CogLM)**：多任务 + 层次化生成；先生成低分辨率图像 token，再用 super-resolution 模块迭代细化；相对 DALL·E-2 提供 ~10× 生成加速 | 6B |
| **CogView3 / CogView-3-Plus** | 2024-03 (arXiv:2403.05121) | 转向**扩散模型**路线；提出 **Relay Diffusion** 级联框架——低分辨率 latent 扩散 + 高分辨率 relay refiner | 3B |
| **CogView4-6B** | 2025-03 | 中文原生 **DiT (Diffusion Transformer)**，宽高 512–2048（32 整除），BF16 | 6B |

CogView 路线显著的"风格"是：从早期 GPT-style 自回归逐步**迁移到 DiT/扩散**，与同期 DALL·E、Stable Diffusion、Imagen 演进路径相似，但保持与 GLM 主家族的工程协同（共享 tokenizer、训练框架）。

### 4.2 CogVideoX（视频生成）

**核心论文**：Yang et al., *CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer*, ICLR 2025（arXiv:2408.06072）。

**预演**：CogVideo (2022, ICLR 2023) 是首个开源 9B 文生视频模型，基于 CogView2 扩展时间维度，但生成时长与运动质量有限。

**CogVideoX 关键创新**：

1. **3D Causal VAE**：沿空间和时间两个维度对视频压缩，时间上采用 **causal**（仅看历史帧）以支持任意长度；显著降低 token 数量同时保持高保真重建；2024-08 单独开源。
2. **Expert Transformer + Expert Adaptive LayerNorm (Expert AdaLN)**：
   - 视频 latent token 与文本 token 拼接进入同一 Transformer，但 LayerNorm 的 affine 参数 (γ, β) 对**两种模态使用不同的 expert**；
   - 这种"按模态分通道、共享 self-attention"的范式，与 Stable Diffusion 3 的 MMDiT、与 CogVLM 的 Visual Expert 思路一脉相承——**深度融合不浅化任一模态**；
3. **Progressive Training + Multi-Resolution Frame Pack**：训练时混合不同分辨率/时长视频，用 frame pack 高效填充 batch；
4. **数据管线**：自研视频字幕模型 + 多阶段过滤；与字幕模型和 3D VAE 一同开源；
5. **生成能力**：10 秒、16 fps、768×1360 分辨率，连续叙事，运动幅度大。

**开源版本**：CogVideoX-2B（基础）/ CogVideoX-5B / CogVideoX-5B-I2V（图生视频）/ CogVideoX-1.5。在国产文生视频开源生态（与 Wan / HunyuanVideo / Open-Sora 并列）中是最早达到工业级长视频质量的模型之一。

---

## 五、推理模型（Reasoning / Deep Thinking）

### 5.1 GLM-Z1-32B-0414

- 基于 GLM-4-32B-0414 通过 **冷启动 + 大规模强化学习** 微调；
- 训练任务包括数学、代码、逻辑（含 AIME、MATH、GSM8K、LiveCodeBench、Codeforces 类问题）；
- 引入**基于 pairwise ranking 反馈的通用 RL**，避免推理能力提升以损失通用对话能力为代价；
- 在线推理速度 200 tokens/s；
- 在 AIME / MATH / GPQA / LiveCodeBench 上接近或超越同期 DeepSeek-R1-Distill-Llama-70B 等模型。

### 5.2 GLM-Z1-Rumination-32B-0414（"反刍模型"）

定位为对标 OpenAI **Deep Research**：
- "反刍 (Rumination)"：相对普通"思考"，可进行更长、更开放、更循环的搜索-思考-搜索；
- 训练通过端到端 RL 扩展，奖励信号来自 **ground-truth 答案 / rubrics**；
- 模型在思考过程中调用外部工具：`search` / `click` / `open` / `finish`（固定四工具集，外接搜索引擎）；
- 显著提升研究型写作（如"分析两座城市 AI 发展并撰写比较报告"）。

### 5.3 GLM-Z1-9B-0414 与 GLM-4.5 Hybrid Reasoning

- **GLM-Z1-9B**：用同套 RL 技术训练 9B 小模型，在数学推理与通用任务上是同尺寸开源模型 Top；
- **GLM-4.5 Thinking Mode**：把推理能力作为 MoE 旗舰内置模式，以 `thinking.type` 显式开关；这是从"独立推理模型"到"统一基座 + 推理模式"的范式转变（2024-09 OpenAI o1 之后业界主流方向，GLM-4.5 是开源端较早实现 hybrid reasoning 的 MoE 旗舰）。

---

## 六、跨代技术演进分析（重点：从 Prefix LM 到 Causal LM 的架构转型）

GLM 家族最具特色的演进，是从最初坚持"自回归填空"独特路线，逐步在保留品牌名"GLM"的同时，**事实上转向标准 Decoder-only Causal LM**。这一过程并非一次性切换，而是分阶段渐进：

### 6.1 关键演进节点

| 阶段 | 时间 | 代表模型 | 预训练目标 | Attention Mask | 位置编码 | Norm | 激活 |
|---|---|---|---|---|---|---|---|
| Prefix LM 时代 | 2021–2022 | GLM-Base/Large/XL/XXL | 自回归填空 (Part A 双向 + Part B 因果) | 混合 mask（Part A 全可见，Part B 因果） | **2D 可学习 PE** | Pre-LN | GeLU |
| 工程化双语 | 2022 | GLM-130B | 自回归填空 | 混合 mask | **RoPE** | **DeepNorm** | **GeGLU** |
| 对话化过渡 | 2023.03 | ChatGLM-6B | GLM 自回归填空 | 混合 mask | RoPE | RMSNorm | GeLU |
| MQA + 长上下文 | 2023.06 | ChatGLM2-6B | GLM 混合目标（同时含 BERT 风格 / GPT 风格 span） | 混合 mask（部分版本简化） | RoPE | RMSNorm | SwiGLU（部分） |
| 实质 Causal | 2023.10 | ChatGLM3-6B | 类 Causal LM（逐步弱化 blank infilling） | **Causal-only**（社区分析；官方文档不再强调 Prefix LM） | RoPE | RMSNorm | SwiGLU |
| 标准 Causal LM | 2024 | GLM-4 / GLM-4-9B | Causal LM | Causal | RoPE + YaRN 扩展 | RMSNorm | SwiGLU |
| 稠密旗舰 | 2025.04 | GLM-4-32B-0414 | Causal LM | Causal | RoPE + YaRN | RMSNorm | SwiGLU |
| MoE Hybrid Reasoning | 2025.07+ | GLM-4.5 / 4.6 / 4.7 | Causal LM + MoE + RL | Causal | RoPE | RMSNorm | SwiGLU + MoE FFN |

### 6.2 转型动因

1. **Causal LM 的"All-in-One"成熟**：GPT-3/4 用纯 Causal LM 同时把 NLU、生成、推理统一；T5/BART 这类编码-解码范式逐渐让位。Prefix LM 在工程上开发链路更复杂（需要为 Part A/B 维护混合 mask），而其相对 Causal LM 的下游优势在 SFT/RLHF 时代被逐步抹平。
2. **生态兼容**：迁移到标准 Causal LM 后可直接复用 Hugging Face transformers / vLLM / FlashAttention / FlashInfer / TensorRT-LLM 等基础设施，工程成本骤降。
3. **长上下文需求**：Prefix LM 的混合 mask 与 KV cache 优化（如 paged attention、prefix caching）耦合度低，移植成本高；切换到 Causal LM 后可享受现代推理框架的所有优化。
4. **对齐流水线**：DPO / RLHF / GRPO / RL-with-verifier 几乎清一色为 Causal LM 设计；继续坚持 Prefix LM 会在每个新 RL 算法上付出额外适配成本。
5. **推理范式（CoT / o1-like）**：思考链是天然的因果生成，Causal LM 与 Thinking Mode / Tool Use / Agent 的契合度最高。

### 6.3 GLM 路线"被取舍"的设计

- **2D Positional Encoding** 在 GLM-130B 即被 RoPE 替换；
- **Span shuffling** 在 ChatGLM2/3 被淡化；
- **Part A 双向 attention** 在 ChatGLM3 之后基本不再强调；
- **保留下来的 GLM 元素**：仅"GLM 品牌 + 训练数据/对齐 know-how + 工程框架（slime、SAT、SwissArmyTransformer）"。

可以理解为：**GLM 已从"特定预训练目标"演化为"团队/家族标识"**，现代 GLM-4.5 在架构上更接近 DeepSeek-MoE / Qwen3-MoE，而非最初的 GLM 论文。

---

## 七、商业与市场动态（2025–2026）

### 7.1 智谱 AI 香港上市（2025-12-20）

智谱 AI（Zhipu AI）于 2025 年 12 月 20 日在香港交易所主板挂牌上市，成为继商汤之后第二家以基础大模型为核心业务的港股 AI 上市公司。此次 IPO 募资约 30 亿港元，估值区间反映市场对国产开源基座模型商业化前景的认可。招股书披露：
- 2025 年 API 与 MaaS 收入同比增长超过 200%；
- 开源模型（GLM-4-9B/32B 系列）Hugging Face 累计下载量突破 5000 万次；
- 企业客户覆盖金融、政务、汽车、教育四大垂直领域。

### 7.2 API 价格大幅上调（2026-03-04）

2026 年 3 月 4 日，智谱宣布对 bigmodel.cn 与 Z.ai 海外平台的 API 定价进行**全线上调 30–100%**。调价背景与影响：
- **背景**：GLM-5 及后续旗舰模型训练与推理成本显著上升（744B MoE 激活 40B，推理集群以 H100/H20 为主）；同时公司上市后面临盈利压力；
- **涨幅**：GLM-4.5 系列输入 \$0.2→\$0.35/M tokens（+75%），输出 \$1.1→\$2.0/M tokens（+82%）；GLM-5 系列定价输入 \$0.5/M、输出 \$3.5/M；
- **市场反应**：部分中小开发者转向 GLM-4-9B/32B 开源自托管方案，但企业级客户对旗舰 API 依赖度较高，迁移成本大；
- **竞品对比**：调价后 GLM-5 价格仍低于 GPT-5.5（\$5/\$30）与 Claude 4 Opus，但差距缩小。

### 7.3 API 调用量翻倍（2026-05）

据智谱 2026 年 5 月官方披露，bigmodel.cn 平台日 API 调用量较 2025 年底**翻倍**，主要驱动因素：
- GLM-5 系列在 SWE-bench、Agent 编码等场景的企业采用率提升；
- GLM-Z1 推理模型在科研、金融分析等长思考任务上的渗透；
- 开源生态反哺：GLM-4-32B-0414 等开源模型带动社区应用，进而转化为商业 API 用户。

### 7.4 GLM Coding Plan 与「低价 + 高额度」打法（2026-04 起，本轮新增）

这条线与模型发布同等重要，是 GLM-5.x 三代共同的商业化载体：

- **2026-04-07**：GLM Coding Plan 随 GLM-5.1 上线（个人版）；
- **2026-05-29**：GLM Coding Plan **团队版**上线，支持席位/权限/用量/预算统一管理、集中账单与统一开票，官方承诺**默认不将代码、提示词与对话内容用于模型训练**，高级版首发接入最新旗舰；
- **2026-08-19 / 08-26**：GLM-5.3 与 GLM-5.3-Flash **全量进入** Coding Plan；Flash 的可用额度为 GLM-5.3 的 **3 倍**（官方口径）；
- **计费机制变化**：新版 Coding Plan 改为**基于积分的配额系统**，官方称额度公开透明；**非高峰时段（含周末全天）的调用只消耗标准积分的 50%**。

**定价叙事的变化值得记一笔**：GLM-5.3-Flash 官方定价为 **GLM-5.3 的 1/10**（限时折扣内 **1/20**）、**Opus 4.8 的 1/40**。这与 §7.2 记录的 2026-03「全线上调 30–100%」方向相反——**旗舰涨价、轻量档大幅降价**，用同一家族内的价格分层来同时守毛利与抢用量。这是本轮最值得跟踪的商业信号（能否兑现取决于 Flash 的实际质量，见 §2.9.3 的核验受限说明）。

---

## 八、关键创新点汇总

| # | 创新 | 出处 | 影响 |
|---|---|---|---|
| 1 | **自回归填空 (Autoregressive Blank Infilling)** | GLM 2021 / ACL 2022 | 用单一目标统一 NLU + 有/无条件生成；启发后续 UL2 等多任务预训练 |
| 2 | **2D 位置编码** | GLM 2021 | 解决 mask span 长度泄漏；后被 RoPE 取代 |
| 3 | **DeepNorm** | GLM-130B | 解决 100B+ 训练稳定性，被 BLOOM 等借鉴 |
| 4 | **INT4 量化无损推理（百亿级）** | GLM-130B | 首次让 130B 模型可在消费卡上推理（4×3090） |
| 5 | **Multi-Query Attention 国产化落地** | ChatGLM2-6B | 推动 MQA/GQA 在中文社区普及 |
| 6 | **All Tools Agent 范式** | GLM-4 | 模型自主决定调用 web/Python/T2I/自定义函数 |
| 7 | **Visual Expert** | CogVLM | 在每层 attention/FFN 并行视觉副本，深度融合而不损害纯文本能力 |
| 8 | **3D Causal VAE + Expert AdaLN** | CogVideoX | 长视频的高效 latent 表征 + 文本-视频深度融合 |
| 9 | **Relay Diffusion** | CogView3 | 级联扩散，低→高分辨率 relay |
| 10 | **Rumination（反刍）模型** | GLM-Z1-Rumination | 对标 Deep Research，工具调用 + RL 训练长程研究 |
| 11 | **Hybrid Reasoning (Thinking/Non-Thinking 单模型双模式)** | GLM-4.5 | 通过 API 参数即可切换；MoE 上较早实现 |
| 12 | **slime RL 框架** | GLM-4.5+ | 异步 rollout/trainer 解耦；GLM-4.5/4.6/4.7/5/5.1 共用 |
| 13 | **Loss-free Balance Routing**（在 GLM-4.5 MoE 中） | GLM-4.5 | 替代 auxiliary load loss，提升 MoE 训练稳定性 |
| 14 | **Preserved Thinking** | GLM-4.7 | 在多轮工具调用之间保留思考链，提升自主编程 |
| 15 | **GLM-5 大规模 MoE 基座** | GLM-5 (2026-02) | 744B/40B 激活，SWE-bench 77.8%，开源旗舰新标杆 |
| 16 | **IndexShare（跨层复用稀疏注意力 indexer）** | GLM-5.2 (2026-06) | 每 4 层稀疏注意力复用同一 indexer，1M 上下文下每 token FLOPs −2.9×（官方口径）；对应论文 arXiv:2603.12201 *IndexCache* |
| 17 | **MTP 层改进（投机解码接受长度 +≤20%）** | GLM-5.2 (2026-06) | 直接提升长程任务的解码效率 |
| 18 | **「同基座 + 极致后训练 Scaling」范式** | GLM-5.3 (2026-08) | 首次公开宣称旗舰代际提升**全部来自后训练**（基座与 GLM-5.2 相同）；Terminal Bench 3.0 4.6→28.3 |
| 19 | **稀疏 + 线性注意力混合架构（开源前沿首个）** | GLM-5.3-Flash (2026-08) | 320B/18B；注意力计算 −3.01×、KV cache −4.44×（相对 GLM-5.3）；结合 mHC 与 30T 多模态语料，原生多模态 |

---

## 九、对比小结

### 8.1 基座模型横向对比

| 模型 | 时间 | 架构类别 | 总参 / 激活 | 上下文 | 训练 tokens | 典型评测亮点 |
|---|---|---|---|---|---|---|
| GLM-130B | 2022.08 | Prefix LM (稠密) | 130B | 2K | 400B | LAMBADA SOTA、INT4 推理 |
| ChatGLM-6B | 2023.03 | Prefix LM (稠密) | 6.2B | 2K | ~1T | 中文对话开源里程碑 |
| ChatGLM2-6B | 2023.06 | Prefix LM + MQA | 6.2B | 32K | 1.4T | MMLU +23%、CEval +33% |
| ChatGLM3-6B | 2023.10 | ≈Causal LM + MQA | 6.2B | 32K / 128K | — | 工具/代码原生模板 |
| GLM-4-9B-Chat | 2024.06 | Causal LM | 9B | 128K / 1M | 10T | 接近 GPT-4 子项 |
| GLM-4-32B-0414 | 2025.04 | Causal LM (稠密) | 32B | 32K → 128K (YaRN) | — | BFCL 69.6、IFEval 87.6 |
| GLM-Z1-32B-0414 | 2025.04 | Causal LM + RL | 32B | 128K | — | 200 tok/s、AIME/MATH 接近 R1 |
| GLM-4.5 | 2025.07 | MoE + Hybrid Reasoning | 355B / 32B | 128K | 23T | 12 项基准均分全球第 2 |
| GLM-4.5-Air | 2025.07 | MoE | 106B / 12B | 128K | 23T | 超越 Gemini 2.5 Flash / Qwen3-235B |
| GLM-4.6 | 2025.09 | MoE | 357B / 32B | **200K** | — | 与 Claude Sonnet 4.5 近平价 |
| GLM-4.7 | 2025.12 / 2026.01 | MoE + Preserved Thinking | 同代 | 200K | — | 自主编程方向 |
| GLM-5 | 2026.02 | MoE | **744B / 40B** | 200K | — | SWE-bench 77.8%，12 项基准全球前 3 |
| GLM-5.1 | 2026.04.07 | MoE（承 GLM-5） | 官方未披露 | 200K | — | SWE-Bench Pro 58.4（官方称全球最佳）；8 小时长程（详见 §2.9.0） |
| GLM-5.2 | 2026.06.16 | MoE + IndexShare + 改进 MTP | 官方未披露 | **1M** | — | DeepSWE 46.2、FrontierSWE 74.4、SWE-Marathon 13.0（带条件，见 §2.9.1）；MIT |
| GLM-5.3 | 2026.08.19 | **与 GLM-5.2 同一基座**（纯后训练） | 同 GLM-5.2 | 1M | — | Terminal Bench 3.0 28.3、DeepSWE 66.9、CyberGym 84.5（带条件，见 §2.9.2）；自定义许可 |
| GLM-5.3-Flash | 2026.08.26 | **稀疏+线性注意力混合 + mHC**（新训基座） | **320B / 18B** | 1M | 30T（多模态语料） | 原生多模态；AA II 57；价格为 GLM-5.3 的 1/10（见 §2.9.3）；MIT |

> ⚠️ 本表「典型评测亮点」列只做条目指路，**不构成跨厂商排名**；每个数字的 harness / 上下文 / effort / 是否第三方评测各不相同，引用前必须回看 §2.9 的对应条件列。
> 另一处口径提示：GLM-5.2 与 GLM-5.3 的**总参/激活参官方均未披露**（本表据实写「官方未披露」，不沿用 GLM-5 的 744B/40B 推测）。

### 9.2 多模态模型横向对比

| 模型 | 时间 | 视觉编码器 | 融合方式 | LLM 底座 | 总参 | 亮点 |
|---|---|---|---|---|---|---|
| CogVLM-17B | 2023.11 | EVA-CLIP-E/14 | **Visual Expert（每层并行）** | Vicuna-7B | 17B | 10 项 SOTA |
| CogVLM2-19B | 2024.05 | SigLIP/EVA | Visual Expert | LLaMA3-8B | 19B | 1344² / 8K |
| GLM-4V-9B | 2024.06 | 同上 | Visual Expert | GLM-4-9B | ~13B | GLM 主家族绑定 |
| GLM-4.1V-9B-Thinking | 2025.07 | 视觉编码器 + MLP | **Encoder + Projector + LLM**（弃用 Visual Expert） | GLM-4-9B | 9B | RL Thinking 链 |
| GLM-4.5V | 2025.08 | 同上 | Encoder + Projector + LLM | GLM-4.5-Air (MoE) | 106B / 12B | 42 项基准 SOTA |
| GLM-4.6V / 4.6V-Flash | 2025 Q4–12 | 同上 | Encoder + Projector + LLM | GLM-4.6 / 9B | 357B / 9B | 200K + 端侧 |
| GLM-5V-Turbo | 2026.04 | 同上 | Encoder + Projector + LLM | GLM-5 (MoE) | 744B / 40B | 旗舰 VLM，多模态推理新高度；技术报告 arXiv:2604.26752（v3 2026-05-12） |
| **GLM-5.3-Flash / FlashX** | 2026.08.26 | 官方未披露（**原生多模态**，非「LLM + 后接编码器」的拼接式） | 视觉原生融入同一主干（官方口径：视觉进入 coding 循环） | 新训基座（稀疏+线性注意力混合 + mHC） | **320B / 18B** | GLM-5 系列首个原生多模态；AA II 57；FlashX 200 tokens/s（见 §2.9.3） |

---

## 十、参考文献

### 论文（按时间）

1. Ding M., Yang Z., Hong W., et al. **CogView: Mastering Text-to-Image Generation via Transformers**. NeurIPS 2021. arXiv:2105.13290. https://keg.cs.tsinghua.edu.cn/jietang/publications/NeurIPS21-Ding-et-al-CogView.pdf
2. Du Z., Qian Y., Liu X., Ding M., Qiu J., Yang Z., Tang J. **GLM: General Language Model Pretraining with Autoregressive Blank Infilling**. ACL 2022. arXiv:2103.10360. https://aclanthology.org/2022.acl-long.26/
3. Hong W., Ding M., Zheng W., Liu X., Tang J. **CogVideo: Large-scale Pretraining for Text-to-Video Generation via Transformers**. ICLR 2023. arXiv:2205.15868.
4. Ding M., Zheng W., Hong W., Tang J. **CogView2: Faster and Better Text-to-Image Generation via Hierarchical Transformers**. NeurIPS 2022. arXiv:2204.14217.
5. Zeng A., Liu X., Du Z., et al. **GLM-130B: An Open Bilingual Pre-trained Model**. ICLR 2023. arXiv:2210.02414. https://arxiv.org/abs/2210.02414
6. Wang W., Lv Q., Yu W., et al. **CogVLM: Visual Expert for Pretrained Language Models**. NeurIPS 2024. arXiv:2311.03079. https://arxiv.org/abs/2311.03079
7. Zheng W., Teng J., Yang Z., et al. **CogView3: Finer and Faster Text-to-Image Generation via Relay Diffusion**. arXiv:2403.05121 (2024).
8. Team GLM (Zeng A., Xu B., et al.). **ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools**. arXiv:2406.12793 (2024). https://arxiv.org/abs/2406.12793
9. Hong W., Wang W., Ding M., et al. **CogVLM2: Visual Language Models for Image and Video Understanding**. arXiv:2408.16500 (2024). https://arxiv.org/abs/2408.16500
10. Yang Z., Teng J., Zheng W., et al. **CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer**. ICLR 2025. arXiv:2408.06072. https://arxiv.org/abs/2408.06072
11. Team GLM-V. **GLM-4.1V-Thinking & GLM-4.5V & GLM-4.6V: Towards Versatile Multimodal Reasoning with a Family of VLMs**. arXiv:2507.01006 (2025).
12. Team GLM. **GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models**. arXiv:2508.06471 (2025-08).
13. Z.ai Blog. **GLM-5: Scaling Reasoning and Coding with 744B MoE**. 2026-02.
14. Team GLM. **GLM-5: from Vibe Coding to Agentic Engineering**. arXiv:2602.15763（**v1 2026-02-17 / v2 2026-02-24**）。GLM-5 / GLM-5.1 / GLM-5.2 / GLM-5.3 的模型卡均引用此报告。
15. Team GLM. **IndexCache: Accelerating Sparse Attention via Cross-Layer Index Reuse**. arXiv:2603.12201（v1 **2026-03-12**）。GLM-5.2 模型卡以 **IndexShare** 之名引用；论文主实验为 30B DSA 模型。
16. Team GLM. **GLM-5V-Turbo: Toward a Native Foundation Model for Multimodal Agents**. arXiv:2604.26752（**v1 2026-04-29 / v3 2026-05-12**）。
17. Z.ai Blog. **GLM-5V-Turbo: Multimodal Reasoning at Scale**. 2026-04.
18. 智谱 AI 招股书 / 港交所公告. **Zhipu AI 香港主板上市**. 2025-12-20.
19. bigmodel.cn 官方公告. **API 价格调整通知**. 2026-03-04.

> 版本口径（本轮）：第 14–16 条 arXiv ID 的标题、版本号、版本日期均于 2026-10-17 回查 `export.arxiv.org/api`；GLM-5 报告作者列为 `GLM-5-Team`（模型卡 bibtex 可见完整作者表）。

### 官方资源

20. Z.AI 官网与开发者文档：https://z.ai ｜ https://docs.z.ai（**注：`z.ai` 与 `docs.z.ai` 在本次核对环境（2026-10-17）TLS 不可达，未能直读博客原文**）
21. 智谱 AI 开放平台 / bigmodel.cn：https://open.bigmodel.cn ｜ https://www.bigmodel.cn
22. **智谱官方发布记录（日期的一手出处）**：https://docs.bigmodel.cn/cn/update/new-releases —— GLM-5（2026-02-12 / 02-03 GLM-OCR）、GLM-5-Turbo（2026-03-15）、GLM-5V-Turbo（2026-04-02）、GLM-5.1（2026-04-07）、GLM-5.2（2026-06-16）、GLM-5.3（2026-08-19）、GLM-5.3-Flash（2026-08-26）的上线日期均取自此页
23. **智谱官方模型文档页**：`docs.bigmodel.cn/cn/guide/models/text/glm-5.2`、`…/glm-5.3`、`…/vlm/glm-5.3-flash`、`…/glm-5.1`、`…/glm-5`（本轮 §2.9 的上下文/输出/思考模式/定价口径来源）
24. Z.AI / 智谱 GitHub 组织：https://github.com/zai-org （含 GLM-130B、GLM-4、GLM-4.5、GLM-V、CogVLM2、CogVideo、CogView4、slime、GLM-5 等仓库）
25. THUDM GitHub 组织：https://github.com/THUDM （含 GLM、ChatGLM-6B、ChatGLM2-6B、ChatGLM3、GLM-4、slime 等历史仓库）
26. Hugging Face：https://huggingface.co/zai-org （GLM-5.3-Flash / GLM-5.3 / GLM-5.2 / GLM-5.1 / GLM-5 等权重）
27. **GLM 官方模型卡（本轮新增内容的核验主源）**：`huggingface.co/zai-org/GLM-5.2`（createdAt 2026-06-16）、`…/GLM-5.3`（2026-08-25）、`…/GLM-5.3-Flash`（2026-08-25）、`…/GLM-5.1`（2026-04-03）、`…/GLM-5`
28. **智谱中文官方研究页**：https://www.zhipuai.cn/zh/research/161 （GLM-5.3 发布文，含任务环境规模化与安全能力叙述）
29. GLM-130B 官方博客：https://keg.cs.tsinghua.edu.cn/glm-130b/
30. CogVLM2-Video 项目页：https://cogvlm2-video.github.io/
31. slime（RL 后训练框架）：https://github.com/THUDM/slime

### 第三方分析（参考）

32. Z.ai Blog. **GLM-4.5: Reasoning, Coding, and Agentic Abililties**. https://z.ai/blog/glm-4.5
33. APXML. *GLM-4.5 / GLM-4.6 Specifications and GPU VRAM Requirements*. https://apxml.com/models/glm-45 ｜ https://apxml.com/models/glm-46
34. The Decoder (2025-12). *Zhipu AI challenges Western rivals with low-cost GLM-4.7*.
35. vLLM 官方博客 (2025-08-19). *GLM-4.5 Meets vLLM: Built for Intelligent Agents*.

---

> 编纂说明：本报告以官方论文与发布信息为主要依据，对于社区流出的部分参数（如 GLM-4.7 / GLM-5 系列的精确激活/总参）已做标注；ChatGLM2/3 在"是否仍为 Prefix LM"上社区描述存在口径不一，本报告以官方仓库 README 与 ChatGLM 综述论文 (arXiv:2406.12793) 的最终归纳为准，并在第六章给出渐进式转型的判断。

> **2026-10-17 增量说明**：本轮只做增补与修正，不改动 2026-06 前已核验的结论。新增内容集中在 **§2.9**（GLM-5.2 / GLM-5.3 / GLM-5.3-Flash，含 §2.9.0 为对照基线补的 GLM-5.1 带条件数字）、**§2.10**（未确证与待跟踪，9 项，均不入正文）、**§7.4**（Coding Plan 与价格分层）；同步更新 §1.1 时间线、§8 创新点表（+4 项）、§9.1/§9.2 横向对比表、§10 参考文献与官方资源编号（原「官方资源」编号与论文列表重复，本轮一并重排）。**证据分级口径**：精读原文（官方模型卡 / 官方文档 / 官方发布记录原文）、摘要级（仅读 arXiv 摘要与元数据）、二手（第三方页面或他人转述）、受限核验（原始页面在本环境不可达）。本轮 GLM-5.2 / 5.3 / 5.3-Flash 的主体数字均为「精读原文」；**受限核验项（z.ai 博客原文、GLM-5.3-Flash 基准图为图片）已明确标注，不参与结论**。
