import requests

API_KEY = "8c4f0d149cf503973c5192b1ad37ba9593bdec6b"

def fetch_weather_data(city_name, lat, lon):
    url = "https://api.gribstream.com/v1/data"
    params = {
        "model": "gfs",
        "lat": lat,
        "lon": lon,
        "parameters": "temp,wind,rain",
        "apikey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"\n🌍 {city_name}")
        print("✅ Response received!")
        print(data)
    except requests.exceptions.HTTPError as errh:
        print(f"❌ HTTP Error for {city_name}:", errh)
    except requests.exceptions.ConnectionError as errc:
        print(f"❌ Connection Error for {city_name}:", errc)
    except requests.exceptions.Timeout as errt:
        print(f"❌ Timeout Error for {city_name}:", errt)
    except requests.exceptions.RequestException as err:
        print(f"❌ Other Error for {city_name}:", err)

# City coordinates
cities = {
    "New Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707),
    "Jaipur": (26.9124, 75.7873),
    "Goa": (15.2993, 74.1240)
}

for city, coords in cities.items():
    fetch_weather_data(city, coords[0], coords[1])
