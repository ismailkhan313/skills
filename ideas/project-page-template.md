# Reusable Prompt — Create a Confluence Project Page

Paste the whole thing into a new chat. Fill in the bracketed fields at the top; leave the rest as-is.

---

## THE PROMPT

```
Create a project page in Confluence for [PROJECT NAME].

## Environment
- Confluence cloudId: thdca.atlassian.net
- Space: C4C (Contact Centre), spaceId 66977807
- Jira project: CCIVR
- Parent location: [PAGE ID or "Projects folder 3971743982"]
- Fiscal year runs 1 February to 31 January. FY2026 = 2026-02-01 to 2027-01-31.
  Never treat the calendar year as the fiscal year. Late-January clusters of closed
  tickets are year-end closes, not bulk cleanup.

## What I'm giving you
[Paste any of: Jira ticket keys or epic, an existing page URL, meeting notes,
email threads, a BRD, a vendor case reference. Or say "find it yourself".]

## Step 1 — Research before writing
Do the research yourself. Do not ask me to supply what you can look up.

1. Query Jira for the project's tickets. If no epic exists, cluster individual
   tickets by theme in the summary text — shared prefixes, numbered parts,
   lifecycle shape (design → build → test → deploy → KT), and close-out
   vocabulary (signoff, RFC, demo, handover, decommission).
2. Verify cluster boundaries by querying the theme across all time, not just the
   target year, so work that started earlier or continued later is caught.
3. Exclude recurring BAU and adhoc tickets from project counts. Note them
   separately if relevant.
4. Search Confluence for existing pages on this project — technical docs, MOPs,
   runbooks, BRDs, a product-team page. Link them; never duplicate their content.
5. Check whether a page for this project already exists. If it does, update it and
   preserve what's there, building the structure around the existing content rather
   than replacing it.
6. Verify every acronym and platform name against our own content before defining
   it. If the literal expansion isn't documented anywhere in the space, say so and
   describe what the thing does instead. Never invent an expansion.

Tell me what you found and what's missing before you publish, if anything material
is ambiguous.

## Step 2 — Page structure
Open with one or two sentences defining what the project is, in plain language.
No metadata line, no owner/reviewed header, no status banner unless the project's
state would mislead a reader without one.

Then:

**## Why it exists**
The problem in concrete terms — what was happening before, what it cost, what the
project changes. Written for someone who has never heard of this work. This is the
most important section on the page; do not reduce it to a restatement of the title.

**## Scope**
Table: Area | Detail. What's in, and explicitly what's out where the boundary is
easily mistaken.

**## How it works** (for anything with a runtime path)
Table: Layer or Component | What it does. Keep to the layers a reader needs to
hold in their head — five to seven rows.

**## Workstreams** or **## What's here**
Table of sub-pages. Use a "Use it when" column, not a "Description" column —
answer *when would I click this*, not *what is this*. Group into sections by
purpose (Design, Testing, Operations, Reporting, Background) when there are more
than about six.

**## Release timeline** (if the project has shipped anything)
Table: Milestone | Date | Status | Ticket. Every date cites its ticket. If a
milestone lands on a fiscal year-end close, say so, or the date reads as a delay.

**## Key decisions**
Four or five, as a decision list. State what was decided, not what you infer the
reasoning was. Where the rationale is visible in the tickets, include it in the
same sentence. Where a question was never resolved, record it as UNDECIDED rather
than guessing or dropping it.

**## Risks & concerns** (only if there are real ones)
Table: Area | Concern.

**## Related**
Every entry a real link, resolved to an actual page ID. Include sibling systems,
the layer above and below, Operations, Releases, and Data & Reporting where
relevant. Never leave a page name as plain text.

## Step 3 — Writing rules

**Publish for the end user, not for me.** Everything you'd say to me in chat —
staleness observations, departed authors, empty pages, structural criticism,
your own uncertainty about my instructions — stays in chat. It does not go on the
page. Report it to me separately after publishing.

**Flag real gaps on the page, but factually.** A cutover date named in a MOP and
never confirmed by a ticket gets an unverified marker and a short explanation.
No rollback procedure recorded gets stated plainly, along with the note that its
absence isn't the same as a decision not to have one. No QA tickets gets stated
next to the defect table, because the two facts explain each other.

**Mark unknowns explicitly.** Write "not established" rather than leaving a field
blank. A blank reads as an oversight; an explicit marker records that the
information genuinely doesn't exist.

**Do not include:** a "Current Status & Next Steps" section, forward-looking
recommendations, open-items checklists, product-template fields that read N/A on
IT work (Metrics/KPIs, UX Assets, SEO), or content duplicated from a page you've
linked.

**Length.** A reader should get the shape of the project in under a minute. If a
section needs more than a screen, it's a sub-page.

## Step 4 — Publishing mechanics
- Author with contentFormat "markdown" unless a Confluence-specific device is
  needed. If authoring HTML, call getContentFormatGuide first.
- Do not HTML-escape characters in the title field. Pass "A & B", not "A &amp; B".
- Panels cannot contain tables. List items cannot contain panels, tables, or
  headings — close the list and place the block after it as a sibling.
- Container choice: a page if anyone would ever read the container itself; a folder
  only for homogeneous chronological drawers (year folders, retros, archive).
  Never a folder with a "Start here" page inside it.
- If content belongs under a section parent, create it as a child page rather than
  overwriting the parent's body.
- Use a clear versionMessage.
- Labels, closed set: one type label (design-record, runbook, reference,
  requirements, release-notes, test-plan, onboarding, retro), plus system labels
  (store-ivr, cc-ivr, gecx, telephony-infra, cti), plus the hub label (ivr). Do not
  label with project names or years.

## Step 5 — Report back
Give me:
1. The page URL.
2. What you could not do through the API, if anything — page ownership, page emoji,
   moving folders, whiteboards, or embeds all need doing by hand. Say so rather
   than silently skipping it.
3. The judgement calls you made — inferred decisions, merged or split items, gaps
   surfaced, anything a reader might otherwise take as verified fact.
4. Anything you found that I should know but that doesn't belong on the page.
5. What status the page warrants, and let me set it. Confluence's native content
   status can't be set through the tools. Never recommend Verified for a page
   carrying unverified claims or a reconstruction note.

Do not ask me to confirm the structure before starting. Research, draft, publish,
then tell me what you did and what you weren't sure about.
```

