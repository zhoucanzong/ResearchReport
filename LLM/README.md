<div align="center" markdown="1">

# 💬 LLM

**11 条** · 语言模型能力与技术专题，覆盖推理、对齐、Agent、RAG 等方向。

[← 返回首页](<../README.md>) · [完整索引](<../INDEX.md>)

</div>

<!-- SCRIPT:panel-readme START · 由 scripts/library_index.py 生成，勿手改 -->

![Entries](https://img.shields.io/badge/Entries-11-3f51b5?style=flat-square)
![Panel](https://img.shields.io/badge/Panel-LLM-9e9e9e?style=flat-square)

## 专题内分析

| 所属报告 | 分册入口 |
| --- | --- |
| 训练数据策展 | [预训练数据配比：从稳健重加权到代理回归](<TrainingData/topics/data-mixture.md>) |
| 视觉语言模型（VLM） | [VLM 评测的输入预算与 grounding：模型究竟看到了什么？](<VLM/topics/evaluation-input-budget.md>) |
| 视觉语言模型（VLM） | [VLMEvalKit 如何把 Video-MME 的回答变成分数](<VLM/topics/vlmevalkit-video-mme-path.md>) |

[查看研究专题与分析分册](<../index/by-topic.md>)

## 主报告

| 条目 | 报告 | 规模 |
| :-- | :-- | --: |
| **模型对齐与后训练** | [模型对齐与后训练：方法、目标与证据边界](<Alignment/report.md>) | 115 行 |
| **决策模型（Decision Models）** | [Decision Models（System One / Typed Decision Model）技术专题调研](<DecisionModels/report.md>) | 875 行 |
| **扩散语言模型** | [扩散语言模型：从随机遮盖到大规模并行生成](<DiffusionLM/report.md>) | 76 行 |
| **OCR 与文档解析** | [OCR 与文档解析：从字符识别到结构还原](<DocumentParsing/report.md>) | 102 行 |
| **长上下文** | [长上下文（Long Context）技术研究报告](<LongContext/report.md>) | 610 行 |
| **混合专家模型（MoE）** | [混合专家模型（Mixture of Experts, MoE）架构演进研究报告](<MoE/report.md>) | 406 行 |
| **检索增强生成（RAG）** | [检索增强生成（Retrieval-Augmented Generation, RAG）技术研究报告](<RAG/report.md>) | 835 行 |
| **推理模型与推理时计算** | [推理模型（Reasoning Models）与 Test-Time Compute 研究报告](<ReasoningModels/report.md>) | 676 行 |
| **LLM 后训练中的强化学习** | [LLM 后训练中的强化学习：轨迹从哪里来，策略何时更新](<ReinforcementLearning/report.md>) | 107 行 |
| **训练数据策展** | [训练数据策展：筛选、去重与配比如何改变训练结果](<TrainingData/report.md>) | 60 行 |
| **视觉语言模型（VLM）** | [多模态大模型（Vision-Language Models, VLM）研究报告](<VLM/report.md>) | 521 行 |

## 📎 子文档

<details>
<summary><b>决策模型（Decision Models）</b>（18 份）</summary>

* [calibration.md](<DecisionModels/calibration.md>) — 261 行 / 28,610 B
* [experiments.md](<DecisionModels/experiments.md>) — 349 行 / 25,166 B
* [open-implementations.md](<DecisionModels/open-implementations.md>) — 412 行 / 32,731 B
* [papers/2609.23886-this-that-model.md](<DecisionModels/papers/2609.23886-this-that-model.md>) — 289 行 / 22,356 B
* [papers/2609.23986-jev-mem.md](<DecisionModels/papers/2609.23986-jev-mem.md>) — 334 行 / 27,127 B
* [papers/2609.24052-crash-narrative-calibration.md](<DecisionModels/papers/2609.24052-crash-narrative-calibration.md>) — 98 行 / 12,094 B
* [papers/2609.24574-css-text-annotation.md](<DecisionModels/papers/2609.24574-css-text-annotation.md>) — 180 行 / 40,168 B
* [papers/2609.25845-visual-jev.md](<DecisionModels/papers/2609.25845-visual-jev.md>) — 291 行 / 22,086 B
* [papers/2609.26532-reflex-selective-control.md](<DecisionModels/papers/2609.26532-reflex-selective-control.md>) — 95 行 / 10,729 B
* [papers/2609.26550-jev-as-a-judge.md](<DecisionModels/papers/2609.26550-jev-as-a-judge.md>) — 60 行 / 5,512 B
* [papers/2609.26758-option-name-vs-definition.md](<DecisionModels/papers/2609.26758-option-name-vs-definition.md>) — 334 行 / 50,064 B
* [papers/2609.28613-decision-hijacking.md](<DecisionModels/papers/2609.28613-decision-hijacking.md>) — 317 行 / 26,528 B
* [papers/2609.30243-jevout-natural-context-flip.md](<DecisionModels/papers/2609.30243-jevout-natural-context-flip.md>) — 312 行 / 33,740 B
* [papers/2609.33209-probability-axioms-coherence.md](<DecisionModels/papers/2609.33209-probability-axioms-coherence.md>) — 92 行 / 10,252 B
* [papers/2610.09683-system-switch.md](<DecisionModels/papers/2610.09683-system-switch.md>) — 90 行 / 10,672 B
* [sources/CANDIDATES.md](<DecisionModels/sources/CANDIDATES.md>) — 70 行 / 8,181 B
* [sources/MANIFEST.md](<DecisionModels/sources/MANIFEST.md>) — 62 行 / 8,116 B
* [taxonomy.md](<DecisionModels/taxonomy.md>) — 254 行 / 25,036 B

</details>

<details>
<summary><b>扩散语言模型</b>（10 份）</summary>

* [papers/2502.09992-llada.md](<DiffusionLM/papers/2502.09992-llada.md>) — 86 行 / 12,781 B
* [papers/2503.09573-block-diffusion.md](<DiffusionLM/papers/2503.09573-block-diffusion.md>) — 59 行 / 7,692 B
* [papers/2505.19223-llada-1.5-vrpo.md](<DiffusionLM/papers/2505.19223-llada-1.5-vrpo.md>) — 105 行 / 12,723 B
* [papers/2510.06303-sdar.md](<DiffusionLM/papers/2510.06303-sdar.md>) — 60 行 / 8,324 B
* [papers/2601.22031-card.md](<DiffusionLM/papers/2601.22031-card.md>) — 63 行 / 8,604 B
* [papers/LLaDA2.0-Scaling-to-100B.md](<DiffusionLM/papers/LLaDA2.0-Scaling-to-100B.md>) — 63 行 / 9,346 B
* [papers/LLaDA2.1-Token-Editing.md](<DiffusionLM/papers/LLaDA2.1-Token-Editing.md>) — 65 行 / 9,366 B
* [papers/LLaDA2.2-Levenshtein-Editing.md](<DiffusionLM/papers/LLaDA2.2-Levenshtein-Editing.md>) — 64 行 / 11,889 B
* [sources/CANDIDATES.md](<DiffusionLM/sources/CANDIDATES.md>) — 32 行 / 4,175 B
* [sources/MANIFEST.md](<DiffusionLM/sources/MANIFEST.md>) — 21 行 / 5,028 B

</details>

<details>
<summary><b>OCR 与文档解析</b>（16 份）</summary>

* [papers/2412.07626-omnidocbench.md](<DocumentParsing/papers/2412.07626-omnidocbench.md>) — 42 行 / 9,196 B
* [papers/2505.14059-bytedance-dolphin.md](<DocumentParsing/papers/2505.14059-bytedance-dolphin.md>) — 40 行 / 5,505 B
* [papers/2509.19760-alibaba-logics-parsing.md](<DocumentParsing/papers/2509.19760-alibaba-logics-parsing.md>) — 38 行 / 5,449 B
* [papers/2510.14528-paddleocr-vl.md](<DocumentParsing/papers/2510.14528-paddleocr-vl.md>) — 53 行 / 10,262 B
* [papers/2510.18234-deepseek-ocr.md](<DocumentParsing/papers/2510.18234-deepseek-ocr.md>) — 47 行 / 8,883 B
* [papers/2510.21603-huawei-doc-researcher.md](<DocumentParsing/papers/2510.21603-huawei-doc-researcher.md>) — 38 行 / 5,906 B
* [papers/2511.19575-hunyuan-ocr.md](<DocumentParsing/papers/2511.19575-hunyuan-ocr.md>) — 39 行 / 8,134 B
* [papers/2601.20552-deepseek-ocr2.md](<DocumentParsing/papers/2601.20552-deepseek-ocr2.md>) — 45 行 / 8,359 B
* [papers/2603.01840-firered-ocr.md](<DocumentParsing/papers/2603.01840-firered-ocr.md>) — 39 行 / 6,932 B
* [papers/2603.13032-multimodal-ocr.md](<DocumentParsing/papers/2603.13032-multimodal-ocr.md>) — 41 行 / 7,530 B
* [papers/2603.24326-coarse-to-fine.md](<DocumentParsing/papers/2603.24326-coarse-to-fine.md>) — 67 行 / 9,350 B
* [papers/2603.28130-mdpbench.md](<DocumentParsing/papers/2603.28130-mdpbench.md>) — 51 行 / 10,106 B
* [papers/2605.17447-jd-fastocr.md](<DocumentParsing/papers/2605.17447-jd-fastocr.md>) — 40 行 / 5,443 B
* [papers/2605.27978-amap-abot-ocr.md](<DocumentParsing/papers/2605.27978-amap-abot-ocr.md>) — 42 行 / 5,791 B
* [papers/2607.04884-hunyuan-ocr-15.md](<DocumentParsing/papers/2607.04884-hunyuan-ocr-15.md>) — 53 行 / 11,829 B
* [papers/2607.21617-amazon-faithc4.md](<DocumentParsing/papers/2607.21617-amazon-faithc4.md>) — 39 行 / 6,093 B

</details>

<details>
<summary><b>LLM 后训练中的强化学习</b>（10 份）</summary>

* [papers/2305.20050-prm800k.md](<ReinforcementLearning/papers/2305.20050-prm800k.md>) — 23 行 / 3,412 B
* [papers/2501.07301-process-reward-model-lessons.md](<ReinforcementLearning/papers/2501.07301-process-reward-model-lessons.md>) — 26 行 / 3,807 B
* [papers/2506.14245-rlvr-correct-reasoning.md](<ReinforcementLearning/papers/2506.14245-rlvr-correct-reasoning.md>) — 22 行 / 3,100 B
* [papers/2609.01354-category-level-verifier-audit.md](<ReinforcementLearning/papers/2609.01354-category-level-verifier-audit.md>) — 29 行 / 5,922 B
* [papers/2609.35677-verifier-errors-selective-control.md](<ReinforcementLearning/papers/2609.35677-verifier-errors-selective-control.md>) — 29 行 / 7,044 B
* [papers/loop.md](<ReinforcementLearning/papers/loop.md>) — 28 行 / 4,539 B
* [papers/online-preference.md](<ReinforcementLearning/papers/online-preference.md>) — 28 行 / 3,980 B
* [papers/prime.md](<ReinforcementLearning/papers/prime.md>) — 30 行 / 4,636 B
* [sources/CANDIDATES.md](<ReinforcementLearning/sources/CANDIDATES.md>) — 26 行 / 4,756 B
* [sources/MANIFEST.md](<ReinforcementLearning/sources/MANIFEST.md>) — 43 行 / 9,592 B

</details>

<details>
<summary><b>训练数据策展</b>（6 份）</summary>

* [papers/2107.06499-deduplicating-training-data.md](<TrainingData/papers/2107.06499-deduplicating-training-data.md>) — 24 行 / 2,755 B
* [papers/2406.11794-datacomp-lm.md](<TrainingData/papers/2406.11794-datacomp-lm.md>) — 27 行 / 3,389 B
* [papers/2406.17557-fineweb.md](<TrainingData/papers/2406.17557-fineweb.md>) — 24 行 / 3,175 B
* [sources/CANDIDATES.md](<TrainingData/sources/CANDIDATES.md>) — 15 行 / 1,873 B
* [sources/MANIFEST.md](<TrainingData/sources/MANIFEST.md>) — 20 行 / 4,832 B
* [topics/data-mixture.md](<TrainingData/topics/data-mixture.md>) — 43 行 / 8,270 B

</details>

<details>
<summary><b>视觉语言模型（VLM）</b>（3 份）</summary>

* [papers/2405.21075-videomme.md](<VLM/papers/2405.21075-videomme.md>) — 35 行 / 7,567 B
* [topics/evaluation-input-budget.md](<VLM/topics/evaluation-input-budget.md>) — 46 行 / 6,622 B
* [topics/vlmevalkit-video-mme-path.md](<VLM/topics/vlmevalkit-video-mme-path.md>) — 51 行 / 10,053 B

</details>

<!-- SCRIPT:panel-readme END -->

---

<sub>本 README 由 `scripts/library_index.py` 自动生成（`scripts/panels.json` 驱动）；完整索引见 [INDEX.md](<../INDEX.md>) 与 [index/](<../index/>)。</sub>
