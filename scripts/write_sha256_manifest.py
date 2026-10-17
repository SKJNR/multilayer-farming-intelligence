from __future__ import annotations
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {".git", ".pytest_cache", "__pycache__"}
EXCLUDE_FILES = {"SHA256SUMS.txt"}


def compute_lines() -> list[str]:
    lines = []
    for p in sorted(ROOT.rglob("*")):
        if p.is_dir():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.suffix in {".pyc", ".pyo"} or p.name in EXCLUDE_FILES:
            continue
        rel = p.relative_to(ROOT).as_posix()
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{h}  {rel}")
    return lines


def main() -> None:
    lines = compute_lines()
    manifest_path = ROOT / "SHA256SUMS.txt"
    if "--check" in sys.argv:
        existing = manifest_path.read_text(encoding="utf-8").strip().splitlines()
        if existing != lines:
            raise SystemExit("SHA256SUMS.txt mismatch!")
        print(f"Verified {len(lines)} file hashes in SHA256SUMS.txt: ALL OK.")
    else:
        manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote {len(lines)} clean file hashes to SHA256SUMS.txt.")


if __name__ == "__main__":
    main()
