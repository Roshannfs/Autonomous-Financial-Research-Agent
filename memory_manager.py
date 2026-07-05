import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Load environment variables from the .env file
load_dotenv()

def initialize_long_term_memory():
    """
    Initializes the Chroma Vector Database to serve as the agent's long-term memory.
    The data will be persisted locally in the 'long_term_memory' directory.
    """
    # Define the local directory to store the database
    persist_directory = "./long_term_memory"

    # Initialize the embedding model to convert text into vectors
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

    # Create or connect to the local vector store
    vector_store = Chroma(
        collection_name="financial_research_data",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )

    print(f"✅ Vector Database initialized. Persisting to: {persist_directory}")
    return vector_store

# Test the initialization
if __name__ == "__main__":
    db = initialize_long_term_memory()