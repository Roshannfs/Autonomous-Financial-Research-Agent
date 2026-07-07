import yfinance as yf
import urllib.request
import urllib.parse
import json
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# 1. Company Profile Tool
# ---------------------------------------------------------
class CompanyProfileInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol (e.g., AAPL, MSFT)")

@tool("company_profile", args_schema=CompanyProfileInput)
def company_profile(ticker: str) -> dict:
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

# Legacy alias for backward compatibility
get_company_profile = company_profile


# ---------------------------------------------------------
# 2. Financial Data API (Legacy Tool)
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# 3. Financial Ratios Tool (New Target Tool)
# ---------------------------------------------------------
class FinancialRatiosInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol (e.g., AAPL, MSFT)")

@tool("financial_ratios", args_schema=FinancialRatiosInput)
def financial_ratios(ticker: str) -> dict:
    """Retrieves key financial ratios for a given company including P/E, PEG, debt-to-equity, and profit margins."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "pe_ratio": info.get("forwardPE", "N/A"),
            "peg_ratio": info.get("pegRatio", "N/A"),
            "price_to_book": info.get("priceToBook", "N/A"),
            "debt_to_equity": info.get("debtToEquity", "N/A"),
            "return_on_equity": info.get("returnOnEquity", "N/A"),
            "profit_margin": info.get("profitMargins", "N/A"),
            "operating_margin": info.get("operatingMargins", "N/A")
        }
    except Exception as e:
        return {"error": f"Failed to retrieve financial ratios for {ticker}: {str(e)}"}


# ---------------------------------------------------------
# 4. Ticker Resolver Tool (New Target Tool)
# ---------------------------------------------------------
class TickerResolverInput(BaseModel):
    company_name: str = Field(description="The company name to resolve to a stock ticker (e.g., 'Apple', 'NVIDIA')")

@tool("ticker_resolver", args_schema=TickerResolverInput)
def ticker_resolver(company_name: str) -> str:
    """Resolves a company name to its corresponding stock ticker symbol."""
    mapping = {
        "apple": "AAPL",
        "microsoft": "MSFT",
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "amazon": "AMZN",
        "tesla": "TSLA",
        "nvidia": "NVDA",
        "meta": "META",
        "netflix": "NFLX",
        "berkshire": "BRK.A",
        "jpmorgan": "JPM",
        "visa": "V",
        "johnson & johnson": "JNJ",
        "walmart": "WMT"
    }
    cleaned = company_name.lower().strip()
    for key, ticker in mapping.items():
        if key in cleaned or cleaned in key:
            return f"Ticker symbol for {company_name}: {ticker}"
    
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={urllib.parse.quote(company_name)}"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get("quotes"):
                best_match = data["quotes"][0]
                symbol = best_match.get("symbol")
                name = best_match.get("shortname", best_match.get("longname", company_name))
                return f"Ticker symbol for {name}: {symbol}"
    except Exception:
        pass
        
    return f"Could not automatically resolve ticker for '{company_name}'."