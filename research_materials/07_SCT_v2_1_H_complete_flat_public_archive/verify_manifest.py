#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
root = Path(__file__).resolve().parent
manifest = root/'MANIFEST.sha256'
failures=[]
for line in manifest.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    h, rel = line.split('  ', 1)
    p = root/rel
    if not p.exists():
        failures.append((rel,'missing'))
        continue
    got = hashlib.sha256(p.read_bytes()).hexdigest()
    if got != h:
        failures.append((rel,'hash_mismatch'))
if failures:
    print('MANIFEST FAIL')
    for f in failures: print(f)
    sys.exit(1)
print('MANIFEST PASS', len(manifest.read_text(encoding='utf-8').splitlines()), 'files')
