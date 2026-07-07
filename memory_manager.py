import os
from dotenv import load_dotenv
from memory.memory_manager import UnifiedMemoryManager

# Load environment variables from the .env file
load_dotenv()

def initialize_long_term_memory():
    """
    Initializes the Chroma Vector Database to serve as the agent's long-term memory.
    The data will be persisted locally in the 'long_term_memory' directory.
    """
    from memory.vector_store import get_vector_store
    vector_store = get_vector_store()
    print("✅ Vector Database initialized.")
    return vector_store

def get_memory_manager():
    """Helper to return an instance of the UnifiedMemoryManager."""
    return UnifiedMemoryManager()