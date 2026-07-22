---
name: academic-researcher
description: A comprehensive academic writing and scientific research assistant. Make sure to trigger and use this skill whenever the user mentions writing research papers, drafting LaTeX code, conducting literature reviews, planning ablation studies, responding to reviewers (rebuttals), or editing academic text, even if they do not explicitly ask for the 'academic-researcher' skill.
---

# Academic Researcher: Unified Scientific Writing & Review Assistant

You are equipped with a high-level academic research skill. This skill orchestrates scientific paper writing, literature review aggregation, and ablation study planning. 

When this skill is triggered, identify the sub-task the user wants to accomplish and follow the corresponding guidelines below.

## 🧭 Sub-Module Navigation

This skill contains three integrated sub-modules. Depending on the task, refer to the corresponding embedded guide below:
- **Literature Review**: See the "Literature Review & Synthesis Guide" section.
- **Ablation Studies**: See the "Ablation Studies & Experimental Design Guide" section.
- **LaTeX/Word Paper Drafting**: See the "Paper Writing & Output Verification Guide" section.

---

## 🔬 Core Academic Task Guidelines

### 1. Literature Review & Synthesis
*   **Story Framing**: Do not merely list papers. Organize reviews around a distinct narrative arc or storyline.
*   **Anti-Hallucination**: Never fabricate citations or DOIs. If a citation's BibTeX cannot be verified via DBLP/CrossRef, perform a search or downgrade the claim.
*   **Detailed Workflow**: Follow the search, filtering, and synthesis loop outlined in `references/literature-review.md`.

### 2. Ablation Planner & Experimental Control
*   **Control Variables**: Map each claim to concrete evidence. Build a Claims-Evidence Matrix to justify the importance of each model component.
*   **Ablation Logical Tree**: Structure the experimental evaluation to prove that removing any single module degrades performance. See `references/ablation-planner.md` for logic structuring.

### 3. Section-by-Section Paper Writing
*   **Claims-Evidence Matrix**: Maintain a strict Claims-Evidence Matrix in `PAPER_PLAN.md` before writing LaTeX.
*   **Drafting Standard**: Write papers section by section. Every section must have a minimum size of 500 characters, and the main paper body must be $\ge 5$ KB.
*   **Real Citation Verification**: Always fetch verified BibTeX from DBLP/CrossRef. Do not hallucinate literature.
*   **Strict Output Contract Verification**: Before concluding the task, you MUST run a validation command to verify the file outputs.

---

## ⛔ Output Validation Contract (Mandatory)

Always execute the following shell script to verify your output before declaring the task complete:

```bash
echo "=== Output verification (must be all ✅) ==="
MODE=$(grep -q "Word（.docx）\|docx mode" CLAUDE.md 2>/dev/null && echo docx || echo pdf)
echo "MODE: $MODE"
PASS=true

if [ "$MODE" = "docx" ]; then
    [ -f paper/main.md ] && SZ=$(wc -c < paper/main.md) || SZ=0
    [ "$SZ" -ge 5120 ] && echo "✅ paper/main.md ($SZ bytes)" || { echo "❌ paper/main.md missing or too small"; PASS=false; }
else
    [ -f paper/main.tex ] && SZ=$(wc -c < paper/main.tex) || SZ=0
    [ "$SZ" -ge 5120 ] && echo "✅ paper/main.tex ($SZ bytes)" || { echo "❌ paper/main.tex missing or too small"; PASS=false; }
    SECT_COUNT=$(ls paper/sections/*.tex 2>/dev/null | wc -l)
    [ "$SECT_COUNT" -ge 3 ] && echo "✅ sections ($SECT_COUNT)" || { echo "❌ too few sections"; PASS=false; }
fi

if [ "$PASS" != true ]; then
    echo "⛔ Output verification FAILED — you must complete missing files or fix formatting before exiting!"
    exit 1
fi
```

If the verification fails, resume writing and complete the placeholders instead of stopping.


---

# 📚 Literature Review & Synthesis Guide (文献综述指导模块)

# 文献综述撰写



为以下研究主题撰写文献综述：**$ARGUMENTS**



## 常量



- **TARGET_PAPER_COUNT** — 从 Additional Parameters 读取（默认 20）

- **CN_EN_RATIO** — 中英文文献比例（默认 "1:1"）

- **CUSTOM_REQUIREMENTS** — 用户自定义要求



## 输入



1. 研究主题（$ARGUMENTS）

2. 用户上传的参考文献（`user_data/*.pdf` 或 `user_data/*.bib`，可选）



## 硬约束（借鉴 PaperSpine citation + lunwen-skill reference_selector）



1. 候选池必须 ≥ 目标数量的 2 倍（如目标 20 篇，候选池 ≥ 40 篇）

2. 80% 以上文献必须是近 3 年（2023 年及以后）

3. 所有文献必须真实可核验：有 DOI、出版社链接或可查证的期刊/会议信息

4. 不确定真实性的文献直接丢弃，绝不使用"猜测型引用"

5. 综述必须按主题分类组织，不能简单罗列

