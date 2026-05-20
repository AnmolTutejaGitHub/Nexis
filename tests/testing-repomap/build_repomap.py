#!/usr/bin/env python3
import os, json, glob

from tools.code_navigation.repomap.get_repomap import get_repomap

DIR = os.path.dirname(__file__)
OUT = os.path.join(DIR, "repomap.json")

files = sorted(glob.glob(os.path.join(DIR, "sample.*")))
repomap = {}

for path in files:
    filename = os.path.basename(path)
    result = get_repomap(path)
    repomap[filename] = result
    status = "error" if "error" in result else f"{sum(len(v) for v in result.get('symbols', {}).values())} symbols"
    print(f"  {filename:<30} {status}")

with open(OUT, "w") as f:
    json.dump(repomap, f, indent=2)

print(f"\nWrote {len(repomap)} entries to repomap.json")
