# Astronomy selection record

筛选截止：2026-10-23。研究问题限定为：主动异常排序在大型星系图像巡天中，能否减少人工筛查负担并找出候选？筛选池 5 篇；1 篇深读，1 篇作为机制背景，3 篇排除或留待后续。PaperFetcher 是论文搜索与元数据核验工具；最终主张以期刊/ arXiv 一手原文为准。

## 本轮深读

| Paper | 决定 | 为什么入选 |
| :-- | :-- | :-- |
| [Astronomaly at scale (2024)](https://doi.org/10.1093/mnras/stae496), arXiv `2309.08660v2` | 深读 | 对真实 DECaLS DR8 近 390 万图像进行全流程搜索，提供 iForest 与主动学习对照、数据切割诊断、透镜/并合/未分类候选列表，以及候选尚待确认的明确边界。 |
| [Astronomaly (2021)](https://doi.org/10.1016/j.ascom.2021.100481), arXiv `2010.11202v2` | 机制背景 | 给出框架的原始主动学习机制及较小规模 Galaxy Zoo / 模拟验证。用来解释方法来源；不与 DECaLS 的规模成绩合并。 |

## 相关但未进入精读

| Candidate | 处理 | 理由 |
| :-- | :-- | :-- |
| [A Hitchhiker's Guide to Anomaly Detection with Astronomaly](https://arxiv.org/abs/2201.10189) | 排除 | 用户指南/框架说明，不是额外的大规模真实目录实证；与原方法论文功能重叠。 |
| [Anomaly detection in the Zwicky Transient Facility DR3](https://doi.org/10.1093/mnras/stab316), arXiv `2012.01419` | 排除 | 时域光变曲线与图像形态的科学问题、特征工程及伪影来源不同；可独立做 transient anomaly 专题，不混入本条。 |
| [Enabling unsupervised discovery in astronomical images through self-supervised representations](https://doi.org/10.1093/mnras/stae926) | 暂缓 | 探索 BYOL、自监督表征和聚类，只有部分章节使用 Astronomaly/并合候选示范；本条中心是大规模异常排序及候选确认界限，纳入会把问题扩到通用表征学习。 |

## 可继续的研究方向

- **候选到确认**：追踪主论文中 3 个此前未发现的透镜候选是否有后续高分辨率成像、光谱或可靠物理确认，并记录被证伪的对象。
- **选择偏差与完备性**：构造较少漏目标的 DECaLS 入口，测量各类 cut 对已知透镜与其他罕见形态的保留率；区分候选排序质量和目录 completeness。
- **面向 Rubin 的主动检索**：将望远镜/巡天数据本地运行、实时反馈、标签者差异和观测后续队列作为同一闭环评估，报告每小时专家审查带来的确认候选数。
