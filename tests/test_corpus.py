"""Corpus, protocol, pack index and server tests."""

from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from skillmcp.corpus import BY_SLUG, PACK, SKILLS  # noqa: E402
from skillmcp.packs import PackError, PackIndex, discover, load_pack  # noqa: E402
from skillmcp.protocol import (  # noqa: E402
    INVALID_REQUEST,
    METHOD_NOT_FOUND,
    PARSE_ERROR,
    ProtocolError,
    parse_message,
    text_content,
)
from skillmcp.render import render_skill, word_count  # noqa: E402
from skillmcp.server import PROTOCOL_VERSION, TOOLS, Context, handle, serve  # noqa: E402
from skillmcp.validate import pack_issues, skill_issues, validate_pack  # noqa: E402

PHASES = ("setup", "design", "invoke", "verify", "govern", "document")


def run_cli(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    env = {"PYTHONPATH": str(ROOT / "src"), "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        [sys.executable, "-m", "skillmcp", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        input=stdin,
        timeout=120,
    )


@pytest.fixture()
def index() -> PackIndex:
    return PackIndex([ROOT])


@pytest.fixture()
def context(index: PackIndex) -> Context:
    return Context(index=index)


# ---------------------------------------------------------------- corpus shape


def test_pack_declares_fifty_and_delivers_fifty() -> None:
    assert PACK["expected_skills"] == 50
    assert len(SKILLS) == 50


def test_slugs_and_titles_are_unique() -> None:
    assert len({skill.slug for skill in SKILLS}) == 50
    assert len({skill.title.lower() for skill in SKILLS}) == 50


def test_every_skill_passes_every_rule() -> None:
    assert validate_pack(PACK, SKILLS) == []


def test_phases_are_known_and_balanced() -> None:
    counts: dict[str, int] = {}
    for skill in SKILLS:
        phase = skill.meta_get("phase")
        assert phase in PHASES
        counts[phase] = counts.get(phase, 0) + 1
    assert set(counts) == set(PHASES)
    assert min(counts.values()) >= 7
    assert max(counts.values()) <= 10


def test_word_floor_is_real_not_theoretical() -> None:
    counts = [word_count(render_skill(PACK, skill)) for skill in SKILLS]
    assert min(counts) >= 180
    assert sum(counts) / len(counts) > 200


def test_committed_skills_match_corpus_render() -> None:
    for skill in SKILLS:
        path = ROOT / "skills" / skill.slug / "SKILL.md"
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8") == render_skill(PACK, skill)


def test_pack_json_carries_descriptions_and_hashes() -> None:
    import hashlib

    manifest = json.loads((ROOT / "pack.json").read_text(encoding="utf-8"))
    assert manifest["skill_count"] == 50
    for entry in manifest["skills"]:
        assert entry["description"], entry["slug"]
        text = (ROOT / entry["path"]).read_text(encoding="utf-8")
        assert hashlib.sha256(text.encode("utf-8")).hexdigest() == entry["sha256"]


# -------------------------------------------------------------------- protocol


def test_parse_message_accepts_a_request() -> None:
    payload = parse_message('{"jsonrpc":"2.0","id":1,"method":"ping"}')
    assert payload["method"] == "ping"


def test_parse_message_rejects_bad_input() -> None:
    with pytest.raises(ProtocolError) as empty:
        parse_message("   ")
    assert empty.value.code == PARSE_ERROR

    with pytest.raises(ProtocolError) as broken:
        parse_message("{not json")
    assert broken.value.code == PARSE_ERROR

    with pytest.raises(ProtocolError) as version:
        parse_message('{"jsonrpc":"1.0","id":1,"method":"ping"}')
    assert version.value.code == INVALID_REQUEST

    with pytest.raises(ProtocolError) as shape:
        parse_message('["not","an","object"]')
    assert shape.value.code == INVALID_REQUEST


def test_text_content_shape() -> None:
    payload = text_content("hello")
    assert payload["content"][0] == {"type": "text", "text": "hello"}
    assert payload["isError"] is False


# -------------------------------------------------------------------- pack index


def test_index_discovers_this_pack(index: PackIndex) -> None:
    names = [pack.name for pack in index.packs]
    assert "skillmcp" in names
    assert len(index.skills) == 50
    assert index.find("get_skill") is None  # tool name, not a skill slug
    assert index.find(BY_SLUG["search-then-fetch-pattern"].slug) is not None


def test_read_skill_returns_text_and_rejects_unknown(index: PackIndex) -> None:
    entry, text = index.read_skill("publishing-a-pack-locally")
    assert entry.pack == "skillmcp"
    assert text.startswith("---\nname: publishing-a-pack-locally")
    with pytest.raises(LookupError):
        index.read_skill("nope")


def test_search_ranks_by_keyword(index: PackIndex) -> None:
    hits = index.search(["protocol"], limit=5)
    assert hits
    assert all(score > 0 for score, _ in hits)
    slugs = [skill.slug for _, skill in hits]
    assert any("protocol" in slug for slug in slugs)
    assert index.search(["zzzz-nothing"]) == []


def test_load_pack_rejects_a_directory_without_manifest(tmp_path: Path) -> None:
    with pytest.raises(PackError):
        load_pack(tmp_path)
    assert discover(tmp_path) == []


def test_discover_reads_a_second_pack(tmp_path: Path) -> None:
    pack = tmp_path / "tiny"
    (pack / "skills" / "demo").mkdir(parents=True)
    (pack / "skills" / "demo" / "SKILL.md").write_text(
        "---\nname: demo\ndescription: \"A demo skill. Use when testing.\"\n---\n\n# Demo\n",
        encoding="utf-8",
    )
    (pack / "pack.json").write_text(
        json.dumps(
            {
                "name": "tiny",
                "version": "0.1.0",
                "category": "test",
                "description": "tiny pack",
                "skill_count": 1,
                "skills": [
                    {
                        "slug": "demo",
                        "title": "Demo",
                        "path": "skills/demo/SKILL.md",
                        "tags": ["demo"],
                        "sha256": "0" * 64,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    packs = discover(tmp_path)
    assert [p.name for p in packs] == ["tiny"]
    assert packs[0].skills[0].description.startswith("A demo skill")
    found = PackIndex([tmp_path]).find("demo")
    assert found is not None and found.pack == "tiny"


# ------------------------------------------------------------------ server logic


def test_initialize_response_shape(context: Context) -> None:
    reply = handle(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2025-03-26", "capabilities": {}},
        },
        context,
    )
    assert reply is not None
    result = reply["result"]
    assert result["protocolVersion"] == PROTOCOL_VERSION
    assert "tools" in result["capabilities"]
    assert result["serverInfo"]["name"] == "skillmcp"
    assert reply["id"] == 1


def test_notifications_get_no_reply(context: Context) -> None:
    assert handle({"jsonrpc": "2.0", "method": "notifications/initialized"}, context) is None
    assert handle({"jsonrpc": "2.0", "method": "ping"}, context) is None


def test_tools_list_advertises_schemas(context: Context) -> None:
    reply = handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, context)
    assert reply is not None
    tools = reply["result"]["tools"]
    assert {tool["name"] for tool in tools} == {"list_packs", "search_skills", "get_skill"}
    for tool in tools:
        assert tool["description"]
        assert tool["inputSchema"]["type"] == "object"
        assert tool["inputSchema"]["additionalProperties"] is False
    assert len(TOOLS) == 3


def test_tools_call_search_and_get(context: Context) -> None:
    search = handle(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "search_skills", "arguments": {"query": "protocol", "limit": 3}},
        },
        context,
    )
    assert search is not None
    payload = json.loads(search["result"]["content"][0]["text"])
    assert payload["matches_total"] <= 3

    fetch = handle(
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "get_skill", "arguments": {"slug": "stdout-purity-check"}},
        },
        context,
    )
    assert fetch is not None
    assert fetch["result"]["content"][0]["text"].startswith("---\nname: stdout-purity-check")
    assert fetch["result"]["isError"] is False


