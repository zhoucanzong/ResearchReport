# 选文说明与候选池 · EmbodiedVLA

> 目的：**先筛选、后精读**。本页保留原始 8 篇基线、2026-10-23 闭环控制批次与世界模型迁移批次的候选、入选理由和排除理由，便于后续只针对新增证据重新筛选。
> 证据纪律：本页只做**选文判断**，不含未精读论文的结论。**下表出现的每一个 arXiv ID 与标题都已逐条回查 `arxiv.org/abs/<id>` 核实**（题名 + 版本 + `published` 日期）；**凡未核实的条目一律不给 ID**，只做类别性说明——**排除项不得编造 ID**。

## 1. 本条目要回答什么（决定了选文标准）

`EmbodiedVLA` 关心的不是"所有机器人学习论文"，而是**"以视觉 + 自然语言指令为条件、直接输出可执行动作信号的策略模型"**这条线。据此分三问筛选：

- **(a) 有没有动作输出？**（必需：关节/末端位姿/夹爪信号）
- **(b) 有没有语言条件化？**（必需：自然语言指令，而非任务 ID / one-hot）
- **(c) 它在这个领域的"轴"上占什么位置？**——动作表征（token / flow matching / diffusion head）｜系统与规模（是否基线）｜数据（真机 / 仿真、规模与许可）｜评测（协议与可比性）

**入选门槛（满足其一）**：提出新机制或新范式 ｜ 首次在某能力上成立且有规模证据 ｜ 成为后续工作的基线或数据/评测基础设施 ｜ 证伪或纠正已有共识。
**淘汰标准（命中其一）**：增量调参无新机制 ｜ 只在玩具设置验证或无消融 ｜ 已被后续工作取代 ｜ 与本条目主题仅擦边 ｜ **拿不到正文（只有摘要）**。

## 2. 入选（8 篇，逐篇一句入选理由）

> 8 篇**全部为 `[精读原文]`**（正文提取文本完整通读，数字逐个回原文核对）。版本与日期见 [MANIFEST.md](MANIFEST.md)。

| # | 分册 | arXiv ID | 入选理由（一句话） |
| --: | :-- | :-- | :-- |
| 1 | [`papers/2303.04137-diffusion-policy.md`](<../papers/2303.04137-diffusion-policy.md>) | `2303.04137` | **diffusion head 路线的定义性工作**：把 visuomotor policy 表述为条件去噪扩散过程，是"动作表征三路线"里第三条的源头与后续 VLA 动作头的技术来源 |
| 2 | [`papers/2307.15818-rt2.md`](<../papers/2307.15818-rt2.md>) | `2307.15818` | **范式的确立点**：首次把动作写成文本 token 与网络规模 VLM **联合微调**，本条目判据 (a)(b)(c) 的历史锚点 |
| 3 | [`papers/2310.08864-open-x-embodiment.md`](<../papers/2310.08864-open-x-embodiment.md>) | `2310.08864` | **数据基础设施与"跨机器人正迁移"的证据**：统一数据格式 + RT-X 模型，是后续几乎所有 VLA 预训练的语料来源 |
| 4 | [`papers/2406.09246-openvla.md`](<../papers/2406.09246-openvla.md>) | `2406.09246` | **开源强 VLA 的基线**：7B 开源主干 + 每维 256-bin 离散 token，让"token 路线"第一次可被第三方复现与对比 |
| 5 | [`papers/2410.24164-pi0.md`](<../papers/2410.24164-pi0.md>) | `2410.24164` | **flow matching 路线的代表**：在预训练 VLM 上加 action expert，用流匹配做高频灵巧动作 chunk，正确立的当前主流动作头 |
| 6 | [`papers/2501.09747-fast.md`](<../papers/2501.09747-fast.md>) | `2501.09747` | **给 token 路线续命的关键技术**：频率域动作 tokenizer 解决"逐维逐时刻分箱在高频灵巧数据上表现差"，回答"token 路线还能不能用于高频任务" |
| 7 | [`papers/2403.12945-droid.md`](<../papers/2403.12945-droid.md>) | `2403.12945` | **真机数据规模与采集标准化的代表**：76k episodes / 564 场景 / 13 机构的 in-the-wild 数据集，是"数据从哪来、边界在哪"的必读锚点 |
| 8 | [`papers/2405.05941-simpler.md`](<../papers/2405.05941-simpler.md>) | `2405.05941` | **评测方法论的代表**：主张"仿真只需真实到让策略**排序**与真机一致"，是"真机 vs 仿真能不能互相替代"的正方证据；与 π0.5 的反方证据成对 |

