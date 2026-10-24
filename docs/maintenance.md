# 🛠 维护指南 · Maintenance

本文件说明 **ResearchReport** 的日常维护流程：拉取与推送、新增报告、与上游存档同步、更新索引与统计，以及已知问题与限制。

仓库首页 [README](../README.md) 只保留精简的维护速览；体积统计见 [statistics.md](statistics.md)；校验留证见 [verification.md](verification.md)。

---

## 1. 日常拉取与推送

本仓库是普通 **monorepo**：所有内容都在同一个仓库内，**不存在** submodule，也不需要 `git submodule update` 之类的操作。

```bash
cd ResearchReport

# 拉取远端最新内容
git pull --ff-only

# 提交并推送本地改动
git add -A
git commit -m "更新报告与索引"
git push origin main

# 查看状态与远端
git status --short
git remote -v
```

**约定**

- 提交者身份沿用全局配置（`zhoucanzong <zhoucanzong@gmail.com>`），不启用 GPG 签名。
- 提交前建议跑一遍 §7 的检查（链接、表格、计数、gitlink）。
- 提交信息用中文，动宾结构（如「新增 X 专题」「修正 Y 统计」）。

---

## 2. 新增 / 修改报告（研究板块）

研究板块以顶层目录组织，主题目录下的主报告固定命名为 `report.md`。Models 可按模型系列拆目录；AI4Science 等领域专题按具体问题拆分。

```bash
cd ResearchReport/AI4Science                      # 或任一现有板块目录

mkdir -p NewTopic
$EDITOR NewTopic/report.md

cd ..                                              # 回到仓库根目录
git add -A
git commit -m "新增 NewTopic 研究报告"
git push origin main
```

**约定**

1. 目录名用 `<Name>`（**不再带 `-research` 后缀**）：按 `scripts/panels.json` 将条目放入对应板块；科学研究专题归入 `AI4Science/`，按具体科学问题拆分，不建立泛化的 AI4Science 总报告。
2. 主报告固定 `report.md`；需要深挖时在目录内新增 `<topic>-<sub>.md` 分册（全小写、连字符，例如 `speculative-eagle-series.md`）。
3. 内容**中文为主、关键术语保留英文**，附来源索引 / 论文引用以便追溯。
4. 按研究问题选择结构。面向读者解释问题、机制、设计取舍、关键证据、相邻研究和失效边界；组织方式遵循 [team.md](team.md)，七问仅作思考提示。

---

## 3. 与上游 GitHub 存档同步（历史：仅适用于旧 `AIGC-Research/`、`LLM-Research/`，6 板块重排后已并入板块目录）

三个子目录中，**只有 `AIGC-Research/`、`LLM-Research/` 是上游 GitHub 仓库的内容快照**，不带 Git 历史；本地已无上游仓库副本（2026-10-16 移入废纸篓，见[历史核验档案](archive/verification-history-2026-10.md)）。如需从上游导入提交，先把存档仓库克隆到本仓库之外，再复制变化：

```bash
# 例：从 GitHub 取上游 AIGC-Research 存档
git clone https://github.com/zhoucanzong/AIGC-Research.git /tmp/AIGC-Research
rsync -a --delete --exclude '.git' --exclude '.DS_Store' \
  /tmp/AIGC-Research/ ResearchReport/   # 上游内容按新板块目录归位（Models/ AIGC/ WorldModel/）

cd ResearchReport && git add -A && git commit -m "同步上游 AIGC-Research"
```

> ⚠️ `rsync --delete` 会删除目标端多余文件，**执行前先加 `--dry-run` 预览**。

> `OpenSource/`（旧 `Repo-Research/`）**不适用本节**：它从来不是 Git 仓库，没有任何上游存档；本仓库内的 `OpenSource/` 就是**唯一权威副本**，直接在其中增删改即可。

> 上游存档仓库（`AIGC-Research`、`LLM-Research`）是否继续保留由维护者决定；**ResearchReport 是唯一在维护的仓库**。

---

## 4. 新增深度阅读项目（OpenSource）

