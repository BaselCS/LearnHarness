#!/usr/bin/env bash
set -e

# Export standard user PATH with mise so desktop environments (rofi/omarchy) find node/npm
export PATH="$HOME/.local/share/mise/shims:$HOME/.local/share/mise/installs/node/latest/bin:$HOME/.local/bin:$PATH"
if command -v mise >/dev/null 2>&1; then
    eval "$(mise activate bash 2>/dev/null)" || true
fi

# Kill any stale servers on ports 12321, 3000, or 2949
fuser -k 12321/tcp 2>/dev/null || true
fuser -k 3000/tcp 2>/dev/null || true
fuser -k 2949/tcp 2>/dev/null || true

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$PROJECT_DIR/desktop/package.json" ]; then
    cd "$PROJECT_DIR/desktop"
else
    cd "$PROJECT_DIR"
fi

# Start Next.js in the background on port 2949
npx next dev -p 2949 &
NEXT_PID=$!

# Ensure Next.js and open ports are cleanly terminated when Electron exits
cleanup() {
    kill $NEXT_PID 2>/dev/null || true
    fuser -k 12321/tcp 2>/dev/null || true
    fuser -k 3000/tcp 2>/dev/null || true
    fuser -k 2949/tcp 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Wait until Next.js and its API endpoints are compiled and actively responding
for i in {1..60}; do
    if curl -s -m 2 http://localhost:2949/api/settings >/dev/null 2>&1; then
        break
    fi
    sleep 0.25
done

# Launch Electron with dev URL
export LH_DEV_URL="http://localhost:2949"
npx electron .
