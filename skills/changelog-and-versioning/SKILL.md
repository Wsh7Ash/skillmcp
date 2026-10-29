---
name: changelog-and-versioning
description: "Version a pack so consumers know when a skill's meaning changed, not just its wording. Use when a pack is consumed by another project, an agent runtime or a pinned install"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [document, versioning, release]
---

# Changelog and Versioning

> Version a pack so consumers know when a skill's meaning changed, not just its wording

**Use when:** a pack is consumed by another project, an agent runtime or a pinned install

**Avoid when:** the pack is a single private draft with one consumer reading the source

## Procedure

1. Decide the versioning rule: major for a slug removal, minor for an addition
2. Write changelog entries in terms of behaviour, not of edits
3. Bump pack.json version and the changelog in the same commit
4. Tag the release so consumers can pin it
5. Announce removals with the replacement slug
6. Re-render the pack after the bump and re-run the validator

## Signals

- the version in pack.json matches the changelog entry
- removals name a replacement
- the release tag matches the version string
- a consumer can pin and re-pin deliberately

## Patterns

**1. Version rule**

```text
major: slug removed; minor: skill added
```

**2. Behavioural entry**

```text
replay now reports errors separately from variance
```

**3. Replacement note**

```text
removed dump-all, use search-skills
```

## Pitfalls

- Bumping the version without a changelog entry
- Removing a slug in a minor release and breaking pinned consumers
- Describing edits, such as rewording, as if they changed behaviour

## Done when

- the version bump and changelog entry land together
- every removal names a replacement

## References

- [Semantic versioning](https://semver.org/)
- [Keep a changelog](https://keepachangelog.com/en/1.1.0/)
