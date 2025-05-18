import pandas as pd

# Update with your local file path
distance_matrix_path = r"C:\Users\devya\Desktop\OA Travel Itenarary\DATA SET\distance_matrix.csv"

# Load the distance matrix
distance_df = pd.read_csv(distance_matrix_path, index_col=0)

# Estimated flight fare rate per km (assumed values)
fare_rate_per_km = 5.0  # ₹5 per km (can be adjusted)
min_flight_fare = 1500  # Minimum base fare for any flight

# Compute flight fare matrix
flight_fare_matrix = distance_df * fare_rate_per_km
flight_fare_matrix = flight_fare_matrix.applymap(lambda x: max(x, min_flight_fare))  # Ensure minimum fare

# Save the flight fare matrix
flight_fare_path = r"C:\Users\devya\Desktop\OA Travel Itenarary\DATA SET\flight_fare_matrix.csv"
flight_fare_matrix.to_csv(flight_fare_path)

print(f"✅ Flight fare matrix saved to {flight_fare_path}")
