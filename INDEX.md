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
| **条目数**（`report.md`） | **48** |
| 板块（[`scripts/panels.json`](<scripts/panels.json>)） | Models 23 · LLM 8 · VisualGen 8 · WorldModel 2 · Infra 3 · OpenSource 4 |
| 条目子文档数 | 90 |
| 条目正文行数（剔除 front-matter） | 32,390 |
| 条目字节 | 2,025,167 B |
| 带 front-matter 的条目 | 5 |
| 带合法 `date` 的条目 | 5 |
| 文档（除生成物外的全部 `.md`） | 151 |
| 其中文件名 `README.md` | 8 |
| 纳入版本控制的文件 | 171 |
| 纳入版本控制的 `.md` | 159 |

> 条目 = `report.md`；`README.md`（根 / 子库 / `scripts/`）、`docs/*.md`、`notes/`、`raw-extracts/`、`plan.md`、`sources-index.md`、`knowledge-graph.md` 都是**文档而非条目**，仅在所属条目的折叠块里作为子文档出现。
> **板块**是逻辑视图（跨物理目录），映射全部在 [`scripts/panels.json`](<scripts/panels.json>)；每个条目恰好归入一个板块，未归类 / 重复归类 / 代表条目缺 `report.md` 都会让脚本在生成前非零退出。

## 按板块入口

| 资料库 | 条目数 | 文档（`.md`） | 条目行数 | 条目字节 | 入口 |
| --- | --: | --: | --: | --: | --- |
| Models | 23 | 33 | 16,005 | 1,022,054 B | [板块页 →](<Models/README.md>) |
| LLM | 8 | 25 | 5,217 | 340,995 B | [板块页 →](<LLM/README.md>) |
| VisualGen | 8 | 9 | 6,807 | 319,099 B | [板块页 →](<VisualGen/README.md>) |
| WorldModel | 2 | 31 | 1,207 | 129,154 B | [板块页 →](<WorldModel/README.md>) |
| Infra | 3 | 29 | 2,098 | 108,615 B | [板块页 →](<Infra/README.md>) |
| OpenSource | 4 | 18 | 1,056 | 105,250 B | [板块页 →](<OpenSource/README.md>) |
| **合计** | **48** | **151** | **32,390** | **2,025,167 B** | — |

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

### Models（23 条目 / 33 文档）

