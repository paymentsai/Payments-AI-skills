---
name: payments-quickstart
description: Guide a new merchant through Payments AI sandbox setup and their first checkout link in under 5 minutes. Use when a developer wants to get started with Payments AI, provision a sandbox environment, or create their first payment.
---

# Payments AI Quickstart

Walk the developer through the full setup flow, one step at a time. Do not skip ahead. Wait for confirmation or input at each step before proceeding.

## Step 0 — Verify MCP server is configured

Call the `payments_ai_health` tool.

If the call fails or the tool is not found, output the following and stop:

---

**Payments AI MCP server not detected.**

Add this to your MCP client config (`claude_desktop_config.json`, Cursor settings, Windsurf settings, or equivalent), then restart your client and run `/payments-quickstart` again.

```json
{
  "mcpServers": {
    "payments-ai": {
      "url": "https://dev.managed.payments.ai/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

Get your token at https://dev.managed.payments.ai/settings/developer-tools.

---

If the tool responds successfully, continue to Step 1.

## Step 1 — Gather merchant info

Ask the developer:

> What is your business name and email address? (These will be used to provision your sandbox environment.)

Wait for their answer.

## Step 2 — Provision sandbox

Call `provision_sandbox_environment` with:
- `name`: the business name they provided
- `email`: the email they provided

Present the result:

```
Sandbox provisioned.

Merchant ID:         {merchantId}
```

Then add:

> ⚠️ These keys are illustrative placeholders during the current preview period. Real credentials will be issued when live provisioning is enabled for your account.

## Step 3 — Create first product

Ask the developer:

> What do you want to sell? Describe it in plain English — for example: "A $29/mo Pro plan with a 14-day trial" or "A one-time course on Python for beginners."

Wait for their answer. Also ask for their **Merchant ID** if it has not appeared in the conversation yet.

Call `assist_agent` with:
- `message`: their product description
- `merchantId`: their merchant ID

Present the result:

```
Product created.

Product ID:  {productId}
Plan ID:     {planId}
```

## Step 4 — Checkout embed

Show the checkout link returned by `assist_agent`:

```html
{checkoutHtml}
```

Then say:

> Paste this anywhere — your site, a landing page, an email, or a Notion page. Anyone who clicks it goes straight to checkout. Payments AI handles the payment, tax, and subscription renewal automatically.

## Done

Summarise what was set up in two sentences and offer to help with next steps (e.g. adding more products, checking transaction history, or understanding webhooks).
