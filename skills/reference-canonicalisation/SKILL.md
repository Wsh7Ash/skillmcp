---
name: reference-canonicalisation
description: "Cite canonical https references so a link keeps working after the pack is published. Use when a skill cites a specification, vendor document or research post"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [document, references, durability]
---

# Reference Canonicalisation

> Cite canonical https references so a link keeps working after the pack is published

**Use when:** a skill cites a specification, vendor document or research post

**Avoid when:** the skill is entirely self-contained and cites nothing external

## Procedure

1. Prefer the standards body or vendor's own documentation over a blog summary
2. Use https and the canonical host, never a mirror or a redirector
3. Cite the specific page, not the site root
4. Check the link resolves before committing
5. Replace a dead link with the archived canonical page
6. Keep one to three references so the list stays meaningful

## Signals

- every reference is https and resolves
- the cited page covers the claim in the skill
- no reference points at a search result page
- the reference list is short and specific

## Patterns

**1. Canonical**

```text
https://www.rfc-editor.org/rfc/rfc9112.html
```

**2. Specific page**

```text
a named cheat sheet page, not the index
```

**3. Archived fallback**

```text
web archive copy when the primary is gone
```

## Pitfalls

- Citing a blog that summarises the RFC instead of the RFC
- Using http and relying on a redirect that later changes
- Linking a site root so the reader cannot find the claim

## Done when

- every reference is canonical, specific and resolving
- the validator enforces the https form

## References

- [RFC 9112 - HTTP/1.1 messaging](https://www.rfc-editor.org/rfc/rfc9112.html)
- [OWASP - cheat sheet series](https://cheatsheetseries.owasp.org/)
