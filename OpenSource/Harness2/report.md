---
display_name: Harness²
type: repo-research
domain: Repo-Research
subject: Harness2
upstream: https://github.com/google-research/harness2@1cfe254e8d25b15f37048c3730134686abe60335
date: 2026-10-28
evidence: 精读原文
status: completed

---

# Harness²：把 harness 本身作为优化对象

论文：*Harness²: Recursive Agent Harnessing for an Open World*（arXiv:2610.14224v1，2026-10-09）。代码：`google-research/harness2` @ `1cfe254`（2026-10-13，Python，`harness2/` 39 文件 / 12,747 行）。

## 1. 它做什么

把"模型外围的提示、工具、记忆、技能、编排"当作**可编辑的优化对象**，用**两级递归**分别改"当前任务的执行 harness"和"改进 harness 本身"。

- **任务级递归**（改执行 harness）：一步 = `Propose → Probe → Compose`。先跑一次**参照执行**（得到基线轨迹与交付物，不判断对错），再提**两个候选**——`INV`（跨域复发的 agent 缺陷：规划、工具使用、上下文管理、委派）与 `DOM`（当前领域的知识、流程、约束）；两候选在**同模型同环境**下跑同一任务，与参照做**行为对照**；最后**选择性合成**（合并受支持改动、修正冲突、采纳其一或保留原状），**每个决策绑定一个具体观察**。`k=1` 即单步；`k>1` 时并行（k 候选 × k 合成会话）或顺序（k 步链式），并在末轮由 selector 只"挑现有交付物"、不重写。
- **harness 级递归**（改"改进 harness"）：任务结束后回看完整改进记录，**只有被执行对照支撑的经验**才写入 `EXPERIENCE.md` 并入索引库；下一任务仍从**公共初始 harness** 起步，旧组件**经 Propose 选择性复用**而非自动继承（`core/library.py`）。

**八个组件各是一个文件**，编辑即 diff（论文 Table 5 / §D.3；代码 `substrate/opencode.py:42-88`）：

| 编号 | 组件 | 文件 | 何时进入上下文 |
|---|---|---|---|
| C1 | System prompt | `systemprompt.md` | 每次调用 |
| C2 | Guardrails | `guardrails.md` | 每次调用 |
| C3 | Memory | `LongTermMEMORY.md` | 每次调用 |
| C4 | Tool guidance | `tool_descriptions/tool_guidance.md` | 每次调用 |
| C5 | Subagents | `sub_agents/<n>/AGENT.md` | task 工具调用时（唯一新增推理上下文） |
| C6 | Skills | `skills/<n>/SKILL.md`（+`scripts/`） | 被 skill 工具按需加载 |
| C7 | Scripts | `scripts/<n>.py` | 经 bash 执行 |
| C8 | Plugin | `plugin/<n>.ts`（Codex 下为 `.codex/hooks.json`） | 工具循环内 |

## 2. 结果与口径

**先看口径，再看数字**：执行器（solver）**冻结**为 Gemini 3.5 Flash 与 GLM-5，套在两个现成外壳（OpenCode / Codex）上，共四配置；**论文的 harness editor 是 Claude Opus 4.8（跑在 OpenCode 上）**；主表是**单步 `k=1`**，`+ Recursion` 行是**并行 `k=5`**；经验库每个基准流**从空开始**、逐任务更新；三次运行、任务顺序打乱、报均值（标准差）。

| 执行器 / 外壳 | WorkBuddy-Bench Avg（base → 单步） | JobBench Score | LAB Partial |
|---|---|---|---|
| Gemini 3.5 Flash / OpenCode | 72.4 → **77.5**（+5.1） | 31.5 → **36.0**（+4.5） | 79.9 → **81.9** |
| Gemini 3.5 Flash / Codex | 74.5 → **77.5**（+3.0） | 33.9 → **35.3** | 71.6 → **75.6** |
| GLM-5 / OpenCode | 64.2 → **75.7**（+11.5） | 20.6 → **24.2** | 59.6 → **71.4**（+11.8pp） |
| GLM-5 / Codex | 64.4 → **75.3**（+10.9） | 23.6 → **24.8** | 58.1 → **65.9** |

（论文 Table 1/2；`+ Recursion`（k=5）在 WorkBuddy-Bench 再加 1.6–4.8，JobBench 再加 3.0–4.2，LAB 再加 2.6–6.7。）

**读这张表要注意三件事**：

1. **"最高 +11.5 / +11.8pp" 来自最弱的 base**（GLM-5/OpenCode 的 64.2 与 59.6）。同一个方法对强 base（Gemini/OpenCode 72.4）只有 +5.1，LAB 上只有 +2.0。**增益与 base 起点强相关**，不能当"通用提升幅度"引用。
2. **有一格没赢**：LAB Partial 上 Gemini 3.5 Flash / Codex 配置，离线搜参的 Meta-Harness 为 76.5，高于 Harness² 单步 75.6。**离线（用训练任务搜一次再部署）与在线递推不是同一资源约束**，跨类比较须注明。
3. **消融说明增益来自结构而非运气**（Gemini/OpenCode，k=1）：去掉经验库 −3.1 / −1.8，去掉 INV-DOM 分工 −2.9 / −3.7，去掉合成（改回"二选一"）−1.6 / −1.9（WorkBuddy / JobBench）。

**失效边界（论文自述）**：额外算力（propose/probe/compose 都是真执行，并行只降时延不降成本）；行为对照受**执行随机性**与**共享模型偏差**影响，**不保证正确性、也不保证迁移**；"恒定"类收益有前提——在 Harness² 里对应的是**递归预算与库作用域**，论文只刻画有限预算区间，没有普适最优。

## 3. 论文与代码的九条差异

