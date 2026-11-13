#!/usr/bin/env python3
"""Static analysis of rumla's *reference* SD bundle. Never used as build input."""
from __future__ import annotations
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

SOURCE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
META = Path(sys.argv[3]).resolve()
if not SOURCE.is_dir():
    raise SystemExit("Missing extracted release root")
candidates = [
    p for p in SOURCE.iterdir()
    if p.is_dir() and (p / "atmosphere").is_dir() and (p / "bootloader").is_dir()
]
if len(candidates) != 1:
    raise SystemExit(f"Expected exactly one SD-card root, got {candidates!r}")
root = candidates[0]
OUT.mkdir(parents=True, exist_ok=True)
files = []
for path in sorted(root.rglob("*")):
    if not path.is_file() or path.is_symlink():
        continue
    rel = path.relative_to(root).as_posix()
    h = hashlib.sha256()
    with path.open("rb") as fd:
        for chunk in iter(lambda: fd.read(1024 * 1024), b""):
            h.update(chunk)
    files.append({"path": rel, "bytes": path.stat().st_size, "sha256": h.hexdigest()})
entrylist = json.loads(META.read_text(encoding="utf-8"))
record = {
    "upstream_tag": entrylist["tag_name"],
    "upstream_release": entrylist["html_url"],
    "original_7z_asset": entrylist["original_asset"],
    "original_7z_sha256": entrylist["original_sha256"],
    "sd_root": root.name,
    "sd_files": len(files),
    "files": files,
}
(OUT / "manifest.json").write_text(json.dumps(record, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
counts = Counter(f["path"].split("/")[0] for f in files)
exts = Counter(Path(f["path"]).suffix.lower() or "(none)" for f in files)
ini_names = [f["path"] for f in files if f["path"].lower().endswith((".ini", ".cfg", ".json", ".txt", ".flag", ".bso"))]
binary_groups = defaultdict(list)
for f in files:
    path = f["path"]
    low = path.lower()
    if low.endswith(".nro"):
        binary_groups["nro"].append(path)
    elif low.endswith(".ovl"):
        binary_groups["ovl"].append(path)
    elif low.endswith(".ips"):
        binary_groups["ips"].append(path)
    elif low.endswith((".bin", ".kip", ".kipm", ".romfs", ".nsp")):
        binary_groups["other binary"].append(path)
notes = [
    "# Rumla 1.12.2 original archive: reverse assembly audit",
    "",
    f"- Source: {record['upstream_release']}",
    f"- Source 7z SHA256: \`{record['original_7z_sha256']}\`",
    f"- Installed SD root: \`{root.name}\`",
    f"- SD-card files: **{len(files)}** (not counting auxiliary guides)",
    "",
    "## Top-level SD directories",
    "",
    "| Prefix | Files |", "| --- | ---: |",
]
notes += [f"| \`{k}\` | {v} |" for k,v in counts.most_common()]
notes += ["", "## Extensions", "", "| Suffix | Files |", "| --- | ---: |"]
notes += [f"| \`{k}\` | {v} |" for k,v in exts.most_common()]
notes += ["", "## Configuration files", ""]
notes += [f"- \`{p}\`" for p in ini_names]
for title, group in binary_groups.items():
    notes += ["", f"## {title.upper()} candidates ({len(group)})", ""]
    notes += [f"- \`{p}\`" for p in group]
(OUT / "inventory.md").write_text("\n".join(notes)+"\n", encoding="utf8")
# Copy only readable, small configuration text to a forensic reference folder,
# NOT whole firmware images or compiled/patch binaries.
saved=[]
for f in files:
    path = Path(f["path"])
    if path.suffix.lower() not in (".ini",".cfg",".json",".txt",".flag",".bso",".config",".cn"):
        continue
    if f["bytes"] > 64 * 1024:
        continue
    raw = (root / path).read_bytes()
    if b"\0" in raw:
        continue
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        try:
            raw.decode("gb18030")
        except UnicodeDecodeError:
            continue
    out = OUT / "config-reference" / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    saved.append(path.as_posix())
(OUT / "README.md").write_text(
    "# Rumla Release baseline (read-only reference)\n\n"
    "This directory was extracted from the author-published .7z **for comparison**. "
    "The CI build MUST NOT download or use the original .7z as an input.\n\n"
    "manifest.json records each installed SD file's SHA256, size and path.\n"
    "config-reference/ contains only small human-readable text configs for research. "
    "Do not assume all of them are safe to copy to a different firmware version.\n\n"
    f"Captured {len(files)} installed files and {len(saved)} text configs.\n",
    encoding="utf8",
)
print(f"Extracted reference inventory: {len(files)} SD files, {len(saved)} readable configs")
print("Top-level:", counts)
print("Binary classes:", {k:len(v) for k,v in binary_groups.items()})
