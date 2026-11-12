#!/usr/bin/env python3
"""Verify the initial skill snapshot without executing any skill code."""
import hashlib
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
records = json.loads((root / "inventory/skillshare-2026-11-12.json").read_text())
errors = []
for item in records:
    path = root / item["path"]
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
        errors.append(item["path"])
if errors:
    raise SystemExit("FAILED:\n" + "\n".join(errors))
print(f"Verified {len(records)} files")
