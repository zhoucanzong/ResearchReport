# 投机解码：随机采样与验证正确性（T>0 下的无损性边界）

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、会议 proceedings、官方文档与开源项目整理生成。部分 2025-2026 年信息可能未经完整同行评审，建议读者直接查阅原始论文验证。加速比数据受测试条件（模型规模、硬件、任务类型、temperature、benchmark）影响较大，跨论文直接对比需谨慎。
>
> **调研日期**：2026 年 10 月（本轮更新）
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦 **T>0（随机采样）条件下动态草稿树的正确性与验证规则**。这是本轮更新的最高优先级章节——它的结论直接决定 [speculative-eagle-series.md](speculative-eagle-series.md) 中"动态树更优"这一表述需要附加什么限定条件。
> **证据等级约定**：本报告对每条结论标注 **[精读原文]**（已获取论文正文/官方文档并逐节阅读）或 **[摘要级]**（仅核验会议页/arXiv 摘要，未读正文）或 **[二手]**（第三方解读、非一手来源）。
> **等级规则**：每条结论只取**一个主等级**（精读原文 / 摘要级 / 二手 / 受限核验）；**混合来源取最弱等级**并在正文注明来源类型（如 `[精读原文（vLLM 官方文档）]`）；不使用 `A + B`、`A（摘要层）` 这类复合标签。

---

## 1. 本章结论（先给答案）

1. **T>0 下，EAGLE-3 式动态草稿树会塌缩为 one-hot，接受率显著下降**。原因不是实现 bug，而是机制性的：动态树的扩展与剪枝用 draft 概率 $q(x)$ 排序，而 T=0 时"$q(x)$ 最大"与"会被接受"高度一致；T>0 时是否接受取决于 $p(x)/q(x)$ 的比值，$q(x)$ 不再是接受率的可靠指标。 **[精读原文]**
2. **朴素的修法（直接采样 + 仍按 $q$ 排序）不仅无效，而且会破坏无损性**。token 的"是否在树中存活"依赖它自身的取值，对"存活"取条件会让条件分布偏离原采样分布，验证时使用的概率与实际分布不再匹配。 **[精读原文]**
3. **正确解法是把"建树"与"验证"的角色解耦**。RheoSampling 给同一个随机 token 分配两个概率身份：建树/排序/剪枝用 **proxy 概率**，验证用**真实采样概率**。这是目前唯一同时具备"上下文感知 top-K 建树 + 随机采样 + 无损"的动态树方法。 **[精读原文]**
4. **验证规则本身也还有优化空间，且优化方向分岔为两条**：
   - **保持严格无损**：Traversal Verification 改为叶到根遍历、按序列级概率接受；RheoSampling 的 RheoVerification 用最优传输（OT）重新分配概率质量。两者都声明输出分布严格等于目标分布。 **[精读原文]**
   - **放宽到有界风险**：ARC-Decode 承认经典无损规则在 T>0 下"过度拒绝低风险草稿"，改用 JS 散度风险界定 + Local Tolerance Score 做"软接受"，以"质量近乎不变"换取接受长度。 **[摘要级]**
5. **因此"无损"在不同论文里指的不是同一件事**。至少要区分：严格分布等价（RheoSampling / Traversal Verification）、序列级等价（Traversal Verification 的序列概率视角）、有界风险近似（ARC-Decode）。把 ARC-Decode 的 1.6× 与 RheoSampling 的增益放进同一句话比较是不成立的。 **[摘要级]**
6. **指标必须成对报告**：acceptance rate 与 mean accepted length 会反向移动，单独报一个数字无法判断系统是变快还是变慢。 **[精读原文（vLLM 官方文档）]**
7. **对本专题既有结论的处置**：EAGLE 章节中"动态草稿树在 T>0 下更优"的表述**需要限定**；EAGLE-3 的 4.79× 等数字基本来自 greedy 设定，不可外推到采样场景。 **[精读原文]**

---

## 2. 问题的准确表述

### 2.1 两个被混用的概率角色 **[精读原文]**

