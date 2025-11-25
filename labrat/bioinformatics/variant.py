# -*- coding: utf-8 -*-
"""Variant lookup and annotation wrapper using MyVariant.info."""

from typing import Any, Dict, List, Optional, Union

import myvariant


class VariantClient:
    """
    A wrapper client for MyVariant.info variant annotation services.

    This client provides a simplified interface for querying variant information
    from the MyVariant.info database. It supports querying by HGVS notation,
    dbSNP rsID, and other identifiers.

    Attributes:
        client: The underlying myvariant.MyVariantInfo client instance.

    Example:
        >>> client = VariantClient()
        >>> info = client.get_variant("chr7:g.140453136A>T")
        >>> print(info.get("dbsnp", {}).get("rsid"))
        rs113488022
    """

    def __init__(self) -> None:
        """Initialize the VariantClient with a MyVariant.info connection."""
        self.client = myvariant.MyVariantInfo()

    def get_variant(
        self,
        variant_id: str,
        fields: Optional[Union[str, List[str]]] = None,
        assembly: str = "hg38",
    ) -> Dict[str, Any]:
        """
        Get annotation information for a single variant.

        Args:
            variant_id: Variant identifier in HGVS notation
                (e.g., "chr7:g.140453136A>T") or dbSNP rsID (e.g., "rs113488022").
            fields: Fields to retrieve. Defaults to common fields if None.
                Can be a comma-separated string or list of field names.
                Use "all" to retrieve all available fields.
            assembly: Genome assembly version ("hg19" or "hg38").

        Returns:
            Dictionary containing variant annotation data.

        Raises:
            ValueError: If the variant is not found.

        Example:
            >>> client = VariantClient()
            >>> info = client.get_variant("rs113488022", fields="dbsnp,clinvar")
        """
        if fields is None:
            fields = [
                "dbsnp",
                "clinvar",
                "cadd",
                "gnomad_genome",
                "gnomad_exome",
            ]

        if isinstance(fields, list):
            fields = ",".join(fields)

        result = self.client.getvariant(variant_id, fields=fields, assembly=assembly)

        if result is None:
            raise ValueError(f"Variant not found: {variant_id}")

        return result

    def query(
        self,
        query: str,
        fields: Optional[Union[str, List[str]]] = None,
        size: int = 10,
        from_: int = 0,
        assembly: str = "hg38",
    ) -> Dict[str, Any]:
        """
        Query variants using a search string.

        Args:
            query: Search query string. Supports field-specific queries
                (e.g., "clinvar.rcv.clinical_significance:pathogenic").
            fields: Fields to retrieve in results.
            size: Number of results to return (max 1000).
            from_: Starting position for pagination.
            assembly: Genome assembly version.

        Returns:
            Dictionary with 'hits' containing list of matching variants
            and metadata about the query.

        Example:
            >>> client = VariantClient()
            >>> results = client.query("BRCA1", size=5)
            >>> for hit in results["hits"]:
            ...     print(hit.get("_id"))
        """
        if fields is None:
            fields = ["_id", "dbsnp.rsid", "clinvar.rcv.clinical_significance"]

        if isinstance(fields, list):
            fields = ",".join(fields)

        return self.client.query(
            query,
            fields=fields,
            size=size,
            from_=from_,
            assembly=assembly,
        )

    def get_variants(
        self,
        variant_ids: List[str],
        fields: Optional[Union[str, List[str]]] = None,
        assembly: str = "hg38",
    ) -> List[Dict[str, Any]]:
        """
        Get annotation information for multiple variants.

        Args:
            variant_ids: List of variant identifiers.
            fields: Fields to retrieve.
            assembly: Genome assembly version.

        Returns:
            List of dictionaries containing variant annotation data.

        Example:
            >>> client = VariantClient()
            >>> variants = client.get_variants(["rs113488022", "rs121913279"])
        """
        if fields is None:
            fields = ["dbsnp", "clinvar", "cadd"]

        if isinstance(fields, list):
            fields = ",".join(fields)

        return self.client.getvariants(variant_ids, fields=fields, assembly=assembly)


def get_variant_info(
    variant_id: str,
    fields: Optional[Union[str, List[str]]] = None,
    assembly: str = "hg38",
) -> Dict[str, Any]:
    """
    Convenience function to get information about a single variant.

    Args:
        variant_id: Variant identifier (HGVS notation or rsID).
        fields: Fields to retrieve.
        assembly: Genome assembly version.

    Returns:
        Dictionary containing variant annotation data.

    Example:
        >>> info = get_variant_info("rs113488022")
        >>> print(info.get("clinvar", {}).get("gene", {}).get("symbol"))
        BRAF
    """
    client = VariantClient()
    return client.get_variant(variant_id, fields=fields, assembly=assembly)


def query_variants(
    query: str,
    fields: Optional[Union[str, List[str]]] = None,
    size: int = 10,
    assembly: str = "hg38",
) -> List[Dict[str, Any]]:
    """
    Convenience function to query variants by search string.

    Args:
        query: Search query string.
        fields: Fields to retrieve.
        size: Number of results to return.
        assembly: Genome assembly version.

    Returns:
        List of matching variant records.

    Example:
        >>> variants = query_variants("BRCA1", size=5)
        >>> for var in variants:
        ...     print(var.get("_id"))
    """
    client = VariantClient()
    result = client.query(query, fields=fields, size=size, assembly=assembly)
    return result.get("hits", [])
