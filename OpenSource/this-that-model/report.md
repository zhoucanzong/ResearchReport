---
display_name: this-that-model
type: repo-research
domain: Repo-Research
subject: this-that-model
upstream: https://github.com/FLock-io/this-that-model@6af11c63c8bb260aa4bed2b7717f33f25decd16e
date: 2026-10-16
evidence: 精读原文
status: completed

---

# this-that-model 仓库深读

> **源码与证据范围**：代码结论对应 `FLock-io/this-that-model` 固定 commit `6af11c63c8bb260aa4bed2b7717f33f25decd16e`；模型配置来自 `flock-io/this-that-model-1.0` 的 `config.json`，外部研究背景见 [arXiv:2609.23886](https://arxiv.org/abs/2609.23886)。代码事实、文档自述、二手信息与受限核验分别标注 `[精读原文]`、`[摘要级]`、`[二手]`、`[受限核验]`。未下载权重或运行模型，因此权重数值属性不超出配置文件声明。源码索引见 [sources/MANIFEST.md](sources/MANIFEST.md)。

---

## 0. 本章结论

1. **类型化决策头走「隐藏状态直读」，且没有独立分类头**：读数矩阵直接取 **LM head（与词嵌入 tied）中「声明标签 token」对应的行**做内积——不是新训练的 head，也不是全词表 softmax。`[精读原文]`（代码事实：`thisthat/backends/torch_backend.py:85`、`thisthat/backends/mlx_backend.py:112`；配置佐证：`config.json` 的 `tie_word_embeddings = True`）
2. **归一化是「受限 softmax + 温度」**：越界选项先置 `-inf`，再在该行上归一化，因此分布的输出位置**限制在声明选项内**（有限精度下可有零概率项）。`[精读原文]`（代码事实：`thisthat/model.py:40`、`thisthat/model.py:47`、`thisthat/backends/torch_backend.py:88`）
3. **每个实际 batch 单次前向读出其全部答案 slot**：`model.py:118-132` 先按 `batch_size` 分 chunk，每个 chunk 的 `slot_logits(...)` 取回其全部 slot 的 logits，再 softmax 并按题切片——没有解码循环。`[精读原文]`（代码事实：`thisthat/model.py:132`、`thisthat/model.py:134`、`thisthat/model.py:137`）
4. **训练目标 / 损失：本仓库不含训练代码**，因此「损失中是否含校准项」**未确证**；仓库只提供推理包与复现脚本（已读推理/复现入口未见训练过程；字面搜索只作为线索）。`[精读原文]`（代码事实：`scripts/` 与 `thisthat/` 全目录无训练路径）
5. **`confidence` 不是独立输出头**，而是「所选选项的概率」；校准是**事后测量**（benchmark 的 calibration 划分 + 回归测试）；本仓库无训练实现，**不能据此排除仓外训练使用校准损失**。`[精读原文]`（代码事实：`thisthat/types.py:52`、`thisthat/types.py:53`、`tests/test_published_results.py:49`）
6. **与生成式分类头的区别**：该实现复用 tied LM head 的标签行做选项受限打分，而非新增独立分类层；分类范围来自声明选项集。`[精读原文]`

> 一句话定位：这是一套**限定在声明选项集上的单次前向打分器**——把「生成后解析」换成「在选项行上做一次受限内积 + softmax」。

---

## 1. 源码版本与模型接口

| 项 | 来源信息 |
|---|---|
| 代码仓库 | `FLock-io/this-that-model`，固定 commit `6af11c63c8bb260aa4bed2b7717f33f25decd16e` |
| 模型配置 | `flock-io/this-that-model-1.0`，`config.json`；24 层、hidden size 2048、词表 248,320、`tie_word_embeddings=True`，含 18 个 linear attention 层和 6 个 full attention 层 |
| 研究材料 | [arXiv:2609.23886](https://arxiv.org/abs/2609.23886)；模型卡与论文口径在相关章节单独区分 |
| 代码结构 | `thisthat/` 提供模型、prompt/slot 构造、类型、服务协议及 PyTorch/MLX 后端；`scripts/reproduce_*.py` 与结果 JSON 提供复现入口 |

上述参数是 `config.json` 的声明值；权重张量未加载，故不能据此断言实际嵌入行与输出行逐元素相同。代码路径、配置属性和论文/模型卡自述在下文分别标注。

## 2. 类型化决策头的实现路径

### 2.1 候选路径与判定

| 候选实现路径 | 是否存在 | 依据（钉住 SHA） | 判定 |
| :-- | :-- | :-- | :-- |
| **隐藏状态直读**（指定位置取 hidden state） | ✅ **是** | `thisthat/backends/torch_backend.py:83`、`thisthat/backends/mlx_backend.py:110` | **本仓库实际路径** |
| 线性打分（linear readout） | ✅ **是**，但**复用 tied LM head 的标签行**，非新 head | `thisthat/backends/torch_backend.py:85`、`thisthat/backends/torch_backend.py:86`、`thisthat/backends/mlx_backend.py:112` | **本仓库实际路径** |
| 微调分类头（独立 classifier / `[CLS]` 头） | ❌ **无** | 全仓无独立 head 模块；读数矩阵来自 `lm_head.weight` / `embed_tokens` | **排除** |
| 生成式解码 + 解析选项字母 | ❌ **无** | `thisthat/model.py` 无 decode loop；选项之外「不可表示」 | **排除** |
| 逐选项 `[MASK]` 占位打分（Laya 式） | ❌ **无** | `thisthat/prompt.py` 无 mask 占位符 | **排除** |

**实现路径**：隐藏状态直读 → tied LM head 标签行内积 → 选项掩码与受限 softmax（`thisthat/backends/torch_backend.py:85`、`thisthat/backends/mlx_backend.py:112`）。仓库实现没有独立微调分类头，也没有生成后再解析选项字母的解码循环。

### 2.2 读数矩阵来自哪里

- 标签集在**构造 backend 时**固定为「选项标签 token」：`self._labels = torch.tensor(option_label_ids(tokenizer), ...)`（`thisthat/backends/torch_backend.py:53`），标签表本身由 `label_table` 生成 **255 个单 token 标签**（`thisthat/prompt.py:35`、`thisthat/prompt.py:63`）。
- PyTorch 路径取 **LM head 的标签行**：`w = self.model.lm_head.weight[self._labels]`（`thisthat/backends/torch_backend.py:85`），即从 `vocab_size = 248320` 的词表中只取 ≤255 行做内积。
- MLX 路径不做权重复制，直接用 tied 投影：`logits = backbone.embed_tokens.as_linear(h)[:, self._labels]`（`thisthat/backends/mlx_backend.py:112`）。
- 上游 `config.json` 的 `tie_word_embeddings = True` 是「两条路径等价」的配置级依据：`lm_head.weight` 与 `embed_tokens` 是同一矩阵。

### 2.3 关键短引用（共 14 行，均标注 `文件:行`）

```text
thisthat/model.py:47                      z = logits.astype(np.float32) / temperature
thisthat/model.py:132                     logits = self.backend.slot_logits(ids, attn, np.array(slot_idx), np.array(slot_batch),
thisthat/model.py:134                     probs = _softmax(logits, temperature)
thisthat/model.py:137                     p = [float(x) for x in probs[row_i][:len(q.options)]]
thisthat/model.py:141                     index=max(range(len(p)), key=p.__getitem__), probabilities=p)
thisthat/backends/torch_backend.py:83     h = hidden[torch.as_tensor(slot_batch, device=dev),
thisthat/backends/torch_backend.py:85     w = self.model.lm_head.weight[self._labels]            # [MAX_OPTIONS, H]
thisthat/backends/torch_backend.py:86     logits = torch.nn.functional.linear(h, w).float().cpu().numpy()
thisthat/backends/torch_backend.py:88     return np.where(past, -np.inf, logits).astype(np.float32)
thisthat/backends/mlx_backend.py:112      logits = backbone.embed_tokens.as_linear(h)[:, self._labels]
thisthat/types.py:7                       MAX_OPTIONS = 255
thisthat/types.py:53                      return self.probabilities[self.index]
thisthat/prompt.py:63                     def option_label_ids(tok) -> list[int]:
thisthat/server.py:103                    "confidence": d.confidence, "latency_ms": round(ms, 2)},
```

---

## 3. 输出层与训练目标

### 3.1 head 结构（输出层）

- **打分**：`h`（每个答案 slot 的隐藏状态）与 `w`（标签行）做内积（`thisthat/backends/torch_backend.py:86`）。
- **温度**：内积结果先除以 `temperature`（`thisthat/model.py:47`，默认 `1.0`，`decide` 参数）。
- **受限 softmax**：`_softmax` 在 float32 下逐行归一化（`thisthat/model.py:40`），并在打分阶段把**越界选项置 `-inf`**（`thisthat/backends/torch_backend.py:88`），因此分母只覆盖本题声明的选项。
- **切片与再归一化**：按该题选项宽度切片并二次归一化（`thisthat/model.py:137`），最后 argmax 选答案、分布存进 `Decision.probabilities`（`thisthat/model.py:141`）。
- **对外形态**：`Decision.confidence` = 所选选项的概率（`thisthat/types.py:53`），服务端按需暴露（`thisthat/server.py:103`），OpenAI 兼容面把它映射成 `logprob`。
- **选项上限**：`MAX_OPTIONS = 255`（`thisthat/types.py:7`）；`Question` 强制 ≥2、≤255、且互异（`thisthat/types.py:22-30`）。

### 3.2 损失 / 训练目标：**本仓库内未确证**

本仓库**不含训练代码**（无 `loss` / `backward()` / `optimizer` / 数据加载路径），因此：

- 「标签 token 打分」是否由**交叉熵**训练、是否带 temperature 学习、是否含**校准正则项**：**未确证** `[精读原文]`（范围内的否定证据：全仓零命中）。
- 可确证的只有**推理侧**事实：分布是「真正的选项分布」而非词表 softmax，README 与 `types.py` 文档均以「阈值因此有意义」作为**设计主张**——属**文档自述**，非代码可证。`[摘要级]`

### 3.3 confidence 与校准

| 问题 | 代码事实 | 等级 |
| :-- | :-- | :-- |
| 是否有独立 confidence head / 校准层？ | **无**：`confidence` 是 `@property`，返回 `probabilities[index]`（`thisthat/types.py:52-53`） | `[精读原文]` |
| 是否有校准损失项？ | **未确证**（无训练代码） | `[精读原文]`（范围内否定） |
| 校准如何被验证？ | 作为**评测**存在：`tests/test_published_results.py:49` 的 `test_calibration_beats_a_constant_predictor` 用 simulator 的随机集合比对「常数预测器」；`benchmarks/simulator/tasks.py` 设 `calibration` 划分 | `[精读原文]` |

**推论（研究推断，非代码事实）**：该设计的「可信」来自**支撑集受限 + 事后校准测量**，而不是某个校准模块。引用其置信度阈值（如 `confidence < 0.8` 升级人工）时，应同时说明「阈值有效性由该项目自测，非第三方验证」。

---

## 4. 与 `DecisionModels` 的方法对照

> 对账对象（均为 `[二手]`/`[摘要级]` 的模型卡口径）：[taxonomy.md](../../LLM/DecisionModels/taxonomy.md)、[open-implementations.md](../../LLM/DecisionModels/open-implementations.md)、[report.md](../../LLM/DecisionModels/report.md)。

| # | DecisionModels 说法（出处） | 代码事实（本条目锚点） | 判定 |
| :-- | :-- | :-- | :-- |
| R1 | 「隐藏状态直读 + 声明标签 token 打分」（`open-implementations.md:26`） | `torch_backend.py:83`、`:85`、`:86` | **一致** |
| R2 | 「**不是**在全词表 LM head 上取字母 token 概率」+ 归入「**专用打分头**」（`open-implementations.md:32`、`:49`） | 读数矩阵**就是** LM head 的标签行（`torch_backend.py:85`；tied 见 `mlx_backend.py:112` + `config.json` `tie_word_embeddings=True`） | **需修正**：应写「复用 tied LM head 的标签行做受限打分；**无独立分类头**」 |
| R3 | 「选项上限 255，≤10 用 (A)…(J)」（`taxonomy.md:99`、`open-implementations.md:51`） | `types.py:7`、`prompt.py:35` | **一致** |
| R4 | 「支撑集 = 选项表，选项之外**不可表示**」（`taxonomy.md:99`、`report.md:152`） | `torch_backend.py:88`（越界项置 `-inf`，代码事实与文档自述相符） | **一致** |
| R5 | 「同 state 多问题共享一次前向、条件独立」（`report.md:184`） | `model.py:118-132` 每 chunk 统一取 slot | **部分支持**：共享一次前向成立；代码没有证明问题/输出在统计意义上条件独立，slot 还受同一构造 prompt 影响 |
| R6 | 「31 ms / 30 ms（`open-implementations.md:79`：两份材料、条件未给出）」 | 仓库记录：`results_latency_mlx.json` `mean 25.24 / p90 30.50 ms`（n=100，68 题，mlx float16）；`results_latency_mps.json` `mean 113.34 ms`；**无 30.9** | **未确证 / 口径不可并表**：应记为「同一量级，条件不同」 |
| R7 | 「`answer.confidence` 是 calibrated，阈值有意义」（`open-implementations.md:81`） | `types.py:52-53`（confidence = argmax 概率）；校准是事后测试（`test_published_results.py:49`） | **需修正口径**：非独立校准头 / 非损失项，属**自测主张** |
| R8 | 「1.88B、24 层中 18 层 DeltaNet、MIT」（`report.md:416`） | `config.json`：24 层 = 18 `linear_attention` + 6 `full_attention`、`hidden_size=2048`；`LICENSE:1` MIT；`README.md:52` | **一致**（参数量 1.88B 由 README/权重规模自述，`[摘要级]`） |

**供 `DecisionModels` 条目引用的结论**：

> `this-that-model` 的读数**复用 tied LM head 的标签行**（无独立分类头），实现细节见 [this-that-model-research/report.md](report.md) 章 2–3。



---

## 5. 单次前向读出候选概率的代码路径（逐处 `文件:行`）

调用链（自上而下，全部为代码行）：

1. `thisthat/model.py:110` —— `build(...)` 为每个 (state, questions) 生成 `slots` / `n_options`
2. `thisthat/prompt.py:89` —— `_answer_slots(...)` 决定「第 k 问的答案落在哪个位置」
3. `thisthat/model.py:132` —— **单次** `self.backend.slot_logits(ids, attn, slot_idx, slot_batch, n_opt)`（一批的全部 slot 一次算完）
4. `thisthat/backends/torch_backend.py:79` —— 骨干前向取 `last_hidden_state`
5. `thisthat/backends/torch_backend.py:83` —— 按 slot 索引取出 `[N, H]` 隐藏状态
6. `thisthat/backends/torch_backend.py:85` —— 取 tied LM head 的标签行 `w`（MLX 等价：`thisthat/backends/mlx_backend.py:112`）
7. `thisthat/backends/torch_backend.py:86` —— 线性打分（MLX 等价：`mlx_backend.py:109`、`:110`）
8. `thisthat/backends/torch_backend.py:88` —— 越界选项置 `-inf`（MLX 等价：`mlx_backend.py:117`）
9. `thisthat/model.py:134` —— `_softmax(logits, temperature)`（温度在 `model.py:47`）
10. `thisthat/model.py:137` —— 按该题选项宽度切片并再归一化
11. `thisthat/model.py:141` —— argmax 得答案、写入 `probabilities`
12. `thisthat/prompt.py:63` / `thisthat/backends/torch_backend.py:53` —— 标签 token 集合的来源（`_labels`）

---

## 6. 锚点表

> 复核方式：钉住 commit `6af11c6`，逐条 `git show <SHA>:<path> | sed -n '<行>p'`；落在**注释行 / 文档串 / 空行**的锚点判不合格。

| 编号 | 断言 | 锚点 | 依据 | 判定 |
| :-- | :-- | :-- | :-- | :-- |
| A01 | 选项上限硬编码为 255 | `thisthat/types.py:7` | `MAX_OPTIONS = 255` | 命中 |
| A02 | `confidence` 即所选选项的概率（非独立头） | `thisthat/types.py:53` | `return self.probabilities[self.index]` | 命中 |
| A03 | 标签表构造（255 个单 token 标签） | `thisthat/prompt.py:35` | `def label_table(tok):` | 命中 |
| A04 | head 被限制到的标签 token 集合 | `thisthat/prompt.py:63` | `def option_label_ids(tok) -> list[int]:` | 命中 |
| A05 | 每题一个答案 slot 位置 | `thisthat/prompt.py:89` | `def _answer_slots(...)` | 命中 |
| A06 | 受限 softmax 定义 | `thisthat/model.py:40` | `def _softmax(logits, temperature)` | 命中 |
| A07 | 温度 τ 的落点 | `thisthat/model.py:47` | `z = logits.astype(np.float32) / temperature` | 命中 |
| A08 | 单次调用取回该批全部 slot 的 logits | `thisthat/model.py:132` | `logits = self.backend.slot_logits(...)` | 命中 |
| A09 | logits → 概率 | `thisthat/model.py:134` | `probs = _softmax(logits, temperature)` | 命中 |
| A10 | 只取该题选项宽度 | `thisthat/model.py:137` | `p = [float(x) for x in probs[row_i][:len(q.options)]]` | 命中 |
| A11 | argmax 选答案 + 存分布 | `thisthat/model.py:141` | `index=max(range(len(p)), key=p.__getitem__), probabilities=p)` | 命中 |
| A12 | 读数标签集来自标签 token 表 | `thisthat/backends/torch_backend.py:53` | `self._labels = torch.tensor(option_label_ids(tokenizer), ...)` | 命中 |
| A13 | 骨干前向（PyTorch 路径） | `thisthat/backends/torch_backend.py:79` | `hidden = self.model.model(` | 命中 |
| A14 | 按 slot 取隐藏状态 | `thisthat/backends/torch_backend.py:83` | `h = hidden[torch.as_tensor(slot_batch, device=dev),` | 命中 |
| A15 | 读数矩阵 = tied LM head 的标签行 | `thisthat/backends/torch_backend.py:85` | `w = self.model.lm_head.weight[self._labels]` | 命中 |
| A16 | 线性打分（内积） | `thisthat/backends/torch_backend.py:86` | `logits = torch.nn.functional.linear(h, w)...` | 命中 |
| A17 | 越界选项置 `-inf` | `thisthat/backends/torch_backend.py:88` | `return np.where(past, -np.inf, logits)...` | 命中 |
| A18 | 骨干前向（MLX 路径） | `thisthat/backends/mlx_backend.py:109` | `hidden = backbone(mx.array(np.asarray(ids, ...)))` | 命中 |
| A19 | 按 slot 取隐藏状态（MLX） | `thisthat/backends/mlx_backend.py:110` | `h = hidden[mx.array(np.asarray(slot_batch, ...)),` | 命中 |
| A20 | tied 投影取标签列（无独立 head 权重） | `thisthat/backends/mlx_backend.py:112` | `logits = backbone.embed_tokens.as_linear(h)[:, self._labels]` | 命中 |
| A21 | 越界选项置 `-inf`（MLX） | `thisthat/backends/mlx_backend.py:117` | `return np.where(past, -np.inf, out)...` | 命中 |
| A22 | 服务端按需暴露 confidence | `thisthat/server.py:103` | `"confidence": d.confidence, "latency_ms": ...` | 命中 |
| A23 | `build(...)` 为每个 (state, questions) 生成 slots / n_options | `thisthat/model.py:110` | `built = [build(self.tokenizer, s, q, layout=layout, ...)]` | 命中 |
| A24 | `Question` 构造校验（≥2、≤255、互斥） | `thisthat/types.py:22` | `def __post_init__(self):` | 命中 |
| A25 | `confidence` 为属性而非独立头输出 | `thisthat/types.py:52` | `def confidence(self) -> float:` | 命中 |

**未命中数 = 0**（25/25 命中；无一条落在注释行、文档串或空行）。

---

## 7. 未确证事项

1. **训练目标与损失**：本仓库没有训练代码，训练目标与校准损失无法由推理实现确定；公开论文材料需另行确认。
2. **时延口径**：仓库记录 MLX `mean 25.24 / p90 30.50 ms`（68 题、n=100）；模型卡「约 31 ms」、论文标题「30 ms」、论文正文「30.9 ± 16.6 ms（内部套件）」**条件互不相同** → 本条目按「同一量级、口径不可并表」处理。
3. **参数量 1.88B**：来自 README/权重规模自述，不是从 `config.json` 逐项推导的参数总数（`hidden_size=2048`、24 层、`intermediate_size=6144`、`vocab_size=248320` 已核；完整参数量不在当前证据范围内）。`[摘要级]`
4. **权重内部数值**：`tie_word_embeddings=True` 已由配置确证，但「标签行与嵌入行在权重层面完全一致」目前只有配置声明，权重级相等未确认。`[受限核验]`


---