6. 每个主题分类下必须有综合分析，不能只是逐篇摘要

7. 最终输出文件名：`LITERATURE_REVIEW.md`



## ⛔⛔⛔ 完成铁律（最高优先级，违反则本步骤失败）



**本步骤必须产出 `LITERATURE_REVIEW.md`（≥ 5KB，完整的文献综述内容）**。



⛔ **结束前必跑产出验证**：

```bash

[ -f LITERATURE_REVIEW.md ] && SZ=$(wc -c < LITERATURE_REVIEW.md) || SZ=0

[ "$SZ" -ge 5120 ] && echo "✅ LITERATURE_REVIEW.md ($SZ bytes)" \

    || echo "❌ LITERATURE_REVIEW.md 缺失或过小 ($SZ bytes) — 必须补全后重新跑验证, 不要结束本步骤"

```



**如果验证失败,继续补全 LITERATURE_REVIEW.md 而不是退出**。



## 工作流程



### Step 1: 确定检索策略



根据研究主题，确定：

- 核心关键词（中文 + 英文各 3-5 个）

- 扩展关键词（同义词、相关术语）

- 检索时间范围（默认 2020-2026）

- 目标数据库：AMiner（中文优先）、Semantic Scholar、CrossRef、DBLP、arXiv



### Step 2: 文献检索与候选池构建



**⛔ 优先使用 `$SCHOLAR_SCRIPT` 工具搜索（自动调用 AMiner + Semantic Scholar + DBLP + CrossRef）：**



```bash

PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)

# 中文主题搜索（AMiner 自动返回中文标题 + 作者 + 年份 + DOI）

$PYTHON "$SCHOLAR_SCRIPT" bibtex "研究主题关键词" --max 10

# 英文补充搜索

$PYTHON "$SCHOLAR_SCRIPT" bibtex "English keywords" --max 10

```



如果 `$SCHOLAR_SCRIPT` 结果不足，再用 WebSearch 补充搜索学术文献。



**搜索策略（借鉴 PaperSpine 三维度）：**



1. **核心方法论文**：直接相关的方法/技术论文

2. **应用领域论文**：该方法在不同场景的应用

3. **综述/Survey 论文**：已有的综述文章（了解领域全貌）

4. **基础理论论文**：奠基性工作（可以是较早的经典论文）



**对每篇候选文献记录：**



| 序号 | 标题 | 作者 | 年份 | 来源 | DOI/URL | 主题分类 | 核心贡献 | 与本综述的关联 |

|------|------|------|------|------|---------|----------|----------|---------------|



将候选池保存到 `papers_pool.md`。



### Step 3: 文献真实性验证



**验证规则（借鉴 PaperSpine citation_quality_audit）：**



对每篇候选文献执行：

1. 如果有 DOI → 通过 WebSearch 验证 DOI 是否可解析

2. 如果无 DOI → 验证期刊/会议名称是否真实存在

3. 检查作者名 + 标题组合是否能在网上找到对应记录



**验证结果标记：**

- ✅ 已验证（DOI 可解析或有明确出版记录）

- ⚠️ 待确认（信息不完整但来源可信）

- ❌ 不可验证（丢弃，不使用）



丢弃所有标记为 ❌ 的文献。将验证结果更新到 `papers_pool.md`。



### Step 4: 主题聚类



将验证通过的文献按研究主题分为 3-5 个类别：



**分类原则：**

- 每个类别至少 3 篇文献

- 类别之间有逻辑递进关系（如：基础理论 → 方法改进 → 应用实践）

- 类别命名要具体（不能用"其他"这种模糊分类）



输出分类结果到 `papers_pool.md` 的末尾。



### Step 5: 撰写文献综述



基于分类结果，撰写完整文献综述。输出到 `LITERATURE_REVIEW.md`。



**标准结构：**



```markdown

# [综述标题]



## 摘要



（200-300 字，概述综述范围、方法、主要发现）



## 一、引言



### 1.1 研究背景

（领域概述 + 为什么需要这篇综述，500-800 字）



### 1.2 综述目的与范围

（明确综述覆盖的主题、时间范围、文献来源，200-300 字）



### 1.3 文献检索方法

（数据库 + 关键词 + 筛选标准 + 最终纳入篇数，200-300 字）



## 二、[主题分类 A]



### 2.1 [子主题 A1]

（综合分析该方向的研究进展，引用具体文献，800-1200 字）



### 2.2 [子主题 A2]

（...）



## 三、[主题分类 B]



### 3.1 [子主题 B1]

（...）



## 四、[主题分类 C]



（...）



## 五、研究趋势与热点分析



（基于文献时间分布和引用关系，分析领域发展趋势，500-800 字）



## 六、现有研究不足与未来方向



### 6.1 现有研究的局限性

（指出 2-3 个主要不足，每个 200-300 字）



### 6.2 未来研究方向

（基于不足提出 2-3 个可能的研究方向，每个 200-300 字）



## 七、结论



（总结综述主要发现，200-300 字）



## 参考文献



[1] 作者. 题名[J]. 刊名, 年, 卷(期): 页码.

...

```



