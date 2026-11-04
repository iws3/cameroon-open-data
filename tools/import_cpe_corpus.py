#!/usr/bin/env python3
"""Convert the Spoken Corpus of Cameroon Pidgin English (Oxford Text Archive, ota:2563) into AI-ready files.

The corpus is licensed CC BY-NC-SA 3.0 (noncommercial, share-alike, attribution required).
Because of the noncommercial condition the output goes to build/cpe-corpus, NOT into data/,
which is licensed CC BY-SA 4.0. Keep it separate, keep the NOTICE file with it, and do not use it commercially.

Step 1, look at what is inside:
    python tools/import_cpe_corpus.py --zip 2563.zip --inspect
Step 2, convert:
    python tools/import_cpe_corpus.py --zip 2563.zip --contributor "Your Name"

Outputs (in --out):
    utterances.jsonl   one utterance per line with speaker and source file
    documents.jsonl    one audio_transcript record per recording, in this project's schema
    text.train.txt / text.valid.txt   plain text, one utterance per line, for language models
    NOTICE.md, stats.json
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

from common import ROOT, slug

TURN = re.compile(r"<\$([^>\s]+)>")                 # speaker tag, as in ICE-style mark-up
UNIT = re.compile(r"<#(?::[^>]*)?>")                 # text unit marker
COMMENT = re.compile(r"<&>.*?</&>", re.S)            # editorial comments
UNCLEAR = re.compile(r"<\.>.*?</\.>", re.S)          # unclear words
TAG = re.compile(r"<[^>]*>")
DOC_NAMES = re.compile(r"(manual|readme|participant|spelling|word.?list|guide|metadata|licen[cs]e)", re.I)
POS_NAMES = re.compile(r"(tag|pos)", re.I)
AUDIO_EXT = {".wav", ".mp3"}

NOTICE = """# Spoken Corpus of Cameroon Pidgin English, converted

Original work: Green, M., Ayafor, M. and Ozon, G. (2016). A spoken corpus of Cameroon Pidgin English: pilot study.
Oxford Text Archive, ota:2563. http://ota.ox.ac.uk/desc/2563

Licence: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0).
https://creativecommons.org/licenses/by-nc-sa/3.0/

Changes made: mark-up removed or simplified, transcripts split into utterances by speaker, converted to JSON Lines
and plain text. The audio is unchanged and is not included here.

