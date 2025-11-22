"""Protein Analysis functions."""

from pathlib import Path
from labrat.utils import import_json

# Load codon dictionary from JSON file in the same directory
_codons_json_path = Path(__file__).parent / "codons.json"
__codons_dict = import_json(str(_codons_json_path))
CODONS = __codons_dict['CODONS']


def dna2aminoacid(fasta_file: str, codons: dict = None) -> str:
    """
    Convert a DNA sequence from a FASTA file to an amino acid sequence.

    This function reads a FASTA-formatted file, extracts the DNA sequence
    (skipping the header line that starts with '>'), and translates it into
    an amino acid sequence using the genetic code. The sequence is processed
    in groups of three nucleotides (codons), and each codon is looked up in
    the codon dictionary to determine the corresponding amino acid.

    Args:
        fasta_file (str): Path to the FASTA file containing the DNA sequence.
        codons (dict, optional): Dictionary mapping 3-letter DNA codons to
            single-letter amino acid codes. Defaults to the standard genetic code.

    Returns:
        str: The translated amino acid sequence as a single-letter code string.

    Raises:
        FileNotFoundError: If the FASTA file cannot be found.
        KeyError: If an invalid codon (not in the dictionary) is encountered.
        ValueError: If the DNA sequence length is not a multiple of 3.

    Example:
        >>> sequence = dna2aminoacid("sequence.fasta")
        >>> print(sequence)
        MKTAYIAKQR...
    """
    if codons is None:
        codons = CODONS

    # Read and parse the FASTA file
    # FASTA format: first line is a header (starts with '>'), followed by sequence lines
    dna_sequence = ''
    
    try:
        with open(fasta_file, 'r') as file_obj:
            for line in file_obj:
                # Skip header lines (start with '>')
                if line.startswith('>'):
                    continue
                
                # Remove all whitespace and newlines, convert to uppercase
                # FASTA sequences may be split across multiple lines
                # Remove all whitespace characters (spaces, tabs, etc.)
                cleaned_line = ''.join(line.split()).upper()
                dna_sequence += cleaned_line
    except FileNotFoundError:
        raise FileNotFoundError(f"FASTA file not found: {fasta_file}")

    # Validate that we have a sequence
    if not dna_sequence:
        raise ValueError(f"No DNA sequence found in {fasta_file}")

    # Validate sequence length is a multiple of 3 (codons are triplets)
    if len(dna_sequence) % 3 != 0:
        raise ValueError(
            f"DNA sequence length ({len(dna_sequence)}) is not a multiple of 3. "
            "Codons must be complete triplets."
        )

    # Translate DNA sequence to amino acid sequence
    # Process the sequence in groups of 3 nucleotides (codons)
    aa_sequence = ''
    
    for i in range(0, len(dna_sequence), 3):
        # Extract the current codon (3 nucleotides)
        codon = dna_sequence[i:i + 3]
        
        # Look up the codon in the dictionary to get the amino acid
        # Stop codons are represented as '_' in the codon table
        try:
            amino_acid = codons[codon]
            aa_sequence += amino_acid
        except KeyError:
            raise KeyError(
                f"Invalid codon '{codon}' at position {i}-{i+2}. "
                f"Valid codons contain only A, T, G, C."
            )

    return aa_sequence
