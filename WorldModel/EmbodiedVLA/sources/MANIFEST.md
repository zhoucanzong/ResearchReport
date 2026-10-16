# 原文清单 · EmbodiedVLA

> 本仓库**只存清单与本条目的精读分册**（`papers/*.md`），**不存论文全文**（PDF 或转出的 markdown / txt 都不入库）。
> 需要回看原文时：按下面的 arXiv 链接现取。**本地缓存路径**：`~/Documents/paper-cache/<arXiv-ID>@latest/`（**仓库外、不入库**），内含 `<ID>.pdf`、`<ID>.txt`（`pdftotext -layout` 提取）与 `meta.json`（题名 / 版本 / 日期 / 第一作者 / SHA256）。**本清单不依赖缓存存在**。

## 1. 本轮精读的 8 篇（主等级 `[精读原文]`）

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

### 1.1 版本日期口径说明（重要）

- **「版本日期」取自论文 PDF 首页照抄的 `arXiv:<ID>v<N> [...] <d Mmm yyyy>` 行**，即**该版本的发布日期**，是引用时应写出的日期。
- arXiv Atom API 的 `published` 字段返回的是 **v1 的提交日期**；两者**在 v1 时相同、在后续版本时不同**（例：DROID v2 的版本日期 2025-04-22 而 `published`=2024-03-19；π0 v4 版本日期 2026-01-08 而 `published`=2024-10-31）。表中已同时标出，避免混用。
- 同一论文的后续版本可能修改结论；**引用具体数字时以本表版本为准**。

## 2. 抓取与核验方式（可复现）

| 环节 | 做法 | 证据 |
| :-- | :-- | :-- |
| 缓存优先 | 先查 `~/Documents/paper-cache/<ID>@latest/`，**命中即读、不重复下载** | 8 篇中 7 篇命中既有缓存（本地 `pdftotext` 提取文本） |
| 未命中才抓 | DROID（2403.12945）缓存未命中 → `paper-fetcher` skill 取原文 | `~/.dsh/skills/paper-fetcher/scripts/fetch_paper.py fetch/download` |
| 文本提取 | `pdftotext -layout <ID>.pdf <ID>.txt`（版本行/表格锚点均可逐字核对） | 每篇缓存目录内 `<ID>.txt` |
| 元数据核实 | `export.arxiv.org/api/query?id_list=<ID>` 批量回查**题名 + 版本 + `published`** | 本文表格第 4–6 列 |
| license 核实 | `arxiv.org/abs/<ID>` 页内 `creativecommons.org/licenses/...` 标识 | 本文表格 license 列（**5 篇 CC BY 4.0 / 3 篇 arXiv 默认许可**） |

## 3. 许可与「全文不入库」的合规说明

1. **arXiv 默认许可是「永久非独占许可」，不授予第三方再分发权**；CC BY 4.0 虽允许再分发，但要求署名且本仓库定位是**研究报告而非论文镜像**。
2. 因此本条目**只在仓库内保留自己的精读分册与来源清单**，PDF / txt / 转出的 markdown **一律不入库**（缓存放在 `~/Documents/paper-cache/`，仓库外）。
3. 分册内引用采用**短引用 + `arXiv ID + 版本日期` + 章节锚点**，不整段转录原文。

## 4. 未入本清单的引用（说明）

`report.md` 的参考文献中还包含**未设精读分册**的对象（官方仓库、官方项目页、官方博客，以及 `[摘要级]` / `[受限核验]` 的论文）。它们**不在本清单的 8 篇之内**，等级与出处逐条写在 `report.md` 的「参考文献」与「链接核验清单」中；选文取舍理由见 [CANDIDATES.md](CANDIDATES.md)。

---

*编制时间：2026-10-17 ｜ 元数据核实：`export.arxiv.org/api/query`；版本日期：论文 PDF 首页照抄行；license：`arxiv.org/abs/<id>` 页内标识*
