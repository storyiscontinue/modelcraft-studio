# ModelCraft Workbench

ModelCraft Workbench is a portable Windows mathematical-modeling workbench.
The release keeps the recovered v0.2.9 formal desktop interface and connects
it to the remediated local workflow service. The standard workflow is executed
through this chain:

```text
Desktop UI
  -> loopback application service and workflow engine
  -> Claude Code CLI
  -> loopback Anthropic Messages adapter
  -> user-configured OpenAI Responses relay
  -> configured GPT-5.6 model
```

Workflow state, checkpoints, runtime events, Claude session IDs, generated
artifacts, and recovery metadata remain on the local machine. Automated tests
and startup diagnostics do not contact a real relay.

## Runtime setup

The portable package includes the Python application, a packaged `HC_PYTHON`
execution mode with the core scientific-modeling stack, 88 built-in Skills,
DrawIO 28.2.5, and the Pillow 12.2.0 Windows CPython 3.10 compatibility runtime
required by the preserved formal interface. The Skill library consists of the
original 71 academic modeling Skills plus 17 competition application Skills.
DrawIO is stored under `runtime\drawio`; Python package metadata and licenses
are retained in the PyInstaller runtime; Pillow's compatibility license and
artifact provenance are included under `_internal\formal_runtime`.

The package does not prebundle Node.js or Claude Code CLI. Their path fields
may be left empty. The application first discovers an existing installation
from its local `runtime` directory, common Windows, nvm, fnm, Volta, and npm
locations, and `PATH`.
An npm `claude.cmd` wrapper is automatically resolved to its native
`claude.exe` when that binary is present.

Before using the native executor:

1. Configure the executor Base URL and model ID.
2. Save the relay key in Settings, where it is protected by Windows
   current-user DPAPI, or inject it through the environment variable named by
   `executor_api_key_env` (default: `OMA_EXECUTOR_API_KEY`). An environment
   value explicitly overrides the protected value.

Node and Claude Code paths are optional. A compatible existing Node/npm pair
is reused when Claude Code needs to be installed. When a required runtime is
not found, the first native workflow run installs it under the application's
own `runtime` directory. Node `22.17.0` is downloaded only from `nodejs.org` and
verified against the official `SHASUMS256.txt`. Claude Code `2.1.177` is
installed with that application-local Node/npm prefix from
`registry.npmjs.org`; npm cache and configuration also remain under
`runtime\.downloads`. No global npm prefix, system folder, or user Node
installation is modified. `OMA_STRICT_OFFLINE=1` disables these downloads and
reports the missing runtime as a workflow failure.

Claude Code compatibility is determined by a local `--help` capability probe,
not a fixed version allowlist. The executor requires `--print`, `--bare`,
`--verbose`, `--output-format stream-json`, `--permission-mode`, `--model`,
`--resume`, and `--session-id`. Versions `2.1.132` and `2.1.177` remain the
prevalidated references, while other versions are accepted when all required
capabilities are present.

Relay URLs, model IDs, custom headers, runtime paths, and keys are not written
in plaintext to `data/settings.json`. They are stored in
`data/protected-settings.json` as a current-user DPAPI envelope. Keys are not
written to SQLite, logs, exports, or the release ZIP. Opening the application
or Settings does not test the relay.

### GPT image relay

Paper illustrations use a separate OpenAI-compatible Images API. Configure an
image Base URL, image model, and independent image API key in Settings. The
request contract is:

```text
POST <image Base URL>/v1/images/generations
Authorization: Bearer <image API key>
{ "model": "...", "prompt": "...", "n": 1, "size": "..." }
```

The response may contain either `data[0].b64_json` or `data[0].url`. Image
credentials are injected only into the local Claude Code child process and
are not written into the workspace. If a planned GPT image lacks its Base
URL, model, or key, or the configured Images API fails, the figure step fails.
It does not replace that image with DrawIO, TikZ, or another generator.

Run local diagnostics without network access:

