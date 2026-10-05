# Vision transcription

Used when a book is an Arabic scan or has a garbled text layer. You — or subagents you dispatch — read each rendered page image and write its text. The output is a **diplomatic transcription**: the page's words exactly as printed, in reading order.

## Batching

- `render` writes `page-0001.png` … into the work folder, plus `manifest.json`.
- Split the pages into batches of about 20. Give each batch to a subagent with the Agent tool, and run up to 4 at a time. Give each subagent: the work folder, its page range, and this file's path. Its job is to write `page-NNNN.md` for each page in its range.
- Before reporting, a subagent confirms that every page in its range has a file. It reports any page it couldn't read in full.
- Pages that already have a `page-NNNN.md` are done. Skip them, so an interrupted run can resume.

## Writing one page file — `page-NNNN.md`

1. **Printed page number:** if the page shows one (often in the header, e.g. `( ١١ )`), the first line of the file is `printed: ١١`, written as printed. Otherwise, leave that line out.
2. **Leave out** running headers (book title or chapter name repeated at the top), the page number, decorative rules and borders, and printer's marks.
3. **Body text:** transcribe every word in reading order (right to left for Arabic). Join the lines of a paragraph into one line, and leave a blank line between paragraphs.
   - Keep spelling and orthography exactly as printed: ى/ي, ه/ة, missing hamzas, old-style spellings. Correct nothing.
   - Write diacritics only where printed.
   - Write honorific formulas as printed: write صلى الله عليه وسلم out in full if it is written out, and use the ligature ﷺ only if the page uses it.
4. **Headings:** section starts that are visually set apart (larger, bold, centred, ornamented, or a word such as فصل, باب, كتاب, or مسألة standing at the head of a section) become Markdown headings. Use `##` for a كتاب or chapter, `###` for a باب or فصل, and `####` for anything below that. Keep the heading's words exactly as printed, without the ornaments (﴿ ﴾, ❁, *).
5. **Qur'an:** transcribe the verses as printed, inside their ornate brackets if the page uses them.
6. **Footnotes:** after the body, add a line `---`, then each footnote as printed, starting with its marker, e.g. `(١) …`.
7. **Unreadable text:** `[illegible]` for a word, `[illegible: N lines]` for more. If you have a likely reading, put it in: `[uncertain: الكبائر]`.
8. **Blank or image-only pages:** leave the file empty, or write a one-line description in square brackets: `[blank]`, `[image: title page ornament]`.

Write only what is on the page: no commentary, translation, summary, or expanded abbreviations.
