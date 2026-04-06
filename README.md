# 🇮🇳 mftool-mcp

> **MCP Server for real-time Indian Mutual Funds data**  
> Powered by [mftool](https://github.com/NayakwadiS/mftool) · AMFI data · Works with Claude, Cursor, and any MCP-compatible LLM client

[![PyPI version](https://img.shields.io/pypi/v/mftool-mcp.svg)](https://pypi.org/project/mftool-mcp/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://modelcontextprotocol.io)

---

## What is this?

`mftool-mcp` is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that gives any LLM client access to **live Indian Mutual Fund data** from AMFI (Association of Mutual Funds in India).

Ask your AI assistant questions like:
- *"What is the current NAV of SBI Bluechip Direct Growth?"*
- *"Show me 3-year returns for HDFC Midcap Opportunities Fund"*
- *"List all schemes under Mirae Asset AMC"*
- *"Find all flexi cap funds and compare their 5-year returns"*

---

## Tools Available

| Tool | Description |
|---|---|
| `get_scheme_quote` | Live NAV for any scheme by code |
| `get_scheme_details` | Fund house, type, category, start date |
| `get_scheme_historical_nav` | Full NAV history (all dates) |
| `get_scheme_historical_nav_for_dates` | NAV history within a date range |
| `get_scheme_codes` | All AMFI scheme codes and names |
| `get_available_schemes` | All schemes under a specific AMC |
| `is_valid_scheme_code` | Validate a scheme code |
| `search_scheme_by_name` | Find scheme codes by keyword |
| `get_equity_scheme_performance` | Daily equity fund performance (1Y/3Y/5Y) |
| `get_debt_scheme_performance` | Daily debt fund performance |
| `get_hybrid_scheme_performance` | Daily hybrid fund performance |
| `get_elss_scheme_performance` | ELSS / tax-saving fund performance |

---

## Quick Start

### Using `uvx` (Recommended — no install needed)

```bash
uvx mftool-mcp
```

### Using `pip`

```bash
pip install mftool-mcp
mftool-mcp
```

---

## Claude Desktop Setup

Add this to your `claude_desktop_config.json`:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mftool-mcp": {
      "command": "uvx",
      "args": ["mftool-mcp"]
    }
  }
}
```

Restart Claude Desktop. You'll see **mftool-mcp** listed under connected tools.

---

## Cursor / Other MCP Clients

In your MCP client settings, add:

```json
{
  "mftool-mcp": {
    "command": "uvx",
    "args": ["mftool-mcp"]
  }
}
```

---

## Example Conversations

**Finding a fund:**
> You: "Find all SBI midcap mutual fund scheme codes"  
> Claude: *calls `search_scheme_by_name(query='midcap', amc_name='sbi')`*  
> Claude: "Here are the SBI midcap schemes: SBI Magnum Midcap Fund - Direct Growth (code: 125497)..."

**Live NAV:**
> You: "What's the current NAV of scheme 125497?"  
> Claude: *calls `get_scheme_quote(scheme_code='125497')`*  
> Claude: "SBI Magnum Midcap Fund - Direct Growth: NAV ₹234.56 (as of 05-Apr-2025)"

**Performance comparison:**
> You: "Compare 5-year returns for large cap equity funds"  
> Claude: *calls `get_equity_scheme_performance()`*  
> Claude: "Here's the 5-year return comparison for Large Cap funds: ..."

---

## Data Source

All data is sourced from **AMFI India** (amfiindia.com) via the `mftool` library. Data accuracy depends on AMFI's published figures. This tool is for **informational purposes only** and does not constitute financial advice.

---

## Development

```bash
git clone https://github.com/yourusername/mftool-mcp
cd mftool-mcp
pip install -e ".[dev]"

# Run the server locally
python -m mftool_mcp.server
```

<!-- ### Project Structure

```
mftool-mcp/
├── src/
│   └── mftool_mcp/
│       ├── __init__.py
│       ├── server.py          # MCP server entry point
│       └── tools/
│           ├── __init__.py
│           ├── nav.py         # NAV & historical data tools
│           ├── schemes.py     # Scheme discovery & search tools
│           └── performance.py # Daily performance tools
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## Publishing to PyPI

```bash
pip install build twine
python -m build
twine upload dist/*
```

---

## Submitting to Official MCP Registry

To list this on [modelcontextprotocol.io](https://modelcontextprotocol.io):

1. Fork `github.com/modelcontextprotocol/servers`
2. Add entry under `README.md` → Community Servers section
3. Open a PR with your server details -->

---

## License

MIT © 2025 Your Name

---

## Acknowledgements

- [mftool](https://github.com/NayakwadiS/mftool) by NayakwadiS — the underlying data library
- [AMFI India](https://www.amfiindia.com/) — the data source
- [Anthropic MCP](https://modelcontextprotocol.io) — the protocol
