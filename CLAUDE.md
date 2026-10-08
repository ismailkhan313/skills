# CLAUDE.md — Skills Repository Guide

This repo holds Claude Agent Skills: some I wrote myself, some pulled in from
other repos. This file tells any agent working in this repo how it's
organized and what to do when adding, editing, or importing a skill.

## Structure

```
skills-repo/
├── CLAUDE.md          # this file
├── README.md           # human index: table of all skills, one row each
├── SOURCES.md           # provenance log for every imported/forked skill
├── <skill-name>/
│   ├── SKILL.md         # required — frontmatter + instructions
│   ├── scripts/          # optional — executable code the skill runs
│   ├── references/        # optional — docs loaded on demand
│   └── assets/             # optional — templates, static files
├── <another-skill>/
├── ilm/                # own skills for one area of work (Islamic studies and metaphysics research)
│   ├── calibre-to-markdown/
│   └── ...
└── mattpocock/         # an imported collection, kept together under its author
    ├── tdd/
    │   └── SKILL.md
    └── ...
```

Skills are **flat at the repo root** — no `skills/` wrapper, and no `own/`
vs `vendored/` subfolders. Ownership is tracked in `SOURCES.md`, not in the
directory tree, so the repo root can be pointed at directly as a skills
directory — the Skill tool scans one directory for folders containing a
`SKILL.md`.

Two kinds of folder may group skills one level down:

- **An imported collection**, e.g. `mattpocock/`: a whole upstream collection,
  kept in its own folder so its 37 skills stay identifiable as his.
- **An area of my own work**, e.g. `ilm/`: my own skills for Islamic studies
  and metaphysics research (sources, translation, lecture notes). A new skill
  for that work goes in `ilm/<skill-name>/`.

Never nest a folder for a single skill, and never nest more than one level.
Skills inside a group folder aren't found by tools that scan only the repo
root, so each one is linked into `~/.claude/skills/` individually.

## The SKILL.md format (Agent Skills spec)

Every skill folder needs a `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: What this skill does and when to use it. Be specific — this is
  the only thing read at startup, before the skill is activated.
license: MIT          # optional
---

Instructions the agent follows once this skill is active.
```

Rules an agent must follow when creating or renaming a skill:

- `name` is lowercase letters, numbers, and hyphens only. No leading/trailing
  hyphen, no consecutive hyphens. Max 64 characters.
- `name` **must exactly match the parent folder name**.
- `description` must state both what the skill does and when to use it —
  this is what triggers activation, so be concrete and keyword-rich rather
  than vague ("Helps with PDFs" is a bad description).
- Keep `SKILL.md` under ~500 lines. Move detailed material into
  `references/` and link to it — skills load progressively (metadata first,
  full body on activation, `references/`/`scripts/`/`assets/` only as
  needed). Don't front-load everything into one file.
- Reference other files with relative paths, one level deep from
  `SKILL.md` (e.g. `references/FORMS.md`), not nested reference chains.

## When adding a skill I wrote myself

1. Create `<skill-name>/SKILL.md` at the repo root, following the format above.
2. Add one row to `README.md`'s skill table: name, one-line purpose,
   `source: own`.
3. Do **not** add an entry to `SOURCES.md` — that file is only for skills
   that originated elsewhere.

## When importing a skill from another repo

1. Copy the skill folder to the repo root as-is, unmodified. An entire
   upstream collection goes into one folder named for its author or repo
   (see `mattpocock/`).
2. If the name collides with an existing skill, rename the folder to
   prefix the source (e.g. `acme-pdf-tools` instead of `pdf-tools`), and
   update `name:` in its frontmatter to match — `name` must equal the
   folder name.
3. Add an entry to `SOURCES.md`:

   ```markdown
   ## <skill-name>
   Source: <repo URL>
   Commit/tag: <commit hash if known>
   License: <license>
   Imported: <YYYY-MM-DD>
   Modified: no
   ```

4. Add a row to `README.md`'s table with `source: <origin repo name>`.
5. Do not edit the imported skill's content in this step — a straight
   import stays byte-for-byte importable so it can be diffed against
   upstream later if it's updated.

## When modifying an imported skill

1. Edit the skill in place — there's no separate "forked" folder.
2. Update its `SOURCES.md` entry: set `Modified: yes`, and add a line
   describing what changed and why.
3. Leave the original `Source:` and `License:` lines intact — the fork
   still owes attribution to where it came from.

## Before finishing any skill work

- Validate frontmatter: `skills-ref validate ./<skill-name>` if the
  `skills-ref` CLI is available.
- Confirm `SOURCES.md` and `README.md` are updated for any skill that was
  imported, renamed, or forked in this session — these are the only record
  of provenance, so an agent should never leave them out of sync with
  what's actually on disk.