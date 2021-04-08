Releasing
=========

1. Update the new version in  `pyproject.toml` and `fintoc/__init__.py`.
2. Update the `CHANGELOG.md` for the impending release.
3. `git commit -am "Release X.Y.Z."` (where X.Y.Z is the new version)
4. `git tag -a X.Y.Z -m "Version X.Y.Z"` (where X.Y.Z is the new version).
5. `git push origin X.Y.Z`
