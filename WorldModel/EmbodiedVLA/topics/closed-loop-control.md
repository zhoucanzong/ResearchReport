# 横切专题：机器人闭环控制与 VLA

> **范围**：截至 2026-10-23 的 VLA 运行期反馈与部署后学习。重点是闭环放在哪里、何时更新什么状态，以及仿真/真机证据分别证明了什么。
> **不做排行榜**：不同论文的动作空间、硬件、任务、回合长度和评价指标不可合并成同一成功率排名。

## 0. 先区分四类“闭环”

在机器人论文里，chunk、重规划、学习和世界模型 rollout 常被笼统地叫 feedback loop，但它们控制的对象与时间尺度不同。

| 类别 | 回路跨越的时间尺度 | 真正在更新什么 | 本轮代表 | 证据判断 |
| :-- | :-- | :-- | :-- | :-- |
| **action chunk / receding-horizon feedback** | 一段动作执行完后再取观察、出下一段 | 当前观测上下文与下一段动作 | Diffusion Policy、π0 | 可让 chunk 之间重新观察；若 chunk 内无重推理，chunk 内仍是开环动作执行 |
| **episode 内失败恢复** | 同一任务 episode 的多个控制 block | VLCP 的 Python 控制函数 | VLCP（仿真） | “恢复了失败抓取”是仿真测量；不能据此推断真机效果 |
| **跨 episode 策略学习 / 修订** | 多轮数据收集与训练，或每次 episode 结束后更新 | π*0.6 / RECAP 更新 policy/value 参数；VersualRL 修改符号 BT | RECAP（真实双臂）；VersualRL（真实移动机器人、任务层） | RECAP 有真机策略吞吐与失败数据；VersualRL 的 BT 更新不等于 VLA 低层动作策略学习 |
| **世界模型滚动与真实观测接地** | 模型预测 chunk 与动作执行并行，之后再用真实观测修正 | 预测 latent/history 与下个视频/动作 chunk | LingBot-VA | 物理任务与仿真均有结果；async 2×速度消融仅在 RoboTwin，且 naive async 对长 horizon 退化 |

这些不是互斥“模型路线”：一个策略可以同时分 chunk 执行，也可以跨 chunk 接反馈；但只有显式更新 policy/BT/code 才能称作对应层级的策略学习或程序修订。

## 1. 四个代表工作，四种闭环位置

### 1.1 π0 与 Diffusion Policy：chunk 外重观察

π0 每次推理产生动作 chunk，再执行预设步数后重新观察；论文给出 20 Hz 本体 0.8 秒一轮（执行 16 步）和 50 Hz 本体 0.5 秒（执行 25 步）的配置。Diffusion Policy 在其真机任务使用 10 Hz 决策、125 Hz 插值执行；每次预测较长 horizon 并只执行部分动作，支持 receding-horizon warm start。[π0 分册](../papers/2410.24164-pi0.md) §3–4；[Diffusion Policy 分册](../papers/2303.04137-diffusion-policy.md) §2–3

**判读**：chunk 重规划可以让动作块与动作块之间接收新观测，但不能自动证明 episode 内失败恢复。必须同时报告 chunk 长度、实际执行步数、观察频率和推理延迟。

### 1.2 VLCP：在同一 episode 改写控制逻辑

VLCP 在 MuJoCo/RoboVerse 的 Franka Panda 环境里，每 50 simulation steps 重观察并改写控制函数。其闭环对照把 pooled success 从 3.5% 提到 35.1%（57 个任务的单次 episode sweep）；另一组 75 个抓放 episode 中，55 次出现失败抓取，15 次之后成功重新接近并举起，恢复率 27.3%，中位需要 3 次 replan（arXiv:2608.16978v1，Fig. 2、Table 2）。

限制很关键：作者明确说只跑过仿真，物体 pose 由 simulator 提供；Panda 的真实视觉感知噪声、动力学与执行安全尚未验证。单次 VLM replan 中位延迟 18.8 秒，因此 50 simulation steps 并非 50 Hz 的 VLM 闭环（Fig. 2、§4.6、§5）。详见 [VLCP 分册](../papers/2608.16978-vlcp.md)。

### 1.3 π*0.6 / RECAP：跨 episode 从真机经验学习

RECAP 收集 autonomous rollouts 和专家遥操作修正，把 success/failure 与进展信号用于 value function 和 advantage-conditioned policy 更新；每轮数据收集后重新从预训练 checkpoint 微调以避免累积漂移。平台为 50 Hz 双 6-DoF 手臂、平行夹爪、三摄像头。作者报告多品种洗衣与 espresso 吞吐超过 offline-RL+SFT 起始策略 2×，失败率约减半；容易洗衣任务的成功率早已接近上限，后续主要改善吞吐（Fig. 7–10）。任务分别有 200、500、600 秒等成功时限，不能混成统一成功率；T-shirt/shorts 洗衣两轮改进每轮 300 条 autonomous trajectories，箱体装配主文称每轮 600 autonomous + 360 intervention trials（§6-C.1–2）。补充材料还列出多品种洗衣 450 evaluation + 287 correction episodes、咖啡单轮 414 autonomous + 429 correction episodes；纸箱的 600 在补充材料中称 demonstrations，标签与主文用语有差异。详见 [RECAP 分册](../papers/2511.14759-pi-star-0.6-recap.md)。

