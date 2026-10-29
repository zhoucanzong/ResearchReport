---
display_name: 世界模型
type: topic-research
domain: WorldModel
subject: WorldModels
date: 2026-10-29
evidence: 精读原文
status: needs-review
---

# WorldModels 技术专题调研

**范围**：本条目将世界模型操作性地指为“从数据学习环境状态转移，并可被动作驱动、供规划、训练或评测调用”的模型。像素渲染是一种表示和接口路线，不是所有世界模型的必要条件；世界模型、视频生成模型、策略模型和规则模拟器需按交付物与动力学来源区分。

**阅读提示**：本页负责串起研究路线与跨论文比较；`papers/` 放代表性工作的逐篇机制和实验，`topics/` 比较横切问题。数字均应按论文的模型、环境、数据、硬件和评测协议理解；本文未复现实验。

---

## 阅读入口

建议先用本页建立路线，再按问题阅读 `papers/` 中的逐篇机制与实验，最后用 `topics/` 比较跨论文设计轴。官方发布稿不是论文，Genie 4 的来源和证据边界单列在[官方发布材料读法](sources/genie4-official-release.md)。

**逐篇论文阅读**

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

**官方发布材料（非论文）**

- [Genie 4 官方发布材料读法](sources/genie4-official-release.md)：仅依据 Google DeepMind 2026-10-27 博客，帮助区分官方能力主张与未披露实现；不把演示或产品描述当成技术报告结果。

**跨论文专题**

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
4. **三条架构主线并行**：action 条件化视频/3D 生成、潜空间预测模型（JEPA / Dreamer）、world foundation model 平台化。三条主线可进一步拆成「动作注入层 × 预测目标 × 行为派生 × 治漂移手段」四根可判定的轴（见 [topics/dynamics-and-action-conditioning.md](topics/dynamics-and-action-conditioning.md)）。`[精读原文]`
5. **交互性瓶颈在长时程一致性与 action-following 响应延迟**，而非单帧画质；评测仍呈碎片化（各应用域各自 benchmark，缺统一口径）。三套基准口径互不重叠且都不测交互（见 [topics/incomparability-checklist.md](topics/incomparability-checklist.md)）。`[精读原文]`

> 前三条是本报告采用的操作性范围判据，而非领域统一定义；后三条是从所引论文机制与评测条件归纳出的研究判断。

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

### 1.4 边界仍需明确的问题

- 混合系统中，何种程度的规则模拟、外部状态或人工先验仍可称为“学得的动力学”？需说明状态转移中哪些部分来自数据、哪些由规则给定。

---

## 2. 架构谱系：模型预测什么

World Models、PlaNet 与 Dreamer 从观测中编码潜状态并学习状态如何随动作变化。World Models 将 VAE 视觉压缩、MDN-RNN 潜动力学和线性控制器拆成三块，并展示可以在模型生成的“dream”里训练控制器；PlaNet 用 RSSM 同时维护确定性记忆和随机状态，并通过 latent overshooting 训练多步预测，再用 CEM 做在线 MPC；Dreamer 则让 actor-critic 在想象出的 latent trajectory 上学习。它们都用学得的转移支持行为，但观测重构、规划搜索和策略学习承担的作用并不相同。详见 [World Models](papers/1803.10122-world-models.md)、[PlaNet](papers/1811.04551-planet.md)、[Dreamer](papers/1912.01603-dreamer.md) 与 [DreamerV3](papers/2301.04104-dreamerv3.md)。

这几种方法回答“模型要预测什么”的方式不同：像素或潜状态重构提供感知一致性，reward/value 预测服务于行动选择，多步 latent prediction 试图让内部规划状态可滚动。画面更像真实观测不自动代表更适合控制；只预测规划量则能支持搜索，却没有可查看的未来观测。

MuZero 把“规划模型是否必须重构像素”推到另一端：它的 recurrent model 迭代预测 reward、policy 和 value，供 MCTS 使用；训练不要求像素解码器，因此学的是规划充分信息而非可视模拟器。将 MuZero 的搜索表现和 GameNGen 的视频保真放在一个排行榜上会混淆交付物：前者关心行动选择，后者关心动作条件化生成。[MuZero §3–4](papers/1911.08265-muzero.md)

