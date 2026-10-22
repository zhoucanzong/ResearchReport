# 世界模型怎样把预测变成 VLA 的真实改进？

> **问题范围**：论文提出的世界模型，究竟通过合成示范、想象环境中的强化学习，还是动作候选规划来改善策略？本文先比较前两条训练路径，并把真机结果、真实交互预算和验证方式放在同一张证据表里。世界模型的环境/状态转移定位见 [WorldModels 报告](../../WorldModels/report.md)；推理时的候选动作规划见[闭环控制专题](closed-loop-control.md)；世界模型用作策略评测器的证据见[评测科学专题](../../../Evaluation/EvaluationScience/report.md)。

## 先区分世界模型承担的角色

“预测未来”并不等于策略已经学会控制。至少有三种不同接口：

| 角色 | 预测如何影响策略 | 训练/部署时需要什么 | 本专题代表作 |
|---|---|---|---|
| **合成示范生成器** | 生成视频和伪动作，作为监督数据训练策略 | 需要验证动作标签和物理可执行性；可以混入真机示范 | Grounded-Dreamer；与其不同，SimVLA 从程序化物理仿真生成动作与视觉问答监督 |
| **想象环境 / RL 模拟器** | 策略在模型预测出的状态与奖励中采样，再按回报更新 | 需要可靠奖励、可控动作条件和对策略分布变化的适应 | VLAW、World-VLA-Loop、WoVR |
| **在线候选规划器** | 预测各个候选动作后果，选择并执行一段动作，再观察真实世界 | 推理期间运行预测或排序；不一定生成新训练数据 | Cosmos Policy、GPC、τ₀-WM；留作后续专题候选 |

这三条路线的结果不能合并成“世界模型提高了 VLA”。模型角色、真机数据预算、是否使用真实示范、任务和评测指标都不同。

## 论文证据对照

