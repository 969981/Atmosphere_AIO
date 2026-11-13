#!/usr/bin/env python3
"""Independent rumla-style builder. Never downloads the original rumla Release."""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import zipfile

ROOT = Path.cwd()
WORK = ROOT / "work"
SD = WORK / "sd" / "Rumla-Rebuild-SD"
DIST = ROOT / "dist"
ASSETS = WORK / "assets"
PROFILE = json.loads((ROOT / "profiles/rumla-1.12.2.json").read_text())
REFERENCE = json.loads((ROOT / "reference/manifest.json").read_text())
ANCHORS = {"atmosphere","bootloader","switch","config","warmboot_mariko",
           "exosphere.ini","hbmenu.nro","hbmenu.nsp","payload.bin","boot.dat"}
WRITES, SOURCES, FAILURES = {}, [], []

def digest(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def run(*args):
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return result.stdout.strip()

def dest_for(relative):
    p = PurePosixPath(relative.replace("\\", "/"))
    if p.is_absolute() or not p.parts or ".." in p.parts:
        raise ValueError(f"Unsafe destination: {relative}")
    dest = SD.joinpath(*p.parts)
    if not dest.resolve().is_relative_to(SD.resolve()):
        raise ValueError(f"Path outside SD: {relative}")
    return dest

def write(relative, data, owner):
    dst = dest_for(relative)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    WRITES[relative] = owner

def zip_relative(member):
    p = PurePosixPath(member.replace("\\", "/"))
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"Unsafe archive member: {member}")
    for i, segment in enumerate(p.parts):
        if segment.lower() in ANCHORS:
            return "/".join(p.parts[i:])
    return None

def fetch(item):
    work = ASSETS / item["id"]
    work.mkdir(parents=True, exist_ok=True)
    run("gh", "release", "download", item["tag"], "--repo", item["repo"],
        "--pattern", item["asset"], "--dir", str(work), "--clobber")
    path = work / item["asset"]
    if not path.is_file() or path.stat().st_size < 1:
        raise RuntimeError("Release asset not downloaded")
    return path

def open_safe_zip(path):
    archive = zipfile.ZipFile(path)
    members = archive.infolist()
    if sum(i.file_size for i in members) > 2_000_000_000:
        raise RuntimeError("Archive expansion limit")
    for entry in members:
        if entry.file_size > 400_000_000:
            raise RuntimeError("ZIP member too large")
        p = PurePosixPath(entry.filename.replace("\\", "/"))
        if p.is_absolute() or ".." in p.parts:
            raise RuntimeError(f"Unsafe ZIP member {entry.filename}")
    if archive.testzip() is not None:
        raise RuntimeError("Corrupt ZIP")
    return archive

def integrate(item, path):
    if item.get("save_english_nyx"):
        base = SD / "bootloader/sys/nyx.bin"
        english = SD / "bootloader/sys/nyx.bin.en"
        if base.is_file() and not english.exists():
            english.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(base, english)
            WRITES["bootloader/sys/nyx.bin.en"] = "official-hekate"
    if item["kind"] == "file":
        write(item["dest"], path.read_bytes(), item["id"])
        return 1
    with open_safe_zip(path) as z:
        if item["kind"] == "overlay":
            total = 0
            for member in z.infolist():
                if member.is_dir():
                    continue
                rel = zip_relative(member.filename)
                if rel:
                    write(rel, z.read(member), item["id"])
                    total += 1
            if not total:
                raise RuntimeError("Archive contains no SD-card paths")
            return total
        if item["kind"] == "find":
            hits = [m for m in z.infolist() if not m.is_dir() and
                    fnmatch.fnmatch(PurePosixPath(m.filename).name.casefold(),
                                   item["match"].casefold())]
            if len(hits) != 1:
                raise RuntimeError(f"Expected one {item['match']}, found {len(hits)}")
            write(item["dest"], z.read(hits[0]), item["id"])
            return 1
    raise RuntimeError(f"Unsupported kind: {item['kind']}")

def apply_configs():
    folder = ROOT / "reference/config-reference"
    if not folder.is_dir():
        raise RuntimeError("Reference text configurations missing")
    done = []
    for src in sorted(folder.rglob("*")):
        if not src.is_file():
            continue
        name = src.relative_to(folder).as_posix()
        if name == "bootloader/patches.ini":
            continue  # must be generated from independently verifiable patches
        if src.suffix.lower() not in {".ini",".json",".txt",".flag",".config"}:
            continue
        content = src.read_bytes()
        if len(content) > 65536 or b"\x00" in content:
            continue
        write(name, content, "researched-text-config")
        done.append(name)
    return done

def inventory():
    result = {}
    for file in sorted(SD.rglob("*")):
        if file.is_file():
            result[file.relative_to(SD).as_posix()] = {
                "size": file.stat().st_size, "sha256": digest(file)}
    return result

