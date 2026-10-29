---
name: argument-construction-from-artifacts
description: "Build tool arguments from captured artifacts rather than from memory, so ids and paths are exact. Use when a tool needs an identifier that already exists in a capture, report or file"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [invoke, arguments, accuracy]
---

# Argument Construction From Artifacts

> Build tool arguments from captured artifacts rather than from memory, so ids and paths are exact

**Use when:** a tool needs an identifier that already exists in a capture, report or file

**Avoid when:** the argument is a free-text query with no exactness requirement

## Procedure

1. Locate the artifact that holds the exact value
2. Copy the value rather than retyping it
3. Confirm the value's shape against the schema before the call
4. Pass the smallest necessary set of arguments
5. Check the returned record refers to the same identifier
6. Record the source artifact beside the call for traceability

## Signals

- the identifier in the call is byte-identical to the one in the artifact
- the result references the same object, not a similar one
- no argument was reconstructed from memory
- the source file path appears in the notes

## Patterns

**1. Copy not retype**

```text
slug taken from pack.json rather than the report
```

**2. Shape check**

```text
value matches ^[a-z0-9]+(-[a-z0-9]+)*$ before the call
```

**3. Traceability**

```text
argument source: results/catalog.md line 42
```

## Pitfalls

- Reconstructing a UUID or hash from memory and getting a near-miss
- Passing a display name where the tool expects a slug
- Losing the artifact reference so the call cannot be audited

## Done when

- every exact-value argument is copied from a named artifact
- the result is confirmed to reference the same identifier

## References

- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
- [NIST - evidence handling](https://csrc.nist.gov/)
