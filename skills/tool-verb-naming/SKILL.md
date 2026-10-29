---
name: tool-verb-naming
description: "Name tools after the action they perform so a model chooses correctly from the name alone. Use when a new tool is being added and the name is still free-form"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [design, naming, tools]
---

# Tool Verb Naming

> Name tools after the action they perform so a model chooses correctly from the name alone

**Use when:** a new tool is being added and the name is still free-form

**Avoid when:** the server exposes one tool and naming ambiguity cannot arise

## Procedure

1. Write the one sentence the tool performs, in verb-first form
2. Derive the name from that verb and its object, in snake_case
3. Check the name against existing tools for collisions and near-duplicates
4. Avoid generic verbs such as run, do, execute or process
5. Put the distinguishing detail in the description, not the name
6. Re-read the final name as a model would, with no other context

## Signals

- the name states what happens, such as get_skill or search_skills
- no two tools differ only by a suffix
- the description adds constraints rather than repeating the name
- a reader can predict the return shape from the name

## Patterns

**1. Verb object**

```text
search_skills, get_skill, list_packs
```

**2. Avoided names**

```text
run_task, do_thing, execute_action
```

**3. Distinct pair**

```text
search_skills versus get_skill: one query, one fetch
```

## Pitfalls

- Naming a tool after its implementation, such as index_lookup
- Two tools whose names differ only by a word the model cannot see the effect of
- Encoding prerequisites in the name instead of the schema

## Done when

- every tool name is verb-first and unique
- each name's return shape is guessable before reading the schema

## References

- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
- [Anthropic - tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
