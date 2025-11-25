# -*- coding: utf-8 -*-
"""Serial dilution and dilution calculation utilities."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

import pint

# Initialize unit registry
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


@dataclass
class DilutionSeries:
    """
    Represents a serial dilution series with all calculated values.

    Attributes:
        initial_concentration: Starting concentration.
        dilution_factor: Fold dilution at each step.
        num_dilutions: Number of dilution steps.
        transfer_volume: Volume transferred at each step.
        final_volume: Final volume in each tube.
        concentrations: List of concentrations at each dilution.
        volumes: Dictionary of volumes needed for preparation.

    Example:
        >>> series = serial_dilution(100, factor=10, dilutions=5)
        >>> print(series)
    """

    initial_concentration: float
    concentration_unit: str
    dilution_factor: float
    num_dilutions: int
    transfer_volume: float
    final_volume: float
    concentrations: List[float]
    volumes: Dict[str, Any]

    def __str__(self) -> str:
        """Return a formatted string representation of the dilution series."""
        lines = [
            f"Serial Dilution Series (1:{self.dilution_factor} fold)",
            f"Initial concentration: {self.initial_concentration} {self.concentration_unit}",
            f"Transfer volume: {self.transfer_volume} µL",
            f"Final volume per tube: {self.final_volume} µL",
            "-" * 50,
            "Step | Concentration | Diluent Volume",
            "-" * 50,
        ]
        for i, conc in enumerate(self.concentrations):
            step = "Stock" if i == 0 else f"D{i}"
            diluent = 0 if i == 0 else self.final_volume - self.transfer_volume
            lines.append(
                f"{step:5s} | {conc:12.4g} {self.concentration_unit:5s} | "
                f"{diluent:.1f} µL"
            )
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Return the dilution series as a dictionary."""
        return {
            "initial_concentration": self.initial_concentration,
            "concentration_unit": self.concentration_unit,
            "dilution_factor": self.dilution_factor,
            "num_dilutions": self.num_dilutions,
            "transfer_volume": self.transfer_volume,
            "final_volume": self.final_volume,
            "concentrations": self.concentrations,
            "volumes": self.volumes,
        }


def serial_dilution(
    initial_concentration: float,
    factor: float = 10.0,
    dilutions: int = 6,
    transfer_volume: float = 100.0,
    final_volume: float = 1000.0,
    concentration_unit: str = "µM",
) -> DilutionSeries:
    """
    Calculate a serial dilution series.

    Args:
        initial_concentration: Starting concentration.
        factor: Dilution factor at each step (e.g., 10 for 1:10 dilution).
        dilutions: Number of dilution steps (not including stock).
        transfer_volume: Volume to transfer at each step (in µL).
        final_volume: Final volume in each tube (in µL).
        concentration_unit: Unit of concentration.

    Returns:
        DilutionSeries object with all calculated values.

    Example:
        >>> series = serial_dilution(100, factor=10, dilutions=5)
        >>> print(series.concentrations)
        [100, 10.0, 1.0, 0.1, 0.01, 0.001]
    """
    # Validate inputs
    if factor <= 1:
        raise ValueError("Dilution factor must be greater than 1")

    if transfer_volume >= final_volume:
        raise ValueError("Transfer volume must be less than final volume")

    # For proper serial dilution, the transfer volume should create the dilution factor
    expected_transfer = final_volume / factor
    actual_factor = final_volume / transfer_volume

    if abs(actual_factor - factor) > 0.01:
        # Adjust to achieve requested dilution factor
        diluent_volume = final_volume - transfer_volume
        actual_factor = (transfer_volume + diluent_volume) / transfer_volume

    # Calculate concentrations
    concentrations = [initial_concentration]
    for i in range(dilutions):
        next_conc = concentrations[-1] / factor
        concentrations.append(next_conc)

    # Calculate volumes needed
    diluent_volume = final_volume - transfer_volume
    total_diluent = diluent_volume * dilutions
    total_transfer = transfer_volume * dilutions

    volumes = {
        "transfer_per_step": transfer_volume,
        "diluent_per_step": diluent_volume,
        "total_diluent_needed": total_diluent,
        "total_transfers": total_transfer,
        "stock_volume_needed": transfer_volume,  # Initial transfer from stock
    }

    return DilutionSeries(
        initial_concentration=initial_concentration,
        concentration_unit=concentration_unit,
        dilution_factor=factor,
        num_dilutions=dilutions,
        transfer_volume=transfer_volume,
        final_volume=final_volume,
        concentrations=concentrations,
        volumes=volumes,
    )


