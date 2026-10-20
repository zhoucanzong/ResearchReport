# DeepSeek Harness 深读：compaction 后端与 base 插件清单（只读）

> **版本依据**：`package.json:3` 的 `"version": "0.2.1-rc.2"`。快照 `/tmp/dsh-src` **没有 git 元数据**（无 `.git`），所以本文不引 commit SHA，所有引用写成 `packages/...#行`（行号对应上述快照）。
> **纪律**：源码只读（不改 `/tmp/dsh-src`、不动正在运行的 App）；行为结论一律落到代码行，"推断"单独标注。
> **范围**：任务 1 = `packages/compaction/` 下 5 个目录（`compaction`、`compaction-basic`、`compaction-image-offload`、`compaction-tool-result-pruner`、`command-compact`）；任务 2 = `packages/bundle/base/cordis.patch.yml`（529 行）。

---

## 结论摘要（5 条）

1. **5 个目录里只有 1 个是真后端**：`compaction` 是抽象契约（`CompactionEngine` 基类 + `super(ctx, 'compaction')`，`packages/compaction/compaction/src/index.ts:119-122`，三个抽象操作在 `:136`、`:162`、`:187`）；`compaction-basic` 是唯一 `extends CompactionEngine` 的实现（`packages/compaction/compaction-basic/src/index.ts:113`）；`compaction-tool-result-pruner` 是独立服务（`packages/compaction/compaction-tool-result-pruner/src/index.ts:44`）；`compaction-image-offload` 是监听 `agent/request-error` 的投影插件（`packages/compaction/compaction-image-offload/src/index.ts:25-40`）；`command-compact` 只是 `/compact` 的触发器（`packages/compaction/command-compact/src/index.ts:67`）。

2. **只有 `compaction-basic` 替换"历史区间"**：它把一段表面节点换成一条摘要用户消息（`packages/compaction/compaction-basic/src/region.ts:505-509`）。pruner 只改单条 `tool/result` 的文本中段（`packages/compaction/compaction-tool-result-pruner/src/index.ts:83-122`）；image-offload 只把选中图片标成 `offloaded: true`、由投影换占位文本（`packages/compaction/compaction-image-offload/src/project-message.ts:13-36`）；command-compact 自身不压缩任何内容（`packages/compaction/command-compact/src/index.ts:67-73`）。

3. **"被遮蔽内容仍留在会话日志"不是文档承诺，而是会话层的两条硬约束**：①日志只 `push` 不 splice（`packages/core/session/src/index.ts:886`），替换只改模型可见投影 `state.nodes`（`packages/core/session/src/surface.ts:570`）；②替换事件必须把**每一个**被遮蔽 seq 列入 `sourceEventSeqs`，缺一个就拒绝 append（`packages/core/session/src/surface.ts:361-364`）。压缩后端照此执行（`packages/compaction/compaction-basic/src/region.ts:505-509`；`packages/compaction/compaction-tool-result-pruner/src/index.ts:165-171`）。

4. **所有 `compaction/*`、`command/*` 事件都是 log-only**：`SurfaceEventType` 是封闭联合，只含 system/developer/user/assistant/tool-result（`packages/core/session/src/types.ts:440-448`）；非 surface 事件携带 `surfaceOp` 会被拒（`packages/core/session/src/surface.ts:302-313`）。因此压缩元数据永远不会挤掉模型可见内容，也不可能"顺手"删除历史。

5. **`packages/bundle/base/cordis.patch.yml` 共 96 条插件行：87 条必挂 + 1 条 `disabled: true` + 8 条 `disabled: !!js` 条件挂载**（`packages/bundle/base/cordis.patch.yml:15-529`）。三种独立数法（行级 grep / awk 状态机 / YAML 结构解析）结果一致；但 `!!js` 出现 **16 次**，只有 8 次是挂载条件，另 8 次在 `config` 值里——只数 `!!js` 会把 96/1/8 误算成"96/1/14"。

---

## compaction 后端对比表

先给结论的骨架：5 个目录分四类——**契约**（`compaction`）、**后端**（`compaction-basic`）、**伴随服务**（pruner / image-offload）、**人工触发器**（`command-compact`）。5 个包在 base 组合里都挂了（`packages/bundle/base/cordis.patch.yml:351-357`、`:425-435`）。

| 目录 | 角色 | ① 压缩什么 | ② 丢弃 / 保留 | ③ 触发 | ④ 日志中保留被遮蔽内容的实现 | ⑤ 失败 / 回滚 |
|---|---|---|---|---|---|---|
| `compaction/` | 契约（无实现） | 不压缩任何内容 | 不适用 | 无自动触发；只定义 `pressure`/`context-overflow` 与手动失败码 | 只规定 `compaction/*` 为 log-only、禁止 `surfaceOp`；替换必须走 checkpoint 标记 | 自身无运行时路径；只定义失败分类闭集 |
| `compaction-basic/` | 真后端（`ctx.compaction`） | 一段"非 system 起、平衡切点止"的旧历史区间 → 一条文本摘要 | 丢：区间内逐条原文/工具细节/图片输出；留：system 头、按 token 预算保留的近期尾部、成对工具调用 | 自动：`agent/pre-step` 压力 + `agent/request-error` 上下文溢出；手动：`/compact` 或程序调 `compactNow` | 替换 `user/message` 带 `surfaceOp.replace`，并把 `start`、`summary` 与全部被遮蔽 seq 写进 `sourceEventSeqs` | 替换前失败 = 历史不变；替换后失败 = 只追加带 `error` 的 `compaction/end`；**无回滚**，孤儿 start 即锁 |
| `compaction-tool-result-pruner/` | 伴随服务（`ctx.toolResultPruner`） | 单条 `tool/result` 超阈值的**文本中段** | 丢：中段文本；留：文本头/尾、非文本块及其顺序、事件其余字段 | 不自触发；只被 compaction-basic 在压缩触发合格后调用 | 先追加 `compaction/prune` 影子价事件，再追加 `tool/result` 替换（`sourceEventSeqs: [原 seq]`） | 无回滚；本轮已提交的替换保持持久（逐条原子 append） |
| `compaction-image-offload/` | 伴随插件（消息投影） | 不改历史：把选中的输入图片标记为 `offloaded` | 丢：后续请求里的图片本体（换占位文本）；留：消息身份、图片块、日志 | 自动：`IMAGE_OFFLOAD_REQUIRED` 请求错误 + 摘要错误瀑布 | `image/offload` 是 log-only 消息投影事件，读取时才把选中块投影成 `offloaded: true` | 无可关选项即失败即 `next()`（保留原错误）；append 抛错直接上抛，无回滚 |
| `command-compact/` | 人工命令 | 不压缩；委托给当前后端 | 不适用 | 仅人手动 `/compact`（无参数） | 命令生命周期 `command/run`/`command/done` 是 log-only；`sourceEventSeq` 指向 `compaction/summary` | 把预期失败映射成稳定文案；取消/未知错误分别处理 |

