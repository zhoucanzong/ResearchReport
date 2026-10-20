# DSH `api/gateway` 与"事件→客户端"投影（深读第六步）

> **对象**：`/tmp/dsh-src`（`deepseek-harness` `master`，`@deepseek-ai/dsh-root` **0.2.1-rc.2**），全程只读。
> **方法**：`code-researcher` deep 模式的"运行路径 + 设计追问"，结论一律带 `文件:行`；否定性结论按 `docs/verification.md §5.7` 三要素（搜索面/方法/结果）写。
> **本文回答四问**：①事件如何投影到客户端；②审批卡如何被投影、为何天然会话级；③是否存在跨会话汇总出口；④`Orchestrator run is unavailable` 这类不可用如何表达。

---

## 1. 结论摘要（5 条）

1. **投影是"白名单 + 单一声明"**：Host 只转发 `API_REMOTE_FORWARDED_EVENTS` 里的 26 个事件，声明集中在 `packages/api/remotes/src/remote-events.ts:26-55`。
2. **审批走 waterfall 事件**：`{ event: 'approval/request', mode: 'waterfall' }`（同文件 `:28`），与 `user-questions/request`（`:54`）同一类——**一问一答的交互式事件**，不是广播。
3. **会话级是结构性设计**：会话集合事件显式带 `resources: { session: … }`（`:29-34`），事件是**资源受限**的；审批事件虽未声明资源，但客户端把它归到**发起它的会话**的待处理交互上（`ui-session` 的 `PendingSessionInteractionMap`）。
4. **没有"全局审批汇总"出口**：白名单里**没有**任何聚合审批/任务的事件；集合类变化按文档说明走 **follow streams**，而不是一次性广播（`:20-24` 注释）。
5. **`Orchestrator run is unavailable` 不在本仓库**：`grep -rn "Orchestrator run"` **0 命中**；该文案来自闭源 Bot Harness 编排层。仓库内可见的相关事件是 `api-session/error`（`:32`）与 `cordis/request-run`（`:39`）。

---

## 2. 机制：从 Host 事件到客户端

| 环节 | 位置 | 说明 |
|---|---|---|
| **Host 侧 RPC 入口** | `packages/api/gateway/README.zh.md` 概述 | `ctx.typertGateway`（Host）与 `ctx.remote`（Client）共用一份生成式 `InvocationDescriptor`；Connection 负责一元调用的请求关联，Gateway 拥有多路复用的 Remote 流 |
| **转发白名单（唯一真源）** | `packages/api/remotes/src/remote-events.ts:26-55` | 注释即契约：*"The one home of this application's forwarded-Host-event allowlist"*（`:1-6`）|
| **模式语义** | 同上 `:20-24` | `emit` 条目声明其 payload 携带的资源（或 global）；**只有访问控制允许时才到达非属主 Peer**；集合变化走 follow streams |
| **waterfall 模式** | 同文件 `:28`、`:54` | 交互式请求（审批 / 用户提问）：需要应答者参与，因此走 waterfall 而非 emit |
| **类型投影** | `packages/api/remotes/src/types.ts:15` | `ApiRemoteForwardedEvent = typeof API_REMOTE_FORWARDED_EVENTS[number]['event']` —— 白名单既是运行时列表，也是客户端 `$on` 的合法键集 |

> **能读出的一件事**：客户端能"看到什么"是由**这个数组**定义的，不是由 UI 组件定义。要新增一种可见事件，改这里；UI 只是消费方。

---

## 3. 审批卡为什么天然是"会话级"（代码事实）

