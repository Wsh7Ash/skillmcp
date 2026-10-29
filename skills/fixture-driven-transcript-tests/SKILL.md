---
name: fixture-driven-transcript-tests
description: "Keep a request/response transcript on disk and assert the server still matches it. Use when a protocol server has behaviours that must not drift across refactors"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [verify, fixtures, regression]
---

# Fixture Driven Transcript Tests

> Keep a request/response transcript on disk and assert the server still matches it

**Use when:** a protocol server has behaviours that must not drift across refactors

**Avoid when:** the server output is intentionally non-deterministic, such as timestamped logs

## Procedure

1. Record one transcript per behaviour: handshake, search, fetch, error
2. Store requests and expected responses as separate JSON lines
3. Drive the server with the request lines in a subprocess
4. Compare the meaningful fields, ignoring volatile ones such as paths
5. Fail the test on any unexpected field or missing reply
6. Update the fixture in the same commit as an intended behaviour change

## Signals

- each transcript replays with identical semantic output
- volatile fields are named in an ignore list
- a deliberate behaviour change requires a fixture update in the same commit
- the fixture set covers happy and error paths

## Patterns

**1. Pair files**

```text
handshake.requests.jsonl and handshake.expected.jsonl
```

**2. Ignore list**

```text
ignore: serverInfo.version when bumped deliberately
```

**3. Diff on failure**

```text
print the first differing field, not the whole payload
```

## Pitfalls

- Asserting the whole response including volatile fields, so tests fail for no reason
- Regenerating fixtures blindly to make CI green
- Testing through a client library that reformats the response

## Done when

- each behaviour has a committed transcript that replays identically
- volatile fields are excluded by an explicit list

## References

- [MCP - lifecycle](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle)
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
