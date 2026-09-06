"""Tests for query providers and provenance-preserving results."""

from collections.abc import Callable
from datetime import datetime
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest

from labrat.query import PubTatorClient, QueryError
from labrat.query.gene import query_gene
from labrat.query.literature import query_literature
from labrat.query.models import QueryResult, retrieval_timestamp
from labrat.query.variant import query_variant


def test_query_gene_retains_results_and_build_metadata() -> None:
    """A gene query should keep both annotations and their database build."""
    client = MagicMock()
    client.query.return_value = {
        "total": 1,
        "hits": [{"_id": "659", "symbol": "BMPR2", "taxid": 9606}],
    }
    client.metadata.return_value = {
        "build_version": "20260830",
        "build_date": "2026-08-30T07:00:01-07:00",
    }

    result = query_gene("BMPR2", client=client)

    assert result.provider == "mygene"
    assert result.metadata["build_version"] == "20260830"
    assert result.data["hits"][0]["symbol"] == "BMPR2"
    client.query.assert_called_once()


def test_query_variant_retains_source_versions() -> None:
    """A variant query should expose source versions that may differ in age."""
    client = MagicMock()
    client.query.return_value = {
        "total": 1,
        "hits": [{"_id": "chr19:g.44908684T>C", "dbsnp": {"rsid": "rs429358"}}],
    }
    client.metadata.return_value = {
        "build_version": "20250624",
        "src": {
            "clinvar": {"version": "2025-05"},
            "gnomad": {"version": "2.1"},
            "unrequested_source": {"version": "1"},
        },
    }

    result = query_variant("rs429358", client=client)

    assert result.provider == "myvariant"
    assert result.metadata["sources"] == {
        "clinvar": {"version": "2025-05"},
        "gnomad": {"version": "2.1"},
    }
    assert result.data["hits"][0]["dbsnp"]["rsid"] == "rs429358"
    client.query.assert_called_once_with(
        "dbsnp.rsid:rs429358",
        fields=(
            "_id,dbsnp.rsid,clinvar,cadd.phred,gnomad_exome.af," "gnomad_genome.af"
        ),
        size=5,
    )
    assert result.metadata["primary_assembly"] == "hg19"


def test_query_literature_uses_free_text() -> None:
    """Free-text searches should pass through without entity rewriting."""
    client = MagicMock(spec=PubTatorClient)
    client.search.return_value = {
        "results": [
            {"pmid": 34023242, "title": "Significance of BMPR2 mutations"},
            {"pmid": 36603064, "title": "BMPR2 Mutation and Metabolism"},
        ]
    }

    result = query_literature(
        search_text="BMPR2 pulmonary arterial hypertension",
        limit=1,
        client=client,
    )

    assert result.query == "BMPR2 pulmonary arterial hypertension"
    assert len(result.data["results"]) == 2
    assert result.metadata["display_limit"] == 1
    client.search.assert_called_once_with(
        "BMPR2 pulmonary arterial hypertension",
        page=1,
    )


def test_query_literature_resolves_structured_entities() -> None:
    """Structured searches should use PubTator's normalized identifiers."""
    client = MagicMock(spec=PubTatorClient)
    client.autocomplete.side_effect = [
        [{"_id": "@GENE_BMPR2", "name": "BMPR2"}],
        [
            {
                "_id": "@DISEASE_Pulmonary_Arterial_Hypertension",
                "name": "Pulmonary Arterial Hypertension",
            }
        ],
    ]
    client.search.return_value = {"results": []}

    result = query_literature(
        entities={
            "gene": "BMPR2",
            "disease": "pulmonary arterial hypertension",
        },
        client=client,
    )

    expected_query = "@GENE_BMPR2 AND @DISEASE_Pulmonary_Arterial_Hypertension"
    assert result.query == expected_query
    client.search.assert_called_once_with(expected_query, page=1)


