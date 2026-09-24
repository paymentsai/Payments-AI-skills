---
name: checkout-customization
description: Official Payments AI checkout branding — theme, colors, fonts, input style, and logo over MCP. Use when a developer wants to customize or brand their hosted checkout, change checkout colors or theme, or set the checkout logo.
license: Apache-2.0
compatibility: Requires the official Payments AI MCP server (https://doc.managed.payments.ai/mcp). Network access to managed.payments.ai over HTTPS.
metadata:
  author: paymentsai
  homepage: https://payments.ai
  repository: https://github.com/paymentsai/Payments-AI-skills
---

# Payments AI Checkout Customization

Official first-party skill from [Payments AI](https://payments.ai). Source repository: https://github.com/paymentsai/Payments-AI-skills. MCP documentation: https://doc.managed.payments.ai/mcp.

Gated branding of the hosted checkout at `https://managed.payments.ai/payment/{planId}`: complete each step and wait for input before the next.

## Security and data handling

- **First-party endpoint only.** Use the Payments AI MCP server at `https://managed.payments.ai/api/mcp`. Do not substitute other URLs or proxies.
- **OAuth preferred.** Recommend Option A in [references/mcp-setup.md](references/mcp-setup.md). The MCP client stores and refreshes tokens; never ask the developer to paste a bearer token into chat.
- **Merchant ID only.** Collect the merchant ID at Step 1. Do not log or repeat credentials.

## Step 0 — MCP health

Call `get_my_merchant`. It takes no arguments and doubles as a liveness and authorization check.

Complete when the tool returns successfully (an empty result is normal — it just means no merchant exists yet). If the call fails or the tool is missing, read [references/mcp-setup.md](references/mcp-setup.md), paste that setup to the developer, and stop.

If a later step returns "Insufficient scope", the MCP connection needs `checkout:read` and `checkout:write` scopes. Recommend Option A (OAuth) in [references/mcp-setup.md](references/mcp-setup.md). If using Option B, tell the developer to mint a token with those scopes at https://managed.payments.ai/developer-tools and configure it in their local MCP client only — never paste the token into chat.

## Step 1 — Merchant ID

Ask if it is not already in the conversation:

> What is your Merchant ID? (It looks like a UUID — you got it when you created your merchant account.)

Complete when you have a merchant ID.

## Step 2 — Current branding

Call `get_checkout_customization` with `merchantId`.

Present:

```
Current checkout branding:

Theme mode:        {themeMode or "default"}
Background color:  {backgroundColor or "default"}
Button color:      {buttonColor or "default"}
Button text color: {buttonTextColor or "default"}
Font color:        {fontColor or "default"}
Font family:       {fontFamily or "default"}
Input style:       {inputStyle or "default"}
Logo:              {logoUrl ? "set" : "none"}
```

Complete when every field above has been shown.

## Step 3 — Gather changes

Ask:

> What would you like to change? For example: "dark theme with a blue button", "use the Roboto font", "make the background #0E0E10", or "set my checkout logo".

Translate into:
- **themeMode** — `light` or `dark`
- **backgroundColor**, **buttonColor**, **buttonTextColor**, **fontColor** — 6-digit hex with leading `#`, e.g. `#0A84FF`
- **fontFamily** — `Inter` or `Roboto`
- **inputStyle** — `rounded` or `square`
- **logo** — a local image path (png, jpeg, or webp, ≤ 5 MB)

Complete when the request is mapped onto those fields (and a file path, if they want a logo).

## Step 4 — Apply

If any theme, color, font, or input field is changing, **merge** via `update_checkout_customization`:
- `merchantId`: their merchant ID
- `customization`: nested object of **only the fields that are changing**, e.g. `{ "themeMode": "dark", "buttonColor": "#0A84FF" }`

Omitted fields keep their current value. Nest them under `customization`; a flat top-level update is rejected.

Present the full merged customization the tool returns:

```
Checkout branding updated.

{list each field and its new value}
```

If they asked to **remove** or **reset** a field to default, clearing is done from the dashboard (https://managed.payments.ai/developer-tools) — not over MCP.

If they asked for a logo, follow [references/set-logo.md](references/set-logo.md).

Complete when every requested change is on screen (merged fields and/or logo).

## Done

Complete when the summary names every field that changed. To preview, call `list_products` and open a plan's returned `checkoutUrl` — it already points at sandbox or live depending on where the merchant is, so there is no path to assemble and no query param to remember.
