"""Capability Registry - Dynamic tracking of tools, skills, and knowledge with validation."""

from typing import Any, Callable, Dict, List, Optional
from evo.config import Config
from evo.validation import validate_tool_name, validate_skill_level, validate_name, get_logger
from evo.types import KnowledgeValue

logger = get_logger("evo.capability")


class CapabilityRegistry:
    """Dynamic tracking of tools, skills, and knowledge."""
    
    def __init__(self) -> None:
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._skills: Dict[str, Dict[str, Any]] = {}
        self._knowledge: Dict[str, Any] = {}
        # Search index: maps lowercase tokens to tool names for fast lookup
        self._tool_search_index: Dict[str, List[str]] = {}
    
    # Tool methods
    def _build_tool_search_index(self, name: str, description: str) -> None:
        """Build search index for a tool from its name and description."""
        # Remove tool from existing index entries
        for token_list in self._tool_search_index.values():
            if name in token_list:
                token_list.remove(name)
        
        # Tokenize name and description
        text = f"{name} {description}".lower()
        tokens = text.split()
        
        # Index each token
        for token in tokens:
            if token not in self._tool_search_index:
                self._tool_search_index[token] = []
            if name not in self._tool_search_index[token]:
                self._tool_search_index[token].append(name)
    
    def register_tool(
        self,
        name: str,
        description: str,
        callable_func: Optional[Callable] = None
    ) -> None:
        """Register a tool in the capability registry."""
        if not validate_tool_name(name):
            raise ValueError(f"Invalid tool name: {name}")
        self._tools[name] = {
            "description": description,
            "callable": callable_func
        }
        # Build search index from name and description
        self._build_tool_search_index(name, description)
        logger.debug(f"Registered tool: {name}")
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a tool by name, returns None if not found."""
        return self._tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
    
    def unregister_tool(self, name: str) -> None:
        """Remove a tool from the registry."""
        self._tools.pop(name, None)
        # Remove from search index
        for token_list in self._tool_search_index.values():
            if name in token_list:
                token_list.remove(name)
        logger.debug(f"Unregistered tool: {name}")
    
    def search_tools(self, query: str) -> List[str]:
        """Search for tools by name containing the query string.
        
        Uses a search index for faster lookups when multiple tools exist.
        Falls back to linear search for partial matches if index doesn't help.
        """
        if not query:
            return []
        
        query_lower = query.lower()
        results: set[str] = set()
        
        # Check search index for exact token matches
        for token, tool_names in self._tool_search_index.items():
            if query_lower in token:
                results.update(tool_names)
        
        # If index didn't find matches, do fallback linear search
        if not results:
            results = {name for name in self.list_tools() if query_lower in name.lower()}
        
        return sorted(results)
    
    # Skill methods
    def register_skill(self, name: str, description: str, level: Optional[float] = None) -> None:
        """Register a skill in the capability registry."""
        if not validate_name(name, "Skill"):
            raise ValueError(f"Invalid skill name: {name}")
        
        skill_level = level if level is not None else Config.CAPABILITY_DEFAULT_LEVEL
        if not validate_skill_level(skill_level):
            raise ValueError(f"Invalid skill level: {skill_level}")
        
        self._skills[name] = {
            "description": description,
            "level": skill_level
        }
        logger.debug(f"Registered skill: {name} (level: {skill_level})")
    
    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a skill by name, returns None if not found."""
        return self._skills.get(name)
    
    def list_skills(self) -> List[str]:
        """List all registered skill names."""
        return list(self._skills.keys())
    
    def unregister_skill(self, name: str) -> None:
        """Remove a skill from the registry."""
        self._skills.pop(name, None)
        logger.debug(f"Unregistered skill: {name}")
    
    def update_skill_level(self, name: str, level: float) -> None:
        """Update the proficiency level of a skill."""
        if not validate_skill_level(level):
            raise ValueError(f"Invalid skill level: {level}")
        
        if name in self._skills:
            self._skills[name]["level"] = level
            logger.debug(f"Updated skill level: {name} -> {level}")
    
    # Knowledge methods
    def register_knowledge(self, key: str, value: KnowledgeValue) -> None:
        """Register a knowledge fact in the capability registry."""
        self._knowledge[key] = value
        logger.debug(f"Registered knowledge: {key}")
    
    def get_knowledge(self, key: str) -> Optional[Any]:
        """Get knowledge by key, returns None if not found."""
        return self._knowledge.get(key)
    
    def list_knowledge(self) -> List[str]:
        """List all registered knowledge keys."""
        return list(self._knowledge.keys())
    
    def unregister_knowledge(self, key: str) -> None:
        """Remove knowledge from the registry."""
        self._knowledge.pop(key, None)
        logger.debug(f"Unregistered knowledge: {key}")
    
    # Query methods
    def list_all_capabilities(self) -> Dict[str, List[str]]:
        """List all registered capabilities by type."""
        return {
            "tools": self.list_tools(),
            "skills": self.list_skills(),
            "knowledge": self.list_knowledge()
        }
    
    def get_capability_count(self) -> int:
        """Get total count of all registered capabilities."""
        return len(self._tools) + len(self._skills) + len(self._knowledge)
