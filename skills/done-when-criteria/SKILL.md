---
name: done-when-criteria
description: "Define completion as observable artifacts so a skill cannot be declared finished on vibes. Use when a procedure has several steps and the endpoint of the work is ambiguous"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [document, completion, discipline]
---

# Done When Criteria

> Define completion as observable artifacts so a skill cannot be declared finished on vibes

**Use when:** a procedure has several steps and the endpoint of the work is ambiguous

**Avoid when:** the skill is one mechanical action whose result is self-evident

## Procedure

1. Write what exists on disk when the skill is complete
2. Require at least one artifact a reviewer can open
3. Include a verification step that compares two artifacts
4. Avoid verbs like understand, consider or ensure
5. Check each criterion can be marked pass or fail without argument
6. Re-read after a session and confirm you actually produced each artifact

## Signals

- each criterion names a file, a pair or a captured response
- no criterion depends on an unstated judgement
- the criteria can be checked by someone else
- a session that skipped a criterion has a visible hole

## Patterns

**1. Artifact criterion**

```text
a baseline and candidate capture exist for the same target
```

**2. Verification criterion**

```text
a second run reproduces the same digest
```

**3. Rejected verb**

```text
understand the cache behaviour
```

## Pitfalls

- Writing completion criteria as feelings or intentions
- Requiring an artifact that the procedure never produces
- Making criteria so strict that routine work always fails them

## Done when

- every criterion is a pass or fail check on an artifact
- a completed session can be audited against the list

## References

- [NIST - documentation](https://csrc.nist.gov/)
- [OWASP - methodology](https://owasp.org/www-project-web-security-testing-guide/)
