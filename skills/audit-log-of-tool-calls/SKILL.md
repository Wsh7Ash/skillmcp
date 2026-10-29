---
name: audit-log-of-tool-calls
description: "Log every call with arguments and outcome so an agent's actions can be reconstructed. Use when the server can change state or reach anything outside its own directory"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [govern, audit, logging]
---

# Audit Log of Tool Calls

> Log every call with arguments and outcome so an agent's actions can be reconstructed

**Use when:** the server can change state or reach anything outside its own directory

**Avoid when:** the server is read-only over public content and no audit is required

## Procedure

1. Decide the log destination: stderr, a file or both, never stdout
2. Log timestamp, tool name, argument names and outcome
3. Redact argument values that are credentials
4. Log the failure reason for refused and errored calls
5. Rotate or cap the log so it cannot fill the disk
6. Verify a session can be reconstructed from the log alone

## Signals

- each call appears exactly once in the log
- argument values that are secrets are redacted
- refusals and errors are logged with reasons
- the log never appears on stdout

## Patterns

**1. Structured line**

```text
{"ts":...,"tool":"get_skill","args":["slug"],"ok":true}
```

**2. Redaction**

```text
args values logged as [redacted] when the key matches token|key|secret
```

**3. Log size cap**

```text
rotate at 10 MB, keep three files
```

## Pitfalls

- Logging whole argument objects including credentials
- Writing the audit log to stdout and breaking the protocol
- Logging failures without the reason, making the entry useless

## Done when

- a session can be reconstructed from the log
- no credential value appears in any log line

## References

- [NIST SP 800-53 - audit controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - logging cheat sheet](https://cheatsheetseries.owasp.org/)
