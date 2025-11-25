# -*- coding: utf-8 -*-
"""Gene set enrichment analysis wrapper using Enrichr and GSEApy."""

from typing import Any, Dict, List, Optional, Union

import gseapy as gp
import pandas as pd


class EnrichmentClient:
    """
    A wrapper client for gene set enrichment analysis.

    This client provides a simplified interface for running enrichment analysis
    using Enrichr via the GSEApy library. It supports multiple gene set libraries
    and organisms.

    Attributes:
        organism: The organism to use for analysis.

    Example:
        >>> client = EnrichmentClient()
        >>> results = client.enrichr(["BRCA1", "BRCA2", "TP53"])
        >>> print(results.head())
    """

    # Common gene set libraries for different analysis types
    PATHWAY_LIBRARIES = [
        "KEGG_2021_Human",
        "Reactome_2022",
        "WikiPathway_2023_Human",
        "BioPlanet_2019",
    ]

    ONTOLOGY_LIBRARIES = [
        "GO_Biological_Process_2023",
        "GO_Molecular_Function_2023",
        "GO_Cellular_Component_2023",
    ]

    DISEASE_LIBRARIES = [
        "DisGeNET",
        "OMIM_Disease",
        "GWAS_Catalog_2023",
    ]

    TRANSCRIPTION_LIBRARIES = [
        "ENCODE_TF_ChIP-seq_2015",
        "ChEA_2022",
        "TRRUST_Transcription_Factors_2019",
    ]

    def __init__(self, organism: str = "human") -> None:
        """
        Initialize the EnrichmentClient.

        Args:
            organism: The organism to use for analysis.
                Options: "human", "mouse", "fly", "yeast", "worm", "fish".
        """
        self.organism = organism

    def enrichr(
        self,
        gene_list: List[str],
        gene_sets: Optional[Union[str, List[str]]] = None,
        description: str = "labrat_enrichment",
        cutoff: float = 0.05,
    ) -> pd.DataFrame:
        """
        Run Enrichr enrichment analysis on a gene list.

        Args:
            gene_list: List of gene symbols to analyze.
            gene_sets: Gene set library or list of libraries to query.
                Defaults to common pathway libraries if None.
            description: Description for the analysis job.
            cutoff: P-value cutoff for significant results.

        Returns:
            DataFrame with enrichment results including:
            - Term: The enriched term name
            - Overlap: Number of genes overlapping with term
            - P-value: Uncorrected p-value
            - Adjusted P-value: Benjamini-Hochberg corrected p-value
            - Combined Score: Enrichr combined score
            - Genes: Overlapping genes

        Example:
            >>> client = EnrichmentClient()
            >>> results = client.enrichr(
            ...     ["BRCA1", "BRCA2", "TP53"],
            ...     gene_sets="KEGG_2021_Human"
            ... )
        """
        if gene_sets is None:
            gene_sets = self.PATHWAY_LIBRARIES

        if isinstance(gene_sets, str):
            gene_sets = [gene_sets]

        # Run Enrichr analysis
        enr = gp.enrichr(
            gene_list=gene_list,
            gene_sets=gene_sets,
            organism=self.organism,
            description=description,
            outdir=None,  # Don't save to file
            cutoff=cutoff,
        )

        return enr.results

    def pathway_enrichment(
        self,
        gene_list: List[str],
        cutoff: float = 0.05,
    ) -> pd.DataFrame:
        """
        Run pathway enrichment analysis.

        Uses KEGG, Reactome, WikiPathway, and BioPlanet databases.

        Args:
            gene_list: List of gene symbols to analyze.
            cutoff: P-value cutoff for significant results.

        Returns:
            DataFrame with pathway enrichment results.

        Example:
            >>> client = EnrichmentClient()
            >>> results = client.pathway_enrichment(["BRCA1", "BRCA2", "TP53"])
        """
        return self.enrichr(
            gene_list,
            gene_sets=self.PATHWAY_LIBRARIES,
            description="pathway_enrichment",
            cutoff=cutoff,
        )

    def go_enrichment(
        self,
        gene_list: List[str],
        cutoff: float = 0.05,
    ) -> pd.DataFrame:
        """
        Run Gene Ontology (GO) enrichment analysis.

        Analyzes Biological Process, Molecular Function, and Cellular Component.

        Args:
            gene_list: List of gene symbols to analyze.
            cutoff: P-value cutoff for significant results.

        Returns:
            DataFrame with GO enrichment results.

        Example:
            >>> client = EnrichmentClient()
            >>> results = client.go_enrichment(["BRCA1", "BRCA2", "TP53"])
        """
        return self.enrichr(
            gene_list,
            gene_sets=self.ONTOLOGY_LIBRARIES,
            description="go_enrichment",
            cutoff=cutoff,
        )

    def disease_enrichment(
        self,
        gene_list: List[str],
        cutoff: float = 0.05,
    ) -> pd.DataFrame:
        """
        Run disease association enrichment analysis.

        Uses DisGeNET, OMIM, and GWAS Catalog databases.

        Args:
            gene_list: List of gene symbols to analyze.
            cutoff: P-value cutoff for significant results.

        Returns:
            DataFrame with disease enrichment results.

        Example:
            >>> client = EnrichmentClient()
            >>> results = client.disease_enrichment(["BRCA1", "BRCA2", "TP53"])
        """
        return self.enrichr(
            gene_list,
            gene_sets=self.DISEASE_LIBRARIES,
            description="disease_enrichment",
            cutoff=cutoff,
        )

    def tf_enrichment(
        self,
        gene_list: List[str],
        cutoff: float = 0.05,
    ) -> pd.DataFrame:
        """
        Run transcription factor enrichment analysis.

        Identifies transcription factors that may regulate the gene list.

        Args:
            gene_list: List of gene symbols to analyze.
            cutoff: P-value cutoff for significant results.

        Returns:
            DataFrame with transcription factor enrichment results.

        Example:
            >>> client = EnrichmentClient()
            >>> results = client.tf_enrichment(["BRCA1", "BRCA2", "TP53"])
        """
        return self.enrichr(
            gene_list,
            gene_sets=self.TRANSCRIPTION_LIBRARIES,
            description="tf_enrichment",
            cutoff=cutoff,
        )

    @staticmethod
    def list_libraries(organism: str = "human") -> List[str]:
        """
        List all available Enrichr gene set libraries.

        Args:
            organism: Organism to list libraries for.

        Returns:
            List of available library names.

        Example:
            >>> libraries = EnrichmentClient.list_libraries()
            >>> print(len(libraries))
        """
        return gp.get_library_name(organism=organism)


