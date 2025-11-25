# -*- coding: utf-8 -*-
"""Tests for report generation."""

import unittest
from labrat.reports import (
    ReportGenerator,
    generate_qc_report,
    generate_variant_summary,
    generate_wetlab_report,
)


class TestReportGenerator(unittest.TestCase):
    """Test cases for ReportGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = ReportGenerator()

    def test_generate_qc_report_basic(self):
        """Test basic QC report generation."""
        report = self.generator.generate_qc_report(
            project_name="Test Project",
            analyst="Dr. Smith",
            metrics=[
                {"name": "Total Reads", "value": "50M", "status": "PASS"},
                {"name": "Q30", "value": "92%"},
            ],
        )
        self.assertIn("Test Project", report)
        self.assertIn("Dr. Smith", report)
        self.assertIn("Total Reads", report)
        self.assertIn("50M", report)
        self.assertIn("PASS", report)
        self.assertIn("Q30", report)

    def test_generate_qc_report_with_all_options(self):
        """Test QC report with all options."""
        report = self.generator.generate_qc_report(
            project_name="Full Test",
            analyst="Dr. Jones",
            metrics=[{"name": "Metric1", "value": "100"}],
            sample_count=10,
            summary="This is a summary.",
            samples=[{"name": "Sample1", "metrics": {"reads": "1M"}}],
            warnings=["Warning 1", "Warning 2"],
            notes="Additional notes here.",
        )
        self.assertIn("Full Test", report)
        self.assertIn("10", report)
        self.assertIn("This is a summary", report)
        self.assertIn("Sample1", report)
        self.assertIn("Warning 1", report)
        self.assertIn("Additional notes", report)

    def test_generate_variant_summary_basic(self):
        """Test basic variant summary generation."""
        report = self.generator.generate_variant_summary(
            project_name="Exome Analysis",
            analyst="Dr. Variant",
            total_variants=15000,
        )
        self.assertIn("Exome Analysis", report)
        self.assertIn("Dr. Variant", report)
        self.assertIn("15000", report)

    def test_generate_variant_summary_with_counts(self):
        """Test variant summary with variant counts."""
        report = self.generator.generate_variant_summary(
            project_name="Test",
            analyst="Test",
            total_variants=15000,
            variant_counts={"SNV": 12000, "INDEL": 3000},
            by_impact={"HIGH": 100, "MODERATE": 500},
        )
        self.assertIn("SNV", report)
        self.assertIn("12000", report)
        self.assertIn("INDEL", report)
        self.assertIn("HIGH", report)

    def test_generate_wetlab_report_basic(self):
        """Test basic wet lab report generation."""
        report = self.generator.generate_wetlab_report(
            experiment_name="PCR Test",
            researcher="Dr. Lab",
            objective="Test PCR conditions",
            materials=[{"name": "Taq Polymerase", "vendor": "NEB"}],
            methods=["Step 1", "Step 2", "Step 3"],
        )
        self.assertIn("PCR Test", report)
        self.assertIn("Dr. Lab", report)
        self.assertIn("Test PCR conditions", report)
        self.assertIn("Taq Polymerase", report)
        self.assertIn("NEB", report)
        self.assertIn("Step 1", report)

    def test_generate_wetlab_report_with_all_options(self):
        """Test wet lab report with all options."""
        report = self.generator.generate_wetlab_report(
            experiment_name="Full Experiment",
            researcher="Dr. Full",
            objective="Complete all tests",
            materials=[
                {"name": "Buffer", "concentration": "10X"},
                {"name": "Enzyme"},
            ],
            methods=["Do this", "Do that"],
            lab="Main Lab",
            samples=[{"id": "S1", "description": "Sample 1"}],
            results="Experiment was successful.",
            observations=["Observation 1", "Observation 2"],
            conclusions="It worked!",
            next_steps=["Next 1", "Next 2"],
            notes="Some notes.",
        )
        self.assertIn("Full Experiment", report)
        self.assertIn("Main Lab", report)
        self.assertIn("Experiment was successful", report)
        self.assertIn("Observation 1", report)
        self.assertIn("It worked!", report)
        self.assertIn("Next 1", report)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions for report generation."""

    def test_generate_qc_report_function(self):
        """Test generate_qc_report convenience function."""
        report = generate_qc_report(
            project_name="Test",
            analyst="Test",
            metrics=[{"name": "M1", "value": "V1"}],
        )
        self.assertIn("Test", report)
        self.assertIn("M1", report)

    def test_generate_variant_summary_function(self):
        """Test generate_variant_summary convenience function."""
        report = generate_variant_summary(
            project_name="Test",
            analyst="Test",
            total_variants=100,
        )
        self.assertIn("Test", report)
        self.assertIn("100", report)

    def test_generate_wetlab_report_function(self):
        """Test generate_wetlab_report convenience function."""
        report = generate_wetlab_report(
            experiment_name="Test Exp",
            researcher="Dr. Test",
            objective="Test objective",
            materials=[{"name": "Material"}],
            methods=["Method 1"],
        )
        self.assertIn("Test Exp", report)
        self.assertIn("Test objective", report)


class TestReportSaving(unittest.TestCase):
    """Test report saving functionality."""

    def setUp(self):
        """Set up test fixtures."""
        import tempfile
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ReportGenerator()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_report(self):
        """Test saving a report to file."""
        import os
        report = self.generator.generate_qc_report(
            project_name="Save Test",
            analyst="Test",
            metrics=[{"name": "M", "value": "V"}],
        )
        output_path = os.path.join(self.temp_dir, "test_report.txt")
        path = self.generator.save_report(report, output_path=output_path)
        self.assertTrue(path.exists())
        with open(path) as f:
            content = f.read()
        self.assertIn("Save Test", content)

    def test_save_report_auto_filename(self):
        """Test saving with auto-generated filename."""
        import os
        report = "Test report content"
        # Change to temp dir to avoid polluting the repo
        original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        try:
            path = self.generator.save_report(report, base_name="auto_test")
            self.assertTrue(path.exists())
            self.assertTrue("auto_test" in str(path))
        finally:
            os.chdir(original_dir)


if __name__ == "__main__":
    unittest.main()
