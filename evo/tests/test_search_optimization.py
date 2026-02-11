"""Tests for optimized search functionality."""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from evo.capability import CapabilityRegistry


def test_search_tools_uses_index():
    """Test that search_tools uses the index for fast lookups."""
    registry = CapabilityRegistry()
    
    # Register tools
    registry.register_tool("search_web", "Search the web for information", lambda: None)
    registry.register_tool("search_images", "Search for images", lambda: None)
    registry.register_tool("send_email", "Send an email", lambda: None)
    registry.register_tool("web_scrape", "Scrape web pages", lambda: None)
    
    # Search for "search"
    results = registry.search_tools("search")
    assert "search_web" in results
    assert "search_images" in results
    assert len(results) >= 2


def test_search_tools_case_insensitive():
    """Test that search is case-insensitive."""
    registry = CapabilityRegistry()
    
    registry.register_tool("SearchWeb", "Web search", lambda: None)
    registry.register_tool("ImageSearch", "Image search", lambda: None)
    
    results_lower = registry.search_tools("search")
    results_upper = registry.search_tools("SEARCH")
    results_mixed = registry.search_tools("SeArCh")
    
    assert results_lower == results_upper == results_mixed


def test_search_tools_description_matching():
    """Test that search matches in tool descriptions."""
    registry = CapabilityRegistry()
    
    registry.register_tool("fetch_data", "Retrieve data from API", lambda: None)
    registry.register_tool("process_data", "Process the retrieved data", lambda: None)
    
    results = registry.search_tools("api")
    assert "fetch_data" in results


def test_search_tools_empty_query():
    """Test that empty query returns empty list."""
    registry = CapabilityRegistry()
    
    registry.register_tool("test_tool", "Test description", lambda: None)
    
    results = registry.search_tools("")
    assert results == []


def test_search_tools_no_matches():
    """Test that search returns empty list when no matches."""
    registry = CapabilityRegistry()
    
    registry.register_tool("test_tool", "Test description", lambda: None)
    
    results = registry.search_tools("nonexistent")
    assert results == []


def test_search_tools_unregister_removes_from_index():
    """Test that unregistering a tool removes it from search index."""
    registry = CapabilityRegistry()
    
    registry.register_tool("test_tool", "Test description", lambda: None)
    
    # Should find the tool
    results_before = registry.search_tools("test")
    assert "test_tool" in results_before
    
    # Unregister the tool
    registry.unregister_tool("test_tool")
    
    # Should not find the tool anymore
    results_after = registry.search_tools("test")
    assert "test_tool" not in results_after


def test_search_tools_sorted_results():
    """Test that search results are sorted alphabetically."""
    registry = CapabilityRegistry()
    
    registry.register_tool("zebra_tool", "Tool z", lambda: None)
    registry.register_tool("alpha_tool", "Tool a", lambda: None)
    registry.register_tool("beta_tool", "Tool b", lambda: None)
    
    results = registry.search_tools("tool")
    assert results == ["alpha_tool", "beta_tool", "zebra_tool"]


def test_search_tools_duplicate_prevention():
    """Test that the same tool isn't returned multiple times."""
    registry = CapabilityRegistry()
    
    # Register a tool with name and description that both match
    registry.register_tool("search_search", "Search for search results", lambda: None)
    
    results = registry.search_tools("search")
    # Should only appear once in results
    assert results.count("search_search") == 1


def test_search_tools_partial_word_match():
    """Test that search finds tools matching partial words."""
    registry = CapabilityRegistry()
    
    registry.register_tool("web_browser", "Browse the web", lambda: None)
    registry.register_tool("web_server", "Run a web server", lambda: None)
    
    results = registry.search_tools("web")
    assert "web_browser" in results
    assert "web_server" in results


def test_search_tools_with_many_tools_performance():
    """Test search performance with many tools."""
    import time
    
    registry = CapabilityRegistry()
    
    # Register 100 tools
    for i in range(100):
        registry.register_tool(f"tool_{i}", f"Tool number {i}", lambda x=i: x)
    
    # Time the search
    start = time.time()
    results = registry.search_tools("tool_")
    end = time.time()
    
    # Should be fast (< 1ms) and find all tools
    assert len(results) == 100
    assert (end - start) < 0.01


def test_search_index_building_on_register():
    """Test that search index is properly built on tool registration."""
    registry = CapabilityRegistry()
    
    # Check index is empty initially
    assert len(registry._tool_search_index) == 0
    
    # Register a tool
    registry.register_tool("test_tool", "test description", lambda: None)
    
    # Check index has been built
    assert len(registry._tool_search_index) > 0
    # Should have entries for "test_tool", "test", "description"
    assert "test_tool" in registry._tool_search_index or "test" in registry._tool_search_index