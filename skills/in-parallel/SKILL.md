---
name: in-parallel
description: Coordinate separable work across parallel Codex threads. Use when the user asks to do work in parallel, split several tasks across threads, fan out independent investigations or edits, or run multiple Codex sessions toward one outcome.
---

# In Parallel

## Contract

When invoked, turn the user's request into independent work packets and run them in parallel Codex threads or subagents when the available tool surface supports it.

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
2. Check the available thread or subagent tools.
   - If the user explicitly asks for Codex threads, search for `create_thread`, `send_message_to_thread`, `read_thread`, and related thread tools before claiming they are unavailable.
   - For current-turn subwork, prefer multi-agent tools when available rather than creating sidebar-visible user-owned threads.
   - If no parallel execution tool is available, prepare the packets as copyable prompts and say that live parallel execution is unavailable in this environment.
3. Write each packet as a self-contained prompt.
   - Include the goal, relevant paths or URLs, constraints, expected output, and any verification requested by the user.
   - Tell workers not to edit shared files unless their packet explicitly requires it.
   - Tell workers to report findings, changed files, commands run, and blockers.
4. Start workers in parallel only after the packets are clear.
   - Use separate threads or agents for independent packets.
   - Avoid sending multiple workers into the same file unless the task is read-only.
   - Keep a main-thread checklist of packets, statuses, and integration work.
5. Merge and verify.
   - Read each worker result.
   - Reconcile conflicts, duplicated findings, and inconsistent assumptions.
   - Perform any final integration, tests, formatting, or user-facing synthesis in the main thread.
6. Report the outcome.
   - Name each packet and its result.
   - Include links to created Codex threads when thread tools return them.
   - State what was verified and what remains blocked.

## Guardrails

- Do not create user-owned Codex threads for ordinary subtasks unless the user explicitly asks for threads; use subagents when that is the intended local execution model.
- Do not claim work was done in parallel if only prompts were prepared.
- Do not let worker outputs bypass review; the main thread owns the final answer and any committed changes.
- Do not split a task so finely that coordination costs exceed the benefit.
- Do not parallelize commands that are known to contend on the same local database, lockfile, deployment, or external resource.
- Preserve the user's newest instruction if it conflicts with an already-started packet.

## Output Expectations

When work runs in parallel, keep the user updated with:

- the packet list before or immediately after launch
- worker status as results arrive
- the final integrated result, including verification

When live parallel execution is unavailable, output:

- `Parallel execution unavailable here.`
- the shortest useful set of copyable prompts for the user to launch manually
