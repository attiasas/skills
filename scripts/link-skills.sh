#!/usr/bin/env bash
set -euo pipefail

# Symlink every skill in this repo into the local harness skill directories.
# A git pull then updates installed skills. Re-run after adding, renaming,
# or removing a skill directory.
#
# Destinations:
#   ~/.cursor/skills   Cursor
#   ~/.agents/skills   other Agent Skills harnesses
#
# Refuses to replace a real directory. Remove or move that directory yourself
# if you want the symlink.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.cursor/skills" "$HOME/.agents/skills")

names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/node_modules/*' -print0)

if [ ${#names[@]} -eq 0 ]; then
  echo "No SKILL.md files under $REPO/skills"
  exit 0
fi

seen=""
dup=0
for name in "${names[@]}"; do
  case " $seen " in
    *" $name "*)
      echo "error: more than one skill is named '$name'. Directory names must be unique across buckets." >&2
      dup=1
      ;;
  esac
  seen="$seen $name"
done
if [ "$dup" -ne 0 ]; then
  exit 1
fi

for DEST in "${DESTS[@]}"; do
  if [ -L "$DEST" ]; then
    resolved="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$DEST")"
    case "$resolved" in
      "$REPO"|"$REPO"/*)
        echo "error: $DEST is a symlink into this repo ($resolved)." >&2
        echo "Remove it and re-run so this script can create a real directory." >&2
        exit 1
        ;;
    esac
  fi

  mkdir -p "$DEST"

  for i in "${!names[@]}"; do
    name="${names[$i]}"
    src="${srcs[$i]}"
    target="$DEST/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skip $name: $target exists and is not a symlink" >&2
      continue
    fi

    ln -sfn "$src" "$target"
    echo "linked $name -> $src ($DEST)"
  done
done
