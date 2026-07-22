# ModelCraft 数模工坊 (ModelCraft Workbench)

[中文说明](#中文说明) | [English Version](#english-version)

---

## 中文说明

ModelCraft Workbench 是一款便携式 Windows 数学建模工作流工作台。
本发布版本保留了恢复后的 v0.2.9 正式桌面界面，并将其连接至修复后的本地工作流服务。标准工作流通过以下链路执行：

```text
桌面 UI 界面
  -> 本地环回 (Loopback) 应用服务与工作流引擎
  -> Claude Code CLI
  -> 本地环回 (Loopback) Anthropic Messages 适配器
  -> 用户配置的 OpenAI Responses 中转站
  -> 已配置的 GPT-5.6 模型
```

工作流状态、检查点 (Checkpoints)、运行时事件、Claude 会话 ID (Session IDs)、生成的产物成果以及恢复元数据均保留在本地机器上。自动化测试与启动诊断不会连接真实的远程中转站。

### 运行环境设置 (Runtime setup)

便携包中包含了 Python 应用程序、打包的 `HC_PYTHON` 执行模式（内置核心科学建模工具栈）、88 个内置 Skills、DrawIO 28.2.5 以及保留的正式界面所需的 Pillow 12.2.0 Windows CPython 3.10 兼容运行时。Skill 库由原本的 71 个学术建模 Skills 加上 17 个竞赛应用 Skills 组成。DrawIO 存储在 `runtime\drawio` 下；Python 包元数据和许可证保留在 PyInstaller 运行时中；Pillow 的兼容性许可证和产物溯源信息包含在 `_internal\formal_runtime` 下。

便携包未预先捆绑 Node.js 或 Claude Code CLI，其路径字段可留空。应用程序首先会从其本地 `runtime` 目录、通用的 Windows 安装位置、nvm、fnm、Volta、npm 位置以及系统 `PATH` 中自动检索已有的安装。当存在 npm `claude.cmd` 包装脚本时，它会自动解析为其原生的 `claude.exe`。

在使用原生执行器之前：

1. 配置执行器的 Base URL 和模型 ID (Model ID)。
2. 在设置中保存中转站密钥 (Relay Key)，该密钥受 Windows 当前用户 DPAPI 加密保护，或者通过由 `executor_api_key_env` 指定的环境变量注入（默认：`OMA_EXECUTOR_API_KEY`）。显式指定的环境变量值将覆盖加密受保护的值。

Node 和 Claude Code 路径是可选的。当需要安装 Claude Code 时，将复用现有的兼容 Node/npm 配对。当找不到必需的运行时时，首次原生工作流运行将在应用程序自己的 `runtime` 目录下自动安装它们。Node `22.17.0` 仅从 `nodejs.org` 下载并根据官方 `SHASUMS256.txt` 进行校验。Claude Code `2.1.177` 将通过应用本地的 Node/npm 前缀从 `registry.npmjs.org` 安装；npm 缓存和配置也保留在 `runtime\.downloads` 下。绝不会修改全局 npm 前缀、系统文件夹或用户的 Node 安装。`OMA_STRICT_OFFLINE=1` 会禁用这些下载并将缺失的运行时报告为工作流失败。

Claude Code 的兼容性是由本地 `--help` 能力探针决定的，而不是固定的版本白名单。执行器需要 `--print`、`--bare`、`--verbose`、`--output-format stream-json`、`--permission-mode`、`--model`、`--resume` 和 `--session-id`。版本 `2.1.132` 和 `2.1.177` 保持为预验证的参考版本，而在所有必需能力都存在时，也接受其他版本。

中转站 URL、模型 ID、自定义请求头、运行时路径和密钥不会以明文形式写入 `data/settings.json`。它们作为当前用户 DPAPI 包存储在 `data/protected-settings.json` 中。密钥不会写入 SQLite、日志、导出文件或发布 ZIP。打开应用程序或设置页面不会触发测试中转站。

#### GPT 图像中转站 (GPT image relay)

论文插图使用独立的兼容 OpenAI 的 Images API。在设置中配置图像 Base URL、图像模型和独立的图像 API 密钥。请求契约如下：

```text
POST <图像 Base URL>/v1/images/generations
Authorization: Bearer <图像 API 密钥>
{ "model": "...", "prompt": "...", "n": 1, "size": "..." }
```

响应可能包含 `data[0].b64_json` 或 `data[0].url`。图像凭据仅注入到本地 Claude Code 子进程中，不会写入工作区。如果计划的 GPT 图像缺失 Base URL、模型或密钥，或者配置的 Images API 失败，则插图步骤失败。它不会用 DrawIO、TikZ 或其他生成器替换该图像。

在无网络连接的情况下运行本地诊断：

```powershell
.\OfflineModelingAgent.exe --diagnose
```

该诊断是只读的，检查 Python、Node、Claude Code、Git、Pandoc、XeLaTeX 和 DrawIO。原生 Claude 可执行文件不需要 Node；脚本包装器需要。缺失或不兼容的必需工具会阻止原生 Agent 执行，直到工作流引导安装它们。其他工具被报告为可选能力。解析出的 DrawIO 和 XeLaTeX 路径被作为 `HC_DRAWIO` 和 `HC_XELATEX` 注入到 Agent 进程中。

### 启动 (Start)

运行 `release-v0.2.17-live-verified\OfflineModelingAgent\OfflineModelingAgent.exe`。全新的配置默认使用 `claude-code-gpt-adapter`；它不会静默回退到旧版提供程序。仅在离线 UI 或工作流冒烟测试时显式选择 `mock`。

新的执行器配置文件默认也使用 OpenAI Responses API。仅当用户显式选择 `chat_completions` 兼容模式时，Chat Completions 才可用；它不被视为完整的推理和响应链恢复路径。

标准的中文建模工作流恰好有七个步骤：

1. 问题分析 (Problem analysis)
2. 数学建模 (Modeling)
3. 代码与结果 (Code and results)
4. 数据图表 (Data figures)
5. DrawIO 结构图表 (DrawIO structure figures)
6. 中文论文起草 (Chinese paper)
7. XeLaTeX PDF 编译 (XeLaTeX PDF compilation)

在启用检查点时，审批或反馈检查点在步骤 1、2、3 和 6 之后发生。只要转录记录可用，反馈和定向修复就会恢复相同的 Claude 会话。检查点默认处于禁用状态；启用时，其本地自动审批超时是可配置的，并且可以通过将其设置为 0 来禁用。

每个竞赛工作区都会收到显式的本地格式配置文件、竞赛名称和最大页数契约。论文关卡从章节来源估计正文长度，验证每个计划的图表和 DrawIO/TikZ 伴随文件，并确认计划的图表被最终 LaTeX 引用。在原生 Agent 执行期间，一旦 CLI 初始化就持久化会话 ID，模型输出批量提交到 SQLite，工作区文件更改在进程仍在运行时即被报告。

### 数据布局 (Data layout)

- `data/agent.db`: 版本化模式的本地工作流数据库
- `data/claude-code/`: 本地 Claude CLI 转录/配置根目录
- `runtime/node/`: 自动安装的便携式 Node.js 分发包
- `runtime/claude-code/`: 应用本地的 Claude Code npm 前缀
- `runtime/.downloads/`: 应用本地的下载和 npm 缓存
- `workspaces/<workflow>/user_data/`: 保留的用户输入
- `workspaces/<workflow>/.agent/`: 本地清单和恢复元数据
- `workspaces/<workflow>/code`, `figures`, `paper`: 生成的最终交付物

最终交付 ZIP 使用允许列表，并排除 `user_data``、`.agent`、数据库、设置、转录记录、Prompt 提示词、日志、隐藏文件和配置的秘密。

设置 `OMA_DATA_DIR` 可迁移运行时数据。设置 `OMA_STRICT_OFFLINE=1` 可禁用远程 API 和搜索提供程序模式。

### 构建与测试 (Build and test)

使用 CPython 3.10：

```powershell
$env:PYTHONPATH = "src"
& "C:\Program Files\Python310\python.exe" -m compileall -q src tests
python -m unittest discover -s tests -v
powershell -ExecutionPolicy Bypass -File .\packaging\build_portable.ps1
```

构建会运行编译、自动化测试、源码自测、PyInstaller、正式界面冒烟测试、打包诊断、运行时许可证检查、ZIP 内容检查、本地路径/秘密扫描以及 SHA-256 生成。其默认输出为 `release-formal`；废弃的 `release` 目录不是交付目标。

真实的 Claude CLI 集成测试是显式的，仅使用本地环回服务器：

```powershell
$env:PYTHONPATH = "src"
$env:OMA_RUN_REAL_CLAUDE_CLI = "1"
python -m unittest discover -s tests -p "test_real_claude_cli.py" -v
```

上述命令均不使用真实中转站。真实的 GPT-5.6 中转站接收仍为手动操作，因为它需要用户的主机和凭据确认。
参见 `SECURITY.md`、`MIGRATION.md` 和 `RUNTIME_NOTICES.md`。

---

## English Version

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

### Runtime setup

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

#### GPT image relay

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

### Start

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

### Data layout

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

### Build and test

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
