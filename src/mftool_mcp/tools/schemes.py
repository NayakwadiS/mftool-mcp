"""
Scheme discovery, metadata, validation and search MCP tools wrapping mftool APIs.
"""

from mftool import Mftool
from mftool_mcp.mcp_instance import mcp

_mf = Mftool()


@mcp.tool()
def get_scheme_codes() -> dict:
    """
    Get a dictionary of ALL mutual fund scheme codes and names available on AMFI.
    Returns a large dataset with scheme_code -> scheme_name mappings.
    Use this to discover scheme codes for funds you want to query.

    Returns:
        Dictionary mapping scheme codes (str) to scheme names (str).
    """
    try:
        result = _mf.get_scheme_codes(as_json=False)
        if not result:
            return {"error": "Could not fetch scheme codes."}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_available_schemes(amc_name: str) -> dict:
    """
    Get all mutual fund schemes available under a specific AMC (Asset Management Company).

    Args:
        amc_name: Partial or full name of the AMC (case-insensitive).
                  Examples: 'hdfc', 'sbi', 'axis', 'icici', 'mirae', 'parag', 'dsp'.

    Returns:
        Dictionary mapping scheme codes (str) to scheme names (str) for the given AMC.
    """
    try:
        result = _mf.get_available_schemes(amc_name)
        if not result:
            return {"error": f"No schemes found for AMC: '{amc_name}'. Try a shorter keyword."}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_scheme_details(scheme_code: str) -> dict:
    """
    Get detailed metadata for a mutual fund scheme including fund house,
    type, category, and scheme start date. Uses AMFI scheme codes.

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
def get_scheme_info(scheme_code: str) -> dict:
    """
    Get complete information for a mutual fund scheme using its BSE/YFinance code.
    Returns richer data than get_scheme_details (includes AUM, returns, ratings, etc.).
    Validate the code first with is_valid_new_scheme_code.

    Args:
        scheme_code: BSE scheme code (new format, e.g., '0P0000XVB1').

    Returns:
        Dictionary with complete scheme information from Yahoo Finance.
    """
    try:
        result = _mf.get_scheme_info(scheme_code, as_json=False)
        if not result:
            return {"error": f"No info found for scheme code: {scheme_code}. Make sure it's a valid BSE/new scheme code."}
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def is_valid_scheme_code(scheme_code: str) -> dict:
    """
    Check whether a given scheme code is a valid AMFI scheme code.

    Args:
        scheme_code: Numeric AMFI scheme code to validate (e.g., '119597').

    Returns:
        Dictionary with 'scheme_code' and 'valid' (bool).
    """
    try:
        result = _mf.is_valid_code(scheme_code)
        return {"scheme_code": scheme_code, "valid": bool(result)}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def is_valid_new_scheme_code(scheme_code: str) -> dict:
    """
    Check whether a given code is a valid NEW BSE scheme code (used with
    get_scheme_history and get_scheme_info). Different from AMFI codes.

    Args:
        scheme_code: BSE scheme code to validate (e.g., '0P0000XVB1').

    Returns:
        Dictionary with 'scheme_code' and 'valid' (bool).
    """
    try:
        result = _mf.is_code(scheme_code)
        return {"scheme_code": scheme_code, "valid": bool(result)}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_schemes(query: str, limit: int = 10) -> dict:
    """
    Search for mutual fund schemes by name using built-in relevance matching.
    Results ranked: exact > prefix > whole-word > partial match.

    Args:
        query: Name or partial name to search for (case-insensitive).
               Examples: 'HDFC midcap', 'Axis bluechip', 'flexi cap'.
        limit: Maximum number of results to return (default: 10, use 0 for all).

    Returns:
        List of matching schemes with 'code' and 'name' keys, sorted by relevance.
    """
    try:
        result = _mf.search_schemes(query, limit=limit, as_json=False)
        if not result:
            return {"error": f"No schemes found matching '{query}'."}
        return {"query": query, "results": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_schemes_by_amc(amc_name: str, query: str = "", limit: int = 10) -> dict:
    """
    Search for mutual fund schemes within a specific AMC (fund house).
    Optionally filter further by a name keyword.

    Args:
        amc_name: AMC/fund house name (e.g., 'HDFC', 'ICICI', 'Axis', 'SBI', 'Mirae').
        query: Optional keyword to filter schemes within the AMC (e.g., 'midcap', 'index').
        limit: Maximum number of results (default: 10, use 0 for all).

    Returns:
        List of matching schemes with 'code' and 'name' keys.
    """
    try:
        result = _mf.search_schemes_by_amc(amc_name, search_term=query, limit=limit, as_json=False)
        if not result:
            return {"error": f"No schemes found for AMC '{amc_name}'" + (f" matching '{query}'" if query else "") + "."}
        return {"amc": amc_name, "query": query or "all", "results": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_schemes_by_type(scheme_type: str, query: str = "", limit: int = 10) -> dict:
    """
    Search for mutual fund schemes by type/category keyword.

    Args:
        scheme_type: Type keyword to search in scheme names.
                     Examples: 'equity', 'debt', 'hybrid', 'elss', 'index', 'liquid',
                               'overnight', 'gilt', 'arbitrage', 'balanced'.
        query: Optional additional keyword to narrow results (e.g., AMC name or sub-type).
        limit: Maximum number of results (default: 10, use 0 for all).

    Returns:
        List of matching schemes with 'code' and 'name' keys.
    """
    try:
        result = _mf.search_schemes_by_type(scheme_type, search_term=query, limit=limit, as_json=False)
        if not result:
            return {"error": f"No '{scheme_type}' schemes found" + (f" matching '{query}'" if query else "") + "."}
        return {"type": scheme_type, "query": query or "all", "results": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_average_aum(year_quarter: str) -> dict:
    """
    Get the Average Assets Under Management (AAUM) for all AMCs for a given quarter.
    Returns both domestic and overseas AAUM for each fund house.

    Args:
        year_quarter: Quarter string in the format 'Month - Month YYYY'.
                      Examples: 'April - June 2023', 'July - September 2023',
                                'October - December 2023', 'January - March 2024'.

    Returns:
        List of dicts with 'Fund Name', 'AAUM Domestic', and 'AAUM Overseas' for each AMC.
    """
    try:
        result = _mf.get_average_aum(year_quarter, as_json=False)
        if not result:
            return {"error": f"No AUM data found for quarter: '{year_quarter}'. Use format like 'April - June 2023'."}
        return {"quarter": year_quarter, "data": result}
    except Exception as e:
        return {"error": str(e)}
