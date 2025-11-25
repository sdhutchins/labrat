# -*- coding: utf-8 -*-
"""PCR and qPCR helper functions for laboratory work."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

import pint

# Initialize unit registry
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


@dataclass
class MasterMix:
    """
    Represents a PCR master mix composition and volumes.

    Attributes:
        reactions: Number of reactions to prepare.
        volume_per_reaction: Volume per reaction in microliters.
        components: Dictionary of component volumes per reaction.
        total_volume: Total volume including extra for pipetting error.
        extra_percent: Percentage of extra volume for pipetting loss.

    Example:
        >>> mm = calculate_mastermix(reactions=10, volume=25.0)
        >>> print(mm)
    """

    reactions: int
    volume_per_reaction: float
    components: Dict[str, Dict[str, Any]]
    total_volume: float
    extra_percent: float = 10.0

    def __str__(self) -> str:
        """Return a formatted string representation of the master mix."""
        lines = [
            f"PCR Master Mix ({self.reactions} reactions + {self.extra_percent}% extra)",
            f"Volume per reaction: {self.volume_per_reaction} µL",
            f"Total volume: {self.total_volume:.2f} µL",
            "-" * 50,
        ]
        for component, data in self.components.items():
            lines.append(
                f"{component:25s}: {data['total_volume']:8.2f} µL "
                f"(per rxn: {data['per_reaction']:.2f} µL)"
            )
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Return the master mix as a dictionary."""
        return {
            "reactions": self.reactions,
            "volume_per_reaction": self.volume_per_reaction,
            "total_volume": self.total_volume,
            "extra_percent": self.extra_percent,
            "components": self.components,
        }


def calculate_mastermix(
    reactions: int,
    volume: float = 25.0,
    extra_percent: float = 10.0,
    polymerase_type: str = "taq",
    include_template: bool = False,
) -> MasterMix:
    """
    Calculate PCR master mix volumes for the specified number of reactions.

    Args:
        reactions: Number of reactions to prepare.
        volume: Total volume per reaction in microliters.
        extra_percent: Percentage of extra volume for pipetting error.
        polymerase_type: Type of polymerase ("taq" or "high_fidelity").
        include_template: Whether to include template DNA in the mix.

    Returns:
        MasterMix object with calculated volumes.

    Example:
        >>> mm = calculate_mastermix(reactions=10, volume=25.0, extra_percent=10)
        >>> print(mm.components["Water"]["total_volume"])
    """
    # Calculate total reactions including extra
    total_reactions = reactions * (1 + extra_percent / 100)

    # Standard PCR component concentrations and volumes
    # Based on typical Taq polymerase reaction setup
    if polymerase_type == "taq":
        components = {
            "10X Buffer": {"per_reaction": volume * 0.1, "final_conc": "1X"},
            "dNTPs (10 mM each)": {"per_reaction": volume * 0.02, "final_conc": "200 µM"},
            "Forward Primer (10 µM)": {"per_reaction": volume * 0.02, "final_conc": "0.2 µM"},
            "Reverse Primer (10 µM)": {"per_reaction": volume * 0.02, "final_conc": "0.2 µM"},
            "Taq Polymerase (5 U/µL)": {"per_reaction": 0.25, "final_conc": "1.25 U"},
            "MgCl2 (25 mM)": {"per_reaction": volume * 0.06, "final_conc": "1.5 mM"},
        }
    elif polymerase_type == "high_fidelity":
        components = {
            "5X HF Buffer": {"per_reaction": volume * 0.2, "final_conc": "1X"},
            "dNTPs (10 mM each)": {"per_reaction": volume * 0.02, "final_conc": "200 µM"},
            "Forward Primer (10 µM)": {"per_reaction": volume * 0.02, "final_conc": "0.2 µM"},
            "Reverse Primer (10 µM)": {"per_reaction": volume * 0.02, "final_conc": "0.2 µM"},
            "HF Polymerase (2 U/µL)": {"per_reaction": 0.5, "final_conc": "1 U"},
        }
    else:
        raise ValueError(f"Unknown polymerase type: {polymerase_type}")

    # Add template if requested
    if include_template:
        components["Template DNA"] = {"per_reaction": 1.0, "final_conc": "variable"}

    # Calculate used volume per reaction
    used_volume = sum(c["per_reaction"] for c in components.values())

    # Calculate water to bring to final volume
    water_volume = volume - used_volume
    if water_volume < 0:
        raise ValueError(
            f"Component volumes ({used_volume:.2f} µL) exceed reaction volume ({volume} µL)"
        )

    components["Water"] = {"per_reaction": water_volume, "final_conc": "-"}

    # Calculate total volumes for each component
    for component in components.values():
        component["total_volume"] = component["per_reaction"] * total_reactions

    total_volume = volume * total_reactions

    return MasterMix(
        reactions=reactions,
        volume_per_reaction=volume,
        components=components,
        total_volume=total_volume,
        extra_percent=extra_percent,
    )


