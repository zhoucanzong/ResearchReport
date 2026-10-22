# EmbodiedVLA 技术专题调研

> **声明**：本报告由 AI Agent 自动调研生成，未经官方确认；引用具体参数、日期或 benchmark 前请回溯原始来源。
> **调研日期**：2026-10-16 起骨架 → 2026-10-17 第二轮深度精读升级 → 2026-10-23 闭环控制与世界模型迁移两批论文补核。
> **主要增量**：原有 8 篇基础精读后，先新增 3 篇机器人闭环机制分册及专题，再新增 5 篇“世界模型数据如何改善 VLA 真机表现”分册及横切专题。第二批按合成数据、想象 RL、物理验证三种角色选文；版本、候选取舍与精读范围见[来源清单](sources/MANIFEST.md)和[选文说明](sources/CANDIDATES.md)。
> **定位**：本报告采用操作性定义：EmbodiedVLA（Vision-Language-Action）指**以自然语言指令 + 视觉观测为输入、直接输出机器人动作信号的可部署策略模型**；据此建立判据、动作表征架构谱系、代表系统、数据、评测与应用边界。**世界模型作为 VLA 的训练环境**是本专题与 `WorldModels` 的交叉点（见第 7 章）。

**证据等级约定（单一主等级）**：`[精读原文]` 已通读一手正文（论文有 `papers/` 分册，或官方仓库已做固定 commit 代码核验）；`[摘要级]` 仅核验官方摘要 / 页面，**未通读正文，细节不得当作已成立事实**；`[二手]` 第三方转述；`[受限核验]` 一手对象只能经镜像 / API 间接确证。每条只给**一个主等级**；来源类型写在括号内。本报告代码类证据一律写成 `仓库@commit:文件:行`，并按第 2.3 节区分**代码事实**与**研究推断**。

---

> **补充核验（2026-10-22）**：已读取缓存原文，抽核八篇分册的关键数字；OpenVLA 的 16.5 改为成功率百分点差，Diffusion Policy 的 46.9% 明确为逐任务相对指标增益平均，DROID 标定记录与物理场景计数分开。此范围不包含训练/评测代码复现，也不代表所有数字已逐项通过。

