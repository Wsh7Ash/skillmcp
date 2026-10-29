---
name: protocol-conformance-test
description: "Test the wire protocol directly, so a client bug and a server bug are distinguishable. Use when a client reports a failure and the server's own behaviour is unproven"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [verify, protocol, testing]
---

# Protocol Conformance Test

> Test the wire protocol directly, so a client bug and a server bug are distinguishable

**Use when:** a client reports a failure and the server's own behaviour is unproven

**Avoid when:** the server is a thin library wrapper with no wire protocol of its own

## Procedure

1. Write the exact JSON-RPC lines the client should send
2. Pipe them into the server process with a bounded timeout
3. Assert the response shape, not only the presence of a reply
4. Check the jsonrpc field, id echo and error codes
5. Repeat for a malformed line and for an unknown method
6. Keep the transcript as a fixture so the test is reproducible

## Signals

- every response echoes the request id
- malformed input produces a parse error, not a crash
- an unknown method produces method-not-found
- the server keeps serving after an error line

## Patterns

**1. Piped transcript**

```text
printf '%s\n' '{"jsonrpc":"2.0",...}' | python -m skillmcp serve
```

**2. Shape assertion**

```text
jsonrpc == '2.0' and id == sent id
```

**3. Survival check**

```text
send a bad line, then a good one, expect two replies
```

## Pitfalls

- Testing through the client library, which hides the raw response
- Asserting only that some output appeared
- Forgetting that a server which crashes on a bad line fails every later call

## Done when

- happy path, malformed line and unknown method each have a fixture
- the server is shown to survive an error line

## References

- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
- [MCP - lifecycle](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle)
