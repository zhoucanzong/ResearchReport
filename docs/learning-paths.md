# 跨领域学习路线

这份地图把图书馆中已有的主报告连成几条阅读路线，帮助读者从一个问题走到相邻领域。它是导航，不是新的综述，也不代表各方向构成单一、连续的方法谱系。每条路线都应回到专题报告理解机制、论文证据与适用边界。

## 1. 语言模型能力如何形成

**训练数据 → 模型系列中的训练披露 → 对齐目标 → 强化学习更新 → 推理时计算**

推荐顺序：[训练数据策展](../LLM/TrainingData/report.md) → 选择 [DeepSeek](../Models/DeepSeek/report.md) 或 [MiMo](../Models/MiMo/report.md) 中公开训练信息较多的路线作案例 → [模型对齐与后训练](../LLM/Alignment/report.md) → [LLM 强化学习](../LLM/ReinforcementLearning/report.md) → [推理模型与测试时计算](../LLM/ReasoningModels/report.md)。

沿途要区分：数据构成影响模型学到什么；偏好优化定义哪些输出更可取；强化学习描述策略如何依据反馈更新；测试时计算则是在推理阶段分配搜索或采样预算。它们有关联，但发生在不同阶段，报告披露程度也不相同；厂商系列报告只能作为各自公开证据下的案例。

## 2. 语言模型怎样成为行动系统

**推理与规划 → 工具调用 → 界面操作或权限边界 → 任务验收**；进入物理环境时再接到 **VLA 闭环控制**。

推荐顺序：[推理模型与测试时计算](../LLM/ReasoningModels/report.md) → [智能体系统](../Agents/AgentSystems/report.md) → 按问题读 [电脑使用 Agent](../Agents/ComputerUse/report.md) 或 [工具 Agent 安全](../Agents/AgentSecurity/report.md) → [评测科学](../Evaluation/EvaluationScience/report.md)。若关注真实机器人动作与环境反馈，转读[具身 VLA](../WorldModel/EmbodiedVLA/report.md)。

这条路线从文本中的中间推理走向外部动作。网页/桌面任务的状态变化、工具权限和终态验收，与机器人策略的连续控制、传感反馈和 sim-to-real 不是同一种评测对象；Agent 能完成数字任务不能直接推出它具备物理闭环能力。

## 3. 扩散语言模型与投机解码中的“扩散”

先读[扩散语言模型](../LLM/DiffusionLM/report.md)，再读[投机解码](../Infra/SpeculativeDecoding/report.md)，最后看 [Nemotron-Labs-Diffusion](../OpenSource/nemotron/report.md) 作为具体方案案例。

关键是分清两种角色：扩散语言模型把去噪过程作为模型自身的生成机制；投机解码通常让草稿器为自回归目标模型提出候选，再由目标模型验证，以减少串行解码开销。它们可以共享并行生成或噪声建模等工具，但目标、正确性保证和系统瓶颈并不相同。

## 4. 从模型架构走到推理系统

**稀疏模型结构 → 专家通信与执行 → KV 状态管理 → 服务调度和评测 → 固定源码实现**。

推荐顺序：[混合专家模型](../LLM/MoE/report.md) → [MoE 执行](../Infra/MoEExecution/report.md) → [KV Cache 与 Prefill/Decode 分离](../Infra/KVCachePD/report.md) → [在线推理服务与评测](../Infra/ServingEvaluation/report.md) → 按实现问题阅读 [DeepInfer](../OpenSource/DeepInfer/report.md)、[vLLM](../OpenSource/vllm/report.md) 或 [SGLang](../OpenSource/sglang/report.md) → 回到[评测科学](../Evaluation/EvaluationScience/report.md)理解指标和负载条件。

阅读时追踪同一请求经过的资源与状态：路由决定计算落在哪些专家，执行系统决定通信和批处理如何发生，KV 管理影响内存与数据移动，服务评测再决定吞吐、延迟和请求完成如何被计量。论文中的算法收益不能自动等同于真实服务收益；实现报告也只支持其固定版本中能定位到的行为。

## 5. 训练状态、量化表示与部署格式

若问题从训练集群开始，先读[训练基础设施](../Infra/TrainingInfra/report.md)中的状态分片与 FSDP2 生命周期，再看其 [PyTorch FSDP 原论文精读](../Infra/TrainingInfra/papers/2304.11277-pytorch-fsdp.md)，区分论文中的 FSDP1 设计与当前固定版本的 FSDP2 实现；接着比较同一报告中的 GPipe、1F1B、Zero Bubble 与 DualPipe，理解流水线空泡、梯度更新语义和激活生命周期。若问题从模型压缩开始，读[量化专题](../Infra/QuantizationEdge/report.md)：先对照 GPTQ/AWQ 的后训练标量量化，再按需求进入旋转、向量码本、KV cache、QAT 或原生低精度训练。

这里连接的是两个不同阶段的问题：FSDP2 主要安排训练状态如何分布和参与计算；量化方法改变参数、激活或 KV 状态的数值表示。QAT 还要区分“适配已有模型”与“从头训练低位宽模型”。最后回到[在线推理服务与评测](../Infra/ServingEvaluation/report.md)，检查压缩后的表示是否有匹配格式、kernel 和评测工作负载；低位宽本身不保证端到端服务加速。

## 6. 图像生成机制、控制与厂商系统

推荐顺序：[图像生成](../AIGC/ImageGeneration/report.md)建立问题地图 → [扩散模型](../AIGC/DiffusionModels/report.md)理解生成目标与采样 → [DiT](../AIGC/DiT/report.md)理解 Transformer 去噪骨干 → 按任务转向[可控生成](../AIGC/ControllableGen/report.md)或[图像编辑](../AIGC/ImageEditing/report.md)。之后可选读 [OpenAI](../Models/OpenAI-Gen/report.md)、[Google](../Models/Google-Gen/report.md)、[DeepSeek](../Models/DeepSeek/report.md) 等模型系列报告，观察公开系统如何落在这些问题上。

机制专题回答“方法怎样工作”，厂商报告回答“某系列公开了什么研究或产品证据”；后者不能代替未公开实现的机制说明。遇到提示遵循、空间关系、文字渲染、主体一致性或编辑保留等具体问题，应回到相应任务的实验与评测条件，而不是由模型名称推断能力。

## 7. AI for Science：从候选生成到可信发现

先选一个具体科学问题，例如[蛋白质 binder 设计](../AI4Science/ProteinDesign/report.md)、[材料发现](../AI4Science/MaterialsDiscovery/report.md)或[化学反应优化](../AI4Science/Chemistry/report.md)；再读[自主实验室](../AI4Science/AutonomousLabs/report.md)理解实验闭环，按需补[大模型辅助运筹建模与求解](../LLM/OperationsResearch/report.md)中的约束表达、求解器反馈与算法搜索；最后读[科学发现的评测方法](../Evaluation/ScientificDiscovery/report.md)。

这些专题共同关心预测或候选如何变成可检验结果，但不同学科的实验对象、成本和有效性判据差异很大，不能把它们压成统一方法排行榜。评估证据可从回顾性数据、前瞻预测、真实实验到机制干预逐步理解；模型分数提升本身不等于发现了新规律。

---

路线依据图书馆当前报告中的交叉链接和研究范围整理。新增或重组专题后，应同步检查路线的入口、顺序和边界是否仍成立。
