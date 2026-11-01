# Maintainer guide: keeping contributions flowing without conflicts

## Why conflicts do not happen

Every contribution is a brand new file with its own name. The name contains the subject, the paper, the question number and a short fingerprint of the question text, for example `physics-paper-2-q1-521fe9.jsonl`. Because two contributors never edit the same file, their pull requests never collide, however many are open at once. Nobody edits a shared index or a shared list. Anything that combines many files, such as a full dataset download, is built from the folders afterwards and is never committed by hand.

## Why duplicates are caught

Each question gets a fingerprint made from its subject and its text, ignoring capitals, accents, spaces and punctuation. Three checks use it. The form refuses a question that is already in the collection. It also refuses one that is waiting in another open pull request. And `python tools/validate.py` fails the pull request if the same question appears twice. Two different versions of the same numbered question (same exam, subject, year, paper and number but different text) produce a warning, so a reviewer can decide which typing is correct.

To stop people from typing the same paper at the same time, ask them to use the "Claim a paper to transcribe" form first.

## Settings to switch on once, in the repository settings

1. **Branches, then add a rule for main.** Require a pull request before merging, require 1 approval, and require the status check named `validate` to pass.
2. **General, Pull Requests.** Allow squash merging only, allow auto-merge, and automatically delete head branches after merge.
3. **Actions, General.** Allow GitHub Actions to create and approve pull requests.
4. **Labels.** Create these labels: `submit-question`, `needs-transcription`, `needs-conversion`, `claimed`, `data-quality`, `structure`, `wanted`.

With these in place, a form submission becomes a pull request that merges itself the moment one reviewer approves it and the check is green. Reviewers only look and click Approve.

## Reviewing quickly

For each pull request, open "Files changed" and check four things: the question matches the original, the marks add up, the diagram description makes sense, and the answer, if given, is correct. Approve, or comment with what to fix. When the reviewer knows the subject, add their GitHub username to `verified_by` before approving.

## Sending subjects to the right reviewers

Create a team for each subject area, for example physics teachers, and list them in a `.github/CODEOWNERS` file such as `/data/education/gce/ordinary-level/physics/ @your-organization/physics-reviewers`. GitHub then asks the right people to review automatically.

## Spreadsheets and photos

For a spreadsheet, run `python tools/csv_to_jsonl.py file.csv`, then `python tools/validate.py`, create a branch, commit and open one pull request. Duplicates are skipped automatically. For photos, label the issue `claimed`, transcribe the paper, or ask a volunteer to, and submit the questions through the form.
