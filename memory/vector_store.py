import os
from langchain_chroma import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

def get_vector_store():
    """Initializes and returns the Chroma vector database using NVIDIA embeddings."""
    
    # Initialize the NVIDIA embedding model
    embeddings = NVIDIAEmbeddings(
        model="NV-Embed-QA", 
        api_key=os.getenv("NVIDIA_API_KEY"),
        base_url="https://integrate.api.nvidia.com/v1"
    )
    
    # Define where the database will be saved on your hard drive
    persist_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "long_term_memory")
    
    # Create or connect to the Chroma database
    vector_store = Chroma(
        collection_name="financial_research",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    
    return vector_store