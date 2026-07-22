# Research Sources

Checked on 2026-07-19. Current-cycle rules must still be refreshed at runtime.

## Official competition sources

- Ministry of Education, 2025-2028 national competition list for primary and secondary students:
  https://www.moe.gov.cn/srcsite/A29/202510/t20251029_1418393.html
- Ministry of Education notice for China International College Students Innovation Competition 2025:
  https://www.moe.gov.cn/srcsite/A08/s5672/202504/t20250417_1187732.html
- Ministry of Education launch report for China International College Students Innovation
  Competition 2026, published 2026-07-17. This confirms the current national cycle but is not a
  substitute for the full notice, track rules, or judging attachments:
  https://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/202607/t20260717_1425743.html
- Official innovation competition platform, judging rule attachment page:
  https://cy.ncss.cn/en/notifications/2c93f4c696aa01a10196eca57202006a
- Challenge Cup official site:
  https://www.tiaozhanbei.net/
- Challenge Cup official legacy notice for the fifteenth national entrepreneurship competition
  series, published 2026-01-30:
  https://old.tiaozhanbei.net/tzb/d73/30982.html
- Challenge Cup official legacy news index:
  https://old.tiaozhanbei.net/
- National College Student Entrepreneurship Service portal:
  https://cy.ncss.cn/
- China Undergraduate Mathematical Contest in Modeling, 2025 AI-use guidance:
  https://www.mcm.edu.cn/html_cn/node/79b9f62bcf0415aab3e2b5d47d559235.html
- China Association of Higher Education competition analysis reports:
  https://www.cahe.edu.cn/site/content/18960.html

## Skill structure and method references

- OpenAI skills catalog: https://github.com/openai/skills
- Anthropic skills catalog: https://github.com/anthropics/skills
- K-Dense scientific skills: https://github.com/K-Dense-AI/claude-scientific-skills
- VoltAgent catalog: https://github.com/VoltAgent/awesome-agent-skills
- PM skills, including market sizing and business model methods:
  https://github.com/phuryn/pm-skills
- Product-on-Purpose PM skills, Apache-2.0:
  https://github.com/product-on-purpose/pm-skills

## Local research adapter reference

- Agent Reach 1.5.0 capability routing was inspected from the local Antigravity/Gemini skill
  configuration on 2026-07-19.
- The Antigravity and Codex Agent Reach skill copies have identical normalized content.
- The local environment exposed OpenCLI 1.8.6, mcporter 0.12.3, GitHub CLI 2.96.0,
  twitter-cli 0.8.5, and bili-cli 0.6.2.
- Credential configuration contains Twitter credential keys, but no Cookie, Token, API key,
  browser profile, authorization value, or secret is copied into this pack.
- The current Codex process did not expose the `agent-reach` wrapper on PATH and PowerShell policy
  blocked some npm shims. Capability probing must therefore run inside the actual App process and
  support direct backend fallbacks.
- See `../app-contracts/WEB_RESEARCH_GATEWAY.md` for the independently written App design.

## Source policy

Official organizer documents govern competition behavior. Open-source skills are method references
only. Before copying code or substantial text, verify the exact repository and file license. This
pack uses independently written instructions and does not vendor third-party skill text. A launch
report or portal activity is not equivalent to a complete rule package; qualification, deadlines,
track definitions, scoring, and AI policies remain unverified until the current official documents
and attachments are captured.