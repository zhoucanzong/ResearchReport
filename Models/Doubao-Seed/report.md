---
display_name: Doubao-Seed
---

# Doubao/Seed系列模型深度调研报告

## 概述与时间线

字节跳动（ByteDance）旗下的AI大模型研发主要由**Seed团队**（2023年正式组建）主导，产品侧通过**豆包（Doubao）**品牌面向消费者和企业用户。Seed团队定位为"探索通用智能的无限可能"，其研究覆盖语言模型、多模态理解与生成、语音、图像、视频等全方向。

### 关键时间线

| 时间 | 事件 |
|------|------|
| 2023年 | ByteDance Seed团队正式组建，豆包App上线 |
| 2024年6月 | Seed-TTS论文发布（语音合成基础模型） |
| 2024年7月 | Seed-ASR论文发布（LLM-based语音识别） |
| 2024年9月 | PixelDance与Seaweed视频生成模型发布 |
| 2024年11月 | PixelDance/Seaweed在即梦AI上线 |
| 2025年1月 | Doubao-1.5-pro发布（MoE架构基座模型） |
| 2025年4月 | Seedream 3.0图像生成模型发布 |
| 2025年4月 | Seed-Thinking-v1.5推理模型技术报告发布 |
| 2025年5月 | Seed1.5-VL视觉语言模型发布 |
| 2025年5月 | BAGEL统一多模态模型开源 |
| 2025年6月 | Seed-Coder代码模型开源 |
| 2025年6月 | Seedance 1.0视频生成模型技术报告发布 |
| 2025年下半年 | Seedream 4.0/4.5图像生成模型发布 |
| 2025年12月 | Seedance 1.5 Pro（音画同步视频生成）上线即梦 |
| 2026年2月 | Seed 2.0系列（Pro/Lite/Mini）正式发布 |
| 2026年2月 | Seedance 2.0视频生成模型发布 |
| 2026年3月 | Seed1.8 Agent模型发布 |

---

## 一、基座语言模型演进

### 1.1 早期阶段：Doubao基座模型

早期 Seed/Doubao 基座的论文和训练资料有限。产品运行规模或云 API 可用性不能说明参数规模、架构或训练目标；本报告从 Doubao-1.5-pro 首次较详细的官方技术材料开始讨论语言模型设计。

### 1.2 Doubao-1.5-pro（2025年1月）

Doubao-1.5-pro是字节跳动第一次大规模公开披露技术细节的基座模型，于2025年1月22日发布。

**架构特征：**
- **MoE（Mixture-of-Experts）架构**：采用高度稀疏的MoE设计
- **训练-推理一体化设计**：从预训练阶段即考虑推理效率
- **性能杠杆达到7倍**：激活参数仅为等效Dense模型参数量的1/7，即可超过Dense模型性能（此前业界普遍水平不到3倍）
- 训练数据量超过9T tokens（中间版本），最终版本更大
- 性能超过Llama3.1-405B等超大稠密模型

**推理系统优化：**
- Prefill/Decode分离的Serving系统
- 四象限异构硬件策略（Prefill Attention/FFN、Decode Attention/FFN）
- Prefill阶段Tensor Core利用率接近60%
- FlashAttention 8-bit实现 + Per N tokens Per Sequence量化
- Decode FFN采用W4A8量化 + EP部署
- 支持Prefill和Decode集群灵活配比和动态扩缩

**Post-Training特色：**
- 完全自主数据生产体系，**不使用任何其他模型数据**
- SFT阶段：算法驱动的训练数据优化 + 模型自演进（Self-evolve）
- Reward Model：融合合成与挖掘数据，多阶段训练框架
- RL阶段：基于veRL框架，高并行化多角色训练推理一体框架
- 提出生成式RM建模方法（区别于传统判别式RM）

> 该说法是 Doubao-1.5-pro 技术材料对其训练目标/数据来源的团队声明，不应扩展为整个 Seed 团队不使用任何外部模型。Seed-Coder 的技术报告明确使用 DeepSeek-V2-Chat 对代码文件进行质量打分；这是模型辅助数据标注，不等同于将教师模型输出作为预训练目标。本文在跨线比较中分别记录“训练目标是否蒸馏自外部模型”与“数据管线是否调用外部模型工具”。