def test_tool_call_errors(context: Context) -> None:
    missing = handle(
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "nope"}},
        context,
    )
    assert missing is not None
    assert missing["error"]["code"] == -32602

    bad_query = handle(
        {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {"name": "search_skills", "arguments": {}},
        },
        context,
    )
    assert bad_query is not None
    assert bad_query["error"]["code"] == -32602

    bad_limit = handle(
        {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {"name": "search_skills", "arguments": {"query": "a", "limit": 500}},
        },
        context,
    )
    assert bad_limit is not None
    assert bad_limit["error"]["code"] == -32602

    unknown_slug = handle(
        {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {"name": "get_skill", "arguments": {"slug": "nope"}},
        },
        context,
    )
    assert unknown_slug is not None
    assert unknown_slug["result"]["isError"] is True
    assert "unknown skill" in unknown_slug["result"]["content"][0]["text"]


def test_unknown_method(context: Context) -> None:
    reply = handle({"jsonrpc": "2.0", "id": 9, "method": "resources/list"}, context)
    assert reply is not None
    assert reply["error"]["code"] == METHOD_NOT_FOUND


def test_serve_handles_a_full_session(context: Context) -> None:
    lines = [
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
        json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}),
        "not json",
        json.dumps({"jsonrpc": "2.0", "id": 3, "method": "ping"}),
    ]
    stdout = io.StringIO()
    code = serve(io.StringIO("\n".join(lines) + "\n"), stdout, context)
    assert code == 0
    replies = [json.loads(line) for line in stdout.getvalue().splitlines()]
    assert [reply.get("id") for reply in replies] == [1, 2, None, 3]
    assert replies[2]["error"]["code"] == PARSE_ERROR


