---
name: pagination-and-limit-discipline
description: "Page through results deliberately and stop when the remaining results stop being useful. Use when a tool returns a truncated list with a total count"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [invoke, pagination, context]
---

# Pagination and Limit Discipline

> Page through results deliberately and stop when the remaining results stop being useful

**Use when:** a tool returns a truncated list with a total count

**Avoid when:** the result set is smaller than one page and truncation never occurs

## Procedure

1. Compare the returned count against the total
2. Decide whether the missing results could change the decision
3. Refine the query before paging when the first page is unfocused
4. Page with an explicit limit and offset only when the extra results matter
5. Stop as soon as the decision is determined
6. Record how many results were actually consumed

## Signals

- the total count is compared against the returned count every time
- paging happens only when the decision depends on it
- the query is refined instead of paging through noise
- the notes state how many results were used

## Patterns

**1. Count comparison**

```text
returned 10 of 50 -> is 11-50 relevant?
```

**2. Refine first**

```text
add a tag to the query instead of offset=10
```

**3. Explicit page**

```text
limit=10 offset=10 only when needed
```

## Pitfalls

- Paging through every result when the first three answered the question
- Assuming a short page means the end when the total says otherwise
- Raising the limit to the maximum and re-reading the same first page

## Done when

- the returned and total counts are compared before any paging
- the number of results actually consumed is recorded

## References

- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
- [Anthropic - context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
