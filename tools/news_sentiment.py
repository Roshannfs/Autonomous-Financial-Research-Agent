from textblob import TextBlob
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from tools.web_search import web_search

class NewsSentimentInput(BaseModel):
    query: str = Field(description="The company or topic to analyze sentiment for.")
    num_articles: int = Field(default=5, description="Number of articles to analyze.")
    lookback_days: int = Field(default=7, description="Days to look back (currently simulated).")

@tool("news_sentiment", args_schema=NewsSentimentInput)
def news_sentiment(query: str, num_articles: int = 5, lookback_days: int = 7) -> str:
    """Analyzes sentiment of recent news articles about a company or topic using NLP."""
    try:
        # Programmatically invoke our own web_search tool to gather the raw text
        raw_news = web_search.invoke({"query": f"{query} financial news", "num_results": num_articles})
        
        if "encountered an error" in raw_news or "No recent web results" in raw_news:
            return "Could not retrieve enough news to analyze sentiment."

        snippets = raw_news.split("\n\n")
        total_polarity = 0
        total_subjectivity = 0
        analyzed_count = 0
        
        detailed_analysis = "News Sentiment Breakdown:\n"
        
        # Analyze each snippet individually using TextBlob NLP
        for snippet in snippets:
            blob = TextBlob(snippet)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            total_polarity += polarity
            total_subjectivity += subjectivity
            analyzed_count += 1
            
            detailed_analysis += f"- Snippet: {snippet[:60]}... | Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}\n"

        if analyzed_count == 0:
            return "No valid text available for sentiment analysis."

        avg_polarity = total_polarity / analyzed_count
        avg_subjectivity = total_subjectivity / analyzed_count
        
        # Classify the numerical average into a distinct label
        if avg_polarity > 0.1:
            overall = "POSITIVE"
        elif avg_polarity < -0.1:
            overall = "NEGATIVE"
        else:
            overall = "NEUTRAL"
            
        summary = (
            f"Overall Sentiment: {overall}\n"
            f"Average Polarity Score: {avg_polarity:.2f} (Scale: -1.0 to 1.0)\n"
            f"Average Subjectivity Score: {avg_subjectivity:.2f} (Scale: 0.0 to 1.0)\n\n"
        )
        
        return summary + detailed_analysis
        
    except Exception as e:
        return f"Sentiment analysis encountered an error: {str(e)}"