"""Shared models and errors for external biological queries."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


class QueryError(RuntimeError):
    """Report a provider or input error that can be shown to a CLI user."""


@dataclass(frozen=True)
class QueryResult:
    """Retain normalized provenance alongside an unmodified provider response."""

    kind: str
    query: str
    provider: str
    retrieved_at: str
    metadata: dict[str, Any]
    data: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the query result."""
        return asdict(self)


def retrieval_timestamp() -> str:
    """Return an unambiguous UTC timestamp for result provenance."""
    return datetime.now(timezone.utc).isoformat()
