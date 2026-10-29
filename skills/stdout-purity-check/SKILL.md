---
name: stdout-purity-check
description: "Assert that stdout carries only protocol messages, because one stray print breaks every client. Use when the server logs, warns or prints anything during normal operation"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [verify, stdio, protocol]
---

# Stdout Purity Check

> Assert that stdout carries only protocol messages, because one stray print breaks every client

**Use when:** the server logs, warns or prints anything during normal operation

**Avoid when:** the server is not a stdio transport and has no dedicated protocol channel

## Procedure

1. Run the server and capture stdout separately from stderr
2. Parse every stdout line as JSON
3. Fail the test when any line is not a JSON-RPC message
4. Trigger a warning path and confirm it appears on stderr only
5. Check the process exit path for a trailing print
6. Add the check to CI so a new log statement cannot sneak in

## Signals

- every stdout line parses as a JSON object with a jsonrpc field
- warnings appear on stderr
- the exit path prints nothing to stdout
- a deliberately injected print makes the test fail

## Patterns

**1. Split streams**

```text
stdout=protocol, stderr=diagnostics
```

**2. Line parse**

```text
json.loads(line) for every non-empty stdout line
```

**3. Injected failure**

```text
temporarily print('debug') and expect a failing test
```

## Pitfalls

- Using the default logging configuration, which writes to stdout
- Printing a startup banner for humans, which the client tries to parse
- Capturing both streams together in the test and missing the leak

## Done when

- every stdout line parses as JSON during a full session
- a diagnostic on stderr is proven not to reach stdout

## References

- [MCP - transports](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
- [Python - logging](https://docs.python.org/3/library/logging.html)
