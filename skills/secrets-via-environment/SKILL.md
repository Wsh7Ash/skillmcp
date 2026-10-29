---
name: secrets-via-environment
description: "Pass credentials through the environment so they never appear in process arguments or config files. Use when a tool server needs a token to call an external service on the agent's behalf"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [setup, secrets, process]
---

# Secrets Via Environment

> Pass credentials through the environment so they never appear in process arguments or config files

**Use when:** a tool server needs a token to call an external service on the agent's behalf

**Avoid when:** the server needs no credential and reads only local files

## Procedure

1. Identify every credential the server needs at runtime
2. Read each one from the environment inside the server, failing clearly when absent
3. Keep the value out of argv, config files and log lines
4. Ensure error messages never echo the value back
5. Set the variables in the launching environment, not in a committed file
6. Verify the server refuses to start when a required variable is missing

## Signals

- the server fails fast with a message naming the missing variable, not its value
- process listings show no credential
- logs contain no token material after a failure
- the config file holds a reference, never the secret

## Patterns

**1. Read at startup**

```text
token = os.environ["HUNT_TOKEN"]
```

**2. Clear failure**

```text
missing HUNT_TOKEN in environment; refusing to start
```

**3. Redacted log**

```text
token: [set] or [unset]
```

## Pitfalls

- Passing a token as a command line argument where every process can read it
- Logging the full request headers when an error occurs
- Using a default placeholder secret that silently works in production

## Done when

- no credential appears in argv, config or logs
- a missing variable produces a clear startup failure

## References

- [OWASP - secrets management](https://cheatsheetseries.owasp.org/)
- [MCP - security best practices](https://modelcontextprotocol.io/specification/2025-03-26/basic/security_best_practices)
