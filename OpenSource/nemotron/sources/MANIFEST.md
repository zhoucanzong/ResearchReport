# Nemotron 原文与证据清单

| 版本 | 来源 | 本轮核验 |
|---|---|---|
| NVIDIA technical report，2026-05-19，21页，v1文件 | [官方发布页](https://research.nvidia.com/publication/2026-05_nemotron-labs-diffusion-tri-mode-language-model-unifying-autoregressive)；[带对象版本的PDF](https://d1qx31qr3h6wln.cloudfront.net/publications/Nemotron_Diffusion_Tech_Report_v1.pdf?VersionId=db8_EMO8B.vmU26.jr7Le9pN3MqcUDNL) | 已下载并以PDF页图核Table1、Fig7/Table4、Fig9；SHA-256 `da7243d3a0db640732bb33f4c929c47ebc2ee7f9745fdb2cce1e5c899ac28edd` |
| 后补arXiv条目2607.05722，首投2026-07-07 | [arXiv](https://arxiv.org/abs/2607.05722) | `paper-fetcher fetch 2607.05722 --citations`核题名/作者/首投日期；未以该版本替代5月PDF实验数字 |
| 本库旧抽取 | [nemotron-tri-mode-fulltext.md](../raw-extracts/nemotron-tri-mode-fulltext.md) | 原Zotero PDF路径当前不存在；保留旧抽取不改写，核验以重取官方PDF为准 |
| 推理实现 | [NVlabs/Nemotron-Labs-Diffusion](https://github.com/NVlabs/Nemotron-Labs-Diffusion) | 只核官方入口与模式说明；本轮没有源码deep或运行，不宣称完整训练pipeline可复现 |

- `license`：官方发布页标 NVIDIA Open Model License；后补arXiv记录是独立版本，不将二者授权混写。
- 定位：Table1 p.4 累计训练消融；Table2–3 p.5–6 α扫描/AR配对比较；§4.1–4.2、Fig7、Table4 p.8–10 SOL；Table5 p.11 8B instruct；Table6 p.12 LoRA；§6.5/Fig9 p.14 吞吐。
- 已知源内差异：Fig7的图中舍入均值与§4.2文字/Table4并非所有数值完全相同；本文6.02/3.41及7.60/6.82采用作者正文口径，不从低分辨率图推导额外精度。
- 候选范围：这是单论文精读复核，没有做领域候选筛选，不将参考文献列表升级为逐篇已读。
- 使用技能：`researcher deep`、`paper-fetcher`；PDF只读取证与渲染图表，未修改或重新分发PDF。缓存位于仓库外 `/tmp/research-code-audit-20261022/nemotron-v1.pdf`，哈希用于以后核对；临时路径不承诺长期可用。
- 未解决：旧全文抽取目前仍在版本库，与现行“不入库全文”的规则不一致；保留既有资料，迁移待单独处理。本次没有删除它，也没有把占位提取模板当阅读证据。