**研究推断 / 报告建议** `[推断]`：结合 [VLCP 分册](../papers/2608.16978-vlcp.md) 的同回合恢复与 [RECAP 分册](../papers/2511.14759-pi-star-0.6-recap.md) 的跨回合更新，可把“纠正当下失误”与“把经验转成下一轮参数化策略改进”区分开。RECAP 的专家干预是按需提供，不是每回合必需；作者也指出干预会打断自主运行，且质量不稳定，难以持续改进速度等细节（RECAP v2 §V-D）。引用时宜分别报告自然成功轨迹、专家干预与任务示范。

### 1.4 LingBot-VA：世界模型 rollout 与观测接地

LingBot-VA 自回归预测视觉 latent 并由 inverse dynamics 生成动作 chunk。策略执行当前 chunk 时并行推理下一个；每轮后，真实 observation 加进 KV cache，FDM 对过时 latent 做重新接地。RoboTwin Easy 上 async 比 sync 快 2×、成功率近似；naive async 因未来预测漂移而在 horizon=3 降到 32.9%，FDM-grounded 版本为 85.6%（Table 3）。

论文另有六项真实操作任务，每项 50 条示范后适配、详细结果各 20 trials（Fig. 5–6、Table S2–S7）；这是真机成功证据，但**不是**2×速度消融的硬件口径。该方法体现世界模型 rollout 进入策略执行环路，不等于模型先验替代了真实状态反馈，也不等于策略通过 real-world RL 更新。详见 [LingBot-VA 分册](../papers/2601.21998-lingbot-va.md)。

### 1.5 VersualRL：真机任务层策略改写的边界样本

arXiv:2603.22169 的准确题名是 *VersualRL: Closed-Loop Verbal Reinforcement Learning with Visual Execution Feedback for Task-Level Robot Planning*，不是在 VLA 低层输出动作的模型。它在真实移动机器人上每 episode 执行 Behavior Tree，以视觉 critic 与人工核验分数为依据跨 episode 编辑 BT；五个 field layout、每个配置 10 个连续 episode。基础模型部署期冻结，更新对象是符号任务树。Qwen2.5-VL-3B critic 的 LoRA 用 88 个执行 episode 单独微调，训练不应与 50 个策略 refinement episode 混算（§III、IV、V）。

它说明真实机器人上的语言化策略反馈与迭代执行有研究价值，但本专题操作性判据要求 VLA 直接输出动作；BT actor 本身不读原始感知或控制硬件，执行由固定节点库承担。故将其登记为边界参照，不列入 VLA 精读论文榜。详见 [CANDIDATES.md](../sources/CANDIDATES.md) §4.2 与 arXiv:2603.22169v3 §III–V。

## 2. 实验数字不可混榜

| 工作 | 平台与回合单位 | 主要报告 | 可以支持 | 不可支持 |
| :-- | :-- | :-- | :-- | :-- |
| VLCP | MuJoCo/RoboVerse；57-task 主 sweep，每任务 1 episode | 35.1% vs matched open-loop 3.5%；另一 75 episode 子集恢复 15/55 失败抓取 | 在该仿真配置中重写代码可恢复一部分空抓 | 真实机器表现、与真机 VLA 排名 |
| RECAP | 真实双臂；多任务 episode，时限按任务定 | 困难洗衣/咖啡吞吐 >2×，失败约减半；箱体 600 秒指标 | 真机经验和 advantage conditioning 可改进多个任务 | 与 VLCP/VA 的不同指标跨论文直接比值 |
| LingBot-VA | 真机 6 项、每项 20 trials；另有 RoboTwin / LIBERO | 真机按任务 success/progress；仿真 async 2× speed ablation | 世界模型政策的 chunk 滚动可在真机任务评估，FDM 接地对 async 仿真重要 | 声称真机全任务 2×、真实 VLA RL |
| VersualRL | 真实移动机器人；5 layouts × 10 sequential episodes/configuration | episode score、issue recall、critic confidence、human alarm | 任务树可由有地面约束的视觉反馈逐轮修改 | 低层 VLA 动作策略成功率 |

## 3. 最低限度的闭环报告要素

引用闭环控制实验时至少记录：

1. 回路里更新的对象：动作 chunk、代码、BT、模型隐状态、参数权重，分别写清。
2. 反馈出现的位置与频率：每步、block 边界、每 episode 后，或训练迭代。
3. 同步/异步的执行关系、chunk 长度、推理等待与硬件吞吐。
4. episode 内恢复判据和分母，例如“失败抓取 episode 中后来成功举起”不等于任务最终成功率。
5. 真机/仿真、观测 pose 是否 privileged、视觉噪声与硬件本体。
6. 每任务 trial 数、随机种子、停止条件、超时以及 success/progress/throughput 的定义。
7. 跨 episode 经验量：示范数、自主 rollouts、人工干预数、训练更新量，以及模型是否重新初始化。

## 4. 阅读路径

- 想了解 chunk 重规划、动作频率与延迟：先读 [动作表征三路线](action-representation.md)，再读 π0 与 Diffusion Policy 分册。
- 想看失败后同回合能否纠错：读 VLCP 分册，特别核实其仿真边界。
- 想看 VLA 如何从部署体验持续改进：读 RECAP 分册。
- 想理解视频世界模型滚动、并行执行与闭环接地：读 LingBot-VA 分册。
- 想看真机任务级语言/符号策略 refinement 的边缘案例：参阅 VersualRL 的 arXiv 全文；它不等价于 VLA 低层控制。

---

*编制时间：2026-10-23。论文版本、图表锚点与实验边界按一手 arXiv 原文逐篇核对。*
