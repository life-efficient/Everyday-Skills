---
name: granola-brain-ingest
description: Ingest recent Granola meeting notes into the local BigBrain brain when the user asks to import, sync, backfill, or automate Granola meetings with sanitized transcripts.
---

# Granola Brain Ingest

Ingest recent Granola meetings into the user's local BigBrain brain. Preserve
durable meeting context while preventing unsafe transcript material from being
stored.

## Contract

Use this skill when the user asks to import, sync, backfill, or automate Granola
meetings into the local brain.

Successful completion means:

- the target brain is the local brain, normally `/Users/hq/projects/brain`
- current brain filing rules are read before choosing paths
- only recent or not-yet-ingested Granola meetings are considered
- existing `granola_id` values and raw sidecars are checked before writing
- each new meeting gets one `meetings/*.md` page following the local page shape
- transcript sidecars are sanitized before saving; verbatim transcripts are not saved
- no slander, profanity, insults, personal topics, sexual topics, or sensitive topics are copied into the brain
- `bigbrain sync --json` runs after writes, and the final report names what changed

## Workflow

1. Resolve the brain and rules.
   - Work from `/Users/hq/projects/brain` unless the user names another brain.
   - Read top-level `FILING.md` and `meetings/FILING.md` before writing.
   - Use the existing local meeting-page pattern: frontmatter with `type:
     meeting`, `title`, `date`, `created`, `source: granola`, and
     `granola_id`; body with summary, decisions, action items, discussion notes,
     raw-source links, separator, and `## Timeline`.
2. Build the duplicate and cutoff index.
   - Search `meetings/**/*.md` for `granola_id:` and source links to Granola.
   - Search `meetings/.raw` for existing Granola document, source-note, and
     transcript sidecars.
   - Treat a matching Granola UUID as already ingested, even if the title has
     changed.
   - Determine the newest ingested Granola meeting date. Query Granola from two
     days before that date to catch late summaries, or use the last 30 days when
     no prior Granola import exists.
3. Fetch candidate meetings from Granola.
   - Use the Granola MCP list tool for the chosen window.
   - Fetch details for candidate IDs in batches of at most 10.
   - Fetch transcripts only for meetings that are not already ingested or whose
     existing page is missing a transcript/source sidecar and the user asked to
     repair gaps.
4. Classify each candidate.
   - `new`: no existing page with the same `granola_id`.
   - `duplicate`: matching `granola_id` already exists; skip unless repairing a
     missing sidecar.
   - `metadata-only`: Granola has no useful transcript or summary; create a
     low-information page only when there is enough metadata to preserve
     idempotency.
   - `unsafe`: the transcript is dominated by material the user said to expunge;
     do not save a transcript sidecar, and keep the meeting page to safe
     metadata plus a redaction note.
5. Sanitize before saving any transcript.
   - Never write the verbatim transcript to disk, scratch files, raw sidecars, or
     final output.
   - Remove slander, profanity, insults, personal topics, sexual topics, and
     sensitive topics before saving.
   - Prefer deletion over masking when a sentence is unsafe. If context is
     needed, replace the removed span with `[redacted: category]` where category
     is one of `profanity`, `insult`, `slander`, `personal`, `sexual`, or
     `sensitive`.
   - Use `scripts/sanitize_transcript.py` as a first-pass filter for obvious
     material, then review the result semantically before saving. The script is
     not a substitute for judgment.
   - If you cannot review a transcript fully because tool output is truncated,
     do not save a transcript sidecar. Record that the transcript endpoint
     returned content but a complete sanitized transcript could not be verified.
6. Write the meeting artifacts.
   - Put canonical pages under `meetings/<slug>.md`.
   - Put raw sidecars under `meetings/.raw/` with collision-safe names such as
     `<slug>-source-note.md`, `<slug>-granola-document.json`, and
     `<slug>-transcript.txt`.
   - The transcript sidecar must contain sanitized content only and should state
     that unsafe material was expunged before storage.
   - Store Granola metadata and summaries only after removing unsafe personal or
     sensitive material.
   - Link sidecars from the meeting page's `Raw Source` line.
7. Verify and sync.
   - Re-scan for duplicate `granola_id` values.
   - Confirm every new page has the required frontmatter and `## Timeline`.
   - Confirm no saved sidecar contains obvious banned terms from the sanitizer's
     pattern set.
   - Run `bigbrain sync --json` from the brain root.

## Guardrails

- Do not store verbatim Granola transcripts. The saved transcript is a sanitized
  source artifact, not a literal raw transcript.
- Do not ingest old meetings just because they appear in a broad Granola query;
  use the cutoff and duplicate index.
- Do not create people, companies, deals, tasks, or concept pages from a meeting
  unless the filing rules and the meeting evidence clearly justify durable
  updates.
- Do not invent attendees, decisions, dates, or action owners. If Granola
  metadata is thin, say so in the page.
- Do not include examples of removed profanity, insults, sexual content, or
  sensitive personal details in the page, source note, transcript, or final
  report.
- Do not treat a clean helper-script result as proof that the transcript is safe;
  semantic review is required.

## Output

Report briefly:

- Granola window checked
- meetings found, skipped as duplicates, ingested, metadata-only, and unsafe
- pages and sidecars written
- transcript sanitization method used
- `bigbrain sync --json` result
- warnings, especially truncated transcripts or meetings skipped for safety
