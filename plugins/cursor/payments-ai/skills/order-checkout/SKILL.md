---
name: order-checkout
description: Order checkout with create_order. Use when the buyer pays for several items in one checkout, the caller sets the price, or the buyer pays on the order's hosted checkout link.
license: Apache-2.0
compatibility: Requires the official Payments AI MCP server (https://doc.managed.payments.ai/mcp). Network access to managed.payments.ai over HTTPS.
metadata:
  author: paymentsai
  homepage: https://payments.ai
  repository: https://github.com/paymentsai/Payments-AI-skills
---

# Payments AI Order Checkout

Finish each step before the next. One catalogue plan stays on `payments-quickstart` and that plan's returned `checkoutUrl`.

## Security and data handling

- **First-party endpoint only.** Use the Payments AI MCP server at `https://managed.payments.ai/api/mcp`.
- **OAuth preferred.** Recommend Option A in [references/mcp-setup.md](references/mcp-setup.md). The MCP client stores and refreshes tokens. A bearer token stays in the local MCP client, never in chat.
- **`checkout:write`.** `create_order` requires it. On "Insufficient scope", recommend Option A in [references/mcp-setup.md](references/mcp-setup.md). For Option B, the developer mints a token with that scope at https://managed.payments.ai/developer-tools and configures it locally.
- **Hosted checkout.** `create_order` runs from this agent or the merchant's server. The buyer pays on the returned `checkoutUrl`.

## Step 0 — MCP health

Call `get_my_merchant`. It takes no arguments and doubles as a liveness and authorization check.

Complete when the tool returns successfully (an empty result means no merchant exists yet). If the call fails or the tool is missing, read [references/mcp-setup.md](references/mcp-setup.md), paste that setup to the developer, and stop.

## Step 1 — Merchant ID

Ask if it is not already in the conversation:

> What is your Merchant ID? (It looks like a UUID — you got it when you created your merchant account.)

Complete when you have a merchant ID.

## Step 2 — The order

Ask:

> What is the buyer paying for in this checkout? List each item. For a product you already created, give the plan ID and quantity. For a price you are setting, give the label, the price in dollars, the quantity, and whether it is one-time or recurring.

Collect:

- `merchantId`
- `currency`: 3 letters, `"usd"` unless they stated otherwise
- `items`: 1 to 20

A **catalogue** item is `{ planId, quantity }`. The price comes from the plan.

A **caller-priced** item is `{ label, unitPrice, quantity, type }`. You set `unitPrice` in decimal dollars (`10` means $10.00). `type` is `one_time` or `recurring`. Recurring also needs `billingPeriod` (`day`, `week`, `month`, or `year`) and `periodLength`. `create_product` spells one-time as `one-time`; `create_order` spells it `one_time`.

The two shapes stay separate. A mix of `planId` with `label` or `unitPrice` on one item is rejected.

One billing schedule per order. A different cart is a new order. The call accepts `merchantId`, `currency`, `items`, and an optional `idempotencyKey` (1–255 characters). A promo code is rejected. The same `idempotencyKey` returns the same `orderId`; omit it to create a new order. Pass it only when they want to reuse an order.

Complete when `currency` is 3 letters and every item is catalogue (`planId`, `quantity`) or caller-priced (`label`, `unitPrice`, `quantity`, `type`, plus `billingPeriod` and `periodLength` when `type` is `recurring`).

## Step 3 — Create the order

Call `create_order` with `merchantId`, `currency`, and `items`. Include `idempotencyKey` only when Step 2 collected one.

Present:

```
Order created.

Order ID:      {orderId}
Checkout URL:  {checkoutUrl}
```

Use `orderId` and `checkoutUrl` verbatim. Send the buyer to `checkoutUrl`. That hosted page shows the items and takes payment. While the merchant is on sandbox the link ends in `?isSandbox=true`. `go_live` copies nothing: that sandbox link never becomes a live link. After go-live, call `create_order` again with the same `merchantId` and items; share the new `checkoutUrl`, which has no `?isSandbox=true`. An assembled URL 404s. Tax is one line added on top of the pre-tax amount, and it first appears on the receipt.

Say:

> Send the buyer to this checkout link:
>
> `{checkoutUrl}`

Complete when `orderId` and `checkoutUrl` are on screen.

## Done

Complete when the summary names the order ID and the checkout URL. Offer checkout branding via `/checkout-customization`.
