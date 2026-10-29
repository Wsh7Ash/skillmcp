---
name: tool-surface-minimisation
description: "Ship the fewest tools that cover the workflow, because every extra tool is a wrong choice waiting to happen. Use when a server is accumulating tools and the list is getting hard for a model to choose from"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [design, surface, discipline]
---

# Tool Surface Minimisation

> Ship the fewest tools that cover the workflow, because every extra tool is a wrong choice waiting to happen

**Use when:** a server is accumulating tools and the list is getting hard for a model to choose from

**Avoid when:** the server is new and its first three tools are still being validated

## Procedure

1. List every tool and the workflow step it serves
2. Merge tools that differ only by an argument value
3. Remove tools that duplicate another tool's output
4. Keep one discovery tool, one fetch tool and the minimum for the domain
5. Check that each remaining tool has a distinct reason to exist
6. Document the removal so a later contributor does not re-add it

## Signals

- each tool maps to one workflow step and no two overlap
- the tool list fits on one screen
- a model choosing between two tools cannot pick wrong
- removed tools are recorded with the reason

## Patterns

**1. Core trio**

```text
list_packs, search_skills, get_skill
```

**2. Merge candidate**

```text
get_skill_by_tag folds into search_skills
```

**3. Removal note**

```text
removed dump_all: unbounded output, replaced by search
```

## Pitfalls

- Adding a tool per keyword instead of making search better
- Keeping a convenience tool that returns unbounded output
- Removing a tool without noting why, so it returns in six months

## Done when

- every tool maps to a distinct workflow step
- removals are recorded with their reason

## References

- [Anthropic - writing tools for agents](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
