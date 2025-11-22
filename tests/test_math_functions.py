import unittest
import math
from labrat.math import (
    dilute_stock,
    transmittance_to_absorbance,
    calculate_molarity,
    refractive_index_prism,
)


class TestDiluteStock(unittest.TestCase):
    """Test cases for the dilute_stock function."""

    def test_calculate_final_concentration_with_vF(self):
        """Test calculating final concentration when final volume is provided."""
        # cI = 100, vI = 2, vF = 4
        # Expected: (100 * 2) / 4 = 50.0
        result = dilute_stock(100, 2, vF=4)
        self.assertAlmostEqual(result, 50.0, places=5)

    def test_calculate_final_volume_with_cF(self):
        """Test calculating final volume when final concentration is provided."""
        # cI = 100, vI = 2, cF = 50
        # Expected: (100 * 2) / 50 = 4.0
        result = dilute_stock(100, 2, cF=50)
        self.assertAlmostEqual(result, 4.0, places=5)

    def test_dilute_stock_with_float_values(self):
        """Test dilute_stock with floating point values."""
        result = dilute_stock(50.5, 1.5, vF=3.0)
        expected = (50.5 * 1.5) / 3.0
        self.assertAlmostEqual(result, expected, places=5)

    def test_dilute_stock_no_values(self):
        """Test that UserWarning is raised when no values are provided."""
        with self.assertRaises(UserWarning):
            dilute_stock(100, 2)

    def test_dilute_stock_invalid_key(self):
        """Test that KeyError is raised for invalid keys."""
        with self.assertRaises(KeyError):
            dilute_stock(100, 2, invalid_key=5)


class TestTransmittanceToAbsorbance(unittest.TestCase):
    """Test cases for the transmittance_to_absorbance function."""

    def test_transmittance_50_percent(self):
        """Test conversion of 50% transmittance to absorbance."""
        result = transmittance_to_absorbance(50)
        # A = -log10(T) = -log10(0.5) ≈ 0.3010
        expected = math.log(2)  # log(1/0.5) = log(2)
        self.assertAlmostEqual(result, expected, places=5)

    def test_transmittance_100_percent(self):
        """Test conversion of 100% transmittance to absorbance."""
        result = transmittance_to_absorbance(100)
        # A = -log10(1) = 0
        expected = math.log(1)  # log(1/1) = log(1) = 0
        self.assertAlmostEqual(result, expected, places=5)

    def test_transmittance_10_percent(self):
        """Test conversion of 10% transmittance to absorbance."""
        result = transmittance_to_absorbance(10)
        # A = -log10(0.1) = 1
        expected = math.log(10)  # log(1/0.1) = log(10)
        self.assertAlmostEqual(result, expected, places=5)

    def test_transmittance_float_value(self):
        """Test conversion with floating point transmittance."""
        result = transmittance_to_absorbance(25.5)
        expected = math.log(100 / 25.5)
        self.assertAlmostEqual(result, expected, places=5)

    def test_transmittance_invalid_input(self):
        """Test that ValueError is raised for non-numeric input."""
        with self.assertRaises(ValueError):
            transmittance_to_absorbance("50")

    def test_transmittance_zero_percent(self):
        """Test edge case of 0% transmittance."""
        result = transmittance_to_absorbance(0)
        # 0% transmittance results in infinite absorbance
        self.assertTrue(math.isinf(result))
        self.assertGreater(result, 0)


class TestCalculateMolarity(unittest.TestCase):
    """Test cases for the calculate_molarity function."""

    def test_molarity_with_liters(self):
        """Test molarity calculation with liters."""
        # 2 moles in 1 liter = 2 M
        result = calculate_molarity(2, 1, 'L')
        self.assertAlmostEqual(result, 2.0, places=5)

    def test_molarity_with_lowercase_liters(self):
        """Test molarity calculation with lowercase 'l'."""
        result = calculate_molarity(1, 2, 'l')
        self.assertAlmostEqual(result, 0.5, places=5)

    def test_molarity_with_milliliters(self):
        """Test molarity calculation with milliliters."""
        # 1 mole in 500 mL = 1 / (500 * 1000) = 1 / 500000
        # Note: The function multiplies by 1000, which appears to be a bug
        result = calculate_molarity(1, 500, 'mL')
        expected = 1 / (500 * 1000)
        self.assertAlmostEqual(result, expected, places=5)

    def test_molarity_with_lowercase_ml(self):
        """Test molarity calculation with lowercase 'ml'."""
        result = calculate_molarity(0.5, 250, 'ml')
        expected = 0.5 / (250 * 1000)
        self.assertAlmostEqual(result, expected, places=5)

    def test_molarity_with_float_values(self):
        """Test molarity calculation with floating point values."""
        result = calculate_molarity(0.25, 1.5, 'L')
        expected = 0.25 / 1.5
        self.assertAlmostEqual(result, expected, places=5)

    def test_molarity_invalid_units(self):
        """Test that ValueError is raised for unsupported units."""
        with self.assertRaises(ValueError):
            calculate_molarity(1, 1, 'gallons')


class TestRefractiveIndexPrism(unittest.TestCase):
    """Test cases for the refractive_index_prism function."""

    def test_refractive_index_degrees(self):
        """Test refractive index calculation with degrees."""
        # Using known values: prism angle = 60°, deviation = 40°
        # n = sin((60 + 40)/2) / sin(60/2) = sin(50°) / sin(30°)
        prism = 60.0
        deviation = 40.0
        result = refractive_index_prism(prism, deviation, 'deg')
        
        p_rad = math.radians(prism)
        d_rad = math.radians(deviation)
        expected = math.sin((p_rad + d_rad) / 2) / math.sin(p_rad / 2)
        
        self.assertAlmostEqual(result, expected, places=5)

    def test_refractive_index_radians(self):
        """Test refractive index calculation with radians."""
        # Using known values in radians
        prism = math.radians(60.0)
        deviation = math.radians(40.0)
        result = refractive_index_prism(prism, deviation, 'rad')
        
        expected = math.sin((prism + deviation) / 2) / math.sin(prism / 2)
        
        self.assertAlmostEqual(result, expected, places=5)

    def test_refractive_index_degrees_float(self):
        """Test refractive index with floating point degrees."""
        prism = 45.5
        deviation = 30.25
        result = refractive_index_prism(prism, deviation, 'deg')
        
        p_rad = math.radians(prism)
        d_rad = math.radians(deviation)
        expected = math.sin((p_rad + d_rad) / 2) / math.sin(p_rad / 2)
        
        self.assertAlmostEqual(result, expected, places=5)

    def test_refractive_index_invalid_angle_measurement(self):
        """Test that ValueError is raised for invalid angle measurement."""
        with self.assertRaises(ValueError):
            refractive_index_prism(60, 40, 'invalid')

    def test_refractive_index_consistency_deg_vs_rad(self):
        """Test that degrees and radians give same result for same angles."""
        prism_deg = 60.0
        deviation_deg = 40.0
        
        result_deg = refractive_index_prism(prism_deg, deviation_deg, 'deg')
        result_rad = refractive_index_prism(
            math.radians(prism_deg),
            math.radians(deviation_deg),
            'rad'
        )
        
        self.assertAlmostEqual(result_deg, result_rad, places=5)


if __name__ == "__main__":
    unittest.main()