### Step 6: 质量自检



1. **文献数量**：最终引用的文献是否达到目标数量

2. **时间分布**：近 3 年文献是否 ≥ 80%

3. **中英文比例**：是否符合设定比例

4. **综合性**：每个主题分类下是否有综合分析（不是逐篇摘要）

5. **引用完整性**：正文中引用的文献是否都出现在参考文献列表中

6. **格式规范**：参考文献是否符合 GB/T 7714 格式

7. **字数检查**：总字数是否在 6000-10000 字范围



## 写作风格约束



1. 综述不是摘要堆砌——每个段落必须有综合分析和比较

2. 使用"研究表明[1,2]""多项研究证实[3-5]"等综述特有表述

3. 对比不同研究时要指出异同点和可能原因

4. 避免对单篇文献过度描述（每篇最多 2-3 句）

5. 段落之间要有逻辑过渡，不能突然跳转主题



---



## ⛔⛔⛔ 反 AI 痕迹写作铁律（Word 模式必须遵守，违反等同失败）



Word 输出最常被识别为「AI 写的」就是因为下面这 6 条没遵守。优先级凌驾于章节模板和字数要求。



1. **禁止 markdown bullet/编号列表（`-`、`*`、`1.`、`2.`）作为正文叙述。** 含「主题分类」「研究方向」「现有方法」「研究不足」「未来方向」「分类下的子主题」等场景必须用连贯段落，不许分点罗列。

   - ❌ 错（最典型 AI 痕迹，把综述写成清单）：

     ```

     现有图像质量评估方法主要分为三类：

     - 全参考方法：PSNR、SSIM、MSE…

     - 半参考方法：RR-IQA、RRED…

     - 无参考方法：BRISQUE、NIQE、CNN-IQA…

     ```

   - ✅ 对（连贯段落 + 综合分析）：`现有图像质量评估方法可分为三类。**全参考方法**以 PSNR[1]、SSIM[2] 为代表，假设原始图像可得，但在 AI 生成场景下不存在「真值」，难以直接应用；**半参考方法**如 RR-IQA[3] 通过提取部分参考特征降低对原图的依赖…；**无参考方法**则完全摆脱原图依赖，从早期手工特征（BRISQUE[4]、NIQE[5]）发展到深度学习方法（CNN-IQA[6]、HyperIQA[7]），逐渐成为 AI 图像质量评估的主流方向。`

   - bullet **唯一允许场景**：参考文献列表 / 检索关键词清单 / 文献筛选标准列表，正文综述一律禁止。



2. **加粗写作 `**标签**：内容`，不要 `**标签：**内容`。** 把冒号包进 `**` 里 docx 引擎正则匹配不到，会留下孤立 `**` 残留。

   - ❌ `**全参考方法：** 以 PSNR、SSIM 为代表…`

   - ✅ `**全参考方法**以 PSNR、SSIM 为代表…`（标签和内容直接连写更自然）



3. **每段至少 3-5 句话。** 1-2 句的短段落是 AI 痕迹；要么扩写到 3 句以上，要么并入相邻段落。综述每段一般 5-8 句更合适。



4. **连续段落不能以相同句式开头。** 三段都「研究表明…」开头必须改，交替用「早期工作…」「近年来…」「与之相对…」「另一类方法…」「在此基础上…」等多样化连接词。



5. **不要写成「文献堆砌」。** 每个段落必须有综合性论断，文献作为支撑而非主语。

   - ❌ `[1] 提出了 X 方法。[2] 改进了 X 方法。[3] 进一步扩展了 X。`

   - ✅ `针对 X 问题，早期方法侧重于…[1]，但在 Y 场景下精度受限；后续工作通过引入…机制改进了这一不足[2,3]，在公开数据集上将精度从 80% 提升到 92%。`



6. **去掉 AI 写作口头禅。** 少用「值得注意的是」「综上所述」「这一发现表明」「随着…的发展」「在…的背景下」「具有重要意义」。「研究表明」「多项研究证实」必须紧跟具体引用号 [N]，不能空喊。



---



## 输出文件



- `papers_pool.md` — 候选文献池（含验证状态和分类）

- `LITERATURE_REVIEW.md` — 最终文献综述（主产出）

---

# 🔬 Ablation Studies & Experimental Design Guide (消融实验设计模块)

﻿---
name: ablation-planner
description: Use when main results pass result-to-claim (claim_supported=yes or partial) and ablation studies are needed for paper submission. Codex designs ablations from a reviewer's perspective, CC reviews feasibility and implements.
argument-hint: [method-description-or-claim]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, mcp__codex__codex, mcp__codex__codex-reply
---

# Ablation Planner

Systematically design ablation studies that answer the questions reviewers will ask. Codex leads the design (reviewer perspective), CC reviews feasibility and implements.

## Context: $ARGUMENTS

## When to Use

- Main results pass `/result-to-claim` with claim_supported = yes or partial
- User explicitly requests ablation planning
- `/auto-review-loop` reviewer identifies missing ablations

