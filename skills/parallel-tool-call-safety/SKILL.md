---
name: parallel-tool-call-safety
description: "Only parallelise calls that are independent, and never parallelise anything that writes. Use when several lookups are needed and latency matters"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [invoke, concurrency, safety]
---

# Parallel Tool Call Safety

> Only parallelise calls that are independent, and never parallelise anything that writes

**Use when:** several lookups are needed and latency matters

**Avoid when:** calls depend on each other's output, which makes parallelism meaningless

## Procedure

1. List the calls and mark each as read or write
2. Group the reads; leave writes in their own sequential group
3. Confirm no read depends on another read's result
4. Send the independent reads together
5. Order the writes explicitly by their dependency
6. Reconcile results by call identity, never by arrival order

## Signals

- independent reads complete in one round of latency
- writes are serialised and ordered
- each result is attributed to the exact call that produced it
- a failed read does not cancel the others silently

## Patterns

**1. Read batch**

```text
three searches with different keywords at once
```

**2. Write queue**

```text
index rebuild then publish, in order
```

**3. Identity keyed**

```text
results matched by call id, not position
```

## Pitfalls

- Parallelising two writes that touch the same file
- Assuming response order matches request order
- Cancelling a batch because one call errored, losing the successful results

## Done when

- every parallel group contains only independent reads
- results are attributed by call identity

## References

- [JSON-RPC 2.0 - batch](https://www.jsonrpc.org/specification)
- [MCP - transports](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
