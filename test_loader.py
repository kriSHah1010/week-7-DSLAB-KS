import unittest
import pandas as pd
import numpy as np
# Import everything needed from loader
from loader import get_geolocator, fetch_location_data, build_geo_dataframe

# Helper function for float comparison
def assert_close(test_case, actual, expected, places=5):
    """Asserts that two float values are close."""
    return test_case.assertAlmostEqual(actual, expected, places=places)

class TestLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up geolocator once for all tests."""
        cls.geolocator = get_geolocator()

    # ------------------------------------------------------------------
    # EXERCISE 2: Test valid locations
    # ------------------------------------------------------------------
    def test_valid_locations(self):
        # Known location data for testing
        known_locations = {
            "Museum of Modern Art": (40.7618552, -73.9782438, "museum"),
            "USS Alabama Battleship Memorial Park": (30.684373, -88.015316, "park")
        }
        
        locations_list = list(known_locations.keys())
        
        # ----------------------------------------------------------------------
        # FIX #1: build_geo_dataframe now takes the geolocator argument.
        # ----------------------------------------------------------------------
        df = build_geo_dataframe(locations_list, self.geolocator) 
        
        self.assertEqual(len(df), len(locations_list), 
                         "DataFrame should contain the correct number of locations.")
        
        # Check coordinates and types for each location
        for loc in locations_list:
            expected_lat, expected_lon, expected_type = known_locations[loc]
            row = df[df['location'] == loc].iloc[0]
            
            assert_close(self, row['latitude'], expected_lat, places=2)
            assert_close(self, row['longitude'], expected_lon, places=2)
            
            self.assertTrue(row['type'].lower().startswith(expected_type),
                            f"Type for {loc} should start with '{expected_type}'. Got: {row['type']}")


    # ------------------------------------------------------------------
    # EXERCISE 3: Test invalid location (No need to change logic, just ensures arguments are passed)
    # ------------------------------------------------------------------
    def test_invalid_location(self):
        # Invalid location string
        invalid_loc = "asdfqwer1234" 
        
        # ----------------------------------------------------------------------
        # FIX #2: fetch_location_data must be called with the geolocator instance.
        # This prevents 'NoneType' error if fetch_location_data fails/returns None
        # in an earlier/broken version, but with the corrected loader.py, 
        # it will return the expected dictionary.
        # ----------------------------------------------------------------------
        result_dict = fetch_location_data(self.geolocator, invalid_loc)

        # 1. Check if the location name is preserved
        self.assertEqual(result_dict.get('location'), invalid_loc, 
                         "The location name must be preserved.")

        # 2. Check for NA/NaN values in coordinates and type
        # Using pd.isna() is the correct way to check for the pd.NA type.
        self.assertTrue(pd.isna(result_dict.get('latitude')), 
                        "Latitude for an invalid location must be NA.")
        self.assertTrue(pd.isna(result_dict.get('longitude')), 
                        "Longitude for an invalid location must be NA.")
        self.assertTrue(pd.isna(result_dict.get('type')), 
                        "Type for an invalid location must be NA.")

if __name__ == "__main__":
    unittest.main()