**多模态能力与模型边界：**
官方技术材料描述视觉输入和 Speech2Speech 语音能力，但当前可读材料没有给出足够信息证明视觉、语音和文本均由同一组权重端到端联合训练。本文把能力接口、家族组件和模型内部共享结构分开记录。

**推理能力（深度思考模式）：**
- 官方对 Doubao-1.5-pro-AS1-Preview 的材料报告了 AIME 表现；该预览版本的完整提示、采样预算和对照条件未在本报告可读来源中闭合，因此只作为厂商报告结果，不写成与 o1 的同条件比较。
- RL 用于提升推理能力的官方说明只适用于该模型/训练阶段；不将它推广为 Seed 全线均使用相同数据策略或 RL 方法。

### 1.3 Seed 2.0 系列：接口可见，架构证据仍有限

Seed 2.0 Pro/Lite/Mini/Code 的官方发布与模型卡显示语言、代码、视觉和长视频能力覆盖扩展；但没有公开足以重建其参数结构、训练数据配比或各模态融合位置的完整技术报告。发布材料中的跨模型 benchmark、排名和价格主要用于描述特定版本/产品，不足以确认架构延续或解释能力提升来源。故本报告仅把它作为当前家族的开放证据边界，不从 Seed-Thinking-v1.5 的 MoE 参数推断 Seed 2.0 结构。

### 1.4 UltraMem：超稀疏架构探索

UltraMem（Ultra-Sparse Memory Network）是 Seed 团队关于稀疏记忆层的研究，针对 MoE 激活参数较少但推理时仍要访问大量专家权重的内存带宽瓶颈：

- 提出超稀疏内存层，有效解决MoE推理中的高推理成本和内存访问问题
- 实现2-6倍推理加速
- 相比MoE降低高达83%的推理成本
- 论文比较 UltraMem、MoE 与 dense 方案的特定推理设置；它说明团队研究另一种稀疏计算路径，但没有证明 UltraMem 已用于 Doubao-1.5-pro、Seed 2.0 或其他 Seed 产品。

---

## 二、推理模型：Seed-Thinking

### 2.1 Seed-Thinking-v1.5（2025年4月）

Seed-Thinking-v1.5是字节跳动Seed团队推出的推理模型，2025年4月14日公开技术报告，4月17日通过火山引擎开放API。

**模型架构：**
- **MoE架构**
- 总参数：**200B**
- 激活参数：**20B**
- 相比DeepSeek R1推理成本降低50%

**核心性能：**
- AIME 2024: **86.7**（追平OpenAI o3-mini-high）
- Codeforces pass@8: **55.0%**（接近Gemini 2.5 Pro）
- GPQA: **77.3%**（接近o3-mini-high）
- 人类评估超过DeepSeek R1约8%

**训练方法论——四大技术支柱：**

#### （1）数据系统：融合可验证与创造性数据
- **可验证数据**（数学/代码）：三重清洗（人工审核→模型过滤→多模型验证），从百万样本中保留10万高难度问题
- **不可验证数据**（创意写作）：基于Doubao 1.5 Pro训练集，双向奖励方法优化
- **新基准BeyondAIME**：100道未解答STEM题目，解决现有测试区分度不足问题

#### （2）奖励模型：双轨系统
- **可验证任务**：两代验证器（Seed-Verifier → Seed-Thinking-Verifier），从字符匹配升级到逐行对比推理步骤，准确率超99%
- **不可验证任务**：成对对比训练，数千万"AB测试"捕捉人类隐含偏好
- **双轨融合**：硬指标（对错）与软偏好（优劣）互补

#### （3）训练方法：SFT + RL两阶段
- **SFT阶段**：40万高质量实例（30万可验证 + 10万不可验证），构建长思维链数据集
- **RL阶段**：
  - 三重数据引擎（可验证/通用/混合数据）
  - 算法创新：价值预训练、解耦GE等
  - 在线数据适应技术
  - 解决训练不稳定和长链推理断层问题

#### （4）训练框架
- **HybridFlow编程模型**：支持算法快速探索与分布式并行
- **流式推理系统（SRS）**：解耦模型演进与异步推理，训练速度提升3倍
- **三层并行架构**：Tensor/Expert/Serial并行 + KARP算法优化GPU利用率
- 万亿参数下稳定性达95%

### 2.2 这条路线的设计取舍与证据边界

