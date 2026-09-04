# Payments AI for Gemini CLI

Install from a clone of this repository:

```bash
gemini extensions install ./plugins/gemini/payments-ai
gemini extensions list
```

Restart Gemini CLI after install. The first MCP tool call opens OAuth for [Payments AI](https://payments.ai/).

Google is moving consumer Gemini CLI users to Antigravity CLI. Prefer `plugins/antigravity/payments-ai` when that is the host in use.

MCP uses `httpUrl` inside `gemini-extension.json`. See [Gemini CLI extensions](https://geminicli.com/docs/extensions/).