def test_query_literature_builds_relation_query() -> None:
    """Relation searches should require two resolved biological entities."""
    client = MagicMock(spec=PubTatorClient)
    client.autocomplete.side_effect = [
        [{"_id": "@GENE_BMPR2", "name": "BMPR2"}],
        [
            {
                "_id": "@DISEASE_Pulmonary_Arterial_Hypertension",
                "name": "Pulmonary Arterial Hypertension",
            }
        ],
    ]
    client.search.return_value = {"results": []}

    result = query_literature(
        entities={
            "gene": "BMPR2",
            "disease": "pulmonary arterial hypertension",
        },
        relation="associate",
        client=client,
    )

    assert result.query == (
        "relations:associate|@GENE_BMPR2|" "@DISEASE_Pulmonary_Arterial_Hypertension"
    )


def test_query_literature_rejects_ambiguous_entity() -> None:
    """Ambiguous concepts should be reported instead of chosen silently."""
    client = MagicMock(spec=PubTatorClient)
    client.autocomplete.return_value = [
        {"_id": "@GENE_BMPR2A", "name": "bmpr2a"},
        {"_id": "@GENE_BMPR2B", "name": "bmpr2b"},
    ]

    with pytest.raises(QueryError, match="ambiguous gene"):
        query_literature(entities={"gene": "BMPR2"}, client=client)


def test_query_literature_rejects_mixed_query_modes() -> None:
    """Mixed free-text and semantic inputs need an explicit future contract."""
    client = MagicMock(spec=PubTatorClient)

    with pytest.raises(QueryError, match="either free text"):
        query_literature(
            search_text="BMPR2",
            entities={"gene": "BMPR2"},
            client=client,
        )


@pytest.mark.parametrize(
    ("query_function", "query", "error_message"),
    [
        (query_gene, "BMPR2", "MyGene query failed"),
        (query_variant, "rs429358", "MyVariant query failed"),
    ],
)
def test_query_providers_translate_client_errors(
    query_function: Callable[..., QueryResult],
    query: str,
    error_message: str,
) -> None:
    """Provider failures should become consistent errors for CLI callers."""
    client = MagicMock()
    client.query.side_effect = RuntimeError("provider unavailable")

    with pytest.raises(QueryError, match=error_message):
        query_function(query, client=client)


@pytest.mark.parametrize(
    ("query_function", "query", "error_message"),
    [
        (query_gene, "BMPR2", "MyGene returned an unexpected response"),
        (query_variant, "rs429358", "MyVariant returned an unexpected response"),
    ],
)
def test_query_providers_reject_malformed_responses(
    query_function: Callable[..., QueryResult],
    query: str,
    error_message: str,
) -> None:
    """Non-object responses should fail before result provenance is assembled."""
    client = MagicMock()
    client.query.return_value = []
    client.metadata.return_value = {}

    with pytest.raises(QueryError, match=error_message):
        query_function(query, client=client)


def test_query_variant_preserves_literal_variant_query() -> None:
    """HGVS-style variants should pass through without rsID field rewriting."""
    client = MagicMock()
    client.query.return_value = {"total": 0, "hits": []}
    client.metadata.return_value = {"src": {}}

    result = query_variant("chr19:g.44908684T>C", client=client)

    assert result.metadata["provider_query"] == "chr19:g.44908684T>C"
    client.query.assert_called_once_with(
        "chr19:g.44908684T>C",
        fields=(
            "_id,dbsnp.rsid,clinvar,cadd.phred,gnomad_exome.af,"
            "gnomad_genome.af"
        ),
        size=5,
    )