Seed-Thinking-v1.5 的关键不是简单地选 SFT 或 RL，而是先用包含可验证与非可验证问题的 SFT 初始化，再让两类任务分别获得不同奖励：数学/代码等由 verifier 判断，写作/对话等用成对偏好模型评分。论文报告 RL 训练不稳定，VAPO/DAPO 和流式 rollout 系统是使长链训练可持续的配套部分；奖励函数、数据采样与分布式 rollout 必须一起看。

论文报告 AIME 2024、GPQA 与 Codeforces 等结果，并在若干设置中使用 pass@8、BeyondAIME 或人评。BeyondAIME 是作者新构建的 100 道难题；其发布状态、采样次数和人评提示均影响跨模型比较。公开材料没有给出足以统一比较 DeepSeek-R1 成本或与 o3-mini-high 全面持平的同条件口径，因此这些结果不支持无条件的成本或总体排名结论。该论文更适合用于分析混合奖励和 RL 基础设施，而非仅凭排行榜判断方法优越。

---

## 三、代码模型：Seed-Coder

### 3.1 概述（2025年6月）

Seed-Coder是字节Seed团队开源的代码大语言模型系列，核心理念是**"让代码模型为自己策划数据"（Let the Code Model Curate Data for Itself）**。

**模型规模：** 8B参数
**模型变体：** Base / Instruct / Reasoning三个版本

### 3.2 核心创新：模型中心化数据管线

Seed-Coder最大的创新在于其数据处理方法——**最小化人工参与的模型中心化（Model-Centric）数据管线**：

- 主要使用LLM（而非手工规则）进行代码数据评分和过滤
- LLM能捕捉难以量化的代码质量细微标准
- 可扩展地、一致性地处理数十亿样本

**数据规模：** 6万亿（6T）tokens的代码预训练语料

**数据来源四类：**
1. **文件级代码**：来自GitHub的单个代码文件
2. **仓库级代码**：保留项目结构的代码文件
3. **Commits数据**：GitHub Commits快照，包含消息、元数据、文件和补丁
4. **代码相关网页数据**：Web归档中包含代码块或高度代码相关的文档

### 3.3 LLM质量过滤器

提出文件级评分模型，一次性过滤低质量代码文件，评估四个维度：
- **可读性（Readability）**：注释合理、命名一致、格式规范
- **模块性（Modularity）**：结构良好、避免过于复杂的函数
- **清晰度（Clarity）**：最小化冗余、清晰传达意图
- **可复用性（Reusability）**：无语法/逻辑错误、易于集成

### 3.4 训练策略

- **两阶段预训练**：
  - 常规预训练：文件级代码 + 代码相关网页数据
  - 持续预训练：全四类数据，增强长上下文能力
- **并行化管线设计**：解耦各过滤模块的顺序依赖，支持增量数据扩展
- **Fill-in-the-Middle（FIM）格式**应用于两个训练阶段

### 3.5 性能表现

Seed-Coder-8B在同规模模型中达到SOTA水平，覆盖：
- 代码生成
- 代码解释
- 代码调试
- 代码编辑
- 真实世界软件工程任务

---

## 四、语音模型

### 4.1 Seed-TTS：语音合成基础模型（2024年6月）

Seed-TTS是字节跳动发布的大规模自回归文本到语音（TTS）模型家族，论文发表于2024年6月（arXiv: 2406.02430）。

**系统架构（推理管线四阶段）：**
1. **Speech Tokenizer**：从参考语音学习tokens
2. **自回归语言模型**：基于条件文本和语音生成speech tokens
3. **Diffusion Transformer**：以粗到精方式从speech tokens生成连续语音表示
4. **声学Vocoder**：从扩散输出产生高质量语音

**技术路线：自回归 + 扩散模型的混合架构**

**核心能力：**
- **零样本语音克隆（Zero-shot In-context Learning）**：仅需少量参考语音即可克隆说话人特征
- **跨语言生成**：支持中英文互换生成，保持说话人音色
- **说话人微调（Speaker Fine-tune）**：少量数据即可生成高质量定制语音
- **情感控制**：支持愤怒、快乐、悲伤、温柔、困惑、恐惧等情感
- **语音分解（Speech Factorization）**：零样本语音转换
- **强化学习偏好对齐**：通过RL进行情感控制优化
- **全扩散语音生成**：提供纯Diffusion-based方案作为替代
- **内容编辑**：修改语音中的特定词汇而保持整体音色
- **语速编辑**：精确控制生成语音的速度

