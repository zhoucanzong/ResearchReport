# LLaDA2.2: Enabling Agentic Diffusion Language Models via Levenshtein Editing

## Source and version

- **Report:** Tiwei Bie et al., *LLaDA2.2: Enabling Agentic Diffusion Language Models via Levenshtein Editing*, 11-page technical report.
- **Official source:** [InclusionAI publications page](https://www.inclusion-ai.org/LLaDA-Research/papers/) labels it “Technical Report Jul 1, 2026.” The [commit-pinned PDF](https://github.com/inclusionAI/LLaDA2.X/blob/f402f0b52817e1c3586a024ebf89e69ad8ca5523/LLaDA2_2_tech_report.pdf) was uploaded by commit `f402f0b52817e1c3586a024ebf89e69ad8ca5523` on 2026-07-22; the PDF metadata also gives 2026-07-22. The report itself has no version number, so the site date and file date are recorded separately.
- **Identity:** SHA-256 `06e1f341cd08688c9d85ec0a7e0a57bca86555b72e3dac7f71ef69fcf70d2812` (702,354 bytes; 11 pages). The hash was reproduced from the commit-pinned PDF.
- **Authors:** Tiwei Bie, Jiansheng Cai, Maosong Cao, Xiang Cao, Binbin Chen, Fuyuan Chen, Kun Chen, Yuqi Ding, Lun Du, Zhuocheng Gong, Yanmei Gu, Kaiyuan Guan, Xiaoxu Guo, Kairong Han, Zenan Huang, Zijin Huang, Zhenzhong Lan, Chengxi Li, Jianguo Li, Zhe Li, Ruiqi Liang, Xinyao Lin, Huabin Liu, Lin Liu, Xinyi Liu, Xuejie Liu, Guoshan Lu, Yuan Lu, Yuxin Ma, Chenhui Mao, Xiaojing Qi, Kaida Qiu, Xiaoyu Shi, Yiding Tian, Huanyu Wang, Qi Wang, Rui Wang, Shuaidi Wang, Lanning Wei, Tao Wu, Siyang Xiao, Yipeng Xing, Chenkai Xu, Song Yan, Ying Yan, Jingyi Yang, Yichun Yang, Liangyu Zha, Tianze Zhang, Yifan Zhang, Junbo Zhao, Wenqian Zhao, Da Zheng, Jianyuan Zhong, Jiahao Zhou, Junlin Zhou, Tianyu Zhou, Liwang Zhu, and Yihong Zhuang. The report says authors are listed alphabetically by last name and marks Zhenzhong Lan, Jianguo Li, Junbo Zhao, and Da Zheng as technical leads (PDF p. 1).
- **arXiv and license status:** The official publications page lists this as a technical report and links the GitHub PDF, without an arXiv identifier. An exact-title PaperFetcher search found no matching result; its arXiv and OpenAlex requests were rate-limited (HTTP 429), while Semantic Scholar returned an unrelated paper. Thus no arXiv record was verified as of 2026-10-23. The PDF contains no license statement; no reuse license is inferred from the repository’s separate license file.
- **Reading evidence:** Full text extracted from the official PDF to `/tmp/paper-fetcher-diffusionlm/LLaDA2_2_tech_report.txt`; all 11 pages were read. The PDF is at `/tmp/paper-fetcher-diffusionlm/LLaDA2_2_tech_report.pdf`. Figure 4 and Tables 1–3 were checked for the key claims below.

## Research question and contribution

Can a block-diffusion model repair agent outputs that need a different number of tokens, rather than only replacing tokens in fixed positions? LLaDA2.1's Token-to-Token editing (T2T) corrects tokens position by position but cannot insert or delete them. LLaDA2.2 adds Levenshtein editing with keep, substitute, delete, and insert actions, and trains their labels by aligning intermediate drafts to target sequences with longest-common-subsequence (LCS) matching. It also proposes L-EBPO, an environment-reward-based policy optimization method for multi-turn agent trajectories. The report extends context to 128K tokens and changes MoE expert routing to operate on blocks (abstract, pp. 2–5).

This report is a technical-report supplement to the [LLaDA2.1 dossier](LLaDA2.1-Token-Editing.md): its central contribution is structural editing beyond fixed-length T2T replacement. It should be read as an author-reported method and evaluation, not as independently reproduced or peer-reviewed evidence. Version, license status and the official PDF hash are cross-checked in the [source manifest](../sources/MANIFEST.md).

## Method and workload

**LCS-derived edits.** For a draft and target within one block, LCS matches become keep anchors. Positions between anchors are labeled substitute when aligned tokens differ and delete when the draft has surplus positions. When the target has surplus positions in a gap, the following anchor gets one insert label; further missing positions are handled in later edit rounds. The first training round uses ordinary target-token labels; later rounds recompute LCS labels from the updated draft. At inference, delete removes a token and shifts following tokens left. Insert expands the current token into `[MASK]` plus that token so a later denoising step can fill the new slot. Each block is padded with masks or truncated at its tail to restore its fixed length (PDF pp. 4–5, §3.1, Eq. 2–3).

**Agentic RL.** L-EBPO combines outer trajectory decisions across agent turns with inner splice-edit actions within a generation step. Its action space includes vocabulary tokens, `DELETE`, and `INSERT`. Because the structural edit tokens are transient and absent from final text, the report recovers edit traces by aligning noisy rollouts with the original action sequence for likelihood estimation. Rewards sum tool-call correctness, output-format validity, and task completion. The authors describe ASystem orchestration, SGLang rollouts, AKernel sandboxes, and asynchronous rollout and optimization workers (PDF pp. 5–6, §3.2).

**Model and training.** LLaDA2.2 starts from LLaDA2.1. The reported context extension uses 300B tokens at 64K context, then 200B more at 128K. Block routing first admits a fixed pool of experts using the maximum routing score across tokens in a block, then applies token-wise top-k routing within that pool; the default pool is 48 of 256 routed experts (PDF p. 3, §2.1–2.2, Eq. 1, Figure 3). The report gives these training details but does not quantify hardware, optimizer steps, wall-clock time, or compute cost.

## Evidence and claim audit

- **Editing ablation:** On the same LLaDA2.2 base model and identical SWE trajectories, the report varies whether Levenshtein editing is enabled and reports SWE-bench Verified rising from 35.8 to 44.4 (+8.6 points). Figure 4 (PDF p. 5) is the report’s most direct evidence for the editing mechanism. This is an author-reported fine-tuning ablation; the report does not provide uncertainty estimates or independent replication.
- **Agentic task scores:** LLaDA2.2-flash averages 53.83 across seven agentic benchmarks versus 55.74 for Ling-2.6-flash. It scores higher on τ²-Bench (80.33 vs. 76.36), PinchBench (81.66 vs. 81.30), and MCP-Atlas (46.21 vs. 41.12), while trailing on the SWE-bench tasks and nearly matching Ling on Claw-Eval. Table 1 (PDF p. 7) notes the Ling SWE-bench Verified number comes from a different scaffold (OpenHands); LLaDA2.2 uses Claude Code. Its Verified comparison is therefore not scaffold-matched.
- **General tasks:** The report gives a 56.81 average for LLaDA2.2-flash over 10 general benchmarks, versus 65.90 for Ling-2.6-flash and 59.23 for LLaDA2.1-flash. It exceeds Ling on LongBench v2 and is close on Multi-IF, with gaps on several other tasks. Table 2 (PDF p. 7) is the cited source; these broad results do not isolate editing from the model’s other training and infrastructure changes.
- **Throughput:** Table 3 (PDF p. 7) reports LLaDA2.2-flash BF16 throughput faster than Ling-2.6-flash on all 11 listed workloads, with a 1.64× average; FP8 is reported to add 18.6% average throughput over BF16 (§4.3, PDF p. 8). Ling uses four-draft-token multi-token prediction in this evaluation (table note, PDF p. 7). The report does not give enough hardware, concurrency, and timing detail to generalize these TPS figures to other serving setups.
- **Scope of repair:** The authors state that editing can repair local repetitions and structural defects but cannot guarantee valid JSON or tool calls, restore AR-style prefix constraints, or stop all long-horizon goal drift. They also identify INSERT as harder to learn than DELETE (PDF p. 8, §5).

## Four highlights

1. **Editing moves beyond substitution.** LCS supervision teaches keep, substitute, delete, and insert decisions, extending LLaDA2.1's fixed-position T2T correction to drafts with local length errors (PDF pp. 4–5, §3.1).
2. **The editing ablation is directly relevant.** Figure 4 reports an 8.6-point SWE-bench Verified gain when editing is enabled in the otherwise matched fine-tuning comparison (PDF p. 5). This supports investigating edit actions; it does not establish gains across all tasks or settings.
3. **The system targets agent workloads too.** L-EBPO trains edit decisions with environment rewards, while 128K context and block routing address long interaction histories and MoE inference overhead (PDF pp. 3, 5–6, §§2–3).
4. **The trade-offs are visible in the report.** LLaDA2.2-flash is competitive on some interactive-agent benchmarks and reports higher throughput, but its aggregate agentic and general scores trail Ling-2.6-flash. The SWE-bench Verified baseline also uses a different evaluation scaffold (PDF pp. 7–8, Tables 1–3).

## Limitations

- Insertions need the model to detect omitted content and place it correctly; the authors say this is harder to learn than deleting visible repetition. The fixed block is still padded or truncated after edits, so the mechanism has a bounded editing capacity (PDF p. 5, §3.1; p. 8, §5).
- Local edits do not fully prevent early errors from entering context and causing goal drift. The report also acknowledges weak local consistency for strict structured output and multi-argument tool calls (PDF p. 8, §5).
- Agentic benchmark results are reported as means of five runs, but the report gives no confidence intervals. SWE-bench Verified uses different scaffolds for LLaDA2.2 and Ling, limiting direct comparison (PDF p. 7, Table 1 and note).
- Throughput claims lack enough hardware, batch/concurrency, sequence-length, and timing details for portable comparison. The report says Ling uses four draft tokens in the efficiency evaluation but does not establish matched service conditions for arbitrary deployments (PDF p. 7, Table 3 note; p. 8, §4.3).
- The report does not quantify the RL rollout volume, training steps, hardware, or cost, and identifies EBPO efficiency/stability and MoE train–inference discrepancies as unresolved (PDF pp. 3, 8, §§2.1, 5).
- No reproduction was attempted for this dossier; the benchmark figures remain report claims.

## Seven questions for follow-up

1. How does insertion accuracy and placement quality change across tasks, block positions, and repeated edit rounds compared with deletion accuracy?
2. How often does an edit repair a draft versus damage a correct token, and what is the resulting edit budget and latency per agent turn?
3. Do the reported SWE-bench gains persist with matched scaffolds, more seeds, confidence intervals, and independent evaluation?
4. How much of the agentic performance comes from Levenshtein editing, L-EBPO, context extension, or block routing under controlled ablations?
5. How do block size, mask padding or tail truncation, and the one-insert-per-gap rule affect long outputs and structured tool calls?
6. What hardware, concurrency, prompt/output lengths, and timing boundaries produce each TPS value, and how does the speed-quality frontier compare under matched serving conditions?
7. What are the full RL rollout counts, optimization steps, hardware costs, and stability results for L-EBPO, including its ELBO-to-decoding and routing train–inference gaps?

## References

- Bie et al., [official commit-pinned PDF](https://github.com/inclusionAI/LLaDA2.X/blob/f402f0b52817e1c3586a024ebf89e69ad8ca5523/LLaDA2_2_tech_report.pdf), especially §§2–5, Figure 3, Figure 4, Tables 1–3.
- [Official InclusionAI publications page](https://www.inclusion-ai.org/LLaDA-Research/papers/), which lists LLaDA2.2 as a technical report and links the report.
- Bie et al., [LLaDA2.1 arXiv record](https://arxiv.org/abs/2602.08676), cited by the report as prior work.