## Workflow

### Step 1: Prepare Context

CC reads available project files to build the full picture:
- Method description and components (from docs/research_contract.md or project CLAUDE.md)
- Current experiment results (from EXPERIMENT_LOG.md, EXPERIMENT_TRACKER.md, or W&B)
- Confirmed and intended claims (from result-to-claim output or project notes)
- Available compute resources (from CLAUDE.md server config, if present)

### Step 2: Codex Designs Ablations

```
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a rigorous ML reviewer planning ablation studies.
    Given this method and results, design ablations that:

    1. Isolate the contribution of each novel component
    2. Answer questions reviewers will definitely ask
    3. Test sensitivity to key hyperparameters
    4. Compare against natural alternative design choices

    Method: [description from project files]
    Components: [list of removable/replaceable components]
    Current results: [key metrics from experiments]
    Claims: [what we claim and current evidence]

    For each ablation, specify:
    - name: what to change (e.g., "remove module X", "replace Y with Z")
    - what_it_tests: the specific question this answers
    - expected_if_component_matters: what we predict if the component is important
    - priority: 1 (must-run) to 5 (nice-to-have)

    Also provide:
    - coverage_assessment: what reviewer questions these ablations answer
    - unnecessary_ablations: experiments that seem useful but won't add insight
    - suggested_order: run order optimized for maximum early information
    - estimated_compute: total GPU-hours estimate
```

### Step 3: Parse Ablation Plan

Normalize Codex response into structured format:

```markdown
## Ablation Plan

### Component Ablations (highest priority)
| # | Name | What It Tests | Expected If Matters | Priority |
|---|------|---------------|---------------------|----------|
| 1 | remove module X | contribution of X | performance drops on metric Y | 1 |
| 2 | replace X with simpler Z | value of learned vs fixed | drops, especially on dataset A | 2 |

### Hyperparameter Sensitivity
| # | Parameter | Values to Test | What It Tests | Priority |
|---|-----------|---------------|---------------|----------|
| 3 | lambda | [0.01, 0.1, 1.0] | sensitivity to regularization | 3 |

### Design Choice Comparisons
| # | Name | What It Tests | Priority |
|---|------|---------------|----------|
| 4 | joint vs separate matching | whether joint adds value | 4 |

### Coverage Assessment
[What reviewer questions these ablations answer]

### Unnecessary Ablations
[Experiments that seem useful but won't add insight — skip these]

### Run Order
[Optimized for maximum early information]

### Estimated Compute
[Total GPU-hours]
```

### Step 4: CC Reviews Feasibility

Before running anything, CC checks:
- Compute budget: can we afford all ablations with available GPUs?
- Code changes: which ablations need code modifications vs config-only changes?
- Dependencies: which ablations can run in parallel?
- Cuts: if budget is tight, propose removing lower-priority ablations and ask Codex to confirm

### Step 5: Implement and Run

1. Create configs/scripts for each ablation (config-only changes first)
2. Smoke test each ablation before full run
3. Run in suggested order, using descriptive names (e.g., `ablation-no-module-X`)
4. Track results in EXPERIMENT_LOG.md
5. After all ablations complete → update findings.md with insights

## Rules

- **Codex leads the design. CC does not pre-filter or bias the ablation list** before Codex sees it. Codex thinks like a reviewer; CC thinks like an engineer.
- Every ablation must have a clear `what_it_tests` and `expected_if_component_matters`. No "just try it" experiments.
- Config-only ablations take priority over those needing code changes (faster, less error-prone).
- If total compute exceeds budget, CC proposes cuts and asks Codex to re-prioritize — don't silently drop ablations.
- Component ablations (remove/replace) take priority over hyperparameter sweeps.
- Do not generate ablations for components identical to the baseline (no-op ablations).
- Record all ablation results in EXPERIMENT_LOG.md, including negative results (component removal had no effect = important finding).

---

# 📝 Paper Writing & Output Verification Guide (论文撰写与校验模块)

# Paper Write: Section-by-Section LaTeX Generation

Draft a LaTeX paper based on: **$ARGUMENTS**

## Constants

- **TARGET_VENUE = `ICLR`** — Supported: ICLR, NeurIPS, ICML. Override via Additional Parameters.
- **MAX_PAGES = 9** — Main body to Conclusion end. Refs/appendix excluded. Body pages must be ≥ MAX_PAGES.
- **ANONYMOUS = true**
- **DBLP_BIBTEX = true** — Fetch real BibTeX from DBLP/CrossRef. Never fabricate.
- **CUSTOM_REQUIREMENTS** — Highest priority.
- **REVIEWER_SCRIPT** — External reviewer script

## Inputs

1. PAPER_PLAN.md — outline with claims-evidence matrix, figure plan
2. NARRATIVE_REPORT.md — research narrative
3. experiment_results.md — structured experiment results (from experiment-bridge)
4. figures/ — PDFs + latex_includes*.tex + experiment_data.json
5. Existing .bib file (or will create)

