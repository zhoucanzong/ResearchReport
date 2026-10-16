# EmbodiedVLA 技术专题调研

> **声明**：本报告由 AI Agent 自动调研生成，未经官方确认；引用具体参数、日期或 benchmark 前请回溯原始来源。
> **调研日期**：2026-10-16（第一轮：**骨架**——各章给出可判定的结论与已核验来源，未做逐篇正文精读）。
> **定位**：EmbodiedVLA（Vision-Language-Action）指**以自然语言指令 + 视觉观测为输入、直接输出机器人动作信号的可部署策略模型**；本专题为其判据、动作表征架构谱系、代表系统、数据、评测与应用边界建立框架与证据索引。**世界模型作为 VLA 的训练环境**是本专题与 `WorldModels` 的核心交叉点（见第 7 章）。

**证据等级约定（单一主等级）**：`[精读原文]` 已通读一手正文；`[摘要级]` 仅核验官方摘要 / 官方页面 / 项目页（题名、作者、日期、摘要断言），**未通读正文，细节不得当作已成立事实**；`[二手]` 第三方转述；`[受限核验]` 一手对象无法直接抓取，只能经镜像 / API 间接确证。每条只给**一个主等级**；来源类型写在括号内（arXiv 摘要 / 官方项目页 / 官方仓库 / 官方博客）。本报告代码类证据一律写成 `仓库@commit:文件:行`，并按第 2.3 节区分**代码事实**与**研究推断**。

---

## 0. 本章结论

1. **术语尚无公认定义**，本专题取可判定的操作性判据：`(a) 视觉输入` + `(b) 自然语言指令条件化` + `(c) 直接输出动作信号` 三条**同时满足**才算 VLA；"是否由网络规模 VLM 初始化"作为**强弱标注**而非准入门槛。`[摘要级]`（arXiv 摘要 + 官方项目页，见参考文献 1–11）
2. **动作表征（action representation）是 VLA 架构分化的主轴**，当前并行三条路线：**token（离散 / 自回归）**、**flow matching（连续、向量场回归）**、**diffusion head（连续、逐步去噪）**；代表分别是 RT-2 / OpenVLA / π0-FAST、π0 / GR00T N1、Diffusion Policy / RDT-1B。`[摘要级]` + 代码事实（第 2.3 节）
3. **同一模型常同时提供两条路线**：π0 官方仓库同时给出 flow matching 头（`pi0`）与 FAST tokenizer 自回归头（`pi0_fast`），说明"路线之争"在工程上首先是**延迟 / 精度 / 复用性**的取舍，而非互斥范式。`[摘要级]` + 代码事实（第 2.5 节）
4. **真机数据与仿真数据不可互相替代**：前者是 VLA 预训练的语义与灵巧度来源（Open X-Embodiment、DROID 等），后者是规模化与可复现评测的来源（Isaac Sim / ManiSkill / RoboCasa / LIBERO 等）。`[摘要级]`
5. **评测是当前最大瓶颈**：真机成功率是事实标准但不具可复现性；仿真基准可复现但保真度受限。SIMPLER 主张 sim-real 强相关，而 π0.5 指出仿真表现好的策略在真机泛化仍差——**仿真分数不能直接替代真机结论**。`[摘要级]`
6. **与相邻领域边界**：VLA 是**策略**，VLM 是**输入侧模型**，Agent 是**外层决策循环**，WorldModels 产出的是**环境/状态转移**而非动作；联合模型（WorldVLA 一类）按"交付物"拆分归属，避免重复劳动（第 7 章与 `WorldModels` 章 6/7 显式互引）。`[摘要级]`（arXiv 摘要）

> 本轮为骨架：上述结论均为 `[摘要级]` 或代码事实，**尚无 `[精读原文]` 支撑**；第二轮精读后需逐条升级或推翻。

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

### 1.3 判例（至少 4 例，走通判据）

| 判例 | (a) 视觉 | (b) 语言 | (c) 动作 | 归属与理由 |
| :-- | :-- | :-- | :-- | :-- |
| **CLIPort**（2021） | ✓ | ✓ 语言 grounding | ✗ 输出拾放**动作基元序列**，非可直接执行的动作信号 | **不入 VLA**（R2 邻域）：语言条件化 + 技能组合，争议点被本判据明确排除 |
| **Diffusion Policy**（2023） | ✓ | ✗ 论文任务为视觉运动策略，非语言指令条件 | ✓ 输出连续动作序列（动作 chunk） | **不入 VLA**（R2）：diffusion head 是 VLA 的**动作头技术**，不是 VLA 定义 |
| **RT-1**（2022） | ✓ | ✓ | ✓ 离散动作 token | **入 VLA**，但属**弱 VLA**（R3）：视觉-语言塔非网络规模 VLM 初始化 |
| **RT-2**（2023） | ✓ | ✓ | ✓ 动作**表示为文本 token** | **入 VLA（范式确立点）**：网页规模 VLM 与机器人轨迹**联合微调** |
| **OpenVLA**（2024） | ✓ | ✓ | ✓ 每维 256 bin 的离散动作 token | **入 VLA（强，开源）**：验证了开源 VLM 主干 + 离散动作 token 的完整路线 |
| **π0 / π0-FAST**（2024–2025） | ✓ | ✓ | ✓ flow matching 连续动作 chunk（π0）／FAST token（π0-FAST） | **入 VLA（强）**：同一主干两条动作表征路线 |
| **GR00T N1**（2025） | ✓ | ✓ | ✓ 扩散 transformer（DiT）动作专家 | **入 VLA（强）**：双系统（System 2 VLM + System 1 动作专家） |
| **WorldVLA**（2025） | ✓ | ✓ | ✓ 动作 + 未来帧预测 | **按交付物拆分**（R5）：动作分支 → 本专题；world 分支 → `WorldModels` |
| **MuJoCo / Isaac Sim** | — | — | — | **不入本专题**（R6）：规则模拟器，仅作评测 / 数据环境 |

