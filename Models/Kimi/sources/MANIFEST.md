# 原文清单 · Kimi

> 本仓库**只存清单与我们的精读分册**（`papers/*.md`），**不存论文全文**（PDF 或转出的 markdown 都不入库）。
> 需要回看原文时：按下面的 arXiv 链接现取；本地缓存可选（`~/Documents/paper-cache/<id>@<版本>/`），缓存同样不入库。
> **权重/仓库**只记录 `仓库 @ commit` 与用到的 `文件:行`，源码与权重不入库。

## 1. 论文分册

| # | 分册（我们的精读） | arXiv ID | 版本 | 版本日期 | 标题（arXiv 元数据，逐条核实） | 第一作者（核实） | 去哪找原文 |
| --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | [`papers/2607.24653-kimi-k3.md`](<../papers/2607.24653-kimi-k3.md>) | 2607.24653 | v2 | 2026-08-07 | Kimi K3: Open Frontier Intelligence | Kimi Team（402 位作者，按 arXiv 元数据） | https://arxiv.org/abs/2607.24653 |

### 1.1 分册引用的前置论文（本条目未单独设分册，数字以 report.md 口径为准）

| arXiv ID | 版本 | 版本日期 | 标题 | 在本条目中的用途 |
| :-- | :-- | :-- | :-- | :-- |
| 2510.26692 | v2 | 2025-11-01 | Kimi Linear: An Expressive, Efficient Attention Architecture | KDA 的对照基线（无界负 Softplus、低秩输出门）；report §2.3 |
| 2603.15031 | v1 | 2026-03-16 | Attention Residuals | AttnRes 独立验证（Kimi Linear 48B-A3B / 1.4T tokens）；report §2.3、K3 分册 §2.2 |
| 2507.20534 | v2 | 2026-02-03 | Kimi K2: Open Agentic Intelligence | K3 的对照基座（纯 MLA + RoPE/YaRN）；report §2.4 |
| 2602.02276 | v2 | 2026-08-07 | Kimi K2.5: Visual Agentic Intelligence | MoonViT-3D / 视觉数据分类学的来源；K3 分册 §2.4 |

> 版本口径：版本日期取 arXiv 元数据的 `updated`（最新版本），不是首次提交日。K3 的 v1 为 2026-07-27、v2 为 2026-08-07，本清单与 report.md 均以 **v2** 为准。

## 2. 模型卡与官方页面（非论文，但属一手源）

| # | 来源 | 创建/更新日期 | 用途 | 链接 |
| --: | :-- | :-- | :-- | :-- |
| 1 | HuggingFace 模型卡 `moonshotai/Kimi-K3` | lastModified 2026-09-02；API `createdAt=2026-06-13` 是仓库元数据，不代表权重当日公开 | K3 规格表、评测表与全部条件脚注、许可名称 | https://huggingface.co/moonshotai/Kimi-K3 |
| 1a | HuggingFace 权重仓历史 | 首批权重/README 提交见 2026-07-27 | 辅助确定公开权重时间；不从仓库时间推断模型版本变化 | https://huggingface.co/moonshotai/Kimi-K3/commits/main |
| 2 | HuggingFace 模型卡 `moonshotai/Kimi-K2.7-Code` | createdAt 2026-06-11 / lastModified 2026-06-15 | K2.7 Code 规格、评测与条件脚注 | https://huggingface.co/moonshotai/Kimi-K2.7-Code |
| 3 | 官方博客 `kimi.com/en/blog/kimi-k3` | 页面发布日 2026-07-16；2026-10-23 核验 | 产品/API 发布、完整权重发布时间说明、技术概述与限制；商业价格不纳入正文 | https://www.kimi.com/en/blog/kimi-k3 |
| 4 | 官方资源页 `kimi.com/resources/kimi-k2-7-code` | 页面标注「更新于 2026-10-08」 | K2.7 Code 技术/产品说明；价格不纳入正文 | https://www.kimi.com/resources/kimi-k2-7-code |
| 5 | Kimi API 平台文档 | 访问 2026-10-17 | `kimi-k3` 模型 ID 与调用方式 | https://platform.kimi.com/docs/guide/kimi-k3-quickstart |

## 3. 代码仓库（不入库）

| # | 用途 | 仓库 | 创建日期 | license |
| --: | :-- | :-- | :-- | :-- |
| 1 | K3 权重与部署入口 | `MoonshotAI/Kimi-K3` | 2026-07-27 | 未核实（仓库内 LICENSE 未逐字读） |
| 2 | 完全均衡专家并行（报告 §5.2.1 给出 URL） | `MoonshotAI/MoonEP` | 2026-07-24 | 未核实 |
| 3 | KDA 高性能 kernel | `MoonshotAI/FlashKDA` | 2026-04-20 | 未核实 |
| 4 | AttnRes 参考实现 | `MoonshotAI/Attention-Residuals` | 2026-03-15 | 未核实 |

> license 一栏保留「未核实」而不猜测：本条目本轮未逐字读这些仓库的 LICENSE 文件，报告正文也未据此断言可商用范围。

## 4. 未入库/未确证的候选

Kimi K3 License 条款、Artificial Analysis / Vals AI 原始评测页面、K3 的 low/high effort 档数字、K2.7 Code 的思考 token 绝对计数口径——以上均**未入库、未进正文**，处置理由见 [`../report.md`](../report.md) §4.6。

## 5. Kimi K3 联合设计证据边界与 reader-first 修订（2026-10-23）

- 固定论文仍为 [arXiv `2607.24653v2`](https://arxiv.org/html/2607.24653v2)，2026-08-07。§1/§3.2 说 KDA、AttnRes、Stable LatentMoE 与训练/数据改进合计带来约 2.5× scaling efficiency；没有找到六项架构/训练选择的全因子消融或逐项贡献实验。针对性证据分属 §2.1.1（KDA 下界衰减到 tiled Tensor Core 路径）、§2.3（LatentMoE 稳定化）、§2.4（MoonViT 初始化比较）、§2.5（Per-Head Muon），不能推出六项彼此必要。
- 论文 §2 把 KDA、AttnRes、Stable LatentMoE 与 Per-Head Muon 等称为架构/训练组合；§4.1.4 的 MXFP4 QAT 属部署感知后训练，视觉从零初始化属多模态训练选择。精读分册已把“六项互为前提”改为联合设计，将“完整消融链”改成组件级证据边界。
- 论文 Table 1 给出精确规模 **2.78T/104.2B**；摘要和模型卡写成四舍五入的 2.8T/104B。官方博客自我定位“first open 3T-class”未保留在读者正文。产品/API 日期 2026-07-16、权重公开窗口 7 月 27 日分别按[官方博客](https://www.kimi.com/en/blog/kimi-k3)及[Hugging Face 仓库历史](https://huggingface.co/moonshotai/Kimi-K3/commits/main)记录；模型卡 API 的 `createdAt=2026-06-13` 仅为仓库元数据，不作权重公开日期。
- 主报告与分册移除 API 价格、成本效益与跨厂商排行榜数字；保留 K3 自身代表性结果及 max effort、harness、H20/H100、重复次数和上下文压缩条件。数值仍是作者报告，未独立复跑。
- 本次修改是对固定论文的因果措辞校准与读者聚焦，不是整份 Kimi 报告逐主张重新审计。
