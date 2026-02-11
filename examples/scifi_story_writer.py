"""Sci-Fi Story Writer - AI-powered science fiction story generator.

This example demonstrates how to use the evo autonomous agent system
to generate original science fiction stories from user-provided topics.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evo.main import create_evo_system
from evo.config import Config


class SciFiStoryWriter:
    """Autonomous agent for generating science fiction stories."""

    def __init__(self):
        """Initialize the Sci-Fi Story Writer."""
        self.system = create_evo_system()
        self.memory = self.system.memory
        self.safety = self.system.safety
        self.model = Config.LLM_MODEL
        
        # Initialize LLM client
        try:
            from evo.llm.llm_client_iflow import IFlowClient
            from evo.llm.llm_client_openrouter import OpenRouterClient
            
            # Try iFlow client first, then OpenRouter
            provider = Config.LLM_PROVIDER.upper()
            if provider == 'IFLOW':
                self.llm_client = IFlowClient()
            elif provider == 'OPENROUTER':
                self.llm_client = OpenRouterClient()
            else:
                self.llm_client = None
        except Exception:
            self.llm_client = None
        
        # Configure story modes
        self.modes = self._configure_modes()

    def _configure_modes(self) -> Dict[str, str]:
        """Configure different story generation modes.
        
        Returns:
            Dictionary mapping mode names to descriptions.
        """
        return {
            'short': 'Short story (2,000-5,000 words)',
            'outline': 'Novel outline with chapter summaries',
            'character': 'Character profiles only',
            'world': 'World-building notes only',
            'full': 'Complete novel-length story'
        }

    def analyze_topic(self, topic: str) -> Dict[str, Any]:
        """Analyze a topic and determine sci-fi elements.
        
        Args:
            topic: The story topic.
            
        Returns:
            Dictionary with topic analysis.
        """
        print(f"\n{'='*60}")
        print(f"Analyzing topic: {topic}")
        print(f"{'='*60}\n")
        
        # Safety check
        safety_result = self.safety.check_action_safety(topic)
        if not safety_result['allowed']:
            print(f"Safety blocked: {safety_result['reason']}")
            return {
                'topic': topic,
                'safe': False,
                'reason': safety_result['reason']
            }
        
        # Use LLM to analyze topic
        if self.llm_client:
            try:
                prompt = f"""Analyze this topic for a science fiction story: "{topic}"

Determine:
1. Primary sci-fi genre (cyberpunk, space opera, hard sci-fi, dystopian, time travel, etc.)
2. Main theme or philosophical question
3. Potential technological or social elements
4. Setting possibilities
5. Character archetypes that would work well

Provide a concise analysis in JSON format with keys: genre, theme, elements, setting, characters."""
                
                analysis_text = self.llm_client.respond(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Parse the response (simplified)
                return {
                    'topic': topic,
                    'genre': 'science fiction',
                    'theme': analysis_text[:200],
                    'elements': ['AI', 'future technology'],
                    'setting': 'Unknown',
                    'characters': ['Protagonist', 'Antagonist'],
                    'safe': True
                }
            except Exception:
                pass
        
        # Fallback analysis
        return {
            'topic': topic,
            'genre': 'science fiction',
            'theme': f'Exploration of {topic} in a futuristic setting',
            'elements': ['Technology', 'Future society'],
            'setting': 'Futuristic world',
            'characters': ['Protagonist', 'Antagonist'],
            'safe': True
        }

    def generate_outline(self, topic: str) -> Dict[str, Any]:
        """Generate story outline with acts and scenes.
        
        Args:
            topic: The story topic.
            
        Returns:
            Dictionary with story outline.
        """
        print(f"\n{'='*60}")
        print("Generating story outline...")
        print(f"{'='*60}\n")
        
        # Get topic analysis
        analysis = self.analyze_topic(topic)
        
        if not analysis['safe']:
            return {
                'title': f'Story Blocked',
                'acts': [],
                'safe': False
            }
        
        # Generate outline using LLM
        if self.llm_client:
            try:
                prompt = f"""Create a detailed story outline for a sci-fi story about: {topic}

Create a structure with 3 acts:

Act 1 - Setup (Opening Hook):
- Introduce the protagonist and world
- Establish the status quo
- Inciting incident that disrupts everything

Act 2 - Rising Action:
- Protagonist faces challenges and obstacles
- Escalating stakes and complications
- Midpoint revelation or turning point

Act 3 - Climax and Resolution:
- Final confrontation or major revelation
- Consequences of protagonist's choices
- New equilibrium or transformation

For each act, provide:
- Act title (1-2 words)
- 3-4 key scenes with brief descriptions
- Emotional arc for the protagonist

Format as structured text."""
                
                outline_text = self.llm_client.respond(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return {
                    'title': f"The {topic} Chronicles",
                    'topic': topic,
                    'acts': self._parse_outline(outline_text),
                    'safe': True
                }
            except Exception:
                pass
        
        # Fallback outline
        return {
            'title': f"The {topic} Chronicles",
            'topic': topic,
            'acts': [
                {
                    'act': 1,
                    'title': 'The Discovery',
                    'scenes': [
                        'Introduction to the world and protagonist',
                        'Inciting incident that changes everything',
                        'Protagonist faces the challenge'
                    ]
                },
                {
                    'act': 2,
                    'title': 'The Struggle',
                    'scenes': [
                        'Protagonist attempts to overcome obstacles',
                        'Setbacks and complications arise',
                        'Midpoint revelation changes understanding'
                    ]
                },
                {
                    'act': 3,
                    'title': 'The Resolution',
                    'scenes': [
                        'Final confrontation or revelation',
                        'Consequences of protagonist\'s choice',
                        'New world order or understanding'
                    ]
                }
            ],
            'safe': True
        }

    def _parse_outline(self, outline_text: str) -> List[Dict[str, Any]]:
        """Parse LLM-generated outline text into structured format.
        
        Args:
            outline_text: Raw outline text from LLM.
            
        Returns:
            List of act dictionaries.
        """
        # Simple parsing - in real implementation, would use more sophisticated parsing
        return [
            {
                'act': 1,
                'title': 'The Discovery',
                'scenes': outline_text.split('\n')[:3]
            },
            {
                'act': 2,
                'title': 'The Struggle',
                'scenes': outline_text.split('\n')[3:6]
            },
            {
                'act': 3,
                'title': 'The Resolution',
                'scenes': outline_text.split('\n')[6:9]
            }
        ]

    def create_characters(self, topic: str, num_characters: int = 2) -> List[Dict[str, str]]:
        """Create detailed character profiles.
        
        Args:
            topic: The story topic.
            num_characters: Number of characters to create.
            
        Returns:
            List of character dictionaries.
        """
        print(f"\n{'='*60}")
        print(f"Creating {num_characters} characters...")
        print(f"{'='*60}\n")
        
        characters = []
        
        # Use LLM to create characters
        if self.llm_client:
            try:
                prompt = f"""Create {num_characters} distinct characters for a sci-fi story about: {topic}

For each character, provide:
- Name
- Role (protagonist, antagonist, supporting)
- Background/motivation
- Internal conflict
- Key strength
- Fatal flaw
- Goal

Make them diverse and compelling. Format clearly."""
                
                characters_text = self.llm_client.respond(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Parse characters (simplified)
                for i in range(min(num_characters, 3)):
                    characters.append({
                        'name': f"Character {i+1}",
                        'role': 'Protagonist' if i == 0 else 'Antagonist' if i == 1 else 'Supporting',
                        'background': f"Background for character {i+1}",
                        'motivation': f"Motivation for character {i+1}",
                        'conflict': f"Internal conflict for character {i+1}",
                        'strength': f"Strength of character {i+1}",
                        'flaw': f"Flaw of character {i+1}",
                        'goal': f"Goal for character {i+1}"
                    })
                
                return characters
            except Exception:
                pass
        
        # Fallback characters
        for i in range(num_characters):
            characters.append({
                'name': f"Character {i+1}",
                'role': 'Protagonist' if i == 0 else 'Antagonist' if i == 1 else 'Supporting',
                'background': f"Background for character {i+1}",
                'motivation': f"Motivation for character {i+1}",
                'conflict': f"Internal conflict for character {i+1}",
                'strength': f"Strength of character {i+1}",
                'flaw': f"Flaw of character {i+1}",
                'goal': f"Goal for character {i+1}"
            })
        
        return characters

    def build_world(self, topic: str) -> Dict[str, Any]:
        """Build detailed world for the story.
        
        Args:
            topic: The story topic.
            
        Returns:
            Dictionary with world details.
        """
        print(f"\n{'='*60}")
        print("Building world...")
        print(f"{'='*60}\n")
        
        # Use LLM to build world
        if self.llm_client:
            try:
                prompt = f"""Create a detailed world for a sci-fi story about: {topic}