### 1. `packages/compaction/compaction`——契约层（不是后端）

**① 压缩什么**：什么都不压。它是 Service Definition：`CompactionEngine` 抽象类注册 `ctx.compaction`（`packages/compaction/compaction/src/index.ts:119-122`），三个抽象操作 `compactIfNeeded`（`:136-140`）、`compactNow`（`:162-166`）、`compactRegion`（`:187-192`），由后端实现"何时压、留多少、怎么摘要"。

**② 丢什么、保留什么**：契约不定策略，只定形状——成功运行"把一个表面 span 换成一条摘要节点"（`packages/compaction/compaction/src/index.ts:110-118`），替换必须是带 `compactCheckpointSource` 的 `user/message`（`:174-177`；构造见 `packages/compaction/compaction/src/checkpoint.ts:33-42`）。

**③ 触发方式**：无自动触发、无命令。只定义触发枚举 `'pressure' | 'context-overflow'`（`packages/compaction/compaction/src/index.ts:32`）、手动失败码闭集（`:35-41`）和摘要错误恢复瀑布 `'compaction/summary-error'`（`:106`）。真正的触发全在 `compaction-basic` 与 `command-compact`。

**④ 日志保留的代码依据**：`compaction/*` 三类事件在类型层显式声明为 log-only、不带 `surfaceOp`——`compaction/start`（`packages/compaction/compaction/src/types.ts:19-24`）、`compaction/summary`（`:25-33`）、`compaction/end`（`:68-72`）、`compaction/prune`（`:73-89`）。会话侧再把这条规则变成运行时拒绝：非 surface 事件带 `surfaceOp` 或 `sourceEventSeqs` 直接抛错（`packages/core/session/src/surface.ts:302-313`）；`SurfaceEventType` 封闭联合不含 `compaction/*`（`packages/core/session/src/types.ts:440-448`）。摘要的落点另由 checkpoint 标记保证可识别：`compactCheckpointSource()` 冻结 `{kind:'compact-checkpoint', compactionId}`（`packages/compaction/compaction/src/checkpoint.ts:19-25`、`:33-42`），`isCompactCheckpointSource()` 是消费者谓词（`:49-51`）。

**⑤ 失败/回滚**：契约层没有运行时路径，所以没有回滚代码；它只规定失败分类（`packages/compaction/compaction/src/index.ts:35-41`）与"忙碌/取消/变更/摘要/提交/持久化"六类手动失败语义（`:142-161` 的契约注释）。回滚策略由后端承担，见下。

### 2. `packages/compaction/compaction-basic`——唯一后端

**① 压缩什么**：一段**连续表面区间**。选段算法在 `selectCompactableRange`（`packages/compaction/compaction-basic/src/region.ts:117-155`）：

- 起点 = 第一个非 `system/message` 的表面节点，`system/message` 永远不进区间（`:99-105`、`:131-132`；会话侧另有系统头保护 `packages/core/session/src/surface.ts:493-506`）；
- 从尾往前走，累计到 `retainTokens` 预算为止，预算内是**逐字保留**的近期尾部（`region.ts:133-141`）；
- 切点必须"工具配对平衡"（不能把 assistant tool-call 和它的 result 切开），不平衡就往回退（`:143-148`；平衡判定 `packages/compaction/compaction/src/tool-pairing.ts:104-126`）；
- 区间末端 = 保留尾部前一个节点（`region.ts:150-154`）。

压力阈值由路由模型容量换算：`thresholdTokens = floor(min(contextWindow × thresholdRatio, contextWindow - reservedCompletion - headroom))`（`packages/compaction/compaction-basic/src/config.ts:172-193`），默认 `thresholdRatio = 0.8`（`:20`）、`headroomTokens = 65536`（`:78`）、`retainRatio = 0.16`（`:23`）、`retainTokens < thresholdTokens` 强制（`:198-203`）。

**② 丢什么、保留什么**：

- **丢**：区间内每条事件的原文（工具输出、逐轮细节、图片）。模型看到的只有摘要——摘要输出被强制为**纯文本**，含图片直接报错 `UNSUPPORTED_CONTENT`（`packages/compaction/compaction-basic/src/summarizer.ts:213-220`）；`reasoning`/tool-call 不会进入摘要（`:163-171` 拿 `assembler.blocks()`，`:213-220` 再过滤 text）。
- **保留**：① system 头（`region.ts:99-105`）；② 预算内的近期尾部（`:133-141`）；③ 配对的工具调用（切点平衡，`:143-148`、`:349-355`）；④ **被换掉内容的账本**——`compaction/summary` 事件记录 `shadowedRange`、`shadowedSeqs`、`shadowedTokenCount`、provider/model/usage 与完整 `rawOutput`（`packages/compaction/compaction/src/types.ts:34-67`；落盘在 `region.ts:491-505`）。
- 摘要必须**更小**才允许提交：框架化后的估计 token 必须小于被遮蔽区间的路由价（`region.ts:410-422`）。
- 摘要模板要求固定八段结构（Primary Request / Key Technical Concepts / Files and Code / Errors and Fixes / Pending Jobs / Current Work / Next Step / Critical Context，`summarizer.ts:32-67`），外框为 `<compacted-summary>` 加一段"这是历史检查点"前言（`:188-194`）。

**③ 触发方式**：

- 自动（仅 `auto: true`，默认真：`packages/compaction/compaction-basic/src/config.ts:108`；注册点 `index.ts:140-141`）：
  - `agent/pre-step` 每步前算压力，超阈值就压缩，失败只 warn 不中断本轮（`index.ts:158-176`）；
  - `agent/request-error` 收到 `CONTEXT_WINDOW_EXCEEDED_CODE` 时进入溢出恢复，**绕过阈值与保留策略**（`selectCompactableRange(..., 0)`，`index.ts:294-301`），成功推进表面后返回 `{kind:'retry'}`（`:228-233`）。
- 手动：`compactNow` 在空闲会话上运行（`index.ts:383-435`，非空闲直接 `busy`：`:428-434`）；`/compact` 是它的命令外壳（`packages/compaction/command-compact/src/index.ts:67`）。
- 每次压力触发后先跑可选的 pruner，再复测，仍超阈值才摘要；摘要后仍超阈值就按 `compactionRetries` 重试（`index.ts:289-347`，`spec.compactionRetries` 默认 1：`config.ts:105`）。