JEPA/V-JEPA 路线又改变了预测目标：从 context 预测被遮挡的 target 表征，而非重构像素。这样可把学习压力放在语义/时序表示，避免追逐所有低层像素细节；但 action-free 表征不能单独回答“执行动作 a 后环境会怎样”，需要额外动作条件化模型或策略学习。从此处向像素/视频 rollout 的路线，**2024 年 Genie 的 latent-action 模型**与 GameNGen 的逐帧动作条件化扩散都提供可观察的交互接口，但方法不同，也都承受长时程误差积累。**Genie 4 是后续官方发布的另一种系统线索：强调 Gemini agent 与 Genie 生成器闭环；不能据此把其内部机制归同于 2024 年 Genie 的 latent action model。**UniSim/Cosmos 等多源平台扩大了数据与环境接口，但需区分真实观测、合成训练、规划和评测角色。更细的设计轴见[动作条件化与动力学专题](topics/dynamics-and-action-conditioning.md)。

## 3. 交互性与误差：用途决定评测边界

“可调用模型”不等于模型能稳定支撑行为。作为**在线规划器**（PlaNet/MuZero），一步预测误差会改变搜索树中候选动作的排序；作为**想象训练环境**（Dreamer 系），策略在模型自己生成的状态上反复训练，若模型高估异常状态回报，策略可能利用漏洞；作为**动作条件化视频 rollout**（GameNGen、2024 Genie），生成帧又成为后续输入，局部错误会逐步变成场景漂移。Genie 4 官方博客描述 Gemini 在环内计划并 steering 场景，但没有披露生成器如何接收动作，因此不应直接归类为逐帧动作条件化模型。相同的预测误差在这些闭环中的传播路径不同，不能用一个“模型准确率”概括。

误差控制也对应不同失效来源：PlaNet 的 latent overshooting 约束多步潜状态预测；Dreamer 用 reward/value 学习和 imagined actor-critic 控制策略目标；DreamerV3 用 balanced KL、free bits、symlog/twohot 等方法稳定跨任务训练；视频生成路线研究 noise augmentation、蒸馏或训练/推理分布对齐。比较这些办法时，应识别被控制的是潜状态漂移、奖励尺度、策略利用漏洞，还是视频 rollout 误差，再看各论文相应消融和目标函数（见[专题 §4](topics/dynamics-and-action-conditioning.md)）。

评测应分别报告单帧保真、动作跟随、短时因果一致性、长任务成功、策略是否钻模型漏洞及真实环境外推。FPS 需绑定分辨率、硬件和生成模式；一致性时长要交代动作轨迹与失败标准；规划成功率依赖环境、控制器和搜索预算。视频、游戏和机器人 benchmark 的构念不重叠，应结合[评测不可比性专题](topics/incomparability-checklist.md)逐项判断。

## 4. 代表系统逐案

### 4.1 代表系统揭示的取舍

