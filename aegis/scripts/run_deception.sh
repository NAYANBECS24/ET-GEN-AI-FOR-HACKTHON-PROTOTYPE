#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m uvicorn deception.decoys.api:app --host 0.0.0.0 --port 8081
