# LLaDA2.0: Scaling Up Diffusion Language Models to 100B

## Source and version

- **Paper:** Tiwei Bie et al., *LLaDA2.0: Scaling Up Diffusion Language Models to 100B*, arXiv:2512.15745.
- **Version read:** v2, revised 2025-12-24; 19 pages. The paper page lists v1 on 2025-12-10 and v2 as the current version at time of review (2026-10-23).
- **Full text:** [arXiv HTML, v2](https://arxiv.org/html/2512.15745v2) · [PDF, v2](https://arxiv.org/pdf/2512.15745v2).
- **License:** arXiv.org perpetual, non-exclusive license to distribute. This is the arXiv distribution license, not a Creative Commons reuse grant.
- **Reading evidence:** downloaded the v2 PDF through the PaperFetcher `download` command to `/tmp/paper-fetcher-diffusionlm/2512.15745.pdf` (outside the repository), converted all pages to text for searching, and read the complete paper. Figures 1–6 and Tables 1–2 were checked in the paper; Table 2 and Figures 1, 3–5 are the main evidence cited below.

## Research question and contribution

Can a pretrained autoregressive (AR) model be converted into a large masked-diffusion language model without training a new 100B-scale model from scratch, while retaining useful capability and gaining parallel decoding? LLaDA2.0's central contribution is a staged conversion recipe: first continue training the AR base under diffusion objectives, then train block diffusion at expanding block sizes, switch to full-sequence masked diffusion, and finally return to smaller blocks for inference-time KV-cache reuse.

The released instruction models are LLaDA2.0-mini (16B total parameters) and LLaDA2.0-flash (100B total parameters), both based on the Ling-mini-2.0 and Ling-flash-2.0 AR models. This is a model-conversion and systems result as much as a scaling result; the paper does not report a controlled parameter-scaling curve for diffusion models trained under matched compute.

## Method and workload

**Warmup–Stable–Decay conversion.** During warmup the block size grows through 1, 4, 32, 64, and 4096. At 4096, each training sequence is one fully diffused block. The stable phase trains at that full-sequence setting on large corpora. Decay progressively reduces block size (for example, 4096 to 2048 and eventually 32), recovering blockwise decoding and cache reuse. A document-level attention mask prevents packed examples from attending across document boundaries. The paper also reports top-k checkpoint merging and noise injection into masked-token embeddings early in training to address unstable gradients during AR-to-diffusion conversion.

**Post-training.** The pipeline includes block-diffusion supervised fine-tuning, optional Confidence-Aware Parallel (CAP) training, and DPO. CAP adds an entropy/confidence loss on correctly predicted tokens. DPO estimates masked-token sequence preference scores using an ELBO-based objective; the authors report constructing 1.5 million preference pairs. Inference uses threshold decoding within blocks, accepting sufficiently confident tokens and falling back to a fixed number of top-probability tokens when too few pass the threshold.

**Reported compute and data detail.** The paper identifies the AR starting checkpoints, model sizes, block-size schedule, training objectives, Megatron-LM backend, and distributed-parallelism dimensions (DP, PP, TP, CP, EP). It reports use of cuDNN attention for flexible block masks, with over 1.3× end-to-end speedup and over 90% attention-layer memory savings versus its unfused TransformerEngine implementation on LLaDA2.0-mini. It does **not** give total CPT token count, training steps, hardware type/count, GPU-hours, or a matched-compute budget for the 16B/100B conversion runs. The 1.5M preference pairs are the only explicit post-training dataset size in the paper; SFT and RL dataset totals are not enumerated.

## Evidence and claim audit

- **100B-scale model claim:** Table 2 reports LLaDA2.0-flash at 73.18 average across its listed suite, compared with 73.60 for Qwen3-30B-A3B-Instruct-2507 and 72.15 for Ling-flash-2.0. It is competitive in this reported setup, not a blanket win. For example, its MMLU-Pro score is 73.36 versus 74.23 for Qwen3; its HumanEval score is 94.51 versus 93.29; and its AIME 2025 score is 60.00 versus 61.88.
- **Parallel-decoding benefit:** Figure 3 reports CAP at 4.65 tokens per forward (TPF) and average score 78.57, versus 3.18 TPF and 76.85 for standard LLaDA2.0-flash. In the four task throughput comparison described in §7.3, CAP reaches 535 TPS versus 383 TPS for standard flash, 256 for Ling-flash-2.0, and 237 for Qwen3-30B-A3B-Instruct-2507. This is evidence for the authors' particular serving stack and benchmark setup, not a hardware-independent speed law.
- **Inference settings matter:** the main evaluation uses temperature 0, block size 32, and confidence threshold 0.95. Figure 4 shows that lowering the threshold to 0.85 raises mini TPF to 3.31 but lowers score from the 0.95 setting's 70.15 to 67.90. This speed/quality trade-off is central to interpreting the headline throughput.
- **Long context:** Figure 5 shows RULER scores above 93 for LLaDA2.0-flash through 32k context. The 64k result uses YaRN scaling with factor 2.0 and degrades for both models; it is an extrapolation test, not native 64k performance.
- **Limits on causal attribution:** the evaluations compare a converted model and its post-trained variants with external AR checkpoints. They do not isolate how much performance comes from inherited AR knowledge, WSD, SFT/DPO data, model size, or serving implementation. There is no matched-compute training comparison or uncertainty interval reported for the benchmark aggregates.

## Four highlights

1. **Conversion schedule is the core scaling idea.** WSD treats AR generation as block size 1, progressively exposes the model to larger jointly denoised spans, and then distills back to small blocks. This is a concrete recipe for reconciling global diffusion training with blockwise generation.
2. **The 100B result is competitive, with task-specific strengths and weaknesses.** Table 2 places the flash model near strong AR baselines on the aggregate, while per-task scores vary: code-generation results are strong, but there are clear gaps on some knowledge and mathematics metrics.
3. **CAP turns confidence into decoding parallelism.** The auxiliary confidence objective raises the number of tokens accepted per forward pass; Figure 3 reports a 46% increase in TPF (4.65 vs 3.18) and a 152 TPS increase in the stated four-task comparison (535 vs 383) for flash. These paired results support CAP within the evaluated stack.
4. **The system recipe is part of the result.** Document-level masking, specialized attention kernels, distributed MoE training, and KV-cache reuse all enable the proposed training/inference path. The model's practical throughput cannot be attributed to diffusion alone.

## Limitations and open questions

- The training budget is too sparsely disclosed to assess compute efficiency or reproduce the conversion cost: token counts, steps, hardware, and GPU-hours are absent.
- Comparisons do not control for training data, post-training, parameter activation, or serving stack, so benchmark parity does not establish parity per FLOP or per dollar.
- The aggregate benchmark score has no reported confidence interval, and the evaluation's prompting, sampling, and contamination controls are not described deeply enough here to independently audit every task.
- The block-size schedule and threshold were tuned on a representative subset; transfer of those choices across tasks and deployment contexts is uncertain.
- 64k context requires YaRN extrapolation and loses accuracy relative to the native window.
- The paper says both models are open-sourced, but the arXiv paper's license itself is only a non-exclusive license to distribute. Reuse terms must be checked against the separate model and code licenses.

## Seven questions for follow-up

1. What are the exact token counts, optimization steps, hardware configuration, and GPU-hours for each WSD phase at 16B and 100B?
2. Under equal data, compute, and post-training, how does WSD conversion compare with training an MDLM from scratch and with other AR-to-diffusion conversion recipes?
3. How much of the 100B model is active per token, and how do active parameters and expert routing affect the speed and quality comparisons?
4. Does CAP improve accuracy and TPF consistently across held-out prompts and seeds, or is the reported gain sensitive to the confidence-loss weight and correctness filter?
5. How do thresholds, block size, output length, batch size, and prompt length interact in end-to-end latency and memory use?
6. Can independent serving implementations reproduce the 535 TPS result under fully specified hardware, concurrency, and timing methodology?
7. What are the error profiles of blockwise decoding relative to AR baselines, especially for long-form coherence, tool-call structure, and exact final answers?

## References

- Bie et al., [arXiv:2512.15745v2 full text](https://arxiv.org/html/2512.15745v2), especially §§3–7, Table 2, Figures 1–6.
- [arXiv version history and metadata](https://arxiv.org/abs/2512.15745).
- [arXiv non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html).