RheoSampling 把矛盾说得很清楚：**同一个 draft 概率分布被用于两件互相冲突的事**。

| 角色 | 用途 | 需要的性质 |
|---|---|---|
| **建树（构造/扩展/重排/剪枝）** | 决定哪些 token 进入树、树的拓扑长什么样 | 排序要稳定、要能反映"哪条路径更可能被接受" |
| **验证（接受/拒绝）** | 决定最终输出分布是否等于 $p$ | 必须使用草稿**真实采样分布**的概率 |

T=0 时两者不冲突：draft 的 top-1 通常与 target 对齐，按 $q$ 排序既是一棵好树，也基本等于接受顺序。T>0 时冲突显式化：

- **排序失效**：接受判据是 $\eta \le \min(1, p(x)/q(x))$，与 $q(x)$ 的绝对大小无关。$q(x)$ 小的 token 若 $p(x)$ 足够大仍会被接受；$q(x)$ 大也不保证被接受。
- **无损性被破坏**：若直接把 top-$K$ 换成"随机采样后仍按 $q$ 排序"，那么一个 token **能否存活**取决于它自身取值 → 对"存活"取条件 → 存活 token 的条件分布不再等于 $\tilde q$ → 验证时用错基准概率 → 输出分布不再等于 $p$。

> **这是"动态树 vs 静态树"两难的技术本质**：动态树为了保留上下文感知的拓扑，牺牲了随机采样；静态树为了保留随机采样，牺牲了上下文感知结构。

### 2.2 指标口径的陷阱 **[精读原文]**

vLLM 官方 *Per-Request Acceptance Metrics* 文档给出的定义即口径基准：

| 字段 | 定义 | 说明 |
|---|---|---|
| `mean_acceptance_length` | $1 + \text{num\_accepted\_draft\_tokens} / \text{num\_spec\_steps}$ | 每次验证步平均产出 token 数（**含**必得的 bonus token），范围 $[1, k+1]$ |
| `draft_acceptance_rate` | $\text{num\_accepted\_draft\_tokens} / \text{num\_draft\_tokens}$ | 被提议的草稿 token 中被接受的比例 |
| `acceptance_histogram` | 长度 $k+1$ 的稠密数组，下标 $j$ = "恰好接受 $j$ 个草稿 token"的步数 | 排除 bonus token |
| `num_draft_tokens` | 总提议草稿数，**已扣除被结构化输出约束作废的草稿** | 结构化输出场景下口径会变 |

两个指标的**分母不同**（一个按验证步、一个按提议 token），因此：

> **必须成对报告。** 例如"加深草稿树"通常降低 acceptance rate（多提议了低命中率的 token）却提高 mean accepted length（一旦命中就一次吃更多），只看其中之一都会得出相反的系统结论。

这一提醒在工程侧被反复强调（本报告原计划引用 Morph 的指标说明页，但该链接在核验时被 Vercel 安全检查拦截，见 §6 核验清单，故改用 vLLM 官方文档作为口径依据）。

---

## 3. 三条代表性解法

### 3.1 RheoSampling：双身份解耦（arXiv:2609.21827）**[精读原文]**

**基本信息**：Qiao Hu, Yepeng Weng, Bo Zhang, Takehisa Yairi；arXiv 2609.21827，v1 提交 2026-09-18。

**核心机制**

1. **混合采样**：每个扩展步分配 $K$ 个槽位
   - 前 $m$ 个：按 $q$ **确定性**取 top-$m$（lead tokens，保住高质量骨架）
   - 第 $m+1$ 个：从**残差分布** $\tilde q$（top-$m$ 之外的尾部）**采样**一个代表性 token $x_s$
   - 余下 $K-m-1$ 个：用剩余词表中排名最高者填充（fill tokens）
