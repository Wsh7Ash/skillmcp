# Changelog

## 1.0.0

First release.

- MCP stdio server pinned to protocol revision 2025-03-26
- Tools: `list_packs`, `search_skills`, `get_skill`, all read-only
- JSON-RPC envelope validation with correct codes for parse, request and method
  errors; the loop survives a malformed line
- Tool-level failures returned as `isError` results so an agent can retry with
  a different argument rather than treating the server as broken
- Pack discovery one level below the packs root, tolerant of missing manifests
- Per-request index reload, so a mid-session edit is visible immediately
- Per-skill descriptions in `pack.json`, with frontmatter fallback for packs
  built before the field existed
- 50 validated skills across setup, design, invoke, verify, govern and document
- `tools`, `call` and `index` debug commands
- Corpus harness: byte-deterministic render, SHA-256 manifest, six strength
  floors, and a test that asserts every stdout line is a protocol message
