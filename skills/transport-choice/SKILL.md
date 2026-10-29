---
name: transport-choice
description: "Pick stdio or a network transport deliberately, based on where the server and its data actually live. Use when a new server is being designed and the transport decision is still open"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [setup, mcp, transport]
---

# Transport Choice

> Pick stdio or a network transport deliberately, based on where the server and its data actually live

**Use when:** a new server is being designed and the transport decision is still open

**Avoid when:** the runtime only supports one transport, which settles the question already

## Procedure

1. List where the server runs relative to the client: same host, container or remote
2. Determine whether the server needs credentials the client already holds
3. Choose stdio when the server shares the client's filesystem and lifetime
4. Choose a network transport when several clients must share one server process
5. Document the failure mode of the chosen transport before writing code
6. Test the chosen transport with the real client, not only with a hand-written message

## Signals

- a stdio server dies when the client exits, which is usually what you want
- a network server survives client restarts but needs its own auth story
- the transport choice changes how errors surface to the agent
- stdio avoids port conflicts entirely for local work

## Patterns

**1. Stdio fit**

```text
server reads packs from the same disk the agent runs on
```

**2. Network fit**

```text
two agents share one long-lived index
```

**3. Failure mode**

```text
stdio: client exit kills server; network: orphaned process
```

## Pitfalls

- Choosing a network transport for a local file reader and inheriting an auth problem
- Assuming a hosted transport removes the need to validate tool arguments
- Testing with curl instead of the real client and missing handshake requirements

## Done when

- the transport decision is recorded with its reason
- the chosen transport completes a full handshake with the real client

## References

- [MCP - architecture](https://modelcontextprotocol.io/docs/concepts/architecture)
- [MCP - transports](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
