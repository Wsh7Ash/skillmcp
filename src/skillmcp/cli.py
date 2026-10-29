"""skillmcp command line interface.

Shared corpus commands (validate / list / show / search / build) come from the
pack harness. The domain commands are the server itself and two debug helpers:

    skillmcp serve --packs-root /srv/packs
    skillmcp tools
    skillmcp call search_skills --args '{"query":"cache vary"}'
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .corpus import PACK, SKILLS
from .packs import PackIndex
from .render import build_pack, render_skill, word_count
from .server import TOOLS, build_context, handle, serve
from .validate import (
    MAX_DESCRIPTION,
    MIN_DONE,
    MIN_PATTERNS,
    MIN_PITFALLS,
    MIN_SIGNALS,
    MIN_STEPS,
    MIN_SUMMARY,
    MIN_WORDS,
    Issue,
    validate_pack,
)

PHASE_ORDER = ("setup", "design", "invoke", "verify", "govern", "document")

FLOORS = {
    "min_steps": MIN_STEPS,
    "min_signals": MIN_SIGNALS,
    "min_patterns": MIN_PATTERNS,
    "min_pitfalls": MIN_PITFALLS,
    "min_done_when": MIN_DONE,
    "min_summary_chars": MIN_SUMMARY,
    "min_words": MIN_WORDS,
    "max_description_chars": MAX_DESCRIPTION,
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _report(issues: list[Issue], total: int, as_json: bool, title: str) -> int:
    bad = {issue.slug for issue in issues if issue.slug}
    valid = total - len(bad)
    if as_json:
        print(
            json.dumps(
                {
                    "pack": title,
                    "checked": total,
                    "valid": valid,
                    "passed": not issues,
                    "floors": FLOORS,
                    "issues": [
                        {"slug": i.slug, "rule": i.rule, "message": i.message} for i in issues
                    ],
                },
                indent=2,
            )
        )
    else:
        print(f"{title}: {valid}/{total} skills valid")
        for issue in issues:
            print(f"  FAIL {issue}")
        if not issues:
            print(
                f"  ok  steps>={MIN_STEPS} signals>={MIN_SIGNALS} patterns>={MIN_PATTERNS} "
                f"pitfalls>={MIN_PITFALLS} words>={MIN_WORDS} refs canonical https"
            )
    return 0 if not issues else 1


def cmd_validate(args: argparse.Namespace) -> int:
    issues = validate_pack(PACK, SKILLS)
    root = Path(args.root) if args.root else repo_root()
    if not args.skip_files:
        for skill in SKILLS:
            path = root / "skills" / skill.slug / "SKILL.md"
            if not path.exists():
                issues.append(Issue(skill.slug, "file-missing", "SKILL.md missing"))
                continue
            if path.read_text(encoding="utf-8") != render_skill(PACK, skill):
                issues.append(Issue(skill.slug, "file-drift", "SKILL.md differs from corpus render"))
    return _report(issues, len(SKILLS), args.json, PACK["name"])


def cmd_list(args: argparse.Namespace) -> int:
    skills = [
        skill
        for skill in SKILLS
        if (not args.tag or args.tag in skill.tags)
        and (not args.phase or skill.meta_get("phase") == args.phase)
    ]
    if args.json:
        print(
            json.dumps(
                [
                    {
                        "slug": s.slug,
                        "title": s.title,
                        "tags": list(s.tags),
                        "meta": s.meta,
                        "words": word_count(render_skill(PACK, s)),
                    }
                    for s in skills
                ],
                indent=2,
            )
        )
        return 0
    for skill in skills:
        print(f"{skill.slug:40s} {skill.meta_get('phase', '-'):10s} {skill.title}")
    print(f"-- {len(skills)} skills")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    for skill in SKILLS:
        if skill.slug == args.slug:
            print(render_skill(PACK, skill), end="")
            return 0
    print(f"unknown skill: {args.slug}", file=sys.stderr)
    return 1


def cmd_search(args: argparse.Namespace) -> int:
    terms = [term.lower() for term in args.terms]
    scored: list[tuple[int, Any]] = []
    for skill in SKILLS:
        haystack = " ".join(
            [skill.slug, skill.title, skill.summary, " ".join(skill.tags), " ".join(skill.steps)]
        ).lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            scored.append((score, skill))
    scored.sort(key=lambda pair: (-pair[0], pair[1].slug))
    for score, skill in scored[: args.limit]:
        print(f"{score:3d}  {skill.slug:40s} {skill.title}")
    if not scored:
        print("no matches")
        return 1
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    root = Path(args.root) if args.root else repo_root()
    build_pack(root, PACK, SKILLS)
    issues = validate_pack(PACK, SKILLS)
    for skill in SKILLS:
        path = root / "skills" / skill.slug / "SKILL.md"
        if path.read_text(encoding="utf-8") != render_skill(PACK, skill):
            issues.append(Issue(skill.slug, "file-drift", "render mismatch"))
    bad = {issue.slug for issue in issues if issue.slug}
    report = {
        "pack": PACK["name"],
        "version": PACK["version"],
        "expected_skills": PACK.get("expected_skills", len(SKILLS)),
        "checked": len(SKILLS),
        "valid": len(SKILLS) - len(bad),
        "passed": not issues,
        "floors": FLOORS,
        "issues": [{"slug": i.slug, "rule": i.rule, "message": i.message} for i in issues],
    }
    results = root / "results"
    results.mkdir(parents=True, exist_ok=True)
    (results / "validation.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"built {len(SKILLS)} skills -> {root / 'skills'}")
    return 0 if not issues else 1


# --------------------------------------------------------------- server commands


def cmd_serve(args: argparse.Namespace) -> int:
    ctx = build_context(args.packs_root)
    if not ctx.index.packs:
        print(
            f"warning: no packs found under {args.packs_root or repo_root()}; "
            "tools will return empty results",
            file=sys.stderr,
        )
    return serve(sys.stdin, sys.stdout, ctx)


def cmd_tools(args: argparse.Namespace) -> int:
    if args.json:
        print(json.dumps(TOOLS, indent=2))
        return 0
    for tool in TOOLS:
        schema = tool["inputSchema"]
        required = ", ".join(schema.get("required", [])) or "-"
        print(f"{tool['name']}")
        print(f"  {tool['description']}")
        print(f"  required: {required}")
    return 0


def cmd_call(args: argparse.Namespace) -> int:
    """Call one tool without a protocol session, for humans debugging a server."""
    ctx = build_context(args.packs_root)
    try:
        arguments = json.loads(args.args) if args.args else {}
    except json.JSONDecodeError as exc:
        print(f"--args is not valid JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(arguments, dict):
        print("--args must be a JSON object", file=sys.stderr)
        return 2
    message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": args.tool, "arguments": arguments},
    }
    reply = handle(message, ctx)
    if reply is None:  # pragma: no cover - id was supplied
        return 2
    if "error" in reply:
        print(json.dumps(reply["error"], indent=2), file=sys.stderr)
        return 1
    result = reply["result"]
    for block in result.get("content", []):
        print(block.get("text", ""))
    return 1 if result.get("isError") else 0


def cmd_index(args: argparse.Namespace) -> int:
    index = PackIndex([Path(args.packs_root)])
    if args.json:
        print(
            json.dumps(
                {
                    "packs": [pack.to_dict() for pack in index.packs],
                    "skills_total": len(index.skills),
                },
                indent=2,
            )
        )
        return 0
    for pack in index.packs:
        print(f"{pack.name:14s} {pack.version:8s} {pack.category:20s} {len(pack.skills):3d} skills")
    print(f"-- {len(index.packs)} packs, {len(index.skills)} skills")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=PACK["name"], description=PACK["description"])
    parser.add_argument("--version", action="version", version=f"{PACK['name']} {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="run every corpus rule and check disk sync")
    p.add_argument("--json", action="store_true")
    p.add_argument("--root", default=None)
    p.add_argument("--skip-files", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("list", help="list skills")
    p.add_argument("--tag", default=None)
    p.add_argument("--phase", default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="print one SKILL.md")
    p.add_argument("slug")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("search", help="rank skills by keyword")
    p.add_argument("terms", nargs="+")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("build", help="regenerate skills/, pack.json and results/")
    p.add_argument("--root", default=None)
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("serve", help="run the MCP stdio server")
    p.add_argument("--packs-root", default=None, help="directory containing packs or a pack itself")
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("tools", help="print the tool schemas this server advertises")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_tools)

    p = sub.add_parser("call", help="call one tool without a protocol session")
    p.add_argument("tool")
    p.add_argument("--args", default="{}", help="JSON object of tool arguments")
    p.add_argument("--packs-root", default=None)
    p.set_defaults(func=cmd_call)

    p = sub.add_parser("index", help="list the packs and skills visible from a root")
    p.add_argument("--packs-root", default=".")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_index)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
