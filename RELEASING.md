# Releasing

Manual desde Actions. Toma ~2–3 min.

## Cómo

1. https://github.com/fintoc-com/fintoc-python/actions → **release** → **Run workflow**.
2. `bump`: `patch` / `minor` / `major`. `release-notes`: markdown opcional.
3. **Run workflow**. Solo corre desde `master`.

## Qué hace

`make get-poetry` + `poetry install` →
[`release/prepare`](https://github.com/fintoc-com/release-action/tree/main/prepare) bumpea local →
`poetry build` →
`pypa/gh-action-pypi-publish` (con `PYPI_API_TOKEN`) →
[`release/finalize`](https://github.com/fintoc-com/release-action/tree/main/finalize) pushea commit + tag, crea GitHub Release.

Todo autoreado por `fin-releases[bot]`.

## Si falla

| Falla en | Estado | Recovery |
|---|---|---|
| Antes o durante `pypi-publish` | Nada en el remote | Re-run |
| `release/finalize` (post-publish) | Paquete en PyPI, sin tag/release | PR con el commit del bump + `gh release create vX.Y.Z` |
