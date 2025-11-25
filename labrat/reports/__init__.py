# -*- coding: utf-8 -*-
"""Report generation templates for laboratory work."""

from .generator import (
    ReportGenerator,
    generate_qc_report,
    generate_variant_summary,
    generate_wetlab_report,
)
from .templates import (
    QC_REPORT_TEMPLATE,
    VARIANT_SUMMARY_TEMPLATE,
    WETLAB_REPORT_TEMPLATE,
)

__all__ = [
    "ReportGenerator",
    "generate_qc_report",
    "generate_variant_summary",
    "generate_wetlab_report",
    "QC_REPORT_TEMPLATE",
    "VARIANT_SUMMARY_TEMPLATE",
    "WETLAB_REPORT_TEMPLATE",
]
