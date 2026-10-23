# Research 仓库图书馆索引

> 本文件由 scripts/library_index.py 自动生成，请勿手改。
> 生成命令：`python3 scripts/library_index.py --repo-root . --out-root .`
> 输出根目录：`.`
> 条目口径：条目 = `report.md`

---

## 统计总览

> 数字由 `scripts/library_index.py` 产出；机器可读版见 [index/stats.json](<index/stats.json>)。生成物（本文件、`index/*`）不计入**条目与文档**计数；「纳入版本控制」两行取自 `git ls-files`，**含**生成物本身。

| 指标 | 数量 |
| --- | --- |
| **条目数**（`report.md`） | **64** |
| 板块（[`scripts/panels.json`](<scripts/panels.json>)） | Models 23 · LLM 11 · VisualGen 8 · WorldModel 2 · AI4Science 10 · Evaluation 1 · Infra 3 · OpenSource 6 |
| 条目子文档数 | 204 |
| 条目正文行数（剔除 front-matter） | 27,918 |
| 条目字节 | 2,114,262 B |
| 带 front-matter 的条目 | 23 |
| 带合法 `date` 的条目 | 23 |
| 文档（除生成物外的全部 `.md`） | 286 |
| 其中文件名 `README.md` | 10 |
| 纳入版本控制的文件 | 307 |
| 纳入版本控制的 `.md` | 291 |

> 条目 = `report.md`；`README.md`（根 / 子库 / `scripts/`）、`docs/*.md`、`notes/`、`raw-extracts/`、`plan.md`、`sources-index.md`、`knowledge-graph.md` 都是**文档而非条目**，仅在所属条目的折叠块里作为子文档出现。
> **板块**是逻辑视图（跨物理目录），映射全部在 [`scripts/panels.json`](<scripts/panels.json>)；每个条目恰好归入一个板块，未归类 / 重复归类 / 代表条目缺 `report.md` 都会让脚本在生成前非零退出。

## 按板块入口

| 资料库 | 条目数 | 文档（`.md`） | 条目行数 | 条目字节 | 入口 |
| --- | --: | --: | --: | --: | --- |
| Models | 23 | 41 | 12,127 | 906,140 B | [板块页 →](<Models/README.md>) |
| LLM | 11 | 55 | 4,365 | 343,808 B | [板块页 →](<LLM/README.md>) |
| VisualGen | 8 | 9 | 6,758 | 320,420 B | [板块页 →](<VisualGen/README.md>) |
| WorldModel | 2 | 41 | 1,244 | 139,523 B | [板块页 →](<WorldModel/README.md>) |
| AI4Science | 10 | 53 | 836 | 138,955 B | [板块页 →](<AI4Science/README.md>) |
| Evaluation | 1 | 7 | 101 | 21,992 B | [板块页 →](<Evaluation/README.md>) |
| Infra | 3 | 37 | 918 | 75,497 B | [板块页 →](<Infra/README.md>) |
| OpenSource | 6 | 35 | 1,569 | 167,927 B | [板块页 →](<OpenSource/README.md>) |
| **合计** | **64** | **286** | **27,918** | **2,114,262 B** | — |

## 分面索引

| 分面 | 说明 |
| --- | --- |
| [index/by-domain.md](<index/by-domain.md>) | 按领域（domain） |
| [index/by-subject.md](<index/by-subject.md>) | 按主题（subject） |
| [index/by-repo.md](<index/by-repo.md>) | 按来源仓库（upstream / 本地库根） |
| [index/by-topic.md](<index/by-topic.md>) | 按专题（topic） |
| [index/by-report.md](<index/by-report.md>) | 按条目（report.md）平铺 |
| [index/recent.md](<index/recent.md>) | 最近更新（按 date 降序） |
| [index/stale.md](<index/stale.md>) | 陈旧 / 待复核（status 或超期） |

## 条目索引（按板块目录折叠，可直达条目与子报告）

### Models（23 条目 / 41 文档）