**D7 / D8 / D9 置顶**：这三条会让"照论文复现"直接失败，或让基线本身位移。

| # | 论文/文档说法 | 代码实际 | 定位 | 性质 |
|---|---|---|---|---|
| **D7** | §3.1：默认 editor = Claude Opus 4.8（OpenCode） | **默认 editor = solver 同一模型**：`IMPROVER_MODEL = env("HARNESS2_IMPROVER_MODEL", SOLVER_MODEL_OC)`，通道默认 opencode | `config.py:99-101,174-175` | **默认值不同**：不显式设环境变量，复现出的是"自己改自己"，不是"Opus 改 GLM" |
| **D8** | 称 continual / persistent improvement harness | 库根按 **run + mode** 分作用域（`<base>/<bench>/k<k>[-variant]`），**每个 sweep 每个域从空开始**；跨 sweep 共享须显式 `tag` | `core/library.py:21-23,215-222` | **语义差**：默认只是"单次 sweep 内持续"，不是跨任务长期累积 |
| **D9** | 只提 OpenCode / Codex 两个 substrate | `install_mode` 三种投递通道（JB / WB / LAB）**不可互换**，docstring 明写"换一条就把该基准的基线挪了"；`home_dir_jinja` 还要求恰好一个末尾 `{{ instruction }}` | `substrate/opencode.py:17-24,93,99-110` | 论文未述，但**直接动基线** |
| D3 | 全文 0 次提及 `hooks.json` | C8 在两种 substrate 是**两种机制**：OpenCode 用 `plugin/<n>.ts`（插件目录），Codex 用 `.codex/hooks.json`（10 个生命周期事件、Claude-Code hook schema） | `opencode.py:62,77-80`；`codex.py:57-72`；`prompts.py:431` vs `:480` | 论文未述（仓库实现） |
| D4 | "on-demand 组件相同"（暗示可迁移） | 技能命名规则**相反**：OpenCode `must_match`（frontmatter `name:` 必须等于目录名），Codex `overrides_dir`（`name:` **覆盖**目录名）。同一棵树换 substrate 会**静默失效**，两种规则报错文案都不同 | `opencode.py:53`；`codex.py:48`；`core/tree.py:277-291` | 论文未述，属**能力差异**（最危险） |
| D5 | 未提校验强度差异 | 技能自带脚本：OpenCode **不**做 `py_compile`（默认 False），Codex 做（True） | `core/tree.py:57,364-370`；`codex.py:73` | 论文未述（仓库实现） |
| D6 | 预算以 R=4k 表述 | 并行模式下 k 个 finals **在合成之后仍各跑一次**（`_roll_many`），顺序模式每轮合成后同样再跑一次 → **R 里含"合成后再验证"的 rollout**；论文未说明是否计入 | `core/recursion.py:303`（定义）、`:393/:436/:519`（调用） | **口径差异**（论文措辞与实现不同，读"预算-增益"曲线时须核对） |
| D2 | §D.1「Codex 下 always-on 文本住在 `AGENTS.md`，on-demand 组件相同」 | 八个逻辑组件在 Codex **塌缩成 5 个物理落点**：`AGENTS.md` / `.agents/skills/` / `sub_agents/` / `scripts/` / `.codex/hooks.json` | `substrate/codex.py:39-74` | 论文未述；"5 个落点"为**推断**（数 surface 字段得出，论文无对应句） |
| D1 | Table 5：C2 = Guardrails `guardrails.md` | 注释把 `guardrails.md` 标成 **c6**，全仓再无 c2 | `core/prompts.py:425` | **仓库笔误**（不影响行为） |

## 4. 想改它，先知道哪里不能碰

- **跨 substrate 迁移会静默失效（D4）**：技能 `name:` 规则相反，迁过去不报错、只在加载期丢技能。改 substrate 前先跑一遍技能加载并核对数量。
- **`install_mode` 不是"打包方式"（D9）**：它决定 always-on 文本**投到哪个通道**，换一条就把基准的 base 分数挪了——想做纵向对比必须锁定同一个 mode。
- **别把评测口径写进上下文**：`GRADER_VERDICT_MARKERS` 含 `"pass_rate"` / `"test_pass_rate"` / `"passed_count"` 等字面量，`assert_no_grader_verdicts` 在 harness 树、`EXPERIENCE.md`、合成与选择阶段都会检查（`core/context.py:419-427,454,493`；调用点 `core/library.py:122-123`、`core/selection.py:504`、`core/recursion.py:129`）。往上下文里塞分数会**直接抛 `ValueError`**，这是防"评委结论泄进方法侧"的绊线。
- **复现论文配置要显式设置 `HARNESS2_IMPROVER_MODEL`（D7）**，否则 editor 与 solver 同模型，得到的增益含义不同。
- **跨 sweep 的"持续改进"不是默认行为（D8）**：要长期库，必须显式走 `tag`，且注意库按 bench 分作用域。

## 5. 许可（三段分开看）

- **论文**：arXiv 元数据标 **CC BY 4.0**（abs 页许可图标；正文 PDF 无许可声明）。
- **仓库**：**Apache-2.0**（`LICENSE`、`pyproject.toml`；仓内无 CC BY 提及）。
- **第三方 runner**（`dependencies/`）：Job-Bench **Apache-2.0**、harvey-labs **MIT**、opencode **MIT**；**WorkBuddy-Bench 为腾讯自定义许可，含欧盟地区使用限制**——这是**可用性风险**，与开源许可证不是一回事，落地前要单独核。

**未确证**：论文未说明 D6 的 R 是否含"合成后再验证"的 rollout（只能从代码读出实现包含）；Codex 的"5 个物理落点"是从 surface 字段数出的推断；`third_party/` 与 `docs/` 未逐节读。
