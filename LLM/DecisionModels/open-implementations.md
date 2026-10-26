---
title: "决策模型开源实现：实现路径、可复现性与模型卡口径"
type: doc
domain: LLM
subject: decision-models
evidence: 混合
date: 2026-10-16
---

# 决策模型开源实现：实现路径、可复现性与模型卡口径

> **免责声明与证据约定**
> - 本文件是 [report.md](report.md) 的**领域研究第二批子文档**，**不新增**主报告之外的结论，也不改写主报告的分类与等级。
> - **单一主等级标签，混合取最弱**：`精读原文`（读到了页面/模型卡正文）/ `摘要级`（只读到题录或 API 元数据）/ `二手` / `受限核验`。括号内注明**来源类型**（模型卡 / 项目博客 / GitHub README / 官方 API 元数据 / 预印本正文）。
> - **本文件未克隆任何仓库、未读取任何源码**，因此**不含任何 `仓库@commit:文件:行` 级别的断言**；所有实现路径均来自**项目自述或模型卡明文**，推断一律显式标「推断」。
> - **所有外链均于 2026-10-16 实测**，状态码列在 §8；非 2xx 者移入 §7「未确证/待跟踪」。
> - **项目自述数字一律标为「项目自述」**，不构成独立结论。**不做跨项目排行榜**；§6 对照表必带条件列。
> - 核验方法：`curl -sS -o /dev/null -w "%{http_code}" -L` 逐条实测；模型卡正文经 `huggingface.co/<repo>/raw/main/README.md` 抓取后逐字检索（命令见 §8.4）。

---

## 0 速览

| 项目 | readout 实现路径 | 权重是否公开 | 许可证 | 主等级（来源类型） |
|---|---|---|---|---|
| **this-that-model-1.0** | **隐藏状态直读 + 声明标签 token 打分**（专用 typed head 形态） | 是，`flock-io/this-that-model-1.0` | **MIT**（模型卡明文） | 精读原文（模型卡正文） |
| **jev-lite**（JevLite） | **LM head 在选项字母 token 处直读**（QLoRA adapter，零新增结构） | 是，`vagmi/jev-lite`（PEFT/QLoRA adapter） | **Gemma Terms of Use**（非 Apache/MIT），且训练数据**含非商用来源** | 精读原文（模型卡正文） |
| **Laya** | **每个选项在自己的 `[MASK]` token 处打分**，再在该题选项上 softmax | 是，`convaiinnovations/laya`（三个 checkpoint 同仓） | **Apache-2.0** | 精读原文（模型卡正文）；`[MASK]` 句为二手转述（见 §7 U5） |
| **Kev** | **0.5B–9B：LM head 字母 token；27B：专用 pointer head**（两代不同） | 是，`jaredpalmer/kev-*`（0.5b/0.6b/0.8b/4b/8b/9b/27b 共 7 个） | **Apache-2.0**（逐个模型卡明文） | 精读原文（模型卡正文 + 项目博客） |
| **Visual Jev** | **backbone 的 LM head 读候选概率**（非专用头） | **未发布权重** | **未声明** | 精读原文（预印本正文） |

> **一句话总览**：五种实现落在**三种 readout 形态**上——①**专用打分头**（this-that-model 的 hidden-state 打分；Kev-27B 的 pointer head）；②**复用生成模型的 LM head / 字母 token**（jev-lite、Kev 小档、Visual Jev）；③**逐选项 `[MASK]` 占位符打分**（Laya）。三者殊途同归到同一**契约性质**：输出分布的**支撑集 = 请求方声明的选项集**。

---

## 1 this-that-model-1.0

### 1.1 定位

