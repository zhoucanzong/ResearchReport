# library_index.py 单趟未收敛（自指统计）

**现象**：新增一个条目后再运行一次 `scripts/library_index.py --write-stats`，`INDEX.md` 与 `index/stats.json` 本身又是脏的；必须再跑一次才稳定。

**最小复现**（`main` 上，2026-10-28 实测）：
1. 新建 `OpenSource/TESTX/report.md` 并 `git add`；
2. 跑一次生成器 → 记录 `INDEX.md` / `index/stats.json`；
3. 再跑一次 → 两份文件仍不同：`INDEX.md` 里 `OpenSource/README.md` 一行由 `106 行 / 4,717 B` 变成 `107 行 / 4,782 B`；根 `README.md` 由 `14,530 B` 变成 `14,514 B`；`content_fingerprint` 两次不同。
4. 第三次运行才与第二次一致（收敛）。

**原因**：生成器统计的文件集合包含它自己正在重写的面板 `README.md`，因此首趟按**改写前**的内容统计，必然少算自己刚新增的那一行（≈1 行 / 99 B）。

**期望**：单次运行后即达到稳定状态；或明确在 `--write-stats` 内做两趟（先写面板，再统计写回），让一次调用自洽。

**影响**：所有"新增条目 → 跑生成器 → 提交"的流程都会带进一份 stale 统计；CI 若只跑一次生成器并断言 0 diff，会把正常流程判成失败，或反过来漏掉真实漂移。
