# fintoc-python

The official Python SDK for the Fintoc API.

## Skills

Edit skills in `.agents/skills/`; `.claude/skills` links there.
Use `add-api-resource` when adding or updating API resources, actions, or fields.

## Releases

Merging a PR to `master` with a `release:patch`, `release:minor` or `release:major` label
publishes a release, with notes from the PR's `## Release notes` section (see `RELEASING.md`).
Do not bump the version in feature PRs.

Pick one label by what SDK users get:

- `release:minor`: new resources, methods, parameters or fields.
- `release:patch`: fixes to existing behavior, with no new public surface.
- `release:major`: removes or renames something public, or changes it incompatibly.
- No label: changes SDK users don't get, such as tests, CI, docs or agent files.

Write `## Release notes` in English for SDK users: one bullet per change, naming what changed
(resource, method, field or error), without internal details.
