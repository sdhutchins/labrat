"""MyGene-backed gene queries."""

from typing import Any

import mygene

from labrat.query.models import QueryError, QueryResult, retrieval_timestamp

GENE_FIELDS = "_id,symbol,name,taxid,entrezgene,ensembl.gene,summary,uniprot,refseq"


def query_gene(
    gene: str,
    species: str = "human",
    limit: int = 5,
    client: Any | None = None,
) -> QueryResult:
    """Query MyGene while retaining its raw response and build metadata."""
    gene_client = client or mygene.MyGeneInfo()

    try:
        response = gene_client.query(
            gene,
            species=species,
            fields=GENE_FIELDS,
            size=limit,
        )
        metadata = gene_client.metadata()
    except Exception as error:
        raise QueryError(f"MyGene query failed: {error}") from error

    if not isinstance(response, dict):
        raise QueryError("MyGene returned an unexpected response.")

    return QueryResult(
        kind="gene",
        query=gene,
        provider="mygene",
        retrieved_at=retrieval_timestamp(),
        metadata={
            "build_version": metadata.get("build_version"),
            "build_date": metadata.get("build_date"),
            "species": species,
        },
        data=response,
    )
