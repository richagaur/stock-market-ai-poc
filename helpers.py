# helpers.py
from datetime import datetime, timezone
from typing import Any, Optional

def iso_from_ts(ts: Optional[int]) -> Optional[str]:
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    except Exception:
        return None

def first_or_none(seq):
    return seq[0] if seq else None

def try_float(s: Any) -> Optional[float]:
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    try:
        return float(str(s).strip())
    except Exception:
        return None

def clean_string(s):
    if isinstance(s, str):
        return s.replace('\n', ' ').replace('\t', ' ').replace('"', '\"').strip()
    return s
