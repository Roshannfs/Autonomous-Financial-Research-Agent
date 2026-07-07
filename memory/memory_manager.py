import os
from typing import List, Dict, Any, Optional
from memory.vector_store import get_vector_store
from memory.episodic_memory import EpisodicMemory

class UnifiedMemoryManager:
    """
    Unified Memory Manager coordinates all three memory systems of the agent:
    1. Short-Term Memory: Conversational message history within the agent graph.
    2. Long-Term Memory: Semantic vector store (Chroma) for persistent facts and research.
    3. Episodic Memory: Complete task execution logs to allow learning from experiences.
    """
    def __init__(self, episodic_filepath: Optional[str] = None):
        self.episodic_memory = EpisodicMemory(filepath=episodic_filepath)
        
    def get_short_term_memory(self, state: Dict[str, Any]) -> List[Any]:
        """Retrieves conversational messages (short-term memory) from the current state."""
        return state.get("messages", [])

    def store_long_term_fact(self, content: str, metadata: Dict[str, Any]) -> str:
        """Stores a research fact in long-term memory (Chroma vector database)."""
        import uuid
        try:
            db = get_vector_store()
            doc_id = str(uuid.uuid4())
            db.add_texts(texts=[content], metadatas=[metadata], ids=[doc_id])
            return doc_id
        except Exception as e:
            raise RuntimeError(f"Failed to store fact in long-term memory: {str(e)}")

    def search_long_term_memory(self, query: str, top_k: int = 3, filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Searches long-term semantic memory for facts matching the query."""
        try:
            db = get_vector_store()
            results = db.similarity_search_with_score(query, k=top_k, filter=filter)
            return [{"content": doc.page_content, "metadata": doc.metadata, "score": score} for doc, score in results]
        except Exception as e:
            raise RuntimeError(f"Failed to search long-term memory: {str(e)}")

    def record_episode(self, query: str, grounded_query: str, tool_calls: List[Dict[str, Any]], final_report: str, success: bool = True) -> str:
        """Records an execution episode (episodic memory)."""
        return self.episodic_memory.record_episode(
            query=query,
            grounded_query=grounded_query,
            tool_calls=tool_calls,
            final_report=final_report,
            success=success
        )

    def recall_episodes(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Recalls past episodes (episodic memory) matching the query."""
        return self.episodic_memory.search_episodes(query=query, limit=limit)
