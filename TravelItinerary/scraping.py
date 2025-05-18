import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time


# Function to get flight info
def get_flight_info(from_city, to_city, date="19032025"):
    url = f"https://www.ixigo.com/search/result/flight?from={from_city}&to={to_city}&date={date}&adults=1&children=0&infants=0&class=e&source=Search+Form&hbs=true"

    try:
        # Using undetected_chromedriver
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")  # Open browser maximized
        driver = uc.Chrome(options=options)

        print("Opening website...")
        driver.get(url)
        time.sleep(5)  # Wait for page to load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        # Extracting flight details (Modify according to Ixigo's structure)
        flights = soup.find_all("div", class_="container flight-item")

        results = []
        for flight in flights[:2]:  # Fetch only top 2 results
            airline = flight.find("div", class_="airline-name")
            departure = flight.find("div", class_="time-dep")
            arrival = flight.find("div", class_="time-arr")
            price = flight.find("div", class_="price")

            if airline and departure and arrival and price:
                results.append({
                    "Airline": airline.text.strip(),
                    "Departure": departure.text.strip(),
                    "Arrival": arrival.text.strip(),
                    "Price": price.text.strip()
                })

        return results
    except Exception as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    from_city = input("Enter departure city code (e.g., DEL for Delhi): ")
    to_city = input("Enter destination city code (e.g., BOM for Mumbai): ")

    flights = get_flight_info(from_city, to_city)

    if flights:
        print("\nTop Flight Results:")
        for idx, flight in enumerate(flights, 1):
            print(
                f"{idx}. {flight['Airline']} - Dep: {flight['Departure']} | Arr: {flight['Arrival']} | Price: {flight['Price']}")
    else:
        print("No flights found or an error occurred.")