# skills

A collection of [Claude Skills](https://docs.claude.com/en/docs/claude-code/skills) — picked up from other repos or written from scratch.

## Skills

| Skill | What it does | Source |
| --- | --- | --- |
| [excalidraw-diagram](excalidraw-diagram) | Generates `.excalidraw` diagram JSON that argues visually, with a Playwright render loop for self-validation | [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) |
| [idea-validator](idea-validator) | Stress-tests a SaaS or AI-consulting idea — market, moats, MVP timeline, earning potential — in blunt operator voice | own |
| [mattpocock/](mattpocock) *(37 skills)* | Matt Pocock's full collection — TDD, code review, debugging, domain modelling, writing workflows, TypeScript setup | [mattpocock/skills](https://github.com/mattpocock/skills) |

Full provenance for imported skills (upstream repo, license, import date, whether it's been forked) lives in [SOURCES.md](SOURCES.md).

## Structure

Each skill is a folder at the repo root containing a `SKILL.md` (plus any supporting files it needs):

```
.
├── some-skill/
│   └── SKILL.md
├── another-skill/
│   ├── SKILL.md
│   └── references/
└── mattpocock/          # an imported collection, kept together under its author
    ├── tdd/
    │   └── SKILL.md
    └── ...
```

Flat at the root — no `skills/` wrapper, no `own/` vs `vendored/` split; ownership is tracked in `SOURCES.md`, not in the directory tree. That way the repo itself is a skills directory. The one exception is `mattpocock/`, a whole upstream collection kept in its own folder so the 37 skills stay identifiable as his.

## Adding a skill

- **From elsewhere:** copy the folder to the repo root unmodified, add a row to the table above with the source repo, and add an entry to [SOURCES.md](SOURCES.md).
- **New:** create `<name>/SKILL.md` describing what it does and when to use it, and add a row above with `own`.

See [CLAUDE.md](CLAUDE.md) for the full rules an agent should follow when adding, importing, or forking a skill.

## Using these skills

Symlink or copy the ones you want into a project's `.claude/skills/` directory, or point your Claude Code config at this repo.
