#!/usr/bin/env python3
"""Turn a filled Lamnso' translation sheet into parallel text records (Lamnso' to English).

    python tools/lamnso_kit_to_jsonl.py filled.csv --contributor "Team name" --batch 2026-12-first-round

Rows are used only when the lamnso column is filled and consent_to_share says yes.
Output goes to a new file, data/languages/national-languages/lns/translations-<batch>.jsonl, so batches never conflict.
"""
import argparse
import csv
import json
import sys
from datetime import date

from common import ROOT, existing_fingerprints, record_fingerprint

OUT_DIR = ROOT / "data" / "languages" / "national-languages" / "lns"
YES = {"yes", "y", "true", "1", "oui"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csvfile")
    ap.add_argument("--contributor", required=True, help="Credit line used when the translator column is empty.")
    ap.add_argument("--batch", required=True, help="A short name for this round, used in the file name.")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    seen, rows, skipped = existing_fingerprints(), [], {"empty": 0, "no_consent": 0, "duplicate": 0}
    with open(a.csvfile, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            lns, en = (r.get("lamnso") or "").strip(), (r.get("english") or "").strip()
            if not lns or not en:
                skipped["empty"] += 1
                continue
            if (r.get("consent_to_share") or "").strip().lower() not in YES:
                skipped["no_consent"] += 1
                continue
            domain = ""
            note = (r.get("dialect_note") or "").strip()
            area = (r.get("village_or_area") or "").strip()
            if area:
                note = (note + " " if note else "") + f"Area: {area}."
            who = (r.get("translator") or "").strip() or a.contributor
            rid = "lns-" + (r.get("id") or "").strip().lower().replace("_", "-")
            rec = {"id": rid, "type": "parallel_text",
                   "meta": {"contributor": who, "language": ["lns", "en"], "region": "North-West", "rights": "contributor_owned", "sensitivity": "none",
                            "collected_on": date.today().isoformat(),
                            "source": {"kind": "personal_knowledge", "citation": "Translated by a Lamnso' speaker from the project's English seed sentence " + (r.get("id") or "").strip()}},
                   "content": {"source_language": "lns", "target_language": "en", "source_text": lns, "target_text": en, "domain": domain or "everyday sentences"}}
            if note:
                rec["content"]["dialect_note"] = note
            if (r.get("reviewed_by") or "").strip():
                rec["meta"]["verified_by"] = [x.strip() for x in r["reviewed_by"].split(";") if x.strip()]
            fp = record_fingerprint(rec)
            if fp in seen:
                skipped["duplicate"] += 1
                continue
            seen[fp] = rid
            rows.append(rec)
    out = OUT_DIR / f"translations-{a.batch}.jsonl"
    if a.dry_run:
        print(f"Would write {len(rows)} record(s) to {out.relative_to(ROOT)}. Skipped: {skipped}")
        return
    if not rows:
        sys.exit(f"Nothing to write. Skipped: {skipped}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(f"Wrote {len(rows)} record(s) to {out.relative_to(ROOT)}. Skipped: {skipped}")
    print("Next: python tools/validate.py")


if __name__ == "__main__":
    main()
