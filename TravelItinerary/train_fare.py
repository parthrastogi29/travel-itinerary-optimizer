import pandas as pd

# Update with your local file path
distance_matrix_path = r"C:\Users\devya\Desktop\OA Travel Itenarary\DATA SET\distance_matrix.csv"

# Load the distance matrix
distance_df = pd.read_csv(distance_matrix_path, index_col=0)

# Train fare rate per km (assumed values)
fare_rates = {
    "SL": 0.50,  # Sleeper
    "3A": 1.25,  # AC 3-Tier
    "2A": 2.00,  # AC 2-Tier
    "1A": 3.50   # AC 1-Tier
}

# Minimum fare for each class
min_fare = {
    "SL": 50,
    "3A": 100,
    "2A": 150,
    "1A": 250
}

# Create fare matrices for each class
fare_matrices = {}
for class_type, rate in fare_rates.items():
    fare_matrix = distance_df * rate
    fare_matrix = fare_matrix.applymap(lambda x: max(x, min_fare[class_type]))  # Ensure minimum fare
    fare_matrices[class_type] = fare_matrix

# Save the matrices
for class_type, fare_matrix in fare_matrices.items():
    file_path = rf"C:\Users\devya\Desktop\OA Travel Itenarary\DATA SET\train_fare_matrix_{class_type}.csv"
    fare_matrix.to_csv(file_path)
    print(f"✅ Train fare matrix for {class_type} saved to {file_path}")
