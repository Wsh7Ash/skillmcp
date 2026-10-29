"""skillmcp corpus: pack metadata plus 50 authored MCP-for-hunting skills.

These skills are also the server's bundled pack, so a fresh install serves a
useful index before any other pack is put on disk.
"""

from __future__ import annotations

from typing import Any

from ..model import skill_from_dict
from .part1 import SKILLS as PART1
from .part2 import SKILLS as PART2
from .part3 import SKILLS as PART3

PACK: dict[str, Any] = {
    "name": "skillmcp",
    "version": "1.0.0",
    "category": "ai-tool",
    "license": "MIT",
    "runtime": "Claude Code, opencode, or any agent runtime that loads SKILL.md files",
    "description": (
        "50 validated skills for running a skills server over MCP stdio: wiring "
        "clients, designing tools, invoking them without wasting context, "
        "verifying the protocol, governing side effects and publishing packs."
    ),
    "expected_skills": 50,
    "meta_keys": ("phase",),
    "requires_verification": False,
}

SKILLS: list[Any] = [skill_from_dict(raw) for raw in (*PART1, *PART2, *PART3)]
BY_SLUG: dict[str, Any] = {skill.slug: skill for skill in SKILLS}
