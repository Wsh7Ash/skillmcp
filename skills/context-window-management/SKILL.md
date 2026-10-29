---
name: context-window-management
description: "Spend context on the procedure you will follow, not on everything the server could return. Use when a session accumulates tool output and the budget for reasoning is shrinking"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [invoke, context, efficiency]
---

# Context Window Management

> Spend context on the procedure you will follow, not on everything the server could return

**Use when:** a session accumulates tool output and the budget for reasoning is shrinking

**Avoid when:** the session is short and every returned document is used immediately

## Procedure

1. Track roughly how much text each tool call returned
2. Prefer summaries and counts over full documents when deciding
3. Fetch full text only for the item you will act on
4. Drop or summarise earlier output that no longer affects the task
5. Re-fetch a needed detail by id rather than keeping it in context
6. Record the identifiers you will need later, not the bodies

## Signals

- the working notes contain identifiers rather than full documents
- each fetch is followed by an action
- summaries replace full listings once a decision is made
- no document is fetched twice

## Patterns

**1. Identifiers not bodies**

```text
keep skillmcp slug list, not 50 SKILL.md files
```

**2. Summarise**

```text
10 matches -> 2 candidates and why
```

**3. Re-fetch by id**

```text
get_skill(slug) when the detail is needed again
```

## Pitfalls

- Fetching a whole pack to answer one question
- Keeping every response verbatim and running out of room for reasoning
- Re-fetching the same document because the identifier was not recorded

## Done when

- only the acted-on documents are kept in full
- identifiers are recorded so any document can be re-fetched

## References

- [Anthropic - context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
