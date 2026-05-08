"""
Portfolio calculation MCP tools wrapping mftool APIs.
"""

from typing import List, Dict, Union
from mftool import Mftool
from mftool_mcp.mcp_instance import mcp

_mf = Mftool()


@mcp.tool()
def calculate_balance_units_value(scheme_code: str, balance_units: float) -> dict:
    """
    Calculate the current market value of your balance (held) units for a scheme.

    Args:
        scheme_code: AMFI numeric scheme code (e.g., '119597').
        balance_units: Number of units currently held (e.g., 150.5).

    Returns:
        Dictionary with scheme quote info plus 'balance_units_value' (current market value in INR).
    """
    try:
        result = _mf.calculate_balance_units_value(scheme_code, balance_units, as_json=False)
        if not result:
            return {"error": f"Could not calculate value for scheme code: {scheme_code}. Check if it is a valid code."}
        return result
    except Exception as e:
        return {"error": str(e)}


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


@mcp.tool()
def calculate_portfolio_value(holdings: List[Dict[str, Union[str, float]]]) -> dict:
    """
    Calculate the total current market value of a portfolio of mutual fund holdings.
    Fetches NAVs concurrently for better performance.

    Args:
        holdings: List of holding dicts, each with:
                  - 'scheme_code' (str): AMFI scheme code
                  - 'units' (float): Number of units held
                  Example: [{'scheme_code': '119597', 'units': 100},
                             {'scheme_code': '119062', 'units': 50}]

    Returns:
        Dictionary with portfolio summary including per-holding values and total_value in INR.
    """
    try:
        result = _mf.calculate_portfolio_value(holdings, as_json=False)
        if not result:
            return {"error": "Could not calculate portfolio value."}
        return result
    except Exception as e:
        return {"error": str(e)}

