# -*- coding: utf-8 -*-
"""Science and laboratory glossary terms."""

from typing import Any, Dict, List, Optional

# Science and Lab Glossary
GLOSSARY: Dict[str, Dict[str, Any]] = {
    # Molecular Biology
    "PCR": {
        "term": "Polymerase Chain Reaction (PCR)",
        "abbreviation": "PCR",
        "definition": "A method used to rapidly make millions to billions of copies of a specific DNA sample, allowing scientists to take a very small sample of DNA and amplify it to a large enough amount to study in detail.",
        "category": "molecular_biology",
        "related": ["qPCR", "RT-PCR", "primer", "Taq polymerase"],
    },
    "qPCR": {
        "term": "Quantitative PCR (qPCR)",
        "abbreviation": "qPCR",
        "definition": "A laboratory technique of molecular biology based on the polymerase chain reaction (PCR) that monitors the amplification of a targeted DNA molecule during the PCR in real-time, allowing quantification of the starting amount of DNA.",
        "category": "molecular_biology",
        "related": ["PCR", "Ct value", "amplification curve", "SYBR Green"],
    },
    "RT-PCR": {
        "term": "Reverse Transcription PCR (RT-PCR)",
        "abbreviation": "RT-PCR",
        "definition": "A laboratory technique combining reverse transcription of RNA into DNA with amplification of specific DNA targets using PCR. Used to detect and quantify RNA.",
        "category": "molecular_biology",
        "related": ["PCR", "qPCR", "cDNA", "reverse transcriptase"],
    },
    "primer": {
        "term": "Primer",
        "definition": "A short strand of RNA or DNA (generally about 18-22 bases) that serves as a starting point for DNA synthesis. Required for DNA replication because DNA polymerases can only add new nucleotides to an existing strand of DNA.",
        "category": "molecular_biology",
        "related": ["PCR", "Tm", "annealing", "DNA synthesis"],
    },
    "Tm": {
        "term": "Melting Temperature (Tm)",
        "abbreviation": "Tm",
        "definition": "The temperature at which 50% of the DNA molecules are in double-stranded form and 50% are in single-stranded form. Important for PCR primer design.",
        "category": "molecular_biology",
        "related": ["primer", "annealing", "GC content", "PCR"],
    },
    "annealing": {
        "term": "Annealing",
        "definition": "The process where two complementary single-stranded DNA or RNA molecules base pair to form a double-stranded molecule. In PCR, it refers to the step where primers bind to template DNA.",
        "category": "molecular_biology",
        "related": ["Tm", "primer", "PCR", "hybridization"],
    },
    "denaturation": {
        "term": "Denaturation",
        "definition": "The process of disrupting the hydrogen bonds that hold the two DNA strands together, causing them to separate into single strands. Occurs at high temperatures (94-98°C) in PCR.",
        "category": "molecular_biology",
        "related": ["PCR", "annealing", "extension"],
    },
    "extension": {
        "term": "Extension",
        "definition": "The PCR step where DNA polymerase synthesizes new DNA strands complementary to the template strands. Typically occurs at 72°C for Taq polymerase.",
        "category": "molecular_biology",
        "related": ["PCR", "Taq polymerase", "denaturation", "annealing"],
    },
    "Taq polymerase": {
        "term": "Taq Polymerase",
        "definition": "A thermostable DNA polymerase isolated from Thermus aquaticus, a bacterium that lives in hot springs. Essential for PCR as it can withstand the high temperatures used to denature DNA.",
        "category": "molecular_biology",
        "related": ["PCR", "extension", "hot start"],
    },
    "cDNA": {
        "term": "Complementary DNA (cDNA)",
        "abbreviation": "cDNA",
        "definition": "DNA synthesized from a single-stranded RNA template in a reaction catalyzed by reverse transcriptase. Represents the expressed genes in a cell.",
        "category": "molecular_biology",
        "related": ["mRNA", "reverse transcriptase", "RT-PCR"],
    },
    # Genetics
    "SNP": {
        "term": "Single Nucleotide Polymorphism (SNP)",
        "abbreviation": "SNP",
        "definition": "A variation in a single nucleotide that occurs at a specific position in the genome. SNPs are the most common type of genetic variation among people.",
        "category": "genetics",
        "related": ["variant", "mutation", "polymorphism", "allele"],
    },
    "indel": {
        "term": "Insertion/Deletion (Indel)",
        "abbreviation": "Indel",
        "definition": "A type of genetic variation where nucleotides are either inserted or deleted from the genome. Can range from a single base pair to thousands of base pairs.",
        "category": "genetics",
        "related": ["SNP", "variant", "frameshift"],
    },
    "allele": {
        "term": "Allele",
        "definition": "One of two or more versions of a gene. An individual inherits two alleles for each gene, one from each parent.",
        "category": "genetics",
        "related": ["gene", "heterozygous", "homozygous", "genotype"],
    },
    "genotype": {
        "term": "Genotype",
        "definition": "The genetic constitution of an individual organism, often referring to the specific combination of alleles at a particular locus or set of loci.",
        "category": "genetics",
        "related": ["phenotype", "allele", "heterozygous", "homozygous"],
    },
    "phenotype": {
        "term": "Phenotype",
        "definition": "The observable physical properties of an organism, including appearance, development, and behavior. Results from the interaction of genotype and environment.",
        "category": "genetics",
        "related": ["genotype", "trait", "expression"],
    },
    "heterozygous": {
        "term": "Heterozygous",
        "definition": "Having two different alleles of a particular gene at a given locus on homologous chromosomes.",
        "category": "genetics",
        "related": ["homozygous", "allele", "genotype"],
    },
    "homozygous": {
        "term": "Homozygous",
        "definition": "Having two identical alleles of a particular gene at a given locus on homologous chromosomes.",
        "category": "genetics",
        "related": ["heterozygous", "allele", "genotype"],
    },
    # Bioinformatics
    "FASTA": {
        "term": "FASTA Format",
        "definition": "A text-based format for representing nucleotide or amino acid sequences. Each sequence begins with a single-line description (starting with '>'), followed by lines of sequence data.",
        "category": "bioinformatics",
        "related": ["FASTQ", "sequence alignment", "BLAST"],
    },
    "FASTQ": {
        "term": "FASTQ Format",
        "definition": "A text-based format for storing both biological sequence data and quality scores. Used for storing the output of high-throughput sequencing instruments.",
        "category": "bioinformatics",
        "related": ["FASTA", "quality score", "Phred score", "NGS"],
    },
    "BAM": {
        "term": "Binary Alignment Map (BAM)",
        "abbreviation": "BAM",
        "definition": "The compressed binary version of the Sequence Alignment Map (SAM) format, used for storing sequence alignment data.",
        "category": "bioinformatics",
        "related": ["SAM", "alignment", "NGS", "read mapping"],
    },
    "SAM": {
        "term": "Sequence Alignment Map (SAM)",
        "abbreviation": "SAM",
        "definition": "A tab-delimited text format for storing sequence alignment data. Contains header lines and alignment lines describing mapped reads.",
        "category": "bioinformatics",
        "related": ["BAM", "alignment", "CIGAR string"],
    },
    "VCF": {
        "term": "Variant Call Format (VCF)",
        "abbreviation": "VCF",
        "definition": "A text file format for storing gene sequence variations. Contains meta-information lines, a header line, and data lines containing information about a position in the genome.",
        "category": "bioinformatics",
        "related": ["variant calling", "SNP", "indel", "genotype"],
    },
    "NGS": {
        "term": "Next-Generation Sequencing (NGS)",
        "abbreviation": "NGS",
        "definition": "High-throughput sequencing technologies that allow rapid sequencing of DNA or RNA. Includes Illumina sequencing, Ion Torrent, and PacBio platforms.",
        "category": "bioinformatics",
        "related": ["whole genome sequencing", "exome sequencing", "FASTQ"],
    },
    # Biochemistry
    "buffer": {
        "term": "Buffer",
        "definition": "A solution that resists changes in pH when small quantities of acid or base are added. Essential for maintaining proper pH in biological experiments.",
        "category": "biochemistry",
        "related": ["PBS", "TBS", "Tris", "pH"],
    },
    "PBS": {
        "term": "Phosphate Buffered Saline (PBS)",
        "abbreviation": "PBS",
        "definition": "A buffer solution commonly used in biological research. It is a water-based salt solution containing sodium chloride, disodium hydrogen phosphate, potassium dihydrogen phosphate, and potassium chloride.",
        "category": "biochemistry",
        "related": ["buffer", "TBS", "isotonic"],
    },
    "TBS": {
        "term": "Tris Buffered Saline (TBS)",
        "abbreviation": "TBS",
        "definition": "A buffer solution used in molecular biology and biochemistry, containing Tris base and sodium chloride. Often used as a wash buffer in Western blotting.",
        "category": "biochemistry",
        "related": ["buffer", "PBS", "TBST"],
    },
    "Tris": {
        "term": "Tris (Trisaminomethane)",
        "definition": "A common buffer component (tris(hydroxymethyl)aminomethane) used in biochemistry and molecular biology. Has a pKa of approximately 8.1 at 25°C.",
        "category": "biochemistry",
        "related": ["buffer", "TBS", "TE buffer"],
    },
    "EDTA": {
        "term": "Ethylenediaminetetraacetic Acid (EDTA)",
        "abbreviation": "EDTA",
        "definition": "A chelating agent that binds metal ions, particularly divalent cations like Mg2+ and Ca2+. Used to inhibit metalloproteases and nucleases in molecular biology.",
        "category": "biochemistry",
        "related": ["chelating agent", "TE buffer", "anticoagulant"],
    },
    "molarity": {
        "term": "Molarity (M)",
        "abbreviation": "M",
        "definition": "A unit of concentration equal to the number of moles of a solute per liter of solution. Also called molar concentration.",
        "category": "biochemistry",
        "related": ["concentration", "mole", "dilution"],
    },
    "dilution": {
        "term": "Dilution",
        "definition": "The process of reducing the concentration of a solute in a solution, usually by mixing with more solvent. Calculated using C1V1 = C2V2.",
        "category": "biochemistry",
        "related": ["serial dilution", "molarity", "concentration"],
    },
    "serial dilution": {
        "term": "Serial Dilution",
        "definition": "A stepwise dilution of a substance in solution, where each step dilutes by a constant factor. Used to create a range of concentrations for standard curves or dose-response experiments.",
        "category": "biochemistry",
        "related": ["dilution", "standard curve", "dilution factor"],
    },
    # Cell Biology
    "cell culture": {
        "term": "Cell Culture",
        "definition": "The process of growing cells under controlled conditions, generally outside their natural environment. Includes primary cells and immortalized cell lines.",
        "category": "cell_biology",
        "related": ["passage", "confluency", "media", "FBS"],
    },
    "passage": {
        "term": "Passage",
        "definition": "The transfer of cells from one culture vessel to another. Passage number indicates how many times cells have been subcultured.",
        "category": "cell_biology",
        "related": ["cell culture", "subculture", "confluency"],
    },
    "confluency": {
        "term": "Confluency",
        "definition": "The percentage of the surface area of a culture vessel covered by cells. 100% confluency means cells completely cover the surface.",
        "category": "cell_biology",
        "related": ["cell culture", "passage", "growth phase"],
    },
    "transfection": {
        "term": "Transfection",
        "definition": "The process of introducing nucleic acids (DNA or RNA) into eukaryotic cells. Can be transient or stable.",
        "category": "cell_biology",
        "related": ["transformation", "lipofection", "electroporation"],
    },
    "transformation": {
        "term": "Transformation",
        "definition": "The genetic alteration of a cell by uptake of exogenous DNA. In bacteria, refers to the process of introducing plasmid DNA into competent cells.",
        "category": "cell_biology",
        "related": ["transfection", "competent cells", "plasmid"],
    },
    # Protein Analysis
    "Western blot": {
        "term": "Western Blot",
        "definition": "A technique used to detect specific proteins in a sample. Involves separating proteins by gel electrophoresis, transferring to a membrane, and detecting with specific antibodies.",
        "category": "protein_analysis",
        "related": ["SDS-PAGE", "antibody", "transfer", "blocking"],
    },
    "SDS-PAGE": {
        "term": "Sodium Dodecyl Sulfate Polyacrylamide Gel Electrophoresis",
        "abbreviation": "SDS-PAGE",
        "definition": "A technique used to separate proteins based on their molecular weight. SDS denatures proteins and gives them a uniform negative charge.",
        "category": "protein_analysis",
        "related": ["Western blot", "gel electrophoresis", "molecular weight"],
    },
    "ELISA": {
        "term": "Enzyme-Linked Immunosorbent Assay (ELISA)",
        "abbreviation": "ELISA",
        "definition": "A plate-based assay technique for detecting and quantifying substances such as proteins, antibodies, and hormones. Uses enzyme-linked antibodies for detection.",
        "category": "protein_analysis",
        "related": ["antibody", "immunoassay", "colorimetric detection"],
    },
    # Statistics
    "p-value": {
        "term": "P-value",
        "definition": "The probability of obtaining test results at least as extreme as the observed results, assuming the null hypothesis is correct. A low p-value (typically ≤ 0.05) indicates statistical significance.",
        "category": "statistics",
        "related": ["significance", "null hypothesis", "alpha"],
    },
    "fold change": {
        "term": "Fold Change",
        "definition": "A measure describing how much a quantity changes between two conditions. Calculated as the ratio of the final value to the initial value.",
        "category": "statistics",
        "related": ["differential expression", "log2 fold change"],
    },
    "standard deviation": {
        "term": "Standard Deviation",
        "abbreviation": "SD",
        "definition": "A measure of the amount of variation or dispersion of a set of values. A low standard deviation indicates values tend to be close to the mean.",
        "category": "statistics",
        "related": ["variance", "mean", "standard error"],
    },
    "standard error": {
        "term": "Standard Error (SE)",
        "abbreviation": "SE",
        "definition": "The standard deviation of the sampling distribution of a statistic. Indicates how precise the sample mean is as an estimate of the population mean.",
        "category": "statistics",
        "related": ["standard deviation", "confidence interval", "mean"],
    },
}


