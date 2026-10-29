---
name: lifecycle-test-initialize-then-tools
description: "Prove the handshake before the tool list, because a client never calls tools on a failed initialize. Use when a new server is being validated against a real client for the first time"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [verify, lifecycle, handshake]
---

# Lifecycle Test Initialize Then Tools

> Prove the handshake before the tool list, because a client never calls tools on a failed initialize

**Use when:** a new server is being validated against a real client for the first time

**Avoid when:** the transport is already proven and only a single tool changed

## Procedure

1. Send initialize with a supported protocolVersion and client info
2. Assert protocolVersion, capabilities and serverInfo in the reply
3. Send the initialized notification and expect no reply
4. Send tools/list and assert every tool has a name, description and schema
5. Call one tool and assert the result shape
6. Record the whole sequence as a transcript fixture

## Signals

- initialize returns before any tool call is attempted
- the initialized notification produces no response line
- tools/list returns a non-empty array with schemas
- the first tool call succeeds on the same connection

## Patterns

**1. Handshake**

```text
initialize -> initialized -> tools/list -> tools/call
```

**2. No reply**

```text
notifications never produce a response id
```

**3. Schema check**

```text
each tool has inputSchema.type == 'object'
```

## Pitfalls

- Skipping the notification and wondering why a strict client stalls
- Calling a tool before initialize completes
- Asserting the tool list without checking schema presence

## Done when

- the full sequence passes on one connection in one process
- the transcript fixture is committed

## References

- [MCP - lifecycle](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
