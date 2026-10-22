# Chemistry 来源清单

核查日期：2026-10-23。来源范围为反应条件优化与前瞻性实验验证的定向选读，不是系统综述。版本日期取期刊正式记录；论文证据为作者报告并回到一手来源核对，不表示本地独立复现实验。

## 核心来源

| 论文 | 固定身份、版本与许可 | 可复核位置与数据/评价协议 | 可支持的结论与边界 | 原文获取与核验状态 |
| :-- | :-- | :-- | :-- | :-- |
| Connor J. Taylor et al., [Accelerated Chemical Reaction Optimization Using Multi-Task Learning](https://doi.org/10.1021/acscentsci.3c00050) | *ACS Central Science* 9(5), 957–968 (2023), DOI `10.1021/acscentsci.3c00050`; received 2023-01-10, revised/accepted 2023-04-03, online 2023-04-13, issue 2023-05-24; version of record. CC BY 4.0, publisher page rights line: “This publication is licensed under a Creative Commons Attribution 4.0 International License.” | 正文 Fig. 1（MTBO 机制）、Schemes 1–2 与 Figs. 2–3（文献 Suzuki surrogate benchmark；辅助任务 96 点；20 次重复及 95% CI；R2 负迁移）、Table 1 与 Schemes 3–6/Figs. 4–6（实验变量、4 个 C–H 活化 campaign 和实验数）、Methods “Gaussian Processes”, “Multitask Gaussian Processes”, “Bayesian Optimization”, “Flow Reactor Platform”。SI “Benchmarking using Literature Data”说明从原始文献提取并转为 ORD 的流程及全部实验数据。代码在 [sustainable-processes/multitask](https://github.com/sustainable-processes/multitask)，算法作为 Summit 包的一部分发布。 | 支持相似历史反应数据可在这项研究中帮助搜索特定新底物；模拟 benchmark 与真实实验分别报告。失效边界包括低活性/噪声辅助任务引发负迁移；campaign 连续推进，缺少独立重跑、随机化 STBO 对照和跨实验室外部验证。产率优化与新药/新反应发现不同。 | ACS 正式版本、补充材料目录和全文搜索摘录已核；PMC 记录 PMCID `PMC10214532`。PaperFetcher 直接 DOI `fetch` 返回 Hugging Face HTTP 404、arXiv HTTP 400（工具输入不适用）；以 ACS 正文、ACS/PMC 记录和 SI 索引为一手证据。未发现匹配本地 PDF 缓存。 |
| Benjamin J. Shields et al., [Bayesian reaction optimization as a tool for chemical synthesis](https://doi.org/10.1038/s41586-021-03213-y) | *Nature* 590, 89–96 (2021), DOI `10.1038/s41586-021-03213-y`; received 2020-06-24, accepted 2020-12-11, version of record / online 2021-02-03, issue 2021-02-04. Nature 页面未显示 CC 许可记录；按出版社版权与授权页面处理，不能据此复制正文或图表。 | 正文 Fig. 1（流程）、Figs. 2–4（直接芳基化 benchmark、实验优化游戏及与专家比较）、Fig. 5（Mitsunobu 和脱氧氟化真实优化）；Extended Data Tables 1–2。反应数据、auto-QChem、EDBO、EvML 代码按 Data/Code Availability 指向作者 GitHub 与 Code Ocean。 | BO 在该研究中连接了文献/HTE benchmark、专家决策比较及真实反应优化；作为 MTBO 的单任务前史。游戏比较结果不等同于每个化学家都被算法普遍超越；实验只支持所研究反应和参数空间。 | Nature 正式页面和摘要、图表目录、Data/Code Availability 核对。PaperFetcher 未提供 DOI 直取全文能力；未发现本地 PDF 缓存。 |
| Juan A. Garrido-Torres et al., [Bayesian Optimization of Computer-Proposed Multistep Synthetic Routes on an Automated Robotic Flow Platform](https://doi.org/10.1021/acscentsci.2c00207) | *ACS Central Science* 8(6), 825–836 (2022), DOI `10.1021/acscentsci.2c00207`; received 2022-02-24, issue 2022-06-22; PMC `PMC9228554`. PMC 记录 CC BY-NC-ND 4.0（非商业、禁止衍生作品，须署名并保持完整）。 | Scheme 1（ASKCOS 路线建议与人工精炼）、Figs. 3–5、Methods 与 Abstract；目标 sonidegib，三步/一分离的实验开发，优化产率、生产率、成本相关条件。 | 清楚展示 CASP 路线输出经过人工可行性筛选后仍需要真实实验开发；BO 优化的是路线执行细节。不能把路线预测 benchmark 的正确率当成实验成功率，也不是 Taylor 2023 MTBO 的复现。 | ACS 正式页面、PubMed/PMC 记录的摘要、图表锚点和许可记录已核；全文可由 PMC 获取。本文只用作边界说明，没有逐项重算全部流程指标。 |

## 检索与核验记录

- 已读取 researcher `deep` 与 PaperFetcher skill 入口，按定向搜索、原始来源核查、证据分层的流程执行。PaperFetcher 在 `/Users/zhoucanzong/Documents/codes/paper-fetcher` 搜索 `closed-loop Bayesian optimization chemical reaction conditions experimental validation` 与 `machine learning reaction condition optimization chemical synthesis`；Crossref 有结果，OpenAlex 与 Semantic Scholar 对第一组查询返回 429，第二组检索成功。检索结果用于候选发现，不作研究结论依据。
- PaperFetcher `fetch 10.1021/acscentsci.3c00050` 返回 Hugging Face 404 与 arXiv 400；该 DOI 论文不在工具支持的 arXiv/Hugging Face 获取通道。正式正文和补充材料目录来自 ACS，PMC 用于交叉定位。没有把工具失败解释为论文不可获取。
- 可核范围：题录、版本/日期、许可、正文方法与图表锚点、主要模拟/实验协议、作者报告的部分具体条件和产率、代码及补充材料入口。未逐行核对补充材料内所有原始 HPLC 数据，未独立重新拟合模型，也未执行反应或验证化学新颖性。
- 本目录只保留馆藏地图和研究报告，不保存 PDF、全篇 Markdown 或补充材料副本。
