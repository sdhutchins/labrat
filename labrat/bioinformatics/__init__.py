# -*- coding: utf-8 -*-
"""Bioinformatics tools and wrappers for gene and variant lookups."""

from .gene import GeneClient, get_gene_info, query_genes
from .variant import VariantClient, get_variant_info, query_variants
from .enrichment import EnrichmentClient, run_enrichment

__all__ = [
    "GeneClient",
    "VariantClient",
    "EnrichmentClient",
    "get_gene_info",
    "query_genes",
    "get_variant_info",
    "query_variants",
    "run_enrichment",
]
