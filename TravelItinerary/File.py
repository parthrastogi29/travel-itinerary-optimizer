import openrouteservice
import pandas as pd
from geopy.geocoders import Nominatim
import time
import pickle
import numpy as np

# 🔹 STEP 1: Initialize ORS Client (Use Your API Key)
API_KEY = "5b3ce3597851110001cf624850832d51cf4d48ec923ada361a10c30e"
client = openrouteservice.Client(key=API_KEY)

# 🔹 STEP 2: Load Unique Destinations
with open(r"C:\Users\devya\Desktop\OA Travel Itenarary\unique_destinations.pkl", "rb") as f:
    unique_destinations = pickle.load(f)

print(f"✅ Loaded {len(unique_destinations)} unique destinations.")

# 🔹 STEP 3: Convert City Names to Coordinates
geolocator = Nominatim(user_agent="geoapi")
coordinates = []
valid_places = []

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

# 🔹 STEP 4: Split Coordinates into Smaller Chunks (ORS Limit Handling)
def chunk_list(lst, size):
    """Splits a list into smaller chunks of given size."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]

chunk_size = 50  # Maximum places per batch (Adjust as needed)
coordinate_chunks = chunk_list(coordinates, chunk_size)
place_chunks = chunk_list(valid_places, chunk_size)

# 🔹 STEP 5: Fetch Distance Matrices in Chunks
distance_matrices = []

for i, (coord_chunk, place_chunk) in enumerate(zip(coordinate_chunks, place_chunks)):
    try:
        print(f"🔄 Fetching distances for batch {i + 1}/{len(coordinate_chunks)}...")
        result = client.distance_matrix(
            locations=coord_chunk,
            profile="driving-car",
            metrics=["distance"]
        )
        df_chunk = pd.DataFrame(result["distances"], index=place_chunk, columns=place_chunk)
        distance_matrices.append(df_chunk)
    except Exception as e:
        print(f"❌ Error fetching batch {i + 1}: {e}")
    time.sleep(1)  # Avoid hitting ORS API rate limits

# 🔹 STEP 6: Merge All Chunks into One Large Distance Matrix
if distance_matrices:
    final_matrix = pd.concat(distance_matrices, axis=1).fillna(0)  # Merge horizontally
    final_matrix = pd.concat([final_matrix] * len(distance_matrices), axis=0).fillna(0)  # Merge vertically

    # 🔹 Convert Meters to Kilometers
    final_matrix = final_matrix / 1000  # Convert meters to km

    # 🔹 Save Final Distance Matrix
    final_matrix.to_csv("distance_matrix.csv")
    print("✅ Distance matrix saved to 'distance_matrix.csv'")
    print(final_matrix)
else:
    print("❌ No valid distance matrix was created.")
