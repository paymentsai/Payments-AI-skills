---
name: payments-quickstart
description: Official Payments AI onboarding — merchant account, product, and sandbox checkout via MCP. Use when a developer wants to get started with Payments AI, integrate payments, create a merchant account, or build their first checkout link.
license: Apache-2.0
compatibility: Requires the official Payments AI MCP server (https://doc.managed.payments.ai/mcp). Network access to managed.payments.ai over HTTPS.
metadata:
  author: paymentsai
  homepage: https://payments.ai
  repository: https://github.com/paymentsai/Payments-AI-skills
---

# Payments AI Quickstart

Official first-party skill from [Payments AI](https://payments.ai). Source repository: https://github.com/paymentsai/Payments-AI-skills. MCP documentation: https://doc.managed.payments.ai/mcp.

Gated wizard: complete each step and wait for the developer's input before the next.

## Security and data handling

- **First-party endpoint only.** Use the Payments AI MCP server at `https://managed.payments.ai/api/mcp`. Do not substitute other URLs or proxies.
- **OAuth preferred.** Recommend Option A in [references/mcp-setup.md](references/mcp-setup.md). The MCP client stores and refreshes tokens; never ask the developer to paste a bearer token into chat.
- **PII with consent.** Collect business name, email, and phone only at Step 1 after the developer provides them. Pass those fields only to `create_merchant_account`. Do not log or repeat credentials.
- **Sandbox by default.** `create_product` creates sandbox resources. Share checkout links with `?isSandbox=true` until the merchant has gone live on production.

## Step 0 — MCP health

Call `payments_ai_health`.

Complete when the tool returns successfully. If the call fails or the tool is missing, read [references/mcp-setup.md](references/mcp-setup.md), paste that setup to the developer, and stop.

## Step 1 — Merchant info

Ask:

> What is your business name, email address, and phone number in E.164 format with country code (e.g. `+14155552671`)? These will be used to create your merchant account.

Complete when you have name, email, and an E.164 phone (leading `+` and country code). If the phone is missing either, ask them to correct it.

## Step 2 — Create merchant account

Call `create_merchant_account` with `name`, `email`, and `phone` from Step 1.

Present:

```
Merchant account created.

Merchant ID:         {merchantId}
```

Complete when that merchant ID is on screen.

## Step 3 — First product

Ask:

> What do you want to sell? Describe it in plain English — for example: "A $29/mo Pro plan with a 14-day trial" or "A one-time course on Python for beginners."

Complete when you have the description and a merchant ID (from Step 2, or asked for if it is not in the conversation).

Call `create_product`, inferring:
- `name`: product name (max 30 chars)
- `merchantId`: their merchant ID
- `plans`: array with at least one plan:
  - `name`: plan display name (max 30 chars)
  - `currency`: `"usd"` unless they stated otherwise
  - `amount`: price in USD as a decimal (e.g. `29.00`)
  - `type`: `"recurring"` | `"one-time"` | `"free-access"`
  - `billingPeriod`: `"month"` | `"year"` | `"week"`
  - `periodLength`: `1` unless they stated otherwise
  - `freeTrial`: trial days if mentioned

Present:

```
Product and plan created.

Product ID:  {id}
Plan ID:     {planIds[0]}
```

If there are multiple plans, list every plan ID with its index (Plan 1, Plan 2, …). Complete when every returned product ID and plan ID has been presented.

## Step 4 — Checkout link

`create_product` already returned the link. Read `checkoutUrl` from its response and
use it exactly as returned — never assemble one from the plan ID.

The returned URL is already correct for where the merchant actually is: it carries
`?isSandbox=true` until `go_live` succeeds and drops it afterwards, so there is
nothing for you to switch. A hand-assembled link can only be right by coincidence —
pointing at the live path before go-live resolves to `404 Plan not found`.

Say:

> Your product is ready. Here is your checkout link:
>
> `{checkoutUrl}`
>
> Paste this link anywhere — your site, a landing page, an email, or a Notion page.

While the merchant is still on sandbox the link ends in `?isSandbox=true`, which is
the test checkout — real cards are not charged. It becomes the live link on its own
once `go_live` succeeds; re-read it from `list_products` after that rather than
editing the one you already showed.

If there are multiple plans, `planCheckoutUrls` holds one `{planId, checkoutUrl}`
entry per plan — output each `checkoutUrl` verbatim. Complete when every plan has a
returned URL on screen.

## Done

Complete when the summary names the merchant ID, product ID, every plan ID, and the sandbox vs live URL distinction. Offer next steps (more products, webhooks, or checkout branding via `/checkout-customization`).
