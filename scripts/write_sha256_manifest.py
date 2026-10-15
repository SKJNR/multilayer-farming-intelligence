from __future__ import annotations
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "SHA256SUMS.txt"
EXCLUDED = {"SHA256SUMS.txt", ".git"}
rows = []
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or any(part in EXCLUDED for part in path.relative_to(ROOT).parts):
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"Wrote {len(rows)} hashes to {OUT.relative_to(ROOT)}")
