"""DNA Analysis functions."""

from typing import Dict


def atgc_content(dna_sequence: str) -> Dict[str, int]:
    """
    Calculate the nucleotide composition of a DNA sequence.

    Counts the occurrences of each nucleotide (A, T, G, C) in the sequence.
    Non-standard nucleotides are ignored in the count.

    Args:
        dna_sequence (str): The DNA sequence to analyze. Case-insensitive.

    Returns:
        dict: A dictionary with keys 'A', 'T', 'G', 'C' and their counts as values.

    Example:
        >>> atgc_content("ATGCGAT")
        {'A': 2, 'T': 2, 'G': 2, 'C': 1}
    """
    if not isinstance(dna_sequence, str):
        raise TypeError(f"Expected str, got {type(dna_sequence).__name__}")

    atgc_dict = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
    dna_sequence_upper = dna_sequence.upper()

    for nucleotide in dna_sequence_upper:
        if nucleotide in atgc_dict:
            atgc_dict[nucleotide] += 1

    return atgc_dict


def complementary_dna(dna_sequence: str) -> str:
    """
    Create the complementary DNA sequence.

    Generates the complementary strand by replacing each nucleotide with its
    complement: A↔T and G↔C. Non-standard nucleotides are replaced with 'X'.

    Args:
        dna_sequence (str): The DNA sequence to complement. Case-insensitive.

    Returns:
        str: The complementary DNA sequence as a string.

    Example:
        >>> complementary_dna("ATGC")
        'TACG'
        >>> complementary_dna("ATGN")
        'TACGX'
    """
    if not isinstance(dna_sequence, str):
        raise TypeError(f"Expected str, got {type(dna_sequence).__name__}")

    complementary_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    dna_sequence_upper = dna_sequence.upper()
    cdna_list = []

    for nucleotide in dna_sequence_upper:
        cdna_list.append(complementary_map.get(nucleotide, 'X'))

    return ''.join(cdna_list)
