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

# A rendered project names no part of EBaMl, because the template serves every domain.
if grep -rniIF -f "$root/tests/forbidden-names.txt" --exclude-dir=.venv --exclude-dir=.git --exclude=uv.lock "$dest"; then
  echo "The rendered project contains a forbidden name (tests/forbidden-names.txt)." >&2
  exit 1
fi

if [ "$checks" != "--no-checks" ]; then
  cd "$dest"
  just check
  just test
  just docs
fi
