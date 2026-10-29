---
name: credential-isolation
description: "Give the server its own credential scope so a compromised tool call cannot reach everything. Use when the server calls an upstream service on behalf of the agent"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [govern, credentials, least-privilege]
---

# Credential Isolation

> Give the server its own credential scope so a compromised tool call cannot reach everything

**Use when:** the server calls an upstream service on behalf of the agent

**Avoid when:** the server needs no credential at all, which is the preferred design

## Procedure

1. List what the server must do upstream and the scopes that allows
2. Provision a credential limited to exactly those scopes
3. Keep it separate from any human operator credential
4. Store it only in the launching environment
5. Verify a call outside the granted scope fails
6. Record the scope in the README so it is reviewed with the server

## Signals

- the scope list matches the documented purpose
- a call outside the scope is refused by the upstream
- the credential differs from the operator's own
- no scope grants broader access than the tool needs

## Patterns

**1. Scoped token**

```text
read-only packs scope, no write scope
```

**2. Negative proof**

```text
write attempt returns 403 from upstream
```

**3. Documented**

```text
requires: read access to the packs API only
```

## Pitfalls

- Reusing a personal admin token because it was already in the environment
- Granting write scope for a tool that only reads
- Sharing one credential across several servers, so revocation breaks all

## Done when

- the server's credential scope is minimal and documented
- a call beyond the scope is proven to fail

## References

- [OWASP - secrets management](https://cheatsheetseries.owasp.org/)
- [NIST - least privilege](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
