# 投机解码：领域与语种特化

> ⚠️ **信息来源声明**：本报告由 AI Agent 基于公开论文、会议 proceedings（ACL Anthology、NAACL、IEEE SSE）、GitHub 开源 PR 与 arXiv 预印本整理生成。本领域**存在大量未经同行评审的工程实践**，相关条目已逐条标注证据等级，请勿把工程博客/PR 描述等同于已验证结论。
>
> **调研日期**：2026 年 10 月（本轮新增）
> **本文定位**：本文是《投机解码技术深度调研报告》的子报告之一，聚焦**非拉丁语系**与**结构化/受限输出**这两类领域特化场景，回答同一个问题：**在什么条件下，检索式/字典式/无训练草稿比模型式草稿更有优势？** 与 [speculative-block-diffusion.md](speculative-block-diffusion.md)（检索式方法）、[speculative-stochastic-verification.md](speculative-stochastic-verification.md)（受限输出下的指标口径）交叉。
> **证据等级约定**：**[精读原文]**、**[摘要级]**、**[二手]**、**⚠️[受限核验]**。

---

## 1. 本章结论

1. **非拉丁语系的核心矛盾是"分词肥度（tokenizer fertility）"**：乌克兰语或克里米亚鞑靼语中的一个词，被切成 **英文等价词的 2–3 倍 token**。同一句话要验证的 token 数成倍增加，投机解码的收益空间与代价结构都被改变。 **[精读原文]**
2. **字典式草稿（DictSpec）在低资源语种上的收益与分词肥度强相关**。离线从未标注语料构建的静态 n-gram 查找表：**无训练参数、无 GPU 需求、内存开销 <5 MB、可在共享 tokenizer 的模型间复用**。受控仿真中**验证步数最多减少 1.65×**，且**增益与 tokenizer fertility 显著相关**。 **[精读原文]**
3. **但在真实服务中，纯字典式收益"温和"**；反而是**"字典式 + prompt-local n-gram 投机"的混合方案**达到最高 **1.76×**。这是一个重要的工程边界：**字典法不是替代品，而是补丁**——它补的是"模型式 drafter 对低资源语种覆盖不足"这个洞，而不是全面超越模型式 drafter。 **[精读原文]**
4. **受限/结构化输出场景下，草稿的"无效 token"必须在指标口径里被扣除**。vLLM 的 `num_draft_tokens` 定义明确写着"**已扣除被结构化输出约束作废的草稿**"——这意味着**开启语法约束后，acceptance rate 的分母会变**，与不加约束的实验**不可直接对比**。 **[精读原文]**
5. **"受限解码"与"投机解码"合流的两条不同路径**：
   - **把约束纳入草稿生成**：vLLM PR #47885 "grammar-aware draft token sampling"，让草稿采样阶段就遵守语法，避免产出必然被作废的草稿。 **[二手（PR 标题级）]**
   - **把约束纳入验证/奖励**：CDSL（NAACL 2025）用 target LLM + **任务特定奖励函数**共同验证草稿，把原本昂贵的 lookahead roll-out 变成一次投机验证，在两类约束解码任务上相对 CDLH 取得 **2.2×–12.15× 加速**且性能无显著下降。 **[精读原文]**
6. **领域特化的通用判断**：当目标领域的输出**高度模板化/可枚举**（代码片段、JSON/SQL 结构、格式化字段、重复引用）时，**检索/字典式草稿的单位成本优势最大**；当领域输出**语义自由度高**时，模型式 drafter（EAGLE 系、MTP）仍然占优。 **[综合判断，非单一论文结论]**

---

## 2. DictSpec：非拉丁语系的字典式草稿（ACL 2026）**[精读原文]**

**基本信息**：Oleksiy Syvokon；*Dictionary-Based Speculative Decoding for Non-Latin-Script Languages*；ACL 2026（UNLP workshop 轨道）；核验页 <https://aclanthology.org/2026.unlp-1.15/>。

