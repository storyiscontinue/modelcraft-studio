---
name: evidence-provenance
description: >
  Build a provenance graph for claims, data, interviews, experiments, citations, figures, code, and generated artifacts. Use whenever a competition submission makes factual, performance, market, social-impact, or implementation claims.
---

# evidence-provenance

## Purpose

确保每个关键主张都能追溯到真实证据，禁止把建议、模拟数据或模型输出伪装成事实。

## Required input

Accept a unified execution envelope containing:

- `run_id`, `skill_id`, and `skill_version`
- `competition_profile` with official rule sources and `retrieved_at`
- `inputs`, existing `artifacts`, and evidence references
- `budget`, allowed tools, privacy level, and current approvals

If the current official rules are absent or stale, stop rule-dependent work and route to `competition-rule-ingestor`.

## Operating rules

- Treat official current-cycle documents as authoritative. Community posts are context only.
- Never fabricate data, interviews, users, revenue, patents, awards, partnerships, deployments, citations, experiment results, or judge feedback.
- Label simulated or synthetic data conspicuously and block it from being presented as real evidence.
- Keep raw secrets and personal data out of prompts and artifacts; store references or redacted summaries.
- Record sources, retrieval time, transformations, model use, and human edits.
- Separate planning from side-effecting execution. Require approval before spending money, launching compute, contacting people, publishing, uploading, or submitting.

## Failure and escalation

- Return `needs_input` when required facts or files are missing.
- Return `needs_rule_refresh` when official rules are unavailable, conflicting, or stale.
- Return `needs_approval` for red-line compliance, privacy, budget, external communication, or submission decisions.
- Return `partial` with explicit gaps when useful work can continue safely.
- Never silently replace missing real evidence with generated evidence.

## App response

Return the updated execution envelope plus:

```json
{
  "status": "completed|partial|needs_input|needs_rule_refresh|needs_approval|blocked",
  "artifacts": [],
  "evidence": [],
  "ai_usage": [],
  "approvals": [],
  "warnings": [],
  "next_actions": []
}
```

Validate against `../../app-contracts/execution-envelope.schema.json`.

## Workflow

1. 抽取可核验主张并分类。
1. 连接来源、数据集、实验、访谈、代码版本和图表。
1. 标记模拟、推断、未核实和过期证据。
1. 对无证据的高风险主张生成阻断项。

## Required outputs

- `provenance_graph.json`
- `claims_evidence_matrix.csv`
- `unsupported_claims.md`

Every artifact must include source_run_id, generated_at, confidence, and provenance references.

## Zero-config behavior

This skill must remain usable when no optional API, authenticated browser, platform CLI, remote
compute, Office bridge, or paid provider is configured.

- Run the reasoning, planning, checklist, local-file, and user-provided-evidence portions normally.
- Use local files, pasted text, manual uploads, and explicit user answers as the default inputs.
- Return status partial, needs_input, or needs_rule_refresh only for the unavailable evidence or
  side effect; do not disable the whole skill.
- Produce a concrete manual task list for steps that require an unavailable backend.
- Never invent search results, experiments, interviews, financial numbers, citations, or rule text
  to make a zero-config run look complete.

## Human-authored output quality

- Write for the named audience and artifact type, using the team's actual project terms, constraints,
  evidence, and decisions.
- Prefer concrete nouns, varied sentence lengths, natural transitions, and justified uncertainty.
- Remove generic openings, inflated claims, repetitive summary phrases, and interchangeable
  competition-template language.
- Preserve the team's voice when samples exist. Otherwise use clear, restrained Chinese suitable
  for a capable student team, not marketing copy or bureaucratic filler.
- Do not fabricate first-person experience, emotion, fieldwork, quotations, or personal testimony.
- Natural writing does not override AI-use disclosure rules and must not be used to evade detectors.

## Approval gates

Request explicit human approval before:

- treating uncertain eligibility or rule interpretation as resolved;
- using personal, confidential, or regulated data;
- executing paid APIs, remote compute, outreach, publication, upload, or submission;
- converting assumptions, simulations, or plans into claimed real-world achievements.