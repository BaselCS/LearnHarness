#!/usr/bin/env bash
set -e

# ==============================================================================
# LearnHarness Upstream Sync Script
# Updates desktop/ from upstream (https://github.com/amosblomqvist/learnharness)
# while preserving all local customizations (Arabic localization, Anki bridge, etc.)
# ==============================================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "==> 1. Fetching latest changes from upstream..."
git fetch upstream main

echo "==> 2. Checking working directory state..."
if ! git diff-index --quiet HEAD --; then
    echo "WARNING: You have uncommitted changes. Please commit or stash them before syncing."
    exit 1
fi

echo "==> 3. Merging upstream updates into desktop/ subtree..."
git subtree pull --prefix=desktop upstream main --squash -m "chore: sync updates from upstream main"

echo "==> 4. Sync complete! Pushing updated main to your GitHub..."
git push origin main

echo "==> All done successfully!"
