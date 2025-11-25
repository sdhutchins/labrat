# -*- coding: utf-8 -*-
"""External knowledge sources for glossary lookups (Wikipedia, PubMed)."""

from typing import Any, Dict, List, Optional

import wikipediaapi


def fetch_wikipedia_definition(
    term: str,
    sentences: int = 3,
    language: str = "en",
) -> Optional[Dict[str, Any]]:
    """
    Fetch a definition from Wikipedia.

    Args:
        term: The term to look up.
        sentences: Number of sentences to include in the summary.
        language: Wikipedia language code.

    Returns:
        Dictionary with term information from Wikipedia, or None if not found.

    Example:
        >>> result = fetch_wikipedia_definition("PCR")
        >>> if result:
        ...     print(result['definition'])
    """
    wiki = wikipediaapi.Wikipedia(
        user_agent="labrat/1.0 (https://github.com/sdhutchins/labrat)",
        language=language,
    )

    page = wiki.page(term)

    if not page.exists():
        # Try with different capitalizations
        for variant in [term.upper(), term.lower(), term.title()]:
            page = wiki.page(variant)
            if page.exists():
                break

    if not page.exists():
        return None

    # Get the summary (first few sentences)
    summary = page.summary
    if sentences > 0:
        # Split into sentences and take the first N
        sentence_list = summary.split(". ")
        summary = ". ".join(sentence_list[:sentences])
        if not summary.endswith("."):
            summary += "."

    return {
        "term": page.title,
        "definition": summary,
        "source": "wikipedia",
        "url": page.fullurl,
        "categories": [cat for cat in list(page.categories.keys())[:5]],
    }


def search_wikipedia(
    query: str,
    limit: int = 5,
    language: str = "en",
) -> List[Dict[str, Any]]:
    """
    Search Wikipedia for terms matching a query.

    Args:
        query: Search query string.
        limit: Maximum number of results to return.
        language: Wikipedia language code.

    Returns:
        List of matching term dictionaries with titles and summaries.

    Example:
        >>> results = search_wikipedia("DNA replication")
        >>> for r in results:
        ...     print(r['term'])
    """
    wiki = wikipediaapi.Wikipedia(
        user_agent="labrat/1.0 (https://github.com/sdhutchins/labrat)",
        language=language,
    )

    # Wikipedia-API doesn't have direct search, so we'll use page lookup
    # with the query term and related terms
    results = []

    page = wiki.page(query)
    if page.exists():
        summary = page.summary
        sentence_list = summary.split(". ")
        short_summary = ". ".join(sentence_list[:2])
        if not short_summary.endswith("."):
            short_summary += "."

        results.append({
            "term": page.title,
            "definition": short_summary,
            "source": "wikipedia",
            "url": page.fullurl,
        })

    return results[:limit]


def fetch_pubmed_definition(term: str) -> Optional[Dict[str, Any]]:
    """
    Fetch information about a term from PubMed/NCBI.

    Note: This is a placeholder for future PubMed integration.
    Full implementation would require the Entrez API.

    Args:
        term: The term to look up.

    Returns:
        Dictionary with term information, or None if not found.
    """
    # PubMed integration would require biopython or direct Entrez API calls
    # This is a placeholder for future implementation
    return None
