"""
Daily scheme performance MCP tools wrapping mftool APIs.
Returns 1Y/3Y/5Y returns for open-ended schemes.
"""

from mftool import Mftool
from mftool_mcp.mcp_instance import mcp

_mf = Mftool()


@mcp.tool()
def get_equity_scheme_performance() -> dict:
    """
    Get daily performance data for all open-ended EQUITY mutual fund schemes.
    Includes Large Cap, Mid Cap, Small Cap, Flexi Cap, ELSS, Sectoral, etc.
    Shows latest NAV (Regular & Direct plans) and 1Y/3Y/5Y returns.

    Returns:
        Dictionary categorized by equity fund type with performance metrics.
    """
    try:
        result = _mf.get_open_ended_equity_scheme_performance(as_json=False)
        if not result:
            return {"error": "Could not fetch equity scheme performance data."}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_debt_scheme_performance() -> dict:
    """
    Get daily performance data for all open-ended DEBT mutual fund schemes.
    Includes Liquid, Overnight, Short Duration, Corporate Bond, Gilt funds, etc.
    Shows latest NAV (Regular & Direct plans) and 1Y/3Y/5Y returns.

    Returns:
        Dictionary categorized by debt fund type with performance metrics.
    """
    try:
        result = _mf.get_open_ended_debt_scheme_performance(as_json=False)
        if not result:
            return {"error": "Could not fetch debt scheme performance data."}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_hybrid_scheme_performance() -> dict:
    """
    Get daily performance data for all open-ended HYBRID mutual fund schemes.
    Includes Balanced Advantage, Aggressive Hybrid, Conservative Hybrid, Arbitrage, etc.
    Shows latest NAV (Regular & Direct plans) and 1Y/3Y/5Y returns.

    Returns:
        Dictionary categorized by hybrid fund type with performance metrics.
    """
    try:
        result = _mf.get_open_ended_hybrid_scheme_performance(as_json=False)
        if not result:
            return {"error": "Could not fetch hybrid scheme performance data."}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_solution_scheme_performance() -> dict:
    """
    Get daily performance data for open-ended SOLUTION-ORIENTED mutual fund schemes.
    Includes Retirement Fund and Children's Fund categories.
    Shows latest NAV (Regular & Direct plans) and 1Y/3Y/5Y returns.

    Returns:
        Dictionary categorized by solution-oriented fund type with performance metrics.
    """
    try:
        result = _mf.get_open_ended_solution_scheme_performance(as_json=False)
        if not result:
            return {"error": "Could not fetch solution-oriented scheme performance data."}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_other_scheme_performance() -> dict:
    """
    Get daily performance data for open-ended OTHER mutual fund schemes.
    Includes Index Funds and Fund of Funds (FoF) categories.
    Shows latest NAV (Regular & Direct plans) and 1Y/3Y/5Y returns.

    Returns:
        Dictionary categorized by index/FoF fund type with performance metrics.
    """
    try:
        result = _mf.get_open_ended_other_scheme_performance(as_json=False)
        if not result:
            return {"error": "Could not fetch other (index/FoF) scheme performance data."}
        return result
    except Exception as e:
        return {"error": str(e)}
