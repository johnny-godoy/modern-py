#!/usr/bin/env bash
# Render one answer file of tests/answers/ into a directory, then run the checks of the rendered project.
# Usage: scripts/render.sh <answer name> <directory> [--no-checks]
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
name=$1
dest=$2
checks=${3:-}

rm -rf "$dest"
# --vcs-ref HEAD renders the working tree, with uncommitted changes, so a change is tested before its commit.
uvx --from 'copier>=9.4' copier copy --trust --defaults --vcs-ref HEAD \
  --data-file "$root/tests/answers/$name.yml" "$root" "$dest"

if [ "$checks" != "--no-checks" ]; then
  cd "$dest"
  just check
  just test
  just docs
fi