1. **公开指标集中在「分辨率 × 帧率 × 一致性时长」三角，三者不可同时拉满**：Genie 3 官方称 720p / 24 FPS / 维持数分钟（[Genie 3 官方博客](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)）；GameNGen 在 DOOM 上以 320×240、20 FPS 达成数分钟稳定（PSNR 29.43，[arXiv:2408.14837v2 摘要 / §5](https://arxiv.org/html/2408.14837v2)），分辨率与场景复杂度显著更低。`[摘要级]`（Genie 3 官方博客）+ `[精读原文]`（GameNGen 分册及正文）
2. **潜空间路线不追像素级实时渲染，而追「想象中训练」的可扩展性**：Dreamer 4 以 shortcut forcing 实现**单 GPU 实时交互推理**，并首次做到纯离线数据在 Minecraft 取得钻石（[arXiv:2509.24527](https://arxiv.org/abs/2509.24527)）。`[摘要级]`
3. **机器人侧世界模型以「少量真机数据 + 零样本部署」为标志**：V-JEPA 2-AC 仅用 **<62 小时**无标注 Droid 数据 post-train，零样本在 Franka 上做图像目标规划抓放。`[摘要级]`
4. **平台化路线把世界模型做成可被下游 fine-tune 的基础设施**：Cosmos 开源因果视频 tokenizer 与 Predict1 多规格模型（7B / 12B / 13B / 14B）。`[摘要级]`
5. **可复核的公开数字多为作者自述、评测条件互不统一**，跨系统横向比较必须先回到各自 benchmark 定义（见章 5）。`[精读原文]`

Genie 4 的官方发布稿可补充“多模态交互与 Gemini 环内规划”的系统路线，但未给帧率、分辨率或一致性时长等量化结果，因此能更新研究问题地图，不能把它放进这条性能三角做比较。[Genie 4 官方发布材料读法](sources/genie4-official-release.md)

### 4.2 代表系统的机制和证据

| 系统 | 公开结果 / 能力主张 | 出处 | 证据性质 |
| :-- | :-- | :-- | :-- |
| **Genie 3**（Google DeepMind） | 实时导航 **24 FPS**、分辨率 **720p**、一致性维持**数分钟** | [官方博客 2025-08-05](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) | `[摘要级]` |
| **Genie 4**（Google DeepMind） | 官方发布稿声称原生音频、文本实时 steering、键盘导航及 Gemini 3.8 Flash 环内引导；**未披露帧率、分辨率、时长基准或内部架构** | [官方博客 2026-10-27](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/)；[发布材料读法](sources/genie4-official-release.md) | 官方博客（非技术报告） |
| **GameNGen** | DOOM，320×240；**单 TPU 20 FPS**；**PSNR 29.43 / LPIPS 0.249**（5 关卡 2048 条轨迹）；连续游玩 **5–10 分钟**后人类判别仍接近随机 | [arXiv:2408.14837v2 摘要 / §5](https://arxiv.org/html/2408.14837v2)；精读定位见 [分册 §7.8](papers/2408.14837-gamengen.md) | `[精读原文]` |
| **Dreamer 4** | **单 GPU 实时交互推理**（shortcut forcing + 高效 transformer）；纯离线数据在 Minecraft **首次取得钻石** | [arXiv:2509.24527](https://arxiv.org/abs/2509.24527) 正文 | `[摘要级]` |
| **V-JEPA 2 / V-JEPA 2-AC** | 预训练 **>1M 小时**互联网视频；2-AC 用 **<62h** Droid 无标注视频 post-train；**零样本** Franka 抓放 | [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) 正文 | `[摘要级]` |
| **Cosmos WFM**（NVIDIA） | 平台化：视频 curation 流水线 + **因果视频 tokenizer** + **Cosmos-Predict1 7B/12B/13B/14B** + 开放权重 | [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) 正文 | `[摘要级]` |
| **Matrix-Game** | **17B 参数**；Matrix-Game-MC 数据集 **>2,700 小时** Minecraft；配套 **GameWorld Score** | [arXiv:2506.18701](https://arxiv.org/abs/2506.18701) 正文 | `[摘要级]` |
| **Hunyuan-GameCraft** | 推理**加速 20×**，达 **6.6 FPS** | [arXiv:2506.17201](https://arxiv.org/abs/2506.17201) 正文 | `[摘要级]` |
| **CausVid** | 当前实现约 **10 FPS**（作者称可经编译/量化/并行进一步优化） | [arXiv:2412.07772](https://arxiv.org/abs/2412.07772) 正文 | `[摘要级]` |
| **Self Forcing** | **17.0 FPS**、**亚秒级延迟** | [arXiv:2506.08009](https://arxiv.org/abs/2506.08009) 正文 | `[摘要级]` |
| **Genie（2024）** | **11B 参数**；无标注互联网视频无监督训练；潜动作模型（latent action model） | [arXiv:2402.15391](https://arxiv.org/abs/2402.15391) 摘要 | `[摘要级]` |
| **DIAMOND** | 图像空间扩散世界模型，可作环境 **drop-in 替代**；**3 NFE/帧**（对比 IRIS 的 16 NFE/帧） | [arXiv:2405.12399](https://arxiv.org/abs/2405.12399) 正文 | `[摘要级]` |

**跨系统比较**：帧率数字的**评测口径差异极大**——20 FPS（GameNGen，320×240，单 TPU）与 24 FPS（Genie 3，720p，官方博客）不可直接比较；Self Forcing 的 17.0 FPS 与 Hunyuan-GameCraft 的 6.6 FPS 属不同分辨率/任务设定，横向对比须同时给出分辨率与硬件。`[摘要级]`

## 5. 评测与基准

### 5.1 本章结论

1. **评测呈三层碎片化**：通用视频质量（VBench，16 维）、内在真实性/物理（VBench-2.0 五维、Physics-IQ 五类物理）、世界级属性（WorldScore 的可控性/质量/动态）。三者维度定义互不重叠，**无法相互替代**。`[摘要级]`（VBench）+ `[精读原文]`（其余）
2. **交互性指标仍靠各系统自报**（帧率、一致性时长、PSNR/LPIPS），**缺统一第三方基准**；这也是章 4 数字不可直接比较的根因。`[精读原文]`
3. **具身侧已出现世界模型专用评测**：EWMBench（Genie Envisioner）测视觉保真、物理一致性、指令-动作对齐；游戏侧有 GameWorld Score（Matrix-Game）。`[摘要级]`
4. **规则模拟器 benchmark 在本专题只作环境，不作世界模型评测口径**（章 1.2 排除口径一致）。`[精读原文]`

### 5.2 基准测量的构念与边界

| benchmark | 维度 / 指标 | 面向对象 | 主等级 | 来源 |
| :-- | :-- | :-- | :-- | :-- |
| **VBench** | **16 个**层级化、解耦维度（各配 prompt 与评测方法） | 通用视频生成质量 | `[摘要级]` | [arXiv:2311.17982](https://arxiv.org/abs/2311.17982) 摘要 |
| **VBench-2.0** | **5 个**维度：Human Fidelity / Controllability / Creativity / Physics / Commonsense（细分为 **18 维**，针对 intrinsic faithfulness） | 视频生成的「内在真实性」 | `[精读原文]` | [arXiv:2503.21755](https://arxiv.org/abs/2503.21755) 正文 |
| **WorldScore** | **3 个**方面：controllability / quality / dynamics；含统一 world specification + 数据集 + 多面指标；评测 **19 个**代表模型 | 世界生成（世界模型统一评测的最接近形态） | `[精读原文]` | [arXiv:2504.00983](https://arxiv.org/abs/2504.00983) 正文 |
| **Physics-IQ** | **5 类物理**：Solid Mechanics / Fluid Dynamics / Optics / Thermodynamics / Magnetism；预测后续 **5 秒**；含 Sora / Runway / Pika / Lumiere / SVD / VideoPoet 对照 | 物理理解 | `[精读原文]` | [arXiv:2501.09038](https://arxiv.org/abs/2501.09038) 正文 |
| **GameWorld Score** | 游戏世界交互质量（随 Matrix-Game 发布） | 游戏域交互式世界模型 | `[摘要级]` | [arXiv:2506.18701](https://arxiv.org/abs/2506.18701) 正文 |
| **EWMBench** | 视觉保真 / 物理一致性 / 指令-动作对齐 | 机器人操作世界模型 | `[精读原文]` | [arXiv:2508.05635](https://arxiv.org/abs/2508.05635) 正文 |
| 系统自报指标 | FPS / 一致性时长 / PSNR / LPIPS | 各交互式系统 | `[精读原文]` | 见章 4.2 |

**当前不可比缺口**：① 视频、游戏、机器人评测口径不同；② action-following 延迟与可交互时长缺少统一跨域指标；③ 长时程记忆缺少可比测量；④ sim-to-real 对齐证据不能由仿真成功率替代。

## 6. 应用域

### 6.1 本章结论

1. **世界模型在具身侧被消费为三类资源**：①想象中训练（RL in imagination）；②可交互练习环境；③评测环境（与 EmbodiedVLA 条目 §4.3 的接口定义一致）。VLA 侧关于合成数据、想象 RL 和真机迁移的论文比较见[世界模型到 VLA 迁移专题](../EmbodiedVLA/topics/world-model-to-vla-transfer.md)。`[精读原文]`
2. **数据接口呈「少量真机 + 大规模无标注视频」组合**：V-JEPA 2-AC 用 **<62h** Droid 无标注数据；Cosmos 提供 curation 流水线与 tokenizer；游戏域 Matrix-Game-MC **>2,700h**（不可直接迁移到机器人）。`[摘要级]`
3. **评测接口开始专门化**：**EWMBench**（视觉保真 / 物理一致性 / 指令-动作对齐）是机器人操作场景的专用套件；Genie Envisioner 同时提供 **GE-Sim** 作 action-conditioned 神经模拟器以支持闭环 rollout。`[精读原文]`
4. **UniSim 与 Cosmos 代表两种平台化姿态**：前者主张「学一个真实世界交互的通用模拟器，使具身 agent 纯在模拟中训练后直接部署」；后者把世界模型做成 Physical AI 的**世界数字孪生**（digital twin of the world，与政策模型并列）。`[摘要级]`
5. **归属**：本节对象的世界模型/环境侧归本专题，策略/动作侧归 `EmbodiedVLA`（见章 7 互引）。`[精读原文]`

### 6.2 具身与机器人：模型作为环境和训练信号

| 对象 | 作为环境的角色 | 关键事实 | 主等级 |
| :-- | :-- | :-- | :-- |
| **[Dreamer 4](https://arxiv.org/abs/2509.24527)** | ①想象中训练 | 在可扩展世界模型内部做 RL；纯离线数据在 Minecraft 取得钻石；作者将「离线想象训练」对齐机器人场景（真机交互不安全、缓慢） | `[摘要级]` |
| **[UniSim](https://arxiv.org/abs/2310.06114)** | ①+②通用模拟器 | 以生成式建模学习真实世界交互的通用模拟器，目标包含「机器人在模拟经验中学习后直接部署真机」 | `[精读原文]` |
| **[Genie Envisioner](https://arxiv.org/abs/2508.05635)** | ②+③平台 | GE-Base（指令条件视频扩散世界模型）+ GE-Sim（action-conditioned 神经模拟器，闭环 rollout）+ EWMBench（评测） | `[精读原文]` |
| **[Cosmos WFM](https://arxiv.org/abs/2501.03575)** | ①工业化形态 | Physical AI 的「世界数字孪生」；覆盖 curation / 预训练 / post-train / tokenizer 全链路并开放权重 | `[摘要级]` |
| **[V-JEPA 2-AC](https://arxiv.org/abs/2506.09985)** | ②规划环境 | 62h Droid 数据 post-train 后零样本规划抓放（少量真机数据范式） | `[摘要级]` |
| **Genie 4**（官方发布稿） | 提议的模拟训练环境 | 博客称其可能用于机器人与 Agent 训练场景；未展示策略训练、迁移或闭环评测，因此是用途主张，不是训练收益证据 | `[官方发布稿]` |

**数据/评测接口清单（可直接复用，避免二次造轮子）**

| 接口 | 类型 | 规模/维度 | 域 | 主等级 |
| :-- | :-- | :-- | :-- | :-- |
| Droid（经 V-JEPA 2-AC 使用） | 真机数据 | <62h 无标注 | 机器人操作 | `[摘要级]` |
| Matrix-Game-MC | 交互数据 | >2,700h | 游戏（Minecraft） | `[摘要级]` |
| EWMBench | benchmark | 视觉保真/物理一致性/指令-动作对齐 | 机器人操作 | `[精读原文]` |
| GameWorld Score | benchmark | 游戏世界交互 | 游戏 | `[精读原文]` |
| VBench / VBench-2.0 / WorldScore / Physics-IQ | benchmark | 见章 5.2 | 通用视频 / 世界生成 | 见章 5.2 |

### 6.3 相邻应用域的归属

- **游戏引擎**：Genie 3 / Genie 4（官方博客）、GameNGen、Matrix-Game、Hunyuan-GameCraft —— 已在章 4 区分论文实测与官方发布主张。
- **自动驾驶**：GAIA-1、GAIA-2、Vista（参考文献 30–32）—— 作为相邻方向补充阅读（`[摘要级]`）。
- **开放世界探索**：由 38（交互式视频世界建模综述）的 domain 章节给出索引（`[摘要级]`）。


## 7. 与 AIGC / Embodied / LLM 的边界及交叉引用

### 7.1 本章结论

1. **判据落地为三条判定**：(i) 交付物是**动作策略** → Embodied；(ii) 交付物是**环境/状态演化** → WorldModels；(iii) **双交付物** → 按分支归属，同一论文可被两处引用而**互不吞并**。`[摘要级]`（对 V-JEPA 2-AC / WorldVLA 的正文与摘要判定）
2. **π0 类 action head → Embodied**：输出为动作策略，不因「内置世界模型或流匹配」改判。`[摘要级]`（arXiv:2410.24164 摘要）
3. **WorldVLA → 按交付物拆分**：其动作分支归 `EmbodiedVLA`，未来帧预测（world）分支归本专题。`[摘要级]`（arXiv:2506.21539 摘要）
4. **V-JEPA 2-AC → world 侧归本专题**：其交付物是 **action-conditioned 潜空间世界模型**（预测未来表示）；在 Franka 上的抓放部署属应用验证，不改变归属。`[摘要级]`
5. **与 EmbodiedVLA 的边界按交付物划分**：输出动作的策略归具身策略，预测环境状态演化的模型归本专题；联合系统按不同分支分别讨论。

### 7.2 判据如何作用于具体工作

| 具体工作 | (a) | (b) | (c) | 归属判定 | 主等级 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **π0**（VLA flow model） | — | ✗ 交付物是策略 | ✓（用预训练 VLM/世界知识） | **Embodied**（`EmbodiedVLA`） | `[摘要级]` |
| **OpenVLA** | — | ✗ | ✓ | **Embodied** | `[摘要级]` |
| **WorldVLA** | ✓ | ✓（未来帧）+ ✗（动作侧） | ✓ | **拆分**：world 分支→本专题；动作分支→EmbodiedVLA | `[摘要级]` |
| **V-JEPA 2-AC** | ✓ | ✓ | ✓ | **WorldModels**（本专题章 2/4）；机器人应用登记在章 6 | `[摘要级]` |
| **Dreamer 4** | ✓ | ✓ | ✓ | **WorldModels**；其 agent 训练属具身应用（章 6） | `[摘要级]` |
| **Genie 3 / GameNGen** | ✓ | ✓ | ✓ | **WorldModels** | `[摘要级]` / `[摘要级]` |
| **Sora / Veo** | ✗ | ✗ | ✓ | **AIGC** | `[摘要级]`（官方产品页，仅作类别示例） |
| **MuJoCo / Atari / Doom / Isaac / LIBERO / SIMPLER** | ✓ | ✓ | ✗ 硬编码 | **排除**；仅作评测环境/数据来源 | `[摘要级]` |

### 7.3 与 `EmbodiedVLA` 的阅读接口

> 具身策略的逐篇分析见 [`EmbodiedVLA`](../EmbodiedVLA/report.md)。

| 交叉对象 | 本专题处理 | EmbodiedVLA 条目处理 |
| :-- | :-- | :-- |
| **π0 类策略本体** | 章 1.3 / 7.2 判定 → Embodied，**不展开** | 该条目章 2、3 展开 |
| **WorldVLA** | 章 7.2 负责 **world 分支** | 该条目只登记动作分支 |
| **V-JEPA 2 / V-JEPA 2-AC** | 章 2、4 负责模型与规划机制 | 该条目 §4.3 只登记「作为训练/规划环境」的接口 |
| **Dreamer 4** | 章 4、6.2 负责想象训练机制 | 该条目 §4.3 接口①②案例 |
| **Cosmos WFM** | 章 2、4、6.2 平台化 | 该条目 §4.3 接口①工业化形态 |
| **Genie 3 / GameNGen 等交互式世界模型** | 章 2、4 | 该条目明确**不在其内出现**（无动作交付物） |
| **规则模拟器（MuJoCo / Isaac / LIBERO / SIMPLER 等）** | 章 1.2 排除出 WorldModels，仅作评测环境 | 该条目章 4.2、5 按评测环境引用——**口径一致** |
| **自动驾驶世界模型（GAIA-1/2、Vista）** | 章 6.3 作为相邻方向提及 | 该条目章 6 介绍其应用背景 |

> 两个专题的交叉阅读位置：本报告第 1、7 章与 [`EmbodiedVLA`](../EmbodiedVLA/report.md) 第 1、4、7 章。联合系统按动作策略与环境模型的具体交付物分别分析。

### 7.4 与 AIGC / LLM 的交叉

- **AIGC**：纯视频/图像生成归 `VideoGen` / `OpenAI-Gen`；本专题只收「可交互 + 系统可调用」的部分，章 1.2 已给出排除口径。
- **LLM**：无环境状态演化的理解与规划归 `ReasoningModels`；Agent 外层循环归 `Agent`。

## 8. 未决问题

**本章要回答**：定义何时可能收敛？评测统一化的现实路径？sim-to-real 与安全部署的门槛？物理一致性是否可被现有指标证伪？

**计划证据来源**：参考文献 37–38（两篇 2026 综述与 2411.14499）、以及第 5.2 节缺口清单。

> 尚待研究的问题包括：① 「帧率」类指标须与分辨率/硬件绑定后才可比较（章 4.2）；② 交互性第三方基准缺位（章 5.2）；③ 术语定义和范围判据是本专题的操作约定，不是单篇论文直接给出的结论。

---

## 9. 跨系统对比：目标、动作和行为派生

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

## 11. 研究路线：不同工作改变了什么问题

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
| **要训练 RL 策略**（省交互） | 想象训练 | Dreamer / DreamerV3 | 想象误差 → 策略误差（[Dreamer §4](papers/1912.01603-dreamer.md)；[DreamerV3 §4](papers/2301.04104-dreamerv3.md)）；需防钻空子（[World Models §4](papers/1803.10122-world-models.md)）；表征瓶颈（[DreamerV3 §4](papers/2301.04104-dreamerv3.md)） |
| **要训练视觉-语言-动作策略** | 动作进-视频出模拟器 | UniSim | 域内零样本，跨域未证明；动作是"伪动作" |
| **只要通用视觉表征**（不要环境） | 特征预测 | V-JEPA | 不能规划、不能生成、不证明物理理解 |
| **要评测"懂不懂物理"** | 真实拍摄基准 | Physics-IQ（物理理解）、VBench-2.0（内在真实性） | 两套口径不可互换；都不测交互 |

---

## 13. 阅读路线：从预测目标到可用证据

初读可按“模型究竟要预测什么”建立主线：先读 [World Models](papers/1803.10122-world-models.md) 与 [PlaNet](papers/1811.04551-planet.md)，看潜状态如何从观测中形成、如何用想象或在线规划利用动力学；再读 [Dreamer](papers/1912.01603-dreamer.md) 与 [DreamerV3](papers/2301.04104-dreamerv3.md)，理解世界模型误差怎样进入策略训练，以及稳定训练所需的目标与损失设计。随后读 [MuZero](papers/1911.08265-muzero.md)，比较“预测可规划的量”与“重构可观看的未来”两种目标。

若关注生成式交互环境，接着读 [GameNGen](papers/2408.14837-gamengen.md) 和 [UniSim](papers/2310.06114-unisim.md)，并对照[动作条件化与动力学专题](topics/dynamics-and-action-conditioning.md)：重点看动作如何进入生成过程、生成轨迹如何继续作为下一步状态，以及训练数据与真实环境之间的差距。若关注表征是否必须重构像素，读 [V-JEPA](papers/2404.08471-vjepa.md)；若关注评测，读 [Physics-IQ](papers/2501.09038-physics-iq.md)、[VBench-2.0](papers/2503.21755-vbench-2.md) 与[评测不可比性专题](topics/incomparability-checklist.md)。机器人策略与训练环境的接口另见[世界模型到 VLA 迁移专题](../EmbodiedVLA/topics/world-model-to-vla-transfer.md)。

## 14. 跨论文综合：预测目标决定模型能回答的问题

世界模型的关键分歧不是“谁的模型更大”，而是为了让下游系统做什么，模型需要保留什么信息。World Models、PlaNet 与 Dreamer 保留潜状态的可预测性，以降低规划或想象训练的交互成本；MuZero 进一步舍弃像素重构，只预测搜索所需的 reward、policy 和 value，因此不能把它当作可视模拟器。V-JEPA 的特征预测避免为无关像素细节付出重构代价，却没有动作条件化转移时也不能回答行动后果。GameNGen、Genie 等视频路线提供可观察的后续帧和动作接口，但把视觉生成误差带入后续 rollout。

由此，评估必须跟交付物匹配：规划模型看模型误差是否改变动作排序与任务结果；想象训练模型看策略是否利用模型漏洞、并能否回到真实环境；可交互视频模型看动作响应、长时程一致性和场景状态保持；特征模型看下游任务是否能从表示中恢复所需状态信息。VBench-2.0、Physics-IQ、WorldScore 分别覆盖视频内在真实性、若干物理预测任务、世界生成的控制/质量/动态维度，不能相互替代，也都不足以单独证明长时程闭环能力。具体条件见第 4–6 章及 [评测不可比性专题](topics/incomparability-checklist.md)。

本文与[具身预测规划专题](../EmbodiedPlanning/report.md)的边界是：部署时用模型预测候选机器人动作属于预测规划；本专题聚焦作为模型本身的学得动力学、想象训练和可交互环境。与 [EmbodiedVLA](../EmbodiedVLA/report.md) 的关系则是环境/状态演化与动作策略的接口，不能把策略成功率直接解释成世界模型精度。

## 15. 术语表（读本条目所需的最小集合）

> 只收**本条目用到的机制术语**，每条给"是什么 + 谁在用 + 在哪一章/分册"；定义以入选分册的正文为准。

| 术语 | 是什么 | 谁在用 | 出处 |
| :-- | :-- | :-- | :-- |
| **RSSM**（Recurrent State Space Model） | 循环状态空间模型：**确定性路径**（记历史） + **随机路径**（建模不确定性）双分量 | PlaNet / Dreamer / DreamerV3 | [papers/1811.04551](papers/1811.04551-planet.md) §1.2 |
| **latent overshooting** | 多步变分目标：不只训 1 步预测，强制多步一致性 | PlaNet | 同上 §1.3 |
| **CEM**（Cross-Entropy Method） | 种群采样 + 精英筛选 + 迭代的免梯度优化，用作模型内规划器 | PlaNet | [papers/1811.04551-planet.md](papers/1811.04551-planet.md) §1.4 |
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
| **寻找后续问题** | §8 未决问题、§19 开放问题 | 评测环境、交互基准、跨域零样本和 sim-to-real 仍有哪些证据边界 |
| **要看机制细节** | 对应 `papers/` 分册（方法/实验/消融/失效边界） | 该系统的具体设计、关键超参、失效条件 |

---

## 18. 证据读法

文中 FPS、成功率、环境步数和数据规模均为论文或官方材料在对应条件下报告的结果，应连同模型版本、环境、分辨率/控制频率、数据、训练或评测预算阅读。不同来源的 FPS、PSNR、奖励和真机成功率不是同一指标。固定版本仓库的源码事实只支持该版本中可见的实现行为，不能单独证明论文训练、权重或线上服务完全采用相同路径。

逐篇论文的方法细节和条件见对应 `papers/`；跨论文问题见 `topics/`。摘要和官方博客只支持其公开披露，不足以推断未公开的训练架构。本文未独立重算或复现实验。

## 19. 开放问题：评测、数据与部署

> 下列问题限制当前结果的外推范围；尚未找到统一协议不等于证明某种能力不存在。

#### 评测缺口

| 缺口 | 现状证据 | 补的入口 |
| :-- | :-- | :-- |
| **交互性评测覆盖尚未核全** | VBench-2.0（内在真实性）、Physics-IQ（物理理解）、WorldScore（`[摘要级]`）**都不测** action-conditioned 响应与延迟 | 需要新基准：动作条件响应准确率、长时程一致性时长、action-following 延迟 |
| **感知与物理不可互换** | Physics-IQ 证明视觉真实感 ≠ 物理理解（8 模型 / 5 类物理 / 66 场景） | 任何"更真 ⇒ 更懂物理"的推论都要附真实拍摄验证 |
| **"在模型里评测"不可信** | 见 [topics/world-model-as-env.md](topics/world-model-as-env.md) §5：模型误差 → 评测分数不可信 | 先解决模型误差上界，再谈"模型即评测环境" |

#### 数据缺口

| 缺口 | 现状证据 | 补的入口 |
| :-- | :-- | :-- |
| **动作标签稀缺** | World Models/PlaNet/Dreamer 靠环境自带动作；GameNGen 需要先训 agent 采数据；UniSim 只能用"伪动作" | 采集带动作标注的真实交互数据，或研究动作无关到有动作的迁移 |
| **多源信息鸿沟** | UniSim：不同社区为不同目的采集，信息发散是**物理上限** | 数据编排之外，需要"信息补齐"的技术（不只是拼接） |
| **跨域零样本无证据** | 现有最强证据（UniSim）是**域内**零样本 | 明确设计跨域实验（不同真机域/不同仿真器） |

#### 部署缺口

| 缺口 | 现状证据 | 补的入口 |
| :-- | :-- | :-- |
| **实时性依赖蒸馏** | GameNGen 单 TPU 20 FPS（320×240）；实时扩散常用 few-step 蒸馏/短程强制（`[摘要级]`） | 报"实时"必须带分辨率+硬件；蒸馏带来的质量损失需单列 |
| **长时程一致性无机制保证** | GameNGen 靠噪声增强压漂移、无显式长期记忆；UniSim 只证 8 次交互 | 显式记忆/检索机制 + 一致性时长指标 |
| **安全与不可逆场景** | 世界模型在"被钻空子"时给出的高分**不可信**（World Models §4.5） | 部署前必须做对抗性利用测试，而非只看真环境回报 |

**三张清单共同指向一件事**：本专题纳入的代表系统中，GameNGen 已报告单 TPU 实时推理；本专题同时识别出跨系统交互评测口径缺口（§5.2）、动作标注与跨域证据缺口（§19.2），以及对抗性利用测试需求（§19.3）。

---

## 参考文献

> 体例：编号 + 标题 + 一手来源链接 + 归属章节。

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
39. Sora: A Review on Background, Technology, Limitations, and Opportunities of Large Vision Models — [arXiv:2402.17177](https://arxiv.org/abs/2402.17177) — `[二手]` — 章 7（仅作视频生成背景，不用于判断具体产品的内部架构）
40. Genie Envisioner: A Unified World Foundation Platform for Robotic Manipulation — [arXiv:2508.05635](https://arxiv.org/abs/2508.05635) — `[摘要级]` — 章5/6
41. Learning Interactive Real-World Simulators (UniSim) — [arXiv:2310.06114](https://arxiv.org/abs/2310.06114) — `[精读原文]` — 章6
42. Diffusion for World Modeling: Visual Details Matter in Atari (DIAMOND) — [arXiv:2405.12399](https://arxiv.org/abs/2405.12399) — `[摘要级]` — 章4

---

## 来源范围

本文优先引用论文正文、官方技术报告和固定版本代码。跨论文比较保留各自原始任务、模型和硬件条件；未公开的内部结构不作推断，正文列出的数字均为作者报告结果，未独立复现。