<details>
<summary><b>模型系列 Models（23 条目 / 9 子文档）</b></summary>

  <details>
  <summary><b>Alibaba-Gen</b> · <code>Models/Alibaba-Gen/report.md</code> · 803 行 · —</summary>
  

    * **条目**：[Models/Alibaba-Gen/report.md](<Models/Alibaba-Gen/report.md>)（803 行 / 36,092 B）
    * **专题目录**：`Models/Alibaba-Gen`
    * **元数据**：type=`—` · domain=`Models` · subject=`Alibaba-Gen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>ByteDance-Gen</b> · <code>Models/ByteDance-Gen/report.md</code> · 711 行 · —</summary>
  

    * **条目**：[Models/ByteDance-Gen/report.md](<Models/ByteDance-Gen/report.md>)（711 行 / 41,175 B）
    * **专题目录**：`Models/ByteDance-Gen`
    * **元数据**：type=`—` · domain=`Models` · subject=`ByteDance-Gen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Claude</b> · <code>Models/Claude/report.md</code> · 611 行 · —</summary>
  

    * **条目**：[Models/Claude/report.md](<Models/Claude/report.md>)（611 行 / 47,565 B）
    * **专题目录**：`Models/Claude`
    * **元数据**：type=`—` · domain=`Models` · subject=`Claude` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>DeepSeek</b> · <code>Models/DeepSeek/report.md</code> · 751 行 · —</summary>
  

    * **条目**：[Models/DeepSeek/report.md](<Models/DeepSeek/report.md>)（751 行 / 58,512 B）
    * **专题目录**：`Models/DeepSeek`
    * **元数据**：type=`—` · domain=`Models` · subject=`DeepSeek` · date=`—` · status=`—`
    * **子文档（2）**
        * [deepseek-multimodal-and-specialized.md](<Models/DeepSeek/deepseek-multimodal-and-specialized.md>) — 367 行 / 24,706 B
        * [deepseek-text-models.md](<Models/DeepSeek/deepseek-text-models.md>) — 407 行 / 33,119 B

  </details>

  <details>
  <summary><b>Doubao-Seed</b> · <code>Models/Doubao-Seed/report.md</code> · 643 行 · —</summary>
  

    * **条目**：[Models/Doubao-Seed/report.md](<Models/Doubao-Seed/report.md>)（643 行 / 27,470 B）
    * **专题目录**：`Models/Doubao-Seed`
    * **元数据**：type=`—` · domain=`Models` · subject=`Doubao-Seed` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>GLM</b> · <code>Models/GLM/report.md</code> · 737 行 · —</summary>
  

    * **条目**：[Models/GLM/report.md](<Models/GLM/report.md>)（737 行 / 68,363 B）
    * **专题目录**：`Models/GLM`
    * **元数据**：type=`—` · domain=`Models` · subject=`GLM` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>GPT</b> · <code>Models/GPT/report.md</code> · 759 行 · —</summary>
  

    * **条目**：[Models/GPT/report.md](<Models/GPT/report.md>)（759 行 / 57,281 B）
    * **专题目录**：`Models/GPT`
    * **元数据**：type=`—` · domain=`Models` · subject=`GPT` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Gemini</b> · <code>Models/Gemini/report.md</code> · 1094 行 · —</summary>
  

    * **条目**：[Models/Gemini/report.md](<Models/Gemini/report.md>)（1094 行 / 57,347 B）
    * **专题目录**：`Models/Gemini`
    * **元数据**：type=`—` · domain=`Models` · subject=`Gemini` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Google-Gen</b> · <code>Models/Google-Gen/report.md</code> · 878 行 · —</summary>
  

    * **条目**：[Models/Google-Gen/report.md](<Models/Google-Gen/report.md>)（878 行 / 40,233 B）
    * **专题目录**：`Models/Google-Gen`
    * **元数据**：type=`—` · domain=`Models` · subject=`Google-Gen` · date=`—` · status=`—`
    * **子文档（1）**
        * [papers/2604.20329-vision-banana.md](<Models/Google-Gen/papers/2604.20329-vision-banana.md>) — 423 行 / 54,321 B

  </details>

  <details>
  <summary><b>Grok</b> · <code>Models/Grok/report.md</code> · 469 行 · —</summary>
  

    * **条目**：[Models/Grok/report.md](<Models/Grok/report.md>)（469 行 / 32,693 B）
    * **专题目录**：`Models/Grok`
    * **元数据**：type=`—` · domain=`Models` · subject=`Grok` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Hunyuan</b> · <code>Models/Hunyuan/report.md</code> · 525 行 · —</summary>
  

    * **条目**：[Models/Hunyuan/report.md](<Models/Hunyuan/report.md>)（525 行 / 36,518 B）
    * **专题目录**：`Models/Hunyuan`
    * **元数据**：type=`—` · domain=`Models` · subject=`Hunyuan` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Kimi</b> · <code>Models/Kimi/report.md</code> · 616 行 · —</summary>
  

    * **条目**：[Models/Kimi/report.md](<Models/Kimi/report.md>)（616 行 / 55,129 B）
    * **专题目录**：`Models/Kimi`
    * **元数据**：type=`—` · domain=`Models` · subject=`Kimi` · date=`—` · status=`—`
    * **子文档（2）**
        * [papers/2607.24653-kimi-k3.md](<Models/Kimi/papers/2607.24653-kimi-k3.md>) — 251 行 / 30,000 B
        * [sources/MANIFEST.md](<Models/Kimi/sources/MANIFEST.md>) — 47 行 / 3,924 B

  </details>

  <details>
  <summary><b>Kling</b> · <code>Models/Kling/report.md</code> · 537 行 · —</summary>
  

    * **条目**：[Models/Kling/report.md](<Models/Kling/report.md>)（537 行 / 28,134 B）
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
  <summary><b>MiMo</b> · <code>Models/MiMo/report.md</code> · 749 行 · —</summary>
  

    * **条目**：[Models/MiMo/report.md](<Models/MiMo/report.md>)（749 行 / 63,156 B）
    * **专题目录**：`Models/MiMo`
    * **元数据**：type=`—` · domain=`Models` · subject=`MiMo` · date=`—` · status=`—`
    * **子文档（1）**
        * [papers/2610.11959-mimo-v2-6.md](<Models/MiMo/papers/2610.11959-mimo-v2-6.md>) — 437 行 / 36,488 B

  </details>

  <details>
  <summary><b>Midjourney</b> · <code>Models/Midjourney/report.md</code> · 587 行 · —</summary>
  

    * **条目**：[Models/Midjourney/report.md](<Models/Midjourney/report.md>)（587 行 / 35,037 B）
    * **专题目录**：`Models/Midjourney`
    * **元数据**：type=`—` · domain=`Models` · subject=`Midjourney` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>MiniMax</b> · <code>Models/MiniMax/report.md</code> · 517 行 · —</summary>
  

    * **条目**：[Models/MiniMax/report.md](<Models/MiniMax/report.md>)（517 行 / 41,294 B）
    * **专题目录**：`Models/MiniMax`
    * **元数据**：type=`—` · domain=`Models` · subject=`MiniMax` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Mistral</b> · <code>Models/Mistral/report.md</code> · 495 行 · —</summary>
  

    * **条目**：[Models/Mistral/report.md](<Models/Mistral/report.md>)（495 行 / 29,315 B）
    * **专题目录**：`Models/Mistral`
    * **元数据**：type=`—` · domain=`Models` · subject=`Mistral` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Nemotron</b> · <code>Models/Nemotron/report.md</code> · 465 行 · —</summary>
  

    * **条目**：[Models/Nemotron/report.md](<Models/Nemotron/report.md>)（465 行 / 32,720 B）
    * **专题目录**：`Models/Nemotron`
    * **元数据**：type=`—` · domain=`Models` · subject=`Nemotron` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>OpenAI-Gen</b> · <code>Models/OpenAI-Gen/report.md</code> · 859 行 · —</summary>
  

    * **条目**：[Models/OpenAI-Gen/report.md](<Models/OpenAI-Gen/report.md>)（859 行 / 36,915 B）
    * **专题目录**：`Models/OpenAI-Gen`
    * **元数据**：type=`—` · domain=`Models` · subject=`OpenAI-Gen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Qwen</b> · <code>Models/Qwen/report.md</code> · 1111 行 · —</summary>
  

    * **条目**：[Models/Qwen/report.md](<Models/Qwen/report.md>)（1111 行 / 72,586 B）
    * **专题目录**：`Models/Qwen`
    * **元数据**：type=`—` · domain=`Models` · subject=`Qwen` · date=`—` · status=`—`
    * **子文档（3）**
        * [qwen-omni-and-ecosystem.md](<Models/Qwen/qwen-omni-and-ecosystem.md>) — 563 行 / 22,446 B
        * [qwen-text-models.md](<Models/Qwen/qwen-text-models.md>) — 489 行 / 20,718 B
        * [qwen-vl-models.md](<Models/Qwen/qwen-vl-models.md>) — 543 行 / 21,664 B

  </details>

  <details>
  <summary><b>Runway</b> · <code>Models/Runway/report.md</code> · 732 行 · —</summary>
  

    * **条目**：[Models/Runway/report.md](<Models/Runway/report.md>)（732 行 / 33,709 B）
    * **专题目录**：`Models/Runway`
    * **元数据**：type=`—` · domain=`Models` · subject=`Runway` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>StabilityAI</b> · <code>Models/StabilityAI/report.md</code> · 873 行 · —</summary>
  

    * **条目**：[Models/StabilityAI/report.md](<Models/StabilityAI/report.md>)（873 行 / 48,275 B）
    * **专题目录**：`Models/StabilityAI`
    * **元数据**：type=`—` · domain=`Models` · subject=`StabilityAI` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

</details>

### LLM（8 条目 / 25 文档）

<details>
<summary><b>语言模型 LLM（8 条目 / 16 子文档）</b></summary>

  <details>
  <summary><b>Agent</b> · <code>LLM/Agent/report.md</code> · 698 行 · —</summary>
  

    * **条目**：[LLM/Agent/report.md](<LLM/Agent/report.md>)（698 行 / 31,433 B）
    * **专题目录**：`LLM/Agent`
    * **元数据**：type=`—` · domain=`LLM` · subject=`Agent` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>Alignment</b> · <code>LLM/Alignment/report.md</code> · 588 行 · —</summary>
  

    * **条目**：[LLM/Alignment/report.md](<LLM/Alignment/report.md>)（588 行 / 35,714 B）
    * **专题目录**：`LLM/Alignment`
    * **元数据**：type=`—` · domain=`LLM` · subject=`Alignment` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>DecisionModels</b> · <code>LLM/DecisionModels/report.md</code> · 869 行 · —</summary>
  

    * **条目**：[LLM/DecisionModels/report.md](<LLM/DecisionModels/report.md>)（869 行 / 107,578 B）
    * **专题目录**：`LLM/DecisionModels`
    * **元数据**：type=`—` · domain=`LLM` · subject=`DecisionModels` · date=`—` · status=`—`
    * **子文档（16）**
        * [calibration.md](<LLM/DecisionModels/calibration.md>) — 261 行 / 28,387 B
        * [experiments.md](<LLM/DecisionModels/experiments.md>) — 349 行 / 25,166 B
        * [open-implementations.md](<LLM/DecisionModels/open-implementations.md>) — 412 行 / 32,731 B
        * [papers/2609.23886-this-that-model.md](<LLM/DecisionModels/papers/2609.23886-this-that-model.md>) — 102 行 / 9,013 B
        * [papers/2609.23986-jev-mem.md](<LLM/DecisionModels/papers/2609.23986-jev-mem.md>) — 88 行 / 7,976 B
        * [papers/2609.24052-crash-narrative-calibration.md](<LLM/DecisionModels/papers/2609.24052-crash-narrative-calibration.md>) — 98 行 / 12,094 B
        * [papers/2609.24574-css-text-annotation.md](<LLM/DecisionModels/papers/2609.24574-css-text-annotation.md>) — 180 行 / 40,168 B
        * [papers/2609.25845-visual-jev.md](<LLM/DecisionModels/papers/2609.25845-visual-jev.md>) — 90 行 / 9,091 B
        * [papers/2609.26532-reflex-selective-control.md](<LLM/DecisionModels/papers/2609.26532-reflex-selective-control.md>) — 95 行 / 10,729 B
        * [papers/2609.26550-jev-as-a-judge.md](<LLM/DecisionModels/papers/2609.26550-jev-as-a-judge.md>) — 245 行 / 36,150 B
        * [papers/2609.26758-option-name-vs-definition.md](<LLM/DecisionModels/papers/2609.26758-option-name-vs-definition.md>) — 334 行 / 50,076 B
        * [papers/2609.28613-decision-hijacking.md](<LLM/DecisionModels/papers/2609.28613-decision-hijacking.md>) — 97 行 / 9,916 B
        * [papers/2609.30243-jevout-natural-context-flip.md](<LLM/DecisionModels/papers/2609.30243-jevout-natural-context-flip.md>) — 310 行 / 33,313 B
        * [papers/2609.33209-probability-axioms-coherence.md](<LLM/DecisionModels/papers/2609.33209-probability-axioms-coherence.md>) — 92 行 / 10,312 B
        * [papers/2610.09683-system-switch.md](<LLM/DecisionModels/papers/2610.09683-system-switch.md>) — 90 行 / 10,672 B
        * [taxonomy.md](<LLM/DecisionModels/taxonomy.md>) — 254 行 / 24,924 B

  </details>

  <details>
  <summary><b>LongContext</b> · <code>LLM/LongContext/report.md</code> · 608 行 · —</summary>
  

    * **条目**：[LLM/LongContext/report.md](<LLM/LongContext/report.md>)（608 行 / 30,373 B）
    * **专题目录**：`LLM/LongContext`
    * **元数据**：type=`—` · domain=`LLM` · subject=`LongContext` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>MoE</b> · <code>LLM/MoE/report.md</code> · 405 行 · —</summary>
  

    * **条目**：[LLM/MoE/report.md](<LLM/MoE/report.md>)（405 行 / 27,806 B）
    * **专题目录**：`LLM/MoE`
    * **元数据**：type=`—` · domain=`LLM` · subject=`MoE` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>RAG</b> · <code>LLM/RAG/report.md</code> · 851 行 · —</summary>
  

    * **条目**：[LLM/RAG/report.md](<LLM/RAG/report.md>)（851 行 / 44,423 B）
    * **专题目录**：`LLM/RAG`
    * **元数据**：type=`—` · domain=`LLM` · subject=`RAG` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>ReasoningModels</b> · <code>LLM/ReasoningModels/report.md</code> · 681 行 · —</summary>
  

    * **条目**：[LLM/ReasoningModels/report.md](<LLM/ReasoningModels/report.md>)（681 行 / 34,752 B）
    * **专题目录**：`LLM/ReasoningModels`
    * **元数据**：type=`—` · domain=`LLM` · subject=`ReasoningModels` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>VLM</b> · <code>LLM/VLM/report.md</code> · 517 行 · —</summary>
  

    * **条目**：[LLM/VLM/report.md](<LLM/VLM/report.md>)（517 行 / 28,916 B）
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
  <summary><b>3DGen</b> · <code>VisualGen/3DGen/report.md</code> · 899 行 · —</summary>
  

    * **条目**：[VisualGen/3DGen/report.md](<VisualGen/3DGen/report.md>)（899 行 / 47,178 B）
    * **专题目录**：`VisualGen/3DGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`3DGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>AudioGen</b> · <code>VisualGen/AudioGen/report.md</code> · 913 行 · —</summary>
  

    * **条目**：[VisualGen/AudioGen/report.md](<VisualGen/AudioGen/report.md>)（913 行 / 41,462 B）
    * **专题目录**：`VisualGen/AudioGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`AudioGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>AvatarGen</b> · <code>VisualGen/AvatarGen/report.md</code> · 592 行 · —</summary>
  

    * **条目**：[VisualGen/AvatarGen/report.md](<VisualGen/AvatarGen/report.md>)（592 行 / 27,386 B）
    * **专题目录**：`VisualGen/AvatarGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`AvatarGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>ControllableGen</b> · <code>VisualGen/ControllableGen/report.md</code> · 923 行 · —</summary>
  

    * **条目**：[VisualGen/ControllableGen/report.md](<VisualGen/ControllableGen/report.md>)（923 行 / 43,040 B）
    * **专题目录**：`VisualGen/ControllableGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`ControllableGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>DiT</b> · <code>VisualGen/DiT/report.md</code> · 893 行 · —</summary>
  

    * **条目**：[VisualGen/DiT/report.md](<VisualGen/DiT/report.md>)（893 行 / 46,314 B）
    * **专题目录**：`VisualGen/DiT`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`DiT` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>DiffusionModels</b> · <code>VisualGen/DiffusionModels/report.md</code> · 855 行 · —</summary>
  

    * **条目**：[VisualGen/DiffusionModels/report.md](<VisualGen/DiffusionModels/report.md>)（855 行 / 36,106 B）
    * **专题目录**：`VisualGen/DiffusionModels`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`DiffusionModels` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>ImageEditing</b> · <code>VisualGen/ImageEditing/report.md</code> · 834 行 · —</summary>
  

    * **条目**：[VisualGen/ImageEditing/report.md](<VisualGen/ImageEditing/report.md>)（834 行 / 42,897 B）
    * **专题目录**：`VisualGen/ImageEditing`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`ImageEditing` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>VideoGen</b> · <code>VisualGen/VideoGen/report.md</code> · 898 行 · —</summary>
  

    * **条目**：[VisualGen/VideoGen/report.md](<VisualGen/VideoGen/report.md>)（898 行 / 34,716 B）
    * **专题目录**：`VisualGen/VideoGen`
    * **元数据**：type=`—` · domain=`VisualGen` · subject=`VideoGen` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

</details>

### WorldModel（2 条目 / 31 文档）

<details>
<summary><b>世界模型 WorldModel（2 条目 / 28 子文档）</b></summary>

  <details>
  <summary><b>EmbodiedVLA</b> · <code>WorldModel/EmbodiedVLA/report.md</code> · 609 行 · —</summary>
  

    * **条目**：[WorldModel/EmbodiedVLA/report.md](<WorldModel/EmbodiedVLA/report.md>)（609 行 / 68,857 B）
    * **专题目录**：`WorldModel/EmbodiedVLA`
    * **元数据**：type=`—` · domain=`WorldModel` · subject=`EmbodiedVLA` · date=`—` · status=`—`
    * **子文档（13）**
        * [papers/2303.04137-diffusion-policy.md](<WorldModel/EmbodiedVLA/papers/2303.04137-diffusion-policy.md>) — 246 行 / 38,524 B
        * [papers/2307.15818-rt2.md](<WorldModel/EmbodiedVLA/papers/2307.15818-rt2.md>) — 222 行 / 29,179 B
        * [papers/2310.08864-open-x-embodiment.md](<WorldModel/EmbodiedVLA/papers/2310.08864-open-x-embodiment.md>) — 241 行 / 26,488 B
        * [papers/2403.12945-droid.md](<WorldModel/EmbodiedVLA/papers/2403.12945-droid.md>) — 227 行 / 22,519 B
        * [papers/2405.05941-simpler.md](<WorldModel/EmbodiedVLA/papers/2405.05941-simpler.md>) — 289 行 / 37,844 B
        * [papers/2406.09246-openvla.md](<WorldModel/EmbodiedVLA/papers/2406.09246-openvla.md>) — 250 行 / 28,667 B
        * [papers/2410.24164-pi0.md](<WorldModel/EmbodiedVLA/papers/2410.24164-pi0.md>) — 239 行 / 24,171 B
        * [papers/2501.09747-fast.md](<WorldModel/EmbodiedVLA/papers/2501.09747-fast.md>) — 250 行 / 23,574 B
        * [sources/CANDIDATES.md](<WorldModel/EmbodiedVLA/sources/CANDIDATES.md>) — 100 行 / 11,008 B
        * [sources/MANIFEST.md](<WorldModel/EmbodiedVLA/sources/MANIFEST.md>) — 47 行 / 6,276 B
        * [topics/action-representation.md](<WorldModel/EmbodiedVLA/topics/action-representation.md>) — 175 行 / 14,193 B
        * [topics/deployment-boundaries.md](<WorldModel/EmbodiedVLA/topics/deployment-boundaries.md>) — 154 行 / 11,387 B
        * [topics/evaluation-and-datasets.md](<WorldModel/EmbodiedVLA/topics/evaluation-and-datasets.md>) — 166 行 / 15,824 B

  </details>

  <details>
  <summary><b>WorldModels</b> · <code>WorldModel/WorldModels/report.md</code> · 598 行 · 2026-10-17</summary>
  

    * **条目**：[WorldModel/WorldModels/report.md](<WorldModel/WorldModels/report.md>)（598 行 / 60,297 B）
    * **专题目录**：`WorldModel/WorldModels`
    * **元数据**：type=`topic-research` · domain=`WorldModel` · subject=`WorldModels` · date=`2026-10-17` · status=`completed`
    * **子文档（15）**
        * [papers/1803.10122-world-models.md](<WorldModel/WorldModels/papers/1803.10122-world-models.md>) — 204 行 / 14,821 B
        * [papers/1811.04551-planet.md](<WorldModel/WorldModels/papers/1811.04551-planet.md>) — 204 行 / 13,762 B
        * [papers/1911.08265-muzero.md](<WorldModel/WorldModels/papers/1911.08265-muzero.md>) — 205 行 / 13,351 B
        * [papers/1912.01603-dreamer.md](<WorldModel/WorldModels/papers/1912.01603-dreamer.md>) — 208 行 / 12,686 B
        * [papers/2301.04104-dreamerv3.md](<WorldModel/WorldModels/papers/2301.04104-dreamerv3.md>) — 212 行 / 12,864 B
        * [papers/2310.06114-unisim.md](<WorldModel/WorldModels/papers/2310.06114-unisim.md>) — 206 行 / 13,348 B
        * [papers/2404.08471-vjepa.md](<WorldModel/WorldModels/papers/2404.08471-vjepa.md>) — 206 行 / 11,471 B
        * [papers/2408.14837-gamengen.md](<WorldModel/WorldModels/papers/2408.14837-gamengen.md>) — 204 行 / 11,946 B
        * [papers/2501.09038-physics-iq.md](<WorldModel/WorldModels/papers/2501.09038-physics-iq.md>) — 206 行 / 12,991 B
        * [papers/2503.21755-vbench-2.md](<WorldModel/WorldModels/papers/2503.21755-vbench-2.md>) — 206 行 / 11,671 B
        * [sources/CANDIDATES.md](<WorldModel/WorldModels/sources/CANDIDATES.md>) — 63 行 / 6,676 B
        * [sources/MANIFEST.md](<WorldModel/WorldModels/sources/MANIFEST.md>) — 24 行 / 3,898 B
        * [topics/dynamics-and-action-conditioning.md](<WorldModel/WorldModels/topics/dynamics-and-action-conditioning.md>) — 175 行 / 13,882 B
        * [topics/incomparability-checklist.md](<WorldModel/WorldModels/topics/incomparability-checklist.md>) — 174 行 / 13,137 B
        * [topics/world-model-as-env.md](<WorldModel/WorldModels/topics/world-model-as-env.md>) — 152 行 / 12,825 B

  </details>

</details>

### Infra（3 条目 / 29 文档）

<details>
<summary><b>基础设施 Infra（3 条目 / 25 子文档）</b></summary>

  <details>
  <summary><b>QuantizationEdge</b> · <code>Infra/QuantizationEdge/report.md</code> · 777 行 · —</summary>
  

    * **条目**：[Infra/QuantizationEdge/report.md](<Infra/QuantizationEdge/report.md>)（777 行 / 34,205 B）
    * **专题目录**：`Infra/QuantizationEdge`
    * **元数据**：type=`—` · domain=`Infra` · subject=`QuantizationEdge` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>SpeculativeDecoding</b> · <code>Infra/SpeculativeDecoding/report.md</code> · 601 行 · 2026-10-17</summary>
  

    * **条目**：[Infra/SpeculativeDecoding/report.md](<Infra/SpeculativeDecoding/report.md>)（601 行 / 42,561 B）
    * **专题目录**：`Infra/SpeculativeDecoding`
    * **元数据**：type=`topic-research` · domain=`Infra` · subject=`SpeculativeDecoding` · date=`2026-10-17` · status=`completed`
    * **子文档（25）**
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
        * [papers/2401.15077-eagle-series.md](<Infra/SpeculativeDecoding/papers/2401.15077-eagle-series.md>) — 244 行 / 19,834 B
        * [papers/2402.02057-lookahead.md](<Infra/SpeculativeDecoding/papers/2402.02057-lookahead.md>) — 202 行 / 15,419 B
        * [papers/2408.11049-magicdec.md](<Infra/SpeculativeDecoding/papers/2408.11049-magicdec.md>) — 200 行 / 14,379 B
        * [papers/2609.21827-rheosampling.md](<Infra/SpeculativeDecoding/papers/2609.21827-rheosampling.md>) — 216 行 / 15,804 B
        * [papers/sglang-implementation.md](<Infra/SpeculativeDecoding/papers/sglang-implementation.md>) — 220 行 / 15,358 B
        * [papers/vllm-implementation.md](<Infra/SpeculativeDecoding/papers/vllm-implementation.md>) — 220 行 / 16,656 B
        * [sources/CANDIDATES.md](<Infra/SpeculativeDecoding/sources/CANDIDATES.md>) — 82 行 / 7,644 B
        * [sources/CODE-AUDIT.md](<Infra/SpeculativeDecoding/sources/CODE-AUDIT.md>) — 87 行 / 8,110 B
        * [sources/MANIFEST.md](<Infra/SpeculativeDecoding/sources/MANIFEST.md>) — 40 行 / 5,225 B
        * [topics/algorithm-families.md](<Infra/SpeculativeDecoding/topics/algorithm-families.md>) — 164 行 / 11,910 B
        * [topics/systems-throughput-latency.md](<Infra/SpeculativeDecoding/topics/systems-throughput-latency.md>) — 168 行 / 10,532 B
        * [topics/verification-acceptance.md](<Infra/SpeculativeDecoding/topics/verification-acceptance.md>) — 216 行 / 12,395 B

  </details>

  <details>
  <summary><b>TrainingInfra</b> · <code>Infra/TrainingInfra/report.md</code> · 720 行 · —</summary>
  

    * **条目**：[Infra/TrainingInfra/report.md](<Infra/TrainingInfra/report.md>)（720 行 / 31,849 B）
    * **专题目录**：`Infra/TrainingInfra`
    * **元数据**：type=`—` · domain=`Infra` · subject=`TrainingInfra` · date=`—` · status=`—`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

</details>

### OpenSource（4 条目 / 18 文档）

<details>
<summary><b>开源仓库 OpenSource（4 条目 / 12 子文档）</b></summary>

  <details>
  <summary><b>nemotron</b> · <code>OpenSource/nemotron/report.md</code> · 206 行 · —</summary>
  

    * **条目**：[OpenSource/nemotron/report.md](<OpenSource/nemotron/report.md>)（206 行 / 13,183 B）
    * **专题目录**：`OpenSource/nemotron`
    * **元数据**：type=`—` · domain=`OpenSource` · subject=`nemotron` · date=`—` · status=`—`
    * **子文档（6）**
        * [knowledge-graph.md](<OpenSource/nemotron/knowledge-graph.md>) — 136 行 / 10,088 B
        * [notes/structured-reading.md](<OpenSource/nemotron/notes/structured-reading.md>) — 169 行 / 10,416 B
        * [plan.md](<OpenSource/nemotron/plan.md>) — 28 行 / 2,561 B
        * [raw-extracts/nemotron-tri-mode-fulltext.md](<OpenSource/nemotron/raw-extracts/nemotron-tri-mode-fulltext.md>) — 2430 行 / 98,525 B
        * [raw-extracts/pdf-fu_等__nemotronlabsdiffusion_a_trimode_language_model_unifying_autoregressive_dif.md](<OpenSource/nemotron/raw-extracts/pdf-fu_等__nemotronlabsdiffusion_a_trimode_language_model_unifying_autoregressive_dif.md>) — 28 行 / 1,141 B
        * [sources-index.md](<OpenSource/nemotron/sources-index.md>) — 41 行 / 2,363 B

  </details>

  <details>
  <summary><b>sglang</b> · <code>OpenSource/sglang/report.md</code> · 310 行 · 2026-10-16</summary>
  

    * **条目**：[OpenSource/sglang/report.md](<OpenSource/sglang/report.md>)（310 行 / 32,226 B）
    * **专题目录**：`OpenSource/sglang`
    * **元数据**：type=`repo-research` · domain=`Repo-Research` · subject=`sglang` · date=`2026-10-16` · status=`completed`
    * **子文档（3）**
        * [claim-audit.md](<OpenSource/sglang/claim-audit.md>) — 149 行 / 11,627 B
        * [scheduler-and-prefix-cache.md](<OpenSource/sglang/scheduler-and-prefix-cache.md>) — 174 行 / 20,863 B
        * [speculative-decoding-path.md](<OpenSource/sglang/speculative-decoding-path.md>) — 230 行 / 25,244 B

  </details>

  <details>
  <summary><b>this-that-model</b> · <code>OpenSource/this-that-model/report.md</code> · 246 行 · 2026-10-16</summary>
  

    * **条目**：[OpenSource/this-that-model/report.md](<OpenSource/this-that-model/report.md>)（246 行 / 24,264 B）
    * **专题目录**：`OpenSource/this-that-model`
    * **元数据**：type=`repo-research` · domain=`Repo-Research` · subject=`this-that-model` · date=`2026-10-16` · status=`completed`
    * **子文档（0）**
        * _该条目暂无子文档_

  </details>

  <details>
  <summary><b>vllm</b> · <code>OpenSource/vllm/report.md</code> · 294 行 · 2026-10-16</summary>
  

    * **条目**：[OpenSource/vllm/report.md](<OpenSource/vllm/report.md>)（294 行 / 35,577 B）
    * **专题目录**：`OpenSource/vllm`
    * **元数据**：type=`repo-research` · domain=`Repo-Research` · subject=`vllm` · date=`2026-10-16` · status=`completed`
    * **子文档（3）**
        * [claim-audit.md](<OpenSource/vllm/claim-audit.md>) — 422 行 / 52,479 B
        * [kv-cache-and-prefix-reuse.md](<OpenSource/vllm/kv-cache-and-prefix-reuse.md>) — 206 行 / 19,051 B
        * [scheduling-and-spec-decode.md](<OpenSource/vllm/scheduling-and-spec-decode.md>) — 244 行 / 24,087 B

  </details>

</details>

### 游离文档（不属于任何条目目录）

以下文档位于资料库内，但没有对应的 `report.md` 条目目录，索引在此单独列出以保证可达：

| 文档 | 板块 | 行数 | 字节 |
| --- | --- | --: | --: |
| [Infra/README.md](<Infra/README.md>) | Infra | 59 | 4,167 B |
| [LLM/README.md](<LLM/README.md>) | LLM | 55 | 3,584 B |
| [Models/README.md](<Models/README.md>) | Models | 87 | 4,166 B |
| [OpenSource/README.md](<OpenSource/README.md>) | OpenSource | 59 | 2,471 B |
| [OpenSource/mini-swe-agent/mini-swe-agent-deep-report.md](<OpenSource/mini-swe-agent/mini-swe-agent-deep-report.md>) | OpenSource | 735 | 34,490 B |
| [README.md](<README.md>) |  | 105 | 7,822 B |
| [VisualGen/README.md](<VisualGen/README.md>) | VisualGen | 31 | 1,616 B |
| [WorldModel/README.md](<WorldModel/README.md>) | WorldModel | 67 | 3,896 B |
| [docs/maintenance.md](<docs/maintenance.md>) | docs | 187 | 10,798 B |
| [docs/statistics.md](<docs/statistics.md>) | docs | 212 | 16,435 B |
| [docs/team.md](<docs/team.md>) | docs | 106 | 10,731 B |
| [docs/verification.md](<docs/verification.md>) | docs | 243 | 16,496 B |
| [scripts/README.md](<scripts/README.md>) | scripts | 99 | 4,589 B |


## 说明

* 本索引是**派生数据**，仓库里的条目文件才是唯一事实来源；重建索引只需重跑脚本。
* 当前 front-matter 为 0 份：所有条目的 `type` / `date` / `status` 显示为 `—`，domain / subject / topic 由路径推断。补齐 front-matter 后重跑即可自动填充。
* 键位契约：`title` / `type` / `domain` / `subject` / `topic` / `upstream` / `date`（另容忍可选 `topic`）。
* 脚本只读扫描、只写生成物；**不会删除或改写任何条目文件**。
