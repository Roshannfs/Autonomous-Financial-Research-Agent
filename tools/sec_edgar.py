import requests
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.tools import tool

class SECFilingInput(BaseModel):
    ticker: str = Field(description="Stock ticker symbol (e.g., AAPL, MSFT)")
    filing_type: str = Field(description="Type of SEC filing to retrieve (10-K, 10-Q, 8-K, DEF 14A)")
    year: Optional[int] = Field(default=None, description="Filing year (defaults to most recent)")

@tool("sec_filing_search", args_schema=SECFilingInput)
def sec_filing_search(ticker: str, filing_type: str, year: int = None) -> str:
    """
    Search and retrieve SEC EDGAR filings for a publicly traded US company. 
    Use this tool when you need official regulatory disclosures including annual reports (10-K), 
    quarterly reports (10-Q), material event reports (8-K), or proxy statements (DEF 14A).
    """
    # The SEC strictly requires a User-Agent header to prevent blocking
    headers = {'User-Agent': 'QuantumEdge Research Agent (admin@quantumedge.com)'}
    
    try:
        # Step 1: Convert Ticker to SEC CIK Number
        tickers_url = "https://www.sec.gov/files/company_tickers.json"
        tickers_response = requests.get(tickers_url, headers=headers)
        tickers_response.raise_for_status()
        tickers_data = tickers_response.json()
        
        cik_str = None
        for key, value in tickers_data.items():
            if value['ticker'].upper() == ticker.upper():
                # SEC CIKs must be exactly 10 digits, zero-padded
                cik_str = str(value['cik_str']).zfill(10)
                break
                
        if not cik_str:
            return f"Error: Could not find SEC CIK for ticker {ticker}."
            
        # Step 2: Fetch the company's entire filing history
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik_str}.json"
        sub_response = requests.get(submissions_url, headers=headers)
        sub_response.raise_for_status()
        sub_data = sub_response.json()
        
        recent_filings = sub_data.get('filings', {}).get('recent', {})
        
        # Step 3: Search history for the requested filing type and year
        forms = recent_filings.get('form', [])
        dates = recent_filings.get('filingDate', [])
        accession_numbers = recent_filings.get('accessionNumber', [])
        
        for i in range(len(forms)):
            current_form = forms[i]
            current_date = dates[i]
            current_year = int(current_date.split('-')[0])
            
            if current_form == filing_type:
                if year is None or current_year == year:
                    acc_num = accession_numbers[i]
                    
                    # Note: We return metadata instead of the full text to avoid overflowing the LLM context window.
                    # In a full production RAG pipeline, the text would be routed straight to the Vector DB.
                    return (
                        f"✅ SEC Filing Confirmed:\n"
                        f"Ticker: {ticker}\n"
                        f"Filing Type: {filing_type}\n"
                        f"Filing Date: {current_date}\n"
                        f"Accession Number: {acc_num}\n"
                        f"[Note to Agent: The filing is confirmed. Use the financial_data_api tool to extract specific quantitative metrics.]"
                    )
                    
        return f"No {filing_type} filing found for {ticker} in year {year if year else 'recent history'}."

    except Exception as e:
        return f"Error fetching SEC filing: {str(e)}"