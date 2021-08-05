Releasing
=========

1. From `master`, bump the package version, using `make bump! minor` (you can bump `patch`, `minor` or `major`).
2. Push the new branch to `origin`.
3. After merging the bumped version to `master`, make a Pull Request from `master` to `stable`. Make sure to include every change, using the template located at `.github/PULL_REQUEST_TEMPLATE/release.md`.
4. Merge the Pull Request.