### 2.1 入选结构自检（避免选文偏斜）

| 维度 | 覆盖 |
| :-- | :-- |
| 动作表征路线 | token：2、4、6 ｜ flow matching：5 ｜ diffusion head：1 ｜（7、8 为非策略本体） |
| 系统 vs 基础设施 | 策略本体：1、2、4、5、6 ｜ 数据：3、7 ｜ 评测：8 |
| 真机 vs 仿真 | 真机为主：2、4、5、6、7 ｜ 仿真评测：8 ｜ 真机+仿真：1 |
| 弱 VLA 判例（R3） | 由 1 作为 R2 边界样本、2 作为强 VLA 起点提供 |

## 3. 排除清单（19 条：13 条带**已核实 ID**，6 条为类别性排除）

### 3.1 带已核实 ID 的排除（13 条）

> 下列论文**本轮未精读**（未通读正文）。理由仅为**选文判断**（主题分布、代际关系、与本条目判据的关系），**不构成对其质量的评价**。ID / 版本 / 日期 / 标题均取自 arXiv 元数据回查结果。

**A. 被后继工作取代或本轮以后继为准（4 条）**

| # | arXiv ID（已核实） | 论文（arXiv 题名） | 排除理由（一句话） |
| --: | :-- | :-- | :-- |
| 1 | `2212.06817`（v2, 2022-12-13） | RT-1: Robotics Transformer for Real-World Control at Scale | 本条目以 RT-2 作为"范式确立点"；RT-1 无网络规模 VLM 初始化，作为**弱 VLA 判例**在 RT-2 分册与 `report.md` 判据章内交代即可，无需重复设册 |
| 2 | `2405.12213`（v2, 2024-05-20） | Octo: An Open-Source Generalist Robot Policy | 通用策略，但主干非网络规模 VLM、动作头为 diffusion head 的同族应用；其机制位置已被 Diffusion Policy（1）与 π0（5）覆盖 |
| 3 | `2409.12514`（v5, 2024-09-19） | TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation | 轻量化/数据高效路线的增量工作，未提出可判定的新机制；"小模型 VLA"作为 `report.md` 选型章的一句话登记 |
| 4 | `2410.13126`（v1, 2024-10-17） | ALOHA Unleashed: A Simple Recipe for Robot Dexterity | 双臂灵巧的工程配方；动作表征无新范式，数据侧位置由 DROID（7）与 π0 分册的灵巧任务吸收 |

**B. 属于"评测/数据环境"，按本条目 R6 只作环境引用、不设分册（5 条）**

| # | arXiv ID（已核实） | 论文（arXiv 题名） | 排除理由（一句话） |
| --: | :-- | :-- | :-- |
| 5 | `2306.03310`（v2, 2023-06-05） | LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning | 是**基准**而非 VLA 本体（本条目 R6）；其评测维度是任务间迁移，与真机成功率不可直接比较——写入「评测/数据集」专题册的对照表 |
| 6 | `2406.02523`（v1, 2024-06-04） | RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots | 仿真环境/数据生成平台（R6）；评测协议位置在专题册交代，不占精读名额 |
| 7 | `2404.05695`（v2, 2024-04-08） | Humanoid-Gym: Reinforcement Learning for Humanoid Robot with Zero-Shot Sim2Real Transfer | 人形 sim-to-real 的 RL 工程工作，**无语言条件化**（违反判据 (b)）——按 R2 排除，只作"仿真到真机"的邻域对照 |
| 8 | `2407.07726`（v2, 2024-07-10） | PaliGemma: A versatile 3B VLM for transfer | **VLM，无动作输出**（违反判据 (c)）；它是 π0 的视觉-语言主干，属上游组件，归 `LLM/VLM` 条目 |
| 9 | `2401.02117`（v1, 2024-01-04） | Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation | 数据采集**硬件与遥操作系统**，非语言条件化策略本身（R2）；数据侧位置写在「评测/数据集」专题册与 π0 分册 |

