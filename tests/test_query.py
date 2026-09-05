"""Tests for query providers and provenance-preserving results."""

from unittest.mock import MagicMock

import pytest

from labrat.query import PubTatorClient, QueryError
from labrat.query.gene import query_gene
from labrat.query.literature import query_literature
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
