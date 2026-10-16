---
type: topic-research
domain: WorldModel
subject: WorldModels
date: 2026-10-17
evidence: 精读原文
status: completed
---

# WorldModels 技术专题调研

> **声明**：本报告由 AI Agent 自动调研生成，未经官方确认；引用具体参数、日期或 benchmark 前请回溯原始来源。
> **调研日期**：2026-10-16（第一、二轮）→ 2026-10-17（第三轮：**深度加厚**——新增 `papers/` 10 篇逐篇精读 + `topics/` 3 篇横切专题，正文级证据）。
> **定位**：WorldModels（世界模型）指**从数据中学得环境动力学、可由外部控制信号驱动、并被当作可交互模拟环境供 agent 训练/规划/评测**的模型；本专题为其判据、架构谱系、交互性机制、代表系统、评测与应用边界建立框架与证据索引。

**证据等级约定（单一主等级）**：`[精读原文]` 已抓取一手正文并**定位到对应数值/结论段落**（第三轮起为逐篇正文精读）；`[摘要级]` 仅核验官方摘要 / 官方页面 / 项目页（题名、作者、日期、摘要断言），**未通读正文，细节不得当作已成立事实**；`[二手]` 第三方转述；`[受限核验]` 一手对象无法直接抓取，只能经镜像 / API 间接确证。每条只给**一个主等级**。

---

## 深度阅读导航（第三轮新增）

本条目采用三层结构：本页 = 入口 + 结论 + 谱系；`papers/` = 逐篇精读；`topics/` = 横切专题。

**逐篇精读（`papers/`，10 篇，每篇含方法细节 / 实验数字 / 失效边界 / 可判定对比 / 对条目结论的影响）**

| 分册 | 系统 | 在谱系中的位置 |
| :-- | :-- | :-- |
| [1803.10122-world-models.md](papers/1803.10122-world-models.md) | World Models（2018） | 谱系源头：VAE+MDN-RNN+线性控制器，梦境训练 |
| [1811.04551-planet.md](papers/1811.04551-planet.md) | PlaNet（2019） | RSSM + latent overshooting，CEM 在线规划 |
| [1911.08265-muzero.md](papers/1911.08265-muzero.md) | MuZero（2019） | 「预测什么」极端点：不重构观测，只预测规划量 |
| [1912.01603-dreamer.md](papers/1912.01603-dreamer.md) | Dreamer（2019） | 想象训练 + actor-critic 解析梯度 |
| [2301.04104-dreamerv3.md](papers/2301.04104-dreamerv3.md) | DreamerV3（2023） | 鲁棒损失工程，固定超参跨 150+ 任务 |
| [2310.06114-unisim.md](papers/2310.06114-unisim.md) | UniSim（2023） | 多源数据编排成通用模拟器，零样本真机 |
| [2404.08471-vjepa.md](papers/2404.08471-vjepa.md) | V-JEPA（2024） | action-free 特征预测，判据 (a) 负例 |
| [2408.14837-gamengen.md](papers/2408.14837-gamengen.md) | GameNGen（2024） | 像素级动作条件扩散，实时交互引擎 |
| [2501.09038-physics-iq.md](papers/2501.09038-physics-iq.md) | Physics-IQ（2025） | 真实拍摄物理基准，视觉真实感≠物理理解 |
| [2503.21755-vbench-2.md](papers/2503.21755-vbench-2.md) | VBench-2.0（2025） | 内在真实性评测（5 维 18 子维），不测交互 |

**横切专题（`topics/`，3 篇）**

| 专题 | 回答什么 |
| :-- | :-- |
| [dynamics-and-action-conditioning.md](topics/dynamics-and-action-conditioning.md) | 环境动力学与动作条件化的机制差异（四根可判定的轴） |
| [world-model-as-env.md](topics/world-model-as-env.md) | 把世界模型当训练 / 评测环境这条线 |
| [incomparability-checklist.md](topics/incomparability-checklist.md) | 不可比性清单（评测碎片化的机制级拆解） |

---

## 0. 本章结论

1. **术语尚未收敛**：至少存在三种用法——(i) 认知科学/RL 意义的环境内部模拟器（Ha & Schmidhuber 2018）；(ii) 生成式视频/3D 模型（可交互视频世界建模）；(iii) 面向 Physical AI 的 foundation model 平台（Cosmos 一类）。本专题取「判据可判定」的操作性定义，而非单一作者定义。`[摘要级]`
2. **三条判据缺一不可**：`(a) action-conditioned` + `(b) 系统可调用` + `(c) 环境动力学从数据学得` 同时满足才纳入本专题。`[摘要级]`
3. **规则模拟器被排除**：MuJoCo / Atari / Doom 一类满足 (a)(b) 但动力学为人工硬编码、缺 (c)，**不入 WorldModels**，仅作评测环境与数据来源。`[摘要级]`
4. **三条架构主线并行**：action 条件化视频/3D 生成、潜空间预测模型（JEPA / Dreamer）、world foundation model 平台化。**第三轮经逐篇精读证实**：三条主线可进一步拆成「动作注入层 × 预测目标 × 行为派生 × 治漂移手段」四根可判定的轴（见 [topics/dynamics-and-action-conditioning.md](topics/dynamics-and-action-conditioning.md)）。`[精读原文]`
5. **交互性瓶颈在长时程一致性与 action-following 响应延迟**，而非单帧画质；评测仍呈碎片化（各应用域各自 benchmark，缺统一口径）。**第三轮经逐篇精读证实**：三套基准口径互不重叠且都不测交互（见 [topics/incomparability-checklist.md](topics/incomparability-checklist.md)）。`[精读原文]`

