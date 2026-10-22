# Sources Manifest — LLM Reinforcement Learning

检索截止：2026-10-23。原文 HTML 或出版版入口优先；缓存 PDF 位于仓库外 `/Users/zhoucanzong/Documents/paper-cache/llm-rl-2026-10-23/`，未将论文全文加入仓库。PDF SHA-256 是缓存完整性信息，不表示独立复现。

| ID | 固定版本 / 日期 | 许可 | 来源与定位 | 使用范围 / 缓存 |
|---|---|---|---|---|
| S1 | arXiv:2403.08635v1 / 2024-03-13 | arXiv HTML 标示 CC BY 4.0 | [HTML](https://arxiv.org/html/2403.08635v1), §3–6, Table 1–2, Appendix B.1 | 深读在线偏好机制及摘要结果；PDF `2403.08635.pdf`, SHA256 `09fb1dda73b459930af5a88efdc1c8ce965b51465f2e4d23f731e32069ae9f7c` |
| S2 | arXiv:2502.01456v2 / 2025-09-26 | CC BY-NC-ND 4.0 | [HTML](https://arxiv.org/html/2502.01456v2), §2–5, Table 1, Algorithm 1, Appendix A | 深读 PRIME 机制、七基准实验和 limitation；PDF `2502.01456.pdf`, SHA256 `b9b0d4ee041d5f21dec9489a67582e3775c3900a61bad979814522ab8b3faef6` |
| S3 | arXiv:2502.01600v3 / 2025-03-08 | CC BY-NC-ND 4.0 | [HTML](https://arxiv.org/html/2502.01600v3), §4–5, Table 1–2, Appendix E | 深读 LOOP 长时序 agent 更新；PDF `2502.01600.pdf`, SHA256 `632efe95b1d8c4ea09b66734e3fc5088ed994cbe8da021fc4d17f749f5be59dd` |
| S4 | arXiv:2411.02337v3 / 2025-01-27 | CC BY-NC-SA 4.0 | [HTML](https://arxiv.org/html/2411.02337v3), §2–3, Table 1, Figure 5 | 原文选读 WebRL 课程、ORM、KL 与回放；PDF `2411.02337.pdf`, SHA256 `79a93b02cca5586d9e3e2742c5af53f683c632dc0eaed3b7bf87f53daaa2d462` |
| S5 | arXiv:2505.16421v2 / 2025-10-08 | arXiv HTML 标示 arXiv.org perpetual non-exclusive license | [HTML](https://arxiv.org/html/2505.16421v2), §2–3, Table 2, Figure 4 | 原文选读多轮 GRPO、BC 消融和 WebArena-Lite 评测；PDF `2505.16421.pdf`, SHA256 `d71d94da517b6b024e95ee53e5f56a09ed26fc5e56d2dfc9b87a794086001447` |
| S6 | arXiv:2604.15149v1 / 2026-04-16 | CC BY 4.0 | [HTML](https://arxiv.org/html/2604.15149v1), §1、§4、Appendix C | verifier gaming / 同构扰动测试及 extensional/isomorphic reward 对照；用于失败模式选读，不做全面精读 |
| S7 | arXiv:2608.00220v2 / 2026-09-29 | arXiv abs 页面 | [Abstract](https://arxiv.org/abs/2608.00220v2) | support reshaping 及 Qwen3-8B-Base / IFEval 数字仅按 v2 摘要核对，正文数值未逐项复算 |
| S8 | arXiv:2506.14245v2 / 2025-10-02; ICLR 2026 | CC BY 4.0 (arXiv) | [HTML](https://arxiv.org/html/2506.14245v2), ICLR proceedings [abstract](https://proceedings.iclr.cc/paper_files/paper/2026/hash/517f9b9c227b9dd51dba4560f37165ed-Abstract-Conference.html) | RLVR correct reasoning 正向机制论文候选；未深读正文 |
| S9 | arXiv:2509.08755v1 / 2025-09-10 | arXiv 页面 | [HTML](https://arxiv.org/html/2509.08755v1) | AgentGym-RL 多环境、逐步扩展交互长度候选；主文未复核数表 |
| S10 | arXiv:2606.02031v2 / 2026-06-04 | arXiv.org perpetual non-exclusive license | [HTML](https://arxiv.org/html/2606.02031v2), §4–5, Table 2–4 | 原文选读真实网页视觉 agent 在线 RL、judge 设计与 reward hacking ablation；未缓存 PDF |
| S11 | arXiv:2412.16145v2 / 2024-12-25 | arXiv 页面 | [OREO](https://arxiv.org/abs/2412.16145v2) | 离线多步推理 RL 候选；摘要确认，正文未读 |
| S12 | arXiv:2402.03300v3 / 2024-02-06 | arXiv 页面 | [DeepSeekMath](https://arxiv.org/html/2402.03300v3), §4.1 | GRPO 来源论文；报告避免重述已在 Alignment 涵盖的算法推导 |
| S13 | arXiv:2503.14476v1 / 2025-03-18 | arXiv 页面 | [DAPO](https://arxiv.org/html/2503.14476v1), §3–4 | Alignment 已有 DAPO 四项设计、原文核对和消融，不再重复 |
| S14 | arXiv:2504.05118v1 / 2025-04-07 | arXiv 页面 | [VAPO](https://arxiv.org/html/2504.05118v1), §4–5 | Alignment 已有长链 critic/GAE 和长度异质奖励阅读，不再重复 |

## 审计与限制

- 2026-10-23 使用本机 canonical `claim_audit.py` 检查主报告及三篇精读：主报告 **14 项高影响结论 / 2 项未检出邻近本地路径**；`online-preference.md` **4/0**、`prime.md` **7/0**、`loop.md` **6/0**。主报告剩余两条提示分别是比较表的“主要风险”列标题和诊断清单的重复性建议，不是独立实验结论；其余主要事实段落具有近邻论文精读或来源清单路径。脚本只识别 Markdown 邻近行里的本地路径，不识别外部 URL、章节/表格定位，也不验证来源是否支持主张。该计数是导航/结构提示，不是事实通过数。主报告的逐篇版本和章节/表图定位见本清单各行；高影响数字按表中固定版本回到原文核对，未独立复现。

## 获取与版本记录

- `paper-fetcher` 搜索用于发现偏好学习、PRIME 和 agent RL 候选；批量元数据获取 S1–S5，论文原文后回到 arXiv HTML 固定版本阅读。
- PaperFetcher PDF 成功缓存 S1–S5；网页 HTML 为主要核查入口，摘要字段不替代全文定位。
- 本轮未训练/复现算法。所有结果数字都是论文作者报告；开放可下载代码不等于本轮运行过作者代码。
- **技能使用证据**：本批次按本机 `researcher` skill 的 deep 路径进行研究问题界定、候选筛选、固定版本原文精读与跨论文综合；具体问题和筛选理由记于主报告与 [CANDIDATES](CANDIDATES.md)。使用 `paper-fetcher` 搜索并获取 S1–S5 元数据/PDF，之后回到固定 arXiv HTML 核对正文。技能入口分别为 `/Users/zhoucanzong/Documents/codes/researcher/skills/researcher/SKILL.md` 与 `/Users/zhoucanzong/Documents/codes/paper-fetcher/skills/paper-fetcher/SKILL.md`；没有保存完整命令日志，故这里是产出与方法的可查记录，不声称可独立重放每次调用。