def test_pubtator_client_builds_request_and_respects_rate_limit() -> None:
    """Consecutive PubTator requests should retain parameters and throttle."""
    client = PubTatorClient("https://example.test/")
    client._last_request_at = 10.0
    response_context = MagicMock()
    response_context.__enter__.return_value = MagicMock()

    with (
        patch(
            "labrat.query.literature.time.monotonic",
            side_effect=[10.1, 10.2],
        ),
        patch("labrat.query.literature.time.sleep") as sleep,
        patch(
            "labrat.query.literature.urlopen",
            return_value=response_context,
        ) as urlopen,
        patch(
            "labrat.query.literature.json.load",
            return_value={"results": []},
        ),
    ):
        result = client.search("BMPR2 PAH", page=2)

    request = urlopen.call_args.args[0]
    assert result == {"results": []}
    assert request.full_url == (
        "https://example.test/search/?text=BMPR2+PAH&page=2"
    )
    assert request.get_header("User-agent") == "pylabrat literature query"
    sleep.assert_called_once_with(pytest.approx((1 / 3) - 0.1))


def test_pubtator_client_translates_transport_errors() -> None:
    """Transport errors should retain a stable package-level exception type."""
    client = PubTatorClient()

    with (
        patch("labrat.query.literature.time.monotonic", return_value=10.0),
        patch(
            "labrat.query.literature.urlopen",
            side_effect=URLError("offline"),
        ),
        pytest.raises(QueryError, match="PubTator 3 request failed"),
    ):
        client.search("BMPR2")


def test_pubtator_client_rejects_invalid_response_shapes() -> None:
    """Endpoint-specific response types should be validated consistently."""
    client = PubTatorClient()
    client._get_json = MagicMock(side_effect=[{}, []])

    with pytest.raises(QueryError, match="invalid autocomplete data"):
        client.autocomplete("BMPR2", "gene")

    with pytest.raises(QueryError, match="invalid search data"):
        client.search("BMPR2")


@pytest.mark.parametrize(
    ("arguments", "error_message"),
    [
        ({}, "Provide search text"),
        (
            {"search_text": "BMPR2", "relation": "associate"},
            "requires structured entity options",
        ),
    ],
)
def test_query_literature_validates_input_modes(
    arguments: dict[str, str],
    error_message: str,
) -> None:
    """Incomplete query modes should fail before contacting PubTator."""
    client = MagicMock(spec=PubTatorClient)

    with pytest.raises(QueryError, match=error_message):
        query_literature(client=client, **arguments)

    client.search.assert_not_called()


def test_query_literature_rejects_unresolved_entity() -> None:
    """An entity with no PubTator matches should retain its input label."""
    client = MagicMock(spec=PubTatorClient)
    client.autocomplete.return_value = []

    with pytest.raises(QueryError, match="could not resolve gene 'BMPR2'"):
        query_literature(entities={"gene": "BMPR2"}, client=client)


def test_query_literature_requires_two_relation_entities() -> None:
    """Relation syntax should require two normalized biological endpoints."""
    client = MagicMock(spec=PubTatorClient)
    client.autocomplete.return_value = [{"_id": "@GENE_BMPR2", "name": "BMPR2"}]

    with pytest.raises(QueryError, match="exactly two entities"):
        query_literature(
            entities={"gene": "BMPR2"},
            relation="associate",
            client=client,
        )


def test_query_literature_rejects_invalid_results() -> None:
    """Literature results should remain a list before presentation limits apply."""
    client = MagicMock(spec=PubTatorClient)
    client.search.return_value = {"results": {"pmid": 34023242}}

    with pytest.raises(QueryError, match="invalid literature results"):
        query_literature(search_text="BMPR2", client=client)


def test_query_result_serializes_with_utc_timestamp() -> None:
    """Query results should provide JSON-ready provenance with a UTC offset."""
    retrieved_at = retrieval_timestamp()
    result = QueryResult(
        kind="gene",
        query="BMPR2",
        provider="mygene",
        retrieved_at=retrieved_at,
        metadata={"species": "human"},
        data={"hits": []},
    )

    assert result.to_dict() == {
        "kind": "gene",
        "query": "BMPR2",
        "provider": "mygene",
        "retrieved_at": retrieved_at,
        "metadata": {"species": "human"},
        "data": {"hits": []},
    }
    assert datetime.fromisoformat(retrieved_at).utcoffset().total_seconds() == 0
