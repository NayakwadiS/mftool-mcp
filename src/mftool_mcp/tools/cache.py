"""
Cache management MCP tools wrapping mftool APIs.
"""

from mftool import Mftool
from mftool_mcp.mcp_instance import mcp

_mf = Mftool()


@mcp.tool()
def get_cache_stats() -> dict:
    """
    Get cache statistics for the mftool internal cache layers.
    Shows hit/miss counts and entry counts for NAV and scheme codes caches.

    Returns:
        Dictionary with 'nav_cache' and 'scheme_codes_cache' statistics.
    """
    try:
        return _mf.get_cache_stats()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def clear_cache() -> dict:
    """
    Clear all cached mftool data (NAV cache and scheme codes cache).
    Useful when you want to force fresh data to be fetched from AMFI/BSE.

    Returns:
        Confirmation dictionary.
    """
    try:
        _mf.clear_cache()
        return {"status": "success", "message": "All caches cleared successfully."}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def set_cache_enabled(enabled: bool) -> dict:
    """
    Enable or disable mftool's internal caching globally.
    Disabling cache forces fresh API calls every time (slower but always up-to-date).

    Args:
        enabled: True to enable caching, False to disable.

    Returns:
        Confirmation dictionary with new cache status.
    """
    try:
        if enabled:
            _mf.enable_cache()
        else:
            _mf.disable_cache()
        return {"status": "success", "cache_enabled": enabled}
    except Exception as e:
        return {"error": str(e)}

