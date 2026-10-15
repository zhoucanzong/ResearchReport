# WorldModels 技术专题调研

> **声明**：本报告由 AI Agent 自动调研生成，未经官方确认；引用具体参数、日期或 benchmark 前请回溯原始来源。
> **调研日期**：2026-10-16（第一轮：骨架，未做正文精读）。
> **定位**：WorldModels（世界模型）指**从数据中学得环境动力学、可由外部控制信号驱动、并被当作可交互模拟环境供 agent 训练/规划/评测**的模型；本专题为其判据、架构谱系、交互性机制、代表系统、评测与应用边界建立框架与证据索引。

**证据等级约定**：`[精读原文]` 已通读一手正文；`[摘要级]` 仅核验官方摘要/页面（题名、作者、日期），**未通读正文，相关表述不得当作已成立事实**；`[二手]` 第三方转述。

---

## 0. 本章结论

1. **术语尚未收敛**：至少存在三种用法——(i) 认知科学/RL 意义的环境内部模拟器（Ha & Schmidhuber 2018）；(ii) 生成式视频/3D 模型（可交互视频世界建模）；(iii) 面向 Physical AI 的 foundation model 平台（Cosmos 一类）。本专题取「判据可判定」的操作性定义，而非单一作者定义。`[摘要级]`
2. **三条判据缺一不可**：`(a) action-conditioned` + `(b) 系统可调用` + `(c) 环境动力学从数据学得` 同时满足才纳入本专题。`[摘要级]`
3. **规则模拟器被排除**：MuJoCo / Atari / Doom 一类满足 (a)(b) 但动力学为人工硬编码、缺 (c)，**不入 WorldModels**，仅作评测环境与数据来源。`[摘要级]`
4. **三条架构主线并行**：action 条件化视频/3D 生成、潜空间预测模型（JEPA / Dreamer）、world foundation model 平台化。`[摘要级]`
5. **交互性瓶颈在长时程一致性与 action-following 响应延迟**，而非单帧画质；评测仍呈碎片化（各应用域各自 benchmark，缺统一口径）。`[摘要级]`

> 本轮为骨架：上述结论全部为 `[摘要级]`，尚无 `[精读原文]` 支撑；第二轮精读后需逐条升级或推翻。

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

- 定义谱系仍需回到原始一手正文核对（结论 1）；`(c)` 的判定需要可操作阈值（学到 vs 混合）：留待第二轮。

---

## 2. 架构谱系

**本章要回答**：三条主线各自的代表架构、训练目标与分界是什么？action 条件化生成与潜空间预测在表示、目标函数、可控性上如何取舍？平台化路线（foundation model + post-train）与单系统路线差异在哪？

**计划证据来源**：参考文献 2–17（PlaNet / Dreamer 系 / MuZero / I-JEPA / V-JEPA 系 / IRIS / Genie / GameNGen / Matrix-Game / Hunyuan-GameCraft / Cosmos 及官方仓库）。

## 3. 交互性机制与指标

**本章要回答**：长时程一致性、记忆、action-following 响应延迟如何度量？自回归/扩散的误差累积如何缓解（teacher forcing 偏差、few-step 蒸馏）？实时性（帧率、首帧延迟）与保真度如何权衡？

**计划证据来源**：参考文献 18–19（CausVid、Self Forcing）、14–16、以及 37 的 benchmark 章节。

## 4. 代表系统逐案

**本章要回答**：每个系统在三条判据上如何落位？其可交互性宣称（分钟级一致性、实时帧率等）出自何种一手材料、可否复核？

**计划证据来源**：参考文献 20–23（Genie 3 官方博客与模型页、GameNGen 项目页、Dreamer 4 项目页、V-JEPA 2 官方仓库），并交叉 9、10、13、16。

## 5. 评测与基准

**本章要回答**：现有 benchmark 覆盖哪些维度（视觉质量、物理合理性、世界一致性、交互可控性）？哪些可迁移为 WorldModels 的统一评测？缺什么？

**计划证据来源**：参考文献 24–28（VBench、VBench-2.0、WorldScore、Physics-IQ、Awesome-Interactive-World-Model 索引）。

