---
name: tool-call-error-paths
description: "Exercise each error path deliberately so a bad argument cannot produce a silent success. Use when a tool validates arguments and the failure branches are untested"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [verify, errors, testing]
---

# Tool Call Error Paths

> Exercise each error path deliberately so a bad argument cannot produce a silent success

**Use when:** a tool validates arguments and the failure branches are untested

**Avoid when:** the tool has no failure branches because it takes no input

## Procedure

1. Enumerate the failure branches in the handler
2. Send a request that triggers each one
3. Assert the error code and message for each case
4. Assert that none of them returns a success envelope
5. Check the server continues serving after each error
6. Add the cases to the fixture transcript

## Signals

- missing required argument returns invalid params
- out-of-range value returns invalid params with the key named
- unknown tool name returns invalid params listing alternatives
- each error leaves the server able to answer the next call

## Patterns

**1. Missing key**

```text
{"arguments": {}} for a required query
```

**2. Out of range**

```text
limit 500 -> invalid params
```

**3. Unknown tool**

```text
name 'nope' -> invalid params with the available list
```

## Pitfalls

- Testing only the happy path and shipping an error branch that returns success
- Asserting the message text so tightly that a wording change breaks CI
- Forgetting to re-check that the server still serves after an error

## Done when

- every failure branch has a request and an asserted error code
- post-error liveness is verified in the same test

## References

- [JSON-RPC 2.0 - errors](https://www.jsonrpc.org/specification)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