def lookup_term(term: str) -> Optional[Dict[str, Any]]:
    """
    Look up a term in the glossary.

    Args:
        term: The term to look up (case-insensitive).

    Returns:
        Dictionary with term information, or None if not found.

    Example:
        >>> result = lookup_term("PCR")
        >>> print(result['definition'])
    """
    # First try exact match (case-insensitive)
    term_lower = term.lower()
    for key, value in GLOSSARY.items():
        if key.lower() == term_lower:
            return value
        # Also check the full term name
        if value.get("term", "").lower() == term_lower:
            return value
        # Check abbreviation
        if value.get("abbreviation", "").lower() == term_lower:
            return value

    return None


def search_glossary(
    query: str,
    category: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search the glossary for terms matching a query.

    Args:
        query: Search query string.
        category: Optional category filter.

    Returns:
        List of matching term dictionaries.

    Example:
        >>> results = search_glossary("DNA")
        >>> for r in results:
        ...     print(r['term'])
    """
    query_lower = query.lower()
    results = []

    for key, value in GLOSSARY.items():
        # Filter by category if specified
        if category and value.get("category", "").lower() != category.lower():
            continue

        # Search in term name, abbreviation, definition, and related terms
        searchable = " ".join(
            [
                key,
                value.get("term", ""),
                value.get("abbreviation", ""),
                value.get("definition", ""),
                " ".join(value.get("related", [])),
            ]
        ).lower()

        if query_lower in searchable:
            results.append(value)

    return results


def list_categories() -> List[str]:
    """
    List all glossary categories.

    Returns:
        List of category names.

    Example:
        >>> categories = list_categories()
        >>> print(categories)
    """
    categories = set()
    for value in GLOSSARY.values():
        if "category" in value:
            categories.add(value["category"])
    return sorted(list(categories))


def get_terms_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Get all terms in a specific category.

    Args:
        category: Category name.

    Returns:
        List of term dictionaries in the category.

    Example:
        >>> terms = get_terms_by_category("molecular_biology")
        >>> for t in terms:
        ...     print(t['term'])
    """
    category_lower = category.lower()
    return [
        value
        for value in GLOSSARY.values()
        if value.get("category", "").lower() == category_lower
    ]
