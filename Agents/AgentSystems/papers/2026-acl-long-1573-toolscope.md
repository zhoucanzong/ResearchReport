# ToolScope：工具太多时，Agent 先要整理候选集

> Liu et al., *ToolScope: Enhancing LLM Agent Tool Use through Tool Merging and Context-Aware Filtering*, ACL 2026, pp. 34095–34119。 [论文页](https://aclanthology.org/2026.acl-long.1573/) · [PDF](https://aclanthology.org/2026.acl-long.1573.pdf)

## 研究问题与方法

Agent 的工具集会包含语义重叠、名字相近或描述冗余的工具，同时模型上下文有限。ToolScope 把工具选择前的整理拆成两部分：ToolScopeMerger 用语义相似度找候选重叠，再由 LLM 验证关系、聚合并自动修正；ToolScopeRetriever 结合稀疏/稠密检索、query decomposition 与 reranking，为当前请求选出 top-k 工具（§1、§3）。

这把 Agent 研究从“模型会不会调用工具”向“工具目录怎样表示、去重、筛选”推进。它的判断对象是候选工具集合，不能替代调用后的参数验证或执行权限控制。

## 结果与读法

Table 2 使用 GPT-4o、Llama-3.3-70B、Command-R，在 BFCL、Seal-Tools、UltraTool 报告 CSR@k（正确选出的工具集合比例）。论文摘要报告相对强 baseline 的提升：Seal-Tools +34.6%、UltraTool +38.6%、BFCL +8.8%；这些是指定任务、模型和 k 下的工具选择差异，不是 Agent 端到端成功率。模块消融显示 merger 的贡献最大；auto-correction 还能部分修复错误合并，而 reranker 的收益主要出现在较大、较嘈杂的工具集（§4.2–4.3、Tables 2–3）。

## 限制与部署含义

检索依赖工具名、签名和描述；论文建议增加典型用例、领域和 I/O schema 等元数据。作者还指出 reasoning 模型可能改变 Auto-Correction 表现；LLM 驱动的合并和检索存在幻觉与错合风险，因此论文明确表示不适用于医疗、法律、金融等高后果工具决策（Limitations / Ethical Considerations）。

正确学习结论是：整理工具候选集能改善该评测中的选择准确率；不能外推成任意真实工具目录上的安全或通用收益。
