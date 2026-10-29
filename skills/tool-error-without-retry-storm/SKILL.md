---
name: tool-error-without-retry-storm
description: "Distinguish transient from deterministic tool failures so a retry cannot become a loop. Use when a tool call fails and the next action is still undecided"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [invoke, errors, retries]
---

# Tool Error Without Retry Storm

> Distinguish transient from deterministic tool failures so a retry cannot become a loop

**Use when:** a tool call fails and the next action is still undecided

**Avoid when:** the tool is known to be idempotent and free, where retries cost nothing

## Procedure

1. Read the error text and classify it as transient or deterministic
2. Retry at most once for a transient error, with the same arguments
3. Never retry a deterministic error such as an unknown slug
4. Change the input when the error names a bad argument
5. Record the classification so the same failure is not re-tested
6. Escalate to the user only when the cause is outside your control

## Signals

- a deterministic error is not retried with identical arguments
- one retry is attempted and then abandoned for transient failures
- the error text names an input you can fix
- the notes state the classification and the action taken

## Patterns

**1. Classify**

```text
unknown skill -> deterministic; socket timeout -> transient
```

**2. Single retry**

```text
attempt 2 uses identical arguments and then stops
```

**3. Input fix**

```text
limit 500 -> invalid params -> resend with 50
```

## Pitfalls

- Retrying an unknown-slug error five times with the same spelling
- Treating a rate limit as a bug in the tool rather than backpressure
- Swallowing the error text and reporting a generic failure

## Done when

- each failure is classified and the action recorded
- no deterministic error is retried unchanged

## References

- [JSON-RPC 2.0 - errors](https://www.jsonrpc.org/specification)
- [Anthropic - tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
