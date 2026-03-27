from __future__ import annotations

import json
import random
from pathlib import Path


REAL_PACKAGES = ["requests", "numpy", "pandas", "fastapi", "sqlalchemy"]
FAKE_SUFFIX = ["pro", "secure", "ultimate", "plus"]


def generate_dataset(count: int = 100, output: str = "synthetic_hallucinations.jsonl") -> Path:
    out_path = Path(output)
    with out_path.open("w", encoding="utf-8") as fh:
        for _ in range(count):
            real = random.choice(REAL_PACKAGES)
            fake = f"{real}-{random.choice(FAKE_SUFFIX)}"
            row = {"code": f"import {fake}", "label": "hallucination", "alternative": real}
            fh.write(json.dumps(row) + "\n")
    return out_path
