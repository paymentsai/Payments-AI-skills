# Payments AI for Gemini CLI

The public gallery indexes the **repo root** (`gemini-extension.json` + `GEMINI.md`). Install from GitHub:

```bash
gemini extensions install https://github.com/paymentsai/Payments-AI-skills
gemini extensions list
```

From a clone of this repository:

```bash
gemini extensions install .
gemini extensions list
```

The self-contained host package is the same extension:

```bash
gemini extensions install ./plugins/gemini/payments-ai
```

Restart Gemini CLI after install. On the first MCP tool call your client opens a browser or prints a sign-in URL for [Payments AI](https://payments.ai/).

Google is moving consumer Gemini CLI users to Antigravity CLI. Prefer `plugins/antigravity/payments-ai` when that is the host in use.

MCP uses `httpUrl` inside `gemini-extension.json`. See [Gemini CLI extensions](https://geminicli.com/docs/extensions/).
