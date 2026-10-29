---
name: publishing-a-pack-locally
description: "Lay out a pack so any skill-aware runtime recognises it without a bespoke loader. Use when a new skill pack is ready to be used by an agent runtime on the same machine"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [document, publishing, layout]
---

# Publishing a Pack Locally

> Lay out a pack so any skill-aware runtime recognises it without a bespoke loader

**Use when:** a new skill pack is ready to be used by an agent runtime on the same machine

**Avoid when:** the skills are consumed by a hosted service with its own ingestion format

## Procedure

1. Create the pack root with pack.json at the top level
2. Write each skill to skills/<slug>/SKILL.md
3. Include a skill_count and a SHA-256 per file in the manifest
4. Generate a catalog so a human can browse without opening every file
5. Point the runtime at the parent directory so discovery finds the pack
6. Verify the server lists the pack and returns one skill by slug

## Signals

- the manifest's skill_count matches the number of skill files
- every manifest path resolves on disk
- the catalog lists all slugs
- a runtime pointed at the parent directory finds the pack

## Patterns

**1. Pack layout**

```text
pack.json, skills/<slug>/SKILL.md, results/catalog.md
```

**2. Manifest entry**

```text
{"slug":..., "path":"skills/x/SKILL.md", "sha256":...}
```

**3. Runtime pointer**

```text
serve --packs-root <parent directory>
```

## Pitfalls

- Putting pack.json below the skill directory so discovery misses it
- Committing skills without the manifest, leaving consumers unable to verify
- Pointing the runtime at the pack itself when it expects a parent directory

## Done when

- a runtime discovers the pack from its parent directory
- the manifest validates against the files on disk

## References

- [MCP - resources](https://modelcontextprotocol.io/specification/2025-03-26/server/resources)
- [Anthropic - skills](https://docs.anthropic.com/en/docs/claude-code)