What this means: you must credit the authors, you may not use this material commercially, and anything you
build from it must be shared under the same licence. This material is not part of the CC BY-SA 4.0 data
collection in this project's data folder. Participant details that came with the original corpus were not read
and must not be published.
"""


def read_text(path):
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def parse(text, drop_unclear=False):
    text = COMMENT.sub(" ", text.replace("\r\n", "\n").replace("\r", "\n"))
    if drop_unclear:
        text = UNCLEAR.sub(" ", text)
    parts = TURN.split(text)
    turns = [("unknown", parts[0])] if len(parts) == 1 else [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]
    out = []
    for speaker, body in turns:
        for unit in UNIT.split(body):
            t = re.sub(r"\s+", " ", TAG.sub(" ", unit)).strip()
            if t:
                out.append((speaker, t))
    return out


def find_files(root, ext, include, exclude):
    files = sorted(p for p in root.rglob("*") if p.is_file())
    audio = {p.stem.lower(): p.name for p in files if p.suffix.lower() in AUDIO_EXT}
    inc, exc = (re.compile(include, re.I) if include else None), (re.compile(exclude, re.I) if exclude else None)
    chosen = []
    for p in files:
        if p.suffix.lower() != ext.lower():
            continue
        if exc and exc.search(p.name):
            continue
        if inc and not inc.search(p.name):
            continue
        if not inc and (DOC_NAMES.search(p.name) or POS_NAMES.search(p.name)):
            continue
        chosen.append(p)
    return files, chosen, audio


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--zip", help="The corpus zip downloaded from the Oxford Text Archive.")
    src.add_argument("--dir", help="A folder where the corpus is already unzipped.")
    ap.add_argument("--out", default=str(ROOT / "build" / "cpe-corpus"))
    ap.add_argument("--contributor", help="Your name, for the credit line. Required when converting.")
    ap.add_argument("--inspect", action="store_true", help="Only list the files and show the start of two transcripts.")
    ap.add_argument("--ext", default=".txt", help="Transcript file extension.")
    ap.add_argument("--include", help="Regular expression that transcript file names must match.")
    ap.add_argument("--exclude", help="Regular expression for file names to skip.")
    ap.add_argument("--drop-unclear", action="store_true", help="Remove words marked as unclear.")
    ap.add_argument("--valid-every", type=int, default=10, help="Every Nth recording goes to the validation text file.")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.zip:
        root = out / "raw"
        with zipfile.ZipFile(a.zip) as z:
            z.extractall(root)
    else:
        root = Path(a.dir)

    files, chosen, audio = find_files(root, a.ext, a.include, a.exclude)
    if a.inspect:
        by_ext = {}
        for p in files:
            by_ext.setdefault(p.suffix.lower() or "(none)", []).append(p)
        print("Files by type:")
        for e, ps in sorted(by_ext.items()):
            print(f"  {e:8} {len(ps):4} files, {sum(x.stat().st_size for x in ps) / 1e6:.1f} MB, e.g. {ps[0].name}")
        print(f"\n{len(chosen)} file(s) would be treated as transcripts. First few: {[p.name for p in chosen[:5]]}")
        for p in chosen[:2]:
            print(f"\n----- {p.name} (first 25 lines)")
            print("\n".join(read_text(p).splitlines()[:25]))
        print("\nSend me the file list and one of these samples if the transcripts look wrong, and I will adjust the parser.")
        return

    if not a.contributor:
        sys.exit("--contributor is required when converting.")
    if not chosen:
        sys.exit("No transcript files found. Run with --inspect, then use --ext, --include or --exclude.")

    all_utts, docs, train, valid, words = [], [], [], [], 0
    for idx, p in enumerate(chosen):
        utts = parse(read_text(p), a.drop_unclear)
        if not utts:
            continue
        for i, (spk, t) in enumerate(utts):
            all_utts.append({"source_file": p.name, "utterance_index": i, "speaker": spk, "text": t})
            words += len(t.split())
            (valid if a.valid_every and idx % a.valid_every == a.valid_every - 1 else train).append(t)
        speakers = {s for s, _ in utts if s != "unknown"}
        content = {"audio_file": audio.get(p.stem.lower(), p.stem + ".wav"),
                   "transcript": "\n".join(f"{s}: {t}" for s, t in utts),
                   "dialect_note": "Cameroon Pidgin English with code switching. Spelling follows the corpus orthography."}
        if speakers:
            content["speaker_count"] = len(speakers)
        docs.append({"id": ("cpe-" + slug(p.stem))[:80], "type": "audio_transcript", "meta": {
            "contributor": a.contributor, "language": ["wes"], "region": "national", "rights": "open_license",
            "source": {"kind": "other", "year": 2016, "url": "http://ota.ox.ac.uk/desc/2563",
                       "citation": "Green, Ayafor and Ozon (2016), A spoken corpus of Cameroon Pidgin English, Oxford Text Archive ota:2563. Licence CC BY-NC-SA 3.0 (noncommercial). Mark-up removed and converted to JSON Lines."}},
            "content": content})

    def dump(name, rows):
        with (out / name).open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    dump("utterances.jsonl", all_utts)
    dump("documents.jsonl", docs)
    (out / "text.train.txt").write_text("\n".join(train) + "\n", encoding="utf-8")
    (out / "text.valid.txt").write_text("\n".join(valid) + ("\n" if valid else ""), encoding="utf-8")
    (out / "NOTICE.md").write_text(NOTICE, encoding="utf-8")
    stats = {"recordings": len(docs), "utterances": len(all_utts), "words": words, "train_utterances": len(train), "valid_utterances": len(valid)}
    (out / "stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))
    print(f"Written to {out}. Check it with: python tools/validate.py {out / 'documents.jsonl'}")


if __name__ == "__main__":
    main()
