import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import requests
from io import StringIO

# Define the CSV file path
# DATA_FILE = 'https://raw.githubusercontent.com/MyoMinKo1011/gis/refs/heads/main/gis_project/locations_data.csv'


def load_data():
    """Load data from the CSV file into a DataFrame."""
    url = 'https://raw.githubusercontent.com/MyoMinKo1011/gis/refs/heads/main/gis_project/locations_data.csv'
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text))
        return df
    else:
        return pd.DataFrame(columns=["name", "lat", "lon", "type", "details"])

def show_dashboard():
    st.title("Archaeological Database Management System with GIS Integrations")
    st.markdown(
        """
        <style>
            .header {
                font-size: 2.5em;
                color: #4B0082;
                text-align: center;
                margin: 20px 0;
            }
            .metric {
                text-align: center;
                font-size: 1.5em;
                margin: 10px 0;
            }
            .section-title {
                margin-top: 30px;
                font-size: 1.75em;
                color: #4B0082;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    locations_df = load_data()

    # Overview Statistics
    st.markdown("<div class='header'>Overview Statistics</div>", unsafe_allow_html=True)
    total_locations = len(locations_df)
    excavated_sites = len(locations_df[locations_df['type'] == 'Excavated Site'])
    monument_sites = len(locations_df[locations_df['type'] == 'Monument Site'])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Locations", total_locations)
    with col2:
        st.metric("Excavated Sites", excavated_sites)
    with col3:
        st.metric("Monument Sites", monument_sites)

    # Recent Activity
    st.markdown("<div class='section-title'>Recent Activity</div>", unsafe_allow_html=True)
    if total_locations > 0:
        recent_activity = locations_df.tail(5)  # Last 5 entries
        st.table(recent_activity[['name', 'type', 'lat', 'lon']])
    else:
        st.write("No recent activity available.")

    # Location Types Breakdown
    st.markdown("<div class='section-title'>Location Types Breakdown</div>", unsafe_allow_html=True)
    type_counts = locations_df['type'].value_counts()
    if not type_counts.empty:
        fig, ax = plt.subplots()
        type_counts.plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e'])
        ax.set_ylabel("Number of Locations")
        ax.set_title("Distribution of Location Types")
        st.pyplot(fig)
    else:
        st.write("No location types available to display.")

    # Map to get current location (click to get lat/lon)
    st.markdown("<div class='section-title'>Click on the Map to Get Coordinates</div>", unsafe_allow_html=True)
    if total_locations > 0:
        mean_lat = locations_df['lat'].mean()
        mean_lon = locations_df['lon'].mean()
        m = folium.Map(location=[mean_lat, mean_lon], zoom_start=12)

        # Add markers for existing locations
        for _, row in locations_df.iterrows():
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=f"<strong>{row['name']}</strong><br>Type: {row['type']}",
                icon=folium.Icon(color='blue' if row['type'] == 'Excavated Site' else 'green'),
            ).add_to(m)

        # Use LatLngPopup to get coordinates from the map
        folium.LatLngPopup().add_to(m)

        # Display the map
        folium_static(m, width=700)

        # To select the coordinates after clicking on the map
        st.write("Select a location on the map to see the coordinates.")
        lat = st.number_input("Latitude", value=mean_lat)
        lon = st.number_input("Longitude", value=mean_lon)

        # Find nearest location
        if st.button("Find Nearest Location"):
            if not locations_df.empty:
                user_location = (lat, lon)
                locations_df['distance'] = locations_df.apply(
                    lambda row: geodesic(user_location, (row['lat'], row['lon'])).kilometers, axis=1)

                # Find top 5 nearest locations
                nearest_locations = locations_df.nsmallest(5, 'distance')

                # Display nearest locations
                st.markdown("<div class='section-title'>Top 5 Nearest Locations</div>", unsafe_allow_html=True)
                st.table(nearest_locations[['name', 'lat', 'lon', 'type', 'distance']])

                # Show the route on the map
                folium.Marker(location=user_location, popup="Your Location", icon=folium.Icon(color='red')).add_to(m)
                for _, loc in nearest_locations.iterrows():
                    folium.Marker(location=(loc['lat'], loc['lon']), popup=loc['name'],
                                  icon=folium.Icon(color='orange')).add_to(m)
                    folium.PolyLine(locations=[user_location, (loc['lat'], loc['lon'])], color='blue', weight=1).add_to(
                        m)

                # Show updated map
                folium_static(m, width=900)
    else:
        st.write("No locations to display on the map.")



    # Filter locations by condition
    st.markdown("<div class='section-title'>Filter Locations by Condition</div>", unsafe_allow_html=True)
    conditions = ['All', 'Good', 'Moderate', 'Urgent', 'Damaged']
    selected_condition = st.selectbox("Select Condition", conditions)

    if selected_condition != 'All':
        filtered_locations = locations_df[locations_df['condition'] == selected_condition]
    else:
        filtered_locations = locations_df

    # Display the filtered results
    if not filtered_locations.empty:
        st.table(filtered_locations[['name', 'lat', 'lon', 'type', 'condition']])
    else:
        st.write("No locations found for the selected condition.")