def report(built, configs):
    baseline = {e["path"]:e for e in REFERENCE["files"]}
    exact = sorted(x for x in built if x in baseline and
                   built[x]["sha256"] == baseline[x]["sha256"])
    changed = sorted(x for x in built if x in baseline and
                     built[x]["sha256"] != baseline[x]["sha256"])
    missing = sorted(set(baseline) - set(built))
    extra = sorted(set(built) - set(baseline))
    stats = {"reference_files":len(baseline),"rebuilt_files":len(built),
             "byte_identical":len(exact),"different_hash":len(changed),
             "missing_files":len(missing),"extra_files":len(extra),
             "exact_percent":round(100*len(exact)/max(len(baseline),1),2)}
    lines = [
        "# Independent rumla-style rebuild vs original",
        "",
        "Experimental source assembly; NOT the original author's binary and NOT hardware tested.",
        "The original .7z is never accessed by this builder.",
        "",
        "| Comparison | Count |","| --- | ---: |",
    ]
    lines += [f"| {name} | {n} |" for name,n in stats.items()]
    lines.append("")
    for label,files in [("Identical",exact),("Different SHA256",changed),
                        ("Missing",missing),("Extra",extra)]:
        lines += [f"## {label} ({len(files)})",""]
        lines += ["- " + name for name in files]
        lines.append("")
    lines += ["## Download or extraction failures",""]
    lines += ["- "+err for err in FAILURES] or ["- None"]
    lines += ["","## Still unmapped",""]
    lines += ["- "+x for x in PROFILE["known_exclusions"]]
    lines += ["",f"Researched text configs applied: {len(configs)}",""]
    (DIST / "PARITY.md").write_text("\n".join(lines),encoding="utf8")
    (DIST / "BUILD_REPORT.json").write_text(
        json.dumps({"stats":stats,"exact":exact,"changed":changed,
                    "missing":missing,"extra":extra,"failures":FAILURES,
                    "configs":configs,"component_sources":SOURCES,
                    "file_origin":WRITES},indent=2,ensure_ascii=False)+"\n",
        encoding="utf8")
    return stats

def main():
    if not os.environ.get("GH_TOKEN"):
        raise RuntimeError("Missing GH_TOKEN")
    if REFERENCE["upstream_tag"] != "1.12.2":
        raise RuntimeError("Reference version mismatch")
    SD.mkdir(parents=True,exist_ok=True)
    DIST.mkdir(parents=True,exist_ok=True)
    for item in PROFILE["components"]:
        print(f"::group::{item['id']}: {item['repo']}@{item['tag']}",flush=True)
        try:
            source = fetch(item)
            count = integrate(item,source)
            SOURCES.append({"id":item["id"],"repo":item["repo"],
                            "tag":item["tag"],"asset":item["asset"],
                            "sha256":digest(source),"size":source.stat().st_size,
                            "integrated":count,"result":"success"})
            print(f"Merged {count} files",flush=True)
        except Exception as exc:
            reason = f"{item['id']}: {exc}"
            print("WARNING " + reason,file=sys.stderr,flush=True)
            FAILURES.append(reason)
            SOURCES.append({"id":item["id"],"repo":item["repo"],
                            "tag":item["tag"],"result":"failed",
                            "reason":str(exc)})
            if item.get("required"):
                raise
        finally:
            print("::endgroup::",flush=True)
    configs = apply_configs()
    # The source sys-clk archive uses a subfolder, while rumla places the
    # same upstream binary at switch/sys-clk-manager.nro.
    manager = SD / "switch/sys-clk/sys-clk.nro"
    if manager.exists():
        write("switch/sys-clk-manager.nro", manager.read_bytes(), "sysclk-manager-mapped")
    # rumla selects Hekate's update.bin as Atmosphere's reboot payload.
    update = SD / "bootloader/update.bin"
    if update.exists():
        write("atmosphere/reboot_payload.bin", update.read_bytes(), "hekate-reboot-payload")
    # Keep the package's SD tree close to the author's hand-selected baseline.
    # Upstream vendors sometimes include extra themes, debug flags or configs.
    known_paths = {f["path"] for f in REFERENCE["files"]}
    removed = []
    for f in sorted(SD.rglob("*")):
        if f.is_file() and f.relative_to(SD).as_posix() not in known_paths:
            removed.append(f.relative_to(SD).as_posix())
            f.unlink()
    print("Pruned non-baseline vendor extras:", len(removed),flush=True)
    # The author supplies hekate-specific signature patches in patches.ini.
    # Without a verified independent patch source, remove the unavailable
    # kip1patch directive instead of leaving a broken reference.
    if not (SD / "bootloader/patches.ini").exists():
        for name in ("bootloader/hekate_ipl.ini","bootloader/ini/more.ini"):
            p=SD / name
            if p.exists():
                raw=p.read_bytes()
                filtered=b"\n".join(line for line in raw.split(b"\n")
                                     if not line.strip().startswith(b"kip1patch="))
                p.write_bytes(filtered)
                WRITES[name]="reviewed-boot-config-no-missing-ips"
    files = inventory()
    stats = report(files,configs)
    (DIST / "SOURCE_LOCK.json").write_text(
        json.dumps(SOURCES,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    (DIST / "REBUILD_MANIFEST.json").write_text(
        json.dumps(files,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    must_have = ["atmosphere/package3","bootloader/update.bin",
                 "bootloader/sys/nyx.bin","bootloader/payloads/fusee.bin","payload.bin"]
    absent = [p for p in must_have if p not in files]
    if absent:
        raise RuntimeError(f"Essential boot files missing: {absent}")
    date = datetime.now(timezone.utc).strftime("%Y%m%d")
    out = DIST / f"AMS1.12.2-rumla-rebuild-experimental-{date}.7z"
    run("7z","a","-t7z","-mx=7",str(out),str(SD))
    run("7z","t",str(out))
    (DIST / "SHA256SUMS").write_text(f"{digest(out)}  {out.name}\n",encoding="utf8")
    print(f"INDEPENDENT BUILD {stats} failures={len(FAILURES)}",flush=True)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"],"a",encoding="utf8") as summary:
            summary.write("## Rumla source rebuild (experimental)\n\n")
            summary.write(f"Original {stats['reference_files']} files; "
                          f"rebuilt {stats['rebuilt_files']}; "
                          f"exact hashes {stats['byte_identical']}; "
                          f"missing {stats['missing_files']}; "
                          f"different {stats['different_hash']}.\n\n")
            summary.write("Read PARITY.md and BUILD_REPORT.json before using.\n")

if __name__ == "__main__":
    main()