**C. 相邻领域 / 归属按交付物拆分（2 条）**

| # | arXiv ID（已核实） | 论文（arXiv 题名） | 排除理由（一句话） |
| --: | :-- | :-- | :-- |
| 10 | `2506.21539`（v1, 2025-06-26） | WorldVLA: Towards Autoregressive Action World Model | **联合模型**：按本条目 R5 拆交付物——world 分支归 `WorldModels`（该条目已设分册），本条目只登记其动作分支，不重复精读 |
| 11 | `2502.13130`（v1, 2025-02-18） | Magma: A Foundation Model for Multimodal AI Agents | 多模态 agent 基础模型，动作侧不输出机器人动作信号——按 R1 不入 VLA，归 `LLM/VLM` / Agent |

**D. 综述类：不作为事实来源，故不给精读名额（2 条）**

| # | arXiv ID（已核实） | 论文（arXiv 题名） | 排除理由（一句话） |
| --: | :-- | :-- | :-- |
| 12 | `2505.04769`（v2, 2025-05-07） | Vision-Language-Action (VLA) Models: Concepts, Progress, Applications and Challenges | 综述：可用于**定位术语与检索线索**，但其转述不能作为一手事实，本条目 `[受限核验]` 登记，不设分册 |
| 13 | `2412.14058`（v4, 2024-12-18） | What Matters in Building Vision-Language-Action Models for Generalist Robots | 偏"设计要素对比"的分析性工作；其结论属对他人系统的二次比较，**本轮未逐条回一手核实**，故不作事实来源 |

### 3.2 类别性排除（6 条，**未逐一核实 ID，故不给 ID**）

| # | 类别 | 排除理由（一句话） |
| --: | :-- | :-- |
| 14 | **闭源强 VLA 的官方报告**（如大型厂商的机器人基础模型报告） | 只发布博客/演示、**拿不到可供逐字核对的方法细节与消融**；命中淘汰标准"拿不到正文"。列为跟踪对象，不设分册 |
| 15 | **VLA 的复现 / 批评 / 基准横评**类工作 | 属对已有结论的检验；其要点将作为**证据**写入入选分册的"失效边界"与「评测/数据集」专题册，单独设册会重复 |
| 16 | **纯动作表征的消融研究**（只改 tokenizer / 只改 bin 数） | 变量单一、无新机制；其变量已被 FAST 分册（6）的消融章覆盖 |
| 17 | **自动驾驶 / 导航领域的语言条件策略** | 语言条件化弱、动作空间与操作类 VLA 不同源；归 `WorldModels` 与导航条目，本条目仅登记边界 |
| 18 | **2026 年新增的 VLA 增量工作**（多篇） | 多为在既有动作头上换主干/换数据的增量改进，**未提出可判定的新机制**；等形成新判据再按本页门槛重筛 |
| 19 | **仅发布在项目页 / 预印本平台而无稳定标识的工程报告** | 无法给出可复核的 ID 与版本日期，违反引用纪律，不作为来源 |

## 4. 历史统计口径（原始批次 + 闭环控制批次）

- 原始批次 **27 = 入选 8 + 排除 19**；2026-10-23 闭环控制批次新增 4 个候选，3 个设分册、1 个边界排除，使当时合计为 **31 = 入选 11 + 排除 20**。世界模型迁移批次的累计数字见 §6.3；
- **ID 纪律**：3.1 的 13 个 ID + 版本 + 日期 + 题名**已逐条回查 arXiv 元数据**；3.2 是类别性排除，**不给 ID、不编造 ID**；
- **精度纪律**：原始 + 闭环批次入选的 11 篇各有独立分册（`papers/*.md`），每篇开头含「亮点与差异」四行并展开七问；11 篇**主等级均为 `[精读原文]`**；
- 本页与 [MANIFEST.md](MANIFEST.md) 配套：**清单一手核实、全文不入库**。

---

## 5. 2026-10-23 补充批次：闭环控制与 VLA

> 本批次从四个候选中精读三篇，按“闭环修改了什么”而非按模型新旧筛选。版本、实验数字与真机/仿真归属见对应分册与 [闭环控制专题](../topics/closed-loop-control.md)。

### 5.1 入选三篇

