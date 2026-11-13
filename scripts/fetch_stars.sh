#!/usr/bin/env bash
# Regenerate raw starred-repo data for the authenticated user (needs gh auth / GITHUB_TOKEN).
set -euo pipefail
OUT="${1:-$(dirname "$0")/../raw/starred_raw.json}"
mkdir -p "$(dirname "$OUT")"
for i in 1 2 3 4 5; do
  if gh api --paginate -H 'Accept: application/vnd.github.star+json' '/user/starred?per_page=100' \
     | jq -s 'add' > "$OUT.tmp"; then mv "$OUT.tmp" "$OUT"; echo "fetched $(jq length "$OUT") repos -> $OUT"; exit 0; fi
  echo "retry $i..." >&2; sleep $((i*5))
done
exit 1
