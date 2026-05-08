"""
Portfolio calculation MCP tools wrapping mftool APIs.
"""

from mftool import Mftool
from mftool_mcp.mcp_instance import mcp

_mf = Mftool()


@mcp.tool()
def calculate_returns(
    scheme_code: str,
    balance_units: float,
    monthly_sip: float,
    investment_in_months: int,
) -> dict:
    """
    Calculate SIP investment returns for a mutual fund scheme.
    Shows current market value, absolute return, and annualised IRR.

    Args:
        scheme_code: AMFI numeric scheme code (e.g., '119062').
        balance_units: Current total units held (e.g., 1718.925).
        monthly_sip: Monthly SIP investment amount in INR (e.g., 2000).
        investment_in_months: Total number of months invested (e.g., 51).

    Returns:
        Dictionary with scheme info, final_investment_value, absolute_return (%),
        and IRR_annualised_return (%).

    Example:
        calculate_returns('119062', 1718.925, 2000, 51)
    """
    try:
        result = _mf.calculate_returns(
            scheme_code, balance_units, monthly_sip, investment_in_months, as_json=False
        )
        if not result:
            return {"error": f"Could not calculate returns for scheme code: {scheme_code}. Check if it is a valid code."}
        return result
    except Exception as e:
        return {"error": str(e)}
