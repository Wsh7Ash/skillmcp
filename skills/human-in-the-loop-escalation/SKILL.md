---
name: human-in-the-loop-escalation
description: "Define the decisions an agent must hand back to a person instead of making alone. Use when an agent can act on systems where a wrong call is expensive or irreversible"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [govern, escalation, process]
---

# Human in the Loop Escalation

> Define the decisions an agent must hand back to a person instead of making alone

**Use when:** an agent can act on systems where a wrong call is expensive or irreversible

**Avoid when:** the workflow is entirely read-only and reversible

## Procedure

1. List decisions with irreversible or external effect
2. Write the trigger for each: monetary, destructive, legal or scope crossing
3. Make the agent stop and state the decision it needs
4. Include the evidence and the options with their consequences
5. Record the human decision so it is auditable later
6. Re-check the list when the toolchain gains new capability

## Signals

- irreversible actions have a named human approver
- the escalation message contains evidence, not just a question
- the decision is recorded with who made it
- new tools trigger a review of the escalation list

## Patterns

**1. Trigger list**

```text
delete, publish, or any target outside scope
```

**2. Escalation message**

```text
decision needed: publish pack to production
```

**3. Decision record**

```text
approved by operator at 2026-10-29T08:12Z
```

## Pitfalls

- Escalating everything, which trains the human to approve without reading
- Escalating after acting rather than before
- Leaving the escalation list unchanged after adding a destructive tool

## Done when

- every irreversible action has a named human approver
- escalations include evidence and are recorded

## References

- [NIST - human factors](https://csrc.nist.gov/)
- [OWASP - secure design](https://cheatsheetseries.owasp.org/)
