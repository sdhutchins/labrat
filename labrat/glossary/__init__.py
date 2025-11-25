# -*- coding: utf-8 -*-
"""Science and laboratory glossary module."""

from .terms import (
    GLOSSARY,
    lookup_term,
    search_glossary,
    list_categories,
    get_terms_by_category,
)
from .external import (
    fetch_wikipedia_definition,
    search_wikipedia,
    fetch_pubmed_definition,
)

__all__ = [
    "GLOSSARY",
    "lookup_term",
    "search_glossary",
    "list_categories",
    "get_terms_by_category",
    "fetch_wikipedia_definition",
    "search_wikipedia",
    "fetch_pubmed_definition",
]