> **闭环控制补核（2026-10-23）**：新增 π*0.6/RECAP、VLCP、LingBot-VA 三篇逐篇分册，并将 VersualRL（[arXiv:2603.22169v3](https://arxiv.org/html/2603.22169v3)，原文题名拼作 VersualRL）作为真机任务层策略学习的边界案例登记。四项分别涉及跨 episode VLA 参数学习、同 episode 代码修订、世界模型滚动/接地、任务级 Behavior Tree 更新；成功率、吞吐与恢复率不互换，也不组成排行榜。见[闭环控制专题](topics/closed-loop-control.md)。

> **世界模型迁移补核（2026-10-23）**：新增 SimVLA、Grounded-Dreamer、VLAW、World-VLA-Loop、WoVR 五篇全文精读，并比较其模型角色：程序化仿真数据源、视频生成和物理回放校验、真实 rollout 更新模拟器后合成监督、以及模型内 RL。跨论文结果不组成排行榜；特别区分 task progress / success rate、策略训练中的真机预算和独立物理评估。见[世界模型到 VLA 迁移专题](topics/world-model-to-vla-transfer.md)。

## 深度阅读导航

### 精读分册（`papers/`，16 篇，均 `[精读原文]`）

| # | 分册 | 一句话定位 | 动作表征路线 |
| --: | :-- | :-- | :-- |
| 1 | [Diffusion Policy（2303.04137）](papers/2303.04137-diffusion-policy.md) | diffusion head 路线的定义性工作：把策略建模为条件去噪扩散过程 | **diffusion head** |
| 2 | [RT-2（2307.15818）](papers/2307.15818-rt2.md) | 把动作写成文本 token 与网络规模 VLM 联合微调——VLA 范式确立点 | **token** |
| 3 | [Open X-Embodiment（2310.08864）](papers/2310.08864-open-x-embodiment.md) | 跨 22 本体的数据格式标准化 + 跨机器人正迁移证据 | —（数据） |
| 4 | [OpenVLA（2406.09246）](papers/2406.09246-openvla.md) | 7B 开源主干 + 每维 256-bin 离散 token，token 路线的可复现基线 | **token** |
| 5 | [π0（2410.24164）](papers/2410.24164-pi0.md) | 预训练 VLM + action expert，flow matching 出高频灵巧动作 chunk | **flow matching** |
| 6 | [FAST（2501.09747）](papers/2501.09747-fast.md) | 频率域动作 tokenizer，回答"token 路线能否用于高频灵巧任务" | **token（压缩）** |
| 7 | [DROID（2403.12945）](papers/2403.12945-droid.md) | 统一硬件栈 + 分布式采集的大规模 in-the-wild 真机数据集 | —（数据） |
| 8 | [SIMPLER（2405.05941）](papers/2405.05941-simpler.md) | 用仿真评测真机策略，主张"相对排序强相关" | —（评测） |
| 9 | [π*0.6 / RECAP（2511.14759）](papers/2511.14759-pi-star-0.6-recap.md) | 从真机 rollouts、回报与人工纠正中跨 episode 改进 VLA | **advantage-conditioned policy** |
| 10 | [VLCP（2608.16978）](papers/2608.16978-vlcp.md) | 同一 episode 按观测改写失败的代码策略；证据目前限仿真 | **代码控制器重规划** |
| 11 | [LingBot-VA（2601.21998）](papers/2601.21998-lingbot-va.md) | 预测视觉未来并输出动作，以异步执行和真实观测回灌滚动 | **world-model rollout** |
| 12 | [SimVLA（2610.11248）](papers/2610.11248-simvla.md) | SimAction / SimVQA / SimDeploy 三种仿真监督，部署到移动操作真机 | **flow matching + tokenized action** |
| 13 | [Grounded-Dreamer（2610.13164）](papers/2610.13164-grounded-dreamer.md) | 从真实初始图像重建场景，视频模型合成后用物理仿真 replay 筛轨迹 | **video WM + IDM** |
| 14 | [VLAW（2602.12063）](papers/2602.12063-vlaw.md) | 真机 rollouts 校准世界模型，生成成功轨迹与真实成功样本混合微调 | **flow matching policy** |
| 15 | [World-VLA-Loop（2602.06508）](papers/2602.06508-world-vla-loop.md) | 近成功数据 + 内生奖励，在学得的模拟器里做 VLA 强化学习并共同迭代 | **world-model RL** |
| 16 | [WoVR（2602.13977）](papers/2602.13977-wovr.md) | KIR 缩短想象误差深度，PACE 跟踪策略引起的模型分布漂移 | **world-model RL** |

### 横切专题（`topics/`，5 篇）

| 专题 | 回答什么 | 何时读 |
| :-- | :-- | :-- |
| [评测与数据集](topics/evaluation-and-datasets.md) | 真机 vs 仿真能力边界、评测协议与指标、数据规模来源与许可、跨系统可比性 | **引用任何成功率之前必读** |
| [动作表征三路线](topics/action-representation.md) | token / flow matching / diffusion head 的训练目标、超参、推理代价与边界 | 要判断某系统属哪条路线时 |
| [失效边界与部署条件](topics/deployment-boundaries.md) | 六类可命名的失效机制 + 上线前自检清单 | 讨论"能不能部署"时 |
| [机器人闭环控制与 VLA](topics/closed-loop-control.md) | chunk feedback、episode 内恢复、跨 episode 学习、世界模型 rollout 的机制与证据边界 | 讨论"闭环到底闭在哪里"时 |
| [世界模型到 VLA 迁移](topics/world-model-to-vla-transfer.md) | 合成示范、想象 RL 与物理校验各自怎样带来真机增益，以及真机数据预算 | 要判断"模型预测是否真的改善机器人动作"时 |

### 选文与来源（`sources/`）

| 文件 | 内容 |
| :-- | :-- |
| [CANDIDATES.md](sources/CANDIDATES.md) | 历史 27 篇 + 闭环 4 篇 + 世界模型迁移 20 篇；累计入选 16，排除/边界 35，并记录选择依据 |
| [MANIFEST.md](sources/MANIFEST.md) | 16 篇的 arXiv ID / 版本 / 版本日期 / 标题 / 第一作者 / license / 来源 |

> **全文不入库**：论文 PDF / 转出的 txt 一律不进入本仓库；缓存放在仓库外 `~/Documents/paper-cache/`，理由见 [MANIFEST.md](sources/MANIFEST.md) §3。

---

## 0. 本章结论

1. **术语尚无公认定义**，本专题取可判定的操作性判据：`(a) 视觉输入` + `(b) 自然语言指令条件化` + `(c) 直接输出动作信号` 三条**同时满足**才算 VLA；"是否由网络规模 VLM 初始化"作为**强弱标注**而非准入门槛。`[摘要级]`（arXiv 摘要 + 官方项目页，见参考文献 1–8）
2. **动作表征（action representation）是 VLA 架构分化的主轴**，当前并行三条路线：**token（离散 / 自回归）**、**flow matching（连续、向量场回归）**、**diffusion head（连续、逐步去噪）**；代表分别是 RT-2 / OpenVLA / π0-FAST、π0 / GR00T N1、Diffusion Policy / RDT-1B。`[精读原文]`（分册 1/2/4/5/6）+ `[摘要级]`（GR00T N1、RDT-1B）+ 代码事实（第 2.3 节）
3. **同一模型常同时提供两条路线**：π0 官方仓库同时给出 flow matching 头（`pi0`）与 FAST tokenizer 自回归头（`pi0_fast`），说明"路线之争"在工程上首先是**延迟 / 精度 / 复用性**的取舍，而非互斥范式。`[代码事实]`（第 2.3 节）
4. **真机数据与仿真数据不可互相替代**：前者是 VLA 预训练的语义与灵巧度来源（Open X-Embodiment、DROID 等），后者是规模化与可复现评测的来源（Isaac Sim / ManiSkill / RoboCasa / LIBERO 等）。`[精读原文]`（分册 3/7）+ `[摘要级]`
5. **评测是当前最大瓶颈**：真机成功率是事实标准但不具可复现性；仿真基准可复现但保真度受限。SIMPLER 主张 sim-real **相对排序**强相关（原文自承"仿真永远是不完美代理"），而 π0.5 指出仿真表现好的策略在真机泛化仍差——**仿真分数不能直接替代真机结论**。`[精读原文]`（分册 8）+ `[摘要级]`（π0.5）。**两条不矛盾：一个谈排序，一个谈绝对泛化。**
6. **动作 token 化在高频灵巧任务上会撞墙**，压缩型 tokenizer（FAST 一类）是 token 路线可用于高频任务的**先决条件**；π0 的 flow matching 选择"固定 10 步积分 + H=50 的 chunk"正是为绕开这一瓶颈。`[精读原文]`（分册 5/6）
7. **规模不等于多样性**：DROID 的核心论点是场景与**交互位置**多样性（564 场景 / 52 建筑 / 86 任务），而非单纯堆轨迹数；这与 OXE 的"跨本体格式标准化"是**两个互补的数据命题**。`[精读原文]`（分册 3/7）
8. **与相邻领域边界**：VLA 是**策略**，VLM 是**输入侧模型**，Agent 是**外层决策循环**，WorldModels 产出的是**环境/状态转移**而非动作；联合模型（WorldVLA 一类）按"交付物"拆分归属，避免重复劳动（第 7 章与 `WorldModels` 章显式互引）。`[摘要级]`（arXiv 摘要）
9. **闭环要按修改对象与时间尺度拆开**：chunk 间重规划、episode 内控制代码修订、跨 episode VLA 参数学习、世界模型预测接地各自是不同机制；实验跨仿真与不同真机任务，指标不可合并为排行榜。`[精读原文]`（[闭环控制专题](topics/closed-loop-control.md)）

> **口径变化**：第一轮骨架的 6 条结论全部为 `[摘要级]`；第二轮后，第 2–7 条由基础八篇分册支撑。2026-10-23 先新增闭环控制三篇，再新增世界模型迁移五篇分册。第 1 条（术语无公认定义）与第 8 条（边界约定）**仍为 `[摘要级]`**——它们是本专题的操作性约定，而非文献结论。

### 0.1 本轮证据普查（可逐条核对）

| 等级 | 条数 | 覆盖对象 | 能被用来支撑什么 |
| :-- | --: | :-- | :-- |
| `[精读原文]` | **21** | **16 篇论文分册**（基础八篇、闭环三篇、世界模型迁移五篇）+ **5 个官方仓库**（均有固定 commit 代码核验） | 具体数字、超参、协议、规模——**但必须带分册给出的条件** |
| `[摘要级]` | **35** | RT-1、Octo、π0.5、π0.7、VersualRL（只作任务级边界参照）、RDT-1B、GR00T N1、TinyVLA、Mobile ALOHA、ALOHA Unleashed、Gemini Robotics、LIBERO、RoboCasa、Isaac Sim、ManiSkill、robosuite、V-JEPA 2、Dreamer 4、Cosmos WFM、WorldVLA、Magma、RT-H、OpenVLA-OFT、PaliGemma、BridgeData V2、RH20T、Humanoid-Gym、各官方项目页等 | **只能支撑"存在性"与"定位"**（某系统存在、它自述做什么）；**不得引用其数值** |
| `[受限核验]` | **2** | VLA 综述（2505.04769）、VLA 设计要素分析（2412.14058） | 仅作术语与检索线索；**正文未读，不作事实来源** |
| `[二手]` | **0** | — | — |

> **使用规则**：引用某条时，**先看它的等级**；`[摘要级]` 的数字**一律不入正文**，只写进第 3.3 节的登记表与第 15 章的待跟踪清单。

---

## 1. 定义与判据

### 1.1 三条判据

同时满足才纳入本专题：

- **(a) 视觉输入**：观测包含至少一路视觉信号（RGB / 深度 / 多视角），且视觉是动作生成的实际条件之一；
- **(b) 语言条件化**：动作生成以自然语言指令（或语言分解的子任务）为条件，而**不是**只用固定任务 ID / one-hot 任务标签；
- **(c) 动作输出**：模型输出**可直接执行的机器人动作信号**（关节位置 / 末端位姿增量 / 夹爪开合），或经本仓库认可的轻量动作解码器转换后可执行。

**强弱标注（不改变准入）**：

- **强 VLA**：动作头挂在**网络规模预训练 VLM**上（RT-2、OpenVLA、π0、GR00T N1）；
- **弱 VLA（无 VLM 初始化）**：满足 (a)(b)(c) 但视觉-语言塔为自有训练（RT-1 一类）。标注差异**不改变归属，只影响结论的适用范围**。

### 1.2 边界规则（可判定）

| # | 规则 | 判定 |
| :-- | :-- | :-- |
| R1 | 只输出文本 / 具身问答 / 空间指代，不输出动作 | **不入 VLA**（归 `VLM`） |
| R2 | 输出动作但**无语言指令条件化**（纯模仿 / 目标条件策略） | **不入 VLA**（归模仿学习 / Diffusion Policy 类） |
| R3 | 满足 (a)(b)(c) 但视觉-语言塔非网络规模 VLM | **入 VLA**，标注「弱 VLA（无 VLM 初始化）」 |
| R4 | **交付物是环境 / 未来观测 / 状态转移**（可交互世界模型） | **不入 VLA**，归 `WorldModels`；世界模型**作为 VLA 训练环境**计入第 4 章 |
| R5 | 联合模型（既出动作又出未来帧） | **按交付物拆分**：动作分支引本专题，world 分支引 `WorldModels` |
| R6 | 规则模拟器 / 数据集合 / benchmark 本身 | 既非 VLA 也非 WorldModels，仅作**数据与评测环境**引用 |

> **与 `WorldModels` 的对称约定**（该条目章 1 判据为 action 条件化 + 系统可调用 + 动力学自数据学得）：**输出动作 → 本专题；输出状态演化 / 可交互环境 → WorldModels**。同一篇论文的两个分支各自归属，互不吞并。

### 1.3 判例（走通判据）

| 判例 | (a) 视觉 | (b) 语言 | (c) 动作 | 归属与理由 |
| :-- | :-- | :-- | :-- | :-- |
| **CLIPort**（2021） | ✓ | ✓ 语言 grounding | ✗ 输出拾放**动作基元序列**，非可直接执行的动作信号 | **不入 VLA**（R2 邻域） |
| **Diffusion Policy**（2023） | ✓ | ✗ 论文任务为视觉运动策略，非语言指令条件 | ✓ 输出连续动作序列（动作 chunk） | **不入 VLA**（R2）：diffusion head 是 VLA 的**动作头技术**，不是 VLA 定义。`[精读原文]`（分册 1 第 1、2 问） |
| **RT-1**（2022） | ✓ | ✓ | ✓ 离散动作 token | **入 VLA**，但属**弱 VLA**（R3）：视觉-语言塔非网络规模 VLM 初始化 |
| **RT-2**（2023） | ✓ | ✓ | ✓ 动作**表示为文本 token** | **入 VLA（范式确立点）**：网页规模 VLM 与机器人轨迹**联合微调**。`[精读原文]`（分册 2） |
| **OpenVLA**（2024） | ✓ | ✓ | ✓ 每维 256 bin 的离散动作 token | **入 VLA（强，开源）**：验证了开源 VLM 主干 + 离散动作 token 的完整路线。`[精读原文]`（分册 4） |
| **π0 / π0-FAST**（2024–2025） | ✓ | ✓ | ✓ flow matching 连续动作 chunk（π0）／FAST token（π0-FAST） | **入 VLA（强）**：同一主干两条动作表征路线。`[精读原文]`（分册 5/6） |
| **GR00T N1**（2025） | ✓ | ✓ | ✓ 扩散 transformer（DiT）动作专家 | **入 VLA（强）**：双系统（System 2 VLM + System 1 动作专家） |
| **WorldVLA**（2025） | ✓ | ✓ | ✓ 动作 + 未来帧预测 | **按交付物拆分**（R5）：动作分支 → 本专题；world 分支 → `WorldModels` |
| **MuJoCo / Isaac Sim** | — | — | — | **不入本专题**（R6）：规则模拟器，仅作评测 / 数据环境 |
| **DROID**（2024–2025） | — | —（有语言标注） | ✗ **不输出动作** | **不入本专题**（R6）：它是**数据集**，不是策略。`[精读原文]`（分册 7 第 1 问自述"目标不是提出新策略架构"） |
| **SIMPLER**（2024） | — | — | ✗ **不输出动作** | **不入本专题**（R6）：它是**评测方法与环境**。`[精读原文]`（分册 8 第 1 问） |

### 1.4 判据落地时的三个已知难点（本轮更新）

1. **(b) 的"语言条件化"仍缺可操作阈值**：语言**实际影响**动作 vs 语言仅作任务标签，目前只能靠"换指令是否改变行为"的对照测试来判定（见 [失效边界专题](topics/deployment-boundaries.md) §5 的可观测信号）。**仍未定稿。**
2. **"轻量动作解码器"的边界**：把 latent action 解码为动作是否算 (c)，尚无判定案例。**未确证。**
3. **数据/评测类工作（DROID、SIMPLER）虽不入 VLA 本体，却必须精读**：因为它们决定了 VLA 数字的**可用性与可比性**——本轮为此设了独立分册（分册 7/8）与评测专题，**归属仍是 R6，不因精读而升格**。

---

## 2. 架构谱系：动作表征三条路线

**本章要回答**：三种动作表征（token / flow matching / diffusion head）各自的训练目标、推理代价、代表系统是什么？为什么同一主干会同时提供多条路线？

> **本章的机制级展开见 [`topics/action-representation.md`](topics/action-representation.md)**（含判定规则、超参速查、代码事实索引）。此处只给结论与对照。

### 2.1 路线总览

| 路线 | 动作空间 | 训练目标 | 推理形态 | 代表系统（证据） |
| :-- | :-- | :-- | :-- | :-- |
| **token（离散 / 自回归）** | 离散 token 序列 | 与语言模型同源的 next-token 交叉熵 | 自回归解码，token 数 = 动作维 × 步数（或 FAST 压缩后更少） | RT-2、OpenVLA、π0-FAST |
| **flow matching（连续）** | 连续 action chunk | 向量场 / 速度回归（噪声与目标线性插值） | 少数步（π0 官方默认 10 步）数值积分 | π0、GR00T N1 的 System 1 |
| **diffusion head（连续）** | 连续 action chunk | 去噪目标（DDPM 式） | 多步迭代去噪（可用 DPM-Solver 等加速） | Diffusion Policy、RDT-1B |

### 2.2 token 路线

- **动作作为文本 token**：RT-2 把动作写成文本 token 并入训练集，与网络规模视觉-语言任务**联合微调**（co-fine-tuning），**不新增 action 专用参数层**——语言与动作任务完全共享权重。`[精读原文]`（分册 2 §2）
- **每维分箱离散化**：OpenVLA 沿用 7B 开源 VLM 主干 + **每动作维 256 bin** 的离散 token 化；目标区间均匀分箱、取 bin 中心反离散化、再做 q01/q99 反归一化。`[精读原文]`（分册 4 §2）+ `[代码事实]`（2.3 节）
- **FAST tokenizer**：解决"逐维逐时刻分箱在高频灵巧数据上表现差"的问题——用频率域变换 + BPE 把动作 chunk 压成"学到的字"，把 token 数降到**每臂约 30 个 token**量级。`[精读原文]`（分册 6 §2/§4）
- **压缩率带条件**：FAST 的压缩率与训练步数收益**逐数据集不同**（Bridge V2 / DROID / bussing / shirt-folding 各不相同）——**引用必须带数据集与频率条件**。`[精读原文]`（分册 6 Table I）

### 2.3 代码事实核验（file:line）

> **口径**：下列为**代码事实**（对固定 commit 的源码读数），**不等于论文方法**；与论文表述冲突时以论文为准并另行标注。**研究推断**单独标 `[推断]`。完整表见 [动作表征专题](topics/action-representation.md) §7。

| 事实 | 证据（`仓库@commit:文件:行`） |
| :-- | :-- |
| OpenVLA 动作离散化：目标 -1:1 均匀分箱 + 取 bin 中心反离散化 + q01/q99 反归一化 | `openvla/openvla@c8f03f48af692657d3060c19588038c7220e9af9:prismatic/extern/hf/modeling_prismatic.py:499-500`（`self.bins = np.linspace(-1, 1, config.n_action_bins)`、`self.bin_centers`）、`:506-536`（`predict_action` 解码与反归一化）、`:492`（`class OpenVLAForActionPrediction`） |
| π0 的 flow matching 训练目标为线性插值 + 速度回归 | `Physical-Intelligence/openpi@215abfb217dbac7d5f1273282331b9b1866c0479:src/openpi/models/pi0.py:192-201`（`noise`、`time ~ Beta(1.5,1)`、`x_t = t·noise + (1-t)·actions`、`u_t = noise - actions`） |
| π0 采样为固定步长积分，默认 **10 步** | 同上 `:217-220`（`sample_actions(..., num_steps: int = 10)`）、`:273-284`（`jax.lax.while_loop` 到 `time >= -dt/2`） |
| π0-FAST 用交叉熵自回归预测动作 token（next-token shift） | 同上 `:src/openpi/models/pi0_fast.py:198-212`（`compute_loss` → one-hot targets，input tokens 左移 1） |
| FAST tokenizer 默认从 HF Hub 取 `physical-intelligence/fast`，并跳过 PaliGemma 词表末尾 128 个 special token | 同上 `:src/openpi/models/tokenizer.py:51-62` |
| GR00T N1.7 动作头是 **DiT + flow matching 扩散过程**（torch 侧，非 JAX） | `NVIDIA/Isaac-GR00T@dac54b313160c201c450f97df0fd74ebd379c892:gr00t/model/gr00t_n1d7/gr00t_n1d7.py:38-40`（`class Gr00tN1d7ActionHead` docstring "flow matching diffusion policy"）、`:50-61`（`AlternateVLDiT` / `DiT`）、`:326-360`（`get_action_with_features`：先 `torch.randn` 初始化动作再积分）；`gr00t/model/modules/dit.py:222`（`class DiT`）、`:61-71`（`TimestepEncoder`） |
| RDT-1B 用 DDPM 训练 + DPM-Solver 多步采样 | `thu-ml/RoboticsDiffusionTransformer@cd79363a1387e8f81c7724d070ef7e45fd23150f:models/rdt_runner.py:59-73`（`DDPMScheduler` / `DPMSolverMultistepScheduler` / `num_inference_timesteps`）、`:119-163`（`conditional_sample` 迭代） |
| LeRobot 的 DiffusionPolicy 用 1D UNet + DDPM/DDIM 调度器 | `huggingface/lerobot@297774fca4e3ad0aa34e7425fbf937111637e77b:src/lerobot/policies/diffusion/modeling_diffusion.py:56-63`、`:201-244`（`DiffusionModel`、`self.unet = DiffusionConditionalUnet1d(...)`、`_make_noise_scheduler`） |

**研究推断** `[推断]`：token 路线的推理延迟随"token 数"（∝ 动作维 × 频率 ÷ 压缩率）增长，故 **FAST 一类压缩 tokenizer 可以缓解特定自回归 token 配方的高频瓶颈**；flow matching 与 diffusion head 的取舍主要在**步数与稳定性**（π0 代码默认 10 步 vs Diffusion Policy 典型 100 步训练 / 多步采样），此推断需以论文消融表核对。

### 2.4 路线分界的可判定表述

- 动作是**离散符号**、由语言模型头直接生成 → **token 路线**；
- 动作是**连续向量**、由回归"噪声→目标"的向量场得到 → **flow matching**（线性插值目标，π0 代码形态）；
- 动作是**连续向量**、由逐步去噪（DDPM/DDIM/DPM-Solver）得到 → **diffusion head**。

### 2.5 本章遗留（本轮未能关闭）

- GR00T N1 论文（DiT 动作专家）与 GR00T N1.7 代码（`AlternateVLDiT`）的差异需显式对齐；**旧路径 `gr00t/model/gr00t_n1.py` 在默认分支已 404**，对齐论文须取发布 tag 或历史 commit。`[受限核验]`
- 三类动作头在同一基准上的**延迟 / 成功率对照实验**本轮**仍未找到**（各方均为自报数据）。
- π0 / FAST 的 token 压缩率与推理加速倍数已入分册（带数据集条件），但**"压缩率 → 下游成功率"的因果曲线原文未给**。

---

## 3. 代表系统逐案（精读后更新）

**本章要回答**：RT-2、π0、OpenVLA、FAST 等系统各自的判据落位、动作表征、一手来源与关键结论是什么？

### 3.1 核心四案（本轮均为 `[精读原文]`）

| 系统 | 判据落位 | 动作表征 | 关键结论（带条件） | 分册 |
| :-- | :-- | :-- | :-- | :-- |
| **RT-2**（Google DeepMind，2023-07-28） | 强 VLA（网络规模 VLM 联合微调） | **文本 token**（动作写成离散 bin 序号整数） | 把动作表达为文本 token 与网页数据**联合微调**；约 **6,000 条**评测轨迹；消融显示 **co-fine-tuning 优于纯机器人数据微调**（55B unseen 总平均 63 vs 52），涌现语义能力可定量度量；**闭源** | [分册 2](papers/2307.15818-rt2.md) |
| **OpenVLA**（Stanford 等，2024-06-13 / v3 2024-09-05） | 强 VLA，**开源** | **离散 token（每维 256 bin）** | 7B 开源 VLA，**970k 真机示范**（OpenX）；64×A100×14 天 ≈ **21,500 A100-hours**、27 epochs；开箱即用跨本体 + 参数高效微调（LoRA r=32）+ 量化推理均有对照 | [分册 4](papers/2406.09246-openvla.md) |
| **π0**（Physical Intelligence，2024-10-31 / v4 2026-01-08） | 强 VLA | **flow matching** 连续 action chunk | 预训练 VLM 主干 + **300M action expert**；`H = 50`、**固定 10 步** Euler 积分、时间采样 **shifted Beta(1.5,1) 且 s=0.999**；on-board 推理 **73 ms**（RTX 4090）；20 Hz 本体每 0.8 s 推理（执行 16 步）、50 Hz 本体每 0.5 s（执行 25 步） | [分册 5](papers/2410.24164-pi0.md) |
| **FAST**（Physical Intelligence 等，2025-01-16） | token 路线的**使能技术** | **频率域 + BPE 动作 tokenizer** | 解决逐维逐时刻分箱在高频灵巧数据上失效；token 数降到每臂约 30；DROID 零样本评测 **16 任务 × 每策略 44 trials × 3 校园**；训练步数与 GPU 小时收益**逐任务不同** | [分册 6](papers/2501.09747-fast.md) |

### 3.2 数据与评测三案（本轮新增精读，归属仍为 R6）

| 对象 | 交付物 | 关键结论（带条件） | 分册 |
| :-- | :-- | :-- | :-- |
| **Open X-Embodiment**（2023-10-13 / v9 2025-05-14） | 数据集 + RT-X 模型（社区聚合） | **1M+ 轨迹 / 22 本体 / 60 数据集 / 34 实验室 / 527 技能**；训练侧只用 **9 本体**、真机评测 **6 机器人 / 3600 trials**；Table II 消融给出**收益门槛**（5B 有 2 帧历史 44.4% vs 无历史 14.5%；55B 75.8%；**from scratch 0%**）；**跨本体正迁移依赖互联网预训练** | [分册 3](papers/2310.08864-open-x-embodiment.md) |
| **DROID**（2024-03-19 / v2 2025-04-22） | 数据集 + 采集协议 + 权重 | **76k 轨迹 / 350 小时 / 564 场景 / 52 建筑 / 86 任务 / 50 采集员 / 13 机构 / 12 个月**；统一 **Franka Panda + 15 Hz** 硬件栈、复刻 **18 套**；6 任务 4 地点、平均 **+20%**；**CC-BY 4.0 全开源**；**单本体是硬边界** | [分册 7](papers/2403.12945-droid.md) |
| **SIMPLER**（2024-05-09） | 仿真评测环境 + 方法论 | 真机策略放进仿真做**成对评测**；2 本体 / 9 个策略 checkpoint / 约 **∼1500 配对 episodes**；主张**相对排序强相关**，原文自承"仿真永远是不完美代理"；**相关性系数不可外推为绝对成功率** | [分册 8](papers/2405.05941-simpler.md) |

### 3.3 同族、相邻与闭环系统

| 系统 | 一句话定位 | 证据 |
| :-- | :-- | :-- |
| RT-1 (2022) | VLA 前置形态：无网络规模 VLM 初始化的语言条件化机器人 Transformer | `[摘要级]`（arXiv:2212.06817 v2 2022-12-13） |
| Octo (2024) | 开源通用机器人策略（非网络规模 VLM 主干） | `[摘要级]`（arXiv:2405.12213 v2 2024-05-20） |
| π0.5 (2025-04-22) | 异构任务**协同训练**支持开放世界泛化（多机器人 + 高层语义 + 网页数据） | `[摘要级]`（arXiv:2504.16054 v1 2025-04-22 摘要 + 官方博客） |
| π*0.6 / RECAP (2025-11-19 v2) | 从真机 rollouts、回报与纠正中跨 episode 改进 VLA | `[精读原文]`（分册 9；arXiv:2511.14759v2） |
| VLCP (2026-08-17 v1) | 冻结 VLM 在同一仿真 episode 内重写 Python 控制函数；当前无实机证据 | `[精读原文]`（分册 10；arXiv:2608.16978v1） |
| LingBot-VA (2026-03-22 v2) | 自回归视频/动作世界模型；异步 chunk 执行时用真实 observation 接地 | `[精读原文]`（分册 11；arXiv:2601.21998v2） |
| VersualRL (2026-07-19 v3) | 真实移动机器人按视觉 critic 跨 episode 修改任务级 Behavior Tree；不直接输出低层动作 | `[摘要级]`（arXiv:2603.22169v3；仅作边界参照） |
| π0.7 (2026-04-16) | 官方博客称"可引导（steerable）模型 + 涌现能力"的机器人基础模型；**本轮未找到对应 arXiv 条目** | `[摘要级]`（官方博客 "A Steerable Model with Emergent Capabilities"）；**待跟踪** |
| RDT-1B (2024-10-10) | 双臂操作的 **diffusion** 基础模型（1B 级，非网络规模 VLM） | `[摘要级]`（arXiv:2410.07864 v2 2024-10-10 + 官方仓库） |
| GR00T N1 (2025-03-18) | 人形双系统基础模型：System 2 VLM + System 1 DiT 动作专家 | `[摘要级]`（arXiv:2503.14734 v2 2025-03-27 + 官方仓库） |
| TinyVLA (2024-09-19) | 快速、数据高效的轻量 VLA | `[摘要级]`（arXiv:2409.12514 v5 2024-09-19） |
| ALOHA Unleashed (2024-10-17) | 双臂灵巧操作的工程配方（数据侧） | `[摘要级]`（arXiv:2410.13126 v1 2024-10-17） |
| Mobile ALOHA (2024-01-04) | 低成本全身遥操作 + 双臂移动操作（数据侧，非 VLA 本体） | `[摘要级]`（arXiv:2401.02117 v1 2024-01-04） |
| LIBERO / RoboCasa | 仿真基准 / 仿真环境（R6，仅作评测环境） | `[摘要级]`（arXiv:2306.03310 v2 2023-06-05 / arXiv:2406.02523 v1 2024-06-04） |
| OpenVLA-OFT (2025-02-27) | VLA 微调的速度—成功率优化 | `[摘要级]`（arXiv:2502.19645 v2 2025-02-27 + 官方页） |
| Gemini Robotics (2025-03-25) | 物理世界多模态 agent 方向的大厂报告 | `[摘要级]`（arXiv:2503.20020 v1 2025-03-25）；**归属待定（R1/R3 边界）** |
| Humanoid-Gym (2024-04-08) | 人形 sim-to-real 的 RL 工程工作（**无语言条件化，R2 排除**） | `[摘要级]`（arXiv:2404.05695 v2 2024-04-08） |

> **口径提醒**：仍标 `[摘要级]` 的条目定位取自摘要/官方页面。三个闭环分册的结果须按对应图表、任务条件和边界引用；VersualRL 只证明任务层 BT 迭代，不证明低层 VLA 成功率。

### 3.4 本章遗留

- GR00T N1 / RDT-1B / π0.5 是否需升格为独立分册（名额与分工问题，见 [CANDIDATES.md](sources/CANDIDATES.md) §1/§3）——本轮按"先筛选后精读、按价值不硬凑"的口径**未设分册**；
- π0.5 / π*0.6 / π0.7 是否为同一系统的迭代，**不得据博客标题推断**；
- 各系统自报成功率、延迟、数据规模的**具体数值**已按分册收入的入表，但**跨系统横比仍不可做**（第 5 章）。

---

## 4. 数据：真机与仿真

**本章要回答**：真机数据与仿真数据各自提供什么、边界在哪？世界模型作为训练环境处于什么位置？

> **本章的机制级展开见 [`topics/evaluation-and-datasets.md`](topics/evaluation-and-datasets.md) §3**（数据规模、频率不一致、许可与可再分发性）。

### 4.1 真机数据（一线来源）

| 数据集 / 平台 | 规模与要点 | 证据 |
| :-- | :-- | :-- |
| **Open X-Embodiment** | 面向"跨机器人（X-robot）通用策略"的**标准化数据格式 + 数据集 + RT-X 模型**；1M+ 轨迹 / 22 本体 / 60 数据集 / 34 实验室 | `[精读原文]`（[分册 3](papers/2310.08864-open-x-embodiment.md)） |
| **DROID** | in-the-wild 大规模真机操作数据集：76k 轨迹 / 350 小时 / 564 场景 / 52 建筑 / 86 任务；统一 Franka Panda + 15 Hz 硬件栈 | `[精读原文]`（[分册 7](papers/2403.12945-droid.md)） |
| **OpenVLA 训练数据** | 970k 真机示范（OpenX 子集，含 DROID 保守权重，末段移除 DROID） | `[精读原文]`（[分册 4](papers/2406.09246-openvla.md) §3） |
| **π0 预训练混合** | 自有数据 + 开源数据（开源约占 9.1%，含 OXE 子集 / Bridge v2 / DROID） | `[精读原文]`（[分册 5](papers/2410.24164-pi0.md) §3） |
| **FAST 用的 DROID 切片** | 仅取成功 episode 并滤 idle 步（轻量清洗） | `[精读原文]`（[分册 6](papers/2501.09747-fast.md) §3 + Appendix D） |
| BridgeData V2 / RH20T / Mobile ALOHA | 多环境操作数据 / 多样化技能数据 / 低成本遥操作采集 | `[摘要级]`（官方页 / arXiv 摘要） |

> **口径纪律**：不同数据集的"规模"口径不同（轨迹 / episodes / 小时 / 帧数），**跨表比较无效**。已发现一处**未裁决的口径冲突**：DROID 原文报 **350 小时**，而 GR00T N1 论文的数据表把 "DROID (OXE)" 记为 **23.1M 帧 / 428.3 小时**——两者不一致，引用以 DROID 原文为准。详见 [分册 7 待核清单](papers/2403.12945-droid.md) 与 [评测专题 §7](topics/evaluation-and-datasets.md)。

### 4.2 仿真平台（评测 / 合成数据）

| 平台 | 定位 | 证据 |
| :-- | :-- | :-- |
| **MuJoCo / robosuite** | 规则物理引擎（本专题不视为世界模型，见第 7 章 R6） | `[摘要级]`（官方页） |
| **Isaac Sim** | NVIDIA 机器人仿真与合成数据生成平台 | `[摘要级]`（官方页 developer.nvidia.com/isaac/sim） |
| **ManiSkill** | 操作技能仿真 / 基准平台 | `[摘要级]`（官方页 maniskill.ai） |
| **LIBERO** | 面向**终身机器人学习**的操作基准（任务间迁移维度） | `[摘要级]`（arXiv:2306.03310 v2 2023-06-05 + 官方项目页） |
| **RoboCasa** | 日常场景（厨房为主）大规模仿真 | `[摘要级]`（arXiv:2406.02523 v1 2024-06-04 + 官方页 robocasa.ai） |
| **SIMPLER** | 用"控制 + 视觉差异缓解"构建真机对应仿真环境，做 sim-real **成对评测** | `[精读原文]`（[分册 8](papers/2405.05941-simpler.md)） |
| **Humanoid-Gym** | 人形 RL + 零样本 sim2real（无语言条件化） | `[摘要级]`（arXiv:2404.05695 v2 2024-04-08） |

### 4.3 世界模型作为训练环境（与 `WorldModels` 的接口）

- **接口定义**：世界模型在本专题中**不作为 VLA 本体**，而作为三类资源：①**合成训练数据**（生成轨迹 / 观测）；②**可交互练习环境**（策略在学得的环境里做 RL / 规划）；③**评测环境**（在与真机对齐的想象环境中打分）。
- **已核验的一手接口对象**（本轮均只登记，**不重复展开**）：
  - V-JEPA 2 官方摘要称其视频模型可支持 **understanding / prediction / planning**。`[摘要级]`（arXiv:2506.09985）
  - Dreamer 4 官方摘要题为 "Training Agents Inside of Scalable World Models"。`[摘要级]`（arXiv:2509.24527）
  - Cosmos World Foundation Model Platform 定位为 Physical AI 的**世界基础模型平台**。`[摘要级]`（arXiv:2501.03575）
  - **WorldVLA** 为"自回归动作世界模型"，同时涉及动作与未来帧。`[摘要级]`（arXiv:2506.21539 v1 2025-06-26）
- **归属规则**：上述四条**全部归属 `WorldModels`**，本专题只登记"可被 VLA 消费"的接口，**不重复展开其架构与评测**（见第 7 章）。

**本章遗留**：①真机数据集许可与可下载性按 [MANIFEST.md](sources/MANIFEST.md) 分别核对；②已有五篇直接研究世界模型数据、imagined RL 与 VLA 真机迁移（见[迁移专题](topics/world-model-to-vla-transfer.md)），但各论文的模型角色、真机预算和指标不同，仍无同任务同预算的跨方法对照；③LingBot-VA 是部署时预测/动作闭环与真机表现证据，不等于世界模型合成数据训练效果。

---

## 5. 评测

**本章要回答**：真机成功率与仿真基准能否相互替代？差异来源与可比性边界是什么？

> **本章的机制级展开见 [`topics/evaluation-and-datasets.md`](topics/evaluation-and-datasets.md)**（六问检查表、协议对照、引用模板）。此处只给结论。

### 5.1 本章结论

1. **真机评测**：指标以任务成功率 / 吞吐为主，是事实标准；缺陷是**不可复现**（场景、初始条件、物体摆放、机器人本体差异大），且成功判据**普遍依赖人工**。
2. **仿真评测**：可复现、可大规模并行，缺陷是**保真度受限**。SIMPLER 的明确立场是：不必做全保真数字孪生，只需缓解**控制差异与视觉差异**，其目标是**相对排序**相关。`[精读原文]`（分册 8）
3. **反方证据（一手摘要级）**：π0.5 以真机开放世界泛化为目标，说明"在仿真中表现好的策略在真机泛化上仍然不够"。`[摘要级]`（arXiv:2504.16054 摘要）
4. **两条不矛盾**：SIMPLER 谈**排序**，π0.5 谈**绝对泛化**；把它们当成对立观点是误读。
5. **LIBERO 的定位**：面向**终身学习**（知识迁移）的基准，评估维度是任务间迁移而非单一真机成功率，**与其他基准不可直接比较**。`[摘要级]`（arXiv:2306.03310）
6. **可比性规则（本专题约定）**：
   1. 不同基准的分数**不得横向比较**，除非明确说明本体、观测、动作空间与评测协议一致；
   2. 引用任一 VLA 成功率必须同时给出**基准 / 本体 / 评测协议**三要素（建议再加频率与 trial 数）；
   3. 仿真结果只能作为**相对排序**参考，不能作为真机绝对性能的代理。

### 5.2 引用前的六问（强制）

| # | 检查项 | 缺了会怎样 |
| --: | :-- | :-- |
| 1 | **本体**（型号 + 自由度 + 夹爪） | 跨本体求和 = 编造 |
| 2 | **控制频率** | 高频任务与低频不可换算 |
| 3 | **任务数与每任务 trial 数** | 小样本被当结论 |
| 4 | **评测协议**（相机、是否腕部、评分是否含部分分、成功判据由谁判） | 协议差异被当模型差异 |
| 5 | **是否有仿真成分**及其角色（训练 / 评测） | 把仿真分数当真机结论 |
| 6 | **数据来源与许可** | 数字无法复现 |

### 5.3 本章遗留

- SIMPLER 的相关系数具体数值与样本量**已入分册**（引用时带 `arXiv:2405.05941 v1 2024-05-09`），但**其内部两处口径不一致仍标 `[待核]`**（见 [分册 8](papers/2405.05941-simpler.md) §9）；
- 真机评测的标准报告项清单**仍未形成**；
- 「失败类型分布」各论文普遍不报，导致失效模式**无法从成功率反推**（见第 10 章）。

---

## 6. 应用域

| 应用域 | 判据落位要点 | 当前证据 |
| :-- | :-- | :-- |
| **固定工位机械臂 / 抓取装配** | 语言条件化 + 高精度动作；数据以真机示范为主 | `[精读原文]`（分册 2/4 的评测形态）；`[摘要级]`（RT-1） |
| **双臂 / 灵巧操作** | 动作频率高、维数高，**token 路线压力最大**（FAST 的直接动机） | `[精读原文]`（分册 6 §1；分册 5 的 50 Hz 任务） |
| **移动操作 / 家务开放世界** | 需要跨场景泛化与长时程任务分解，依赖异构数据协同训练 | `[精读原文]`（分册 7 的家庭评测；分册 5 的多阶段任务）；`[摘要级]`（π0.5） |
| **人形机器人** | 全身动作，双系统分工（慢思考 + 快动作） | `[摘要级]`（GR00T N1 摘要 + 官方仓库） |
| **自动驾驶** | 语言指令条件化弱、评测在仿真世界模型中闭环 | `[摘要级]`（本专题**不展开**：GAIA-1/2、Vista 属 `WorldModels` 章 6） |
| **实验室 / 办公室自动化** | 场景可控、任务可枚举；DROID 与 SIMPLER 的评测场景 | `[精读原文]`（分册 7/8） |

**本章遗留**：每域补 1 个可核验的一手评测案例；明确"自动驾驶是否算 VLA"的判定（语言条件化不满足时按 R2 排除，**仍未定稿**）。

---

## 7. 与 WorldModels / VLM / Agent 的边界与交叉引用

**本章要回答**：四者边界如何执行？哪些工作应引对方报告而非重复？

### 7.1 边界表（可判定）

| 领域 | 交付物 | 判据要点 | 归属 |
| :-- | :-- | :-- | :-- |
| **本专题 EmbodiedVLA** | **动作信号 / 可部署策略** | 视觉 + 语言条件化 + 动作输出（R1–R3） | 本报告 |
| **WorldModels** | **状态演化 / 可交互环境** | action 条件化 + 系统可调用 + 动力学自数据学得 | `WorldModel/WorldModels/report.md` 章 1 |
| **VLM** | **文本 / 具身问答 / 空间指代** | 无动作输出 | `LLM/VLM/report.md` |
| **Agent** | **外层决策循环 / 工具调用** | 编排与记忆，动作由下层策略执行 | `LLM/Agent/report.md` |
| **规则模拟器 / 数据集 / 基准** | 环境或数据（硬编码动力学 / 采集数据 / 评测协议） | 不满足 WorldModels 的 (c) 也不满足本专题的 (c)（R6） | 本专题仅作评测环境 / 数据引用 |

### 7.2 与 `WorldModels` 的显式互引（避免重复劳动）

| 交叉对象 | 在本专题的处理 | 在 WorldModels 条目的处理 |
| :-- | :-- | :-- |
| **π0 类策略本体（action head）** | 本专题第 2、3 章展开 | 该条目章 1.3 已判定："**Embodied**，不因「用了世界模型」改判"——**互引确认，不重复展开** |
| **WorldVLA** | 只登记动作分支（本报告参考文献 6） | 该条目负责 world 分支 |
| **V-JEPA 2 / V-JEPA 2-AC** | 本专题第 4.3 节只登记"作为训练/规划环境"的接口 | 该条目负责模型与规划机制 |
| **Dreamer 4** | 接口②③的案例 | 该条目负责模型与评测 |
| **Cosmos WFM** | 接口①的工业化形态 | 该条目负责平台与机制 |
| **Genie / GameNGen 等交互式世界模型** | **不在本专题出现**（无动作策略交付物） | 该条目展开 |
| **仿真平台（Isaac Sim / ManiSkill / RoboCasa / LIBERO / SIMPLER）** | 本专题第 4.2、5 章按"评测环境"引用；**SIMPLER 本轮已精读** | 该条目已将规则模拟器排除出 WorldModels，仅作评测环境/数据来源——**口径一致** |
| **自动驾驶世界模型（GAIA-1/2、Vista）** | 本专题仅在第 6 章登记"不展开" | 该条目展开 |

> **互引落点（精确到章）**：本报告章 1.3 / 4.3 / 7.1 ↔ `WorldModels` 章 1.3 / 1.2 / 7。两侧口径若冲突，**以"交付物判定"为准**。

### 7.3 与 VLM / Agent 的交叉

- **VLM → VLA**：VLA 的"视觉-语言塔"直接复用 VLM（RT-2 联合微调、OpenVLA 开源主干、π0 建于预训练 VLM 之上）——VLM 条目的架构与时序能力是其上游，本专题只处理**动作头与训练目标**的差异。`[精读原文]`（分册 2/4/5）
- **VLA vs Agent**：VLA 是**策略**（观测→动作），Agent 是**外层循环**（规划、工具、记忆）。含高层语义子任务预测的 π0.5 处于两者交叠，需定判定细则。`[摘要级]`（π0.5 摘要含 "semantic subtask prediction"）
- **具身问答 / 指代**（如 Magma 一类多模态 agent 基础模型）按 R1 判为**不入 VLA**。`[摘要级]`（arXiv:2502.13130 v1 2025-02-18）

---

## 8. 未决问题

1. **定义收敛**：VLA 是否需要"网络规模 VLM 初始化"作为必要条件？RT-1 一类如何表述才不引起误用？（第 1 章）
2. **动作表征的量化取舍**：token / flow matching / diffusion head 的**推理延迟—成功率**曲线为何？现有对照均为各系统自报，**无共基准横评**。（第 2 章、[动作表征专题](topics/action-representation.md) §8）
3. **世界模型怎样影响 VLA 真机表现**：现有论文报告了合成示范、视频生成轨迹和模型内 RL 的真机结果；仍需在相同 backbone、任务协议和真实交互预算下比较三条路线。（[世界模型到 VLA 迁移专题](topics/world-model-to-vla-transfer.md)）
4. **sim-real 相关性是否可复现**：SIMPLER 主张**排序**强相关、π0.5 主张真机泛化仍难；两者是否在同一本体 / 同一评测协议下可比，需要精读核对。（第 5 章）
5. **双系统是否为必要架构**：GR00T N1 的 System 2 / System 1 分工是设计选择还是规模必需？（第 3.3 章，未精读）
6. **安全问题**：VLA 的失败恢复、越界动作抑制、人在环路接管缺乏统一判据与报告项；新增工作在各自实验边界内研究恢复/策略更新，仍无通用协议（见[闭环控制专题](topics/closed-loop-control.md)）。
7. **口径冲突未裁决**：DROID 的 350 小时 vs GR00T N1 引用的 428.3 小时（第 4.1 章）。
8. **数据频率混合的一致性**：同一训练混合里不同子集的控制频率不同，"一个动作 token 代表多少秒"在子集间不一致——**是否需要显式频率条件化**尚无一手结论。（[评测专题](topics/evaluation-and-datasets.md) §3.1）

---

## 9. 基线系统对比总表（基础批次 8 篇精读汇总）

> **本表不是排行榜**：每列数值都来自各自的条件（本体 / 频率 / 任务数 / trial 数 / 协议），**列之间不可比**。用途是"一张表看清各系统的口径差异"。

| 维度 | RT-2 | OpenVLA | π0 | FAST | Diffusion Policy | OXE（数据） | DROID（数据） | SIMPLER（评测） |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 类型 | 强 VLA（闭源） | 强 VLA（开源） | 强 VLA | 动作 tokenizer | 动作头（非 VLA） | 数据集 + RT-X | 数据集 + 协议 | 评测方法论 |
| 动作表征 | 文本 token | 256-bin 离散 token | **flow matching** | 频率域 + BPE tokenizer | **diffusion head** | 256 bins × 8 维 | —（语言标注 + 动作） | — |
| 主干 | PaLI-X 5B/55B、PaLM-E 12B | Prismatic-7B（Llama 2） | PaliGemma 3B + 300M expert | —（插到自回归 VLA 上） | 1D UNet / ViT | RT-1-X 35M / RT-2-X 55B | — | — |
| 数据规模（口径） | RT-1 协议 + 网页数据 | **970k 示范** | 自有 + 开源 9.1% | 与 π0 同混合 | 仿真 + 真机任务集 | **1M+ 轨迹 / 22 本体** | **76k / 350 h / 564 场景** | 训练集 ≥80k demos |
| 评测本体 | Google Robot 等 | Google Robot / WidowX / Franka ×2 | 7 类配置（含移动） | 7 套件（6 真机 + 1 仿真） | 仿真 15 任务 + 真机 7 任务 | 6 机器人 / 3600 trials | 6 任务 / 4 地点 | 2 本体 / 9 checkpoint |
| 开源 | ✗ | ✓（权重+代码+数据） | ✓（代码/权重） | ✓ | ✓ | ✓（数据+工具+checkpoint） | ✓（数据+权重+指南） | ✓（环境） |
| license | arXiv 默认 | CC BY 4.0 | arXiv 默认 | CC BY 4.0 | arXiv 默认 | CC BY 4.0 | **CC BY 4.0** | CC BY 4.0 |
| 主要失效边界 | 闭源不可复现；无新物理技能；1–3 Hz | DROID 域学不会；离散化误差 | 步数—成功率曲线未给 | 压缩率逐数据集不同 | 多步采样延迟 | 小容量 + 大数据域欠拟合 | **单本体**；成功轨迹过滤 | 只支撑排序，不支撑绝对值 |

> 逐条数字与条件见对应分册；本表**刻意不填跨系统可比的"统一分数"**——因为没有共基准。

---

## 10. 失效边界综述（按类归纳）

> **机制级展开见 [`topics/deployment-boundaries.md`](topics/deployment-boundaries.md)**。此处给出结论级的六类。

1. **数据分布缺口**：目标场景 / 本体 / 任务不在训练分布内 → 语义理解对、动作不对。OXE 的分域结论与 DROID 的单本体边界都属此类。
2. **仿真—真机错位**：用仿真分数替代真机结论。SIMPLER 自承"不完美代理"；π0.5 反证绝对泛化仍有落差。
3. **延迟 / 频率不匹配**：控制频率高于推理吞吐 → 策略"看到的是过去"。π0 的推理间隔按频率分档（0.8 s/16 步 vs 0.5 s/25 步）正是这一约束的显式体现。
4. **动作离散化误差**：高频灵巧 + 逐维分箱 → 抖动与不连贯。FAST 的核心动机；OpenVLA 训练中 DROID 域 action token accuracy 持续偏低的案例是**可观测证据**。
5. **表征 / 容量瓶颈**：异构度超过容量 → 某数据域"学不会"（可观测为分域 accuracy 不收敛）。OXE 的 35M 欠拟合与 OpenVLA 移除 DROID 都属此类。
6. **评测 / 安全缺位**：本次核对的工作分别提出局部恢复、越界处理或人在环路方案，但尚未形成可跨任务通用的协议（见[闭环控制专题](topics/closed-loop-control.md)）；这限制跨系统结论的可比性。

**跨类共同点**：没有一篇给出可跨任务通用的失败恢复 / 人工接管协议。闭环控制新文献已有各自方案，但分别落在 episode 内代码修订、跨 episode 参数学习、世界模型 chunk 接地与任务级 BT 更新；细节见[闭环控制专题](topics/closed-loop-control.md)。第 3 类（延迟）与第 4 类（离散化）在**高频 + 高动作维**场景会同时命中。

---

## 11. 演进时间线（每个节点"新增了什么判据 / 机制"）

| 时间 | 工作 | 新增了什么（判据 / 机制 / 数据） | 等级 |
| :-- | :-- | :-- | :-- |
| 2021-09 | CLIPort（2109.12098） | 语言 grounding + 动作基元组合；**不满足 (c)，被 R2 排除** | `[摘要级]` |
| 2022-12 | RT-1（2212.06817） | 语言条件化机器人 Transformer；**无网络规模 VLM 初始化 → R3 弱 VLA** | `[摘要级]` |
| 2023-03 | **Diffusion Policy**（2303.04137） | **把策略建模为条件去噪扩散**；动作多模态的非参数化建模 | `[精读原文]` |
| 2023-07 | **RT-2**（2307.15818） | **动作即文本 token + 与网页数据联合微调** → VLA 范式确立 | `[精读原文]` |
| 2023-10 | **Open X-Embodiment**（2310.08864） | **跨本体数据格式标准化 + 正迁移证据 + 收益门槛（容量 × 数据域）** | `[精读原文]` |
| 2024-01 | Mobile ALOHA（2401.02117） | 低成本全身遥操作数据采集（数据侧） | `[摘要级]` |
| 2024-03 | **DROID**（2403.12945） | **统一硬件栈 + 分布式采集协议**；场景/交互位置多样性成为可分析的量 | `[精读原文]` |
| 2024-05 | **SIMPLER**（2405.05941） | **real→sim 成对评测 + MMRV**；把"仿真能不能代理真机"变成可度量命题 | `[精读原文]` |
| 2024-06 | **OpenVLA**（2406.09246） | **开源 7B + 256-bin 离散 token 的可复现基线**；参数高效微调与量化推理 | `[精读原文]` |
| 2024-10 | π0（2410.24164） | **flow matching 动作头 + action expert**；高频灵巧的连续动作 chunk | `[精读原文]` |
| 2024-10 | RDT-1B（2410.07864） | 双臂 diffusion 基础模型 + 异构数据统一动作空间 | `[摘要级]` |
| 2025-01 | **FAST**（2501.09747） | **频率域动作 tokenizer**；token 路线可用于高频任务的使能技术 | `[精读原文]` |
| 2025-03 | GR00T N1（2503.14734） | 人形双系统（System 2 VLM + System 1 DiT） | `[摘要级]` |
| 2025-04 | π0.5（2504.16054） | 异构任务协同训练支持开放世界泛化 | `[摘要级]` |
| 2025-06 | WorldVLA（2506.21539） | 自回归动作世界模型（按 R5 拆归属） | `[摘要级]` |
| 2025-11 | **π*0.6 / RECAP**（2511.14759） | advantage-conditioned policy 通过真机 rollouts 与纠正跨 episode 改善 VLA | `[精读原文]` |
| 2026-01 | **LingBot-VA**（2601.21998） | 视频世界模型、动作 chunk 和执行并行；新 chunk 以真实 observation 与 FDM 接地 | `[精读原文]` |
| 2026-03 | [VersualRL（2603.22169v3）](https://arxiv.org/html/2603.22169v3) | 真移动机器人上按视觉反馈跨 episode 改写任务层 Behavior Tree；actor 在符号层修改预置节点树，不直接接收原始感知流或控制机器人（§III-A–B） | `[摘要级]`（仅边界核对） |
| 2026-08 | **VLCP**（2608.16978） | 仿真 episode 内按失败踪迹改写 Python 控制函数，并测量抓取恢复率 | `[精读原文]` |

---

## 12. 可引用事实清单（每条都带限定，复制即用）

> **用法**：直接引用下列句子时**必须同时保留限定语**。它们都已回一手分册核对（SIMPLER 两条沿用上一轮条目级核对，见第 14 章第 6 点）。

1. RT-2 把机器人动作表示为离散 bin 序号整数（文本 token），与网络规模视觉-语言数据**联合微调**，且**不新增 action 专用参数层**；其真机评测约 **6,000 条轨迹**。`[精读原文]`（[分册 2](papers/2307.15818-rt2.md)）
2. OpenVLA 是 7B 开源 VLA，动作按**每维 256 bin** 离散化，在 **970k** 真机示范上微调，训练约 **21,500 A100-hours / 27 epochs**。`[精读原文]`（[分册 4](papers/2406.09246-openvla.md)）
3. OpenVLA 训练时 DROID 子集的 action token accuracy 持续偏低，最终**在训练最后 1/3 阶段移除 DROID**。`[精读原文]`（[分册 4](papers/2406.09246-openvla.md) §3）
4. π0 的 flow matching 采样为**固定 10 步** Euler 积分，action chunk **H = 50**，时间步采样为 **shifted Beta(1.5, 1) 且 s = 0.999**；on-board 推理 **73 ms**（RTX 4090）。`[精读原文]`（[分册 5](papers/2410.24164-pi0.md)）
5. π0 的推理间隔与频率绑定：**20 Hz 本体每 0.8 s 推理一次（执行 16 步）**，**50 Hz 本体每 0.5 s（执行 25 步）**。`[精读原文]`（[分册 5](papers/2410.24164-pi0.md)）
6. FAST 用频率域变换 + BPE 做动作 tokenization，把 token 数降到**每臂约 30 个**量级；压缩率与训练收益**逐数据集不同（必须带条件）**。`[精读原文]`（[分册 6](papers/2501.09747-fast.md)）
7. Open X-Embodiment 汇集 **1M+ 轨迹 / 22 本体 / 60 数据集 / 34 实验室**；但其**训练侧只用 9 个本体**，真机评测涉及 **6 种机器人 / 3600 trials**。`[精读原文]`（[分册 3](papers/2310.08864-open-x-embodiment.md)）
8. OXE 消融显示：无图像历史时 emergent 从 44.4% 掉到 14.5%；**from scratch（无网页预训练）时 emergent 为 0%**——跨本体数据与互联网预训练是**互补项**。`[精读原文]`（[分册 3](papers/2310.08864-open-x-embodiment.md) Table II）
9. DROID 包含 **76k 轨迹 / 350 小时 / 564 场景 / 52 建筑 / 86 任务**，由 **50 名采集员**在 **12 个月**内用**同一 Franka Panda + 15 Hz 硬件栈（复刻 18 套）**采集，**CC-BY 4.0 开源**。`[精读原文]`（[分册 7](papers/2403.12945-droid.md)）
10. DROID 在**6 个任务、4 个地点**（含真实家庭）的实验中，使其策略的性能与泛化**平均提升 20%**（相对使用既有大规模数据集的先进方法）。`[精读原文]`（[分册 7](papers/2403.12945-droid.md)）
11. SIMPLER 的目标**不是**替代真机评测，而是让策略的**相对性能排序**在仿真中保持相关；原文自述"a simulator will always be an imperfect proxy for the real world"。`[精读原文]`（[分册 8](papers/2405.05941-simpler.md)）
12. Diffusion Policy 在 **15 个任务**（仿真 + 真机）上相对基线的平均提升为 **46.9%**；其扩展版真机含三个双臂任务（Egg Beater / Mat Unrolling / Shirt Folding）。`[精读原文]`（[分册 1](papers/2303.04137-diffusion-policy.md)）

---

## 13. 阅读路径（按目的）

| 你的目的 | 建议路径 |
| :-- | :-- |
| 快速建立判据 | 第 1 章 → [评测专题](topics/evaluation-and-datasets.md) §1 六问 |
| 搞清"动作怎么表示" | 第 2 章 → [动作表征专题](topics/action-representation.md) → 分册 1/2/4/5/6 |
| 评估"能不能部署" | 第 10 章 → [失效边界专题](topics/deployment-boundaries.md) §3 清单 |
| 引用某个成功率数字 | [评测专题](topics/evaluation-and-datasets.md) §1 → 第 12 章可引用事实清单 → 对应分册 |
| 判断某工作归属 | 第 1.2/1.3 节判据与判例 → 第 7 章边界表 |
| 了解选文取舍 | [CANDIDATES.md](sources/CANDIDATES.md) |

---

## 14. 本轮方法学注记（证据是怎么处理的）

1. **先筛选后精读**：`sources/CANDIDATES.md` 分批记录历史候选池 27、闭环控制批次 4、世界模型迁移批次 20；当前累计 **51 = 入选 16 + 排除/边界 35**。**类别性排除项不给 ID**（不编造）。
2. **原文获取**：先查本地缓存 `~/Documents/paper-cache/`，**7 篇命中即用、不重复下载**；仅 DROID（2403.12945）未命中，用 `paper-fetcher` skill 抓取。
3. **文本提取**：`pdftotext -layout` 提取为 txt（版本行、表锚点均可逐字核对）；**txt / PDF 一律不入库**。
4. **等级纪律**：单一主等级；**`[精读原文]` 只授予有分册的 16 篇**（以及已做固定 commit 代码核验的官方仓库）；摘要支撑的**不升格**；未确证的进第 15 章。
5. **推断分离**：每份分册的第 6 问把「论文自承」与「本文推断」分成 6.1 / 6.2；跨文档结论若混合来源，**按最弱等级读**。
6. **闭环批次复核边界**：RECAP 按 arXiv v2 HTML 全文核对；VLCP 与 LingBot-VA 由 PaperFetcher PDF 抽取并对照 arXiv HTML 核验图表、数字与边界。**未做**评测代码复现、统计重算或统一硬件复现实验；图像曲线中未在正文列出的数字不估读。
7. **生成物不改手**：`INDEX.md` / `index/*` / MkDocs nav / `docs/statistics.md` 全部由 `scripts/library_index.py` 产出。
8. **本批次技能证据**：按 `researcher deep` 路径检索至 2026-10-23、通读选中工作并逐篇回答七问；使用 `paper-fetcher` 的 `fetch_paper.py download` 取 VLCP / LingBot-VA 并以 `pdftotext -layout` 抽取。RECAP 的 PDF 下载未完成，故全文改由 arXiv v2 HTML 核读并在分册标明；VersualRL 的真机实验只作任务层边界分析。
9. **世界模型迁移论文批次**：按 `researcher deep` 以“合成示范训练 VLA”“世界模型中的 VLA-RL”“sim-to-real 与策略评测”分线检索；PaperFetcher 使用四组 `search_papers.py` 查询和 `fetch_paper.py batch … --citations` 核对题录及版本入口。五篇选中文章以固定 arXiv HTML 全文核读；没有把 WorldGym/GigaWorld 评测器、DreamZero/Cosmos Policy 直接控制器或普通 3D 仿真 RL 当成同一类训练证据。分册各自保留 4 行亮点、七问、具体原文锚点与 canonical claim-audit 计数；未下载 PDF、未复现训练，也未将作者结果写成独立验证。

---

## 15. 未确证 / 待跟踪

> 以下条目**不写进正文**，仅登记待核对象；核验通过后才可入正文并升格为参考文献。

| 对象 | 当前状态 | 后续动作 |
| :-- | :-- | :-- |
| π0.7 的 arXiv / 技术报告 | 仅有官方博客（2026-04-16），**未找到 arXiv 条目** | 持续跟踪官方渠道；找到后核对是否与 π*0.6 为同系列 |
| 同条件跨方法比较世界模型训练路线 | **未确证**：本轮找到合成示范、视频模型生成轨迹与 imagined RL 的直接真机证据，但模型角色、预训练数据、真实交互预算与指标不同 | 按[迁移专题](topics/world-model-to-vla-transfer.md)继续收敛同 backbone / 同任务 / 同交互预算的可比实验 |
| 代码仓库中 `gr00t/model/gr00t_n1.py`（N1 论文对应实现） | 默认分支已演进为 `gr00t_n1d7/`，**旧路径 404** | 如需对齐 N1 论文，应取发布 tag 或历史 commit |
| π0-FAST 在 GR00T / 其他系统的采用情况 | 未核验 | 检索官方仓库引用 |
| 跨任务通用的 VLA 安全 / 失败恢复协议 | **本轮检索范围内仍未确证**；已有 episode 内恢复、跨 episode 策略学习与任务级 BT 改写的局部证据（见[闭环控制专题](topics/closed-loop-control.md)），不能据此推断通用协议不存在 | 继续专项检索，保持各自平台和指标边界 |
| **DROID 小时数口径冲突** | DROID 原文 **350 h** vs GR00T N1 数据表 **428.3 h / 23.1M 帧**，**未裁决** | 回两篇原文对比计数口径 |
| SIMPLER 的内部口径不一致（Table I "Drawer" vs Fig. 6） | **未裁决**（见分册 8 §9） | 回原文逐表核对 |
| 各系统自报成功率、延迟、数据规模的**具体数值** | 16 篇精读对象**已入分册**；未精读对象**一律不引用** | 引用时带条件 |
| 「自动驾驶是否算 VLA」 | 语言条件化不满足时按 R2 排除，**判定未定稿** | 回一手文献定判定细则 |
| 三类动作头的延迟—成功率共基准曲线 | **未确证**（无第三方横评） | 检索或自建同基准消融 |

---

## 参考文献

> 体例：编号 + 标题 + 一手来源链接 + **单一主等级**（括号内为来源类型）+ 归属章节。
> **当前文献条目共 58 条**：`[精读原文]` **21 条**（16 篇分册论文 + 5 个已在分册内做固定 commit 代码核验的官方仓库）+ `[摘要级]` **35 条** + `[受限核验]` **2 条** + `[二手]` **0 条**（21 + 35 + 2 = 58）。
> **口径变化**：原有基础批次含 8 篇分册论文与 5 个固定 commit 仓库；后续新增 RECAP、VLCP、LingBot-VA，再新增本报告列示的五篇世界模型迁移精读，并登记 VersualRL 为摘要级边界案例（版本与出处见[来源清单](sources/MANIFEST.md)）。凡未设分册的论文一律保持 `[摘要级]`，不因"读过摘要"升格。

**判据与定义（章 1）**

1. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control — [arXiv:2307.15818](https://arxiv.org/abs/2307.15818) — **`[精读原文]`**（[分册](papers/2307.15818-rt2.md)，v1 2023-07-28） — 章 1/2/3
2. RT-1: Robotics Transformer for Real-World Control at Scale — [arXiv:2212.06817](https://arxiv.org/abs/2212.06817)（v2 2022-12-13） — `[摘要级]`（arXiv 摘要 + 官方项目页 https://robotics-transformer1.github.io/） — 章 1/3
3. CLIPort: What and Where Pathways for Robotic Manipulation — [arXiv:2109.12098](https://arxiv.org/abs/2109.12098)（官方项目页 [cliport.github.io](https://cliport.github.io/)） — `[摘要级]`（arXiv 摘要 + 官方项目页） — 章 1.3
4. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion — [arXiv:2303.04137](https://arxiv.org/abs/2303.04137) — **`[精读原文]`**（[分册](papers/2303.04137-diffusion-policy.md)，v5 2024-03-14） — 章 1.3/2/3
5. OpenVLA: An Open-Source Vision-Language-Action Model — [arXiv:2406.09246](https://arxiv.org/abs/2406.09246) — **`[精读原文]`**（[分册](papers/2406.09246-openvla.md)，v3 2024-09-05） — 章 1.3/2/3
6. WorldVLA: Towards Autoregressive Action World Model — [arXiv:2506.21539](https://arxiv.org/abs/2506.21539)（v1 2025-06-26） — `[摘要级]`（arXiv 摘要） — 章 1.3/4.3/7
7. Magma: A Foundation Model for Multimodal AI Agents — [arXiv:2502.13130](https://arxiv.org/abs/2502.13130)（v1 2025-02-18） — `[摘要级]`（arXiv 摘要） — 章 7.3
8. RT-H: Action Hierarchies Using Language — [arXiv:2403.01823](https://arxiv.org/abs/2403.01823)（v2 2024-03-04） — `[摘要级]`（arXiv 摘要） — 章 7.3（待精读）

**动作表征与训练目标（章 2）**

9. π0: A Vision-Language-Action Flow Model for General Robot Control — [arXiv:2410.24164](https://arxiv.org/abs/2410.24164) — **`[精读原文]`**（[分册](papers/2410.24164-pi0.md)，v4 2026-01-08） — 章 2/3
10. FAST: Efficient Action Tokenization for Vision-Language-Action Models — [arXiv:2501.09747](https://arxiv.org/abs/2501.09747) — **`[精读原文]`**（[分册](papers/2501.09747-fast.md)，v1 2025-01-16） — 章 2/3/6
11. RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation — [arXiv:2410.07864](https://arxiv.org/abs/2410.07864)（v2 2024-10-10） — `[摘要级]`（arXiv 摘要 + 官方仓库） — 章 2/3
12. openpi 官方仓库（Physical Intelligence） — [https://github.com/Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi)（固定 commit `215abfb2…`） — **`[精读原文]`**（代码事实，见章 2.3） — 章 2.3
13. openvla 官方仓库 — [https://github.com/openvla/openvla](https://github.com/openvla/openvla)（固定 commit `c8f03f48…`） — **`[精读原文]`**（代码事实） — 章 2.3
14. Isaac-GR00T 官方仓库（NVIDIA） — [https://github.com/NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)（固定 commit `dac54b31…`） — **`[精读原文]`**（代码事实） — 章 2.3/3
15. LeRobot 官方仓库（Hugging Face） — [https://github.com/huggingface/lerobot](https://github.com/huggingface/lerobot)（固定 commit `297774fc…`） — **`[精读原文]`**（代码事实） — 章 2.3
16. RoboticsDiffusionTransformer 官方仓库（RDT-1B） — [https://github.com/thu-ml/RoboticsDiffusionTransformer](https://github.com/thu-ml/RoboticsDiffusionTransformer)（固定 commit `cd79363a…`） — **`[精读原文]`**（代码事实） — 章 2.3
17. PaliGemma: A versatile 3B VLM for transfer — [arXiv:2407.07726](https://arxiv.org/abs/2407.07726)（v2 2024-07-10） — `[摘要级]`（arXiv 摘要） — 章 2.3（π0 主干）
18. Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success（OpenVLA-OFT） — [arXiv:2502.19645](https://arxiv.org/abs/2502.19645)（v2 2025-02-27） — `[摘要级]`（arXiv 摘要 + 官方页 https://openvla-oft.github.io/） — 章 2/5（待精读）

**代表系统（章 3）**

19. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots — [arXiv:2503.14734](https://arxiv.org/abs/2503.14734)（v2 2025-03-27） — `[摘要级]`（arXiv 摘要 + 官方仓库） — 章 3.3
20. π0.5: a Vision-Language-Action Model with Open-World Generalization — [arXiv:2504.16054](https://arxiv.org/abs/2504.16054)（v1 2025-04-22） — `[摘要级]`（arXiv 摘要 + 官方博客） — 章 3.3/5
21. π*0.6: a VLA That Learns From Experience（RECAP） — [arXiv:2511.14759](https://arxiv.org/abs/2511.14759) — **`[精读原文]`**（[分册](papers/2511.14759-pi-star-0.6-recap.md)，v2 2025-11-19） — 章 3.3/8/闭环专题
22. A Steerable Model with Emergent Capabilities（π0.7 官方博客，2026-04-16） — [https://www.physicalintelligence.company/blog/pi07](https://www.physicalintelligence.company/blog/pi07) — `[摘要级]`（官方博客） — 章 3.3（**待跟踪：未找到对应 arXiv 条目**）
23. Octo: An Open-Source Generalist Robot Policy — [arXiv:2405.12213](https://arxiv.org/abs/2405.12213)（v2 2024-05-20） — `[摘要级]`（arXiv 摘要） — 章 3.3
24. TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation — [arXiv:2409.12514](https://arxiv.org/abs/2409.12514)（v5 2024-09-19） — `[摘要级]`（arXiv 摘要） — 章 3.3
25. ALOHA Unleashed: A Simple Recipe for Robot Dexterity — [arXiv:2410.13126](https://arxiv.org/abs/2410.13126)（v1 2024-10-17） — `[摘要级]`（arXiv 摘要） — 章 3.3（待精读）
26. Gemini Robotics: Bringing AI into the Physical World — [arXiv:2503.20020](https://arxiv.org/abs/2503.20020)（v1 2025-03-25） — `[摘要级]`（arXiv 摘要） — 章 3.3（归属待定）
27. OpenVLA 官方项目页 — [https://openvla.github.io/](https://openvla.github.io/) — `[摘要级]`（官方项目页） — 章 3
28. RT-2 官方项目页 — [https://robotics-transformer2.github.io/](https://robotics-transformer2.github.io/) — `[摘要级]`（官方项目页） — 章 3

**数据（章 4）**
29. Open X-Embodiment: Robotic Learning Datasets and RT-X Models — [arXiv:2310.08864](https://arxiv.org/abs/2310.08864) — **`[精读原文]`**（[分册](papers/2310.08864-open-x-embodiment.md)，v9 2025-05-14） — 章 4.1
30. DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset — [arXiv:2403.12945](https://arxiv.org/abs/2403.12945) — **`[精读原文]`**（[分册](papers/2403.12945-droid.md)，v2 2025-04-22） — 章 4.1
31. Open X-Embodiment 官方项目页 — [https://robotics-transformer-x.github.io/](https://robotics-transformer-x.github.io/) — `[摘要级]`（官方项目页） — 章 4.1
32. DROID 官方项目页 — [https://droid-dataset.github.io/](https://droid-dataset.github.io/) — `[摘要级]`（官方项目页） — 章 4.1
33. BridgeData V2 官方项目页 — [https://rail-berkeley.github.io/bridgedata/](https://rail-berkeley.github.io/bridgedata/) — `[摘要级]`（官方项目页） — 章 4.1
34. RH20T 官方项目页 — [https://rh20t.github.io/](https://rh20t.github.io/) — `[摘要级]`（官方项目页） — 章 4.1
35. Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation — [arXiv:2401.02117](https://arxiv.org/abs/2401.02117)（v1 2024-01-04） — `[摘要级]`（arXiv 摘要） — 章 3.3/4.1
36. RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots — [arXiv:2406.02523](https://arxiv.org/abs/2406.02523)（v1 2024-06-04） — `[摘要级]`（arXiv 摘要） — 章 4.2
37. LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning — [arXiv:2306.03310](https://arxiv.org/abs/2306.03310)（v2 2023-06-05） — `[摘要级]`（arXiv 摘要） — 章 4.2/5
38. Isaac Sim 官方页（NVIDIA） — [https://developer.nvidia.com/isaac/sim](https://developer.nvidia.com/isaac/sim) — `[摘要级]`（官方页面） — 章 4.2
39. ManiSkill 官方页 — [https://maniskill.ai/](https://maniskill.ai/) — `[摘要级]`（官方页面） — 章 4.2
40. LIBERO 官方项目页 — [https://libero-project.github.io/main.html](https://libero-project.github.io/main.html) — `[摘要级]`（官方项目页） — 章 4.2
41. RoboCasa 官方项目页 — [https://robocasa.ai/](https://robocasa.ai/) — `[摘要级]`（官方项目页） — 章 4.2
42. robosuite 官方页 — [https://robosuite.ai/](https://robosuite.ai/) — `[摘要级]`（官方页面） — 章 4.2
43. Humanoid-Gym: Reinforcement Learning for Humanoid Robot with Zero-Shot Sim2Real Transfer — [arXiv:2404.05695](https://arxiv.org/abs/2404.05695)（v2 2024-04-08） — `[摘要级]`（arXiv 摘要；按 R2 排除出 VLA 本体） — 章 4.2

**评测（章 5）**

44. Evaluating Real-World Robot Manipulation Policies in Simulation（SIMPLER） — [arXiv:2405.05941](https://arxiv.org/abs/2405.05941) — **`[精读原文]`**（[分册](papers/2405.05941-simpler.md)，v1 2024-05-09） — 章 5
45. SIMPLER 官方项目页 — [https://simpler-env.github.io/](https://simpler-env.github.io/) — `[摘要级]`（官方项目页） — 章 5

**世界模型作为训练环境 / 交叉引用（章 4.3、7）**

46. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning — [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) — `[摘要级]`（arXiv 摘要） — 章 4.3/7
47. Training Agents Inside of Scalable World Models（Dreamer 4） — [arXiv:2509.24527](https://arxiv.org/abs/2509.24527) — `[摘要级]`（arXiv 摘要） — 章 4.3/7
48. Cosmos World Foundation Model Platform for Physical AI — [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) — `[摘要级]`（arXiv 摘要） — 章 4.3/7

**综述与背景（章 1、8；`[受限核验]`）**

49. Vision-Language-Action (VLA) Models: Concepts, Progress, Applications and Challenges — [arXiv:2505.04769](https://arxiv.org/abs/2505.04769)（v2 2025-05-07） — `[受限核验]`（arXiv 条目已核验题名/版本/日期，**正文未读**；综述类，**不作为事实来源**） — 章 1/8
50. What Matters in Building Vision-Language-Action Models for Generalist Robots — [arXiv:2412.14058](https://arxiv.org/abs/2412.14058)（v4 2024-12-18） — `[受限核验]`（arXiv 条目已核验，**正文未读**；其结论属对他人系统的二次比较，**不作事实来源**） — 章 2/8
51. VLCP: Vision Language Control Policy Closed-Loop Code Replanning for Robot Manipulation — [arXiv:2608.16978](https://arxiv.org/abs/2608.16978) — **`[精读原文]`**（[分册](papers/2608.16978-vlcp.md)，v1 2026-08-17） — 章 3.3/闭环专题
52. Causal World Modeling for Robot Control（LingBot-VA） — [arXiv:2601.21998](https://arxiv.org/abs/2601.21998) — **`[精读原文]`**（[分册](papers/2601.21998-lingbot-va.md)，v2 2026-03-22） — 章 3.3/4/闭环专题
53. VersualRL: Closed-Loop Verbal Reinforcement Learning with Visual Execution Feedback for Task-Level Robot Planning — [arXiv:2603.22169](https://arxiv.org/abs/2603.22169) — `[摘要级]`（v3 2026-07-19；本轮仅核对其定位与实机设置；主张留在闭环专题的边界段） — 闭环专题
54. SimVLA: Zero-Shot Sim-to-Real VLA Learning for Mobile Manipulation — [arXiv:2610.11248](https://arxiv.org/abs/2610.11248) — **`[精读原文]`**（[分册](papers/2610.11248-simvla.md)，v1 2026-10-08） — 世界模型迁移专题
55. Grounded-Dreamer: Robot Learning from World Model Synthetic Data with Physical Grounding — [arXiv:2610.13164](https://arxiv.org/abs/2610.13164) — **`[精读原文]`**（[分册](papers/2610.13164-grounded-dreamer.md)，v1 2026-10-09） — 世界模型迁移专题
56. VLAW: Iterative Co-Improvement of Vision-Language-Action Policy and World Model — [arXiv:2602.12063](https://arxiv.org/abs/2602.12063) — **`[精读原文]`**（[分册](papers/2602.12063-vlaw.md)，v2 2026-02-15） — 世界模型迁移专题
57. World-VLA-Loop: Closed-Loop Learning of Video World Model and VLA Policy — [arXiv:2602.06508](https://arxiv.org/abs/2602.06508) — **`[精读原文]`**（[分册](papers/2602.06508-world-vla-loop.md)，v2 2026-05-25） — 世界模型迁移专题
58. WoVR: World Models as Reliable Simulators for Post-Training VLA Policies with RL — [arXiv:2602.13977](https://arxiv.org/abs/2602.13977) — **`[精读原文]`**（[分册](papers/2602.13977-wovr.md)，v2 2026-06-27） — 世界模型迁移专题

> **`[受限核验]` 的用法**：这两条的**题名、版本与日期已确证**（可作检索线索与术语定位），但**正文未读**，因此其**任何转述性结论都不得作为本报告的事实依据**。

---

## 链接核验清单

> 完整链接清单核验时间：2026-10-17。2026-10-23 补核了 RECAP、VLCP、LingBot-VA 与 VersualRL 四个 arXiv ID 的当前题名、版本、日期及链接；本次未重跑原有全库链接扫描。代码类条目仍仅对其列出的固定 commit 成立。

| 类别 | 条数 / 链接数 | 结果 |
| :-- | --: | :-- |
| arXiv 链接（Atom API / 页面核对编号、题名、日期） | 历史核验 36 条 + 本次新增 4 个 ID | 旧清单全部通过；本次新增 4 个 ID 全部与题名/版本匹配 |
| GitHub 官方仓库（状态码 200 + 仓库标题） | 5 条 / 5 链接 | 全部 200 |
| 官方项目页 / 官方页（状态码 200 + 标题） | 9 条 / 9 链接 | 全部 200 |
| 官方博客（状态码 200 + 标题 + 页内日期） | 3 条 / 3 链接 | 全部 200 |
| **本次新增** | RECAP、VLCP、LingBot-VA、VersualRL 的 4 个 arXiv 页面 | 当前页面可访问，题名与编号匹配；全库链接检查未重跑 |

**未确证 / 已剔除（不进正文）**

| 对象 | 结果 | 处置 |
| :-- | :-- | :-- |
| `github.com/NVlabs/GR00T-N1` | **404** | 剔除；NVIDIA 官方仓库实为 `github.com/NVIDIA/Isaac-GR00T`（已核验 200） |
| `openvla-oft` 旧项目页路径变体 | **404** | 改用 `https://openvla-oft.github.io/`（200） |
| `physicalintelligence.company/blog/pi06`、`/research/recap` | **404** | 改用正确路径 `/blog/pistar06`（200） |
| π0.7 arXiv 编号 | 未找到 | 列入「未确证 / 待跟踪」 |
| GR00T N1 旧代码路径 `gr00t/model/gr00t_n1.py` | **404**（默认分支已演进） | 需取发布 tag / 历史 commit；列入待跟踪 |

**代码事实核验表（固定 commit）**

| 仓库 | commit | 核验文件 | 结果 |
| :-- | :-- | :-- | :-- |
| openvla/openvla | `c8f03f48af692657d3060c19588038c7220e9af9` | `prismatic/extern/hf/modeling_prismatic.py` | 200，行号已记录（第 2.3 节） |
| Physical-Intelligence/openpi | `215abfb217dbac7d5f1273282331b9b1866c0479` | `src/openpi/models/pi0.py`、`pi0_fast.py`、`tokenizer.py` | 200，行号已记录 |
| NVIDIA/Isaac-GR00T | `dac54b313160c201c450f97df0fd74ebd379c892` | `gr00t/model/gr00t_n1d7/gr00t_n1d7.py`、`gr00t/model/modules/dit.py` | 200，行号已记录 |
| thu-ml/RoboticsDiffusionTransformer | `cd79363a1387e8f81c7724d070ef7e45fd23150f` | `models/rdt_runner.py`、`models/rdt/model.py` | 200，行号已记录 |
| huggingface/lerobot | `297774fca4e3ad0aa34e7425fbf937111637e77b` | `src/lerobot/policies/diffusion/modeling_diffusion.py` | 200，行号已记录 |

> 说明：`commit` 为 2026-10-16 抓取时的默认分支 HEAD；代码事实**只对上述 commit 成立**，仓库后续演进不保证一致。所有行号均为该 commit 下的真实行号。

---

*截至 2026-10-23：16 篇分册（`papers/`，均 `[精读原文]`）+ 5 篇横切专题（`topics/`）+ 选文与来源清单（`sources/`）。证据按单一主等级标注；未确证项集中在第 15 章。*
