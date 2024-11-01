import streamlit as st
from geopy.distance import geodesic
from streamlit_folium import st_folium
import folium

def show():
    st.title("Calculate Distance Between Locations")

    # Check if there are any locations in session state
    if 'locations' not in st.session_state or len(st.session_state['locations']) < 2:
        st.write("At least two locations are required. Please add more locations on the Data Entry page.")
        return

    # Select two locations for distance calculation
    location_names = [loc['name'] for loc in st.session_state['locations']]
    loc1_name = st.selectbox("Select Start Location", location_names)
    loc2_name = st.selectbox("Select End Location", location_names)

    # Retrieve the selected locations' data
    loc1 = next(loc for loc in st.session_state['locations'] if loc['name'] == loc1_name)
    loc2 = next(loc for loc in st.session_state['locations'] if loc['name'] == loc2_name)

    # Calculate the distance using geodesic from geopy
    loc1_coords = (loc1["lat"], loc1["lon"])
    loc2_coords = (loc2["lat"], loc2["lon"])
    distance = geodesic(loc1_coords, loc2_coords).kilometers
    st.write(f"Distance between {loc1_name} and {loc2_name}: {distance:.2f} km")

    # Initialize map centered between the two locations
    midpoint = [(loc1["lat"] + loc2["lat"]) / 2, (loc1["lon"] + loc2["lon"]) / 2]
    m = folium.Map(location=midpoint, zoom_start=14)

    # Add markers for the start and end locations
    folium.Marker(
        location=loc1_coords, popup=f"<b>{loc1_name}</b>", tooltip="Start Location", icon=folium.Icon(color="blue")
    ).add_to(m)
    folium.Marker(
        location=loc2_coords, popup=f"<b>{loc2_name}</b>", tooltip="End Location", icon=folium.Icon(color="red")
    ).add_to(m)

    # Draw a line (route) between the two locations
    folium.PolyLine([loc1_coords, loc2_coords], color="blue", weight=2.5, opacity=1).add_to(m)

    # Display the map with the route
    st_folium(m, width="100%", height=500)
