# query_parsing.py
from typing import Optional, Tuple

METRIC_ALIASES = {
    "price": "Current Price",
    "close": "Current Price",
    "pe": "Stock P/E",
    "p/e": "Stock P/E",
    "marketcap": "Market Cap",
    "market cap": "Market Cap",
    "roe": "ROE",
    "roce": "ROCE",
    "eps": "EPS",
    "dividend": "Dividend Yield",
    "yield": "Dividend Yield",
    "book": "Book Value",
    "book value": "Book Value",
    "ps": "Price to Sales",
    "price to sales": "Price to Sales",
    "profit growth": "Profit growth",
    "sales growth": "Sales growth",
    "high/low": "High / Low",
    "high": "High / Low",
    "low": "High / Low"
}

def detect_query_type(q: str) -> str:
    ql = q.lower().strip()
    if "sector" in ql:
        return "sector"
    metric_keys = sorted(METRIC_ALIASES.keys(), key=len, reverse=True)
    has_metric = any(m in ql for m in metric_keys)
    if any(x in ql for x in ["nifty", "bank stocks", "it sector", "fmcg sector"]):
        return "sector"
    return "stock_metric" if has_metric else "stock_only"

def extract_metric_key(q: str) -> Optional[Tuple[str, str]]:
    ql = q.lower()
    for alias, field in METRIC_ALIASES.items():
        if alias in ql:
            return alias, field
    return None

def extract_entity_text(q: str, metric_alias: Optional[str]) -> str:
    ql = q.lower()
    entity = ql
    if metric_alias:
        entity = entity.replace(metric_alias, "").strip()
    for w in ["pe", "p/e", "price", "roe", "roce", "eps", "dividend", "yield", "sector", "stocks"]:
        entity = entity.replace(w, "").strip()
    return entity.strip() or q.strip()
