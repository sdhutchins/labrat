"""Tests for readable, scientifically qualified terminal output."""

from io import StringIO

from rich.console import Console

from labrat.query.models import QueryResult
from labrat.query.render import render_query_result


def _render(result: QueryResult) -> str:
    output = StringIO()
    console = Console(
        file=output,
        color_system=None,
        highlight=False,
        width=100,
    )
    render_query_result(result, console=console)
    return output.getvalue()


def test_render_highest_ranked_gene_and_alternatives_notice() -> None:
    """Gene output should explain ranking and preserve access to alternatives."""
    result = QueryResult(
        kind="gene",
        query="BMPR2",
        provider="mygene",
        retrieved_at="2026-09-04T12:00:00+00:00",
        metadata={"build_version": "20260830", "species": "human"},
        data={
            "hits": [
                {
                    "_id": "657",
                    "_score": 1.2171311,
                    "symbol": "BMPR1A",
                    "name": "bone morphogenetic protein receptor type 1A",
                },
                {
                    "_id": "659",
                    "_score": 144.19098,
                    "symbol": "BMPR2",
                    "name": "bone morphogenetic protein receptor type 2",
                    "taxid": 9606,
                    "ensembl": {"gene": "ENSG00000204217"},
                    "uniprot": {"Swiss-Prot": "Q13873"},
                    "refseq": {
                        "rna": ["NM_001204.7", "NM_033346.3"],
                        "protein": ["NP_001195.2", "NP_203132.1"],
                    },
                    "summary": "A receptor in the BMP signaling pathway.",
                },
            ]
        },
    )

    output = _render(result)

    assert "Highest-ranked MyGene match · BMPR2" in output
    assert "ENSG00000204217" in output
    assert "Q13873" in output
    assert "A receptor in the BMP signaling pathway." in output
    assert "MyGene score 144.19098" in output
    assert "1 additional match returned" in output
    assert "BMPR1A" not in output


def test_render_all_gene_matches() -> None:
    """The optional alternatives table should include lower MyGene scores."""
    result = QueryResult(
        kind="gene",
        query="BMPR2",
        provider="mygene",
        retrieved_at="2026-09-04T12:00:00+00:00",
        metadata={"species": "human"},
        data={
            "hits": [
                {"_id": "659", "_score": 10.0, "symbol": "BMPR2"},
                {"_id": "657", "_score": 1.2, "symbol": "BMPR1A"},
            ]
        },
    )
    output = StringIO()
    console = Console(file=output, color_system=None, width=100)

    render_query_result(result, console=console, show_all_gene_matches=True)

    rendered_output = output.getvalue()
    assert "Additional MyGene matches" in rendered_output
    assert "BMPR1A" in rendered_output
    assert "1.2" in rendered_output


def test_render_variant_annotations() -> None:
    """Variant panels should expose useful annotations without merging labels."""
    result = QueryResult(
        kind="variant",
        query="rs429358",
        provider="myvariant",
        retrieved_at="2026-09-04T12:00:00+00:00",
        metadata={"build_version": "20250624", "primary_assembly": "hg19"},
        data={
            "hits": [
                {
                    "_id": "chr19:g.45411941T>C",
                    "dbsnp": {"rsid": "rs429358"},
                    "clinvar": {
                        "gene": {"symbol": "APOE"},
                        "rcv": [
                            {"clinical_significance": "risk factor"},
                            {"clinical_significance": "drug response"},
                        ],
                    },
                    "cadd": {"phred": 0.007},
                    "gnomad_exome": {"af": {"af": 0.138498}},
                    "gnomad_genome": {"af": {"af": 0.164436}},
                }
            ]
        },
    )

    output = _render(result)

    assert "chr19:g.45411941T>C" in output
    assert "APOE" in output
    assert "risk factor, drug response" in output
    assert "0.138498" in output
    assert "ClinVar labels are condition-specific" in output
    assert "primary coordinates: hg19" in output


def test_render_literature_citation() -> None:
    """Literature tables should retain enough metadata to identify each paper."""
    result = QueryResult(
        kind="literature",
        query="BMPR2 pulmonary arterial hypertension",
        provider="pubtator3",
        retrieved_at="2026-09-04T12:00:00+00:00",
        metadata={"display_limit": 1},
        data={
            "results": [
                {
                    "pmid": 34023242,
                    "title": "Significance of BMPR2 mutations in PAH",
                    "authors": ["Tatius B", "Wasityastuti W"],
                    "journal": "Respir Investig",
                    "meta_date_publication": "2021 Jul",
                    "doi": "10.1016/j.resinv.2021.03.011",
                }
            ]
        },
    )

    output = _render(result)

    assert "Significance of BMPR2 mutations in PAH" in output
    assert "Tatius B, Wasityastuti W" in output
    assert "PMID: 34023242" in output
    assert "10.1016/j.resinv.2021.03.011" in output
