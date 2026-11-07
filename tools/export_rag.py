#!/usr/bin/env python3
"""Export the collection in a form that is ready for a retrieval (RAG) system.

    python tools/export_rag.py                 writes build/rag/
    python tools/export_rag.py --index-qa      also puts question and answer pairs in the index

Outputs:
    chunks.jsonl    one retrievable chunk per record: id, title, text, metadata
    eval.jsonl      question and answer pairs for testing retrieval and answers
    manifest.json   counts, filters used, licence and attribution notes

By default question and answer pairs are NOT put in the index, so that you can use them to test it
without the answers leaking into the thing being tested. Use --index-qa if you want them as chunks too.
"""
import argparse
import json
import re
from datetime import date
from pathlib import Path

from common import ROOT, normalize

DATA = ROOT / "data"
LICENCE = "CC BY-SA 4.0"


def label(key):
    return key.replace("_", " ").capitalize()


def render(rec):
    """Turn one record into the text that gets embedded. The name comes first, because that is what people ask about."""
    t, c = rec["type"], rec["content"]
    if t == "structured_record":
        head = f"{c['name']} ({c['entity_type'].replace('_', ' ')})"
        lines = [f"{label(k)}: {v}" for k, v in c["attributes"].items()]
        if c.get("as_of_date"):
            lines.append(f"As of: {c['as_of_date']}")
        return c["name"], head + "\n" + "\n".join(lines)
    if t == "text_document":
        title = c.get("title") or c["kind"].replace("_", " ").capitalize()
        parts = [title, c["text"]]
        for k, lab in (("meaning_or_context", "Meaning or context"), ("translation_en", "English translation"), ("translation_fr", "French translation")):
            if c.get(k):
                parts.append(f"{lab}: {c[k]}")
        return title, "\n".join(parts)
    if t == "parallel_text":
        title = f"{c['source_language']} to {c['target_language']} translation"
        return title, f"{title}\n{c['source_language']}: {c['source_text']}\n{c['target_language']}: {c['target_text']}" + (f"\nSubject: {c['domain']}" if c.get("domain") else "")
    if t == "audio_transcript":
        return "Transcript of " + c["audio_file"], "Transcript of " + c["audio_file"] + "\n" + c["transcript"]
    if t == "exam_question":
        title = f"{c['exam_name']} {c['subject']}" + (f" {c['year']}" if c.get("year") else "")
        text = f"{title}, question {c.get('question_number', '')}\n{c['question_text']}".strip()
        if c.get("answer"):
            text += f"\nAnswer: {c['answer']}"
        return title, text
    if t == "qa_pair":
        return c["question"], f"Question: {c['question']}\nAnswer: {c['answer']}"
    return rec.get("id", ""), json.dumps(c, ensure_ascii=False)


def flat_meta(rec, path, line):
    m, s = rec["meta"], rec["meta"]["source"]
    parts = path.relative_to(DATA).parts
    out = {
        "type": rec["type"], "sector": parts[0], "folder": "/".join(parts[:-1]), "path": path.relative_to(ROOT).as_posix(), "line": line,
        "region": m.get("region", "national"), "language": ",".join(m["language"]), "rights": m["rights"],
        "sensitivity": m.get("sensitivity", "none"), "source_kind": s["kind"], "source_citation": s["citation"],
        "contributor": m["contributor"], "collected_on": m.get("collected_on", ""), "licence": LICENCE,
        "attribution": f"Cameroon Open Data ({LICENCE}), contributed by {m['contributor']}. Source: {s['citation']}",
    }
    if s.get("url"):
        out["source_url"] = s["url"]
    if rec["type"] == "structured_record":
        out["entity_type"] = rec["content"]["entity_type"]
    return out


def is_match(title, question):
    """Fallback for questions with no based_on link: the record's name (with or without a bracketed alias) appears in the question."""
    for variant in {title, re.sub(r"\([^)]*\)", " ", title)}:
        n = normalize(variant)
        if not n:
            continue
        if len(n) <= 4:
            if n in re.findall(r"[a-z0-9]+", normalize_words(variant if False else question)):
                return True
        elif n in normalize(question):
            return True
    return False


