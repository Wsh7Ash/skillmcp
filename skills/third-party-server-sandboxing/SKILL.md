---
name: third-party-server-sandboxing
description: "Run untrusted tool servers with the smallest filesystem and network reach that still works. Use when a server you did not write is part of the toolchain"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [govern, sandbox, isolation]
---

# Third Party Server Sandboxing

> Run untrusted tool servers with the smallest filesystem and network reach that still works

**Use when:** a server you did not write is part of the toolchain

**Avoid when:** the server is written and reviewed in-house with matching review history

## Procedure

1. Determine the directories and hosts the server must reach
2. Run it as a user with access to only those paths
3. Block outbound network access when the server is a local reader
4. Give it a read-only mount for content it should not modify
5. Check the server still works under the restriction
6. Record the sandbox in the README so it survives reinstallation

## Signals

- the server cannot read outside its granted directory
- outbound connections fail for a server that should not make any
- writes to the read-only mount are refused
- the server's documented purpose still works under restriction

## Patterns

**1. Read-only mount**

```text
bind mount packs as ro
```

**2. No egress**

```text
container with no network namespace
```

**3. User scope**

```text
run as a dedicated unprivileged user
```

## Pitfalls

- Running a third-party server as your own user with home directory access
- Granting network access because installation was easier that way
- Sandboxing so tightly that the server silently returns empty results

## Done when

- the server runs with the documented minimal reach
- a read outside its grant is proven to fail

## References

- [NIST - zero trust architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [OWASP - supply chain](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
