---
name: capability-negotiation-check
description: "Declare only the capabilities the server implements and refuse calls outside them. Use when the server exposes tools and the client must know whether to look for resources or prompts"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [setup, mcp, capabilities]
---

# Capability Negotiation Check

> Declare only the capabilities the server implements and refuse calls outside them

**Use when:** the server exposes tools and the client must know whether to look for resources or prompts

**Avoid when:** the server is a thin wrapper over one tool and capability breadth is irrelevant

## Procedure

1. List what the server can do: tools, resources, prompts, sampling
2. Declare exactly that subset in the initialize response
3. Return method-not-found for capabilities that were not declared
4. Verify the client only calls what was advertised
5. Add a test that asserts undeclared capabilities are refused
6. Update the declaration the same commit a new capability ships

## Signals

- the response capabilities block matches the implemented handlers
- an undeclared method returns a JSON-RPC method-not-found error
- the client hides features the server did not advertise
- a new handler without a capability entry is caught by the test

## Patterns

**1. Tools only**

```text
"capabilities": {"tools": {"listChanged": false}}
```

**2. Refusal shape**

```text
method_not_found for resources/list when undeclared
```

**3. Parity test**

```text
declared capabilities == implemented handlers
```

## Pitfalls

- Declaring resources because a future version might add them
- Leaving an undeclared handler reachable, which clients will not exercise and tests will not cover
- Forgetting listChanged semantics when the tool list is dynamic

## Done when

- declared capabilities match implemented handlers exactly
- undeclared methods return a clean JSON-RPC error

## References

- [MCP - server capabilities](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle)
- [MCP - tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)