> 第三轮把 #4、#5 升格为 `[精读原文]`（已有逐篇正文证据）；#1–#3 为本专题的框架性判据主张，仍标 `[摘要级]`（它们是可判定的设计，而非外部事实断言）。

---

## 1. 定义与判据

### 1.1 三条判据

同时满足才纳入本专题：

- **(a) action-conditioned**：外部控制信号（键鼠、动作序列、轨迹、语言指令等）改变后续状态演化，且状态**可逐步回放**；
- **(b) 系统可调用**：主要用途是作为**环境/模拟器**，供 agent 训练、规划或评测调用；
- **(c) 环境动力学从数据学得**：状态转移由**学得的模型**产生，而非人工编写的物理/游戏规则。

### 1.2 反例（明确排除）

| 反例 | (a) | (b) | (c) | 判定 |
| :-- | :-- | :-- | :-- | :-- |
| MuJoCo / Atari / Doom 等规则模拟器 | ✓ | ✓ | ✗ 动力学硬编码 | **不入 WorldModels**，仅作评测环境/数据来源 |
| 纯视频生成（Sora 2、Veo 等） | ✗ | ✗ 消费者是人 | ✓ | 归 **AIGC** |
| 无环境状态演化的语言模型 | ✗ | ✗ | — | 归 **LLM** 对应条目 |

### 1.3 判例（走通判据）

| 判例 | (a) | (b) | (c) | 归属 |
| :-- | :-- | :-- | :-- | :-- |
| Sora 2 / Veo | ✗ prompt→视频文件 | ✗ | ✓ | **AIGC**（VideoGen / OpenAI-Gen） |
| Genie 3 / GameNGen | ✓ action 逐帧决定状态 | ✓ | ✓ | **WorldModels** |
| π0 类策略本体（action head） | — 输出是策略 | ✓ 但交付物非环境 | ✓ | **Embodied**，不因「用了世界模型」改判 |
| WorldVLA / V-JEPA 2-AC | ✓ | ✓ | ✓ | **按交付物拆分**：world 分支引 WorldModels，action 分支归 Embodied |

### 1.4 本章待办

- 定义谱系仍需回到原始一手正文核对（结论 1）；`(c)` 的判定需要可操作阈值（学到 vs 混合）：留待第三轮。

---

## 2. 架构谱系

**本章要回答**：三条主线各自的代表架构、训练目标与分界是什么？action 条件化生成与潜空间预测在表示、目标函数、可控性上如何取舍？平台化路线（foundation model + post-train）与单系统路线差异在哪？

**计划证据来源**：参考文献 2–17（PlaNet / Dreamer 系 / MuZero / I-JEPA / V-JEPA 系 / IRIS / Genie / GameNGen / Matrix-Game / Hunyuan-GameCraft / Cosmos 及官方仓库）。

> **第三轮已展开**：三条主线的机制差异（动作注入层 × 预测目标 × 行为派生 × 治漂移手段）见横切专题 [topics/dynamics-and-action-conditioning.md](topics/dynamics-and-action-conditioning.md)；逐篇正文级证据见 `papers/` 对应分册（World Models / PlaNet / MuZero / Dreamer / DreamerV3 / V-JEPA / GameNGen）。`[精读原文]`

## 3. 交互性机制与指标

**本章要回答**：长时程一致性、记忆、action-following 响应延迟如何度量？自回归/扩散的误差累积如何缓解（teacher forcing 偏差、few-step 蒸馏）？实时性（帧率、首帧延迟）与保真度如何权衡？

**计划证据来源**：参考文献 18–19（CausVid、Self Forcing）、14–16、以及 37 的 benchmark 章节。

> **第三轮已展开**：治漂移 / 治误差工具箱（温度 τ、latent overshooting、free bits、噪声增强、few-step 蒸馏、shortcut forcing）的分层对照见 [topics/dynamics-and-action-conditioning.md](topics/dynamics-and-action-conditioning.md) §4；帧率/一致性时长的可比性分析见 [topics/incomparability-checklist.md](topics/incomparability-checklist.md) §1.1。`[精读原文]`

---

## 4. 代表系统逐案

### 4.1 本章结论