> **作者说明**：ACL Anthology 页面为该论文的**唯一署名作者**（Oleksiy Syvokon）。本报告如实标注。

### 2.1 问题：分词肥度

> 大语言模型对非拉丁文字语言的分词效率低下：**一个乌克兰语或克里米亚鞑靼语的单词，会被切成英文等价词的 2–3 倍 token 数。**

这个观察有双重含义：
- **直接代价**：同一句内容需要更多次解码步 → 基线自回归更慢；
- **投机解码的代价结构被改变**：需要验证的 token 数成倍增加，**验证阶段（target 前向）而非草稿阶段成为支配项** → 单位草稿收益的杠杆被放大。

### 2.2 机制：DictSpec

| 属性 | 内容 |
|---|---|
| 草稿来源 | **静态 n-gram 查找表**，**离线**从**未标注语料**构建 |
| 训练参数 | **无**（no trainable parameters） |
| GPU 需求 | **无** |
| 内存开销 | **<5 MB** |
| 复用性 | 可**跨共享同一 tokenizer 的模型**复用 |

### 2.3 实验（论文自报）

| 设置 | 内容 |
|---|---|
| 语种 | 乌克兰语（西里尔字母）、克里米亚鞑靼语（同时涉及西里尔与拉丁字母） |
| 实现 | **vLLM 插件** |
| 模型 | **5 个模型，3B 到 70B** |
| 硬件 | 消费级 + 服务器级 GPU |
| 结果 1（受控仿真） | **验证步数最多减少 1.65×**，**增益与 tokenizer fertility 显著相关** |
| 结果 2（真实 vLLM 服务） | 纯 DictSpec 收益**温和** |
| 结果 3（混合方案） | **DictSpec + prompt-local n-gram 投机 → 最高 1.76×** |
| 开源 | 代码与 vLLM 插件开源 |

### 2.4 本报告对该工作的解读（标注为推断）

- "受控仿真 1.65×"与"真实服务 1.76×（混合）"这两个数字**不可直接比较**：前者是验证步数减少的仿真值，后者是真实服务的端到端加速，混合方案还额外引入了 prompt-local n-gram 组件。**要判断 DictSpec 本身的贡献，应看纯 DictSpec 的真实服务收益（论文描述为"温和"）。**
- 论文明确指出**增益与 tokenizer fertility 相关** → 这条结论可外推为一句话操作规则：**先测你的目标语种在目标 tokenizer 下的肥度，再决定是否引入字典式草稿**。

---

## 3. 代码与结构化输出的草稿实践

### 3.1 受限解码 + 投机解码的合流（CDSL, NAACL 2025）**[精读原文]**

**基本信息**：*Constrained Decoding with Speculative Lookaheads* (CDSL)；NAACL 2025 Long；DOI `10.18653/v1/2025.naacl-long.239`；核验页 <https://aclanthology.org/2025.naacl-long.239/>。

**问题**

- **CDLH**（constrained decoding with lookahead heuristics）是让 LLM 生成对齐人类偏好的高效方法，但**每个生成 token 都要做大量 lookahead roll-out** → 代价高到无法实用。
- 与之相对，**贪心解码**极快，但**约束满足率极低**。

**机制**

CDSL 借用投机解码的框架，但改变了"验证"的含义：

| 角色 | 传统投机解码 | CDSL |
|---|---|---|
| 草稿 | 小 draft LLM 生成候选 token | 小 draft LLM 生成 **lookahead** |
| 验证 | target LLM 单次并行前向验证 | **target LLM + 任务特定奖励函数**的组合验证 |

即：把"昂贵的 lookahead roll-out"整体替换为"一次投机 + 奖励函数验证"，从而**减少计算负担而不牺牲性能**。

**实验（论文自报）**

- 两个约束解码任务 × 三个 LLM 家族
- 相对 CDLH 取得 **2.2×–12.15× 加速**，**无显著性能下降**

