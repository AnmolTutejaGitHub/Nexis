#!/usr/bin/env python3
"""
Run get_repomap against sample files for every supported language and
print a structured pass/fail/symbols report.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.code_navigation.repomap.get_repomap import get_repomap

SAMPLE_DIR = os.path.dirname(__file__)

SAMPLES = [
    ("python",      "sample.py"),
    ("javascript",  "sample.js"),
    ("typescript",  "sample.ts"),
    ("tsx",         "sample.tsx"),
    ("java",        "sample.java"),
    ("c",           "sample.c"),
    ("cpp",         "sample.cpp"),
    ("go",          "sample.go"),
    ("rust",        "sample.rs"),
    ("ruby",        "sample.rb"),
    ("php",         "sample.php"),
    ("kotlin",      "sample.kt"),
    ("scala",       "sample.scala"),
    ("c_sharp",     "sample.cs"),
    ("bash",        "sample.sh"),
    ("lua",         "sample.lua"),
    ("r",           "sample.r"),
    ("perl",        "sample.pl"),
    ("haskell",     "sample.hs"),
    ("elixir",      "sample.ex"),
    ("sql",         "sample.sql"),
    ("objc",        "sample.m"),
    ("erlang",      "sample.erl"),
    ("ocaml",       "sample.ml"),
    ("fortran",     "sample.f90"),
    ("commonlisp",  "sample.lisp"),
    ("dockerfile",  "sample.dockerfile"),
    ("gomod",       "sample.mod"),
    ("html",        "sample.html"),
    ("css",         "sample.css"),
    ("json",        "sample.json"),
    ("yaml",        "sample.yaml"),
    ("toml",        "sample.toml"),
    ("markdown",    "sample.md"),
    ("make",        "sample.makefile"),
    ("hcl",         "sample.tf"),
    ("regex",       "sample.regex"),
]

GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def symbol_summary(symbols: dict) -> str:
    parts = []
    for cat, items in symbols.items():
        names = [i["value"][:30] for i in items[:3]]
        tail = f"+{len(items)-3}" if len(items) > 3 else ""
        parts.append(f"{cat}({len(items)}): {', '.join(names)}{tail}")
    return " | ".join(parts)

def run():
    passed = failed = empty = 0
    rows = []

    for lang, filename in SAMPLES:
        path = os.path.join(SAMPLE_DIR, filename)
        if not os.path.exists(path):
            rows.append((RED, "MISS", lang, filename, "sample file not found", {}))
            failed += 1
            continue

        result = get_repomap(path)

        if "error" in result:
            rows.append((RED, "FAIL", lang, filename, result["error"], {}))
            failed += 1
        elif not result.get("symbols"):
            rows.append((YELLOW, "EMPTY", lang, filename, "parsed OK, no symbols extracted", {}))
            empty += 1
        else:
            rows.append((GREEN, "PASS", lang, filename, "", result["symbols"]))
            passed += 1

    total = len(SAMPLES)
    print(f"\n{BOLD}Repomap language coverage — {total} languages{RESET}")
    print("=" * 72)

    for color, status, lang, fname, msg, symbols in rows:
        tag = f"{color}[{status:5}]{RESET}"
        label = f"{BOLD}{lang:<14}{RESET} {fname}"
        if symbols:
            detail = symbol_summary(symbols)
            print(f"  {tag} {label}")
            print(f"           {detail}")
        elif msg:
            print(f"  {tag} {label}")
            print(f"           {RED}{msg}{RESET}")
        else:
            print(f"  {tag} {label}")

    print("=" * 72)
    print(
        f"  {GREEN}PASS: {passed}{RESET}  "
        f"{YELLOW}EMPTY: {empty}{RESET}  "
        f"{RED}FAIL: {failed}{RESET}  "
        f"TOTAL: {total}"
    )
    print()

if __name__ == "__main__":
    run()
