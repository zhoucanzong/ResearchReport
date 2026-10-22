# Astronomy source manifest

核查日期：2026-10-23（Asia/Shanghai）。本专题聚焦 DECaLS 巡天星系图像中的主动异常排序和候选发现。正文数字均来自一手论文；不入库论文全文、PDF 或复制表格数据。

| Source | 固定身份 / 版本 / 许可证 | 阅读锚点 | 本文使用及边界 |
| :-- | :-- | :-- | :-- |
| [Astronomaly at scale: searching for anomalies amongst 4 million galaxies](https://doi.org/10.1093/mnras/stae496) | Verlon Etsebeth et al., *MNRAS* 529(1), 732–747 (2024); online 2024-02-22; DOI `10.1093/mnras/stae496`; 期刊全文标示 **CC BY 4.0**。与固定版本相配的 arXiv `2309.08660v2`，修订日期 2024-03-29；该 arXiv 页面记录 arXiv non-exclusive distribution license（这与期刊许可分别记录）。 | 期刊正文 §§2.1–2.3、3.1–3.3、4.1–4.3、5；Figs. 2–9；Tables 1–4；Appendix A–B。arXiv abs 页确认 v2 日期及期刊版本。 | 主证据。近 390 万 DECaLS 图像排序和候选输出；评估集对比主动学习与 iForest。8 个强透镜候选中仅 3 个此前未发现，且未由本论文独立确认；目录切割已漏掉大量已知透镜。逐篇证据见 [papers/2309.08660.md](../papers/2309.08660.md)。 |
| [Astronomaly: Personalised Active Anomaly Detection in Astronomical Data](https://doi.org/10.1016/j.ascom.2021.100481) | Michelle Lochner & Bruce A. Bassett, *Astronomy and Computing* 36 (2021), 100481; arXiv `2010.11202v2`, revised 2021-10-06; arXiv license 为 non-exclusive distribution grant。本文记录的是 arXiv 权限，未在本轮核验出版社版本许可。 | arXiv v2 abstract 与 journal reference；论文 §§3–5、Galaxy Zoo / simulated-data results。 | 框架前史：把人类兴趣标签整合进异常排序，并在首 100 个浏览对象中报告约两倍有趣异常。只作方法背景，未将其玩具/较小数据测试与 DECaLS 规模结果合并。 |
| [A Hitchhiker's Guide to Anomaly Detection with Astronomaly](https://arxiv.org/abs/2201.10189) | Michelle Lochner & Bruce A. Bassett, arXiv `2201.10189v1`, submitted 2022-01-25；arXiv non-exclusive distribution license；未核实期刊发表记录。 | arXiv abstract 与正文框架说明。 | PaperFetcher 返回的相关指南候选。保留在候选池，未作实证证据；其教程定位与 2021 原始框架论文有重叠。 |

## 工具与证据使用记录

- `researcher` skill 已按 deep 模式执行：以明确问题为起点，完成候选筛选、一手文献阅读、逐项结果/边界整理。Skill 入口：`/Users/zhoucanzong/Documents/codes/researcher/skills/researcher/SKILL.md`。
- `paper-fetcher` skill 已执行。入口：`/Users/zhoucanzong/Documents/codes/paper-fetcher/skills/paper-fetcher/SKILL.md`。运行 `search_papers.py` 精确检索 “Astronomaly at scale searching anomalies 4 million galaxies”；`fetch_paper.py fetch 2309.08660` 和 `fetch_paper.py batch 2309.08660 2010.11202 2201.10189 --citations` 返回与主论文题名、作者、arXiv ID、摘要及 DOI 相符的记录。另用 Crossref 检查主论文期刊 DOI 元数据。
- 主论文按 arXiv v2 与 Oxford Academic / MNRAS 正文交叉定位；许可证取期刊文章末尾的 CC BY 4.0 声明，版本日期取 arXiv 版本历史。没有使用新闻稿替代论文证据。
- 人工 claim audit：对 report 中 12 组主要数量与结论逐组确认附近原文锚点；没有发现无出处的实质性主张。此仓库未提供通用 `claim_audit.py`，故不报告自动扫描结果，也不把人工核对等同于独立事实复核。
- 没有运行作者模型、复制数据或进行候选天体的独立观测核实。原始论文的定性边界和“需 follow-up”表述保留在报告中。
