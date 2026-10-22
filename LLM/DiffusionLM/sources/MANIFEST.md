# 原文与证据清单 · DiffusionLM

> 原文只引用官方固定版本；论文全文与文本抽取保存在仓库外，不复制进仓库。SHA-256 用于缓存完整性识别，不代表复现实验。

| ID | 固定版本 / 许可 | 原文位置 | 缓存与本次阅读范围 |
|---|---|---|---|
| D1 | Nie et al., [LLaDA](https://arxiv.org/abs/2502.09992v3), `2502.09992v3`, 2025-10-18；arXiv perpetual non-exclusive distribution license | [HTML v3](https://arxiv.org/html/2502.09992v3), §§2–3, Tables 1–10, 18–19, Appendix A / B.1–B.7. 重点支撑随机 mask 目标、反向采样、8B规模与AR比较 | `/Users/zhoucanzong/Documents/paper-cache/LLM-DiffusionLM/2502.09992.pdf`; SHA-256 `18942f14544d696bef711acd43c84017e51b8428b15edc74130761218e66f73b`; 已通读指定章节，未运行作者代码或复现 |
| D2 | Zhu et al., [LLaDA 1.5 / VRPO](https://arxiv.org/abs/2505.19223v2), `2505.19223v2`, 2025-10-12；CC BY 4.0；ACL 2026 收录 | [HTML v2](https://arxiv.org/html/2505.19223v2), §§2–4, Tables 1–3, Appendix B–D. 重点核验 ELBO 估计、方差来源、VRPO 对照 | `/Users/zhoucanzong/Documents/paper-cache/LLM-DiffusionLM/2505.19223.pdf`; SHA-256 `4ec09b450c8560ce7757c00024c929daa2bb6bc73cd401ea161a21ab3b9aa359`; 未运行对齐代码或独立复现 |
| D3 | Bie et al., [LLaDA2.0](https://arxiv.org/abs/2512.15745v2), `2512.15745v2`, 2025-12-24；arXiv perpetual non-exclusive distribution license | [HTML v2](https://arxiv.org/html/2512.15745v2), §§3–7, Table 2, Figures 1–6. 关注 WSD 转换、规模、DPO 与服务证据；总训练计算量未完整披露 | `/tmp/paper-fetcher-diffusionlm/2512.15745.pdf`; SHA-256 `b6c3d73e2cbbd1b5b11660d2aeb438b4597403fca52650dc470f0d0ad98ee18f`; 未运行训练或服务代码 |
| D4 | Bie et al., [LLaDA2.1](https://arxiv.org/abs/2602.08676v3), `2602.08676v3`, 2026-02-13；arXiv perpetual non-exclusive distribution license | [HTML v3](https://arxiv.org/html/2602.08676v3), §§2–6, Tables 1–4, Figures 1–3. 关注 M2T/T2T、MBE、S/Q模式、TPF/TPS与量化损失 | `/tmp/paper-fetcher-diffusionlm/2602.08676.pdf`; SHA-256 `d4dc2e6bb5f5615d00fc6ce9bff240f1112ef26ea43c7300f15e084906ff4c7a`; 未运行训练或推理代码 |
| D5 | Arriola et al., [Block Diffusion](https://arxiv.org/abs/2503.09573v3), `2503.09573v3`, 2025-05-17; ICLR 2025 Oral; CC BY 4.0 | [HTML v3](https://arxiv.org/html/2503.09573v3), §§3–7, Appendices A–D, Figs. 1–4, Tables 2–8. 核验块内/块间生成、mask-rate schedule、可变长度和 KV cache 的证据边界 | `/Users/zhoucanzong/Documents/paper-cache/LLM-DiffusionLM/2503.09573.pdf`; SHA-256 `d57ae21f556a9c1d5d5a95b2067d3232933be2d421b484bea7cc2b39b980ce92`; 未运行代码或模型 |
| D6 | Cheng et al., [SDAR](https://arxiv.org/abs/2510.06303v3), `2510.06303v3`, 2025-10-18; CC BY 4.0 | [HTML v3](https://arxiv.org/html/2510.06303v3), §§2–8, Appendices A–B, Figs. 1–8, Tables 1–7. 核验 AR checkpoint 转换、30B science 与 8B/H200 条件，区分领域结果与通用能力 | `/Users/zhoucanzong/Documents/paper-cache/LLM-DiffusionLM/2510.06303.pdf`; SHA-256 `fcc94cf3cf62cc4b44e75ded09a84b102726c7f01e6e943dc7cc4f8ea66bc0f4`; 未运行代码或模型 |
| D7 | Ruan et al., [CARD](https://arxiv.org/abs/2601.22031v1), `2601.22031v1`, 2026-01-29; CC BY 4.0 | [HTML v1](https://arxiv.org/html/2601.22031v1), §§2–6, Appendices A–D, Figs. 1–4, Tables 1–8. 核验 causal-tail diffusion、局部上下文加权及质量—TPF/TPS 关系 | `/Users/zhoucanzong/Documents/paper-cache/LLM-DiffusionLM/2601.22031.pdf`; SHA-256 `cc032058974d5baea8490b1f78d174a3885c08597e76be739d28c51c969b3e41`; 未运行代码或模型 |
| D8 | Bie et al., [LLaDA2.2: Enabling Agentic Diffusion Language Models via Levenshtein Editing](https://github.com/inclusionAI/LLaDA2.X/blob/f402f0b52817e1c3586a024ebf89e69ad8ca5523/LLaDA2_2_tech_report.pdf), 11-page official technical report；无 arXiv ID；官网标注 2026-07-01，commit-pinned PDF 上传/创建日期为 2026-07-22；PDF 未声明 license | 官方 PDF §§2–5, Figure 3–4, Tables 1–3；重点看 LCS 编辑监督、插入/删除动作、同基座 SWE editing ablation 及 agent benchmark / throughput 限制 | SHA-256 `06e1f341cd08688c9d85ec0a7e0a57bca86555b72e3dac7f71ef69fcf70d2812` (702,354 bytes); PDF 与全文抽取位于 `/tmp/paper-fetcher-diffusionlm/`; 没有独立运行或复现。未从 repository root 的 Apache license 推断 PDF 许可 |

## 证据纪律与限制

- 各论文的作者结果、复核范围和 claim-audit 说明见对应 `papers/*.md`；章节/表图编号必须与 fixed version 一起读取。
- 训练目标、条件化结构、采样、服务内核和量化常常同时变化；跨论文的参数规模、benchmark分数、TPF与TPS不能拼成单一排名。
- 仅把 LLaDA 2.1 的 token editing 当作它的候选修订机制；未把速度收益独占归因给 editing。对 LLaDA 2.0 的规模主张同样保留未披露的训练预算边界。
- D1–D7 的逐篇来源定位与证据限制见对应论文分册；缓存仅用于复查和完整性识别，所有实验数值均为作者报告。
