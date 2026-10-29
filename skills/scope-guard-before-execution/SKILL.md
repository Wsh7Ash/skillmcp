---
name: scope-guard-before-execution
description: "Check the engagement scope before a tool touches a target, and refuse rather than warn. Use when a tool can act on arbitrary hosts and the agent may have the wrong target in context"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [govern, scope, safety]
---

# Scope Guard Before Execution

> Check the engagement scope before a tool touches a target, and refuse rather than warn

**Use when:** a tool can act on arbitrary hosts and the agent may have the wrong target in context

**Avoid when:** the tool is a pure reader of local packs with no target concept

## Procedure

1. Load the in-scope asset list at startup, failing when it is absent
2. Normalise each requested target before comparison
3. Refuse any target that does not match the list exactly
4. Return a refusal that names the target and the reason
5. Log refusals so repeated mistakes are visible
6. Test a target one character outside the list and confirm refusal

## Signals

- an out-of-scope target is refused, not merely warned about
- the refusal message quotes the requested and the allowed assets
- refusals are logged with a timestamp
- a near-miss target such as a lookalike domain is refused

## Patterns

**1. Exact match**

```text
target in scope_set, with normalised case and trailing dot
```

**2. Refusal shape**

```text
refused: evil.example is not in scope
```

**3. Near-miss test**

```text
api.example.test.evil.example refused
```

## Pitfalls

- Warning about scope and continuing, which is the same as no guard
- Matching on a substring so a lookalike domain passes
- Caching the scope list so a mid-engagement change is ignored

## Done when

- an out-of-scope target produces a refusal and no action
- a lookalike domain is proven to be refused

## References

- [OWASP - testing scope](https://owasp.org/www-project-web-security-testing-guide/)
- [MCP - security best practices](https://modelcontextprotocol.io/specification/2025-03-26/basic/security_best_practices)