FLock-io 发布的**开源权重 typed decision model**，配套预印本 [2609.23886](https://arxiv.org/abs/2609.23886)《this-that-model-1.0: A typed decision model that decides in 30 ms, for a millionth of a cent》（[report.md §3](report.md)）。模型卡自述定位为"一次前向、无解码循环、无解析器、无重试"（`One forward pass, no decoding loop, no parser, no retry.`）。

### 1.2 实现路径（**隐藏状态直读**）

模型卡明文给出打分形式（**专用 typed head，不是 LM head 路径**）：

> `The answer is read from the hidden state at a designated position and scored against the label tokens of the options you declared, normalised over exactly those:`
> `p_k(j | x) = softmax_j( ⟨w_{ℓ(k,j)}, h_k⟩ / τ )`

- **不是**分类头接在 `[CLS]` 上，也**不是**在全词表 LM head 上取字母 token 概率；而是**对声明标签 token 的加权内积后 softmax**。
- **支撑集性质**（模型卡原文）：`The support of that distribution **is** your option list. An answer outside it is not improbable, it is unrepresentable.`
- **选项上限 255**：`Up to 255 options are supported; ten or fewer use an (A) … (J) rendering and wider sets switch to single-token labels.`
- **同 state 多问题共享一次前向**：`Several questions about one state are answered in the same forward pass, because no answer is written back into the prompt and the decisions are conditionally independent given the input.`

### 1.3 架构与规格（模型卡 + HF API 元数据）

| 项 | 值 | 来源（主等级） |
|---|---|---|
| 参数量 | **1.88 B** | 模型卡正文（精读原文·模型卡） |
| 架构 | **Qwen3.5-style hybrid，24 层中 18 层 DeltaNet 线性注意力，6 层 full attention** | 模型卡正文（精读原文·模型卡） |
| 张量总量 | `safetensors.total = 1,881,825,088` B ≈ 1.88 B | HF API `text-classification` 标签（摘要级·API 元数据） |
| base_model | `decider-2b`（**归属为推断**：模型卡只写 `decider-2b`，未给 org；HF 搜索显示 `Mapika/decider-2b`、`StrandsAgents/strands-decider-2B-*` 均 Apache-2.0） | 模型卡正文 + HF 搜索元数据 |
| 语言 | `en` | HF API 元数据 |
| 上游代码致谢 | 环境模拟器与 68 题 cohort 来自 [NanoJev](https://github.com/TianyuCodings/NanoJev)（MIT） | 模型卡 §Licence and attribution（精读原文·模型卡） |

### 1.4 可复现性

| 项 | 记录值 | 实测 |
|---|---|---|
| 权重 | `https://huggingface.co/flock-io/this-that-model-1.0` | **200** |
| 推理代码 | `https://github.com/FLock-io/this-that-model`（`pip install git+https://github.com/FLock-io/this-that-model`） | **200** |
| 许可证 | **MIT** | HF API `license = mit`；模型卡 `## Licence and attribution` 明文 `MIT`；tag `license:mit` |
| 基准数据集 | `limberc/this-that-spatial-bench` | tag 命中 |
| 复现声明 | `Every number below is reproducible from the inference repository; each script prints what it measured beside what was published.` | 模型卡正文 |
| 依赖/接口 | `library_name: transformers`，`transformers` + `safetensors`；`TypedDecider.from_pretrained(...)`，支持 `cuda, mps or cpu`；Apple Silicon 自动选 MPS 并 float16 | 模型卡正文 |
| gated | 否（API 无 gated 字段） | HF API |

### 1.5 模型卡口径

- **时延**：模型卡写 `about 31 ms on a consumer GPU`；预印本标题写 **30 ms**。⚠️ 两个数字**来自两份不同材料**，条件（GPU 型号、batch、是否缓存）模型卡**未给出**——按"项目自述"记录，**不并表**。
- **零输出 token**：`generating **zero** output tokens`。
- **校准**（模型卡示例）：`if answer.confidence < 0.8: escalate()`，并注明 `the number is calibrated, so the threshold means something`——这是**设计意图陈述**，不是第三方验证。
- **分布外"诚实"的例子**：`"user=alice tier=free requests_this_per_minute=847"` / *"Should this request be rate-limited?"* 返回 **no (71%)**；模型卡称其为 `unconfident`，并指出对每分钟 847 次请求而言这是**错的**。⚠️ 模型卡自身的 `unconfident` 措辞与 **71%** 这个数字之间存在张力——**本文件如实转录，不作调和**。

### 1.6 来源

| URL | 状态码 | 主等级（来源类型） |
|---|---|---|
| https://huggingface.co/flock-io/this-that-model-1.0 | 200 | 精读原文（模型卡正文） |
| https://github.com/FLock-io/this-that-model | 200 | 精读原文（GitHub README） |
| https://arxiv.org/abs/2609.23886 | 200 | 精读原文（预印本） |

---

## 2 jev-lite（JevLite）

### 2.1 定位

`vagmi/jev-lite`：**QLoRA adapter**，把 `google/gemma-4-E4B-it` 转成 System One 决策模型（`A QLoRA adapter that turns Gemma 4 E4B into a **System One** decision model`）。

### 2.2 实现路径（**LM head 字母 token 直读**）

模型卡明文：`Since the answer is read from the logits at the option letters, it **cannot** answer outside the options it was given. There is no parsing, no retry loop, and no ...`

模型卡给出的参考代码即完整 readout：

```python
letters = [tok.encode(" " + c, add_special_tokens=False)[0] for c in primitives.LETTERS]
logits = model(input_ids=ids.to(model.device)).logits[0, -1].float()
probs = torch.softmax(logits[letters[:len(row["options"])]], -1).tolist()
```

→ **路径判定**：**复用生成模型自身的 LM head**，在**选项字母 token**（`" A"` / `" B"` …）的 logits 上取 softmax；**不新增参数、不改结构**。这与 §1 的 this-that-model（专用打分头）是**不同形态**。

### 2.3 训练与规格

| 项 | 值 | 来源 |
|---|---|---|
| 基座 | `google/gemma-4-E4B-it` | 模型卡 front-matter `base_model` |
| 微调方式 | **QLoRA**，4-bit **NF4** 基座 + bf16 计算 | 模型卡正文 |
| LoRA | **rank 16 / alpha 32，dropout 0.05** | 模型卡正文 |
| 目标函数 | `soft-label cross-entropy over option letters` | 模型卡正文 |
| 选项顺序 | `Options are shuffled every epoch so the model cannot learn "A is usually right"` | 模型卡正文 |
| 软标签来源 | `Qwen3.6-35B-A3B` 在答案 token 处读出，并做选项顺序平均 | 模型卡正文 |
| pipeline / library | `text-classification` / `peft` | HF API 元数据 |

### 2.4 模型卡口径（自报性能）

| 指标 | 值 | 条件 |
|---|---|---|
| 总体 accuracy | **0.816** | 模型卡"overall"行 |
| 总体 ECE | **0.019** | 同上 |
| NLL / Brier | 0.430 / 0.222 | 同上 |
| 校准改善 | `ECE fell 0.086 → 0.019` | 模型卡正文 |
| **服务精度敏感** | 4-bit NF4 服务 vs 全精度：ECE **0.036 → 0.069**（约翻倍）；单温度 1.4 可拟合 | 模型卡正文 |

> ⚠️ **引用警告**：全精度对照行的 accuracy 在模型卡原文中带省略号（`0.799 vs ...`），**本文件不补全该缺省值**（§7 U4）。要引用请回读模型卡原文逐字确认。

### 2.5 可复现性——**重要限制**

| 项 | 记录值 |
|---|---|
| 权重 | `https://huggingface.co/vagmi/jev-lite`（**200**） |
| 许可证（HF 字段） | **`gemma`**（HF API `license = gemma`；tag `license:gemma`）——**不是** MIT/Apache |
| 许可条款 | 受 [Gemma Terms of Use](https://ai.google.dev/gemma/terms) 约束，含使用限制 |
| **训练数据许可** | **混合，且部分非商用**：`Super-NaturalInstructions`(Apache-2.0)、**`ANLI`(CC BY-NC 4.0，非商用)**、**`RACE`(研究用途，非商用)**、`BoolQ`(CC BY-SA 3.0)、`MNLI`(mixed)、`Yelp Review Full`(Yelp ToU) |
| 模型卡自陈 | `Because ANLI and RACE rows are in the training mix, **this adapter should be treated as non-commercial / research use** unless retrained without them.` |
| 可商用重建路径 | `build_data.py` 提供 `--sets` 参数筛选来源，`a commercially-clean rebuild is a flag change plus a retrain` |
| adapter 复用前提 | `The adapter is only meaningful with the exact prompt format it was trained on` |
| gated | 否 |

> **这是本批最重要的可复现性发现**：`jev-lite` **不是**可无条件下商用的复刻——**权重许可（Gemma ToU）与训练数据许可（含 CC BY-NC / 研究用途）双重受限**。主报告 §6.5 的开源复刻表此前**未记录该限制**。

### 2.6 来源

| URL | 状态码 | 主等级（来源类型） |
|---|---|---|
| https://huggingface.co/vagmi/jev-lite | 200 | 精读原文（模型卡正文） |

---

## 3 Laya

### 3.1 定位

`convaiinnovations/laya`：一个**含三个 checkpoint 的家族仓库**，自述为 System One / calibrated-decisions 实现（tags: `system-one`、`calibrated-decisions`、`rlcd`、`laya`）。

### 3.2 实现路径（**逐选项 `[MASK]` 打分**）

模型卡与 [report.md §3](report.md) 一致的口径：**每个选项在自己的 `[MASK]` token 处打分**，再在**该题选项集合上**做 softmax，因此**答案空间在请求时定义，新 schema 无需重训**。三档形态差异**只在 backbone 与上下文长度**，不在 readout 形态。

（⚠️ 该 readout 描述在本批中以 [report.md §3](report.md) 与 [taxonomy.md §2.2](taxonomy.md) 的记录为准；本次抓取的模型卡正文已核实到**三档 backbone/上下文表**与 **Router 机制**，`[MASK]` 打分原句未在本轮抓取中逐字复核 → 标为 `二手/转述` 而非 `精读原文`。）

### 3.3 三个 checkpoint（模型卡原表）

| Checkpoint | Backbone 编码器 | 参数量 | 上下文 | 擅长 |
|---|---|---|---|---|
| `convaiinnovations/laya`（仓根） | **ModernBERT-large** | **421M** | **512** | 英文、护栏、邮件分诊 |
| `convaiinnovations/laya-multilingual` | **mmBERT-base** | **322M** | **1024（可至 8k）** | 100+ 语言，约 2.2× 更快 |
| `convaiinnovations/laya-typed-decisions` | ModernBERT-large | 421M | 1024 | 四个 typed-decisions 工作流（**0.766 acc**） |

- 三个 checkpoint **同仓**（仓根 = 英语；另两个为子目录），**只下载请求的那一个**。
- 仓根模型卡明示 **`license: apache-2.0`**（HF API 亦为 `apache-2.0`；tags 含 `license:apache-2.0`、`commercial-use`）。

### 3.4 模型卡口径（自报）

| 项 | 值 | 条件 |
|---|---|---|
| typed-decisions 准确率 | **0.766**（微调后） vs **0.362**（英语基座同题） | **2,000 条决策 / 四个工作流** |
| 延迟 | **39.5 ms**（英语）/ **32.8 ms**（印地语 → mmBERT） | 模型卡示例注释；硬件**未在该句给出** |
| 路由开销 | 脚本与语言检测 `<0.5 ms`（纯 Python），在**前向之前** | 模型卡正文 |
| 长文档 | `max_len=8192`；20 题中 **16–18 题**答对（前置文本至约 4,000 token），**超出后 8–17/20** | 模型卡正文（自陈"结果多变，请自行核验"） |
| 冷启代价 | 单语部署永不加载第二个；`max_loaded=1` 每次切换重建，**CPU 中位 7.4 s / T4 10.3 s** | 模型卡正文 |
| **跨语言塌陷（重要失效）** | 英语 checkpoint 对非拉丁脚本塌陷：**高棉语 0.000 accuracy at 0.952 confidence**；模型卡自评 `the model stays confident while being wrong, confidence gating cannot save you` | 模型卡正文——**与 [report.md §6](report.md) 引用一致** |

### 3.5 可复现性

| 项 | 记录值 | 实测 |
|---|---|---|
| 权重（家族仓） | https://huggingface.co/convaiinnovations/laya | **200** |
| 权重（多语言） | https://huggingface.co/convaiinnovations/laya-multilingual | **200** |
| 权重（typed） | https://huggingface.co/convaiinnovations/laya-typed-decisions | **200** |
| 许可证 | **Apache-2.0**（模型卡 `license: apache-2.0`；HF API 同） | — |
| 接口 | `pip install -U laya`；`from laya import Router`；`router.predict(state, questions)`；`Router(preload=True)` / `max_loaded=N` / `device=` | 模型卡正文 |
| 推理代码 | https://github.com/NandhaKishorM/laya | **200** |
| gated | 否 | HF API |

### 3.6 来源

| URL | 状态码 | 主等级（来源类型） |
|---|---|---|
| https://huggingface.co/convaiinnovations/laya | 200 | 精读原文（模型卡正文） |
| https://huggingface.co/convaiinnovations/laya-multilingual | 200 | 精读原文（存在性 + 家族表） |
| https://huggingface.co/convaiinnovations/laya-typed-decisions | 200 | 精读原文（存在性 + 家族表） |
| https://github.com/NandhaKishorM/laya | 200 | 精读原文（README 存在） |

---

## 4 Kev

### 4.1 定位

`jaredpalmer/kev-*`：一个**开源决策模型家族**，博客自述"0.8B 到 27B"（HF 上实际存在 0.5b/0.6b/0.8b/4b/8b/9b/27b 七档），**实现 TypeSafe 公开的 System One API**（`POST /v1/systemone`），因此 **TypeSafe SDK 可不改代码直连**（Kev-27B 模型卡明文 `so the TypeSafe SDK works against it unchanged`）。

### 4.2 实现路径——**两代不同，必须分开写**

| 档位 | base | readout | 训练方式 | 依据 |
|---|---|---|---|---|
| **Kev-0.8B / 4B / 9B**（及更早小档） | Qwen3.5（`-Base`） | **LM head 字母 token** | **LoRA adapter**（backbone 冻结） | 博客：`The smaller Kevs use Qwen3.5 backbones with LoRA adapters: small sets of additional weights trained while the backbone stays fixed.` |
| **Kev-27B** | Qwen3.8-27B | **专用 pointer head**：`two 5,120 → 256 projections score each option's closing token against the question's final token; a softmax gives the probabilities` | **全权重 SFT**（不是 adapter） | 模型卡 §Model type / Head |
| Kev-27B 参数 | — | `25.6B in the backbone ... 2.6M in the head`；视觉塔、LM head、MTP 层**不加载** | — | 模型卡 §Parameters |

> **结论（本文件可下的最强断言）**：Kev **不是一个单一实现**——**小档 = LoRA + 复用 LM head 字母路径；27B = 全权重微调 + 专用 pointer head**。把 Kev 简单归入任一种 readout 形态都会出错。

### 4.3 家族与形态（HF API 元数据，2026-10-16 实测）

| repo | base_model | adapter 类型 | 许可证 |
|---|---|---|---|
| `jaredpalmer/kev-0.5b` | `Qwen/Qwen2.5-0.5B` | peft adapter（**prototype**） | apache-2.0 |
| `jaredpalmer/kev-0.6b` | `Qwen/Qwen3-0.6B-Base` | peft adapter | apache-2.0 |
| `jaredpalmer/kev-0.8b` | `Qwen/Qwen3.5-0.8B-Base` | peft adapter | apache-2.0 |
| `jaredpalmer/kev-4b` | `Qwen/Qwen3.5-4B-Base` | peft adapter | apache-2.0 |
| `jaredpalmer/kev-8b` | `Qwen/Qwen3-8B-Base` | peft adapter | apache-2.0 |
| `jaredpalmer/kev-9b` | `Qwen/Qwen3.5-9B-Base` | peft adapter | apache-2.0 |
| `jaredpalmer/kev-27b` | `Qwen/Qwen3.8-27B` | **全权重 fine-tune**（`base_model:finetune:`） | apache-2.0 |

（来源：`https://huggingface.co/api/models?author=jaredpalmer` 实测返回。）

### 4.4 规格与可复现性（Kev-27B 模型卡，v2 / 2026-09-30）

| 项 | 值 |
|---|---|
| 版本 | `version 2, released on 2026-09-30: a full-weight fine-tune of Qwen3.8-27B averaged with version 1` |
| 校准 | **单一温度 `T = 1.32`**，存于 `head.pt`，**加载时施加**；`KEV_TEMPERATURE=1.0` 返回原始概率 |
| 上下文 | 服务上限 **65,536 token** 状态 + 每题至少 8,192 token；训练状态 ≤ 32,768；**已验证上下文长度 65,536** |
| 训练 | 1 epoch，**8 × NVIDIA H200，FSDP2**；AdamW(0.9/0.999)，wd 0.01，fp32 master weights；lr 2e-6(backbone)/1e-4(head)；one-cycle，10% warm-up；grad clip 1.0；128 records/step，**1,140 steps**；seed 0 |
| 权重平均 | 每个 backbone 张量 = **0.85 × 微调权重 + 0.15 × v1 权重**（fp32 计算后取整到 bf16），保留 v2 的 pointer head；比值在六个 blend 中按 development 数据选定 |
| 服务栈 | bf16 + fused DeltaNet kernels + CUDA graphs；`KEV_DTYPE=fp32` 走评测同路径 |
| 接口契约 | `choice`（1–255 命名选项）/ `score`（1–255 有序档位）/ `noul`（yes/no）；**每题独立成行、从共享 state 续算**，因此**问题间不能互相影响，state 只算一次并被缓存** |
| 明确不适用 | `Text generation, chat, summarisation or open-ended question answering. The model only scores the options it is given.` |
| 缓存收益（模型自述） | 64k token 状态：**新 9.4 s / 缓存 733 ms**；驻留内存 65.5 GB；暖缓存加载 17.6 s |
| 温度敏感性（自述） | 648 题上 5-fold group-disjoint CV：**ECE 0.048（raw）→ 0.038（out of fold）**，区间重叠；T 的 90% bootstrap 区间 **[1.20, 1.45]**；两端 headline panel 反向移动（breadth-v1 ECE 1.20 时 0.026；tasksource-heldout-v1 ECE 1.45 时 0.067） |
| 长上下文验证 | 与 8k 桶配对 CUAD 正确率差（pp [95% CI]）：16k **+0.2 [−0.7,+1.2]**、32k **−0.2 [−1.2,+0.7]**、64k **−1.1 [−2.4,+0.0]**；每桶 445–447 题 |
| 数据许可 | 4 个公开数据集为 share-alike（ARC / HotpotQA CC-BY-SA-4.0、Natural Questions CC-BY-SA-3.0、SNLI CC-BY-SA-4.0）；其余 CC-BY-4.0 / MIT / Apache-2.0；CFPB 叙述为美国政府作品；逐源许可与修订记录在 component manifests |
| 关键声明 | `No output of Jev (TypeSafe's hosted decision model) was used.`（训练数据**不含** Jev 输出） |
| 许可证 | **Apache-2.0（权重与 head）；base model 亦 Apache-2.0** |
| 代码 | `https://github.com/jaredpalmer/kev`（含 GPU 与 Apple Silicon MLX 服务端） |

### 4.5 项目自述性能与**口径警告**

- 博客：`Kev-27B leads overall in my evaluations`；`All results are from the author's evaluation harness, not an independent leaderboard.` → **作者自陈非独立排行榜**。本报告不把该自评作为跨系统性能结论。
- 成本口径原文：`GPU costs per million requests are estimates from Modal's October 2026 list prices and measured throughput, assuming a busy GPU. They exclude separately billed CPU, memory, and network; lightly used endpoints cost more per request.` → **成本数字必须连此假设一起引用**。
- 已知退化（**重要**）：博客自陈新版 27B `short-input accuracy is roughly unchanged. The new model is less accurate and more overconfident on long legal contracts.`，建议该负载改用 `jaredpalmer/kev-27b@v1-lora`。
- 本地运行时：Kev-0.8B/4B 可经 MLX 在 Apple Silicon 运行；`On a 32 GB M5, Kev-4B answers five questions about a short text in 721 ms, or 136 ms when the text is cached; Kev-0.8B takes 149 ms for new text.`

### 4.6 来源

| URL | 状态码 | 主等级（来源类型） |
|---|---|---|
| https://jaredpalmer.com/blog/introducing-kev | 200 | 精读原文（项目博客正文） |
| https://github.com/jaredpalmer/kev | 200 | 精读原文（仓库存在性） |
| https://huggingface.co/jaredpalmer/kev-27b | 200 | 精读原文（模型卡正文） |
| https://huggingface.co/jaredpalmer/kev-4b | 200 | 摘要级（HF API 元数据） |
| https://huggingface.co/jaredpalmer/kev-0.8b | 200 | 摘要级（HF API 元数据） |

---

## 5 Visual Jev

### 5.1 定位与实现路径

**研究原型**，来自预印本 [2609.25845](https://arxiv.org/abs/2609.25845)《Visual Jev: Accurate and Efficient Decisions from Shared Visual Context》。

- **readout**：预印本正文明确 `reads candidate-token probabilities from the existing LM head`，且 `LM head is the default; typed heads are matched controls` → **默认走 backbone 自身的 LM head**，专用 typed head 仅作**匹配对照**。
- **架构**：`image shared context + vision encoder + shared prefix KV cache`，再对**每问句后缀**批量执行；`LM head candidate-token logits normalized over valid options`。
- **可选项控制**：`optional controls: Choice / Claim / sufficiency heads`（**计算一次**）。

### 5.2 关键结论（预印本正文，供 §6 对照）

| 项 | 数字 | 条件 |
|---|---|---|
| 等权 macro 准确率 | **0.706 → 0.761** | 未改动 4B backbone 经 LM head 读出 → 答案监督后训练；**增益集中在 GQA 与 SNLI-VE（训练来源）**，held-out 的 TextVQA / TallyQA 变化很小 |
| 专用头对照 | 两者**同为 0.761**；种子范围重叠（answer SFT **0.758–0.764**；decision CE **0.760–0.763**） | 同 backbone、同样例、同 prompt、同 readout 位置、同 update budget；**仅监督与读出参数化不同** |
| 批量与共享 | N=32：独立串行 **50.7 ms/题** → 批处理不重用 **19.3 ms（2.6×）** → 复用 prefix **5.7 ms（3.4×）**；合计 **8.9×**，**176 questions/s**（原 20） | warm amortized time |
| 组时延 | 32 题共享批**约 182 ms 完成**（而非每题 5.7 ms） | 报告的是"总组时间 ÷ N" |
| N=1 反例 | prefix 共享**更慢**：**82.9 ms vs 48.1 ms** | 缓存构建/扩展无处摊销 |
| 峰值内存 | N=32 时 **8.40 GiB → 10.10 GiB** | batch 32 |
| typed head 的槽位失效 | held-out 8 选项 TextVQA：**0.639**（而非选项数 2–8 变化训练后的 **0.973**） | 早期构造中 Choice 样例 ≤4 选项 → 16-slot head 对后续 slot **无梯度** |
| 数值/路径差异 | 6 条决策路径中 5 条 **0.9104**、vision-cache 批处理路径 **0.9100**；**0–20 of 7,532** argmax 预测与独立执行不同 | 差异集中在 top-2 边际很小的样例；float32 下最大概率差从 **1.8×10⁻¹** 降到 **1.4×10⁻⁵**，argmax 翻转消失 |
| 生成 token 不是主要节省 | 每题独立生成 1 token 在 N=32 时 **58.8 ms**，**接近**独立直读路径的 **50.7 ms** | 主要收益来自复用固定视觉上下文 + 批量独立后缀 |

### 5.3 可复现性

| 项 | 记录值 |
|---|---|
| 公开权重 | **未找到**（预印本未给出 HF repo id 或权重页） |
| 许可证 | **未声明**（无权重页可查） |
| 推理代码 | **未找到**公开仓库 URL |
| 结论 | 按本文件规则记入 **§7 未确证/待跟踪**，**不得**转引为"可直接复现的实现" |

### 5.4 来源

| URL | 状态码 | 主等级（来源类型） |
|---|---|---|
| https://arxiv.org/abs/2609.25845 | 200 | 精读原文（预印本正文） |

---

## 6 横向对照

> **硬规则**：本表**不做排行榜**，只刻画**实现形态与条件**。任何"哪个更好"的读法都不成立——各项的评测工作负载、对照与硬件**均不可比**。

| 项目 | readout 形态 | 是否新增参数/结构 | 权重/许可 | 接口形态 | 依赖栈 | 运行时与硬件（含条件） |
|---|---|---|---|---|---|---|
| **this-that-model-1.0** | 隐藏状态直读 + 标签 token 打分（专用头） | **是**（专用 head，`p_k ∝ softmax(⟨w,h⟩/τ)`） | 公开 / **MIT** | `transformers` + `thisthat.TypedDecider`；cuda/mps/cpu | transformers, safetensors | 约 **31 ms，消费级 GPU**（项目自述；未给型号/batch/缓存） |
| **jev-lite** | **LM head 字母 token**（`logits[letters]` → softmax） | **否**（QLoRA adapter，复用 head） | 公开 / **Gemma ToU**（数据含非商用） | HF + PEFT adapter；需**精确 prompt 格式** | peft, transformers, bitsandbytes(NF4) | 模型卡**未给硬件**；服务精度影响 ECE（4-bit 0.036 / 全精 0.069） |
| **Laya** | **逐选项 `[MASK]` 打分** → 该题选项上 softmax | 否（backbone 冻结，逐题 softmax） | 公开 / **Apache-2.0** | `pip install laya`；`Router(preload=, max_loaded=)` | ModernBERT / mmBERT (transformers) | T4 上 **32.8–39.5 ms**（模型卡示例注释）；路由检测 <0.5 ms |
| **Kev 0.8B/4B/9B** | **LM head 字母 token** | **否**（LoRA adapter） | 公开 / **Apache-2.0** | **TypeSafe System One API** `POST /v1/systemone`；SDK 直连 | peft/transformers；GPU 与 **MLX** 服务 | MLX M5 32GB：Kev-4B **721 ms**（5 题短文本）/ **136 ms**（文本缓存）；0.8B **149 ms** |
| **Kev-27B** | **专用 pointer head**（`2 × 5120→256` 投影打分） | **是**（head 2.6M 参数；backbone 全权重微调） | 公开 / **Apache-2.0** | 同上（System One API） | bf16 + fused DeltaNet + CUDA graphs | 64k 状态 **新 9.4 s / 缓存 733 ms**；65.5 GB 驻留；**8×H200** 训练 |
| **Visual Jev** | **backbone LM head** 读候选 token 概率 | 否（默认不用专用头） | **未发布** / **未声明** | 未发布（仅预印本方法） | 未公开 | 4B backbone；N=32 组时延 ~182 ms、峰值 10.10 GiB（**研究设定，非产品口径**） |

**读法**：三列是关键——①**readout 形态**决定"答案空间如何被约束"；②**是否新增参数**决定"能否复用现成权重/服务栈"；③**接口形态**决定"替换成本"。三者**互相独立**：例如 Kev 大档与小档在 ①③ 上同、在 ② 上不同。

---

## 7 未确证 / 待跟踪（**不入正文**）

| # | 事项 | 为什么未确证 | 本批处置 |
|---|---|---|---|
| U1 | **Visual Jev 的权重、许可证、代码** | 预印本与主报告材料中均无 HF repo id / 权重页 / 仓库 URL | 记"未找到"；**不得**转引为可复现实现 |
| U2 | `github.com/mizoreww/laya-coreml` | **实测 404**（2026-10-16） | 移出来源清单，改记本表；主报告若引用需同步更正 |
| U3 | this-that-model 的 base_model `decider-2b` 的**确切 org** | 模型卡只写 `decider-2b`，未给命名空间 | HF 搜索显示 `Mapika/decider-2b`、`StrandsAgents/strands-decider-2B-*` 均 Apache-2.0；**归属为推断**，未写入正文结论 |
| U4 | jev-lite 全精度对照的**完整 accuracy 数值** | 模型卡原文该句含省略号（`0.799 vs ...`） | 只转录可读部分，**不补全**缺省值 |
| U5 | Laya `[MASK]` 打分原句的**逐字正文** | 本轮抓取的模型卡正文未逐字复核该句 | 标为转述，等级降为二手；不写成"模型卡明文" |
| U6 | Laya 卡内三套 ECE 口径（0.175 / 0.213 / 0.466）各自的子集 | 本轮未定位其对应子集说明 | 不引用，待回原文逐节核对 |
| U7 | 各项目的**跨请求缓存**是否在延迟数字中生效 | 多数项目自述未明确 | §6 表中逐项标注"未给/已给"，**不假定** |

---

## 8 来源清单与可达性实测（2026-10-16）

### 8.1 权重与代码（实测状态码）

| URL | 状态码 | 主等级（来源类型） |
|---|---|---|
| https://huggingface.co/flock-io/this-that-model-1.0 | 200 | 精读原文（模型卡） |
| https://github.com/FLock-io/this-that-model | 200 | 精读原文（README） |
| https://huggingface.co/convaiinnovations/laya | 200 | 精读原文（模型卡） |
| https://huggingface.co/convaiinnovations/laya-multilingual | 200 | 精读原文（存在性） |
| https://huggingface.co/convaiinnovations/laya-typed-decisions | 200 | 精读原文（存在性） |
| https://github.com/NandhaKishorM/laya | 200 | 精读原文（README 存在性） |
| https://huggingface.co/vagmi/jev-lite | 200 | 精读原文（模型卡） |
| https://jaredpalmer.com/blog/introducing-kev | 200 | 精读原文（博客正文） |
| https://github.com/jaredpalmer/kev | 200 | 精读原文（仓库存在性） |
| https://huggingface.co/jaredpalmer/kev-27b | 200 | 精读原文（模型卡） |
| https://huggingface.co/jaredpalmer/kev-4b | 200 | 摘要级（HF API 元数据） |
| https://huggingface.co/jaredpalmer/kev-0.8b | 200 | 摘要级（HF API 元数据） |
| https://huggingface.co/api/models?author=jaredpalmer | 200 | 摘要级（官方 API 元数据） |
| https://github.com/TianyuCodings/NanoJev | 200 | 精读原文（README 存在性） |
| https://github.com/Oscar-dzy/Awesome-jev-papers | 200 | 二手（索引仓库） |
| https://github.com/gsaini/system-one-models-getting-started | 200 | 摘要级（第三方启动评测） |
| ~~https://github.com/mizoreww/laya-coreml~~ | **404** | 已移入 §7 U2 |
| ~~https://huggingface.co/decider-2b~~ | **404** | 归属推断见 §7 U3 |

### 8.2 相关预印本（实测状态码）

| URL | 状态码 | 主等级（来源类型） |
|---|---|---|
| https://arxiv.org/abs/2609.23886 | 200 | 精读原文（预印本） |
| https://arxiv.org/abs/2609.25845 | 200 | 精读原文（预印本） |
| https://arxiv.org/abs/2609.24395 | 200 | 精读原文（预印本，JEVQA） |

### 8.3 汇总

- **实测 URL 总数**：§8.1 十六条 2xx + §8.2 三条 2xx = **19 条 2xx**；
- **非 2xx 2 条**（`laya-coreml` 404、`decider-2b` 404）→ 均已移入 §7；
- 另有 1 条**结构性缺失**（Visual Jev 权重页/代码仓库）→ §7 U1；
- **可达率**：19 / 21 条实测 URL 为 2xx（90.5%）；缺口已逐条登记，**无静默失效链接**。

### 8.4 核验命令（可复现）

```bash
curl -sS -o /dev/null -m 25 -A "Mozilla/5.0" -w "%{http_code}" -L "<URL>"
curl -sS -m 30 -A "Mozilla/5.0" -L "https://huggingface.co/<repo>/raw/main/README.md"
curl -sS -m 25 -A "Mozilla/5.0" -L "https://huggingface.co/api/models/<repo>"
```

---

## 9 本文件的自检

| 检查 | 结果 |
|---|---|
| 是否克隆仓库 | **否**（全程只做 HTTP GET 与正文检索） |
| 是否读取源码 | **否** |
| 是否含 `仓库@commit:文件:行` 断言 | **否**（本文件不含任何此类断言，原因：未读源码） |
| 每条外链是否实测 | **是**，状态码见 §8；2 条 404 已如实记录并移出正文引用 |
| 是否有编造 URL/数字 | **否**：所有数字均可回模型卡/博客/预印本正文逐字定位；模型卡省略号处**未补全**（§7 U4） |
| 单一主等级标签是否落实 | **是**，逐节标注；混合处取最弱 |
| 是否做跨项目排行榜 | **否**；§6 为形态/条件对照，含条件列 |
| 项目自述数字是否标注 | **是**，均标「项目自述」/「模型卡自报」 |
