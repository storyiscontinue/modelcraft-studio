# Web Research Gateway

This gateway turns web access into a governed App capability. Skills request evidence; they do not
invoke browser sessions, CLIs, cookies, or provider APIs directly.

## Local capability snapshot

Checked on 2026-07-19:

| Component | Version/status | Intended use |
|---|---|---|
| Agent Reach | 1.5.0 | capability probe and backend routing |
| OpenCLI | 1.8.6 | browser-session read access for supported social platforms |
| mcporter | 0.12.3 | MCP-backed search and service adapters |
| GitHub CLI | 2.96.0 | repository, code, issue, and release research |
| twitter-cli | 0.8.5 | Twitter fallback |
| bili-cli | 0.6.2 | Bilibili search and metadata |

The capability probe reported OpenCLI routes for Twitter, Reddit, Facebook, Instagram, and
Xiaohongshu; `bili-cli` for Bilibili; Jina Reader for general web pages; and public adapters for
V2EX and RSS. Exa and LinkedIn were not configured, Xiaoyuzhou lacked its media dependency, and
Xueqiu required a refreshed login. Treat this table as a machine-specific snapshot, not a runtime
guarantee.

The Antigravity/Gemini and Codex Agent Reach skill copies were compared after newline
normalization and matched file-for-file. Credential configuration was inspected by key name only;
secret values were not read into or copied to this pack. The current Codex process did not expose
the `agent-reach` wrapper on PATH, and PowerShell execution policy blocked some npm shims. This is a
concrete reason to probe capabilities inside the serving process and retain direct backend
fallbacks instead of trusting an installation-level health report.

## Boundary

Implement:

```text
WebResearchGateway
  -> CapabilityProbe
  -> SourcePolicy
  -> CredentialBroker
  -> BackendAdapter
  -> SnapshotStore
  -> EvidenceNormalizer
```

- `CapabilityProbe` runs a health check before a multi-source or authenticated task.
- `SourcePolicy` selects sources by authority, task, freshness, license, and competition rules.
- `CredentialBroker` exposes short-lived handles, never raw credentials.
- `BackendAdapter` owns commands, browser bridges, timeouts, retries, and rate limits.
- `SnapshotStore` preserves retrieved content, timestamp, URL, and hash where permitted.
- `EvidenceNormalizer` returns a stable record to the execution envelope.

## Routing policy

| Need | Preferred route | Fallback |
|---|---|---|
| Current competition rules | organizer or ministry page via HTTP/Jina | browser adapter, then manual upload |
| Official notices and attachments | direct organizer URL with snapshot | browser download with approval |
| GitHub skill/code research | `gh` or GitHub API | authenticated browser |
| General technical research | configured semantic search | official docs, GitHub, Jina |
| Community experience | OpenCLI or platform CLI | mark unavailable; never replace official rules |
| Bilibili search/details | `bili-cli` | OpenCLI |
| Social platform reading | OpenCLI browser session | supported platform CLI |

Official and organizer sources always outrank community sources. Community posts may identify
questions, examples, and judge concerns, but cannot define eligibility, deadlines, scoring, or
submission requirements.

## Request contract

```json
{
  "query_id": "rq-123",
  "purpose": "competition_rule|prior_art|market|technical|community",
  "query": "string",
  "preferred_channels": ["web", "github"],
  "required_authority": ["official", "organizer"],
  "freshness_days": 30,
  "max_results": 10,
  "allow_authenticated_read": false,
  "allow_paid_search": false
}
```

Return:

```json
{
  "query_id": "rq-123",
  "status": "completed|partial|needs_login|unavailable|failed",
  "backend_attempts": [
    {
      "channel": "web",
      "backend": "jina-reader",
      "status": "ok",
      "checked_at": "RFC3339 timestamp"
    }
  ],
  "evidence": [],
  "warnings": []
}
```

## Credential rules

- Never place Cookie, Token, API key, Authorization header, browser profile path, or session export
  in a prompt, execution envelope, artifact, log, eval, or source snapshot.
- Store credentials outside the plugin and App repository.
- Refer to credentials through opaque handles such as `credential_ref`.
- Browser-backed access must use an isolated profile or approved bridge and read-only commands.
- Do not copy credentials from Antigravity into Codex or the App. Configure each runtime through
  its own credential broker.
- Redact command output before persistence. Platform result URLs may contain access parameters;
  normalize or encrypt them before storage.

## Evidence normalization

Each retrieved item should record:

```text
evidence_id
kind
title
url
publisher
authority
channel
backend
retrieved_at
published_at
snapshot_sha256
verified
credential_mode
license_or_usage_note
```

Use `credential_mode` values `none`, `browser-session`, `token-broker`, or `manual-upload`. It
describes the access mechanism and never contains the credential itself.

## Failure behavior

1. Probe the requested channel.
2. Try the allowed fallback chain.
3. Return `partial` when authoritative results are incomplete.
4. Return `needs_login` without exposing login data when authentication is missing or stale.
5. Return `needs_rule_refresh` when current official rules cannot be verified.
6. Never silently substitute community guidance for official rules.

## App tests

- Missing browser bridge returns `needs_login` or falls back without leaking session data.
- A result containing token-like URL parameters is redacted before logging.
- Community-only search cannot mark a competition rule as verified.
- Disabled paid search is never invoked.
- Backend retries respect rate limits and do not duplicate evidence.
- Health status is cached briefly and refreshed before authenticated or long-running research.