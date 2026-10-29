# skillmcp

An **MCP stdio server** that makes skill packs callable by any agent — search
them, fetch one, done. No copying folders into a prompt, no giant context dump.

Ships with **50 validated skills** about running such a server: wiring clients,
designing tools, invoking them cheaply, verifying the protocol, governing side
effects and publishing packs.

```text
skillmcp serve --packs-root /srv/packs     # JSON-RPC 2.0 over stdin/stdout
skillmcp tools                              # what this server advertises
skillmcp index --packs-root .               # packs and skills it can see
skillmcp call search_skills --args '{"query":"stdout purity"}'
```

## Why a server instead of a directory

A skill directory only helps an agent that already knows the folder exists and
can afford to read it. A server turns that directory into three calls:

| Tool | Returns | Bounded by |
|---|---|---|
| `list_packs` | every pack with category and skill count | number of packs |
| `search_skills` | ranked slugs with title, tags and description | `limit`, max 50 |
| `get_skill` | one full `SKILL.md` | one document |

So the agent searches with keywords, reads one procedure, and acts. Search
covers slug, title, tags and the per-skill description, which is why a query
like `stdout purity` finds exactly the right skill.

## Protocol

Protocol revision pinned to **2025-03-26**, newline-delimited JSON-RPC 2.0 over
stdio. Implemented: `initialize`, `notifications/initialized`, `ping`,
`tools/list`, `tools/call`. Everything else returns `-32601`.

```text
$ printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26"}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_skills","arguments":{"query":"stdout purity","limit":2}}}' \
  | skillmcp serve

{"id":1,"protocolVersion":"2025-03-26","capabilities":{"tools":{"listChanged":false}},"serverInfo":{"name":"skillmcp","version":"1.0.0"}}
{"id":2,"tools":["list_packs","search_skills","get_skill"]}
{"id":3,"matches":["stdout-purity-check"],"total":1}
```

Notifications never get a reply. Malformed lines get `-32700` and the server
keeps serving. stdout carries protocol messages only; diagnostics go to stderr,
which the test suite asserts.

## Client config

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

Point `--packs-root` at a directory of packs, or at a single pack. Anything with
a `pack.json` is discovered, including packs built by the other repos in this
series.

## The 50 skills

| Phase | Skills | Focus |
|---|---|---|
| `setup` | 8 | Client config, transport choice, version handshake, capability declaration, trust, boundaries, secrets, reload semantics |
| `design` | 8 | Tool naming, schema strictness, bounded output, error shape, idempotency, surface minimisation, destructive gating, descriptions as contracts |
| `invoke` | 9 | Search-then-fetch, call budgets, parallel safety, argument exactness, error classification, pagination, determinism, context management, verification |
| `verify` | 8 | Protocol conformance, lifecycle, schema validation, error paths, transcript fixtures, stdout purity, concurrency, replay |
| `govern` | 9 | Scope guard, rate limits, credential isolation, audit log, destructive confirmation, retention, least privilege, sandboxing, escalation |
| `document` | 8 | Frontmatter contract, one procedure per skill, use/avoid clauses, signals and pitfalls, done-when, references, versioning, local publishing |

```text
skillmcp list --phase govern
skillmcp search stdout
skillmcp show protocol-conformance-test
```

Each skill renders deterministically from a Python corpus dict, carries a
SHA-256 in `pack.json`, and is re-validated against six floors on every run.

## Install

```bash
python -m venv .venv && . .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
skillmcp serve --packs-root .
```

Python 3.10+. No runtime dependencies, and the server never opens a socket —
stdio only.

## Safety

The server is read-only: three tools, no writes, no network. It reads files
under the packs root you give it and returns text. Credentials never belong in
the client config; a server that needs one should read it from the environment,
as `secrets-via-environment` describes.

MIT licensed.
