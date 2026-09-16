Here's an exhaustive catalog, organized by what a refinement agent would actually check. I've tagged each with who acts:

**🤖 Auto** — agent can do it alone (deterministic, low-risk edit or comment)
**👤 Ping assignee/reporter** — needs the person with context
**🧑‍🏫 Ping scrum master / PO** — needs prioritization or process authority

---

## 1. Field hygiene & completeness

- Missing story points on items in the next 1–2 sprints → 🤖 propose estimate as comment, 👤 assignee confirms
- Missing acceptance criteria → 👤 (agent drafts a starter set from the description)
- Missing or empty description (title-only tickets) → 👤
- Missing issue type or wrong type (bug filed as story, task that's really an epic) → 🤖 flag + suggest, 🧑‍🏫 approve bulk changes
- Missing components / labels / team field required by your board config → 🤖 infer from similar past issues, 👤 confirm
- Missing fix version or target release on committed work → 🧑‍🏫
- Missing priority, or priority left at default "Medium" for 90% of backlog → 🧑‍🏫
- Missing epic link / parent → 🤖 suggest best-fit epic by similarity, 🧑‍🏫 confirm
- Missing assignee on items entering the sprint → 🧑‍🏫
- Missing reporter context: no environment, browser, version on bug reports → 👤
- Required custom fields empty (security review flag, compliance tag, cost center) → 👤
- Inconsistent summary formatting (no "As a… I want…", ALL CAPS, ticket IDs in title, trailing "???") → 🤖 normalize
- Placeholder text left in ("TBD", "TODO", "fill this in", "copy from doc") → 👤

## 2. Description & story quality

- Story doesn't follow user-story form or has no stated user value → 👤 (agent drafts rewrite)
- Acceptance criteria present but untestable ("works well", "fast", "intuitive") → 👤
- Acceptance criteria that are actually implementation steps, not outcomes → 👤
- No definition of "done" for non-functional aspects (perf, a11y, analytics, logging) → 👤
- Story contains multiple independent deliverables → 🤖 propose a split into N children, 🧑‍🏫 approve
- Story too small / should be merged into a sibling → 🧑‍🏫
- Ambiguous or conflicting requirements between description and comments → 👤
- Open questions in comments that were never answered → 👤 nudge the asker + asker's target
- Links to design/spec that are dead, private, or point to an outdated Confluence version → 🤖 detect, 👤 replace
- Referenced Confluence page has changed since the ticket was written → 🤖 comment with the diff summary
- Screenshots/attachments referenced in text but not attached → 👤

## 3. Estimation & sizing

- Unestimated items above a rank threshold → 👤
- Estimate wildly outside the team's historical distribution (e.g. 21 points when team max is 8) → 🧑‍🏫 propose split
- Estimate inconsistent with similar completed stories → 🤖 comment with the comparables, 👤 decide
- Re-estimation needed after scope changed post-estimation → 👤
- Items with time tracking but no story points, or vice versa, where your process wants both → 🤖
- Epics with no rolled-up estimate / unestimated children → 🧑‍🏫

## 4. Readiness gating (Definition of Ready)

- Score each candidate story against your DoR checklist → 🤖 post a readiness score + checklist as comment
- Block/label items failing DoR from entering sprint planning → 🤖 apply "not-ready" label
- Items ready but not ranked into a sprint → 🧑‍🏫
- Items pulled into sprint that never passed refinement → 🧑‍🏫
- Generate the refinement-meeting agenda: top N unready items, ordered by rank → 🤖
- Post-meeting: capture decisions from the meeting notes back onto tickets → 🤖 with 👤 verification

## 5. Duplicates, relationships & dependencies

- Near-duplicate issues by title/description similarity → 🤖 propose link "duplicates", 🧑‍🏫 close one
- Same bug reported multiple times by different reporters → 🤖 link, 👤 notify reporters
- Missing "blocks / is blocked by" links inferred from description text ("after X ships…") → 🤖 create link
- Blocked items with no blocker recorded, or blocker already Done → 🤖 unflag / 👤 explain
- Cross-team dependency with no owner on the other side → 🧑‍🏫
- Circular dependency chains → 🧑‍🏫
- Orphaned subtasks whose parent is Done or cancelled → 🤖 flag, 👤 resolve
- Related-but-unlinked work discovered via the same code area or PR → 🤖 suggest link
- Spike with no follow-up implementation ticket after the spike closed → 👤

## 6. Staleness & lifecycle

- No update in N days while in an active status → 👤
- In "In Progress" beyond 2× cycle-time average → 👤 then 🧑‍🏫 escalate
- Created >12 months ago, never ranked, never discussed → 🧑‍🏫 propose archive/close as stale
- Assignee no longer on the team or deactivated → 🧑‍🏫 reassign
- Reporter left the company and no one else has context → 🧑‍🏫
- Items carried over 3+ sprints → 🧑‍🏫 (with the carry-over count in the comment)
- Fix version in the past but issue still open → 🧑‍🏫
- Duplicate-of-a-closed-item that should just be closed → 🤖 propose closure with 7-day objection window
- Backlog size trend / aging histogram per epic → 🤖 report

## 7. Hierarchy & epic integrity

- Epics with no children → 🧑‍🏫
- Epics where all children are Done but epic is still open → 🤖 propose transition
- Epics with no target date, no success metric, or no problem statement → 🧑‍🏫
- Children in a different project/board than the epic → 🤖 flag
- Stories parented to the wrong epic based on content → 🤖 suggest, 🧑‍🏫 approve
- Epics that have grown past a size threshold → 🧑‍🏫 propose split
- Initiative/theme coverage gaps: roadmap item with no backlog representation → 🧑‍🏫

## 8. Bug triage specifics

- New bugs with no severity/priority set → 👤 reporter
- No reproduction steps, or steps that don't include expected vs actual → 👤
- No affected version / environment → 👤
- Bug with no linked failing test or no test-to-add note → 👤
- Bugs open longer than your SLA for their severity → 🧑‍🏫
- Severity inconsistent with described impact (P4 describing data loss) → 🤖 flag, 🧑‍🏫 decide
- Customer-reported bugs missing the support ticket link → 🤖 fetch from linked systems
- Bug clusters in the same component → 🤖 report as a possible tech-debt epic, 🧑‍🏫 decide

## 9. Workflow & data consistency

- Status contradicts reality (Done with open subtasks; In Review with no PR) → 🤖 flag
- Resolution field empty on closed issues → 🤖
- Items in a status not used by your team's workflow anymore → 🧑‍🏫
- Sprint field set but sprint is closed → 🤖
- Flagged/impediment set with no comment explaining it → 👤
- Work logged after issue closure → 👤
- Two people effectively working the same ticket per comments → 🧑‍🏫

## 10. Capacity & planning support

- Sprint candidate list exceeds historical velocity → 🧑‍🏫
- Skill/role imbalance in the proposed sprint (all backend, no QA capacity) → 🧑‍🏫
- One person assigned a disproportionate share → 🧑‍🏫
- Planned work conflicts with known PTO/holidays → 🧑‍🏫
- Unbalanced mix vs. your target ratio of feature / bug / tech-debt / KTLO → 🧑‍🏫
- Committed items that depend on unstarted blockers → 🧑‍🏫

## 11. Meta / process health reporting

- Weekly "backlog health scorecard": % with estimates, % DoR-passing, median age, duplicate count → 🤖
- List of the top 10 tickets most likely to derail the next sprint → 🤖
- Which refinement issues repeat most often (e.g. "AC always missing from Team X") → 🤖 to 🧑‍🏫
- Digest per assignee: "here are your 4 tickets needing input" → 🤖 posts one consolidated comment/DM instead of 4 pings

---

## Design notes

**Ping etiquette matters more than coverage.** The failure mode for this agent is comment spam. Batch findings into one comment per issue per run, and one digest per person per day. Never re-comment on the same finding — track what's been raised (a label like `refine-flagged-ac` or a hidden property works).

**Split the autonomy tiers explicitly in your prompt:** silent auto-fix (formatting, resolution field, closing duplicates of duplicates), comment-and-suggest (estimates, splits, links), and escalate-only (closure, priority, reassignment, anything that changes commitment). Anything that changes rank, priority, or scope should be scrum-master/PO territory — that's the line that keeps people trusting it.

**Skill vs Rovo agent:** a Rovo agent lives inside Jira and can be wired to triggers/automation, so it's the better fit for scheduled sweeps and on-create hygiene checks. A Claude skill is better when you want richer reasoning, multi-source context (Confluence + Slack + PRs + Jira), or output that isn't a Jira comment — like the refinement agenda or the health scorecard. Many teams end up with both: Rovo for the always-on hygiene checks, Claude for the weekly deep pass and meeting prep.

**Start with a JQL-driven scope**, not the whole backlog. Something like "top 40 ranked, unestimated or DoR-failing, in projects X/Y" keeps the first version useful and cheap.

Want me to turn a subset of these into an actual SKILL.md with the JQL queries, autonomy tiers, and comment templates spelled out?