# -*- coding: utf-8 -*-
"""Gene lookup and annotation wrapper using MyGene.info."""

from typing import Any, Dict, List, Optional, Union

import mygene


class GeneClient:
    """
    A wrapper client for MyGene.info gene annotation services.

    This client provides a simplified interface for querying gene information
    from the MyGene.info database. It supports querying by gene symbol, Entrez ID,
    Ensembl ID, and other identifiers.

    Attributes:
        client: The underlying mygene.MyGeneInfo client instance.

    Example:
        >>> client = GeneClient()
        >>> info = client.get_gene("BRCA1")
        >>> print(info.get("symbol"), info.get("name"))
        BRCA1 BRCA1 DNA repair associated
    """

    def __init__(self) -> None:
        """Initialize the GeneClient with a MyGene.info connection."""
        self.client = mygene.MyGeneInfo()

    def get_gene(
        self,
        gene_id: Union[str, int],
        fields: Optional[Union[str, List[str]]] = None,
        species: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get annotation information for a single gene.

        Args:
            gene_id: Gene identifier (symbol, Entrez ID, Ensembl ID, etc.).
            fields: Fields to retrieve. Defaults to common fields if None.
                Can be a comma-separated string or list of field names.
                Use "all" to retrieve all available fields.
            species: Species filter (e.g., "human", "mouse", "9606").

        Returns:
            Dictionary containing gene annotation data.

        Raises:
            ValueError: If the gene is not found.

        Example:
            >>> client = GeneClient()
            >>> info = client.get_gene("BRCA1", fields="symbol,name,summary")
        """
        if fields is None:
            fields = ["symbol", "name", "entrezgene", "ensembl", "summary", "type_of_gene"]

        if isinstance(fields, list):
            fields = ",".join(fields)

        kwargs: Dict[str, Any] = {"fields": fields}
        if species:
            kwargs["species"] = species

        result = self.client.getgene(gene_id, **kwargs)

        if result is None:
            raise ValueError(f"Gene not found: {gene_id}")

        return result

    def query(
        self,
        query: str,
        fields: Optional[Union[str, List[str]]] = None,
        species: Optional[str] = None,
        size: int = 10,
        from_: int = 0,
    ) -> Dict[str, Any]:
        """
        Query genes using a search string.

        Args:
            query: Search query string. Supports field-specific queries
                (e.g., "symbol:BRCA*", "go:0000001").
            fields: Fields to retrieve in results.
            species: Species filter.
            size: Number of results to return (max 1000).
            from_: Starting position for pagination.

        Returns:
            Dictionary with 'hits' containing list of matching genes
            and metadata about the query.

        Example:
            >>> client = GeneClient()
            >>> results = client.query("BRCA", species="human", size=5)
            >>> for hit in results["hits"]:
            ...     print(hit.get("symbol"))
        """
        if fields is None:
            fields = ["symbol", "name", "entrezgene", "taxid"]

        if isinstance(fields, list):
            fields = ",".join(fields)

        kwargs: Dict[str, Any] = {
            "fields": fields,
            "size": size,
            "from_": from_,
        }
        if species:
            kwargs["species"] = species

        return self.client.query(query, **kwargs)

    def get_genes(
        self,
        gene_ids: List[Union[str, int]],
        fields: Optional[Union[str, List[str]]] = None,
        species: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get annotation information for multiple genes.

        Args:
            gene_ids: List of gene identifiers.
            fields: Fields to retrieve.
            species: Species filter.

        Returns:
            List of dictionaries containing gene annotation data.

        Example:
            >>> client = GeneClient()
            >>> genes = client.get_genes(["BRCA1", "BRCA2", "TP53"])
        """
        if fields is None:
            fields = ["symbol", "name", "entrezgene", "ensembl", "summary"]

        if isinstance(fields, list):
            fields = ",".join(fields)

        kwargs: Dict[str, Any] = {"fields": fields}
        if species:
            kwargs["species"] = species

        return self.client.getgenes(gene_ids, **kwargs)


def get_gene_info(
    gene_id: Union[str, int],
    fields: Optional[Union[str, List[str]]] = None,
    species: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function to get information about a single gene.

    Args:
        gene_id: Gene identifier (symbol, Entrez ID, Ensembl ID, etc.).
        fields: Fields to retrieve.
        species: Species filter.

    Returns:
        Dictionary containing gene annotation data.

    Example:
        >>> info = get_gene_info("BRCA1", species="human")
        >>> print(info.get("name"))
        BRCA1 DNA repair associated
    """
    client = GeneClient()
    return client.get_gene(gene_id, fields=fields, species=species)


def query_genes(
    query: str,
    fields: Optional[Union[str, List[str]]] = None,
    species: Optional[str] = None,
    size: int = 10,
) -> List[Dict[str, Any]]:
    """
    Convenience function to query genes by search string.

    Args:
        query: Search query string.
        fields: Fields to retrieve.
        species: Species filter.
        size: Number of results to return.

    Returns:
        List of matching gene records.

    Example:
        >>> genes = query_genes("kinase", species="human", size=5)
        >>> for gene in genes:
        ...     print(gene.get("symbol"), gene.get("name"))
    """
    client = GeneClient()
    result = client.query(query, fields=fields, species=species, size=size)
    return result.get("hits", [])
