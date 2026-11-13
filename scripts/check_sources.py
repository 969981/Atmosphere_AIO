#!/usr/bin/env python3
"""Read-only upstream release monitor for independently sourced components."""
import collections
import json
import os
import urllib.request
from pathlib import Path

cfg = json.loads(Path("profiles/rumla-1.12.2.json").read_text())
unique = {}
for c in cfg["components"]:
    unique[c["repo"]] = c["tag"]
headers = {"Accept":"application/vnd.github+json","User-Agent":"Atmosphere-AIO-rumla-rebuild-monitor"}
if os.environ.get("GH_TOKEN"):
    headers["Authorization"]="Bearer "+os.environ["GH_TOKEN"]
rows=[]
for repo,pin in unique.items():
    try:
        req=urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/latest",headers=headers)
        with urllib.request.urlopen(req,timeout=25) as resp:
            d=json.load(resp)
        new=d["tag_name"]
        rows.append({"repository":repo,"pinned":pin,"latest":new,
                     "changed":pin!=new,"url":d["html_url"]})
    except Exception as e:
        rows.append({"repository":repo,"pinned":pin,"error":str(e)})
out=Path("dist")
out.mkdir(exist_ok=True)
(out/"UPSTREAM_VERSION_CHECK.json").write_text(json.dumps(rows,indent=2,ensure_ascii=False)+"\n")
changed=sum(1 for r in rows if r.get("changed"))
errors=sum(1 for r in rows if r.get("error"))
text=["# Independent rumla builder: upstream version check","","| Repository | Locked | Latest | Status |","| --- | --- | --- | --- |"]
for r in rows:
    state="⚠️ source lookup failed" if r.get("error") else ("🆕 update" if r.get("changed") else "same")
    text.append(f"| {r['repository']} | {r['pinned']} | {r.get('latest','?')} | {state} |")
text += ["",f"Changes detected: {changed}; failed lookups: {errors}.",
         "New versions are NOT silently substituted into a firmware bundle without a new locked profile and verification."]
(out/"UPSTREAM_VERSION_CHECK.md").write_text("\n".join(text)+"\n",encoding="utf8")
print(f"Upstream monitor: {changed} newer/different tags; {errors} errors")
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"],"a",encoding="utf8") as f:
        f.write("\n".join(text)+"\n")
