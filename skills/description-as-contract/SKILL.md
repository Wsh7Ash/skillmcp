---
name: description-as-contract
description: "Write tool descriptions as the contract a model will follow, including what the tool does not do. Use when an agent must choose between tools without seeing the implementation"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [design, documentation, agents]
---

# Description as Contract

> Write tool descriptions as the contract a model will follow, including what the tool does not do

**Use when:** an agent must choose between tools without seeing the implementation

**Avoid when:** a human is the only caller and reads the source directly

## Procedure

1. State what the tool returns in one sentence
2. State what it does not do, such as no network access or no writes
3. Name the failure modes a caller will encounter
4. Keep the description free of implementation detail the model cannot act on
5. Put constraints in the same order the model must respect them
6. Re-read the description as if it were the only information available

## Signals

- the description names the return shape and its bounds
- a caller knows which sibling tool to use next
- limitations appear in the description, not only in an error
- the text has no marketing adjectives

## Patterns

**1. Return statement**

```text
ranks skills by keyword over slug, title, tags and description
```

**2. Negation**

```text
does not read outside the packs root and sends no network traffic
```

**3. Failure note**

```text
returns isError with a suggestion when nothing matches
```

## Pitfalls

- Describing the mechanism instead of the contract
- Omitting limits so a model assumes completeness
- Repeating the tool name in the description instead of adding constraints

## Done when

- each description states return shape, bounds and limitations
- no description relies on source-reading to be understood

## References

- [Anthropic - tool definitions](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
