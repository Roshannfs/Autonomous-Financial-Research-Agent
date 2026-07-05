import yfinance as yf
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class CompanyProfileInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol (e.g., AAPL, MSFT)")

@tool("company_profile", args_schema=CompanyProfileInput)
def get_company_profile(ticker: str) -> dict:
    """Retrieves basic company information including sector, industry, market cap, and description."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "name": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "summary": info.get("longBusinessSummary", "N/A")
        }
    except Exception as e:
        return {"error": f"Failed to retrieve data for {ticker}: {str(e)}"}

class FinancialDataInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol (e.g., AAPL, MSFT)")

@tool("financial_data_api", args_schema=FinancialDataInput)
def get_financial_data(ticker: str) -> dict:
    """Retrieves structured financial data including key ratios and margins."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "revenue": info.get("totalRevenue", "N/A"),
            "ebitda": info.get("ebitda", "N/A"),
            "profit_margin": info.get("profitMargins", "N/A"),
            "operating_margin": info.get("operatingMargins", "N/A"),
            "debt_to_equity": info.get("debtToEquity", "N/A")
        }
    except Exception as e:
        return {"error": f"Failed to retrieve financials for {ticker}: {str(e)}"}