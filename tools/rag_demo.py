#!/usr/bin/env python3
"""A small keyword (BM25) retriever over the exported chunks, as a baseline and a smoke test.

    python tools/export_rag.py
    python tools/rag_demo.py "Which people celebrate the Ngondo festival?"
    python tools/rag_demo.py --eval

It uses no libraries. Replace it with embeddings plus keyword search in your real system, and use --eval
(or the same idea in your own code) to check that every change makes retrieval better and not worse.
"""
import argparse
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

from common import ROOT

STOP = set("a an and are as at be by did do does for from how in is it its of on or that the their to was were what when where which who with".split())


def tokens(text):
    text = "".join(ch for ch in unicodedata.normalize("NFKD", text) if unicodedata.category(ch) != "Mn")
    return [w for w in re.findall(r"[a-z0-9]+", text.casefold()) if w not in STOP]


class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.tf = [Counter(d) for d in docs]
        self.len = [len(d) for d in docs]
        self.avg = sum(self.len) / len(self.len)
        df = Counter(w for d in self.tf for w in d)
        n = len(docs)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in df.items()}

    def score(self, query):
        q = tokens(query)
        out = []
        for i, tf in enumerate(self.tf):
            s = 0.0
            for w in q:
                if w in tf:
                    f = tf[w]
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
            out.append(s)
        return out

    def top(self, query, k):
        sc = self.score(query)
        return sorted(range(len(sc)), key=lambda i: -sc[i])[:k]


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?")
    ap.add_argument("--dir", default=str(ROOT / "build" / "rag"))
    ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--eval", action="store_true")
    a = ap.parse_args()
    d = Path(a.dir)
    chunks = load(d / "chunks.jsonl")
    index = BM25([tokens(c["title"] + " " + c["title"] + " " + c["text"]) for c in chunks])  # the title counts double

    if a.query:
        for rank, i in enumerate(index.top(a.query, a.k), 1):
            c = chunks[i]
            print(f"{rank}. {c['title']}  [{c['metadata']['folder']}]")
            print(f"   {c['text'][:170].replace(chr(10), ' | ')}")
            print(f"   source: {c['metadata'].get('source_url', 'n/a')}\n")
    if a.eval:
        ev = [e for e in load(d / "eval.jsonl") if e["relevant_chunk_ids"]]
        ids = [c["id"] for c in chunks]
        hits = {1: 0, 3: 0, 5: 0}
        rr, misses = 0.0, []
        for e in ev:
            ranked = [ids[i] for i in index.top(e["question"], 5)]
            rel = set(e["relevant_chunk_ids"])
            pos = next((r for r, cid in enumerate(ranked, 1) if cid in rel), None)
            for k in hits:
                hits[k] += bool(pos and pos <= k)
            rr += 1 / pos if pos else 0
            if not pos:
                misses.append(e["question"])
        n = len(ev)
        print(f"Questions with ground truth: {n}")
        print(f"hit@1 {hits[1] / n:.1%}   hit@3 {hits[3] / n:.1%}   hit@5 {hits[5] / n:.1%}   MRR {rr / n:.3f}")
        print("Missed in the top 5 (first 8):")
        for q in misses[:8]:
            print("  -", q)


if __name__ == "__main__":
    main()
