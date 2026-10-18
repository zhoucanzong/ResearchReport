# DSH Harness 反馈清单（2026-10-18，来自一次真实事故）

> 场景：多 Bot 协作 + 无人值守夜间任务。下面是**行为层证据**，不是源码审计（`app.asar` 为打包产物，未解包）。

## 1. 审批卡只投"发起频道"，Bot DM 发起时人类不可见

- 现象：图图的审批卡 `approval/asked`（reason: *"This tool call may access files outside the authorized folder"*）由**Bot 间 DM** 触发的轮次产生，卡片落在该 Bot DM 频道；人类界面**看不到**，因此无法放行。
- 影响：任务静默卡死，协调者只能靠"会话无推进"间接发现。
- 建议：审批卡在**投递发起频道的同时**，兜底投递到该 Bot 的 **Human DM**（或标记为"孤儿审批"进 Human 收件箱）。

## 2. "记住此规则"只写进会话作用域，跨会话不继承

- 证据：`tool_approval_rules` 表 11 条规则全部为 `kind=all-opaque`、`tool_name=*`，但 `scope_key` 形如
  `["assignment","/Users/zhoucanzong/Documents/Research",["88334c1f-5da2-44d1-b41a-377adad34296"]]`
  —— **绑定到具体会话 id**。
- 影响：新开 Assignment（新 id）不命中旧规则 → 第一次 `git` 再次弹审批；某些 Bot（研研）**0 条规则**，等于每次都要人点。
- 建议：允许 **bot + 角色 + 工具** 级别的规则（不含会话 id），或提供"对该 Bot 永久允许"。

## 3. 挂起审批的轮次会阻塞后续唤醒，且无超时/提醒

- 证据：`bot_source_wake_attempts` 显示图图/研研/究究在某时刻后**零唤醒记录**，同期协调者多次发 DM；会话 activity 停在 `working`。
- 影响：表现为"消息投递不到"，实为"轮次挂起 → 不再唤醒"，容易误判为传输故障。
- 建议：对等待审批超过 N 分钟的轮次，进入"待审批"状态并在 Human 侧提示；同时**不阻塞**新消息唤醒（或排队而非抑制）。

## 4. 复合 shell 重定向命令的可达性分析过于保守

- 现象：`cd <bot-memory> && cat >> notes/x.md <<'MDEOF' …`（**目标路径完全在授权区内**）仍被判"may access files outside the authorized folder"。
- 对照：改用 `write`/`edit` 文件工具写同一路径 → **不再弹审批**（图图实测，同一会话内）。
- 影响：Bot 用 heredoc 记笔记这种常规操作会反复打扰人；而"改写法"并不总是直觉可达。
- 建议：对 `cd <授权内路径> && <重定向到相对路径>` 做白名单解析；或在 reason 文案里点明"请改用 write/edit"。

## 附：我们已落地的规避（团队侧）

- 会话统一 `sandbox=danger-full-access` + `approval=never`（不绑会话 id），或对需要确认的动作接受"审批卡必须落在可见频道"。
- 执行类任务**不从 Bot DM 发起**，改从 Group / Human DM 发起。
- 写文件一律 `write`/`edit`，**禁用 `cat >> … <<EOF`**。
- 卡点 5–10 分钟无推进即上报；超 30 分钟无观测推进由协调者接管。
