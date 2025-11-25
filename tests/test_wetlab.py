# -*- coding: utf-8 -*-
"""Tests for wet lab utilities."""

import unittest
from labrat.wetlab.pcr import (
    calculate_mastermix,
    calculate_tm,
    calculate_primer_concentration,
    generate_qpcr_plate_layout,
    MasterMix,
)
from labrat.wetlab.dilutions import (
    serial_dilution,
    calculate_dilution,
    create_dilution_series,
)
from labrat.wetlab.buffers import (
    get_buffer_recipe,
    calculate_buffer_volume,
    list_buffers,
    COMMON_BUFFERS,
)


class TestMasterMix(unittest.TestCase):
    """Test cases for PCR master mix calculations."""

    def test_calculate_mastermix_basic(self):
        """Test basic master mix calculation."""
        mm = calculate_mastermix(reactions=10, volume=25.0)
        self.assertEqual(mm.reactions, 10)
        self.assertEqual(mm.volume_per_reaction, 25.0)
        self.assertIn("Water", mm.components)
        self.assertIn("10X Buffer", mm.components)

    def test_calculate_mastermix_extra_percent(self):
        """Test master mix with custom extra percentage."""
        mm = calculate_mastermix(reactions=10, volume=25.0, extra_percent=20.0)
        self.assertEqual(mm.extra_percent, 20.0)
        # Total volume should be 10 * 25 * 1.2 = 300
        self.assertAlmostEqual(mm.total_volume, 300.0, places=1)

    def test_calculate_mastermix_high_fidelity(self):
        """Test master mix for high-fidelity polymerase."""
        mm = calculate_mastermix(
            reactions=10, volume=25.0, polymerase_type="high_fidelity"
        )
        self.assertIn("5X HF Buffer", mm.components)
        self.assertIn("HF Polymerase (2 U/µL)", mm.components)

    def test_calculate_mastermix_invalid_polymerase(self):
        """Test that invalid polymerase type raises error."""
        with self.assertRaises(ValueError):
            calculate_mastermix(reactions=10, polymerase_type="invalid")

    def test_mastermix_to_dict(self):
        """Test master mix to_dict method."""
        mm = calculate_mastermix(reactions=5)
        d = mm.to_dict()
        self.assertIn("reactions", d)
        self.assertIn("components", d)
        self.assertEqual(d["reactions"], 5)


class TestMeltingTemperature(unittest.TestCase):
    """Test cases for primer Tm calculations."""

    def test_tm_wallace_method(self):
        """Test Tm calculation using Wallace rule."""
        # Sequence: ATGCATGC (4 AT + 4 GC)
        # Wallace: 2*4 + 4*4 = 8 + 16 = 24
        tm = calculate_tm("ATGCATGC", method="wallace")
        self.assertEqual(tm, 24.0)

    def test_tm_gc_content_method(self):
        """Test Tm calculation using GC content method."""
        tm = calculate_tm("ATGCGATCGATCGATCG", method="gc_content")
        self.assertIsInstance(tm, float)
        self.assertGreater(tm, 0)

    def test_tm_nearest_neighbor_method(self):
        """Test Tm calculation using nearest neighbor method."""
        tm = calculate_tm("ATGCGATCGATCGATCG", method="nearest_neighbor")
        self.assertIsInstance(tm, float)
        self.assertGreater(tm, 0)

    def test_tm_invalid_method(self):
        """Test that invalid method raises error."""
        with self.assertRaises(ValueError):
            calculate_tm("ATGC", method="invalid_method")

    def test_tm_case_insensitive(self):
        """Test that Tm calculation is case insensitive."""
        tm_upper = calculate_tm("ATGCATGC")
        tm_lower = calculate_tm("atgcatgc")
        self.assertEqual(tm_upper, tm_lower)


class TestPrimerConcentration(unittest.TestCase):
    """Test cases for primer concentration calculations."""

    def test_concentration_with_od(self):
        """Test concentration calculation from OD260."""
        conc = calculate_primer_concentration(1.0)
        self.assertIn("uM", conc)
        self.assertIn("nM", conc)
        self.assertGreater(conc["uM"], 0)

    def test_concentration_with_sequence(self):
        """Test concentration calculation with sequence."""
        conc = calculate_primer_concentration(0.5, sequence="ATGCGATCG")
        self.assertIn("uM", conc)
        self.assertGreater(conc["uM"], 0)


