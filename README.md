# Payments AI skills

[Payments AI](https://payments.ai/) agent skills and MCP server, for Claude Code, Cursor, Codex, Antigravity, Gemini CLI, Copilot, and any other client that supports [Agent Skills](https://agentskills.io/).

Two ways to use this repository:

- **Install the skills** — copies `skills/` into your agent. Add the MCP server yourself.
- **Add the plugin** — registers this repo as a marketplace (or installs a host package) and bundles the same skills plus the MCP server.

After either path, ask:

```text
Help me get started with Payments AI.
```

The first MCP tool call opens a browser to connect your Payments AI account.

## Install skills

```bash
npx skills add paymentsai/Payments-AI-skills
```

That installs only what is in `skills/`. Point your client at the [Payments AI MCP server](https://payments.ai/mcp):

```json
{
  "mcpServers": {
    "payments-ai": {
      "url": "https://managed.payments.ai/api/mcp"
    }
  }
}
```

Antigravity uses `serverUrl` instead of `url`. Gemini CLI uses `httpUrl`.

## Add as a plugin

Add this GitHub repository as a marketplace, then install **Payments AI**.

### Claude Code

```text
/plugin marketplace add paymentsai/Payments-AI-skills
/plugin install payments-ai@payments-ai
```

### Cursor

```text
/add-plugin https://github.com/paymentsai/Payments-AI-skills
```

Then install **Payments AI** from Customize.

If you already cloned this repo, you can load the Cursor package locally instead:

```bash
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(pwd)/plugins/cursor/payments-ai" ~/.cursor/plugins/local/payments-ai
```

Reload the window and confirm the skills and the `payments-ai` MCP server in Customize.

### Codex

```bash
codex plugin marketplace add paymentsai/Payments-AI-skills \
  --sparse .agents/plugins \
  --sparse plugins/codex/payments-ai
```

Restart Codex and install **Payments AI**.

### Antigravity

```bash
agy plugin install https://github.com/paymentsai/Payments-AI-skills.git
agy plugin list
```

From a clone:

```bash
agy plugin install ./plugins/antigravity/payments-ai
```

### Gemini CLI

The gallery crawler needs `gemini-extension.json` at the repo root (topic `gemini-cli-extension`). Install from GitHub:

```bash
gemini extensions install https://github.com/paymentsai/Payments-AI-skills
gemini extensions list
```

From a clone, either the root or the host package works:

```bash
gemini extensions install .
gemini extensions install ./plugins/gemini/payments-ai
```

Consumer Gemini CLI is moving to Antigravity. Prefer the Antigravity package when that is the host in use.

### Copilot / Agent Plugins

This package is the portable [Agent Plugins](https://agent-plugins.org/) layout. Install or symlink `plugins/copilot/payments-ai` into the host's local plugins directory, then reload.

## Skills

| Skill | What it does |
| --- | --- |
| `payments-quickstart` | Merchant account → first product → sandbox checkout |
| `checkout-customization` | Hosted checkout theme, colors, font, input style, and logo |

## License

Apache 2.0. See `LICENSE`.
