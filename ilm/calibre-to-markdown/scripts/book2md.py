#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pymupdf"]
# ///
"""Convert a book from a Calibre library (or any PDF/EPUB) into one Markdown file.

  book2md.py find "<title or author words>"
  book2md.py probe <book> [--dir <work>]                 # what's in it; renders sample pages
  book2md.py convert <book> --engine text|tesseract --out <file.md> [--lang ara]
  book2md.py render <book> --dir <work> [--dpi 200]      # page images for vision transcription
  book2md.py assemble --dir <work> --out <file.md>       # build the .md from page-NNNN.md files

<book> is a Calibre book id, or a path to a .pdf/.epub. EPUBs always convert with pandoc
(`convert --engine text`). The Calibre library is only ever read (metadata.db opened read-only).

Every PDF page starts with `<!-- page N -->` (N = PDF page), plus `· printed P` when the
printed page number is known. Chapters come from the PDF outline when it has one; otherwise
from font sizes (text engine) or from the transcriber's headings (vision). Running headers,
footers, and images are dropped. Refuses to overwrite --out.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import sqlite3
import subprocess
import sys

PREF_FILES = ["~/Library/Preferences/calibre/global.py.json", "~/.config/calibre/global.py.json"]
LONE_NUMBER = re.compile(r"^[\s\-–—()]*([0-9]+|[٠-٩]+|[ivxlcdm]+)[\s\-–—()]*$", re.I)
ARABIC = re.compile("[\u0600-\u06FF]")
# Lam-alef ligatures extracted in the wrong order ("الله" -> "هللا", "الأ" -> "األ"): the PDF's
# Arabic is corrupt. Not auto-fixable: "سلام" comes out as "سالم", a different real word.
LAM_ALEF_SWAP = re.compile("هللا|هلل|(?<![\u0600-\u06FF])ا[أإآا]ل")
PAGE_FILE = "page-{:04d}.md"


# ---------------------------------------------------------------- source + metadata
def library_path(explicit: str | None) -> pathlib.Path:
    if explicit:
        return pathlib.Path(explicit).expanduser()
    if os.environ.get("CALIBRE_LIBRARY"):
        return pathlib.Path(os.environ["CALIBRE_LIBRARY"]).expanduser()
    for f in PREF_FILES:
        p = pathlib.Path(f).expanduser()
        if p.exists() and json.loads(p.read_text()).get("library_path"):
            return pathlib.Path(json.loads(p.read_text())["library_path"])
    sys.exit("error: can't find the Calibre library; pass --library or set CALIBRE_LIBRARY")


def connect(lib: pathlib.Path) -> sqlite3.Connection:
    if not (lib / "metadata.db").exists():
        sys.exit(f"error: no metadata.db in {lib}")
    return sqlite3.connect(f"{(lib / 'metadata.db').as_uri()}?mode=ro", uri=True)


def book_meta(con, book_id: int) -> dict:
    row = con.execute("select title, path, pubdate from books where id=?", (book_id,)).fetchone()
    if not row:
        sys.exit(f"error: no Calibre book with id {book_id}")
    q = lambda sql: [r[0] for r in con.execute(sql, (book_id,))]
    pubdate = row[2] or ""
    return {
        "title": row[0],
        "authors": q("select a.name from authors a join books_authors_link l on l.author=a.id where l.book=? order by l.id"),
        "language": q("select g.lang_code from languages g join books_languages_link l on l.lang_code=g.id where l.book=? order by l.item_order"),
        "publisher": (q("select p.name from publishers p join books_publishers_link l on l.publisher=p.id where l.book=?") or [""])[0],
        "series": (q("select s.name from series s join books_series_link l on l.series=s.id where l.book=?") or [""])[0],
        "pubdate": pubdate[:10] if pubdate and not pubdate.startswith("0101") else "",
        "identifiers": dict(con.execute("select type, val from identifiers where book=?", (book_id,)).fetchall()),
        "calibre_id": book_id,
        "_path": row[1],
        "_formats": dict(con.execute("select format, name from data where book=?", (book_id,)).fetchall()),
    }


def load_source(book: str, library: str | None, fmt: str | None = None) -> tuple[pathlib.Path, dict]:
    if book.isdigit():
        lib = library_path(library)
        meta = book_meta(connect(lib), int(book))
        fmts = meta.pop("_formats")
        pick = fmt.upper() if fmt else next((f for f in ("EPUB", "PDF") if f in fmts), None)
        if not pick or pick not in fmts:
            sys.exit(f"error: book {book} has formats {sorted(fmts)}; this script reads PDF or EPUB")
        src = lib / meta.pop("_path") / f"{fmts[pick]}.{pick.lower()}"
    else:
        src, meta = pathlib.Path(book).expanduser(), {"title": pathlib.Path(book).stem}
    if not src.exists():
        sys.exit(f"error: {src} not found")
    if src.suffix.lower() not in (".pdf", ".epub"):
        sys.exit("error: input must be a Calibre id, .pdf, or .epub")
    return src, meta


def open_pdf(src: pathlib.Path, pages: str | None = None):
    """Open a PDF -> (doc, first PDF page number). `pages` like "10-14" keeps only that range."""
    import pymupdf
    doc = pymupdf.open(src)
    if not pages:
        return doc, 1
    a, _, b = pages.partition("-")
    doc.select(list(range(int(a) - 1, min(int(b or a), len(doc)))))
    return doc, int(a)


def outline(doc) -> list:
    toc = [t for t in doc.get_toc(simple=True) if 1 <= t[2] <= len(doc)]
    return toc if len(toc) >= 2 else []


# ---------------------------------------------------------------- find / probe
def cmd_find(args) -> int:
    con = connect(library_path(args.library))
    terms = args.query.split()
    where = " and ".join("(b.title like ? or b.author_sort like ?)" for _ in terms)
    params = [x for t in terms for x in (f"%{t}%", f"%{t}%")]
    rows = con.execute(
        "select b.id, b.title, b.author_sort, (select group_concat(format) from data where book=b.id), "
        "(select group_concat(g.lang_code) from books_languages_link l join languages g on g.id=l.lang_code where l.book=b.id) "
        f"from books b where {where} order by b.title limit 40", params).fetchall()
    for r in rows:
        print(f"{r[0]:>6}  {r[1]}  —  {r[2]}  [{r[3]}] {r[4] or ''}")
    if not rows:
        print("no matches")
    return 0


def cmd_probe(args) -> int:
    src, meta = load_source(args.book, args.library, args.format)
    report = {"source": str(src), "mb": round(src.stat().st_size / 1e6, 2),
              **{k: v for k, v in meta.items() if k in ("title", "authors", "language")}}
    if src.suffix.lower() == ".epub":
        report["recommendation"] = "convert --engine text (EPUB via pandoc)"
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return 0
    doc, _ = open_pdf(src)
    sample = list(range(0, len(doc), max(1, len(doc) // 25)))
    chars = [len(doc[i].get_text().strip()) for i in sample]
    thin = sum(c < 40 for c in chars) / len(sample)
    mid = [len(doc) // 3, 2 * len(doc) // 3]
    text = "".join(doc[i].get_text() for i in sample)
    odd = sum(1 for ch in text if (ord(ch) < 32 and ch not in "\n\t\r") or ch == "\ufffd")
    garbled = odd / max(1, len(text))
    swaps = len(LAM_ALEF_SWAP.findall(text))
    report.update({
        "pages": len(doc), "outline_entries": len(outline(doc)), "garbled_char_ratio": round(garbled, 3),
        "arabic_lam_alef_swaps": swaps,
        "median_text_chars_per_page": sorted(chars)[len(chars) // 2],
        "pages_without_text_layer": f"{thin:.0%}",
        "sample_text": {i + 1: doc[i].get_text()[:400] for i in mid},
    })
    if args.dir:
        d = pathlib.Path(args.dir).expanduser()
        d.mkdir(parents=True, exist_ok=True)
        for i in mid:
            doc[i].get_pixmap(dpi=150).save(d / f"probe-{i + 1:04d}.png")
        report["sample_images"] = [str(d / f"probe-{i + 1:04d}.png") for i in mid]
    arabic = "ara" in meta.get("language", []) or any(ARABIC.search(t) for t in report["sample_text"].values())
    if thin > 0.3:
        report["recommendation"] = "scan: vision (render + assemble)" if arabic else "scan: convert --engine tesseract"
    elif garbled > 0.01:
        report["recommendation"] = "garbled text layer: vision (render + assemble)" if arabic else "garbled text layer: convert --engine tesseract"
    else:
        report["recommendation"] = ("text layer: compare sample_text with sample_images; if garbled use vision, "
                                    "else convert --engine text")
    if swaps:
        report["warning"] = ("Arabic in the text layer has lam-alef order corruption; Latin text is fine. "
                             "If the Arabic matters, use vision for the affected pages.")
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


# ---------------------------------------------------------------- per-page text
def norm(s: str) -> str:
    return re.sub(r"\d+|[٠-٩]+", "#", re.sub(r"\s+", " ", s)).strip().lower()


def join_lines(lines: list[str]) -> str:
    out = ""
    for line in lines:
        out = out[:-1] + line if out.endswith("-") and line[:1].islower() else (f"{out} {line}" if out else line)
    return out


def text_layer_pages(doc) -> list[dict]:
    """Blocks per page with font size and margin flag, from the PDF's own text layer."""
    pages, size_chars = [], collections.Counter()
    for page in doc:
        h, blocks = page.rect.height, []
        for b in page.get_text("dict", sort=True)["blocks"]:
            if b.get("type") != 0:
                continue
            lines, sizes = [], collections.Counter()
            for l in b["lines"]:
                t = "".join(s["text"] for s in l["spans"]).strip()
                if t:
                    lines.append(t)
                    for s in l["spans"]:
                        sizes[round(s["size"] * 2) / 2] += len(s["text"].strip())
            if lines:
                size_chars.update(sizes)
                blocks.append({"text": join_lines(lines), "lines": len(lines),
                               "size": sizes.most_common(1)[0][0],
                               "margin": b["bbox"][3] < h * 0.09 or b["bbox"][1] > h * 0.91})
        pages.append({"blocks": blocks, "printed": ""})
    body = size_chars.most_common(1)[0][0] if size_chars else 10
    return pages, body


