#!/usr/bin/env python3
"""Convert a filled spreadsheet (CSV) into records placed in the correct data folders.

Usage:  python tools/csv_to_jsonl.py my-questions.csv
Rows are grouped by exam, subject, year and paper and appended to the matching files.
"""
import csv
import json
import sys

from common import ROOT, build_record, clean

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
    with open(sys.argv[1], encoding="utf-8-sig", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), 2):
            fields = {COLUMNS[k]: clean(v) for k, v in row.items() if k in COLUMNS}
            if not fields.get("question"):
                continue
            if not fields.get("exam") or not fields.get("subject"):
                print(f"Row {n}: exam and subject are required, skipped.")
                continue
            record, folder, filename = build_record(fields, "anonymous")
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / filename
            with path.open("a", encoding="utf-8") as out:
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
            written[path] = written.get(path, 0) + 1
    for p, c in written.items():
        print(f"{c} record(s) -> {p.relative_to(ROOT)}")
    print("Now run: python tools/validate.py")


if __name__ == "__main__":
    main()