**④ "被遮蔽内容仍留在会话日志"的代码实现**：这是本任务最核心的一问，答案是**两层校验 + 一次投影**：

1. 后端提交替换时，用 `surfaceOp: { op: 'replace', startSeq, endSeq }`，并把 `[startEvent.seq, summaryEvent.seq, ...shadowedSeqs]` 全部写进 `sourceEventSeqs`（`packages/compaction/compaction-basic/src/region.ts:505-509`）；
2. 会话在 append 时校验：`sourceEventSeqs` 必须**覆盖每一个被遮蔽表面节点**，否则抛 `surface replace: sourceEventSeqs must include every shadowed surface node`（`packages/core/session/src/surface.ts:330-364`，判定在 `:361-364`）；
3. 表面折叠只 splice 模型可见节点列表 `state.nodes`（`packages/core/session/src/surface.ts:563-585`，替换分支在 `:570`），而日志本身只是 `this.log.push(event)`（`packages/core/session/src/index.ts:886`）——**没有任何删除日志的路径**；
4. 同一校验还限制"改内容"的边界：`tool/result` 替换只允许改 `content`（`packages/core/session/src/surface.ts:455-485`，比对在 `:481-483`），所以被遮蔽事件的其余字段一定原样留在日志；
5. 元数据侧再留一份清单：`compaction/summary` 自述 `shadowedRange`/`shadowedSeqs`/`shadowedTokenCount`（`packages/compaction/compaction/src/types.ts:34-53`），`compaction/start` 与 `compaction/end` 成对标注 `turn`（`:24`、`:72`），失败重放可从日志重建那次事务。

结论：日志保留不是"后端自觉"，而是**会话层强制替换必须引用被遮蔽 seq**；后端少引一个 seq 就无法提交。

**⑤ 失败/回滚路径**：

- **替换前失败**（选段/摘要/稳定性）：`compaction/start` 已落盘（`region.ts:210`，它就是锁），失败时**恰好一次** `compaction/end` 带 `error`（`:240-251`）；这段历史完全没变。
- **替换后失败**（提交/持久化）：提交体与 end 事件相邻追加（`region.ts:235-239`），若提交阶段抛错，回滚不存在，只把 `stage` 记为 `commit` 并分类成 `ManualCompactionError('commit', ...)`（`:279-286`）；自动路径则 `throw failure.error` 上抛（`:262-265`）。
- **flush 失败**：表面已提交、flush 失败 → 抛 `ManualCompactionError('persistence', ...)`（`region.ts:253-272`）。
- **摘要失败**：先走 `compaction/summary-error` 瀑布（`region.ts:396-409`，注入点 `index.ts:442-448`），无人接住才报错。
- **孤儿锁**：关闭尝试失败会故意留下不配对的 start，后续所有入口报 `busy`（`region.ts:308-320`；`assertNoActiveCompaction` 在 `:327-334`）；只有更晚的 `session/end-seed` 才能把旧孤儿判定为"上一生命周期的陈旧证据"（`:312-315`）。
- **取消**：`signal` 在选段前、摘要期间、提交前后都被检查（`region.ts:182`、`:232`、`:261`），并转发进模型调用（`summarizer.ts:161`）；取消优先于错误分类（`region.ts:279-299`）。
- **无回滚，但有"已取得进展"的判定**：溢出恢复中，若表面 `replaceGeneration` 前进了（说明 pruner 或部分压缩已落盘），即使后续摘要失败也允许重试，而不是回滚（`index.ts:202-219`）。

### 3. `packages/compaction/compaction-tool-result-pruner`——无模型的工具输出裁剪

**① 压缩什么**：只压当前表面上的 `tool/result` 节点，且只压**文本中段**（`packages/compaction/compaction-tool-result-pruner/src/index.ts:136-143` 收集候选，`:83-122` 裁剪）。阈值默认 `thresholdChars = 8192`、`headChars = 4096`、`tailChars = 1024`（`packages/compaction/compaction-tool-result-pruner/src/config.ts:9-14`），base 组合显式传同一组值（`packages/bundle/base/cordis.patch.yml:425-430`）。

**② 丢什么、保留什么**：丢中段文本，插入固定标记 `\n\n[... tool result middle pruned ...]\n\n`（`config.ts:7`）；保留头 4096、尾 1024 个 Unicode 码点（按码点切，不拆代理对：`index.ts:76-122`）、非文本块及其顺序（`:93-96`）、事件其余全部字段——"每个替换保留除 `content` 外的完整事件数据"（`:124-129`），会话侧强制这一点（`packages/core/session/src/surface.ts:455-485`）。裁剪后必须更小且不超阈值，否则报错（`index.ts:116-120`）。

**③ 触发方式**：**没有自己的触发器**。它是服务 `ctx.toolResultPruner`（`index.ts:44-61`），唯一调用方是 compaction-basic：溢出路径先 prune 再无保留预算地选段（`packages/compaction/compaction-basic/src/index.ts:294-301`），压力路径在阈值合格后才 prune 并复测（`:319-327`）。仓库文档也明说"低于压力阈值绝不触碰"（`packages/compaction/compaction-basic/README.md:90`）。

**④ 日志保留实现**：每次替换是**两条相邻 append**——先 `compaction/prune` 记录被遮蔽 seq 与"影子价"（`packages/compaction/compaction-tool-result-pruner/src/index.ts:160-164`），再 `tool/result` 替换，`surfaceOp.replace` 且 `sourceEventSeqs: [原 seq]`（`:165-171`）。原 `tool/result` 事件留在日志里，替换只覆盖模型可见投影（`packages/core/session/src/surface.ts:570`）；若替换事件没有引用原 seq，会话会拒绝（`surface.ts:361-364`）。

**⑤ 失败/回滚**：**无回滚**。逐条替换各自原子提交，注释明确"本轮更早提交的替换保持持久"（`index.ts:132-134`）。配置错误在加载期就失败（`config.ts:36-64`：未知键、非正整数、`head+marker+tail > threshold` 都抛错），因此运行期没有"半配置"状态。

### 4. `packages/compaction/compaction-image-offload`——图片占位（不是压缩历史）

**① 压缩什么**：不压历史节点。它把当前请求里"最旧的 N 个输入图片出现位置"记进一个决策事件（`packages/compaction/compaction-image-offload/src/image-offload.ts:7-15`、`:16-45`；计数语义 `count` 在 `:13`、递减在 `:32-35`）。

