#!/usr/bin/env python3
"""Copy canonical skills, MCP config, and logo into each host package."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL_SKILLS = ROOT / "skills"
CANONICAL_MCP = ROOT / "shared" / "mcp.json"
CANONICAL_LOGO = ROOT / "assets" / "logo.svg"

HOSTS = {
    "claude": {
        "dir": ROOT / "plugins" / "claude" / "payments-ai",
        "mcp_kind": "url",
        "mcp_name": ".mcp.json",
        "copy_logo": False,
    },
    "cursor": {
        "dir": ROOT / "plugins" / "cursor" / "payments-ai",
        "mcp_kind": "url",
        "mcp_name": "mcp.json",
        "copy_logo": True,
    },
    "codex": {
        "dir": ROOT / "plugins" / "codex" / "payments-ai",
        "mcp_kind": "url",
        "mcp_name": ".mcp.json",
        "copy_logo": True,
    },
    "antigravity": {
        "dir": ROOT / "plugins" / "antigravity" / "payments-ai",
        "mcp_kind": "serverUrl",
        "mcp_name": "mcp_config.json",
        "copy_logo": False,
    },
    "gemini": {
        "dir": ROOT / "plugins" / "gemini" / "payments-ai",
        "mcp_kind": "httpUrl",
        "mcp_name": "gemini-extension.json",
        "copy_logo": False,
    },
    "copilot": {
        "dir": ROOT / "plugins" / "copilot" / "payments-ai",
        "mcp_kind": "url",
        "mcp_name": "mcp.json",
        "copy_logo": False,
    },
}


def copy_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns(".DS_Store"))


def mcp_url(canonical: dict) -> str:
    return canonical["mcpServers"]["payments-ai"]["url"]


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_host_mcp(host_dir: Path, spec: dict, canonical: dict) -> None:
    url = mcp_url(canonical)
    kind = spec["mcp_kind"]
    target = host_dir / spec["mcp_name"]
    if kind == "url":
        write_json(target, {"mcpServers": {"payments-ai": {"url": url}}})
        return
    if kind == "serverUrl":
        write_json(target, {"mcpServers": {"payments-ai": {"serverUrl": url}}})
        return
    if kind == "httpUrl":
        if not target.is_file():
            raise SystemExit(f"missing {target.relative_to(ROOT)}")
        data = json.loads(target.read_text(encoding="utf-8"))
        servers = data.setdefault("mcpServers", {})
        payments = servers.setdefault("payments-ai", {})
        payments["httpUrl"] = url
        payments.pop("url", None)
        payments.pop("serverUrl", None)
        write_json(target, data)
        return
    raise SystemExit(f"unknown mcp_kind {kind}")


def sync_host(name: str, spec: dict, canonical: dict) -> None:
    host_dir: Path = spec["dir"]
    host_dir.mkdir(parents=True, exist_ok=True)
    copy_tree(CANONICAL_SKILLS, host_dir / "skills")
    write_host_mcp(host_dir, spec, canonical)
    if spec["copy_logo"]:
        assets = host_dir / "assets"
        assets.mkdir(exist_ok=True)
        shutil.copy2(CANONICAL_LOGO, assets / "logo.svg")
    print(f"synced {name} -> {host_dir.relative_to(ROOT)}")


def main() -> None:
    if not CANONICAL_SKILLS.is_dir():
        raise SystemExit("canonical skills/ directory is missing")
    if not CANONICAL_MCP.is_file():
        raise SystemExit("shared/mcp.json is missing")
    canonical = json.loads(CANONICAL_MCP.read_text(encoding="utf-8"))
    shutil.copy2(CANONICAL_MCP, ROOT / ".mcp.json")
    for name, spec in HOSTS.items():
        sync_host(name, spec, canonical)
    print("host packages synced")


if __name__ == "__main__":
    main()
