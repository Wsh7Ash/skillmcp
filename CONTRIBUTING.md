# Contributing

## Local loop

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m skillmcp validate
```

## The rule that matters

**stdout is the protocol channel.** No print, no logging handler, no library
that writes to stdout. Diagnostics go to stderr. `tests/test_corpus.py` pipes a
real session through a subprocess and parses every stdout line, so a stray print
fails CI rather than a user's client.

## Adding a tool

1. Add an entry to `TOOLS` in `src/skillmcp/server.py` with a description that
   states the return shape, the bounds, and what the tool does not do.
2. Write a handler `(ctx, arguments) -> mcp result` and register it in
   `TOOL_HANDLERS`.
3. Validate arguments explicitly and raise `ProtocolError(INVALID_PARAMS, ...)`
   with the offending key named.
4. Return bounded output: a limit with a hard maximum and a total count.
5. Add tests for the happy path and each rejection.

Keep the surface small. Three tools that a model always chooses correctly beat
ten that it has to guess between.

## Changing the protocol layer

`handle()` must stay a pure function from message to reply. Timestamps, clock
reads and file writes belong in `serve()` or the tool handlers, not in the
dispatcher. A protocol change means bumping the pinned revision constant in one
place and updating the docs in the same commit.

## Changing the corpus

Skills are dicts in `src/skillmcp/corpus/part1.py` .. `part3.py`. Run
`python -m skillmcp build` then `pytest -q`. Never edit `skills/**/SKILL.md` by
hand — it is generated and hash-checked.

Floors: 6 steps, 4 signals, 3 patterns, 3 pitfalls, 2 done-when items, 1
canonical `https` reference, 180 rendered words, unique slug and title. Pattern
labels must be at least eight characters; that floor exists because short labels
carry no information.

## Style

- Standard library only at runtime; `pytest` is the only dev dependency.
- Type hints on public functions, `from __future__ import annotations` first.
- No network in tests.
