---
name: replay-transcript-for-regression
description: "Re-run a stored session against a new build to catch protocol drift before a client does. Use when the server is about to be released and its wire behaviour must not change"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [verify, regression, release]
---

# Replay Transcript For Regression

> Re-run a stored session against a new build to catch protocol drift before a client does

**Use when:** the server is about to be released and its wire behaviour must not change

**Avoid when:** the release intentionally changes the protocol and new fixtures were written

## Procedure

1. Pick the transcript that covers the most client-visible behaviour
2. Run it against the previous build and store the output as the baseline
3. Run it against the new build with identical input
4. Compare semantically, ignoring declared volatile fields
5. Investigate every difference before deciding it is intended
6. Publish the new baseline only with the release notes that explain it

## Signals

- the replay completes without a timeout or crash
- differences are limited to fields the release intended to change
- the baseline file is committed with the release
- a deliberate change appears in the changelog

## Patterns

**1. Baseline pair**

```text
transcript-before.jsonl and transcript-after.jsonl
```

**2. Semantic compare**

```text
parse both, drop volatile fields, diff
```

**3. Explained diff**

```text
new field 'instructions' added in 1.1.0
```

## Pitfalls

- Comparing raw bytes and failing on key ordering
- Accepting a diff without checking it against the release intent
- Replaying without a timeout so a hung build blocks the release

## Done when

- a baseline exists for the previous build and is compared semantically
- every difference is either explained in the changelog or fixed

## References

- [MCP - lifecycle](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle)
- [Semantic versioning](https://semver.org/)
