# -*- coding: utf-8 -*-
"""Report generator for laboratory work."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from jinja2 import Template

from .templates import (
    QC_REPORT_TEMPLATE,
    VARIANT_SUMMARY_TEMPLATE,
    WETLAB_REPORT_TEMPLATE,
)


class ReportGenerator:
    """
    Generator for laboratory reports using Jinja2 templates.

    This class provides methods to generate various types of lab reports
    including QC reports, variant summaries, and wet lab experiment reports.

    Example:
        >>> generator = ReportGenerator()
        >>> report = generator.generate_qc_report(
        ...     project_name="My Project",
        ...     analyst="Dr. Smith",
        ...     metrics=[{"name": "Total Reads", "value": "1000000"}]
        ... )
        >>> print(report)
    """

    def __init__(self) -> None:
        """Initialize the ReportGenerator."""
        self.qc_template = Template(QC_REPORT_TEMPLATE)
        self.variant_template = Template(VARIANT_SUMMARY_TEMPLATE)
        self.wetlab_template = Template(WETLAB_REPORT_TEMPLATE)

    def generate_qc_report(
        self,
        project_name: str,
        analyst: str,
        metrics: List[Dict[str, Any]],
        date: Optional[str] = None,
        sample_count: Optional[int] = None,
        summary: Optional[str] = None,
        samples: Optional[List[Dict[str, Any]]] = None,
        warnings: Optional[List[str]] = None,
        notes: Optional[str] = None,
    ) -> str:
        """
        Generate a QC (Quality Control) report.

        Args:
            project_name: Name of the project.
            analyst: Name of the analyst.
            metrics: List of metric dictionaries with keys: name, value, unit (optional), status (optional).
            date: Report date (defaults to today).
            sample_count: Number of samples.
            summary: Summary text.
            samples: List of sample dictionaries with keys: name, metrics.
            warnings: List of warning messages.
            notes: Additional notes.

        Returns:
            Formatted report string.

        Example:
            >>> report = generator.generate_qc_report(
            ...     project_name="NGS Run 001",
            ...     analyst="Dr. Smith",
            ...     metrics=[
            ...         {"name": "Total Reads", "value": "50M", "status": "PASS"},
            ...         {"name": "Q30", "value": "92%", "status": "PASS"}
            ...     ]
            ... )
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        return self.qc_template.render(
            project_name=project_name,
            date=date,
            analyst=analyst,
            sample_count=sample_count,
            summary=summary,
            metrics=metrics,
            samples=samples,
            warnings=warnings,
            notes=notes,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    def generate_variant_summary(
        self,
        project_name: str,
        analyst: str,
        total_variants: int,
        date: Optional[str] = None,
        reference_genome: Optional[str] = None,
        variant_counts: Optional[Dict[str, int]] = None,
        by_impact: Optional[Dict[str, int]] = None,
        by_consequence: Optional[Dict[str, int]] = None,
        top_genes: Optional[List[Dict[str, Any]]] = None,
        clinvar_variants: Optional[List[Dict[str, Any]]] = None,
        notes: Optional[str] = None,
    ) -> str:
        """
        Generate a variant summary report.

        Args:
            project_name: Name of the project.
            analyst: Name of the analyst.
            total_variants: Total number of variants.
            date: Report date (defaults to today).
            reference_genome: Reference genome version.
            variant_counts: Dict of variant type counts (e.g., SNV, INDEL).
            by_impact: Dict of impact category counts.
            by_consequence: Dict of consequence type counts.
            top_genes: List of top affected genes with name and variant_count.
            clinvar_variants: List of ClinVar variants with id, gene, significance.
            notes: Additional notes.

        Returns:
            Formatted report string.

        Example:
            >>> report = generator.generate_variant_summary(
            ...     project_name="Exome Analysis",
            ...     analyst="Dr. Jones",
            ...     total_variants=15000,
            ...     variant_counts={"SNV": 12000, "INDEL": 3000}
            ... )
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        return self.variant_template.render(
            project_name=project_name,
            date=date,
            analyst=analyst,
            total_variants=total_variants,
            reference_genome=reference_genome,
            variant_counts=variant_counts,
            by_impact=by_impact,
            by_consequence=by_consequence,
            top_genes=top_genes,
            clinvar_variants=clinvar_variants,
            notes=notes,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    def generate_wetlab_report(
        self,
        experiment_name: str,
        researcher: str,
        objective: str,
        materials: List[Dict[str, Any]],
        methods: List[str],
        date: Optional[str] = None,
        lab: Optional[str] = None,
        samples: Optional[List[Dict[str, Any]]] = None,
        results: Optional[str] = None,
        observations: Optional[List[str]] = None,
        conclusions: Optional[str] = None,
        next_steps: Optional[List[str]] = None,
        notes: Optional[str] = None,
    ) -> str:
        """
        Generate a wet lab experiment report.

        Args:
            experiment_name: Name of the experiment.
            researcher: Name of the researcher.
            objective: Experiment objective.
            materials: List of material dictionaries with keys: name, concentration (optional), vendor (optional).
            methods: List of method steps.
            date: Report date (defaults to today).
            lab: Lab name/location.
            samples: List of sample dictionaries with keys: id, description, notes (optional).
            results: Results text.
            observations: List of observations.
            conclusions: Conclusions text.
            next_steps: List of next steps.
            notes: Additional notes.

        Returns:
            Formatted report string.

        Example:
            >>> report = generator.generate_wetlab_report(
            ...     experiment_name="PCR Optimization",
            ...     researcher="Dr. Smith",
            ...     objective="Optimize PCR conditions for BRCA1",
            ...     materials=[{"name": "Taq Polymerase", "vendor": "NEB"}],
            ...     methods=["Step 1...", "Step 2..."]
            ... )
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        return self.wetlab_template.render(
            experiment_name=experiment_name,
            date=date,
            researcher=researcher,
            lab=lab,
            objective=objective,
            materials=materials,
            methods=methods,
            samples=samples,
            results=results,
            observations=observations,
            conclusions=conclusions,
            next_steps=next_steps,
            notes=notes,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    def save_report(
        self,
        report: str,
        output_path: Optional[Union[str, Path]] = None,
        base_name: str = "report",
    ) -> Path:
        """
        Save a report to a file.

        Args:
            report: The report content to save.
            output_path: Optional path to save to. If None, generates dated filename.
            base_name: Base name for auto-generated filename.

        Returns:
            Path to the saved file.
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_path = Path.cwd() / f"{base_name}_{timestamp}.txt"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(report)

        return output_path


def generate_qc_report(
    project_name: str,
    analyst: str,
    metrics: List[Dict[str, Any]],
    **kwargs: Any,
) -> str:
    """
    Convenience function to generate a QC report.

    Args:
        project_name: Name of the project.
        analyst: Name of the analyst.
        metrics: List of metric dictionaries.
        **kwargs: Additional arguments passed to ReportGenerator.generate_qc_report.

    Returns:
        Formatted report string.

    Example:
        >>> report = generate_qc_report(
        ...     project_name="Run001",
        ...     analyst="Dr. Smith",
        ...     metrics=[{"name": "Reads", "value": "50M"}]
        ... )
    """
    generator = ReportGenerator()
    return generator.generate_qc_report(project_name, analyst, metrics, **kwargs)


def generate_variant_summary(
    project_name: str,
    analyst: str,
    total_variants: int,
    **kwargs: Any,
) -> str:
    """
    Convenience function to generate a variant summary report.

    Args:
        project_name: Name of the project.
        analyst: Name of the analyst.
        total_variants: Total number of variants.
        **kwargs: Additional arguments passed to ReportGenerator.generate_variant_summary.

    Returns:
        Formatted report string.

    Example:
        >>> report = generate_variant_summary(
        ...     project_name="Exome001",
        ...     analyst="Dr. Jones",
        ...     total_variants=15000
        ... )
    """
    generator = ReportGenerator()
    return generator.generate_variant_summary(project_name, analyst, total_variants, **kwargs)


def generate_wetlab_report(
    experiment_name: str,
    researcher: str,
    objective: str,
    materials: List[Dict[str, Any]],
    methods: List[str],
    **kwargs: Any,
) -> str:
    """
    Convenience function to generate a wet lab report.

    Args:
        experiment_name: Name of the experiment.
        researcher: Name of the researcher.
        objective: Experiment objective.
        materials: List of material dictionaries.
        methods: List of method steps.
        **kwargs: Additional arguments passed to ReportGenerator.generate_wetlab_report.

    Returns:
        Formatted report string.

    Example:
        >>> report = generate_wetlab_report(
        ...     experiment_name="PCR Test",
        ...     researcher="Dr. Smith",
        ...     objective="Test PCR conditions",
        ...     materials=[{"name": "Taq"}],
        ...     methods=["Mix reagents", "Run PCR"]
        ... )
    """
    generator = ReportGenerator()
    return generator.generate_wetlab_report(
        experiment_name, researcher, objective, materials, methods, **kwargs
    )
