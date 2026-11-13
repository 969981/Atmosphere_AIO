# Atmosphere AIO — upstream-tracked builds

This repository tracks four automated Nintendo Switch CFW bundle builders plus one verified mirror of a manually assembled stable bundle, in separate branches:

| Branch | Upstream | Build |
| --- | --- | --- |
| [`upstream/switchscript`](../../tree/upstream/switchscript) | [huangqian8/SwitchScript](https://github.com/huangqian8/SwitchScript) | SwitchSD.zip |
| [`upstream/atmosphere-for-switch`](../../tree/upstream/atmosphere-for-switch) | [gzk47/Atmosphere-for-Switch](https://github.com/gzk47/Atmosphere-for-Switch) | SwitchSD, Pure, Tesla, Horizon-OC |
| [`upstream/ascent`](../../tree/upstream/ascent) | [exploitz86/Ascent](https://github.com/exploitz86/Ascent) | Ascent variants |
| [`upstream/vanillatmosphere`](../../tree/upstream/vanillatmosphere) | [mlemiam/Vanillatmosphere](https://github.com/mlemiam/Vanillatmosphere) | artifact-syspatches |
| [`upstream/rumla-stable`](../../tree/upstream/rumla-stable) | [rumla3434/Atmosphere-Stable](https://github.com/rumla3434/Atmosphere-Stable) | **Original manually packaged .7z mirror** |

## How it works

- The **default `main` branch** owns the scheduled workflow (GitHub schedules do not execute from non-default branches).
- The workflow mirrors each upstream's `.github/workflows/` directory **as data** into its branch's `upstream-workflows/`, and records the exact upstream revision in `upstream-revision.txt`.
- A separate read-only CI job checks out that pinned upstream revision, runs the equivalent upstream build script, and uploads ZIP artifacts.
- A separate publish job may attach build outputs to namespaced GitHub Releases; it does not execute upstream code.
- Scheduled builds check upstream versions again, even when the upstream workflow YAML has not changed.

**Security:** Upstream workflow YAML is not executed as a GitHub workflow in this repository. It is mirrored for inspection. Upstream build scripts run with read-only `GITHUB_TOKEN`; inspect third-party code and resulting packages before installing. The branches are independent and are not automatically merged into `main`.

Use [Actions](../../actions/workflows/sync-build.yml) to run the schedule manually (`target=all` or one target). GitHub may delay scheduled events, or pause them on inactive repositories.

This is an independent automation mirror, not an official release of any upstream project. Review upstream license and component redistribution requirements before redistributing output.

## Rumla Stable manual package tracking

[Dedicated GitHub Actions workflow](../../actions/workflows/rumla-stable.yml) checks the upstream release archive SHA256 every six hours (at :29 UTC), not just its release tag. If the author replaces an archive under an unchanged tag, it creates a **new digest-scoped mirror Release** with the original unchanged .7z, SHA256SUMS, source provenance and a 7z file-layout audit. This does not claim to reproduce the author's unpublished SD-card assembly recipe. The primary four-builder workflow remains unchanged.

## Independent rumla-style source rebuild (experimental)

Unlike the byte-exact [original rumla mirror](../../tree/upstream/rumla-stable), the [`upstream/rumla-rebuild` branch](../../tree/upstream/rumla-rebuild) builds a **new package from individual original-component Releases** without downloading the author's original 7z. Its [workflow](../../actions/workflows/rumla-rebuild.yml) retrieves a locked list of upstream component assets, integrates them into an SD directory, and compares every resulting file with a previously audited reference SHA256 manifest. Results are intentionally labeled **experimental** and published as GitHub Pre-releases because signature patches, Mariko warmboot data and some author artwork/forwarders have not been reproduced or hardware tested. The separate [reference forensic audit](../../actions/workflows/rumla-rebuild-audit.yml) collected the reference file tree, not a binary build input. Do not confuse a source assembly build with the separately verified byte-identical original mirror.
