# Atmosphere AIO — upstream-tracked builds

This repository tracks four independent Nintendo Switch CFW bundle builders in separate branches:

| Branch | Upstream | Build |
| --- | --- | --- |
| [`upstream/switchscript`](../../tree/upstream/switchscript) | [huangqian8/SwitchScript](https://github.com/huangqian8/SwitchScript) | SwitchSD.zip |
| [`upstream/atmosphere-for-switch`](../../tree/upstream/atmosphere-for-switch) | [gzk47/Atmosphere-for-Switch](https://github.com/gzk47/Atmosphere-for-Switch) | SwitchSD, Pure, Tesla, Horizon-OC |
| [`upstream/ascent`](../../tree/upstream/ascent) | [exploitz86/Ascent](https://github.com/exploitz86/Ascent) | Ascent variants |
| [`upstream/vanillatmosphere`](../../tree/upstream/vanillatmosphere) | [mlemiam/Vanillatmosphere](https://github.com/mlemiam/Vanillatmosphere) | artifact-syspatches |

## How it works

- The **default `main` branch** owns the scheduled workflow (GitHub schedules do not execute from non-default branches).
- The workflow mirrors each upstream's `.github/workflows/` directory **as data** into its branch's `upstream-workflows/`, and records the exact upstream revision in `upstream-revision.txt`.
- A separate read-only CI job checks out that pinned upstream revision, runs the equivalent upstream build script, and uploads ZIP artifacts.
- A separate publish job may attach build outputs to namespaced GitHub Releases; it does not execute upstream code.
- Scheduled builds check upstream versions again, even when the upstream workflow YAML has not changed.

**Security:** Upstream workflow YAML is not executed as a GitHub workflow in this repository. It is mirrored for inspection. Upstream build scripts run with read-only `GITHUB_TOKEN`; inspect third-party code and resulting packages before installing. The branches are independent and are not automatically merged into `main`.

Use [Actions](../../actions/workflows/sync-build.yml) to run the schedule manually (`target=all` or one target). GitHub may delay scheduled events, or pause them on inactive repositories.

This is an independent automation mirror, not an official release of any upstream project. Review upstream license and component redistribution requirements before redistributing output.
