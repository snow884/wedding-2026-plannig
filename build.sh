#!/usr/bin/env bash
# One-command rebuild of all cards + master battle plan, followed by the audit.
# Usage: ./build.sh            (regenerate, then audit)
#        ./build.sh --audit    (audit only, no regeneration)
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-$(command -v python3 || command -v python)}"

if [[ "${1:-}" != "--audit" ]]; then
  "$PY" generate_cards.py >/dev/null
  echo "Regenerated cards/ ($(ls cards/*.html | wc -l | tr -d ' ') HTML files)"
fi

# Audit exit codes: 0 clean, 1 gaps/broken links, 2 only unmapped cells (review).
set +e
"$PY" audit_cards.py
status=$?
set -e
exit $status
