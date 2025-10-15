'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pandas as pd


def get_geolocator(agent='h501-student'):
    return Nominatim(user_agent=agent)


def fetch_location_data(geolocator, loc):
    """
    Fetches geographical data for a given location string.
    """
    try:
        location = geolocator.geocode(loc, timeout=10)
    except (GeocoderTimedOut, GeocoderServiceError):
        print(f"Error: Geocoding failed for {loc}")
        location = None

    if location is None:
        # Returns the location name with NA values as per Exercise 3
        return {"location": loc, "latitude": pd.NA, "longitude": pd.NA, "type": pd.NA}
    
    # ----------------------------------------------------------------------
    # FIX: Change 'location.geo_type' to 'location.raw['type']'
    # ----------------------------------------------------------------------
    return {"location": loc, 
            "latitude": location.latitude, 
            "longitude": location.longitude, 
            "type": location.raw['type']} # <--- CORRECTED LINE

def build_geo_dataframe(locations, geolocator): 
    """
    Builds a DataFrame from a list of locations using the geolocator.
    """
    geo_data = [fetch_location_data(geolocator, loc) for loc in locations]
    
    df = pd.DataFrame.from_records(geo_data) 
    
    # Ensure correct dtypes in the final output
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    return df


if __name__ == "__main__":
    geolocator = get_geolocator()

    locations = ["Museum of Modern Art", "iuyt8765(*&)", "Alaska", "Franklin's Barbecue", "Burj Khalifa", "asdfqwer1234"]

    df = build_geo_dataframe(locations, geolocator) 

    print(df)
    df.to_csv("./geo_data.csv", index=False)
