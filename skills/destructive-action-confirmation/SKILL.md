---
name: destructive-action-confirmation
description: "Require a second, explicit signal before a destructive call leaves a trace that cannot be undone. Use when the server exposes a tool whose effect cannot be reversed by the caller"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [govern, confirmation, safety]
---

# Destructive Action Confirmation

> Require a second, explicit signal before a destructive call leaves a trace that cannot be undone

**Use when:** the server exposes a tool whose effect cannot be reversed by the caller

**Avoid when:** every operation is reversible through the same interface

## Procedure

1. Classify each tool as reversible or irreversible
2. For irreversible tools, require a confirmation argument derived from the target
3. Refuse when the confirmation does not match the target exactly
4. Return the effect that will occur before performing it when a dry run exists
5. Log the confirmation value with the call
6. Test a mismatched confirmation and confirm the refusal

## Signals

- an irreversible call without a matching confirmation is refused
- the refusal states the expected confirmation value
- the log records both the target and the confirmation
- a dry run leaves no state change

## Patterns

**1. Confirmation token**

```text
confirm='delete pack:legacy' must equal the target
```

**2. Refusal shape**

```text
confirmation mismatch: expected 'delete pack:legacy'
```

**3. Dry run mode**

```text
same call with dry_run=true, no write
```

## Pitfalls

- Accepting a boolean confirm flag that any agent can set blindly
- Confirming a category rather than the exact target
- Skipping the dry run because the tool is internal

## Done when

- irreversible tools require a target-derived confirmation
- a mismatched confirmation is proven to be refused

## References

- [OWASP - fail-safe defaults](https://cheatsheetseries.owasp.org/)
- [MCP - security best practices](https://modelcontextprotocol.io/specification/2025-03-26/basic/security_best_practices)