`OpenSource/` 不套用统一模板，以「一个项目一个顶层目录」组织，目录内按用途分层：

```bash
cd ResearchReport/OpenSource
mkdir -p <new-project>/notes <new-project>/raw-extracts <new-project>/papers
# 建议产出：report.md（综述）、plan.md（计划）、knowledge-graph.md（概念卡）、
#          sources-index.md（来源）、notes/（笔记）、raw-extracts/（原文）、papers/*.json（结构化数据）
cd .. && git add -A && git commit -m "新增 XXX 深度阅读" && git push origin main
```

**约定**

- 原始提取（`raw-extracts/`）应注明来源与提取方式；**避免写入仅在本机有效的绝对路径**（见 §6 第 8 条）。
- 个人解读与评分类字段建议显式标注（如 `个人评价`），便于读者区分事实与观点。

---

## 5. 新增资料库

若新增研究板块：

1. 在仓库根目录建立板块目录（普通目录即可，**不要**引入嵌套 `.git`、submodule 或 gitlink）。
2. 在 `scripts/panels.json` 登记板块的路径匹配规则、代表条目和展示配置；目录必须唯一映射到一个板块。
3. 运行索引生成器更新首页、导航、统计与各索引，再按需补充板块入口 `README.md`。
4. 在 [statistics.md](statistics.md) 更新当前板块汇总与明细；历史统计快照应明确标记历史口径。
5. 若有嵌套 `.git`：先确认其全部对象在上游可按同一 SHA 找到，再删除（参考[历史核验档案](archive/verification-history-2026-10.md)中扁平化记录的做法），否则 `git add` 只会记录一个 gitlink，推送后目录内容为空。

---

## 6. 更新索引与统计

任何内容变更后，请同步更新以下文件，保持数字**实测一致**：

| 变更 | 需要更新 |
| :-- | :-- |
| 新增 / 删除报告 | 首页「完整索引」折叠块、徽章 `Reports`、[statistics.md](statistics.md) 表 1/3/4 |
| 新增 / 删除资料库或项目 | 首页卡片与徽章 `Collections`、[statistics.md](statistics.md) 表 1/2/5 |
| `docs/` 文件变动 | 首页「文档」区、[statistics.md](statistics.md) 表 2 |
| 重新校验仓库 | [verification.md](verification.md) 对应小节 |

**统计方法**（与 [statistics.md](statistics.md) §6 一致）：

```bash
git ls-files | wc -l                                    # 跟踪文件数
git ls-files '*.md' | wc -l                             # 全仓库 .md 数
git ls-files 'Models/*.md' 'LLM/*.md' 'AIGC/*.md' 'WorldModel/*.md' 'AI4Science/*.md' 'Infra/*.md' 'OpenSource/*.md' | grep -vc 'README\.md$'   # 报告数（精确值以索引统计为准）
find <dir> -type f -exec stat -f '%z' {} + | awk '{s+=$1} END{print s}'          # 字节数
du -sk <dir>                                            # 磁盘占用
```

---

## 7. 提交前检查清单

```bash
cd ResearchReport

# 1) 无 gitlink
git ls-files -s | awk '$1==160000' | wc -l                       # 期望 0
git ls-files -s | awk '{print $1}' | sort | uniq -c              # 期望全部 100644

# 2) 计数
git ls-files | wc -l
git ls-files '*.md' | wc -l
git ls-files 'Models/*.md' 'LLM/*.md' 'AIGC/*.md' 'WorldModel/*.md' 'Infra/*.md' | grep -vc 'README\.md$'   # 期望（按新目录重算）

# 3) 工作区干净
git status --short

# 4) 相对链接与表格自检（示例脚本，检查 markdown 相对链接是否指向存在的文件）
python3 - <<'PY'
import re, os
for root, _, files in os.walk('.'):
    if '/.git' in root or root.startswith('./.git'): continue
    for f in files:
        if not f.endswith('.md'): continue
        p = os.path.join(root, f)
        txt = open(p, encoding='utf-8').read()
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', txt):
            if re.match(r'^(https?:|mailto:|#)', link): continue
            t = os.path.normpath(os.path.join(root, link.split('#')[0]))
            if not os.path.exists(t) and not os.path.exists(t.replace('%E7%AD%89', '等')):
                print('BROKEN', p, '->', link)
PY
```

