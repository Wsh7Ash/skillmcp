---
name: tool-call-budgeting
description: "Decide the call budget for a task before starting so an agent cannot loop on a tool. Use when an agent may retry or search repeatedly and each call costs context and latency"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [invoke, budget, discipline]
---

# Tool Call Budgeting

> Decide the call budget for a task before starting so an agent cannot loop on a tool

**Use when:** an agent may retry or search repeatedly and each call costs context and latency

**Avoid when:** the task needs exactly one call, where a budget adds no constraint

## Procedure

1. Estimate how many calls the task genuinely needs
2. Write that number down as a ceiling before the first call
3. Count each call in the working notes
4. Stop and reassess when the ceiling is reached, rather than making one more
5. Replace repeated calls with a single broader query where possible
6. Record whether the ceiling was hit, because that is a signal about the tool

## Signals

- the call count stays within the written ceiling
- the same arguments are never sent twice
- a hit ceiling triggers a reassessment instead of another attempt
- the notes show why each call was made

## Patterns

**1. Call ceiling**

```text
budget: 3 search calls, 1 fetch for this step
```

**2. No repeats**

```text
identical arguments -> use the cached result
```

**3. Reassess marker**

```text
budget reached: results too broad, refine keywords
```

## Pitfalls

- Retrying identical calls hoping for a different answer
- Counting only successful calls and ignoring errors that also cost time
- Raising the budget mid-task because progress feels slow

## Done when

- a ceiling is stated before the first call and compared afterwards
- no identical call is sent twice in one task

## References

- [Anthropic - agent design](https://docs.anthropic.com/en/docs/build-with-claude)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
