#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pymupdf"]
# ///
"""Find a book in the Calibre library and pull out what it says about a topic.

  lookup.py find "<title or author words>" [--topic] # is it in the library? -> ids
  lookup.py toc <book>                                # chapters with their PDF pages
  lookup.py search <book> "<term>" ["<term>" ...]     # pages ranked by hits, with snippets
  lookup.py pages <book> 120-124                      # the text of those pages

<book> is a Calibre book id, or a path to a .pdf/.epub. Pages are PDF page numbers;
`printed P` is the number printed on the page, when one can be read. Terms are
case-insensitive and match word starts, so "element" also finds "elements" and
"elemental"; a term in /slashes/ is a regex. The library is only ever read.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sqlite3
import sys

PREF_FILES = ["~/Library/Preferences/calibre/global.py.json", "~/.config/calibre/global.py.json"]
LONE_NUMBER = re.compile(r"^[\s\-–—()]*([0-9]{1,4}|[ivxlcdm]{1,6})[\s\-–—()]*$", re.I)


# ---------------------------------------------------------------- library
def library_path(explicit: str | None) -> pathlib.Path:
    if explicit:
        return pathlib.Path(explicit).expanduser()
    if os.environ.get("CALIBRE_LIBRARY"):
        return pathlib.Path(os.environ["CALIBRE_LIBRARY"]).expanduser()
    for f in PREF_FILES:
        p = pathlib.Path(f).expanduser()
        if p.exists() and json.loads(p.read_text()).get("library_path"):
            return pathlib.Path(json.loads(p.read_text())["library_path"])
    return pathlib.Path("~/Ismail's Library").expanduser()


def connect(lib: pathlib.Path) -> sqlite3.Connection:
    if not (lib / "metadata.db").exists():
        sys.exit(f"error: no metadata.db in {lib}; pass --library")
    return sqlite3.connect(f"{(lib / 'metadata.db').as_uri()}?mode=ro", uri=True)


def open_book(book: str, library: str | None, fmt: str | None):
    """-> (pymupdf doc, title). Prefers PDF (real page numbers), then EPUB."""
    import pymupdf
    if not book.isdigit():
        src = pathlib.Path(book).expanduser()
        return pymupdf.open(src), src.stem
    lib = library_path(library)
    con = connect(lib)
    row = con.execute("select title, path from books where id=?", (int(book),)).fetchone()
    if not row:
        sys.exit(f"error: no Calibre book with id {book}")
    fmts = dict(con.execute("select format, name from data where book=?", (int(book),)).fetchall())
    pick = fmt.upper() if fmt else next((f for f in ("PDF", "EPUB", "AZW3", "MOBI") if f in fmts), None)
    if not pick or pick not in fmts:
        sys.exit(f"error: book {book} has formats {sorted(fmts)}; this script reads PDF, EPUB, AZW3, MOBI")
    return pymupdf.open(lib / row[1] / f"{fmts[pick]}.{pick.lower()}"), row[0]


# ---------------------------------------------------------------- page text
def printed_number(text: str) -> str:
    lines = [l for l in text.splitlines() if l.strip()]
    for l in lines[:3] + lines[-3:]:
        m = LONE_NUMBER.match(l)
        if m:
            return m.group(1)
    return ""


def page_label(doc, i: int, text: str) -> str:
    p = printed_number(text)
    return f"page {i + 1}" + (f" · printed {p}" if p else "")


def flat(text: str) -> str:
    """Join hard-wrapped lines and de-hyphenate, for readable snippets."""
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


def term_pattern(term: str) -> re.Pattern:
    if len(term) > 2 and term.startswith("/") and term.endswith("/"):
        return re.compile(term[1:-1], re.I)
    words = [re.escape(w) for w in term.split()]
    return re.compile(r"\b" + r"\s+".join(words), re.I)


def parse_range(s: str, n: int) -> range:
    a, _, b = s.partition("-")
    a, b = int(a), int(b or a)
    if not 1 <= a <= b:
        sys.exit(f"error: bad page range {s}")
    return range(a - 1, min(b, n))


# ---------------------------------------------------------------- commands
def cmd_find(args) -> int:
    con = connect(library_path(args.library))
    terms = args.query.split()
    fields = ["b.title like ?", "b.author_sort like ?",
              "exists (select 1 from books_authors_link l join authors a on a.id=l.author "
              "where l.book=b.id and a.name like ?)"]
    if args.topic:  # also the book's tags and description, for "which books cover X"
        fields += ["exists (select 1 from books_tags_link l join tags t on t.id=l.tag "
                   "where l.book=b.id and t.name like ?)",
                   "exists (select 1 from comments c where c.book=b.id and c.text like ?)"]
    where = " and ".join(f"({' or '.join(fields)})" for _ in terms)
    params = [x for t in terms for x in (f"%{t}%",) * len(fields)]
    rows = con.execute(
        "select b.id, b.title, b.author_sort, (select group_concat(format) from data where book=b.id), "
        "substr(b.pubdate, 1, 4) "
        f"from books b where {where} order by b.title limit 40", params).fetchall()
    for r in rows:
        year = r[4] if r[4] and r[4] != "0101" else ""
        print(f"{r[0]:>6}  {r[1]}  —  {r[2]}  [{r[3]}] {year}")
    if not rows:
        print("no matches (try fewer or shorter words, or the author's surname alone)")
    return 0


def cmd_toc(args) -> int:
    doc, title = open_book(args.book, args.library, args.format)
    toc = doc.get_toc(simple=True)
    print(f"{title}  ({len(doc)} pages)")
    for level, heading, page in toc:
        print(f"{'  ' * (level - 1)}{heading}  ..p{page}")
    if not toc:
        print("no outline; read the contents pages instead (`pages <book> 5-12`)")
    return 0


def cmd_search(args) -> int:
    doc, title = open_book(args.book, args.library, args.format)
    pats = [term_pattern(t) for t in args.terms]
    toc = doc.get_toc(simple=True)
    hits, blank = [], 0
    for i, page in enumerate(doc):
        raw = page.get_text()
        if len(raw.strip()) < 50:
            blank += 1
            continue
        text = flat(raw)
        found = [(m.start(), m.end()) for p in pats for m in p.finditer(text)]
        if not found:
            continue
        found.sort()
        snippets, last_end = [], -1
        for s, e in found:
            if s < last_end:  # already inside the previous snippet
                continue
            a, b = max(0, s - args.context), min(len(text), e + args.context)
            snippets.append(("…" if a else "") + text[a:b] + ("…" if b < len(text) else ""))
            last_end = b
        chapter = next((h for _, h, p in reversed(toc) if p <= i + 1), "")
        hits.append((len(found), i, page_label(doc, i, raw), chapter, snippets))

    total = sum(h[0] for h in hits)
    print(f"{title}: {total} hits on {len(hits)} of {len(doc)} pages for {args.terms}")
    if blank > len(doc) * 0.3:
        print(f"warning: {blank} pages have no text layer (scanned?); they were not searched")
    order = sorted(hits, key=lambda h: (-h[0], h[1])) if args.rank else hits
    for n, _, label, chapter, snippets in order[: args.limit]:
        print(f"\n## {label}  ({n} hits){'  — ' + chapter if chapter else ''}")
        for s in snippets[: args.snippets]:
            print(f"  {s}")
    if len(hits) > args.limit:
        print(f"\n… {len(hits) - args.limit} more pages; raise --limit to see them")
    return 0


def cmd_pages(args) -> int:
    doc, _ = open_book(args.book, args.library, args.format)
    for i in parse_range(args.range, len(doc)):
        raw = doc[i].get_text()
        print(f"<!-- {page_label(doc, i, raw)} -->")
        print(raw.strip() or "[no text layer on this page]")
        print()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--library", help="Calibre library folder (default: Calibre's own setting)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find")
    f.add_argument("query")
    f.add_argument("--topic", action="store_true", help="also match tags and the book description")
    for name in ("toc", "search", "pages"):
        p = sub.add_parser(name)
        p.add_argument("book", help="Calibre id or path to a .pdf/.epub")
        p.add_argument("--format", help="PDF, EPUB, ... (default: PDF if present)")
    s = sub.choices["search"]
    s.add_argument("terms", nargs="+")
    s.add_argument("--context", type=int, default=160, help="characters either side of a hit")
    s.add_argument("--limit", type=int, default=25, help="pages to show")
    s.add_argument("--snippets", type=int, default=3, help="snippets per page")
    s.add_argument("--rank", action="store_true", help="most hits first instead of page order")
    sub.choices["pages"].add_argument("range", help='e.g. "120-124" or "57"')
    args = ap.parse_args()
    return {"find": cmd_find, "toc": cmd_toc, "search": cmd_search, "pages": cmd_pages}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
