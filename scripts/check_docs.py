#!/usr/bin/env python3
"""Check ROB-SN documentation structure without network access or dependencies.

Run from any directory. --known-paths supports a sparse editorial workspace:
its UTF-8 file lists repository-relative destinations known from a full inventory.
Those omitted files are valid link destinations but are not parsed or validated.
This is not a Markdown renderer or an RxJS runtime-conformance checker.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--known-paths", type=Path, help="Optional inventory for omitted files")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"Not a directory: {root}")
    known: set[Path] = set()
    if args.known_paths:
        for line in args.known_paths.read_text(encoding="utf-8").splitlines():
            if line.strip():
                destination = (root / line.strip()).resolve()
                if not destination.is_relative_to(root):
                    parser.error(f"Inventory path leaves repository: {line}")
                known.add(destination)
    errors: list[str] = []
    files = sorted(root.rglob("*.md"))
    if not files:
        parser.error("No Markdown documents found")
    local_links = 0
    rxjs_links = 0
    for path in files:
        label = str(path.relative_to(root))
        text = path.read_text(encoding="utf-8")
        fenced = False
        prose: list[str] = []
        for line in text.splitlines():
            if line.lstrip().startswith("```"):
                fenced = not fenced
            elif not fenced:
                prose.append(line)
        if fenced:
            errors.append(f"{label}: unbalanced triple-backtick fences")
        body = "\n".join(prose)
        if sum(line.strip() == "$$" for line in prose) % 2:
            errors.append(f"{label}: unbalanced display-math delimiters")
        for match in re.finditer(r"\[[^\]\n]*\]\(([^)\s]+)\)", body):
            href = match.group(1)
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                if parsed.netloc.lower() == "github.com" and parsed.path.startswith("/ReactiveX/rxjs/blob/"):
                    rxjs_links += 1
                    if not parsed.path.startswith("/ReactiveX/rxjs/blob/7.8.2/"):
                        errors.append(f"{label}: unpinned RxJS implementation link: {href}")
                continue
            if not parsed.path or parsed.path.startswith("<"):
                continue
            local_links += 1
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root):
                errors.append(f"{label}: relative target leaves repository: {href}")
            elif not destination.exists() and destination not in known:
                errors.append(f"{label}: missing relative target: {href}")
    catalogue = root / "docs/TRANSITION-RULE-CATALOGUE.md"
    if not catalogue.is_file():
        errors.append("Missing transition-rule catalogue")
        identifiers: list[str] = []
    else:
        identifiers = re.findall(r"^\| ([LVBTCFS]\d+) \|", catalogue.read_text(encoding="utf-8"), re.M)
        counts = {"L": 4, "V": 7, "B": 7, "T": 6, "C": 6, "F": 6, "S": 4}
        expected = {f"{prefix}{index}" for prefix, count in counts.items() for index in range(1, count + 1)}
        if len(identifiers) != 40 or set(identifiers) != expected:
            errors.append("Expected exactly 40 unique rule IDs in the declared seven families")
    if errors:
        print("FAIL\n" + "\n".join(errors), file=sys.stderr)
        return 1
    omitted = sum(not path.exists() for path in known)
    print(f"PASS: {len(files)} Markdown files inspected; {local_links} relative link destinations; "
          f"{rxjs_links} pinned RxJS links; {len(identifiers)} unique transition rules.")
    if omitted:
        print(f"Sparse workspace: {omitted} known destinations were not parsed.")
    print("No external URLs, anchor fragments, rendering, or runtime semantics checked.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
