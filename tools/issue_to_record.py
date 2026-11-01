#!/usr/bin/env python3
"""Turn a submitted GitHub issue form into a record in the right data folder.

Reads the issue text from the ISSUE_BODY environment variable. Used by the
workflow in .github/workflows/issue-to-record.yml, so contributors never touch it.
"""
import json
import os
import re
import sys

from common import ROOT, build_record, clean, existing_fingerprints
from forms_spec import FORMS
import generic_records

EXAM_LABELS = {
    "Exam": "exam", "Subject": "subject", "Year of the exam": "year", "Paper or section": "paper",
    "Question number": "number", "The question": "question", "Marks": "marks",
    "Describe any diagram, graph or table": "figure", "Answer or marking guide": "answer",
    "Language of the question": "language", "Where did this question come from?": "source",
    "Your right to share it": "rights", "Your name for credit": "contributor", "Agreement": "agreement",
}


def headings(body):
    return set(re.findall(r"^### (.+?)\s*$", body, flags=re.M))


def parse(body, labels):
    parts = re.split(r"^### (.+?)\s*$", body, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        key = labels.get(parts[i].strip())
        if key:
            out[key] = clean(parts[i + 1])
    return out


def fail(message):
    with open(os.environ.get("ERROR_FILE", "/tmp/submission-error.txt"), "w", encoding="utf-8") as fh:
        fh.write(message)
    print(message)
    sys.exit(1)


def detect(body):
    h = headings(body)
    if {"Exam", "The question"} <= h:
        return "exam"
    for form_id, spec in FORMS.items():
        if spec["marker"] in h:
            return form_id
    return None


def main():
    body = os.environ.get("ISSUE_BODY", "")
    user = os.environ.get("ISSUE_USER", "anonymous")
    form_id = detect(body)
    if not form_id:
        fail("I could not recognise this as one of the submission forms, so nothing was created.")

    if form_id == "exam":
        fields = parse(body, EXAM_LABELS)
        for needed, human in [("exam", "Exam"), ("subject", "Subject"), ("question", "The question")]:
            if not fields.get(needed):
                fail(f"The box '{human}' is empty, so I could not create a record. Please edit your issue and fill it in.")
        if "[x]" not in fields.get("agreement", "").lower():
            fail("The agreement box was not ticked. Please tick it and try again.")
        record, folder, filename, fp = build_record(fields, user)
    else:
        spec = FORMS[form_id]
        labels = {f["label"]: f["id"] for f in spec["fields"]}
        fields = parse(body, labels)
        for f in spec["fields"]:
            if f["req"] and f["kind"] != "checkboxes" and not fields.get(f["id"]):
                fail(f"The box '{f['label']}' is empty, so I could not create a record. Please edit your issue and fill it in.")
        if "[x]" not in fields.get("agreement", "").lower():
            fail("The agreement box was not ticked. Please tick it and try again.")
        record, folder, filename, fp = generic_records.build(form_id, fields, user)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"fingerprint={fp}\n")
    already = existing_fingerprints().get(fp)
    if already:
        fail(f"This is already in the collection ({already}). Thank you for trying! If you found a mistake in it, please open the 'Report an error in the data' form instead.")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    print("Wrote", rel)
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"path={rel}\n")


if __name__ == "__main__":
    main()
