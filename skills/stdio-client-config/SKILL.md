---
name: stdio-client-config
description: "Wire a stdio MCP server into a client config so the agent can call it without a restart loop. Use when a skill or tool server exists on disk and the agent runtime needs a config entry for it"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [setup, mcp, configuration]
---

# Stdio Client Config

> Wire a stdio MCP server into a client config so the agent can call it without a restart loop

**Use when:** a skill or tool server exists on disk and the agent runtime needs a config entry for it

**Avoid when:** the runtime loads tools over a hosted protocol that needs no local config entry

## Procedure

1. Locate the runtime's config file and read any existing entries before editing
2. Add one server entry with a single-word name and an absolute command path
3. Pass the packs root through an argument rather than an environment variable
4. Keep credentials out of the config file and read them from the environment at runtime
5. Restart the client and confirm the server appears in the tool list
6. Record the exact config snippet in the project README for the next person

## Signals

- the server appears in the client's tool list after a restart
- the client log shows a completed initialize handshake
- tools/call returns content rather than a transport error
- no shell wrapper is needed to find the executable

## Patterns

**1. Config entry**

```text
{"command":"python","args":["-m","skillmcp","serve"]}
```

**2. Absolute packs root**

```text
"--packs-root", "/srv/packs/skills"
```

**3. Secret via env**

```text
env: {"HUNT_TOKEN": "${HUNT_TOKEN}"}
```

## Pitfalls

- Using a relative command that resolves differently when the client starts from another directory
- Embedding a token in the config file which then gets committed
- Editing the config while the client runs and concluding the server is broken

## Done when

- the server appears in the tool list after a clean restart
- the config snippet in the README matches the working file

## References

- [MCP - transports](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
- [Claude Code - MCP setup](https://docs.anthropic.com/en/docs/claude-code)
