---
name: local-vs-remote-boundary
description: "Keep a local file-reading server local, and state the trust boundary before anything crosses it. Use when a tool server could be exposed on a port to serve several agents"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [setup, boundary, network]
---

# Local Versus Remote Boundary

> Keep a local file-reading server local, and state the trust boundary before anything crosses it

**Use when:** a tool server could be exposed on a port to serve several agents

**Avoid when:** the server only ever serves one client on one machine

## Procedure

1. Write down what the server can read and write today
2. Decide whether a remote caller could reach sensitive files through the same tools
3. Keep the server on stdio unless a second client genuinely needs it
4. If exposing it, add authentication before the first remote request
5. Restrict the reachable paths to the packs root only
6. Re-run the surface review after the transport change, not before

## Signals

- a remote caller cannot read paths outside the packs root
- the server refuses requests without a valid credential
- the tool list is identical local and remote, so behaviour is predictable
- logs distinguish local from remote callers

## Patterns

**1. Path confinement**

```text
resolve(path).is_relative_to(packs_root) before reading
```

**2. Credential gate**

```text
reject when the token header is absent
```

**3. Boundary note**

```text
local: same user; remote: authenticated agents only
```

## Pitfalls

- Exposing a stdio server behind a socket shim and inheriting no authentication
- Assuming a private network is a security boundary
- Forgetting that a read tool becomes a data-exfiltration path once remote

## Done when

- the trust boundary is written down next to the transport choice
- any remote exposure has authentication and path confinement

## References

- [MCP - security best practices](https://modelcontextprotocol.io/specification/2025-03-26/basic/security_best_practices)
- [NIST - zero trust architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
