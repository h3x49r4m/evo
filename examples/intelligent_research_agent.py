"""Intelligent Research Agent - Automated research and paper writing system.

This example demonstrates how to use the evo autonomous agent system
to conduct automated research on a topic and generate a research paper.
"""

from typing import Any, Dict, List, Optional
from evo.main import create_evo_system


class IntelligentResearchAgent:
    """Autonomous agent for conducting research and writing papers."""

    def __init__(self):
        """Initialize the Intelligent Research Agent."""
        self.system = create_evo_system()
        self.capability = self.system.capability
        self.memory = self.system.memory
        self.safety = self.system.safety
        self.llm_client = self.system.action.llm_client if hasattr(self.system.action, 'llm_client') else None
        
        # Register research tools
        self._register_tools()

    def _register_tools(self):
        """Register research-specific tools."""
        # Search tool
        def search_tool(query: str) -> str:
            return f"Search results for: {query}"
        
        # Read tool
        def read_tool(source: str) -> str:
            return f"Content from: {source}"
        
        # Write tool
        def write_tool(content: str) -> str:
            return f"Written: {len(content)} characters"
        
        # Analyze tool
        def analyze_tool(data: str) -> str:
            return f"Analysis of: {data[:50]}..."
        
        self.capability.register_tool("search", search_tool, "Search for information")
        self.capability.register_tool("read", read_tool, "Read and parse documents")
        self.capability.register_tool("write", write_tool, "Write content")
        self.capability.register_tool("analyze", analyze_tool, "Analyze data")

    def research(self, topic: str, show_progress: bool = False) -> Dict[str, Any]:
        """Conduct research on a given topic.
        
        Args:
            topic: The research topic to investigate.
            show_progress: Whether to show progress during research.
            
        Returns:
            Dictionary containing research findings.
        """
        print(f"\n{'='*60}")
        print(f"Starting research on: {topic}")
        print(f"{'='*60}\n")
        
        # Safety check
        safety_result = self.safety.check_action_safety(topic)
        if not safety_result['allowed']:
            print(f"Safety blocked: {safety_result['reason']}")
            return {
                'topic': topic,
                'findings': [],
                'safety_blocked': True,
                'reason': safety_result['reason']
            }
        
        # Research phases
        phases = [
            "Analyzing topic and generating research questions",
            "Searching for relevant information",
            "Collecting and analyzing data",
            "Synthesizing findings"
        ]
        
        findings = []
        progress = []
        
        for i, phase in enumerate(phases, 1):
            if show_progress:
                print(f"[{i}/{len(phases)}] {phase}...")
                progress.append(f"Phase {i} completed")
            
            # Simulate research work
            phase_result = self._execute_research_phase(topic, i)
            findings.append(phase_result)
        
        # Store findings in memory
        self.memory.working.store("research_findings", findings)
        
        print(f"\n✓ Research completed on: {topic}")
        print(f"  - {len(findings)} research phases completed")
        
        result = {
            'topic': topic,
            'findings': findings,
            'safety_blocked': False,
            'progress': progress if show_progress else None
        }
        
        return result

    def _execute_research_phase(self, topic: str, phase: int) -> Dict[str, Any]:
        """Execute a single research phase.
        
        Args:
            topic: The research topic.
            phase: The phase number.
            
        Returns:
            Dictionary with phase results.
        """
        # Use LLM for intelligent planning if available
        if self.llm_client:
            try:
                prompt = f"Generate research plan for phase {phase} on topic: {topic}"
                llm_response = self.llm_client.respond(
                    model=self.system.action.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return {
                    'phase': phase,
                    'plan': llm_response,
                    'data': f"Research data for phase {phase}"
                }
            except Exception:
                pass
        
        # Fallback to simple planning
        return {
            'phase': phase,
            'plan': f"Standard research plan for phase {phase}",
            'data': f"Research data for phase {phase}"
        }

    def generate_paper(self, research_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a research paper from research findings.
        
        Args:
            research_result: The research results from research() method.
            
        Returns:
            Dictionary containing paper structure and content.
        """
        print(f"\n{'='*60}")
        print("Generating research paper...")
        print(f"{'='*60}\n")
        
        if research_result.get('safety_blocked'):
            return {
                'title': 'Research Blocked',
                'abstract': 'Research was blocked due to safety concerns.',
                'sections': []
            }
        
        # Generate paper structure
        paper = {
            'title': f"Research on {research_result['topic']}",
            'abstract': self._generate_abstract(research_result),
            'sections': self._generate_sections(research_result)
        }
        
        print(f"✓ Paper generated:")
        print(f"  - Title: {paper['title']}")
        print(f"  - Abstract: {len(paper['abstract'])} characters")
        print(f"  - Sections: {len(paper['sections'])}")
        
        return paper

    def _generate_abstract(self, research_result: Dict[str, Any]) -> str:
        """Generate paper abstract.
        
        Args:
            research_result: The research results.
            
        Returns:
            Abstract text.
        """
        findings = research_result.get('findings', [])
        topic = research_result.get('topic', 'Unknown')
        
        abstract = f"This paper presents research findings on {topic}. "
        abstract += f"The study explores {len(findings)} key aspects of the topic. "
        abstract += "The methodology combines automated information gathering "
        abstract += "with intelligent analysis to provide comprehensive insights."
        
        return abstract

    def _generate_sections(self, research_result: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate paper sections.
        
        Args:
            research_result: The research results.
            
        Returns:
            List of section dictionaries.
        """
        sections = [
            {
                'title': 'Introduction',
                'content': f"Introduction to {research_result.get('topic', 'the topic')}."
            },
            {
                'title': 'Methodology',
                'content': "Research methodology using automated agents and AI tools."
            },
            {
                'title': 'Findings',
                'content': f"Key findings from {len(research_result.get('findings', []))} research phases."
            },
            {
                'title': 'Discussion',
                'content': "Discussion of results and implications."
            },
            {
                'title': 'Conclusion',
                'content': "Summary and future research directions."
            }
        ]
        
        return sections

    def export_paper(self, paper: Dict[str, Any], output_file: str) -> None:
        """Export paper to a markdown file.
        
        Args:
            paper: The paper dictionary.
            output_file: Path to output file.
        """
        print(f"\n{'='*60}")
        print(f"Exporting paper to: {output_file}")
        print(f"{'='*60}\n")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Title
            f.write(f"# {paper['title']}\n\n")
            
            # Abstract
            f.write("## Abstract\n\n")
            f.write(f"{paper['abstract']}\n\n")
            
            # Sections
            for section in paper['sections']:
                f.write(f"## {section['title']}\n\n")
                f.write(f"{section['content']}\n\n")
        
        print(f"✓ Paper exported successfully")


def main():
    """Main entry point for Intelligent Research Agent demo."""
    print("="*60)
    print("Intelligent Research Agent")
    print("Automated research and paper writing system")
    print("="*60)
    
    # Create agent
    agent = IntelligentResearchAgent()
    
    # Research a topic
    topic = "The impact of AI on scientific research"
    result = agent.research(topic, show_progress=True)
    
    # Generate paper
    paper = agent.generate_paper(result)
    
    # Export paper
    output_file = "research_paper.md"
    agent.export_paper(paper, output_file)
    
    print(f"\n{'='*60}")
    print("Research complete!")
    print(f"Paper saved to: {output_file}")
    print("="*60)


if __name__ == "__main__":
    main()