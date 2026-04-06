"""
Scheme discovery and search MCP tools wrapping mftool APIs.
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
def is_valid_scheme_code(scheme_code: str) -> dict:
    """
    Check whether a given scheme code is a valid AMFI scheme code.

    Args:
        scheme_code: Numeric scheme code to validate (e.g., '119597').

    Returns:
        Dictionary with 'valid' (bool) and 'scheme_code' fields.
    """
    try:
        result = _mf.is_valid_code(scheme_code)
        return {"scheme_code": scheme_code, "valid": bool(result)}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_scheme_by_name(query: str, amc_name: str = "") -> dict:
    """
    Search for mutual fund schemes by name keyword. Optionally filter by AMC.
    Use this when you know a fund name but not its scheme code.

    Args:
        query: Keyword to search in scheme names (e.g., 'midcap', 'bluechip', 'flexi').
        amc_name: Optional AMC filter (e.g., 'hdfc', 'sbi'). Leave empty to search all.

    Returns:
        Dictionary mapping scheme codes to matching scheme names.
    """
    try:
        if amc_name:
            all_schemes = _mf.get_available_schemes(amc_name)
        else:
            all_schemes = _mf.get_scheme_codes(as_json=False)

        if not all_schemes:
            return {"error": "Could not fetch schemes for search."}

        query_lower = query.lower()
        matches = {
            code: name
            for code, name in all_schemes.items()
            if query_lower in name.lower()
        }

        if not matches:
            return {
                "error": f"No schemes found matching '{query}'"
                + (f" under AMC '{amc_name}'" if amc_name else ""),
                "suggestion": "Try broader keywords like 'midcap', 'large', 'debt', 'liquid'.",
            }

        return {"query": query, "amc_filter": amc_name or "all", "results": matches}
    except Exception as e:
        return {"error": str(e)}
