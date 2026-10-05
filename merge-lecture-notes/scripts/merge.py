#!/usr/bin/env python3
"""Merge lecture-note files into one Markdown document, verbatim, in the order given.

Usage: merge.py --title "Series title" --out combined.md lecture1.md lecture2.md ...

- Strips each file's YAML frontmatter; uses its title/date/speaker for the section heading.
- Demotes each lecture's headings two levels (outside code fences, capped at ######) so they
  nest under its `## Lecture N` section.
- Refuses to overwrite --out. Exits 1 if any lecture's word count changes in the output.
Standard library only.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

SPEAKER_KEYS = ("speaker", "teacher", "author", "author_or_speaker", "shaykh")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})(\s)")


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m and m.group(2) and not m.group(2).startswith(("{", "[")):
            meta[m.group(1).lower()] = m.group(2).strip().strip("'\"")
    close = text.find("\n", end + 4)
    return meta, text[close + 1:] if close != -1 else ""


def demote(body: str) -> str:
    out, in_fence = [], False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            m = HEADING_RE.match(line)
            if m:
                line = "#" * min(len(m.group(1)) + 2, 6) + line[len(m.group(1)):]
        out.append(line)
    return "\n".join(out)


def words(text: str) -> int:
    return len(re.findall(r"[^\s#]+", text))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True)
    ap.add_argument("--out", required=True, type=pathlib.Path)
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    args = ap.parse_args()

    if args.out.exists():
        sys.exit(f"error: {args.out} already exists; choose another --out")
    for f in args.files:
        if f.suffix.lower() not in (".md", ".txt"):
            sys.exit(f"error: {f} is not .md or .txt; convert it first")
        if not f.is_file():
            sys.exit(f"error: {f} not found")

    lectures = []
    for n, f in enumerate(args.files, 1):
        meta, body = split_frontmatter(f.read_text(encoding="utf-8"))
        title = meta.get("title") or f.stem.replace("-", " ").replace("_", " ")
        speaker = next((meta[k] for k in SPEAKER_KEYS if meta.get(k)), "")
        byline = " · ".join(x for x in (meta.get("date", ""), speaker, f"source: {f.name}") if x)
        lectures.append((n, f, f"Lecture {n} — {title}", byline, body.strip("\n")))

    parts = [f"# {args.title}", "", "## Contents", ""]
    parts += [f"{n}. {heading}" for n, _, heading, _, _ in lectures]
    for _, _, heading, byline, body in lectures:
        parts += ["", f"## {heading}", "", f"*{byline}*", "", demote(body)]
    output = "\n".join(parts).rstrip("\n") + "\n"
    args.out.write_text(output, encoding="utf-8")

    # Verify: each lecture's section in the output has the same word count as its input body.
    sections = re.split(r"^## Lecture \d+ — .*$", output, flags=re.M)[1:]
    failed = False
    print(f"Wrote {args.out}")
    for (n, f, _, byline, body), section in zip(lectures, sections):
        got = words(section) - words(f"*{byline}*")
        want = words(body)
        status = "ok" if got == want else "MISMATCH"
        failed |= got != want
        print(f"  {n:>2}. {f.name}: {want} words in, {got} out — {status}")
    if len(sections) != len(lectures):
        print("  section count mismatch (a lecture body contains a '## Lecture N — ' line?)")
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
