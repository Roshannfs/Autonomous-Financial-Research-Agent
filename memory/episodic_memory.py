import json
import os
import uuid
import datetime
from typing import List, Dict, Any, Optional

class EpisodicMemory:
    """
    Manages Episodic Memory for the Autonomous Financial Research Agent.
    Stores and retrieves historical execution episodes (past queries, tool calls, and final responses).
    """
    def __init__(self, filepath: Optional[str] = None):
        if filepath is None:
            # Save episodic memory in the local directory under 'long_term_memory'
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = os.path.join(base_dir, "long_term_memory", "episodic_memory.json")
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load_episodes(self) -> List[Dict[str, Any]]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_episodes(self, episodes: List[Dict[str, Any]]):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(episodes, f, indent=2)
        except Exception as e:
            print(f"Error saving episodic memory: {str(e)}")

    def record_episode(self, query: str, grounded_query: str, tool_calls: List[Dict[str, Any]], final_report: str, success: bool = True) -> str:
        """Records an execution episode containing the query, tool calls, final report, and success status."""
        episodes = self._load_episodes()
        episode_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        episode = {
            "episode_id": episode_id,
            "timestamp": timestamp,
            "query": query,
            "grounded_query": grounded_query,
            "tool_calls": tool_calls,
            "final_report": final_report,
            "success": success
        }
        
        episodes.append(episode)
        self._save_episodes(episodes)
        return episode_id

    def search_episodes(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Searches past episodes using query keyword relevance."""
        episodes = self._load_episodes()
        if not episodes:
            return []
            
        keywords = [w.lower() for w in query.split() if len(w) > 3]
        if not keywords:
            # Return latest episodes if query is short/generic
            return episodes[-limit:]
            
        scored_episodes = []
        for ep in episodes:
            score = 0
            ep_query_lower = ep.get("query", "").lower()
            for kw in keywords:
                if kw in ep_query_lower:
                    score += 1
            if score > 0:
                scored_episodes.append((score, ep))
                
        # Sort by score descending, then timestamp descending
        scored_episodes.sort(key=lambda x: (x[0], x[1].get("timestamp", "")), reverse=True)
        return [ep for _, ep in scored_episodes[:limit]]

    def get_all_episodes(self) -> List[Dict[str, Any]]:
        return self._load_episodes()