## 6. 应用域

**本章要回答**：游戏引擎、具身/机器人、自动驾驶、开放世界探索四个域各自的数据与指标要求是什么？跨域可复用什么、不可复用什么？

**计划证据来源**：参考文献 29–32（GAIA-1/GAIA-2、Vista、自动驾驶世界模型综述）、23、16。

## 7. 与 AIGC / Embodied / LLM 的边界及交叉引用

**本章要回答**：边界判据如何在具体工作中执行（尤其 VLA 与 action-world 联合模型）？与 `VideoGen`、`DiT`、`3DGen`、`Agent`、`VLM`、`ReasoningModels` 的交叉引用点有哪些？

**计划证据来源**：参考文献 33–35（π0、OpenVLA、WorldVLA）、39（Sora 事实的二手来源）；以及本仓库既有报告 `AIGC-Research/TechnicalTopics/VideoGen-research/report.md`、`LLM-Research/TechnicalTopics/Agent-research/report.md`。

## 8. 未决问题

**本章要回答**：定义何时可能收敛？评测统一化的现实路径？sim-to-real 与安全部署的门槛？物理一致性是否可被现有指标证伪？

**计划证据来源**：参考文献 36–38（两篇 2026 综述与 2411.14499）、以及第 5 章缺口清单。

---

## 参考文献

> 体例：编号 + 标题 + 一手来源链接 + 证据等级 + 归属章节。**本轮共 39 条：`[摘要级]` 38 条 + `[二手]` 1 条 + `[精读原文]` 0 条**（骨架轮未通读正文）。

