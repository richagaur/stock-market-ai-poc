# response_builders.py
import math
import time
from typing import Dict, Any, List
from helpers import iso_from_ts
from models import V1Response, V1Results

def build_stock_metric_response(doc: Dict[str, Any], metric_field: str, start_ns: int) -> V1Response:
    symbol = doc.get("symbol") or doc.get("id")
    name = doc.get("Company_name")
    val = doc.get(metric_field)
    change = None
    change_percent = None
    last_updated = iso_from_ts(doc.get("_ts"))
    elapsed_ms = math.ceil((time.time_ns() - start_ns) / 1_000_000)
    return V1Response(
        query_type="stock_metric",
        results=V1Results(
            symbol=symbol,
            name=name,
            metric_requested=metric_field,
            value=val,
            change=change,
            change_percent=change_percent,
            last_updated=last_updated
        ),
        response_time_ms=elapsed_ms,
    )

def build_stock_overview_response(doc: Dict[str, Any], start_ns: int) -> V1Response:
    symbol = doc.get("symbol") or doc.get("id")
    name = doc.get("Company_name")
    last_updated = iso_from_ts(doc.get("_ts"))
    elapsed_ms = math.ceil((time.time_ns() - start_ns) / 1_000_000)
    overview = {
        "Market Cap": doc.get("Market Cap"),
        "Current Price": doc.get("Current Price"),
        "High / Low": doc.get("High / Low"),
        "Stock P/E": doc.get("Stock P/E"),
        "ROE": doc.get("ROE"),
        "ROCE": doc.get("ROCE"),
        "EPS": doc.get("EPS"),
        "Dividend Yield": doc.get("Dividend Yield"),
        "Sector": doc.get("Sector")
    }
    return V1Response(
        query_type="stock_only",
        results=V1Results(
            symbol=symbol,
            name=name,
            last_updated=last_updated,
            overview=overview
        ),
        response_time_ms=elapsed_ms
    )

def build_sector_response(rows: List[Dict[str, Any]], sector_text: str, start_ns: int) -> V1Response:
    elapsed_ms = math.ceil((time.time_ns() - start_ns) / 1_000_000)
    constituents = []
    for r in rows:
        constituents.append({
            "symbol": r.get("symbol") or r.get("id"),
            "name": r.get("Company_name"),
            "last_updated": iso_from_ts(r.get("_ts"))
        })
    return V1Response(
        query_type="sector_index",
        results=V1Results(
            symbol="",
            name=sector_text,
            constituents=constituents
        ),
        response_time_ms=elapsed_ms
    )
