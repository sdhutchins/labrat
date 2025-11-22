import unittest
from pathlib import Path
from labrat.genetics.protein_analysis import dna2aminoacid
import shutil


class TestProteinAnalysis(unittest.TestCase):
    """Test cases for the protein_analysis module."""

    def setUp(self):
        """
        Set up temporary directories and files for testing.
        """
        self.test_dir = Path("./test_protein_analysis")
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """
        Clean up temporary files and directories.
        """
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_dna2aminoacid_simple_sequence(self):
        """
        Test translation of a simple DNA sequence.
        """
        # Create a test FASTA file
        # ATG = M (start/methionine), AAA = K (lysine), TGG = W (tryptophan)
        fasta_file = self.test_dir / "test_simple.fasta"
        fasta_content = ">test_sequence\nATGAAATGG\n"
        fasta_file.write_text(fasta_content)

        result = dna2aminoacid(str(fasta_file))
        self.assertEqual(result, "MKW")

    def test_dna2aminoacid_multiline_sequence(self):
        """
        Test translation of a FASTA sequence split across multiple lines.
        """
        fasta_file = self.test_dir / "test_multiline.fasta"
        fasta_content = ">test_sequence\nATGCGT\nAAGCTA\nTAA\n"
        fasta_file.write_text(fasta_content)

        result = dna2aminoacid(str(fasta_file))
        # ATG=M, CGT=R, AAG=K, CTA=L, TAA=_ (stop codon)
        self.assertEqual(result, "MRKL_")

    def test_dna2aminoacid_with_stop_codon(self):
        """
        Test translation including stop codons.
        """
        fasta_file = self.test_dir / "test_stop.fasta"
        # ATG=M, TAA=_ (stop), TAG=_ (stop), TGA=_ (stop)
        fasta_content = ">test_sequence\nATGTAA\nTAGTGA\n"
        fasta_file.write_text(fasta_content)

        result = dna2aminoacid(str(fasta_file))
        self.assertEqual(result, "M___")

    def test_dna2aminoacid_lowercase_sequence(self):
        """
        Test that lowercase sequences are converted to uppercase.
        """
        fasta_file = self.test_dir / "test_lowercase.fasta"
        fasta_content = ">test_sequence\natgaaatgg\n"
        fasta_file.write_text(fasta_content)

        result = dna2aminoacid(str(fasta_file))
        self.assertEqual(result, "MKW")

    def test_dna2aminoacid_mixed_case_sequence(self):
        """
        Test that mixed case sequences are handled correctly.
        """
        fasta_file = self.test_dir / "test_mixed.fasta"
        fasta_content = ">test_sequence\nAtGaAaTgG\n"
        fasta_file.write_text(fasta_content)

        result = dna2aminoacid(str(fasta_file))
        self.assertEqual(result, "MKW")

    def test_dna2aminoacid_with_whitespace(self):
        """
        Test that whitespace in sequences is properly removed.
        """
        fasta_file = self.test_dir / "test_whitespace.fasta"
        fasta_content = ">test_sequence\nATG AAA TGG\n"
        fasta_file.write_text(fasta_content)

        result = dna2aminoacid(str(fasta_file))
        self.assertEqual(result, "MKW")

    def test_dna2aminoacid_custom_codons(self):
        """
        Test translation with a custom codon dictionary.
        """
        fasta_file = self.test_dir / "test_custom.fasta"
        fasta_content = ">test_sequence\nATGAAATGG\n"
        fasta_file.write_text(fasta_content)

        # Custom codon dictionary where ATG maps to X instead of M
        custom_codons = {
            "ATG": "X",
            "AAA": "K",
            "TGG": "W"
        }

        result = dna2aminoacid(str(fasta_file), codons=custom_codons)
        self.assertEqual(result, "XKW")

    def test_dna2aminoacid_file_not_found(self):
        """
        Test that FileNotFoundError is raised for non-existent files.
        """
        with self.assertRaises(FileNotFoundError):
            dna2aminoacid("nonexistent_file.fasta")

    def test_dna2aminoacid_empty_file(self):
        """
        Test that ValueError is raised for empty FASTA files.
        """
        fasta_file = self.test_dir / "test_empty.fasta"
        fasta_file.write_text(">header_only\n")

        with self.assertRaises(ValueError) as context:
            dna2aminoacid(str(fasta_file))
        
        self.assertIn("No DNA sequence found", str(context.exception))

    def test_dna2aminoacid_invalid_length(self):
        """
        Test that ValueError is raised when sequence length is not a multiple of 3.
        """
        fasta_file = self.test_dir / "test_invalid_length.fasta"
        # Sequence length is 10, not a multiple of 3
        fasta_content = ">test_sequence\nATGCGTAAAG\n"
        fasta_file.write_text(fasta_content)

        with self.assertRaises(ValueError) as context:
            dna2aminoacid(str(fasta_file))
        
        self.assertIn("not a multiple of 3", str(context.exception))

    def test_dna2aminoacid_invalid_codon(self):
        """
        Test that KeyError is raised for invalid codons (containing non-ATGC characters).
        """
        fasta_file = self.test_dir / "test_invalid_codon.fasta"
        # Contains 'N' which is not a valid nucleotide
        fasta_content = ">test_sequence\nATGNGG\n"
        fasta_file.write_text(fasta_content)

        with self.assertRaises(KeyError) as context:
            dna2aminoacid(str(fasta_file))
        
        self.assertIn("Invalid codon", str(context.exception))

    def test_dna2aminoacid_complex_sequence(self):
        """
        Test translation of a longer, more complex sequence.
        """
        fasta_file = self.test_dir / "test_complex.fasta"
        # A longer sequence with various codons (24 nucleotides = 8 codons)
        # ATG=M, CGA=R, GCT=A, GAC=D, GAT=D, GAG=E, GAG=E, GCC=A
        fasta_content = ">test_sequence\nATGCGAGCTGACGATGAGGAGGCC\n"
        fasta_file.write_text(fasta_content)

        result = dna2aminoacid(str(fasta_file))
        # ATG=M, CGA=R, GCT=A, GAC=D, GAT=D, GAG=E, GAG=E, GCC=A
        expected = "MRADDEEA"
        self.assertEqual(result, expected)

    def test_dna2aminoacid_multiple_headers(self):
        """
        Test that multiple header lines are properly skipped.
        """
        fasta_file = self.test_dir / "test_multiple_headers.fasta"
        fasta_content = ">header1\n>header2\nATGAAATGG\n"
        fasta_file.write_text(fasta_content)

        result = dna2aminoacid(str(fasta_file))
        self.assertEqual(result, "MKW")


if __name__ == "__main__":
    unittest.main()