Describe:
- Setting (time period, location, environment)
- Technology level and key innovations
- Social structure and political system
- Economy and resource distribution
- Cultural values and beliefs
- Any unique or exotic elements

Make it vivid and immersive. Include specific details."""
                
                world_text = self.llm_client.respond(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return {
                    'topic': topic,
                    'setting': f"Setting for {topic}",
                    'technology': f"Technology for {topic}",
                    'society': f"Society for {topic}",
                    'economy': f"Economy for {topic}",
                    'culture': f"Culture for {topic}",
                    'details': world_text
                }
            except Exception:
                pass
        
        # Fallback world
        return {
            'topic': topic,
            'setting': f"A futuristic world focused on {topic}",
            'technology': f"Advanced technology related to {topic}",
            'society': f"Society shaped by {topic}",
            'economy': f"Economy centered on {topic}",
            'culture': f"Culture influenced by {topic}",
            'details': f"Detailed world building for {topic}"
        }

    def write_story(self, topic: str, mode: str = 'short') -> Dict[str, Any]:
        """Write a complete science fiction story.
        
        Args:
            topic: The story topic.
            mode: Story generation mode.
            
        Returns:
            Dictionary with story content.
        """
        print(f"\n{'='*60}")
        print("Writing story...")
        print(f"{'='*60}\n")
        
        # Safety check
        safety_result = self.safety.check_action_safety(topic)
        if not safety_result['allowed']:
            return {
                'title': 'Story Blocked',
                'content': f"Story generation blocked: {safety_result['reason']}",
                'safe': False
            }
        
        # Generate story components
        outline = self.generate_outline(topic)
        characters = self.create_characters(topic, 3)
        world = self.build_world(topic)
        
        # Write story using LLM
        if self.llm_client:
            try:
                prompt = f"""Write a compelling science fiction short story (2000-3000 words) about: {topic}

Story Outline:
{self._format_outline(outline)}

Characters:
{self._format_characters(characters)}

World:
{self._format_world(world)}

Requirements:
- Begin with a compelling hook
- Show, don't tell - use vivid descriptions
- Include dialogue between characters
- Build tension throughout
- End with a satisfying resolution
- Include sensory details and atmosphere
- Make the protagonist face meaningful choices

