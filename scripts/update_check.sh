#!/usr/bin/env bash
# Render a project from an earlier template version, then run `copier update` to the current commit, and fail on a
# conflict. An untouched project must take each template change with no conflict, or `copier update` is no use.
# Usage: scripts/update_check.sh <directory> [base ref] [answer name]
# The base ref defaults to the newest tag before HEAD. With no such tag, the check has nothing to compare and passes.
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
dest=$1
base=${2:-$(git -C "$root" describe --tags --abbrev=0 HEAD^ 2>/dev/null || true)}
name=${3:-everything}
copier=(uvx --from 'copier>=9.4' copier)

if [ -z "$base" ]; then
  echo "No tag before HEAD: there is no earlier template version to update from."
  exit 0
fi

rm -rf "$dest"
"${copier[@]}" copy --trust --defaults --vcs-ref "$base" --data-file "$root/tests/answers/$name.yml" "$root" "$dest"
cd "$dest"
git commit --quiet --no-verify -m "build: start the project from the template"
# --defaults keeps the stored answers and takes the default of each new question.
"${copier[@]}" update --trust --defaults --vcs-ref HEAD --conflict inline

conflicts=$(git diff --name-only --diff-filter=U; grep -rlE '^(<<<<<<<|>>>>>>>) ' --exclude-dir=.venv --exclude-dir=.git . || true)
if [ -n "$conflicts" ]; then
  echo "copier update from $base left conflicts in:" >&2
  printf '%s\n' "$conflicts" | sort -u >&2
  exit 1
fi
echo "copier update from $base to HEAD applied with no conflict."
