#!/usr/bin/env python3
"""Validate every .jsonl file under data/ (and docs/examples/) against the schemas.

Usage:
    python tools/validate.py              check everything
    python tools/validate.py path/to.jsonl  check one file or folder
"""
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<!\d)(?:\+?237[\s-]?)?6[5-9]\d[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}(?!\d)")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_validators():
    fc = FormatChecker()
    envelope = Draft202012Validator(load(SCHEMA_DIR / "record.schema.json"), format_checker=fc)
    meta = Draft202012Validator(load(SCHEMA_DIR / "meta.schema.json"), format_checker=fc)
    types = {
        p.name.replace(".schema.json", ""): Draft202012Validator(load(p), format_checker=fc)
        for p in (SCHEMA_DIR / "types").glob("*.schema.json")
    }
    return envelope, meta, types


def files_to_check(args):
    if args:
        targets = [Path(a) for a in args]
    else:
        targets = [ROOT / "data", ROOT / "docs" / "examples"]
    found = []
    for t in targets:
        if t.is_dir():
            found.extend(sorted(t.rglob("*.jsonl")))
        elif t.suffix == ".jsonl":
            found.append(t)
    return found


def check_file(path, envelope, meta, types):
    errors, warnings, count = [], [], 0
    seen_ids = set()
    with path.open(encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            count += 1
            where = f"{path}:{n}"
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{where}: not valid JSON ({exc.msg})")
                continue
            for e in envelope.iter_errors(rec):
                errors.append(f"{where}: {'/'.join(map(str, e.path)) or 'record'}: {e.message}")
            if not isinstance(rec, dict):
                continue
            for e in meta.iter_errors(rec.get("meta", {})):
                errors.append(f"{where}: meta/{'/'.join(map(str, e.path))}: {e.message}")
            validator = types.get(rec.get("type"))
            if validator:
                for e in validator.iter_errors(rec.get("content", {})):
                    errors.append(f"{where}: content/{'/'.join(map(str, e.path))}: {e.message}")
            rid = rec.get("id")
            if rid:
                if rid in seen_ids:
                    errors.append(f"{where}: duplicate id '{rid}' in this file")
                seen_ids.add(rid)
            text = json.dumps(rec.get("content", {}), ensure_ascii=False)
            if EMAIL.search(text):
                warnings.append(f"{where}: looks like it contains an email address. Remove personal contact details.")
            if PHONE.search(text):
                warnings.append(f"{where}: looks like it contains a phone number. Remove personal contact details.")
            if rec.get("meta", {}).get("rights") == "unclear_needs_review":
                warnings.append(f"{where}: rights are marked unclear, a maintainer will review before release.")
    return count, errors, warnings


def main():
    envelope, meta, types = build_validators()
    files = files_to_check(sys.argv[1:])
    total, all_errors, all_warnings = 0, [], []
    for f in files:
        c, e, w = check_file(f, envelope, meta, types)
        total += c
        all_errors += e
        all_warnings += w
    for w in all_warnings:
        print("WARNING", w)
    for e in all_errors:
        print("ERROR  ", e)
    print(f"\nChecked {len(files)} file(s), {total} record(s): {len(all_errors)} error(s), {len(all_warnings)} warning(s).")
    sys.exit(1 if all_errors else 0)


if __name__ == "__main__":
    main()