Write in engaging prose with good pacing."""
                
                story_content = self.llm_client.respond(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return {
                    'title': outline['title'],
                    'topic': topic,
                    'mode': mode,
                    'content': story_content,
                    'characters': characters,
                    'world': world,
                    'outline': outline,
                    'safe': True
                }
            except Exception as e:
                print(f"  LLM error: {e}")
        
        # Fallback story
        story_content = f"# {outline['title']}\n\n"
        story_content += f"## The Discovery\n\n"
        story_content += "In the year 2187, the world had changed irrevocably. "
        story_content += f"The discovery involving {topic} had begun.\n\n"
        story_content += f"## The Struggle\n\n"
        story_content += f"Protagonist faced challenges related to {topic}. "
        story_content += "Obstacles mounted, and the journey was far from over.\n\n"
        story_content += f"## The Resolution\n\n"
        story_content += f"Ultimately, the issue of {topic} was resolved. "
        story_content += "The world moved forward, forever changed.\n\n"
        story_content += "The End.\n\n"
        
        return {
            'title': outline['title'],
            'topic': topic,
            'mode': mode,
            'content': story_content,
            'characters': characters,
            'world': world,
            'outline': outline,
            'safe': True
        }

    def _format_outline(self, outline: Dict[str, Any]) -> str:
        """Format outline for display.
        
        Args:
            outline: Outline dictionary.
            
        Returns:
            Formatted outline text.
        """
        text = f"Title: {outline['title']}\n\n"
        for act in outline['acts']:
            text += f"Act {act['act']}: {act['title']}\n"
            for scene in act['scenes']:
                text += f"  - {scene}\n"
            text += "\n"
        return text

    def _format_characters(self, characters: List[Dict[str, str]]) -> str:
        """Format characters for display.
        
        Args:
            characters: List of character dictionaries.
            
        Returns:
            Formatted characters text.
        """
        text = ""
        for char in characters:
            text += f"{char['name']} ({char['role']})\n"
            text += f"  Background: {char['background']}\n"
            text += f"  Motivation: {char['motivation']}\n"
            text += f"  Conflict: {char['conflict']}\n"
            text += f"  Goal: {char['goal']}\n\n"
        return text

    def _format_world(self, world: Dict[str, Any]) -> str:
        """Format world for display.
        
        Args:
            world: World dictionary.
            
        Returns:
            Formatted world text.
        """
        text = f"Setting: {world['setting']}\n\n"
        text += f"Technology: {world['technology']}\n"
        text += f"Society: {world['society']}\n"
        text += f"Economy: {world['economy']}\n"
        text += f"Culture: {world['culture']}\n"
        return text

    def export_story(self, story: Dict[str, Any]) -> str:
        """Export story to markdown file.
        
        Args:
            story: The story dictionary.
            
        Returns:
            Path to exported file.
        """
        print(f"\n{'='*60}")
        print("Exporting story...")
        print(f"{'='*60}\n")
        
        # Generate filename with date and sanitized title
        safe_title = ''.join(c for c in story['title'] if c.isalnum() or c in (' ', '-', '_'))
        filename = f"_out/scifi_story_{datetime.now().strftime('%Y%m%d')}_{safe_title[:20]}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Title
            f.write(f"# {story['title']}\n\n")
            f.write(f"*Generated by Sci-Fi Story Writer*\n\n")
            f.write(f"**Topic:** {story['topic']}\n")
            f.write(f"**Mode:** {story['mode']}\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write("---\n\n")
            
            # Story content
            f.write(story['content'])
            
            # Add metadata section
            f.write("\n---\n\n")
            f.write("## Story Metadata\n\n")
            f.write(f"**Characters:** {len(story['characters'])}\n")
            f.write(f"**Acts:** {len(story['outline']['acts'])}\n")
            f.write(f"**Genre:** Science Fiction\n\n")
            
            # Characters section
            if story['characters']:
                f.write("## Characters\n\n")
                for char in story['characters']:
                    f.write(f"### {char['name']} ({char['role']})\n\n")
                    f.write(f"- **Background:** {char['background']}\n")
                    f.write(f"- **Motivation:** {char['motivation']}\n")
                    f.write(f"- **Conflict:** {char['conflict']}\n")
                    f.write(f"- **Goal:** {char['goal']}\n\n")
            
            # World section
            if story['world']:
                f.write("## World Building\n\n")
                f.write(f"**Setting:** {story['world']['setting']}\n\n")
                f.write(f"**Technology:** {story['world']['technology']}\n\n")
                f.write(f"**Society:** {story['world']['society']}\n\n")
                f.write(f"**Economy:** {story['world']['economy']}\n\n")
                f.write(f"**Culture:** {story['world']['culture']}\n\n")
        
        print(f"✓ Story exported to: {filename}")
        
        return filename


def main():
    """Main entry point for Sci-Fi Story Writer demo."""
    print("="*60)
    print("Sci-Fi Story Writer")
    print("AI-powered science fiction story generator")
    print("="*60)
    
    # Create writer
    writer = SciFiStoryWriter()
    
    # Get topic from user or use default
    topic = "robot learning to feel emotions"
    
    # Generate story
    story = writer.write_story(topic)
    
    # Export story
    output_file = writer.export_story(story)
    
    print(f"\n{'='*60}")
    print("Story complete!")
    print(f"Story saved to: {output_file}")
    print("="*60)


if __name__ == "__main__":
    main()