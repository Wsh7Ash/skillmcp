---
name: deterministic-command-choices
description: "Prefer commands whose output does not depend on locale, globbing or shell state. Use when an agent constructs commands that a shell will interpret before the tool sees them"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [invoke, shell, determinism]
---

# Deterministic Command Choices

> Prefer commands whose output does not depend on locale, globbing or shell state

**Use when:** an agent constructs commands that a shell will interpret before the tool sees them

**Avoid when:** the command is a fixed literal with no interpolation

## Procedure

1. Identify every part of the command that the shell expands
2. Replace globs with explicit file lists where the set matters
3. Quote every path and value that could contain a space
4. Avoid locale-sensitive sorting by specifying the collation or sorting explicitly
5. Pin time formats to a fixed zone and format
6. Re-run the command and confirm identical output

## Signals

- two runs produce byte-identical output
- no path in the command is unquoted
- the file set passed to the tool is explicit
- timestamps carry a zone and a fixed format

## Patterns

**1. Explicit list**

```text
cmd a.txt b.txt instead of cmd *.txt
```

**2. Quoted path**

```text
"results/my file.json"
```

**3. Fixed time**

```text
--date 2026-10-29T00:00:00Z
```

## Pitfalls

- Relying on glob expansion order which differs by filesystem and locale
- Leaving a date unformatted so the output changes every run
- Passing an unquoted path that breaks silently on a space

## Done when

- the command produces identical output on a rerun
- no shell expansion affects which files or values are used

## References

- [POSIX shell quoting](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [Python - os.environ](https://docs.python.org/3/library/os.html)
