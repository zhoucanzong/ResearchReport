<div align="center" markdown="1">

# ⚙️ Infra

**6 条** · 推理 / 训练基础设施，覆盖投机解码、量化边缘与训练基建。

[← 返回首页](<../README.md>) · [完整索引](<../INDEX.md>)

</div>

<!-- SCRIPT:panel-readme START · 由 scripts/library_index.py 生成，勿手改 -->

![Entries](https://img.shields.io/badge/Entries-6-3f51b5?style=flat-square)
![Panel](https://img.shields.io/badge/Panel-Infra-9e9e9e?style=flat-square)

## 专题内分析

| 所属报告 | 分册入口 |
| --- | --- |
| 模型量化与边缘部署 | [量化感知适配与原生低精度训练：模型从哪里开始量化？](<QuantizationEdge/topics/low-precision-training.md>) |
| 投机解码 | [横切专题①：投机解码的算法家族谱系](<SpeculativeDecoding/topics/algorithm-families.md>) |
| 投机解码 | [扩散语言模型与投机解码：草稿、验证和生成目标](<SpeculativeDecoding/topics/diffusion-drafters.md>) |
| 投机解码 | [横切专题：草稿从哪里来，怎样训练到会被接受](<SpeculativeDecoding/topics/draft-side-and-training.md>) |
| 投机解码 | [草稿位置与验证上下文为何需要不同预算](<SpeculativeDecoding/topics/heterogeneous-budget-allocation.md>) |
| 投机解码 | [横切专题③：系统实现与吞吐—延迟权衡](<SpeculativeDecoding/topics/systems-throughput-latency.md>) |
| 投机解码 | [横切专题②：验证、接受率与无损性的适用条件](<SpeculativeDecoding/topics/verification-acceptance.md>) |

[查看研究专题与分析分册](<../index/by-topic.md>)

## 主报告

| 条目 | 报告 | 规模 |
| :-- | :-- | --: |
| **KV Cache 与预填充／解码分离** | [KV Cache 服务与 Prefill/Decode 分离：什么时候复用，什么时候传输](<KVCachePD/report.md>) | 84 行 |
| **MoE 执行与专家通信** | [MoE 执行：从专家路由到跨设备回收](<MoEExecution/report.md>) | 95 行 |
| **模型量化与边缘部署** | [模型量化与边缘部署研究报告](<QuantizationEdge/report.md>) | 244 行 |
| **在线推理服务与评测** | [在线 LLM Serving：SLO、Goodput 与请求完整性](<ServingEvaluation/report.md>) | 81 行 |
| **投机解码** | [投机解码（Speculative Decoding）技术专题 · 深度调研](<SpeculativeDecoding/report.md>) | 542 行 |
| **分布式训练基础设施** | [大模型训练基础设施与分布式训练研究报告](<TrainingInfra/report.md>) | 295 行 |

## 📎 子文档

<details>
<summary><b>KV Cache 与预填充／解码分离</b>（5 份）</summary>

* [implementation/lmcache-vllm-v1.md](<KVCachePD/implementation/lmcache-vllm-v1.md>) — 67 行 / 14,287 B
* [papers/lmcache-system-paper.md](<KVCachePD/papers/lmcache-system-paper.md>) — 26 行 / 3,198 B
* [papers/mooncake-fast25.md](<KVCachePD/papers/mooncake-fast25.md>) — 21 行 / 3,051 B
* [sources/CANDIDATES.md](<KVCachePD/sources/CANDIDATES.md>) — 13 行 / 1,614 B
* [sources/MANIFEST.md](<KVCachePD/sources/MANIFEST.md>) — 22 行 / 4,882 B

</details>

<details>
<summary><b>MoE 执行与专家通信</b>（3 份）</summary>

* [implementation/deepep-v2-dispatch-compute-combine.md](<MoEExecution/implementation/deepep-v2-dispatch-compute-combine.md>) — 78 行 / 15,317 B
* [papers/2601.17111-llep.md](<MoEExecution/papers/2601.17111-llep.md>) — 45 行 / 5,234 B
* [papers/2606.04101-ultraep.md](<MoEExecution/papers/2606.04101-ultraep.md>) — 49 行 / 6,061 B

</details>

<details>
<summary><b>模型量化与边缘部署</b>（9 份）</summary>

* [papers/2401.06118-aqlm.md](<QuantizationEdge/papers/2401.06118-aqlm.md>) — 23 行 / 2,849 B
* [papers/2402.02750-kivi.md](<QuantizationEdge/papers/2402.02750-kivi.md>) — 21 行 / 2,720 B
* [papers/2404.00456-quarot.md](<QuantizationEdge/papers/2404.00456-quarot.md>) — 29 行 / 3,981 B
* [papers/2405.04532-qserve.md](<QuantizationEdge/papers/2405.04532-qserve.md>) — 21 行 / 2,761 B
* [papers/2405.16406-spinquant.md](<QuantizationEdge/papers/2405.16406-spinquant.md>) — 29 行 / 3,770 B
* [papers/2510.06175-vecinfer.md](<QuantizationEdge/papers/2510.06175-vecinfer.md>) — 25 行 / 3,279 B
* [papers/2606.10531-lc-qat.md](<QuantizationEdge/papers/2606.10531-lc-qat.md>) — 27 行 / 3,718 B
* [papers/2609.39223-qatfactory.md](<QuantizationEdge/papers/2609.39223-qatfactory.md>) — 32 行 / 4,461 B
* [topics/low-precision-training.md](<QuantizationEdge/topics/low-precision-training.md>) — 46 行 / 7,033 B

</details>

<details>
<summary><b>在线推理服务与评测</b>（3 份）</summary>

* [papers/2401.09670-distserve.md](<ServingEvaluation/papers/2401.09670-distserve.md>) — 23 行 / 3,276 B
* [papers/2410.14257-slo-goodput.md](<ServingEvaluation/papers/2410.14257-slo-goodput.md>) — 33 行 / 4,110 B
* [sources/MANIFEST.md](<ServingEvaluation/sources/MANIFEST.md>) — 9 行 / 1,815 B

</details>

<details>
<summary><b>投机解码</b>（68 份）</summary>

* [legacy/speculative-block-diffusion.md](<SpeculativeDecoding/legacy/speculative-block-diffusion.md>) — 230 行 / 18,837 B
* [legacy/speculative-cascade-heterogeneous.md](<SpeculativeDecoding/legacy/speculative-cascade-heterogeneous.md>) — 12 行 / 1,084 B
* [legacy/speculative-classical-and-self.md](<SpeculativeDecoding/legacy/speculative-classical-and-self.md>) — 157 行 / 12,113 B
* [legacy/speculative-domain-language.md](<SpeculativeDecoding/legacy/speculative-domain-language.md>) — 182 行 / 14,598 B
* [legacy/speculative-draft-training-2026.md](<SpeculativeDecoding/legacy/speculative-draft-training-2026.md>) — 199 行 / 15,847 B
* [legacy/speculative-eagle-series.md](<SpeculativeDecoding/legacy/speculative-eagle-series.md>) — 113 行 / 11,905 B
* [legacy/speculative-edge-cloud-hardware.md](<SpeculativeDecoding/legacy/speculative-edge-cloud-hardware.md>) — 182 行 / 18,130 B
* [legacy/speculative-multimodal.md](<SpeculativeDecoding/legacy/speculative-multimodal.md>) — 152 行 / 15,666 B
* [legacy/speculative-stochastic-verification.md](<SpeculativeDecoding/legacy/speculative-stochastic-verification.md>) — 234 行 / 28,412 B
* [legacy/speculative-systems-and-frameworks.md](<SpeculativeDecoding/legacy/speculative-systems-and-frameworks.md>) — 206 行 / 18,540 B
* [legacy/speculative-training-optimization.md](<SpeculativeDecoding/legacy/speculative-training-optimization.md>) — 128 行 / 14,089 B
* [papers/2026.acl-long.353-hcspec.md](<SpeculativeDecoding/papers/2026.acl-long.353-hcspec.md>) — 32 行 / 5,022 B
* [papers/2026.acl-long.589-heterospec.md](<SpeculativeDecoding/papers/2026.acl-long.589-heterospec.md>) — 42 行 / 5,874 B
* [papers/2026.findings-emnlp.2228-pv-decoding.md](<SpeculativeDecoding/papers/2026.findings-emnlp.2228-pv-decoding.md>) — 49 行 / 7,790 B
* [papers/2305.09781-specinfer.md](<SpeculativeDecoding/papers/2305.09781-specinfer.md>) — 201 行 / 15,667 B
* [papers/2401.10774-medusa.md](<SpeculativeDecoding/papers/2401.10774-medusa.md>) — 204 行 / 15,815 B
* [papers/2401.15077-eagle-series.md](<SpeculativeDecoding/papers/2401.15077-eagle-series.md>) — 244 行 / 19,850 B
* [papers/2402.02057-lookahead.md](<SpeculativeDecoding/papers/2402.02057-lookahead.md>) — 202 行 / 15,270 B
* [papers/2402.12374-sequoia.md](<SpeculativeDecoding/papers/2402.12374-sequoia.md>) — 76 行 / 9,166 B
* [papers/2408.11049-magicdec.md](<SpeculativeDecoding/papers/2408.11049-magicdec.md>) — 200 行 / 14,379 B
* [papers/2505.12398-traversal-verification.md](<SpeculativeDecoding/papers/2505.12398-traversal-verification.md>) — 61 行 / 7,601 B
* [papers/2509.18085-spiffy.md](<SpeculativeDecoding/papers/2509.18085-spiffy.md>) — 19 行 / 2,586 B
* [papers/2510.19779-adaspec.md](<SpeculativeDecoding/papers/2510.19779-adaspec.md>) — 49 行 / 5,391 B
* [papers/2511.16665-tlt-adaptive-drafter.md](<SpeculativeDecoding/papers/2511.16665-tlt-adaptive-drafter.md>) — 58 行 / 7,214 B
* [papers/2601.05724-hsd.md](<SpeculativeDecoding/papers/2601.05724-hsd.md>) — 84 行 / 8,788 B
* [papers/2602.05774-vsd.md](<SpeculativeDecoding/papers/2602.05774-vsd.md>) — 66 行 / 7,379 B
* [papers/2602.06036-dflash.md](<SpeculativeDecoding/papers/2602.06036-dflash.md>) — 21 行 / 2,771 B
* [papers/2602.16994-delayed-tree.md](<SpeculativeDecoding/papers/2602.16994-delayed-tree.md>) — 83 行 / 9,007 B
* [papers/2604.12989-ddtree.md](<SpeculativeDecoding/papers/2604.12989-ddtree.md>) — 21 行 / 2,490 B
* [papers/2605.01106-component-aware-self-spec.md](<SpeculativeDecoding/papers/2605.01106-component-aware-self-spec.md>) — 51 行 / 7,035 B
* [papers/2605.09329-test-time-speculation.md](<SpeculativeDecoding/papers/2605.09329-test-time-speculation.md>) — 49 行 / 6,904 B
* [papers/2605.09992-attention-drift.md](<SpeculativeDecoding/papers/2605.09992-attention-drift.md>) — 52 行 / 6,283 B
* [papers/2605.18810-dpace.md](<SpeculativeDecoding/papers/2605.18810-dpace.md>) — 56 行 / 6,035 B
* [papers/2606.01813-caddtree.md](<SpeculativeDecoding/papers/2606.01813-caddtree.md>) — 53 行 / 8,309 B
* [papers/2606.02091-dflare.md](<SpeculativeDecoding/papers/2606.02091-dflare.md>) — 23 行 / 2,424 B
* [papers/2606.08048-poe-bridge.md](<SpeculativeDecoding/papers/2606.08048-poe-bridge.md>) — 17 行 / 2,114 B
* [papers/2606.30265-when-is-draft-accepted.md](<SpeculativeDecoding/papers/2606.30265-when-is-draft-accepted.md>) — 32 行 / 3,833 B
* [papers/2607.05147-dspark.md](<SpeculativeDecoding/papers/2607.05147-dspark.md>) — 50 行 / 7,524 B
* [papers/2607.16673-specla.md](<SpeculativeDecoding/papers/2607.16673-specla.md>) — 85 行 / 10,809 B
* [papers/2607.22634-presto.md](<SpeculativeDecoding/papers/2607.22634-presto.md>) — 19 行 / 2,452 B
* [papers/2608.03447-approximate-sd.md](<SpeculativeDecoding/papers/2608.03447-approximate-sd.md>) — 70 行 / 8,066 B
* [papers/2608.13524-dartree.md](<SpeculativeDecoding/papers/2608.13524-dartree.md>) — 31 行 / 3,850 B
* [papers/2609.06498-dflow.md](<SpeculativeDecoding/papers/2609.06498-dflow.md>) — 56 行 / 8,514 B
* [papers/2609.21827-rheosampling.md](<SpeculativeDecoding/papers/2609.21827-rheosampling.md>) — 216 行 / 15,804 B
* [papers/2609.24150-acceptance-aware-training.md](<SpeculativeDecoding/papers/2609.24150-acceptance-aware-training.md>) — 74 行 / 8,060 B
* [papers/2609.24197-hspec.md](<SpeculativeDecoding/papers/2609.24197-hspec.md>) — 47 行 / 6,070 B
* [papers/2609.33184-specstream.md](<SpeculativeDecoding/papers/2609.33184-specstream.md>) — 44 行 / 5,416 B
* [papers/2610.07350-tlar.md](<SpeculativeDecoding/papers/2610.07350-tlar.md>) — 54 行 / 9,515 B
* [papers/2610.08678-secure-sd.md](<SpeculativeDecoding/papers/2610.08678-secure-sd.md>) — 55 行 / 6,108 B
* [papers/2610.10411-expected-decoding-rounds.md](<SpeculativeDecoding/papers/2610.10411-expected-decoding-rounds.md>) — 56 行 / 7,869 B
* [papers/2610.11750-exit-guided-tree-verification.md](<SpeculativeDecoding/papers/2610.11750-exit-guided-tree-verification.md>) — 56 行 / 7,463 B
* [papers/2610.13708-adaptive-dhisparse.md](<SpeculativeDecoding/papers/2610.13708-adaptive-dhisparse.md>) — 52 行 / 8,113 B
* [papers/2610.23787-dlite.md](<SpeculativeDecoding/papers/2610.23787-dlite.md>) — 48 行 / 6,161 B
* [papers/2610.28355-dpal.md](<SpeculativeDecoding/papers/2610.28355-dpal.md>) — 46 行 / 6,551 B
* [papers/2610.30644-long-position-acceptance.md](<SpeculativeDecoding/papers/2610.30644-long-position-acceptance.md>) — 51 行 / 6,724 B
* [papers/2610.31338-valuspec.md](<SpeculativeDecoding/papers/2610.31338-valuspec.md>) — 33 行 / 4,165 B
* [papers/eagle4-one-flexible-drafter.md](<SpeculativeDecoding/papers/eagle4-one-flexible-drafter.md>) — 211 行 / 19,192 B
* [papers/sglang-implementation.md](<SpeculativeDecoding/papers/sglang-implementation.md>) — 220 行 / 15,358 B
* [papers/vllm-implementation.md](<SpeculativeDecoding/papers/vllm-implementation.md>) — 227 行 / 18,077 B
* [sources/CANDIDATES.md](<SpeculativeDecoding/sources/CANDIDATES.md>) — 111 行 / 15,845 B
* [sources/CODE-AUDIT.md](<SpeculativeDecoding/sources/CODE-AUDIT.md>) — 99 行 / 12,828 B
* [sources/MANIFEST.md](<SpeculativeDecoding/sources/MANIFEST.md>) — 105 行 / 19,614 B
* [topics/algorithm-families.md](<SpeculativeDecoding/topics/algorithm-families.md>) — 166 行 / 12,772 B
* [topics/diffusion-drafters.md](<SpeculativeDecoding/topics/diffusion-drafters.md>) — 130 行 / 20,286 B
* [topics/draft-side-and-training.md](<SpeculativeDecoding/topics/draft-side-and-training.md>) — 107 行 / 17,496 B
* [topics/heterogeneous-budget-allocation.md](<SpeculativeDecoding/topics/heterogeneous-budget-allocation.md>) — 34 行 / 3,978 B
* [topics/systems-throughput-latency.md](<SpeculativeDecoding/topics/systems-throughput-latency.md>) — 232 行 / 20,155 B
* [topics/verification-acceptance.md](<SpeculativeDecoding/topics/verification-acceptance.md>) — 197 行 / 16,883 B

</details>

<details>
<summary><b>分布式训练基础设施</b>（3 份）</summary>

* [papers/2304.11277-pytorch-fsdp.md](<TrainingInfra/papers/2304.11277-pytorch-fsdp.md>) — 52 行 / 8,091 B
* [papers/2401.10241-zero-bubble.md](<TrainingInfra/papers/2401.10241-zero-bubble.md>) — 35 行 / 3,802 B
* [papers/2405.15362-controllable-memory.md](<TrainingInfra/papers/2405.15362-controllable-memory.md>) — 29 行 / 3,941 B

</details>

<!-- SCRIPT:panel-readme END -->

---

<sub>本 README 由 `scripts/library_index.py` 自动生成（`scripts/panels.json` 驱动）；完整索引见 [INDEX.md](<../INDEX.md>) 与 [index/](<../index/>)。</sub>
