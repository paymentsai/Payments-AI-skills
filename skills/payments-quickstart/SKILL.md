---
name: payments-quickstart
description: Guide a new merchant through Payments AI onboarding and their first checkout link in under 5 minutes. Use when a developer wants to get started with Payments AI, create a merchant account, or create their first payment.
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
      "url": "https://stage.managed.payments.ai/api/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

Get your token at https://stage.managed.payments.ai/settings/developer-tools.

---

If the tool responds successfully, continue to Step 1.

## Step 1 — Gather merchant info

Ask the developer:

> What is your business name and email address? (These will be used to create your merchant account.)

Wait for their answer.

## Step 2 — Create merchant account

Call `create_merchant_account` with:
- `name`: the business name they provided
- `email`: the email they provided

Present the result:

```
Merchant account created.

Merchant ID:         {merchantId}
```

## Step 3 — Create first product

Ask the developer:

> What do you want to sell? Describe it in plain English — for example: "A $29/mo Pro plan with a 14-day trial" or "A one-time course on Python for beginners."

Wait for their answer. Also ask for their **Merchant ID** if it has not appeared in the conversation yet.

Translate their description into a `create_product` call. Infer the plan fields from their description:
- `name`: product name (max 30 chars)
- `merchantId`: their merchant ID
- `plans`: array with at least one plan:
  - `name`: plan display name (max 30 chars)
  - `currency`: `"usd"` (default unless stated otherwise)
  - `amount`: price in USD as a decimal (e.g. `29.00`)
  - `type`: `"recurring"` for subscriptions, `"one-time"` for single purchases, `"free-access"` for free
  - `billingPeriod`: `"month"`, `"year"`, `"week"`, or `"day"`
  - `periodLength`: `1` (default)
  - `freeTrial`: number of trial days if mentioned (optional)

Present the result:

```
Product and plan created.

Product ID:  {id}
Plan ID:     {planIds[0]}
```

If the product has multiple plans, list all plan IDs with their index (Plan 1, Plan 2, …).

## Step 4 — Checkout link

Say:

> Your product is ready. Here is your checkout link:
>
> `/payment/{planIds[0]}`
>
> Paste this link anywhere — your site, a landing page, an email, or a Notion page. Anyone who clicks it goes straight to checkout. Payments AI handles the payment, tax, and subscription renewal automatically.

If the product has multiple plans, output one checkout URL per plan ID.

## Done

Summarise what was set up in two sentences and offer to help with next steps (e.g. adding more products, checking transaction history, or understanding webhooks).
