#!/usr/bin/env python3
"""Track and verify manually assembled rumla3434 releases.

No upstream code is executed. The original 7z archive is mirrored byte-for-byte,
and its file names are inspected (not extracted). The source repository Makefile
builds Atmosphere itself, not the author's full SD-card bundle.
"""
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

UPSTREAM = "rumla3434/Atmosphere-Stable"
TARGET = "969981/Atmosphere_AIO"
UA = "969981-Atmosphere-AIO-rumla-release-checker/1.0"


def api_json(url, not_found_ok=False):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": UA}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=40) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if not_found_ok and e.code == 404:
            return None
        raise


def inspect_release():
    r = api_json(f"https://api.github.com/repos/{UPSTREAM}/releases/latest")
    assets = [a for a in r.get("assets", []) if re.fullmatch(r"[A-Za-z0-9_.+-]+[.]7z", a.get("name", ""))]
    if not assets:
        raise RuntimeError("Latest rumla release does not contain a supported .7z asset")
    # Fails safely rather than mirroring a random asset if the author adds another bundle.
    if len(assets) != 1:
        raise RuntimeError("More than one .7z asset; update the asset selection rules")
    a = assets[0]
    raw_digest = a.get("digest", "")
    if not re.fullmatch("sha256:[0-9a-fA-F]{64}", raw_digest):
        raise RuntimeError("GitHub did not provide a SHA256 digest; refusing unverified mirror")
    digest = raw_digest.split(":", 1)[1].lower()
    tag = str(r["tag_name"])
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,100}", tag):
        raise RuntimeError("Unexpected upstream tag")
    return {
        "source_repository": UPSTREAM,
        "source_release_tag": tag,
        "source_release_name": r.get("name", ""),
        "source_release_url": r["html_url"],
        "source_release_id": r["id"],
        "source_release_updated_at": r["updated_at"],
        "source_asset_id": a["id"],
        "source_asset_name": a["name"],
        "source_asset_url": a["browser_download_url"],
        "source_asset_size": a["size"],
        "source_asset_updated_at": a["updated_at"],
        "source_asset_sha256": digest,
        "mirror_release_tag": f"rumla-stable-{tag}-{digest[:12]}",
    }


def output_kv(items):
    if not os.getenv("GITHUB_OUTPUT"):
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf8") as f:
        for k, v in items.items():
            f.write(f"{k}={str(v).lower() if isinstance(v, bool) else v}\n")


def check():
    r = inspect_release()
    previous = api_json(
        f"https://api.github.com/repos/{TARGET}/releases/tags/{r['mirror_release_tag']}",
        not_found_ok=True,
    )
    published = False
    if previous:
        names = {a["name"] for a in previous.get("assets", [])}
        published = {
            r["source_asset_name"],
            "SHA256SUMS",
            "SOURCE_RELEASE.json",
            "ARCHIVE_LAYOUT.md",
        }.issubset(names) and not previous.get("draft", True)
    force = os.getenv("FORCE_BUILD", "").lower() == "true"
    output_kv({
        "release_tag": r["mirror_release_tag"],
        "asset_name": r["source_asset_name"],
        "sha256": r["source_asset_sha256"],
        "source_tag": r["source_release_tag"],
        "should_build": force or not published,
    })
    print(f"Upstream {r['source_release_tag']} asset SHA256: {r['source_asset_sha256']}")
    print(f"Existing valid mirror: {published}; rebuild needed: {force or not published}")


def download(url, target):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as source, open(target, "wb") as out:
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
            return
        except Exception:
            target.unlink(missing_ok=True)
            if attempt == 2:
                raise
            time.sleep((attempt + 1) * 3)


