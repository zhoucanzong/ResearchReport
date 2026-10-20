# 🔍 校验记录 · Verification Log

本文件保存 **ResearchReport** 仓库的全部校验留证：上游仓库最终状态、复制阶段校验、扁平化校验、Repo-Research 复制与移除留证。

仓库首页 [README](../README.md) 只保留摘要；体积与数量的完整统计见 [statistics.md](statistics.md)；维护流程见 [maintenance.md](maintenance.md)。

**目录**

1. [上游原始仓库最终状态](#1-上游原始仓库最终状态本地副本已于-2026-10-16-移除)
2. [复制阶段校验（扁平化前）](#2-复制阶段校验扁平化前历史留证)
3. [扁平化与新仓库校验](#3-扁平化与新仓库校验)
4. [Repo-Research 复制与移除校验](#4-repo-research-复制与移除校验2026-10-16)

---

## 1. 上游原始仓库最终状态（本地副本已于 2026-10-16 移除）

（**历史记录**）`AIGC-Research`、`LLM-Research` 在复制与校验阶段**只读、全程未改动**（见本文 §2），其最终状态如下。后续决定「统一维护 ResearchReport」，两个本地原始目录已于 **2026-10-16** 移入废纸篓（`~/.Trash/AIGC-Research`、`~/.Trash/LLM-Research`），可从废纸篓恢复，直至清空废纸篓。

| 校验项 | AIGC-Research | LLM-Research |  <!-- 历史记录：重排前旧库路径 -->
| :-- | :-- | :-- |
| 原路径 | `/Users/zhoucanzong/Documents/AIGC-Research`（已移除） | `/Users/zhoucanzong/Documents/LLM-Research`（已移除） |
| `rev-parse HEAD` | `101ae640ea043572f2c6dc64742eb520394c1d3e` | `7deacb5b841c0b0925e1ac024323255b1b7eaf58` |
| `log -1` | `初步调研AIGC` · zhoucanzong \<zhoucanzong@gmail.com\> · 2026-06-07 23:19:52 +0800 | `修正readme` · zhoucanzong \<zhoucanzong@gmail.com\> · 2026-06-07 01:18:47 +0800 |
| `status --short` | `?? .DS_Store`（未跟踪，来源既有状态） | （空 → 干净） |
| `remote -v` | `origin  git@github.com:zhoucanzong/AIGC-Research.git`（fetch/push） | `origin  git@github.com:zhoucanzong/LLM-Research.git`（fetch/push） |
| 提交数 / 分支 | 1 · `main` | 7 · `main` |
| 本地目录处置 | 🗑️ 2026-10-16 移入废纸篓 | 🗑️ 2026-10-16 移入废纸篓 |
| 历史留存位置 | GitHub 存档仓库，删除前核对 `refs/heads/main` = `101ae64…` ✅ | GitHub 存档仓库，删除前核对 `refs/heads/main` = `7deacb5…` ✅ |

> 上述两个 GitHub 存档仓库（`git@github.com:zhoucanzong/AIGC-Research.git`、`git@github.com:zhoucanzong/LLM-Research.git`）是否继续保留由维护者决定；此后 **ResearchReport 是唯一在维护的仓库**。

---

## 2. 复制阶段校验（扁平化前，历史留证）

复制方式：`cp -a <源> Research/<名称>`（保留权限、时间戳与 `.git`）。当时两个副本各含完整 `.git`，校验结论如下 —— 该 `.git` 现已按计划删除（见本文 §3）。

| 校验项 | AIGC-Research | LLM-Research |  <!-- 历史记录：重排前旧库路径 -->
| :-- | :-- | :-- |
| 工作区 `.md` 数量（源 → 副本） | 17 → **17** | 37 → **37** |
| `report.md` 数量（源 → 副本） | 16 → **16** | 25 → **25** |
| 全部普通文件数（源 → 副本） | 80 → **80** | 206 → **206** |
| 工作区文件 SHA-256 逐文件比对 | ✅ 全部一致（18 个非 `.git` 文件） | ✅ 全部一致（42 个非 `.git` 文件） |
| `.git` 内文件 SHA-256 比对 | ⚠️ 仅 `.git/index` 不同（stat cache） | ⚠️ 仅 `.git/index` 不同（stat cache） |
| HEAD tree（源 = 副本） | ✅ `ca974128baf589ecbaf2ed4d9af2bee1b18f2852` | ✅ `fd6ccaf955341f9b7e28de5443862cb578f4eff9` |
| `git fsck --full --strict` | ✅ exit 0，无输出 | ✅ exit 0，无输出 |

---

## 3. 扁平化与新仓库校验

### 3.1 嵌套 `.git` 已删除（依据：内容完全由上游保留，删除不丢失任何历史）

删除前逐项留证，证明两个嵌套 `.git` 与上游仓库**逐字节等价**（仅 `index` 这个 stat cache 文件不同），且**副本中的每一个对象都能在上游仓库中按同一 SHA 找到**：

| 证据 | AIGC-Research | LLM-Research |
| :-- | :-- | :-- |
| `rev-parse HEAD`（副本 = 上游） | `101ae64…` = `101ae64…` ✅ | `7deacb5…` = `7deacb5…` ✅ |
| `show-ref` 校验和（副本 = 上游） | `0ed5835…` ✅ | `4b14806…` ✅ |
| `count-objects`（副本 = 上游） | 37 objects ✅ | 136 objects ✅ |
| 副本对象是否存在于上游 | ✅ 37/37 命中，无缺失 | ✅ 113/113 可达对象命中，无缺失 |
| 全量 `.git` 文件 SHA-256 比对 | 62 个文件，仅 `index` 不同 | 164 个文件，仅 `index` 不同 |
| `git fsck --full --strict`（删除前） | exit 0，无输出 | exit 0，无输出 |
| 已删除路径（绝对路径已实时校验） | `/Users/zhoucanzong/Documents/Research/AIGC-Research/.git` | `/Users/zhoucanzong/Documents/Research/LLM-Research/.git` |

> 结论：这两个 `.git` 只是上游仓库的同构副本，**没有任何仅存于副本的提交、分支、tag 或对象**；其历史仍完整保存在上游独立仓库（`AIGC-Research` 1 次 commit、`LLM-Research` 7 次 commit，均可 `git log` 追溯）。因此删除它们是安全的，也是让本仓库能扁平推送的**必要步骤** —— 保留嵌套 `.git` 会使 `git add` 只记录一个 gitlink（mode 160000），推送后目录内容为空。
> `Repo-Research` 无需此步骤：它**本来就不是 Git 仓库**，直接以普通文件纳入。

### 3.2 仓库结构校验

| 检查项 | 结果 |
| :-- | :-- |
| 根目录是否为 Git 仓库 | ✅ 是（`.git` 仅存在于 `/Users/zhoucanzong/Documents/Research/.git`） |
| 是否存在嵌套 `.git` | ✅ 不存在（三个子目录均为普通目录） |
| 缺失模式检查 `git ls-files -s \| awk '{print $1}' \| sort \| uniq -c` | ✅ **仅 `66 100644`**，gitlink（`160000`）计数 **0** |
| 是否存在 submodule | ✅ 无 `.gitmodules` |
| `git ls-files \| wc -l` | ✅ **66** |
| `git ls-files '*.md' \| wc -l` | ✅ **63**（52 份报告 + 8 份 Repo 深读 + 3 个 README） |
| AIGC / LLM 报告是否全部被跟踪 | ✅ AIGC 16/16 + LLM 36/36 = **52/52** |
| Repo-Research 文件是否全部被跟踪 | ✅ **9/9**（8 个 `.md` + 1 个 `.json`） |
| `git status --short`（提交后） | ✅ **空**（干净；`.claude/settings.local.json` 被全局 gitignore 忽略，不产生噪声） |
| 提交者身份 | `zhoucanzong <zhoucanzong@gmail.com>`（来自全局 `~/.gitconfig`，未设置任何 BotHarness 身份） |
| GPG 签名 | 未启用（`commit.gpgsign` 未设置） |
| 提交 SHA / 分支 / remote | 见 `git log -1`、`git branch --show-current`、`git remote -v` |

> ⏱ **统计时点**：上表的跟踪文件数为**该次校验时**的值（66 个跟踪文件 / 63 个 `.md`）。随着 `docs/` 等内容的加入，当前计数会增加；**最新值以 [statistics.md](statistics.md) 为准**。

---

## 4. Repo-Research 复制与移除校验（2026-10-16）

（**历史记录**）来源 `/Users/zhoucanzong/Documents/Repo-Research`（**非 Git 仓库**，无 `.git`）→ 目标 `Research/Repo-Research/`。流程为**先复制、校验通过后才移除原位**。

| 校验项 | 结果 |
| :-- | :-- |
| 复制方式 | `cp -a`（目标不存在时执行；执行前已确认目标不存在） |
| 源 / 副本文件数（排除 `.DS_Store`） | 9 → **9** ✅ |
| 源 / 副本总字节（排除 `.DS_Store`） | 189,061 B → **189,061 B** ✅ |
| **逐文件 SHA-256 比对** | ✅ **9/9 完全一致**，无差异、无缺失 |
| 副本内 `.DS_Store` | 🗑️ 已删除（源含 1 个 `.DS_Store`，按维护要求不复制、不提交） |
| 副本 `du -sk` | 204 KB（源 212 KB；差额来自已删除的 `.DS_Store`） |
| 移除前 `realpath` 确认 | ✅ `/Users/zhoucanzong/Documents/Repo-Research`（与目标路径完全一致） |
| 移除前废纸篓冲突检查 | ✅ `~/.Trash/Repo-Research` 当时不存在，无需改用带时间戳的名字 |
| 原位处置方式 | `mv`（**不是 `rm -rf`**）→ `~/.Trash/Repo-Research` |
| 移除后确认 | ✅ `~/Documents/Repo-Research` 已不存在；`~/.Trash/Repo-Research` 存在，`du -sk` = **212 KB**、10 个文件（含 `.DS_Store`），与源一致 |
| 取证方式说明 | macOS TCC 禁止 `ls ~/.Trash/`（Operation not permitted），故改用**直接路径** `stat` / `du` / `find` 取证 |
| 备份状况 | ⚠️ Repo-Research **没有上游 Git 存档**，仓库内副本是主副本，废纸篓副本是**唯一**可恢复的旧位置（清空废纸篓后不可恢复） |

逐文件 SHA-256（源 = 副本，9/9 一致）：

```
e2e60cc59547de1209aa773abea8e8a39ee78ba8181c42e040a771073d51d0a3  mini-swe-agent-research/mini-swe-agent-deep-report.md
d6ed2728b89cd3c0df175589442b0bee5dccb867558b54612fb5fe9d82289b4a  nemotron-tri-mode-diffusion/report.md
84132eaf20f60a97cb884739565c5ddcd628634faff7ae684c1a8ac64a64d58d  nemotron-tri-mode-diffusion/plan.md
433f81d51cc7376c032bc134dc220f0cef639607d95a02c81cdaeffd711aa354  nemotron-tri-mode-diffusion/knowledge-graph.md
160cf5b3218345e2fa4d492c5c51807044cea1e5a1eb0e5d8391fb767c109d5b  nemotron-tri-mode-diffusion/sources-index.md
91700645a85dc9b1b3183fb7948552a11a6667f225506478d98397f078a24f76  nemotron-tri-mode-diffusion/notes/structured-reading.md
add59912f210a242d8cd988d54303dac8cabefc78ce94d55008c5b26e8e5d710  nemotron-tri-mode-diffusion/raw-extracts/nemotron-tri-mode-fulltext.md
82c0c591022421004c40ed26239206da1369d3172dad2332f11d90d784f626bb  nemotron-tri-mode-diffusion/raw-extracts/pdf-fu_等__…dif.md
1faa4df3e1123a026e085d91f02ddf7f5ce290d8291b8c0fb4e819e9e199f985  nemotron-tri-mode-diffusion/papers/nemotron-labs-diffusion.json
```

---

## 5. SGLang 条目新增校验（2026-10-16）

新增条目 `OpenSource/sglang/`（1 条目 + 3 子文档）。分析对象为外部开源仓库，**源码不入口**：clone 只放 `/tmp`，读完即删，仓库内只保留报告文本与 `文件:行` 短引用。

| 校验项 | 结果 |
| :-- | :-- |
| 分析对象版本 | `sgl-project/sglang` @ `2a08e261ecd4cdfb04ec354f9005f18b88108b7d`（2026-10-16 13:24:48 +0800） |
| clone 位置 | `/tmp/sglang-clone`（`--filter=blob:none` 部分克隆，**只读**，未构建、未修改），校验后删除 |
| 仓库内是否含源码 / 克隆残留 | ✅ 无：`git status --porcelain` 只有新增的 4 个 `.md`；无 `.py` / `.rs` / `.cuh` 等源文件 |
| 报告内单处引用长度 | ✅ 全部 ≤ 15 行（实际最长 4 行，均为 `文件:行` 标注的短引用） |
| 结论审计（`claim_audit.py --lang zh`） | ✅ 4 份文档全部 **0 处缺少邻近源码证据**（高影响结论数：report 9 / spec-path 3 / scheduler-prefix 5 / claim-audit 12；口径见 [claim-audit.md §2](../OpenSource/sglang/claim-audit.md)） |
| GitHub 链接钉 SHA | ✅ 124 处「默认分支路径」链接（`blob` + 分支名）全部改为 `blob/2a08e261ecd4cdfb04ec354f9005f18b88108b7d`；全仓 `grep -ro` 该默认分支路径 = 0（命中数 92 行 / 124 处） |
| 行号更正 | ✅ 原先误标的 999 行引用在本条目内**全仓归零**（8 处全部改为 `eagle_utils.py:1000–1003`），并在首次出现处补 999 / 1003 行归属说明 |
| deep 模式 Mermaid 图 | ✅ 3 张（架构总览、decode 运行时序、spec 三段流程；见 [report.md](../OpenSource/sglang/report.md) 与 [speculative-decoding-path.md](../OpenSource/sglang/speculative-decoding-path.md)） |
| 相对链接回测（全仓，剥 `<>` 角括号口径） | 旧基线 **693 解析 / 0 失效** → 新状态 **722 解析 / 0 失效**（**0 新增失效**，含剥 `<>` 角括号后的口径） |
| 生成物重跑 | ✅ `scripts/library_index.py --write-stats --check-links`（先 `--dry-run`）；新增条目 4 份 `.md` 的 3 个文件已重跑一致性通过 |
| `docs/statistics.md` | ✅ 按 §1–§5 的同一口径重算并更新（未沿用旧估算） |
| gitlink（子模块）数 | ✅ `git ls-files -s \| awk '$1==160000'` = **0** |
| 统计口径 | ✅ `INDEX.md` / `index/*` / `docs/statistics.md` 全部来自脚本产出或实测，未手改任何脚本口径数字 |

---

## 6. 入库验收检查（Outbound Checklist）

论文 / 领域调研类条目入库前逐条勾选（与 [team.md](team.md) 的「原文与引用规约」「深挖批次标准」配套）：

- [ ] 论文类条目附 `sources/MANIFEST.md`（ID/版本/license/去向齐全）；正文引用无"引了未落地"（有缓存版原文时行号可核）；论文全文（PDF/markdown）未入库。

---

*记录时间：2026-10-16 · 数据来源：本仓库实际文件系统与 Git 状态*

---

## 5. 深挖体量与渲染校验（机器可查，2026-10-18 起）

> 用途：把"够不够深""公式是否误伤""生成物是否可复现""代码锚点是否自洽"变成**可执行判据**，不再靠目测。
> 基准值随每次合并更新；**判据只认输出，不认自述**。

### 5.1 分册体量（行数或字符数任一达标）

```bash
# 分册：≥300 行 或 ≥15,000 字符
for f in */papers/*.md; do
  l=$(wc -l < "$f"); c=$(wc -m < "$f")
  { [ "$l" -ge 300 ] || [ "$c" -ge 15000 ]; } || echo "UNDER: $f ($l 行 / $c 字符)"
done
# 旗舰篇：每条目至少 1 篇 ≥400 行 或 ≥20,000 字符
```

**理由**：只查行数会导致"拆句凑行"；只查字符会漏掉"表格密但文字少"的情况。两者取一，能覆盖两种极端。

### 5.2 伪公式 = 0（含"纯数字+斜杠"型）

```bash
python3 - <<'PY'
import re,glob
cur=re.compile(r'^\s*[\d.,]+\s*(/\s*[\d.,]*)?\s*$'); cjk=re.compile(r'[\u4e00-\u9fff]')
bad=[]
for p in glob.glob("site/**/*.html", recursive=True):
    t=open(p,encoding="utf-8").read()
    for m in re.finditer(r'class="arithmatex"[^>]*>\s*\\\((.{0,240}?)\\\)\s*</span>', t, flags=re.S):
        s=re.sub('<[^>]+>','',m.group(1)).strip()
        if cur.match(s) or cjk.search(s) or re.search(r'per\s*1M|千条|千问|/月', s):
            bad.append((p,s[:60]))
print("伪公式:", len(bad)); [print("  ",b) for b in bad[:5]]
PY
```

**判据**：伪公式必须 **0**。典型误伤：`$2.0/$8.0` 被配对成 `\(2.0/\)`；价格类 `$` 一律写 `\$`。

### 5.3 真公式计数不下降

```bash
python3 - <<'PY'
import re,glob
real=0
for p in glob.glob("site/**/*.html", recursive=True):
    t=open(p,encoding="utf-8").read()
    for m in re.finditer(r'class="arithmatex"[^>]*>\s*\\\((.{0,240}?)\\\)\s*</span>', t, flags=re.S):
        s=re.sub('<[^>]+>','',m.group(1))
        if re.search(r'\\[a-zA-Z]|\^|_|\{|\}', s): real+=1
print("真公式:", real)
PY
```

**判据**：合并前后**必须相等**（历史基准：`f95a6f5` 起 198；2026-10-18 起随合并更新）。**减少即判失败**——说明误伤。

### 5.4 代码类核证三件套（`papers/*` 含代码事实时）

1. **锚点自洽**：同一分册内所有代码锚点必须属于**同一个 `仓库@commit`**；出现两套 SHA 即判不合格（2026-10-17 曾出现 vLLM/SGLang SHA 互换）。
2. **锚点支撑力**：每条锚点必须**逐字支撑**其所附断言；落在 `import`／注释／日志串／实参行的判"引而未落地"；**行为级断言需 2–3 处锚点构成调用链**（入口→中间→分支）。
3. **复核留痕**：必须附 `sources/CODE-AUDIT.md`，每条 = `仓库@commit:文件:行` ｜ 支撑哪句断言 ｜ 核验日期 ｜ 更正历史。**没有清单 = 未核。**

附：`state_reason` / `closed_by` / `created_at` 这类 API 字段必须**逐项回查**，不许凭印象写（2026-10-17 曾把 issue 开立日写错、把 `completed` 写成 `inactive`）。

### 5.5 生成物幂等（必须用会写文件的同一组参数）

```bash
python3 scripts/library_index.py --repo-root . --out-root . --write-stats --check-links
git status --porcelain   # 必须为空
python3 scripts/library_index.py --repo-root . --out-root . --write-stats --check-links
git status --porcelain   # 再跑一次仍必须为空
```

**为什么连跑两次**：只用 `--check-links`（不写文件）会掩盖统计漂移；2026-10-17 就因此漏过一版 `stats.json` 不一致。


### 5.7 当前基准（`7af2928`，2026-10-18）

| 指标 | 基准值 |
|---|---|
| `entries` | **48** |
| `children` | **90** |
| 分册体量 | 31/39 篇 ≥300 行或 ≥15k 字符（其余为早期条目，待回炉）|
| 伪公式 | **0** |
| 真公式 | **198**（随合并更新）|
| 相对链接失效 | **0** |
| 生成器幂等 | `--write-stats` 连跑两次 **0 diff** |

### 5.6 否定性结论的三要素（2026-10-20 新增）

> 来源：DSH 仓库深读收口质检（图图提出、协调者落地）。"没找到 X"是**否定性结论**，不能只写"没找到"。

一条合格的否定性结论必须同时给出：

| 要素 | 要求 | 反例 |
|---|---|---|
| **搜索面** | 在**哪些文件/目录**里找（路径级，不是"整个仓库"）| "检查过代码，没有" |
| **方法** | 用什么手段找（`grep` 正则原文、符号枚举、静态分析）| "看过一遍" |
| **结果** | 命中数与唯一入口/唯一写入点；**并限定结论范围**（"这些文件里没有"≠"系统不存在"）| "确认不存在" |

**已用此标准的两条结论（可作为模板）**
1. `ptc` 未找到绕过审批的提权路径：搜索面 `packages/core/tools/src/ptc.ts`、`ptc-calls.ts`、`packages/ptc-runtime/**`；方法 `grep -rn 'approveEscalation\|approval'` 全量枚举；结果=唯一审批调用 `ptc.ts:395`，其余为类型导入与 schema 描述。
2. 会话日志无删除路径：搜索面 `packages/core/session/src/*.ts`；方法 `grep -rnE "\.log\.(splice|pop|shift|length *=)|delete .*log|truncate"`；结果=**0 命中**，唯一写入 `this.log.push`（2 处）。

**验收动作**：任何出现"未找到 / 不存在 / 无 X 路径"字样的交付，必须能回答"搜索面是什么、方法是什么、结论边界到哪"——答不上来即判不合格。