class TestQPCRPlateLayout(unittest.TestCase):
    """Test cases for qPCR plate layout generation."""

    def test_generate_layout_basic(self):
        """Test basic plate layout generation."""
        layout = generate_qpcr_plate_layout(
            samples=["Sample1", "Sample2"],
            genes=["GAPDH", "Target1"],
            replicates=3,
        )
        self.assertIn("layout", layout)
        self.assertIn("well_assignments", layout)
        self.assertIn("summary", layout)

    def test_generate_layout_with_ntc(self):
        """Test plate layout includes NTC."""
        layout = generate_qpcr_plate_layout(
            samples=["Sample1"],
            genes=["GAPDH"],
            replicates=3,
            include_ntc=True,
        )
        # Should have 3 sample replicates + 3 NTC replicates = 6 wells
        self.assertEqual(layout["summary"]["wells_used"], 6)

    def test_generate_layout_384_well(self):
        """Test plate layout for 384-well plate."""
        layout = generate_qpcr_plate_layout(
            samples=["Sample1", "Sample2", "Sample3"],
            genes=["Gene1", "Gene2", "Gene3", "Gene4"],
            replicates=3,
            plate_size=384,
        )
        self.assertEqual(len(layout["row_labels"]), 16)
        self.assertEqual(len(layout["col_labels"]), 24)

    def test_generate_layout_capacity_exceeded(self):
        """Test that exceeding plate capacity raises error."""
        with self.assertRaises(ValueError):
            # Too many samples/genes for 96-well plate
            generate_qpcr_plate_layout(
                samples=[f"S{i}" for i in range(20)],
                genes=[f"G{i}" for i in range(10)],
                replicates=3,
            )


class TestSerialDilution(unittest.TestCase):
    """Test cases for serial dilution calculations."""

    def test_serial_dilution_basic(self):
        """Test basic serial dilution series."""
        series = serial_dilution(100, factor=10, dilutions=3)
        self.assertEqual(len(series.concentrations), 4)  # Stock + 3 dilutions
        self.assertEqual(series.concentrations[0], 100)
        self.assertAlmostEqual(series.concentrations[1], 10.0, places=5)
        self.assertAlmostEqual(series.concentrations[2], 1.0, places=5)
        self.assertAlmostEqual(series.concentrations[3], 0.1, places=5)

    def test_serial_dilution_custom_volumes(self):
        """Test serial dilution with custom volumes."""
        series = serial_dilution(
            100, factor=2, dilutions=4, transfer_volume=500, final_volume=1000
        )
        self.assertEqual(series.transfer_volume, 500)
        self.assertEqual(series.final_volume, 1000)

    def test_serial_dilution_invalid_factor(self):
        """Test that invalid dilution factor raises error."""
        with self.assertRaises(ValueError):
            serial_dilution(100, factor=0.5)  # Factor must be > 1

    def test_serial_dilution_to_dict(self):
        """Test serial dilution to_dict method."""
        series = serial_dilution(100, factor=10, dilutions=3)
        d = series.to_dict()
        self.assertIn("concentrations", d)
        self.assertIn("volumes", d)


class TestCalculateDilution(unittest.TestCase):
    """Test cases for single dilution calculations."""

    def test_calculate_dilution_basic(self):
        """Test basic dilution calculation (C1V1 = C2V2)."""
        result = calculate_dilution(100, 10, 1000)
        self.assertEqual(result["stock_volume"], 100.0)
        self.assertEqual(result["diluent_volume"], 900.0)
        self.assertEqual(result["dilution_factor"], 10.0)

    def test_calculate_dilution_fractional(self):
        """Test dilution calculation with fractional values."""
        result = calculate_dilution(50, 12.5, 200)
        self.assertAlmostEqual(result["stock_volume"], 50.0, places=2)
        self.assertAlmostEqual(result["diluent_volume"], 150.0, places=2)

    def test_calculate_dilution_invalid_concentration(self):
        """Test that final > initial concentration raises error."""
        with self.assertRaises(ValueError):
            calculate_dilution(10, 100, 1000)  # Final > Initial


class TestCreateDilutionSeries(unittest.TestCase):
    """Test cases for custom dilution series creation."""

    def test_create_series_basic(self):
        """Test creating custom dilution series."""
        series = create_dilution_series(100, [50, 25, 10, 5])
        self.assertEqual(len(series), 4)
        # Should be sorted in descending order
        self.assertEqual(series[0]["concentration"], 50)
        self.assertEqual(series[3]["concentration"], 5)

    def test_create_series_exceeds_stock(self):
        """Test that target > stock raises error."""
        with self.assertRaises(ValueError):
            create_dilution_series(100, [50, 150])  # 150 > 100