**为什么这属于"领域特化"章节**：CDSL 是**约束（领域）驱动的投机解码**——它的验证判据不是纯分布等价，而是"分布 + 任务奖励"。这与 [speculative-stochastic-verification.md](speculative-stochastic-verification.md) 中 ARC-Decode 的"有界风险"同属**放宽严格无损**的一类，但放宽的依据不同（ARC 用分布散度上界，CDSL 用任务奖励）。

### 3.2 语法感知的草稿采样（vLLM PR #47885）**[二手（PR 标题级）]**

- **标题**：`feat(spec_decode): Grammar-aware draft token sampling for structured outputs`
- **仓库**：vllm-project/vllm；**PR**: #47885；核验页 <https://github.com/vllm-project/vllm/pull/47885>（页面可达，但本报告**仅核验了标题与存在性，未读取代码 diff 与讨论**）
- **含义（推断）**：在**草稿采样阶段**就应用语法约束，避免产出"必然被约束作废"的草稿 token，从而提升有效接受率、减少浪费的验证计算。
- **⚠️ 本报告不据此展开任何量化结论。** 该 PR 的状态（是否合并、影响哪个版本）未核验。

### 3.3 受限输出改变指标口径（vLLM 官方文档）**[精读原文]**

vLLM 的 *Per-Request Acceptance Metrics* 文档在 `num_draft_tokens` 字段的定义里明确写了：

> "Total proposed draft tokens, **after subtracting drafts invalidated by structured-output constraints**."

**这条口径细节的实际影响**：

| 场景 | `num_draft_tokens` | `draft_acceptance_rate` 分母 | 可比性 |
|---|---|---|---|
| 无约束 | 全部提议草稿 | 全部提议 | 基准 |
| 有语法/结构化约束 | **扣除被约束作废的草稿** | **变小** | **与无约束实验不可直接对比** |

> **工程建议**：在报告结构化输出场景的加速比时，必须同时声明（a）是否启用约束，（b）约束类型（JSON Schema / 正则 / EBNF 语法），（c）`num_draft_tokens` 是否已按上述规则扣除。否则 acceptance rate 的跨实验比较没有意义。

### 3.4 专用框架动向（Tencent AngelSpec）**[二手]**

检索中出现开源动向报道：**Tencent 开源 AngelSpec 投机解码框架**（开源媒体报道，2026-08）。**本报告未取得一手仓库页面并核验其能力范围，故不据此展开任何技术结论**，仅作为"专用框架开始出现"的线索登记。

---

## 4. 领域特化的选型表

| 场景特征 | 推荐草稿路线 | 依据 | 证据等级 |
|---|---|---|---|
| 非拉丁语系、tokenizer 肥度高 | **字典式（DictSpec）+ prompt-local n-gram 混合** | 增益与 fertility 显著相关；混合方案真实服务 1.76× | 精读原文 |
| 非拉丁语系、但有现成同族小模型 | 模型式 drafter 仍优先 | 论文未对角；模型式 drafter 有语义泛化能力 | 推断 |
| 结构化输出（JSON / SQL / 固定 schema） | **语法感知草稿** + 严格声明指标口径 | `num_draft_tokens` 会扣除作废草稿 | 精读原文（口径）+ 二手（PR） |
| 受限生成（偏好对齐 / 约束满足） | **草稿 + 任务奖励函数验证（CDSL）** | 相对 CDLH 2.2×–12.15× | 精读原文 |
| 高度重复的引用/模板文本 | **检索式 / prompt-local n-gram** | REST/PLD 的既有结论，见 [block-diffusion 章节](speculative-block-diffusion.md) | 既有报告 |
| 语义自由度高的开放对话 | **模型式 drafter（EAGLE / MTP）** | 检索式在无重复场景命中率低 | 既有报告 |

---

## 5. 尚未确证 / 待跟踪

