"""
mftool-mcp: MCP Server for Indian Mutual Funds data via mftool
Exposes AMFI mutual fund data to any MCP-compatible LLM client.
"""

from mftool_mcp.mcp_instance import mcp

# Importing these modules registers all @mcp.tool() decorated functions
import mftool_mcp.tools.nav  # noqa: F401
import mftool_mcp.tools.schemes  # noqa: F401
import mftool_mcp.tools.performance  # noqa: F401


def main():
    mcp.run()


if __name__ == "__main__":
    main()
