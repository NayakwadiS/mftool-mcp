"""
NAV-related MCP tools wrapping mftool APIs.
"""

from mftool import Mftool
from mftool_mcp.mcp_instance import mcp

_mf = Mftool()


@mcp.tool()
def get_scheme_quote(scheme_code: str) -> dict:
    """
    Get the latest NAV (Net Asset Value) quote for a mutual fund scheme.

    Args:
        scheme_code: AMFI numeric scheme code (e.g., '119597' for an SBI fund).
                     Use get_scheme_codes or search_scheme_by_name to find codes.

    Returns:
        Dictionary with scheme_code, scheme_name, last_updated, nav.
    """
    try:
        result = _mf.get_scheme_quote(scheme_code, as_json=False)
        if not result:
            return {"error": f"No data found for scheme code: {scheme_code}"}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_scheme_details(scheme_code: str) -> dict:
    """
    Get detailed metadata for a mutual fund scheme including fund house,
    type, category, and scheme start date.

    Args:
        scheme_code: AMFI numeric scheme code (e.g., '119597').

    Returns:
        Dictionary with fund_house, scheme_type, scheme_category,
        scheme_code, scheme_name, scheme_start_date.
    """
    try:
        result = _mf.get_scheme_details(scheme_code, as_json=False)
        if not result:
            return {"error": f"No details found for scheme code: {scheme_code}"}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_scheme_historical_nav(scheme_code: str) -> dict:
    """
    Get the full historical NAV data for a mutual fund scheme (all available dates).

    Args:
        scheme_code: AMFI numeric scheme code (e.g., '119597').

    Returns:
        Dictionary with fund metadata and a 'data' list of {date, nav} entries,
        sorted latest first.
    """
    try:
        result = _mf.get_scheme_historical_nav(scheme_code, as_json=False)
        if not result:
            return {"error": f"No historical data found for scheme code: {scheme_code}"}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_scheme_historical_nav_for_dates(
    scheme_code: str, start_date: str, end_date: str
) -> dict:
    """
    Get historical NAV for a mutual fund scheme within a specific date range.

    Args:
        scheme_code: AMFI numeric scheme code (e.g., '119597').
        start_date: Start date in 'DD-MM-YYYY' format (e.g., '01-01-2023').
        end_date: End date in 'DD-MM-YYYY' format (e.g., '31-12-2023').

    Returns:
        Dictionary with fund metadata and filtered NAV data for the date range.
    """
    try:
        result = _mf.get_scheme_historical_nav_for_dates(
            scheme_code, start_date, end_date, as_json=False
        )
        if not result:
            return {
                "error": (
                    f"No data found for scheme {scheme_code} "
                    f"between {start_date} and {end_date}"
                )
            }
        return result
    except Exception as e:
        return {"error": str(e)}
