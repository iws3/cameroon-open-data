# Parallel Corpora

Aligned translations between any pair of languages spoken in Cameroon.

**Recommended record types:** parallel_text

Every file in this folder is a `.jsonl` file with one record per line, checked against the schemas in the `schema` folder. Name your file with the year or a short description, for example `2021-short-description.jsonl`. Read `docs/FORMAT_GUIDE.md` for how each record type is written, and run `python tools/validate.py` before opening a pull request.
