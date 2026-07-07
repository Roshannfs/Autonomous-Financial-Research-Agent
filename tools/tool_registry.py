from pydantic import BaseModel, Field
from typing import Optional, Dict
from langchain_core.tools import tool
import uuid

# Existing Tools
from tools.financial_api import (
    company_profile,
    financial_ratios,
    ticker_resolver,
    get_financial_data
)
from memory.vector_store import get_vector_store
from tools.sec_edgar import sec_filing_search
from tools.web_search import web_search
from tools.news_sentiment import news_sentiment

# NEW Advanced Tools
from tools.advanced_tools import (
    earnings_transcript,
    peer_comparison,
    calculator,
    fact_checker,
    report_generator
)

# ---------------------------------------------------------
# Memory Tools (Renamed to match exact targets)
# ---------------------------------------------------------
class VectorStoreInput(BaseModel):
    content: str = Field(description="The research findings or text content to save.")
    metadata: Dict[str, str] = Field(description="Dictionary containing 'ticker', 'date', and 'source_type'.")

@tool("vector_store", args_schema=VectorStoreInput)
def vector_store(content: str, metadata: dict) -> str:
    """Stores new research findings in the agent's long-term memory for future retrieval."""
    try:
        db = get_vector_store()
        doc_id = str(uuid.uuid4())
        db.add_texts(texts=[content], metadatas=[metadata], ids=[doc_id])
        return f"✅ Successfully stored in long-term memory. Document ID: {doc_id}"
    except Exception as e:
        return f"Error storing to memory: {str(e)}"

# Legacy alias
vector_db_store = vector_store

class VectorSearchInput(BaseModel):
    query: str = Field(description="The search query to find relevant past research.")
    top_k: int = Field(default=3, description="Number of results to return.")
    filter: Optional[Dict[str, str]] = Field(default=None, description="Optional metadata filter.")

@tool("vector_search", args_schema=VectorSearchInput)
def vector_search(query: str, top_k: int, filter: dict = None) -> str:
    """Searches the agent's long-term memory (vector database) for previously researched information."""
    try:
        db = get_vector_store()
        results = db.similarity_search_with_score(query, k=top_k, filter=filter)
        if not results:
            return "No relevant information found in long-term memory."
        
        output = "Memory Results:\n"
        for doc, score in results:
            output += f"- [Relevance: {score:.4f}] {doc.page_content} (Source: {doc.metadata})\n"
        return output
    except Exception as e:
        return f"Error searching memory: {str(e)}"

# Legacy alias
vector_db_search = vector_search

# ---------------------------------------------------------
# TOOL COMPILATION
# ---------------------------------------------------------

def get_all_tools():
    """Returns a list of all tools available to the Agent."""
    tools = [
        # The 10 Target Tools explicitly requested:
        company_profile,
        earnings_transcript,
        financial_ratios,
        peer_comparison,
        report_generator,
        calculator,
        fact_checker,
        vector_search,
        vector_store,
        ticker_resolver,
        
        # Legacy/Support tools
        get_financial_data,
        sec_filing_search,
        web_search,
        news_sentiment
    ]
    return tools