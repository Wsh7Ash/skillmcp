---
name: tools-list-schema-validation
description: "Validate every advertised schema as JSON Schema before a client tries to obey it. Use when a tool's input schema was edited and clients construct arguments from it"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [verify, schema, tools]
---

# Tools List Schema Validation

> Validate every advertised schema as JSON Schema before a client tries to obey it

**Use when:** a tool's input schema was edited and clients construct arguments from it

**Avoid when:** the tool takes no arguments and its schema is a constant empty object

## Procedure

1. Read tools/list output and collect every inputSchema
2. Check each schema is an object with type object and a properties map
3. Check required names exist in properties
4. Check enums are non-empty and defaults satisfy their own constraints
5. Check additionalProperties is explicitly false where strictness is intended
6. Add the checks to the test suite so a schema edit cannot regress

## Signals

- no required key is missing from properties
- every enum has at least one value
- no default value violates its own bounds
- strict tools declare additionalProperties false

## Patterns

**1. Required check**

```text
set(schema['required']) <= set(schema['properties'])
```

**2. Bounds check**

```text
1 <= default <= maximum
```

**3. Strictness**

```text
additionalProperties is False, not absent
```

## Pitfalls

- Assuming a client validates the schema and finding out it does not
- Leaving a default outside its own min or max
- Declaring required keys that the handler treats as optional

## Done when

- every advertised schema passes the structural checks
- the checks run in CI on every change

## References

- [JSON Schema - validation](https://json-schema.org/draft/2020-12/json-schema-validation.html)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
