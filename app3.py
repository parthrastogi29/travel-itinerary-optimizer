import streamlit as st
import pandas as pd
import networkx as nx
import pickle
import random
import time
import folium
import os
from streamlit_folium import st_folium

# ------------------ Load Data ------------------
st.set_page_config(page_title="Travel Optimizer", layout="wide", page_icon="🌍")

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "DATA SET")

try:
    distance_matrix = pd.read_csv(f"{DATA_FOLDER}/distance_matrix.csv", index_col=0)
    flight_cost_matrix = pd.read_csv(f"{DATA_FOLDER}/flight_fare_matrix.csv", index_col=0)
    road_cost_matrix = pd.read_csv(f"{DATA_FOLDER}/road_fare_matrix.csv", index_col=0)
    train_classes = ["1A", "2A", "3A", "SL"]
    train_fare_data = {cls: pd.read_csv(f"{DATA_FOLDER}/train_fare_matrix_{cls}.csv", index_col=0) for cls in
                       train_classes}

    df = pd.read_csv(f"{DATA_FOLDER}/final_corrected_data.csv")
    city_coords = pd.read_csv(f"{DATA_FOLDER}/unique_destinations_with_coordinates.csv")

    with open(f"{DATA_FOLDER}/unique_destinations.pkl", 'rb') as f:
        unique_cities = pickle.load(f)
except Exception as e:
    st.error(f"⚠️ Error loading dataset: {e}")
    st.stop()

# Fill NaN values
for matrix in [distance_matrix, flight_cost_matrix, road_cost_matrix] + list(train_fare_data.values()):
    matrix.fillna(0, inplace=True)

# Convert city coordinates into a dictionary
city_location = {row["Destination"]: (row["Latitude"], row["Longitude"]) for _, row in city_coords.iterrows()}

# Process sightseeing data
df['Destination'] = df['Destination'].astype(str).apply(lambda x: [city.strip() for city in x.split('|')])
df['Sightseeing Places Covered'] = df['Sightseeing Places Covered'].astype(str).apply(
    lambda x: [place.strip() for place in x.split('|') if place.strip().lower() != 'nan' and 'bus' not in place.lower()]
)

city_to_places = {}
for _, row in df.iterrows():
    for city in row['Destination']:
        if city in unique_cities:
            if city not in city_to_places:
                city_to_places[city] = set()
            city_to_places[city].update(row['Sightseeing Places Covered'])


def recommend_places(selected_cities, min_places=5, max_places=7):
    recommended_places = set()
    for city in selected_cities:
        if city in city_to_places:
            recommended_places.update(city_to_places[city])
    recommended_places = list(recommended_places)
    random.shuffle(recommended_places)
    return recommended_places[:random.randint(min_places, max_places)]


# ------------------ Streamlit UI ------------------
st.title("🌍 Travel Itinerary Optimization System")
st.markdown("✈️ Plan your multi-city trip with **optimal routes & cost analysis**!")

# Sidebar Inputs
st.sidebar.header("🗺️ Trip Planning")
destinations = st.sidebar.multiselect("Select Your Destinations:", list(distance_matrix.index))

if len(destinations) > 1:
    col1, col2 = st.columns([2, 3])  # Creating two columns for better layout

    with col1:
        st.subheader("🚀 Optimized Route")
        G = nx.Graph()
        for city1 in destinations:
            for city2 in destinations:
                if city1 != city2:
                    G.add_edge(city1, city2, weight=distance_matrix.loc[city1, city2])
        optimized_route = nx.approximation.traveling_salesman_problem(G, cycle=False)
        st.write(" → ".join(optimized_route))

        # Progress Bar for UI Enhancement
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        progress_bar.empty()  # Clear the progress bar after completion

    with col2:
        with st.expander("🏛️ Recommended Sightseeing Places", expanded=True):
            recommendations = recommend_places(optimized_route)
            if recommendations:
                for place in recommendations:
                    st.write(f"- {place}")
            else:
                st.write("No recommendations available for the selected cities.")

    # Travel Mode Selection
    st.sidebar.subheader("🚆✈️🚗 Choose Travel Modes")
    travel_modes = {}
    train_classes_selected = {}

    for i in range(len(optimized_route) - 1):
        from_city, to_city = optimized_route[i], optimized_route[i + 1]
        mode = st.sidebar.selectbox(f"Mode of travel from **{from_city}** to **{to_city}**:",
                                    ["Train", "Flight", "Driving"], key=f"mode_{i}")
        travel_modes[(from_city, to_city)] = mode
        if mode == "Train":
            train_class = st.sidebar.selectbox(f"Train Class from {from_city} to {to_city}", train_classes,
                                               key=f"class_{i}")
            train_classes_selected[(from_city, to_city)] = train_class

    # Cost Calculation
    st.subheader("📊 Optimized Route & Cost Breakdown")
    trip_summary = []
    total_cost = 0

    for (from_city, to_city), mode in travel_modes.items():
        cost = 0
        try:
            if mode == "Train":
                train_class = train_classes_selected[(from_city, to_city)]
                cost = train_fare_data[train_class].loc[from_city, to_city] if train_class else 0
            elif mode == "Flight":
                cost = flight_cost_matrix.loc[from_city, to_city]
            elif mode == "Driving":
                cost = road_cost_matrix.loc[from_city, to_city]
        except KeyError:
            st.error(f"⚠️ No travel cost data found for {from_city} to {to_city}. Skipping...")
            continue

        trip_summary.append([from_city, to_city, mode, f"₹{cost:,.2f}"])
        total_cost += cost

    summary_df = pd.DataFrame(trip_summary, columns=["From", "To", "Mode", "Cost"])
    st.dataframe(summary_df, use_container_width=True)

    st.success(f"💰 Estimated Total Travel Cost: **₹{total_cost:,.2f}**")

    # Cost Breakdown Visualization
    if not summary_df.empty:
        st.subheader("📉 Cost Distribution by Mode")
        cost_chart = summary_df.groupby("Mode")["Cost"].sum().reset_index()
        st.bar_chart(cost_chart.set_index("Mode"))

    # ------------------ Folium Map ------------------
    st.subheader("🌍 Interactive Travel Route Map")

    # Center map around the first selected city
    first_city = optimized_route[0]
    map_center = city_location.get(first_city, (20.5937, 78.9629))  # Default to India’s center if not found

    m = folium.Map(location=map_center, zoom_start=5, tiles="OpenStreetMap")

    # Add markers for each city
    for city in optimized_route:
        if city in city_location:
            lat, lon = city_location[city]
            folium.Marker([lat, lon], tooltip=city, icon=folium.Icon(color="blue")).add_to(m)

    # Draw travel route
    route_coords = [city_location[city] for city in optimized_route if city in city_location]
    folium.PolyLine(route_coords, color="red", weight=4, opacity=0.7).add_to(m)

    # Display map in Streamlit
    st_folium(m, width=800, height=500)

    st.toast("✅ Your optimized travel plan is ready! 🚀")

else:
    st.warning("⚠️ Please select at least **two destinations** to plan your trip.")
