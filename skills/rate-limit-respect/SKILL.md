---
name: rate-limit-respect
description: "Keep the server and its caller under whatever limits the target or host imposes. Use when tool calls cause outbound work, indexing scans or remote requests"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [govern, rate-limit, backpressure]
---

# Rate Limit Respect

> Keep the server and its caller under whatever limits the target or host imposes

**Use when:** tool calls cause outbound work, indexing scans or remote requests

**Avoid when:** the server only reads local files and has no external dependency

## Procedure

1. Identify the limit that applies: a host API quota, a filesystem scan cost or a client timeout
2. Add a small delay or token bucket where the limit is known
3. Return a clear backpressure message instead of a generic failure
4. Record the rate the server allows so callers can plan
5. Test a burst above the limit and confirm a predictable refusal
6. Never retry internally in a loop, which converts backpressure into an outage

## Signals

- a burst produces a refusal with a retry hint, not a hang
- the server's allowed rate is documented
- no internal retry loop exists
- the client can plan around a stated ceiling

## Patterns

**1. Token bucket**

```text
allow N calls per window, refuse the rest
```

**2. Backpressure message**

```text
rate limit: 10 calls/s, retry in 1s
```

**3. No silent retry**

```text
return the refusal instead of looping
```

## Pitfalls

- Retrying internally until the upstream blocks the whole server
- Refusing with a message that gives no retry guidance
- Applying a limit per process when several clients share the same quota

## Done when

- the allowed rate is documented and enforced
- an over-limit burst produces a predictable refusal

## References

- [RFC 6585 - 429 Too Many Requests](https://www.rfc-editor.org/rfc/rfc6585.html)
- [MCP - security best practices](https://modelcontextprotocol.io/specification/2025-03-26/basic/security_best_practices)