2. **同一个 token，两个概率身份**
   - 建树期用 **proxy 概率** $q_{\text{proxy}}(x_s) = \min\{q(x_m),\, z\}$，其中 $z = 1-\sum_{i=1}^{m} q(x_i)$ 为残差质量，$q(x_m)$ 为第 $m$ 个确定性概率
   - 验证期用**真实采样概率** $\tilde q(x_s)$
   - 由于 proxy 与 $x_s$ 的**取值无关**，$x_s$ 穿过全局剪枝的存活与否与它采到什么 token 独立——这是保住无损性的关键
   - 边界情形 $m=0$：取 $q_{\text{proxy}} = q(x_1)+\epsilon\ (\epsilon>0)$，把采样 token 锚在首位
3. **rheostat 参数 $m$**：$m$ 小 → proxy 大 → 采样 token 更易存活、随机探索更能落到实处，但确定性骨架变弱；$m$ 大 → 拓扑质量高，但采样节点可能被剪掉。$m$ 是"随机存活 vs 结构质量"的连续调节旋钮。
4. **稀疏分布实现**：softmax 前把 logits 截到 top-128、其余置 $-\infty$。只要**验证阶段使用同一截断分布**，无损性不受影响——这是一个容易被忽略的实现前提。
5. **RheoVerification（OT 验证）**：若 $x_s$ 存活，先用**真实采样概率**独立验证 $\min(1, p(x_s)/\tilde q(x_s))$；若被拒，用残差 $r=\text{norm}(\max(0,p-\tilde q))$ 在候选集上递归拒绝采样。作者论证 OT 方案比 RRSw（无放回递归拒绝采样）能取得更高的采样 token 接受率，因为它全局重分配质量、与 $p$ 的重叠更大。
6. **温度与建树解耦**：建树（扩展 + 重排）**不做温度缩放**，沿用原始 draft 概率排序；温度只作用于采样与验证阶段。理由：低温会破坏 token 相对排序的序信息。

**理论结果**

- **Theorem 1（无损性）**：对任意剪枝预算 $R \ge 1$ 与任意 token 序列 $\mathbf{Seq}$，
  $\mathbb{E}_{T_R}\big[\Pr(\mathrm{Rheo}(T_R)=\mathbf{Seq})\big] = p(\mathbf{Seq})$。
  证明难点在于**动态树本身是随机的**：$Y\sim\tilde q$ 同时决定自身取值和后续 fill tokens 的身份，进而影响更深节点的路径分数与剪枝结果，两层随机性强耦合。作者用**等价类分析**把随机树空间压缩为可处理类别。
- **Lemma 1（proxy 的必要条件）**：proxy 与 $\tilde q$ 独立是**必要但非充分**的，还必须满足排序下界 $q_{\text{proxy}} \ge q(x_{m+1})$；否则采样槽的存活仍依赖采样 token，无损性被破坏。论文给出反例：词表 $\{A,B,C\}$ 上 $q=\{0.5,0.3,0.2\}$、$K=3,m=1$ 时，用 $q_{\text{proxy}}=0.25$ 会让存活 token 被强制为 $B$（概率 1）而非 $\tilde q(B)=0.6$。

**实验（已公布的正文数字）** **[精读原文]**

设定：6 个 benchmark（Alpaca / GSM8K / HumanEval / MT-bench / Natural Questions / CNN-DailyMail），每个 80 题；target 为 Llama-3.1-8B-Instruct、Vicuna-13B-v1.3、DeepSeek-R1-Distill-Llama-8B；draft 全部使用官方 EAGLE-3 checkpoint、不额外微调；单张 A6000；默认 $T=1.0$；树宽 60、深度 8（沿用 EAGLE-3 设置）；3 个随机种子。

| 模型 | 采样方式 | 平均接受长度 $\tau$ | 端到端加速比 | $\tau$ 增益 |
|---|---|---|---|---|
| Vicuna-13B | Top-$K$ | 5.75 ±0.03 | 3.37× | — |
| Vicuna-13B | Rheo | **5.89** ±0.03 | **3.43×** | +0.14 |
| Llama-3.1-8B | Top-$K$ | 5.04 ±0.02 | 2.84× | — |
| Llama-3.1-8B | Rheo | **5.25** ±0.03 | **2.93×** | +0.21（+4.2%） |
| DeepSeek-R1-Distill-8B | Top-$K$ | 4.99 ±0.01 | 2.89× | — |
| DeepSeek-R1-Distill-8B | Rheo | **5.21** ±0.02 | **2.99×** | +0.22 |

