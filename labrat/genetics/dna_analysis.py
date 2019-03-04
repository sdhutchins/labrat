"""DNA Analysis functions."""


def ATGC_content(dna_sequence):
    """Returns ATGC contents in the form of a dict."""
    ATGCDict = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
    for nucleotide in dna_sequence:
        try:
            ATGCDict[nucleotide] += 1
        except KeyError:
            pass
    return ATGCDict


def complementary_dna(dna_sequence):
    """Create a complementary DNA sequence."""
    cDNA = []
    complementary = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    for nucleotide in dna_sequence:
        try:
            cDNA.append(complementary[nucleotide])
        except KeyError:
            cDNA.append('X')

    # Return cDNA as string instead of list. Remove if list is prefered
    cDNA = ''.join(cDNA)

    return cDNA
