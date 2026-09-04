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

The first MCP tool call opens the OAuth browser flow for [Payments AI](https://payments.ai/).
