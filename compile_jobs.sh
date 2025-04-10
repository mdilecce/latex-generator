#!/bin/bash

echo "==================="

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${INPUT_EMAIL}"
git config --global --add safe.directory /github/workspace

python3 /usr/bin/compile_jobs.py

# Commit and push changes to the branch that triggered the action
find . -type f \( -name "*.log" -o -name "*.pdf" \) -exec git add {} +
git commit -m "Updated Compiled Files" || echo "No changes to commit"
git push origin "${GITHUB_REF#refs/heads/}"

echo "==================="
