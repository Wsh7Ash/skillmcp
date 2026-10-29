---
name: one-procedure-per-skill
description: "Keep each skill to a single reproducible procedure so an agent can follow it without branching. Use when a skill has grown into a survey of several unrelated techniques"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [document, scope, structure]
---

# One Procedure Per Skill

> Keep each skill to a single reproducible procedure so an agent can follow it without branching

**Use when:** a skill has grown into a survey of several unrelated techniques

**Avoid when:** the steps genuinely form one sequence that cannot be split

## Procedure

1. Read the skill and name the single outcome it produces
2. Split any step that serves a different outcome into its own skill
3. Give each split skill a title that states its outcome
4. Check the cross-references point at the new slugs
5. Confirm the original skill still stands alone
6. Re-run the corpus validator after the split

## Signals

- the skill has one stated outcome and one done-when set
- no step could be executed independently of the others
- the title matches the outcome
- the validator passes after restructuring

## Patterns

**1. Single outcome**

```text
produce a cache key verdict, not 'test caching'
```

**2. Split decision**

```text
vary inspection separated from poisoning probes
```

**3. Cross-reference**

```text
see also: cache-key-header-probe
```

## Pitfalls

- Keeping a catch-all skill because splitting feels like admin work
- Splitting so finely that each skill has three trivial steps
- Leaving dangling references after a split

## Done when

- each skill names exactly one outcome
- every split skill passes the validator standalone

## References

- [OWASP - methodology](https://owasp.org/www-project-web-security-testing-guide/)
- [Anthropic - skills](https://docs.anthropic.com/en/docs/claude-code)
