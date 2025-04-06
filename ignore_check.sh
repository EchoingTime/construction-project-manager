#!/bin/bash

# ---------------------------------------------
# Provided by ChatGPT for easy git ignoring
# Script to make files/folders ignored by Git (run in bash)
# Usage: ./ignore_check.sh <target>
# Example: ./ignore_check.sh __pycache__/
# Check it: git check-ignore -v __pycache__/
# ---------------------------------------------

# Check if user gave an argument
if [ -z "$1" ]; then
  echo "❌ No target provided. Usage: ./ignore_check.sh <file_or_folder>"
  exit 1
fi

TARGET="$1"

# Check if the target is ignored
if git check-ignore -q "$TARGET"; then
  echo "✅ '$TARGET' is already ignored by Git."
else
  echo "⚠️ '$TARGET' is NOT ignored. Fixing now..."

  # Add it to .gitignore if it's not already listed
  if ! grep -qxF "$TARGET" .gitignore; then
    echo "$TARGET" >> .gitignore
    echo "➕ Added '$TARGET' to .gitignore"
  else
    echo "ℹ️ '$TARGET' already in .gitignore but not yet effective (might be tracked)."
  fi

  # Untrack it from Git if it's being tracked
  if git ls-files --error-unmatch "$TARGET" >/dev/null 2>&1 || [ -d "$TARGET" ]; then
    git rm -r --cached "$TARGET"
    echo "🧹 Removed '$TARGET' from Git tracking"
  fi

  # Stage the .gitignore
  git add .gitignore

  # Commit only if there are staged changes
  if ! git diff --cached --quiet; then
    git commit -m "Ignore $TARGET and remove from tracking"
    echo "✅ '$TARGET' is now ignored and untracked."
  else
    echo "ℹ️ No changes to commit."
  fi
fi
