import pickle
from geopy.geocoders import Nominatim
import time

# 🔹 Load Unique Destinations (from the previous pickle file)
with open(r"C:\Users\devya\Desktop\OA Travel Itenarary\unique_destinations.pkl", "rb") as f:
    unique_destinations = pickle.load(f)

print(f"✅ Loaded {len(unique_destinations)} unique destinations.")

# 🔹 Initialize Geolocator
geolocator = Nominatim(user_agent="geoapi")

coordinates = []
valid_places = []

# 🔹 Fetch Coordinates and Save to a File
for place in unique_destinations:
    try:
        location = geolocator.geocode(place)
        if location:
            coordinates.append([location.longitude, location.latitude])
            valid_places.append(place)
        else:
            print(f"⚠️ Could not find coordinates for: {place}")
    except Exception as e:
        print(f"❌ Error fetching coordinates for {place}: {e}")
    time.sleep(1.5)  # Avoid hitting rate limits

# 🔹 Save Coordinates to a Pickle File
with open(r"C:\Users\devya\Desktop\OA Travel Itenarary\coordinates.pkl", "wb") as f:
    pickle.dump({'places': valid_places, 'coordinates': coordinates}, f)

print(f"✅ Saved {len(coordinates)} coordinates to 'coordinates.pkl'")
