---
name: least-privilege-tool-grants
description: "Grant the agent only the tools it needs for the current task, not the whole server surface. Use when a client can restrict which tools an agent may call"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [govern, least-privilege, grants]
---

# Least Privilege Tool Grants

> Grant the agent only the tools it needs for the current task, not the whole server surface

**Use when:** a client can restrict which tools an agent may call

**Avoid when:** the client offers no per-tool restriction and the server must self-limit

## Procedure

1. List the tools needed for the current task and justify each
2. Disable the rest in the client configuration where supported
3. Where the client cannot restrict, split servers by capability
4. Re-check the grant list at the start of each phase
5. Record the granted set with the session notes
6. Revoke grants that no longer serve the task

## Signals

- the enabled set is smaller than the full tool list
- each enabled tool maps to a task step
- server splitting keeps write tools on a separate connection
- grants are reviewed per phase, not once per project

## Patterns

**1. Task set**

```text
search_skills, get_skill only
```

**2. Split servers**

```text
read server and write server as separate processes
```

**3. Phase review**

```text
authz phase enables cross-role tools only
```

## Pitfalls

- Enabling everything because disabling is tedious
- Granting write tools for a read-only analysis task
- Reviewing grants once and never again after scope narrows

## Done when

- the enabled tool set is justified tool by tool
- grants are reviewed at each phase boundary

## References

- [NIST - least privilege](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [MCP - security best practices](https://modelcontextprotocol.io/specification/2025-03-26/basic/security_best_practices)
