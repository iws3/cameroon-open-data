# Adding a whole paper from your own computer

This is the route for a volunteer who has the text of a full paper and wants to add every question at once, then open a pull request with the GitHub CLI. Most contributors should use the web forms instead. Use this one only for material you have the right to share.

## Before you start

Check the rights first. Past papers belong to the examination body, and a website that has typed them or added corrections may hold rights over its own work too. Only import text that you wrote, that you have written permission to use, or whose rights you have cleared. If the rights are unclear, keep the files on your own computer, or in a private repository, and do not push them to the public project. Never copy a website's corrections or explanations without permission.

## Steps

1. Put the text of one paper in a plain text file, for example `paper.txt`. Questions must start a line with their number, as in `1. ...`, and be numbered in order. Lines like `Section II` are noticed and recorded.
2. Preview what will be created:
   ```bash
   python tools/paper_to_jsonl.py paper.txt --exam "GCE Ordinary Level" --subject Physics \
     --year 2019 --paper "Paper 2" --contributor YourName \
     --source-note "Typed from my own copy of the paper" --dry-run
   ```
   Use `--drop "regular expression"` to ignore adverts, phone numbers or watermarks. It can be repeated.
3. Remove `--dry-run` to write the files. Each question becomes its own small file in the right subject and year folder. Questions already in the collection are skipped.
4. Run `python tools/validate.py`.
5. Log in once with `gh auth login`, then open the pull request:
   ```bash
   bash tools/submit_pr.sh add-physics-2019-paper-2 "Add Physics 2019 Paper 2 questions"
   ```
   The script validates, creates a branch from the latest default branch, commits only the `data` folder, pushes, and opens the pull request.

## Things to check by hand

The tool splits questions by their numbers and adds up any marks written as `(2 marks)`. It cannot describe diagrams, so add a `figure_description` to each question that depends on a figure, either by editing the file or by resubmitting through the web form. Read each file against the original before you open the pull request.
