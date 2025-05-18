import pickle
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Load unique destinations from the pickle file
input_file = r"C:\Users\devya\Desktop\OA Travel Itenarary\unique_destinations.pkl"  # Update path if needed
with open(input_file, "rb") as f:
    unique_destinations = pickle.load(f)

# Initialize Nominatim geolocator with a custom user-agent
geolocator = Nominatim(user_agent="parthrastogi29@gmail.com")  # Replace with your email

# Function to fetch coordinates with retry and delay
def get_coordinates(place):
    try:
        location = geolocator.geocode(place, timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except (GeocoderTimedOut, GeocoderServiceError):
        time.sleep(2)
        return get_coordinates(place)
    except Exception as e:
        print(f"Error fetching {place}: {e}")
        return None
    return None


coordinates_dict = {}
for i, destination in enumerate(unique_destinations):
    time.sleep(1.5)
    coordinates = get_coordinates(destination)
    if coordinates:
        coordinates_dict[destination] = coordinates
    print(f"{i+1}/{len(unique_destinations)}: {destination} -> {coordinates}")
output_file = r"C:\Users\devya\Desktop\OA Travel Itenarary\unique_destinations_with_coordinates.pkl"
with open(output_file, "wb") as f:
    pickle.dump(coordinates_dict, f)

print(f"Coordinates saved to {output_file}")
