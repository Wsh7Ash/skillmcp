# Security

## What this server can do

`skillmcp serve` is read-only. It exposes three tools:

- `list_packs` — pack metadata and counts.
- `search_skills` — ranked slugs, titles, tags and descriptions.
- `get_skill` — the text of one `SKILL.md`.

It reads files under the packs root you pass on the command line, writes
nothing, opens no sockets, and performs no discovery. There is no tool that
executes a command, fetches a URL or modifies a pack.

## Trust boundaries

A skill file is **data, not code**. Content served through `get_skill` is text
for an agent to read; nothing in a `SKILL.md` is executed by this server. Treat
served text as untrusted input all the same: a third-party pack can contain
instructions aimed at the agent reading it.

`--packs-root` defines the trust boundary. Only point it at directories whose
contents you would be comfortable having an agent read in full.

## Client configuration

Never put a credential in the client config file. A server that needs one should
read it from the environment (`skillmcp` does not need any), and the config
should hold a reference rather than the value.

## Authorised use

The bundled skills describe testing techniques that require permission from the
system owner. Reading a skill grants nothing; the engagement scope decides what
may be executed, and by which tool.

## Reporting a vulnerability

Open a private security advisory on the repository. Include the version, the
pack layout that triggers the problem, and the JSON-RPC messages involved.
Never attach a pack containing real credentials or personal data.

## Dependencies

None at runtime beyond the Python standard library. `pytest` is a development
dependency. No telemetry, no network calls, no automatic updates.