def normalize_words(s):
    import unicodedata
    s = "".join(ch for ch in unicodedata.normalize("NFKD", s) if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s.casefold())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "build" / "rag"))
    ap.add_argument("--index-qa", action="store_true", help="Also put question and answer pairs in chunks.jsonl.")
    ap.add_argument("--exclude-rights", nargs="*", default=["unclear_needs_review"])
    ap.add_argument("--exclude-sensitivity", nargs="*", default=["culturally_sensitive", "needs_community_review"])
    a = ap.parse_args()

    chunks, qas, seen_ids, excluded = [], [], set(), {"rights": 0, "sensitivity": 0}
    for path in sorted(DATA.rglob("*.jsonl")):
        with path.open(encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                rec = json.loads(line)
                if rec["meta"]["rights"] in a.exclude_rights:
                    excluded["rights"] += 1
                    continue
                if rec["meta"].get("sensitivity", "none") in a.exclude_sensitivity:
                    excluded["sensitivity"] += 1
                    continue
                title, text = render(rec)
                cid = rec.get("id") or f"{path.stem}-{n}"
                while cid in seen_ids:
                    cid += "-x"
                seen_ids.add(cid)
                chunk = {"id": cid, "title": title, "text": text, "metadata": flat_meta(rec, path, n)}
                if rec["type"] == "qa_pair":
                    qas.append((rec, chunk))
                    if not a.index_qa:
                        continue
                chunks.append(chunk)

    # evaluation set. Ground truth is exact when the question carries a based_on link, and a name-match guess otherwise.
    fact_chunks = [c for c in chunks if c["metadata"]["type"] != "qa_pair"]
    present = {c["id"] for c in fact_chunks}
    by_url = {}
    for c in fact_chunks:
        by_url.setdefault(c["metadata"].get("source_url", ""), []).append(c)
    ev = []
    for rec, ch in qas:
        c = rec["content"]
        url = c.get("evidence") or rec["meta"]["source"].get("url", "")
        rel = [i for i in c.get("based_on", []) if i in present]
        how = "exact"
        if not rel:
            rel = [x["id"] for x in by_url.get(url, []) if is_match(x["title"], c["question"])]
            how = "heuristic"
        ev.append({"id": ch["id"], "question": c["question"], "reference_answer": c["answer"], "topic": c.get("topic", ""),
                   "evidence_url": url, "relevant_chunk_ids": rel, "relevance": how if rel else "none"})

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in (("chunks.jsonl", chunks), ("eval.jsonl", ev)):
        with (out / name).open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    by_type, by_sector = {}, {}
    for c in chunks:
        by_type[c["metadata"]["type"]] = by_type.get(c["metadata"]["type"], 0) + 1
        by_sector[c["metadata"]["sector"]] = by_sector.get(c["metadata"]["sector"], 0) + 1
    manifest = {
        "generated_on": date.today().isoformat(), "source": "Cameroon Open Data", "licence": LICENCE,
        "chunks": len(chunks), "chunks_by_type": by_type, "chunks_by_sector": by_sector,
        "eval_questions": len(ev), "eval_questions_with_ground_truth": sum(1 for e in ev if e["relevant_chunk_ids"]),
        "eval_ground_truth_exact": sum(1 for e in ev if e["relevance"] == "exact"),
        "qa_pairs_indexed": a.index_qa, "excluded_records": excluded,
        "filters": {"exclude_rights": a.exclude_rights, "exclude_sensitivity": a.exclude_sensitivity},
        "notes": ["Show the attribution field when you use a chunk.", "Records are not yet reviewed by a second person unless verified_by says so.",
                  "Some records carry caveats where sources disagree. Repeat them instead of choosing a side."],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in ("chunks", "chunks_by_type", "eval_questions", "eval_questions_with_ground_truth", "eval_ground_truth_exact", "excluded_records")}, indent=2))
    print("Written to", out)


if __name__ == "__main__":
    main()
