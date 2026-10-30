# How to contribute

Thank you for being here. Every record, big or small, makes Cameroon a little more visible to the tools of the future. This guide takes you from your first idea to a merged contribution.

## Ways to help

You can add records, correct records that contain mistakes, review pull requests from other members, translate records into other languages, record and transcribe speech, suggest a new folder, or improve these guides. Reviewing and correcting are as valuable as adding.

## The easiest way

If you are not a developer, read `docs/EASY_START.md`. You can contribute by filling in a web form, by sharing photos of a paper, or by sending a spreadsheet. No code and no file formats are involved.

## Step by step for developers

1. Make sure you have been given access. See `ACCESS.md`.
2. Fork the repository using the Fork button on its GitHub page, then clone your fork to your computer.
3. Install the checker once by running `pip install -r requirements.txt`.
4. Open the `data` folder and find the folder that fits your material. Read the short `README.md` in it. If nothing fits, use `data/_inbox`.
5. Create a file ending in `.jsonl` with a name that starts with the year or a clear description, for example `2018-chemistry-paper-2.jsonl`. Put one record on each line.
6. Write your records following `docs/FORMAT_GUIDE.md`. The six record types and their fields are explained there with examples.
7. Run `python tools/validate.py` and fix anything it reports.
8. Commit your work, push it to your fork, and open a pull request. In the description, say what you added, where it came from, and anything the reviewer should look at closely.
9. A maintainer and at least one other member will review it. They may ask for changes. This is normal and kind, not a criticism.

## Rules that keep the collection trustworthy

Write what the source says, not what you think it should have said. If you correct something, say so in the pull request. Always fill in the `source` block honestly, so another person can find the original. Choose the `rights` value that matches what you truly know, and use `unclear_needs_review` when you are not sure. That is a fine answer, and it is better than guessing.

Keep text in its original language. Do not translate an examination question from French to English and file it as the original. If you translate, use a parallel text record.

Use UTF-8 so that accents and special letters in our languages are preserved exactly.

## Material we need to handle with care

Read `docs/RIGHTS_AND_PRIVACY.md` before contributing exam papers, books, newspaper articles, recordings of people, or anything about living individuals.

## Proposing a new folder

Open an issue using the new category template and explain what is missing and who it would serve. If members agree, add it to `tools/build_structure.py` and run the script, which creates the folder and its guide.

## Be kind

All members follow the `CODE_OF_CONDUCT.md`. We are building something for our whole country, and we will not always agree about everything. We expect disagreement to be respectful.
