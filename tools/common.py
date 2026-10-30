"""Shared helpers for turning simple contributions into schema-valid records."""
import re
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GCE = ROOT / "data" / "education" / "gce"
EDU = ROOT / "data" / "education"

EXAM_FOLDERS = {
    "GCE Ordinary Level": GCE / "ordinary-level",
    "GCE Advanced Level": GCE / "advanced-level",
    "Technical GCE Ordinary Level": GCE / "technical-ordinary-level",
    "Technical GCE Advanced Level": GCE / "technical-advanced-level",
    "Other GCE examination": GCE / "other-gce-examinations",
    "BEPC": EDU / "francophone-secondary" / "bepc",
    "Probatoire": EDU / "francophone-secondary" / "probatoire",
    "Baccalauréat": EDU / "francophone-secondary" / "baccalaureat",
    "Baccalauréat technique": EDU / "francophone-secondary" / "baccalaureat-technique",
    "CAP or BEP": EDU / "francophone-secondary" / "cap-bep",
    "FSLC": EDU / "primary" / "fslc",
    "CEP": EDU / "primary" / "cep",
    "Common Entrance": EDU / "primary" / "common-entrance",
    "University or professional concours": EDU / "university-concours" / "other-concours",
    "Other": ROOT / "data" / "_inbox",
}

SOURCE_KINDS = {
    "a past paper i have": "exam_paper",
    "past paper": "exam_paper",
    "i wrote it myself": "personal_knowledge",
    "written by me": "personal_knowledge",
    "a textbook or revision book": "book",
    "textbook": "book",
    "another source": "other",
    "other": "other",
}

RIGHTS = {
    "i wrote it myself": "contributor_owned",
    "my own work": "contributor_owned",
    "i have written permission from the owner": "permission_granted",
    "permission granted": "permission_granted",
    "it is an official past paper and the maintainers should check the rights": "unclear_needs_review",
    "official past paper": "unclear_needs_review",
    "i am not sure": "unclear_needs_review",
    "not sure": "unclear_needs_review",
}

LANGUAGES = {"english": ["en"], "french": ["fr"], "both english and french": ["en", "fr"], "en": ["en"], "fr": ["fr"]}


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "unknown"


def clean(value):
    if value is None:
        return ""
    value = value.strip()
    return "" if value in ("_No response_", "None") else value


def target_folder(exam, subject):
    base = EXAM_FOLDERS.get(exam, ROOT / "data" / "_inbox")
    sub = base / slug(subject)
    if sub.is_dir():
        return sub
    other = base / "other-subjects"
    if other.is_dir():
        return other
    return base


def build_record(f, contributor_fallback):
    """f is a dict of cleaned simple fields. Returns (record, folder, filename)."""
    exam = f["exam"]
    subject = f["subject"]
    content = {"exam_name": exam, "subject": subject, "question_text": f["question"]}
    year = f.get("year", "")
    if year.isdigit():
        content["year"] = int(year)
    if f.get("paper"):
        content["paper"] = f["paper"]
    if f.get("section"):
        content["section"] = f["section"]
    if f.get("number"):
        content["question_number"] = f["number"]
    marks = f.get("marks", "")
    try:
        if marks:
            content["marks"] = float(marks) if "." in marks else int(marks)
    except ValueError:
        pass
    if f.get("figure"):
        content["figure_description"] = f["figure"]
    if f.get("answer"):
        content["answer"] = f["answer"]
    if f.get("explanation"):
        content["answer_explanation"] = f["explanation"]
    if f.get("topics"):
        content["topics"] = [t.strip() for t in f["topics"].split(";") if t.strip()]

    kind = SOURCE_KINDS.get(f.get("source", "").lower(), "other")
    rights = RIGHTS.get(f.get("rights", "").lower(), "unclear_needs_review")
    citation_bits = [exam, subject, str(year) if year else "", f.get("paper", "")]
    label = " ".join(b for b in citation_bits if b)
    prefix = {"exam_paper": "Past paper submitted by a contributor: ",
              "personal_knowledge": "Written by the contributor: ",
              "book": "Textbook or revision book: "}.get(kind, "Submitted by a contributor: ")
    meta = {
        "contributor": f.get("contributor") or contributor_fallback,
        "language": LANGUAGES.get(f.get("language", "english").lower(), ["en"]),
        "source": {"kind": kind, "citation": prefix + label},
        "rights": rights,
        "region": "national",
        "collected_on": date.today().isoformat(),
    }
    if year.isdigit():
        meta["source"]["year"] = int(year)

    folder = target_folder(exam, subject)
    paper = slug(f.get("paper", "")) if f.get("paper") else "questions"
    filename = f"{year if year.isdigit() else 'unknown-year'}-{slug(subject)}-{paper}.jsonl"
    rid = "-".join(x for x in [slug(subject), year if year.isdigit() else "unknown-year", paper, "q" + slug(f.get("number", "")) if f.get("number") else ""] if x)
    record = {"id": rid.lower(), "type": "exam_question", "meta": meta, "content": content}
    return record, folder, filename
