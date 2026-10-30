#!/usr/bin/env python3
"""Turn a submitted GitHub issue form into a record in the right data folder.

Reads the issue text from the ISSUE_BODY environment variable. Used by the
workflow in .github/workflows/issue-to-record.yml, so contributors never touch it.
"""
import json
import os
import re
import sys

from common import ROOT, build_record, clean

LABELS = {
    "Exam": "exam",
    "Subject": "subject",
    "Year of the exam": "year",
    "Paper or section": "paper",
    "Question number": "number",
    "The question": "question",
    "Marks": "marks",
    "Describe any diagram, graph or table": "figure",
    "Answer or marking guide": "answer",
    "Language of the question": "language",
    "Where did this question come from?": "source",
    "Your right to share it": "rights",
    "Your name for credit": "contributor",
    "Agreement": "agreement",
}


def parse(body):
    parts = re.split(r"^### (.+?)\s*$", body, flags=re.M)
    fields = {}
    for i in range(1, len(parts), 2):
        key = LABELS.get(parts[i].strip())
        if key:
            fields[key] = clean(parts[i + 1])
    return fields


def fail(message):
    with open(os.environ.get("ERROR_FILE", "/tmp/submission-error.txt"), "w", encoding="utf-8") as fh:
        fh.write(message)
    print(message)
    sys.exit(1)


def main():
    fields = parse(os.environ.get("ISSUE_BODY", ""))
    for needed, human in [("exam", "Exam"), ("subject", "Subject"), ("question", "The question")]:
        if not fields.get(needed):
            fail(f"The box '{human}' is empty, so I could not create a record. Please edit your issue and fill it in.")
    if "[x]" not in fields.get("agreement", "").lower():
        fail("The agreement box was not ticked. Please tick it and try again.")
    record, folder, filename = build_record(fields, os.environ.get("ISSUE_USER", "anonymous"))
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    rel = path.relative_to(ROOT).as_posix()
    print("Wrote", rel)
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"path={rel}\n")


if __name__ == "__main__":
    main()
