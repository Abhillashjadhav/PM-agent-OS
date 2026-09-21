set -euo pipefail
../peos/.venv/bin/python ../peos/examples/barebones/contract-file.py verify \
  --packet reviews/task-tracker-v1 \
  --root PM-agent-OS=. --root production-engineering-os=../peos \
  --freeze-digest sha256:1dd281e55cc20ce1861e3bed55799617191f38c5cc4e2322c7e463ef9a6e37f2 \
  --candidate ../peos/docs/evidence/task-tracker-live-20260918/live/candidate \
  --output ../approved-handoff-verification --authorized-host-fallback
