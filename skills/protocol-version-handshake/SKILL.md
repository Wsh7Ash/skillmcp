---
name: protocol-version-handshake
description: "Negotiate the protocol revision explicitly and pin the one the server actually implements. Use when the client may run a different protocol revision than the server was written against"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [setup, mcp, protocol]
---

# Protocol Version Handshake

> Negotiate the protocol revision explicitly and pin the one the server actually implements

**Use when:** the client may run a different protocol revision than the server was written against

**Avoid when:** server and client ship together and are upgraded as one unit

## Procedure

1. Read the client's requested protocolVersion from the initialize params
2. Decide the revision the server implements and state it in the response
3. Reject or downgrade gracefully when the client asks for an unsupported revision
4. Record the pinned revision in the README and in a constant
5. Assert the revision in a conformance test so a silent change is caught
6. Log both versions at handshake time to stderr for diagnosis

## Signals

- the initialize response names a revision the server genuinely implements
- a mismatched client revision produces a clear error instead of odd behaviour
- the pinned constant appears in exactly one place in the code
- the conformance test fails when the constant is edited without the docs

## Patterns

**1. Pinned constant**

```text
PROTOCOL_VERSION = "2025-03-26"
```

**2. Response shape**

```text
{"protocolVersion": PROTOCOL_VERSION, "capabilities": {...}}
```

**3. Diagnostic log**

```text
handshake: client=2024-11-05 server=2025-03-26
```

## Pitfalls

- Echoing the client's requested version without implementing it
- Scattering the version string through the code so a change is partial
- Treating a version mismatch as a transport failure and retrying forever

## Done when

- the server names one revision in a single constant and returns it
- a test asserts the returned revision equals the constant

## References

- [MCP - lifecycle](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle)
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
