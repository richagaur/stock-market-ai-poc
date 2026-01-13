from typing import Dict, Any, Optional, List
from pydantic import BaseModel

# ---------- Models ----------
class V1Results(BaseModel):
    symbol: str
    name: str
    metric_requested: Optional[str] = None
    value: Optional[Any] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    last_updated: Optional[str] = None
    overview: Optional[Dict[str, Any]] = None
    constituents: Optional[List[Dict[str, Any]]] = None

class V1Response(BaseModel):
    query_type: str
    results: V1Results
    response_time_ms: int