| # | 分册 | arXiv ID / 当前版本 | 入选理由（一句话） |
| --: | :-- | :-- | :-- |
| 20 | [`papers/2511.14759-pi-star-0.6-recap.md`](<../papers/2511.14759-pi-star-0.6-recap.md>) | `2511.14759v2`，2025-11-19 | **跨 episode 真机 VLA 学习的直接证据**：advantage conditioning 把自主轨迹、稀疏成功信号和专家纠正纳入更新；真双臂长时程任务给出吞吐与失败变化。 |
| 21 | [`papers/2608.16978-vlcp.md`](<../papers/2608.16978-vlcp.md>) | `2608.16978v1`，2026-08-17 | **单 episode 代码级恢复机制**：匹配 open-loop 对照并统计失败抓取恢复率，机制独立；明确仅仿真，故不能据此宣称真机提升。 |
| 22 | [`papers/2601.21998-lingbot-va.md`](<../papers/2601.21998-lingbot-va.md>) | `2601.21998v2`，2026-03-22 | **世界模型滚动与实际观测接地**：区分同步、异步和 FDM-grounded async，兼有仿真消融与六项真机任务。 |

### 5.2 边界排除一篇

| 候选 | arXiv ID / 当前版本 | 排除理由 |
| :-- | :-- | :-- |
| *VersualRL: Closed-Loop Verbal Reinforcement Learning with Visual Execution Feedback for Task-Level Robot Planning* | `2603.22169v3`，2026-07-19 | **任务层策略而非本文定义的 VLA 本体**：真实移动机器人上确有跨 episode Behavior Tree refinement，值得作为边界案例；但 actor 修改符号树，不接收低层视觉流，也不直接输出机器人动作。故在闭环专题用短段登记，不另设精读分册或与真 VLA success rate 比较。 |

### 5.3 口径与数量

- 本轮 4 个对象均回查 arXiv abs 页的题名、当前版本与日期；VersualRL 的原文题名为 **VersualRL**（不是 Verbal-RL）。
- 新增三篇分册均含固定版本、四行「亮点与差异」、七问及原文图表锚点；详细数字和实验边界不得脱离分册条件引用。
- 到闭环控制批次为止：候选池累计 `27 + 4 = 31`；累计入选 `8 + 3 = 11`；累计排除 `19 + 1 = 20`。后续世界模型迁移批次见 §6.3。

---

*原筛选说明编制时间：2026-10-17 ｜ 补充批次核验时间：2026-10-23。arXiv 元数据逐条回查；全文由 PaperFetcher PDF 抽取或 arXiv 全文 HTML 核读。*

---

## 6. 2026-10-23 补充批次：世界模型数据与 VLA 真机迁移

> **研究问题**：合成示范、世界模型中的 imagined RL、或经过物理验证的生成轨迹，分别在什么条件下改善真实机器人策略？本批候选池 **20 篇**；选择 5 篇精读，另 15 篇作为不同方法角色或证据边界排除出核心分册。筛选优先看真机结果、机制归属能否由消融/对照区分，以及完整原文是否足以回答七问。

### 6.1 入选精读（5 篇）

| # | 分册 | arXiv ID / 固定版本 | 入选理由 |
| --: | :-- | :-- | :-- |
| 1 | [`papers/2610.11248-simvla.md`](<../papers/2610.11248-simvla.md>) | `2610.11248v1`，2026-10-08 | **全仿真合成监督与移动操作真机迁移**：同一系统组合动作轨迹、特权视觉问答、策略部署轨迹，并做 2,120 次真机评估；能检验“simulation-only”具体排除了哪些真实采集。 |
| 2 | [`papers/2610.13164-grounded-dreamer.md`](<../papers/2610.13164-grounded-dreamer.md>) | `2610.13164v1`，2026-10-09 | **用物理回放过滤视频世界模型伪动作**：直接对照真机与合成训练数据，区分视觉逼真、动作标签和物理可执行性。 |
| 3 | [`papers/2602.12063-vlaw.md`](<../papers/2602.12063-vlaw.md>) | `2602.12063v2`，2026-02-15 | **合成 rollouts 是否增加真实策略能力**：真实失败轨迹校准模拟器、生成成功候选，再与真实成功轨迹混合微调；含数据量与真机 rollout 消融。 |
| 4 | [`papers/2602.06508-world-vla-loop.md`](<../papers/2602.06508-world-vla-loop.md>) | `2602.06508v2`，2026-05-25 | **把 RL 放进视频世界模型**：SANS 近成功数据、生成器内生奖励和策略—模拟器共演化形成完整训练环；报告了两项真机任务，但真机样本规模有限。 |
| 5 | [`papers/2602.13977-wovr.md`](<../papers/2602.13977-wovr.md>) | `2602.13977v2`，2026-06-27 | **显式控制 imagined RL 的模型幻觉**：关键帧初始化与策略对齐更新分别处理长 horizon 误差和分布漂移，并在两个机械臂平台上进行真机测试。 |

