---
name: data-retention-policy
description: "Decide how long tool inputs, outputs and logs live, and make deletion real rather than implied. Use when the server stores captures, findings or credentials-adjacent data"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [govern, retention, privacy]
---

# Data Retention Policy

> Decide how long tool inputs, outputs and logs live, and make deletion real rather than implied

**Use when:** the server stores captures, findings or credentials-adjacent data

**Avoid when:** the server keeps nothing beyond process memory

## Procedure

1. List every artifact the server writes and where
2. Assign each a retention period based on the engagement rules
3. Implement deletion for the shortest-lived class first
4. Verify deletion removes the bytes rather than only the index entry
5. Document the periods where a reviewer can find them
6. Re-test deletion after any change to the storage layout

## Signals

- each stored artifact class has a stated period
- deletion removes files, not only references
- the documented periods match the implementation
- no orphaned file remains after a retention sweep

## Patterns

**1. Artifact classes**

```text
logs: 30 days, captures: engagement end, indexes: ephemeral
```

**2. Real delete**

```text
unlink the file and confirm the path is gone
```

**3. Documented**

```text
retention table in SECURITY.md
```

## Pitfalls

- Deleting the index entry while the file remains on disk
- Keeping captures indefinitely because they were useful once
- Documenting a period that no code enforces

## Done when

- every artifact class has an enforced retention period
- deletion is verified at the filesystem level

## References

- [NIST - data retention](https://csrc.nist.gov/)
- [OWASP - privacy risks](https://owasp.org/www-project-top-10-privacy-risks/)
