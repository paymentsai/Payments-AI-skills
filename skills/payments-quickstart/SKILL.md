---
name: payments-quickstart
description: Gated Payments AI onboarding from merchant account to first sandbox checkout. Use when a developer wants to get started with Payments AI, create a merchant account, or create their first payment.
---

# Payments AI Quickstart

Gated wizard: complete each step and wait for the developer's input before the next.

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

## Step 4 — Sandbox checkout link

MCP creates products on **sandbox**. Say:

> Your product is ready. Here is your **sandbox** checkout link for testing:
>
> `https://managed.payments.ai/payment/{planIds[0]}?isSandbox=true`
>
> Paste this link anywhere — your site, a landing page, an email, or a Notion page.
>
> After you go live and the plan exists on production, use `https://managed.payments.ai/payment/{planIds[0]}`.

If there are multiple plans, output one sandbox URL per plan ID. Complete when every plan has a sandbox URL (`?isSandbox=true`) on screen. Share the live URL (no query param) only after `go_live` and the plan exists on live.

## Done

Complete when the summary names the merchant ID, product ID, every plan ID, and the sandbox vs live URL distinction. Offer next steps (more products, webhooks, or checkout branding via `/checkout-customization`).
