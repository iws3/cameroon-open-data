#!/usr/bin/env bash
# Validate, branch, commit, push and open a pull request with the GitHub CLI.
# Usage: bash tools/submit_pr.sh <branch-name> "<pull request title>"
set -euo pipefail

branch="${1:?Usage: bash tools/submit_pr.sh <branch-name> \"<pull request title>\"}"
title="${2:?Usage: bash tools/submit_pr.sh <branch-name> \"<pull request title>\"}"

gh auth status >/dev/null 2>&1 || { echo "Run 'gh auth login' first."; exit 1; }
python3 tools/validate.py

base="$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)"
git fetch origin "$base"
git switch -c "$branch" "origin/$base"      # your new, untracked files come along
git add data
git commit -m "$title"
git push -u origin "$branch"
gh pr create --base "$base" --title "$title" \
  --body "Added with tools/paper_to_jsonl.py. Each question is its own file, so this cannot conflict with other pull requests. A reviewer should check the typing against the original."