def tesseract_pages(doc, lang: str, dpi: int) -> list[dict]:
    if not shutil.which("tesseract"):
        sys.exit("error: tesseract isn't installed (brew install tesseract tesseract-lang)")
    pages = []
    for i, page in enumerate(doc, 1):
        png = page.get_pixmap(dpi=dpi, colorspace="gray").tobytes("png")
        text = subprocess.run(["tesseract", "stdin", "stdout", "-l", lang], input=png,
                              capture_output=True, check=True).stdout.decode("utf-8")
        paras = [join_lines([l.strip() for l in p.splitlines() if l.strip()]) for p in re.split(r"\n\s*\n", text)]
        n = len([p for p in paras if p])
        blocks = [{"text": p, "lines": 1, "size": 0, "margin": k < 1 or k >= n - 1}
                  for k, p in enumerate(p for p in paras if p)]
        pages.append({"blocks": blocks, "printed": ""})
        print(f"\rOCR page {i}/{len(doc)}", end="", file=sys.stderr)
    print(file=sys.stderr)
    return pages


def header_key(s: str) -> str:
    """Letters only, lowercased: running headers match despite page numbers and punctuation."""
    return "".join(ch for ch in s.lower() if ch.isalpha())


EDGE_NUMBER = re.compile(r"^\W*([0-9]+|[٠-٩]+)\b|\b([0-9]+|[٠-٩]+)\W*$")


