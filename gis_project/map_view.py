# import streamlit as st
# from streamlit_folium import st_folium
# import folium
#
# def show():
#     st.title("Map View")
#
#     # Filter option
#     st.write("### Filter Locations")
#     location_type_filter = st.selectbox("Select Location Type to View", ["All", "Excavated Site", "Monument Site"])
#
#     # Check if there are any locations in session state
#     if 'locations' in st.session_state and st.session_state['locations']:
#         # Initialize the map
#         first_location = st.session_state['locations'][0]
#         m = folium.Map(location=[first_location["lat"], first_location["lon"]], zoom_start=5)
#
#         # Add markers based on the filter and location type
#         for loc in st.session_state['locations']:
#             # Apply filter
#             if location_type_filter == "All" or loc["type"] == location_type_filter:
#                 # Set different icons or colors based on type
#                 if loc["type"] == "Excavated Site":
#                     icon = folium.Icon(color="blue", icon="cloud")
#                 elif loc["type"] == "Monument Site":
#                     icon = folium.Icon(color="green", icon="flag")
#
#                 # Add marker to map
#                 folium.Marker(
#                     location=[loc["lat"], loc["lon"]],
#                     popup=f"<b>{loc['name']}</b><br>{loc['details']}",
#                     tooltip=loc["name"],
#                     icon=icon
#                 ).add_to(m)
#
#         # Display the map
#         st_folium(m, width = '100%', height = 500)
#     else:
#         st.write("No data available. Please enter some locations on the Data Entry page.")

import streamlit as st
from streamlit_folium import st_folium
import folium


def show():
    st.title("Map View")

    # Filter option
    st.write("### Filter Locations")
    location_type_filter = st.selectbox("Select Location Type to View", ["All", "Excavated Site", "Monument Site"])

    # Check if there are any locations in session state
    if 'locations' in st.session_state and st.session_state['locations']:
        # Initialize the map
        first_location = st.session_state['locations'][0]
        m = folium.Map(location=[first_location["lat"], first_location["lon"]], zoom_start=12)

        # Add markers based on the filter and location type
        for loc in st.session_state['locations']:
            # Apply filter
            if location_type_filter == "All" or loc["type"] == location_type_filter:
                # Set different icons or colors based on type
                if loc["type"] == "Excavated Site":
                    icon = folium.Icon(color="blue", icon="cloud")
                elif loc["type"] == "Monument Site":
                    icon = folium.Icon(color="green", icon="flag")

                # Custom HTML for the pop-up
                popup_html = f"""
                <div style="width: 300px; height: 200px; overflow: auto;">
                    <h4 style="margin: 0;">{loc['name']}</h4>
                    <p style="margin: 5px 0;">{loc['details']}</p>
                    
                </div>
                """

                # Add marker to map
                folium.Marker(
                    location=[loc["lat"], loc["lon"]],
                    popup=folium.Popup(popup_html, max_width=300, min_width=300),  # Set fixed width
                    tooltip=loc["name"],
                    icon=icon
                ).add_to(m)

        # Display the map
        st_folium(m, width='100%', height=500)
    else:
        st.write("No data available. Please enter some locations on the Data Entry page.")




show()


