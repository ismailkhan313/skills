# skills

A collection of [Claude Skills](https://docs.claude.com/en/docs/claude-code/skills) — picked up from other repos or written from scratch.

## Skills

| Skill | What it does | Source |
| --- | --- | --- |
| [ask-matt](skills/ask-matt) | Ask which skill or flow fits your situation. A router over the skills in this repo. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [claude-handoff](skills/claude-handoff) | Hand the current conversation off to a fresh background agent that picks up the work immediately. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [code-review](skills/code-review) | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow thi… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [codebase-design](skills/codebase-design) | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [diagnosing-bugs](skills/diagnosing-bugs) | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [domain-modeling](skills/domain-modeling) | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recor… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [excalidraw-diagram](skills/excalidraw-diagram) | Create Excalidraw diagram JSON files that make visual arguments. Use when the user wants to visualize workflows, architectures… | [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) |
| [git-guardrails-claude-code](skills/git-guardrails-claude-code) | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [grill-me](skills/grill-me) | A relentless interview to sharpen a plan or design. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [grill-with-docs](skills/grill-with-docs) | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [grilling](skills/grilling) | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [handoff](skills/handoff) | Compact the current conversation into a handoff document for another agent to pick up. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [idea-validator](skills/idea-validator) | Validate a SaaS app idea or AI consulting pitch with market research, viability, moats, MVP timeline, and earning potential, de… | own |
| [implement](skills/implement) | Implement a piece of work based on a spec or set of tickets. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [implement-spec](skills/implement-spec) | Implement a specification in code. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [improve-codebase-architecture](skills/improve-codebase-architecture) | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [loop-me](skills/loop-me) | Grill me about specs for the workflows I want to build, within this workspace. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [migrate-to-shoehorn](skills/migrate-to-shoehorn) | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [prototype](skills/prototype) | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [research](skills/research) | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [resolving-merge-conflicts](skills/resolving-merge-conflicts) | Use when you need to resolve an in-progress git merge/rebase conflict. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [retro](skills/retro) | Conduct a retrospective on a coding session. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [scaffold-exercises](skills/scaffold-exercises) | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [setup-matt-pocock-skills](skills/setup-matt-pocock-skills) | Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run o… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [setup-pre-commit](skills/setup-pre-commit) | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [setup-ts-deep-modules](skills/setup-ts-deep-modules) | Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and r… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [tdd](skills/tdd) | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wa… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [teach](skills/teach) | Teach the user a new skill or concept, within this workspace. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [to-questionnaire](skills/to-questionnaire) | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [to-spec](skills/to-spec) | Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [to-tickets](skills/to-tickets) | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, publish… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [triage](skills/triage) | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-read… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [wait-what](skills/wait-what) | Stop. That last message did not land: re-pitch it. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [wayfinder](skills/wayfinder) | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [wizard](skills/wizard) | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructur… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [writing-beats](skills/writing-beats) | Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [writing-for-agents](skills/writing-for-agents) | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [writing-fragments](skills/writing-fragments) | Writing, explore: mine raw fragments, no structure yet. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [writing-shape](skills/writing-shape) | Writing, exploit: shape raw material into an article, paragraph by paragraph. | [mattpocock/skills](https://github.com/mattpocock/skills) |

Full provenance for imported skills (upstream repo, license, import date, whether it's been forked) lives in [SOURCES.md](SOURCES.md).

## Structure

Each skill is a folder under `skills/` containing a `SKILL.md` (plus any supporting files it needs):

```
skills/
├── some-skill/
│   └── SKILL.md
├── another-skill/
│   ├── SKILL.md
│   └── references/
└── ...
```

Flat under `skills/` — no `own/` vs `vendored/` split, and no per-author folders. Ownership is tracked in `SOURCES.md`, not in the directory tree; this is also what the Skill tool expects, since it scans one directory for folders containing a `SKILL.md`.

## Adding a skill

- **From elsewhere:** copy the folder into `skills/` unmodified, add a row to the table above with the source repo, and add an entry to [SOURCES.md](SOURCES.md).
- **New:** create `skills/<name>/SKILL.md` describing what it does and when to use it, and add a row above with `own`.

See [CLAUDE.md](CLAUDE.md) for the full rules an agent should follow when adding, importing, or forking a skill.

## Using these skills

Symlink or copy the ones you want into a project's `.claude/skills/` directory, or point your Claude Code config at this repo.
