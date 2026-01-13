# app_v1.py
import time
from fastapi import FastAPI, HTTPException, Query
from models import V1Response, V1Results
from db import get_cosmos_container
from entity_resolver import EntityResolver
from user_query_parsing import detect_query_type, extract_metric_key, extract_entity_text
from response_builders import build_stock_metric_response, build_stock_overview_response, build_sector_response

container = get_cosmos_container()

app = FastAPI(title="V1 Text Search for Stocks")

# ---------- Main Endpoint ----------
@app.get("/v1/search", response_model=V1Response)
def v1_search(q: str = Query(..., description="User query, e.g., 'Basilic PE', 'Basilic', 'Entertainment sector'")):
    start_ns = time.time_ns()
    qtype = detect_query_type(q)
    
    entity_resolver = EntityResolver(container)

    if qtype == "stock_metric":
        metric_info = extract_metric_key(q)
        if not metric_info:
            raise HTTPException(status_code=400, detail="No known metric in query (V1).")
        metric_alias, metric_field = metric_info
        entity_text = extract_entity_text(q, metric_alias)
        doc = entity_resolver.resolve_stock(entity_text)
        if not doc:
            raise HTTPException(status_code=404, detail=f"No stock found for '{entity_text}'.")
        resp = build_stock_metric_response(doc, metric_field, start_ns)
        return resp

    elif qtype == "stock_only":
        doc = entity_resolver.resolve_stock(q)
        if not doc:
            raise HTTPException(status_code=404, detail=f"No stock found for '{q}'.")
        resp = build_stock_overview_response(doc, start_ns)
        return resp

    elif qtype == "sector":
        # Strip 'sector' word for fuzzy resolution
        entity_text = extract_entity_text(q, metric_alias=None)
        print("Entity text for sector resolution:", entity_text)
        rows = entity_resolver.resolve_sector(entity_text or q)
        if not rows:
            raise HTTPException(status_code=404, detail=f"No constituents found for sector '{entity_text or q}'.")
        resp = build_sector_response(rows, sector_text=(entity_text or q), start_ns=start_ns)
        return resp

    # Fallback (should not hit)
    raise HTTPException(status_code=400, detail="Unsupported query type in V1.")
