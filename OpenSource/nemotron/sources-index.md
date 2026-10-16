# 来源索引 (Sources Index)

> 最后更新: 2026-05-27
> 总条目: 1（单论文深度阅读）

## 主要论文（本次研究对象）

| ID | 标题 | 作者 | 日期 | 来源 | 提取文件 |
|----|------|------|------|------|----------|
| nld-2026 | Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding | Yonggan Fu et al. (NVIDIA + Georgia Tech + HKU + MIT) | 2026-05-19 | 本地 PDF (Zotero) | [全文提取](raw-extracts/nemotron-tri-mode-fulltext.md) |

- **页数**: 21
- **原始路径**: `/Users/zhoucanzong/Zotero/storage/VZ5BMRZW/Fu 等 - Nemotron-Labs-Diffusion A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Spec.pdf`
- **模型开源**: Hugging Face — Nemotron-Labs-Diffusion 模型家族（3B/8B/14B base/instruct/VLM）
- **训练框架**: Megatron Bridge（NVIDIA 已 release training/inference pipeline）

## PDF（脚本自动生成的占位）

- [pdf-fu_等__nemotronlabsdiffusion_a_trimode_language_model_unifying_autoregressive_dif](raw-extracts/pdf-fu_等__nemotronlabsdiffusion_a_trimode_language_model_unifying_autoregressive_dif.md) — 2026-05-27（提取模板，正文见上方完整提取）

## 论文中重要的引用上下文

| Ref | 论文 | 角色 |
|-----|------|------|
| [1] | SPEED-Bench (Abramovich et al. 2026) | 评测基准 |
| [2] | LLaDA (Nie et al. 2025) | Diffusion LM 基线 |
| [3] | Dream-7B (Ye et al. 2025) | Diffusion LM 基线 |
| [4] | SDAR-8B (Cheng et al. 2025) | Diffusion-AR 混合基线 |
| [7] | "Your LLM knows the future" (Samragh et al. 2025) | AR 模型的 lookahead 能力分析 |
| [8] | Eagle-3 (Li et al. 2025) | MTP/SD 主要竞争对手 |
| [9] | Block Diffusion (Arriola et al. 2025) | block-wise 注意力设计起源 |
| [10] | Fu et al. (block-wise diffusion 后续工作) | 沿用其 block-wise 设置 |
| [13] | confidence-based sampling 相关工作 | diffusion 解码策略 |
| [14] | 联合 AR + Diffusion 训练的先驱工作 | 本文方法论的最近邻 |
| [17] | Speculative Decoding (Leviathan et al.) | 推测解码经典工作 |
| [18] | LoRA (Hu et al.) | drafter 增强方式 |
| [19] | LK-hybrid loss | 分布匹配 loss |
| [21] | Ministral3 | 训练起点的预训练模型 |

## 其它资源（暂未使用）
- 无 web 搜索内容（本任务为单论文深读）
