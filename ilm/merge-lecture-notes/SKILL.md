---
name: merge-lecture-notes
description: Combine the full text of several lecture-note files into one Markdown document, in lecture order, word for word, with a contents list. Use when asked to merge, combine, or compile multiple lecture notes or a lecture series into a single document.
---

# Merge lecture notes

The output holds the **full text** of every lecture, copied **verbatim** — nothing summarized, edited, deduplicated, or reworded. The copy is done by `scripts/merge.py`, never retyped, so the wording survives byte for byte. Input files are never modified.

## Steps

1. **Collect the inputs:** the paths, folder, or glob the user gave. If the project has its own rules about where files go or what frontmatter a file needs (its `CLAUDE.md`), read them now; they override the defaults below.
2. **Get every input into Markdown or text.** The script reads `.md` and `.txt` only.
   - `.docx`: `textutil -convert txt -output <tmp>.txt <file>` (macOS) or `pandoc <file> -o <tmp>.md`.
   - `.pdf` or scans: extract the text into a temporary `.md` in the scratchpad, word for word, before merging.
   - Arabic notes that should be merged in English: translate each with the `translate-arabic-notes` skill first, then merge the `.en.md` files.
3. **Fix the order.** Default: lecture number, then date, from frontmatter or filename (`lecture-03`, `2026-09-14`…). If any two files could go either way, show the user the proposed order and wait for confirmation. Done when the order is unambiguous or confirmed.
4. **Choose the title and output path.** Default title: the series name if the files share one, otherwise ask. Default path: `<series-slug>-combined.md` beside the inputs. Never overwrite an existing file.
5. **Run the script** with the inputs in order:

   ```
   python3 <this-skill-dir>/scripts/merge.py --title "<title>" --out <path> <file1> <file2> …
   ```

   It strips each file's frontmatter and turns its `title`, `date`, and `speaker`/`teacher`/`author` fields into the section heading. It moves each lecture's headings down two levels (# becomes ###) so they nest under that section, writes a contents list, and prints a word count per lecture.
6. **Check:** the script exits non-zero if any lecture's word count in the output doesn't match its input. Fix the cause and re-run. Then open the output and check that the first and last lines of each lecture are present.
7. **Report:** the output path, the lectures in order with their word counts, and any input you converted or translated on the way.

## Output shape

```markdown
# <Title>

## Contents
1. Lecture 1 — <title>
…

## Lecture 1 — <title>
*<date> · <speaker> · source: <filename>*

<full text, headings shifted down two levels>
```
