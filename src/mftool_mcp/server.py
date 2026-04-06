"""
mftool-mcp: MCP Server for Indian Mutual Funds data via mftool
Exposes AMFI mutual fund data to any MCP-compatible LLM client.
"""

from mcp.server.fastmcp import FastMCP
from mftool_mcp.tools.nav import (
    get_scheme_quote,
    get_scheme_details,
    get_scheme_historical_nav,
    get_scheme_historical_nav_for_dates,
)
from mftool_mcp.tools.schemes import (
    get_scheme_codes,
    get_available_schemes,
    is_valid_scheme_code,
    search_scheme_by_name,
)
from mftool_mcp.tools.performance import (
    get_equity_scheme_performance,
    get_debt_scheme_performance,
    get_hybrid_scheme_performance,
    get_elss_scheme_performance,
)

mcp = FastMCP(
    name="mftool-mcp",
    instructions=(
        "You have access to real-time Indian Mutual Fund data via AMFI (Association of Mutual Funds in India). "
        "Use these tools to answer questions about NAV, scheme details, historical data, and performance. "
        "Always use scheme codes (numeric IDs) when fetching NAV or details. "
        "Use search_scheme_by_name to find scheme codes from fund names."
    ),
)

# --- NAV Tools ---
mcp.tool()(get_scheme_quote)
mcp.tool()(get_scheme_details)
mcp.tool()(get_scheme_historical_nav)
mcp.tool()(get_scheme_historical_nav_for_dates)

# --- Scheme Discovery Tools ---
mcp.tool()(get_scheme_codes)
mcp.tool()(get_available_schemes)
mcp.tool()(is_valid_scheme_code)
mcp.tool()(search_scheme_by_name)

# --- Performance Tools ---
mcp.tool()(get_equity_scheme_performance)
mcp.tool()(get_debt_scheme_performance)
mcp.tool()(get_hybrid_scheme_performance)
mcp.tool()(get_elss_scheme_performance)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
