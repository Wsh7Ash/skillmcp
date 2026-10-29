"""JSON-RPC 2.0 messages for the stdio transport.

Spec: https://modelcontextprotocol.io/specification/2025-03-26/basic
JSON-RPC: https://www.jsonrpc.org/specification

Only what a stdio MCP server needs: parse a line, build a result, build an
error, and never write anything but protocol messages to stdout.
"""

from __future__ import annotations

import json
from typing import Any

JSONRPC_VERSION = "2.0"

PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


class ProtocolError(Exception):
    """A JSON-RPC level failure that must be returned, not raised to the host."""

    def __init__(self, code: int, message: str, data: Any | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data


def parse_message(line: str) -> dict[str, Any]:
    """Parse one newline-delimited JSON-RPC message."""
    text = line.strip()
    if not text:
        raise ProtocolError(PARSE_ERROR, "empty message")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ProtocolError(PARSE_ERROR, f"invalid JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ProtocolError(INVALID_REQUEST, "message must be a JSON object")
    if payload.get("jsonrpc") != JSONRPC_VERSION:
        raise ProtocolError(INVALID_REQUEST, "jsonrpc must be exactly '2.0'")
    if "method" in payload:
        if not isinstance(payload["method"], str) or not payload["method"]:
            raise ProtocolError(INVALID_REQUEST, "method must be a non-empty string")
        if "id" in payload and not isinstance(payload["id"], (str, int, type(None))):
            raise ProtocolError(INVALID_REQUEST, "id must be a string, number or null")
    elif "result" not in payload and "error" not in payload:
        raise ProtocolError(INVALID_REQUEST, "message has neither method nor result")
    return payload


def result(message_id: Any, value: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": message_id, "result": value}


def error(message_id: Any, code: int, message: str, data: Any | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "jsonrpc": JSONRPC_VERSION,
        "id": message_id,
        "error": {"code": code, "message": message},
    }
    if data is not None:
        payload["error"]["data"] = data
    return payload


def text_content(text: str) -> dict[str, Any]:
    """MCP tool result with a single text block."""
    return {"content": [{"type": "text", "text": text}], "isError": False}
