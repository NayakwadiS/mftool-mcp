"""
Shared FastMCP instance — imported by both server.py and tool modules
so that @mcp.tool() decorators work directly in each tool file.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="mftool-mcp",
    instructions=(
        "You have access to real-time Indian Mutual Fund data via AMFI (Association of Mutual Funds in India). "
        "Use these tools to answer questions about NAV, scheme details, historical data, and performance. "
        "Always use scheme codes (numeric IDs) when fetching NAV or details. "
        "Use search_scheme_by_name to find scheme codes from fund names."
    ),
)

