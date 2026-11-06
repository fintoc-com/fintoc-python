#!/usr/bin/env bash
set -uo pipefail

SCRIPT="$(dirname "$0")/resolve-release.sh"
SHA=abc123
failures=0

pulls_json() {
  local labels=$1 body=$2
  jq -nc --arg sha "$SHA" --arg body "$body" --argjson labels "$labels" \
    '[{number: 7, merged_at: "2026-01-01T00:00:00Z", merge_commit_sha: $sha,
       body: $body, labels: ($labels | map({name: .}))}]'
}

read_output() {
  local file=$1 name=$2
  awk -v name="$name" '
    index($0, name "=") == 1 { print substr($0, length(name) + 2); exit }
    index($0, name "<<") == 1 { delimiter = substr($0, length(name) + 3); reading = 1; next }
    reading && $0 == delimiter { exit }
    reading { print }
  ' "$file"
}

assert_release() {
  local description=$1 expected_status=$2 expected_bump=$3 expected_notes=$4
  shift 4
  local output status
  output=$(mktemp)
  env GITHUB_OUTPUT="$output" "$@" bash "$SCRIPT" > /dev/null
  status=$?

  if [ "$status" -ne "$expected_status" ]; then
    echo "FAIL: $description (exit $status, expected $expected_status)"
    failures=$((failures + 1))
  elif [ "$expected_status" -eq 0 ] &&
    { [ "$(read_output "$output" bump)" != "$expected_bump" ] ||
      [ "$(read_output "$output" notes)" != "$expected_notes" ]; }; then
    echo "FAIL: $description"
    echo "  bump:  '$(read_output "$output" bump)' expected '$expected_bump'"
    echo "  notes: '$(read_output "$output" notes)' expected '$expected_notes'"
    failures=$((failures + 1))
  else
    echo "ok: $description"
  fi
  rm -f "$output"
}

assert_push() {
  local description=$1 expected_status=$2 expected_bump=$3 expected_notes=$4 labels=$5 body=$6
  assert_release "$description" "$expected_status" "$expected_bump" "$expected_notes" \
    EVENT_NAME=push SHA="$SHA" PULLS_JSON="$(pulls_json "$labels" "$body")"
}

assert_push "notes section at the end, comments stripped" 0 minor $'- Added X.\n- Removed Y.' \
  '["bug", "release:minor"]' \
  $'## Contexto\nctx\n\n## Release notes\n\n<!-- instructions\nspanning lines -->\n\n- Added X.\n- Removed Y.\n'

assert_push "notes section followed by another section" 0 patch $'Fixed X.\n### Details\nmore' \
  '["release:patch"]' \
  $'## Release notes\r\n\r\nFixed X.\r\n### Details\r\nmore\r\n\r\n## Rollback\r\nsafe\r\n'

assert_push "notes section with only a comment" 0 major "" \
  '["release:major"]' $'## Release notes\n<!-- empty -->\n## Rollback\nx'

assert_push "no notes section" 0 patch "" '["release:patch"]' $'## Contexto\nctx'

assert_push "PR without release label is skipped" 0 "" "" '["bug"]' $'## Release notes\nx'

assert_push "more than one release label fails" 1 "" "" '["release:patch", "release:minor"]' "x"

assert_push "unknown release label fails" 1 "" "" '["release:hotfix"]' "x"

assert_release "push without merged PR is skipped" 0 "" "" \
  EVENT_NAME=push SHA="$SHA" PULLS_JSON='[{"number": 8, "merged_at": null, "merge_commit_sha": "abc123", "labels": [{"name": "release:patch"}], "body": ""}]'

assert_release "workflow_dispatch uses the inputs" 0 minor "notes here" \
  EVENT_NAME=workflow_dispatch INPUT_BUMP=minor INPUT_NOTES=$'  \n notes here\n'

assert_release "workflow_dispatch with empty notes" 0 patch "" \
  EVENT_NAME=workflow_dispatch INPUT_BUMP=patch INPUT_NOTES=""

[ "$failures" -eq 0 ] || { echo "$failures failing case(s)"; exit 1; }