1. World Models (Ha & Schmidhuber, 2018) — [arXiv:1803.10122](https://arxiv.org/abs/1803.10122) — `[摘要级]` — 章1
2. Learning Latent Dynamics for Planning from Pixels (PlaNet) — [arXiv:1811.04551](https://arxiv.org/abs/1811.04551) — `[摘要级]` — 章2
3. Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model (MuZero) — [arXiv:1911.08265](https://arxiv.org/abs/1911.08265) — `[摘要级]` — 章2
4. Dream to Control: Learning Behaviors by Latent Imagination (Dreamer) — [arXiv:1912.01603](https://arxiv.org/abs/1912.01603) — `[摘要级]` — 章2
5. Mastering Atari with Discrete World Models (DreamerV2) — [arXiv:2010.02193](https://arxiv.org/abs/2010.02193) — `[摘要级]` — 章2
6. Mastering Diverse Domains through World Models (DreamerV3) — [arXiv:2301.04104](https://arxiv.org/abs/2301.04104) — `[摘要级]` — 章2
7. Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (I-JEPA) — [arXiv:2301.08243](https://arxiv.org/abs/2301.08243) — `[摘要级]` — 章2
8. Revisiting Feature Prediction for Learning Visual Representations from Video (V-JEPA) — [arXiv:2404.08471](https://arxiv.org/abs/2404.08471) — `[摘要级]` — 章2
9. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning — [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) — `[摘要级]` — 章2/4
10. Training Agents Inside of Scalable World Models (Dreamer 4) — [arXiv:2509.24527](https://arxiv.org/abs/2509.24527) — `[摘要级]` — 章2/4
11. Transformers are Sample-Efficient World Models (IRIS) — [arXiv:2209.00588](https://arxiv.org/abs/2209.00588) — `[摘要级]` — 章2
12. Genie: Generative Interactive Environments — [arXiv:2402.15391](https://arxiv.org/abs/2402.15391) — `[摘要级]` — 章2
13. Diffusion Models Are Real-Time Game Engines (GameNGen) — [arXiv:2408.14837](https://arxiv.org/abs/2408.14837) — `[摘要级]` — 章2/4
14. Matrix-Game: Interactive World Foundation Model — [arXiv:2506.18701](https://arxiv.org/abs/2506.18701) — `[摘要级]` — 章2
15. Hunyuan-GameCraft: High-dynamic Interactive Game Video Generation — [arXiv:2506.17201](https://arxiv.org/abs/2506.17201) — `[摘要级]` — 章2
16. Cosmos World Foundation Model Platform for Physical AI — [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) — `[摘要级]` — 章2/4
17. cosmos-predict1 官方仓库（NVIDIA） — [官方仓库](https://github.com/nvidia-cosmos/cosmos-predict1) — `[摘要级]` — 章2
18. From Slow Bidirectional to Fast Autoregressive Video Diffusion Models (CausVid) — [arXiv:2412.07772](https://arxiv.org/abs/2412.07772) — `[摘要级]` — 章3
19. Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion — [arXiv:2506.08009](https://arxiv.org/abs/2506.08009) — `[摘要级]` — 章3
20. Genie 3: A new frontier for world models（官方博客，2025-08-05） — [官方博客](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) — `[摘要级]` — 章4
21. Genie 3 官方模型页 — [官方模型页](https://deepmind.google/models/genie/) — `[摘要级]` — 章4
22. GameNGen 官方项目页 — [官方项目页](https://gamengen.github.io/) — `[摘要级]` — 章4
23. Dreamer 4 官方项目页 — [官方项目页](https://danijar.com/dreamer4/) — `[摘要级]` — 章4
24. V-JEPA 2 官方仓库（Meta） — [官方仓库](https://github.com/facebookresearch/vjepa2) — `[摘要级]` — 章4
25. VBench: Comprehensive Benchmark Suite for Video Generative Models — [arXiv:2311.17982](https://arxiv.org/abs/2311.17982) — `[摘要级]` — 章5
26. VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness — [arXiv:2503.21755](https://arxiv.org/abs/2503.21755) — `[摘要级]` — 章5
27. WorldScore: A Unified Evaluation Benchmark for World Generation — [arXiv:2504.00983](https://arxiv.org/abs/2504.00983) — `[摘要级]` — 章5
28. Do generative video models understand physical principles? (Physics-IQ) — [arXiv:2501.09038](https://arxiv.org/abs/2501.09038) — `[摘要级]` — 章5
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

---

## 链接核验清单

> 核验方式：arXiv 条目经 `export.arxiv.org` Atom API 逐条比对**编号 ↔ 题名 ↔ 发布日期**；非 arXiv 条目经 HTTP 状态码探测。核验时间：2026-10-16。

| 链接 | 核验方式 | 结果 |
| :-- | :-- | :-- |
| 参考文献 1–16、18–19、25–28、30–39 共 **32 条** arXiv 链接 | arXiv Atom API 批量比对题名/发布日期 | **全部通过**（题名与编号一致，无错配） |
| [https://github.com/nvidia-cosmos/cosmos-predict1](https://github.com/nvidia-cosmos/cosmos-predict1) | HTTP 状态码 | 200 |
| [https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) | HTTP 状态码 + 正文抓取 | 200，标题/日期（2025-08-05）/作者一致 |
| [https://deepmind.google/models/genie/](https://deepmind.google/models/genie/) | HTTP 状态码 | 200 |
| [https://gamengen.github.io/](https://gamengen.github.io/) | HTTP 状态码 | 200 |
| [https://danijar.com/dreamer4/](https://danijar.com/dreamer4/) | HTTP 状态码 | 200 |
| [https://github.com/facebookresearch/vjepa2](https://github.com/facebookresearch/vjepa2) | HTTP 状态码 | 200 |
| [https://github.com/liujiuming123/Awesome-Interactive-World-Model](https://github.com/liujiuming123/Awesome-Interactive-World-Model) | HTTP 状态码 | 200 |

**不可达 / 反爬条目及处置**

| 链接 | 结果 | 处置 |
| :-- | :-- | :-- |
| [https://openai.com/index/sora-2/](https://openai.com/index/sora-2/) | **403 反爬** | 剔除一手引用；Sora 相关事实改引 `[二手]`（参考文献 39）并显式标注二手，**不拿二手充一手** |
| [https://openai.com/index/video-generation-models-as-world-simulators/](https://openai.com/index/video-generation-models-as-world-simulators/) | **403 反爬** | 同上，本轮不作为参考文献列出 |

---

*本轮为第一轮骨架：章节仅含「本章要回答什么 + 计划证据来源」，正文与精读升级留待第二轮；全部结论为 `[摘要级]`。*