def strip_margins(pages: list[dict]) -> int:
    """Drop running headers/footers and lone page numbers; record printed page numbers."""
    counts = collections.Counter(header_key(b["text"]) for p in pages for b in p["blocks"] if b["margin"])
    threshold, removed = max(3, len(pages) * 0.02), 0
    for p in pages:
        keep = []
        for b in p["blocks"]:
            text = b["text"]
            if b["margin"] and len(text) <= 80 and not p["printed"]:
                edge = EDGE_NUMBER.search(text)
                if edge:
                    p["printed"] = edge.group(1) or edge.group(2)
            key = header_key(text)
            if b["margin"] and (LONE_NUMBER.match(text) or (key and len(text) <= 80 and counts[key] >= threshold)):
                removed += 1
            else:
                keep.append(b)
        p["blocks"] = keep
    return removed


def apply_outline(pages: list[dict], toc: list) -> None:
    for level, title, pno in toc:
        p = pages[pno - 1]
        heading = "#" * min(level + 1, 6) + " " + re.sub(r"\s+", " ", title).strip()
        match = next((b for b in p["blocks"] if norm(b["text"]) == norm(title) and "heading" not in b), None)
        if match:
            match["heading"] = heading
        else:
            p.setdefault("insert", []).append(heading)


def apply_font_headings(pages: list[dict], body: float) -> None:
    def candidate(b):
        return b["size"] >= body * 1.25 and b["lines"] <= 2 and len(b["text"]) <= 120
    sizes = sorted({b["size"] for p in pages for b in p["blocks"] if candidate(b)}, reverse=True)
    level = {s: min(i + 2, 4) for i, s in enumerate(sizes)}
    for p in pages:
        for b in p["blocks"]:
            if candidate(b):
                b["heading"] = "#" * level[b["size"]] + " " + b["text"]