def sevenzip_entries(archive):
    subprocess.run(["7z", "t", str(archive)], check=True, stdout=subprocess.DEVNULL, timeout=600)
    r = subprocess.run(["7z", "l", "-slt", str(archive)], check=True, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    lines = r.stdout.splitlines()
    seen_files = False
    entries = []
    entry = {}
    for line in lines:
        if line.startswith("----------"):
            seen_files = True
            continue
        if not seen_files:
            continue
        if not line.strip():
            if entry.get("Path"):
                entries.append(entry)
            entry = {}
            continue
        if " = " in line:
            k, v = line.split(" = ", 1)
            if k in ("Path", "Size", "Folder", "Attributes"):
                entry[k] = v
    if entry.get("Path"):
        entries.append(entry)
    if not entries:
        raise RuntimeError("7z validation succeeded but the archive file table is empty")
    for entry in entries:
        path = entry["Path"].replace("\\", "/")
        parts = path.split("/")
        if path.startswith("/") or re.match(r"^[a-zA-Z]:", path) or ".." in parts:
            raise RuntimeError("Unsafe archive path detected: " + repr(path))
    return entries


def build():
    info = inspect_release()
    expected = os.environ.get("EXPECTED_SHA256", "").lower()
    if expected != info["source_asset_sha256"]:
        raise RuntimeError("Upstream asset changed between check and build; retry the workflow")
    dist = Path("dist")
    dist.mkdir(exist_ok=True)
    archive = dist / info["source_asset_name"]
    download(info["source_asset_url"], archive)
    if archive.stat().st_size != info["source_asset_size"]:
        raise RuntimeError("Downloaded asset byte count differs from the GitHub API")
    sha = hashlib.file_digest(open(archive, "rb"), "sha256").hexdigest()
    if sha != expected:
        raise RuntimeError("Downloaded archive SHA256 differs from the GitHub API digest")
    entries = sevenzip_entries(archive)
    paths = [e["Path"].replace("\\", "/") for e in entries]
    files = [e for e in entries if e.get("Folder") != "+"]
    dirs = [e for e in entries if e.get("Folder") == "+"]
    top = collections.Counter(p.split("/", 1)[0] for p in paths)
    suffixes = collections.Counter(Path(e["Path"]).suffix.lower() or "(none)" for e in files)
    report = [
        "# rumla stable: original 7z layout audit",
        "",
        f"- Upstream: {info['source_release_url']}",
        f"- Release tag: `{info['source_release_tag']}`",
        f"- Original asset: `{info['source_asset_name']}`",
        f"- Verified bytes: {info['source_asset_size']:,}",
        f"- Verified SHA256: `{sha}`",
        f"- Archive items: {len(entries):,} (files {len(files):,}; folders {len(dirs):,})",
        "",
        "## Top-level paths (entry count under each prefix)",
        "",
        "| Prefix | Entries |",
        "| --- | ---: |",
    ]
    report += [f"| `{k.replace(chr(96), '')}` | {v:,} |" for k, v in top.most_common()]
    report += [
        "",
        "## Common file extensions",
        "",
        "| Extension | Files |",
        "| --- | ---: |",
    ]
    report += [f"| `{k}` | {v:,} |" for k, v in suffixes.most_common(25)]
    report += [
        "",
        "## Audit note",
        "",
        "This is an index of the **original manually packaged archive**, not evidence of",
        "how the author produced each component. No binaries or configuration values",
        "were modified, and no files from the 7z were executed by this workflow.",
        "",
    ]
    (dist / "ARCHIVE_LAYOUT.md").write_text("\n".join(report), encoding="utf8")
    (dist / "ARCHIVE_PATHS.txt").write_text("\n".join(paths) + "\n", encoding="utf8")
    (dist / "SHA256SUMS").write_text(f"{sha}  {archive.name}\n", encoding="utf8")
    (dist / "SOURCE_RELEASE.json").write_text(
        json.dumps(info, indent=2, ensure_ascii=False) + "\n", encoding="utf8"
    )
    (dist / "RELEASE_NOTES.md").write_text(
        f"# rumla upstream package mirror\n\n"
        f"Source: {info['source_release_url']}\n\n"
        f"Asset: `{archive.name}`\n\n"
        f"SHA256: `{sha}`\n\n"
        "The .7z file is **byte-for-byte identical** to the upstream Release asset. "
        "The original author assembles this bundle manually; this workflow mirrors "
        "and checks it instead of claiming to reproduce the entire packaging process.\n\n"
        "The bundle is third-party software; compatibility and safety have not "
        "been tested on Switch hardware by this workflow.\n",
        encoding="utf8",
    )
    print(f"Verified original archive: {len(entries)} entries, {len(files)} files, SHA256={sha}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: rumla_release.py check|build")
    if sys.argv[1] == "check":
        check()
    elif sys.argv[1] == "build":
        build()
    else:
        sys.exit("Unsupported command")
