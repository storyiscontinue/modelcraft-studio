# Mathematical Modeling Competition Workflow Basis

This document records the operating assumptions used by the `competition_zh` template. It is a workflow aid, not an official rule replacement. Teams must read the current announcement and their participating institution's notice before submission.

## Stable rules reflected in the workflow

- The competition is team-based and timed; the official current-year notice controls the exact start, end, eligibility, and submission deadlines.
- The built-in CUMCM profile plans against a 30-page ceiling. Users can override `MAX_PAGES` when the current notice or an institution-specific rule requires a different limit.
- The paper structure is: Chinese abstract and keywords, problem restatement, problem analysis, assumptions, notation, model construction and solution, validation or sensitivity analysis, model evaluation and extension, references, and appendices.
- The default CUMCM profile requires a Chinese abstract only; it does not add an English abstract unless the selected competition profile requires one.
- Reproducible source code belongs in the appendix, while the solver, result tables, and figures remain available as separate workspace artifacts.
- The CUMCM LaTeX profile uses the `cumcmthesis` document class and is compiled locally with XeLaTeX.
- Reproducibility matters: source code, data provenance, parameter definitions, and any computational limitations should be recorded with the work.
- The workflow includes a review checkpoint between stages so a team can inspect assumptions and outputs before continuing.
- The tool does not fabricate sources, claim an online search that did not occur, or hide model limitations. Search results must be checked by the team.

## Official sources to verify before a real submission

- China Society for Industrial and Applied Mathematics (official site): https://www.csiam.org.cn/
- National Undergraduate Mathematical Contest in Modeling portal: https://www.mcm.edu.cn/
- The current-year competition notice, problem statement, submission specification, and institution notice published by the official organizers.

The application deliberately does not hard-code a year-specific deadline, naming rule, or judging detail because those values can change. The `competition_zh` workflow therefore produces editable drafts and local compliance checks, not a claim of official acceptance by itself.
