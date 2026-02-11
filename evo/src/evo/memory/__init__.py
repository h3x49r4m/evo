"""Memory System - Three-tier memory architecture with ChromaDB."""

import json
from typing import Any, Dict, List, Optional

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


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
        
        def __init__(self, collection_name: str = "episodes", use_chromadb: bool = True) -> None:
            self.collection_name = collection_name
            self.use_chromadb = use_chromadb and CHROMADB_AVAILABLE
            self._experiences: Dict[str, Dict[str, Any]] = {}
            
            if self.use_chromadb:
                # Initialize ChromaDB client
                self.client = chromadb.Client()
                self.collection = self.client.get_or_create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
            else:
                # Fallback to in-memory dictionary
                self.client = None
                self.collection = self
        
        async def store_experience(self, experience: Dict[str, Any]) -> str:
            """Store an experience and return its ID."""
            experience_str = json.dumps(experience, sort_keys=True)
            experience_id = str(hash(experience_str))
            
            if self.use_chromadb:
                # Store in ChromaDB with embedding
                self.collection.add(
                    documents=[experience_str],
                    ids=[experience_id],
                    metadatas=[{"timestamp": str(experience.get("timestamp", "now"))}]
                )
            else:
                # Fallback to dictionary
                self._experiences[experience_id] = experience
            
            return experience_id
        
        async def retrieve_similar(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
            """Retrieve k most similar experiences to the query."""
            if self.use_chromadb:
                # Query ChromaDB for similar experiences
                results = self.collection.query(
                    query_texts=[query],
                    n_results=k
                )
                
                experiences = []
                if results and results["documents"] and results["documents"][0]:
                    for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
                        experiences.append(json.loads(doc))
                
                return experiences
            else:
                # Fallback: return first k experiences
                return list(self._experiences.values())[:k]
        
        async def cleanup(self) -> None:
            """Clean up the collection."""
            if self.use_chromadb and self.client:
                self.client.delete_collection(name=self.collection_name)
            else:
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
    
    def __init__(self, collection_name: str = "episodes", use_chromadb: bool = True) -> None:
        self.working = self.WorkingMemory()
        self.episodic = self.EpisodicMemory(
            collection_name=collection_name,
            use_chromadb=use_chromadb
        )
        self.semantic = self.SemanticMemory()
    
    async def cleanup(self) -> None:
        """Clean up episodic memory resources."""
        await self.episodic.cleanup()
