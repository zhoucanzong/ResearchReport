<div align="center" markdown="1">

# ⚙️ Infra

**6 条** · 推理 / 训练基础设施，覆盖投机解码、量化边缘与训练基建。

[← 返回首页](<../README.md>) · [完整索引](<../INDEX.md>)

</div>

<!-- SCRIPT:panel-readme START · 由 scripts/library_index.py 生成，勿手改 -->

![Entries](https://img.shields.io/badge/Entries-6-3f51b5?style=flat-square)
![Panel](https://img.shields.io/badge/Panel-Infra-9e9e9e?style=flat-square)

| 条目 | 报告 | 规模 |
| :-- | :-- | --: |
| **KVCachePD** | [KV Cache 服务与 Prefill/Decode 分离：什么时候复用，什么时候传输](<KVCachePD/report.md>) | 84 行 |
| **MoEExecution** | [MoE 执行：token 如何抵达专家，又如何回到原序](<MoEExecution/report.md>) | 25 行 |
| **QuantizationEdge** | [模型量化与边缘部署研究报告](<QuantizationEdge/report.md>) | 188 行 |
| **ServingEvaluation** | [在线 LLM Serving：SLO、Goodput 与请求完整性](<ServingEvaluation/report.md>) | 81 行 |
| **SpeculativeDecoding** | [投机解码（Speculative Decoding）技术专题 · 深度调研](<SpeculativeDecoding/report.md>) | 549 行 |
| **TrainingInfra** | [大模型训练基础设施与分布式训练研究报告](<TrainingInfra/report.md>) | 181 行 |

## 📎 子文档

<details>
<summary><b>KVCachePD</b>（5 份）</summary>

* [implementation/lmcache-vllm-v1.md](<KVCachePD/implementation/lmcache-vllm-v1.md>) — 67 行 / 14,287 B
* [papers/lmcache-system-paper.md](<KVCachePD/papers/lmcache-system-paper.md>) — 26 行 / 3,198 B
* [papers/mooncake-fast25.md](<KVCachePD/papers/mooncake-fast25.md>) — 21 行 / 3,051 B
* [sources/CANDIDATES.md](<KVCachePD/sources/CANDIDATES.md>) — 13 行 / 1,614 B
* [sources/MANIFEST.md](<KVCachePD/sources/MANIFEST.md>) — 22 行 / 4,882 B

</details>

<details>
<summary><b>MoEExecution</b>（1 份）</summary>

* [implementation/deepep-v2-dispatch-compute-combine.md](<MoEExecution/implementation/deepep-v2-dispatch-compute-combine.md>) — 78 行 / 15,317 B

</details>

<details>
<summary><b>ServingEvaluation</b>（3 份）</summary>

* [papers/2401.09670-distserve.md](<ServingEvaluation/papers/2401.09670-distserve.md>) — 23 行 / 3,276 B
* [papers/2410.14257-slo-goodput.md](<ServingEvaluation/papers/2410.14257-slo-goodput.md>) — 33 行 / 4,110 B
* [sources/MANIFEST.md](<ServingEvaluation/sources/MANIFEST.md>) — 9 行 / 1,815 B

</details>

<details>
<summary><b>SpeculativeDecoding</b>（33 份）</summary>

* [legacy/speculative-block-diffusion.md](<SpeculativeDecoding/legacy/speculative-block-diffusion.md>) — 230 行 / 18,588 B
* [legacy/speculative-cascade-heterogeneous.md](<SpeculativeDecoding/legacy/speculative-cascade-heterogeneous.md>) — 141 行 / 11,829 B
* [legacy/speculative-classical-and-self.md](<SpeculativeDecoding/legacy/speculative-classical-and-self.md>) — 157 行 / 12,113 B
* [legacy/speculative-domain-language.md](<SpeculativeDecoding/legacy/speculative-domain-language.md>) — 182 行 / 14,598 B
* [legacy/speculative-draft-training-2026.md](<SpeculativeDecoding/legacy/speculative-draft-training-2026.md>) — 199 行 / 15,583 B
* [legacy/speculative-eagle-series.md](<SpeculativeDecoding/legacy/speculative-eagle-series.md>) — 113 行 / 11,905 B
* [legacy/speculative-edge-cloud-hardware.md](<SpeculativeDecoding/legacy/speculative-edge-cloud-hardware.md>) — 182 行 / 18,130 B
* [legacy/speculative-multimodal.md](<SpeculativeDecoding/legacy/speculative-multimodal.md>) — 152 行 / 15,666 B
* [legacy/speculative-stochastic-verification.md](<SpeculativeDecoding/legacy/speculative-stochastic-verification.md>) — 234 行 / 28,412 B
* [legacy/speculative-systems-and-frameworks.md](<SpeculativeDecoding/legacy/speculative-systems-and-frameworks.md>) — 206 行 / 18,397 B
* [legacy/speculative-training-optimization.md](<SpeculativeDecoding/legacy/speculative-training-optimization.md>) — 128 行 / 14,089 B
* [papers/2305.09781-specinfer.md](<SpeculativeDecoding/papers/2305.09781-specinfer.md>) — 201 行 / 15,667 B
* [papers/2401.10774-medusa.md](<SpeculativeDecoding/papers/2401.10774-medusa.md>) — 204 行 / 15,815 B
* [papers/2401.15077-eagle-series.md](<SpeculativeDecoding/papers/2401.15077-eagle-series.md>) — 244 行 / 19,850 B
* [papers/2402.02057-lookahead.md](<SpeculativeDecoding/papers/2402.02057-lookahead.md>) — 202 行 / 15,270 B
* [papers/2408.11049-magicdec.md](<SpeculativeDecoding/papers/2408.11049-magicdec.md>) — 200 行 / 14,379 B
* [papers/2601.05724-hsd.md](<SpeculativeDecoding/papers/2601.05724-hsd.md>) — 84 行 / 8,788 B
* [papers/2602.16994-delayed-tree.md](<SpeculativeDecoding/papers/2602.16994-delayed-tree.md>) — 83 行 / 9,007 B
* [papers/2606.01813-caddtree.md](<SpeculativeDecoding/papers/2606.01813-caddtree.md>) — 53 行 / 8,309 B
* [papers/2608.13524-dartree.md](<SpeculativeDecoding/papers/2608.13524-dartree.md>) — 31 行 / 3,850 B
* [papers/2609.21827-rheosampling.md](<SpeculativeDecoding/papers/2609.21827-rheosampling.md>) — 216 行 / 15,804 B
* [papers/2609.33184-specstream.md](<SpeculativeDecoding/papers/2609.33184-specstream.md>) — 44 行 / 5,416 B
* [papers/2610.07350-tlar.md](<SpeculativeDecoding/papers/2610.07350-tlar.md>) — 54 行 / 9,515 B
* [papers/2610.08678-secure-sd.md](<SpeculativeDecoding/papers/2610.08678-secure-sd.md>) — 55 行 / 6,108 B
* [papers/2610.23787-dlite.md](<SpeculativeDecoding/papers/2610.23787-dlite.md>) — 48 行 / 6,161 B
* [papers/sglang-implementation.md](<SpeculativeDecoding/papers/sglang-implementation.md>) — 220 行 / 15,358 B
* [papers/vllm-implementation.md](<SpeculativeDecoding/papers/vllm-implementation.md>) — 227 行 / 18,077 B
* [sources/CANDIDATES.md](<SpeculativeDecoding/sources/CANDIDATES.md>) — 91 行 / 9,644 B
* [sources/CODE-AUDIT.md](<SpeculativeDecoding/sources/CODE-AUDIT.md>) — 99 行 / 12,828 B
* [sources/MANIFEST.md](<SpeculativeDecoding/sources/MANIFEST.md>) — 65 行 / 9,872 B
* [topics/algorithm-families.md](<SpeculativeDecoding/topics/algorithm-families.md>) — 164 行 / 12,014 B
* [topics/systems-throughput-latency.md](<SpeculativeDecoding/topics/systems-throughput-latency.md>) — 168 行 / 10,532 B
* [topics/verification-acceptance.md](<SpeculativeDecoding/topics/verification-acceptance.md>) — 173 行 / 11,577 B

</details>

<!-- SCRIPT:panel-readme END -->

---

<sub>本 README 由 `scripts/library_index.py` 自动生成（`scripts/panels.json` 驱动）；完整索引见 [INDEX.md](<../INDEX.md>) 与 [index/](<../index/>)。</sub>
