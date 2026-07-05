from typing import Dict, Any

class QueryAnalyzer:
    def __init__(self):
        self.banking_keywords = ["bank", "banks", "banking", "fed", "rate", "yield", "macro"]
        self.tech_keywords = ["cloud", "software", "semiconductor", "ai", "hardware", "chip", "microsoft", "nvidia", "apple"]

    def analyze_query(self, query: str) -> Dict[str, Any]:
        cleaned_query = query.lower()
        words = cleaned_query.split()
        
        potential_tickers = [w.strip("?,.!") for w in query.split() if w.isupper() and len(w) <= 5]
        
        is_banking = any(kw in words for kw in self.banking_keywords)
        is_tech = any(kw in words for kw in self.tech_keywords)
        
        category = "General"
        if is_banking:
            category = "Banking/Macro"
        elif is_tech:
            category = "Technology"

        # FIX: If the query names explicit mega-cap companies, it is NOT ambiguous
        has_explicit_target = "microsoft" in cleaned_query or "nvidia" in cleaned_query or "apple" in cleaned_query
        is_ambiguous = len(potential_tickers) == 0 and not has_explicit_target
        
        return {
            "original_query": query,
            "category": category,
            "extracted_tickers": potential_tickers,
            "is_ambiguous": is_ambiguous,
            "complexity_score": "High" if is_ambiguous or len(potential_tickers) > 2 else "Standard"
        }