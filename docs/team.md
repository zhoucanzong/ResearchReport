# Team · 技术研究

一页约定摘要：新成员照此协作，不必翻聊天记录。

## 仓库身份
- 路径：`/Users/zhoucanzong/Documents/Research` = **ResearchReport**（主线 `main`）
- 远端：`https://github.com/zhoucanzong/ResearchReport.git`
- 提交者：`zhoucanzong <zhoucanzong@gmail.com>`；不开 GPG；提交信息用中文动宾式（例：`docs(library): 校正基线数字使其可复现`）

## 成员与范围
| 成员 | 角色 | 范围 | 写权限 |
| --- | --- | --- | --- |
| 泡泡(人类) | 决策 / 授权 / 对外操作 | 拍板、授权、GitHub 侧（如存档仓库归档） | — |
| 泡泡(Bot) | 任务分发 + 交叉核验 | 派单、验收把关 | Research 只读 |
| 研研 | 深度研究 / 报告撰写 | SpecDec 专题、`report.md`、统计数字 | 该专题 |
| 究究 | 深度研究 / 报告撰写 | 新主题（现：WorldModels） | 分支提交 |
| 图图 | 图书馆管理 / 合并 | 索引、元数据、统计、合入 `main` | Research 写（经 Assignment） |

## 规则
1. **触发**：仅被点名或被指派者响应；没任务不唤醒。
2. **流水线**：写 → `research/<topic>-<作者>` 分支 → 图图 merge 到 `main`（无冲突 fast-forward；有冲突图图解，仅内容语义不明时回问作者）。
3. **单写者**：一个目录同一时间只有一个写者；入库 / 索引 / 统计更新由图图独占。
4. **门禁**：合入 `main` 前全仓链接回测 0 失效（相对 + 指向 GitHub 的绝对链接）；统计数字与实测一致（或注明由脚本刷新）。
5. **派单格式**：目标 / 产出物 / 验收标准 / 交付方式 / 状态（由泡泡(Bot) 维护）。
6. **条目定义**：**条目 = 主文档**。当前实现口径为「条目 = `report.md`」——每个 `<topic>-research/` 目录一份；同目录的其它 `.md`（分册、`plan.md`、`notes/`、`raw-extracts/`、`sources-index.md`、`knowledge-graph.md`）是它的**子文档**。`README.md`（根 / 子库 / `scripts/`）、`docs/*.md` **不算条目**。front-matter 契约（`type` / `domain` / `subject` / `upstream`（代码类带 `@commit`）/ `date` / `evidence` / `status`）已定但**当前填充 0 份**，索引必须在无元数据时优雅退化。索引由脚本生成，人不手改。
7. **统计口径**：**脚本落地前**，内容写者随改动同步自己那部分并注明"人工维护"；**脚本落地后**（`scripts/library_index.py --write-stats` 已可用），统计数字一律由脚本产出、图图解，写者不再手改。`docs/statistics.md` 与根 `README.md` 的统计数字以 `index/stats.json` 为唯一真值。
8. **写权限**：Grant 的 `orchestratorWrite` 不是开关；会话直写被拒（`Operation not permitted`）时，走 `create_assignment` + 该目录 grant（Assignment 侧权限 `workspace-write`、cwd = 仓库目录，实测可 commit / push）。

## 技能强制规约（Skill Mandate）

调研类任务必须使用对应 skill，且**交付必须附 skill 使用证据**（不靠自觉）：

| 任务类型 | 必用 skill | 模式 |
| --- | --- | --- |
| 论文 / 领域调研 | `researcher` | 默认 **deep**（快速档需明确批准） |
| 仓库 / 代码调研 | `code-researcher` | 按需 `map` / `trace` / `deep` / `compare` |
| 取原文 / 做引用 | `paper-fetcher` | — |

- **派单层**：派单必须声明所用 skill 与模式；
- **验收层**：交付必须附 skill 使用证据——deep 产出特征（分册页首 `arXiv ID + 版本日期`、`claim_audit` 报数）、代码类必须有 `文件:行` 锚点；**无证据不入库**；
- **深度优先**：不限单文件长度，写长了就拆——`report.md`（入口/结论/判据）+ `papers/*.md`（逐篇精读）+ `topics/*.md`（横切专题）；仅摘要支撑的内容标 `[摘要级]` / `[⚠️受限核验]`，**不许升格为 `[精读原文]`**。

## 索引与统计（由脚本产出）
- 索引：`INDEX.md` + `index/*.md`（`by-domain` / `by-subject` / `by-repo` / `by-topic` / `by-report` / `recent` / `stale`）；输出根 = **仓库根**，脚本仍保留 `--out-root` 便于将来换布局。
- 机器可读统计：`index/stats.json`。
- 重建命令：`python3 scripts/library_index.py --repo-root . --out-root . --write-stats --check-links`
- 生成物不计入条目 / 文档统计（否则跑一次脚本数字就变一次，无法复现）。
