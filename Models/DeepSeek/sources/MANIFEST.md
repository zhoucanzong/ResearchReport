# DeepSeek 更新来源清单（2026-10-22 起的分批更新）

> 核查截止：2026-10-23（Asia/Shanghai）。§1–7 记录 2026-10-22 的 V4/V4.1 身份与 FP8 复核；§8 记录 2026-10-23 加入的相位敏感性论文。两份历史子报告不在对应批次改写范围；未将当前 API alias 当作固定论文 checkpoint。

## 1. 事件、论文和服务身份分开

| 日期/身份 | 原始出处 | 本批结论 |
|---|---|---|
| 2026-04-24 V4 Preview | [官方公告](https://api-docs.deepseek.com/news/news260424/) | 公告/API/开放权重入口事件；不是0813或4.1 |
| 2026-07-31 Flash-0731 | [官方日志](https://api-docs.deepseek.com/updates/) 07-31条目 + 固定模型卡 | Flash正式版API public beta；和Preview、DSpark组件分开 |
| 2026-08-13 Pro-0813 | [GA公告](https://api-docs.deepseek.com/news/news260813/) | Pro GA；API名仍deepseek-v4-pro |
| 2026-08-21 Vision-Exp | [官方公告](https://api-docs.deepseek.com/news/news260821/) | 视觉实验API事件；未以此推定权重首发日 |
| 2026-09-10 V4.1-Flash | [官方公告](https://api-docs.deepseek.com/news/news260910/) | API deepseek-flash，原生图文输入；公开模型仓库 |
| 2026-09-17 2609.19969v1 | [arXiv元数据](https://arxiv.org/abs/2609.19969v1) / PDF首页 | 原版4.1技术报告提交日，晚于模型公告 |
| 2026-10-17 V4.1-Flash-1017 | [官方公告](https://api-docs.deepseek.com/news/news261017/) | 新公开checkpoint；API deepseek-flash随之更新 |

## 2. 实际读取的模型卡与仓库revision

下表日期是HF仓库元数据，**不作为全部权重分片首次可下载时间**；本批读取卡片、两个4.1配置和权重索引，没有下载权重。线上模型与仓库revision的对应来自官方版本标签，服务端权重SHA未披露，不证明位级相同。

| 精确HF ID | 固定 revision | createdAt (UTC) | lastModified (UTC) |
|---|---|---|---|
| `deepseek-ai/DeepSeek-V4.1-Flash` | [`314113f8a7dadb388215396ba5fbee2c610a04d6`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/README.md) | 2026-09-10T02:17:58.000Z | 2026-10-16T09:27:28.000Z |
| `deepseek-ai/DeepSeek-V4.1-Flash-1017` | [`1bae0e1088993b9b82de08f59de5be5a34e42170`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/blob/1bae0e1088993b9b82de08f59de5be5a34e42170/README.md) | 2026-10-17T02:40:38.000Z | 2026-10-17T05:46:55.000Z |
| `deepseek-ai/DeepSeek-V4-Pro-0813` | [`72e1d3230f6c080a530b0a1d46f8eb4602340597`](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/blob/72e1d3230f6c080a530b0a1d46f8eb4602340597/README.md) | 2026-08-13T03:05:06.000Z | 2026-08-13T16:28:28.000Z |
| `deepseek-ai/DeepSeek-V4-Flash-0731` | [`7872f01b1d1fe23eabc4c98b48bffcef5a386062`](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731/blob/7872f01b1d1fe23eabc4c98b48bffcef5a386062/README.md) | 2026-07-31T07:30:24.000Z | 2026-08-01T03:07:41.000Z |
| `deepseek-ai/DeepSeek-V4-Pro` | [`b5968e9190ef611bbf34a7229255be88a0e937c1`](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/b5968e9190ef611bbf34a7229255be88a0e937c1/README.md) | 2026-04-22T06:04:45.000Z | 2026-06-22T12:12:50.000Z |

原版4.1卡本次读取的是10月16日revision，**不是9月10日原始网页快照**。1017与原版的公开config哈希相同，值为 `8be45ce0476004a3f529fd896115a4a2e800a129ad2d3ec05b16050f52e21879`，包括40层、vocab_size 129280；权重索引均列48分片和96085映射张量。这证明静态配置相同，不证明分片内容相同或训练流程没有变化。

## 3. 论文文件身份与读取范围

| 来源 | 固定身份 / SHA256 | 本批实际阅读 |
|---|---|---|
| arXiv PDF | `2609.19969v1`；`0cfdda19c8e1691b5226dd0d4949e2397051268e8a823c2fb61db94ea20c4ac0` | 摘要与§1开头，§2.4.2 Engram，§4.2.1，§5.3.1，§6；未逐表审完全部消融/训练 |
| HF内PDF | `deepseek-ai/DeepSeek-V4.1-Flash@314113f8a7dadb388215396ba5fbee2c610a04d6/DeepSeek_V41_Tech_Report.pdf`；`ba68e2e40408125ae6d2f63a9a241b61c73910691c74ec1a2a7023c851eac08d` | 核对标题/摘要与目录；不默认为与arXiv PDF同一字节版本 |

两个PDF字节不同，分别保留；本批没有据HF文件生成日期推断论文首次公开日。arXiv版本取PDF首页/abs版本历史；1017卡指向既有4.1报告，不构成新论文日期。

## 4. 动态官方文档快照

原始HTML与提取文字保存在仓库外 `~/Documents/paper-cache/research-audit-2026-10-22/models/deepseek-update/`。下表的哈希固定本次内容，HTTP Last-Modified只是站点构建头，**不是模型或论文发布时间**。

| 来源 | 本次HTML SHA256 | 使用位置 |
|---|---|---|
| [updates](https://api-docs.deepseek.com/updates/) | `9abda5ba89b86be5d82ad045864dbe5047e0908b45c161d8a4631d4d5fcb6f18` | 07-31/08-13/09-10/10-17更新与脚注、Speciale临时API历史 |
| [preview](https://api-docs.deepseek.com/news/news260424/) | `9fec5d17e3ed62a4624c87027b36254c317bd5a093b7c38b2244c101eec98ce6` | Preview身份与deepseek-chat/reasoner停用计划 |
| [pro-ga](https://api-docs.deepseek.com/news/news260813/) | `4ec9c3b7bc0ccb3e0244bb40bc2c1a47b743f0d61a5b467026c7d90fc881168c` | Pro GA与模式接口事件 |
| [vision-exp](https://api-docs.deepseek.com/news/news260821/) | `eba2eee488415b13dfab8e1a0c4ae264794d3316c21e990eb518ba625e95b09e` | 视觉实验API日期和ID |
| [flash-41](https://api-docs.deepseek.com/news/news260910/) | `43a9508b564cd2f901feda4f18c0a202f1e5c5102ae01b040aa50f78a1f6ca8a` | 4.1原生图文和迁移原计划 |
| [flash-1017](https://api-docs.deepseek.com/news/news261017/) | `c557ba334297a0a802282431dd15c9ba6942846a71860051c1c7b9e53d5dc037` | 1017上线、权重入口、Harness版本建议 |
| [pricing](https://api-docs.deepseek.com/quick_start/pricing/) | `b856a6e93fa4793ecc8f3fd03a01bb7d8f7572f78a4739da8ce6dbdb09328d66` | 当前API ID→模型版本、视觉差异、上下文/输出与分项计价 |
| [thinking](https://api-docs.deepseek.com/guides/thinking_mode/) | `7d9762238e92a7391173ba1726778e46ec11c7bc599e3e395265488f196618b7` | 当前托管API字符串effort与格式映射 |
| [vision](https://api-docs.deepseek.com/guides/vision/) | `53c5ad4dcd6433fe7130cea78113e2b2bba119ee42ec7591759e8f6f66b51ae9` | 当前Flash视觉输入及旧Vision-Exp兼容路由 |
| [paper-abs](https://arxiv.org/abs/2609.19969v1) | `85e17c9066aff54c0ef751eebe286cff15b9c1f4d05d7615270950bd82509881` | 4.1论文标题/版本/提交日 |

## 5. 冲突和不允许的继承

- **Pro迁移原计划已被后续口径覆盖**：9月10日独立公告仍写9月14日转路由；日志补充“应用户要求继续V4 Pro”，当前接口表标Pro-0813。主报告按补充+当前接口表写继续服务，保留原计划变更记录；没有凭据实测端点。
- **数值effort与托管接口不同层**：原版论文/权重编码允许1–100，当前托管文档按low/high/max和协议映射呈现。不能直接移植为所有SDK接受数值100。
- **1017成绩不倒灌到9月论文**：1017的Terminal-Bench4.0使用Claude Code、DeepSWE使用Mini-SWE-V2；原版论文使用的脚手架与之未完全一致。不得将分差全部归因于权重更新。
- **官方数字也有条件**：552B是backbone，196B Engram另计；890bytes/token是global KV；1/8是persistent cache，非整机显存；51.0为ZeroBench-main w/tools Pass@5。
- **权重/API/Paper三个时间不混同**：repo createdAt不是模型上线日期、API ID不是不可变checkpoint、同名模型卡引用旧论文不是新论文发布。

## 6. 历史子报告保留与本批未解决项

| 保留文件 | 本批前后SHA256 |
|---|---|
| [deepseek-text-models.md](../deepseek-text-models.md) | `e5ea33fd2ba80a3ec431ce5c9364927c8b392a5c6ce0e28e3fc76183aaf89c50` |
| [deepseek-multimodal-and-specialized.md](../deepseek-multimodal-and-specialized.md) | `b742cbfe359bd478805e310b2f4ea4510c4beeb24ce2ba5d4127a611cfc07d98` |

历史子报告的文字与原先证据口径保持原样；本次未把它们动态URL自动升级为新论文。原有未固定URL的历史引用仍是未解决项，不能因上表固定文件内容就称旧来源全部可复现。

未解决：未穷举全部HF权重/论文新作；未审Vision-Exp权重；未测API或推理；未独立复跑1017成绩；原版与1017的全部训练差异未披露；不确认V4.1-Pro发布；第三方云/IDE的逐型号接入与价格仍待核。V4原论文链接2606.19348v1仅核对标题与元数据，未将其摘要级核对升级为全篇精读。

Skill使用：按 `researcher` 的来源/数字条件/不确定值要求处理更新；论文用 `paper-fetcher download` 获取。未调用 `code-researcher` 做仓库行为深读，也不将配置读取称为源码执行链审查。

## 7. DeepSeek-V3 FP8 单切面复核（2026-10-22）

本批仅重写[文本子报告 §4.3.3](../deepseek-text-models.md#433-fp8-混合精度训练)与[主报告 §3.3](../report.md#33-fp8-训练与低成本策略)及其直接重复摘要。§1–6是上一批更新的历史记录，其中子报告的前后哈希只指**上一批**；本批明确授权更改FP8小节，不把旧哈希当当前文件哈希。其余历史章节与多模态子报告未改。

| 一手来源 | 固定身份与本地证据 | 实际阅读及用途 |
|---|---|---|
| [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437v2) / [PDF](https://arxiv.org/pdf/2412.19437v2) | `2412.19437v2`，2025-02-18修订（v1提交2024-12-27）；PDF SHA256 `812a3fd645c80725354de9d831a6785503007a60681461407f64e97305fa9330` | 通读§3.3 pp.14–18及附录B.1–B.2 pp.47–48；核对摘要、§1/Table 1、§3.1。区分载荷字节数、GEMM理论计算速度、loss对照和完整训练系统结果；未宣称全篇重新精读 |
| [官方DeepSeek-V3仓库](https://github.com/deepseek-ai/DeepSeek-V3/tree/9b4e9788e4a3a731f7567338ed15d3ec549ce03b) | commit `9b4e9788e4a3a731f7567338ed15d3ec549ce03b`，2025-08-28T11:24:26+08:00；后于论文修订，不能当原始训练代码 | 全树扫描；实际阅读README推理说明与`inference/model.py`的Linear分支、`inference/kernel.py`量化/反量化/GEMM。只核对公开推理demo的静态行为，未运行GPU、未检查权重 |

源码定位（均为上述固定commit）：

- [`README.md:231–246`](https://github.com/deepseek-ai/DeepSeek-V3/blob/9b4e9788e4a3a731f7567338ed15d3ec549ce03b/README.md#L231-L246)：FP8/BF16 inference demo与权重转换说明；不提供训练吞吐证据。
- [`inference/model.py:153–163`](https://github.com/deepseek-ai/DeepSeek-V3/blob/9b4e9788e4a3a731f7567338ed15d3ec549ce03b/inference/model.py#L153-L163)：高精度权重直接linear、BF16分支先反量化、FP8分支`act_quant → fp8_gemm`。
- [`inference/kernel.py:38–57`](https://github.com/deepseek-ai/DeepSeek-V3/blob/9b4e9788e4a3a731f7567338ed15d3ec549ce03b/inference/kernel.py#L38-L57)：FP8激活加每128元素一个FP32 scale；132/256=51.5625%只计算这两个输出载荷。
- [`inference/kernel.py:156–196`](https://github.com/deepseek-ai/DeepSeek-V3/blob/9b4e9788e4a3a731f7567338ed15d3ec549ce03b/inference/kernel.py#L156-L196)：FP32累加、缩放、转换输出；不是论文Wgrad/Dgrad训练实现。

本批撤回“BF16训练显存减半 + GEMM实测/端到端翻倍”的合并断言，改写为FP8对BF16的**理论载荷**比例和论文明确限定的**理论计算速度**；将“零loss spike”纠正为作者报告“无不可恢复loss spike”，补入16B/230B训练loss对照与Dgrad block量化发散反例。没有把2.788M H800 GPU-hours视为FP8单项因果收益。

未解决但不再当成确定收益：671B完整BF16控制实验、训练峰值显存拆账、原始训练内核固定M/N/K吞吐与计时方法、可归因FP8的完整step/端到端推理收益；本次未取得这些实测数据。附录B未单列两组小规模对照的卡数/批量，不假定其均使用2048卡。未扩大到新模型、其他历史技术争议或社区内核基准。

本地缓存：`~/Documents/paper-cache/research-audit-2026-10-22/models/deepseek-v3-fp8/`，含固定PDF、文本抽取、官方源码checkout及`repo-scan.json`。精确输入/输出哈希与范围检查另记本地审计底账`.rehearsal/audit/goal-batches/deepseek-v3-fp8.json`。按`researcher`核对论文，按`code-researcher`追公开推理调用链，论文由`paper-fetcher`获取；三个skill未被脚本检查替代。

## 8. 分块 KV 压缩相位敏感性（2026-10-23）

本次定向选读该论文，是因为它提出并测试了与 V4/V4.1 分块 KV-cache 机制直接相关的 phase failure mode；不声称穷尽 2026 长上下文论文，也未把预印本当成独立复现结论。

| 来源 | 固定身份 / 许可 | 精读范围与用途 |
|---|---|---|
| Zhu et al., [Periodic Weak Spots: Phase Sensitivity from Chunked KV-Cache Compression](https://arxiv.org/abs/2609.36322v1) | arXiv `2609.36322v1`，提交 2026-09-28 21:54 UTC；PDF 首页标 2026-09-30；arXiv 版本页链接 CC BY 4.0；预印本 | 官方 arXiv PDF：§§1–2、Fig. 1–2、Table 7、Appendix B–C；§3.2、Fig. 3、Table 8、Appendix F；§4.1–4.2、Figs. 4–5、Appendix E/G–H。结果支持压缩 stride 与周期敏感性相关；对生产 DeepSeek 模型的结果是作者报告，受控因果机制证据来自 Qwen3-0.6B 派生模型与有限 head/layer 干预。 |

- ByteDance Seed 官方论文页确认题名、作者列表、2026-09-28 发布日期与摘要：[Seed publication page](https://seed.bytedance.com/en/public_papers/periodic-weak-spots-phase-sensitivity-from-chunked-kv-cache-compression)。作者单位脚注表明核心贡献者在 ByteDance Seed 实习；合作作者亦来自 Princeton、Stanford 与 UC Berkeley。
- 工具使用记录：本文所在批次的过程说明报告调用了 Researcher deep 和 PaperFetcher `fetch 2609.36322 --citations`；但仓库没有保存二者的原始输出或调用日志，故工具执行本身无法由当前留档独立审计。本次定向复核直接查看官方 arXiv 版本页、PDF 与 Seed 页面，核实题名、作者、v1 提交时间、PDF 日期及许可证；这只能复核元数据和原文主张，不能充当 Researcher/PaperFetcher 的执行凭证。PaperFetcher 元数据一致性目前仍是过程记录中的报告结果。
- `/Users/zhoucanzong/Documents/paper-cache` 未找到该 ID 对应文件；未复制论文全文进仓库。本文阅读了 PDF 的主文 §1–5 与相关附录 C、E、F、G、H；没有从头运行 100B-token 训练或重跑 DeepSeek/NIAH 评测。
- Claim audit：人工逐项核对精读中的 **8 个数值主张簇**。取数方式是数 `deepseek-phase-sensitivity.md`「可复查锚点」表编号 1–8 的数据行（每行按一个 claim cluster 计；不把行内拆成多个 claim，也不把年份/型号编号计入）；8 行均指向固定 PDF 锚点。第 8 行区分 Fig. 3 所示 75.3 pp 与 Table 8 完整压缩扫描最高 78 pp；DeepSeek-V4 的干预锚点区分整层 attention-output replacement 与受控模型的逐 KV-head knockout。该数不是全文自动扫描统计。未运行作者训练或推理代码，也未独立复现实验。