- **加速比增益小于 $\tau$ 增益**（Llama-3.1-8B：$\tau$ +4.2%，speedup 只 +3.2%），因为随机探针的采样与验证本身有额外开销。作者称净加速在所有模型上严格为正。
- **rheostat 消融**：$m=1$ 在多数设定下最好或接近最好；$m=0,2$ 也可行且优于 Top-$K$ 基线；$m\ge3$ 时 proxy 概率被摊薄，采样 token 在重排阶段被剪掉，收益退化。
- **温度影响**：温度降低 → 分布尖锐化 → 任何基于概率的采样都退化为确定性取 top token → Top-$K$ / RRS / OT 三类验证策略趋于等价。**这意味着该章方法的价值集中在"温度不是极低"的采样区间。**

**该文自述的定位与边界**：作者称 RheoSampling 是"首个同时具备上下文感知 top-K 建树与随机采样、且保持无损的动态树方法"，并希望这套框架成为分析随机树结构的模板。

**数字的跨论文可比性提醒**：上表 $\tau$ 约为 5（树深 8），而主报告表 2 中 EAGLE-3 的"4-5× 加速"是在另一套设定下得到的；两处不可直接对齐。

---

### 3.2 Traversal Verification：换验证的遍历顺序（NeurIPS 2025）**[精读原文]**

**基本信息**：Yepeng Weng, Qiao Hu, Xujie Chen, Li Liu, Dianwen Mei, Huishi Qiu, Jiang Tian, Zhongchao Shi（联想 AI 技术中心 + 中国科学院数学与系统科学研究院 NCMIS）；NeurIPS 2025 主会；arXiv 2505.12398。

**问题定位**：验证机制沿用了 vanilla speculative decoding 的 **token 级**判据，搬到树上产生两个缺陷：

1. **序列概率 ≠ 逐 token 概率之积**：逐 token 判接受牺牲了全局（序列级）最优性。
2. **自顶向下逐层验证的浪费**：父节点一被拒，其全部子节点被丢弃——但这些子节点可能构成**合法且概率更高**的序列。

**机制**：改为**叶到根（leaf-to-root）**遍历。从叶子出发，若节点被接受，则从该节点到根整条序列一起被接受；若被拒，转去验证其兄弟节点（或其兄弟的最深子节点）；兄弟全被拒则回溯到父节点，直到某节点被接受或全树被拒。父节点只有当其所有子节点都被拒后才被验证，从而最小化草稿浪费。作者称这是"首个用满整棵 token 树的验证算法"。

**理论结果**：证明输出分布与目标模型**完全相同**（无损）；并证明在**单链**情形下该遍历策略理论上最优。

**实验（已公布的正文数字）** **[精读原文]**

- 模型：Llama3 系列与 Llama2；数据集 **Spec-Bench**（多轮对话 / 翻译 / 摘要 / 问答 / 数学推理 / RAG 六类任务）；跨多种树结构。
- 结果：**平均接受长度一致优于 token 级验证 2.2%–5.7%**；作者指出更**深、更大**的解码树可能获得更大增益。
- 定位：plug-and-play，可直接替换既有验证过程，无需改动投机解码流水线的其他部分。

**与 RheoSampling 的分工**：Traversal Verification 改的是**验证的遍历顺序与判据粒度**（序列级），RheoSampling 改的是**建树期的随机性注入 + 验证的概率重分配（OT）**。两者是互补维度，理论上可以叠加（RheoVerification 的 OT 方案与 RRSw 的对比，本身也属于"验证策略"这一维度）。

---

### 3.3 ARC-Decode：把"无损"换成"风险可控"（ICML 2026）**[摘要级]**

