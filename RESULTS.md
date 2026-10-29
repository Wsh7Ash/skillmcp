# Results

Observed output only. Every block below was produced by the committed code on
this machine.

## Environment

- OS: Windows (MSYS2 shell), Python 3.14.3
- Runtime: Python 3.10+ standard library only; `pytest` as dev dependency
- Network: none. The server speaks stdio and reads local packs only.

## Corpus gate

```text
$ python -m skillmcp validate
skillmcp: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https
```

Phase distribution: `setup` 8, `design` 8, `invoke` 9, `verify` 8, `govern` 9,
`document` 8 — 50 unique slugs, 50 unique titles.

## Test suite

```text
$ python -m pytest -q
.............................                                            [100%]
```

29 tests. The protocol tests drive `handle()` directly; the CLI test pipes a
real session through a subprocess and asserts every stdout line parses as a
JSON-RPC message, which is the stdout-purity guarantee.

## Server session

```text
$ skillmcp index --packs-root .
skillmcp       1.0.0    ai-tool               50 skills
-- 1 packs, 50 skills
```

```text
$ printf '%s\n' <initialize> <initialized> <tools/list> <search_skills> <unknown method> <garbage> \
    | skillmcp serve
{"id": 1, "protocolVersion": "2025-03-26", "capabilities": {"tools": {"listChanged": false}}, "serverInfo": {"name": "skillmcp", "version": "1.0.0"}}
{"id": 2, "tools": ["list_packs", "search_skills", "get_skill"]}
{"id": 3, "matches": ["stdout-purity-check"], "total": 1}
{"id": 4, "error": -32601, "message": "unknown method 'nope'"}
{"id": null, "error": -32700, "message": "invalid JSON: Expecting value"}
```

Five lines in, five replies out: the `notifications/initialized` line produced
no reply, the unknown method produced `-32601`, and the malformed line produced
`-32700` without killing the session.

## One tool call, no protocol

```text
$ skillmcp call get_skill --args '{"slug":"stdout-purity-check"}' --packs-root .
---
name: stdout-purity-check
description: "Assert that stdout carries only protocol messages, because one stray print breaks every client. Use when the server logs, warns or prints anything during normal operation"
pack: skillmcp
version: 1.0.0
category: ai-tool
tags: [verify, stdio, protocol]
---
```

## Generated artifacts

- `results/catalog.md` — 50-skill index table
- `results/validation.json` — machine-readable gate report
- `results/demo_transcript.txt` — the session above, verbatim
- `pack.json` — manifest with per-skill description, phase and SHA-256

## Known limitations

- One pack per root is discovered directly; nested pack trees deeper than one
  level are not walked. Point `--packs-root` at the directory that contains the
  packs.
- The index is rebuilt per request. That keeps a live edit visible without a
  restart and costs a directory scan plus a manifest parse per call; for very
  large pack trees a cache keyed on mtime would be the next step.
- Search is term-frequency matching, not semantic. A query with no shared
  vocabulary returns nothing rather than a best guess, and the tool says so.
- The server implements the tools capability only. Resources, prompts and
  sampling are deliberately undeclared and return `-32601`.
