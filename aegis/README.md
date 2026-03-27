# AEGIS Prototype

AEGIS is a dual-module prototype:
- **GhostGuard**: import/package verification for development-time protection.
- **Chimera**: adaptive deception environment for runtime attacker engagement.

## Quickstart

```bash
cd aegis
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Run deception decoy API:

```bash
./scripts/run_deception.sh
```

Run tests:

```bash
PYTHONPATH=backend pytest -q
```

## API Endpoints

- `POST /api/v1/package/verify`
- `POST /api/v1/deception/deploy`
- `POST /api/v1/threat/correlate`
- `GET /healthz`
- `WS /ws`

## VS Code Extension

From `extension/`:

```bash
npm install
npm run compile
```

Configure:
- `aegis.backendUrl`: backend URL (default `http://localhost:8000`)
- `aegis.token`: bearer token

## Notes

- Intent analysis uses a rule-based fallback and optional Redis cache.
- Decoy deployment currently simulates container IDs for MVP.
- Training scripts provide synthetic data generation and stub RL training.

## Next-Level Enhancements in this revision

- Added risk-aware package analysis (`risk_reason`, `typosquat_risk`) and a seeded trusted package catalog for offline-friendly detection.
- Added response orchestration API: `POST /api/v1/response/alert` for autonomous actions with manual-approval gating.
- Added MITRE ATT&CK technique hints and confidence level output in threat correlation.
- Upgraded WebSocket endpoint to multi-client broadcast with connection management.

