# Using the collection in a RAG system

This guide is for the team building a retrieval system on top of Cameroon Open Data, for example an assistant that answers questions about Cameroonian culture and entertainment. The data is stored as one small record per fact. The export tool turns those records into chunks that a retrieval system can load directly.

## Get the chunks

```bash
pip install -r requirements.txt
python tools/export_rag.py
```

This writes three files to `build/rag/`. Every push to the default branch also builds them in GitHub Actions, and you can download them from the run page as the `rag-export` artifact.

| File | What it holds |
|---|---|
| `chunks.jsonl` | One retrievable chunk per record: `id`, `title`, `text` and flat `metadata`. |
| `eval.jsonl` | Question and answer pairs for testing, each with the ids of the chunks that answer it. |
| `manifest.json` | Counts, the filters used, the licence and attribution notes. |

By default records marked `unclear_needs_review` for rights, and records marked culturally sensitive or needing community review, are left out. Change this with `--exclude-rights` and `--exclude-sensitivity`.

## What a chunk looks like

```json
{
  "id": "festival-ngondo",
  "title": "Ngondo",
  "text": "Ngondo (festival)\nType: Annual water-centred festival\nPeople: The Sawa coastal peoples, including the Duala, Bassa, Bakoko, Bakweri and Ewodi.\nPlace: Douala, on the banks of the Wouri River.\n...",
  "metadata": {
    "type": "structured_record",
    "sector": "culture",
    "folder": "culture/festivals-and-ceremonies",
    "path": "data/culture/festivals-and-ceremonies/traditional-festivals.jsonl",
    "line": 1,
    "region": "Littoral",
    "language": "en",
    "rights": "contributor_owned",
    "sensitivity": "none",
    "source_kind": "website",
    "source_citation": "Wikipedia, Ngondo (CC BY-SA 4.0), the Agenda 21 for Culture good practice page on the Ngondo, Xinhua via The Star (10 December 2025), and a Global Bush tour page. Compiled for this collection and not yet reviewed by a second person.",
    "contributor": "Fonyuy Gita",
    "collected_on": "2026-11-03",
    "licence": "CC BY-SA 4.0",
    "attribution": "Cameroon Open Data (CC BY-SA 4.0), contributed by Fonyuy Gita. Source: Wikipedia, Ngondo (CC BY-SA 4.0), the Agenda 21 for Culture good practice page on the Ngondo, Xinhua via The Star (10 December 2025), and a Global Bush tour page. Compiled for this collection and not yet reviewed by a second person.",
    "source_url": "https://en.wikipedia.org/wiki/Ngondo",
    "entity_type": "festival"
  }
}
```

The `text` field starts with the name of the thing, because that is what people ask about. The `metadata` values are plain strings and numbers, so they work as filters in any vector database.

## Loading it

Plain Python, no libraries:

```python
import json
chunks = [json.loads(line) for line in open("build/rag/chunks.jsonl", encoding="utf-8")]
```

LangChain (a sketch, not run in this repository):

```python
from langchain_core.documents import Document
docs = [Document(page_content=c["text"], metadata={**c["metadata"], "id": c["id"], "title": c["title"]}) for c in chunks]
```

LlamaIndex (a sketch, not run in this repository):

```python
from llama_index.core import Document
docs = [Document(text=c["text"], metadata=c["metadata"], doc_id=c["id"]) for c in chunks]
```

## Retrieval advice

Use keyword search and embeddings together, and give extra weight to an exact match on the record's name. `tools/rag_demo.py` is a keyword-only baseline with no libraries, and its mistakes show why: a question about the capital of the West Region can be outranked by records that merely mention that region.

A real example from the baseline: the question "Who is Ngonnso?" ranks the record about the statue above the record about Ngonnso' herself, because both mention her name many times. A reranker, or a filter on `entity_type`, fixes this kind of mistake.

Use the metadata for filters. `region` narrows a question about one part of the country, `sector` and `folder` separate culture from administration, and `type` and `entity_type` let you ask only about dishes, festivals or people.

Questions will arrive in English, French and Pidgin, and the records are in English with French names. Use a multilingual embedding model and test with French questions.

## How the assistant should answer

Show the source. Every chunk has `source_url` and an `attribution` line, and the CC BY-SA 4.0 licence requires credit.

Repeat caveats. Where sources disagree, the record says so, in fields such as `note`, `origin_note` and `caution`. The assistant should pass that on instead of choosing a side.

Say when it does not know. The records are compiled from cited sources and have not all been reviewed by a second person. The collection is small, so low retrieval scores should lead to an honest "I am not sure", not a guess.

Mind the dates. Facts about the current state of things (office holders, counts, allowances) carry a date or a caution, and may have changed.

## Testing retrieval

`eval.jsonl` holds question and answer pairs. Where a pair has a `based_on` link, `relevant_chunk_ids` is exact (`"relevance": "exact"`). Otherwise it is a guess from names and is marked `heuristic`. Questions with no ground truth have an empty list and should be skipped for retrieval tests.

Run the baseline with `python tools/rag_demo.py --eval`. On the current data it finds the right chunk in the top 3 for about 94% of the questions that have ground truth. Treat that as an upper bound: the questions were written from the same records and use their wording. Real users write vaguer, messier questions, so add some from your own logs.

The question and answer pairs are not in the index by default, so the answers cannot leak into the test. Use `--index-qa` if you want them as chunks as well, and test on separate questions if you do.

## Rights and licence

Everything in `chunks.jsonl` comes from the collection's CC BY-SA 4.0 data. Each chunk keeps its `rights` value, so a commercial product can filter further. Noncommercial datasets, such as the Oxford Pidgin corpus, are listed in the catalogue but never copied into the collection. Please have the licence checked against how your product will use it.