**应用场景：**
- 有声书（多说话人）
- 跨语言内容创作（带口型编辑）
- 豆包AI对话语音

**成就：** 在说话人相似度和自然度方面达到接近人类水平的性能。

### 4.2 Seed-ASR：语音识别（2024年7月）

Seed-ASR是基于大语言模型的语音识别模型，论文发表于2024年7月（arXiv: 2407.04675）。

**架构特点：**
- 基于"音频条件化LLM"框架：将连续语音表示输入LLM，结合文本指令进行转录
- 支持上下文感知（Context-Aware）识别

**上下文感知能力：**
- 对话历史上下文：利用前文对话纠正同音词
- Agent名称上下文：识别特定角色名称
- Agent描述信息：利用角色描述提升识别准确度
- 修改历史记录：学习用户纠正模式，避免重复错误
- 会议参与者名称：利用参会者列表提升人名识别

**多样性支持：**
- 多领域（直播、美食、游戏等）
- 多方言（吴语、粤语、四川话、湖南话等）
- 多口音
- 多语言（中、英、印尼语、葡萄牙语等）
- 强噪声环境

**已部署到豆包App的语音对话功能。**

### 4.3 Seeduplex：全双工语音模型

Seeduplex是Seed团队推出的原生全双工语音LLM（Native Full-Duplex Speech LLM），相比上一代豆包端到端语音模型，实现了真正的"边听边说"能力，通过预训练和对齐技术，实现低延迟语音到语音生成。

---

## 五、图像生成模型：Seedream系列

### 5.1 Seedream 3.0（2025年4月）

Seedream 3.0是字节跳动推出的高性能中英双语图像生成基础模型。

**核心特性：**
- **原生高分辨率**：支持原生高分辨率生成
- **中英双语原生支持**：深度理解中文语义
- **3秒快速生成**：面向海报设计和创意视觉，可在约3秒内生成高质量图像
- 基于Diffusion模型架构

### 5.2 Seedream 4.0（2025年下半年）

Seedream 4.0是新一代多模态图像创作模型，实现了**生成与编辑能力的统一架构整合**。

**核心创新：**
- **统一架构**：将Text-to-Image（T2I）生成和图像编辑集成在单一统一架构中
- **高分辨率支持**：最高支持4K分辨率
- **多模态输入**：支持文本、图像等多种输入条件

**技术路线：** 基于Diffusion Transformer架构

**性能：** 声称在图像生成和编辑方面超过Gemini 2.5 Flash Image（基于内部评估基准）。

### 5.3 Seedream 4.5

Seedream 4.5在4.0基础上进一步升级：
- 精确识别多张输入图像中的目标元素
- 支持可控且一致的多图像生成
- 增强的一致性保持能力

---

## 六、视频生成模型

### 6.1 PixelDance与Seaweed（2024年9月-11月）

2024年9月，字节跳动通过火山引擎发布了两款视频生成模型：

**PixelDance：**
- 增强多主体交互能力
- 流畅的角色动作
- 2024年11月在即梦AI上线

**Seaweed：**
- 多摄像机视频生成
- 与PixelDance互补的技术路线
- 采用3D Multi-modal RoPE位置编码

> 这两款模型标志着字节跳动正式进入AI视频生成竞赛。

### 6.2 Seedance 1.0（2025年6月）

Seedance 1.0是字节Seed团队的视频生成基础模型，2025年6月发布技术报告并集成到豆包和即梦平台。

**架构设计：**
- **VAE**：时序因果卷积架构（Temporally-Causal Compression）
  - 压缩比：时间4x，空间16x16
  - 潜在通道数C=48
  - 训练使用L1重建损失 + KL损失 + LPIPS感知损失 + 对抗训练损失
- **Diffusion Transformer（DiT）**：
  - 解耦空间层与时间层（Decoupled Spatial and Temporal Layers）
  - 空间层：帧内注意力 + 文本交叉注意力
  - 时间层：跨帧注意力 + 窗口分割
  - MMDiT架构（类似Stable Diffusion 3）
  - 文本编码器：基于fine-tuned decoder-only LLM
- **多镜头MM-RoPE**：支持交错的视觉/文本token序列，原生多镜头叙事
- **统一任务公式化**：通过通道拼接和二值掩码统一T2I/T2V/I2V任务
- **级联扩散框架**：Base模型生成480p → Diffusion Refiner上采样至720p/1080p

