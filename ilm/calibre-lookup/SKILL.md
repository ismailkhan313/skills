---
name: calibre-lookup
description: Check whether a book is in the user's Calibre library and quickly pull out what it says about a topic — finds the book from metadata.db, shows its chapters, searches its full text for terms, and reads the matching pages, then answers with page citations. Use when asked "do I have <book>", "what does <book/author> say about X", "find X in <book>", or "which of my books cover X". For converting a whole book to Markdown, use calibre-to-markdown instead.
---

# Calibre lookup

Answer a question from one book in the Calibre library without converting it. Everything goes through `scripts/lookup.py` (run with `uv run`; it pulls in PyMuPDF). It opens `metadata.db` **read-only** and works while the Calibre app is open. `calibredb` does not: it refuses to run beside the GUI. Its `--help` lists every option.

## Steps

1. **Find the book:** `uv run scripts/lookup.py find "<title or author words>"`. Words match the title or author, and short distinctive words work best (`"nasr cosmological"`). If there is no hit, try the surname alone. To ask "which of my books cover X", add `--topic`, which also searches tags and descriptions. If several results could be the book, list them (id, title, formats) and ask which one. If none matches, say the book isn't in the library, and stop there.
2. **Map it:** `uv run scripts/lookup.py toc <id>`. This lists the chapters with their PDF pages. A section whose title names the topic is usually the best page to read.
3. **Search:** `uv run scripts/lookup.py search <id> "<term>" ["<synonym>" ...] --rank`. Terms match word starts, so `element` also finds `elements`. Add synonyms and transliterations (e.g. `"four elements" "'anasir" "/ust[uū]qus/"`), and use a term in `/slashes/` as a regex. The results list pages ranked by hits, each with its chapter and snippets. If it warns that pages have no text layer, the book is a scan, so tell the user and offer calibre-to-markdown (OCR or vision).
4. **Read:** `uv run scripts/lookup.py pages <id> <a-b>` for the strongest 2–4 page ranges: those with the most hits plus the section the TOC points to. Snippets alone aren't enough to answer from. Cap reading at about 15 pages, then ask before reading more.
5. **Answer briefly:** say whether the book is in the library (title, author, id), then give the book's position, grouped by thinker or chapter when the book compares several. Cite every point as `p. <printed>` (with the PDF page in brackets when they differ). Quote key sentences exactly. List any further pages that are relevant but weren't read.

## Notes

- `page N` is the PDF page. `printed P` is the number printed on the page, read from its first or last lines. It's missing on some pages, so work it out from the offset of a nearby page.
- PDF is preferred over EPUB because it has real page numbers. Pass `--format EPUB` to read the EPUB instead, but its page numbers come from the layout and aren't citable.
- OCR'd PDFs carry noise (e.g. `Ibn Sinii` for Ibn Sīnā). Correct obvious OCR errors in quotes, but don't paraphrase inside quotation marks.