**② 丢什么、保留什么**：丢后续请求里的图片本体（换成占位文本）；保留消息身份与块结构——投影只把选中的 image 块标 `offloaded: true`（`packages/compaction/compaction-image-offload/src/project-message.ts:13-36`，返回 `{...message, content}` 且 `deepFreeze` 在 `:35`），投影声明"消息节点与identity保持不变"（`packages/compaction/compaction-image-offload/src/projection.ts:16-27`）。占位文本由适配器渲染（DeepSeek 路由：`packages/llm/llm-deepseek/src/images.ts:43`；pi-ai 路由：`packages/llm/llm-pi-ai/src/context.ts:359`）。图片原始字节本就不在会话日志里（base 注释：`packages/bundle/base/cordis.patch.yml:143-145`），而在附件存储（`attachment-local`，`:146-147`）。

**③ 触发方式**：自动、被动——两条监听：`agent/request-error` 收到 `IMAGE_OFFLOAD_REQUIRED_CODE` 且带 `failure.offloadImages` 时落一次决策并返回 `{kind:'retry'}`（`packages/compaction/compaction-image-offload/src/index.ts:27-32`，注释说明它"不花重试预算"在 `:29`）；`compaction/summary-error` 里同样的错误也能恢复（`:33-40`）。无配置项（`:18-19` 只有 `name`/`inject`）。

**④ 日志保留实现**：`image/offload` 被声明为**消息投影事件**（`projection.ts:16-27`），投影在读取时才展开（`:40-73`），原始 `user/message` / `tool/result` 事件因此原样留在日志；投影还会校验目标必须是当前表面节点（`:56`）、必须是非 assistant 输入节点（`:58-60`）、索引严格递增（`:61-67`）。`offloadOldestImages` 只做一次 `session.append('image/offload', { targets })`（`image-offload.ts:44`）。

**⑤ 失败/回滚**：没有可选空间时返回 `false`，监听器 `next()` 把原错误交回（`index.ts:30`、`:38`），即"决策没写成 = 什么都没发生"。代码里**没有 try/catch**（`index.ts:27-40`），append 校验失败会沿 `agent/request-error` 瀑布上抛，不会伪造重试；决策一旦落盘也不会撤销（下一次请求继续按投影发占位文本）。

### 5. `packages/compaction/command-compact`——`/compact` 命令壳

**① 压缩什么**：自己不压，纯委托：`ctx.compaction.compactNow(invocation.agent, invocation.signal, invocation.commandId)`（`packages/compaction/command-compact/src/index.ts:67`）。

**② 丢什么、保留什么**：不适用；成功结果只报"压缩了多少条 + 估算 token"，并带 `sourceEventSeq: result.summarySeq`（`index.ts:69-73`）。命令生命周期是 log-only（`packages/interaction/commands/src/types.ts:105-112`，追加在 `packages/interaction/commands/src/index.ts:373-382`）。

**③ 触发方式**：唯一人工 `/compact`，无参数（多余参数回 `Usage: /compact (no arguments)`，`index.ts:63-65`）；注册在 `apply()` 里（`:101-107`）。空闲/忙碌由后端裁决（`compaction-basic` 的 `runMaintenance` + `busy`，`packages/compaction/compaction-basic/src/index.ts:390`、`:428-434`）。

**④ 日志保留实现**：它不产生任何遮蔽。`command/run` / `command/done` 是 log-only 事件（`packages/interaction/commands/src/types.ts:105-112`），不在 `SurfaceEventType` 封闭联合里（`packages/core/session/src/types.ts:440-448`），若误带 `surfaceOp` 会被会话拒绝（`packages/core/session/src/surface.ts:302-313`）。真正的替换与引用校验仍由后端完成。

**⑤ 失败/回滚**：把六类预期失败映射成稳定文案（`index.ts:24-56`）；取消优先（`:75`）；未分类异常重新抛出而不是吞掉（`:77`）。它自身没有副作用，因此无需回滚。

---

## base 插件清单统计

### 统计口径与文件形态

- 文件 **529 行**（`wc -l`，与实测一致）；结构是**一个顶层 `- insert:`**（`packages/bundle/base/cordis.patch.yml:15`），96 个插件行全是 4 空格缩进的 `    - id: <别名>`。
- 96 行 = 96 个 `name:`（每个插件行恰好一个包名），其中 33 行带 `config:`。
- 行序无加载语义、分组只为读者：`packages/bundle/base/cordis.patch.yml:12-13`（"Row order carries no load semantics … the grouping is for readers"）。所以下面的"分组"是**读者视角的职责标注**，不是仓库元数据。

### 按职责分组（13 组，共 96 条）

> 分组规则：按插件在主链路中的职责归并（一行只归一组，合计必须等于 96）；组名是我的标注，依据 `cordis.patch.yml:12-13` 的"分组给读者"。

| 组（职责标注） | 条目数 | 条目（`行号:id`，按文件出现顺序） |
|---|---|---|
| G1 内核骨架与装配 | 11 | `16:tool-plugin-manager`、`20:plugin-manager`、`24:timer`、`28:hmr`、`82:agent`、`85:plugin-package-inventory-deepseek`、`105:config-editor`、`109:settings`、`499:tools`、`504:system-prompt`、`511:agent-loop` |
| G2 类型协议与 API 网关 | 4 | `46:typert`、`49:typert-loader`、`52:typert-gateway`、`57:remote-access` |
| G3 LLM 路由与计量 | 8 | `34:llm`、`37:deepseek-llm-api-extensions`、`90:agent-default-model`、`99:llm-retry`、`135:llm-pi-ai`、`348:token-meter`、`525:llm-deepseek`、`528:llm-deepseek-account` |
| G4 凭据与账户 | 3 | `117:authorization`、`120:deepseek-account`、`125:credentials` |
| G5 会话、存储与持久化 | 14 | `40:session`、`43:session-log-deepseek`、`60:session-title`、`67:session-title-llm`、`138:session-persistence-jsonl`、`146:attachment-local`、`157:session-query-sqlite`、`166:working-directory`、`172:session-projection`、`179:storage`、`182:storage-json`、`187:storage-domain`、`196:session-projection-cache`、`420:session-checkpoint-policy` |
| G6 遥测 | 2 | `202:otel`、`218:session-telemetry-otel` |
| G7 执行边界：子进程 / 沙箱 / 权限 / Shell 环境 | 11 | `96:jobs`、`234:subprocess`、`240:sandbox`、`243:sandbox-policy`、`249:bash-sandbox`、`255:pwsh-sandbox`、`259:approval`、`264:permission`、`278:shell-env`、`292:fs-observation-policy`、`518:fs-sandbox` |
| G8 文件与 Shell 工具 | 6 | `169:tool-working-directory`、`281:tool-bash`、`285:tool-pwsh`、`289:tool-jobs`、`295:tool-fs`、`298:tool-fs-search` |
| G9 技能、指令与 MCP | 5 | `303:agent-instructions`、`308:skill`、`311:skill-filesystem`、`314:tool-skill`、`492:mcp-resources` |
| G10 交互、命令、计划与目标 | 9 | `79:user-questions`、`317:commands`、`320:command-feedback`、`323:goal`、`326:goal-round-driver`、`329:command-goal`、`332:plan-mode`、`437:tool-todo`、`444:tool-goal` |
| G11 上下文治理与压缩 | 8 | `351:compaction-basic`、`356:command-compact`、`408:timeout-policy`、`411:spill-local`、`414:spill-policy`、`425:tool-result-pruner`、`434:image-offload`、`448:repeat-tool-reminder` |
| G12 子代理与工作流 | 10 | `359:subagent`、`362:subagent-spawn-in-process`、`367:subagent-fork-in-process`、`374:tool-subagent-control`、`377:tool-subagent-list-agents`、`380:tool-subagent`、`391:tool-subagent-fork`、`397:ptc-runtime`、`400:workflow-ptc`、`405:tool-workflow` |
| G13 Web 检索 | 5 | `467:web`、`473:web-search-deepseek`、`478:web-deepseek-api`、`483:web-fetch-http`、`486:tool-web` |
| **合计** | **96** | 11+4+8+3+14+2+11+6+5+9+8+10+5 = 96 |