def run_enrichment(
    gene_list: List[str],
    analysis_type: str = "pathway",
    organism: str = "human",
    cutoff: float = 0.05,
) -> pd.DataFrame:
    """
    Convenience function to run enrichment analysis.

    Args:
        gene_list: List of gene symbols to analyze.
        analysis_type: Type of analysis to run.
            Options: "pathway", "go", "disease", "tf", "all".
        organism: Organism for analysis.
        cutoff: P-value cutoff.

    Returns:
        DataFrame with enrichment results.

    Example:
        >>> results = run_enrichment(
        ...     ["BRCA1", "BRCA2", "TP53"],
        ...     analysis_type="pathway"
        ... )
    """
    client = EnrichmentClient(organism=organism)

    if analysis_type == "pathway":
        return client.pathway_enrichment(gene_list, cutoff=cutoff)
    elif analysis_type == "go":
        return client.go_enrichment(gene_list, cutoff=cutoff)
    elif analysis_type == "disease":
        return client.disease_enrichment(gene_list, cutoff=cutoff)
    elif analysis_type == "tf":
        return client.tf_enrichment(gene_list, cutoff=cutoff)
    elif analysis_type == "all":
        all_libraries = (
            client.PATHWAY_LIBRARIES
            + client.ONTOLOGY_LIBRARIES
            + client.DISEASE_LIBRARIES
            + client.TRANSCRIPTION_LIBRARIES
        )
        return client.enrichr(gene_list, gene_sets=all_libraries, cutoff=cutoff)
    else:
        raise ValueError(
            f"Unknown analysis type: {analysis_type}. "
            "Options: 'pathway', 'go', 'disease', 'tf', 'all'"
        )
