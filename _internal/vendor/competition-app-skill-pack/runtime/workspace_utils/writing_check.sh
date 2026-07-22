#!/usr/bin/env bash
set -euo pipefail
: "${HC_PYTHON:?HC_PYTHON must be provided by the local runtime}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$HC_PYTHON" "$SCRIPT_DIR/workspace_check.py" writing "${1:-.}"