### 必挂 vs 条件挂载

| 分类 | 判定条件 | 条数 | 行号 |
|---|---|---|---|
| **必挂** | 该行没有 `disabled:` 字段 | **87** | 见下方全量清单中标"必挂"者 |
| **默认关** | `disabled: true`（无 `!!js`） | **1** | `tool-plugin-manager`（`:16-18`） |
| **条件挂载** | `disabled: !!js <表达式>` | **8** | ① `profileContext` 四行：`:20`（plugin-manager）、`:28`（hmr）、`:105`（config-editor）、`:109`（settings）；② 平台对子四行：`:249`（bash-sandbox）、`:255`（pwsh-sandbox）、`:281`（tool-bash）、`:285`（tool-pwsh） |
| **合计** | | **96** | 与 `grep -c '^    - id:'` 一致 |

补充事实：

- 没有 `disabled: false` 行；`disabled:` 共 **9 处** = 1（true）+ 8（`!!js`）。
- 平台对子成对互斥：`tool-bash` 在 win32 关、`tool-pwsh` 在非 win32 关（`cordis.patch.yml:281-287`），两对 Shell 行合计 4 条条件挂载。
- `profileContext` 四行决定"profile 编辑器/HMR/settings"这层是否存在（`:20-30`、`:105-111`）。

### 怎么数的（可复跑的三种方法）

**方法 A：行级正则（grep，最小假设）**

```bash
cd packages/bundle/base
grep -c '^    - id: ' cordis.patch.yml        # 96  ← 插件行总数
grep -c '^      name: ' cordis.patch.yml      # 96  ← 独立佐证：每行恰好一个包名
grep -c 'disabled: true' cordis.patch.yml     # 1   ← 默认关
grep -c 'disabled: !!js' cordis.patch.yml     # 8   ← 条件挂载
grep -c '!!js' cordis.patch.yml               # 16  ← 陷阱：含 config 值
```

**方法 B：awk 状态机（按"行块"分类，不依赖字段顺序）**

```bash
cd packages/bundle/base
awk '
/^    - id: /            { if(row!=""){count[row]++}; row="required"; next }
/^      disabled: true/ { row="disabled-true"; next }
/^      disabled: !!js/ { row="disabled-js"; next }
END                     { if(row!=""){count[row]++}; for(k in count) print k, count[k] }
' cordis.patch.yml
# 输出：required 87 / disabled-true 1 / disabled-js 8
awk '/^    - id: /{n++} END{print n}' cordis.patch.yml   # 96
```

**方法 C：YAML 结构解析（第三方独立口径）**

用带 `!!js` 自定义构造器的 PyYAML 把文件真正解析成对象，再对 `doc[0].insert` 逐项判 `disabled` 的类型（`None` / `bool true` / `!!js` 标量）：

```text
rows 96 / unique ids 96 / required 87 / disabled-js 8 / disabled-true 1
rows with config 33 / row keys ['config','disabled','id','name']
```

**三种方法结论一致：96 条 = 87 必挂 + 1 默认关 + 8 条件挂载**，因此不需要"以原始行号清单为准"的仲裁；为可复核仍把全量清单贴在下一节。两处容易数错的地方：① `- id:` 在文件里全是 4 空格缩进（无嵌套行），所以 `grep -c -- '- id:'`=96 与 `grep -c '^    - id: '`=96 相同；② `!!js` 共 16 次但只有 8 次是 `disabled:` 行，另 8 次是 config 表达式（见下表）。

### `config` 里出现 `!!js` 的 6 行（**不是**挂载条件）

| 行号 | 插件 | 用在哪 | 表达式用途 |
|---|---|---|---|
| `:123` | `deepseek-account` | `config.desktopPlatform` | 桌面平台判定（`profileContext?.name === 'desktop'` 且 darwin/win32） |
| `:141` | `session-persistence-jsonl` | `config.root` | `dshHomePath('sessions')` |
| `:185` | `storage-json` | `config.root` | `dshHomePath('storages')` |
| `:221` / `:225` | `session-telemetry-otel` | `config.mode` / `config.exporter.url` | 环境变量默认值（`DSH_TELEMETRY_MODE` / `DSH_TELEMETRY_OTLP_URL`） |
| `:246` / `:247` | `sandbox-policy` | `config.mode` / `config.workspaceRoot` | `DSH_PERMISSION_MODE` 默认 `workspace-write` / `process.cwd()` |
| `:262` | `approval` | `config.policy` | `danger-full-access` 时把审批设为 `never`，否则 `ask` |

结论：若把"含 `!!js` 的行"当条件挂载，会得到 14 条，与真实的 8 条差 6——这 6 行插件的挂载状态是**必挂**。

### 全量行号清单（96 条，原始行号为准）

