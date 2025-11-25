# -*- coding: utf-8 -*-
"""Output utilities for saving calculations to files."""

import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def get_dated_filename(base_name: str, extension: str = "txt") -> str:
    """
    Generate a dated filename.

    Args:
        base_name: Base name for the file (e.g., "mastermix", "dilution_series").
        extension: File extension (default: "txt").

    Returns:
        Filename with date stamp (e.g., "mastermix_2024-01-15_14-30-45.txt").

    Example:
        >>> filename = get_dated_filename("mastermix")
        >>> print(filename)  # mastermix_2024-01-15_14-30-45.txt
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{base_name}_{timestamp}.{extension}"


def save_text_output(
    content: str,
    output_path: Optional[Union[str, Path]] = None,
    base_name: str = "output",
) -> Path:
    """
    Save text content to a dated file.

    Args:
        content: Text content to save.
        output_path: Optional path to save to. If None, generates dated filename
            in current directory.
        base_name: Base name for auto-generated filename.

    Returns:
        Path to the saved file.

    Example:
        >>> path = save_text_output("Hello, World!", base_name="test")
        >>> print(f"Saved to: {path}")
    """
    if output_path is None:
        output_path = Path.cwd() / get_dated_filename(base_name, "txt")
    else:
        output_path = Path(output_path)

    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(content)

    return output_path


def save_csv_output(
    data: List[Dict[str, Any]],
    output_path: Optional[Union[str, Path]] = None,
    base_name: str = "output",
    delimiter: str = ",",
) -> Path:
    """
    Save data to a CSV or TSV file.

    Args:
        data: List of dictionaries to save.
        output_path: Optional path to save to. If None, generates dated filename.
        base_name: Base name for auto-generated filename.
        delimiter: Delimiter character ("," for CSV, "\\t" for TSV).

    Returns:
        Path to the saved file.

    Example:
        >>> data = [{"name": "A", "value": 1}, {"name": "B", "value": 2}]
        >>> path = save_csv_output(data, base_name="results")
    """
    extension = "tsv" if delimiter == "\t" else "csv"

    if output_path is None:
        output_path = Path.cwd() / get_dated_filename(base_name, extension)
    else:
        output_path = Path(output_path)

    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not data:
        with open(output_path, "w") as f:
            f.write("")
        return output_path

    # Get all unique keys from all dictionaries
    fieldnames = []
    for row in data:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)

    return output_path


def format_dilution_for_csv(
    dilution_result: Dict[str, Any],
    initial_conc: float,
    final_conc: float,
    final_volume: float,
    unit: str = "",
) -> List[Dict[str, Any]]:
    """
    Format a single dilution result for CSV export.

    Args:
        dilution_result: Result from calculate_dilution().
        initial_conc: Initial concentration.
        final_conc: Final concentration.
        final_volume: Final volume.
        unit: Concentration unit.

    Returns:
        List with single dictionary formatted for CSV.
    """
    return [
        {
            "Initial Concentration": f"{initial_conc} {unit}".strip(),
            "Final Concentration": f"{final_conc} {unit}".strip(),
            "Final Volume": f"{final_volume}",
            "Stock Volume": dilution_result["stock_volume"],
            "Diluent Volume": dilution_result["diluent_volume"],
            "Dilution Factor": f"{dilution_result['dilution_factor']:.1f}x",
        }
    ]


def format_serial_dilution_for_csv(series: Any) -> List[Dict[str, Any]]:
    """
    Format a serial dilution series for CSV export.

    Args:
        series: DilutionSeries object.

    Returns:
        List of dictionaries formatted for CSV export.
    """
    data = []
    for i, conc in enumerate(series.concentrations):
        step = "Stock" if i == 0 else f"D{i}"
        diluent = 0 if i == 0 else series.final_volume - series.transfer_volume

        data.append(
            {
                "Step": step,
                "Concentration": conc,
                "Unit": series.concentration_unit,
                "Transfer Volume (µL)": series.transfer_volume if i > 0 else "-",
                "Diluent Volume (µL)": diluent if i > 0 else "-",
                "Final Volume (µL)": series.final_volume,
            }
        )
    return data


def format_mastermix_for_csv(mastermix: Any) -> List[Dict[str, Any]]:
    """
    Format a master mix for CSV export.

    Args:
        mastermix: MasterMix object.

    Returns:
        List of dictionaries formatted for CSV export.
    """
    data = []
    for component, values in mastermix.components.items():
        data.append(
            {
                "Component": component,
                "Volume per Reaction (µL)": values["per_reaction"],
                "Total Volume (µL)": f"{values['total_volume']:.2f}",
                "Final Concentration": values.get("final_conc", "-"),
            }
        )

    # Add summary row
    data.append({})  # Empty row
    data.append(
        {
            "Component": "SUMMARY",
            "Volume per Reaction (µL)": mastermix.volume_per_reaction,
            "Total Volume (µL)": f"{mastermix.total_volume:.2f}",
            "Final Concentration": f"{mastermix.reactions} reactions + {mastermix.extra_percent}% extra",
        }
    )
    return data


def format_buffer_for_csv(
    recipe: Any,
    volume_ml: float = 1000.0,
) -> List[Dict[str, Any]]:
    """
    Format a buffer recipe for CSV export.

    Args:
        recipe: BufferRecipe object.
        volume_ml: Volume to prepare in mL.

    Returns:
        List of dictionaries formatted for CSV export.
    """
    scale_factor = volume_ml / 1000.0
    data = []

    for component, values in recipe.components.items():
        scaled_amount = values["amount"] * scale_factor
        data.append(
            {
                "Component": component,
                "Amount per Liter": f"{values['amount']} {values['unit']}",
                f"Amount for {volume_ml} mL": f"{scaled_amount:.3f} {values['unit']}",
                "Molecular Weight": values.get("mw", "-"),
            }
        )

    # Add notes
    if recipe.notes:
        data.append({})  # Empty row
        data.append({"Component": "NOTES", "Amount per Liter": "", f"Amount for {volume_ml} mL": "", "Molecular Weight": ""})
        for i, note in enumerate(recipe.notes, 1):
            data.append({"Component": f"{i}. {note}", "Amount per Liter": "", f"Amount for {volume_ml} mL": "", "Molecular Weight": ""})

    return data


def format_qpcr_layout_for_csv(layout: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Format a qPCR plate layout for CSV export.

    Args:
        layout: Dictionary from generate_qpcr_plate_layout().

    Returns:
        List of dictionaries formatted for CSV export.
    """
    data = []
    for well_id, assignment in layout["well_assignments"].items():
        data.append(
            {
                "Well": well_id,
                "Sample": assignment["sample"],
                "Gene": assignment["gene"],
                "Replicate": assignment["replicate"],
                "Type": assignment["type"],
            }
        )
    return data
