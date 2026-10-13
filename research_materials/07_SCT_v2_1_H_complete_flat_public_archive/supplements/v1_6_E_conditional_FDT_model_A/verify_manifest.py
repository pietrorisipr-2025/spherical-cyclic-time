#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
base=Path(__file__).resolve().parent
manifest=base/'MANIFEST.sha256'
fail=[]
for line in manifest.read_text().splitlines():
    if not line.strip(): continue
    h, rel = line.split('  ',1)
    p=base/rel
    if not p.exists(): fail.append((rel,'missing')); continue
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=h: fail.append((rel,'hash_mismatch'))
if fail:
    print('MANIFEST FAIL')
    for item in fail: print(item)
    sys.exit(1)
print('MANIFEST PASS')