| 项 | 状态 | 说明 |
|---|---|---|
| DictSpec 在中文/日文/韩文上的表现 | **未验证** | 论文仅覆盖乌克兰语与克里米亚鞑靼语 |
| DictSpec 的 <5 MB 内存是否随语种规模线性增长 | **未验证** | 摘要给出单点数值，未给增长规律 |
| vLLM PR #47885 是否已合并及影响范围 | **未验证** | 仅核验标题存在，未读 diff/讨论 |
| CASD（IEEE SSE 2026, `document/11664971`） | **⚠️受限核验** | IEEE 页面被反爬拦截；仅确证标题与会议归属，**未取得摘要** |
| AngelSpec 的能力范围与指标 | **未验证** | 仅二手媒体报道 |
| CDSL 是否与模型式 drafter（EAGLE）叠加 | **未验证** | 论文使用小 draft LLM，未与 EAGLE 组合实验 |

---

## 6. 链接核验清单（本轮实测，2026-10-16）

| # | 来源 | 链接 | 核验结果 |
|---|---|---|---|
| 1 | DictSpec, ACL 2026 | https://aclanthology.org/2026.unlp-1.15/ | ✅ HTTP 200，标题/作者/摘要一致 |
| 2 | CDSL, NAACL 2025 | https://aclanthology.org/2025.naacl-long.239/ | ✅ HTTP 200，标题/摘要/DOI `10.18653/v1/2025.naacl-long.239` 一致 |
| 3 | vLLM PR #47885（grammar-aware draft sampling） | https://github.com/vllm-project/vllm/pull/47885 | ✅ HTTP 200（仅核验标题与存在性） |
| 4 | vLLM 验收指标口径 | https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/ | ✅ HTTP 200，`num_draft_tokens` 定义已核实 |
| 5 | CASD, IEEE SSE 2026 | https://ieeexplore.ieee.org/document/11664971 | ❌ **HTTP 202 空响应（IEEE 反爬拦截）** → 未取得摘要，仅登记标题与会议归属 |
| 6 | Tencent AngelSpec（二手报道） | https://www.opensourceforu.com/2026/08/tencent-open-sources-angelspec/ | ⚠️ 二手来源，未取一手仓库页面 |

> **失效/受限链接处置**：第 5 项（CASD）因 IEEE 反爬拦截无法核验内容，**本报告不引用其任何技术细节**，仅在 §5 登记为待跟踪项。第 6 项为二手媒体报道，同样不展开技术结论。

---

## 参考文献

| # | 论文 / 来源 | 年份 / 出处 | 链接 | 证据等级 |
|---|---|---|---|---|
| 1 | DictSpec, *Dictionary-Based Speculative Decoding for Non-Latin-Script Languages* | ACL 2026 (UNLP) | https://aclanthology.org/2026.unlp-1.15/ | 精读原文 |
| 2 | CDSL, *Constrained Decoding with Speculative Lookaheads* | NAACL 2025 Long | https://aclanthology.org/2025.naacl-long.239/ | 精读原文 |
| 3 | vLLM PR #47885, *Grammar-aware draft token sampling for structured outputs* | 开源 PR | https://github.com/vllm-project/vllm/pull/47885 | 二手（标题级） |
| 4 | vLLM, *Per-Request Acceptance Metrics*（口径依据） | 官方文档 | https://docs.vllm.ai/en/latest/features/speculative_decoding/acceptance_metrics/ | 精读原文 |
| 5 | CASD, *A Contract-Aware Speculative Decoding Method for Constrained Output Generation* | IEEE SSE 2026 | https://ieeexplore.ieee.org/document/11664971 | ⚠️受限核验（仅登记） |
| 6 | REST / PLD（检索式方法背景） | NAACL 2024 / 2023 | https://arxiv.org/abs/2311.08252 | 既有报告 |

---

> **报告说明**：本报告结论按证据等级标注，并区分「本环境无法直接核验」的情况。DictSpec 与 CDSL 的关键数字来自 ACL Anthology 一手页面；vLLM PR 仅为标题级核验；CASD 与 AngelSpec 未取得一手内容，故不展开结论。所有加速比数字为论文自报值，**受控仿真值与真实服务值不可直接比较**。
>
> *数据截至 2026-10-16。*
