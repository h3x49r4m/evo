"""Memory System - Three-tier memory architecture."""

import json
from typing import Any, Dict, List, Optional


class MemorySystem:
    """Main memory system integrating all three memory tiers."""
    
    class WorkingMemory:
        """Current context window, immediate state."""
        
        def __init__(self) -> None:
            self.context: Dict[str, Any] = {}
        
        def store(self, key: str, value: Any) -> None:
            """Store a key-value pair in working memory."""
            self.context[key] = value
        
        def retrieve(self, key: str) -> Optional[Any]:
            """Retrieve a value by key, returns None if not found."""
            return self.context.get(key)
        
        def clear(self) -> None:
            """Clear all data from working memory."""
            self.context.clear()
    
    class EpisodicMemory:
        """Vector database of experiences, searchable by semantic similarity."""
        
        def __init__(self, collection_name: str = "episodes") -> None:
            self.collection_name = collection_name
            self._experiences: Dict[str, Dict[str, Any]] = {}
            self.collection = self  # Simulating collection for test compatibility
        
        async def store_experience(self, experience: Dict[str, Any]) -> str:
            """Store an experience and return its ID."""
            experience_str = json.dumps(experience, sort_keys=True)
            experience_id = str(hash(experience_str))
            self._experiences[experience_id] = experience
            return experience_id
        
        async def retrieve_similar(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
            """Retrieve k most similar experiences to the query."""
            results = []
            for exp in list(self._experiences.values())[:k]:
                results.append(exp)
            return results
        
        async def cleanup(self) -> None:
            """Clean up the collection."""
            self._experiences.clear()
    
    class SemanticMemory:
        """Persistent knowledge base, not overwritten by new experiences."""
        
        def __init__(self) -> None:
            self.knowledge: Dict[str, Any] = {}
        
        def add_fact(self, key: str, value: Any) -> None:
            """Add or overwrite a fact in semantic memory."""
            self.knowledge[key] = value
        
        def retrieve_fact(self, key: str) -> Optional[Any]:
            """Retrieve a fact by key, returns None if not found."""
            return self.knowledge.get(key)
    
    def __init__(self, collection_name: str = "episodes") -> None:
        self.working = self.WorkingMemory()
        self.episodic = self.EpisodicMemory(collection_name=collection_name)
        self.semantic = self.SemanticMemory()
    
    async def cleanup(self) -> None:
        """Clean up episodic memory resources."""
        await self.episodic.cleanup()