| # | 行号 | id | 包名 | 挂载状态 |
|---|---|---|---|---|
| 1 | 16 | `tool-plugin-manager` | `@deepseek-ai/dsh-plugin-manager/tools` | 默认关（`disabled: true`） |
| 2 | 20 | `plugin-manager` | `@deepseek-ai/dsh-plugin-manager` | 条件（`disabled: !!js`） |
| 3 | 24 | `timer` | `@deepseek-ai/cordis-plugin-timer` | 必挂 |
| 4 | 28 | `hmr` | `@deepseek-ai/dsh-hmr` | 条件（`disabled: !!js`） |
| 5 | 34 | `llm` | `@deepseek-ai/dsh-llm` | 必挂 |
| 6 | 37 | `deepseek-llm-api-extensions` | `@deepseek-ai/dsh-deepseek-llm-api-extensions` | 必挂 |
| 7 | 40 | `session` | `@deepseek-ai/dsh-session` | 必挂 |
| 8 | 43 | `session-log-deepseek` | `@deepseek-ai/dsh-session-log-deepseek` | 必挂 |
| 9 | 46 | `typert` | `@deepseek-ai/dsh-typert-registry` | 必挂 |
| 10 | 49 | `typert-loader` | `@deepseek-ai/dsh-typert-loader` | 必挂 |
| 11 | 52 | `typert-gateway` | `@deepseek-ai/dsh-api-gateway` | 必挂 |
| 12 | 57 | `remote-access` | `@deepseek-ai/dsh-api-remote-access` | 必挂 |
| 13 | 60 | `session-title` | `@deepseek-ai/dsh-session-title` | 必挂 |
| 14 | 67 | `session-title-llm` | `@deepseek-ai/dsh-session-title-first-prompt-llm` | 必挂 |
| 15 | 79 | `user-questions` | `@deepseek-ai/dsh-user-questions` | 必挂 |
| 16 | 82 | `agent` | `@deepseek-ai/dsh-agent` | 必挂 |
| 17 | 85 | `plugin-package-inventory-deepseek` | `@deepseek-ai/dsh-plugin-package-inventory-deepseek` | 必挂 |
| 18 | 90 | `agent-default-model` | `@deepseek-ai/dsh-agent-default-model` | 必挂 |
| 19 | 96 | `jobs` | `@deepseek-ai/dsh-jobs-local` | 必挂 |
| 20 | 99 | `llm-retry` | `@deepseek-ai/dsh-llm-retry` | 必挂 |
| 21 | 105 | `config-editor` | `@deepseek-ai/dsh-config-editor` | 条件（`disabled: !!js`） |
| 22 | 109 | `settings` | `@deepseek-ai/dsh-settings` | 条件（`disabled: !!js`） |
| 23 | 117 | `authorization` | `@deepseek-ai/dsh-authorization` | 必挂 |
| 24 | 120 | `deepseek-account` | `@deepseek-ai/dsh-deepseek-account-platform` | 必挂 |
| 25 | 125 | `credentials` | `@deepseek-ai/dsh-credentials-local` | 必挂 |
| 26 | 135 | `llm-pi-ai` | `@deepseek-ai/dsh-llm-pi-ai` | 必挂 |
| 27 | 138 | `session-persistence-jsonl` | `@deepseek-ai/dsh-session-persistence-jsonl` | 必挂 |
| 28 | 146 | `attachment-local` | `@deepseek-ai/dsh-attachment-local` | 必挂 |
| 29 | 157 | `session-query-sqlite` | `@deepseek-ai/dsh-session-query-sqlite` | 必挂 |
| 30 | 166 | `working-directory` | `@deepseek-ai/dsh-working-directory` | 必挂 |
| 31 | 169 | `tool-working-directory` | `@deepseek-ai/dsh-tool-working-directory` | 必挂 |
| 32 | 172 | `session-projection` | `@deepseek-ai/dsh-session-projection` | 必挂 |
| 33 | 179 | `storage` | `@deepseek-ai/dsh-storage` | 必挂 |
| 34 | 182 | `storage-json` | `@deepseek-ai/dsh-storage-json` | 必挂 |
| 35 | 187 | `storage-domain` | `@deepseek-ai/dsh-storage-domain` | 必挂 |
| 36 | 196 | `session-projection-cache` | `@deepseek-ai/dsh-session-projection-cache` | 必挂 |
| 37 | 202 | `otel` | `@deepseek-ai/dsh-otel` | 必挂 |
| 38 | 218 | `session-telemetry-otel` | `@deepseek-ai/dsh-session-telemetry-otel` | 必挂 |
| 39 | 234 | `subprocess` | `@deepseek-ai/dsh-subprocess-local` | 必挂 |
| 40 | 240 | `sandbox` | `@deepseek-ai/dsh-sandbox-local` | 必挂 |
| 41 | 243 | `sandbox-policy` | `@deepseek-ai/dsh-sandbox-policy` | 必挂 |
| 42 | 249 | `bash-sandbox` | `@deepseek-ai/dsh-bash-sandbox` | 条件（`disabled: !!js`） |
| 43 | 255 | `pwsh-sandbox` | `@deepseek-ai/dsh-pwsh-sandbox` | 条件（`disabled: !!js`） |
| 44 | 259 | `approval` | `@deepseek-ai/dsh-user-approval` | 必挂 |
| 45 | 264 | `permission` | `@deepseek-ai/dsh-permission-presets` | 必挂 |
| 46 | 278 | `shell-env` | `@deepseek-ai/dsh-shell-env` | 必挂 |
| 47 | 281 | `tool-bash` | `@deepseek-ai/dsh-tool-bash` | 条件（`disabled: !!js`） |
| 48 | 285 | `tool-pwsh` | `@deepseek-ai/dsh-tool-pwsh` | 条件（`disabled: !!js`） |
| 49 | 289 | `tool-jobs` | `@deepseek-ai/dsh-tool-jobs` | 必挂 |
| 50 | 292 | `fs-observation-policy` | `@deepseek-ai/dsh-fs-observation-policy` | 必挂 |
| 51 | 295 | `tool-fs` | `@deepseek-ai/dsh-tool-fs` | 必挂 |
| 52 | 298 | `tool-fs-search` | `@deepseek-ai/dsh-tool-fs-search` | 必挂 |
| 53 | 303 | `agent-instructions` | `@deepseek-ai/dsh-agent-instructions` | 必挂 |
| 54 | 308 | `skill` | `@deepseek-ai/dsh-skill` | 必挂 |
| 55 | 311 | `skill-filesystem` | `@deepseek-ai/dsh-skill-filesystem` | 必挂 |
| 56 | 314 | `tool-skill` | `@deepseek-ai/dsh-tool-skill` | 必挂 |
| 57 | 317 | `commands` | `@deepseek-ai/dsh-commands` | 必挂 |
| 58 | 320 | `command-feedback` | `@deepseek-ai/dsh-command-feedback` | 必挂 |
| 59 | 323 | `goal` | `@deepseek-ai/dsh-goal` | 必挂 |
| 60 | 326 | `goal-round-driver` | `@deepseek-ai/dsh-goal-round-driver` | 必挂 |
| 61 | 329 | `command-goal` | `@deepseek-ai/dsh-command-goal` | 必挂 |
| 62 | 332 | `plan-mode` | `@deepseek-ai/dsh-plan-mode` | 必挂 |
| 63 | 348 | `token-meter` | `@deepseek-ai/dsh-token-meter` | 必挂 |
| 64 | 351 | `compaction-basic` | `@deepseek-ai/dsh-compaction-basic` | 必挂 |
| 65 | 356 | `command-compact` | `@deepseek-ai/dsh-command-compact` | 必挂 |
| 66 | 359 | `subagent` | `@deepseek-ai/dsh-subagent` | 必挂 |
| 67 | 362 | `subagent-spawn-in-process` | `@deepseek-ai/dsh-subagent-spawn-in-process` | 必挂 |
| 68 | 367 | `subagent-fork-in-process` | `@deepseek-ai/dsh-subagent-fork-in-process` | 必挂 |
| 69 | 374 | `tool-subagent-control` | `@deepseek-ai/dsh-tool-subagent-control` | 必挂 |
| 70 | 377 | `tool-subagent-list-agents` | `@deepseek-ai/dsh-tool-subagent-control/list-agents` | 必挂 |
| 71 | 380 | `tool-subagent` | `@deepseek-ai/dsh-tool-subagent` | 必挂 |
| 72 | 391 | `tool-subagent-fork` | `@deepseek-ai/dsh-tool-subagent` | 必挂 |
| 73 | 397 | `ptc-runtime` | `@deepseek-ai/dsh-ptc-runtime-node` | 必挂 |
| 74 | 400 | `workflow-ptc` | `@deepseek-ai/dsh-workflow-ptc` | 必挂 |
| 75 | 405 | `tool-workflow` | `@deepseek-ai/dsh-tool-workflow` | 必挂 |
| 76 | 408 | `timeout-policy` | `@deepseek-ai/dsh-tool-call-timeout-policy` | 必挂 |
| 77 | 411 | `spill-local` | `@deepseek-ai/dsh-spill-local` | 必挂 |
| 78 | 414 | `spill-policy` | `@deepseek-ai/dsh-spill-policy` | 必挂 |
| 79 | 420 | `session-checkpoint-policy` | `@deepseek-ai/dsh-session-checkpoint-policy` | 必挂 |
| 80 | 425 | `tool-result-pruner` | `@deepseek-ai/dsh-compaction-tool-result-pruner` | 必挂 |
| 81 | 434 | `image-offload` | `@deepseek-ai/dsh-compaction-image-offload` | 必挂 |
| 82 | 437 | `tool-todo` | `@deepseek-ai/dsh-tool-todo` | 必挂 |
| 83 | 444 | `tool-goal` | `@deepseek-ai/dsh-tool-goal` | 必挂 |
| 84 | 448 | `repeat-tool-reminder` | `@deepseek-ai/dsh-repeat-tool-reminder` | 必挂 |
| 85 | 467 | `web` | `@deepseek-ai/dsh-web` | 必挂 |
| 86 | 473 | `web-search-deepseek` | `@deepseek-ai/dsh-web-search-deepseek` | 必挂 |
| 87 | 478 | `web-deepseek-api` | `@deepseek-ai/dsh-web-deepseek-api` | 必挂 |
| 88 | 483 | `web-fetch-http` | `@deepseek-ai/dsh-web-fetch-http` | 必挂 |
| 89 | 486 | `tool-web` | `@deepseek-ai/dsh-tool-web` | 必挂 |
| 90 | 492 | `mcp-resources` | `@deepseek-ai/dsh-mcp-resources` | 必挂 |
| 91 | 499 | `tools` | `@deepseek-ai/dsh-tools` | 必挂 |
| 92 | 504 | `system-prompt` | `@deepseek-ai/dsh-system-prompt` | 必挂 |
| 93 | 511 | `agent-loop` | `@deepseek-ai/dsh-agent-loop` | 必挂 |
| 94 | 518 | `fs-sandbox` | `@deepseek-ai/dsh-fs-sandbox` | 必挂 |
| 95 | 525 | `llm-deepseek` | `@deepseek-ai/dsh-llm-deepseek-api-key` | 必挂 |
| 96 | 528 | `llm-deepseek-account` | `@deepseek-ai/dsh-llm-deepseek-account` | 必挂 |