# -------------------------------------------------------------------------- CLI


def test_cli_validate_reports_fifty_of_fifty() -> None:
    proc = run_cli("validate")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "50/50 skills valid" in proc.stdout


def test_cli_index_and_tools() -> None:
    indexed = run_cli("index", "--packs-root", ".")
    assert indexed.returncode == 0
    assert "1 packs, 50 skills" in indexed.stdout

    tools = run_cli("tools")
    assert tools.returncode == 0
    assert "search_skills" in tools.stdout
    assert "required: query" in tools.stdout

    as_json = run_cli("tools", "--json")
    assert [tool["name"] for tool in json.loads(as_json.stdout)] == ["list_packs", "search_skills", "get_skill"]


def test_cli_call_round_trip() -> None:
    ok = run_cli("call", "list_packs", "--packs-root", ".")
    assert ok.returncode == 0
    payload = json.loads(ok.stdout)
    assert payload["skills_total"] == 50

    bad = run_cli("call", "get_skill", "--args", '{"slug":"nope"}', "--packs-root", ".")
    assert bad.returncode == 1
    assert "unknown skill" in bad.stdout

    malformed = run_cli("call", "get_skill", "--args", "{oops", "--packs-root", ".")
    assert malformed.returncode == 2


def test_cli_serve_over_stdio() -> None:
    stdin = (
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        + "\n"
        + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        + "\n"
    )
    proc = run_cli("serve", "--packs-root", ".", stdin=stdin)
    assert proc.returncode == 0, proc.stderr
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    assert len(lines) == 2
    # stdout purity: every line must parse as a JSON-RPC message.
    for line in lines:
        payload = json.loads(line)
        assert payload["jsonrpc"] == "2.0"
        assert "result" in payload or "error" in payload


def test_cli_list_show_and_search() -> None:
    listed = run_cli("list", "--phase", "govern")
    assert listed.returncode == 0
    assert listed.stdout.strip().endswith("skills")

    show = run_cli("show", SKILLS[0].slug)
    assert show.returncode == 0
    assert show.stdout.startswith(f"---\nname: {SKILLS[0].slug}")

    assert run_cli("show", "not-a-real-skill").returncode == 1

    search = run_cli("search", "protocol")
    assert search.returncode == 0
    assert search.stdout.strip() != ""

    nohit = run_cli("search", "zzzz-no-such-term")
    assert nohit.returncode == 1
    assert "no matches" in nohit.stdout


# ------------------------------------------------------------------ integrity


def test_pack_issues_catches_a_short_corpus() -> None:
    issues = pack_issues(PACK, SKILLS[:-1])
    assert any(issue.rule == "skill-count" for issue in issues)


def test_single_skill_rule_violations_are_reported() -> None:
    broken = dict(SKILLS[0].__dict__)
    broken["steps"] = ("one", "two")
    from skillmcp.model import skill_from_dict

    issues = skill_issues(PACK, skill_from_dict(broken), "")
    assert "steps-count" in {issue.rule for issue in issues}
