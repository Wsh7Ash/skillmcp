---
name: server-discovery-and-trust
description: "Decide which third-party tool servers to load by reading what they do before granting them a call surface. Use when an agent is about to be pointed at a server you did not write"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [setup, trust, supply-chain]
---

# Server Discovery and Trust

> Decide which third-party tool servers to load by reading what they do before granting them a call surface

**Use when:** an agent is about to be pointed at a server you did not write

**Avoid when:** the server is internal, versioned and already reviewed by your own team

## Procedure

1. Identify the publisher and the exact version or commit being installed
2. Read the tool list and every description before enabling the server
3. Check what the server can reach: filesystem paths, network hosts, credentials
4. Prefer servers that read local files over ones that proxy network access
5. Pin the version so an upstream change cannot alter behaviour silently
6. Record the review in the project so the next person inherits the decision

## Signals

- the server's tools are read-only or clearly bounded
- the package is pinned to a commit rather than a floating tag
- the server requests no credentials it does not strictly need
- tool descriptions state what is read and what is written

## Patterns

**1. Pinned install**

```text
pip install skillmcp==1.0.0
```

**2. Surface review**

```text
list_packs, search_skills, get_skill: read-only
```

**3. Reach check**

```text
reads a local packs directory, no network
```

## Pitfalls

- Loading a server because its description sounds useful without reading its tools
- Granting filesystem access to a server that only needs one directory
- Trusting a floating tag that could be repointed at any time

## Done when

- the tool list of every third-party server has been read and recorded
- each server is pinned to a version or commit

## References

- [MCP - security best practices](https://modelcontextprotocol.io/specification/2025-03-26/basic/security_best_practices)
- [OWASP - supply chain risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
