import pickle
import numpy as np
import pandas as pd
from haversine import haversine

# Load the pickle file
file_path = r"C:\Users\devya\Desktop\OA Travel Itenarary\unique_destinations_with_coordinates.pkl"  # Adjust path
with open(file_path, "rb") as f:
    destinations_data = pickle.load(f)

# Convert data into a dictionary
if isinstance(destinations_data, list):
    destinations_dict = {dest: (lat, lon) for dest, lat, lon in destinations_data if lat is not None and lon is not None}
else:
    destinations_dict = destinations_data

# Get the list of destinations
destinations = list(destinations_dict.keys())

# Initialize an empty distance matrix
num_destinations = len(destinations)
distance_matrix = np.zeros((num_destinations, num_destinations))

# Compute the Haversine distance for each pair
for i in range(num_destinations):
    for j in range(num_destinations):
        if i != j:  # No need to compute distance from a place to itself
            coord1 = destinations_dict[destinations[i]]
            coord2 = destinations_dict[destinations[j]]
            distance_matrix[i, j] = haversine(coord1, coord2)  # Distance in km

# Convert to DataFrame
distance_df = pd.DataFrame(distance_matrix, index=destinations, columns=destinations)

# Save the distance matrix as a CSV file
output_file = r"C:\Users\devya\Desktop\OA Travel Itenarary\distance_matrix.csv"
distance_df.to_csv(output_file)
print(f"Distance matrix saved to {output_file}")
