#!/usr/bin/env python3
"""Convert a filled spreadsheet (CSV) into records placed in the correct data folders.

Usage:  python tools/csv_to_jsonl.py my-questions.csv
Each row becomes its own small file, so two people never edit the same file. Duplicates are skipped.
"""
import csv
import json
import sys

from common import ROOT, build_record, clean, existing_fingerprints

COLUMNS = {
    "exam": "exam", "subject": "subject", "year": "year", "paper": "paper", "section": "section",
    "question_number": "number", "question_text": "question", "marks": "marks",
    "figure_description": "figure", "answer": "answer", "answer_explanation": "explanation",
    "topics": "topics", "language": "language", "source": "source", "rights": "rights",
    "contributor": "contributor",
}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    written = {}
    seen = existing_fingerprints()
    skipped = 0
    with open(sys.argv[1], encoding="utf-8-sig", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), 2):
            fields = {COLUMNS[k]: clean(v) for k, v in row.items() if k in COLUMNS}
            if not fields.get("question"):
                continue
            if not fields.get("exam") or not fields.get("subject"):
                print(f"Row {n}: exam and subject are required, skipped.")
                continue
            record, folder, filename, fp = build_record(fields, "anonymous")
            if fp in seen:
                print(f"Row {n}: already in the collection ({seen[fp]}), skipped.")
                skipped += 1
                continue
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / filename
            path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
            seen[fp] = str(path.relative_to(ROOT))
            written[path] = 1
    print(f"{len(written)} new file(s) written, {skipped} duplicate(s) skipped.")
    print("Now run: python tools/validate.py")


if __name__ == "__main__":
    main()
