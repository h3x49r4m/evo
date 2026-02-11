"""Tests for Capability Registry (TDD Red Phase)."""

import pytest
from evo.capability import CapabilityRegistry


class TestToolRegistration:
    """Tests for tool registration and management."""
    
    def test_register_tool_adds_tool_to_registry(self):
        """Given a capability registry, When registering a tool, Then it is retrievable."""
        registry = CapabilityRegistry()
        registry.register_tool("file_read", "Read files from filesystem")
        assert "file_read" in registry.list_tools()
    
    def test_register_tool_with_callable_stores_function(self):
        """Given a capability registry, When registering tool with callable, Then stores the function."""
        registry = CapabilityRegistry()
        def mock_tool():
            pass
        registry.register_tool("mock_tool", "Mock tool", callable_func=mock_tool)
        tool = registry.get_tool("mock_tool")
        assert tool["callable"] is mock_tool
    
    def test_unregister_tool_removes_from_registry(self):
        """Given a registry with tool, When unregistering, Then tool is removed."""
        registry = CapabilityRegistry()
        registry.register_tool("temp_tool", "Temporary tool")
        registry.unregister_tool("temp_tool")
        assert "temp_tool" not in registry.list_tools()
    
    def test_get_nonexistent_tool_returns_none(self):
        """Given a registry, When getting nonexistent tool, Then returns None."""
        registry = CapabilityRegistry()
        assert registry.get_tool("nonexistent") is None


class TestSkillRegistration:
    """Tests for skill registration and management."""
    
    def test_register_skill_adds_skill_to_registry(self):
        """Given a capability registry, When registering a skill, Then it is retrievable."""
        registry = CapabilityRegistry()
        registry.register_skill("python_programming", "Write Python code")
        assert "python_programming" in registry.list_skills()
    
    def test_register_skill_with_level_stores_proficiency(self):
        """Given a capability registry, When registering skill with level, Then stores proficiency."""
        registry = CapabilityRegistry()
        registry.register_skill("rust", "Write Rust code", level=0.7)
        skill = registry.get_skill("rust")
        assert skill["level"] == 0.7
    
    def test_unregister_skill_removes_from_registry(self):
        """Given a registry with skill, When unregistering, Then skill is removed."""
        registry = CapabilityRegistry()
        registry.register_skill("temp_skill", "Temporary skill")
        registry.unregister_skill("temp_skill")
        assert "temp_skill" not in registry.list_skills()
    
    def test_update_skill_level_changes_proficiency(self):
        """Given a registry with skill, When updating level, Then proficiency changes."""
        registry = CapabilityRegistry()
        registry.register_skill("analysis", "Analyze code", level=0.5)
        registry.update_skill_level("analysis", 0.8)
        assert registry.get_skill("analysis")["level"] == 0.8


class TestKnowledgeRegistration:
    """Tests for knowledge registration and management."""
    
    def test_register_knowledge_adds_fact_to_registry(self):
        """Given a capability registry, When registering knowledge, Then it is retrievable."""
        registry = CapabilityRegistry()
        registry.register_knowledge("python_3_12_syntax", "Python 3.12 syntax rules")
        assert "python_3_12_syntax" in registry.list_knowledge()
    
    def test_unregister_knowledge_removes_from_registry(self):
        """Given a registry with knowledge, When unregistering, Then knowledge is removed."""
        registry = CapabilityRegistry()
        registry.register_knowledge("temp_fact", "Temporary fact")
        registry.unregister_knowledge("temp_fact")
        assert "temp_fact" not in registry.list_knowledge()
    
    def test_get_knowledge_retrieves_stored_value(self):
        """Given a registry with knowledge, When getting knowledge, Then returns stored value."""
        registry = CapabilityRegistry()
        registry.register_knowledge("fact_key", "fact_value")
        assert registry.get_knowledge("fact_key") == "fact_value"


class TestCapabilityRegistryQueries:
    """Tests for querying the capability registry."""
    
    def test_list_all_capabilities_returns_all_registered(self):
        """Given a registry with mixed capabilities, When listing all, Then returns all types."""
        registry = CapabilityRegistry()
        registry.register_tool("tool1", "Tool 1")
        registry.register_skill("skill1", "Skill 1")
        registry.register_knowledge("knowledge1", "Knowledge 1")
        all_caps = registry.list_all_capabilities()
        assert len(all_caps["tools"]) == 1
        assert len(all_caps["skills"]) == 1
        assert len(all_caps["knowledge"]) == 1
    
    def test_search_tools_by_name_finds_matching(self):
        """Given a registry with tools, When searching by name, Then returns matches."""
        registry = CapabilityRegistry()
        registry.register_tool("file_read", "Read files")
        registry.register_tool("file_write", "Write files")
        registry.register_tool("web_fetch", "Fetch web content")
        results = registry.search_tools("file")
        assert len(results) == 2
        assert all("file" in tool_name for tool_name in results)
    
    def test_get_capability_count_returns_total_registered(self):
        """Given a registry with capabilities, When getting count, Then returns total."""
        registry = CapabilityRegistry()
        registry.register_tool("tool1", "Tool 1")
        registry.register_skill("skill1", "Skill 1")
        registry.register_knowledge("knowledge1", "Knowledge 1")
        count = registry.get_capability_count()
        assert count == 3


class TestDynamicCapabilityManagement:
    """Tests for dynamic capability addition/removal."""
    
    def test_add_multiple_tools_increases_registry_size(self):
        """Given a registry, When adding multiple tools, Then registry grows."""
        registry = CapabilityRegistry()
        for i in range(5):
            registry.register_tool(f"tool_{i}", f"Tool {i}")
        assert len(registry.list_tools()) == 5
    
    def test_remove_all_tools_clears_tool_registry(self):
        """Given a registry with tools, When removing all, Then tools cleared."""
        registry = CapabilityRegistry()
        registry.register_tool("tool1", "Tool 1")
        registry.register_tool("tool2", "Tool 2")
        for tool in registry.list_tools():
            registry.unregister_tool(tool)
        assert len(registry.list_tools()) == 0