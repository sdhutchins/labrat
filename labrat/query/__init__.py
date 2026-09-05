"""Query public gene, variant, and biomedical literature resources."""

from labrat.query.gene import query_gene
from labrat.query.models import QueryError, QueryResult
from labrat.query.variant import query_variant

__all__ = [
    "QueryError",
    "QueryResult",
    "query_gene",
    "query_variant",
]
