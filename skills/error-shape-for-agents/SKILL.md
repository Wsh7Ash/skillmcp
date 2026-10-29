---
name: error-shape-for-agents
description: "Return errors an agent can act on: what failed, why, and the next call that would work. Use when a tool can fail because of bad arguments, missing files or an empty result"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [design, errors, agents]
---

# Error Shape For Agents

> Return errors an agent can act on: what failed, why, and the next call that would work

**Use when:** a tool can fail because of bad arguments, missing files or an empty result

**Avoid when:** the tool cannot fail, such as a constant return

## Procedure

1. Separate protocol errors from tool-level failures
2. Use JSON-RPC errors for malformed requests and invalid params
3. Use a tool result with isError for failures inside a valid call
4. Name the failing input and the accepted shape in the message
5. Suggest the next call, such as list_packs when a slug is unknown
6. Never return a bare stack trace as the only content

## Signals

- an unknown slug returns isError with a suggestion to list packs
- invalid params carry the offending key name
- the message distinguishes not-found from unreadable
- no traceback reaches the client

## Patterns

**1. Tool failure**

```text
{"content": [{"type": "text", "text": "..."}], "isError": true}
```

**2. Protocol failure**

```text
{"error": {"code": -32602, "message": "invalid params"}}
```

**3. Actionable text**

```text
unknown skill 'x'; try search_skills first
```

## Pitfalls

- Returning isError for a malformed request instead of a JSON-RPC error
- Leaking a filesystem path or a stack trace into the tool result
- Returning success with empty content when the lookup failed

## Done when

- protocol errors and tool failures are distinguishable by shape
- each error names the input and suggests a next step

## References

- [JSON-RPC 2.0 - error object](https://www.jsonrpc.org/specification)
- [MCP - tools result](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
