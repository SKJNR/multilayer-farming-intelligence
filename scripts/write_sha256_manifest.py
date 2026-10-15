"""Write a SHA-256 manifest for source/data artifacts, excluding volatile caches.

Run this after tests/audit generation and immediately before packaging a snapshot.
Re-running scripts that change tracked artifacts (for example candidate_audit.json)
requires regenerating the manifest. The manifest itself is excluded.
"""
from __future__ import annotations
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "SHA256SUMS.txt"
EXCLUDED_FILES = {"SHA256SUMS.txt"}
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "build", "dist"}
rows = []
for path in sorted(ROOT.rglob("*")):
    relative = path.relative_to(ROOT)
    if not path.is_file():
        continue
    if relative.name in EXCLUDED_FILES or any(part in EXCLUDED_DIRS for part in relative.parts):
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append(f"{digest}  {relative.as_posix()}")
OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"Wrote {len(rows)} hashes to {OUT.relative_to(ROOT)} (volatile caches excluded)")
