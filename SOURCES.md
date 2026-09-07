# SOURCES

Provenance for every skill in this repo that originated somewhere else.

Skills written from scratch are **not** listed here — absence from this file
means "mine". The `README.md` table is the human-facing index; this file is the
record of where imported skills came from, what license they carry, and whether
they've been forked since import.

Format for each entry:

```markdown
## <skill-name>
Source: <repo URL>
Commit/tag: <commit hash or tag, if known>
License: <license>
Imported: <YYYY-MM-DD>
Modified: no | yes
```

When `Modified: yes`, add a `Changes:` list under it describing what was
changed and why. Never remove or rewrite `Source:` / `License:` — a fork still
owes attribution upstream.

---

## mattpocock/ (37 skills)
Source: https://github.com/mattpocock/skills
Commit/tag: 3cca18b368ae95cdbdebbff572ccafa662551015 (upstream `HEAD` at import time)
License: not stated upstream (no LICENSE file in the source repo as imported)
Imported: 2026-09-07
Modified: no

Installed with `npx skills@latest add mattpocock/skills -a claude-code -s '*' -y --copy`
(`--copy` so real files land in the repo rather than symlinks into `node_modules`),
then moved from the tool's `.claude/skills/` output into `mattpocock/`.

Unlike every other entry here, this is a **nested collection**: the 37 skill
folders live one level deeper, under `mattpocock/<skill-name>/`, to keep the
whole set identifiable as his. Every other skill is a folder at the repo root.

Upstream groups these into `skills/engineering/`, `skills/writing/`,
`skills/in-progress/` etc.; the installer flattens that grouping away, so
`skills-lock.json` from the install (kept out of this repo) is the only record of
each skill's original upstream path.

The 37 skills:

- `ask-matt` — Ask which skill or flow fits your situation. A router over the skills in this repo.
- `claude-handoff` — Hand the current conversation off to a fresh background agent that picks up the work immediately.
- `code-review` — Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does…
- `codebase-design` — Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's inter…
- `diagnosing-bugs` — Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", o…
- `domain-modeling` — Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a…
- `git-guardrails-claude-code` — Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) befor…
- `grill-me` — A relentless interview to sharpen a plan or design.
- `grill-with-docs` — A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
- `grilling` — Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their t…
- `handoff` — Compact the current conversation into a handoff document for another agent to pick up.
- `implement` — Implement a piece of work based on a spec or set of tickets.
- `implement-spec` — Implement a specification in code.
- `improve-codebase-architecture` — Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through which…
- `loop-me` — Grill me about specs for the workflows I want to build, within this workspace.
- `migrate-to-shoehorn` — Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn…
- `prototype` — Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a…
- `research` — Investigate a question against high-trust primary sources and capture the findings as a Markdown file in th…
- `resolving-merge-conflicts` — Use when you need to resolve an in-progress git merge/rebase conflict.
- `retro` — Conduct a retrospective on a coding session.
- `scaffold-exercises` — Create exercise directory structures with sections, problems, solutions, and explainers that pass linting.…
- `setup-matt-pocock-skills` — Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and doma…
- `setup-pre-commit` — Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Us…
- `setup-ts-deep-modules` — Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden…
- `tdd` — Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-gr…
- `teach` — Teach the user a new skill or concept, within this workspace.
- `to-questionnaire` — Turn a decision you can't fully answer into a questionnaire for someone else to fill in.
- `to-spec` — Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just s…
- `to-tickets` — Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blo…
- `triage` — Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed,…
- `wait-what` — Stop. That last message did not land: re-pitch it.
- `wayfinder` — Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on you…
- `wizard` — Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provis…
- `writing-beats` — Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on…
- `writing-for-agents` — Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
- `writing-fragments` — Writing, explore: mine raw fragments, no structure yet.
- `writing-shape` — Writing, exploit: shape raw material into an article, paragraph by paragraph.

---

## excalidraw-diagram
Source: https://github.com/coleam00/excalidraw-diagram-skill
Commit/tag: unknown — imported by copy, upstream ref not recorded at the time
License: not stated upstream (no LICENSE file in the source repo as imported)
Imported: 2026-09-01
Modified: no

Notes: imported as-is, including its own `README.md` (upstream install/setup
instructions) and `references/` render pipeline. Because it is byte-for-byte
upstream, it can still be diffed against the source repo when that repo updates.

---

## Skills written in this repo (no entry needed)

- `idea-validator` — written from scratch, 2026-09-04.
