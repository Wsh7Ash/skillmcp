---
name: signal-and-pitfall-sections
description: "Write signals as observations and pitfalls as the mistakes that produce false findings. Use when a skill needs to help a reader decide mid-procedure whether they are on track"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [document, signals, pitfalls]
---

# Signal and Pitfall Sections

> Write signals as observations and pitfalls as the mistakes that produce false findings

**Use when:** a skill needs to help a reader decide mid-procedure whether they are on track

**Avoid when:** the procedure is entirely deterministic and has no judgement step

## Procedure

1. List the observations that confirm the skill is working
2. Phrase each as something visible in a response, header or byte count
3. List the mistakes that have produced false positives for this technique
4. Phrase each pitfall as a specific action to avoid
5. Remove any signal that is really an interpretation
6. Check the pitfalls against your own past notes

## Signals

- each signal can be verified from a capture
- each pitfall names a concrete wrong action
- no signal restates a step
- the pitfalls explain a class of false positive

## Patterns

**1. Observable signal**

```text
age header resets to zero when the header changes
```

**2. Actionable pitfall**

```text
replaying a POST that creates a record each time
```

**3. Removed signal**

```text
looks suspicious: too vague to verify
```

## Pitfalls

- Writing signals that are conclusions rather than observations
- Listing pitfalls that are just restatements of the steps
- Omitting the false-positive class that this technique invites

## Done when

- every signal is verifiable from captured evidence
- every pitfall names an action and the false finding it causes

## References

- [OWASP - reporting](https://owasp.org/www-project-web-security-testing-guide/)
- [Anthropic - skills](https://docs.anthropic.com/en/docs/claude-code)
