# ResearchReport 项目规范

本文件是项目规范的唯一入口与真值来源。根目录 [`AGENTS.md`](../AGENTS.md) 负责引导；[`research-method.md`](research-method.md) 讲阅读方法；[`verification.md`](verification.md) 讲证据核验。遇到重复或冲突时，以本文件为准。

## 项目用途

ResearchReport 是面向阅读学习的 AI 研究图书馆。研究的价值在于让读者理解问题为何重要、方法如何工作、设计为何如此、实验支持到什么程度、与相邻工作的关系、失效边界和未解决的问题。内容是否有助于理解，比篇幅、目录数量、引文数量或模板完整度重要。

## 阅读入口与目录

- `report.md` 是专题入口：交代覆盖范围和推荐阅读顺序，先建立直观理解，再解释关键机制、论文关系、实验依据、限制与开放问题。
- `papers/` 可放独立论文精读；只有逐篇阅读能增加理解时才建。
- `topics/` 可放跨论文的综合分析；只有问题确实横跨多篇工作时才建。
- `sources/` 可集中必要来源信息；保持简洁，通常记录官方链接、实际阅读版本和相关章节、表格、图或源码位置即可。

不要求每个专题创建上述全部目录。七问只作思考提示：研究问题、核心机制、关键设计选择、支持性证据、与相邻方法的关系、失效条件、开放问题。按主题自然组织，不机械逐项作答、不设置固定章节，也不为填满目录而扩写。

## 行文与分析

- 用读者熟悉的例子、图或短推导先解释直觉，再引入必要术语、公式和实现细节。
- 解释设计取舍：作者要解决什么约束，为什么选择该机制，替代方案会改变什么。
- 区分论文直接报告的事实与基于证据的研究判断；证据不能支持的地方就收窄结论。
- 只保留能说明机制或边界的数字、对照和消融。一般不关心的 API 价格、版本退役动态、营销排名不进入重点，除非它们直接改变技术判断。
- 正文面向读者，不写修订时间线、下载与检索日志、例行核验记录、重复免责声明或内部协作经过。
- 术语第一次出现时给出简短解释。公式应解释变量和用途；不能增加理解的公式可以省略。

## 证据与引用

- 优先读官方论文、规范、数据集说明和固定版本源码；引用给出官方来源、实际阅读版本以及相关章节、图表或代码位置。
- 关键实验结论要保留其适用条件，例如模型、任务、指标、对照或预算。相对变化与百分点要分清；只核验支撑核心判断所需的指标与条件。
- 已有核验可在版本和结论未变时复用。遇到版本变化、来源矛盾、复现差异或结论争议，再回查相应原文，不重复核算所有数字。
- “论文报告”“原文已读”“源码已读”“本次独立运行”是不同证据；没有执行的实验不写成已复现。测试存在也不等于本次测试已运行。
- 通常不在报告里附本机缓存路径、文件哈希或逐下载台账。完整在线原文优先；仅当正文只有 PDF、需查看原图/公式、离线阅读或反复回查时才下载。

## Skills 与远程来源

对应 Skill 是调研方法的入口，任务开始前阅读实际 Skill 文档。远程仓库是获取和安装来源；本机绝对路径只用于确认当前环境的安装位置，不作为项目规范。

| 工作 | Skill | 项目约定 | 官方仓库 |
|---|---|---|---|
| 论文与领域研究 | `researcher` | 默认 deep；deep 指原文理解和分析深度，不指日志或篇幅 | [zhoucanzong/researcher](https://github.com/zhoucanzong/researcher) |
| 获取论文原文 | `paper-fetcher` | 先读完整在线原文，PDF 按需获取 | [zhoucanzong/paper-fetcher](https://github.com/zhoucanzong/paper-fetcher) |
| 代码库研究 | `code-researcher` | 以固定源码版本为准，重要行为给文件与行号 | [zhoucanzong/code-researcher](https://github.com/zhoucanzong/code-researcher) |

本机已安装副本可通过以下路径定位和阅读；它们不是下载或安装来源：

- `/Users/zhoucanzong/Documents/codes/researcher/skills/researcher/SKILL.md`
- `/Users/zhoucanzong/Documents/codes/paper-fetcher/skills/paper-fetcher/SKILL.md`
- `/Users/zhoucanzong/Documents/codes/code-researcher/skills/code-researcher/SKILL.md`

其他环境应从上表远程仓库获取，并按各仓库 README 安装，不依赖这些本机路径。

## 缓存与生成索引

`.paper-cache/` 是本地临时阅读缓存，已加入 Git 忽略规则；不应出现在报告、索引、站点 staging 或常规扫描中，也不应上传。迁移和归档只保留确有阅读用途的原文，精确重复文件可以合并，不同论文版本必须分别保留。

`report.md` 是图书馆条目入口。索引和站点导航由 `scripts/panels.json` 与 `scripts/library_index.py` 生成，不手工改生成区。更新后运行：

```bash
python3 scripts/library_index.py --repo-root . --out-root . --write-stats --check-links
```

再运行仓库所需的站点构建或相关验证。提交与推送按用户当次授权执行。
