---
name: destructive-tool-gating
description: "Require an explicit target and an explicit intent for any tool that deletes or overwrites. Use when a server exposes a tool that changes or removes data the agent did not create"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [design, destructive, safety]
---

# Destructive Tool Gating

> Require an explicit target and an explicit intent for any tool that deletes or overwrites

**Use when:** a server exposes a tool that changes or removes data the agent did not create

**Avoid when:** the server is read-only, which removes the whole class of risk

## Procedure

1. Enumerate the tools that remove or overwrite data
2. Require the exact target as a separate argument rather than a wildcard
3. Require a dry-run first or return a preview when that is possible
4. Refuse ambiguous targets instead of choosing one
5. Log the full target and the caller identity for every destructive call
6. Test a wildcard target and confirm it is refused

## Signals

- a wildcard target is rejected with a clear message
- destructive tools name the exact object in their output
- a dry run returns the plan without effect
- logs record every destructive call with its target

## Patterns

**1. Explicit target**

```text
delete_skill(slug, pack) instead of delete_skills(tag)
```

**2. Preview call**

```text
dry_run returns the same output with no write
```

**3. Refusal shape**

```text
refusing wildcard target '*'
```

## Pitfalls

- Accepting a tag or glob as a delete target
- Letting an agent retry a destructive call after an ambiguous timeout
- Logging the action without the target, making an audit useless

## Done when

- destructive tools require an exact, non-wildcard target
- every destructive call is logged with its target

## References

- [OWASP - destructive operations](https://cheatsheetseries.owasp.org/)
- [MCP - security best practices](https://modelcontextprotocol.io/specification/2025-03-26/basic/security_best_practices)