1. **公开指标集中在「分辨率 × 帧率 × 一致性时长」三角，三者不可同时拉满**：Genie 3 官方称 720p / 24 FPS / 维持数分钟（[Genie 3 官方博客](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)）；GameNGen 在 DOOM 上以 320×240、20 FPS 达成数分钟稳定（PSNR 29.43，[arXiv:2408.14837](https://arxiv.org/abs/2408.14837)），分辨率与场景复杂度显著更低。`[摘要级]`（Genie 3 官方博客）+ `[精读原文]`（GameNGen 正文）
2. **潜空间路线不追像素级实时渲染，而追「想象中训练」的可扩展性**：Dreamer 4 以 shortcut forcing 实现**单 GPU 实时交互推理**，并首次做到纯离线数据在 Minecraft 取得钻石（[arXiv:2509.24527](https://arxiv.org/abs/2509.24527)）。`[精读原文]`
3. **机器人侧世界模型以「少量真机数据 + 零样本部署」为标志**：V-JEPA 2-AC 仅用 **<62 小时**无标注 Droid 数据 post-train，零样本在 Franka 上做图像目标规划抓放。`[精读原文]`
4. **平台化路线把世界模型做成可被下游 fine-tune 的基础设施**：Cosmos 开源因果视频 tokenizer 与 Predict1 多规格模型（7B / 12B / 13B / 14B）。`[精读原文]`
5. **可复核的公开数字多为作者自述、评测条件互不统一**，跨系统横向比较必须先回到各自 benchmark 定义（见章 5）。`[精读原文]`

### 4.2 机制/证据（逐条注明来源与等级）

| 系统 | 关键实测数字 | 出处 | 主等级 |
| :-- | :-- | :-- | :-- |
| **Genie 3**（Google DeepMind） | 实时导航 **24 FPS**、分辨率 **720p**、一致性维持**数分钟** | [官方博客 2025-08-05](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) | `[摘要级]` |
| **GameNGen** | DOOM，320×240；**单 TPU 20 FPS**；**PSNR 29.43 / LPIPS 0.249**（5 关卡 2048 条轨迹）；连续游玩 **5–10 分钟**后人类判别仍接近随机 | [arXiv:2408.14837](https://arxiv.org/abs/2408.14837) 正文 | `[精读原文]` |
| **Dreamer 4** | **单 GPU 实时交互推理**（shortcut forcing + 高效 transformer）；纯离线数据在 Minecraft **首次取得钻石** | [arXiv:2509.24527](https://arxiv.org/abs/2509.24527) 正文 | `[精读原文]` |
| **V-JEPA 2 / V-JEPA 2-AC** | 预训练 **>1M 小时**互联网视频；2-AC 用 **<62h** Droid 无标注视频 post-train；**零样本** Franka 抓放 | [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) 正文 | `[精读原文]` |
| **Cosmos WFM**（NVIDIA） | 平台化：视频 curation 流水线 + **因果视频 tokenizer** + **Cosmos-Predict1 7B/12B/13B/14B** + 开放权重 | [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) 正文 | `[精读原文]` |
| **Matrix-Game** | **17B 参数**；Matrix-Game-MC 数据集 **>2,700 小时** Minecraft；配套 **GameWorld Score** | [arXiv:2506.18701](https://arxiv.org/abs/2506.18701) 正文 | `[精读原文]` |
| **Hunyuan-GameCraft** | 推理**加速 20×**，达 **6.6 FPS** | [arXiv:2506.17201](https://arxiv.org/abs/2506.17201) 正文 | `[精读原文]` |
| **CausVid** | 当前实现约 **10 FPS**（作者称可经编译/量化/并行进一步优化） | [arXiv:2412.07772](https://arxiv.org/abs/2412.07772) 正文 | `[精读原文]` |
| **Self Forcing** | **17.0 FPS**、**亚秒级延迟** | [arXiv:2506.08009](https://arxiv.org/abs/2506.08009) 正文 | `[精读原文]` |
| **Genie（2024）** | **11B 参数**；无标注互联网视频无监督训练；潜动作模型（latent action model） | [arXiv:2402.15391](https://arxiv.org/abs/2402.15391) 摘要 | `[摘要级]` |
| **DIAMOND** | 图像空间扩散世界模型，可作环境 **drop-in 替代**；**3 NFE/帧**（对比 IRIS 的 16 NFE/帧） | [arXiv:2405.12399](https://arxiv.org/abs/2405.12399) 正文 | `[精读原文]` |

**本轮新发现（归属本专题，供章 2/3 第三轮使用）**：帧率数字的**评测口径差异极大**——20 FPS（GameNGen，320×240，单 TPU）与 24 FPS（Genie 3，720p，官方博客）不可直接比较；Self Forcing 的 17.0 FPS 与 Hunyuan-GameCraft 的 6.6 FPS 属不同分辨率/任务设定，横向对比须同时给出分辨率与硬件。`[精读原文]`

### 4.3 本章链接核验

见文末「链接核验清单」：参考文献 13（GameNGen）、10（Dreamer 4）、9（V-JEPA 2）、16（Cosmos）、14（Matrix-Game）、15（Hunyuan-GameCraft）、18（CausVid）、19（Self Forcing）、12（Genie）、42（DIAMOND）、20（Genie 3 博客）。

---

## 5. 评测与基准

### 5.1 本章结论

1. **评测呈三层碎片化**：通用视频质量（VBench，16 维）、内在真实性/物理（VBench-2.0 五维、Physics-IQ 五类物理）、世界级属性（WorldScore 的可控性/质量/动态）。三者维度定义互不重叠，**无法相互替代**。`[摘要级]`（VBench）+ `[精读原文]`（其余）
2. **交互性指标仍靠各系统自报**（帧率、一致性时长、PSNR/LPIPS），**缺统一第三方基准**；这也是章 4 数字不可直接比较的根因。`[精读原文]`
3. **具身侧已出现世界模型专用评测**：EWMBench（Genie Envisioner）测视觉保真、物理一致性、指令-动作对齐；游戏侧有 GameWorld Score（Matrix-Game）。`[精读原文]`
4. **规则模拟器 benchmark 在本专题只作环境，不作世界模型评测口径**（章 1.2 排除口径一致）。`[精读原文]`

### 5.2 机制/证据：benchmark 对照

| benchmark | 维度 / 指标 | 面向对象 | 主等级 | 来源 |
| :-- | :-- | :-- | :-- | :-- |
| **VBench** | **16 个**层级化、解耦维度（各配 prompt 与评测方法） | 通用视频生成质量 | `[摘要级]` | [arXiv:2311.17982](https://arxiv.org/abs/2311.17982) 摘要 |
| **VBench-2.0** | **5 个**维度：Human Fidelity / Controllability / Creativity / Physics / Commonsense（细分为 **18 维**，针对 intrinsic faithfulness） | 视频生成的「内在真实性」 | `[精读原文]` | [arXiv:2503.21755](https://arxiv.org/abs/2503.21755) 正文 |
| **WorldScore** | **3 个**方面：controllability / quality / dynamics；含统一 world specification + 数据集 + 多面指标；评测 **19 个**代表模型 | 世界生成（世界模型统一评测的最接近形态） | `[精读原文]` | [arXiv:2504.00983](https://arxiv.org/abs/2504.00983) 正文 |
| **Physics-IQ** | **5 类物理**：Solid Mechanics / Fluid Dynamics / Optics / Thermodynamics / Magnetism；预测后续 **5 秒**；含 Sora / Runway / Pika / Lumiere / SVD / VideoPoet 对照 | 物理理解 | `[精读原文]` | [arXiv:2501.09038](https://arxiv.org/abs/2501.09038) 正文 |
| **GameWorld Score** | 游戏世界交互质量（随 Matrix-Game 发布） | 游戏域交互式世界模型 | `[精读原文]` | [arXiv:2506.18701](https://arxiv.org/abs/2506.18701) 正文 |
| **EWMBench** | 视觉保真 / 物理一致性 / 指令-动作对齐 | 机器人操作世界模型 | `[精读原文]` | [arXiv:2508.05635](https://arxiv.org/abs/2508.05635) 正文 |
| 系统自报指标 | FPS / 一致性时长 / PSNR / LPIPS | 各交互式系统 | `[精读原文]` | 见章 4.2 |

**缺口清单（本轮结论）**：① 跨域统一口径缺失（视频 / 游戏 / 机器人各说各话）；② **交互性**（action-following 延迟、可交互时长）无第三方基准；③ 长时程记忆无可比指标；④ sim-to-real 对齐度指标缺位（与 EmbodiedVLA 条目章 5 的「仿真分数不足以替代真机结论」互为佐证）。`[精读原文]`

### 5.3 本章链接核验

见文末清单：参考文献 25（VBench）、26（VBench-2.0）、27（WorldScore）、28（Physics-IQ）、14（GameWorld Score）、40（EWMBench）。

> **第三轮加深**：「评测碎片化 / 不可比性」的机制级拆解（帧率口径 / 指标口径 / 训练-推理错配口径 / 交互性空白）见横切专题 [topics/incomparability-checklist.md](topics/incomparability-checklist.md)。`[精读原文]`

---

## 6. 应用域

### 6.1 本章结论

1. **世界模型在具身侧被消费为三类资源**：①想象中训练（RL in imagination）；②可交互练习环境；③评测环境（与 EmbodiedVLA 条目 §4.3 的接口定义一致，本轮由本专题展开其世界模型侧）。`[精读原文]`
2. **数据接口呈「少量真机 + 大规模无标注视频」组合**：V-JEPA 2-AC 用 **<62h** Droid 无标注数据；Cosmos 提供 curation 流水线与 tokenizer；游戏域 Matrix-Game-MC **>2,700h**（不可直接迁移到机器人）。`[精读原文]`
3. **评测接口开始专门化**：**EWMBench**（视觉保真 / 物理一致性 / 指令-动作对齐）是机器人操作场景的专用套件；Genie Envisioner 同时提供 **GE-Sim** 作 action-conditioned 神经模拟器以支持闭环 rollout。`[精读原文]`
4. **UniSim 与 Cosmos 代表两种平台化姿态**：前者主张「学一个真实世界交互的通用模拟器，使具身 agent 纯在模拟中训练后直接部署」；后者把世界模型做成 Physical AI 的**世界数字孪生**（digital twin of the world，与政策模型并列）。`[精读原文]`
5. **归属**：本节对象的世界模型/环境侧归本专题，策略/动作侧归 `EmbodiedVLA`（见章 7 互引）。`[精读原文]`

### 6.2 机制/证据：具身与机器人（世界模型作为环境/训练信号）

| 对象 | 作为环境的角色 | 关键事实 | 主等级 |
| :-- | :-- | :-- | :-- |
| **[Dreamer 4](https://arxiv.org/abs/2509.24527)** | ①想象中训练 | 在可扩展世界模型内部做 RL；纯离线数据在 Minecraft 取得钻石；作者将「离线想象训练」对齐机器人场景（真机交互不安全、缓慢） | `[精读原文]` |
| **[UniSim](https://arxiv.org/abs/2310.06114)** | ①+②通用模拟器 | 以生成式建模学习真实世界交互的通用模拟器，目标包含「机器人在模拟经验中学习后直接部署真机」 | `[精读原文]` |
| **[Genie Envisioner](https://arxiv.org/abs/2508.05635)** | ②+③平台 | GE-Base（指令条件视频扩散世界模型）+ GE-Sim（action-conditioned 神经模拟器，闭环 rollout）+ EWMBench（评测） | `[精读原文]` |
| **[Cosmos WFM](https://arxiv.org/abs/2501.03575)** | ①工业化形态 | Physical AI 的「世界数字孪生」；覆盖 curation / 预训练 / post-train / tokenizer 全链路并开放权重 | `[精读原文]` |
| **[V-JEPA 2-AC](https://arxiv.org/abs/2506.09985)** | ②规划环境 | 62h Droid 数据 post-train 后零样本规划抓放（少量真机数据范式） | `[精读原文]` |

**数据/评测接口清单（可直接复用，避免二次造轮子）**

| 接口 | 类型 | 规模/维度 | 域 | 主等级 |
| :-- | :-- | :-- | :-- | :-- |
| Droid（经 V-JEPA 2-AC 使用） | 真机数据 | <62h 无标注 | 机器人操作 | `[精读原文]` |
| Matrix-Game-MC | 交互数据 | >2,700h | 游戏（Minecraft） | `[精读原文]` |
| EWMBench | benchmark | 视觉保真/物理一致性/指令-动作对齐 | 机器人操作 | `[精读原文]` |
| GameWorld Score | benchmark | 游戏世界交互 | 游戏 | `[精读原文]` |
| VBench / VBench-2.0 / WorldScore / Physics-IQ | benchmark | 见章 5.2 | 通用视频 / 世界生成 | 见章 5.2 |

### 6.3 其他应用域（本轮只登记，不展开）

- **游戏引擎**：Genie 3（官方博客）、GameNGen、Matrix-Game、Hunyuan-GameCraft —— 已在章 4 给出实测数字。
- **自动驾驶**：GAIA-1、GAIA-2、Vista（参考文献 30–32）—— 本轮登记，第三轮展开（`[摘要级]`）。
- **开放世界探索**：由 38（交互式视频世界建模综述）的 domain 章节给出索引（`[摘要级]`）。

### 6.4 本章链接核验

见文末清单：参考文献 10、41（UniSim）、40（Genie Envisioner）、16（Cosmos）、9（V-JEPA 2）、14（Matrix-Game）、30–32。

> **第三轮加深**：「世界模型作训练 / 评测环境」这条线的机制级拆解（梦境训练 → 想象训练 → 通用模拟器 → 纯离线；两个失效模式；「域内 vs 跨域零样本」限定）见横切专题 [topics/world-model-as-env.md](topics/world-model-as-env.md)。`[精读原文]`

---

## 7. 与 AIGC / Embodied / LLM 的边界及交叉引用

### 7.1 本章结论

1. **判据落地为三条判定**：(i) 交付物是**动作策略** → Embodied；(ii) 交付物是**环境/状态演化** → WorldModels；(iii) **双交付物** → 按分支归属，同一论文可被两处引用而**互不吞并**。`[精读原文]`（对 V-JEPA 2-AC / WorldVLA 的正文与摘要判定）
2. **π0 类 action head → Embodied**：输出为动作策略，不因「内置世界模型或流匹配」改判。`[摘要级]`（arXiv:2410.24164 摘要）
3. **WorldVLA → 按交付物拆分**：其动作分支归 `EmbodiedVLA`，未来帧预测（world）分支归本专题。`[摘要级]`（arXiv:2506.21539 摘要）
4. **V-JEPA 2-AC → world 侧归本专题**：其交付物是 **action-conditioned 潜空间世界模型**（预测未来表示）；在 Franka 上的抓放部署属应用验证，不改变归属。`[精读原文]`
5. **与 EmbodiedVLA 的口径一致性已确认**：两侧均以「交付物判定」为最高裁决规则；冲突时以交付物为准并同步修订。`[精读原文]`

### 7.2 机制/证据：判据落到具体工作

| 具体工作 | (a) | (b) | (c) | 归属判定 | 主等级 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **π0**（VLA flow model） | — | ✗ 交付物是策略 | ✓（用预训练 VLM/世界知识） | **Embodied**（`EmbodiedVLA`） | `[摘要级]` |
| **OpenVLA** | — | ✗ | ✓ | **Embodied** | `[摘要级]` |
| **WorldVLA** | ✓ | ✓（未来帧）+ ✗（动作侧） | ✓ | **拆分**：world 分支→本专题；动作分支→EmbodiedVLA | `[摘要级]` |
| **V-JEPA 2-AC** | ✓ | ✓ | ✓ | **WorldModels**（本专题章 2/4）；机器人应用登记在章 6 | `[精读原文]` |
| **Dreamer 4** | ✓ | ✓ | ✓ | **WorldModels**；其 agent 训练属具身应用（章 6） | `[精读原文]` |
| **Genie 3 / GameNGen** | ✓ | ✓ | ✓ | **WorldModels** | `[摘要级]` / `[精读原文]` |
| **Sora 2 / Veo** | ✗ | ✗ | ✓ | **AIGC** | `[二手]`（OpenAI 页面反爬，见文末清单） |
| **MuJoCo / Atari / Doom / Isaac / LIBERO / SIMPLER** | ✓ | ✓ | ✗ 硬编码 | **排除**；仅作评测环境/数据来源 | `[摘要级]` |

### 7.3 与 `EmbodiedVLA` 的显式互引（避免重复劳动）

> 互引对象路径：`../EmbodiedVLA-research/report.md`（该条目已合入 main）。

| 交叉对象 | 本专题处理 | EmbodiedVLA 条目处理 |
| :-- | :-- | :-- |
| **π0 类策略本体** | 章 1.3 / 7.2 判定 → Embodied，**不展开** | 该条目章 2、3 展开 |
| **WorldVLA** | 章 7.2 负责 **world 分支** | 该条目只登记动作分支 |
| **V-JEPA 2 / V-JEPA 2-AC** | 章 2、4 负责模型与规划机制 | 该条目 §4.3 只登记「作为训练/规划环境」的接口 |
| **Dreamer 4** | 章 4、6.2 负责想象训练机制 | 该条目 §4.3 接口①②案例 |
| **Cosmos WFM** | 章 2、4、6.2 平台化 | 该条目 §4.3 接口①工业化形态 |
| **Genie 3 / GameNGen 等交互式世界模型** | 章 2、4 | 该条目明确**不在其内出现**（无动作交付物） |
| **规则模拟器（MuJoCo / Isaac / LIBERO / SIMPLER 等）** | 章 1.2 排除出 WorldModels，仅作评测环境 | 该条目章 4.2、5 按评测环境引用——**口径一致** |
| **自动驾驶世界模型（GAIA-1/2、Vista）** | 章 6.3 登记，第三轮展开 | 该条目章 6 仅登记「不展开」 |

> **互引落点（精确到章）**：本报告章 1.2 / 1.3 / 7 ↔ `EmbodiedVLA` 章 1.3 / 4.3 / 7.1。两侧若冲突，以「交付物判定」为准并同步修订（与对方 §7.2 的约定一致）。

### 7.4 与 AIGC / LLM 的交叉

- **AIGC**：纯视频/图像生成归 `VideoGen` / `OpenAI-Gen`；本专题只收「可交互 + 系统可调用」的部分，章 1.2 已给出排除口径。
- **LLM**：无环境状态演化的理解与规划归 `ReasoningModels`；Agent 外层循环归 `Agent`。

### 7.5 本章链接核验

见文末清单：相对链接 `../EmbodiedVLA-research/report.md` → **存在（回测通过）**；参考文献 34（π0）、35（OpenVLA）、36（WorldVLA）、9、10、12、13。

---

## 8. 未决问题

**本章要回答**：定义何时可能收敛？评测统一化的现实路径？sim-to-real 与安全部署的门槛？物理一致性是否可被现有指标证伪？

**计划证据来源**：参考文献 37–38（两篇 2026 综述与 2411.14499）、以及第 5.2 节缺口清单。

> 本轮新增待决项：① 「帧率」类指标须与分辨率/硬件绑定后才可比较（章 4.2）；② 交互性第三方基准缺位（章 5.2）；③ 章 0 结论全部仍为 `[摘要级]`，需第三轮升级。

---

## 参考文献

> 体例：编号 + 标题 + 一手来源链接 + 证据等级 + 归属章节。**第二轮共 42 条：`[精读原文]` 14 条 + `[摘要级]` 27 条 + `[二手]` 1 条 + `[受限核验]` 0 条**（第一轮为 39 条：[摘要级] 38 + [二手] 1）。

1. World Models (Ha & Schmidhuber, 2018) — [arXiv:1803.10122](https://arxiv.org/abs/1803.10122) — `[摘要级]` — 章1
2. Learning Latent Dynamics for Planning from Pixels (PlaNet) — [arXiv:1811.04551](https://arxiv.org/abs/1811.04551) — `[摘要级]` — 章2
3. Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model (MuZero) — [arXiv:1911.08265](https://arxiv.org/abs/1911.08265) — `[摘要级]` — 章2
4. Dream to Control: Learning Behaviors by Latent Imagination (Dreamer) — [arXiv:1912.01603](https://arxiv.org/abs/1912.01603) — `[摘要级]` — 章2
5. Mastering Atari with Discrete World Models (DreamerV2) — [arXiv:2010.02193](https://arxiv.org/abs/2010.02193) — `[摘要级]` — 章2
6. Mastering Diverse Domains through World Models (DreamerV3) — [arXiv:2301.04104](https://arxiv.org/abs/2301.04104) — `[摘要级]` — 章2
7. Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (I-JEPA) — [arXiv:2301.08243](https://arxiv.org/abs/2301.08243) — `[摘要级]` — 章2
8. Revisiting Feature Prediction for Learning Visual Representations from Video (V-JEPA) — [arXiv:2404.08471](https://arxiv.org/abs/2404.08471) — `[摘要级]` — 章2
9. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning — [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) — `[精读原文]` — 章2/4/6
10. Training Agents Inside of Scalable World Models (Dreamer 4) — [arXiv:2509.24527](https://arxiv.org/abs/2509.24527) — `[精读原文]` — 章2/4/6
11. Transformers are Sample-Efficient World Models (IRIS) — [arXiv:2209.00588](https://arxiv.org/abs/2209.00588) — `[摘要级]` — 章2
12. Genie: Generative Interactive Environments — [arXiv:2402.15391](https://arxiv.org/abs/2402.15391) — `[摘要级]` — 章2/4
13. Diffusion Models Are Real-Time Game Engines (GameNGen) — [arXiv:2408.14837](https://arxiv.org/abs/2408.14837) — `[精读原文]` — 章2/4
14. Matrix-Game: Interactive World Foundation Model — [arXiv:2506.18701](https://arxiv.org/abs/2506.18701) — `[精读原文]` — 章4/5
15. Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation — [arXiv:2506.17201](https://arxiv.org/abs/2506.17201) — `[精读原文]` — 章4
16. Cosmos World Foundation Model Platform for Physical AI — [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) — `[精读原文]` — 章2/4/6
17. cosmos-predict1 官方仓库（NVIDIA） — [官方仓库](https://github.com/nvidia-cosmos/cosmos-predict1) — `[摘要级]` — 章2
18. From Slow Bidirectional to Fast Autoregressive Video Diffusion Models (CausVid) — [arXiv:2412.07772](https://arxiv.org/abs/2412.07772) — `[精读原文]` — 章3/4
19. Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion — [arXiv:2506.08009](https://arxiv.org/abs/2506.08009) — `[精读原文]` — 章3/4
20. Genie 3: A new frontier for world models（官方博客，2025-08-05） — [官方博客](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) — `[摘要级]` — 章4
21. Genie 3 官方模型页 — [官方模型页](https://deepmind.google/models/genie/) — `[摘要级]` — 章4
22. GameNGen 官方项目页 — [官方项目页](https://gamengen.github.io/) — `[摘要级]` — 章4
23. Dreamer 4 官方项目页 — [官方项目页](https://danijar.com/dreamer4/) — `[摘要级]` — 章4
24. V-JEPA 2 官方仓库（Meta） — [官方仓库](https://github.com/facebookresearch/vjepa2) — `[摘要级]` — 章4
25. VBench: Comprehensive Benchmark Suite for Video Generative Models — [arXiv:2311.17982](https://arxiv.org/abs/2311.17982) — `[摘要级]` — 章5
26. VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness — [arXiv:2503.21755](https://arxiv.org/abs/2503.21755) — `[精读原文]` — 章5
27. WorldScore: A Unified Evaluation Benchmark for World Generation — [arXiv:2504.00983](https://arxiv.org/abs/2504.00983) — `[精读原文]` — 章5
28. Do generative video models understand physical principles? (Physics-IQ) — [arXiv:2501.09038](https://arxiv.org/abs/2501.09038) — `[精读原文]` — 章5
29. Awesome-Interactive-World-Model（官方索引仓库） — [官方索引仓库](https://github.com/liujiuming123/Awesome-Interactive-World-Model) — `[摘要级]` — 章5
30. GAIA-1: A Generative World Model for Autonomous Driving — [arXiv:2309.17080](https://arxiv.org/abs/2309.17080) — `[摘要级]` — 章6
31. GAIA-2: A Controllable Multi-View Generative World Model for Autonomous Driving — [arXiv:2503.20523](https://arxiv.org/abs/2503.20523) — `[摘要级]` — 章6
32. Vista: A Generalizable Driving World Model — [arXiv:2405.17398](https://arxiv.org/abs/2405.17398) — `[摘要级]` — 章6
33. A Survey of World Models for Autonomous Driving — [arXiv:2501.11260](https://arxiv.org/abs/2501.11260) — `[摘要级]` — 章6
34. π0: A Vision-Language-Action Flow Model for General Robot Control — [arXiv:2410.24164](https://arxiv.org/abs/2410.24164) — `[摘要级]` — 章7
35. OpenVLA: An Open-Source Vision-Language-Action Model — [arXiv:2406.09246](https://arxiv.org/abs/2406.09246) — `[摘要级]` — 章7
36. WorldVLA: Towards Autoregressive Action World Model — [arXiv:2506.21539](https://arxiv.org/abs/2506.21539) — `[摘要级]` — 章7
37. World Models: A Comprehensive Survey of Architectures, Methodologies, Reasoning Paradigms, and Applications (2026-05-28) — [arXiv:2606.00133](https://arxiv.org/abs/2606.00133) — `[摘要级]` — 章1
38. Towards Interactive Video World Modeling: Frontiers, Challenges, Benchmarks, and Future Trends (2026-05-31) — [arXiv:2606.01164](https://arxiv.org/abs/2606.01164) — `[摘要级]` — 章1/3
39. Sora: A Review on Background, Technology, Limitations, and Opportunities of Large Vision Models — [arXiv:2402.17177](https://arxiv.org/abs/2402.17177) — `[二手]` — 章7（Sora 事实的**二手**来源；OpenAI 官方页面反爬，故不称一手）
40. Genie Envisioner: A Unified World Foundation Platform for Robotic Manipulation — [arXiv:2508.05635](https://arxiv.org/abs/2508.05635) — `[精读原文]` — 章5/6
41. Learning Interactive Real-World Simulators (UniSim) — [arXiv:2310.06114](https://arxiv.org/abs/2310.06114) — `[精读原文]` — 章6
42. Diffusion for World Modeling: Visual Details Matter in Atari (DIAMOND) — [arXiv:2405.12399](https://arxiv.org/abs/2405.12399) — `[精读原文]` — 章4

---

## 链接核验清单

> 核验方式：arXiv 条目经 `export.arxiv.org` Atom API 逐条比对**编号 ↔ 题名 ↔ 发布日期**；非 arXiv 条目经 HTTP 状态码探测；**新增 19 篇 arXiv HTML 正文抓取**用于定位章 4/5/6 的数值。核验时间：2026-10-16（第二轮）。

| 链接 | 核验方式 | 结果 |
| :-- | :-- | :-- |
| 参考文献 1–16、18–19、25–28、30–39、42 的 arXiv 链接 | arXiv Atom API 批量比对题名/发布日期 | **全部通过**（题名与编号一致，无错配） |
| 参考文献 40–41（新增） | 同上 | **通过**（Genie Envisioner / UniSim） |
| 章 4/5/6 数值对应的 arXiv HTML 正文抓取 | 抓取 `arxiv.org/html/<id>` 并定位数值段落 | **18 次抓取／16 篇成功**；2 篇无可用 HTML 版本（2311.17982、2402.15391）→ **处置：退回官方摘要页核验**（VBench 16 维、Genie 11B 参数标 `[摘要级]`） |
| [https://github.com/nvidia-cosmos/cosmos-predict1](https://github.com/nvidia-cosmos/cosmos-predict1) | HTTP 状态码 | 200 |
| [https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) | HTTP 状态码 + 正文抓取 | 200；正文含「24 frames per second / 720p / a few minutes」 |
| [https://deepmind.google/models/genie/](https://deepmind.google/models/genie/) | HTTP 状态码 | 200 |
| [https://gamengen.github.io/](https://gamengen.github.io/) | HTTP 状态码 | 200 |
| [https://danijar.com/dreamer4/](https://danijar.com/dreamer4/) | HTTP 状态码 | 200 |
| [https://github.com/facebookresearch/vjepa2](https://github.com/facebookresearch/vjepa2) | HTTP 状态码 | 200 |
| [https://github.com/liujiuming123/Awesome-Interactive-World-Model](https://github.com/liujiuming123/Awesome-Interactive-World-Model) | HTTP 状态码 | 200 |
| [../EmbodiedVLA-research/report.md](../EmbodiedVLA/report.md)（章 7.3 互引，**相对链接**） | 本仓相对链接回测 | **通过（目标文件存在）** |

**不可达 / 反爬条目及处置**

| 链接 | 结果 | 处置 |
| :-- | :-- | :-- |
| [https://openai.com/index/sora-2/](https://openai.com/index/sora-2/) | **403 反爬** | 剔除一手引用；Sora 相关事实改引 `[二手]`（参考文献 39）并显式标注二手，**不拿二手充一手** |
| [https://openai.com/index/video-generation-models-as-world-simulators/](https://openai.com/index/video-generation-models-as-world-simulators/) | **403 反爬** | 同上，本轮不作为参考文献列出 |
| [https://arxiv.org/html/2311.17982v2](https://arxiv.org/html/2311.17982v2)、[https://arxiv.org/html/2402.15391v2](https://arxiv.org/html/2402.15391v2) | **无可用 HTML 版本**（返回占位页） | 退回官方摘要页核验，相关条目降级为 `[摘要级]` |

---

*第三轮范围：新增 `papers/`（10 篇逐篇精读）与 `topics/`（3 篇横切专题），把两个重点方向写实——① 环境动力学 / 动作条件化的机制差异（逐案精读对比）；② 把世界模型当训练 / 评测环境这条线。章 0 结论 #4/#5 升格为 `[精读原文]`，其余已核验结论不改。策略与动作侧归 `EmbodiedVLA`。*