### 1.4 本章待办

- (b) 的"语言条件化"需可操作阈值（语言**实际影响**动作 vs 语言仅作任务标签）：留待第二轮；
- "轻量动作解码器"的边界（如把 latent action 解码为动作）需给出判定案例；
- 判据 1、3 与 R3 的措辞需回到 RT-1 / RT-2 一手正文核对。

---

## 2. 架构谱系：动作表征三条路线

**本章要回答**：三种动作表征（token / flow matching / diffusion head）各自的训练目标、推理代价、代表系统是什么？为什么同一主干会同时提供多条路线？

### 2.1 路线总览

| 路线 | 动作空间 | 训练目标 | 推理形态 | 代表系统（证据） |
| :-- | :-- | :-- | :-- | :-- |
| **token（离散 / 自回归）** | 离散 token 序列 | 与语言模型同源的 next-token 交叉熵 | 自回归解码，token 数 = 动作维 × 步数（或 FAST 压缩后更少） | RT-2、OpenVLA、π0-FAST |
| **flow matching（连续）** | 连续 action chunk | 向量场 / 速度回归（噪声与目标线性插值） | 少数步（π0 官方默认 10 步）数值积分 | π0、GR00T N1 的 System 1 |
| **diffusion head（连续）** | 连续 action chunk | 去噪目标（DDPM 式） | 多步迭代去噪（可用 DPM-Solver 等加速） | Diffusion Policy、RDT-1B |

### 2.2 token 路线

- **动作作为文本 token**：RT-2 把动作写成文本 token 并入训练集，与网络规模视觉-语言任务**联合微调**（co-fine-tuning）。`[摘要级]`（arXiv 摘要，参考文献 2）
- **每维分箱离散化**：OpenVLA 沿用 7B 开源 VLM 主干 + **每动作维 256 bin** 的离散 token 化；官方 README 明确其相对 vanilla 基线是 "256-bin action discretization"，并推荐 FAST 作为压缩替代。`[摘要级]`（官方仓库 README）+ 代码事实（2.3 节）
- **FAST tokenizer**：解决"逐维逐时刻分箱在高频灵巧数据上表现差"的问题，用频率域变换压缩动作 chunk，`fast_tokenizer_path` 默认从 HF Hub 拉 `physical-intelligence/fast`。`[摘要级]`（arXiv 摘要 + 官方仓库代码）

### 2.3 代码事实核验（file:line）

> **口径**：下列为**代码事实**（对固定 commit 的源码读数），**不等于论文方法**；与论文表述冲突时以论文为准并另行标注。**研究推断**单独标 `[推断]`。

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

**研究推断** `[推断]`：token 路线的推理延迟随"动作维 × 步数"线性增长，故 **FAST 一类压缩 tokenizer 是 token 路线能否用于高频灵巧任务的先决条件**；flow matching 与 diffusion head 的取舍主要在**步数与稳定性**（π0 代码默认 10 步 vs Diffusion Policy 典型 100 步训练 / 多步采样），此推断需以论文消融表核对。

### 2.4 路线分界的可判定表述

- 动作是**离散符号**、由语言模型头直接生成 → **token 路线**；
- 动作是**连续向量**、由回归"噪声→目标"的向量场得到 → **flow matching**（线性插值目标，π0 代码形态）；
- 动作是**连续向量**、由逐步去噪（DDPM/DDIM/DPM-Solver）得到 → **diffusion head**。

### 2.5 本章待办

- GR00T N1 论文（DiT 动作专家）与 GR00T N1.7 代码（`AlternateVLDiT`）的差异需显式对齐，避免把新代码形态当作 N1 论文方法；
- 需补：三类动作头在同一基准上的**延迟 / 成功率对照实验**（当前只有各系统自报数据）；
- 需精读 π0 / FAST 正文以确认 token 压缩率与推理加速倍数的具体口径。

---

## 3. 代表系统逐案

**本章要回答**：RT-2、π0、OpenVLA、GR00T 四个系统各自的判据落位、动作表征、一手来源与关键结论是什么？

| 系统 | 判据落位 | 动作表征 | 关键结论（均来自一手来源） | 证据 |
| :-- | :-- | :-- | :-- | :-- |
| **RT-2**（Google DeepMind，2023-07-28） | 强 VLA（网络规模 VLM 联合微调） | **文本 token** | 把动作表达为文本 token，与网络规模视觉-语言任务**co-fine-tune**；目标是把网页知识与新兴语义推理带入端到端机器人控制 | `[摘要级]`（arXiv:2307.15818 摘要 + 官方项目页 robotics-transformer2.github.io） |
| **π0**（Physical Intelligence，2024-10-31 / v 更新至 2026-01-08） | 强 VLA | **flow matching** 连续动作 chunk | 在预训练 VLM 之上构建 **flow matching 架构**，以继承互联网规模语义知识；面向多平台高灵巧任务 | `[摘要级]`（arXiv:2410.24164 摘要 + 官方博客 "Our First Generalist Policy"） |
| **OpenVLA**（Stanford 等，2024-06-13） | 强 VLA，**开源** | **离散 token（每维 256 bin）** | 7B 开源 VLA，训练于 **970k 真机示范**；动机之一是既有 VLA 大多闭源且缺少高效微调方法 | `[摘要级]`（arXiv:2406.09246 摘要 + 官方项目页 openvla.github.io + 官方仓库） |
| **GR00T N1**（NVIDIA，2025-03-18） | 强 VLA，**人形** | **扩散 transformer（DiT）动作专家** | **双系统**：视觉-语言模块 System 2 理解环境与指令，扩散 transformer System 1 实时生成电机动作；两模块紧耦合并**联合端到端训练** | `[摘要级]`（arXiv:2503.14734 摘要 + 官方仓库 NVIDIA/Isaac-GR00T） |