**Prompt Engineering模块：**
- 基于Qwen2.5-14B初始化
- SFT + DPO两阶段训练
- 将用户提示转换为密集视频描述

**后训练优化：**
- 精选少量高质量数据进行SFT
- 视频定制RLHF算法
- 多个奖励模型驱动的反馈学习

**推理加速：**
- 多阶段蒸馏框架
- 减少NFE（函数评估次数）
- 实现10倍以上端到端加速
- 5秒1080p视频仅需41.4秒（NVIDIA L20）

**核心特色：**
- 中英双语原生支持
- 综合生成能力：运动流畅性、物理合理性、真实感
- 精确指令遵循：多主体交互、自适应相机控制
- 原生多镜头叙事能力

### 6.3 Seedance 1.5 Pro（2025年12月）

Seedance 1.5 Pro在即梦网页版上线，核心升级为**音画同步视频生成**：
- 独家音频-视频联合生成技术
- 人物口型同步
- 乐器演奏同步
- 自然音效对齐

### 6.4 Seedance 2.0（2026年2月）

Seedance 2.0 的报告将任务接口扩展为文本、图像、视频和音频组合输入，并覆盖参考生成、编辑、延展与音视频输出。相对 Seedance 1.0，公开可比较的是任务和评测范围变宽；报告未披露足以重建主干的网络图、tokenizer 或完整训练配方。论文中的 SeedVideoBench 2.0 结果为作者报告，依赖其提示集、评审方式和任务定义，不据此宣称跨模型的无条件领先。

### 6.5 产品接口与模型边界

豆包、即梦、剪映和火山引擎分别提供消费应用、创作界面或 API 入口。产品支持某种生成工作流，只能确认用户接口；没有技术报告时，不据此推断底层权重、训练数据或模型架构相同。

---

## 七、多模态理解模型

### 7.1 Seed1.5-VL（2025年5月）

Seed1.5-VL是字节Seed团队的视觉语言基础模型，设计目标是推进通用多模态理解与推理。

**架构：**
- **视觉编码器**：532M参数
- **LLM主干**：MoE架构，**20B激活参数**
- 相对紧凑的架构实现顶级性能

**能力覆盖：**
- 通用多模态理解与推理
- GUI控制/Agent能力
- 视频理解
- 多种视觉推理任务SOTA

**开源发布：** GitHub（ByteDance-Seed/Seed1.5-VL）

### 7.2 BAGEL：统一多模态基础模型（2025年5月）

BAGEL是字节Seed团队开源的统一多模态基础模型，支持理解与生成的统一。

**模型规格：**
- 7B激活参数（14B总参数）
- 基于大规模交错多模态数据训练
- 预训练从LLM初始化

**核心能力：**
- **统一理解与生成**：单一模型同时支持多模态理解和图像生成
- 支持文本、图像的统一处理
- 图像生成与编辑
- 图像理解与推理

**架构创新：** 论文标题"Emerging Properties in Unified Multimodal Pretraining"揭示了统一多模态预训练中涌现的属性。

**开源地址：** GitHub（ByteDance-Seed/BAGEL）

### 7.3 Seed1.8：通用Agent模型（2026年3月）

Seed1.8定位为"面向通用现实世界Agent能力"的基础模型。

**设计理念：**
- 超越单轮预测，支持多轮交互和任务执行
- 保留核心LLM和VLM能力的同时扩展Agent能力
- 工作流导向的MaaS（Model-as-a-Service）基础

**能力特征：**
- 支持文本和图像输入
- 强大的工具调用能力
- 多步骤高精度任务执行
- 标准LLM/VLM基准保持竞争力
- 推理、复杂指令遵循、知识任务表现优异

**应用方向：**
- 网页浏览自动化
- 终端操作
- 真实世界多轮任务

**开源发布：** GitHub（ByteDance-Seed/Seed-1.8）

### 7.4 Seed-X：多语言翻译模型（2025年）

值得注意的是，"Seed-X"这一名称在字节体系中指代的是多语言翻译LLM系列（而非早期传闻的通用多模态模型）：
- 7B参数规模
- 包含Instruct和Reasoning模型
- 推进翻译能力的极限
- 开源发布（含奖励模型Seed-X-RM-7B）

---

