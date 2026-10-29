---
name: concurrency-and-ordering-check
description: "Send several requests at once and confirm replies stay attributable and the server stays consistent. Use when the server indexes files or holds state that concurrent calls could race on"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [verify, concurrency, ordering]
---

# Concurrency and Ordering Check

> Send several requests at once and confirm replies stay attributable and the server stays consistent

**Use when:** the server indexes files or holds state that concurrent calls could race on

**Avoid when:** the server serialises all work by design and concurrency cannot occur

## Procedure

1. Write several requests with distinct ids
2. Send them without waiting for individual replies
3. Read replies and match each to its id
4. Check that no reply is missing or duplicated
5. Confirm the index was not left in a torn state after concurrent reads and one reload
6. Record the observed ordering for the notes, since it is not guaranteed

## Signals

- every id appears exactly once in the replies
- reply order differs from request order without breaking attribution
- a concurrent reload does not produce a partial index
- the server stays responsive throughout

## Patterns

**1. Distinct ids**

```text
requests 1..5 sent in one write
```

**2. Attribution**

```text
replies keyed by id, never by arrival order
```

**3. Torn state check**

```text
search after reload returns the same count
```

## Pitfalls

- Assuming replies arrive in request order
- Reloading the index mid-call and reading a half-built list
- Treating a duplicated id as harmless when it means a lost reply

## Done when

- every request id is answered exactly once
- the index is consistent after a concurrent reload

## References

- [JSON-RPC 2.0 - batch](https://www.jsonrpc.org/specification)
- [Python - threading](https://docs.python.org/3/library/threading.html)
