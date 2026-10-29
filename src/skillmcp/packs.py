"""Index of skill packs on disk.

A pack is a directory containing ``pack.json`` and a ``skills/`` tree, which is
exactly what the packs in this project already ship. The index is rebuilt on
demand, so a pack edited on disk is visible without restarting the server.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


class PackError(ValueError):
    """Raised when a directory does not contain a readable pack."""


@dataclass(frozen=True)
class SkillEntry:
    pack: str
    slug: str
    title: str
    description: str
    tags: tuple[str, ...]
    phase: str
    path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "pack": self.pack,
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "tags": list(self.tags),
            "phase": self.phase,
            "path": self.path,
        }


@dataclass
class Pack:
    name: str
    version: str
    category: str
    description: str
    root: Path
    skills: list[SkillEntry] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "category": self.category,
            "description": self.description,
            "skills": len(self.skills),
            "root": str(self.root),
        }


def _read_manifest(root: Path) -> dict[str, Any]:
    manifest_path = root / "pack.json"
    if not manifest_path.is_file():
        raise PackError(f"{root} has no pack.json")
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PackError(f"{manifest_path} is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict) or "name" not in payload:
        raise PackError(f"{manifest_path} is not a pack manifest")
    return payload


def _frontmatter_description(path: Path) -> str:
    """Read the description field out of a SKILL.md frontmatter block."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    for line in text[3:end].splitlines():
        if line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            if value.startswith("\"") and value.endswith("\""):
                try:
                    return str(json.loads(value))
                except json.JSONDecodeError:
                    return value.strip("\"")
            return value
    return ""


def load_pack(root: Path) -> Pack:
    """Read one pack directory into memory, skipping entries without files."""
    manifest = _read_manifest(root)
    pack = Pack(
        name=str(manifest.get("name", root.name)),
        version=str(manifest.get("version", "0.0.0")),
        category=str(manifest.get("category", "")),
        description=str(manifest.get("description", "")),
        root=root,
    )
    for raw in manifest.get("skills", []):
        if not isinstance(raw, dict):
            continue
        rel = str(raw.get("path", ""))
        if not rel:
            continue
        path = root / rel
        if not path.is_file():
            continue
        meta = {key[5:]: value for key, value in raw.items() if key.startswith("meta_")}
        description = str(raw.get("description") or "")
        if not description:
            # Packs written before descriptions existed in the manifest still
            # need per-skill text, otherwise search only sees the pack summary.
            description = _frontmatter_description(path) or pack.description
        pack.skills.append(
            SkillEntry(
                pack=pack.name,
                slug=str(raw.get("slug", "")),
                title=str(raw.get("title", "")),
                description=description,
                tags=tuple(str(tag) for tag in raw.get("tags", [])),
                phase=str(meta.get("phase", "")),
                path=str(path),
            )
        )
    return pack


def discover(root: Path) -> list[Pack]:
    """Find every pack under ``root``: the root itself, then one level down."""
    packs: list[Pack] = []
    if (root / "pack.json").is_file():
        try:
            packs.append(load_pack(root))
        except PackError:
            pass
    for child in sorted(root.iterdir()) if root.is_dir() else []:
        if not child.is_dir():
            continue
        if not (child / "pack.json").is_file():
            continue
        try:
            packs.append(load_pack(child))
        except PackError:
            continue
    return packs


class PackIndex:
    """Searchable view over one or more packs, rebuilt from disk per request."""

    def __init__(self, roots: Iterable[Path]) -> None:
        self.roots = [Path(root) for root in roots]
        self.packs: list[Pack] = []
        self._digests: dict[str, str] = {}
        self.reload()

    def reload(self) -> None:
        packs: list[Pack] = []
        for root in self.roots:
            packs.extend(discover(root))
        self.packs = packs

    @property
    def skills(self) -> list[SkillEntry]:
        return [skill for pack in self.packs for skill in pack.skills]

    def pack_by_name(self, name: str) -> Pack | None:
        for pack in self.packs:
            if pack.name == name:
                return pack
        return None

    def find(self, slug: str, pack: str | None = None) -> SkillEntry | None:
        for skill in self.skills:
            if skill.slug != slug:
                continue
            if pack and skill.pack != pack:
                continue
            return skill
        return None

    def read_skill(self, slug: str, pack: str | None = None) -> tuple[SkillEntry, str]:
        entry = self.find(slug, pack)
        if entry is None:
            where = f" in pack {pack!r}" if pack else ""
            raise LookupError(f"unknown skill {slug!r}{where}")
        path = Path(entry.path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise LookupError(f"cannot read {path}: {exc}") from exc
        self._digests[str(path)] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return entry, text

    def search(self, terms: list[str], *, limit: int = 10, pack: str | None = None) -> list[tuple[int, SkillEntry]]:
        """Rank skills by term frequency over slug, title, tags and description."""
        lowered = [term.lower() for term in terms if term.strip()]
        scored: list[tuple[int, SkillEntry]] = []
        for skill in self.skills:
            if pack and skill.pack != pack:
                continue
            haystack = " ".join(
                [skill.slug, skill.title, " ".join(skill.tags), skill.description]
            ).lower()
            score = sum(haystack.count(term) for term in lowered)
            if score:
                scored.append((score, skill))
        scored.sort(key=lambda pair: (-pair[0], pair[1].pack, pair[1].slug))
        return scored[:limit]
