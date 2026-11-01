"""Turns answers from the text, Q&A, translation and fact forms into a record."""
import re
from datetime import date

from common import record_fingerprint, slug
from forms_spec import (FACT_KINDS, FORMS, REGION_CHOICES, RIGHTS_CHOICES, SENSITIVITY_CHOICES, SOURCE_CHOICES,
                        TEXT_KINDS, resolve_folder, resolve_language, resolve_one)


def parse_details(text):
    attrs, notes = {}, []
    for line in text.splitlines():
        line = line.strip().lstrip("-* ").strip()
        if not line:
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            if key.strip() and val.strip():
                attrs[key.strip()] = val.strip()
                continue
        notes.append(line)
    if notes:
        attrs["note"] = " ".join(notes)
    return attrs


def build(form_id, f, user):
    spec = FORMS[form_id]
    kind = spec["type"]
    codes, note = resolve_language(f.get("language"), f.get("language_other"))
    content, stem_text = {}, ""

    if kind == "text_document":
        content = {"kind": TEXT_KINDS.get(f.get("kind"), "other"), "text": f["text"]}
        for src, dst in (("title", "title"), ("meaning", "meaning_or_context"), ("translation_en", "translation_en"), ("translation_fr", "translation_fr")):
            if f.get(src):
                content[dst] = f[src]
        stem_text = f.get("title") or f["text"]
    elif kind == "qa_pair":
        content = {"question": f["question"], "answer": f["answer"]}
        for k in ("topic", "evidence"):
            if f.get(k):
                content[k] = f[k]
        stem_text = f["question"]
    elif kind == "parallel_text":
        c1, n1 = resolve_one(f["first_language"])
        c2, n2 = resolve_one(f["second_language"])
        content = {"source_language": c1, "target_language": c2, "source_text": f["first_text"], "target_text": f["second_text"]}
        if f.get("domain"):
            content["domain"] = f["domain"]
        if f.get("dialect_note"):
            content["dialect_note"] = f["dialect_note"]
        codes = [c for c in dict.fromkeys([c1, c2])]
        note = "; ".join(x for x in [n1, n2] if x)
        stem_text = f["first_text"]
    elif kind == "structured_record":
        attrs = parse_details(f["details"])
        content = {"entity_type": FACT_KINDS.get(f.get("entity_type"), "other"), "name": f["name"], "attributes": attrs}
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", f.get("as_of", "")):
            content["as_of_date"] = f["as_of"]
        stem_text = f["name"]

    meta = {
        "contributor": f.get("contributor") or user,
        "language": codes,
        "source": {"kind": SOURCE_CHOICES.get(f.get("source_kind"), "other"), "citation": f.get("source_note", "")[:500] or "Submitted by a contributor"},
        "rights": RIGHTS_CHOICES.get(f.get("rights"), "unclear_needs_review"),
        "sensitivity": SENSITIVITY_CHOICES.get(f.get("sensitivity"), "none"),
        "collected_on": date.today().isoformat(),
    }
    if f.get("region") in REGION_CHOICES:
        meta["region"] = "national" if f["region"] == "Whole country" else f["region"]
    if note:
        meta["language_note"] = note

    record = {"type": kind, "meta": meta, "content": content}
    fp = record_fingerprint(record)
    stem = (slug(stem_text)[:40].strip("-") or kind.replace("_", "-")) + "-" + fp[:6]
    record = {"id": stem, **record}

    folder = resolve_folder(f.get("folder"), kind)
    if folder.name == "national-languages" and codes and codes[0] != "und":
        folder = folder / codes[0]
    return record, folder, stem + ".jsonl", fp
