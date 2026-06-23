# Payments AI skills

This repository contains Agent Skills for [Payments AI](https://paidev.dev/)

# Installation

```bash
npx skills@latest add paymentsai/Payments-AI-skills
```

From the `npx install` command, you can select the specific skills from this
repo to install.

## Available Skills

### `payments-quickstart`

Guided wizard that takes a new merchant from zero to their first checkout link in under 5 minutes.

**Flow:** detects MCP server config → provisions sandbox → creates first product via plain-English description → returns embeddable checkout link.

**Trigger:** `/payments-quickstart` or ask *"help me get started with Payments AI"*.

Requires the [Payments AI MCP server](https://paidev.dev) to be configured in your MCP client.

### `checkout-customization`

Guided flow to brand a merchant's hosted checkout — theme mode, colors, font family, and input style.

**Flow:** detects MCP server config → reads current branding (`get_checkout_customization`) → applies the requested changes via a partial merge (`update_checkout_customization`, omitted fields unchanged).

**Trigger:** `/checkout-customization` or ask *"customize my checkout"* / *"change my checkout colors"*.

Requires the [Payments AI MCP server](https://paidev.dev) to be configured in your MCP client.

## License

You are free to copy, modify, and distribute these skills under the terms of the
Apache 2.0 license. See the `LICENSE` file for details.
