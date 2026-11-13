# Rumla Stable upstream mirror

Upstream: https://github.com/rumla3434/Atmosphere-Stable/releases

This branch tracks the author's manually assembled 7z SD-card bundle, independently
from the four automated builders in this repository.

- The upstream repository's `Makefile` builds Atmosphère firmware, **not** the
  author's complete stable SD-card configuration.
- The primary workflow lives on `main`: [rumla-stable.yml](../../blob/main/.github/workflows/rumla-stable.yml).
- It checks the *release asset SHA256* four times a day. The author may replace a
  file without changing its release tag.
- On a change it downloads the original .7z, verifies asset size, SHA256 and 7z
  integrity, lists its file paths, and publishes the original **unchanged** .7z
  together with a machine-generated layout audit.
- The successful release updates this branch with `upstream-release.json`,
  `upstream-asset-sha256.txt`, `upstream-release.txt`, and `ARCHIVE_LAYOUT.md`.
- Mirror releases are named `rumla-stable-<upstream-tag>-<digest-prefix>`, so a
  replaced file in the same upstream tag receives its own historical version.

**Important:** This process mirrors the author's assembled package; it is not
a claim of reproducible component-by-component building or Switch hardware testing.
The author has not supplied a public bundle assembly recipe.

Source assets remain attributed to their author and third-party component creators.
Verify compatibility and preserve console backups before use.
