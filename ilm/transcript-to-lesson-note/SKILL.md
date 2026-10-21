---
name: transcript-to-lesson-note
description: Turn a raw course or video lecture transcript (.txt, .md, .srt/.vtt, auto-captions) into a readable Obsidian lesson note — headings, bullet points and lists, Arabic terminology in callouts, and a summary of the main concepts — for rereading and refreshing later. Use whenever the user wants a transcript, lecture, class recording, dars or lesson "written up", "turned into notes", "made readable" or "converted to a lesson note", including a whole course folder of transcripts, even if they don't say "skill" or "lesson note".
---

# Transcript to lesson note

The note is for **rereading once a year to refresh the memory**, not for exam revision. It should read like a clean, well-organized record of what the teacher taught: the gist first, then every point in the lecture's own order, easy to skim. So: no questions, flashcards, quizzes, "test yourself" or "reflection" sections.

The note keeps **everything taught**: each point, definition, example, story, condition, difference of opinion and cited source. It drops only what carries no content: filler, repetition, small talk, technical trouble, admin and attendance. If you're unsure whether something is content, keep it.

## Steps

1. **Read the project rules.** In a vault with a `CLAUDE.md`/`README.md`, read them first; they decide links, frontmatter, folders and callouts, and override the defaults here.
2. **Collect the inputs.** One note per transcript file. If a folder holds both part files (`1.1`, `1.2`…) and merged lessons (`Concatenated_Lessons/`, `Lesson_1_Complete`), ask which to use. Convert `.srt`/`.vtt` to plain text first (drop timestamps and cue numbers).
3. **Learn the course's conventions from sibling lesson notes** (same course folder, `type: lesson-note`): frontmatter keys and values (`source`, `term`, tags such as `text/…`, `course/…`), filename pattern (e.g. `01-2 <Title>.md`), and transliteration style. Copy them. If there are no siblings, ask the user once for `source`, `term` and the `text/` tag, and use them for the whole batch.
4. **Read the whole transcript before writing.** Work out the lecture's real structure: its topics and subtopics, in order. Transcripts are often auto-generated, so names and Arabic come out garbled ("Prophery" = Porphyry, "Isagوج" = Īsāghūjī/Isagoge, "rahimahullah" run together). Fix mis-hearings you're confident of from context, silently. When unsure, write your best reading followed by `(?)`.
   - **Only what the lecture says.** Don't complete a list, add a ḥadīth, date, name or book, or fill a gap from your own knowledge, even when you're sure it's right. If the teacher names three of the six books, the note names three. A year from now the user needs to trust that every line came from this class.
   - **Correcting a word is silent; correcting the teacher is not.** If the teacher seems to have the facts wrong (who wrote what, a date, a ruling), or a vault note disagrees, keep the teacher's version and add a visible bullet beneath it: `- *Note:* Salem's preface ([[01 Translators Preface]]) attributes this to al-Abharī.`
5. **Write the note** in the shape below.
6. **Link.** Search the vault for notes on the main texts, scholars and concepts the lecture names, and wikilink the first mention when a note exists. Don't link to notes that don't exist.
7. **Save** beside the sibling lesson notes in the course folder, never beside the transcripts (in ilm-vault they live in a separate `98 Sources/Transcripts/<course path>/`), named after the sibling pattern with a title that states the lesson's main topic. Never overwrite an existing file; if one exists, tell the user and save under a new name.
8. **Check.** If the vault has a link checker (e.g. `python3 .claude/scripts/vault.py check`), run it; the unresolved-link count must not go up. Then reread the transcript against the note section by section and add anything taught that is missing.
9. **Report** each note's path, its sections, and any `(?)` readings the user may want to confirm.

## Note shape

```markdown
---
<frontmatter copied from siblings: created (today), type: lesson-note, source, term, tags>
---
> [!summary] Main concepts
> - <3–7 bullets: the lesson's main ideas, each a full sentence that stands on its own>

## <First topic, as the teacher framed it>

- <point>
  - <supporting detail, example, or reason>
- <point>

> [!term] Manṭiq — مَنْطِق
> Logic; literally "articulate speech". Technically: a tool (*āla*) that guards the mind from error in thinking.

1. <steps, conditions, categories or anything else the teacher counted out>

## <Next topic>
…
```

### How to write it

- **Headings follow the lecture.** `##` for each main topic, `###` for subtopics. Name them by content ("Why the Ḥanafī school spread in Kufa"), not "Part 2" or "Introduction to the lecture".
- **Bullets, not paragraphs.** One idea per bullet, nested for detail, and short complete sentences. Use a numbered list when the teacher counts things out (conditions, pillars, categories, stages, steps), and a table when comparing positions across schools, scholars or opinions. Bold only the key phrase in a bullet, not whole sentences.
- **Attribute.** Say whose view a point is: "Abū Ḥanīfa holds…", "the teacher's view…", "al-Ṭaḥāwī reports…". Where the lecture gives differing views, give each with its holder.
- **Keep examples and stories.** They are what jogs the memory a year later. Give each a bullet, e.g. `- *Example:* …` or `- *Story:* …`.
- **Don't narrate the lecture.** Write the content itself ("Logic is a tool…") rather than "The speaker then explains that…". Leave out meta-notes such as "no Qurʾān verses were quoted".

### Arabic

- **`[!term]` callout:** for each technical term the teacher explains in any way (defines it, glosses it, gives its literal meaning or root, or contrasts it with another term), at the point where it is first taught. A typical lecture has several, so one callout for a whole lecture usually means terms were missed. The title is the transliteration, an em dash, then the Arabic script. The body gives the meaning: the literal sense if one is given, then the technical sense as this teacher defined it. Later mentions of the term are just italic transliteration (*manṭiq*).
- **Passing mentions:** a term that is only used, not explained, gets italic transliteration only, with no callout. This keeps the note from turning into a wall of callouts.
- **`[!arabic]` callout:** Arabic passages such as Qurʾān, ḥadīth, lines of the *matn*, poetry and duʿāʾ go in this callout, Arabic only (the vault styles it right-to-left with a hidden title). Put the English translation as a normal line or bullet directly below it, with the reference (e.g. *al-Baqara 2:255*).
- **Accuracy:** reproduce Arabic script only when you are certain of it, e.g. the Qurʾān, well-known ḥadīth or standard terms. If the transcript garbles a passage you can't identify with certainty, give its sense in English, mark it `(?)`, and don't make up Arabic text.
- **Transliteration:** match the sibling notes' style. Default: full diacritics (ḥ, ṣ, ā, ʿ, ʾ).
- **Quotations** from scholars or books, given in English, go in `> [!cite] <who / which book>`.