If no PAPER_PLAN.md, generate minimal outline from available docs.

## Orchestra References (use when needed)

- `../shared-references/writing-principles.md` — story framing, clarity
- `../shared-references/venue-checklists.md` — submission requirements
- `../shared-references/citation-discipline.md` — citation fallback

## Load shared rules

```bash
cat _utils/writing_rules.md 2>/dev/null || cat skills/shared-scripts/writing_rules.md
```

## ⛔⛔⛔ Output Contract (highest priority, violating fails the step)

**Mandatory output depends on `params.output_format`**:

- **PDF mode (default)**: `paper/main.tex` (template-based, ≥ 5KB) + `paper/sections/*.tex` (each ≥ 500 chars) + `paper/references.bib`
- **docx mode (user chose Word)**: `paper/main.md` (**single file** with complete paper, ≥ 5KB). **Do NOT create paper/main.tex**

⛔ **Detect current mode**:
```bash
grep -q "Word（.docx）\|docx mode\|output_format.*docx" CLAUDE.md && echo "MODE=docx" || echo "MODE=pdf"
```

⛔ **MUST run output verification before ending the step**:
```bash
echo "=== Output verification (must be all ✅) ==="
MODE=$(grep -q "Word（.docx）\|docx mode" CLAUDE.md 2>/dev/null && echo docx || echo pdf)
echo "MODE: $MODE"
PASS=true
if [ "$MODE" = "docx" ]; then
    [ -f paper/main.md ] && SZ=$(wc -c < paper/main.md) || SZ=0
    [ "$SZ" -ge 5120 ] && echo "✅ paper/main.md ($SZ bytes)" || { echo "❌ paper/main.md missing or too small"; PASS=false; }
else
    [ -f paper/main.tex ] && SZ=$(wc -c < paper/main.tex) || SZ=0
    [ "$SZ" -ge 5120 ] && echo "✅ paper/main.tex ($SZ bytes)" || { echo "❌ paper/main.tex missing or too small"; PASS=false; }
    SECT_COUNT=$(ls paper/sections/*.tex 2>/dev/null | wc -l)
    [ "$SECT_COUNT" -ge 3 ] && echo "✅ sections ($SECT_COUNT)" || { echo "❌ too few sections"; PASS=false; }
fi
[ "$PASS" != true ] && echo "⛔ Output verification FAILED — must complete missing artifacts before ending"
```

**If verification fails, complete the missing files instead of exiting**.

## Workflow

### Step 0: Backup + resume check + upstream validation

**⛔ 上游输出完整性检查（写论文前必做）：**
```bash
echo "=== Upstream outputs validation ==="
UPSTREAM_OK=true

# 1. 核心文件是否存在
for f in PAPER_PLAN.md RESULTS.md; do
    if [ -f "$f" ]; then
        sz=$(wc -c < "$f")
        echo "✅ $f ($sz chars)"
        [ "$sz" -lt 500 ] && { echo "  ⚠ File too small, content may be incomplete"; UPSTREAM_OK=false; }
    else
        echo "⚠ $f not found (paper-write will use minimal outline)"
    fi
done

# 2. 实验数据文件
[ -f figures/all_results.json ] && echo "✅ figures/all_results.json" || echo "⚠ No all_results.json — numerical values may be inaccurate"
[ -f experiment_results.md ] && echo "✅ experiment_results.md" || echo "  (no experiment_results.md, will rely on RESULTS.md)"

# 3. 图表文件
PDF_COUNT=$(ls figures/*.pdf 2>/dev/null | wc -l)
echo "Figures: $PDF_COUNT PDFs"
[ "$PDF_COUNT" -eq 0 ] && echo "⚠ No PDF figures — paper will lack visual content"

# 4. latex_includes.tex 是否存在
[ -f figures/latex_includes.tex ] && echo "✅ figures/latex_includes.tex" || echo "⚠ No latex_includes.tex — figure embedding code missing"

# 5. Claims-Evidence 匹配检查（如果 PAPER_PLAN.md 有 matrix）
if [ -f PAPER_PLAN.md ]; then
    CLAIM_ROWS=$(grep -c '|.*|.*|' PAPER_PLAN.md 2>/dev/null || echo 0)
    [ "$CLAIM_ROWS" -gt 2 ] && echo "✅ Claims-Evidence matrix in PAPER_PLAN.md ($CLAIM_ROWS rows)" || echo "  (no claims-evidence matrix detected)"
fi

echo "=== Validation complete ==="
$UPSTREAM_OK || echo "⚠ Some upstream files incomplete — proceeding anyway but results may be less reliable"
```

Back up existing `paper/` to `paper-backup-{timestamp}/`. Clean stale section files. Check for incomplete sections:
```bash
echo "=== Resume check ==="
if [ -d "paper/sections" ]; then
    for f in paper/sections/*.tex; do
        [ -f "$f" ] || continue
        chars=$(wc -c < "$f")
        if [ "$chars" -lt 500 ]; then
            echo "⚠ Placeholder: $(basename $f) ($chars chars) — needs writing"
        else
            echo "✅ Complete: $(basename $f) ($chars chars)"
        fi
    done
fi
```
Resume: only write placeholder sections (<500 chars or contains "placeholder"/"TODO"), skip completed ones (>2000 chars). See `<resume_strategy>` in writing_rules.md.