| 事实 | 证据 |
|---|---|
| 审批以 `approval/request` 事件转发，模式为 `waterfall` | `packages/api/remotes/src/remote-events.ts:28` |
| 该事件与会话相关的生命周期事件并列在同一声明里；会话类事件带 `resources: { session }` | 同文件 `:29-34` |
| 客户端把待处理审批映射为会话的状态字段 `pendingInteraction: SessionPendingInteraction \| undefined` | `packages/client/ui-session/src/client/index.ts:64` |
| 会话列表行取该字段（`this.pendingSnapshot.get(id)`），变化检测也基于它 | 同文件 `:538`、`:706` |
| 审批详情插槽的作用域写作 `scope: 'session'` | `packages/client/ui-approval/src/client/contract/slots.ts:36-39` |

**推论（研究推断）**：审批的"会话级"不是 UI 偶然，而是**三层叠加**：事件以 waterfall 交互形式下发（要求应答者）、客户端以会话 id 索引待处理交互、插槽作用域显式声明 session。**因此"后台会话的审批无人可见"是这套设计的必然结果**——不是渲染 bug，而是缺少一个"面向跨会话"的出口。

---

## 4. 有没有跨会话汇总出口？（否定性结论，按三要素写）

**结论**：在**这个白名单**里**没有**跨会话的审批/待办汇总事件。

| 要素 | 内容 |
|---|---|
| **搜索面** | `packages/api/remotes/src/remote-events.ts`（唯一的转发白名单文件）|
| **方法** | 逐条读 26 个条目的 `event` 名与 `mode`；并 `grep -rn "approval" packages/api/remotes/src/remote-events.ts` 确认只有 `approval/request` 一条 |
| **结果** | 26 条中与审批相关仅 `approval/request`（`:28`）；与会话集合相关的是 `api-session/{added,removed,status,activity,error}`（`:29-34`），均为**单会话资源**事件；**没有任何** `approvals/*` 聚合事件或全局待办流 |
| **结论边界** | 这证明的是"**该应用的转发白名单里没有跨会话审批汇总**"；如果闭源层另有推送通道（如 Bot Harness 自建），本仓库看不到 |

---

## 5. `Orchestrator run is unavailable` 在哪一层？

| 事实 | 证据 |
|---|---|
| 仓库中 **`Orchestrator run` 0 命中** | `grep -rn "Orchestrator run" packages apps --include="*.ts"` |
| 仓库中 **`orchestrator run` 0 命中** | 同上（大小写不敏感）|
| 可见的相关事件 | `api-session/error`（`remote-events.ts:32`）、`cordis/request-run` 与 `cordis/request-run-resolved`（`:39-40`）|

**推论**：该错误文案来自**闭源 Bot Harness 编排层**，不在开源仓库；开源层能表达"会话出错"（`api-session/error`）与"Cordis 运行请求"（`cordis/request-run`），但**没有**"编排不可用"的专用事件。所以那类故障在开源侧表现为**普通的工具错误字符串**，人类侧无法据此区分"工具失败"与"编排挂掉"——这也是我们建议 DSH 加**主动通知 + 健康状态位**的原因（见 `docs/harness-feedback.md` 第 6 条）。

---

## 5.5 为什么"加个全局审批入口"不是改 UI，而是改协议

**先看现有约束（代码事实）**

| 约束 | 证据 |
|---|---|
| 转发事件必须由"唯一事件源"注册（`registerRemoteEvents()`），`$events` 是 Gateway 自有的内部 endpoint | `packages/api/gateway/README.zh.md`（"Host 服务"一节）|
| 客户端要收转发事件，`peer.interactions` 必须为 `'answer'` | `packages/api/gateway/src/index.ts:1226-1229`（否则 `gateway/interactions-forbidden`，错误文案：*"forwarded Remote events require interactions=answer"*）|
| **waterfall（审批/提问）是 Agent 作用域的**：帧里带 `agentId`，并有配对取消帧 | `packages/api/gateway/src/stream-protocol.ts:51-59`、`:60-62` |
| waterfall 需要"有人应答"：Gateway 分配传输 id，并在 Client 返回结果或显式 delegate 后才 resolve 源监听器 | `packages/api/gateway/src/types.ts:61-76` |
| 非 owner Peer **从不收到它可以作答的 scoped waterfall**；只有 owner Peer 接收并回答 | `packages/api/gateway/README.zh.md`（`$events` 一节）|

