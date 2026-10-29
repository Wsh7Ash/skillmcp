---
name: input-schema-strictness
description: "Make the input schema the only place argument rules live, and refuse anything outside it. Use when a tool accepts structured arguments that a model will construct from context"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [design, schema, validation]
---

# Input Schema Strictness

> Make the input schema the only place argument rules live, and refuse anything outside it

**Use when:** a tool accepts structured arguments that a model will construct from context

**Avoid when:** the tool takes no arguments at all

## Procedure

1. List every argument, its type, and whether it is required
2. Declare enums for closed sets and bounds for numeric limits
3. Set additionalProperties to false so unknown keys are rejected
4. Validate again inside the handler, because the schema is advisory to the client
5. Return invalid-params with the offending key named
6. Test one rejection per rule so the schema is enforced, not documented

## Signals

- an unknown argument produces an invalid-params error
- an out-of-range number is refused rather than clamped silently
- the error message names the field and the expected shape
- the handler validation matches the declared schema exactly

## Patterns

**1. Closed object**

```text
"additionalProperties": false
```

**2. Bounded integer**

```text
"minimum": 1, "maximum": 50
```

**3. Typed error**

```text
invalid params: limit must be between 1 and 50
```

## Pitfalls

- Trusting client-side validation and skipping handler checks
- Silently clamping a value and returning success, which hides the client's bug
- Declaring an object where a string would be unambiguous for a model

## Done when

- every argument has a type and a required flag
- at least one rejection test exists per constraint

## References

- [JSON Schema - validation](https://json-schema.org/draft/2020-12/json-schema-validation.html)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
