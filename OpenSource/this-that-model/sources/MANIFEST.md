# this-that-model 源码证据与复核边界

- 复核：2026-10-22，使用 `code-researcher deep`（evidence-quality、runtime-story、reading-coverage、claim-audit），重新运行官方 `scan_repo.py`。
- 固定来源：[FLock-io/this-that-model@6af11c63c8bb260aa4bed2b7717f33f25decd16e](https://github.com/FLock-io/this-that-model/tree/6af11c63c8bb260aa4bed2b7717f33f25decd16e)；[源码tarball](https://codeload.github.com/FLock-io/this-that-model/tar.gz/6af11c63c8bb260aa4bed2b7717f33f25decd16e)。
- 仓库外临时阅读目录：`/tmp/research-code-audit-20261022/this-that`；上游源码未入库，未构建或执行上游系统。临时目录不是长期保存承诺，可按固定SHA重新取源。
- 本轮核验的是下列强结论和运行切面，**不是全上游仓库逐行读完、测试全通过或所有配置行为已证实**。旧报告的机械零告警不代表语义通过。

- Traced/Audited：`thisthat/model.py:105-147` → `backends/torch_backend.py:75-88`（骨干/标签行投影）→ `model.py:134-141`（归一化和Decision）→ `types.py:52-53`（confidence）/ `server.py:103`（输出）。
- Audited：`tests/test_published_results.py:49-58`是已存在的校准测试定义，本轮未跑权重/测试；一次chunk前向不等于多问题统计条件独立。
- 本轮HF配置单独固定到 [`flock-io/this-that-model-1.0@3d927195c4f9845efe66c5715883a7a0f42b1239`](https://huggingface.co/flock-io/this-that-model-1.0/blob/3d927195c4f9845efe66c5715883a7a0f42b1239/config.json)；`tie_word_embeddings`是配置声明，不是已下载权重逐字节等同的证明。
- 训练未在已读推理/脚本实现中找到；字面搜索零命中不足以排除仓外训练或校准损失。
- 未核：权重数值/模型参数总数复算、部署延迟复现、预印本训练细节、所有HTTP协议边界。

引用格式：本条目的简写 `文件:行` 均相对上述固定源码根；回源使用 `https://github.com/FLock-io/this-that-model/blob/6af11c63c8bb260aa4bed2b7717f33f25decd16e/<path>#L<line>`。保留旧阅读记录不将其覆盖等级自动升级成本轮已核。