### 边界：base 层的"必挂"≠ 全局必挂

- 组合机制是按 id 的 patch 覆盖、最后一层赢（`packages/bundle/base/cordis.patch.yml:1-10`）；"必挂"只表示**这一层没有 disable**。
- 上层 overlay 可关：`packages/bundle/web-app/cordis.patch.yml:539-546` 在主机面把 `compaction-basic`、`command-compact`、`tool-result-pruner` 设为 `disabled: true`（交给 preset 层）；`packages/bundle/sdk-minimal/cordis.patch.yml:64-68` 是另一套独立清单，直接挂 `compaction-basic` 与 `image-offload`。
- 行存在也不等于注册成功：激活由"服务可用性"驱动（`packages/bundle/base/cordis.patch.yml:12-13`）。

---

## 证据索引（结论 ↔ 文件:行）

| # | 断言 | 证据（`文件:行`） |
|---|---|---|
| A1 | 契约定义三抽象操作，唯一实现是 compaction-basic | `packages/compaction/compaction/src/index.ts:119-122`、`:136-140`、`:162-166`、`:187-192`；`packages/compaction/compaction-basic/src/index.ts:113` |
| A2 | 只有 compaction-basic 替换历史区间（其余是服务/命令/投影） | `packages/compaction/compaction-basic/src/region.ts:505-509`；`packages/compaction/compaction-tool-result-pruner/src/index.ts:44`；`packages/compaction/compaction-image-offload/src/index.ts:25-40`；`packages/compaction/command-compact/src/index.ts:67` |
| A3 | 选段：非 system 起、保留近期尾部、平衡切点 | `packages/compaction/compaction-basic/src/region.ts:117-155`；`packages/compaction/compaction/src/tool-pairing.ts:104-126` |
| A4 | 阈值公式与默认值（0.8 / 65536 / 0.16） | `packages/compaction/compaction-basic/src/config.ts:20`、`:23`、`:78`、`:172-203` |
| A5 | 摘要文本-only、图片输出报错、八段模板 | `packages/compaction/compaction-basic/src/summarizer.ts:32-67`、`:188-194`、`:213-220` |
| A6 | 摘要必须比被遮蔽区间小 | `packages/compaction/compaction-basic/src/region.ts:410-422` |
| A7 | 自动触发：pre-step 压力 + request-error 溢出（溢出绕过保留策略） | `packages/compaction/compaction-basic/src/index.ts:158-176`、`:190-234`、`:299` |
| A8 | 手动触发：compactNow 仅空闲；`/compact` 委托 | `packages/compaction/compaction-basic/src/index.ts:383-435`；`packages/compaction/command-compact/src/index.ts:63-73` |
| A9 | **日志保留保证**：替换必须列出每个被遮蔽 seq，否则 append 拒绝 | `packages/core/session/src/surface.ts:330-364`（判定 `:361-364`） |
| A10 | 日志只 push、替换只改投影 `nodes` | `packages/core/session/src/index.ts:886`；`packages/core/session/src/surface.ts:563-585`（`:570`） |
| A11 | 压缩替换带的 `surfaceOp` 与 `sourceEventSeqs` | `packages/compaction/compaction-basic/src/region.ts:505-509` |
| A12 | `compaction/*` 是 log-only，禁止 surfaceOp | `packages/compaction/compaction/src/types.ts:19-33`、`:68-72`、`:73-89`；`packages/core/session/src/surface.ts:302-313`；`packages/core/session/src/types.ts:440-448` |
| A13 | checkpoint 标记（跨后端可识别） | `packages/compaction/compaction/src/checkpoint.ts:19-25`、`:33-42`、`:49-51` |
| A14 | 失败只做一次 end 尝试、孤儿 start 即锁 | `packages/compaction/compaction-basic/src/region.ts:210`、`:237`、`:240-251`、`:308-334` |
| A15 | flush 失败→`persistence`；提交失败→`commit`；摘要失败→`summary`/`changed` | `packages/compaction/compaction-basic/src/region.ts:253-299` |
| A16 | 取消信号贯穿选段/摘要/提交 | `packages/compaction/compaction-basic/src/region.ts:182`、`:232`、`:261`；`summarizer.ts:161` |
| A17 | pruner 的阈值/头尾默认值，base 显式同值 | `packages/compaction/compaction-tool-result-pruner/src/config.ts:7`、`:9-14`；`packages/bundle/base/cordis.patch.yml:425-430` |
| A18 | pruner 只改单条 tool/result 内容，先影子价事件后替换 | `packages/compaction/compaction-tool-result-pruner/src/index.ts:83-122`、`:160-171`；`packages/core/session/src/surface.ts:455-485` |
| A19 | pruner 无回滚、已提交替换保持持久 | `packages/compaction/compaction-tool-result-pruner/src/index.ts:132-134` |
| A20 | image-offload 是消息投影，原事件不动；占位由适配器渲染 | `packages/compaction/compaction-image-offload/src/projection.ts:16-27`、`:40-73`；`project-message.ts:13-36`；`packages/llm/llm-deepseek/src/images.ts:43` |
| A21 | image-offload 触发两条监听、失败即 `next()` 无回滚 | `packages/compaction/compaction-image-offload/src/index.ts:27-40`；`image-offload.ts:16-45` |
| A22 | 命令生命周期 log-only，替换校验仍由后端完成 | `packages/interaction/commands/src/types.ts:105-112`；`packages/interaction/commands/src/index.ts:373-382`；`packages/compaction/command-compact/src/index.ts:24-56`、`:67-77` |
| B1 | base 是单一 insert、96 行插件行、33 行带 config | `packages/bundle/base/cordis.patch.yml:15`、`:15-529`（`grep`/`awk`/PyYAML 三法一致） |
| B2 | 分组只为读者、行序无加载语义 | `packages/bundle/base/cordis.patch.yml:12-13` |
| B3 | 必挂 87 / 默认关 1 / 条件 8（profileContext 4 + 平台对子 4） | `packages/bundle/base/cordis.patch.yml:16-18`、`:20-22`、`:28-32`、`:105-111`、`:249-257`、`:281-287` |
| B4 | `!!js` 共 16 处但只有 8 处是挂载条件；其余 8 处在 config | `packages/bundle/base/cordis.patch.yml:123`、`:141`、`:185`、`:221`、`:225`、`:246-247`、`:262` |
| B5 | base "必挂"可被上层 overlay 关掉 | `packages/bundle/web-app/cordis.patch.yml:539-546`；`packages/bundle/sdk-minimal/cordis.patch.yml:64-68` |
| B6 | 版本依据是 package.json（快照无 git 元数据） | `package.json:3` |

