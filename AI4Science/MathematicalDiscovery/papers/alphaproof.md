# 精读：AlphaProof——在 Lean 中搜索形式证明

## 亮点与差异

- **一句话亮点**：把 Lean tactic 状态和经内核检查的 proof term 纳入强化学习闭环，让试错反馈有机器可验的数学语义。
- **新在哪**：相对只预测下一步 tactic、整段自然语言证明或静态搜索的系统，AlphaProof 将主 RL、树搜索、自动形式化题库与目标专用 TTRL 组合起来；它不是仅靠自然语言裁判筛答案。
- **证据强度**：有修正后的 miniF2F、258 道非几何历史 IMO 题、PutnamBench-test 及 Lean 核验；2024 IMO 的 28/42 是 AlphaProof 与 AlphaGeometry 2 的组合成绩，且依赖赛后手工形式化和多日目标专用计算。
- **值不值得引用**：适合解释 verifier-grounded proof search、Lean/RL 交互和正式证明与完整自动解题的边界；不适合简写成“AlphaProof 独自获得 IMO 银牌”。

## 文献信息

- Thomas Hubert et al., “Olympiad-level formal mathematical reasoning with reinforcement learning,” *Nature* 651, 607–613 (2026), DOI [10.1038/s41586-025-09833-y](https://doi.org/10.1038/s41586-025-09833-y)。2025-11-12 online，version of record 2026-03-13，CC BY 4.0。没有核验到独立 arXiv 身份，固定来源为 Nature 版本及官方补充材料。
- 本文没有运行 AlphaProof、Lean 项目或作者代码。Supplementary Data 提供高层伪代码，不等于模型权重或完整复现实验环境公开。

## 1. 解决什么问题

自然语言证明模型可能生成貌似合理但不成立的推理，且普通基准通常只判最终答案。论文要做的是让系统在可交互的 proof assistant 中逐步提出 tactics，通过机器检查反馈学习证明策略，并测试这种方法是否能泛化到历史竞赛和大学数学题（正文 §§Introduction、“AlphaProof”）。研究目标是**形式化命题的证明搜索能力**；题意翻译、形式化忠实性与人类所说的数学新颖性是相邻但独立问题。

## 2. 核心方法

AlphaProof 把 Lean 4 tactic-mode 建模为 RL 环境：状态是当前假设和剩余目标的 tactic state，动作是 tactic 字符串；每执行一步奖励为 −1，引导模型寻找短证明。3B 参数 encoder–decoder 证明网络估计动作策略与状态价值；AlphaZero/Sampled MuZero 风格 PUCT tree search 扩展 Lean 状态节点。对分解为多个子目标的节点，作者用最难分支（最小 return）而非所有分支长度之和定义价值，鼓励将目标拆成相对均衡的子问题（正文 Methods “Lean environment”“Prover agent”“Tree search algorithm”；Fig. 1）。

学习分两层：主 RL 从自动形式化语料及自生成的证伪/证明经验中学习一般策略；难题上使用 test-time reinforcement learning (TTRL)，先围绕目标生成简化、推广、引理等变体组成局部课程，再在该课程做目标专用 RL（正文 Fig. 2；Methods “Main RL”“Inference”与“TTRL”）。每个候选 tactic 在 Lean 中执行；完成后，独立调用标准 Lean 命令检查完整 proof term，并检查只依赖 Lean 的三条内建公认公理（Methods “Proof verification final check”）。

## 3. 数据与规模

- 训练语料：论文报告项目期间自动形式化流程生成约 8,000 万题；主 RL 使用约 80,000 TPU-days，自动形式化另约 100,000 TPU-days。补充 Table 4 列出 300B-token 预训练与 300k Mathlib state–tactic 对的 SFT 配置；这些计算规模解释了性能结果不等于普通实验室可轻易复现（正文 Methods “Main RL”“Auto-formalization”；Supplementary Tables 4、6）。
- 基准：经修正的 miniF2F；专家内部形式化的 `formal-imo`（258 道非几何历史 IMO：代数 107、组合 77、数论 74）；PutnamBench-test（189 道题，取 1990 年起偶数年的题）。论文说明原 miniF2F/PutnamBench 含误形式化题，做了修正（正文 Methods “Evaluation”，尤其 “Data separation and generalization”）。
- IMO 2024：非几何五题由专家在题目发布后手工形式化；P4 不由 AlphaProof 处理，而用 AlphaGeometry 2。P1、P2、P5、P6 中需先“找出答案”的题目，先由 Gemini 1.5 Pro + Python 工具生成候选，再进入证明/反驳搜索（正文 §“Performance at the 2024 IMO”、Fig. 5）。

## 4. 主要结果（带条件）

**形式基准上的计算扩展**：树搜索从每题 2 TPU 分钟增加到 12 TPU 小时，formal-imo 与 PutnamBench-test 的 solve rate 提高超过 10 个百分点；再加目标专用 TTRL，与 12 TPU 小时树搜索相比，两项基准都再提高约 15 个百分点（正文 Fig. 4、Table 1）。补充 Table 1 按学科显示：formal-imo 的代数/组合/数论在 12 TPU-hours 时为 53.1%/13.5%/61.3%，50 TPU-days TTRL 后为 67.9%/17.6%/70.3%，500 TPU-days 后为 72.6%/20.3%/75.7%。指标是**Lean 形式化测试题 solve rate**，不是开放自然语言题的端到端正确率。

**IMO 2024 组合成绩**：AlphaProof 用 2–3 天 TTRL 分别解决 P1、P2、P6；P3、P5 未解。AlphaGeometry 2 解 P4；总计 4/6、28/42，银牌分数区间。题目先经专家形式化，某些答案由 Gemini+Python 提议；多日训练时间远超人类竞赛时限。因此这是一个包含人工 formalization、答案生成、两种专用系统和长时间搜索的 pipeline 结果（正文 §“Performance at the 2024 IMO”、Fig. 5、Extended Data Figs. 7–9）。

## 5. 消融 / 对照说明了什么

这篇工作没有一个简单的“移除模块后其他条件完全不变”的架构消融；最有信息量的对照是不同推理计算方案与阶段进展，且应读成**计算分配对结果的作用**。Fig. 4 将树搜索与 TTRL 分图绘制：树搜索轴为 TPU-hours，TTRL 轴为 TPU-days，资源数量级并不相同；前述 +10/+15 个百分点不是等成本比较。Fig. 3b 显示主 RL 随训练计算增加，miniF2F-valid、formal-imo 和 PutnamBench-test 的 solve rate 同步提高；Fig. 3c 显示同等 solve rate 所需搜索模拟次数下降，支持“主 RL 学到更有效的搜索策略”，但不是删掉 RL 的对照。

论文还用 miniF2F、formal-imo、PutnamBench-test 的既有 formal prover 基线作横向比较；主文报告最终系统在评测集上的领先结果，Supplementary Table 1 提供按学科及计算预算的 AlphaProof 指标。不同系统/算力设置不是单一受控消融，应把“强于所列 benchmark baseline”和“某模块因果提升多少”分开。（正文 Fig. 3–4、Table 1；Supplementary Table 1。）

## 6. 失效条件与边界

- **几何/语言形式化边界**：AlphaProof 在该 IMO pipeline 中未解几何 P4，论文解释 Mathlib 当时对 Olympiad-style geometry 的支持有限，改由 AlphaGeometry 2 处理。五道非几何题由专家手工翻译为 Lean；kernel 只能保证 Lean 命题的证明，不保证该命题完全保留原题语义。
- **竞赛剩余问题**：组合题 P3、P5 未解；不应从三题成功推断所有 IMO 题型都可处理。
- **计算预算**：目标题 TTRL 持续 2–3 天；补充结果还使用每题 50 或 500 TPU-days。作者在讨论中指出这种训练计算远超大多数研究组能力。
- **benchmark 边界**：测试题需专家/内部 formalization，且数据集修复本身会改变题目集合。单个 kernel-checked proof 的高可信度不能替代题集切分、形式化准确度及覆盖面的审查。

## 7. 与同类系统的可判定差异

形式定理证明同类系统也使用 Lean proof checker，但 AlphaProof 的论文重点是 **RL 与树搜索在 tactic-state 环境中交互**，并以大规模自动形式化数据和 TTRL 对困难目标作专门适应。它与普通自然语言 CoT 不同：最终答案必须是 Lean 可检验 proof term；与 FunSearch 不同：FunSearch 的 evaluator 打分只验证预设构造/任务条件，AlphaProof 由 proof assistant 检查逻辑推导（FunSearch 原文 §“When does FunSearch work?”）。这并不自动使 AlphaProof 更“能发现数学”，而是使它的证明正确性有更强的机器验收边界。

## 原文定位

- 方法与奖励、搜索：Nature 正文 §§“AlphaProof”“Inference”；Methods “Lean environment”“Tree search algorithm”；Figs. 1–2。
- 主 RL 与 held-out 变化：正文 Fig. 3；Methods “Main RL”。
- 计算扩展与各学科数据：正文 Fig. 4、Table 1；官方 Supplementary Information Table 1。
- Lean kernel 检查：Methods “Proof verification final check”。
- 数据集、切分及形式化：Methods “Evaluation”“Data separation and generalization”。
- IMO pipeline 与证明：正文 Fig. 5；Extended Data Figs. 7–9。
