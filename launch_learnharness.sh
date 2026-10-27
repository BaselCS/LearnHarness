#!/usr/bin/env bash
set -e

# Kill any stale server on port 12321
fuser -k 12321/tcp 2>/dev/null || true

cd /home/basel/Work/LearnHarness/desktop
exec npm run desktop:dev