---

## 未能确证

1. **运行时行为全部未实测**。快照只读、未装依赖、未跑 App、无模型密钥；阈值触发、重试、溢出恢复、取消时序都是**代码静态推断**（clamp/分支已核，但没有端到端观测）。
2. **分组是作者职责标注，不是仓库元数据**。仓库只声明"分组给读者"（`packages/bundle/base/cordis.patch.yml:12-13`）；换个人分组名/边界会不同，但 96 总数与 87/1/8 分类不受影响。分组计数依赖我手写的 id→组映射（另用脚本断言"96 条全覆盖、无重复"）。
3. **"必挂"只相对 base 这一层**：`packages/bundle/web-app/cordis.patch.yml:539-546` 已把 3 条压缩相关行在主机面关掉；更上层的 profile/用户 patch 同样能改。行存在也不代表运行时注册成功（激活靠服务可用性，`cordis.patch.yml:12-13`）。
4. **`compaction/summary-error` 的其它监听者不可穷举**：本仓只搜到 `packages/compaction/compaction-image-offload/src/index.ts:33` 与注入点 `packages/compaction/compaction-basic/src/index.ts:442`，但仓外插件也能注册该瀑布。
5. **会话日志的落盘完整性只核到序列化与计数校验**：JSONL 侧按事件逐行序列化（`packages/session/session-persistence-jsonl/src/format.ts:313-315`），generation 校验比对事件条数（`packages/session/session-persistence-jsonl/src/generation.ts:532-534`）；没有对真实 `.jsonl` 文件做字节级复核。
6. **图片占位文本只核了两条路由**：DeepSeek（`packages/llm/llm-deepseek/src/images.ts:43`）与 pi-ai（`packages/llm/llm-pi-ai/src/context.ts:359`）；其它适配器是否都实现 `offloadedImageText` 投影未逐个核。
7. **pruner 与压缩的交互顺序已读未跑**：压力路径"先 prune、复测、再摘要"（`packages/compaction/compaction-basic/src/index.ts:319-341`）与溢出路径"先 prune、无保留预算选段"（`:294-301`）是代码事实，但没有测试执行记录。