def calculate_tm(
    sequence: str,
    method: str = "wallace",
    na_conc: float = 50.0,
    primer_conc: float = 250.0,
) -> float:
    """
    Calculate the melting temperature (Tm) of a primer sequence.

    Args:
        sequence: DNA primer sequence (5' to 3').
        method: Calculation method ("wallace", "gc_content", or "nearest_neighbor").
        na_conc: Sodium concentration in mM (for nearest_neighbor).
        primer_conc: Primer concentration in nM (for nearest_neighbor).

    Returns:
        Calculated Tm in degrees Celsius.

    Example:
        >>> tm = calculate_tm("ATGCGATCGATCGATCG")
        >>> print(f"Tm: {tm:.1f}°C")
    """
    sequence = sequence.upper().replace(" ", "")

    # Count nucleotides
    a_count = sequence.count("A")
    t_count = sequence.count("T")
    g_count = sequence.count("G")
    c_count = sequence.count("C")
    length = len(sequence)

    if method == "wallace":
        # Wallace rule: Tm = 2(A+T) + 4(G+C)
        # Best for primers < 14 bp
        tm = 2 * (a_count + t_count) + 4 * (g_count + c_count)

    elif method == "gc_content":
        # Basic GC content method
        # Tm = 64.9 + 41 * (G+C-16.4) / (A+T+G+C)
        gc_content = (g_count + c_count) / length
        tm = 64.9 + 41 * (gc_content - 0.41) * 100 / length

    elif method == "nearest_neighbor":
        # Simplified nearest neighbor method
        # More accurate for primers 18-30 bp
        gc_content = (g_count + c_count) / length
        tm = 81.5 + 16.6 * (gc_content) - 675 / length

    else:
        raise ValueError(f"Unknown method: {method}. Use 'wallace', 'gc_content', or 'nearest_neighbor'")

    return round(tm, 1)


def calculate_primer_concentration(
    od260: float,
    extinction_coefficient: Optional[float] = None,
    sequence: Optional[str] = None,
) -> Dict[str, float]:
    """
    Calculate primer concentration from OD260 measurement.

    Args:
        od260: Absorbance at 260 nm.
        extinction_coefficient: Molar extinction coefficient (L/mol·cm).
            If not provided, calculated from sequence.
        sequence: Primer sequence for calculating extinction coefficient.

    Returns:
        Dictionary with concentration in various units.

    Example:
        >>> conc = calculate_primer_concentration(0.5, sequence="ATGCGATCG")
        >>> print(f"Concentration: {conc['uM']:.1f} µM")
    """
    if extinction_coefficient is None:
        if sequence is None:
            # Use average extinction coefficient for DNA
            extinction_coefficient = 33000  # L/(mol·cm) per base average
        else:
            # Calculate from sequence using nearest neighbor values
            sequence = sequence.upper()
            # Simplified individual nucleotide contributions
            coefficients = {"A": 15400, "T": 8700, "G": 11500, "C": 7400}
            extinction_coefficient = sum(
                coefficients.get(base, 10000) for base in sequence
            )

    # Beer-Lambert Law: A = ε * c * l
    # c = A / (ε * l), where l = 1 cm
    concentration_m = od260 / extinction_coefficient
    concentration_um = concentration_m * 1e6
    concentration_nm = concentration_m * 1e9
    concentration_pmol_ul = concentration_um

    return {
        "M": concentration_m,
        "mM": concentration_m * 1e3,
        "uM": concentration_um,
        "nM": concentration_nm,
        "pmol/uL": concentration_pmol_ul,
    }


