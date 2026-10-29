---
name: skill-frontmatter-contract
description: "Keep the frontmatter fields identical across a pack so any loader can index it without special cases. Use when skills from several packs will be loaded by one runtime or one index"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [document, frontmatter, interoperability]
---

# Skill Frontmatter Contract

> Keep the frontmatter fields identical across a pack so any loader can index it without special cases

**Use when:** skills from several packs will be loaded by one runtime or one index

**Avoid when:** the pack is a private draft that no loader will read

## Procedure

1. Fix the field set: name, description, pack, version, category, tags
2. Generate the block from one renderer rather than by hand
3. Assert the field set in the validator
4. Ensure description carries both the summary and the use-when clause
5. Check every file parses as YAML with the expected types
6. Reject a file whose frontmatter drifts from the contract

## Signals

- every SKILL.md has the same field names in the same order
- tags parse as a list of strings
- the description is long enough to be useful and within the limit
- the validator fails on a missing field

## Patterns

**1. Field set**

```text
name, description, pack, version, category, tags
```

**2. Description**

```text
summary plus 'Use when ...' clause
```

**3. Validator**

```text
reject a file missing any declared key
```

## Pitfalls

- Hand-writing frontmatter so fields drift between files
- Putting a path in the description, which varies by machine
- Letting the description grow past what a loader will display

## Done when

- every skill file declares the identical field set
- a missing field is a validation failure

## References

- [MCP - resources and skills](https://modelcontextprotocol.io/specification/2025-03-26/server/resources)
- [YAML - specification](https://yaml.org/spec/1.2.2/)
