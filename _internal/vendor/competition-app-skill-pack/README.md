# Competition App Skill Pack

面向高中和大学竞赛 App 的 Codex Skill-only 插件。重点不是“一键生成参赛材料”，而是把规则、
证据、AI 留痕、人工审批和提交合规放进统一工作流。

## Included

- 17 个标准 Codex skills
- 当前规则抓取和资格合规
- AI 使用台账与主张证据链
- 数模、科研、创新创业、工程、设计、调查、答辩的路由框架
- 创新大赛/挑战杯创业计划专项技能
- App JSON Schema、API 适配器约定和工作流 DAG
- Agent Reach/OpenCLI/平台 CLI 多后端联网研究网关规范
- 17 个 skill 的零配置运行和人工补录降级
- 面向论文、商业计划书、路演和答辩的自然表达规范
- 给 Codex 开发同学的完整交接提示词

## Start here

1. 阅读 `orchestration/ORCHESTRATION.md`。
2. App 接入先实现 `app-contracts/execution-envelope.schema.json`。
3. 实现 `app-contracts/WEB_RESEARCH_GATEWAY.md`，隔离浏览器登录态和 CLI。
4. 实现 `app-contracts/ZERO_CONFIG_AND_HUMAN_OUTPUT.md`，保证未配置外部工具也能运行。
5. 用 `competition-rule-ingestor` 生成当届 `competition_profile`。
6. 用 `competition-router` 选择技能栈。
7. 按 `orchestration/MIGRATION_PLAN.md` 分批迁移原有 prompts。

## Non-goals

- 不替代主办方规则解释。
- 不自动上传或提交。
- 不伪造数据、访谈、合作、专利、收入、实验或社会影响。
- 不把社区经验帖当作官方规则。
