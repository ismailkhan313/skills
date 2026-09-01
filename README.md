# skills

A collection of [Claude Skills](https://docs.claude.com/en/docs/claude-code/skills) — picked up from other repos or written from scratch.

## Structure

Each skill is a folder in the repo root containing a `SKILL.md` (plus any supporting files it needs):

```
skills/
├── some-skill/
│   └── SKILL.md
├── another-skill/
│   └── SKILL.md
└── ...
```

Flat for now — will organize into categories (personal, entrepreneurship, coding, architecture, writing, ...) once there's enough of a collection to make that useful.

## Adding a skill

- **From elsewhere:** copy the skill folder in, and add a row to [Sources](#sources) below.
- **New:** create a folder with a `SKILL.md` describing what it does and when to use it.

## Sources

Skills copied in from elsewhere, and where they came from:

| Skill | Source |
| --- | --- |
| [excalidraw-diagram](excalidraw-diagram) | [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) |

## Using these skills

Symlink or copy the ones you want into a project's `.claude/skills/` directory, or point your Claude Code config at this repo.
