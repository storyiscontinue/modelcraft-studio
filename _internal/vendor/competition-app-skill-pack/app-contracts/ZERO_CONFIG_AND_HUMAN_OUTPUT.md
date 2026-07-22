# Zero-Config Runtime and Human Output

This contract keeps every skill useful on a fresh installation while producing work that reads
like a specific student team wrote and revised it.

## Runtime modes

| Mode | Available behavior |
|---|---|
| `zero-config` | local files, pasted text, manual uploads, reasoning, planning, drafting, checklists, local validation |
| `connected` | zero-config behavior plus configured web, model, compute, Office, browser, and platform adapters |
| `restricted` | only capabilities explicitly allowed by competition rules, school policy, privacy policy, and approvals |

Default to `zero-config`. Optional integrations enhance evidence collection and automation; they
must never be prerequisites for discovering or invoking a skill.

## Required fallback behavior

1. Probe capabilities at run time.
2. Execute all locally possible steps.
3. Isolate unavailable operations instead of failing the whole workflow.
4. Return `partial`, `needs_input`, `needs_login`, or `needs_rule_refresh` with exact missing items.
5. Provide a manual fallback such as upload the official notice, paste the rubric, add a CSV, run a
   local script, or ask a teacher to approve a rule interpretation.
6. Resume the same run after missing inputs arrive; do not discard completed work.
7. Never replace unavailable evidence with invented facts.

## Minimum zero-config capability for every skill

- explain required inputs and inspect supplied local material;
- create a structured plan, checklist, template, or draft;
- distinguish facts, assumptions, synthetic examples, and missing evidence;
- generate machine-readable artifacts and next actions;
- validate internal consistency and competition red lines;
- export a manual evidence-acquisition list for unavailable sources or tools.

## Human output profile

Apply an `output_profile` containing audience, artifact type, language, voice, and formality.

The renderer must:

- use project-specific names, mechanisms, constraints, numbers, decisions, and evidence;
- vary sentence structure and paragraph rhythm without becoming casual or decorative;
- keep uncertainty where evidence is incomplete;
- replace generic claims such as “具有广阔前景” with the actual reason, scope, evidence, or limit;
- preserve team terminology and writing samples when supplied;
- adapt style between paper, business plan, technical report, poster, slide, speech, and defense;
- run a final pass for repetition, unsupported superlatives, empty transitions, and copied rubric
  language.

The renderer must not:

- invent first-person experience, fieldwork, interviews, quotations, emotions, or team history;
- insert fake imperfections, deliberate errors, slang, or inconsistent facts to appear human;
- conceal synthetic data or AI involvement;
- promise that text is “undetectable” or optimize for AI-detector evasion;
- weaken citations, provenance, compliance, or disclosure to improve style.

## Recommended generation pipeline

```text
facts and evidence
-> audience and artifact constraints
-> content outline
-> evidence-grounded draft
-> project-specific language pass
-> natural rhythm and redundancy pass
-> claim/evidence recheck
-> AI disclosure and submission compliance
```

## Acceptance tests

- Every one of the 17 skills can start with network, browser, CLI, remote compute, and paid APIs
  disabled.
- A zero-config run produces at least one useful artifact plus exact next actions.
- Missing official rules are requested through manual upload instead of fabricated.
- The same input rendered for a paper, pitch, and defense produces meaningfully different language.
- Output contains project-specific evidence and avoids generic competition filler.
- Humanization never changes facts, provenance, synthetic labels, or disclosure requirements.