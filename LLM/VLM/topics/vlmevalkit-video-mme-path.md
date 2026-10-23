# VLMEvalKit 如何把 Video-MME 的回答变成分数

> 本文追一条固定实现路径：VLMEvalKit commit [`4d0dc8096b2ee365491c469088cc462ae1fb6041`](https://github.com/open-compass/VLMEvalKit/commit/4d0dc8096b2ee365491c469088cc462ae1fb6041) 中，`Video-MME_8frame` 配置配合 `Qwen2.5-VL-7B-Instruct`。依据该版本源码静态阅读；未下载数据集、未运行推理或评测。

从配置、prompt、生成和评测代码可以看出，分数是“样本与帧输入 → 模型协议 → 文本答案抽取 → 选项对错 → 分组平均”串起来的结果；据此推断，链上任一层的变化都可能改变最终数字。[配置与样本构造](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/video_dataset_config.py#L88-L95) [模型输入与生成](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/vlm/qwen2_vl/model.py#L345-L396) [解析与评分](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/videomme.py#L273-L305) [分组聚合](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/utils/videomme.py#L74-L118)。下面具体说的是本条路径；不同模型可能收到不同形式、甚至不同采样时刻的视频输入，因此相同 benchmark 名称和帧数标签不足以证明输入完全一致。

```mermaid
flowchart LR
    A[Video-MME_8frame 配置] --> B[VideoMME TSV 样本]
    B --> C[原视频路径 + 题目选项]
    C --> D[Qwen adapter 请求 nframes=8]
    D --> E[Qwen 视频预处理与生成]
    E --> F[模型回答文本]
    F --> G[A-D 抽取；必要时 judge 回退]
    G --> H[逐题 0/1 或 -1]
    H --> I[有效样本分组平均]
```

图中 VLMEvalKit 内的配置、prompt、推理、解析和聚合分别由下文链接的固定版本源码支持；Qwen 外部预处理库内部的取帧细节没有展开。

## 从配置名到样本输入

`Video-MME_8frame` 在预设表中对应 `VideoMME(dataset='Video-MME', nframe=8)`；未设置 `use_subtitle`，类构造器默认关闭字幕。[预设配置](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/video_dataset_config.py#L5-L17) [Video-MME 别名](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/video_dataset_config.py#L88-L95) [类默认参数](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/videomme.py#L59-L70)

数据准备从 `lmms-lab/Video-MME` 快照读取压缩视频和字幕，并将 parquet 元数据整理为 TSV：建立 index、视频路径、字幕路径、候选选项和答案列。[准备与表格转换](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/videomme.py#L72-L165) 这一步定义样本的元数据与文件对应关系；源码检查 TSV 的 MD5 和表内视频路径是否存在，但不能保证视频内容可解码或其字幕与视频语义正确。

该配置走视频专用推理分支。对本例的 Qwen adapter，模型类声明 `VIDEO_LLM=True`。推理器将 adapter 的 `nframe` 同步为 dataset 的 8，并因 dataset 未设正 fps 而把 adapter `fps` 置空；随后调用 `VideoMME.build_prompt(..., video_llm=True)`。[模型配置](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/config.py#L2006-L2012) [Qwen 类视频能力](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/vlm/qwen2_vl/model.py#L175-L179) [视频分支与采样参数同步](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/inference_video.py#L165-L207) [主入口选择视频推理器](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/run.py#L834-L846)

由于 `video_llm=True` 且未启用字幕，数据集 prompt 不在 VLMEvalKit 里把 MP4 拆成图片；它传递原视频路径，加上要求只回答 A/B/C/D 的文字指令与题目选项。[Video-MME prompt 构造](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/videomme.py#L202-L240) Qwen adapter 将其转换为原生 video 内容项，并设置 `nframes=8`，再交给 `qwen_vl_utils.process_vision_info` 和处理器生成视觉张量。[Qwen 内容预处理](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/vlm/qwen2_vl/model.py#L335-L396) [Transformers 视频推理与解码](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/vlm/qwen2_vl/model.py#L486-L547)

这里的“8 帧”是交给 Qwen 视频预处理器的请求参数，不足以单独确定具体帧的时间戳、解码与缩放细节；这些由外部 `qwen_vl_utils`、视频解码库和处理器共同决定。VLMEvalKit 的源码路径没有固定这些依赖内部的采样选择，所以仅凭本仓库不能证明该模型最终看到的八个时刻。

同一个 `Video-MME_8frame` 也不意味着所有模型遵循同一个输入协议。若模型声明 `VIDEO_LLM=False`，`VideoMME.build_prompt` 会调用数据集的 `save_video_frames`，使用 decord 按等间隔索引抽出 8 张图片，再把图片项送给模型；Qwen 本例则传整段视频，由 adapter 的视频预处理流程取帧。[数据集抽帧与 prompt 分支](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/videomme.py#L167-L240) 两者共享“目标帧数”的配置意图，但帧时间位置、解码器、图像变换和模型侧视频封装可能不同。跨模型比较因此同时比较了模型与输入管线；如果研究目标是模型差异，应检查实际送入的帧，而不能只对齐配置名。

## 从生成文本到计分

Qwen 路径使用处理器模板化消息、调用模型生成，再跳过特殊 token 解码为字符串。Video-MME 要求模型只返回选项字母，但评测器仍需从任意输出文本中抽取答案。[生成过程](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/vlm/qwen2_vl/model.py#L486-L547) [提示中的输出协议](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/videomme.py#L45-L57)

评测器先取输出中第一个 A–D 字母作为预测，再和标注答案精确比较；若没有可抽取字母，则尝试使用 judge 从完整题目与选项抽答案。若 judge 也失败，该样本记为 `-1`。分数随后按时长、领域、子类别和任务类型分桶；整体分数是所有非负样本分数的算术平均，`-1` 不进入均值。[选项抽取与正则解析](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/utils/videomme.py#L121-L152) [逐样本评分与 judge 回退](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/videomme.py#L242-L305) [维度均值](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/utils/videomme.py#L74-L118)

这套解析会产生两类需要谨慎解释的样本。第一，若输出里出现多个 A–D 字母，代码取第一个匹配项；解析结果可能并非模型最终意图。第二，没有匹配项才触发 judge 回退，因此某些格式异常但含选项字母的输出不会暴露为解析失败。解析器的某些答案前缀字符串还因列表元素间缺少逗号而发生拼接，但当前逻辑随后仍按 A–D 字母搜索；这也说明“代码抽到一个字母”不等于“模型遵守了只输出字母的协议”。[前缀与字符匹配实现](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/utils/videomme.py#L130-L152)

## 如何区分管线错误与模型错误

源码提供的是若干局部信号，并未给错误建立完整、互斥的归因标签：

- **准备或解码阶段失败**：例如找不到视频、文件损坏或解码器失败，属于样本/输入管线问题。某些 RuntimeError 可在 `SKIP_ERR=1` 时记录为失败字符串；未被捕获的异常则由运行入口记录为该模型与数据集组合失败。[推理异常处理](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/inference_video.py#L211-L232) [组合级异常记录](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/run.py#L1058-L1073)
- **模型输出无法解析**：无 A–D 字母时会进入 judge 回退；judge 成功就照其抽出的选项计分，judge 失败才记 `-1`。`-1` 被整体平均排除，因此同时报告完整有效样本数和解析失败数很重要。[回退和失败分数](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/videomme.py#L273-L305) [均值排除负分](https://github.com/open-compass/VLMEvalKit/blob/4d0dc8096b2ee365491c469088cc462ae1fb6041/vlmeval/dataset/utils/videomme.py#L101-L118)
- **解析成功但答案错误**：记为 0。这可能是模型理解或推理错误，也可能源于输入帧遗漏、字幕/题目数据错配、预处理差异或解析器误取字母；仅凭一个 0 分不能区分这些原因。

因此，公平解释一项 Video-MME 分数至少需要同时看推理失败数、有效计分分母和实际输入协议。想把错误归因到模型能力，还需额外检查样本的视频解码与抽帧、输出原文及解析结果；VLMEvalKit 这段静态路径本身没有自动完成这种因果归因。本文没有运行模型或 benchmark，以上是固定版本源码可支持的执行路径与限制判断。