def render_body(pages: list[dict], first: int = 1) -> tuple[str, list[int]]:
    out, empty = [], []
    for i, p in enumerate(pages, first):
        out += [f"<!-- page {i}" + (f" · printed {p['printed']}" if p["printed"] else "") + " -->", ""]
        out += [h + "\n" for h in p.get("insert", [])]
        if p.get("md") is not None:
            if p["md"].strip():
                out += [p["md"].strip(), ""]
            else:
                empty.append(i)
            continue
        if not p["blocks"]:
            empty.append(i)
        out += [x for b in p["blocks"] for x in (b.get("heading") or b["text"], "")]
    return "\n".join(out), empty


def epub_body(epub: pathlib.Path) -> str:
    if not shutil.which("pandoc"):
        sys.exit("error: EPUB conversion needs pandoc (brew install pandoc)")
    md = subprocess.run(["pandoc", str(epub), "-f", "epub", "-t", "gfm-raw_html", "--wrap=none"],
                        check=True, capture_output=True, text=True).stdout
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    md = re.sub(r"\[([^\]]*)\]\(#[^)]*\)", r"\1", md)  # internal links -> plain text
    md = re.sub(r"^#{1,6}\s*$", "", md, flags=re.M)  # empty headings
    md = re.sub(r"^(#{1,5}) ", r"#\1 ", md, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", md)


# ---------------------------------------------------------------- output
def write_markdown(out: pathlib.Path, src: pathlib.Path, meta: dict, method: str,
                   chapters_from: str, body: str, empty: list[int], extra: dict) -> int:
    if out.exists():
        sys.exit(f"error: {out} already exists; choose another --out")
    fm = {
        "type": "Document",
        **{k: meta.get(k) for k in ("title", "authors", "language", "publisher", "pubdate",
                                    "series", "identifiers", "calibre_id")},
        "source_file": str(src),
        "source_bytes": src.stat().st_size,
        "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        "conversion": {"method": method, "chapters_from": chapters_from,
                       "page_markers": "none" if src.suffix.lower() == ".epub" else "<!-- page N --> = PDF page N",
                       "converted_at": dt.datetime.now().astimezone().isoformat(timespec="seconds")},
    }
    fm = {k: v for k, v in fm.items() if v not in (None, "", [], {})}
    head = "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in fm.items()) + "---\n\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head + f"# {fm.get('title', src.stem)}\n\n" + body.strip() + "\n", encoding="utf-8")

    size = out.stat().st_size
    headings = [l for l in body.splitlines() if l.startswith("#")]
    print(json.dumps({
        "out": str(out), "method": method, "chapters_from": chapters_from, **extra,
        "source_mb": round(fm["source_bytes"] / 1e6, 2), "markdown_mb": round(size / 1e6, 2),
        "size_change": f"{100 * size / fm['source_bytes'] - 100:+.1f}%",
        "words": len(body.split()), "empty_pages": empty[:50], "empty_page_count": len(empty),
        "heading_count": len(headings), "headings_preview": headings[:60],
        "arabic_lam_alef_swaps": len(LAM_ALEF_SWAP.findall(body)),
    }, ensure_ascii=False, indent=1))
    return 0


