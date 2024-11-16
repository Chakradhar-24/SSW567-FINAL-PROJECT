"""
Unit tests for the MRTD class.

This module contains various test cases to verify the functionality
of the MRTD class, including validation of country codes, date formatting,
check digit calculation, and interactions with mock database and hardware methods.
"""

import unittest
from unittest.mock import patch
from MRTD import MRTD

class TestMRTD(unittest.TestCase):
    """Unit tests for the MRTD class methods

    This class contains various test cases to verify the functionality
    of the MRTD class, including validation of country codes, date formatting,
    check digit calculation, and interactions with mock database and hardware methods.
    """

    @classmethod
    def setUpClass(cls):
        """Set up a common instance of MRTD for all test cases."""
        cls.mrtd = MRTD()

    def test_validate_country_code_valid(self):
        """Test validate_country_code with a valid code from the document."""
        self.assertTrue(self.mrtd.validate_country_code("GBD"))

    def test_validate_country_code_invalid(self):
        """Test validate_country_code with an invalid code not in the document."""
        self.assertFalse(self.mrtd.validate_country_code("ZZZ"))

    def test_format_date_of_birth_valid(self):
        """Test format_date_of_birth with a valid date to check YYMMDD format."""
        result = self.mrtd.format_date_of_birth(15, 8, 1975)
        self.assertEqual(result, "750815")

    def test_format_date_of_birth_invalid_day(self):
        """Test format_date_of_birth with an invalid day to verify error handling."""
        with self.assertRaises(ValueError):
            self.mrtd.format_date_of_birth(32, 8, 1975)

    def test_format_date_of_birth_invalid_month(self):
        """Test format_date_of_birth with an invalid month to verify error handling."""
        with self.assertRaises(ValueError):
            self.mrtd.format_date_of_birth(15, 13, 1975)

    def test_format_date_of_birth_invalid_year(self):
        """Test format_date_of_birth with an invalid year (negative) to verify error handling."""
        with self.assertRaises(ValueError):
            self.mrtd.format_date_of_birth(15, 8, -1)

    def test_calculate_check_digit_numeric(self):
        """Test calculate_check_digit with a numeric input string."""
        result = self.mrtd.calculate_check_digit("123456789")
        self.assertEqual(result, 7)  # Updated expected check digit to 7

    def test_calculate_check_digit_alphanumeric(self):
        """Test calculate_check_digit with an alphanumeric input string."""
        result = self.mrtd.calculate_check_digit("A12B34C")
        self.assertEqual(result, 9)  # Updated expected check digit to 9

    def test_calculate_check_digit_with_filler(self):
        """Test calculate_check_digit with filler character '<' in input."""
        result = self.mrtd.calculate_check_digit("123<567<9")
        self.assertEqual(result, 5)  # Updated expected check digit to 5

    @patch('MRTD.MRTD.retrieve_nationality_from_db')
    def test_retrieve_nationality_from_db(self, mock_retrieve):
        """Test retrieve_nationality_from_db with a mocked database response."""
        mock_retrieve.return_value = "GBD"
        self.assertEqual(self.mrtd.retrieve_nationality_from_db(123), "GBD")

    @patch('MRTD.MRTD.scan_hardware_device')
    def test_scan_hardware_device(self, mock_scan):
        """Test scan_hardware_device with a mocked hardware response."""
        mock_scan.return_value = "Sample Data"
        self.assertEqual(self.mrtd.scan_hardware_device(), "Sample Data")


if __name__ == '__main__':
    unittest.main()

