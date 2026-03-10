# MCP-perplexica

*"Stop asking Google. Start discovering."*

This little server bridges the gap between Perplexica and any MCP-compatible AI assistant. Think of it as your research companion that never sleeps, never judges your weird search queries, and actually understands what you're trying to find.

## What is Perplexica?

Perplexica is an open-source AI-powered search engine that actually understands your questions. Unlike traditional search that throws keywords at you, Perplexica uses AI to dig into the web and find what you actually need — with sources, no less.

- **Source**: [github.com/ItzCrazyKns/Vane](https://github.com/ItzCrazyKns/Vane) (yes, it got renamed from Perplexica to Vane, don't ask)
- **Privacy-first**: Uses SearXNG to avoid tracking
- **Multiple search modes**: Web, academic papers, images, videos, even YouTube transcripts

## What does this MCP server do?

It wraps Perplexica's API and exposes it as an MCP tool. That means your AI assistant can actually search the web on your behalf, cite sources properly, and hand you real information instead of hallucinated facts.

### Search Modes

| Mode | When to use |
|------|-------------|
| `speed` | Quick fact checks, definitions |
| `balanced` | Everyday research, general questions |
| `quality` | Deep dives, important decisions |

## Setup

### 1. Get Perplexica running

Follow the [official installation guide](https://github.com/ItzCrazyKns/Vane?tab=readme-ov-file#-installation).

### 2. Clone this repo

```bash
git clone https://github.com/ItzCrazyKns/mcp-perplexica.git
cd mcp-perplexica
```

### 3. Create your environment

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure

```bash
cp .env.example .env
```

Edit `.env` with your Perplexica URL:

```env
PERPLEXICA_BASE_URL=http://localhost:3000
LOG_LEVEL=INFO
```

The default port is 3000, but update `PERPLEXICA_BASE_URL` if your instance runs elsewhere.

## 🔧 Configuration for AI Assistants

This section shows how to configure various AI code assistants to use the Perplexica MCP server.

### Claude Code (Anthropic)

Claude Code is Anthropic's official CLI tool for interacting with Claude models locally.

**Configuration file:** `~/.claude.json`

```json
{
  "mcpServers": {
    "perplexica": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp-perplexica/server.py"],
      "env": {
        "PERPLEXICA_BASE_URL": "http://localhost:3000"
      }
    }
  }
}
```

**Note:** Ensure the path to `server.py` is absolute, not relative.

---

### OpenCode (OpenCode CLI)

OpenCode is a modern AI code assistant CLI with MCP support.

**Configuration file:** `~/.config/opencode/config.json` (or set `OPENCODE_CONFIG_PATH`)

```json
{
  "mcp": {
    "servers": {
      "perplexica": {
        "command": "python",
        "args": ["/ABSOLUTE/PATH/TO/mcp-perplexica/server.py"],
        "env": {
          "PERPLEXICA_BASE_URL": "http://localhost:3000"
        }
      }
    }
  }
}
```

---

### Qwen Code (Alibaba/Qwen)

Qwen Code is Alibaba's AI coding assistant based on the Qwen model series.

**Configuration file:** `~/.config/qwen-code/mcp.json`

```json
{
  "mcpServers": {
    "perplexica": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp-perplexica/server.py"],
      "env": {
        "PERPLEXICA_BASE_URL": "http://localhost:3000"
      }
    }
  }
}
```

---

### Cursor (cursor.com)

Cursor is an AI-first code editor built on VS Code with deep MCP integration.

**Configuration file:** `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "perplexica": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp-perplexica/server.py"],
      "env": {
        "PERPLEXICA_BASE_URL": "http://localhost:3000"
      }
    }
  }
}
```

**Alternative:** Open Cursor → Settings → MCP → Add new server

---

### Windsurf (Codeium)

Windsurf is Codeium's AI code assistant with agentic capabilities.

**Configuration file:** `~/.codeium/windsurf/mcp_config.json`

```json
{
  "mcpServers": {
    "perplexica": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp-perplexica/server.py"],
      "env": {
        "PERPLEXICA_BASE_URL": "http://localhost:3000"
      }
    }
  }
}
```

**Note:** Some Windsurf versions also support MCP servers via the settings UI.

---

### GitHub Copilot (VS Code Extension)

GitHub Copilot can use MCP servers through VS Code's MCP extension support.

**Configuration:** Install the "MCP" extension for VS Code, then add to `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "perplexica": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp-perplexica/server.py"],
      "env": {
        "PERPLEXICA_BASE_URL": "http://localhost:3000"
      }
    }
  }
}
```

---

## Quick Reference

| Assistant | Config Location | Config Format |
|-----------|-----------------|---------------|
| Claude Code | `~/.claude.json` | JSON with `mcpServers` |
| OpenCode | `~/.config/opencode/config.json` | JSON with `mcp.servers` |
| Qwen Code | `~/.config/qwen-code/mcp.json` | JSON with `mcpServers` |
| Cursor | `~/.cursor/mcp.json` | JSON with `mcpServers` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | JSON with `mcpServers` |
| Copilot (VS Code) | `.vscode/mcp.json` | JSON with `servers` |

## Usage examples

Once connected, you can ask your AI assistant things like:

```
Search for the latest developments in quantum computing
Find academic papers about transformer architectures from 2024
Get a YouTube transcript for the lecture on neural networks
```

And it'll actually go find the information, cite sources, and come back with real results.

## Troubleshooting

**"Connection refused"**
- Is Perplexica running? Make sure `PERPLEXICA_BASE_URL` in `.env` points to your instance
- Check the port matches your Perplexica setup

**"Timeout"**
- The web is slow. Try `speed` mode for quick queries.
- Perplexica might be overloaded. Give it a moment.

**Import errors**
- Make sure you're in a virtual environment
- Python 3.11+ recommended, 3.9 should work

## Contributing

Found a bug? Want a new feature? Open an issue or PR.

## License

MIT. Go wild.
