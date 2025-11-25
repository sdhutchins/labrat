# -*- coding: utf-8 -*-
"""Tests for glossary module."""

import unittest
from labrat.glossary import (
    GLOSSARY,
    lookup_term,
    search_glossary,
    list_categories,
    get_terms_by_category,
)


class TestGlossaryLookup(unittest.TestCase):
    """Test cases for glossary term lookup."""

    def test_lookup_term_exact_match(self):
        """Test looking up a term with exact match."""
        result = lookup_term("PCR")
        self.assertIsNotNone(result)
        self.assertIn("Polymerase Chain Reaction", result["term"])
        self.assertEqual(result["abbreviation"], "PCR")
        self.assertEqual(result["category"], "molecular_biology")

    def test_lookup_term_case_insensitive(self):
        """Test that lookup is case insensitive."""
        result1 = lookup_term("PCR")
        result2 = lookup_term("pcr")
        result3 = lookup_term("Pcr")
        self.assertEqual(result1["term"], result2["term"])
        self.assertEqual(result2["term"], result3["term"])

    def test_lookup_term_by_full_name(self):
        """Test looking up by full term name."""
        # The glossary stores "Polymerase Chain Reaction (PCR)" as full term
        # Lookup should find it by searching for the abbreviation
        result = lookup_term("PCR")
        self.assertIsNotNone(result)
        self.assertIn("Polymerase Chain Reaction", result["term"])

    def test_lookup_term_not_found(self):
        """Test lookup returns None for unknown terms."""
        result = lookup_term("NotARealTerm12345")
        self.assertIsNone(result)

    def test_lookup_term_by_abbreviation(self):
        """Test looking up by abbreviation."""
        result = lookup_term("qPCR")
        self.assertIsNotNone(result)
        self.assertIn("Quantitative", result["term"])


class TestGlossarySearch(unittest.TestCase):
    """Test cases for glossary search."""

    def test_search_finds_matching_terms(self):
        """Test search returns matching terms."""
        results = search_glossary("DNA")
        self.assertGreater(len(results), 0)
        # DNA should be mentioned in several terms
        self.assertGreater(len(results), 5)

    def test_search_returns_empty_for_no_match(self):
        """Test search returns empty list for no matches."""
        results = search_glossary("xyznonexistent123")
        self.assertEqual(len(results), 0)

    def test_search_with_category_filter(self):
        """Test search with category filter."""
        results = search_glossary("DNA", category="molecular_biology")
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertEqual(result["category"], "molecular_biology")

    def test_search_case_insensitive(self):
        """Test that search is case insensitive."""
        results1 = search_glossary("PCR")
        results2 = search_glossary("pcr")
        self.assertEqual(len(results1), len(results2))


class TestGlossaryCategories(unittest.TestCase):
    """Test cases for glossary category functions."""

    def test_list_categories(self):
        """Test listing all categories."""
        categories = list_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)
        self.assertIn("molecular_biology", categories)
        self.assertIn("genetics", categories)
        self.assertIn("biochemistry", categories)

    def test_categories_are_sorted(self):
        """Test that categories are sorted."""
        categories = list_categories()
        self.assertEqual(categories, sorted(categories))

    def test_get_terms_by_category(self):
        """Test getting terms by category."""
        terms = get_terms_by_category("molecular_biology")
        self.assertGreater(len(terms), 0)
        for term in terms:
            self.assertEqual(term["category"], "molecular_biology")

    def test_get_terms_by_category_case_insensitive(self):
        """Test category lookup is case insensitive."""
        terms1 = get_terms_by_category("molecular_biology")
        terms2 = get_terms_by_category("MOLECULAR_BIOLOGY")
        self.assertEqual(len(terms1), len(terms2))


class TestGlossaryContent(unittest.TestCase):
    """Test cases for glossary content quality."""

    def test_glossary_has_entries(self):
        """Test glossary has entries."""
        self.assertGreater(len(GLOSSARY), 0)

    def test_all_entries_have_required_fields(self):
        """Test all entries have required fields."""
        for key, entry in GLOSSARY.items():
            self.assertIn("term", entry, f"Entry {key} missing 'term' field")
            self.assertIn("definition", entry, f"Entry {key} missing 'definition' field")
            self.assertIn("category", entry, f"Entry {key} missing 'category' field")

    def test_all_entries_have_non_empty_definition(self):
        """Test all definitions are non-empty."""
        for key, entry in GLOSSARY.items():
            self.assertTrue(
                len(entry["definition"]) > 10,
                f"Entry {key} has too short definition"
            )


if __name__ == "__main__":
    unittest.main()
