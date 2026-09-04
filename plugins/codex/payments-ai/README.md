# Payments AI for Codex

Add this repository as a Codex marketplace, then install **Payments AI**:

```bash
codex plugin marketplace add paymentsai/Payments-AI-skills \
  --sparse .agents/plugins \
  --sparse plugins/codex/payments-ai
```

Restart Codex and install **Payments AI** from the plugin directory. The first MCP tool call opens the OAuth browser flow for [Payments AI](https://payments.ai/).
