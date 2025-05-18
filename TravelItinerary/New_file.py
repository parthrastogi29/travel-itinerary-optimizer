import requests

# Your API Key
api_key = "50b90fec41e349eef19f3efff22548a5"

# Sample train details
train_number = "12951"  # Mumbai Rajdhani Express (example)
source_station = "NDLS"  # New Delhi
destination_station = "BCT"  # Mumbai Central
quota = "GN"  # General Quota

# API URL
url = f"http://indianrailapi.com/api/v2/TrainFare/apikey/{api_key}/TrainNumber/{train_number}/From/{source_station}/To/{destination_station}/Quota/{quota}/"

# Send the request
response = requests.get(url)
data = response.json()

# Print the response
print(data)