### Step 1: Initialize

Create paper/, copy venue template, generate math_commands.tex (paper-specific commands only), create section files.

### Step 1.5: Figure inventory

Before writing any section, build a complete inventory of available figures:

```bash
echo "=== Available PDF figures ==="
ls -la figures/*.pdf 2>/dev/null || echo "No PDF figures found"
echo ""
echo "=== latex_includes.tex content (figure→PDF mapping) ==="
cat figures/latex_includes.tex 2>/dev/null || echo "No latex_includes.tex"
echo ""
echo "=== TikZ diagrams ==="
# TikZ 图由 paper-figure-drawio 生成为 figures/tikz_diagrams.tex → 编译成 figures/tikz_diagrams.pdf
# （历史命名可能是 tikz_architecture_examples.tex，一并兼容）。
# TikZ 的 PDF 已经由 paper-figure-drawio 写进 latex_includes.tex，按 latex_includes.tex 嵌入即可。
ls -la figures/tikz_*.pdf figures/tikz_*.tex 2>/dev/null || echo "No TikZ diagrams"
grep -l 'tikz_' figures/latex_includes.tex >/dev/null 2>&1 && echo "→ TikZ 已在 latex_includes.tex 中，按其图块嵌入" || true
```

**⛔ Build a FIGURE EMBEDDING PLAN before writing any section:**
```
FIGURE EMBEDDING PLAN:
1. fig_main_results.pdf → Experiments section
2. fig_ablation.pdf → Experiments section
3. fig_training_curves.pdf → Experiments section
4. TABLE_main.tex (PDF mode) / TABLE_main.md (Word/docx mode) → Experiments section
5. tikz_diagrams.pdf (geometry/algorithm/architecture TikZ, from latex_includes.tex) → Method section
```
> Tables: PDF mode embeds `\input{figures/TABLE_*.tex}`; Word/docx mode embeds Markdown tables via `cat figures/TABLE_*.md`. Embed every TABLE file that exists — match the format to the output mode.
- **Must use figure blocks from `latex_includes.tex`**, not write `\includegraphics` from scratch
- **TikZ diagrams must be embedded** into corresponding sections — every `tikz_*.pdf` referenced in `latex_includes.tex` must appear in some section (paper-figure-drawio already added include blocks for them)
- **Read experiment_results.md / RESULTS.md for exact numbers** — do not invent results

**⛔ CRITICAL: ALL numerical results in the paper MUST come from `figures/all_results.json` or `RESULTS.md`.** Before writing any results/experiments section, run:
```bash
[ -f figures/all_results.json ] && cat figures/all_results.json
[ -f RESULTS.md ] && cat RESULTS.md
[ -f experiment_results.md ] && cat experiment_results.md
```

When quoting specific numbers (accuracy, RMSE, F1, p-values, speedup ratios, parameter counts, etc.), you MUST copy them verbatim from these files. Do NOT estimate, round, or make up values from LLM memory. A paper with fabricated numbers will fail the final quality gate's numerical consistency check.

**⛔ Claims-Evidence 对照（必须严格遵循规划）：**

Before writing each section, re-read PAPER_PLAN.md's claims-evidence matrix:
```bash
# 提取 PAPER_PLAN.md 中的 claims-evidence 表
grep -A 100 'Claims-Evidence\|claim.*evidence\|claim-evidence' PAPER_PLAN.md 2>/dev/null | head -30
```

Writing discipline:
- Every claim in the paper MUST trace back to a row in the matrix
- Do not add new claims not in the plan (if you discover something, update PAPER_PLAN.md first)
- Do not skip claims that were planned (even negative results should be reported)
- Each claim's numerical evidence must match the value in `figures/all_results.json`

If a planned claim has no evidence in the data, write an honest statement like "preliminary results suggest X, though we leave formal validation to future work" instead of fabricating evidence.

### Step 1.5: Pre-fetch verified reference pool (BEFORE writing any text)

**⛔ This step MUST happen before Step 2. Do NOT write any \citep{} until this pool exists.**

The goal is to build a pool of real, verified papers so that when writing body text, you only cite papers that actually exist.

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
mkdir -p _tmp

# Search for papers in each key topic area of this paper
# (adapt these queries to your specific paper topic)
echo "=== Searching key topic areas ==="

# Extract topic keywords from PAPER_PLAN.md
grep -i 'related\|background\|literature\|baseline\|prior work' PAPER_PLAN.md 2>/dev/null | head -20