**同族与相邻系统（本轮仅登记，未精读）**：

| 系统 | 一句话定位 | 证据 |
| :-- | :-- | :-- |
| RT-1 (2022) | VLA 前置形态：无网络规模 VLM 初始化的语言条件化机器人 Transformer | `[摘要级]`（arXiv:2212.06817 + 官方项目页） |
| Octo (2024) | 开源通用机器人策略（非网络规模 VLM 主干） | `[摘要级]`（arXiv:2405.12213） |
| π0-FAST / FAST (2025) | 频率域动作 tokenizer，可插到自回归 VLA 上 | `[摘要级]`（arXiv:2501.09747 + 官方页 physicalintelligence.company/research/fast） |
| π0.5 (2025-04-22) | 异构任务**协同训练**支持开放世界泛化（多机器人 + 高层语义 + 网页数据） | `[摘要级]`（arXiv:2504.16054 摘要 + 官方博客 "A VLA with Open-World Generalization"） |
| π*0.6 / RECAP (2025-11-18) | 用 **advantage conditioning** 做真机 RL，把部署经历、纠正与示范混合进自改进循环 | `[摘要级]`（arXiv:2511.14759 摘要 + 官方博客 "A VLA that Learns from Experience"） |
| π0.7 (2026-04-16) | 官方博客称"可引导（steerable）模型 + 涌现能力"的机器人基础模型；**本轮未找到对应 arXiv 条目** | `[摘要级]`（官方博客 "A Steerable Model with Emergent Capabilities"）；**待跟踪** |
| RDT-1B (2024-10-10) | 双臂操作的 **diffusion** 基础模型（1B 级，非网络规模 VLM） | `[摘要级]`（arXiv:2410.07864 + 官方仓库） |
| TinyVLA (2024-09-19) | 快速、数据高效的轻量 VLA | `[摘要级]`（arXiv:2409.12514） |
| Mobile ALOHA (2024-01-04) | 低成本全身遥操作 + 双臂移动操作（数据侧，非 VLA 本体） | `[摘要级]`（arXiv:2401.02117） |

> **口径提醒**：上表"关键结论"全部取自**摘要/官方页面断言**，未经正文复核；论文中的具体成功率、对比基线、硬件配置**一律不得据本报告引用**。

**本章待办**：四案逐一精读正文，核对动作表征、训练数据规模、评测协议与自报成功率；补充 π0.5 / π*0.6 / π0.7 是否为同一系统的迭代（需回一手正文，**不得据博客标题推断**）。

---

## 4. 数据：真机与仿真

**本章要回答**：真机数据与仿真数据各自提供什么、边界在哪？世界模型作为训练环境处于什么位置？

### 4.1 真机数据（一线来源）

| 数据集 / 平台 | 规模与要点 | 证据 |
| :-- | :-- | :-- |
| **Open X-Embodiment** | 面向"跨机器人（X-robot）通用策略"的**标准化数据格式 + 数据集 + RT-X 模型**；其官方页与论文题名一致（"Robotic Learning Datasets and RT-X Models"） | `[摘要级]`（arXiv:2310.08864 摘要 + 官方页 robotics-transformer-x.github.io） |
| **OpenVLA 训练数据** | 970k 真机示范（论文摘要自报） | `[摘要级]`（arXiv:2406.09246 摘要） |
| **DROID** | 大规模"in-the-wild"机器人操作数据集，含多场景多任务 | `[摘要级]`（官方页 droid-dataset.github.io） |
| **BridgeData V2** | 面向可扩展机器人学习的多环境操作数据集 | `[摘要级]`（官方页 rail-berkeley.github.io/bridgedata） |
| **RH20T** | 面向多样技能学习的综合机器人数据集 | `[摘要级]`（官方页 rh20t.github.io） |
| **Mobile ALOHA** | 低成本全身遥操作采集双臂移动操作数据 | `[摘要级]`（arXiv:2401.02117） |

### 4.2 仿真平台（评测 / 合成数据）

| 平台 | 定位 | 证据 |
| :-- | :-- | :-- |
| **MuJoCo** | 规则物理引擎（本专题不视为世界模型，见第 7 章 R6） | `[摘要级]`（规则模拟器通识，本轮未单列条目） |
| **Isaac Sim** | NVIDIA 机器人仿真与合成数据生成平台 | `[摘要级]`（官方页 developer.nvidia.com/isaac/sim） |
| **ManiSkill** | 操作技能仿真 / 基准平台 | `[摘要级]`（官方页 maniskill.ai） |
| **LIBERO** | 面向**终身机器人学习**的操作基准（5 类研究主题） | `[摘要级]`（arXiv:2306.03310 摘要 + 官方页 libero-project.github.io） |
| **RoboCasa** | 日常场景（厨房为主）大规模仿真，含数千 3D 资产 / 150+ 物体类别 | `[摘要级]`（arXiv:2406.02523 摘要 + 官方页 robocasa.ai） |
| **SIMPLER** | 用"控制 + 视觉差异缓解"构建真机对应仿真环境，做 sim-real 成对评测 | `[摘要级]`（arXiv:2405.05941 摘要 + 官方页 simpler-env.github.io） |

