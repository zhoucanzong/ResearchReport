# 研究计划: Nemotron-Labs-Diffusion (Tri-Mode Language Model)
日期: 2026-05-27
来源 PDF: `/Users/zhoucanzong/Zotero/storage/VZ5BMRZW/Fu 等 - Nemotron-Labs-Diffusion ...pdf`

## 核心研究问题
NVIDIA 提出的 Nemotron-Labs-Diffusion (NLD) 在单一架构内统一了 AR、Diffusion、Self-Speculation 三种解码模式。本研究聚焦于：**该工作如何在不牺牲 AR 精度的前提下，通过联合 AR-Diffusion 训练同时解锁三种推理模式，从而在不同部署场景下都获得更优的"精度-吞吐"权衡？**

## 子问题分解
1. **训练框架（Sec.2）** — 如何在同一模型上联合优化 AR loss 与 block-wise diffusion denoising loss？两阶段训练、global loss averaging、注意力掩码（dual-stream）等关键技巧的作用？
2. **三模式推理（Sec.3）** — AR、Diffusion (confidence-based + 训练采样器)、Linear/Quadratic Self-Speculation 这三种模式的算法细节与各自的适用场景？特别是 self-speculation 中 diffusion 起草 + AR 验证的机制，以及 LoRA 增强 drafter 的方法。
3. **Speed-of-Light 分析（Sec.4）** — 如何用 "serial denoising + recursive dynamic compaction" 构造 SOL 上限？SOL 揭示了 diffusion 模式相对 self-speculation 有多大 headroom？
4. **实证表现（Sec.5-6）** — 在 3B/8B/14B 三种规模上，NLD 与 Qwen3、Ministral3、LLaDA、Dream、SDAR 等基线相比，accuracy、TPF、real-device throughput 各方面的对比？相较 Eagle3/MTP 的优势在哪？
5. **核心洞见（Sec.8）** — 论文给出的关键洞见与未来方向：AR/Diffusion 互补性、self-speculation > MTP、diffusion 的 SOL 潜力。

## 搜索策略
本任务为**单论文深度阅读**，无需 web 多轮搜索。原始 PDF 已完整提取至 `raw-extracts/nemotron-tri-mode-fulltext.md`（约 96K 字符 / 24K tokens）。

## 范围决策
- 包含: 训练框架、推理算法、SOL 分析、所有规模/模态的实验结果、相关工作综述、未来方向
- 排除: 详细附录（采样器细节、quadratic SS 完整算法）暂不展开，仅在概念性层面说明
- 语言: 中文笔记 + 关键技术术语保留英文（如 TPF、SOL、Self-Speculation 等）

## 输出物
- `raw-extracts/nemotron-tri-mode-fulltext.md` — PDF 全文提取（已完成）
- `papers/nemotron-labs-diffusion.json` — 结构化阅读 JSON
- `notes/structured-reading.md` — 深度阅读中文笔记
- `report.md` — 中文综述报告（重点 + 个人解读）
- `knowledge-graph.md` — 核心概念卡片