def cmd_convert(args) -> int:
    src, meta = load_source(args.book, args.library, args.format)
    if src.suffix.lower() == ".epub":
        return write_markdown(pathlib.Path(args.out).expanduser(), src, meta, "epub (pandoc)",
                              "epub structure", epub_body(src), [], {})
    doc, first = open_pdf(src, args.pages)
    if args.engine == "text":
        pages, body = text_layer_pages(doc)
        method = "pdf text layer"
    else:
        lang = args.lang or ("ara" if "ara" in meta.get("language", []) else "eng")
        pages, body, method = tesseract_pages(doc, lang, args.dpi), 0, f"tesseract ({lang})"
    removed = strip_margins(pages)
    toc = outline(doc) if first == 1 else []
    if toc:
        apply_outline(pages, toc)
        chapters_from = "pdf outline"
    elif args.engine == "text":
        apply_font_headings(pages, body)
        chapters_from = "font-size heuristic"
    else:
        chapters_from = "none (no outline; add headings by hand)"
    text, empty = render_body(pages, first)
    return write_markdown(pathlib.Path(args.out).expanduser(), src, meta, method, chapters_from, text, empty,
                          {"pages": len(pages), "removed_margin_blocks": removed})


# ---------------------------------------------------------------- vision: render + assemble
def cmd_render(args) -> int:
    src, meta = load_source(args.book, args.library, "pdf")
    d = pathlib.Path(args.dir).expanduser()
    d.mkdir(parents=True, exist_ok=True)
    doc, first = open_pdf(src, args.pages)
    numbers = list(range(first, first + len(doc)))
    for i, page in zip(numbers, doc):
        png = d / f"page-{i:04d}.png"
        if not png.exists():
            page.get_pixmap(dpi=args.dpi, colorspace="gray").save(png)
    (d / "manifest.json").write_text(json.dumps(
        {"source": str(src), "pages": numbers, "meta": meta, "outline": outline(doc) if first == 1 else []},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"dir": str(d), "pages": len(doc), "outline_entries": len(outline(doc))}, indent=1))
    return 0


def cmd_assemble(args) -> int:
    d = pathlib.Path(args.dir).expanduser()
    man = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
    numbers = man["pages"]
    missing = [i for i in numbers if not (d / PAGE_FILE.format(i)).exists()]
    if missing:
        sys.exit(f"error: {len(missing)} page transcription(s) missing, e.g. {missing[:20]}")
    pages = []
    for i in numbers:
        text = (d / PAGE_FILE.format(i)).read_text(encoding="utf-8")
        printed = ""
        m = re.match(r"\s*printed:\s*(.+?)\s*\n", text)
        if m:
            printed, text = m.group(1), text[m.end():]
        pages.append({"blocks": [], "printed": printed, "md": text})
    if man["outline"]:
        for level, title, pno in man["outline"]:
            pages[pno - numbers[0]].setdefault("insert", []).append("#" * min(level + 1, 6) + " " + title.strip())
    body, empty = render_body(pages, numbers[0])
    return write_markdown(pathlib.Path(args.out).expanduser(), pathlib.Path(man["source"]), man["meta"],
                          "vision transcription", "pdf outline" if man["outline"] else "transcriber headings",
                          body, empty, {"pages": len(numbers)})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--library", help="Calibre library folder (default: from Calibre's settings)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("find").add_argument("query")
    for name in ("probe", "convert", "render"):
        p = sub.add_parser(name)
        p.add_argument("book", help="Calibre book id, or a path to a .pdf/.epub")
        p.add_argument("--format", choices=["pdf", "epub"], help="Calibre format to use (default: EPUB if present)")
    sub.choices["probe"].add_argument("--dir", help="also render two sample pages here")
    c = sub.choices["convert"]
    c.add_argument("--engine", choices=["text", "tesseract"], required=True)
    c.add_argument("--out", required=True)
    c.add_argument("--lang", help="tesseract language(s), e.g. eng, ara, ara+eng")
    c.add_argument("--dpi", type=int, default=300)
    c.add_argument("--pages", help='trial run on a page range only, e.g. "10-14"')
    r = sub.choices["render"]
    r.add_argument("--dir", required=True)
    r.add_argument("--dpi", type=int, default=200)
    r.add_argument("--pages", help='render only this page range, e.g. "10-14"')
    a = sub.add_parser("assemble")
    a.add_argument("--dir", required=True)
    a.add_argument("--out", required=True)
    args = ap.parse_args()
    return {"find": cmd_find, "probe": cmd_probe, "convert": cmd_convert,
            "render": cmd_render, "assemble": cmd_assemble}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
