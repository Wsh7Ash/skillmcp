---
name: idempotency-annotation
description: "Mark which tools change state so a retry after a timeout cannot duplicate an action. Use when a tool writes to disk, sends a request or mutates a remote record"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [design, idempotency, retries]
---

# Idempotency Annotation

> Mark which tools change state so a retry after a timeout cannot duplicate an action

**Use when:** a tool writes to disk, sends a request or mutates a remote record

**Avoid when:** every tool is a pure read, which is the safest design for a skill server

## Procedure

1. Classify each tool as read, write or destructive
2. Say which class it is in the tool description, in plain words
3. Design writes to be idempotent where possible, keyed by content or id
4. Refuse retries of destructive tools without an explicit identifier
5. Log the identifier so a duplicate can be recognised later
6. Test a repeated identical write and confirm no second effect

## Signals

- a repeated write with the same key produces one effect
- the description states whether the call mutates state
- destructive tools require an explicit target argument
- logs show the key that made the operation idempotent

## Patterns

**1. Class in words**

```text
read-only: returns indexed skills, changes nothing
```

**2. Content key**

```text
idempotency key = sha256(payload)
```

**3. Refusal shape**

```text
refusing repeat delete without an explicit id
```

## Pitfalls

- Leaving idempotency implicit and letting an agent retry a write
- Making every write destructive and unguarded because the tool is internal
- Hashing a payload that includes a timestamp, which defeats the key

## Done when

- each tool states whether it mutates state
- a repeated identical write is proven to have one effect

## References

- [RFC 9110 - idempotent methods](https://www.rfc-editor.org/rfc/rfc9110.html)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
