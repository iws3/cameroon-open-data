# National Languages

Text, speech and word lists in Cameroon's national languages. Use one subfolder per language, named by its ISO 639-3 code.

**Recommended record types:** parallel_text, audio_transcript, text_document

Every file in this folder is a `.jsonl` file with one record per line, checked against the schemas in the `schema` folder. Name your file with the year or a short description, for example `2021-short-description.jsonl`. Read `docs/FORMAT_GUIDE.md` for how each record type is written, and run `python tools/validate.py` before opening a pull request.
