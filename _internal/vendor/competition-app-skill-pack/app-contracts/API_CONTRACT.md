# App API Contract

## Endpoint shape

`POST /v1/skill-runs`

Request body is the execution envelope in `execution-envelope.schema.json`.

The App should never call a skill prompt as an unstructured string-only operation. It should:

1. resolve a versioned `skill_id`;
2. validate the envelope;
3. inject the current `competition_profile`;
4. execute in a sandbox with a tool allowlist and budget;
5. validate returned artifacts and provenance;
6. persist AI usage and approval events;
7. schedule the next DAG node only when gates pass.

## Event stream

Recommended events:

- `run.created`
- `run.started`
- `artifact.created`
- `evidence.added`
- `approval.requested`
- `approval.resolved`
- `run.partial`
- `run.completed`
- `run.failed`

## Idempotency

Use `run_id` plus `skill_version` as an idempotency key. Side-effecting adapters must additionally
use provider-specific idempotency keys.

## Adapter interface

Each imported legacy prompt should be wrapped by an adapter with:

```text
prepare(envelope) -> validated context
execute(context, tool_gateway) -> raw result
normalize(raw result) -> envelope patch
validate(envelope patch) -> pass/fail
compensate(side effects) -> status
```

Do not expose provider keys to skill text. The tool gateway owns credentials, retries, timeout,
rate limits, redaction, and cost accounting.

## Web research adapter

Implement web and community research behind `WebResearchGateway`; see
`WEB_RESEARCH_GATEWAY.md`. Skills may request a research purpose, query, source authority, freshness,
and budget, but may not select a credential or construct authenticated CLI commands.

The gateway must:

1. probe current backend availability;
2. prefer official and organizer sources for rules;
3. normalize backend output into evidence records;
4. redact Cookie, Token, URL access parameters, and browser-session details;
5. return explicit partial, unavailable, or needs-login states;
6. preserve source URL, retrieval time, backend name, authority, and snapshot hash.

## Zero-config and output quality

Implement `ZERO_CONFIG_AND_HUMAN_OUTPUT.md`. Every skill remains callable in `zero-config` mode.
Missing optional integrations reduce evidence completeness or side-effect capability; they do not
make the skill unavailable. The response must include `capability_state`, manual fallbacks, and an
honest status.

Apply `output_profile` after evidence and compliance checks. Human-readable artifacts should sound
specific to the project and audience, but the renderer must not invent experience, disguise
synthetic evidence, remove required AI disclosure, or optimize for detector evasion.
