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

from common import normalize, record_fingerprint

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


def repo_duplicates(files):
    """Exact repeats are errors. Same numbered exam question or same named thing with different content is a warning."""
    errors, warnings = [], []
    by_fp, by_key = {}, {}
    data_root = ROOT / "data"
    for path in files:
        try:
            path.resolve().relative_to(data_root)
        except ValueError:
            continue
        with path.open(encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(rec, dict):
                    continue
                c, where = rec.get("content", {}), f"{path}:{n}"
                fp = record_fingerprint(rec)
                if fp in by_fp:
                    errors.append(f"{where}: same as {by_fp[fp]}. Please do not add it twice.")
                else:
                    by_fp[fp] = where
                key = None
                if rec.get("type") == "exam_question" and c.get("year") and c.get("question_number"):
                    key = ("exam", c.get("exam_name"), c.get("subject"), c.get("year"), c.get("paper"), c.get("section"), c.get("question_number"))
                elif rec.get("type") == "structured_record":
                    key = ("fact", normalize(c.get("entity_type", "")), normalize(c.get("name", "")))
                if key:
                    if key in by_key and by_key[key][1] != fp:
                        warnings.append(f"{where}: describes the same thing as {by_key[key][0]} but with different content. A reviewer should compare or merge them.")
                    by_key.setdefault(key, (where, fp))
    return errors, warnings


def main():
    envelope, meta, types = build_validators()
    files = files_to_check(sys.argv[1:])
    total, all_errors, all_warnings = 0, [], []
    for f in files:
        c, e, w = check_file(f, envelope, meta, types)
        total += c
        all_errors += e
        all_warnings += w
    dup_e, dup_w = repo_duplicates(files)
    all_errors += dup_e
    all_warnings += dup_w
    for w in all_warnings:
        print("WARNING", w)
    for e in all_errors:
        print("ERROR  ", e)
    print(f"\nChecked {len(files)} file(s), {total} record(s): {len(all_errors)} error(s), {len(all_warnings)} warning(s).")
    sys.exit(1 if all_errors else 0)


if __name__ == "__main__":
    main()
