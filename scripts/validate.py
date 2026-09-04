#!/usr/bin/env python3
"""Validate marketplace manifests, host packages, skills, and MCP copies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
MARKETPLACE_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
errors: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def read_json(path: Path, context: str) -> dict | None:
    if not path.is_file():
        error(f"{context} is missing: {path.relative_to(ROOT)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(f"{context} is invalid JSON ({path.relative_to(ROOT)}): {exc}")
        return None


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:closing].split("\n"):
        if ":" not in line or line.strip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def trees_equal(left: Path, right: Path, label: str) -> None:
    left_files = {p.relative_to(left): p for p in left.rglob("*") if p.is_file() and p.name != ".DS_Store"}
    right_files = {p.relative_to(right): p for p in right.rglob("*") if p.is_file() and p.name != ".DS_Store"}
    missing = sorted(left_files.keys() - right_files.keys())
    extra = sorted(right_files.keys() - left_files.keys())
    if missing:
        error(f"{label}: missing files {missing}")
    if extra:
        error(f"{label}: extra files {extra}")
    for rel in sorted(left_files.keys() & right_files.keys()):
        if left_files[rel].read_bytes() != right_files[rel].read_bytes():
            error(f"{label}: drift in {rel}")


def validate_skills(skills_dir: Path, context: str) -> None:
    if not skills_dir.is_dir():
        error(f"{context}: skills/ is missing")
        return
    skill_dirs = [p for p in skills_dir.iterdir() if p.is_dir()]
    if not skill_dirs:
        error(f"{context}: skills/ has no skill directories")
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            error(f"{context}: missing SKILL.md in {skill_dir.name}")
            continue
        fields = parse_frontmatter(skill_md)
        if not fields:
            error(f"{context}: {skill_dir.name}/SKILL.md is missing YAML frontmatter")
            continue
        for key in ("name", "description"):
            if not fields.get(key):
                error(f"{context}: {skill_dir.name}/SKILL.md missing frontmatter {key}")


def payments_url(data: dict | None, key: str) -> str | None:
    if not data:
        return None
    server = (data.get("mcpServers") or {}).get("payments-ai") or {}
    value = server.get(key)
    return value if isinstance(value, str) and value else None


def main() -> int:
    claude_market = read_json(ROOT / ".claude-plugin" / "marketplace.json", "Claude marketplace")
    cursor_market = read_json(ROOT / ".cursor-plugin" / "marketplace.json", "Cursor marketplace")
    codex_market = read_json(ROOT / ".agents" / "plugins" / "marketplace.json", "Codex marketplace")
    shared_mcp = read_json(ROOT / "shared" / "mcp.json", "shared MCP config")
    expected_url = payments_url(shared_mcp, "url")
    if not expected_url:
        error("shared/mcp.json must define mcpServers.payments-ai.url")

    if cursor_market:
        name = cursor_market.get("name")
        if not isinstance(name, str) or not MARKETPLACE_NAME.match(name):
            error('Cursor marketplace "name" must be kebab-case')
        owner = cursor_market.get("owner") or {}
        if not owner.get("name"):
            error('Cursor marketplace "owner.name" is required')
        plugins = cursor_market.get("plugins") or []
        if not plugins:
            error("Cursor marketplace plugins[] is empty")
        else:
            entry = plugins[0]
            if entry.get("name") != "payments-ai":
                error("Cursor plugin entry name must be payments-ai")
            if entry.get("source") != "./plugins/cursor/payments-ai":
                error("Cursor plugin source must be ./plugins/cursor/payments-ai")

    if claude_market:
        plugins = claude_market.get("plugins") or []
        if not plugins or plugins[0].get("source") != "./plugins/claude/payments-ai":
            error("Claude plugin source must be ./plugins/claude/payments-ai")

    if codex_market:
        plugins = codex_market.get("plugins") or []
        source = ((plugins[0] or {}).get("source") or {}) if plugins else {}
        if source.get("path") != "./plugins/codex/payments-ai":
            error("Codex plugin source.path must be ./plugins/codex/payments-ai")

    packages = {
        "claude": ROOT / "plugins" / "claude" / "payments-ai",
        "cursor": ROOT / "plugins" / "cursor" / "payments-ai",
        "codex": ROOT / "plugins" / "codex" / "payments-ai",
        "antigravity": ROOT / "plugins" / "antigravity" / "payments-ai",
        "gemini": ROOT / "plugins" / "gemini" / "payments-ai",
        "copilot": ROOT / "plugins" / "copilot" / "payments-ai",
    }
    manifests = {
        "claude": packages["claude"] / ".claude-plugin" / "plugin.json",
        "cursor": packages["cursor"] / ".cursor-plugin" / "plugin.json",
        "codex": packages["codex"] / ".codex-plugin" / "plugin.json",
        "antigravity": packages["antigravity"] / "plugin.json",
        "gemini": packages["gemini"] / "gemini-extension.json",
        "copilot": packages["copilot"] / "plugin.json",
    }
    mcp_checks = {
        "claude": (packages["claude"] / ".mcp.json", "url"),
        "cursor": (packages["cursor"] / "mcp.json", "url"),
        "codex": (packages["codex"] / ".mcp.json", "url"),
        "antigravity": (packages["antigravity"] / "mcp_config.json", "serverUrl"),
        "gemini": (packages["gemini"] / "gemini-extension.json", "httpUrl"),
        "copilot": (packages["copilot"] / "mcp.json", "url"),
    }

    for host, path in packages.items():
        if (path / ".claude-plugin").exists() and host != "claude":
            error(f"{host} package must not contain .claude-plugin/")
        if (path / ".cursor-plugin").exists() and host != "cursor":
            error(f"{host} package must not contain .cursor-plugin/")
        if (path / ".codex-plugin").exists() and host != "codex":
            error(f"{host} package must not contain .codex-plugin/")
        if (path / "gemini-extension.json").exists() and host != "gemini":
            error(f"{host} package must not contain gemini-extension.json")
        if (path / "mcp_config.json").exists() and host != "antigravity":
            error(f"{host} package must not contain mcp_config.json")

    if (ROOT / "gemini-extension.json").exists():
        error("gemini-extension.json must live under plugins/gemini/payments-ai, not the repo root")

    for host, path in manifests.items():
        data = read_json(path, f"{host} plugin manifest")
        if not data:
            continue
        name = data.get("name")
        if not isinstance(name, str) or not PLUGIN_NAME.match(name):
            error(f"{host}: plugin name must be kebab-case")
        if name != "payments-ai":
            error(f"{host}: plugin name must be payments-ai")
        if not data.get("description"):
            error(f"{host}: description is required")
        if host != "antigravity" and data.get("version") != "0.1.0":
            error(f"{host}: version must match 0.1.0")

    cursor_plugin = read_json(manifests["cursor"], "cursor plugin.json")
    if cursor_plugin and cursor_plugin.get("logo") != "assets/logo.svg":
        error("Cursor plugin logo must be assets/logo.svg")
    if not (packages["cursor"] / "assets" / "logo.svg").is_file():
        error("Cursor package is missing assets/logo.svg")
    if not (packages["codex"] / "assets" / "logo.svg").is_file():
        error("Codex package is missing assets/logo.svg")
    if not (packages["gemini"] / "GEMINI.md").is_file():
        error("Gemini package is missing GEMINI.md")

    copilot_plugin = read_json(manifests["copilot"], "copilot plugin.json")
    if copilot_plugin and not str(copilot_plugin.get("$schema") or "").startswith("https://agent-plugins.org/"):
        error("Copilot plugin.json must declare the Agent Plugins $schema")

    for host, (path, key) in mcp_checks.items():
        data = read_json(path, f"{host} MCP config")
        url = payments_url(data, key)
        if expected_url and url != expected_url:
            error(f"{host}: MCP {key} drifted from shared/mcp.json")
        if data and not url:
            error(f"{host}: MCP config must define payments-ai.{key}")

    root_mcp = ROOT / ".mcp.json"
    if root_mcp.exists() and expected_url:
        data = read_json(root_mcp, "root .mcp.json")
        if payments_url(data, "url") != expected_url:
            error("root .mcp.json drifted from shared/mcp.json")

    canonical = ROOT / "skills"
    validate_skills(canonical, "canonical skills")
    for host, path in packages.items():
        validate_skills(path / "skills", f"{host} package")
        trees_equal(canonical, path / "skills", f"{host} skills")

    if (ROOT / ".claude-plugin" / "plugin.json").exists():
        error("root .claude-plugin/plugin.json must be removed; Claude plugin lives under plugins/claude/payments-ai")

    if errors:
        print("Validation failed:")
        for item in errors:
            print(f"- {item}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