| 论文 / 固定版本 | 世界模型如何进入学习 | 真机证据与真实交互 | 可以得出的结论 | 不能据此得出的结论 |
|---|---|---|---|---|
| [VLAW](../papers/2602.12063-vlaw.md) · [原文 v2](https://arxiv.org/html/2602.12063v2)，2026-02-15 | 用策略真机 rollouts 更新 action-conditioned video model；模型生成轨迹经 reward model 筛选，再与真实成功轨迹一起微调 π₀.₅。 | DROID / Franka，五类接触任务；每轮每类 50 条真机轨迹、500 条合成轨迹，共两轮。论文报告合成轨迹相对只用真实成功轨迹的增量；仍需在线真机数据来纠正世界模型。 | 成功筛选的想象轨迹能在本设置补充真实示范，世界模型需见过当前策略的失败分布。 | 不是零样本迁移，也不是纯仿真训练；不是所有提升都来自合成样本。锚点：§5.1–5.3、Algorithm 1、Table 1、Figure 7–9。 |
| [World-VLA-Loop](../papers/2602.06508-world-vla-loop.md) · [原文 v2](https://arxiv.org/html/2602.06508v2)，2026-05-25 | 用近成功轨迹 SANS 训练同时预测视频与二元奖励的世界模型；OpenVLA-OFT 在学习到的世界模型中做 RL，再把新策略 rollouts 反馈给模型。 | ManiSkill 预训练集 35k video-action pairs / 23 tasks；真机特定任务约 50 条成功和 50 条失败轨迹。Franka 上两项真机任务各 30 次评估；作者报告 RL 后分别为 36.7% / 40.0%，两次共同迭代后 50.0% / 53.3%。 | 近成功失败和 reward supervision 会改变模拟器对小动作误差的建模；共同迭代有助于维持策略—模拟器对齐。 | 真机证据是两项任务的小样本实验；初始任务策略仍有示范，物理 rollouts 也参与共演化。>300 帧长任务的画质漂移是作者明确限制。锚点：§3.1–3.3、§4.1–4.4、Tables 2–4、Appendix A.3。 |
| [WoVR](../papers/2602.13977-wovr.md) · [原文 v2](https://arxiv.org/html/2602.13977v2)，2026-06-27 | 在 video world model 中做 imagined RL；KIR 把 rollout 起点移至任务关键帧以缩短预测深度，PACE 用更新策略分布的数据修正模型。 | LIBERO 里以每 suite 2,500 条环境轨迹作预算比较；WoVR 先用 1,500 条 base-policy trajectories 学模型，再用 1,000 条 evolved-policy trajectories 对齐。物理测试覆盖 Franka 与 AgileX Piper、六任务、每任务 30 次。Table 3 的平均成功率：Franka 51.1→80.0%、Piper 15.5→28.9%；π₀.₅/Piper 的独立表格条件为 34.4→56.7%。 | 仅改善视觉保真不够；想象 horizon 与 policy–simulator distribution shift 会改变 reward，交互层控制可提升想象 RL 的稳定性。 | 这些是真机评估的作者结果，不是跨平台大规模复现；表间基线设置不同，不能将一个平均值替代另一个。长时程移动操作仍未验证。锚点：§3.1–3.3、§4.1–4.3、Tables 2–4、Appendix D.2、F。 |
| [SimVLA](../papers/2610.11248-simvla.md) · [原文 v1](https://arxiv.org/html/2610.11248v1)，2026-10-08 | 用程序化物理仿真生成动作轨迹 SimAction、privileged SimVQA、以及仿真策略部署数据 SimDeploy；不是视频生成式世界模型。 | Anubis 上五项长程移动操作，mock kitchen / pantry / real home，合计 2,120 rollouts。主指标是子目标完成度 task progress；作者报告平均 54.4%，高于每任务 50 条真机示范的 π₀.₅ 基线。另使用真实机器人校准运动学/动力学，但没有用于训练的 teleoperation demonstrations。 | 仿真可同时供给动作、空间语言监督和部署分布数据；不同监督的消融显示 SimVQA、tokenized SimAction 均有贡献。 | “训练只用仿真数据”不等于完全没有真实硬件流程：system identification 使用真实运动校准序列；task progress 也不能改称二元任务成功率。锚点：§3.2–3.5、§4.2–4.8、Appendix C、F–H。 |
| [Grounded-Dreamer](../papers/2610.13164-grounded-dreamer.md) · [原文 v1](https://arxiv.org/html/2610.13164v1)，2026-10-09 | 从少量真实初始图像重建任务场景，视频世界模型生成画面、IDM 生成动作；再把合成动作轨迹回放进物理模拟器，只用成功轨迹训练策略。 | Franka、七项任务；表 1 比较 simulation-only、每任务 50 条 real-only 和生成数据；对比评估 20 次/任务，scale analysis 30 次/任务。作者报告 GD-only 策略接近部分 real-only 结果，OOD 下经 replay 验证的数据较稳。 | 视觉生成与物理可行性检查要结合，真实图像可作为场景条件而不提供遥操作动作标签。 | “无需 human demonstrations”不等于“零真实数据”：初始图像、实物/相机几何和任务场景重建仍来自现实；模拟器通过也不等同真机可靠性。锚点：§3.1–3.4、§4.1–4.5、Tables 1–4、Appendix E。 |

## 横向结论：收益取决于监督链闭不闭合

第一，**未来画面要和动作及结果一起对齐**。VLAW 的 action-conditioned world model 使用在线策略交互补充专家数据，World-VLA-Loop 把 reward head 与视频生成联合训练；两者都显示，只看视觉相似度无法确保 reward 对真实操作结果可靠。VLAW 50 条 interaction clips 的 event confusion matrix 中，加入 online rollouts 后 false positive 从 11 降到 1（Table 1）；这对合成轨迹过滤尤其重要。[VLAW §5.2、Table 1]

第二，**策略开始利用模型错误时，更多 imagined rollout 可能扩大偏差**。WoVR 用关键帧初始化来控制预测误差深度，并让模型追踪演化后的策略分布。Grounded-Dreamer 采取另一条路径：生成后回到有物理引擎的场景中 replay 过滤。两者分别管理模型内想象误差和模型外物理约束，不能简化成同一个“准确度增强”模块。

第三，**合成数据路线和想象 RL 路线需要不同的验收指标**。SimVLA 的关键结果是跨场景 task progress 与多监督消融；Grounded-Dreamer 检查物理回放后的数据质量及真机 success rate；VLAW/World-VLA-Loop/WoVR 还需检查策略更新期间的 reward/model alignment。不同论文的基线和数据预算不相同，不能排成统一排行榜。

世界模型作为**评测器**也需独立验证。[WorldGym v3](https://arxiv.org/html/2506.00613v3) 在 Bridge 的 17 项任务上比较 RT-1-X、Octo、OpenVLA（每任务原实机协议 10 次），报告逐任务仿真—实机成功率 Pearson 相关 r=0.78，三种策略平均成功率差异约 3.3 个百分点；这支持特定数据与模型范围里的排序参考，不证明其世界模型适合训练 VLA，也不能外推到上述新管线。[§4.1、Figure 4]

## 仍待论文解决的问题

- 哪些情形下策略更新确实来自合成轨迹：需要统一报告真机轨迹数、合成轨迹数、成功筛选方式，以及只移除 synthetic data 的消融。
- 模型是否在当前策略访问的分布内可靠：除视频指标外，报告 action-following、成功/失败 reward 的 false positive、长 horizon 误差和策略利用模型漏洞后的表现。
- “零样本 sim-to-real”到底排除了什么：遥操作示范、真机校准、真实初始图像、真实 policy rollout 应分别统计。
- 结果是否能迁移到不同本体和复杂任务：上述直接对照主要集中在桌面或厨房任务；VLA 与移动底盘、柔性物、动态环境的证据仍不足。
- 论文的平均分和作者示范不代表长期可靠性；需要跨环境、重复运行、失效分布及独立复核。WorldGym 的相关性结果只能限定在其本次三个策略与已知轨迹范围。

## 阅读顺序

1. 先读 [SimVLA](../papers/2610.11248-simvla.md)：理解仿真如何同时产生动作、视觉语言监督和部署 rollout。
2. 再读 [Grounded-Dreamer](../papers/2610.13164-grounded-dreamer.md)：看视频世界模型的伪动作怎样经物理回放筛选。
3. 然后比较 [VLAW](../papers/2602.12063-vlaw.md) 与 [World-VLA-Loop](../papers/2602.06508-world-vla-loop.md)：前者用合成成功轨迹监督微调，后者在学到的模拟器里做 RL。
4. 最后读 [WoVR](../papers/2602.13977-wovr.md)：把 imagined RL 的长 horizon drift 和策略—模拟器错位作为可靠性设计问题。
