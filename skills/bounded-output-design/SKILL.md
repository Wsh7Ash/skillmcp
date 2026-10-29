---
name: bounded-output-design
description: "Cap every response so one tool call cannot fill an agent's context window. Use when a tool can return an unbounded list, a full file or a large body"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [design, output, context]
---

# Bounded Output Design

> Cap every response so one tool call cannot fill an agent's context window

**Use when:** a tool can return an unbounded list, a full file or a large body

**Avoid when:** the tool always returns a fixed small record

## Procedure

1. Estimate the largest realistic response for the tool
2. Add a limit parameter with a conservative default and a hard maximum
3. Return a total count beside the truncated slice
4. State in the result that truncation happened and how to continue
5. Test the largest allowed request and confirm the response stays small
6. Prefer a fetch-by-id tool over returning whole corpora

## Signals

- responses have a predictable ceiling regardless of input
- truncated results state the total and the applied limit
- a caller can page by raising the offset rather than re-querying everything
- the agent never receives a whole pack in one call

## Patterns

**1. Limit and total**

```text
{"matches": [...10], "matches_total": 50}
```

**2. Truncation note**

```text
showing 10 of 50; raise limit or narrow the query
```

**3. Fetch by id**

```text
get_skill returns one document, not the pack
```

## Pitfalls

- Returning every match and relying on the client to trim it
- Truncating silently so the model believes it saw everything
- Setting the default limit so high that the cap never engages

## Done when

- the worst-case response size is bounded and tested
- every truncated response states the total available

## References

- [Anthropic - context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
