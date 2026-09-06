"""PubTator 3 literature and semantic entity queries."""

import json
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from labrat.query.models import QueryError, QueryResult, retrieval_timestamp

PUBTATOR_API_URL = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api"
REQUEST_INTERVAL_SECONDS = 1 / 3


class PubTatorClient:
    """Access the documented PubTator 3 search and autocomplete endpoints."""

    def __init__(self, base_url: str = PUBTATOR_API_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self._last_request_at: float | None = None

    def _get_json(self, endpoint: str, parameters: dict[str, Any]) -> Any:
        if self._last_request_at is not None:
            # Monotonic time keeps rate limiting stable if wall-clock time changes.
            elapsed = time.monotonic() - self._last_request_at
            if elapsed < REQUEST_INTERVAL_SECONDS:
                # NCBI asks PubTator clients to stay at or below three requests/s.
                time.sleep(REQUEST_INTERVAL_SECONDS - elapsed)

        request_url = f"{self.base_url}/{endpoint}/?{urlencode(parameters)}"
        request = Request(
            request_url,
            headers={"User-Agent": "pylabrat literature query"},
        )

        try:
            self._last_request_at = time.monotonic()
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            raise QueryError(f"PubTator 3 request failed: {error}") from error

    def autocomplete(
        self,
        query: str,
        concept: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Return PubTator concepts matching one biological entity."""
        response = self._get_json(
            "entity/autocomplete",
            {"query": query, "concept": concept, "limit": limit},
        )
        if not isinstance(response, list):
            raise QueryError("PubTator 3 returned invalid autocomplete data.")
        return response

    def search(self, query: str, page: int = 1) -> dict[str, Any]:
        """Return one relevance-ranked PubTator search result page."""
        response = self._get_json("search", {"text": query, "page": page})
        if not isinstance(response, dict):
            raise QueryError("PubTator 3 returned invalid search data.")
        return response


def _resolve_entity(
    client: PubTatorClient,
    entity_type: str,
    value: str,
) -> dict[str, Any]:
    matches = client.autocomplete(value, entity_type)
    # An exact normalized name prevents silently choosing the first autocomplete hit.
    exact_matches = [
        match
        for match in matches
        if str(match.get("name", "")).casefold() == value.casefold()
    ]

    if len(exact_matches) == 1:
        return exact_matches[0]
    if not matches:
        raise QueryError(f"PubTator 3 could not resolve {entity_type} '{value}'.")

    choices = ", ".join(str(match.get("name", "unknown")) for match in matches[:5])
    raise QueryError(
        f"PubTator 3 returned ambiguous {entity_type} '{value}': {choices}."
    )


def _semantic_query(
    client: PubTatorClient,
    entities: dict[str, str],
    relation: str | None,
) -> tuple[str, list[dict[str, Any]]]:
    resolved_entities = [
        _resolve_entity(client, entity_type, value)
        for entity_type, value in entities.items()
    ]
    identifiers = [str(entity["_id"]) for entity in resolved_entities]

    # PubTator relation syntax accepts exactly two normalized concept endpoints.
    if relation is not None:
        if len(identifiers) != 2:
            raise QueryError("A relation search requires exactly two entities.")
        return (
            f"relations:{relation}|{identifiers[0]}|{identifiers[1]}",
            resolved_entities,
        )

    return " AND ".join(identifiers), resolved_entities


def query_literature(
    search_text: str | None = None,
    entities: dict[str, str] | None = None,
    relation: str | None = None,
    page: int = 1,
    limit: int = 10,
    client: PubTatorClient | None = None,
) -> QueryResult:
    """Search PubTator using either free text or normalized biological entities."""
    literature_client = client or PubTatorClient()
    requested_entities = entities or {}

    if search_text and requested_entities:
        raise QueryError("Use either free text or structured entity options, not both.")
    if not search_text and not requested_entities:
        raise QueryError("Provide search text or at least one structured entity.")
    if relation and not requested_entities:
        raise QueryError("A relation search requires structured entity options.")

    resolved_entities: list[dict[str, Any]] = []
    provider_query = search_text
    if requested_entities:
        provider_query, resolved_entities = _semantic_query(
            literature_client,
            requested_entities,
            relation,
        )

    if provider_query is None:
        raise QueryError("Could not construct a PubTator 3 query.")

    response = literature_client.search(provider_query, page=page)
    results = response.get("results", [])
    if not isinstance(results, list):
        raise QueryError("PubTator 3 returned invalid literature results.")

    # Keep the complete PubTator page; the limit affects terminal presentation only.
    return QueryResult(
        kind="literature",
        query=provider_query,
        provider="pubtator3",
        retrieved_at=retrieval_timestamp(),
        metadata={
            "api_version": "3.0",
            "page": page,
            "display_limit": limit,
            "resolved_entities": resolved_entities,
            "relation": relation,
        },
        data=response,
    )
