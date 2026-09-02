# Payments AI skills

This repository contains Agent Skills for [Payments AI](https://payments.ai/)

# Installation

**Claude Code:** install the plugin — registers both skills and the Payments AI MCP server in one go, no manual JSON editing:

```bash
/plugin marketplace add paymentsai/Payments-AI-skills
/plugin install payments-ai@payments-ai
```

The first tool call opens the OAuth browser flow to connect your Payments AI account.

**Other clients (Cursor, Windsurf, etc.):** install just the skills:

```bash
npx skills@latest add paymentsai/Payments-AI-skills
```

From the `npx install` command, you can select the specific skills from this
repo to install. You'll still need to add the [Payments AI MCP server](https://payments.ai/mcp) to your client separately.

## Available Skills

### `payments-quickstart`

Gated wizard from merchant account to first sandbox checkout.

**Flow:** MCP health → create merchant → first product from a plain-English description → sandbox checkout link (`?isSandbox=true`).

**Trigger:** `/payments-quickstart` or ask *"help me get started with Payments AI"*.

Requires the [Payments AI MCP server](https://payments.ai) to be configured in your MCP client.

### `checkout-customization`

Gated branding of a merchant's hosted checkout — theme, colors, font, input style, and logo.

**Flow:** MCP health → read current branding (`get_checkout_customization`) → merge field changes (`update_checkout_customization`) and, when asked, set the logo (`set_checkout_logo`).

**Trigger:** `/checkout-customization` or ask *"customize my checkout"* / *"set my checkout logo"*.

Requires the [Payments AI MCP server](https://payments.ai) to be configured in your MCP client.

## License

You are free to copy, modify, and distribute these skills under the terms of the
Apache 2.0 license. See the `LICENSE` file for details.
