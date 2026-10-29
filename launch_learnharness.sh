#!/usr/bin/env bash
set -e

# Export standard user PATH with mise so desktop environments (rofi/omarchy) find node/npm
export PATH="$HOME/.local/share/mise/shims:$HOME/.local/share/mise/installs/node/latest/bin:$HOME/.local/bin:$PATH"
if command -v mise >/dev/null 2>&1; then
    eval "$(mise activate bash 2>/dev/null)" || true
fi

# Kill any stale server on port 2949
fuser -k 2949/tcp 2>/dev/null || true

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

exec npm run desktop:dev
