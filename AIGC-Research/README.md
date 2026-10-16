<div align="center">

# 🎨 AIGC Research Reports

**AI Agent 驱动的生成式 AI（AIGC）深度调研报告集**

> ⚠️ **重要声明**：本知识库所有报告均由 AI Agent 自动调研生成，信息来源于公开网络搜索、第三方评测站点、社交媒体及行业媒体报道。由于厂商官方披露程度不一，部分日期、参数、benchmark 数据可能存在错误、过时或未经证实的情况。**所有内容仅供参考，不构成权威结论，建议读者直接查阅各厂商官方渠道获取最新准确信息。**

覆盖 **8 个模型 / 系列 + 10 个技术专题** · 重点关注 **模型结构演进**

[![Monorepo](https://img.shields.io/badge/monorepo-ResearchReport-6f42c1?style=flat-square)](https://github.com/zhoucanzong/ResearchReport)
[![Reports](https://img.shields.io/badge/Reports-18-blue?style=flat-square)](.)
[![Files](https://img.shields.io/badge/Files-18-green?style=flat-square)](.)

</div>

---

> 📦 **仓库归属**：本报告集现归属 monorepo **[ResearchReport](https://github.com/zhoucanzong/ResearchReport.git)**，在统一仓库中位于根目录 [`AIGC-Research/`](https://github.com/zhoucanzong/ResearchReport/tree/main/AIGC-Research)，**库内相对路径保持不变**（如 `ModelSeries/StabilityAI-research/report.md`）。
>
> ```bash
> git clone https://github.com/zhoucanzong/ResearchReport.git
> cd ResearchReport/AIGC-Research
> ```
>
> 独立仓库 **AIGC-Research** 作为**上游存档仅保留在 GitHub**（`git@github.com:zhoucanzong/AIGC-Research.git`），本地副本已于 2026-10-16 移除；本目录内容与其一致，后续更新请以统一仓库 ResearchReport 为准。

---

## 📊 总览

### 模型系列

| #  | 图标 | 模型 / 系列 | 所属公司 | 报告数 | 亮点 |
| -- | :--: | ---------- | -------- | :----: | ---- |
| 1  | 🇺🇸 | [**StabilityAI**](./ModelSeries/StabilityAI-research/) | Stability AI / BFL | 1 | SD 1.x→2.x→XL→3→FLUX，U-Net→DiT 架构演进 |
| 2  | 🇺🇸 | [**OpenAI-Gen**](./ModelSeries/OpenAI-Gen-research/) | OpenAI | 1 | DALL-E 2/3→GPT-4o 图像生成→Sora，自回归+扩散混合架构 |
| 3  | 🇺🇸 | [**Google-Gen**](./ModelSeries/Google-Gen-research/) | Google / DeepMind | 1 | Imagen 2/3→Veo 2/3/3.1，级联扩散→DiT 视频生成 |
| 4  | 🇺🇸 | [**Midjourney**](./ModelSeries/Midjourney-research/) | Midjourney | 1 | V4→V5→V6→V7，闭源标杆的架构推测与美学进化 |
| 5  | 🇨🇳 | [**Kling**](./ModelSeries/Kling-research/) | 快手 | 1 | 可灵 1.0→2.0→3.0/O1，国产视频生成的 DiT 架构路线 |
| 6  | 🇺🇸 | [**Runway**](./ModelSeries/Runway-research/) | Runway | 1 | Gen-1→Gen-4.5，Latent Diffusion→DiT 视频编辑与生成 |
| 7  | 🇨🇳 | [**ByteDance-Gen**](./ModelSeries/ByteDance-Gen-research/) | 字节跳动 | 1 | Seedance 1.0→2.0，即梦AI，多模态 cinematic 生成 |
| 8  | 🇨🇳 | [**Alibaba-Gen**](./ModelSeries/Alibaba-Gen-research/) | 阿里巴巴 | 1 | 通义万相 Wan 2.1/2.2/2.6，开源视频生成的 DiT 架构 |

> **🇨🇳 国内 4 家** &nbsp;|&nbsp; **🇺🇸 海外 4 家** &nbsp;|&nbsp; 共 **8 个** 模型系列

### 技术专题

| #  | 图标 | 专题 | 覆盖范围 | 报告数 | 亮点 |
| -- | :--: | ---- | -------- | :----: | ---- |
| 1  | 🔬 | [**DiffusionModels**](./TechnicalTopics/DiffusionModels-research/) | 扩散模型基础 | 1 | DDPM→DDIM→LDM→Consistency Models，数学框架与采样加速 |
| 2  | 🔬 | [**DiT**](./TechnicalTopics/DiT-research/) | Diffusion Transformer | 1 | U-Net→DiT 架构革命，PixArt→SD3→FLUX→Sora 的 Transformer 化 |
| 3  | 🔬 | [**VideoGen**](./TechnicalTopics/VideoGen-research/) | 视频生成技术 | 1 | 时序建模、3D DiT、因果注意力、运动一致性，Sora→可灵→Veo 技术拆解 |
| 4  | 🔬 | [**ControllableGen**](./TechnicalTopics/ControllableGen-research/) | 可控生成 | 1 | ControlNet→IP-Adapter→T2I-Adapter→LoRA，条件注入架构演进 |
| 5  | 🔬 | [**3DGen**](./TechnicalTopics/3DGen-research/) | 3D 生成 | 1 | DreamFusion→Point-E→Shap-E→Tripo3D，NeRF→3D Gaussian Splatting |
| 6  | 🔬 | [**AudioGen**](./TechnicalTopics/AudioGen-research/) | 音频/音乐生成 | 1 | AudioLDM→MusicLM→Suno/Udio，扩散+自回归+流匹配音频架构 |
| 7  | 🔬 | [**AvatarGen**](./TechnicalTopics/AvatarGen-research/) | 数字人/Avatar 生成 | 1 | Wav2Lip→SadTalker→OmniHuman-1，CNN→3DMM→DiT 统一生成 |
| 8  | 🔬 | [**ImageEditing**](./TechnicalTopics/ImageEditing-research/) | 图像编辑与修复 | 1 | GAN→InstructPix2Pix→DiT Joint Attention→Agentic 编辑架构演进 |
| 9  | 🔬 | [**WorldModels**](./TechnicalTopics/WorldModels-research/) | 世界模型 | 1 | action 条件化视频/3D 生成、潜空间预测（JEPA/Dreamer）、world foundation model 平台；判据 = action 条件化 + 系统可调用 + 动力学自数据学得 |
| 10 | 🔬 | [**EmbodiedVLA**](./TechnicalTopics/EmbodiedVLA-research/) | 具身 VLA | 1 | Vision-Language-Action：判据 = 视觉 + 语言条件化 + 直接输出动作；动作表征三路线 token / flow matching / diffusion head；代表 RT-2 · π0 · OpenVLA · GR00T |

> **🔬 技术专题 10 个** &nbsp;|&nbsp; 共 **18 份** Markdown 报告

---

## 📁 仓库结构

```
AIGC-research/
├── ModelSeries/                    # 模型系列报告（8 个）
│   ├── StabilityAI-research/       #   SD 1.x→2.x→XL→3→FLUX 架构演进
│   ├── OpenAI-Gen-research/      #   DALL-E 2/3→GPT-4o→Sora 架构路线
│   ├── Google-Gen-research/      #   Imagen→Veo 级联扩散→DiT 视频
│   ├── Midjourney-research/      #   V4→V7 闭源标杆架构推测
│   ├── Kling-research/             #   可灵 1.0→3.0/O1 DiT 视频生成
│   ├── Runway-research/          #   Gen-1→Gen-4.5 视频编辑与生成
│   ├── ByteDance-Gen-research/   #   Seedance 1.0→2.0 多模态 cinematic
│   └── Alibaba-Gen-research/     #   通义万相 Wan 2.1/2.2/2.6 开源 DiT
│
└── TechnicalTopics/                # 技术专题报告（10 个）
    ├── DiffusionModels-research/   #   扩散模型基础框架与采样加速
    ├── DiT-research/               #   U-Net→DiT 架构革命与 Scaling Law
    ├── VideoGen-research/          #   视频生成时序建模与 3D DiT
    ├── ControllableGen-research/   #   条件注入与可控生成架构
    ├── 3DGen-research/             #   3D 生成 NeRF→Gaussian Splatting
    ├── AudioGen-research/          #   音频生成扩散+自回归+流匹配
    ├── AvatarGen-research/         #   数字人/Avatar 生成 CNN→3DMM→DiT
    ├── ImageEditing-research/      #   图像编辑与修复 GAN→DiT→Agentic
    ├── WorldModels-research/       #   世界模型 action 条件化生成/潜空间预测/WFM 平台
    └── EmbodiedVLA-research/       #   具身 VLA token/flow matching/diffusion head 三路线
```

---

## 🔍 使用方式

```bash
# 克隆统一仓库并进入本报告集
git clone https://github.com/zhoucanzong/ResearchReport.git
cd ResearchReport/AIGC-Research

# 浏览某份报告（库内相对路径不变）
cat ModelSeries/StabilityAI-research/report.md

# 全文搜索（例：搜索所有提到 "DiT" 的报告）
grep -r "DiT" --include="*.md" .
```

---

## ✨ 特色

- 🧠 **AI Agent 生成** — 所有报告由 Agent 自动调研撰写
- 🏗️ **聚焦架构演进** — 重点分析模型结构变迁：U-Net → DiT → 3D DiT
- 📊 **结构化内容** — 统一模板：架构时间线 → 模型结构详解 → 竞品对比
- 🌐 **中英双语** — 报告内容以中文为主，关键术语保留英文
- 🔗 **可追溯** — 附带来源索引、论文原文、架构对比表

---

## 🤝 贡献

欢迎提交 PR 补充新的模型调研、更新过时内容或修正错误。

---

<div align="center">

*Made with ❤️ by AI Agents & [zhoucanzong](https://github.com/zhoucanzong)*

</div>
