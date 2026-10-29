---
name: restart-and-reload-semantics
description: "Know what the server caches and what needs a restart, so stale data never masquerades as a bug. Use when packs or skills change on disk while a client session is running"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [setup, reload, operations]
---

# Restart and Reload Semantics

> Know what the server caches and what needs a restart, so stale data never masquerades as a bug

**Use when:** packs or skills change on disk while a client session is running

**Avoid when:** the server only ever reads immutable content shipped with the package

## Procedure

1. Write down what the server loads once at startup and what it re-reads per request
2. Prefer re-reading the index per request for local file packs
3. Expose no reload tool if re-reading is already cheap
4. Test that a file edited mid-session is visible on the next call
5. Document the behaviour so a stale read is not reported as a defect
6. Keep the startup path tolerant of a missing pack so a reload cannot crash the server

## Signals

- an edited skill appears in the next search without a restart
- a deleted skill disappears from listings on the next call
- a malformed pack is skipped instead of crashing the server
- the server survives a mid-session pack change

## Patterns

**1. Per-request index**

```text
reload packs inside each tools/call
```

**2. Tolerant discovery**

```text
skip directories without pack.json
```

**3. Documented**

```text
reload: index rebuilt per request, no restart needed
```

## Pitfalls

- Caching the index forever and debugging a phantom stale result
- Reloading on every keystroke when the packs are large and unchanged
- Crashing on a half-written manifest during an editor save

## Done when

- the reload policy is documented in the README
- an edit mid-session is visible without restarting the client

## References

- [MCP - lifecycle](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle)
- [MCP - tools listChanged](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
