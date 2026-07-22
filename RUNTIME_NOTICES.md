# Runtime And Redistribution Notice

## Included compatibility runtime

The formal portable package includes Pillow 12.2.0 for CPython 3.10 on Windows
x86-64 because the preserved v0.2.9 interface imports `PIL.ImageTk`.

- Artifact: `pillow-12.2.0-cp310-cp310-win_amd64.whl`
- Artifact SHA-256:
  `673aa32138f3e7531ccdbca7b3901dba9b70940a19ccecc6a37c77d5fdeb05b5`
- Runtime location: `_internal\formal_runtime\PIL`
- License: `_internal\formal_runtime\PIL-LICENSE.txt`
- Provenance: `_internal\formal_runtime\PIL-PROVENANCE.txt`

The artifact hash was matched against the official PyPI 12.2.0 JSON metadata
before its runtime files and license were copied into this project. The build
requires these project-local files and does not fall back to another installed
ModelCraft package.

## Included DrawIO runtime

The portable package includes the signed JGraph DrawIO desktop runtime so the
diagram step remains portable and does not search arbitrary drives or install
software globally.

- Product: draw.io 28.2.5
- Executable: `runtime\drawio\draw.io.exe`
- Executable SHA-256:
  `D34969D2CD3A076CD1BBFCE69F3A7CE8B52BA90E6FCD0171B1B6E967B2A799AD`
- Authenticode signer: JGraph Ltd
- Included Electron/Chromium notices remain beside the executable.

## Included scientific Python runtime

The packaged executable also acts as the `HC_PYTHON` interpreter used by the
workflow. PyInstaller includes the installed CPython runtime plus NumPy, SciPy,
pandas, Matplotlib, scikit-learn, SymPy, NetworkX, openpyxl, and seaborn. Their
distribution metadata and bundled license files are retained in `_internal`.
The build uses the explicitly selected CPython 3.10 environment and never
copies Python files from another installed desktop product.

## Externally discovered tools

The portable ZIP does not bundle Node.js, Claude Code CLI, Git, Pandoc, or a
LaTeX distribution.

The application can discover these tools from:

1. a path explicitly configured by the user;
2. the application-local `runtime/` directory;
3. known per-user or system installation locations;
4. the current process `PATH`.

When no compatible Claude Code installation exists, the application installs
the pinned CLI into its own `runtime\claude-code` npm prefix. When that install
also needs Node.js, the verified portable Node archive is placed under
`runtime\node`. Existing compatible installations remain preferred and are not
modified. Claude Code compatibility is determined by a local capability probe;
versions `2.1.132` and `2.1.177` are the prevalidated references.

Node.js and optional document tools remain subject to their respective
licenses. Before redistributing a customized package that embeds any runtime,
review that runtime's license and add its required notices and source offers.

The repository's built-in Skills and templates are packaged from the existing
project resources. No third-party commercial binary modules, encrypted Skills,
branding assets, or protected source are copied into the reconstructed release.

## Built-in Skill resources

The formal package contains 88 built-in Skills:

- 71 academic modeling Skills from
  `vendor\academic-agent-skills-main\skills`;
- 17 competition application Skills from
  `vendor\competition-app-skill-pack\skills`.

The competition Skill package's `.codex-plugin\plugin.json` declares the
package license as MIT. Its manifest, README, contracts, workflow definitions,
evaluations, and Skill files are preserved with the package.

The upstream materials accompanying the 71 academic Skills do not provide
clear license evidence in this repository. Their provenance is retained, but
this notice does not infer or grant redistribution rights. Anyone
redistributing a customized package must independently confirm that they have
the required rights for those materials.
