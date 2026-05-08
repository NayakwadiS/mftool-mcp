"""
NAV-related MCP tools wrapping mftool APIs.
Covers quote fetching, bulk quotes, and historical NAV data (AMFI and YFinance/BSE).
"""

from mftool import Mftool
from mftool_mcp.mcp_instance import mcp

_mf = Mftool()


@mcp.tool()
def get_scheme_quote(scheme_code: str) -> dict:
    """
    Get the latest NAV (Net Asset Value) quote for a mutual fund scheme.

    Args:
        scheme_code: AMFI numeric scheme code (e.g., '119597').
                     Use get_scheme_codes or search_schemes to find codes.

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
def get_bulk_quotes(scheme_codes: list) -> dict:
    """
    Fetch the latest NAV quotes for multiple mutual fund schemes concurrently.
    Much faster than calling get_scheme_quote one-by-one for portfolios.

    Args:
        scheme_codes: List of AMFI numeric scheme codes (e.g., ['119597', '119062']).

    Returns:
        Dictionary with scheme codes as keys and quote data dicts as values.
        Invalid or unavailable codes will have null values.
    """
    try:
        result = _mf.get_bulk_quotes(scheme_codes, as_json=False)
        if not result:
            return {"error": "Could not fetch bulk quotes."}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_scheme_historical_nav(scheme_code: str) -> dict:
    """
    Get the full historical NAV data for a mutual fund scheme (all available dates).
    Uses AMFI scheme codes.

    Args:
        scheme_code: AMFI numeric scheme code (e.g., '119597').

    Returns:
        Dictionary with fund metadata, 52-week high/low, and a 'data' list of
        {date, nav} entries sorted latest first.
    """
    try:
        result = _mf.get_scheme_historical_nav(scheme_code, as_json=False)
        if not result:
            return {"error": f"No historical data found for scheme code: {scheme_code}"}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_scheme_history(
    scheme_code: str,
    start_date: str = "",
    end_date: str = "",
    period: str = "5d",
) -> dict:
    """
    Get historical NAV data for a mutual fund using its BSE/YFinance code.
    Use either period OR start_date + end_date. Validate codes with is_valid_new_scheme_code.

    Args:
        scheme_code: BSE scheme code (new format, e.g., '0P0000XVB1').
        start_date: Start date in 'YYYY-MM-DD' format (optional).
        end_date: End date in 'YYYY-MM-DD' format (optional).
        period: Period when not using date range.
                Valid values: '1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','max'.
                Default: '5d'.

    Returns:
        JSON string of historical NAV data with date, nav, and dayChange columns.
    """
    try:
        if start_date and end_date:
            result = _mf.history(scheme_code, start=start_date, end=end_date, as_dataframe=False)
        else:
            result = _mf.history(scheme_code, period=period, as_dataframe=False)
        if result is None:
            return {"error": f"No history found for scheme code: {scheme_code}. Make sure it's a valid BSE/new scheme code."}
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_scheme_historical_nav_for_dates(
    scheme_code: str,
    start_date: str,
    end_date: str,
) -> dict:
    """
    Get historical NAV data for a mutual fund scheme within a specific date range.
    Uses AMFI scheme codes. Dates must be in DD-MM-YYYY format.

    Args:
        scheme_code: AMFI numeric scheme code (e.g., '119597').
        start_date: Start date in 'DD-MM-YYYY' format (e.g., '01-01-2023').
        end_date: End date in 'DD-MM-YYYY' format (e.g., '31-12-2023').

    Returns:
        Dictionary with fund metadata and a 'data' list of {date, nav} entries
        filtered to the requested date range.
    """
    try:
        result = _mf.get_scheme_historical_nav_for_dates(
            scheme_code, start_date, end_date, as_json=False
        )
        if not result:
            return {
                "error": (
                    f"No data found for scheme code: {scheme_code} "
                    f"between {start_date} and {end_date}. "
                    "Ensure dates are in DD-MM-YYYY format and the scheme code is valid."
                )
            }
        return result
    except Exception as e:
        return {"error": str(e)}