**三条可选改法（研究建议，非仓库现状）**

| 方案 | 做法 | 代价 | 评价 |
|---|---|---|---|
| **A. 新增只读 emit 事件**（推荐） | 在 `API_REMOTE_FORWARDED_EVENTS` 加一条 `{ event: 'approvals/pending', mode: 'emit', resources: { session: … } }`，内容为"某会话有 N 个待审批" | 需 Host 侧维护一份索引；**不改变 waterfall 语义** | 最小侵入，且天然受 `remoteAccess.decide` 约束 |
| **B. 把审批改成 emit** | 让审批以广播事件下发 | 会**破坏"只有能作答的 Peer 才收到"**这条安全约束 | 不建议 |
| **C. 纯 UI 侧轮询** | 客户端定时拉各会话 `pendingInteraction` | 需要可见"所有会话"；后台 Bot 会话通常不在列表里 | 治标不治本 |

> **关键判断**（依据 `packages/api/gateway/src/stream-protocol.ts:51-59` 的 Agent 作用域 waterfall 帧与 `index.ts:1226-1229` 的 `interactions=answer` 门槛）：**"审批卡只在会话内可见"是协议级设计，不是渲染层的疏漏。** 要做"全局待审批"，正确路径是**新增一条只读 emit 事件**，而不是把交互式事件改成广播。

---

## 5.6 三类"Bot 不回话"的区分表（结合我们踩过的坑）

| 故障 | 可观测信号（本仓库 + 运行库）| 代码位置 |
|---|---|---|
| **① 没被唤醒** | `inbox_admissions` **无该消息的行**；`bot_source_wake_attempts` 无新记录 | 接纳层（闭源 Bot Harness）|
| **② 回合卡住（等审批）** | `inbox_admissions` 有行；会话 `activity` 停在 `working`；`approval/asked` 已写入会话日志但无 `approval/decided` | `approval/asked` 见 `packages/core/session/src/known-event-types.ts:25-26` |
| **③ 编排层不可用** | 工具统一返回 `Orchestrator run is unavailable`（**本仓库 0 命中**，来自闭源层）；恢复后自愈 | 无（不在开源代码内）|

> **用途**：以后再遇到"Bot 不回话"，先按这三行分诊，别一律当"投递失败"处理——今晚三种我们都遇到过。

---

## 6. 证据索引

| 结论 | 证据 |
|---|---|
| 转发白名单是唯一真源（26 条） | `packages/api/remotes/src/remote-events.ts:1-6,26-55` |
| `approval/request` 为 waterfall | 同文件 `:28` |
| `user-questions/request` 同为 waterfall | `:54` |
| 会话类事件带 `resources.session` | `:29-34` |
| ACL 语义（emit 受资源访问控制；集合变化走 follow streams）| `:20-24` |
| 类型投影来自白名单 | `packages/api/remotes/src/types.ts:15` |
| 客户端会话待处理交互字段 | `packages/client/ui-session/src/client/index.ts:64,538,706` |
| 审批插槽 `scope: 'session'` | `packages/client/ui-approval/src/client/contract/slots.ts:36-39` |
| `Orchestrator run` 不在仓库 | `grep -rn "Orchestrator run" packages apps` → 0 命中 |

---

## 7. 未能确证

| # | 事项 |
|---|---|
| 1 | 闭源 Bot Harness 是否另有跨会话推送通道（本仓库看不到）|
| 2 | waterfall 事件在"应答者不在场"时的服务端超时/丢弃策略（未在 gateway 包内找到明确策略）|
| 3 | `resources` 访问控制在 Bot/群场景下的实际判定（属闭源权限模型）|
| 4 | 客户端 follow streams 的断线重连与补洞上限（只在注释提到 follow streams，未逐行核）|
