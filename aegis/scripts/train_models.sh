#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python backend/app/training/train_intent.py
python backend/app/training/train_deception.py
python backend/app/training/eval_models.py
