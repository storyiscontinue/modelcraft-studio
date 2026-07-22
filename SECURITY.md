# Security And Privacy

## Trust boundaries

The desktop UI, SQLite database, workflow engine, Claude Code runner, and
Anthropic compatibility adapter are local components. The application service
and adapter bind only to `127.0.0.1`. The only intended remote model connection
is from the adapter to the relay Base URL explicitly configured by the user.

Remote model responses, uploaded documents, extension Skills, and generated
code are untrusted input.

## Runtime and network controls

- The application service and Anthropic adapter reject non-loopback binding.
- Runtime diagnostics perform version probes only; they make no network
  requests.
- Claude Code receives a random per-adapter local token and a loopback
  `ANTHROPIC_BASE_URL`.
- Nonessential CLI traffic, auto-update, error reporting, and telemetry are
  disabled in the runner environment.
- Automated tests use loopback fake servers. Real relay tests are never
  triggered by startup, diagnostics, unit tests, or packaging.
- API URLs are validated, redirects are host-bounded, and network audit records
  omit request bodies and credentials.

These controls reduce unintended traffic but do not constitute a general OS
network sandbox. Use Windows Firewall or an isolated VM when a hard egress
boundary is required.

## Secrets

Sensitive relay profiles, full URLs, model identifiers, custom headers,
runtime paths, and API keys are stored in `data/protected-settings.json` using
Windows current-user DPAPI with UI disabled. The ordinary `settings.json`
contains only non-sensitive settings plus relay profile IDs and display names.
Legacy plaintext settings are migrated on first load and scrubbed from the
public file.

The native executor can also read its relay key from the configured environment
variable, defaulting to `OMA_EXECUTOR_API_KEY`. An explicit environment value
overrides the protected value for that process. A corrupt or undecryptable
protected-settings envelope fails closed; the application does not fall back
to plaintext credentials.

The key is held in process memory while in use. Export and release scans reject
known configured secret values before creating an archive.

Do not place keys in prompts, workspace files, command arguments, fixtures, or
`settings.json`. `OMA_TEST_API_KEY` is reserved for controlled acceptance and
must be unset for release packaging.

## Generated code and native tools

Claude Code can use native tools in the workflow workspace. Host validation,
path bounding, static checks, timeouts, a sanitized child environment, and
`shell=False` are defense-in-depth measures, not a complete sandbox. Generated
Python or shell commands can still be dangerous. Run untrusted competitions or
third-party Skills in a disposable Windows account or VM without sensitive
files.

XeLaTeX acceptance uses `-no-shell-escape`. Final exports exclude runtime state,
LaTeX intermediates, internal manifests, user originals, and credentials.

## Local data and recovery

Runtime state is stored under `data/` and workflow files under `workspaces/`.
Database migrations create a pre-migration backup and run transactionally.
Stopping the application marks active work interrupted while retaining the
workspace and Claude session ID for recovery.

Before replacing an existing installation, keep a hash-verified copy of the
original directory. Restore that untouched copy to roll back; do not merge
runtime data into a clean release unless following `MIGRATION.md`.

DPAPI data is bound to the Windows user account that encrypted it. When moving
the application to another machine or account, migrate workflow data and
workspaces normally but re-enter protected settings and keys.

## Reporting

When reporting a security issue, do not attach a real API key, private dataset,
Claude transcript, `agent.db`, or a complete user workspace. Provide a minimal
redacted reproduction.