## 八、跨线综合：共享的是研究问题，不是已证实的统一架构

前面各方向并非从同一个“Seed 旗舰底座”单向派生。论文和官方技术材料显示的联系，更适合按训练问题与反馈信号来比较：

| 研究问题 | 代表工作与机制 | 与其他支线的关系 | 证据边界 |
|---|---|---|---|
| 如何以有限激活计算扩展能力？ | [Doubao-1.5-pro 技术材料](https://seed.bytedance.com/en/blog/doubao-1-5-pro)称采用稀疏 MoE；[Seed-Thinking-v1.5](https://arxiv.org/abs/2504.13914) 报告 200B 总参/20B 激活；[Seed1.5-VL](https://arxiv.org/abs/2505.07062) 报告 532M 视觉编码器与 20B 激活 MoE LLM | 语言推理和 VLM 都采用稀疏计算，但主干、输入表示和目标任务不同；Seedream/Seedance 的 DiT 生成线不能一并归为 MoE | Seed 2.0 的模型卡没有公开完整架构，不能从旧代推断；稀疏参数不直接等于端到端低延迟 |
| 数据怎样从通用规模转向任务质量？ | [Seed-Coder](https://arxiv.org/abs/2506.03524) 用模型质量打分器筛代码文件，并在 sandbox 中验证部分样本；[Seedance 1.0](https://arxiv.org/abs/2506.09113) 区分动态/静态视频 caption；[Seedream 3.0](https://arxiv.org/abs/2504.11346v3) 用缺陷感知采样及审美/文字 caption | 三者都将数据处理与目标能力绑定，但“数据质量”由不同任务的过滤器、描述和验收方式具体定义，不是一条统一数据引擎 | Seed-Coder 的质量打分器使用 DeepSeek-V2-Chat 作为 oracle 给约 22 万文件打标签；这不是用外部模型输出作预训练目标，但也不能表述为全链路无外部模型参与。团队“不用他模数据”的声明需限定具体模型/训练阶段 |
| RL 适合哪些任务，奖励如何定义？ | [Seed-Thinking-v1.5](https://arxiv.org/abs/2504.13914) 区分可验证问题的 verifier 与非可验证问题的成对生成式 reward；[Seedance 1.0](https://arxiv.org/abs/2506.09113) 组合对齐、运动、美学 reward；[Seedream 2/3](https://arxiv.org/abs/2503.07703) / [Seedream 3.0](https://arxiv.org/abs/2504.11346v3) 分别使用 CLIP 与 VLM reward | 数学/code 可用答案或执行结果验证；视觉/语音偏好需要人评、模型判别器或代理指标。Seed-TTS 的 RL 目标还须单独看 §4 | 共用“RL”名词不代表同一算法、奖励或可比结果；验证器准确度、偏好数据和生成预算各自影响结论 |
| 理解与生成能否统一？ | [BAGEL](https://arxiv.org/abs/2505.14683) 用两个 Transformer experts、不同视觉编码器，但共享多模态 self-attention；[Seedream 4.0](https://arxiv.org/abs/2509.20427v3) 联合 T2I/编辑；[Seedance 2.0](https://arxiv.org/abs/2604.14148v1) 报告扩展视听任务接口、内部架构披露不足 | “统一”分别指跨模态理解/生成共享上下文、同一图像 DiT 联合多项任务、以及视听输入输出覆盖，不是同一个架构转移 | [Seed 2.0 模型卡](https://arxiv.org/abs/2607.00248v1) 未公开足以重建网络的架构细节，不能用“原生多模态”描述补齐 tokenizer、主干或训练流程 |
| 效率瓶颈在哪一层？ | [UltraMem](https://arxiv.org/abs/2411.12364) 比较超稀疏 memory 与 MoE 的推理内存访问；Doubao-1.5-pro 技术材料披露 PD 分离/量化；Seedance 1.0 把模型蒸馏和系统优化分开讨论 | UltraMem 着眼于专家/记忆访问，PD 分离与量化针对 serving 资源，视频蒸馏减少去噪步数；是三类不同瓶颈 | 局部加速依赖硬件、batch、序列长度和服务栈，不应把倍数相乘或外推到其他模型 |

这几条线可以合成一条研究路线：模型先通过专门数据和表示学会特定模态，再以 SFT/RL 等后训练把能力约束到可执行或可感知的目标，最后通过系统工程将推理开销降到可部署范围。它们共享“数据—表征—反馈—推理系统”的设计问题；公开证据尚不足以证明它们共享同一预训练底座或全线一体化训练管线。

## 九、阅读主线与未闭合问题

建议按问题而非产品家族阅读：

1. **模型如何学推理？** Seed-Thinking-v1.5 的数据、双轨 reward、SFT/RL 及流式 rollout；与 GLM-Z1、DeepSeek-R1 等比较时，先固定 verifier、采样次数和 pass@k 条件。
2. **代码能力怎样进入 Agent 环境？** Seed-Coder 的数据筛选/执行验证，与 Seed1.8 的通用行动接口不是同一目标；查看代码任务、仓库任务和 GUI 操作的输入工具差异。
3. **多模态表示要不要统一？** Seed1.5-VL 的 VLM 训练、BAGEL 的理解/生成共享结构、Seedream 的任务专用扩散、Seedance 的视频扩散分别代表不同选择；把“模型家族统一”与“单模型统一”区分开。
4. **生成任务如何利用偏好？** Seedream 优化图文/审美/文字维度，Seedance 专门建视频运动与视觉 reward，语音模型关注韵律与音色；检查 reward 标注方式和任务覆盖，不能只看整体分数。

仍未闭合的问题包括：不同方向是否共享预训练表示或只共享训练基础设施；AI 生成的合成数据在长尾概念上是否造成反馈环；统一多模态模型相比专用生成器的能力互扰；长视频/长程 Agent 的闭环评测如何纳入任务预算和失败恢复。ByteDance Seed 作者参与的 [Periodic Weak Spots](https://arxiv.org/abs/2609.36322v1) 在 DeepSeek-V4 上展示 chunked KV-cache 的检索位置敏感性，提示长上下文评测还应改变目标相对压缩块的位置；它不是 Seed 模型实验，不证明 Seed 系列采用相同缓存压缩机制。关于 Seed2.0 架构、完整训练流程及 Seedance 2.0 内部生成主干，公开材料仍不足，需保持未知。

豆包 App、即梦和火山引擎是模型的产品/服务入口，不能单凭集成关系推断模型权重共享或研究路线。产品状态与价格不构成本报告的跨线技术证据。

---

## 参考文献

1. ByteDance Seed Team. "Seed-TTS: A Family of High-Quality Versatile Speech Generation Models." arXiv:2406.02430, 2024.

2. ByteDance Seed Team. "Seed-ASR: Understanding Diverse Speech and Contexts with LLM-based Speech Recognition." arXiv:2407.04675, 2024.

3. ByteDance Seed Team. "Seed-Thinking-v1.5: Advancing Superb Reasoning Models with Reinforcement Learning." arXiv:2504.13914, 2025.

4. ByteDance Seed Team. "Seed-Coder: Let the Code Model Curate Data for Itself." arXiv:2506.03524, 2025.

5. ByteDance Seed Team. "Seed1.5-VL Technical Report." arXiv:2505.07062, 2025.

6. ByteDance Seed Team. "Emerging Properties in Unified Multimodal Pretraining (BAGEL)." arXiv:2505.14683, 2025.

7. ByteDance Seed Team. "Seedance 1.0: Exploring the Boundaries of Video Generation Models." arXiv:2506.09113, 2025.

8. ByteDance Seed Team. "Seedream 3.0 Technical Report." arXiv:2504.11346, 2025.

9. ByteDance Seed Team. "Seedream 4.0: Toward Next-generation Multimodal Image Generation." arXiv:2509.20427, 2025.

10. ByteDance Seed Team. "Seed1.8 Model Card: Towards Generalized Real-World Agency." arXiv:2603.20633, 2026.

11. ByteDance Seed Team. "Seed2.0 Model Card: Towards Intelligence Frontier for Real-World Applications." Technical Report, 2026.

12. ByteDance Seed Team. "Ultra-Sparse Memory Network (UltraMem)." ICLR 2025. arXiv:2411.12364.

13. ByteDance Seed Team. "Doubao-1.5-pro Technical Blog." seed.bytedance.com, January 2025.

14. ByteDance Seed Team. "Seedance 2.0." seed.bytedance.com, 2026.

15. ByteDance Seed Team. "Seeduplex: Native Full-Duplex Speech LLM." research.doubao.com, 2025.

---
