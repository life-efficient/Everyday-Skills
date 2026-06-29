---
name: in-parallel
description: Coordinate separable work across parallel Codex threads. Use when the user asks to do work in parallel, split several tasks across threads, fan out independent investigations or edits, or run multiple Codex sessions toward one outcome.
---

# In Parallel

## Contract

When invoked with `$in-parallel` or an explicit request to run work in
parallel, turn the user's request into independent work packets and create
parallel Codex threads for those packets when the available tool surface
supports it.

In the Codex desktop app, the expected thread tool is
`codex_app.create_thread`. It is usually exposed lazily: discover it first with
`tool_search` using a query like `create_thread`, then call it with a
self-contained prompt and a target such as `projectless` or a specific project.

Use this skill for genuinely separable work:

- Multiple unrelated tasks that can proceed without shared intermediate state.
- Independent code investigations, reviews, research tracks, or implementation areas.
- A main task where parallel discovery can reduce wall-clock time before one final integration step.

Do not use this skill when the work must be done sequentially, depends on one shared mutable file or database lock, requires one interactive browser session, or needs a single coherent authorial voice before any delegation.

## Workflow

1. Identify the independent units of work.
   - Split by repository area, route, file ownership, issue, question, or deliverable section.
   - Keep each packet small enough for a fresh thread to complete without hidden context.
   - If dependencies exist, keep dependent steps in the main thread or schedule them after fanout results return.
2. Discover the Codex thread tool before concluding it is unavailable.
   - Call `tool_search` for `create_thread`.
   - Use `codex_app.create_thread` when exposed.
   - Pass a self-contained prompt and the correct target:
     - `projectless` for general work or work that does not belong to one repo.
     - A specific project target for repo-bound work when the tool supports it.
   - Also discover `read_thread`, `send_message_to_thread`, and related tools
     if the main thread needs to monitor or coordinate worker results.
   - Use subagents only when the user explicitly asks for subagents/local
     workers, when `codex_app.create_thread` is genuinely unavailable after
     targeted discovery, or when creating sidebar-visible user-owned threads
     would be inappropriate for the task.
   - If no live parallel execution tool is available after targeted discovery,
     prepare the packets as copyable prompts and say that live parallel
     execution is unavailable in this environment.
3. Write each packet as a self-contained prompt.
   - Include the goal, relevant paths or URLs, constraints, expected output, and any verification requested by the user.
   - Tell workers not to edit shared files unless their packet explicitly requires it.
   - Tell workers to report findings, changed files, commands run, and blockers.
4. Start workers in parallel only after the packets are clear.
   - Use separate Codex threads for independent packets by default.
   - Avoid sending multiple workers into the same file unless the task is read-only.
   - Keep a main-thread checklist of packets, statuses, and integration work.
   - After a successful `create_thread` call, preserve the returned thread ID
     so it can be reported or monitored.
5. Merge and verify.
   - Read each worker result.
   - Reconcile conflicts, duplicated findings, and inconsistent assumptions.
   - Perform any final integration, tests, formatting, or user-facing synthesis in the main thread.
6. Report the outcome.
   - Name each packet and its result.
   - Include links to created Codex threads when thread tools return them.
   - State what was verified and what remains blocked.

## Guardrails

- Do not interpret `$in-parallel` as local shell-command parallelism or
  `multi_tool_use.parallel` only; `$in-parallel` means create parallel Codex
  threads when the tool is available.
- Do not skip `tool_search` for `create_thread` just because the tool is not
  initially visible; Codex thread tools are often lazy-loaded.
- Do not use subagents instead of Codex threads unless the user explicitly asks
  for subagents/local workers or thread creation is unavailable after targeted
  discovery.
- Do not claim work was done in parallel if only prompts were prepared.
- Do not let worker outputs bypass review; the main thread owns the final answer and any committed changes.
- Do not split a task so finely that coordination costs exceed the benefit.
- Do not parallelize commands that are known to contend on the same local database, lockfile, deployment, or external resource.
- Preserve the user's newest instruction if it conflicts with an already-started packet.

## Output Expectations

When work runs in parallel, keep the user updated with:

- the packet list before or immediately after launch
- the created Codex thread IDs or links when available
- worker status as results arrive
- the final integrated result, including verification

When live parallel execution is unavailable, output:

- `Parallel execution unavailable here.`
- the shortest useful set of copyable prompts for the user to launch manually
