---
name: when-to-use-and-avoid
description: "State both conditions so an agent can decline a skill that does not fit the target. Use when a skill is broad enough to be tempting in situations where it is wrong"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [document, selection, clarity]
---

# When to Use and Avoid

> State both conditions so an agent can decline a skill that does not fit the target

**Use when:** a skill is broad enough to be tempting in situations where it is wrong

**Avoid when:** the skill is a narrow mechanical step with no plausible misapplication

## Procedure

1. Write the use-when clause as an observable condition, not a topic
2. Write the avoid-when clause as the situation where it misleads
3. Check the clauses do not overlap
4. Make both clauses specific enough to be checked against a target
5. Add a signal that reveals the avoid-when condition early
6. Re-read after a failed engagement and refine from the failure

## Signals

- the use-when clause names something observable in a capture or request
- the avoid-when clause names a concrete exclusion
- the two clauses cannot both be true
- an early signal warns when the avoid condition holds

## Patterns

**1. Observable use**

```text
a cacheable response reflects a query value
```

**2. Concrete avoid**

```text
response carries no-store on every request
```

**3. Early warning**

```text
age header is zero on repeats, so nothing is cached
```

## Pitfalls

- Writing 'use when testing caching', which is a topic and not a condition
- Omitting avoid-when so the skill is applied everywhere
- Making the clauses so broad they are always true

## Done when

- both clauses are observable and mutually exclusive
- at least one signal reveals the avoid condition early

## References

- [Anthropic - skills](https://docs.anthropic.com/en/docs/claude-code)
- [OWASP - methodology](https://owasp.org/www-project-web-security-testing-guide/)
