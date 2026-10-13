#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys

root = Path(__file__).resolve().parent
manifest = root / 'MANIFEST.sha256'
ok = True
for line in manifest.read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    expected, rel = line.split('  ', 1)
    path = root / rel
    if not path.exists():
        print(f'MISSING {rel}')
        ok = False
        continue
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    actual = h.hexdigest()
    if actual != expected:
        print(f'HASH_MISMATCH {rel} expected={expected} actual={actual}')
        ok = False
if ok:
    print('MANIFEST OK')
sys.exit(0 if ok else 1)
