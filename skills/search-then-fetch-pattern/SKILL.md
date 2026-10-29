---
name: search-then-fetch-pattern
description: "Search first, fetch second, so context is spent on the one procedure that fits the task. Use when a corpus of skills or documents is larger than the context available for reading it"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [invoke, workflow, context]
---

# Search Then Fetch Pattern

> Search first, fetch second, so context is spent on the one procedure that fits the task

**Use when:** a corpus of skills or documents is larger than the context available for reading it

**Avoid when:** the corpus is a single document that can be read whole

## Procedure

1. Search with two or three concrete keywords from the current task
2. Read only the slugs, titles and descriptions in the result
3. Pick the single best match and fetch it by slug
4. If nothing matches, broaden one keyword rather than fetching many documents
5. Apply the procedure and discard text that did not affect the action
6. Record which skill was used so later steps do not re-search

## Signals

- the fetched document is the one you act on, not a survey of five
- search results are short enough to scan in one pass
- a second fetch happens only when the first clearly does not fit
- the skill slug appears in the working notes

## Patterns

**1. Keyword choice**

```text
search_skills("cache vary") then get_skill("vary-header-inspection")
```

**2. Broaden once**

```text
no match -> drop the most specific term
```

**3. No bulk fetch**

```text
never fetch more than one skill per task step
```

## Pitfalls

- Fetching every skill that mentions the topic and drowning in procedure text
- Searching with a full sentence rather than keywords
- Re-searching for the same thing in every step of a task

## Done when

- one skill is fetched per task step and named in the notes
- no search is repeated for a term already resolved

## References

- [Anthropic - context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
