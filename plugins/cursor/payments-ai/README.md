# Payments AI for Cursor

After the plugin is listed on the Cursor Marketplace:

```text
/add-plugin payments-ai
```

Until then, test a local copy:

```bash
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(pwd)/plugins/cursor/payments-ai" ~/.cursor/plugins/local/payments-ai
```

Reload the Cursor window, then confirm **Payments AI** skills and the `payments-ai` MCP server in Customize.

On the first MCP tool call your client opens a browser or prints a sign-in URL for [Payments AI](https://payments.ai/).