**基本信息**：Ying Li, Zhaode Wang, Zhiwen Chen, Chengfei Lv, Huan Wang；ICML 2026 poster；核验页 <https://icml.cc/virtual/2026/poster/66788>。**未找到公开 arXiv 版本**，本报告结论全部来自 ICML 会议页摘要与 Lay Summary，**未读正文**。

**问题定位**：T>0 下观测到的加速比**一贯低于** greedy 设定，原因是经典无损验证规则**过度拒绝低风险草稿**——被拒的草稿虽然与 target 的精确选择不同，但会导向"相似且合法"的续写。

**机制（摘要级）**：

- **训练无关（training-free）**，不需要额外前向传播。
- 通过**风险界定（risk-bounded）**判据放宽接受：识别那些"接受后仍保持 target 输出分布"的草稿，风险用 **Jensen–Shannon 散度**度量，并给出潜在分布偏移的**解析上界**。
- 组合两个部件：**基于置信度的预验证过滤**（先剪掉明显无用的分支，减少浪费的计算）+ **风险界定接受判据**。
- 引入 **Local Tolerance Score** 估计"接受一个被拒草稿是否会显著改变 target 后续行为"，低风险 → 软接受，高风险 → 回退标准验证。
- 集成进 EAGLE-3 流水线后：**接受长度提高、验证计算减少、在采样设定下相对 EAGLE-3 最高 1.6× 端到端加速，跨 benchmark 质量变化可忽略**。

**为什么必须与 §3.1/§3.2 分开读**：ARC-Decode 的"无损"是**有界风险意义下的**（JS 散度受控），不是严格分布等价。它的 1.6× 是**相对 EAGLE-3 的端到端加速**、且限定"under sampling"；RheoSampling 的 2.93× 是**相对自回归解码**的绝对加速比。两个数字不同量纲、不同基准、不同保证等级，**不可相减**。

---

## 4. 综合：无损性的边界条件分类

| 方法/机制 | 随机采样（T>0）支持 | 输出分布保证 | 建树与验证是否解耦 | 证据等级 |
|---|---|---|---|---|
| 经典 draft-then-verify（单链） | ✅ 原生支持 | 严格等于 $p$ | 不涉及树 | — |
| EAGLE-2/EAGLE-3 动态树（原始形式） | ⚠️ 塌缩为 one-hot | 拓扑由 $q$ 排序决定 | ❌ 同一分布两种用途 | [精读原文] |
| 静态树 + 随机采样 | ✅ | 严格（静态拓扑与取值无关） | 部分解耦 | 由 RheoSampling 对比论述 [精读原文] |
| **RheoSampling** | ✅ | **严格等于 $p$**（Theorem 1） | ✅ proxy / 真概率双身份 | [精读原文] |
| **Traversal Verification** | ✅（不改采样语义） | **严格等于 $p$** | 改验证遍历，不动建树 | [精读原文] |
| **ARC-Decode** | ✅（专为采样设计） | **有界风险**（JS 散度上界） | 放宽验证判据 | [摘要级] |

**三条实践含义**：

1. **若产品需要严格可复现的分布等价**（例如对采样分布有审计要求的场景）→ 走 RheoSampling / Traversal Verification 这条线，并在配置中显式记录树宽、深度、$m$、top-$K$ 截断（top-128）等会改变无损性前提的参数。
2. **若接受"质量几乎不变"的工程口径** → ARC-Decode 提供另一条精度-速度前沿，但必须把"有界风险"写进验收标准，不能对外宣称严格无损。
3. **无论走哪条线，指标都要成对报告**（`mean_acceptance_length` + `draft_acceptance_rate` + histogram），否则无法区分"草稿树变深"与"系统变快"。

---

## 5. 尚未确证 / 待跟踪

### 5.1 待办与已核实项（① 已核实；②③ 仍未确证）

> ① 已于 2026-10-16 完成官方代码核验（方式与结论见下表），**可以**作为结论引用；**②③ 仍未确证**，不得写成已成立结论。