### 6.2 相邻机制：不另设分册（15 篇）

| # | arXiv ID / 当前版本与日期 | 论文 | 本批处理 |
| --: | :-- | :-- | :-- |
| 6 | `2511.09515v1`，2025-11-12 | [WMPO: World Model-based Policy Optimization for VLA Models](https://arxiv.org/abs/2511.09515) | 想象轨迹上的 VLA on-policy RL，留作 WoVR 比较基线；WoVR 对模型稳定性与 rollout 起点作了更直接的机制分解。 |
| 7 | `2505.12705v2`，2025-06-17 | [DreamGen: Unlocking Generalization in Robot Learning through Video World Models](https://arxiv.org/abs/2505.12705) | 多本体的视频合成轨迹路线；与本批 Grounded-Dreamer 的伪动作和物理验证问题重叠，保留为历史对照，不在本批重复设册。 |
| 8 | `2606.31101v1`，2026-06-30 | [Efficient Sim-to-Real Transfer of World-Action Models from Synthetic Priors](https://arxiv.org/abs/2606.31101) | 四任务、每任务约 800 仿真轨迹、Franka 真机平均成功率 35%；作者称早期结果且未做可归因于联合视频—动作目标的受控消融，登记为狭义可行性证据。 |
| 9 | `2506.00613v3`，2025-09-30 | [WorldGym: World Model as an Environment for Policy Evaluation](https://arxiv.org/abs/2506.00613) | 世界模型作**评测器**而非训练源；其与真机的相关性进入本专题评测边界，技术报告仍见 Evaluation 交叉链接。 |
| 10 | `2607.02642v1`，2026-07-02 | [GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation](https://arxiv.org/abs/2607.02642) | 以世界模型基准和评测设计为中心，不是策略训练/迁移证据；归入 Evaluation 的候选池。 |
| 11 | `2601.16163v1`，2026-01-22 | [Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning](https://arxiv.org/abs/2601.16163) | 视频模型直接生成动作并用于 test-time planning；属于候选规划器路线，非生成式模拟器扩充 VLA 训练数据。 |
| 12 | `2602.15922v1`，2026-02-17 | [World Action Models are Zero-shot Policies](https://arxiv.org/abs/2602.15922) | DreamZero 将未来视频与动作联合建模为直接控制策略；不是本文所比的 learned simulator / synthetic-rollout training。 |
| 13 | `2502.00622v4`，2026-03-11 | [Inference-Time Enhancement of Generative Robot Policies via Predictive World Modeling](https://arxiv.org/abs/2502.00622) | GPC 以预测未来重排/优化动作 chunk，偏 test-time MPC；不是训练数据或世界模型 RL 迁移路线。 |
| 14 | `2606.01027v2`，2026-08-23 | [τ₀-WM: A Unified Video-Action World Model for Robotic Manipulation](https://arxiv.org/abs/2606.01027) | 将世界模型用于动作候选选择和不确定性下的重查询，偏在线规划；留待闭环控制专题处理。 |
| 15 | `2609.39235v1`，2026-09-30 | [The Planning Limits of Latent World Models](https://arxiv.org/abs/2609.39235) | 研究 latent world-model planning horizon 与反馈限制，主要是模拟/离线轨迹层面的边界分析；不属于 VLA 合成数据训练。 |
| 16 | `2610.10846v1`，2026-10-07 | [Cross-Embodiment Robot Foundation World Models with Latent Actions](https://arxiv.org/abs/2610.10846) | 跨本体动作条件世界模型与 LIBERO 规划，作者明确把 physical hardware validation 列为后续工作，故不计入真机迁移证据。 |
| 17 | `2509.19080v2`，2026-03-19 | [World4RL: Diffusion World Models for Policy Refinement with Reinforcement Learning for Robotic Manipulation](https://arxiv.org/abs/2509.19080) | 有真机 World-Model-RL 结果，但控制器为高斯策略而非 VLA；作为相邻机器人 RL，不纳入 VLA 核心集合。 |
| 18 | `2603.18532v4`，2026-09-29 | [Scaling Sim-to-Real VLA Reinforcement Learning with Generative 3D Worlds](https://arxiv.org/abs/2603.18532) | 生成可交互 3D 场景做仿真 RL；它是程序化/生成式物理环境而非视频世界模型，作相邻 sim-to-real 方法。 |
| 19 | `2604.27792v5`，2026-07-15 | [Motubrain: An Advanced World Action Model for Robot Control](https://arxiv.org/abs/2604.27792) | 视频与动作联合模型直接部署，代表 WAM 控制器方向；本专题聚焦“世界模型怎样变成训练数据/模拟器”，暂不与数据闭环混列。 |
| 20 | `2605.22882v4`，2026-08-03 | [GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation](https://arxiv.org/abs/2605.22882) | 几何一致的视频未来与 inverse dynamics 转成可执行轨迹，重点是预测后规划/轨迹生成，不是基于 imagined rollout 更新 VLA 策略。 |

### 6.3 统计与筛选边界

- 本批候选池 **20 = 入选精读 5 + 相邻机制 / 排除 15**；累计全页候选池 **51 = 入选分册 16 + 排除 / 边界候选 35**（历史 27、闭环控制批次 4、本批 20）。
- 5 篇入选均可读固定版本全文；数字均按本表列示的 arXiv 版本回到原文核对。未下载论文全文入库；缓存如需使用，放仓库外。
- “模型世界、仿真环境、real-world rollouts”在不同论文中代表不同数据来源。相邻候选保留其清楚的角色边界，不据标题或摘要将它们等同为 VLA 训练样本。

---

## 7. 2026-10-23 补充：在线 RL 干预调度机制

> 本次只新增一项闭环机制候选，不扩充 VLA backbone / 动作头精读集。是否纳入按“是否比现有策略更新、episode 内恢复、世界模型 rollout、任务层 BT 修订增加一个闭环位置”判断。

| arXiv ID / 固定版本 | 论文 | 处理与理由 |
| :-- | :-- | :-- |
| `2610.03620v1`，2026-10-02 | [UniIntervene++: An Adaptive Intervention Agent for Efficient Real-World Reinforcement Learning](https://arxiv.org/abs/2610.03620) | **纳入闭环专题，不另建 VLA 论文分册**：在线 Double-DQN 将演化中的 RL、示范轨迹修正与任务 CodePolicy 作为 SMDP Options 分配控制，并用 RL-only probes 追踪能力、回灌辅助经验；这区别于 RECAP 更新 VLA 参数、VLCP 重写 episode 内代码、LingBot-VA 的模型 rollout 与 VersualRL 的 BT refinement。真实 UR7e 五任务结果支持作为相邻在线 RL 机制讨论；它不是 VLA 模型成功率证据。 |

- **固定版本与正文**：题名、作者、v1 与 2026-10-02 日期由 arXiv abs 页、Atom API 与 PDF 首页交叉核对；正文全文 PDF 及 `pdftotext -layout` 文本缓存在仓库外 `/tmp/uniintervenepp-paper/`，HTML 版也缓存用于章节定位。PDF SHA-256：`92e587debd4a8c039667ab42fd8a5fef671322e52c4dd27226287959736b206e`；仅保留摘要与分析，未复制全文入库。
- **数量口径**：候选池累计 `51 + 1 = 52`；其中 17 项进入精读/专题证据（16 篇独立分册 + 本专题 1 个四亮点七问 section），35 项仍为排除 / 边界候选。原批次 §4–§6 数量保持其各自截点口径。
- **证据边界**：平均 SR `89.67%`、HIR `0.77%`、IR `56.04%` 与五项任务的条件只按 v1 §IV-A–C、Table I–II、Fig. 5–7 写入闭环专题；不将低 HIR 表述为总辅助执行低，也不把系统级消融写成某单模块的独立因果结论。
