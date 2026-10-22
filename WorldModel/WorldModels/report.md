---
type: topic-research
domain: WorldModel
subject: WorldModels
date: 2026-10-22
evidence: 精读原文
status: needs-review
---

# WorldModels 技术专题调研

> **声明**：本报告由 AI Agent 自动调研生成，未经官方确认；引用具体参数、日期或 benchmark 前请回溯原始来源。
> **调研日期**：2026-10-16（第一、二轮）→ 2026-10-17（第三轮：**深度加厚**——新增 `papers/` 10 篇逐篇精读 + `topics/` 3 篇横切专题，正文级证据）。
> **定位**：WorldModels（世界模型）在本专题指**从数据学得状态转移、可由动作驱动、并用于训练/规划/评测**的模型；像素渲染是另一个能力维度，不作为所有模型的共同必要条件。本专题为其判据、架构谱系、交互性机制、代表系统、评测与应用边界建立框架与证据索引。

> **2026-10-22 核验范围**：已回 MuZero v2 核对方法、Figure 2–3 与 Reanalyze；已回 DreamerV3 v2 核对 free bits 的损失截断解释。其余分册继承既有阅读记录，未逐项重验。分册存在不是证据充分的证明；本页“已精读”不得解释为全部数字已在本次复核通过。

**证据等级约定（单一主等级）**：`[精读原文]` 已抓取一手正文并**定位到对应数值/结论段落**（第三轮起为逐篇正文精读）；**既有范围记录（第三轮）**：`[精读原文]` **仅授予有对应 `papers/` 分册的论文**——正文级引用但未产出分册的一律标 `[摘要级]`（宁可低估，不可升格）；`[摘要级]` 仅核验官方摘要 / 官方页面 / 项目页（题名、作者、日期、摘要断言），**未通读正文，细节不得当作已成立事实**；`[二手]` 第三方转述；`[受限核验]` 一手对象无法直接抓取，只能经镜像 / API 间接确证。每条只给**一个主等级**。

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

- **(a) action-conditioned**：外部动作或控制信号改变模型预测的后续状态；潜状态转移也可以满足，不要求输出像素；
- **(b) 系统可调用**：模型预测可以被训练、规划或评测过程消费；是否能渲染、闭环交互或替代真实评测另列，不从本条件自动推出；
- **(c) 环境动力学从数据学得**：状态转移由**学得的模型**产生，而非人工编写的物理/游戏规则。