```powershell
.\OfflineModelingAgent.exe --diagnose
```

The diagnostic is read-only and checks Python, Node, Claude Code, Git, Pandoc,
XeLaTeX, and DrawIO. A native Claude executable does not require Node; a script
wrapper does. Missing or incompatible required tools block native Agent
execution until the workflow bootstrap installs them. Other tools are
reported as optional capabilities. Resolved DrawIO and XeLaTeX paths are
injected into the Agent process as `HC_DRAWIO` and `HC_XELATEX`.

## Start

Run `release-v0.2.17-live-verified\OfflineModelingAgent\OfflineModelingAgent.exe`. A fresh
configuration defaults to `claude-code-gpt-adapter`; it does not silently fall
back to the legacy provider. Select `mock` explicitly only for an offline UI or
workflow smoke test.

A fresh executor profile also defaults to the OpenAI Responses API. Chat
Completions is available only when the user explicitly selects the
`chat_completions` compatibility mode; it is not treated as the complete
reasoning and response-chain recovery path.

The standard Chinese modeling workflow has exactly seven steps:

1. Problem analysis
2. Modeling
3. Code and results
4. Data figures
5. DrawIO structure figures
6. Chinese paper
7. XeLaTeX PDF compilation

Approval or feedback checkpoints occur after steps 1, 2, 3, and 6 when
checkpoints are enabled. Feedback and directed repairs resume the same Claude
session whenever the transcript is available. Checkpoints are disabled by
default; when enabled, their local auto-approval timeout is configurable and
can be disabled by setting it to zero.

Each competition workspace receives an explicit local format profile,
competition name, and maximum-page contract. The paper gate estimates body
length from section sources, verifies every planned figure and DrawIO/TikZ
companion, and confirms planned figures are referenced by the final LaTeX.
During native Agent execution, session IDs are persisted as soon as the CLI
initializes, model output is committed to SQLite in batches, and workspace
file changes are reported while the process is still running.

## Data layout

- `data/agent.db`: schema-versioned local workflow database
- `data/claude-code/`: local Claude CLI transcript/configuration root
- `runtime/node/`: automatically installed portable Node.js distribution
- `runtime/claude-code/`: application-local Claude Code npm prefix
- `runtime/.downloads/`: application-local download and npm cache
- `workspaces/<workflow>/user_data/`: preserved user inputs
- `workspaces/<workflow>/.agent/`: local manifests and recovery metadata
- `workspaces/<workflow>/code`, `figures`, `paper`: generated deliverables

Final delivery ZIPs use an allowlist and exclude `user_data`, `.agent`,
databases, settings, transcripts, prompts, logs, hidden files, and configured
secrets.

Set `OMA_DATA_DIR` to relocate runtime data. Set `OMA_STRICT_OFFLINE=1` to
disable remote API and search provider modes.

## Build and test

Use CPython 3.10:

```powershell
$env:PYTHONPATH = "src"
& "C:\Program Files\Python310\python.exe" -m compileall -q src tests
python -m unittest discover -s tests -v
powershell -ExecutionPolicy Bypass -File .\packaging\build_portable.ps1
```

The build runs compilation, automated tests, source self-test, PyInstaller,
formal-interface smoke tests, packaged diagnostics, runtime-license checks,
ZIP content checks, local-path/secret scans, and SHA-256 generation. Its
default output is `release-formal`; the obsolete `release` directory is not a
delivery target.

The real Claude CLI integration test is explicit and uses only local loopback
servers:

```powershell
$env:PYTHONPATH = "src"
$env:OMA_RUN_REAL_CLAUDE_CLI = "1"
python -m unittest discover -s tests -p "test_real_claude_cli.py" -v
```

No command above uses a real relay. Real GPT-5.6 relay acceptance remains a
manual action because it requires the user's host and credential confirmation.
See `SECURITY.md`, `MIGRATION.md`, and `RUNTIME_NOTICES.md`.
