# Host packages

This repository distributes **one plugin** (`payments-ai`) to several hosts. Canonical skills live in `/skills`. Host folders are self-contained packages; do not edit copied skills there.

MCP server work for Antigravity, Gemini CLI, and Copilot (OAuth and transport quirks) is tracked in [PAIM-911](https://masterborn.atlassian.net/browse/PAIM-911).

| Host | Marketplace / install index | Package | MCP file / key |
| --- | --- | --- | --- |
| Claude Code | `.claude-plugin/marketplace.json` | `plugins/claude/payments-ai/` | `.mcp.json` → `url` |
| Cursor | `.cursor-plugin/marketplace.json` | `plugins/cursor/payments-ai/` | `mcp.json` → `url` |
| Codex | `.agents/plugins/marketplace.json` | `plugins/codex/payments-ai/` | `.mcp.json` → `url` |
| Antigravity | `agy plugin install https://github.com/paymentsai/Payments-AI-skills.git` | `plugins/antigravity/payments-ai/` | `mcp_config.json` → `serverUrl` |
| Gemini CLI | gallery (`gemini-cli-extension` topic + root `gemini-extension.json`) | `plugins/gemini/payments-ai/` | `gemini-extension.json` → `httpUrl` |
| Copilot / Agent Plugins | host local plugins dir | `plugins/copilot/payments-ai/` | `mcp.json` → `url` |

## What each package contains

- Host-specific plugin manifest
- Bundled Payments AI MCP server pointing at `https://managed.payments.ai/api/mcp`
- A copy of `skills/` (quickstart + checkout customization)
- Logo for Cursor and Codex (`assets/logo.svg`)

Canonical MCP URL: `shared/mcp.json`. After editing skills, MCP, or the logo, run:

```bash
python3 scripts/sync_host_packages.py
python3 scripts/validate.py
```

CI runs the same validator on every pull request.
