---
name: calibre-to-markdown
description: Convert a book from the user's Calibre library — text PDF, scanned PDF (Arabic or English), or EPUB — into one Markdown file of the entire book with clear chapter headings and page markers, small enough to keep instead of the PDF. Use when asked to convert, extract, or digitize a Calibre book, PDF, or book scan into Markdown.
---

# Calibre book to Markdown

The output is the **entire book** as one `.md` file: every page's text in order, chapters as headings, and a `<!-- page N -->` marker at the top of each PDF page so passages can be cited by page. The original stays in Calibre; the file's frontmatter records its Calibre id and SHA-256, so the `.md` can stand in for the PDF anywhere you store sources.

All work goes through `scripts/book2md.py` (run it with `uv run`; it pulls in PyMuPDF). It opens the Calibre library **read-only** and never writes to it. Its `--help` lists every option.

## Steps

1. **Find the book.** Run `uv run scripts/book2md.py find "<title or author words>"`. If more than one result could be the book, show the user the candidates (id, title, formats, language) and let them choose.
2. **Choose the output path.** If the project has rules about where sources go (its `CLAUDE.md` — e.g. an inbox folder for raw material), follow them. Otherwise use the folder the user named, or the current directory. Name the file `<author>-<short-title>.md`, lowercase ASCII with hyphens, transliterating Arabic simply.
3. **Probe:** `uv run scripts/book2md.py probe <id> --dir <scratch>/probe`. It reports page count, outline (bookmarks), text-layer coverage, garbled-text signals, and a recommendation, and it renders two sample pages. **Read both sample images** and compare them with `sample_text`. Done when you can name the engine:

   | What the probe shows | Engine |
   | --- | --- |
   | EPUB | `convert --engine text` (preferred whenever Calibre has an EPUB) |
   | Text layer matching the page images | `convert --engine text` |
   | Latin-script scan, or a garbled Latin text layer | `convert --engine tesseract` |
   | Arabic scan, or a garbled Arabic text layer | **vision** (step 5) |

   If the probe warns about **lam-alef swaps**, the Arabic in that text layer is corrupt (الله comes out as هللا). The Latin text is still fine. Tell the user, and offer vision for the pages where the Arabic matters.
4. **Text or tesseract:** for tesseract, first run a trial on 3 pages (`--pages 30-32`) and compare it with the page images. If it's poor, use vision instead. Then run the full conversion:

   ```
   uv run scripts/book2md.py convert <id> --engine text|tesseract --out <path> [--lang eng|ara|ara+eng]
   ```

   Tesseract takes about 1.5 s per page. For books over 100 pages, run it in the background.
5. **Vision** (Arabic scans and garbled PDFs):
   1. Estimate the cost: about 3k tokens per page. For books over 50 pages, give the user the page count and the estimate, and **wait for a go-ahead**.
   2. Render the pages into a scratch work folder, outside the project: `uv run scripts/book2md.py render <id> --dir <work>`.
   3. Transcribe every page following [references/vision-transcription.md](references/vision-transcription.md). It covers batching across subagents and the page-file format.
   4. Build the file: `uv run scripts/book2md.py assemble --dir <work> --out <path>`. It refuses if any page file is missing.
6. **Check the result** against the JSON summary the script prints:
   - **Empty pages:** look at each one's image. Confirm it's truly blank or an image, or else re-transcribe it.
   - **Spot check:** render 3 pages spread across the book (`render --pages N --dir <scratch>`). Compare each image with the text under its `<!-- page N -->` marker. Look for missing paragraphs, wrong order, and garbled words.
   - **Chapters:** read the full heading list (`grep '^#' <out>`). When `chapters_from` is a heuristic or `none`, fix the **markup only**: put `##` in front of real chapter titles and `###` in front of sections, and remove the `#` from false headings. Leave the words of the book untouched. Done when the heading list reads as the book's table of contents.
7. **Report:** the output path, the method, the size before and after, page and word counts, the chapter list, the spot-check results, and any warnings (lam-alef swaps, the number of `[illegible]` and `[uncertain]` marks, pages left blank).

## Notes

- `<!-- page N -->` is the PDF page number, which is reliable. The `printed P` beside it is a best-effort reading of the number printed on the page. When citing, prefer the printed number where it exists and check it against the page image.
- Images are dropped. Tables come through as plain text.
- To convert several books, run the steps once per book.
