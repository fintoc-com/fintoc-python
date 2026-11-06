#!/usr/bin/env bash
# Decide the bump and release notes for the release workflow.
# Writes `bump` (empty means skip the release) and `notes` to $GITHUB_OUTPUT.
#
# Required env: EVENT_NAME, GITHUB_OUTPUT
# workflow_dispatch: INPUT_BUMP, INPUT_NOTES
# push: SHA, PULLS_JSON (response of GET repos/{repo}/commits/{sha}/pulls)
set -euo pipefail

extract_release_notes() {
  perl -0777 -ne '
    s/\r//g;
    s/<!--.*?-->//gs;
    if (/^##[ \t]+Release notes[ \t]*$(.*?)(?=^##[ \t]|\z)/msi) {
      my $notes = $1;
      $notes =~ s/^\s+|\s+$//g;
      print $notes;
    }
  '
}

trim() {
  perl -0777 -pe 's/^\s+|\s+$//g'
}

write_output() {
  local bump=$1 notes=$2 delimiter
  delimiter="RELEASE_NOTES_$(openssl rand -hex 16)"
  {
    echo "bump=$bump"
    echo "notes<<$delimiter"
    printf '%s\n' "$notes"
    echo "$delimiter"
  } >> "$GITHUB_OUTPUT"
}

skip_release() {
  echo "::notice::$1 Skipping release."
  write_output "" ""
}

resolve_from_dispatch() {
  write_output "$INPUT_BUMP" "$(printf '%s' "${INPUT_NOTES:-}" | trim)"
}

resolve_from_push() {
  local pr number labels label_count bump
  pr=$(jq -c --arg sha "$SHA" \
    'map(select(.merged_at != null and .merge_commit_sha == $sha)) | first // empty' \
    <<< "$PULLS_JSON")
  if [ -z "$pr" ]; then
    skip_release "No merged PR found for $SHA."
    return
  fi

  number=$(jq -r '.number' <<< "$pr")
  labels=$(jq -r '[.labels[].name | select(startswith("release:"))] | join(" ")' <<< "$pr")
  label_count=$(jq '[.labels[].name | select(startswith("release:"))] | length' <<< "$pr")

  if [ "$label_count" -eq 0 ]; then
    skip_release "PR #$number has no release:* label."
    return
  fi
  if [ "$label_count" -gt 1 ]; then
    echo "::error::PR #$number has more than one release:* label ($labels). Keep only one."
    exit 1
  fi

  bump=${labels#release:}
  case "$bump" in
    patch|minor|major) ;;
    *)
      echo "::error::PR #$number has an unknown label $labels. Use release:patch, release:minor or release:major."
      exit 1
      ;;
  esac

  echo "Releasing PR #$number with bump $bump."
  write_output "$bump" "$(jq -r '.body // ""' <<< "$pr" | extract_release_notes)"
}

case "$EVENT_NAME" in
  workflow_dispatch) resolve_from_dispatch ;;
  push) resolve_from_push ;;
  *)
    echo "::error::Unsupported event $EVENT_NAME."
    exit 1
    ;;
esac
