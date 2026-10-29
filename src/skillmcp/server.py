"""MCP server over stdio: lifecycle, tool listing and tool calls.

Protocol revision pinned to 2025-03-26. stdout carries protocol messages only;
diagnostics go to stderr, because a stray print on stdout breaks every client.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any, TextIO

from . import __version__
from .packs import PackIndex
from .protocol import (
    INTERNAL_ERROR,
    INVALID_PARAMS,
    METHOD_NOT_FOUND,
    INVALID_REQUEST,
    PARSE_ERROR,
    ProtocolError,
    error,
    parse_message,
    result,
    text_content,
)

PROTOCOL_VERSION = "2025-03-26"

TOOLS: list[dict[str, Any]] = [
    {
        "name": "list_packs",
        "description": "List every skill pack visible to this server with its category and skill count.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "search_skills",
        "description": (
            "Rank skills by keyword across slug, title, tags and pack description. "
            "Use it to find the procedure for a task before fetching the full text."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Space separated keywords."},
                "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
                "pack": {"type": "string", "description": "Restrict the search to one pack name."},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_skill",
        "description": "Return the full SKILL.md for one skill, optionally scoped to a pack.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Skill slug, e.g. cache-key-header-probe."},
                "pack": {"type": "string", "description": "Pack name to disambiguate a duplicate slug."},
            },
            "required": ["slug"],
            "additionalProperties": False,
        },
    },
]


@dataclass
class Context:
    index: PackIndex
    name: str = "skillmcp"
    version: str = __version__


def _require_string(params: dict[str, Any], key: str) -> str:
    value = params.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ProtocolError(INVALID_PARAMS, f"{key} must be a non-empty string")
    return value


def _optional_int(params: dict[str, Any], key: str, default: int) -> int:
    value = params.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ProtocolError(INVALID_PARAMS, f"{key} must be an integer")
    if value < 1 or value > 50:
        raise ProtocolError(INVALID_PARAMS, f"{key} must be between 1 and 50")
    return value


def tool_list_packs(ctx: Context, params: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "packs": [pack.to_dict() for pack in ctx.index.packs],
        "skills_total": len(ctx.index.skills),
    }
    return text_content(json.dumps(payload, indent=2))


def tool_search_skills(ctx: Context, params: dict[str, Any]) -> dict[str, Any]:
    query = _require_string(params, "query")
    limit = _optional_int(params, "limit", 10)
    pack = params.get("pack")
    if pack is not None and not isinstance(pack, str):
        raise ProtocolError(INVALID_PARAMS, "pack must be a string")
    terms = [term for term in query.split() if term.strip()]
    hits = ctx.index.search(terms, limit=limit, pack=pack)
    payload = {
        "query": query,
        "matches": [{"score": score, **skill.to_dict()} for score, skill in hits],
        "matches_total": len(hits),
    }
    if not hits:
        payload["note"] = "no skill matched; try broader terms or list_packs"
    return text_content(json.dumps(payload, indent=2))


def tool_get_skill(ctx: Context, params: dict[str, Any]) -> dict[str, Any]:
    slug = _require_string(params, "slug")
    pack = params.get("pack")
    if pack is not None and not isinstance(pack, str):
        raise ProtocolError(INVALID_PARAMS, "pack must be a string")
    try:
        entry, text = ctx.index.read_skill(slug, pack)
    except LookupError as exc:
        return {
            "content": [{"type": "text", "text": str(exc)}],
            "isError": True,
        }
    return text_content(text)


TOOL_HANDLERS = {
    "list_packs": tool_list_packs,
    "search_skills": tool_search_skills,
    "get_skill": tool_get_skill,
}


def handle(message: dict[str, Any], ctx: Context) -> dict[str, Any] | None:
    """Dispatch one JSON-RPC message. Returns None for notifications."""
    method = message.get("method")
    message_id = message.get("id")
    is_notification = "id" not in message

    try:
        if method == "initialize":
            params = message.get("params") or {}
            if not isinstance(params, dict):
                raise ProtocolError(INVALID_PARAMS, "params must be an object")
            client_version = params.get("protocolVersion")
            capabilities = params.get("capabilities")
            if client_version is not None and not isinstance(client_version, str):
                raise ProtocolError(INVALID_PARAMS, "protocolVersion must be a string")
            if capabilities is not None and not isinstance(capabilities, dict):
                raise ProtocolError(INVALID_PARAMS, "capabilities must be an object")
            value = {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": ctx.name, "version": ctx.version},
                "instructions": (
                    "Search skills with search_skills, then read one with get_skill. "
                    "Skills are procedures, not guarantees: check each one against the "
                    "engagement scope before acting on it."
                ),
            }
            return None if is_notification else result(message_id, value)

        if method == "ping":
            return None if is_notification else result(message_id, {})

        if method in ("notifications/initialized", "initialized"):
            return None

        if method == "tools/list":
            return None if is_notification else result(message_id, {"tools": TOOLS})

        if method == "tools/call":
            params = message.get("params") or {}
            if not isinstance(params, dict):
                raise ProtocolError(INVALID_PARAMS, "params must be an object")
            name = params.get("name")
            if not isinstance(name, str) or name not in TOOL_HANDLERS:
                raise ProtocolError(
                    INVALID_PARAMS,
                    f"unknown tool {name!r}; available: {', '.join(sorted(TOOL_HANDLERS))}",
                )
            arguments = params.get("arguments") or {}
            if not isinstance(arguments, dict):
                raise ProtocolError(INVALID_PARAMS, "arguments must be an object")
            value = TOOL_HANDLERS[name](ctx, arguments)
            return None if is_notification else result(message_id, value)

        raise ProtocolError(METHOD_NOT_FOUND, f"unknown method {method!r}")
    except ProtocolError as exc:
        if is_notification:
            return None
        return error(message_id, exc.code, exc.message, exc.data)
    except Exception as exc:  # pragma: no cover - defensive
        if is_notification:
            return None
        return error(message_id, INTERNAL_ERROR, f"internal error: {exc}")


def serve(stdin: TextIO, stdout: TextIO, ctx: Context) -> int:
    """Read newline-delimited messages until stdin closes."""
    for line in stdin:
        if not line.strip():
            continue
        try:
            message = parse_message(line)
        except ProtocolError as exc:
            stdout.write(json.dumps(error(None, PARSE_ERROR, exc.message)) + "\n")
            stdout.flush()
            continue
        if "method" not in message:
            # A response sent to a server is a client bug; report it, keep serving.
            stdout.write(
                json.dumps(error(message.get("id"), INVALID_REQUEST, "server received a response"))
                + "\n"
            )
            stdout.flush()
            continue
        reply = handle(message, ctx)
        if reply is not None:
            stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            stdout.flush()
    return 0


def build_context(packs_root: str | None) -> Context:
    from pathlib import Path

    root = Path(packs_root) if packs_root else Path(__file__).resolve().parents[2]
    return Context(index=PackIndex([root]))


def log(message: str) -> None:
    """Diagnostics go to stderr so stdout stays a clean protocol channel."""
    print(message, file=sys.stderr, flush=True)
