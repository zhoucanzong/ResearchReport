# DeepSeek Harness 源码快照身份与阅读范围

- 复核日期：2026-10-22。
- 上游：[deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)；本地快照 `/tmp/dsh-src`。
- 快照无 `.git`，`package.json:3` 自述版本 `0.2.1-rc.2`；**不能把版本号或 master 当作 commit**，本轮也没有取得可靠的历史 commit 对应关系。
- 对当前可定位、被四份文档引用的 63 个文件生成 [SHA-256 清单](SNAPSHOT_SHA256SUMS.txt)。清单自身 SHA-256：`f78bd1c85a8a370deeb4c4555aa365a08c52885aae9fdb783f9a372b48d3c0fb`。这是被审查文件集合的身份指纹，**不是完整上游树的 commit，也不保证能从远端重建这个快照**。
- 已回读：CLI `bin.ts`/`profile-boot.ts` 的配置组合与 boot；PTC `ptc.ts:378-405,715-746` 的审批→执行→输出；compaction `region.ts:491-509` 的摘要替换与 session `surface.ts:330-364,563-585` 的投影校验；gateway 事件白名单、会话 pendingInteraction 与 approval slot。
- 静态支持：程序审批在执行前；compaction 改模型可见投影并引用被遮蔽 seq；审批详情按 session 归属。
- 仍未验证：端到端运行与 OS 沙箱强度、真实持久化完整性、闭源客户端/编排层行为；未以符号零命中证明不存在绕过路径或全局出口。

使用技能：`code-researcher deep`，按 evidence-quality/runtime-story/claim-audit/reading-coverage 回到代码核实入口、交接和输出；本轮未构建或启动应用。

## 工具副作用与持久化追踪（2026-10-24）

- 上游固定版本：[deepseek-ai/deepseek-harness `22ddee3792402c3e70ec5f86a63c3e3e895a2f60`](https://github.com/deepseek-ai/deepseek-harness/tree/22ddee3792402c3e70ec5f86a63c3e3e895a2f60)，由官方 `master` HEAD 复取；不是 2026-10-20 `/tmp/dsh-src` 无 Git 身份快照的补记版本。
- 阅读覆盖：`packages/core/agent-loop/src/agent.ts`、`packages/core/tools/src/{batch,pipeline}.ts`、`packages/core/session/src/{index,repair}.ts`、`packages/session/session-persistence-jsonl/src/{storage,index}.ts`、`packages/session/session-checkpoint-policy/src/index.ts`、对应 checkpoint 单元与 crash-recovery e2e 测试、`packages/bundle/base/cordis.patch.yml`。
- 追踪结论和逐处不可变源码链接见[工具副作用与会话持久化](../topics/tool-effect-durability.md)：base 组合在顶层工具体前等待 session flush；副作用完成而结果未耐久时恢复为 `TOOL_OUTCOME_UNKNOWN`，不自动重试；缺少 checkpoint policy 的自定义组合保留事件缓冲窗口。
- 本次只静态阅读源码与测试，不运行测试、模型、文件/网络工具副作用或故障注入；测试文件中的 SIGKILL 场景是已有测试，不等于本次复现。未下载论文或源码缓存。
