# Rumla-style independent rebuild (experimental)

**Branch:** `upstream/rumla-rebuild` · **CI:** [Rumla Rebuild](../../actions/workflows/rumla-rebuild.yml)

## What is and is NOT built here

The build retrieves **33 pinned assets directly from the corresponding component authors' GitHub Releases**, layers their SD distributions, applies a small number of version-reviewed text config templates, and builds a fresh .7z.

**It never downloads, extracts or copies the author's rumla Stable .7z as part of the rebuild.**

The original release was inspected once by [the forensic audit workflow](../../actions/workflows/rumla-rebuild-audit.yml) to capture `reference/manifest.json` (277 SD files and SHA256 hashes), `reference/inventory.md`, and 47 readable configuration snapshots. These are the parity baseline, **not a binary input**. Text config snapshots are deliberately version-scoped.

## Architecture

```text
GitHub Releases of 33 independent component assets
     |
     +--> profiles/rumla-1.12.2.json (pinned URL identity and placement)
     +--> scripts/build_rebuild.py (download, validate ZIP, assemble SD tree)
     +--> reference/config-reference/ (audited text settings)
     |
     +--> work/sd/Rumla-Rebuild-SD/
              |
              +--> independent experimental .7z
              +--> BUILD_REPORT.json / SOURCE_LOCK.json
              +--> PARITY.md: per-file compare with original manifest
```

The independent build workflow on `main` checks upstream versions daily, rebuilds the pinned profile and publishes **clearly labeled experimental pre-releases** only if core files, 7z integrity and SHA256 checks succeed. A new upstream version is reported rather than silently replacing firmware components without testing.

## Initial upstream components

- Atmosphère 1.12.2 + fusee (official)
- Hekate 6.5.5 + Nyx, easyworld Chinese Nyx
- ZD's ovlloader, Ultrahand, ovl-sysmodules, EdiZon, sys-clk, StatusMonitor
- Awoo, Checkpoint, DBI 921 and translations, Ascent Toolbox, EdiZon-SE, Goldleaf, JKSV, linkalho, NX-Activity-Log, sphaira, switch-time, Tencent switcher, Tinwoo, wiliwili
- Hekate payload tools from their individual authors

## Known gaps before calling this a rumla-equivalent stable bundle

1. **IPS patches (155 in original)**: ES/FS/NIM/NFIM databases, loader patches, Hekate `patches.ini`; find properly source-attributed, version-matched sources or generate them from documented patch databases. Do not use copied IPS from original rumla as a stand-in.
2. **warmboot_mariko (7 files)**: build/validate per target firmware and hardware instead of embedding unknown artifacts.
3. **Non-source assets**: custom bootlogo/icon BMP, SX `boot.dat`, `sdloader.enc`, universal `hbmenu.nsp`, specific picofly toolbox version.
4. **Possible version differences**: fixed source tags can predate or postdate author's manually selected binaries; the SHA comparison, not a matching label, is authoritative.
5. **Hardware regression tests**: independently test Erista/Mariko, sysNAND/emuMMC, boot, sleep/resume, Wi-Fi and system-module interoperability. CI-only checks do not establish device safety.

**Never install an experimental package over the only working SD card.** Back up `emummc`, `Nintendo`, save data and console configuration first.

## Verification

See the action's `PARITY.md` and `BUILD_REPORT.json`: exact bytes, changed hashes, missing and extra files, source revision/digest for each component, and failed downloads. A successful CI run means package integrity only—not 100% original parity or Switch compatibility.
