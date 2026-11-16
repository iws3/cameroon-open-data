# Lamnso' collection kit

This kit helps a group of Lamnso' speakers build the first open collection of everyday Lamnso' sentences, with matching recordings. It contains 200 original English sentences in 13 everyday areas, a sheet for translations, and a converter that turns the finished sheet into records for the collection.

## What is in the kit

`seed_sentences_en.csv` holds the English sentences, each with an id such as LNS-001 and an area such as greetings, health or film, music and stories. They are original to this project, so there is no copyright problem in translating or recording them.

`translation_template.csv` is the sheet translators fill in. It has one row per sentence and columns for the Lamnso' text, the translator, their village or area, notes about dialect, a reviewer and permission to share.

## How to translate

Give each translator the template, or a part of it. Translate the meaning, not word for word, the way you would say it to a neighbour. Write the sentence in the spelling you normally use for Lamnso', and the whole team should agree one spelling for the glottal stop and for special letters before starting, and keep to it. If a sentence does not make sense in daily life, such as a custom that does not exist, write a note and give the nearest natural sentence. Every sentence needs a second Nso speaker to read it and put their name in `reviewed_by`. Where two speakers say it differently, keep both versions as two rows and note the village of each. Differences between villages are useful data.

## How to record

Use a quiet room and a phone held about a hand's width from the mouth. Record one sentence per file, with a short pause before and after. Name each file `lns_<speaker>_<sentence id>.wav`, for example `lns_s01_LNS-017.wav`. Keep the original recording and never apply filters or noise reduction. Each speaker should read at least 100 sentences, and you should record a mix of men, women, older and younger people, and from different villages, because a system trained on one voice works badly for the others. Before recording, each speaker must hear the plan in their own language and agree to it. Write down their name or code, age group, gender, village and the date, and keep their signed or recorded consent.

## Turning the sheet into records

Rows are used only when the Lamnso' column is filled and `consent_to_share` says yes.

```bash
python tools/lamnso_kit_to_jsonl.py filled.csv --contributor "Your team" --batch 2026-12-first-round
python tools/validate.py
```

Then open a pull request as usual. Each batch becomes its own file, so batches never conflict.

## Please check

The records say who translated and who reviewed each sentence. A Lamnso' speaker should check the first batch before it is published. Audio files are not part of the repository. Keep them in a separate private store until you have decided how to share them, and share them only with the speakers' consent.
