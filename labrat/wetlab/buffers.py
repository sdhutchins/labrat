# -*- coding: utf-8 -*-
"""Buffer recipes and preparation utilities for laboratory work."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

import pint

# Initialize unit registry
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


@dataclass
class BufferRecipe:
    """
    Represents a buffer recipe with components and preparation instructions.

    Attributes:
        name: Buffer name.
        components: Dictionary of components and their concentrations.
        ph: Target pH of the buffer.
        notes: Additional preparation notes.

    Example:
        >>> recipe = get_buffer_recipe("PBS")
        >>> print(recipe)
    """

    name: str
    components: Dict[str, Dict[str, Any]]
    ph: Optional[float] = None
    notes: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        """Return a formatted string representation of the buffer recipe."""
        lines = [
            f"Buffer: {self.name}",
            f"pH: {self.ph}" if self.ph else "",
            "-" * 50,
            "Components (per liter):",
        ]
        for component, data in self.components.items():
            amount = data["amount"]
            unit = data["unit"]
            lines.append(f"  {component}: {amount} {unit}")
        if self.notes:
            lines.append("-" * 50)
            lines.append("Notes:")
            for note in self.notes:
                lines.append(f"  - {note}")
        return "\n".join(line for line in lines if line)

    def scale(self, volume_liters: float) -> Dict[str, Dict[str, Any]]:
        """
        Scale the recipe to a different volume.

        Args:
            volume_liters: Target volume in liters.

        Returns:
            Dictionary with scaled component amounts.
        """
        scaled = {}
        for component, data in self.components.items():
            scaled[component] = {
                "amount": data["amount"] * volume_liters,
                "unit": data["unit"],
            }
        return scaled

    def to_dict(self) -> Dict[str, Any]:
        """Return the recipe as a dictionary."""
        return {
            "name": self.name,
            "components": self.components,
            "ph": self.ph,
            "notes": self.notes,
        }


# Common buffer recipes (amounts are per liter)
COMMON_BUFFERS: Dict[str, BufferRecipe] = {
    "PBS": BufferRecipe(
        name="Phosphate Buffered Saline (PBS) 1X",
        components={
            "NaCl": {"amount": 8.0, "unit": "g", "mw": 58.44},
            "KCl": {"amount": 0.2, "unit": "g", "mw": 74.55},
            "Na2HPO4": {"amount": 1.44, "unit": "g", "mw": 141.96},
            "KH2PO4": {"amount": 0.24, "unit": "g", "mw": 136.09},
        },
        ph=7.4,
        notes=[
            "Dissolve in 800 mL of distilled water",
            "Adjust pH to 7.4 with HCl",
            "Bring volume to 1 L with distilled water",
            "Autoclave for sterilization",
        ],
    ),
    "PBS_10X": BufferRecipe(
        name="Phosphate Buffered Saline (PBS) 10X",
        components={
            "NaCl": {"amount": 80.0, "unit": "g", "mw": 58.44},
            "KCl": {"amount": 2.0, "unit": "g", "mw": 74.55},
            "Na2HPO4": {"amount": 14.4, "unit": "g", "mw": 141.96},
            "KH2PO4": {"amount": 2.4, "unit": "g", "mw": 136.09},
        },
        ph=7.4,
        notes=[
            "Dissolve in 800 mL of distilled water",
            "Adjust pH to 7.4 with HCl",
            "Bring volume to 1 L with distilled water",
            "Dilute 1:10 for working solution",
        ],
    ),
    "TBS": BufferRecipe(
        name="Tris Buffered Saline (TBS) 1X",
        components={
            "Tris base": {"amount": 2.42, "unit": "g", "mw": 121.14},
            "NaCl": {"amount": 8.0, "unit": "g", "mw": 58.44},
        },
        ph=7.6,
        notes=[
            "Dissolve in 800 mL of distilled water",
            "Adjust pH to 7.6 with HCl",
            "Bring volume to 1 L with distilled water",
        ],
    ),
    "TBS_10X": BufferRecipe(
        name="Tris Buffered Saline (TBS) 10X",
        components={
            "Tris base": {"amount": 24.2, "unit": "g", "mw": 121.14},
            "NaCl": {"amount": 80.0, "unit": "g", "mw": 58.44},
        },
        ph=7.6,
        notes=[
            "Dissolve in 800 mL of distilled water",
            "Adjust pH to 7.6 with HCl",
            "Bring volume to 1 L with distilled water",
        ],
    ),
    "TBST": BufferRecipe(
        name="Tris Buffered Saline with Tween-20 (TBST)",
        components={
            "Tris base": {"amount": 2.42, "unit": "g", "mw": 121.14},
            "NaCl": {"amount": 8.0, "unit": "g", "mw": 58.44},
            "Tween-20": {"amount": 1.0, "unit": "mL", "mw": None},
        },
        ph=7.6,
        notes=[
            "Dissolve Tris and NaCl in 800 mL of distilled water",
            "Adjust pH to 7.6 with HCl",
            "Add Tween-20 and mix gently",
            "Bring volume to 1 L with distilled water",
        ],
    ),
    "TE": BufferRecipe(
        name="Tris-EDTA (TE) Buffer",
        components={
            "Tris-HCl": {"amount": 1.21, "unit": "g", "mw": 157.6},
            "EDTA": {"amount": 0.37, "unit": "g", "mw": 372.24},
        },
        ph=8.0,
        notes=[
            "Final concentration: 10 mM Tris, 1 mM EDTA",
            "Dissolve in 800 mL of distilled water",
            "Adjust pH to 8.0 with HCl",
            "Bring volume to 1 L with distilled water",
            "Autoclave or filter sterilize",
        ],
    ),
    "TAE_50X": BufferRecipe(
        name="Tris-Acetate-EDTA (TAE) 50X",
        components={
            "Tris base": {"amount": 242.0, "unit": "g", "mw": 121.14},
            "Glacial acetic acid": {"amount": 57.1, "unit": "mL", "mw": 60.05},
            "EDTA (0.5M, pH 8.0)": {"amount": 100.0, "unit": "mL", "mw": 372.24},
        },
        ph=8.3,
        notes=[
            "Add Tris to 600 mL distilled water",
            "Add glacial acetic acid and EDTA solution",
            "Bring volume to 1 L with distilled water",
            "Dilute 1:50 for working solution (1X TAE)",
        ],
    ),
    "TBE_10X": BufferRecipe(
        name="Tris-Borate-EDTA (TBE) 10X",
        components={
            "Tris base": {"amount": 108.0, "unit": "g", "mw": 121.14},
            "Boric acid": {"amount": 55.0, "unit": "g", "mw": 61.83},
            "EDTA": {"amount": 7.44, "unit": "g", "mw": 372.24},
        },
        ph=8.3,
        notes=[
            "Dissolve in 800 mL of distilled water",
            "Bring volume to 1 L with distilled water",
            "No pH adjustment needed",
            "Dilute 1:10 for working solution",
        ],
    ),
    "RIPA": BufferRecipe(
        name="RIPA Lysis Buffer",
        components={
            "NaCl": {"amount": 8.76, "unit": "g", "mw": 58.44},
            "Tris-HCl (1M, pH 8.0)": {"amount": 50.0, "unit": "mL", "mw": 157.6},
            "NP-40": {"amount": 10.0, "unit": "mL", "mw": None},
            "Sodium deoxycholate": {"amount": 5.0, "unit": "g", "mw": 414.55},
            "SDS": {"amount": 1.0, "unit": "g", "mw": 288.38},
        },
        ph=8.0,
        notes=[
            "Final: 150 mM NaCl, 50 mM Tris, 1% NP-40, 0.5% deoxycholate, 0.1% SDS",
            "Add protease inhibitors fresh before use",
            "Keep on ice during use",
        ],
    ),
    "LOADING_6X": BufferRecipe(
        name="6X DNA Loading Buffer",
        components={
            "Bromophenol blue": {"amount": 0.25, "unit": "g", "mw": 691.9},
            "Xylene cyanol FF": {"amount": 0.25, "unit": "g", "mw": 538.6},
            "Glycerol": {"amount": 300.0, "unit": "mL", "mw": 92.09},
        },
        ph=None,
        notes=[
            "Mix components and bring to 1 L with distilled water",
            "Store at 4°C",
            "Use 1 µL per 5 µL of DNA sample",
        ],
    ),
}


def get_buffer_recipe(buffer_name: str) -> BufferRecipe:
    """
    Get a common buffer recipe by name.

    Args:
        buffer_name: Name of the buffer (case-insensitive).
            Options: PBS, PBS_10X, TBS, TBS_10X, TBST, TE, TAE_50X, TBE_10X, RIPA, LOADING_6X

    Returns:
        BufferRecipe object with recipe details.

    Raises:
        ValueError: If buffer name is not recognized.

    Example:
        >>> recipe = get_buffer_recipe("PBS")
        >>> print(recipe)
    """
    buffer_key = buffer_name.upper()
    if buffer_key not in COMMON_BUFFERS:
        available = ", ".join(COMMON_BUFFERS.keys())
        raise ValueError(
            f"Unknown buffer: {buffer_name}. Available buffers: {available}"
        )
    return COMMON_BUFFERS[buffer_key]


def calculate_buffer_volume(
    buffer_name: str,
    volume_ml: float,
) -> Dict[str, Dict[str, float]]:
    """
    Calculate component amounts for a specific volume of buffer.

    Args:
        buffer_name: Name of the buffer.
        volume_ml: Desired volume in milliliters.

    Returns:
        Dictionary with component amounts scaled to the requested volume.

    Example:
        >>> amounts = calculate_buffer_volume("PBS", 500)
        >>> print(amounts)
    """
    recipe = get_buffer_recipe(buffer_name)
    volume_liters = volume_ml / 1000.0
    return recipe.scale(volume_liters)


def list_buffers() -> List[str]:
    """
    List all available buffer recipes.

    Returns:
        List of buffer names.

    Example:
        >>> buffers = list_buffers()
        >>> print(buffers)
    """
    return list(COMMON_BUFFERS.keys())
