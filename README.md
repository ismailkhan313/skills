# skills

A collection of [Claude Skills](https://docs.claude.com/en/docs/claude-code/skills) — picked up from other repos or written from scratch.

## Structure

Skills are grouped loosely by category. Each skill is a folder containing a `SKILL.md` (plus any supporting files it needs):

```
skills/
├── personal/
├── entrepreneurship/
├── coding/
├── architecture/
├── writing/
└── ...
```

Categories are just for browsing — add new ones freely as new kinds of skills show up.

## Adding a skill

- **From elsewhere:** copy the skill folder into the right category, and note where it came from (a link in its `SKILL.md` or a short line here) if it's not obvious.
- **New:** create a folder under the relevant category with a `SKILL.md` describing what it does and when to use it.

## Using these skills

Symlink or copy the ones you want into a project's `.claude/skills/` directory, or point your Claude Code config at this repo.