---

## 8. 已知问题与限制

1. **（历史记录）上游 README 的自报计数已修正**（2026-10-16）：`LLM-Research/README.md` 的徽章与正文原写 `Reports-32` / 「16 个主流模型 / 系列」，已改为 **36 / 15 个**（表格行数本为 15，与之一致）；`AIGC-Research/README.md` 结构注释「技术专题报告（6 个）」已改为 **（8 个）**。
2. **`.DS_Store` 已清理**：本仓库内所有 `.DS_Store` 已删除，并由根目录 `.gitignore` 覆盖（macOS 之后重新生成也不会进入提交）。已移入废纸篓的本地副本（`AIGC-Research`、`LLM-Research`、`Repo-Research`）中仍带着未跟踪的 `.DS_Store`，属其既有状态，未去改动。
3. **（历史记录）三库均无 `LICENSE` 文件**：`LLM-Research/README.md` 徽章宣称 MIT，其原 `./LICENSE` 死链已改为**无链接文本徽章**；`AIGC-Research/`、`Repo-Research/` 同样没有任何许可证声明。若要以 MIT 等许可公开发布，建议补上统一的许可证文件。
4. **本仓库不含 AIGC-Research / LLM-Research 的 Git 提交历史**：为支持扁平推送，嵌套 `.git` 已移除（见[历史核验档案](archive/verification-history-2026-10.md)）。需要逐次提交历史 / blame 时，请使用上游独立仓库。`Repo-Research` 本来就没有历史。
5. **（历史记录）内容性质与准确性**：`AIGC-Research/`、`LLM-Research/` 的报告为 **AI Agent 自动调研生成、未经官方确认**，引用具体参数 / 日期 / benchmark 前请回溯原始来源；`Repo-Research/` 是**人工 + Agent 的阅读笔记**，其中的「个人解读 / 个人评价」带有主观判断（例如 `papers/nemotron-labs-diffusion.json` 中的评分字段），引用时请区分事实与观点。
6. **（历史记录）`LLM-Research/.claude/settings.local.json` 未纳入版本控制**：它被**全局** gitignore 规则（`~/.config/git/ignore`：`**/.claude/settings.local.json`）忽略；如需强制纳入，使用 `git add -f`。
7. **三个本地原始目录已于 2026-10-16 移入废纸篓**：`~/Documents/AIGC-Research`、`~/Documents/LLM-Research`、`~/Documents/Repo-Research` 均在 `~/.Trash/` 中（可恢复直至清空废纸篓）。移除前已确认内容收录情况（见[历史核验档案](archive/verification-history-2026-10.md)）。其中 `Repo-Research` **没有上游存档**，清空废纸篓后旧副本不可恢复。
8. **（历史记录）`Repo-Research/` 中残留机器相关的绝对路径**：`raw-extracts/nemotron-tri-mode-fulltext.md`、`raw-extracts/pdf-fu_等__…dif.md`、`plan.md`、`sources-index.md` 共 4 个文件、5 处引用了本机的 Zotero 路径 `/Users/zhoucanzong/Zotero/storage/VZ5BMRZW/…pdf`（原始论文 PDF 位置）。这些路径**在其他机器上不可用**，也指向仓库之外的文件；仓库未包含该 PDF 本体。如需跨机使用，建议改为相对路径或补充论文公开链接。
9. **（历史记录）`Repo-Research/raw-extracts/pdf-fu_等__…dif.md` 是未完成的提取占位**：正文仅为脚本生成的模板与待办清单（1,141 B），实际全文在同目录的 `nemotron-tri-mode-fulltext.md`。保留它是为了记录提取流程，**不要误当作论文全文**。

---

*最后更新：2026-10-16*
