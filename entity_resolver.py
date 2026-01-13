# entity_resolver.py
from typing import Dict, Any, Optional, List
from helpers import clean_string, first_or_none

class EntityResolver:
    def __init__(self, container):
        self.container = container

    def resolve_stock(self, text: str) -> Optional[Dict[str, Any]]:
        text = clean_string(text)
        sql = """
        SELECT TOP 5 c.id, c.symbol, c.Company_name, c._ts 
        FROM c
        WHERE FullTextContains(c.symbol, @q) OR FullTextContains(c.Company_name,{"term": @q, "distance":2})
        """
        items = list(self.container.query_items(
            query=sql,
            parameters=[{"name": "@q", "value": text}],
            enable_cross_partition_query=True
        ))
        doc_meta = first_or_none(items)
        if not doc_meta:
            return None
        symbol = doc_meta.get("symbol")
        doc_id = doc_meta.get("id") or symbol
        try:
            full_doc = self.container.read_item(item=doc_id, partition_key=symbol)
            return full_doc
        except Exception:
            return doc_meta

    def resolve_sector(self, text: str) -> List[Dict[str, Any]]:
        print("Resolving sector for text:", text)
        text = clean_string(text)
        sql_exact = """
        SELECT TOP 10 c.id, c.symbol, c.Company_name, c._ts FROM c WHERE 
        FullTextContains(c.Sector, @s)
        """
        exact = list(self.container.query_items(
            query=sql_exact,
            parameters=[{"name": "@s", "value": text}],
            enable_cross_partition_query=True
        ))
        if exact:
            return exact
        sql_like = """
        SELECT TOP 10 c.id, c.symbol, c.Company_name, c._ts
        FROM c
        WHERE FullTextContainsAny(c.Sector, @s)
        """
        return list(self.container.query_items(
            query=sql_like,
            parameters=[{"name": "@s", "value": text}],
            enable_cross_partition_query=True
        ))
