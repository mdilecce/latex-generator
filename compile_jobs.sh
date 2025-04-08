#!/bin/bash

echo "==================="

# git config --global user.name "${GITHUB_ACTOR}"
# git config --global user.email "${INPUT_EMAIL}"
# git config --global --add safe.directory /github/workspace

python3 /usr/bin/compile_jobs.py

# git add -A && git commit -m "Update Feed"
# git push --set-upstream origin main

echo "==================="