---

## Variants

**For a completed project being documented after the fact**, add to Step 2:

```
This is a reconstruction. End the page with a provenance note stating it was
assembled from Jira and other records after the fact, when, and from what — and
that no project page existed at the time. Without it a reader assumes the page is
contemporaneous. Flag that the decision log is inferred and should be checked by
someone who was there.
```

**For a project that spans two hubs** (e.g. IVR and Salesforce), add:

```
Decide which hub owns the page and cross-link from the other rather than creating
two pages. Say which you chose and why.
```

**For a project that has closed**, add:

```
Promote the durable outputs — final architecture, reference material, runbooks —
into the system page they describe. The project page keeps the BRDs, workshop
notes, and interim decisions, and goes to Archive. If nothing was worth promoting,
tell me: it means the project produced no lasting knowledge.
```

---

## Why the prompt is shaped this way

Each rule exists because its absence produced a specific problem:

| Rule | What it prevents |
|---|---|
| "Publish for the end user, not for me" | Chat-style commentary about stale pages and departed authors ending up on a page a new hire reads |
| No metadata header line | An owner/reviewed line nobody maintains, which then misleads |
| "Use it when" column | Sub-page tables that restate titles instead of helping someone choose |
| Every Related entry a real link | Plain-text page names that look like links and aren't |
| Verify acronyms, never invent expansions | Confidently wrong definitions of internal platform names |
| Mark unknowns "not established" | Blank fields that read as oversight rather than absence of record |
| No "Next Steps" section | Project records drifting into stale to-do lists |
| Don't escape the title | A page literally titled with `&amp;` in it |
| Say what you couldn't do via API | Silent gaps between what was asked and what happened |
| Child page, don't overwrite the parent | A section hub replaced by one of its own sub-documents |