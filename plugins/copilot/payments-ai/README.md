# Payments AI for GitHub Copilot / Agent Plugins

This package follows the [Agent Plugins](https://agent-plugins.org/) layout: root `plugin.json`, `mcp.json`, and `skills/`.

Copy or symlink the folder into the host's local plugins directory (Copilot / VS Code Agent Plugins, or any client that loads the standard), then reload.

The first MCP tool call opens OAuth for [Payments AI](https://payments.ai/).
