import pandas as pd

# Update with your local file path
distance_matrix_path = r"C:\Users\devya\Desktop\OA Travel Itenarary\DATA SET\distance_matrix.csv"

# Load the distance matrix
distance_df = pd.read_csv(distance_matrix_path, index_col=0)

# Estimated fuel efficiency (km per liter) and fuel cost per liter
fuel_efficiency_kmpl = 15  # Average car fuel efficiency
fuel_price_per_liter = 100  # ₹100 per liter (adjust based on current fuel price)
toll_cost_per_100km = 50  # Estimated toll cost per 100 km

# Compute on-road travel cost
def calculate_road_cost(distance_km):
    fuel_cost = (distance_km / fuel_efficiency_kmpl) * fuel_price_per_liter
    toll_cost = (distance_km / 100) * toll_cost_per_100km  # Toll cost estimation
    total_cost = fuel_cost + toll_cost
    return total_cost

road_cost_matrix = distance_df.applymap(calculate_road_cost)

# Save the road travel cost matrix
road_fare_path = r"C:\Users\devya\Desktop\OA Travel Itenarary\DATA SET\road_fare_matrix.csv"
road_cost_matrix.to_csv(road_fare_path)

print(f"✅ On-road driving cost matrix saved to {road_fare_path}")