以上是本专题的操作性分类，不是领域公认的唯一定义。MuZero 满足动作条件、规划调用与学得转移，可作为规划型世界模型；其原模型没有像素解码器，应与可渲染环境分开比较。方法依据见 [MuZero v2 §3](https://arxiv.org/html/1911.08265v2#S3)。

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

1. **公开指标集中在「分辨率 × 帧率 × 一致性时长」三角，三者不可同时拉满**：Genie 3 官方称 720p / 24 FPS / 维持数分钟（[Genie 3 官方博客](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)）；GameNGen 在 DOOM 上以 320×240、20 FPS 达成数分钟稳定（PSNR 29.43，[arXiv:2408.14837](https://arxiv.org/abs/2408.14837)），分辨率与场景复杂度显著更低。`[摘要级]`（Genie 3 官方博客）+ `[摘要级]`（GameNGen 正文）
2. **潜空间路线不追像素级实时渲染，而追「想象中训练」的可扩展性**：Dreamer 4 以 shortcut forcing 实现**单 GPU 实时交互推理**，并首次做到纯离线数据在 Minecraft 取得钻石（[arXiv:2509.24527](https://arxiv.org/abs/2509.24527)）。`[摘要级]`
3. **机器人侧世界模型以「少量真机数据 + 零样本部署」为标志**：V-JEPA 2-AC 仅用 **<62 小时**无标注 Droid 数据 post-train，零样本在 Franka 上做图像目标规划抓放。`[摘要级]`
4. **平台化路线把世界模型做成可被下游 fine-tune 的基础设施**：Cosmos 开源因果视频 tokenizer 与 Predict1 多规格模型（7B / 12B / 13B / 14B）。`[摘要级]`
5. **可复核的公开数字多为作者自述、评测条件互不统一**，跨系统横向比较必须先回到各自 benchmark 定义（见章 5）。`[精读原文]`

### 4.2 机制/证据（逐条注明来源与等级）

| 系统 | 关键实测数字 | 出处 | 主等级 |
| :-- | :-- | :-- | :-- |
| **Genie 3**（Google DeepMind） | 实时导航 **24 FPS**、分辨率 **720p**、一致性维持**数分钟** | [官方博客 2025-08-05](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) | `[摘要级]` |
| **GameNGen** | DOOM，320×240；**单 TPU 20 FPS**；**PSNR 29.43 / LPIPS 0.249**（5 关卡 2048 条轨迹）；连续游玩 **5–10 分钟**后人类判别仍接近随机 | [arXiv:2408.14837](https://arxiv.org/abs/2408.14837) 正文 | `[精读原文]` |
| **Dreamer 4** | **单 GPU 实时交互推理**（shortcut forcing + 高效 transformer）；纯离线数据在 Minecraft **首次取得钻石** | [arXiv:2509.24527](https://arxiv.org/abs/2509.24527) 正文 | `[摘要级]` |
| **V-JEPA 2 / V-JEPA 2-AC** | 预训练 **>1M 小时**互联网视频；2-AC 用 **<62h** Droid 无标注视频 post-train；**零样本** Franka 抓放 | [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) 正文 | `[摘要级]` |
| **Cosmos WFM**（NVIDIA） | 平台化：视频 curation 流水线 + **因果视频 tokenizer** + **Cosmos-Predict1 7B/12B/13B/14B** + 开放权重 | [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) 正文 | `[摘要级]` |
| **Matrix-Game** | **17B 参数**；Matrix-Game-MC 数据集 **>2,700 小时** Minecraft；配套 **GameWorld Score** | [arXiv:2506.18701](https://arxiv.org/abs/2506.18701) 正文 | `[摘要级]` |
| **Hunyuan-GameCraft** | 推理**加速 20×**，达 **6.6 FPS** | [arXiv:2506.17201](https://arxiv.org/abs/2506.17201) 正文 | `[摘要级]` |
| **CausVid** | 当前实现约 **10 FPS**（作者称可经编译/量化/并行进一步优化） | [arXiv:2412.07772](https://arxiv.org/abs/2412.07772) 正文 | `[摘要级]` |
| **Self Forcing** | **17.0 FPS**、**亚秒级延迟** | [arXiv:2506.08009](https://arxiv.org/abs/2506.08009) 正文 | `[摘要级]` |
| **Genie（2024）** | **11B 参数**；无标注互联网视频无监督训练；潜动作模型（latent action model） | [arXiv:2402.15391](https://arxiv.org/abs/2402.15391) 摘要 | `[摘要级]` |
| **DIAMOND** | 图像空间扩散世界模型，可作环境 **drop-in 替代**；**3 NFE/帧**（对比 IRIS 的 16 NFE/帧） | [arXiv:2405.12399](https://arxiv.org/abs/2405.12399) 正文 | `[摘要级]` |

**本轮新发现（归属本专题，供章 2/3 第三轮使用）**：帧率数字的**评测口径差异极大**——20 FPS（GameNGen，320×240，单 TPU）与 24 FPS（Genie 3，720p，官方博客）不可直接比较；Self Forcing 的 17.0 FPS 与 Hunyuan-GameCraft 的 6.6 FPS 属不同分辨率/任务设定，横向对比须同时给出分辨率与硬件。`[摘要级]`

### 4.3 本章链接核验

见文末「链接核验清单」：参考文献 13（GameNGen）、10（Dreamer 4）、9（V-JEPA 2）、16（Cosmos）、14（Matrix-Game）、15（Hunyuan-GameCraft）、18（CausVid）、19（Self Forcing）、12（Genie）、42（DIAMOND）、20（Genie 3 博客）。

---

## 5. 评测与基准

### 5.1 本章结论

1. **评测呈三层碎片化**：通用视频质量（VBench，16 维）、内在真实性/物理（VBench-2.0 五维、Physics-IQ 五类物理）、世界级属性（WorldScore 的可控性/质量/动态）。三者维度定义互不重叠，**无法相互替代**。`[摘要级]`（VBench）+ `[精读原文]`（其余）
2. **交互性指标仍靠各系统自报**（帧率、一致性时长、PSNR/LPIPS），**缺统一第三方基准**；这也是章 4 数字不可直接比较的根因。`[精读原文]`
3. **具身侧已出现世界模型专用评测**：EWMBench（Genie Envisioner）测视觉保真、物理一致性、指令-动作对齐；游戏侧有 GameWorld Score（Matrix-Game）。`[摘要级]`
4. **规则模拟器 benchmark 在本专题只作环境，不作世界模型评测口径**（章 1.2 排除口径一致）。`[精读原文]`

### 5.2 机制/证据：benchmark 对照

| benchmark | 维度 / 指标 | 面向对象 | 主等级 | 来源 |
| :-- | :-- | :-- | :-- | :-- |
| **VBench** | **16 个**层级化、解耦维度（各配 prompt 与评测方法） | 通用视频生成质量 | `[摘要级]` | [arXiv:2311.17982](https://arxiv.org/abs/2311.17982) 摘要 |
| **VBench-2.0** | **5 个**维度：Human Fidelity / Controllability / Creativity / Physics / Commonsense（细分为 **18 维**，针对 intrinsic faithfulness） | 视频生成的「内在真实性」 | `[精读原文]` | [arXiv:2503.21755](https://arxiv.org/abs/2503.21755) 正文 |
| **WorldScore** | **3 个**方面：controllability / quality / dynamics；含统一 world specification + 数据集 + 多面指标；评测 **19 个**代表模型 | 世界生成（世界模型统一评测的最接近形态） | `[精读原文]` | [arXiv:2504.00983](https://arxiv.org/abs/2504.00983) 正文 |
| **Physics-IQ** | **5 类物理**：Solid Mechanics / Fluid Dynamics / Optics / Thermodynamics / Magnetism；预测后续 **5 秒**；含 Sora / Runway / Pika / Lumiere / SVD / VideoPoet 对照 | 物理理解 | `[精读原文]` | [arXiv:2501.09038](https://arxiv.org/abs/2501.09038) 正文 |
| **GameWorld Score** | 游戏世界交互质量（随 Matrix-Game 发布） | 游戏域交互式世界模型 | `[摘要级]` | [arXiv:2506.18701](https://arxiv.org/abs/2506.18701) 正文 |
| **EWMBench** | 视觉保真 / 物理一致性 / 指令-动作对齐 | 机器人操作世界模型 | `[精读原文]` | [arXiv:2508.05635](https://arxiv.org/abs/2508.05635) 正文 |
| 系统自报指标 | FPS / 一致性时长 / PSNR / LPIPS | 各交互式系统 | `[精读原文]` | 见章 4.2 |

**缺口清单（本轮结论）**：① 跨域统一口径缺失（视频 / 游戏 / 机器人各说各话）；② **交互性**（action-following 延迟、可交互时长）的统一跨域基准尚未在本专题完成核验；③ 长时程记忆无可比指标；④ sim-to-real 对齐度指标缺位（与 EmbodiedVLA 条目章 5 的「仿真分数不足以替代真机结论」互为佐证）。`[精读原文]`

### 5.3 本章链接核验

见文末清单：参考文献 25（VBench）、26（VBench-2.0）、27（WorldScore）、28（Physics-IQ）、14（GameWorld Score）、40（EWMBench）。

> **第三轮加深**：「评测碎片化 / 不可比性」的机制级拆解（帧率口径 / 指标口径 / 训练-推理错配口径 / 交互性空白）见横切专题 [topics/incomparability-checklist.md](topics/incomparability-checklist.md)。`[精读原文]`

---

## 6. 应用域

### 6.1 本章结论

1. **世界模型在具身侧被消费为三类资源**：①想象中训练（RL in imagination）；②可交互练习环境；③评测环境（与 EmbodiedVLA 条目 §4.3 的接口定义一致）。VLA 侧关于合成数据、想象 RL 和真机迁移的论文比较见[世界模型到 VLA 迁移专题](../EmbodiedVLA/topics/world-model-to-vla-transfer.md)。`[精读原文]`
2. **数据接口呈「少量真机 + 大规模无标注视频」组合**：V-JEPA 2-AC 用 **<62h** Droid 无标注数据；Cosmos 提供 curation 流水线与 tokenizer；游戏域 Matrix-Game-MC **>2,700h**（不可直接迁移到机器人）。`[摘要级]`
3. **评测接口开始专门化**：**EWMBench**（视觉保真 / 物理一致性 / 指令-动作对齐）是机器人操作场景的专用套件；Genie Envisioner 同时提供 **GE-Sim** 作 action-conditioned 神经模拟器以支持闭环 rollout。`[精读原文]`
4. **UniSim 与 Cosmos 代表两种平台化姿态**：前者主张「学一个真实世界交互的通用模拟器，使具身 agent 纯在模拟中训练后直接部署」；后者把世界模型做成 Physical AI 的**世界数字孪生**（digital twin of the world，与政策模型并列）。`[摘要级]`
5. **归属**：本节对象的世界模型/环境侧归本专题，策略/动作侧归 `EmbodiedVLA`（见章 7 互引）。`[精读原文]`

### 6.2 机制/证据：具身与机器人（世界模型作为环境/训练信号）

| 对象 | 作为环境的角色 | 关键事实 | 主等级 |
| :-- | :-- | :-- | :-- |
| **[Dreamer 4](https://arxiv.org/abs/2509.24527)** | ①想象中训练 | 在可扩展世界模型内部做 RL；纯离线数据在 Minecraft 取得钻石；作者将「离线想象训练」对齐机器人场景（真机交互不安全、缓慢） | `[摘要级]` |
| **[UniSim](https://arxiv.org/abs/2310.06114)** | ①+②通用模拟器 | 以生成式建模学习真实世界交互的通用模拟器，目标包含「机器人在模拟经验中学习后直接部署真机」 | `[精读原文]` |
| **[Genie Envisioner](https://arxiv.org/abs/2508.05635)** | ②+③平台 | GE-Base（指令条件视频扩散世界模型）+ GE-Sim（action-conditioned 神经模拟器，闭环 rollout）+ EWMBench（评测） | `[精读原文]` |
| **[Cosmos WFM](https://arxiv.org/abs/2501.03575)** | ①工业化形态 | Physical AI 的「世界数字孪生」；覆盖 curation / 预训练 / post-train / tokenizer 全链路并开放权重 | `[摘要级]` |
| **[V-JEPA 2-AC](https://arxiv.org/abs/2506.09985)** | ②规划环境 | 62h Droid 数据 post-train 后零样本规划抓放（少量真机数据范式） | `[摘要级]` |

**数据/评测接口清单（可直接复用，避免二次造轮子）**

| 接口 | 类型 | 规模/维度 | 域 | 主等级 |
| :-- | :-- | :-- | :-- | :-- |
| Droid（经 V-JEPA 2-AC 使用） | 真机数据 | <62h 无标注 | 机器人操作 | `[摘要级]` |
| Matrix-Game-MC | 交互数据 | >2,700h | 游戏（Minecraft） | `[摘要级]` |
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

1. **判据落地为三条判定**：(i) 交付物是**动作策略** → Embodied；(ii) 交付物是**环境/状态演化** → WorldModels；(iii) **双交付物** → 按分支归属，同一论文可被两处引用而**互不吞并**。`[摘要级]`（对 V-JEPA 2-AC / WorldVLA 的正文与摘要判定）
2. **π0 类 action head → Embodied**：输出为动作策略，不因「内置世界模型或流匹配」改判。`[摘要级]`（arXiv:2410.24164 摘要）
3. **WorldVLA → 按交付物拆分**：其动作分支归 `EmbodiedVLA`，未来帧预测（world）分支归本专题。`[摘要级]`（arXiv:2506.21539 摘要）
4. **V-JEPA 2-AC → world 侧归本专题**：其交付物是 **action-conditioned 潜空间世界模型**（预测未来表示）；在 Franka 上的抓放部署属应用验证，不改变归属。`[摘要级]`
5. **与 EmbodiedVLA 的口径一致性已确认**：两侧均以「交付物判定」为最高裁决规则；冲突时以交付物为准并同步修订。`[精读原文]`

### 7.2 机制/证据：判据落到具体工作

| 具体工作 | (a) | (b) | (c) | 归属判定 | 主等级 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **π0**（VLA flow model） | — | ✗ 交付物是策略 | ✓（用预训练 VLM/世界知识） | **Embodied**（`EmbodiedVLA`） | `[摘要级]` |
| **OpenVLA** | — | ✗ | ✓ | **Embodied** | `[摘要级]` |
| **WorldVLA** | ✓ | ✓（未来帧）+ ✗（动作侧） | ✓ | **拆分**：world 分支→本专题；动作分支→EmbodiedVLA | `[摘要级]` |
| **V-JEPA 2-AC** | ✓ | ✓ | ✓ | **WorldModels**（本专题章 2/4）；机器人应用登记在章 6 | `[摘要级]` |
| **Dreamer 4** | ✓ | ✓ | ✓ | **WorldModels**；其 agent 训练属具身应用（章 6） | `[摘要级]` |
| **Genie 3 / GameNGen** | ✓ | ✓ | ✓ | **WorldModels** | `[摘要级]` / `[摘要级]` |
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

## 9. 跨系统对比总表（第三轮补，10 篇精读汇总）

> **读法**：本表只做**定性对照**，不做排行榜；每行的数字都**带条件**（环境/步数/硬件），脱离条件引用即为不可比（判据见 [topics/incomparability-checklist.md](topics/incomparability-checklist.md)）。所有单元格均可回溯到 `papers/` 对应分册。

| 系统（年） | 预测目标 | 动作条件化 | 可渲染/可交互 | 行为派生 | 训练信号 | 关键数字（带条件） | 主失效条件 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| World Models (2018) | 观测重构 + 潜空间转移 | ✅ 潜变量层（MDN-RNN） | ⚠️ 潜空间可 rollout、像素为近似重构 | 进化控制器（CMA-ES，867 参数） | CarRacing 真实回报；Doom 模型预测终止 | CarRacing 连续 100 次 rollout 均回报 **906 ± 21**（1 万条随机 rollout 训练） | 世界模型被**钻空子**；VAE 与任务无关；无分层规划 |
| PlaNet (2018) | 观测重构（仅作训练信号） | ✅ RSSM 确定性路径 | ⚠️ 潜空间 | CEM + MPC 在线规划 | 无策略训练 | 比 model-free 少约 **200×** 环境交互（DMC 图像） | 规划开销高；多步误差累积；过自信 |
| MuZero (2019) | **reward/policy/value**（不重构） | ✅ 进搜索树 | ❌ 不可渲染 | MCTS | 自我对弈/环境回报 | Atari **42/57** 超 R2D2；棋盘追平 AlphaZero（**不知规则**）；Reanalyze 中位 **731%**（200M frames/game） | 依赖搜索与数据预算；不训练观测解码器；不证明观测信息全丢 |
| Dreamer (2019) | 观测重构 + 潜空间 | ✅ RSSM | ⚠️ 潜空间 | 想象里 actor-critic（解析梯度） | 价值模型估计想象时域外回报 | **5×10⁶ 步 823** > D4PG 在 **10⁸ 步**的 786；20 任务 16 胜 4 平 | 想象误差 → 策略误差；表征瓶颈；短视风险 |
| DreamerV3 (2023) | 同上 + 鲁棒化 | ✅ | ⚠️ 潜空间 | 同上（固定超参） | 同上 + 回报归一化 | 固定超参跨 **150+ 任务**；首个从零 Minecraft 钻石 | 仍是想象训练；归一化阈值敏感；观测重构仍占容量 |
| UniSim (2023) | 视频帧（动作进-视频出） | ✅ 伪动作（文本/机器人指令） | ✅ 视频 | 高层 VLM 策略 + 逆动力学 | 多源编排的视频-动作对 | 真机 **Language Table 零样本**（**域内**）；HM3D **700 样本**；**4 帧 > 1 帧** | 数据集信息鸿沟；域标识符伤泛化；长程一致性未证 |
| V-JEPA (2024) | 表征（被遮挡区域） | ❌ action-free | ❌ 不生成 | 无（只出表征） | 视频自监督 | K400 **81.9** / SSv2 **72.2** / IN1K **77.9**（frozen backbone） | 不可生成；无动作条件；不证明物理理解 |
| GameNGen (2024) | **像素即状态** | ✅ 去噪层 | ✅ 实时可玩 | 外部玩家/agent | 真实游戏回放 + 噪声增强 | **20 FPS**（320×240，单 TPU）；PSNR **29.4** / LPIPS **0.249** | 非精确模拟；单域；需真环境采数据；无长期记忆机制 |
| Physics-IQ (2025) | —（评测） | — | — | — | — | **8 个模型**在 5 类物理 66 场景下**物理理解严重受限且与画质无关** | 只覆盖 5 类物理；静态相机；模型覆盖不全 |
| VBench-2.0 (2025) | —（评测） | — | — | — | — | **5 维 18 子维**内在真实性框架 | 不测交互；自动评判与真拍口径不可互换 |

**三条可直接用于选型的结论**：
1. **要"可渲染可交互"** → 只有 GameNGen / UniSim 一类（像素或视频级）；
2. **要"能规划"** → 潜空间系（PlaNet/Dreamer）或搜索系（MuZero），但**MuZero 不可渲染**；
3. **要"当训练环境"** → World Models / Dreamer 系（RL 策略）与 UniSim（视觉-语言-动作策略），**用于评测时的真实环境对齐证据仍待补充，不能据本页选文断言领域空白**。

---

## 10. 失效边界综述（按类归纳）

把 10 篇的"失效条件"章节合并归纳，得到**六类**可复用的边界。每类都给：机制 → 证据 → 引用时要注意什么。

### 10.1 模型被策略钻空子（对抗性利用）

- **机制**：策略在模型内训练，会过拟合模型缺陷，找到"梦里高分、真环境失效"的对抗策略。
- **证据**：World Models §4.5（MDN-RNN 是近似概率模型）；缓解手段只有**温度 τ**。`[精读原文]`
- **引用注意**：任何"在模型里训练成功"的结论，都要问"它怎么防钻空子"。

### 10.2 误差传播（模型误差 → 策略误差）

- **机制**：训练信号完全来自模型，模型差则梯度差、策略差。
- **证据**：Dreamer（作者列更高视觉复杂度为 future work）；DreamerV3（鲁棒损失工程使误差**跨域可控但不消除**）；PlaNet（多步误差累积、多峰未来、分布外过自信）。`[精读原文]`
- **引用注意**：与 10.1 的区别是"被动不准"与"主动利用"；两者共同前提是模型足够好。

### 10.3 表征瓶颈（重构占用容量）

- **机制**：默认用像素重构学表征 → 高视觉复杂度下容量被无关细节吃掉。
- **证据**：PlaNet（观测模型只是训练信号、重构质量 ≠ 规划好用）；DreamerV3 用 symlog/free bits 缓解；MuZero 直接放弃重构。`[精读原文]`
- **引用注意**：**模型质量与画质不是一回事**——这是"视觉真实感 ≠ 物理理解"（10.6）的机制侧对应。

### 10.4 长时程漂移（自回归与一致性）

- **机制**：像素级自回归逐步生成，误差累积导致画面/状态漂移。
- **证据**：GameNGen（用**噪声增强**压制漂移；作者明说不是逐位精确的引擎；人类判别在**自回归 5–10 分钟后**接近随机水平）；UniSim（8 次指令交互能保持部分物体状态，但**未证明任意长时程**）。`[精读原文]`
- **引用注意**："多分钟稳定"必须带**时长窗口**与**分辨率/硬件**。

### 10.5 数据与域约束（信息鸿沟、域标识符）

- **机制**：多源数据由不同社区为不同目的采集，信息发散是天然上限；域标识符提升域内质量但伤泛化。
- **证据**：UniSim（信息鸿沟是物理上限；域标识符的双刃剑；静态图文只能当"单帧 + 字幕动作"）。`[精读原文]`
- **引用注意**：**"零样本迁移"必须带"域内/跨域"限定**。

### 10.6 评测与理解的错位（不可比、不可外推）

- **机制**：口径错位（感知 vs 物理、自动 vs 人评、分辨率/硬件不同）使跨系统数字不可比。
- **证据**：Physics-IQ（视觉真实感 ≠ 物理理解；8 模型 5 类物理 66 场景）；VBench-2.0（5 维 18 子维、不测交互）；GameNGen 人评口径（3 秒片段）。`[精读原文]`
- **引用注意**：见 [topics/incomparability-checklist.md](topics/incomparability-checklist.md) 的**六问检查表**。

> **六类的共同点**：**"条件"是结论的一部分**。删掉条件（环境、步数、硬件、域、时长、口径）之后，数字就不再是证据。

---

## 11. 演进时间线（每个节点"新增了什么判据/机制"）

| 年 | 节点 | 新增机制 | 对判据的贡献 |
| :-- | :-- | :-- | :-- |
| 2018 | World Models | VAE + MDN-RNN + 线性控制器；**梦境训练再迁移** | 首次完整演示"学到的环境里训练"（(a)(b)(c) 三判据第一次同时被满足） |
| 2018 | PlaNet | **RSSM**（确定+随机）+ latent overshooting；CEM+MPC | 把"从像素学动力学"做到可用；确立"模型内规划"范式 |
| 2019 | MuZero | **只预测 reward/policy/value**，隐状态不对应观测 | 暴露"世界模型"术语歧义：学得隐动力学可支撑规划；可渲染性须另列，不能判作动作无关 |
| 2019 | Dreamer | 想象训练 + actor-critic（解析梯度） | 把"用模型"从在线规划改为**学策略**，交互量降一个量级 |
| 2023 | DreamerV3 | symlog / free bits / KL 平衡 / 回报归一化 | 让"想象训练"跨域可用（固定超参跨 150+ 任务） |
| 2023 | UniSim | 多源数据**编排**成动作进-视频出模拟器 | 把"世界模型当训练环境"推到真机零样本（域内） |
| 2024 | V-JEPA | 纯特征预测、frozen backbone | 明确 **action-free 表征**这一支（原始 V-JEPA 不满足动作条件 a） |
| 2024 | GameNGen | 扩散去噪层动作条件 + 噪声增强 | 把"可交互像素世界模型"推到**实时**（20 FPS） |
| 2025 | Physics-IQ | 真实拍摄 + 受控物理方差的物理理解基准 | **证伪**"视觉真实感 ⇒ 物理理解" |
| 2025 | VBench-2.0 | 5 维 18 子维内在真实性评测 | 把评测从"表面真实感"推到"内在真实性"（仍不测交互） |

**读时间线的三个要点**：
1. **判据不是一直存在的**——(a)(b)(c) 是事后归纳；早期工作（World Models）同时满足，MuZero 的规划接口与 V-JEPA 的表征接口不同，不能因二者都不渲染就作同一归类；
2. **机制演进的主轴是"用模型的方式"**：进化控制器 → 在线规划 → 想象里学策略 → 当训练环境；
3. **评测落后于生成**：生成能力从 2018 走到 2025 实时可玩，而**本专题尚未建立交互性评测的跨域可比口径**。

---

## 12. 选型指引（按诉求选线）

| 你的诉求 | 选哪条线 | 具体系统 | 必须接受的代价 |
| :-- | :-- | :-- | :-- |
| **要可渲染、可交互的环境**（人能玩/能看未来） | 像素/视频生成式 | GameNGen（实时、单域）、UniSim（多源、视频级） | 漂移需噪声增强；单域或信息鸿沟；评测口径不统一 |
| **要能在模型里做规划** | 潜空间 + 搜索 | PlaNet（在线规划）、MuZero（搜索，**不可渲染**） | 规划开销；模型不准则崩；MuZero 原模型不提供观测解码器 |
| **要训练 RL 策略**（省交互） | 想象训练 | Dreamer / DreamerV3 | 想象误差 → 策略误差；需防钻空子；表征瓶颈 |
| **要训练视觉-语言-动作策略** | 动作进-视频出模拟器 | UniSim | 域内零样本，跨域未证明；动作是"伪动作" |
| **只要通用视觉表征**（不要环境） | 特征预测 | V-JEPA | 不能规划、不能生成、不证明物理理解 |
| **要评测"懂不懂物理"** | 真实拍摄基准 | Physics-IQ（物理理解）、VBench-2.0（内在真实性） | 两套口径不可互换；都不测交互 |

---

## 13. 选文说明（第三轮）

- **候选池 22 篇 → 入选 10 篇 → 排除 12 篇**；入选门槛与淘汰标准、逐条排除理由见 [sources/CANDIDATES.md](sources/CANDIDATES.md)；
- **原文出处与许可证提示**见 [sources/MANIFEST.md](sources/MANIFEST.md)：本仓库**只存清单与我们的精读分册，不存论文全文**；
- **下一轮首选补的候选**：Genie（`2402.15391`，生成式可交互环境）、Cosmos（`2501.03575`，世界基础模型平台）、TD-MPC2（`2310.16828`，无解码器规划线，可作判据 (a) 的对照）。

---

## 14. 本轮增量、证据一致性说明与下轮计划

**本轮（第三轮）增量**
1. `papers/` **10 篇逐篇精读**（每篇 ≥200 行：方法细节 / 实验数字带条件 / 消融 / 失效边界 / 对条目结论的影响；开头含「亮点与差异」四行）；
2. `topics/` **3 篇横切专题**（机制轴 / 作环境 / 不可比性，各 150–300 行）；
3. 本页新增 **§9 跨系统对比总表 · §10 失效边界综述 · §11 演进时间线 · §12 选型指引 · §13 选文说明**，把"逐篇证据"收敛成可查阅的总纲；
4. `sources/` 新增 **MANIFEST（原文清单）** 与 **CANDIDATES（候选与排除）**。

**证据一致性说明（已修复，2026-10-17 04:1x）**
- 原问题：章 2/4/6 与参考文献把 **V-JEPA 2（`2506.09985`）**、**Dreamer 4（`2509.24527`）** 等**无 `papers/` 分册**的外部工作标为 `[精读原文]`，与 `topics/*` 里按 `[摘要级]` 引用的写法**自相矛盾**；
- 处理：依「**`[精读原文]` 仅授予有对应分册的论文**」的范围规则（见文首约定），把**所有无分册的正文级引用统一下调为 `[摘要级]`**（V-JEPA 2 / Dreamer 4 / Cosmos / Matrix-Game / Hunyuan-GameCraft / CausVid / Self Forcing / DIAMOND / WorldScore / Genie Envisioner 等），正文共调整 **36 处**；同时把**有分册但此前标成 `[摘要级]`** 的 6 条（World Models / PlaNet / MuZero / Dreamer / DreamerV3 / V-JEPA）**升回 `[精读原文]`**；
- 调整后**参考文献按主等级统计：`[精读原文]` 10 条 = 10 篇分册（一一对应）；`[摘要级]` 31 条；`[二手]` 1 条；`[受限核验]` 0 条**（合计 42 条，可逐条核对）；
- 影响：这些工作的**具体数字不再进入精读级结论**，仅作为"存在该路线/该量级"的线索；10 篇入选论文的 `[精读原文]` 等级不变；
- 复核依据：独立复验中把这处"证据升格"列为合并前必改项（本页 §14 保留记录，便于回溯）。


**下轮计划**
- 补 Genie / Cosmos / TD-MPC2 三篇（见 §13）；
- 若确认要做"世界模型作评测环境"，需先解决 §10.6 的口径问题（否则在模型里测出的分数不可信）。

---

## 15. 术语表（读本条目所需的最小集合）

> 只收**本条目用到的机制术语**，每条给"是什么 + 谁在用 + 在哪一章/分册"；定义以入选分册的正文为准。

| 术语 | 是什么 | 谁在用 | 出处 |
| :-- | :-- | :-- | :-- |
| **RSSM**（Recurrent State Space Model） | 循环状态空间模型：**确定性路径**（记历史） + **随机路径**（建模不确定性）双分量 | PlaNet / Dreamer / DreamerV3 | [papers/1811.04551](papers/1811.04551-planet.md) §1.2 |
| **latent overshooting** | 多步变分目标：不只训 1 步预测，强制多步一致性 | PlaNet | 同上 §1.3 |
| **CEM**（Cross-Entropy Method） | 种群采样 + 精英筛选 + 迭代的免梯度优化，用作模型内规划器 | PlaNet | 同上 §1.4 |
| **MPC**（Model Predictive Control） | 滚动时域：每一步重新规划，只执行第一个动作 | PlaNet | 同上 |
| **MCTS** | 蒙特卡洛树搜索；MuZero 用学到的模型在搜索树里展开 | MuZero | [papers/1911.08265](papers/1911.08265-muzero.md) §1.1 |
| **Reanalyze** | MuZero 变体：用当前模型重新分析旧轨迹 | MuZero | 同上 §2 |
| **free bits** | 给每个潜变量维度的 KL 设下界，防退化解 | DreamerV3 | [papers/2301.04104](papers/2301.04104-dreamerv3.md) §1.2 |
| **symlog** | 对称对数压缩，处理跨域数量级差异 | DreamerV3 | 同上 |
| **twohot** | 用两个相邻桶表示连续量（用于回报预测） | DreamerV3 | 同上 |
| **KL 平衡** | 对先验/后验使用不同学习率，稳住表征 | DreamerV3 | 同上 |
| **回报归一化（5th–95th 分位 + EMA）** | 把回报压到可比范围，跨域复用超参 | DreamerV3 | 同上 |
| **frozen backbone** | 评测协议：冻住主干，只训下游探针 | V-JEPA | [papers/2404.08471](papers/2404.08471-vjepa.md) §2 |
| **action-free** | 训练目标不含动作 → 不能回答"做 a 会怎样" | V-JEPA | 同上 §1.1 |
| **噪声增强（noise augmentation）** | 训练时给历史帧加噪，抑制自回归漂移 | GameNGen | [papers/2408.14837](papers/2408.14837-gamengen.md) §1.3 |
| **teacher forcing / 自回归推理错配** | 训练用真历史、推理用自己生成的历史，天然错配 | GameNGen | 同上 §1.1 |
| **逆动力学模型** | 从相邻视频帧反推动作，使视频可被机器人执行 | UniSim | [papers/2310.06114](papers/2310.06114-unisim.md) §1.2 |
| **域标识符（domain identifier）** | 标明数据来源的 token：提升域内质量、**伤跨域泛化** | UniSim | 同上 §4 |
| **伪动作（pseudo-action）** | 把文本指令/机器人动作当"动作"喂给生成式模拟器 | UniSim | 同上 §1.1 |
| **受控物理方差** | Physics-IQ 的基准设计：只靠真懂物理才能做对的真实拍摄场景 | Physics-IQ | [papers/2501.09038](papers/2501.09038-physics-iq.md) §1.1 |
| **内在真实性（intrinsic faithfulness）** | VBench-2.0 的评测目标：物理、常识、人体结构、构图完整性等 | VBench-2.0 | [papers/2503.21755](papers/2503.21755-vbench-2.md) §1.1 |
| **人类判别协议** | 用人类对短片段（3 秒）判断真假，作为可玩性/画质口径 | GameNGen | 同上 §2 |

---

## 16. 可引用事实清单（每条都带限定，复制即用）

> 用途：**写别的文档时直接引用这里的句子**，避免把带条件的数字写成无条件结论。每条都可回溯到分册。

1. **World Models**：在 CarRacing-v0（俯视像素、1 万条随机 rollout 训练、867 参数线性控制器 + CMA-ES）下，连续 100 次 rollout 平均回报 **906 ± 21**（求解线 ≥900）。—— 引用时不得省略"1 万条随机 rollout"与"连续 100 次"。
2. **World Models（失效）**：世界模型会被控制器**钻空子**（梦里高分、真环境失效）；作者给出的缓解只有调温度 τ。
3. **PlaNet**：在 DeepMind Control Suite（图像输入）上，比 model-free 基线**少约 200× 环境交互**，代价是每步一次 CEM 搜索（慢一个量级）。
4. **MuZero**：Atari **57 个游戏里 42 个**超过 R2D2；Go/chess/shogi 上追平获得规则的 AlphaZero（MuZero 未知规则）；Reanalyze 变体（200M frames/game）中位归一化得分 **731%**。**它不重构观测、不可渲染**。
5. **Dreamer**：DMC 图像输入，**5×10⁶ 环境步平均 823**，超过 D4PG 在 **10⁸ 步**下的 786；20 个任务里 **16 胜 4 平**；每 10⁶ 步约 3 小时。
6. **DreamerV3**：**固定超参**跨 **150+ 任务**；首个**从零**（无人类数据、无课程）在 Minecraft 拿到钻石；模型变大 → 分数更高**且**交互更少。
7. **UniSim**：仿真训练的策略**零样本**部署到真机 **Language Table**（**同一真机域**）；Habitat/HM3D 低数据域仅 **700 样本**；历史帧消融显示 **4 帧 > 1 帧**，**指数间隔过远的 4 帧反而更差**。
8. **V-JEPA**：2M 公开视频、frozen backbone：**K400 81.9 / SSv2 72.2 / IN1K 77.9**；**action-free**，不生成、不能规划。
9. **GameNGen**：单 TPU 上 **20 FPS**（320×240）实时模拟 DOOM；下一帧 **PSNR 29.4 / LPIPS 0.249**；人类判别在**自回归 5–10 分钟后**接近随机水平；作者明说**并非逐位精确**的游戏引擎。
10. **Physics-IQ**：**8 个**视频生成模型在 **5 类物理、66 个场景**下**物理理解严重受限，且与视觉真实感无关**；个别用例已可解出。
11. **VBench-2.0**：**5 维 18 子维**的内在真实性评测；**不测交互**；自动评判与真实拍摄口径**不可互换**。

**使用规则**：上表任何一条**只可在其限定条件内引用**；跨系统比较前先过 [topics/incomparability-checklist.md](topics/incomparability-checklist.md) 的六问。

---

## 17. 阅读路径（按读者目的）

本条目是三层结构（本页总纲 + `papers/` 逐篇 + `topics/` 横切），不同目的走不同路径：

| 你的目的 | 建议路径 | 读完能回答 |
| :-- | :-- | :-- |
| **5 分钟了解这条线是什么** | 本页 §0 → §11 时间线 → §12 选型指引 | 世界模型有哪些用法、"可渲染/可规划/可当环境"分别是什么 |
| **做技术选型**（要可渲染/要规划/要训练环境） | §9 对比总表 → §12 选型指引 → 对应 `papers/` 分册 §2 | 该选哪条线、代价是什么、需要什么数据 |
| **评估某个宣称"世界模型"的系统** | §1 判据 → §7 边界 → [topics/dynamics-and-action-conditioning.md](topics/dynamics-and-action-conditioning.md) §7（走判据） | 它算不算世界模型、缺哪一条判据 |
| **引用具体数字/做对比** | §16 可引用事实清单 → [topics/incomparability-checklist.md](topics/incomparability-checklist.md) 六问 | 这个数字能不能引用、必须带什么限定 |
| **做研究选题** | §8 未决问题 → §13 选文说明（下一轮候选） | 哪些需要补证（评测环境、交互基准、跨域零样本） |
| **要看机制细节** | 对应 `papers/` 分册（方法/实验/消融/失效边界） | 该系统的具体设计、关键超参、失效条件 |

---

## 18. 本轮方法学注记（证据是怎么处理的）

第三轮共处理 10 篇精读 + 3 篇专题，过程中有五类证据问题与对应的处理方式——**记在这里，便于复核与复用**：

1. **术语歧义（"世界模型"三种用法）**：不追求唯一定义，改用**可判定的三判据 (a)(b)(c)** 做筛选，把 MuZero/V-JEPA 明确标为"边界样本"而非"不合格"。
2. **同一系统多篇论文（Dreamer 系）**：按**论文**计数而非系统计数（Dreamer、DreamerV3 各占一篇分册），避免"同一系统记两次"；DreamerV2 因被 V3 取代而进排除清单（见 [sources/CANDIDATES.md](sources/CANDIDATES.md)）。
3. **"提到了但没精读"的引用**：章 2/4/6 出现过 V-JEPA 2 与 Dreamer 4；本轮**不擅自改他人标注**，而是在 §14 登记一致性说明，并在本页/topics 引用时按 `[摘要级]` 处理——**宁可低估，不可升格**。
4. **数字可比性**：凡是跨系统的数字对照，一律先过"六问"（分辨率+硬件、指标口径、训练-推理错配、数据域、评测协议、感知 vs 物理）；不满足就写"条件不同，不作直接比较"。
5. **总纲与分册的边界**：分册给**证据**（方法/数字/失效），总纲给**对照与判定**（§9 表、§10 归类、§12 选型）；同一内容**不在两处重复展开**，只做指向。

**可复用的三条做法**（供后续条目套用）：
- **先筛选后精读**：候选池 → 排除留痕 → 入选分册（见 `sources/CANDIDATES.md`）；
- **每篇分册开头四行「亮点与差异」**：一句话亮点 / 新在哪 / 证据强度 / 值不值得引用；
- **失效边界单列**：每篇必须有独立"失效条件"小节，总纲再做跨篇归类（§10）。

---

## 19. 三张缺口清单（评测 / 数据 / 部署）

> 与 §8「未决问题」的分工：§8 记**问题**，本清单记**可执行的缺口**（缺什么、证据在哪、补的入口是什么）。

### 19.1 评测缺口

| 缺口 | 现状证据 | 补的入口 |
| :-- | :-- | :-- |
| **交互性评测覆盖尚未核全** | VBench-2.0（内在真实性）、Physics-IQ（物理理解）、WorldScore（`[摘要级]`）**都不测** action-conditioned 响应与延迟 | 需要新基准：动作条件响应准确率、长时程一致性时长、action-following 延迟 |
| **感知与物理不可互换** | Physics-IQ 证明视觉真实感 ≠ 物理理解（8 模型 / 5 类物理 / 66 场景） | 任何"更真 ⇒ 更懂物理"的推论都要附真实拍摄验证 |
| **"在模型里评测"不可信** | 见 [topics/world-model-as-env.md](topics/world-model-as-env.md) §5：模型误差 → 评测分数不可信 | 先解决模型误差上界，再谈"模型即评测环境" |

### 19.2 数据缺口

| 缺口 | 现状证据 | 补的入口 |
| :-- | :-- | :-- |
| **动作标签稀缺** | World Models/PlaNet/Dreamer 靠环境自带动作；GameNGen 需要先训 agent 采数据；UniSim 只能用"伪动作" | 采集带动作标注的真实交互数据，或研究动作无关到有动作的迁移 |
| **多源信息鸿沟** | UniSim：不同社区为不同目的采集，信息发散是**物理上限** | 数据编排之外，需要"信息补齐"的技术（不只是拼接） |
| **跨域零样本无证据** | 现有最强证据（UniSim）是**域内**零样本 | 明确设计跨域实验（不同真机域/不同仿真器） |

### 19.3 部署缺口

| 缺口 | 现状证据 | 补的入口 |
| :-- | :-- | :-- |
| **实时性依赖蒸馏** | GameNGen 单 TPU 20 FPS（320×240）；实时扩散常用 few-step 蒸馏/短程强制（`[摘要级]`） | 报"实时"必须带分辨率+硬件；蒸馏带来的质量损失需单列 |
| **长时程一致性无机制保证** | GameNGen 靠噪声增强压漂移、无显式长期记忆；UniSim 只证 8 次交互 | 显式记忆/检索机制 + 一致性时长指标 |
| **安全与不可逆场景** | 世界模型在"被钻空子"时给出的高分**不可信**（World Models §4.5） | 部署前必须做对抗性利用测试，而非只看真环境回报 |

**三张清单共同指向一件事**：这条线的**生成能力已经跑到实时**，而**度量、数据与安全**三件配套都还没跟上。

---

## 参考文献

> 体例：编号 + 标题 + 一手来源链接 + 证据等级 + 归属章节。**共 42 条（按每条主等级统计）：`[精读原文]` 10 条 + `[摘要级]` 31 条 + `[二手]` 1 条 + `[受限核验]` 0 条**。**范围规则**：`[精读原文]` 仅授予**有 `papers/` 分册**的论文（第三轮起）；无分册的正文级引用一律 `[摘要级]`。

1. World Models (Ha & Schmidhuber, 2018) — [arXiv:1803.10122](https://arxiv.org/abs/1803.10122) — `[精读原文]` — 章1
2. Learning Latent Dynamics for Planning from Pixels (PlaNet) — [arXiv:1811.04551](https://arxiv.org/abs/1811.04551) — `[精读原文]` — 章2
3. Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model (MuZero) — [arXiv:1911.08265](https://arxiv.org/abs/1911.08265) — `[精读原文]` — 章2
4. Dream to Control: Learning Behaviors by Latent Imagination (Dreamer) — [arXiv:1912.01603](https://arxiv.org/abs/1912.01603) — `[精读原文]` — 章2
5. Mastering Atari with Discrete World Models (DreamerV2) — [arXiv:2010.02193](https://arxiv.org/abs/2010.02193) — `[摘要级]` — 章2
6. Mastering Diverse Domains through World Models (DreamerV3) — [arXiv:2301.04104](https://arxiv.org/abs/2301.04104) — `[精读原文]` — 章2
7. Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (I-JEPA) — [arXiv:2301.08243](https://arxiv.org/abs/2301.08243) — `[摘要级]` — 章2
8. Revisiting Feature Prediction for Learning Visual Representations from Video (V-JEPA) — [arXiv:2404.08471](https://arxiv.org/abs/2404.08471) — `[精读原文]` — 章2
9. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning — [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) — `[摘要级]` — 章2/4/6
10. Training Agents Inside of Scalable World Models (Dreamer 4) — [arXiv:2509.24527](https://arxiv.org/abs/2509.24527) — `[摘要级]` — 章2/4/6
11. Transformers are Sample-Efficient World Models (IRIS) — [arXiv:2209.00588](https://arxiv.org/abs/2209.00588) — `[摘要级]` — 章2
12. Genie: Generative Interactive Environments — [arXiv:2402.15391](https://arxiv.org/abs/2402.15391) — `[摘要级]` — 章2/4
13. Diffusion Models Are Real-Time Game Engines (GameNGen) — [arXiv:2408.14837](https://arxiv.org/abs/2408.14837) — `[精读原文]` — 章2/4
14. Matrix-Game: Interactive World Foundation Model — [arXiv:2506.18701](https://arxiv.org/abs/2506.18701) — `[摘要级]` — 章4/5
15. Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation — [arXiv:2506.17201](https://arxiv.org/abs/2506.17201) — `[摘要级]` — 章4
16. Cosmos World Foundation Model Platform for Physical AI — [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) — `[摘要级]` — 章2/4/6
17. cosmos-predict1 官方仓库（NVIDIA） — [官方仓库](https://github.com/nvidia-cosmos/cosmos-predict1) — `[摘要级]` — 章2
18. From Slow Bidirectional to Fast Autoregressive Video Diffusion Models (CausVid) — [arXiv:2412.07772](https://arxiv.org/abs/2412.07772) — `[摘要级]` — 章3/4
19. Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion — [arXiv:2506.08009](https://arxiv.org/abs/2506.08009) — `[摘要级]` — 章3/4
20. Genie 3: A new frontier for world models（官方博客，2025-08-05） — [官方博客](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) — `[摘要级]` — 章4
21. Genie 3 官方模型页 — [官方模型页](https://deepmind.google/models/genie/) — `[摘要级]` — 章4
22. GameNGen 官方项目页 — [官方项目页](https://gamengen.github.io/) — `[摘要级]` — 章4
23. Dreamer 4 官方项目页 — [官方项目页](https://danijar.com/dreamer4/) — `[摘要级]` — 章4
24. V-JEPA 2 官方仓库（Meta） — [官方仓库](https://github.com/facebookresearch/vjepa2) — `[摘要级]` — 章4
25. VBench: Comprehensive Benchmark Suite for Video Generative Models — [arXiv:2311.17982](https://arxiv.org/abs/2311.17982) — `[摘要级]` — 章5
26. VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness — [arXiv:2503.21755](https://arxiv.org/abs/2503.21755) — `[精读原文]` — 章5
27. WorldScore: A Unified Evaluation Benchmark for World Generation — [arXiv:2504.00983](https://arxiv.org/abs/2504.00983) — `[摘要级]` — 章5
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
40. Genie Envisioner: A Unified World Foundation Platform for Robotic Manipulation — [arXiv:2508.05635](https://arxiv.org/abs/2508.05635) — `[摘要级]` — 章5/6
41. Learning Interactive Real-World Simulators (UniSim) — [arXiv:2310.06114](https://arxiv.org/abs/2310.06114) — `[精读原文]` — 章6
42. Diffusion for World Modeling: Visual Details Matter in Atari (DIAMOND) — [arXiv:2405.12399](https://arxiv.org/abs/2405.12399) — `[摘要级]` — 章4

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