def calculate_dilution(
    initial_conc: float,
    final_conc: float,
    final_volume: float,
) -> Dict[str, float]:
    """
    Calculate volumes needed for a single dilution using C1V1 = C2V2.

    Args:
        initial_conc: Initial/stock concentration.
        final_conc: Desired final concentration.
        final_volume: Desired final volume.

    Returns:
        Dictionary with stock_volume and diluent_volume.

    Example:
        >>> result = calculate_dilution(100, 10, 1000)
        >>> print(f"Add {result['stock_volume']} µL stock to {result['diluent_volume']} µL diluent")
    """
    if final_conc > initial_conc:
        raise ValueError("Final concentration cannot exceed initial concentration")

    if initial_conc <= 0 or final_conc <= 0 or final_volume <= 0:
        raise ValueError("All values must be positive")

    # C1 * V1 = C2 * V2
    stock_volume = (final_conc * final_volume) / initial_conc
    diluent_volume = final_volume - stock_volume

    return {
        "stock_volume": round(stock_volume, 2),
        "diluent_volume": round(diluent_volume, 2),
        "final_volume": final_volume,
        "dilution_factor": initial_conc / final_conc,
    }


def create_dilution_series(
    initial_conc: float,
    target_concentrations: List[float],
    final_volume: float = 1000.0,
    concentration_unit: str = "µM",
) -> List[Dict[str, Any]]:
    """
    Create a custom dilution series with specific target concentrations.

    Unlike serial_dilution which uses a constant factor, this function
    allows for arbitrary target concentrations.

    Args:
        initial_conc: Stock concentration.
        target_concentrations: List of desired final concentrations.
        final_volume: Final volume for each dilution.
        concentration_unit: Unit of concentration.

    Returns:
        List of dictionaries with preparation details for each concentration.

    Example:
        >>> series = create_dilution_series(100, [50, 25, 10, 5, 1])
        >>> for point in series:
        ...     print(f"{point['concentration']} {point['unit']}")
    """
    dilutions = []

    for target_conc in sorted(target_concentrations, reverse=True):
        if target_conc > initial_conc:
            raise ValueError(
                f"Target concentration {target_conc} exceeds stock concentration {initial_conc}"
            )

        result = calculate_dilution(initial_conc, target_conc, final_volume)
        result["concentration"] = target_conc
        result["unit"] = concentration_unit
        result["source"] = "stock"
        dilutions.append(result)

    return dilutions


def plate_based_dilution(
    initial_conc: float,
    factor: float = 2.0,
    dilutions: int = 12,
    volume_per_well: float = 100.0,
    concentration_unit: str = "µM",
    format: str = "row",
) -> Dict[str, Any]:
    """
    Generate a dilution series suitable for 96-well plate layout.

    Args:
        initial_conc: Starting concentration.
        factor: Dilution factor at each step.
        dilutions: Number of dilution steps.
        volume_per_well: Final volume in each well.
        concentration_unit: Unit of concentration.
        format: Layout format ("row" for horizontal, "column" for vertical).

    Returns:
        Dictionary with plate layout and preparation instructions.

    Example:
        >>> layout = plate_based_dilution(100, factor=2, dilutions=12)
        >>> print(layout["instructions"])
    """
    # Calculate the dilution series
    series = serial_dilution(
        initial_concentration=initial_conc,
        factor=factor,
        dilutions=dilutions - 1,  # -1 because we count the stock as position 1
        transfer_volume=volume_per_well / factor,
        final_volume=volume_per_well,
        concentration_unit=concentration_unit,
    )

    # Generate plate layout
    if format == "row":
        # Horizontal layout (A1 to A12)
        wells = [f"A{i}" for i in range(1, dilutions + 1)]
    else:
        # Vertical layout (A1 to H1)
        row_labels = "ABCDEFGH"
        wells = [f"{row_labels[i]}1" for i in range(min(dilutions, 8))]

    # Create well assignments
    well_assignments = {}
    for i, (well, conc) in enumerate(zip(wells, series.concentrations)):
        well_assignments[well] = {
            "concentration": conc,
            "unit": concentration_unit,
            "dilution_step": i,
        }

    # Generate preparation instructions
    instructions = [
        f"1. Add {volume_per_well} µL of stock ({initial_conc} {concentration_unit}) to well {wells[0]}",
        f"2. Add {volume_per_well - series.transfer_volume} µL of diluent to wells {wells[1]} through {wells[-1]}",
        f"3. Transfer {series.transfer_volume} µL from each well to the next well",
        f"4. Mix thoroughly after each transfer",
        f"5. Remove {series.transfer_volume} µL from the last well to equalize volumes",
    ]

    return {
        "series": series,
        "wells": wells,
        "well_assignments": well_assignments,
        "format": format,
        "instructions": instructions,
    }
