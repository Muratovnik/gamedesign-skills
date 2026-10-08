#!/usr/bin/env python3
"""Check packaging and local document structure, not design quality or discovery."""
from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator
from markdown_it import MarkdownIt
import yaml

from render import projections

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = MarkdownIt("commonmark").enable("table")


def frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("Missing YAML frontmatter")
    end = lines.index("---", 1)
    value = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(value, dict):
        raise ValueError("Frontmatter must be a mapping")
    return value


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.links.append(value)


def document(text: str) -> tuple[list[str], set[str]]:
    if text.startswith("---\n"):
        try:
            text = text.split("\n---\n", 1)[1]
        except IndexError:
            pass
    tokens = MARKDOWN.parse(text)
    links, anchors, seen = [], set(), {}
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            inline = tokens[index + 1]
            title = "".join(child.content for child in (inline.children or []) if child.type in {"text", "code_inline"})
            base = "".join(c for c in title.lower() if not unicodedata.category(c).startswith("P") or c in "-_").replace(" ", "-")
            number = seen.get(base, 0)
            seen[base] = number + 1
            anchors.add(base if number == 0 else f"{base}-{number}")
        pending = [token]
        while pending:
            node = pending.pop()
            pending.extend(node.children or [])
            if node.type == "link_open":
                links.append(node.attrGet("href"))
            elif node.type == "image":
                links.append(node.attrGet("src"))
            elif node.type in {"html_inline", "html_block"}:
                parser = HTMLLinks()
                parser.feed(node.content)
                links.extend(parser.links)
    return links, anchors


def inspect(root: Path) -> dict:
    errors, counters = [], {"skills": 0, "markdown_files": 0, "local_links": 0, "schemas": 0}
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    expected = {entry["name"] for entry in catalog["skills"]}
    actual = {path.name for path in (root / "skills").iterdir() if path.is_dir()}
    if expected != actual or len(expected) != 7 or len(catalog["skills"]) != 7:
        errors.append("Full bundle inventory differs from seven canonical skills")
    if {entry["id"] for entry in catalog["skills"]} != {f"S{n}" for n in range(7)}:
        errors.append("Skill identities are missing or duplicated")
    for name in sorted(expected):
        path = root / "skills" / name / "SKILL.md"
        try:
            content = path.read_text(encoding="utf-8")
            data = frontmatter(content)
            if data.get("name") != name:
                errors.append(f"{name}: frontmatter name mismatch")
            description = data.get("description", "")
            if not isinstance(description, str) or not (20 <= len(description) <= 1024):
                errors.append(f"{name}: invalid description")
            if "use" not in description.lower() or "skip" not in description.lower():
                errors.append(f"{name}: description must say when to use and skip")
            if data.get("license") != "MIT":
                errors.append(f"{name}: missing license")
            if any(not isinstance(v, str) for v in data.get("metadata", {}).values()):
                errors.append(f"{name}: metadata values must be strings")
            if "[TODO" in content or "TODO:" in content:
                errors.append(f"{name}: unfinished scaffold")
            counters["skills"] += 1
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{name}: {exc}")
    for relative, expected_text in projections(root).items():
        path = root / relative
        if not path.exists() or path.read_bytes() != expected_text.encode("utf-8"):
            errors.append(f"Stale generated file: {relative}")
    schemas = list((root / "skills").rglob("*.schema.json")) + [root / "tools/vendor/plugin.schema.json"]
    for path in schemas:
        try:
            Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
            counters["schemas"] += 1
        except Exception as exc:
            errors.append(f"{path.relative_to(root)}: invalid schema: {exc}")
    try:
        schema = json.loads((root / "tools/vendor/plugin.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(json.loads((root / "plugin.json").read_text(encoding="utf-8")))
    except Exception as exc:
        errors.append(f"Portable plugin schema: {exc}")
    documents = {}
    for path in root.rglob("*.md"):
        if any(part in {".git", ".venv", ".cache", ".private", ".state", "tmp", ".godot", "__pycache__", "dist", "evals"} for part in path.relative_to(root).parts):
            continue
        documents[path.resolve()] = document(path.read_text(encoding="utf-8"))
    counters["markdown_files"] = len(documents)
    for path, (links, _) in documents.items():
        for link in links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not (parsed.path or parsed.fragment):
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            counters["local_links"] += 1
            if not target.is_relative_to(root.resolve()) or not target.exists():
                errors.append(f"{path.relative_to(root)}: missing/outside link {link}")
            elif parsed.fragment and target in documents and unquote(parsed.fragment) not in documents[target][1]:
                errors.append(f"{path.relative_to(root)}: missing anchor {link}")
    for path in (root / "skills").rglob("*"):
        if "evals" in path.relative_to(root / "skills").parts or path.is_symlink():
            errors.append(f"Runtime contains evaluator material or symlink: {path.relative_to(root)}")
    if not all(counters.values()):
        errors.append("Empty inspected set")
    return {"status": "fail" if errors else "pass", "scope": "static structure only", "counts": counters, "errors": errors,
            "native_discovery": "not_observed", "behavioral_quality": "not_measured"}


if __name__ == "__main__":
    result = inspect(ROOT)
    print(json.dumps(result, indent=2))
    sys.exit(result["status"] != "pass")