| # | 待办 | 状态 | 为什么不写结论 / 下一步怎么做 |
|---|---|---|---|
| **①** | **读 EAGLE 官方代码（`SafeAILab/EAGLE`）确认 top-$K$ 路径下 draft 概率的实际处理方式** | ✅ **已核实（2026-10-16，仓库 @ commit）** | **核验方式**：将 `SafeAILab/EAGLE` clone 到仓库外的临时目录（`/tmp/…`，读完即删；**未进入 `Research` 仓库、未提交任何代码文件**），只读审阅，不修改、不构建。<br>**版本**：`SafeAILab/EAGLE` @ **`cb7e0841fe0c206c6ed74a197ad5e2a1f13f5a2b`**（2026-02-19）。<br>**结论（确实置 1）**：官方参考实现的 **tree / EA 评估路径**把草稿概率按 **1.0** 处理——`eagle/model/utils.py:398` 为 `qx = 1.0`，第 399 行接受判据 `acp = px / qx`，即接受概率退化为目标概率 $p(x)$，草稿分布被当作 one-hot（delta）提议。该函数 `evaluate_posterior` 的调用点：`eagle/model/ea_model.py:270`、`eagle/model/ea_model.py:452`、`eagle/evaluation/gen_ea_alpha_llama2chat.py:87`、`eagle/evaluation/gen_ea_alpha_vicuna.py:93`。<br>**边界（不夸大）**：同一仓库另有 HF 风格实现 `eagle/modeling_eagle.py`——其自带的 `evaluate_posterior` 定义于第 1352 行、调用处第 1698 行，其中第 1427 行使用 `qx = cart_candidates_prob[batch, j, i]`，即**保留真实草稿概率**。因此"草稿概率置 1"是**官方 tree/EA 评估路径**的事实，**不是仓库内所有路径**的共性；这与 SGLang issue #10308 描述的现象（集成侧 tree attention 路径）方向一致。<br>**影响**：§2.1/§3.1 关于"按 $q$ 建树 + 以 $q$ 验证导致 T>0 接受率下降"的链条，在**该实现路径**上成立——接受率由 $p(x)$ 而非 $\min(1,p(x)/q(x))$ 决定，故随机采样下"草稿分布塌缩"的代价有实现层依据；修补位置即该接受判据与提议分布的传递方式（与 ② 的 SGLang 修复方向一致）。 |
| **②** | **SGLang issue #10308 及其后续 PR 是否已合入，以及对 T>0 下动态树行为的影响** | **issue 已确认真实存在；后续 PR 与合入状态未确证** | 核验情况：<https://github.com/sgl-project/sglang/issues/10308> **真实存在**，标题为 *[Feature] Speculative sampling supports passing the predicted probability of the draft model and sample token for verification when **topk=1***，开于 **2025-09-11**（2025-11-03 指派给 `hnyls2002`），于 **2026-01-03 关闭**（API `state_reason=completed`，`closed_by=github-actions[bot]`），**未观察到任何 linked PR / merged PR**。该 issue 正文与本章结论同源：它指出 EAGLE 使用的 tree attention **默认按 top-$K$ 选择 token 并把该 token 概率置 1、其余置 0**，并给出一个算例——**接受概率从标准投机采样的 0.9 降到 tree attention 下的 0.6**。核验边界：**本报告的上述引用仅限该 issue 的页面陈述本身**；**"是否已有修复 PR 合入、以及合入后对 T>0 行为的影响"本轮未确证**，故不作为本报告的结论；检索中出现的若干 topk=1/EAGLE 相关 PR 编号**未能确证其与 #10308 的对应关系**，本报告**不引用任何具体 PR 编号**。下一步：核实该 issue 的后续关联 PR 与当前主线代码行为。**二次核验（2026-10-16）**：直读 issue 页面 <https://github.com/sgl-project/sglang/issues/10308> 确认 2026-01-03 以 `state_reason=completed` 关闭、**无 linked PR/commit**；另检索到与 `topk` 相关的 SGLang PR **#5318**（Eagle3 topk>1）、**#24054**（adaptive speculative decoding 支持 topk>1）、**#26397**（Reland: *Skip full-vocab softmax in EAGLE draft when topk == 1*），但**没有任何一条与 #10308 建立 linked 关系**；其中 #26397 改的是"topk==1 时跳过全词表 softmax"，与 #10308 请求的"**把 draft 预测概率传给验证阶段**"**不是同一变更** → **结论不变：后续修复/合入状态未确证**，本报告不引用这些 PR 编号作为"已修复"证据。 |
| **③** | **RheoSampling 是否放出代码 / 补充材料** | **未确证（目前仅有论文与摘要）** | 本轮只核验到 arXiv 摘要页与全文 HTML；**未发现公开代码仓库、未确认是否有补充材料（Appendix B/C 的算法与证明）之外的 artifact**。因此本报告对 RheoSampling 的所有数字均为**论文自报值**，**未做独立复现**。下一步：检索其 GitHub/HF 是否有官方实现与模型权重。**二次核验（2026-10-16）**：HF Papers 页（`huggingface.co/papers/2609.21827`）返回 **404**（该论文未在 HF 建立页面）；GitHub / HF / Semantic Scholar 检索**未发现官方代码仓库、模型权重或补充材料 artifact**，仅见第三方论文笔记页（`liuzhao09.github.io/papers/rheosampling.html`）→ **结论不变：未放出代码/资料**，所有数字仍为论文自报值、未独立复现。 |