### 4.3 世界模型作为训练环境（与 `WorldModels` 的接口）

- **接口定义**：世界模型在本专题中**不作为 VLA 本体**，而作为三类资源：①**合成训练数据**（生成轨迹 / 观测）；②**可交互练习环境**（策略在学得的环境里做 RL / 规划）；③**评测环境**（在与真机对齐的想象环境中打分）。
- **已核验的一手接口对象**：
  - V-JEPA 2 官方摘要称其视频模型可支持 **understanding / prediction / planning**（planning = 用世界模型做动作规划，接口②的范式来源）。`[摘要级]`（arXiv:2506.09985）
  - Dreamer 4 官方摘要题为 "Training Agents Inside of Scalable World Models"，即在**可扩展世界模型内部训练 agent**（接口①②的直接案例）。`[摘要级]`（arXiv:2509.24527）
  - Cosmos World Foundation Model Platform 定位为 Physical AI 的**世界基础模型平台**（接口①的工业化形态）。`[摘要级]`（arXiv:2501.03575）
  - **WorldVLA** 为"自回归动作世界模型"，同时涉及动作与未来帧（接口①②）。`[摘要级]`（arXiv:2506.21539）
- **归属规则**：上述四条**全部归属 `WorldModels`**（该条目参考文献 9/10/16/36），本专题只登记"可被 VLA 消费"的接口，**不重复展开其架构与评测**（避免重复劳动，见第 7 章）。

**本章待办**：补真机数据集的实际许可与可下载性核对；补"世界模型合成数据是否真的提升真机成功率"的对照实验证据（当前未确证，列入第 8 章）；`WorldModels` 章 4/6 的对应章节需双向互引定稿。

---

## 5. 评测

**本章要回答**：真机成功率与仿真基准能否相互替代？差异来源与可比性边界是什么？

- **真机评测**：指标以任务成功率 / 吞吐为主，是事实标准；缺陷是**不可复现**（场景、初始条件、物体摆放、机器人本体差异大）。
- **仿真评测**：可复现、可大规模并行，缺陷是**保真度受限**。SIMPLER 的明确立场是：不必做全保真数字孪生，只需缓解**控制差异与视觉差异**，并报告了 sim-real **成对评测的强相关**。`[摘要级]`（arXiv:2405.05941 摘要）
- **反方证据（同为一手）**：π0.5 以真机开放世界泛化为目标，说明"在仿真中表现好的策略在真机泛化上仍然不够"，即**仿真分数不足以替代真机结论**。`[摘要级]`（arXiv:2504.16054 摘要）
- **LIBERO 的定位**：面向**终身学习**（知识迁移）的基准，评估维度是任务间迁移而非单一真机成功率，**与其他基准不可直接比较**。`[摘要级]`（arXiv:2306.03310 摘要）
- **可比性规则（本专题约定）**：
  1. 不同基准的分数**不得横向比较**，除非明确说明本体、观测、动作空间与评测协议一致；
  2. 引用任一 VLA 成功率必须同时给出**基准 / 本体 / 评测协议**三要素；
  3. 仿真结果只能作为**相对排序**参考，不能作为真机绝对性能的代理。

**本章待办**：需精读 SIMPLER 正文以核对相关系数的具体口径与样本量（当前只有摘要级"强相关"表述，**不得引用具体数值**）；需补齐真机评测的标准报告项清单（建议第二轮形成模板）。

---

## 6. 应用域

| 应用域 | 判据落位要点 | 当前证据 |
| :-- | :-- | :-- |
| **固定工位机械臂 / 抓取装配** | 语言条件化 + 高精度动作；数据以真机示范为主 | `[摘要级]`（RT-1/RT-2、OpenVLA 的评测形态） |
| **双臂 / 灵巧操作** | 动作频率高、维数高，**token 路线压力最大**（FAST 的直接动机） | `[摘要级]`（arXiv:2501.09747 摘要指出逐维逐时刻分箱在高频灵巧数据上表现差） |
| **移动操作 / 家务开放世界** | 需要跨场景泛化与长时程任务分解，依赖异构数据协同训练 | `[摘要级]`（π0.5 摘要；Mobile ALOHA 数据侧） |
| **人形机器人** | 全身动作，双系统分工（慢思考 + 快动作） | `[摘要级]`（GR00T N1 摘要） |
| **自动驾驶** | 语言指令条件化弱、评测在仿真世界模型中闭环 | `[摘要级]`（本专题**不展开**：GAIA-1/2、Vista 属 `WorldModels` 章 6） |

**本章待办**：每域补 1 个可核验的一手评测案例；明确"自动驾驶是否算 VLA"的判定（语言条件化不满足时按 R2 排除）。

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
| **规则模拟器** | 环境（硬编码动力学） | 不满足 WorldModels 的 (c) | `WorldModels` 章 1.2，本专题仅作评测环境 |

### 7.2 与 `WorldModels` 的显式互引（避免重复劳动）

