# Usage

## Install

```bash
python -m venv .venv && . .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
```

Without installing: `PYTHONPATH=src python -m skillmcp ...`.

## Start the server

```bash
skillmcp serve --packs-root /srv/packs
```

`--packs-root` may be a directory containing packs or a single pack directory.
With no flag it defaults to this repository, so a fresh clone serves its own 50
skills immediately.

The server reads stdin and writes stdout until stdin closes. It prints nothing
else to stdout; warnings and diagnostics go to stderr.

## Inspect it without a client

```bash
skillmcp tools                  # tool names, descriptions, required args
skillmcp tools --json           # full schemas
skillmcp index --packs-root .   # packs and skill counts
skillmcp call list_packs --packs-root .
skillmcp call search_skills --args '{"query":"cache vary","limit":3}' --packs-root .
skillmcp call get_skill --args '{"slug":"stdout-purity-check"}' --packs-root .
```

`call` is a debugging convenience: it builds the same JSON-RPC message a client
would and dispatches it in-process. Exit code is 0 on success, 1 when the tool
returned `isError`, 2 for bad arguments to `call` itself.

## Wire it into a client

```json
{
  "mcpServers": {
    "skills": {
      "command": "python",
      "args": ["-m", "skillmcp", "serve", "--packs-root", "/srv/packs"]
    }
  }
}
```

Restart the client and check its tool list. If the server does not appear:

1. `skillmcp serve --packs-root ...` by hand and confirm it waits for input.
2. Send an `initialize` line and check you get a reply.
3. Look at the client log for a handshake error.
4. Confirm the command path is absolute and the module is installed for that
   interpreter.

## Protocol, by hand

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26"}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_skills","arguments":{"query":"scope"}}}' \
  | skillmcp serve
```

Notifications produce no reply, so expect fewer output lines than input lines.

## Add packs

Any directory with this shape is discovered:

```text
packs/
  my-pack/
    pack.json
    skills/<slug>/SKILL.md
```

```bash
skillmcp index --packs-root packs
```

The index is rebuilt per request, so a pack added or edited while the client is
running is visible on the next call — no restart needed.

## Browse the bundled skills

```bash
skillmcp list
skillmcp list --phase govern
skillmcp search protocol
skillmcp show lifecycle-test-initialize-then-tools
```

## Regenerate artifacts

```bash
skillmcp build
```

Rewrites `skills/`, `pack.json`, `results/catalog.md` and
`results/validation.json`. Byte deterministic; CI fails when a committed file
differs from a fresh render.

## Operating notes

- The server is read-only. Three tools, no writes, no outbound network.
- Keep credentials out of the client config; a server that needs one should read
  it from the environment.
- `search_skills` is term matching. If a query returns nothing, try the
  vocabulary used in the skill titles rather than a full sentence.
- A pack with a missing `pack.json` is silently skipped at discovery. Run
  `skillmcp index` to confirm what the server actually sees.
