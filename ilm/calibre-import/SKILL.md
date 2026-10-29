---
name: calibre-import
description: Import the books waiting in the user's library inbox (/Users/viz1er/Workspace/library-inbox) into their Calibre library — identifies each file's real title, authors, language and genre from its title page, checks the library for duplicates, shows a metadata table for approval, then adds the books through calibredb and files the originals away. Use when asked to "process my inbox", import, add, or organize new books into Calibre.
---

# Calibre import

Move every book in `/Users/viz1er/Workspace/library-inbox/` into the Calibre library with
clean metadata. The paths and the metadata rules (titles, author spelling, the
fixed genre-tag list) are in `/Users/viz1er/Workspace/library-inbox/CLAUDE.md`. Read that
file first and follow it. Every write goes through `calibredb`. Never edit
`metadata.db` or the library folders by hand.

```sh
CDB=/Applications/calibre.app/Contents/MacOS/calibredb
LIB="/Users/viz1er/Ismail's Library"
```

## Steps

1. **Scan the inbox.** List the book files (`pdf epub mobi azw3 djvu docx txt`
   and similar), leaving out `_imported/` and dotfiles. Group files that are the
   same book: different formats, plus companion files like `X_djvu.txt`,
   `X_text.pdf` and `X_meta.xml` (CLAUDE.md says what to do with each). If the
   inbox is empty, say so and stop. With more than ~10 books, work in batches of
   10 (steps 2–7 for each batch).
2. **Identify each book.** Run `ebook-meta <file>` (same folder as `$CDB`) for
   the embedded metadata, but don't trust it on its own, since downloads often
   carry junk titles. Confirm against the book itself:
   - Text PDF: `pdftotext -f 1 -l 8 -layout <file> -` to read the title page,
     copyright page and contents. Get the page count from `pdfinfo`.
   - EPUB: read the title page and copyright page from the unzipped XHTML.
   - Scanned PDF (no text from pdftotext): render the first few pages with
     `pdftoppm -r 80 -f 1 -l 6 -png <file> <scratch>/p` and read the images.
     For an Arabic scan, the title page (صفحة العنوان) and the publisher page
     are usually within the first 4 pages.
   - If there's an `X_meta.xml`, read its title, creator and date as hints.

   Besides the title and authors, look for: the muhaqqiq or editor (تحقيق،
   حققه، اعتنى به، edited by), the edition (الطبعة), the Hijri and Gregorian
   years, the publisher and place, and the author's death date (المتوفى سنة).
   The death date is often on the title page or in the muhaqqiq's
   introduction.
3. **Check for duplicates.** This step works while Calibre is open:
   `uv run ~/.claude/skills/calibre-lookup/scripts/lookup.py find "<distinctive title words>"`,
   and run it again with the author's surname. Also check the author's existing
   spelling: `sqlite3 "file:$LIB/metadata.db?mode=ro" "select name from authors where name like '%<surname>%'"`.
4. **Propose.** Show one table: file(s) → title, authors, editor, edition,
   year (Gregorian/Hijri), author's death date, tag(s), language, series,
   publisher, with `?` on any value you inferred, plus a **Status** column (`new`, `add format to #id`,
   `possible duplicate of #id`, or `skip: not a book`). Put the descriptions
   under the table. **Wait for the user's approval or corrections.** Don't
   import anything before that.
5. **Check that Calibre is closed.** `pgrep -x calibre`. If it's running, ask
   the user to quit Calibre, because calibredb refuses to write while the GUI
   is open. Then check the custom columns with
   `"$CDB" custom_columns --with-library "$LIB"`. Create any of these that are
   missing (the user has already approved them):
   ```sh
   "$CDB" add_custom_column --with-library "$LIB" --is-multiple --display '{"is_names": true}' editor Editor text
   "$CDB" add_custom_column --with-library "$LIB" edition Edition text
   "$CDB" add_custom_column --with-library "$LIB" hijri "Hijri Year" text
   ```
6. **Import.** For each approved book:
   - New book: `"$CDB" add --with-library "$LIB" -t "<title>" -a "<a1> & <a2>" -T "<tags>" -l <langs> [-s "<series>" -S <n>] [-i <isbn>] "<file>"`.
     Read the new id from the `Added book ids:` line. If calibredb reports it
     as a duplicate and skips it, stop and ask; don't pass `-d` unless the user
     says to.
   - More formats of the same book: `"$CDB" add_format --with-library "$LIB" <id> "<file>"`.
   - The remaining fields: `"$CDB" set_metadata --with-library "$LIB" <id> -f publisher:"…" -f pubdate:<YYYY>-01-01 -f comments:"…" -f '#pages:<n>' -f '#editor:<a> & <b>' -f '#edition:<…>' -f '#hijri:<YYYY>'`.
     Leave out any field with no value. Don't write `?` into Calibre: use the
     value the user approved, and list anything still uncertain in the report.
   - Verify: `"$CDB" list --with-library "$LIB" -s id:<id> -f 'title,authors,tags,languages,formats,#editor,#edition,#hijri'`.
7. **File the originals.** Move each imported book's files (never copy them,
   never delete them) to `_imported/<YYYY-MM-DD>/`, including companion files
   that weren't imported, and keep any subfolder name. Leave skipped
   and unresolved files in the inbox.
8. **Log and report.** Append a dated section to `import-log.md` with one line
   per book (`#id · title · author · tag`) and one line per file left behind,
   with the reason. Then give the user the same summary, and remind them they
   can reopen Calibre.

## Notes

- Calibre may pull metadata from the file and override `-t`/`-a` when they're
  missing, so always pass the title and authors explicitly.
- Multiple authors are separated with ` & `. Calibre builds `author_sort`
  itself.
- If a file is corrupt or calibredb errors out, leave it in the inbox, report
  the error text, and carry on with the rest.
