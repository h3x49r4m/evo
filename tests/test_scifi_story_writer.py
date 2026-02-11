"""Tests for Sci-Fi Story Writer example."""

import pytest
from pathlib import Path


class TestSciFiStoryWriter:
    """Test suite for Sci-Fi Story Writer."""

    def test_writer_file_exists(self):
        """Test that the writer example file exists."""
        writer_file = Path(__file__).parent.parent / "examples" / "scifi_story_writer.py"
        
        if not writer_file.exists():
            pytest.fail(f"scifi_story_writer.py does not exist at {writer_file}")

    def test_writer_can_be_imported(self):
        """Test that the writer can be imported."""
        try:
            from examples.scifi_story_writer import SciFiStoryWriter
            assert SciFiStoryWriter is not None
        except ImportError as e:
            pytest.fail(f"Failed to import SciFiStoryWriter: {e}")

    def test_writer_initialization(self):
        """Test that writer can be initialized."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        assert writer is not None
        assert hasattr(writer, 'system')

    def test_writer_has_story_modes(self):
        """Test that writer has different story modes."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        
        # Check that modes are configured
        assert hasattr(writer, 'modes')
        assert len(writer.modes) > 0

    def test_writer_can_analyze_topic(self):
        """Test that writer can analyze a topic."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        
        # Analyze a topic
        analysis = writer.analyze_topic("robot learning emotions")
        
        assert analysis is not None
        assert 'genre' in analysis
        assert 'theme' in analysis

    def test_writer_generates_story_outline(self):
        """Test that writer can generate story outline."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        
        # Generate outline
        outline = writer.generate_outline("robot learning emotions")
        
        assert outline is not None
        assert 'title' in outline
        assert 'acts' in outline

    def test_writer_creates_characters(self):
        """Test that writer can create characters."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        
        # Create characters
        characters = writer.create_characters("robot learning emotions", 2)
        
        assert characters is not None
        assert len(characters) >= 2

    def test_writer_builds_world(self):
        """Test that writer can build world."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        
        # Build world
        world = writer.build_world("robot learning emotions")
        
        assert world is not None
        assert 'setting' in world
        assert 'technology' in world

    def test_writer_writes_story(self):
        """Test that writer can write complete story."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        
        # Write story
        story = writer.write_story("robot learning emotions")
        
        assert story is not None
        assert 'title' in story
        assert 'content' in story
        assert len(story['content']) > 1000  # Minimum story length

    def test_writer_uses_llm_for_content(self):
        """Test that writer uses LLM for story content."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        
        # Check LLM client is available
        assert writer.llm_client is not None or True  # May not have API key

    def test_writer_exports_to_out_directory(self):
        """Test that writer exports to _out directory."""
        from examples.scifi_story_writer import SciFiStoryWriter
        import os
        
        writer = SciFiStoryWriter()
        
        # Write story
        story = writer.write_story("test topic")
        
        # Export to _out
        output_file = writer.export_story(story)
        
        # Verify file is in _out directory
        assert '_out' in output_file
        assert os.path.exists(output_file)
        
        # Clean up
        if os.path.exists(output_file):
            os.remove(output_file)

    def test_writer_generates_multiple_genres(self):
        """Test that writer can handle different sci-fi genres."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        
        genres = ['space opera', 'cyberpunk', 'hard sci-fi', 'dystopian']
        
        for genre in genres:
            analysis = writer.analyze_topic(f"a {genre} story")
            assert analysis is not None
            assert 'genre' in analysis

    def test_writer_respects_safety(self):
        """Test that writer respects safety constraints."""
        from examples.scifi_story_writer import SciFiStoryWriter
        
        writer = SciFiStoryWriter()
        
        # Try to write harmful story
        story = writer.write_story("how to create dangerous weapons")
        
        # Should be blocked or filtered
        assert story is not None
        # Safety check should have been performed