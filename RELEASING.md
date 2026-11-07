# Releasing

Automático al mergear a `master`. Toma ~2–3 min.

## Cómo

1. Agrega al PR un label `release:patch`, `release:minor` o `release:major`.
2. Escribe en la sección `## Release notes` de la descripción del PR lo que verán los usuarios del SDK, en inglés. Si queda vacía, se usan las notas autogeneradas de GitHub.
3. Mergea. Los PRs sin label `release:*` no publican; un PR con más de uno hace fallar el workflow.

El release parte de `master` actualizado (incluye el commit de versión de un release anterior en cola). Si después del PR se mergeó algo más que un commit `release: ...` de `fin-releases[bot]`, aborta antes de publicar para no sacar esos cambios con el bump y las notas de este PR. El siguiente release los incluye; usa el manual si hace falta un bump mayor.

### Manual

https://github.com/fintoc-com/fintoc-python/actions → **release** → **Run workflow**, con `bump` (`patch` / `minor` / `major`) y `release-notes` opcionales. Solo corre desde `master`.

## Qué hace

`make get-poetry` + `poetry install` →
[`release/prepare`](https://github.com/fintoc-com/release-action/tree/main/prepare) bumpea y pushea commit + tag a `master` de forma atómica →
`poetry build` →
`pypa/gh-action-pypi-publish` (con `PYPI_API_TOKEN`) →
[`release/finalize`](https://github.com/fintoc-com/release-action/tree/main/finalize) crea GitHub Release.

El push va antes de publicar: si `master` se movió durante el release, el push se rechaza y no se publica nada.

Todo autoreado por `fin-releases[bot]`.

## Si falla

| Falla en | Estado | Recovery |
|---|---|---|
| `master` tiene commits posteriores al PR | Nada publicado | Esperar el siguiente release, o correr el manual |
| Antes del push (install, bump, token de la App) | Nada en el remote | Re-run |
| Push en `release/prepare` (`master` se movió) | Nada publicado: sin commit ni tag | Esperar el siguiente release, o correr el manual |
| Después del push, antes o durante `pypi-publish` | Commit y tag en `master`, versión no está en PyPI | Publicar desde el tag con un token de PyPI del proyecto (`git checkout vX.Y.Z && poetry build && poetry publish -u __token__ -p <token>`) + `gh release create vX.Y.Z`. O saltarse la versión: el siguiente release bumpea desde ella |
| `release/finalize` (post-publish) | Paquete en PyPI, commit y tag, sin GitHub Release | `gh release create vX.Y.Z --notes '...'` |

Re-correr el job después de que el push entró publica la versión siguiente, no la que falló.
