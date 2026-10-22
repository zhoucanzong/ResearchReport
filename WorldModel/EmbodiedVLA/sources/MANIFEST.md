# 原文清单 · EmbodiedVLA

> 本仓库**只存清单与本条目的精读分册**（`papers/*.md`），**不存论文全文**（PDF 或转出的 markdown / txt 都不入库）。
> 需要回看原文时：按下面的 arXiv 链接现取。**本地缓存路径**：`~/Documents/paper-cache/<arXiv-ID>@latest/`（**仓库外、不入库**），内含 `<ID>.pdf`、`<ID>.txt`（`pdftotext -layout` 提取）与 `meta.json`（题名 / 版本 / 日期 / 第一作者 / SHA256）。**本清单不依赖缓存存在**。

## 1. 精读的 11 篇（主等级 `[精读原文]`）

| # | 分册（我们的精读） | arXiv ID | 版本 | 版本日期（正文首页照抄） | 标题（arXiv 元数据，逐条核实） | 第一作者（核实） | license（`arxiv.org/abs` 页核验） | 出处 / 本地缓存 |
| --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | [`papers/2303.04137-diffusion-policy.md`](<../papers/2303.04137-diffusion-policy.md>) | 2303.04137 | v5 | 2024-03-14（v1 2023-03-07，`published` 字段） | Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | Chi, Cheng | arXiv 默认「永久非独占许可」（页内无 CC 标识） | https://arxiv.org/abs/2303.04137 ｜ 缓存命中 `~/Documents/paper-cache/2303.04137@latest/` |
| 2 | [`papers/2307.15818-rt2.md`](<../papers/2307.15818-rt2.md>) | 2307.15818 | v1 | 2023-07-28 | RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control | Brohan, Anthony | arXiv 默认「永久非独占许可」（页内无 CC 标识） | https://arxiv.org/abs/2307.15818 ｜ 缓存命中 `~/Documents/paper-cache/2307.15818@latest/` |
| 3 | [`papers/2310.08864-open-x-embodiment.md`](<../papers/2310.08864-open-x-embodiment.md>) | 2310.08864 | v9 | 2025-05-14（v1 2023-10-13） | Open X-Embodiment: Robotic Learning Datasets and RT-X Models | Open X-Embodiment Collaboration | CC BY 4.0 | https://arxiv.org/abs/2310.08864 ｜ 缓存命中 `~/Documents/paper-cache/2310.08864@latest/` |
| 4 | [`papers/2406.09246-openvla.md`](<../papers/2406.09246-openvla.md>) | 2406.09246 | v3 | 2024-09-05（v1 2024-06-13） | OpenVLA: An Open-Source Vision-Language-Action Model | Kim, Moo Jin | CC BY 4.0 | https://arxiv.org/abs/2406.09246 ｜ 缓存命中 `~/Documents/paper-cache/2406.09246@latest/` |
| 5 | [`papers/2410.24164-pi0.md`](<../papers/2410.24164-pi0.md>) | 2410.24164 | v4 | 2026-01-08（v1 2024-10-31） | π0: A Vision-Language-Action Flow Model for General Robot Control | Black, Kevin | arXiv 默认「永久非独占许可」（页内无 CC 标识） | https://arxiv.org/abs/2410.24164 ｜ 缓存命中 `~/Documents/paper-cache/2410.24164@latest/` |
| 6 | [`papers/2501.09747-fast.md`](<../papers/2501.09747-fast.md>) | 2501.09747 | v1 | 2025-01-16 | FAST: Efficient Action Tokenization for Vision-Language-Action Models | Pertsch, Karl | CC BY 4.0 | https://arxiv.org/abs/2501.09747 ｜ 缓存命中 `~/Documents/paper-cache/2501.09747@latest/` |
| 7 | [`papers/2403.12945-droid.md`](<../papers/2403.12945-droid.md>) | 2403.12945 | v2 | 2025-04-22（v1 2024-03-19） | DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset | Khazatsky, Alexander | CC BY 4.0 | https://arxiv.org/abs/2403.12945 ｜ **本轮新抓**：`paper-fetcher` `download` + `pdftotext -layout`，缓存 `~/Documents/paper-cache/2403.12945@latest/` |
| 8 | [`papers/2405.05941-simpler.md`](<../papers/2405.05941-simpler.md>) | 2405.05941 | v1 | 2024-05-09 | Evaluating Real-World Robot Manipulation Policies in Simulation | Li, Xuanlin | CC BY 4.0 | https://arxiv.org/abs/2405.05941 ｜ 缓存命中 `~/Documents/paper-cache/2405.05941@latest/` |
| 9 | [`papers/2511.14759-pi-star-0.6-recap.md`](<../papers/2511.14759-pi-star-0.6-recap.md>) | 2511.14759 | v2 | 2025-11-19 | $π^{*}_{0.6}$: a VLA That Learns From Experience | Physical Intelligence | arXiv 非独占分发许可 | [arXiv v2 HTML](https://arxiv.org/html/2511.14759v2) ｜ arXiv v2 全文 HTML 核读；PaperFetcher PDF 请求未完整结束 |
| 10 | [`papers/2608.16978-vlcp.md`](<../papers/2608.16978-vlcp.md>) | 2608.16978 | v1 | 2026-08-17 | VLCP: Vision Language Control Policy Closed-Loop Code Replanning for Robot Manipulation | Naouali, Dhia | CC BY 4.0 | [arXiv v1 HTML](https://arxiv.org/html/2608.16978v1) ｜ PaperFetcher 下载 PDF + `pdftotext -layout`；临时提取物已读后清理，报告未收录全文 |
| 11 | [`papers/2601.21998-lingbot-va.md`](<../papers/2601.21998-lingbot-va.md>) | 2601.21998 | v2 | 2026-03-22 | Causal World Modeling for Robot Control | Li, Lin | CC BY 4.0 | [arXiv v2 HTML](https://arxiv.org/html/2601.21998v2) ｜ PaperFetcher 下载 PDF + `pdftotext -layout`；临时提取物已读后清理，报告未收录全文 |

### 1.1 版本日期口径说明（重要）

- **「版本日期」取自论文 PDF 首页照抄的 `arXiv:<ID>v<N> [...] <d Mmm yyyy>` 行**，即**该版本的发布日期**，是引用时应写出的日期。
- arXiv Atom API 的 `published` 字段返回的是 **v1 的提交日期**；两者**在 v1 时相同、在后续版本时不同**（例：DROID v2 的版本日期 2025-04-22 而 `published`=2024-03-19；π0 v4 版本日期 2026-01-08 而 `published`=2024-10-31）。表中已同时标出，避免混用。
- 同一论文的后续版本可能修改结论；**引用具体数字时以本表版本为准**。

## 2. 抓取与核验方式（可复现）

| 环节 | 做法 | 证据 |
| :-- | :-- | :-- |
| 缓存优先 | 先查 `~/Documents/paper-cache/<ID>@latest/`，**命中即读、不重复下载** | 原 8 篇中 7 篇命中既有缓存；VLCP 与 LingBot-VA 经 PaperFetcher 临时下载 / 抽取，读完清理 |
| 未命中才抓 | 原 DROID 与本轮 VLCP / LingBot-VA 缓存未命中 → `paper-fetcher` skill 取原文 | `/Users/zhoucanzong/Documents/codes/paper-fetcher/skills/paper-fetcher/scripts/fetch_paper.py download` |
| 文本提取 | 已下载论文用 `pdftotext -layout <ID>.pdf <ID>.txt`；RECAP 由 arXiv v2 全文 HTML 核读 | 新批次 VLCP / LingBot-VA 临时文本；RECAP PDF 请求未完成 |
| 元数据核实 | arXiv abs 页逐条核对**题名 + 当前版本 + 版本日期**；RECAP 的 PDF 请求未完成，以 arXiv v2 HTML 版日期为准 | 本文表格第 4–6 列 |
| license 核实 | `arxiv.org/abs/<ID>` 页内 `creativecommons.org/licenses/...` 标识 | 本文表格 license 列（**7 篇 CC BY 4.0 / 4 篇 arXiv 默认许可**） |

### 2.1 本批次调研技能与可检查产物

| 技能 | 使用记录 | 仓库内证据 |
| :-- | :-- | :-- |
| `researcher`（deep） | 按深度调研流程筛选闭环候选、精读入选工作并逐篇回答七问；对应本机入口 `/Users/zhoucanzong/Documents/codes/researcher/skills/researcher/SKILL.md` | 本批次工作记录见 [`report.md` §14.8](../report.md)；四行亮点与七问见三篇新增分册 |
| `paper-fetcher` | 使用 `fetch_paper.py download` 获取 VLCP 与 LingBot-VA PDF，并用 `pdftotext -layout` 提取；RECAP PDF 下载未完成，改核读 arXiv v2 全文 HTML | 脚本：`/Users/zhoucanzong/Documents/codes/paper-fetcher/skills/paper-fetcher/scripts/fetch_paper.py`；逐篇版本和来源见本表第 9–11 项 |

> **核验范围**：RECAP、VLCP、LingBot-VA 的版本锚点与关键数据见各自分册；VersualRL 只作为任务层边界案例，保留摘要级证据等级。技能名称本身不替代论文来源与章节/图表锚点。

### 2.2 2026-10-23 canonical claim_audit 结果与人工分流

命令：`python3 ~/.dsh/skills/code-researcher/scripts/claim_audit.py <file> --lang zh --format json`。脚本只判断高影响 Markdown 行邻近是否出现可识别的本地路径；不打开论文、不解析 arXiv 章节/表图锚点，也不判断来源是否支持主张。下表报告脚本原始数，不把缺路径提示等同于证据缺失或通过。

| 文档 | 高影响行 | 缺少邻近路径提示 | 人工分流 |
| :-- | --: | --: | :-- |
| [闭环专题](../topics/closed-loop-control.md) | 9 | 3 | `(c)` 三条是 VersualRL 小节标题、对照表列头与编制时间，属结构/元数据误报 |
| [RECAP 分册](../papers/2511.14759-pi-star-0.6-recap.md) | 9 | 5 | `(c)` 五条分别是适用问题 framing、已有 §I/IV–V / §V-D / §VI-C.1–2 定位但脚本不解析、或七问标题 |
| [LingBot-VA 分册](../papers/2601.21998-lingbot-va.md) | 3 | 1 | `(c)` 一条为第 4 问标题 |
| [VLCP 分册](../papers/2608.16978-vlcp.md) | 8 | 5 | `(c)` 四条方法、消融或限制判断已带 v1 §1/§3/§4.3/§5 定位但脚本不解析；另 1 条为第 4 问标题 |
| [主报告](../report.md)（全文件） | 55 | 16 | 全文件口径含旧章节；本次增量声明、定义、边界案例、开放问题和来源计数均有就近路径或固定版本来源，当前新增范围内无未分流提示 |

固定版本原文已逐项打开核对：RECAP v2 的方法与真实任务结果见 §I、§IV–VI（包括 corrections 的限制 §V-D）；LingBot-VA v2 的架构/接地见 §1、§3.4，真机与异步消融见 §4.3–4.4；VLCP v1 的代码重规划、匹配对照、恢复与仿真限制见 §3、§4.3–4.6、§5。VersualRL v3 仅作边界核对：摘要及 §III-A–B 说明它更新符号 Behavior Tree，actor 不接收原始感觉流、也不直接控制机器人；主报告仍标 `[摘要级]`，不据此扩展为完整精读。

增量内的具体分流：专题第 1.3 节“机制意义”原是 `(b)` 研究推断/写作建议，已显式标为 `[推断 / 建议]` 并链接相关分册，因此当前不再是缺近邻路径提示；剩余专题提示均为 `(c)`。RECAP、LingBot-VA、VLCP 表中提示均属 `(c)`：问题 framing、标题，或具有固定版本章节定位但扫描器不能解析的行；未发现 `(a)` 的真实高影响证据缺口。主报告相关增量经补链后当前没有缺近邻路径提示；VersualRL 行仍标摘要级且直达 v3；“通用协议未确证”已限定为检索范围内的受限结论。

**限制**：以上计数是全报告结构扫描。主报告 55/16 包含此前旧章节和表格，不应被解读成新批次的 claim 数或事实错误数；“来源已定位”也不代表原文的作者自报结果已独立复现。

## 3. 许可与「全文不入库」的合规说明

1. **arXiv 默认许可是「永久非独占许可」，不授予第三方再分发权**；CC BY 4.0 虽允许再分发，但要求署名且本仓库定位是**研究报告而非论文镜像**。
2. 因此本条目**只在仓库内保留自己的精读分册与来源清单**，PDF / txt / 转出的 markdown **一律不入库**（缓存放在 `~/Documents/paper-cache/`，仓库外）。
3. 分册内引用采用**短引用 + `arXiv ID + 版本日期` + 章节锚点**，不整段转录原文。

## 4. 未入本清单的引用（说明）

`report.md` 的参考文献中还包含**未设精读分册**的对象（官方仓库、官方项目页、官方博客，以及 `[摘要级]` / `[受限核验]` 的论文）。它们**不在本清单的 11 篇之内**，等级与出处逐条写在 `report.md` 的「参考文献」中；选文取舍理由见 [CANDIDATES.md](CANDIDATES.md)。

---

*编制时间：2026-10-23 ｜ 原有版本日期照论文 PDF 首页行；新增版本日期依 arXiv abs 当前版本记录；license：`arxiv.org/abs/<ID>` 页内标识*