class TestBufferRecipes(unittest.TestCase):
    """Test cases for buffer recipe functions."""

    def test_get_buffer_recipe_pbs(self):
        """Test getting PBS recipe."""
        recipe = get_buffer_recipe("PBS")
        self.assertEqual(recipe.name, "Phosphate Buffered Saline (PBS) 1X")
        self.assertIn("NaCl", recipe.components)
        self.assertEqual(recipe.ph, 7.4)

    def test_get_buffer_recipe_case_insensitive(self):
        """Test that buffer lookup is case insensitive."""
        recipe1 = get_buffer_recipe("PBS")
        recipe2 = get_buffer_recipe("pbs")
        self.assertEqual(recipe1.name, recipe2.name)

    def test_get_buffer_recipe_invalid(self):
        """Test that invalid buffer name raises error."""
        with self.assertRaises(ValueError):
            get_buffer_recipe("INVALID_BUFFER")

    def test_calculate_buffer_volume(self):
        """Test buffer volume scaling."""
        amounts = calculate_buffer_volume("PBS", 500)  # 500 mL
        # NaCl is 8g/L, so 500mL should be 4g
        self.assertAlmostEqual(amounts["NaCl"]["amount"], 4.0, places=2)

    def test_list_buffers(self):
        """Test listing all available buffers."""
        buffers = list_buffers()
        self.assertIn("PBS", buffers)
        self.assertIn("TBS", buffers)
        self.assertIn("TE", buffers)

    def test_buffer_recipe_scale(self):
        """Test recipe scale method."""
        recipe = get_buffer_recipe("PBS")
        scaled = recipe.scale(0.5)  # 500 mL
        self.assertAlmostEqual(scaled["NaCl"]["amount"], 4.0, places=2)


class TestOutputFunctions(unittest.TestCase):
    """Test cases for output/save functions."""

    def setUp(self):
        """Set up test fixtures."""
        import tempfile
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_dated_filename(self):
        """Test dated filename generation."""
        from labrat.wetlab.output import get_dated_filename
        filename = get_dated_filename("test", "txt")
        self.assertTrue(filename.startswith("test_"))
        self.assertTrue(filename.endswith(".txt"))

    def test_save_text_output(self):
        """Test saving text output."""
        from labrat.wetlab.output import save_text_output
        import os
        output_path = os.path.join(self.temp_dir, "test_output.txt")
        path = save_text_output("Test content", output_path=output_path)
        self.assertTrue(path.exists())
        with open(path) as f:
            self.assertEqual(f.read(), "Test content")

    def test_save_csv_output(self):
        """Test saving CSV output."""
        from labrat.wetlab.output import save_csv_output
        import os
        data = [{"name": "A", "value": 1}, {"name": "B", "value": 2}]
        output_path = os.path.join(self.temp_dir, "test_output.csv")
        path = save_csv_output(data, output_path=output_path)
        self.assertTrue(path.exists())

    def test_save_tsv_output(self):
        """Test saving TSV output."""
        from labrat.wetlab.output import save_csv_output
        import os
        data = [{"name": "A", "value": 1}]
        output_path = os.path.join(self.temp_dir, "test_output.tsv")
        path = save_csv_output(data, output_path=output_path, delimiter="\t")
        self.assertTrue(path.exists())

    def test_format_serial_dilution_for_csv(self):
        """Test formatting serial dilution for CSV."""
        from labrat.wetlab.output import format_serial_dilution_for_csv
        series = serial_dilution(100, factor=10, dilutions=2)
        data = format_serial_dilution_for_csv(series)
        self.assertEqual(len(data), 3)  # Stock + 2 dilutions
        self.assertEqual(data[0]["Step"], "Stock")
        self.assertEqual(data[1]["Step"], "D1")

    def test_format_mastermix_for_csv(self):
        """Test formatting mastermix for CSV."""
        from labrat.wetlab.output import format_mastermix_for_csv
        mm = calculate_mastermix(reactions=5)
        data = format_mastermix_for_csv(mm)
        self.assertGreater(len(data), 0)
        # Check that component names are in the data
        component_names = [row.get("Component") for row in data]
        self.assertIn("Water", component_names)

    def test_format_buffer_for_csv(self):
        """Test formatting buffer recipe for CSV."""
        from labrat.wetlab.output import format_buffer_for_csv
        recipe = get_buffer_recipe("PBS")
        data = format_buffer_for_csv(recipe, volume_ml=500)
        self.assertGreater(len(data), 0)
        component_names = [row.get("Component") for row in data]
        self.assertIn("NaCl", component_names)


if __name__ == "__main__":
    unittest.main()
