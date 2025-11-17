"""Sync CSV files from `src/data/` into project `data/`.
Only overwrite target file if it is missing or contains only header.
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_DATA = os.path.join(ROOT, "src", "data")
DST_DATA = os.path.join(ROOT, "data")

os.makedirs(DST_DATA, exist_ok=True)

for fname in os.listdir(SRC_DATA):
    if not fname.lower().endswith('.csv'):
        continue
    src = os.path.join(SRC_DATA, fname)
    dst = os.path.join(DST_DATA, fname if fname != 'user.csv' else 'users.csv')

    # If destination missing -> copy
    if not os.path.exists(dst):
        shutil.copy(src, dst)
        print(f"Copied {src} -> {dst}")
        continue

    # If destination contains only header (1 or 0 lines) -> replace
    with open(dst, 'r', encoding='utf-8') as f:
        lines = [l for l in f.read().splitlines() if l.strip()]

    if len(lines) <= 1:
        shutil.copy(src, dst)
        print(f"Replaced (only header) {dst} with {src}")
    else:
        print(f"Kept existing {dst} (has {len(lines)} lines)")