<details>
<summary><b>模型系列 Models（23 条目 / 17 子文档）</b></summary>

  <details>
  <summary><b>Alibaba-Gen</b> · <code>Models/Alibaba-Gen/report.md</code> · 117 行 · —</summary>


    * **条目**：[Models/Alibaba-Gen/report.md](<Models/Alibaba-Gen/report.md>)（117 行 / 15,414 B）
    * **专题目录**：`Models/Alibaba-Gen`
    * **元数据**：type=`—` · domain=`Models` · subject=`Alibaba-Gen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>ByteDance-Gen</b> · <code>Models/ByteDance-Gen/report.md</code> · 347 行 · —</summary>


    * **条目**：[Models/ByteDance-Gen/report.md](<Models/ByteDance-Gen/report.md>)（347 行 / 26,232 B）
    * **专题目录**：`Models/ByteDance-Gen`
    * **元数据**：type=`—` · domain=`Models` · subject=`ByteDance-Gen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Claude</b> · <code>Models/Claude/report.md</code> · 604 行 · —</summary>


    * **条目**：[Models/Claude/report.md](<Models/Claude/report.md>)（604 行 / 53,717 B）
    * **专题目录**：`Models/Claude`
    * **元数据**：type=`—` · domain=`Models` · subject=`Claude` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>DeepSeek</b> · <code>Models/DeepSeek/report.md</code> · 776 行 · —</summary>


    * **条目**：[Models/DeepSeek/report.md](<Models/DeepSeek/report.md>)（776 行 / 66,117 B）
    * **专题目录**：`Models/DeepSeek`
    * **元数据**：type=`—` · domain=`Models` · subject=`DeepSeek` · date=`—` · status=`—`
    * **子文档（6）**
        * [deepseek-multimodal-and-specialized.md](<Models/DeepSeek/deepseek-multimodal-and-specialized.md>) — 367 行 / 24,706 B
        * [deepseek-phase-sensitivity.md](<Models/DeepSeek/deepseek-phase-sensitivity.md>) — 76 行 / 11,595 B
        * [deepseek-text-models.md](<Models/DeepSeek/deepseek-text-models.md>) — 418 行 / 36,554 B
        * [papers/2610.06851-base-model-cues.md](<Models/DeepSeek/papers/2610.06851-base-model-cues.md>) — 55 行 / 5,163 B
        * [sources/CANDIDATES.md](<Models/DeepSeek/sources/CANDIDATES.md>) — 7 行 / 745 B
        * [sources/MANIFEST.md](<Models/DeepSeek/sources/MANIFEST.md>) — 128 行 / 18,126 B

  </details>

  <details>
  <summary><b>Doubao-Seed</b> · <code>Models/Doubao-Seed/report.md</code> · 651 行 · —</summary>


    * **条目**：[Models/Doubao-Seed/report.md](<Models/Doubao-Seed/report.md>)（651 行 / 29,957 B）
    * **专题目录**：`Models/Doubao-Seed`
    * **元数据**：type=`—` · domain=`Models` · subject=`Doubao-Seed` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>GLM</b> · <code>Models/GLM/report.md</code> · 737 行 · —</summary>


    * **条目**：[Models/GLM/report.md](<Models/GLM/report.md>)（737 行 / 68,351 B）
    * **专题目录**：`Models/GLM`
    * **元数据**：type=`—` · domain=`Models` · subject=`GLM` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>GPT</b> · <code>Models/GPT/report.md</code> · 785 行 · —</summary>


    * **条目**：[Models/GPT/report.md](<Models/GPT/report.md>)（785 行 / 61,581 B）
    * **专题目录**：`Models/GPT`
    * **元数据**：type=`—` · domain=`Models` · subject=`GPT` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Gemini</b> · <code>Models/Gemini/report.md</code> · 842 行 · —</summary>


    * **条目**：[Models/Gemini/report.md](<Models/Gemini/report.md>)（842 行 / 45,955 B）
    * **专题目录**：`Models/Gemini`
    * **元数据**：type=`—` · domain=`Models` · subject=`Gemini` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Google-Gen</b> · <code>Models/Google-Gen/report.md</code> · 895 行 · —</summary>


    * **条目**：[Models/Google-Gen/report.md](<Models/Google-Gen/report.md>)（895 行 / 42,826 B）
    * **专题目录**：`Models/Google-Gen`
    * **元数据**：type=`—` · domain=`Models` · subject=`Google-Gen` · date=`—` · status=`—`
    * **子文档（1）**
        * [papers/2604.20329-vision-banana.md](<Models/Google-Gen/papers/2604.20329-vision-banana.md>) — 425 行 / 55,019 B

  </details>

  <details>
  <summary><b>Grok</b> · <code>Models/Grok/report.md</code> · 265 行 · —</summary>


    * **条目**：[Models/Grok/report.md](<Models/Grok/report.md>)（265 行 / 18,947 B）
    * **专题目录**：`Models/Grok`
    * **元数据**：type=`—` · domain=`Models` · subject=`Grok` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Hunyuan</b> · <code>Models/Hunyuan/report.md</code> · 504 行 · —</summary>


    * **条目**：[Models/Hunyuan/report.md](<Models/Hunyuan/report.md>)（504 行 / 42,348 B）
    * **专题目录**：`Models/Hunyuan`
    * **元数据**：type=`—` · domain=`Models` · subject=`Hunyuan` · date=`—` · status=`—`
    * **子文档（1）**
        * [sources/MANIFEST.md](<Models/Hunyuan/sources/MANIFEST.md>) — 78 行 / 19,522 B

  </details>

  <details>
  <summary><b>Kimi</b> · <code>Models/Kimi/report.md</code> · 585 行 · —</summary>


    * **条目**：[Models/Kimi/report.md](<Models/Kimi/report.md>)（585 行 / 52,148 B）
    * **专题目录**：`Models/Kimi`
    * **元数据**：type=`—` · domain=`Models` · subject=`Kimi` · date=`—` · status=`—`
    * **子文档（2）**
        * [papers/2607.24653-kimi-k3.md](<Models/Kimi/papers/2607.24653-kimi-k3.md>) — 247 行 / 28,554 B
        * [sources/MANIFEST.md](<Models/Kimi/sources/MANIFEST.md>) — 56 行 / 6,030 B

  </details>

  <details>
  <summary><b>Kling</b> · <code>Models/Kling/report.md</code> · 75 行 · —</summary>


    * **条目**：[Models/Kling/report.md](<Models/Kling/report.md>)（75 行 / 9,334 B）
    * **专题目录**：`Models/Kling`
    * **元数据**：type=`—` · domain=`Models` · subject=`Kling` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>LLaMA</b> · <code>Models/LLaMA/report.md</code> · 483 行 · —</summary>


    * **条目**：[Models/LLaMA/report.md](<Models/LLaMA/report.md>)（483 行 / 42,535 B）
    * **专题目录**：`Models/LLaMA`
    * **元数据**：type=`—` · domain=`Models` · subject=`LLaMA` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>MiMo</b> · <code>Models/MiMo/report.md</code> · 757 行 · —</summary>


    * **条目**：[Models/MiMo/report.md](<Models/MiMo/report.md>)（757 行 / 64,784 B）
    * **专题目录**：`Models/MiMo`
    * **元数据**：type=`—` · domain=`Models` · subject=`MiMo` · date=`—` · status=`—`
    * **子文档（1）**
        * [papers/2610.11959-mimo-v2-6.md](<Models/MiMo/papers/2610.11959-mimo-v2-6.md>) — 437 行 / 36,488 B

  </details>

  <details>
  <summary><b>Midjourney</b> · <code>Models/Midjourney/report.md</code> · 85 行 · —</summary>


    * **条目**：[Models/Midjourney/report.md](<Models/Midjourney/report.md>)（85 行 / 9,426 B）
    * **专题目录**：`Models/Midjourney`
    * **元数据**：type=`—` · domain=`Models` · subject=`Midjourney` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>MiniMax</b> · <code>Models/MiniMax/report.md</code> · 524 行 · —</summary>


    * **条目**：[Models/MiniMax/report.md](<Models/MiniMax/report.md>)（524 行 / 42,545 B）
    * **专题目录**：`Models/MiniMax`
    * **元数据**：type=`—` · domain=`Models` · subject=`MiniMax` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Mistral</b> · <code>Models/Mistral/report.md</code> · 502 行 · —</summary>


    * **条目**：[Models/Mistral/report.md](<Models/Mistral/report.md>)（502 行 / 31,260 B）
    * **专题目录**：`Models/Mistral`
    * **元数据**：type=`—` · domain=`Models` · subject=`Mistral` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Nemotron</b> · <code>Models/Nemotron/report.md</code> · 238 行 · —</summary>


    * **条目**：[Models/Nemotron/report.md](<Models/Nemotron/report.md>)（238 行 / 22,850 B）
    * **专题目录**：`Models/Nemotron`
    * **元数据**：type=`—` · domain=`Models` · subject=`Nemotron` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>OpenAI-Gen</b> · <code>Models/OpenAI-Gen/report.md</code> · 393 行 · —</summary>


    * **条目**：[Models/OpenAI-Gen/report.md](<Models/OpenAI-Gen/report.md>)（393 行 / 25,108 B）
    * **专题目录**：`Models/OpenAI-Gen`
    * **元数据**：type=`—` · domain=`Models` · subject=`OpenAI-Gen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Qwen</b> · <code>Models/Qwen/report.md</code> · 1120 行 · —</summary>


    * **条目**：[Models/Qwen/report.md](<Models/Qwen/report.md>)（1120 行 / 75,464 B）
    * **专题目录**：`Models/Qwen`
    * **元数据**：type=`—` · domain=`Models` · subject=`Qwen` · date=`—` · status=`—`
    * **子文档（6）**
        * [papers/2610.02819-text-centric-omni.md](<Models/Qwen/papers/2610.02819-text-centric-omni.md>) — 55 行 / 5,789 B
        * [qwen-omni-and-ecosystem.md](<Models/Qwen/qwen-omni-and-ecosystem.md>) — 565 行 / 22,788 B
        * [qwen-text-models.md](<Models/Qwen/qwen-text-models.md>) — 489 行 / 20,718 B
        * [qwen-vl-models.md](<Models/Qwen/qwen-vl-models.md>) — 543 行 / 22,018 B
        * [sources/CANDIDATES.md](<Models/Qwen/sources/CANDIDATES.md>) — 7 行 / 718 B
        * [sources/MANIFEST.md](<Models/Qwen/sources/MANIFEST.md>) — 22 行 / 2,714 B

  </details>

  <details>
  <summary><b>Runway</b> · <code>Models/Runway/report.md</code> · 103 行 · —</summary>


    * **条目**：[Models/Runway/report.md](<Models/Runway/report.md>)（103 行 / 12,682 B）
    * **专题目录**：`Models/Runway`
    * **元数据**：type=`—` · domain=`Models` · subject=`Runway` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>StabilityAI</b> · <code>Models/StabilityAI/report.md</code> · 739 行 · —</summary>


    * **条目**：[Models/StabilityAI/report.md](<Models/StabilityAI/report.md>)（739 行 / 46,559 B）
    * **专题目录**：`Models/StabilityAI`
    * **元数据**：type=`—` · domain=`Models` · subject=`StabilityAI` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

</details>

### LLM（11 条目 / 55 文档）

<details>
<summary><b>语言模型 LLM（11 条目 / 43 子文档）</b></summary>

  <details>
  <summary><b>Agent</b> · <code>LLM/Agent/report.md</code> · 105 行 · —</summary>


    * **条目**：[LLM/Agent/report.md](<LLM/Agent/report.md>)（105 行 / 9,656 B）
    * **专题目录**：`LLM/Agent`
    * **元数据**：type=`—` · domain=`LLM` · subject=`Agent` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Alignment</b> · <code>LLM/Alignment/report.md</code> · 114 行 · —</summary>


    * **条目**：[LLM/Alignment/report.md](<LLM/Alignment/report.md>)（114 行 / 10,543 B）
    * **专题目录**：`LLM/Alignment`
    * **元数据**：type=`—` · domain=`LLM` · subject=`Alignment` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>DecisionModels</b> · <code>LLM/DecisionModels/report.md</code> · 874 行 · —</summary>


    * **条目**：[LLM/DecisionModels/report.md](<LLM/DecisionModels/report.md>)（874 行 / 109,140 B）
    * **专题目录**：`LLM/DecisionModels`
    * **元数据**：type=`—` · domain=`LLM` · subject=`DecisionModels` · date=`—` · status=`—`
    * **子文档（18）**
        * [calibration.md](<LLM/DecisionModels/calibration.md>) — 261 行 / 28,610 B
        * [experiments.md](<LLM/DecisionModels/experiments.md>) — 349 行 / 25,166 B
        * [open-implementations.md](<LLM/DecisionModels/open-implementations.md>) — 412 行 / 32,731 B
        * [papers/2609.23886-this-that-model.md](<LLM/DecisionModels/papers/2609.23886-this-that-model.md>) — 289 行 / 22,356 B
        * [papers/2609.23986-jev-mem.md](<LLM/DecisionModels/papers/2609.23986-jev-mem.md>) — 334 行 / 27,127 B
        * [papers/2609.24052-crash-narrative-calibration.md](<LLM/DecisionModels/papers/2609.24052-crash-narrative-calibration.md>) — 98 行 / 12,094 B
        * [papers/2609.24574-css-text-annotation.md](<LLM/DecisionModels/papers/2609.24574-css-text-annotation.md>) — 180 行 / 40,168 B
        * [papers/2609.25845-visual-jev.md](<LLM/DecisionModels/papers/2609.25845-visual-jev.md>) — 291 行 / 22,086 B
        * [papers/2609.26532-reflex-selective-control.md](<LLM/DecisionModels/papers/2609.26532-reflex-selective-control.md>) — 95 行 / 10,729 B
        * [papers/2609.26550-jev-as-a-judge.md](<LLM/DecisionModels/papers/2609.26550-jev-as-a-judge.md>) — 60 行 / 5,511 B
        * [papers/2609.26758-option-name-vs-definition.md](<LLM/DecisionModels/papers/2609.26758-option-name-vs-definition.md>) — 334 行 / 50,064 B
        * [papers/2609.28613-decision-hijacking.md](<LLM/DecisionModels/papers/2609.28613-decision-hijacking.md>) — 317 行 / 26,528 B
        * [papers/2609.30243-jevout-natural-context-flip.md](<LLM/DecisionModels/papers/2609.30243-jevout-natural-context-flip.md>) — 312 行 / 33,740 B
        * [papers/2609.33209-probability-axioms-coherence.md](<LLM/DecisionModels/papers/2609.33209-probability-axioms-coherence.md>) — 92 行 / 10,252 B
        * [papers/2610.09683-system-switch.md](<LLM/DecisionModels/papers/2610.09683-system-switch.md>) — 90 行 / 10,672 B
        * [sources/CANDIDATES.md](<LLM/DecisionModels/sources/CANDIDATES.md>) — 70 行 / 8,181 B
        * [sources/MANIFEST.md](<LLM/DecisionModels/sources/MANIFEST.md>) — 62 行 / 8,116 B
        * [taxonomy.md](<LLM/DecisionModels/taxonomy.md>) — 254 行 / 25,036 B

  </details>

  <details>
  <summary><b>DiffusionLM</b> · <code>LLM/DiffusionLM/report.md</code> · 70 行 · 2026-10-23</summary>


    * **条目**：[LLM/DiffusionLM/report.md](<LLM/DiffusionLM/report.md>)（70 行 / 11,793 B）
    * **专题目录**：`LLM/DiffusionLM`
    * **元数据**：type=`topic-research` · domain=`LLM` · subject=`DiffusionLM` · date=`2026-10-23` · status=`current`
    * **子文档（10）**
        * [papers/2502.09992-llada.md](<LLM/DiffusionLM/papers/2502.09992-llada.md>) — 86 行 / 12,921 B
        * [papers/2503.09573-block-diffusion.md](<LLM/DiffusionLM/papers/2503.09573-block-diffusion.md>) — 59 行 / 7,832 B
        * [papers/2505.19223-llada-1.5-vrpo.md](<LLM/DiffusionLM/papers/2505.19223-llada-1.5-vrpo.md>) — 105 行 / 12,891 B
        * [papers/2510.06303-sdar.md](<LLM/DiffusionLM/papers/2510.06303-sdar.md>) — 60 行 / 8,492 B
        * [papers/2601.22031-card.md](<LLM/DiffusionLM/papers/2601.22031-card.md>) — 63 行 / 8,800 B
        * [papers/LLaDA2.0-Scaling-to-100B.md](<LLM/DiffusionLM/papers/LLaDA2.0-Scaling-to-100B.md>) — 63 行 / 9,346 B
        * [papers/LLaDA2.1-Token-Editing.md](<LLM/DiffusionLM/papers/LLaDA2.1-Token-Editing.md>) — 65 行 / 9,366 B
        * [papers/LLaDA2.2-Levenshtein-Editing.md](<LLM/DiffusionLM/papers/LLaDA2.2-Levenshtein-Editing.md>) — 64 行 / 11,889 B
        * [sources/CANDIDATES.md](<LLM/DiffusionLM/sources/CANDIDATES.md>) — 29 行 / 3,474 B
        * [sources/MANIFEST.md](<LLM/DiffusionLM/sources/MANIFEST.md>) — 21 行 / 5,168 B

  </details>

  <details>
  <summary><b>LongContext</b> · <code>LLM/LongContext/report.md</code> · 609 行 · —</summary>


    * **条目**：[LLM/LongContext/report.md](<LLM/LongContext/report.md>)（609 行 / 31,223 B）
    * **专题目录**：`LLM/LongContext`
    * **元数据**：type=`—` · domain=`LLM` · subject=`LongContext` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>MoE</b> · <code>LLM/MoE/report.md</code> · 405 行 · —</summary>


    * **条目**：[LLM/MoE/report.md](<LLM/MoE/report.md>)（405 行 / 28,869 B）
    * **专题目录**：`LLM/MoE`
    * **元数据**：type=`—` · domain=`LLM` · subject=`MoE` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>RAG</b> · <code>LLM/RAG/report.md</code> · 834 行 · —</summary>


    * **条目**：[LLM/RAG/report.md](<LLM/RAG/report.md>)（834 行 / 45,460 B）
    * **专题目录**：`LLM/RAG`
    * **元数据**：type=`—` · domain=`LLM` · subject=`RAG` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>ReasoningModels</b> · <code>LLM/ReasoningModels/report.md</code> · 675 行 · —</summary>


    * **条目**：[LLM/ReasoningModels/report.md](<LLM/ReasoningModels/report.md>)（675 行 / 35,781 B）
    * **专题目录**：`LLM/ReasoningModels`
    * **元数据**：type=`—` · domain=`LLM` · subject=`ReasoningModels` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>ReinforcementLearning</b> · <code>LLM/ReinforcementLearning/report.md</code> · 107 行 · 2026-10-23</summary>


    * **条目**：[LLM/ReinforcementLearning/report.md](<LLM/ReinforcementLearning/report.md>)（107 行 / 22,864 B）
    * **专题目录**：`LLM/ReinforcementLearning`
    * **元数据**：type=`research` · domain=`LLM` · subject=`ReinforcementLearning` · date=`2026-10-23` · status=`current`
    * **子文档（10）**
        * [papers/2305.20050-prm800k.md](<LLM/ReinforcementLearning/papers/2305.20050-prm800k.md>) — 23 行 / 3,412 B
        * [papers/2501.07301-process-reward-model-lessons.md](<LLM/ReinforcementLearning/papers/2501.07301-process-reward-model-lessons.md>) — 26 行 / 3,807 B
        * [papers/2506.14245-rlvr-correct-reasoning.md](<LLM/ReinforcementLearning/papers/2506.14245-rlvr-correct-reasoning.md>) — 22 行 / 3,100 B
        * [papers/2609.01354-category-level-verifier-audit.md](<LLM/ReinforcementLearning/papers/2609.01354-category-level-verifier-audit.md>) — 29 行 / 5,950 B
        * [papers/2609.35677-verifier-errors-selective-control.md](<LLM/ReinforcementLearning/papers/2609.35677-verifier-errors-selective-control.md>) — 29 行 / 7,072 B
        * [papers/loop.md](<LLM/ReinforcementLearning/papers/loop.md>) — 28 行 / 4,539 B
        * [papers/online-preference.md](<LLM/ReinforcementLearning/papers/online-preference.md>) — 28 行 / 3,980 B
        * [papers/prime.md](<LLM/ReinforcementLearning/papers/prime.md>) — 30 行 / 4,636 B
        * [sources/CANDIDATES.md](<LLM/ReinforcementLearning/sources/CANDIDATES.md>) — 26 行 / 4,756 B
        * [sources/MANIFEST.md](<LLM/ReinforcementLearning/sources/MANIFEST.md>) — 43 行 / 9,620 B

  </details>

  <details>
  <summary><b>TrainingData</b> · <code>LLM/TrainingData/report.md</code> · 56 行 · 2026-10-23</summary>


    * **条目**：[LLM/TrainingData/report.md](<LLM/TrainingData/report.md>)（56 行 / 9,286 B）
    * **专题目录**：`LLM/TrainingData`
    * **元数据**：type=`research` · domain=`LLM` · subject=`TrainingData` · date=`2026-10-23` · status=`current`
    * **子文档（5）**
        * [papers/2107.06499-deduplicating-training-data.md](<LLM/TrainingData/papers/2107.06499-deduplicating-training-data.md>) — 24 行 / 2,755 B
        * [papers/2406.11794-datacomp-lm.md](<LLM/TrainingData/papers/2406.11794-datacomp-lm.md>) — 27 行 / 3,389 B
        * [papers/2406.17557-fineweb.md](<LLM/TrainingData/papers/2406.17557-fineweb.md>) — 24 行 / 3,203 B
        * [sources/CANDIDATES.md](<LLM/TrainingData/sources/CANDIDATES.md>) — 13 行 / 1,460 B
        * [sources/MANIFEST.md](<LLM/TrainingData/sources/MANIFEST.md>) — 17 行 / 3,402 B

  </details>

  <details>
  <summary><b>VLM</b> · <code>LLM/VLM/report.md</code> · 516 行 · —</summary>


    * **条目**：[LLM/VLM/report.md](<LLM/VLM/report.md>)（516 行 / 29,193 B）
    * **专题目录**：`LLM/VLM`
    * **元数据**：type=`—` · domain=`LLM` · subject=`VLM` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

</details>

### VisualGen（8 条目 / 9 文档）

<details>
<summary><b>视觉生成 VisualGen（8 条目 / 0 子文档）</b></summary>

  <details>
  <summary><b>3DGen</b> · <code>VisualGen/3DGen/report.md</code> · 857 行 · —</summary>


    * **条目**：[VisualGen/3DGen/report.md](<VisualGen/3DGen/report.md>)（857 行 / 45,923 B）
    * **专题目录**：`VisualGen/3DGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`3DGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>AudioGen</b> · <code>VisualGen/AudioGen/report.md</code> · 914 行 · —</summary>


    * **条目**：[VisualGen/AudioGen/report.md](<VisualGen/AudioGen/report.md>)（914 行 / 41,782 B）
    * **专题目录**：`VisualGen/AudioGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`AudioGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>AvatarGen</b> · <code>VisualGen/AvatarGen/report.md</code> · 594 行 · —</summary>


    * **条目**：[VisualGen/AvatarGen/report.md](<VisualGen/AvatarGen/report.md>)（594 行 / 28,185 B）
    * **专题目录**：`VisualGen/AvatarGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`AvatarGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>ControllableGen</b> · <code>VisualGen/ControllableGen/report.md</code> · 916 行 · —</summary>


    * **条目**：[VisualGen/ControllableGen/report.md](<VisualGen/ControllableGen/report.md>)（916 行 / 43,765 B）
    * **专题目录**：`VisualGen/ControllableGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`ControllableGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>DiT</b> · <code>VisualGen/DiT/report.md</code> · 887 行 · —</summary>


    * **条目**：[VisualGen/DiT/report.md](<VisualGen/DiT/report.md>)（887 行 / 46,258 B）
    * **专题目录**：`VisualGen/DiT`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`DiT` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>DiffusionModels</b> · <code>VisualGen/DiffusionModels/report.md</code> · 858 行 · —</summary>


    * **条目**：[VisualGen/DiffusionModels/report.md](<VisualGen/DiffusionModels/report.md>)（858 行 / 36,713 B）
    * **专题目录**：`VisualGen/DiffusionModels`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`DiffusionModels` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>ImageEditing</b> · <code>VisualGen/ImageEditing/report.md</code> · 834 行 · —</summary>


    * **条目**：[VisualGen/ImageEditing/report.md](<VisualGen/ImageEditing/report.md>)（834 行 / 43,052 B）
    * **专题目录**：`VisualGen/ImageEditing`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`ImageEditing` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>VideoGen</b> · <code>VisualGen/VideoGen/report.md</code> · 898 行 · —</summary>


    * **条目**：[VisualGen/VideoGen/report.md](<VisualGen/VideoGen/report.md>)（898 行 / 34,742 B）
    * **专题目录**：`VisualGen/VideoGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`VideoGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

</details>

### WorldModel（2 条目 / 41 文档）

<details>
<summary><b>世界模型 WorldModel（2 条目 / 38 子文档）</b></summary>

  <details>
  <summary><b>EmbodiedVLA</b> · <code>WorldModel/EmbodiedVLA/report.md</code> · 642 行 · —</summary>


    * **条目**：[WorldModel/EmbodiedVLA/report.md](<WorldModel/EmbodiedVLA/report.md>)（642 行 / 77,578 B）
    * **专题目录**：`WorldModel/EmbodiedVLA`
    * **元数据**：type=`—` · domain=`WorldModel` · subject=`EmbodiedVLA` · date=`—` · status=`—`
    * **子文档（23）**
        * [papers/2303.04137-diffusion-policy.md](<WorldModel/EmbodiedVLA/papers/2303.04137-diffusion-policy.md>) — 246 行 / 38,592 B
        * [papers/2307.15818-rt2.md](<WorldModel/EmbodiedVLA/papers/2307.15818-rt2.md>) — 222 行 / 29,179 B
        * [papers/2310.08864-open-x-embodiment.md](<WorldModel/EmbodiedVLA/papers/2310.08864-open-x-embodiment.md>) — 243 行 / 26,572 B
        * [papers/2403.12945-droid.md](<WorldModel/EmbodiedVLA/papers/2403.12945-droid.md>) — 229 行 / 22,951 B
        * [papers/2405.05941-simpler.md](<WorldModel/EmbodiedVLA/papers/2405.05941-simpler.md>) — 289 行 / 37,844 B
        * [papers/2406.09246-openvla.md](<WorldModel/EmbodiedVLA/papers/2406.09246-openvla.md>) — 252 行 / 28,967 B
        * [papers/2410.24164-pi0.md](<WorldModel/EmbodiedVLA/papers/2410.24164-pi0.md>) — 234 行 / 24,341 B
        * [papers/2501.09747-fast.md](<WorldModel/EmbodiedVLA/papers/2501.09747-fast.md>) — 246 行 / 23,992 B
        * [papers/2511.14759-pi-star-0.6-recap.md](<WorldModel/EmbodiedVLA/papers/2511.14759-pi-star-0.6-recap.md>) — 68 行 / 8,820 B
        * [papers/2601.21998-lingbot-va.md](<WorldModel/EmbodiedVLA/papers/2601.21998-lingbot-va.md>) — 68 行 / 7,620 B
        * [papers/2602.06508-world-vla-loop.md](<WorldModel/EmbodiedVLA/papers/2602.06508-world-vla-loop.md>) — 74 行 / 10,169 B
        * [papers/2602.12063-vlaw.md](<WorldModel/EmbodiedVLA/papers/2602.12063-vlaw.md>) — 69 行 / 9,444 B
        * [papers/2602.13977-wovr.md](<WorldModel/EmbodiedVLA/papers/2602.13977-wovr.md>) — 75 行 / 14,446 B
        * [papers/2608.16978-vlcp.md](<WorldModel/EmbodiedVLA/papers/2608.16978-vlcp.md>) — 69 行 / 7,029 B
        * [papers/2610.11248-simvla.md](<WorldModel/EmbodiedVLA/papers/2610.11248-simvla.md>) — 82 行 / 13,582 B
        * [papers/2610.13164-grounded-dreamer.md](<WorldModel/EmbodiedVLA/papers/2610.13164-grounded-dreamer.md>) — 45 行 / 5,945 B
        * [sources/CANDIDATES.md](<WorldModel/EmbodiedVLA/sources/CANDIDATES.md>) — 182 行 / 22,830 B
        * [sources/MANIFEST.md](<WorldModel/EmbodiedVLA/sources/MANIFEST.md>) — 108 行 / 20,111 B
        * [topics/action-representation.md](<WorldModel/EmbodiedVLA/topics/action-representation.md>) — 175 行 / 14,305 B
        * [topics/closed-loop-control.md](<WorldModel/EmbodiedVLA/topics/closed-loop-control.md>) — 105 行 / 16,293 B
        * [topics/deployment-boundaries.md](<WorldModel/EmbodiedVLA/topics/deployment-boundaries.md>) — 154 行 / 12,115 B
        * [topics/evaluation-and-datasets.md](<WorldModel/EmbodiedVLA/topics/evaluation-and-datasets.md>) — 166 行 / 15,924 B
        * [topics/world-model-to-vla-transfer.md](<WorldModel/EmbodiedVLA/topics/world-model-to-vla-transfer.md>) — 50 行 / 10,098 B

  </details>

  <details>
  <summary><b>WorldModels</b> · <code>WorldModel/WorldModels/report.md</code> · 602 行 · 2026-10-22</summary>


    * **条目**：[WorldModel/WorldModels/report.md](<WorldModel/WorldModels/report.md>)（602 行 / 61,945 B）
    * **专题目录**：`WorldModel/WorldModels`
    * **元数据**：type=`topic-research` · domain=`WorldModel` · subject=`WorldModels` · date=`2026-10-22` · status=`needs-review`
    * **子文档（15）**
        * [papers/1803.10122-world-models.md](<WorldModel/WorldModels/papers/1803.10122-world-models.md>) — 206 行 / 15,578 B
        * [papers/1811.04551-planet.md](<WorldModel/WorldModels/papers/1811.04551-planet.md>) — 204 行 / 13,762 B
        * [papers/1911.08265-muzero.md](<WorldModel/WorldModels/papers/1911.08265-muzero.md>) — 100 行 / 7,780 B
        * [papers/1912.01603-dreamer.md](<WorldModel/WorldModels/papers/1912.01603-dreamer.md>) — 208 行 / 12,686 B
        * [papers/2301.04104-dreamerv3.md](<WorldModel/WorldModels/papers/2301.04104-dreamerv3.md>) — 214 行 / 13,148 B
        * [papers/2310.06114-unisim.md](<WorldModel/WorldModels/papers/2310.06114-unisim.md>) — 206 行 / 13,348 B
        * [papers/2404.08471-vjepa.md](<WorldModel/WorldModels/papers/2404.08471-vjepa.md>) — 206 行 / 11,471 B
        * [papers/2408.14837-gamengen.md](<WorldModel/WorldModels/papers/2408.14837-gamengen.md>) — 204 行 / 11,946 B
        * [papers/2501.09038-physics-iq.md](<WorldModel/WorldModels/papers/2501.09038-physics-iq.md>) — 206 行 / 12,991 B
        * [papers/2503.21755-vbench-2.md](<WorldModel/WorldModels/papers/2503.21755-vbench-2.md>) — 206 行 / 11,671 B
        * [sources/CANDIDATES.md](<WorldModel/WorldModels/sources/CANDIDATES.md>) — 63 行 / 6,676 B
        * [sources/MANIFEST.md](<WorldModel/WorldModels/sources/MANIFEST.md>) — 24 行 / 3,920 B
        * [topics/dynamics-and-action-conditioning.md](<WorldModel/WorldModels/topics/dynamics-and-action-conditioning.md>) — 175 行 / 14,079 B
        * [topics/incomparability-checklist.md](<WorldModel/WorldModels/topics/incomparability-checklist.md>) — 174 行 / 13,264 B
        * [topics/world-model-as-env.md](<WorldModel/WorldModels/topics/world-model-as-env.md>) — 153 行 / 13,254 B

  </details>

</details>

### AI4Science（10 条目 / 53 文档）

<details>
<summary><b>科学研究 AI4Science（10 条目 / 42 子文档）</b></summary>

  <details>
  <summary><b>AntibioticDiscovery</b> · <code>AI4Science/AntibioticDiscovery/report.md</code> · 48 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/AntibioticDiscovery/report.md](<AI4Science/AntibioticDiscovery/report.md>)（48 行 / 10,713 B）
    * **专题目录**：`AI4Science/AntibioticDiscovery`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`AntibioticDiscovery` · date=`2026-10-23` · status=`completed`
    * **子文档（6）**
        * [papers/2024-synthemol-mcts.md](<AI4Science/AntibioticDiscovery/papers/2024-synthemol-mcts.md>) — 38 行 / 6,361 B
        * [papers/2025-cell-de-novo.md](<AI4Science/AntibioticDiscovery/papers/2025-cell-de-novo.md>) — 47 行 / 7,076 B
        * [papers/2026-synthemol-rl.md](<AI4Science/AntibioticDiscovery/papers/2026-synthemol-rl.md>) — 49 行 / 7,988 B
        * [papers/abaucin-screen-to-mechanism.md](<AI4Science/AntibioticDiscovery/papers/abaucin-screen-to-mechanism.md>) — 63 行 / 9,379 B
        * [sources/CANDIDATES.md](<AI4Science/AntibioticDiscovery/sources/CANDIDATES.md>) — 24 行 / 3,417 B
        * [sources/MANIFEST.md](<AI4Science/AntibioticDiscovery/sources/MANIFEST.md>) — 19 行 / 7,017 B

  </details>

  <details>
  <summary><b>Astronomy</b> · <code>AI4Science/Astronomy/report.md</code> · 59 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/Astronomy/report.md](<AI4Science/Astronomy/report.md>)（59 行 / 11,000 B）
    * **专题目录**：`AI4Science/Astronomy`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`Astronomy` · date=`2026-10-23` · status=`completed`
    * **子文档（3）**
        * [papers/2309.08660.md](<AI4Science/Astronomy/papers/2309.08660.md>) — 80 行 / 7,731 B
        * [sources/CANDIDATES.md](<AI4Science/Astronomy/sources/CANDIDATES.md>) — 24 行 / 2,555 B
        * [sources/MANIFEST.md](<AI4Science/Astronomy/sources/MANIFEST.md>) — 17 行 / 3,766 B

  </details>

  <details>
  <summary><b>AutonomousLabs</b> · <code>AI4Science/AutonomousLabs/report.md</code> · 127 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/AutonomousLabs/report.md](<AI4Science/AutonomousLabs/report.md>)（127 行 / 22,012 B）
    * **专题目录**：`AI4Science/AutonomousLabs`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`AutonomousLabs` · date=`2026-10-23` · status=`completed`
    * **子文档（2）**
        * [sources/CANDIDATES.md](<AI4Science/AutonomousLabs/sources/CANDIDATES.md>) — 21 行 / 2,110 B
        * [sources/MANIFEST.md](<AI4Science/AutonomousLabs/sources/MANIFEST.md>) — 30 行 / 9,960 B

  </details>

  <details>
  <summary><b>Chemistry</b> · <code>AI4Science/Chemistry/report.md</code> · 89 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/Chemistry/report.md](<AI4Science/Chemistry/report.md>)（89 行 / 16,487 B）
    * **专题目录**：`AI4Science/Chemistry`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`Chemistry` · date=`2026-10-23` · status=`completed`
    * **子文档（2）**
        * [sources/CANDIDATES.md](<AI4Science/Chemistry/sources/CANDIDATES.md>) — 30 行 / 4,195 B
        * [sources/MANIFEST.md](<AI4Science/Chemistry/sources/MANIFEST.md>) — 19 行 / 7,769 B

  </details>

  <details>
  <summary><b>MaterialsDiscovery</b> · <code>AI4Science/MaterialsDiscovery/report.md</code> · 66 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/MaterialsDiscovery/report.md](<AI4Science/MaterialsDiscovery/report.md>)（66 行 / 9,275 B）
    * **专题目录**：`AI4Science/MaterialsDiscovery`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`MaterialsDiscovery` · date=`2026-10-23` · status=`completed`
    * **子文档（4）**
        * [papers/2312.03687-mattergen.md](<AI4Science/MaterialsDiscovery/papers/2312.03687-mattergen.md>) — 75 行 / 11,695 B
        * [papers/2603.22748-gnome-experiment.md](<AI4Science/MaterialsDiscovery/papers/2603.22748-gnome-experiment.md>) — 45 行 / 4,637 B
        * [sources/CANDIDATES.md](<AI4Science/MaterialsDiscovery/sources/CANDIDATES.md>) — 17 行 / 2,844 B
        * [sources/MANIFEST.md](<AI4Science/MaterialsDiscovery/sources/MANIFEST.md>) — 20 行 / 7,243 B

  </details>

  <details>
  <summary><b>MathematicalDiscovery</b> · <code>AI4Science/MathematicalDiscovery/report.md</code> · 78 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/MathematicalDiscovery/report.md](<AI4Science/MathematicalDiscovery/report.md>)（78 行 / 13,711 B）
    * **专题目录**：`AI4Science/MathematicalDiscovery`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`MathematicalDiscovery` · date=`2026-10-23` · status=`completed`
    * **子文档（6）**
        * [papers/ai-feynman.md](<AI4Science/MathematicalDiscovery/papers/ai-feynman.md>) — 73 行 / 8,398 B
        * [papers/alphaproof.md](<AI4Science/MathematicalDiscovery/papers/alphaproof.md>) — 61 行 / 8,795 B
        * [papers/funsearch-reproducibility.md](<AI4Science/MathematicalDiscovery/papers/funsearch-reproducibility.md>) — 65 行 / 7,952 B
        * [papers/funsearch.md](<AI4Science/MathematicalDiscovery/papers/funsearch.md>) — 65 行 / 9,206 B
        * [sources/CANDIDATES.md](<AI4Science/MathematicalDiscovery/sources/CANDIDATES.md>) — 18 行 / 2,521 B
        * [sources/MANIFEST.md](<AI4Science/MathematicalDiscovery/sources/MANIFEST.md>) — 21 行 / 7,987 B

  </details>

  <details>
  <summary><b>Neuroscience</b> · <code>AI4Science/Neuroscience/report.md</code> · 113 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/Neuroscience/report.md](<AI4Science/Neuroscience/report.md>)（113 行 / 18,430 B）
    * **专题目录**：`AI4Science/Neuroscience`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`Neuroscience` · date=`2026-10-23` · status=`completed`
    * **子文档（2）**
        * [sources/CANDIDATES.md](<AI4Science/Neuroscience/sources/CANDIDATES.md>) — 30 行 / 4,170 B
        * [sources/MANIFEST.md](<AI4Science/Neuroscience/sources/MANIFEST.md>) — 17 行 / 6,089 B

  </details>

  <details>
  <summary><b>ProteinDesign</b> · <code>AI4Science/ProteinDesign/report.md</code> · 80 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/ProteinDesign/report.md](<AI4Science/ProteinDesign/report.md>)（80 行 / 11,452 B）
    * **专题目录**：`AI4Science/ProteinDesign`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`ProteinDesign` · date=`2026-10-23` · status=`completed`
    * **子文档（6）**
        * [papers/2026-bits-to-binders.md](<AI4Science/ProteinDesign/papers/2026-bits-to-binders.md>) — 21 行 / 3,644 B
        * [papers/2504.13075-apm.md](<AI4Science/ProteinDesign/papers/2504.13075-apm.md>) — 59 行 / 5,212 B
        * [papers/2601.13327-pepediff.md](<AI4Science/ProteinDesign/papers/2601.13327-pepediff.md>) — 53 行 / 4,657 B
        * [papers/2608.20755-shortlisting.md](<AI4Science/ProteinDesign/papers/2608.20755-shortlisting.md>) — 54 行 / 5,698 B
        * [sources/CANDIDATES.md](<AI4Science/ProteinDesign/sources/CANDIDATES.md>) — 15 行 / 2,209 B
        * [sources/MANIFEST.md](<AI4Science/ProteinDesign/sources/MANIFEST.md>) — 18 行 / 4,610 B

  </details>

  <details>
  <summary><b>SingleCellPerturbation</b> · <code>AI4Science/SingleCellPerturbation/report.md</code> · 87 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/SingleCellPerturbation/report.md](<AI4Science/SingleCellPerturbation/report.md>)（87 行 / 12,157 B）
    * **专题目录**：`AI4Science/SingleCellPerturbation`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`SingleCellPerturbation` · date=`2026-10-23` · status=`completed`
    * **子文档（4）**
        * [papers/2609.34391-p2p.md](<AI4Science/SingleCellPerturbation/papers/2609.34391-p2p.md>) — 60 行 / 6,419 B
        * [papers/2610.02232-scegflow.md](<AI4Science/SingleCellPerturbation/papers/2610.02232-scegflow.md>) — 61 行 / 6,685 B
        * [sources/CANDIDATES.md](<AI4Science/SingleCellPerturbation/sources/CANDIDATES.md>) — 29 行 / 3,609 B
        * [sources/MANIFEST.md](<AI4Science/SingleCellPerturbation/sources/MANIFEST.md>) — 17 行 / 4,569 B

  </details>

  <details>
  <summary><b>WeatherClimate</b> · <code>AI4Science/WeatherClimate/report.md</code> · 89 行 · 2026-10-23</summary>


    * **条目**：[AI4Science/WeatherClimate/report.md](<AI4Science/WeatherClimate/report.md>)（89 行 / 13,718 B）
    * **专题目录**：`AI4Science/WeatherClimate`
    * **元数据**：type=`research` · domain=`AI4Science` · subject=`WeatherClimate` · date=`2026-10-23` · status=`completed`
    * **子文档（7）**
        * [papers/aurora.md](<AI4Science/WeatherClimate/papers/aurora.md>) — 46 行 / 6,177 B
        * [papers/gencast.md](<AI4Science/WeatherClimate/papers/gencast.md>) — 47 行 / 5,727 B
        * [papers/graphcast.md](<AI4Science/WeatherClimate/papers/graphcast.md>) — 48 行 / 6,422 B
        * [papers/neuralgcm.md](<AI4Science/WeatherClimate/papers/neuralgcm.md>) — 45 行 / 5,321 B
        * [papers/pbc-subseasonal.md](<AI4Science/WeatherClimate/papers/pbc-subseasonal.md>) — 50 行 / 6,294 B
        * [sources/CANDIDATES.md](<AI4Science/WeatherClimate/sources/CANDIDATES.md>) — 43 行 / 5,243 B
        * [sources/MANIFEST.md](<AI4Science/WeatherClimate/sources/MANIFEST.md>) — 23 行 / 8,622 B

  </details>

</details>

### Evaluation（1 条目 / 7 文档）

<details>
<summary><b>评测科学 Evaluation（1 条目 / 5 子文档）</b></summary>

  <details>
  <summary><b>EvaluationScience</b> · <code>Evaluation/EvaluationScience/report.md</code> · 101 行 · 2026-10-23</summary>


    * **条目**：[Evaluation/EvaluationScience/report.md](<Evaluation/EvaluationScience/report.md>)（101 行 / 21,992 B）
    * **专题目录**：`Evaluation/EvaluationScience`
    * **元数据**：type=`research` · domain=`Evaluation` · subject=`EvaluationScience` · date=`2026-10-23` · status=`current`
    * **子文档（5）**
        * [papers/2307.13854-webarena.md](<Evaluation/EvaluationScience/papers/2307.13854-webarena.md>) — 22 行 / 2,837 B
        * [papers/2404.07972-osworld.md](<Evaluation/EvaluationScience/papers/2404.07972-osworld.md>) — 21 行 / 3,410 B
        * [papers/2406.12045-tau-bench.md](<Evaluation/EvaluationScience/papers/2406.12045-tau-bench.md>) — 27 行 / 4,034 B
        * [sources/CANDIDATES.md](<Evaluation/EvaluationScience/sources/CANDIDATES.md>) — 24 行 / 6,023 B
        * [sources/MANIFEST.md](<Evaluation/EvaluationScience/sources/MANIFEST.md>) — 30 行 / 15,802 B

  </details>

</details>

### Infra（3 条目 / 37 文档）

<details>
<summary><b>基础设施 Infra（3 条目 / 33 子文档）</b></summary>

  <details>
  <summary><b>QuantizationEdge</b> · <code>Infra/QuantizationEdge/report.md</code> · 188 行 · 2026-10-22</summary>


    * **条目**：[Infra/QuantizationEdge/report.md](<Infra/QuantizationEdge/report.md>)（188 行 / 15,490 B）
    * **专题目录**：`Infra/QuantizationEdge`
    * **元数据**：type=`topic-research` · domain=`Infra` · subject=`QuantizationEdge` · date=`2026-10-22` · status=`needs-review`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>SpeculativeDecoding</b> · <code>Infra/SpeculativeDecoding/report.md</code> · 549 行 · 2026-10-22</summary>


    * **条目**：[Infra/SpeculativeDecoding/report.md](<Infra/SpeculativeDecoding/report.md>)（549 行 / 46,589 B）
    * **专题目录**：`Infra/SpeculativeDecoding`
    * **元数据**：type=`topic-research` · domain=`Infra` · subject=`SpeculativeDecoding` · date=`2026-10-22` · status=`needs-review`
    * **子文档（33）**
        * [legacy/speculative-block-diffusion.md](<Infra/SpeculativeDecoding/legacy/speculative-block-diffusion.md>) — 230 行 / 18,588 B
        * [legacy/speculative-cascade-heterogeneous.md](<Infra/SpeculativeDecoding/legacy/speculative-cascade-heterogeneous.md>) — 141 行 / 11,829 B
        * [legacy/speculative-classical-and-self.md](<Infra/SpeculativeDecoding/legacy/speculative-classical-and-self.md>) — 157 行 / 12,113 B
        * [legacy/speculative-domain-language.md](<Infra/SpeculativeDecoding/legacy/speculative-domain-language.md>) — 182 行 / 14,598 B
        * [legacy/speculative-draft-training-2026.md](<Infra/SpeculativeDecoding/legacy/speculative-draft-training-2026.md>) — 199 行 / 15,583 B
        * [legacy/speculative-eagle-series.md](<Infra/SpeculativeDecoding/legacy/speculative-eagle-series.md>) — 113 行 / 11,905 B
        * [legacy/speculative-edge-cloud-hardware.md](<Infra/SpeculativeDecoding/legacy/speculative-edge-cloud-hardware.md>) — 182 行 / 18,130 B
        * [legacy/speculative-multimodal.md](<Infra/SpeculativeDecoding/legacy/speculative-multimodal.md>) — 152 行 / 15,666 B
        * [legacy/speculative-stochastic-verification.md](<Infra/SpeculativeDecoding/legacy/speculative-stochastic-verification.md>) — 234 行 / 28,412 B
        * [legacy/speculative-systems-and-frameworks.md](<Infra/SpeculativeDecoding/legacy/speculative-systems-and-frameworks.md>) — 206 行 / 18,397 B
        * [legacy/speculative-training-optimization.md](<Infra/SpeculativeDecoding/legacy/speculative-training-optimization.md>) — 128 行 / 14,089 B
        * [papers/2305.09781-specinfer.md](<Infra/SpeculativeDecoding/papers/2305.09781-specinfer.md>) — 201 行 / 15,667 B
        * [papers/2401.10774-medusa.md](<Infra/SpeculativeDecoding/papers/2401.10774-medusa.md>) — 204 行 / 15,815 B
        * [papers/2401.15077-eagle-series.md](<Infra/SpeculativeDecoding/papers/2401.15077-eagle-series.md>) — 244 行 / 19,850 B
        * [papers/2402.02057-lookahead.md](<Infra/SpeculativeDecoding/papers/2402.02057-lookahead.md>) — 202 行 / 15,270 B
        * [papers/2408.11049-magicdec.md](<Infra/SpeculativeDecoding/papers/2408.11049-magicdec.md>) — 200 行 / 14,379 B
        * [papers/2601.05724-hsd.md](<Infra/SpeculativeDecoding/papers/2601.05724-hsd.md>) — 84 行 / 8,788 B
        * [papers/2602.16994-delayed-tree.md](<Infra/SpeculativeDecoding/papers/2602.16994-delayed-tree.md>) — 83 行 / 9,007 B
        * [papers/2606.01813-caddtree.md](<Infra/SpeculativeDecoding/papers/2606.01813-caddtree.md>) — 53 行 / 8,309 B
        * [papers/2608.13524-dartree.md](<Infra/SpeculativeDecoding/papers/2608.13524-dartree.md>) — 31 行 / 3,850 B
        * [papers/2609.21827-rheosampling.md](<Infra/SpeculativeDecoding/papers/2609.21827-rheosampling.md>) — 216 行 / 15,804 B
        * [papers/2609.33184-specstream.md](<Infra/SpeculativeDecoding/papers/2609.33184-specstream.md>) — 44 行 / 5,416 B
        * [papers/2610.07350-tlar.md](<Infra/SpeculativeDecoding/papers/2610.07350-tlar.md>) — 54 行 / 9,515 B
        * [papers/2610.08678-secure-sd.md](<Infra/SpeculativeDecoding/papers/2610.08678-secure-sd.md>) — 55 行 / 6,108 B
        * [papers/2610.23787-dlite.md](<Infra/SpeculativeDecoding/papers/2610.23787-dlite.md>) — 48 行 / 6,161 B
        * [papers/sglang-implementation.md](<Infra/SpeculativeDecoding/papers/sglang-implementation.md>) — 220 行 / 15,358 B
        * [papers/vllm-implementation.md](<Infra/SpeculativeDecoding/papers/vllm-implementation.md>) — 227 行 / 18,077 B
        * [sources/CANDIDATES.md](<Infra/SpeculativeDecoding/sources/CANDIDATES.md>) — 91 行 / 9,644 B
        * [sources/CODE-AUDIT.md](<Infra/SpeculativeDecoding/sources/CODE-AUDIT.md>) — 87 行 / 8,110 B
        * [sources/MANIFEST.md](<Infra/SpeculativeDecoding/sources/MANIFEST.md>) — 65 行 / 9,894 B
        * [topics/algorithm-families.md](<Infra/SpeculativeDecoding/topics/algorithm-families.md>) — 164 行 / 12,014 B
        * [topics/systems-throughput-latency.md](<Infra/SpeculativeDecoding/topics/systems-throughput-latency.md>) — 168 行 / 10,532 B
        * [topics/verification-acceptance.md](<Infra/SpeculativeDecoding/topics/verification-acceptance.md>) — 159 行 / 9,197 B

  </details>

  <details>
  <summary><b>TrainingInfra</b> · <code>Infra/TrainingInfra/report.md</code> · 181 行 · 2026-10-22</summary>


    * **条目**：[Infra/TrainingInfra/report.md](<Infra/TrainingInfra/report.md>)（181 行 / 13,418 B）
    * **专题目录**：`Infra/TrainingInfra`
    * **元数据**：type=`topic-research` · domain=`Infra` · subject=`TrainingInfra` · date=`2026-10-22` · status=`needs-review`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

</details>

### OpenSource（6 条目 / 35 文档）

<details>
<summary><b>开源仓库 OpenSource（6 条目 / 26 子文档）</b></summary>

  <details>
  <summary><b>DeepInfer</b> · <code>OpenSource/DeepInfer/report.md</code> · 140 行 · 2026-10-22</summary>


    * **条目**：[OpenSource/DeepInfer/report.md](<OpenSource/DeepInfer/report.md>)（140 行 / 32,177 B）
    * **专题目录**：`OpenSource/DeepInfer`
    * **元数据**：type=`repo-research` · domain=`OpenSource` · subject=`DeepInfer` · date=`2026-10-22` · status=`completed`
    * **子文档（4）**
        * [claim-audit.md](<OpenSource/DeepInfer/claim-audit.md>) — 40 行 / 7,404 B
        * [runtime-and-lifetimes.md](<OpenSource/DeepInfer/runtime-and-lifetimes.md>) — 95 行 / 13,293 B
        * [sources/MANIFEST.md](<OpenSource/DeepInfer/sources/MANIFEST.md>) — 41 行 / 6,400 B
        * [speculation-cache-and-so.md](<OpenSource/DeepInfer/speculation-cache-and-so.md>) — 104 行 / 19,862 B

  </details>

  <details>
  <summary><b>DeepSeekHarness</b> · <code>OpenSource/DeepSeekHarness/report.md</code> · 350 行 · 2026-10-20</summary>


    * **条目**：[OpenSource/DeepSeekHarness/report.md](<OpenSource/DeepSeekHarness/report.md>)（350 行 / 26,474 B）
    * **专题目录**：`OpenSource/DeepSeekHarness`
    * **元数据**：type=`repo-research` · domain=`Repo-Research` · subject=`DeepSeekHarness` · date=`2026-10-20` · status=`completed`
    * **子文档（4）**
        * [compaction-and-bundles.md](<OpenSource/DeepSeekHarness/compaction-and-bundles.md>) — 382 行 / 45,773 B
        * [gateway-projection.md](<OpenSource/DeepSeekHarness/gateway-projection.md>) — 125 行 / 10,354 B
        * [ptc.md](<OpenSource/DeepSeekHarness/ptc.md>) — 251 行 / 35,465 B
        * [sources/MANIFEST.md](<OpenSource/DeepSeekHarness/sources/MANIFEST.md>) — 11 行 / 1,525 B

  </details>

  <details>
  <summary><b>nemotron</b> · <code>OpenSource/nemotron/report.md</code> · 220 行 · —</summary>


    * **条目**：[OpenSource/nemotron/report.md](<OpenSource/nemotron/report.md>)（220 行 / 16,175 B）
    * **专题目录**：`OpenSource/nemotron`
    * **元数据**：type=`—` · domain=`OpenSource` · subject=`nemotron` · date=`—` · status=`—`
    * **子文档（7）**
        * [knowledge-graph.md](<OpenSource/nemotron/knowledge-graph.md>) — 136 行 / 10,193 B
        * [notes/structured-reading.md](<OpenSource/nemotron/notes/structured-reading.md>) — 169 行 / 10,647 B
        * [plan.md](<OpenSource/nemotron/plan.md>) — 28 行 / 2,561 B
        * [raw-extracts/nemotron-tri-mode-fulltext.md](<OpenSource/nemotron/raw-extracts/nemotron-tri-mode-fulltext.md>) — 2430 行 / 98,525 B
        * [raw-extracts/pdf-fu_等__nemotronlabsdiffusion_a_trimode_language_model_unifying_autoregressive_dif.md](<OpenSource/nemotron/raw-extracts/pdf-fu_等__nemotronlabsdiffusion_a_trimode_language_model_unifying_autoregressive_dif.md>) — 28 行 / 1,141 B
        * [sources-index.md](<OpenSource/nemotron/sources-index.md>) — 41 行 / 2,547 B
        * [sources/MANIFEST.md](<OpenSource/nemotron/sources/MANIFEST.md>) — 15 行 / 2,335 B

  </details>

  <details>
  <summary><b>sglang</b> · <code>OpenSource/sglang/report.md</code> · 315 行 · 2026-10-16</summary>


    * **条目**：[OpenSource/sglang/report.md](<OpenSource/sglang/report.md>)（315 行 / 32,840 B）
    * **专题目录**：`OpenSource/sglang`
    * **元数据**：type=`repo-research` · domain=`Repo-Research` · subject=`sglang` · date=`2026-10-16` · status=`completed`
    * **子文档（5）**
        * [claim-audit.md](<OpenSource/sglang/claim-audit.md>) — 164 行 / 12,992 B
        * [online-request-lifecycle.md](<OpenSource/sglang/online-request-lifecycle.md>) — 29 行 / 7,686 B
        * [scheduler-and-prefix-cache.md](<OpenSource/sglang/scheduler-and-prefix-cache.md>) — 178 行 / 21,680 B
        * [sources/MANIFEST.md](<OpenSource/sglang/sources/MANIFEST.md>) — 19 行 / 2,705 B
        * [speculative-decoding-path.md](<OpenSource/sglang/speculative-decoding-path.md>) — 230 行 / 25,401 B

  </details>

  <details>
  <summary><b>this-that-model</b> · <code>OpenSource/this-that-model/report.md</code> · 246 行 · 2026-10-16</summary>


    * **条目**：[OpenSource/this-that-model/report.md](<OpenSource/this-that-model/report.md>)（246 行 / 24,458 B）
    * **专题目录**：`OpenSource/this-that-model`
    * **元数据**：type=`repo-research` · domain=`Repo-Research` · subject=`this-that-model` · date=`2026-10-16` · status=`completed`
    * **子文档（1）**
        * [sources/MANIFEST.md](<OpenSource/this-that-model/sources/MANIFEST.md>) — 14 行 / 2,135 B

  </details>

  <details>
  <summary><b>vllm</b> · <code>OpenSource/vllm/report.md</code> · 298 行 · 2026-10-16</summary>


    * **条目**：[OpenSource/vllm/report.md](<OpenSource/vllm/report.md>)（298 行 / 35,803 B）
    * **专题目录**：`OpenSource/vllm`
    * **元数据**：type=`repo-research` · domain=`Repo-Research` · subject=`vllm` · date=`2026-10-16` · status=`completed`
    * **子文档（5）**
        * [claim-audit.md](<OpenSource/vllm/claim-audit.md>) — 437 行 / 53,917 B
        * [kv-cache-and-prefix-reuse.md](<OpenSource/vllm/kv-cache-and-prefix-reuse.md>) — 203 行 / 19,007 B
        * [online-request-lifecycle.md](<OpenSource/vllm/online-request-lifecycle.md>) — 34 行 / 6,168 B
        * [scheduling-and-spec-decode.md](<OpenSource/vllm/scheduling-and-spec-decode.md>) — 246 行 / 24,286 B
        * [sources/MANIFEST.md](<OpenSource/vllm/sources/MANIFEST.md>) — 20 行 / 2,882 B

  </details>

</details>

### 游离文档（不属于任何条目目录）

以下文档位于资料库内，但没有对应的 `report.md` 条目目录，索引在此单独列出以保证可达：

| 文档 | 板块 | 行数 | 字节 |
| --- | --- | --: | --: |
| [AI4Science/README.md](<AI4Science/README.md>) | AI4Science | 137 | 6,760 B |
| [Evaluation/README.md](<Evaluation/README.md>) | Evaluation | 37 | 1,487 B |
| [Infra/README.md](<Infra/README.md>) | Infra | 67 | 5,018 B |
| [LLM/README.md](<LLM/README.md>) | LLM | 103 | 7,059 B |
| [Models/README.md](<Models/README.md>) | Models | 101 | 4,888 B |
| [OpenSource/README.md](<OpenSource/README.md>) | OpenSource | 93 | 4,069 B |
| [OpenSource/mini-swe-agent/mini-swe-agent-deep-report.md](<OpenSource/mini-swe-agent/mini-swe-agent-deep-report.md>) | OpenSource | 708 | 35,748 B |
| [OpenSource/mini-swe-agent/sources/MANIFEST.md](<OpenSource/mini-swe-agent/sources/MANIFEST.md>) | OpenSource | 14 | 2,178 B |
| [README.md](<README.md>) |  | 186 | 11,807 B |
| [VisualGen/README.md](<VisualGen/README.md>) | VisualGen | 31 | 1,616 B |
| [WorldModel/README.md](<WorldModel/README.md>) | WorldModel | 77 | 4,941 B |
| [docs/harness-feedback.md](<docs/harness-feedback.md>) | docs | 86 | 6,458 B |
| [docs/maintenance.md](<docs/maintenance.md>) | docs | 187 | 11,050 B |
| [docs/research-method.md](<docs/research-method.md>) | docs | 44 | 3,472 B |
| [docs/statistics.md](<docs/statistics.md>) | docs | 214 | 15,521 B |
| [docs/team.md](<docs/team.md>) | docs | 140 | 14,594 B |
| [docs/verification.md](<docs/verification.md>) | docs | 303 | 21,756 B |
| [scripts/README.md](<scripts/README.md>) | scripts | 101 | 4,903 B |


## 说明

* 本索引是**派生数据**，仓库里的条目文件才是唯一事实来源；重建索引只需重跑脚本。
* 当前 front-matter 为 0 份：所有条目的 `type` / `date` / `status` 显示为 `—`，domain / subject / topic 由路径推断。补齐 front-matter 后重跑即可自动填充。
* 键位契约：`title` / `type` / `domain` / `subject` / `topic` / `upstream` / `date`（另容忍可选 `topic`）。
* 脚本只读扫描、只写生成物；**不会删除或改写任何条目文件**。