### 5.2 其他未验证项

| 项 | 状态 | 说明 |
|---|---|---|
| RheoSampling 在 greedy（T=0）下的表现 | **未验证** | 论文聚焦 T>0；T=0 下该机制是否退化为 Top-$K$ 等价需读附录 |
| RheoSampling 的 batch / 高并发行为 | **未验证** | 实验为单张 A6000，未见 batch 规模化数据；与 CAST 的"batch 场景边际收益为负"结论是否冲突未知 |
| 与结构化输出约束的耦合 | **未验证** | vLLM 的 `num_draft_tokens` 会扣除被结构化约束作废的草稿，论文未讨论此情形 |
| ARC-Decode 的风险上界是否可外部复核 | **未验证** | 需正文的 JS 上界推导；本报告仅有摘要 |
| ARC-Decode 是否发布了代码/artifact | **未确证** | ICML 页有 Project Page 与 OpenReview 链接，未进一步核验 |
| Traversal Verification 的吞吐绝对值 | **未验证** | 摘要与正文给出的是**相对**接受长度提升（2.2%–5.7%），未见独立复现 |

---

## 6. 链接核验清单（本轮实测，2026-10-16）

| # | 来源 | 链接 | 核验结果 |
|---|---|---|---|
| 1 | RheoSampling, arXiv:2609.21827 | https://arxiv.org/abs/2609.21827 | ✅ HTTP 200，标题/作者/日期/摘要一致；全文 HTML 可读 |
| 2 | RheoSampling 全文 HTML | https://arxiv.org/html/2609.21827v1 | ✅ HTTP 200，本报告 §3.1 机制与定理均据此 |
| 3 | Traversal Verification, NeurIPS 2025 | https://proceedings.neurips.cc/paper_files/paper/2025/hash/70596d70542c51c8d9b4e423f4bf2736-Abstract-Conference.html | ✅ HTTP 200，摘要一致 |
| 4 | Traversal Verification, arXiv:2505.12398 | https://arxiv.org/abs/2505.12398 | ✅ 经 arXiv API 确认标题匹配；全文 HTML 可读 |
| 5 | ARC-Decode, ICML 2026 | https://icml.cc/virtual/2026/poster/66788 | ✅ HTTP 200，摘要 + Lay Summary 一致 |
| 6 | EAGLE-2（背景） | https://ar5iv.labs.arxiv.org/html/2406.16858v1 | ✅ HTTP 200 |
| 7 | vLLM *Per-Request Acceptance Metrics* | https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/ | ✅ HTTP 200，§2.2 口径定义据此 |
| 8 | 指标口径（任务书原引 Morph） | https://www.morphllm.com/speculative-decoding | ⚠️ **被 Vercel Security Checkpoint 拦截（HTTP 429）**，无法核验内容 → 已从正文剔除，改用来源 #7 |
| 9 | SGLang issue #10308（topk=1 下 draft 概率传递；§5.1 待办 ② 的核验对象） | https://github.com/sgl-project/sglang/issues/10308 | ✅ HTTP 200，**issue 真实存在**：标题、开立日期 2025-09-11、指派 `hnyls2002`（2025-11-03）、2026-01-03 关闭（`state_reason=completed`）均已核实；**未观察到 linked/merged PR** → 后续 PR 与修复状态**未确证** |
| 10 | EAGLE 官方仓库（§5.1 ① 的代码核验对象） | https://github.com/SafeAILab/EAGLE | ✅ 只读审阅 @ `cb7e0841fe0c206c6ed74a197ad5e2a1f13f5a2b`（2026-02-19）：`eagle/model/utils.py:398–399`（`qx = 1.0` → `acp = px / qx`），调用点 `eagle/model/ea_model.py:270,452`、`eagle/evaluation/gen_ea_alpha_llama2chat.py:87`、`gen_ea_alpha_vicuna.py:93`；同仓库 `eagle/modeling_eagle.py:1427` 保留真实 `qx`（边界见 §5.1 ①） |

