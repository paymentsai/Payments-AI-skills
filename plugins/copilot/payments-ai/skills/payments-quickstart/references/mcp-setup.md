**Payments AI MCP server not detected.**

If you installed the Payments AI plugin (Claude Code, Cursor, Codex, Antigravity, Gemini CLI, or Copilot), reload the client so the bundled MCP server can connect, then retry. Otherwise add Payments AI to your MCP client config (`claude_desktop_config.json`, Cursor settings, Windsurf settings, or equivalent), restart, and re-run this skill.

Antigravity uses `serverUrl` in `mcp_config.json`. Gemini CLI uses `httpUrl` in `gemini-extension.json`. Other hosts typically use `url`.

Choose **one** of the two authentication methods below.

**Option A — OAuth (recommended).** No token to manage. Your client opens a browser to sign in and authorize, then returns automatically.

```json
{
  "mcpServers": {
    "payments-ai": {
      "url": "https://managed.payments.ai/api/mcp"
    }
  }
}
```

On first connect, approve the authorization in your browser. The client stores the token and refreshes it for you.

**Option B — Bearer token.** Configure a long-lived token in your local MCP client only (never paste it into chat). Mint tokens at https://managed.payments.ai/settings/developer-tools.

```json
{
  "mcpServers": {
    "payments-ai": {
      "url": "https://managed.payments.ai/api/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```
