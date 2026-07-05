import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.tools import tool

class WebSearchInput(BaseModel):
    query: str = Field(description="Search query for current news, analysis, and commentary.")
    num_results: int = Field(default=10, description="Number of search results to return.")
    date_range: Optional[str] = Field(default=None, description="Optional date range.")

@tool("web_search", args_schema=WebSearchInput)
def web_search(query: str, num_results: int = 10, date_range: str = None) -> str:
    """Performs a web search for current news, analysis, and commentary about a company or financial topic."""
    try:
        # We spoof a standard browser User-Agent so the search engine does not block our request
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        search_url = f"https://html.duckduckgo.com/html/?q={query} news"
        
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        # Parse the raw HTML into a searchable tree structure
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # DuckDuckGo HTML results use the 'result__snippet' class for summary paragraphs
        for result in soup.find_all('a', class_='result__snippet', limit=num_results):
            snippet = result.text.strip()
            link = result.get('href', 'No URL')
            results.append(f"Snippet: {snippet} (URL: {link})")
            
        if not results:
            return "No recent web results found for this query."
            
        return "\n\n".join(results)
        
    except Exception as e:
        return f"Web search encountered an error: {str(e)}"