> **任务书失效/存疑链接处置**：第 8 项（Morph）在核验时不可达，本报告不引用其任何具体说法，改以 vLLM 官方文档作为"指标必须成对报告"的依据。ARC-Decode 目前**只有会议页可核验**，无 arXiv 版本，故其全部结论均标为 [摘要级]。第 9 项（SGLang issue #10308）为**本轮新增核验项**，用于支撑 §5.1 待办 ② 的事实基础——仅确证 issue 存在与状态，**不据此推断修复情况**。第 10 项为 **2026-10-16 代码核验**新增：仓库 clone 到 `/tmp`（仓库外）只读审阅、读完即删，`Research` 仓库与提交中**不含任何代码文件**；结论只引用「仓库 @ commit + 文件:行」，不贴大段源码。

---

## 参考文献

| # | 论文 | 年份 / 出处 | 链接 | 证据等级 |
|---|---|---|---|---|
| 1 | RheoSampling, *Resolving the One-Hot Dilemma in Stochastic Dynamic-Tree Speculative Decoding* | 2026-09-18, arXiv 2609.21827 | https://arxiv.org/abs/2609.21827 | **精读原文** |
| 2 | Traversal Verification, *Traversal Verification for Speculative Tree Decoding* | NeurIPS 2025 | https://proceedings.neurips.cc/paper_files/paper/2025/hash/70596d70542c51c8d9b4e423f4bf2736-Abstract-Conference.html | **精读原文**（arXiv:2505.12398） |
| 3 | ARC-Decode, *Accelerated Decoding with Risk-Bounded Acceptance* | ICML 2026 poster | https://icml.cc/virtual/2026/poster/66788 | 摘要级 |
| 4 | EAGLE-2（动态草稿树背景） | EMNLP 2024 | https://arxiv.org/abs/2406.16858 | 精读原文（背景） |
| 5 | EAGLE-3（被本章限定的对象） | NeurIPS 2025 | https://arxiv.org/abs/2503.01840 | 精读原文（背景） |
| 6 | vLLM, *Per-Request Acceptance Metrics* | 官方文档（latest dev preview） | https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/ | **精读原文** |

---

> **报告说明**：本报告按**单一主等级**标注证据（精读原文 / 摘要级 / 二手 / 受限核验；混合来源取最弱等级，来源类型写在括号里）。RheoSampling 与 Traversal Verification 的关键结论已基于正文逐节核对；ARC-Decode 仅有 ICML 会议页可核验，全部标为摘要级，**未读正文**。§5.1 第 ① 项已于 2026-10-16 完成官方代码核验（`SafeAILab/EAGLE` @ `cb7e0841…`，`eagle/model/utils.py:398–399`），结论与边界见该表。加速比与接受长度数字均为论文自报值，跨论文、跨设定不可直接比较。
>
> *数据截至 2026-10-16。*
