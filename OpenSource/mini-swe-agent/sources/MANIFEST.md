# mini-swe-agent 源码证据与复核边界

- 复核：2026-10-22，使用 `code-researcher deep`（evidence-quality、runtime-story、reading-coverage、claim-audit），重新运行官方 `scan_repo.py`。
- 固定来源：[SWE-agent/mini-swe-agent@adfe20233d456104c38c3129161b54f0fd39f2c7](https://github.com/SWE-agent/mini-swe-agent/tree/adfe20233d456104c38c3129161b54f0fd39f2c7)；[源码tarball](https://codeload.github.com/SWE-agent/mini-swe-agent/tar.gz/adfe20233d456104c38c3129161b54f0fd39f2c7)。
- 仓库外临时阅读目录：`/tmp/research-code-audit-20261022/mini`；上游源码未入库，未构建或执行上游系统。临时目录不是长期保存承诺，可按固定SHA重新取源。
- 本轮核验的是下列强结论和运行切面，**不是全上游仓库逐行读完、测试全通过或所有配置行为已证实**。旧报告的机械零告警不代表语义通过。

- 身份：本轮 `git ls-remote ... refs/tags/v2.3.0` 解析到上述SHA；`src/minisweagent/__init__.py:11`同为2.3.0。旧报告缺失main SHA，不能据本轮tag恢复旧快照身份。
- Traced：`src/minisweagent/run/mini.py:55-105` → `agents/default.py:85-138` → `models/litellm_model.py:64-93` / `environments/local.py:23-66` → `DefaultAgent.save:163-170`。入口、组件交接、模型网络边界、shell副作用及trajectory均有源码落点。
- Audited：`config/__init__.py`、`utils/serialize.py`、`models/__init__.py:65-75`的配置合并/回退；`litellm_model.py:80-93`没有FormatError原始response fallback；`local.py:28-39`未建立完整进程树清理保证。
- 未核：74%宣传的逐实例记录/模型预算；所有容器后端实际隔离；SWE-agent/Claude Code固定版本对照；测试仅静态读取，未运行依赖和agent。
- 本tag手数Python文本行：src 5108、tests 8568；正文原约数是旧口径，不作为当前精确规模。

引用格式：本条目的简写 `文件:行` 均相对上述固定源码根；回源使用 `https://github.com/SWE-agent/mini-swe-agent/blob/adfe20233d456104c38c3129161b54f0fd39f2c7/<path>#L<line>`。保留旧阅读记录不将其覆盖等级自动升级成本轮已核。
