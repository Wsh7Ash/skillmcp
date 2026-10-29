# Architecture

Three layers with one rule between them: stdout is a protocol channel and
nothing else may write to it.

## 1. Protocol — `protocol.py`

`parse_message` validates the envelope (a JSON object, `jsonrpc == "2.0"`, a
non-empty string method, an id that is a string, number or null) and raises
`ProtocolError` with the right JSON-RPC code when it does not fit. `result` and
`error` build the two reply shapes; `text_content` builds an MCP tool result.

Keeping validation here means the dispatcher can assume a shaped message.

## 2. Packs — `packs.py`

```text
root/
  pack.json              name, version, category, description, skills[]
  skills/<slug>/SKILL.md  rendered content, hash-listed in the manifest
```

`load_pack` reads the manifest, skips entries whose file is missing (so a
half-finished pack cannot break a session), and takes each skill's description
from the manifest. Packs written before descriptions existed fall back to the
`SKILL.md` frontmatter, then to the pack description.

`discover` looks at the root itself and one level below it. `PackIndex` holds
the result, exposes `find`/`read_skill`/`search`, and is rebuilt per request so a
file edited mid-session is visible immediately.

## 3. Server — `server.py`

`handle(message, ctx)` is a pure function from one message to one reply (or
`None` for notifications). That design is what makes the tests cheap: no
process, no pipes, no timing.

| Method | Behaviour |
|---|---|
| `initialize` | returns pinned `protocolVersion`, `capabilities.tools`, `serverInfo`, short `instructions` |
| `notifications/initialized` | no reply |
| `ping` | empty result |
| `tools/list` | three tools with full JSON schemas |
| `tools/call` | dispatches to a handler; wraps failures in `isError` results |
| anything else | `-32601 method not found` |

Error discipline matters more than it looks:

- **Protocol level** (`-32602`, `-32601`, `-32700`) — the request was wrong.
- **Tool level** (`isError: true`) — the request was well formed but the work
  failed, for example an unknown slug. The agent can retry with a different
  argument instead of treating the server as broken.

`serve` is the only impure part: read a line, parse, dispatch, write one reply,
flush. A malformed line produces a parse error and the loop continues, which is
the difference between a usable server and one that dies on the first stray
newline.

## Tool surface

Three tools, deliberately minimal:

- **`list_packs`** — what exists, with counts.
- **`search_skills`** — ranked candidate slugs, bounded by `limit` (max 50).
- **`get_skill`** — exactly one document.

Search-then-fetch is the intended workflow: the agent spends context on the one
procedure it will follow, not on a survey. Every tool description states what
it returns and what it does not do, because the description is the contract a
model reads.

## Corpus coupling

The server's bundled pack is the same 50 skills this repo documents. The build
step renders `skills/`, writes `pack.json` with a per-skill SHA-256, and the
test suite asserts the on-disk files equal a fresh render. Serving and
documenting therefore cannot drift apart.

## Data flow

```text
client stdin
   │  {"jsonrpc":"2.0","id":3,"method":"tools/call", ...}
   ▼
parse_message ──▶ handle ──▶ TOOL_HANDLERS["search_skills"]
                    │                 │
                    │            PackIndex.reload()
                    │                 │  scan root, read pack.json
                    │                 ▼
                    │            ranked SkillEntry list
                    ▼                 │
              result(id, text_content(json))
                    │
   stdout ◀─────────┘
```

## Test strategy

- Envelope: bad JSON, wrong version, wrong shape, whitespace line.
- Packs: discovery of a synthetic second pack, manifest-less directory, unknown
  slug, search ranking.
- Server: initialize shape, notification silence, tool schemas, three error
  paths, unknown method, and a full `serve()` session including a garbage line.
- CLI: subprocess session with stdout parsed line by line.

No test opens a socket.
