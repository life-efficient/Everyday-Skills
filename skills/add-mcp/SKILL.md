---
name: add-mcp
description: Add a new MCP server to Codex the documented way. Use when a user asks to add MCP, set up an MCP, connect an MCP server, add a hosted MCP server, or wire an MCP into Codex by registering it in ~/.codex/config.toml, authenticating when required, verifying `codex mcp list`, and confirming the tools are callable in a fresh session.
---

# Add MCP

## Contract

- MCP servers are added through `~/.codex/config.toml`, not the plugin marketplace.
- The server must appear in `codex mcp list` with `Status: enabled`.
- If the server uses OAuth, the login flow must be completed with `codex mcp login <name>`.
- The work is not complete until the MCP tools are callable in a fresh Codex session.
- If a plugin scaffold was attempted first, the skill should explicitly retire that path and move to Codex-native MCP config.

## When to use this

Use this skill when the user wants Codex to connect to a hosted MCP server such as:

- `https://mcp.cal.com/mcp`
- `https://mcp.cloudflare.com/mcp`
- other documented remote MCP servers compatible with Codex

Do not use this skill for local repo plugins unless the user specifically wants a plugin package rather than an MCP server config.

## Phases

### Phase 1: Discover the documented MCP endpoint

1. Find the provider's official MCP docs.
2. Confirm the correct hosted MCP URL.
3. Confirm the auth model:
   - OAuth
   - bearer token
   - none

If the provider does not publish an MCP endpoint, stop and say so clearly.

### Phase 2: Register the server in Codex config

Add the server to `~/.codex/config.toml` under:

```toml
[mcp_servers.<name>]
url = "https://example.com/mcp"
enabled = true
```

Use a stable lower-case name. Prefer the provider's obvious canonical name.

### Phase 3: Verify Codex sees it

Run:

```bash
codex mcp list
```

The server should appear with:

- the expected URL
- `Status: enabled`

If it does not appear, re-check the config path and TOML structure before trying anything else.

### Phase 4: Authenticate if required

If `codex mcp list` shows `Not logged in`, run:

```bash
codex mcp login <name>
```

Complete the OAuth or token flow. Then run `codex mcp list` again and confirm auth is present.

### Phase 5: Verify tool availability

After config + auth are correct:

1. Start a fresh Codex session if necessary.
2. Confirm the new MCP namespace or tools appear in the tool registry.
3. Use a harmless read call first.

If config is correct but tools are still missing in the live session, state that a session refresh is the remaining blocker rather than pretending the integration is usable.

## Output Format

Return:

1. The MCP endpoint that was added
2. The config block written
3. Whether `codex mcp list` sees it
4. Whether auth is complete
5. Whether tools are callable in the current session
6. The exact next blocker if not complete

## Anti-Patterns

- Adding hosted MCP servers through plugin marketplace files instead of `~/.codex/config.toml`
- Declaring success before `codex mcp list` shows the server
- Declaring success before OAuth/token auth is actually complete
- Assuming a configured MCP is callable in the already-running session without checking
- Using invented URLs, names, or auth expectations instead of the provider's docs