def generate_qpcr_plate_layout(
    samples: List[str],
    genes: List[str],
    replicates: int = 3,
    include_ntc: bool = True,
    plate_size: int = 96,
) -> Dict[str, Any]:
    """
    Generate a qPCR plate layout for the given samples and genes.

    Args:
        samples: List of sample names.
        genes: List of gene names to assay.
        replicates: Number of technical replicates per sample-gene combination.
        include_ntc: Whether to include no-template controls.
        plate_size: Plate size (96 or 384).

    Returns:
        Dictionary containing:
        - layout: 2D list representing the plate
        - well_assignments: Dict mapping well positions to sample/gene info
        - summary: Summary statistics

    Example:
        >>> layout = generate_qpcr_plate_layout(
        ...     samples=["Sample1", "Sample2"],
        ...     genes=["GAPDH", "ACTB", "Target1"],
        ...     replicates=3
        ... )
        >>> print(layout["summary"])
    """
    if plate_size == 96:
        rows, cols = 8, 12
        row_labels = "ABCDEFGH"
    elif plate_size == 384:
        rows, cols = 16, 24
        row_labels = "ABCDEFGHIJKLMNOP"
    else:
        raise ValueError("Plate size must be 96 or 384")

    # Calculate wells needed
    wells_per_gene = len(samples) * replicates
    if include_ntc:
        wells_per_gene += replicates  # NTC replicates

    total_wells_needed = wells_per_gene * len(genes)
    available_wells = rows * cols

    if total_wells_needed > available_wells:
        raise ValueError(
            f"Not enough wells: need {total_wells_needed}, have {available_wells}. "
            f"Consider reducing replicates or using a larger plate."
        )

    # Initialize plate layout and well assignments
    layout = [[None for _ in range(cols)] for _ in range(rows)]
    well_assignments = {}

    # Assign wells by gene (columns), then samples (rows)
    current_col = 0
    current_row = 0

    for gene in genes:
        # Samples for this gene
        for sample in samples:
            for rep in range(replicates):
                if current_row >= rows:
                    current_row = 0
                    current_col += 1

                if current_col >= cols:
                    raise ValueError("Exceeded plate capacity")

                well_id = f"{row_labels[current_row]}{current_col + 1}"
                layout[current_row][current_col] = f"{sample[:4]}_{gene[:4]}_{rep + 1}"
                well_assignments[well_id] = {
                    "sample": sample,
                    "gene": gene,
                    "replicate": rep + 1,
                    "type": "sample",
                }
                current_row += 1

        # NTC for this gene
        if include_ntc:
            for rep in range(replicates):
                if current_row >= rows:
                    current_row = 0
                    current_col += 1

                well_id = f"{row_labels[current_row]}{current_col + 1}"
                layout[current_row][current_col] = f"NTC_{gene[:4]}_{rep + 1}"
                well_assignments[well_id] = {
                    "sample": "NTC",
                    "gene": gene,
                    "replicate": rep + 1,
                    "type": "ntc",
                }
                current_row += 1

        # Move to next column set for next gene
        current_row = 0
        current_col += 1

    summary = {
        "total_samples": len(samples),
        "total_genes": len(genes),
        "replicates": replicates,
        "include_ntc": include_ntc,
        "wells_used": len(well_assignments),
        "wells_available": available_wells,
        "utilization": f"{len(well_assignments) / available_wells * 100:.1f}%",
    }

    return {
        "layout": layout,
        "well_assignments": well_assignments,
        "summary": summary,
        "row_labels": list(row_labels),
        "col_labels": list(range(1, cols + 1)),
    }
