---
name: verify-tool-output-before-reporting
description: "Treat tool output as an observation to check, never as a conclusion to publish. Use when a tool result will be quoted in a report, ticket or decision"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [invoke, verification, evidence]
---

# Verify Tool Output Before Reporting

> Treat tool output as an observation to check, never as a conclusion to publish

**Use when:** a tool result will be quoted in a report, ticket or decision

**Avoid when:** the output is a step toward a later measurement that will be verified anyway

## Procedure

1. Read what the tool claims and what it actually returned
2. Check the claim against the raw artifact, not against the formatted summary
3. Re-run the call once to confirm the output is stable
4. Confirm the output's scope matches the question you asked
5. Note the tool version and arguments beside the quoted result
6. Report only what you can re-derive from the artifact

## Signals

- the quoted text appears in the artifact at the cited location
- a rerun produces the same result
- the answer addresses the question that was actually asked
- the tool version and arguments appear with the quote

## Patterns

**1. Claim versus artifact**

```text
summary says 50 skills; pack.json says skill_count 50
```

**2. Rerun check**

```text
same call twice, identical output
```

**3. Provenance**

```text
skillmcp 1.0.0, search_skills("cache")
```

## Pitfalls

- Quoting a formatted summary as if it were the underlying data
- Publishing a first-run result that changes on a second run
- Reporting an answer to a different question than the one asked

## Done when

- every quoted result is traceable to an artifact and a rerun
- the tool version and arguments accompany the quote

## References

- [OWASP - evidence handling](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST - evidence integrity](https://csrc.nist.gov/)
