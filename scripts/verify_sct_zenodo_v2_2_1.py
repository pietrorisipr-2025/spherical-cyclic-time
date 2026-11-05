#!/usr/bin/env python3
"""Check authoritative SCT v2.2.1 Zenodo assets and corrected toy labels.

This script checks file integrity and specified published CSV counts; it is
NOT an independent scientific/physical validation or a re-integration of ODEs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "release-notes" / "v2.2.1" / "assets.json"
DEFAULT_OUTPUT = ROOT / "original-zenodo-downloads" / "v2.2.1"


def digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "SCT-v2.2.1-integrity-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=90) as source, temporary.open("wb") as out:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                out.write(block)
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)


def check_csv(path: Path, expected: dict) -> str:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "classification" not in reader.fieldnames:
            raise ValueError(f"{path.name}: missing 'classification' column")
        total = 0
        ok = 0
        by_patch = Counter()
        for row in reader:
            total += 1
            is_ok = (row["classification"] or "").strip().casefold() == "ok toy"
            ok += int(is_ok)
            if is_ok and "patch" in row:
                by_patch[(row["patch"] or "").strip()] += 1
    if total != expected["rows"]:
        raise ValueError(f"{path.name}: rows {total}, expected {expected['rows']}")
    if ok != expected["ok_toy"]:
        raise ValueError(f"{path.name}: OK toy {ok}, expected {expected['ok_toy']}")
    for patch, count in expected.get("ok_by_patch", {}).items():
        if by_patch[patch] != count:
            raise ValueError(f"{path.name}: {patch} OK toy {by_patch[patch]}, expected {count}")
    return f"{total} rows, {ok} OK toy" + (f", by patch {dict(by_patch)}" if by_patch else "")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Download missing official files from Zenodo")
    parser.add_argument("--directory", type=Path, default=DEFAULT_OUTPUT, help="Location of original files")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["zenodo_record_id"] != 23964270 or manifest["version"] != "2.2.1":
        raise ValueError("Unexpected manifest release identifier")
    directory = args.directory.resolve()
    for item in manifest["assets"]:
        name = item["filename"]
        if Path(name).name != name:
            raise ValueError(f"Unsafe path in manifest: {name!r}")
        target = directory / name
        if not target.exists():
            if not args.download:
                raise FileNotFoundError(f"Missing {target}; pass --download to fetch the official copy")
            print(f"Downloading {name} from Zenodo...")
            download(item["url"], target)
        actual_md5 = digest(target, "md5")
        if actual_md5.lower() != item["md5"].lower():
            raise ValueError(f"{name}: MD5 MISMATCH {actual_md5} != {item['md5']}")
        detail = check_csv(target, item["expected_csv"]) if "expected_csv" in item else ""
        print(f"PASS {name}: MD5 {actual_md5}" + (f"; {detail}" if detail else ""))
    sha_note = (directory / "SCT_v2_2_N_PUBLIC_ERRATUM_WITH_CORRECTED_DATA.zip.sha256").read_text(encoding="utf-8")
    found = re.search(r"\b[0-9A-Fa-f]{64}\b", sha_note)
    if not found:
        raise ValueError("The Zenodo .sha256 file does not contain a 64-character SHA-256 value")
    archive = directory / "SCT_v2_2_N_PUBLIC_ERRATUM_WITH_CORRECTED_DATA.zip"
    actual_sha256 = digest(archive, "sha256")
    if actual_sha256.lower() != found.group().lower():
        raise ValueError("ZIP SHA-256 does not match the Zenodo companion checksum text")
    print(f"PASS ZIP SHA-256 {actual_sha256}")
    print("PASS all Zenodo byte-integrity and published CSV classification-count checks")
    print("NOTE: these checks do not independently reproduce numerical integration or validate a physical cosmology.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
