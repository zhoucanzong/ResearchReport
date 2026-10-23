# Qwen 定向方法论文来源清单（2026-10-23）

> 范围：本次只核对指定 arXiv v1 论文中的 Omni 后训练实验。候选筛选记录见 [CANDIDATES.md](CANDIDATES.md)；逐篇精读见 [papers/](../papers/)。不据此更新产品版本、模型卡或 Qwen 内部训练流程。

## 固定原文与读取范围

| 来源 | 固定身份 / 许可 | 全文锚点 |
|---|---|---|
| Cheng et al., [Text-Centric Post-Training for Omni-Modal Reasoning](https://arxiv.org/abs/2610.02819v1) | arXiv `2610.02819v1`，2026-10-02 05:08:25 UTC 提交；版本页提供 arXiv non-exclusive distribution license；预印本 | 官方 v1 PDF 全文 28 页；重点核对 §3.1–3.2/Fig. 2，§4.1–4.2，§5.1–5.5/Tables 2–6，§6。摘要、版本历史与许可以固定版本页/PDF首页为准。 |

PaperFetcher 记录：`search_papers.py "Text-Centric Post-Training for Omni-Modal Reasoning" -n 3 -s arxiv` 找到该论文，返回题名、作者及 v1 日期；`fetch_paper.py fetch 2610.02819v1 --citations` 返回 8 位作者、摘要、分类 `cs.CL` 和固定 v1 链接。PDF 下载脚本产生空文件；随后从 arXiv 固定 PDF URL 完成下载并校验 28 页。缓存路径 `/Users/zhoucanzong/Documents/paper-cache/research-audit-2026-10-23/models/methods/2610.02819v1.pdf`，15,743,521 bytes，SHA-256 `276ce427d853cc8fe01e8c47a3cf299cc9e17e4b15b5cd2f3d4bd58143211d5b`。同目录保留 `2610.02819v1.html`。

## 数字主张核验

- Table 2：Qwen2.5-Omni-7B 推理 Macro Avg. 39.80→49.39，几何均值相对改进 +25.83%；文本 SFT→GRPO 预算为 0.505B input tokens、284.17 GPU-hours，完整音视频 SFT→GRPO 为 1.306B、654.52 GPU-hours（节省 61.3% tokens、56.6% GPU-hours）。
- Table 5：文本 SFT→GRPO 后感知 Macro Avg. 77.37→76.41（下降 0.96）；论文报告几何均值变化 −1.25%。
- Table 6：减少数据音视频 GRPO 的共享输入预算 0.122B tokens、82.7 GPU-hours；相对完整音视频 GRPO 输入 token 减少约 90%。文本 SFT→GRPO 后接该步骤，推理几何均值提升 +24.15%，为 25.83% 的 93.5%；感知 Macro Avg. 为 78.50。
- Table 3：Qwen2.5-Omni-3B、Qwen3-Omni-30B-A3B 与 Gemma-4 结果支持跨设置的方向性观察，但训练对照不同；没有把这些结果合并成统一效果量。

## 解释边界

以上均为作者实验；没有独立复跑训练或评测。主要分阶段结果来自 Qwen2.5-Omni-7B 和有限基准，宏平均/几何平均不代表真实任务全覆盖。梯度投影是局部诊断而非能力模块分离证明。作者报告的训练预算不等于生产硬件成本。不得将结果写成 Qwen3.5-Omni 等后续型号的训练配方或内部训练事实。
