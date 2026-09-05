"""MyVariant-backed variant queries."""

import re
from typing import Any

import myvariant

from labrat.query.models import QueryError, QueryResult, retrieval_timestamp

VARIANT_FIELDS = "_id,dbsnp.rsid,clinvar,cadd.phred,gnomad_exome.af,gnomad_genome.af"
RSID_PATTERN = re.compile(r"^rs\d+$", flags=re.IGNORECASE)


def query_variant(
    variant: str,
    limit: int = 5,
    client: Any | None = None,
) -> QueryResult:
    """Query MyVariant while retaining its raw response and source metadata."""
    variant_client = client or myvariant.MyVariantInfo()
    # A fielded rsID query excludes fuzzy hits without the requested dbSNP record.
    provider_query = (
        f"dbsnp.rsid:{variant}" if RSID_PATTERN.fullmatch(variant) else variant
    )

    try:
        response = variant_client.query(
            provider_query,
            fields=VARIANT_FIELDS,
            size=limit,
        )
        metadata = variant_client.metadata()
    except Exception as error:
        raise QueryError(f"MyVariant query failed: {error}") from error

    if not isinstance(response, dict):
        raise QueryError("MyVariant returned an unexpected response.")

    # Source releases can predate the aggregate build, so retain them separately.
    source_metadata = metadata.get("src", {})
    return QueryResult(
        kind="variant",
        query=variant,
        provider="myvariant",
        retrieved_at=retrieval_timestamp(),
        metadata={
            "build_version": metadata.get("build_version"),
            "build_date": metadata.get("build_date"),
            "provider_query": provider_query,
            "primary_assembly": "hg19",
            "sources": {
                source: source_metadata.get(source)
                for source in ("clinvar", "dbsnp", "gnomad")
                if source in source_metadata
            },
        },
        data=response,
    )