| 交叉对象 | 在本专题的处理 | 在 WorldModels 条目的处理 |
| :-- | :-- | :-- |
| **π0 类策略本体（action head）** | 本专题第 2、3 章展开 | 该条目章 1.3 已判定："**Embodied**，不因「用了世界模型」改判"——**本轮互引确认，不再重复展开** |
| **WorldVLA** | 只登记动作分支（本报告参考文献 45） | 该条目参考文献 36 / 章 7 负责 world 分支 |
| **V-JEPA 2 / V-JEPA 2-AC** | 本专题第 4.3 节只登记"作为训练/规划环境"的接口 | 该条目参考文献 9 / 章 2、4 负责模型与规划机制 |
| **Dreamer 4** | 接口②③的案例 | 该条目参考文献 10 / 章 2、4 |
| **Cosmos WFM** | 接口①的工业化形态 | 该条目参考文献 16 / 章 2、4 |
| **Genie / GameNGen 等交互式世界模型** | **不在本专题出现**（无动作策略交付物） | `WorldModels` 章 2、4 |
| **仿真平台（Isaac Sim / ManiSkill / RoboCasa / LIBERO / SIMPLER）** | 本专题第 4.2、5 章按"评测环境"引用 | 该条目章 1.2 已将规则模拟器排除出 WorldModels，仅作评测环境/数据来源——**口径一致** |
| **自动驾驶世界模型（GAIA-1/2、Vista）** | 本专题仅在第 6 章登记"不展开" | `WorldModels` 章 6 展开 |

> **互引落点（精确到章）**：本报告章 1.3 / 4.3 / 7.1 ↔ `WorldModels` 章 1.3 / 1.2 / 7。两侧口径若冲突，**以"交付物判定"为准**，并在第二轮同步修订。

### 7.3 与 VLM / Agent 的交叉

- **VLM → VLA**：VLA 的"视觉-语言塔"直接复用 VLM（RT-2 联合微调、OpenVLA 开源主干、π0 建于预训练 VLM 之上）——VLM 条目的架构与时序能力是其上游，本专题只处理**动作头与训练目标**的差异。`[摘要级]`
- **VLA vs Agent**：VLA 是**策略**（观测→动作），Agent 是**外层循环**（规划、工具、记忆）。含高层语义子任务预测的 π0.5 处于两者交叠，需在第二轮定判定细则。`[摘要级]`（π0.5 摘要含 "semantic subtask prediction"）
- **具身问答 / 指代**（如 Magma 一类多模态 agent 基础模型）如何归类：当前按 R1 判为**不入 VLA**（其动作侧不带机器人动作信号），是否属"跨 VLM / Agent / VLA 边界案例"待第二轮定稿。`[摘要级]`（arXiv:2502.13130）

---

## 8. 未决问题

1. **定义收敛**：VLA 是否需要"网络规模 VLM 初始化"作为必要条件？RT-1 一类如何表述才不引起误用？（第 1 章待办）
2. **动作表征的量化取舍**：token / flow matching / diffusion head 的**推理延迟—成功率**曲线为何？现有对照均为各系统自报，缺乏同基准横评。（第 2 章）
3. **世界模型是否真的提升 VLA 真机性能**：**本轮未确证任何"用世界模型合成数据训练 VLA 并提升真机成功率"的一手对照实验**，列为待跟踪（第 4.3 章）。
4. **sim-real 相关性是否可复现**：SIMPLER 主张强相关、π0.5 主张真机泛化仍难；两者是否在同一本体 / 同一评测协议下可比，需要精读核对。（第 5 章）
5. **双系统是否为必要架构**：GR00T N1 的 System 2 / System 1 分工是设计选择还是规模必需？（第 3 章）
6. **安全问题**：VLA 的失败恢复、越界动作抑制、人在环路接管缺乏统一判据与报告项（本轮未见专用一手文献，列为待跟踪）。

---

## 参考文献

> 体例：编号 + 标题 + 一手来源链接 + **单一主等级**（括号内为来源类型）+ 归属章节。
> **本轮共 48 条：`[摘要级]` 46 条 + `[受限核验]` 2 条（题名/日期已确证、正文未读的综述，不作为事实来源）+ `[精读原文]` 0 条 + `[二手]` 0 条**（骨架轮未通读正文。计数**仅统计下方 48 条文献**，不含本节开头「证据等级约定」中对四个等级的定义性提及）。其中 **49 个链接全部实测可达**（29 条 arXiv 经 Atom API 比对 + 20 条非 arXiv 经 HTTP 200 与标题确证）；**1 条待跟踪**（参考文献 26 的 π0.7 仅有官方博客、未找到 arXiv 条目）。
> 链接核验方式与结果见文末「链接核验清单」。

**判据与定义（章 1）**

1. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control — [arXiv:2307.15818](https://arxiv.org/abs/2307.15818) — `[摘要级]`（arXiv 摘要） — 章 1/3
2. RT-1: Robotics Transformer for Real-World Control at Scale — [arXiv:2212.06817](https://arxiv.org/abs/2212.06817) — `[摘要级]`（arXiv 摘要 + 官方项目页 https://robotics-transformer1.github.io/） — 章 1/3
3. CLIPort: What and Where Pathways for Robotic Manipulation — [arXiv:2109.12098](https://arxiv.org/abs/2109.12098)（官方项目页 [cliport.github.io](https://cliport.github.io/)） — `[摘要级]`（arXiv 摘要 + 官方项目页） — 章 1.3
4. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion — [arXiv:2303.04137](https://arxiv.org/abs/2303.04137) — `[摘要级]`（arXiv 摘要） — 章 1.3/2
5. OpenVLA: An Open-Source Vision-Language-Action Model — [arXiv:2406.09246](https://arxiv.org/abs/2406.09246) — `[摘要级]`（arXiv 摘要） — 章 1.3/2/3
6. WorldVLA: Towards Autoregressive Action World Model — [arXiv:2506.21539](https://arxiv.org/abs/2506.21539) — `[摘要级]`（arXiv 摘要） — 章 1.3/4.3/7
7. Open X-Embodiment: Robotic Learning Datasets and RT-X Models — [arXiv:2310.08864](https://arxiv.org/abs/2310.08864) — `[摘要级]`（arXiv 摘要） — 章 4.1
8. Octo: An Open-Source Generalist Robot Policy — [arXiv:2405.12213](https://arxiv.org/abs/2405.12213) — `[摘要级]`（arXiv 摘要） — 章 3
9. Magma: A Foundation Model for Multimodal AI Agents — [arXiv:2502.13130](https://arxiv.org/abs/2502.13130) — `[摘要级]`（arXiv 摘要） — 章 7.3
10. TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models — [arXiv:2409.12514](https://arxiv.org/abs/2409.12514) — `[摘要级]`（arXiv 摘要） — 章 3
11. RT-H: Action Hierarchies Using Language — [arXiv:2403.01823](https://arxiv.org/abs/2403.01823) — `[摘要级]`（arXiv 摘要） — 章 7.3（待精读）

**动作表征与训练目标（章 2）**

12. π0: A Vision-Language-Action Flow Model for General Robot Control — [arXiv:2410.24164](https://arxiv.org/abs/2410.24164) — `[摘要级]`（arXiv 摘要 + 官方博客 https://www.physicalintelligence.company/blog/pi0） — 章 2/3
13. FAST: Efficient Action Tokenization for Vision-Language-Action Models — [arXiv:2501.09747](https://arxiv.org/abs/2501.09747) — `[摘要级]`（arXiv 摘要 + 官方页 https://www.physicalintelligence.company/research/fast） — 章 2/3/6
14. RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation — [arXiv:2410.07864](https://arxiv.org/abs/2410.07864) — `[摘要级]`（arXiv 摘要） — 章 2/3
15. openpi 官方仓库（Physical Intelligence） — [https://github.com/Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) — `[摘要级]`（官方仓库） — 章 2.3
16. openvla 官方仓库 — [https://github.com/openvla/openvla](https://github.com/openvla/openvla) — `[摘要级]`（官方仓库） — 章 2.3
17. Isaac-GR00T 官方仓库（NVIDIA） — [https://github.com/NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) — `[摘要级]`（官方仓库） — 章 2.3/3
18. LeRobot 官方仓库（Hugging Face） — [https://github.com/huggingface/lerobot](https://github.com/huggingface/lerobot) — `[摘要级]`（官方仓库） — 章 2.3
19. RoboticsDiffusionTransformer 官方仓库（RDT-1B） — [https://github.com/thu-ml/RoboticsDiffusionTransformer](https://github.com/thu-ml/RoboticsDiffusionTransformer) — `[摘要级]`（官方仓库） — 章 2.3
20. OpenVLA 官方项目页 — [https://openvla.github.io/](https://openvla.github.io/) — `[摘要级]`（官方项目页） — 章 3
21. RT-2 官方项目页 — [https://robotics-transformer2.github.io/](https://robotics-transformer2.github.io/) — `[摘要级]`（官方项目页） — 章 3
22. Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success（OpenVLA-OFT） — [arXiv:2502.19645](https://arxiv.org/abs/2502.19645) — `[摘要级]`（arXiv 摘要 + 官方页 https://openvla-oft.github.io/） — 章 2/5（待精读）

**代表系统（章 3）**

23. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots — [arXiv:2503.14734](https://arxiv.org/abs/2503.14734) — `[摘要级]`（arXiv 摘要） — 章 3
24. π0.5: a Vision-Language-Action Model with Open-World Generalization — [arXiv:2504.16054](https://arxiv.org/abs/2504.16054) — `[摘要级]`（arXiv 摘要 + 官方博客 https://www.physicalintelligence.company/blog/pi05） — 章 3/5/7.3
25. π*0.6: a VLA That Learns From Experience（RECAP） — [arXiv:2511.14759](https://arxiv.org/abs/2511.14759) — `[摘要级]`（arXiv 摘要 + 官方博客 https://www.physicalintelligence.company/blog/pistar06） — 章 3/8
26. A Steerable Model with Emergent Capabilities（π0.7 官方博客，2026-04-16） — [https://www.physicalintelligence.company/blog/pi07](https://www.physicalintelligence.company/blog/pi07) — `[摘要级]`（官方博客） — 章 3（**待跟踪：未找到对应 arXiv 条目**）
27. PaliGemma: A versatile 3B VLM for transfer — [arXiv:2407.07726](https://arxiv.org/abs/2407.07726) — `[摘要级]`（arXiv 摘要） — 章 2.3（π0 主干）
28. ALOHA Unleashed: A Simple Recipe for Robot Dexterity — [arXiv:2410.13126](https://arxiv.org/abs/2410.13126) — `[摘要级]`（arXiv 摘要） — 章 3（待精读）
29. Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation — [arXiv:2401.02117](https://arxiv.org/abs/2401.02117) — `[摘要级]`（arXiv 摘要） — 章 3/4.1

**数据（章 4）**

30. Open X-Embodiment 官方项目页 — [https://robotics-transformer-x.github.io/](https://robotics-transformer-x.github.io/) — `[摘要级]`（官方项目页） — 章 4.1
31. DROID 官方项目页 — [https://droid-dataset.github.io/](https://droid-dataset.github.io/) — `[摘要级]`（官方项目页） — 章 4.1
32. BridgeData V2 官方项目页 — [https://rail-berkeley.github.io/bridgedata/](https://rail-berkeley.github.io/bridgedata/) — `[摘要级]`（官方项目页） — 章 4.1
33. RH20T 官方项目页 — [https://rh20t.github.io/](https://rh20t.github.io/) — `[摘要级]`（官方项目页） — 章 4.1
34. RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots — [arXiv:2406.02523](https://arxiv.org/abs/2406.02523) — `[摘要级]`（arXiv 摘要） — 章 4.2
35. LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning — [arXiv:2306.03310](https://arxiv.org/abs/2306.03310) — `[摘要级]`（arXiv 摘要） — 章 4.2/5
36. Isaac Sim 官方页（NVIDIA） — [https://developer.nvidia.com/isaac/sim](https://developer.nvidia.com/isaac/sim) — `[摘要级]`（官方页面） — 章 4.2
37. ManiSkill 官方页 — [https://maniskill.ai/](https://maniskill.ai/) — `[摘要级]`（官方页面） — 章 4.2
38. LIBERO 官方项目页 — [https://libero-project.github.io/main.html](https://libero-project.github.io/main.html) — `[摘要级]`（官方项目页） — 章 4.2
39. RoboCasa 官方项目页 — [https://robocasa.ai/](https://robocasa.ai/) — `[摘要级]`（官方项目页） — 章 4.2
40. robosuite 官方页 — [https://robosuite.ai/](https://robosuite.ai/) — `[摘要级]`（官方页面） — 章 4.2

**评测（章 5）**

41. Evaluating Real-World Robot Manipulation Policies in Simulation（SIMPLER） — [arXiv:2405.05941](https://arxiv.org/abs/2405.05941) — `[摘要级]`（arXiv 摘要） — 章 5
42. SIMPLER 官方项目页 — [https://simpler-env.github.io/](https://simpler-env.github.io/) — `[摘要级]`（官方项目页） — 章 5

**世界模型作为训练环境 / 交叉引用（章 4.3、7）**

43. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning — [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) — `[摘要级]`（arXiv 摘要） — 章 4.3/7
44. Training Agents Inside of Scalable World Models（Dreamer 4） — [arXiv:2509.24527](https://arxiv.org/abs/2509.24527) — `[摘要级]`（arXiv 摘要） — 章 4.3/7
45. Cosmos World Foundation Model Platform for Physical AI — [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) — `[摘要级]`（arXiv 摘要） — 章 4.3/7
46. Genie: Generative Interactive Environments — [arXiv:2402.15391](https://arxiv.org/abs/2402.15391) — `[摘要级]`（arXiv 摘要） — 章 7.2（**归属 WorldModels，本专题不展开**）

**综述与背景**

47. Vision-Language-Action (VLA) Models: Concepts, Progress, Applications and Challenges — [arXiv:2505.04769](https://arxiv.org/abs/2505.04769) — `[受限核验]`（arXiv 条目已核验题名/日期，正文未读；综述类，**不作为事实来源**） — 章 1/8
48. What Matters in Building Vision-Language-Action Models for Generalist Robots — [arXiv:2412.14058](https://arxiv.org/abs/2412.14058) — `[受限核验]`（arXiv 条目已核验，正文未读） — 章 2/8（待精读）

---

## 未确证 / 待跟踪

> 以下条目**不写进正文**，仅登记待核对象；核验通过后才可入正文并升格为参考文献。

| 对象 | 当前状态 | 后续动作 |
| :-- | :-- | :-- |
| π0.7 的 arXiv / 技术报告 | 仅有官方博客（2026-04-16），**未找到 arXiv 条目** | 持续跟踪官方渠道；找到后核对是否与 π*0.6 为同系列 |
| "世界模型合成数据训练 VLA → 真机成功率提升"的一手对照实验 | **未确证**（Dreamer 4 / V-JEPA 2 面向规划与 agent 训练，非 VLA 真机增益） | 检索 2025–2026 年 sim-to-real 对照文献 |
| 代码仓库中 `gr00t/model` 下 `gr00t_n1.py`（N1 论文对应实现） | 默认分支已演进为 `gr00t_n1d7/`，**旧路径 404** | 如需对齐 N1 论文，应取发布 tag 或历史 commit，而非默认分支 |
| π0-FAST 在 GR00T / 其他系统的采用情况 | 未核验 | 检索官方仓库引用 |
| VLA 安全 / 失败恢复的专用一手文献 | **未检索到** | 专项检索 |
| CLIPort 对应的 arXiv 编号 | ✅ **已确证：arXiv:2109.12098**（题名 `CLIPort: What and Where Pathways for Robotic Manipulation`，2021-09-24），已补入参考文献 3 | 无需再跟踪 |
| 各系统自报成功率、延迟、数据规模的**具体数值** | 未精读正文，**一律不引用** | 第二轮精读时逐个入表 |

---

## 链接核验清单

> 核验时间：2026-10-16。**核验方式**：① arXiv 条目经 `export.arxiv.org/api/query` 逐条比对**编号 ↔ 题名 ↔ 发布日期**（全部 HTTP 200 且题名一致）；② 非 arXiv 条目经 `curl -L` HTTP 状态码 + `<title>` 抓取确证；③ 代码类条目在**固定 commit** 下取原始文件并记录 `文件:行`。

| 类别 | 条数 / 链接数 | 结果 |
| :-- | --: | :-- |
| arXiv 链接（经 Atom API 比对编号/题名/日期） | 文献 **28 条**，对应链接 **29 个**（编号 3 另附官方项目页） | **全部通过**，无编号与题名错配 |
| GitHub 官方仓库（状态码 200 + 仓库标题） | 5 条 / 5 链接 | 全部 200 |
| 官方项目页 / 官方页（状态码 200 + 标题） | 11 条 / 11 链接 | 全部 200 |
| 官方博客（状态码 200 + 标题 + 页内日期） | 4 条 / 4 链接 | 全部 200 |
| **确证合计** | **48 条文献**（29 个 arXiv 链接 + 20 个非 arXiv 链接 = **49 个链接**） | 无失效、无错配 |

**补充回测（第二轮通道）**：对报告内**全部 49 个外部链接**做过一次并发（8 线程）实测，结果 **49/49 HTTP 200**；其中 `https://github.com/openvla/openvla` 曾出现 1 次瞬时 `URLError`，`curl -L` 与 `urllib` 各重试 3 次均 200，判为**网络瞬时抖动、非链接失效**，已记录在此以备复核。

> 说明：本表统计的是**参考文献中实测可达的链接**（49 个）；报告正文中另有两处指向 `physicalintelligence.company` 的官方页面表述（`/research/fast`、`/blog/pi0` 等）已并入上方「官方博客 / 官方页」行，不重复计数。

**逐条状态（摘要）**

| 编号 | 链接 | 方式 | 结果 |
| :-- | :-- | :-- | :-- |
| 1、2、3、4、5、6、7、8、9、10、11、12、13、14、22、23、24、25、27、28、29、34、35、41、43、44、45、46、47、48 | arXiv（见参考文献，共 29 个链接） | Atom API 比对题名 + `published` | **200 / 题名一致** |
| 3（附） | cliport.github.io | HTTP 200 | 标题 = `CLIPort` |
| 15 | github.com/Physical-Intelligence/openpi | HTTP 200 | 标题含 `Physical-Intelligence/openpi` |
| 16 | github.com/openvla/openvla | HTTP 200 | 标题含 `openvla/openvla` |
| 17 | github.com/NVIDIA/Isaac-GR00T | HTTP 200 | 标题 = `NVIDIA Isaac GR00T N1.7 - A Foundation Model for Ge...` |
| 18 | github.com/huggingface/lerobot | HTTP 200 | 标题含 `huggingface/lerobot` |
| 19 | github.com/thu-ml/RoboticsDiffusionTransformer | HTTP 200 | 默认分支解析成功（`HEAD=cd79363…`） |
| 20 | openvla.github.io | HTTP 200 | 标题 = `OpenVLA: An Open-Source Vision-Language-Action Model` |
| 21 | robotics-transformer2.github.io | HTTP 200 | 标题 = `RT-2: Vision-Language-Action Models` |
| 26 | physicalintelligence.company/blog/pi07 | HTTP 200 | 标题 = `A Steerable Model with Emergent Capabilities`，页内日期 2026-04-16 |
| 30 | robotics-transformer-x.github.io | HTTP 200 | 标题 = `Open X-Embodiment: Robotic Learning Datasets and RT-X Models` |
| 31 | droid-dataset.github.io | HTTP 200 | 标题 = `DROID: A Large-Scale In-the-Wild Robot Manipulation Dataset` |
| 32 | rail-berkeley.github.io/bridgedata | HTTP 200 | 标题 = `BridgeData V2` |
| 33 | rh20t.github.io | HTTP 200 | 标题含 `RH20T: A Comprehensive Robotic Dataset` |
| 36 | developer.nvidia.com/isaac/sim | HTTP 200 | 标题 = `Isaac Sim - Robotics Simulation and Synthetic Data Generation` |
| 37 | maniskill.ai | HTTP 200 | 标题 = `ManiSkill` |
| 38 | libero-project.github.io/main.html | HTTP 200 | 标题 = `LIBERO` |
| 39 | robocasa.ai | HTTP 200 | 标题 = `RoboCasa` |
| 40 | robosuite.ai | HTTP 200 | 标题 = `robosuite` |
| 42 | simpler-env.github.io | HTTP 200 | 标题 = `Evaluating Real-World Robot Manipulation Policies in Simulation` |
| （正文引用的官方博客） | physicalintelligence.company/blog/pi0 · /pi05 · /pistar06 | HTTP 200 | 标题分别为 `Our First Generalist Policy`、`A VLA with Open-World Generalization`、`A VLA that Learns from Experience`；页内日期分别为 2025-04-22、2025-04-22、2025-11-17 |
| （正文引用的官方页） | physicalintelligence.company/research/fast | HTTP 200 | 标题 = `FAST: Efficient Robot Action Tokenization` |

**未确证 / 已剔除（不进正文）**

| 对象 | 结果 | 处置 |
| :-- | :-- | :-- |
| `github.com/NVlabs/GR00T-N1` | **404** | 剔除；NVIDIA 官方仓库实为 `github.com/NVIDIA/Isaac-GR00T`（已核验 200） |
| `openvla-oft` 旧项目页路径变体 | **404** | 改用 `https://openvla-oft.github.io/`（200） |
| `physicalintelligence.company/blog/pi06`、`/research/recap` | **404** | 改用正确路径 `/blog/pistar06`（200） |
| `arXiv:2502.13130` 之外的 Magma 类"具身 agent"编号 | 未确证 | 不入正文 |
| π0.7 arXiv 编号 | 未找到 | 列入「未确证 / 待跟踪」 |

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

*本轮为第一轮骨架：各章已给出可判定的结论与已核验来源，但全部结论为 `[摘要级]` 或代码事实，**尚无 `[精读原文]`**；正文精读、数值入表与判据升级留待第二轮。*