# For each major topic/method mentioned in the plan, search for real papers:
# Example queries (REPLACE with your actual topics):
#   $PYTHON "$SCHOLAR_SCRIPT" bibtex "spatial Durbin model digital economy" --max 5
#   $PYTHON "$SCHOLAR_SCRIPT" bibtex "computing infrastructure regional development" --max 5
#   $PYTHON "$SCHOLAR_SCRIPT" bibtex "spatial spillover effect panel data" --max 5
```

After searching, create `_tmp/_verified_refs.txt` with one line per verified paper:
```
key: lesage_2009_spatial_econometrics | title: Introduction to Spatial Econometrics | authors: LeSage, Pace | year: 2009 | match: good
key: elhorst_2014_spatial_panel | title: Spatial Econometrics: From Cross-Sectional Data to Spatial Panels | authors: Elhorst | year: 2014 | match: good
```

**When writing body text in Step 2, ONLY use citation keys from this verified pool.** If you need to cite a paper not in the pool, search for it first and add it to the pool before citing.

**Fallback**: If `scholar_fetch.py` returns no results or `match_label="low"` for a topic, use WebSearch to find the paper on Google Scholar / Semantic Scholar website, then manually verify title + authors + year before adding to the pool.

### Step 2: Write each section

Writing order: Method → Experiments → Introduction → Related Work → Conclusion (core content first).
Save each section immediately. If approaching output limit, create `% [PLACEHOLDER]` files.

**⛔ Writing style rules:**
- **No `\begin{itemize}` or `\begin{enumerate}` in body text** — bullet lists are the #1 AI writing tell. Use flowing prose with inline numbering "(1)...(2)...(3)..." or transition words "First,...Second,...Finally,...".
- **Each paragraph must have ≥3 sentences.** No 1-2 sentence micro-paragraphs.
- **Consecutive paragraphs must not start with the same phrase.**

Follow all rules from `_utils/writing_rules.md` (interleaving, embedding, LaTeX constraints).

For each section, copy the matching figure/table blocks from `figures/latex_includes.tex` (or `figures/*.tex`) into the section file. Path: always `../figures/xxx.pdf` (relative to paper/). Use `[H]` float specifier. Post-write check: every `\ref` must have matching `\label`.

Wide tables (≥6 columns or multiple `p{}` columns): wrap with `\resizebox{\textwidth}{!}{...}`.

After each section, check chars:
```bash
chars=$(wc -c < "paper/sections/current_section.tex")
echo "Current section: $chars chars"
# English LaTeX ≈ 2000-2500 chars/page
# If section page budget is 2 pages but only 2000 chars (~1 page), expand immediately
```

<exemplar_depth>
#### Writing depth by venue

**ICLR/NeurIPS/ICML (9 pages main body)**:
- Abstract (0.3p): what → why hard → how → evidence → strongest result. 150-250 words. Self-contained
- Introduction (1.5p): hook → gap → contributions → results preview → hero figure. Front-load the contribution
- Related Work (1-1.5p): organize by category, synthesize not list. Each category: 3-5 papers with method summary + positioning vs this work
- Method (2-2.5p): notation → formulation → algorithm. Every formula has intuition explanation. Key derivation steps not skipped
- Experiments (3-4p): setup → main results table → comparison plots → ablation table → analysis. Every result has 1-2 paragraphs of interpretation (not just "our method outperforms")
- Conclusion (0.5p): rephrase contributions + limitations + future work

**JMLR/TPAMI journal (15-20 pages)**:
- Introduction (2-3p): more thorough literature positioning
- Related Work (2-3p): comprehensive survey by sub-topic
- Method (4-6p): full derivations, proofs, complexity analysis
- Experiments (6-8p): multiple datasets, extensive ablations, qualitative analysis, failure cases
- Conclusion (1p): detailed limitations and future directions
</exemplar_depth>

**Expansion strategies** (not padding — substantive content):
- Formula listed without derivation → add step-by-step derivation with intuition
- Result only says "as shown in Table X" → add 1-2 paragraphs of interpretation (what numbers mean, comparison, reasoning)
- Related work only lists papers → add method summaries and positioning vs this work
- Algorithm only has pseudocode → add explanation of key steps and complexity analysis

#### Section guidelines
- Abstract: what → why hard → how → evidence → strongest result. Self-contained. 150-250 words.
- Introduction: hook → gap → contributions → results preview → hero figure. 1.5 pages. Front-load contribution.
- Related Work: ≥1 full page. Organize by category, synthesize not list.
- Method: notation → formulation → algorithm. 1.5-2 pages.
- Experiments: setup → main results → ablations. 2.5-3 pages. Every claim needs evidence.
- Conclusion: rephrase contributions + limitations + future work. 0.5 pages.

### Step 3: Build bibliography

Follow the `<references_workflow>` in `_utils/writing_rules.md`.
Venue style: natbib (citep/citet). Verify references.bib is non-empty before proceeding.

**⛔ Use the scholar_fetch.py tool for ALL reference retrieval. NEVER fabricate BibTeX from memory.**

**⛔ 引用写法规则：写正文时，citation key 必须包含描述性关键词，格式为 `作者姓_年份_主题关键词`。**
例如：`\citep{wang_2023_supply_chain_resilience}` 而不是 `\citep{wang2023supply}`。
这样 Step 3b 搜索时能用关键词找到正确的论文。如果不确定作者/年份，用 `TODO__` 前缀：`\citep{TODO__digital_economy_spatial_spillover}`。

```bash
# Step 3a: Collect all cited keys and extract search queries
grep -roh '\\cite[tp]*{[^}]*}' paper/sections/*.tex paper/main.tex 2>/dev/null \
  | grep -oP '\{[^}]+\}' | tr -d '{}' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sort -u > _tmp/_cited_keys.txt
echo "Cited keys: $(wc -l < _tmp/_cited_keys.txt)"
cat _tmp/_cited_keys.txt

# Step 3b: For each cited key, extract descriptive keywords and search
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
while IFS= read -r key; do
    # Convert citation key to search query: replace _ with spaces, remove TODO prefix
    query=$(echo "$key" | sed 's/^TODO__//; s/_/ /g')
    echo "--- Fetching: $key (query: $query) ---"
    $PYTHON "$SCHOLAR_SCRIPT" bibtex "$query" --max 3
    sleep 0.5
done < _tmp/_cited_keys.txt
```

For each result:
1. **Check `match_label`**: if `"good"` → use directly. If `"partial"` → verify title matches your intent. If `"low"` → this is likely the wrong paper, search again with better keywords or use WebSearch.
2. **Check `match_score`**: score < 0.3 means the search result probably doesn't match what you cited. Do NOT blindly use it.
3. Pick the correct paper and copy its `bibtex` field into `paper/references.bib`.
4. Replace the citation key in .tex files with the actual key from the BibTeX entry.
5. If `bibtex_source=auto`, add `% [VERIFY]` above the entry.
6. If `match_label="low"` and no better result found, add `% [LOW_MATCH - verify this is the intended paper]` and use WebSearch as fallback.

### Step 4: De-AI polish

See `<de_ai_polish>` in `_utils/writing_rules.md`.

### Step 5: Cross-review

Send draft to external reviewer for feedback before finalizing:

```bash
mkdir -p _tmp
cat << 'REVIEW_EOF' > _tmp/_review_prompt.txt
Please review this academic paper draft. Focus on:
1. Logical flow and argument structure
2. Claim-evidence alignment (every claim has supporting data?)
3. Writing clarity and conciseness
4. Missing content or weak sections
5. Score (1-10) and top 3 actionable improvements

## Paper sections:
REVIEW_EOF
for f in paper/sections/*.tex; do
    [ -f "$f" ] && echo "### $(basename $f)" >> _tmp/_review_prompt.txt && cat "$f" >> _tmp/_review_prompt.txt
done
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
$PYTHON "$REVIEWER_SCRIPT" --prompt-file _tmp/_review_prompt.txt --thread-file _tmp/_reviewer_thread.json 2>&1 | tee _tmp/_cross_review.txt
```

If reviewer script unavailable, skip this step.

### Step 6: Reverse outline test

Extract topic sentences → read in sequence → check claim coverage → fix gaps.

### Step 7: Final checks

```bash
bash _utils/writing_check.sh paper/ 2>/dev/null || bash skills/shared-scripts/writing_check.sh paper/
```

**Figure embedding verification (must pass before finishing)**:
```bash
echo "=== Figure embedding check ==="
missing=0
# Check every PDF in figures/ is referenced in sections
for pdf in figures/*.pdf; do
    [ -f "$pdf" ] || continue
    bn=$(basename "$pdf")
    if ! grep -rq "$bn" paper/sections/*.tex paper/main.tex 2>/dev/null; then
        echo "MISSING: $bn not embedded in any section"
        missing=$((missing + 1))
    fi
done
# Check every label in figures/*.tex is in sections
for fig_tex in figures/*.tex; do
    [ -f "$fig_tex" ] || continue
    for lbl in $(grep -oh '\\label{[^}]*}' "$fig_tex" 2>/dev/null); do
        if ! grep -rq "$lbl" paper/sections/*.tex paper/main.tex 2>/dev/null; then
            echo "MISSING: $lbl (from $(basename $fig_tex)) not in any section"
            missing=$((missing + 1))
        fi
    done
done
echo "Total missing: $missing"
```
If any figures are missing, go back and embed them into the appropriate sections before finishing. **⛔ Do NOT finish until missing = 0.**

**Page estimate check**:
```bash
echo "=== Section sizes ==="
total=0
for f in paper/sections/*.tex; do
    chars=$(wc -c < "$f")
    total=$((total + chars))
    echo "  $(basename $f): $chars chars"
done
echo "  Total: $total chars (~$((total / 2200)) pages), Target: ≥ MAX_PAGES pages"
```
If total chars < MAX_PAGES × 2000, expand the thinnest sections before finishing.

## Key Rules

- Large files: Bash heredoc
- No author info — anonymous block
- Complete sections, not outlines
- One file per section
- Every claim cites evidence
- Venue style: natbib (citep/citet)
- Clean bib — only cited entries
- Section count flexible (5-8)
- Backup before overwrite
- Front-load the contribution
- Primary output: `paper/` directory, temp files: `_tmp/`
