#!/usr/bin/env python3
"""Split the text of ONE exam paper into one record per numbered question.

You supply the text (typed, pasted, or produced by OCR from a paper you may use).
Each question becomes its own small file in the right data folder, so nothing conflicts.

Example:
    python tools/paper_to_jsonl.py paper.txt --exam "GCE Ordinary Level" --subject Physics \\
        --year 2019 --paper "Paper 2" --source-note "Typed from the author's own copy" --contributor Gita --dry-run

Remove --dry-run to write the files. Questions already in data/ are skipped.
"""
import argparse
import json
import re
import sys

from common import EXAM_FOLDERS, ROOT, build_record, existing_fingerprints

QNUM = re.compile(r"^\s*(\d{1,2})[.)]\s+\S")
QPREFIX = re.compile(r"^\s*\d{1,2}[.)]\s+")
SECTION = re.compile(r"^\s*(section\s+[ivx\d]+)\b", re.I)
MARKS = re.compile(r"\((\d+(?:\.\d+)?)\s*marks?\)", re.I)


def split_questions(text, drop):
    lines = [l.rstrip() for l in text.splitlines()]
    lines = [l for l in lines if not any(re.search(p, l, re.I) for p in drop)]
    questions, cur, expected, section = [], None, 1, ""
    for line in lines:
        s = SECTION.match(line)
        if s:
            word, num = s.group(1).split()[0], s.group(1).split()[-1]
            section = f"{word.capitalize()} {num.upper()}"
            continue
        m = QNUM.match(line)
        if m and int(m.group(1)) == expected:
            if cur:
                questions.append(cur)
            cur = {"number": m.group(1), "section": section, "lines": [QPREFIX.sub("", line, 1).strip()]}
            expected += 1
        elif cur is not None and line.strip():
            cur["lines"].append(line.strip())
    if cur:
        questions.append(cur)
    return questions


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("textfile")
    ap.add_argument("--exam", required=True, choices=list(EXAM_FOLDERS))
    ap.add_argument("--subject", required=True)
    ap.add_argument("--year", default="")
    ap.add_argument("--paper", default="")
    ap.add_argument("--language", default="English", choices=["English", "French"])
    ap.add_argument("--contributor", required=True)
    ap.add_argument("--source", default="past paper", choices=["past paper", "written by me", "textbook", "other"])
    ap.add_argument("--rights", default="official past paper", choices=["my own work", "permission granted", "official past paper", "not sure"])
    ap.add_argument("--source-note", default="", help="Say where your copy of the paper came from.")
    ap.add_argument("--drop", action="append", default=[], help="Regular expression for lines to ignore, such as adverts or watermarks. Can be repeated.")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    text = open(a.textfile, encoding="utf-8").read()
    questions = split_questions(text, a.drop)
    if not questions:
        sys.exit("No numbered questions found. Questions must start a line like '1. ...' and be numbered in order.")
    seen = existing_fingerprints()
    written = skipped = 0
    for q in questions:
        body = "\n".join(q["lines"])
        total = sum(float(x) for x in MARKS.findall(body))
        fields = {
            "exam": a.exam, "subject": a.subject, "year": a.year, "paper": a.paper, "section": q["section"],
            "number": q["number"], "question": body, "marks": (str(int(total)) if total == int(total) else str(total)) if total else "",
            "language": a.language, "source": a.source, "rights": a.rights, "contributor": a.contributor, "source_note": a.source_note,
        }
        record, folder, filename, fp = build_record(fields, a.contributor)
        label = f"Q{q['number']:>2}  marks={fields['marks'] or '?':<4} {body[:60]!r}"
        if fp in seen:
            print("skip (already in collection)", label)
            skipped += 1
            continue
        seen[fp] = filename
        if a.dry_run:
            print("would write", (folder / filename).relative_to(ROOT).as_posix(), "\n          ", label)
        else:
            folder.mkdir(parents=True, exist_ok=True)
            (folder / filename).write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
            print("wrote", (folder / filename).relative_to(ROOT).as_posix())
        written += 1
    print(f"\n{written} question(s) {'to write' if a.dry_run else 'written'}, {skipped} skipped.")
    if a.rights in ("official past paper", "not sure"):
        print("Rights are marked unclear. Do not push these to the public repository until the rights are cleared.")
    print("Next: python tools/validate.py, then bash tools/submit_pr.sh <branch-name> \"<title>\"")


if __name__ == "__main__":
    main()
