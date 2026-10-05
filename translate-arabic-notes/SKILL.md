---
name: translate-arabic-notes
description: Translate Arabic lecture notes (or any Arabic study notes — Markdown, text, Word, PDF, or scanned pages) into a faithful, complete English Markdown file saved beside the original. Use when asked to translate Arabic notes, lecture notes, or dars notes into English.
---

# Translate Arabic notes

The output is a **faithful translation**: every line of the source rendered in English, nothing summarized, nothing added. The original file is never modified.

## Steps

1. **Get the input.** Take the path(s) given. If the project has its own rules about where files go or what frontmatter a file needs (its `CLAUDE.md`), read them now; they override the defaults below.
2. **Read the whole source.**
   - `.md`, `.txt`: read directly.
   - `.docx`: convert first with `textutil -convert txt -stdout <file>` (macOS) or `pandoc <file> -t markdown`.
   - `.pdf`, images, scans: read them page by page with the Read tool (PDFs in chunks of up to 20 pages).
   - Done when you can say how many pages or sections the source has.
3. **Ask only what you can't infer.** If the lecture's title, teacher, or date are in the notes or the filename, use them; otherwise ask the user once, in one message. Don't guess them.
4. **Translate section by section, in source order**, following *Translation rules* below. For long sources, write the output file incrementally, section by section, so nothing is dropped.
5. **Save** as `<original-name>.en.md` in the same folder as the original, unless the user or project rules say otherwise. Never overwrite an existing file — append `-2`, `-3`, and so on.
6. **Check completeness.** Compare source and translation: the same number of headings, numbered points, and list items, in the same order. Every source section must map to a translated one. Fix any gap before reporting.
7. **Report:** the output path, the number of sections translated, and every `[unclear]` and `[TN]` mark, with its location, so the user can resolve them.

## Translation rules

- **Structure:** keep the source's headings, numbering, lists, tables, and paragraph breaks. Arabic numerals and abjad numbering become 1, 2, 3.
- **Register:** plain, accurate English that follows the teacher's meaning. Where the notes are shorthand or fragments, translate them as fragments and don't expand them into prose.
- **Technical terms:** at first use, transliterate the term and gloss it in parentheses — *mu'tamad (the relied-upon position)* — then use the transliteration alone. Use one spelling throughout the file. Use simple transliteration with no diacritics, ' for hamza and ʿayn (*shari'ah*, *da'if*).
- **Qur'an:** translate the verse and give its reference, *(al-Baqarah 2:255)*. If the notes cite a verse without its words, keep it as a reference only; don't supply the text.
- **Hadith and quotations:** translate what is written. Keep any grading, collection, or narrator chain exactly as the notes give it, and add none.
- **Honorifics:** render ﷺ, صلى الله عليه وسلم and similar formulas after the Prophet's name as ﷺ. Render رضي الله عنه as *(may Allah be pleased with him)*, رحمه الله as *(may Allah have mercy on him)*, and so on for the others.
- **Uncertainty:** illegible or ambiguous words become `[unclear: <Arabic as written>]`, with your best reading after it if you have one: `[unclear: الحكم — possibly "the ruling"]`.
- **Translator's notes:** anything that isn't translation — a glossed abbreviation, a note that a term has several possible meanings — goes in `[TN: …]`, kept short.
- **Fidelity:** content outside the source appears only inside `[TN: …]`. If the notes seem to contain an error, translate it as written and flag it with a `[TN]`.

## Output header

Start the file with this header, unless project rules require a different one:

```markdown
# <Lecture title> — English translation

- Source: <original filename>
- Teacher: <name, if known>
- Date: <date, if known>
- Translated: <YYYY-MM-DD>, machine translation, unreviewed
```
