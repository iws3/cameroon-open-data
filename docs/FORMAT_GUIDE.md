# Format guide

Every contribution is a `.jsonl` file. That means a plain text file where each line is one complete record written as JSON. You can write it by hand, produce it from a spreadsheet, or generate it with a script. Always save it as UTF-8.

Working examples of every record type are in `docs/examples/format-illustrations.jsonl`. They are format illustrations only and are not real data.

## The shape of every record

Each record has four parts.

- `id` (optional): a short stable name for the record, using lowercase letters, numbers, dots, dashes and underscores. It must be unique inside its file.
- `type`: one of `exam_question`, `qa_pair`, `text_document`, `parallel_text`, `audio_transcript`, `structured_record`.
- `meta`: honest information about the record. Described below.
- `content`: the data itself, with fields that depend on the type.

## The meta block

| Field | Required | Meaning |
|---|---|---|
| `contributor` | yes | Your GitHub username or the name you want to be credited under. |
| `language` | yes | List of language codes. `en` English, `fr` French, `pcm` Cameroon Pidgin English. For other languages use the ISO 639-3 code. |
| `source.kind` | yes | One of `exam_paper`, `official_publication`, `book`, `newspaper_or_magazine`, `website`, `broadcast`, `oral_tradition`, `field_recording`, `personal_knowledge`, `other`. |
| `source.citation` | yes | Where it came from, written so another person can find it. |
| `source.url`, `source.year` | no | A link and the year of the source. |
| `rights` | yes | One of `public_domain`, `open_license`, `contributor_owned`, `permission_granted`, `official_public_document`, `unclear_needs_review`. |
| `region` | no | `national` or one of the ten regions: Adamawa, Centre, East, Far North, Littoral, North, North-West, South, South-West, West. |
| `sensitivity` | no | `none`, `personal_information_removed`, `culturally_sensitive`, `needs_community_review`. |
| `collected_on` | no | Date in the form 2024-05-31. |
| `verified_by` | no | List of members who checked the record. |

## The six record types

### exam_question
Required: `exam_name`, `subject`, `year`, `question_text`. Optional: `exam_body`, `session`, `paper`, `question_number`, `question_format` (multiple_choice, short_answer, essay, problem_solving, practical, true_false, fill_in, other), `options`, `answer`, `answer_explanation`, `marks`, `topics`, `figure_file`.

Keep the question in its original language. If a question depends on a diagram, save the image beside your file and give its relative path in `figure_file`.

### qa_pair
Required: `question`, `answer`. Optional: `topic`, `evidence`.

### text_document
Required: `kind` and `text`. Kinds include proverb, folktale, song_lyrics, poem, speech, law_text, news_article, article, description, recipe, dictionary_entry, oral_history and other. Optional: `title`, `author_or_speaker`, `translation_en`, `translation_fr`, `meaning_or_context`.

### parallel_text
Required: `source_language`, `target_language`, `source_text`, `target_text`. Optional: `domain`, `dialect_note`.

### audio_transcript
Required: `audio_file`, `transcript`. Optional: `translation_en`, `translation_fr`, `duration_seconds`, `speaker_count`, `dialect_note`, `consent_of_speakers`.

### structured_record
Required: `entity_type`, `name`, `attributes` (an object with at least one entry). Optional: `as_of_date`. Use this for institutions, places, laws, crops, statistics and similar facts. For statistics always include the date the figure refers to.

## Using a spreadsheet

If you prefer a spreadsheet, put one record per row, export it to CSV, and ask a maintainer for help converting it. A conversion script for common sheets is welcome as a contribution to the `tools` folder.

## Checking your work

Run `python tools/validate.py` from the root of the repository. To check a single file, give its path: `python tools/validate.py data/education/gce/ordinary-level/2018-chemistry-paper-2.jsonl`. The same check runs automatically on every pull request.
