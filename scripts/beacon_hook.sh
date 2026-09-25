#!/bin/sh
# A recording failure is never a Claude permission or PMOS quality decision.
beacon_project_root=${CLAUDE_PROJECT_DIR:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}
if [ -x "$beacon_project_root/.venv/bin/python3" ]; then
  "$beacon_project_root/.venv/bin/python3" "$beacon_project_root/scripts/beacon_hook.py" >/dev/null 2>&1 || true
elif command -v python3 >/dev/null 2>&1; then
  python3 "$beacon_project_root/scripts/beacon_hook.py" >/dev/null 2>&1 || true
fi
exit 0
