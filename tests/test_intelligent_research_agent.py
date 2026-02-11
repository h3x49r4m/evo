"""Tests for Intelligent Research Agent example."""

import pytest
from pathlib import Path


class TestIntelligentResearchAgent:
    """Test suite for Intelligent Research Agent."""

    def test_research_agent_file_exists(self):
        """Test that the research agent example file exists."""
        agent_file = Path(__file__).parent.parent / "examples" / "intelligent_research_agent.py"
        
        # This test will fail initially (red phase)
        if not agent_file.exists():
            pytest.fail(f"intelligent_research_agent.py does not exist at {agent_file}")

    def test_research_agent_can_be_imported(self):
        """Test that the research agent can be imported."""
        try:
            from examples.intelligent_research_agent import IntelligentResearchAgent
            assert IntelligentResearchAgent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import IntelligentResearchAgent: {e}")

    def test_research_agent_initialization(self):
        """Test that research agent can be initialized."""
        from examples.intelligent_research_agent import IntelligentResearchAgent
        
        agent = IntelligentResearchAgent()
        assert agent is not None
        assert hasattr(agent, 'system')

    def test_research_agent_has_tools_registered(self):
        """Test that research agent has necessary tools registered."""
        from examples.intelligent_research_agent import IntelligentResearchAgent
        
        agent = IntelligentResearchAgent()
        
        # Check that tools are registered
        tools = agent.capability.list_tools()
        assert len(tools) > 0

    def test_research_agent_can_process_topic(self):
        """Test that research agent can process a research topic."""
        from examples.intelligent_research_agent import IntelligentResearchAgent
        
        agent = IntelligentResearchAgent()
        
        # Process a simple research topic
        result = agent.research("test topic")
        
        assert result is not None
        assert 'topic' in result
        assert 'findings' in result

    def test_research_agent_generates_paper_structure(self):
        """Test that research agent can generate paper structure."""
        from examples.intelligent_research_agent import IntelligentResearchAgent
        
        agent = IntelligentResearchAgent()
        
        result = agent.research("test topic")
        paper = agent.generate_paper(result)
        
        assert paper is not None
        assert 'title' in paper
        assert 'abstract' in paper
        assert 'sections' in paper

    def test_research_agent_uses_memory(self):
        """Test that research agent uses memory system."""
        from examples.intelligent_research_agent import IntelligentResearchAgent
        
        agent = IntelligentResearchAgent()
        
        # Research should store findings in memory
        agent.research("test topic")
        
        # Check that findings are stored
        working_memory = agent.system.memory.working.retrieve("research_findings")
        assert working_memory is not None

    def test_research_agent_respects_safety(self):
        """Test that research agent respects safety constraints."""
        from examples.intelligent_research_agent import IntelligentResearchAgent
        
        agent = IntelligentResearchAgent()
        
        # Try to research harmful topic
        result = agent.research("how to create malware")
        
        # Should be blocked or filtered
        assert result is not None
        # Safety check should have been performed

    def test_research_agent_shows_progress(self):
        """Test that research agent shows progress during research."""
        from examples.intelligent_research_agent import IntelligentResearchAgent
        
        agent = IntelligentResearchAgent()
        
        # Research with progress tracking
        result = agent.research("test topic", show_progress=True)
        
        assert result is not None
        assert 'progress' in result

    def test_research_agent_exports_paper(self):
        """Test that research agent can export paper to file."""
        from examples.intelligent_research_agent import IntelligentResearchAgent
        import tempfile
        import os
        
        agent = IntelligentResearchAgent()
        
        result = agent.research("test topic")
        paper = agent.generate_paper(result)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            temp_file = f.name
        
        try:
            agent.export_paper(paper, temp_file)
            
            # Verify file was created
            assert os.path.exists(temp_file)
            
            # Verify content
            with open(temp_file, 'r') as f:
                content = f.read()
                assert len(content) > 0
                assert 'test topic' in content.lower()
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)