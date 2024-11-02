import streamlit as st
import pandas as pd
import os
import requests
from io import StringIO

# Define the CSV file path
# DATA_FILE = 'https://raw.githubusercontent.com/MyoMinKo1011/gis/refs/heads/main/gis_project/locations_data.csv'

def load_data():
    """Load data from the CSV file into session state."""
    url = 'https://raw.githubusercontent.com/MyoMinKo1011/gis/refs/heads/main/gis_project/locations_data.csv'
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text))
        st.session_state['locations'] = df.to_dict(orient='records')
    else:
        st.session_state['locations'] = []

# def save_data():
#     """Save the current session state locations data to the CSV file."""
#     if 'locations' in st.session_state:
#         df = pd.DataFrame(st.session_state['locations'])
#         df.to_csv(DATA_FILE, index=False)
GITHUB_API_URL = 'https://api.github.com/repos/MyoMinKo1011/gis/gis_project/locations_data.csv'
def save_data():
    """Save the current session state locations data to the GitHub file."""
    if 'locations' in st.session_state:
        df = pd.DataFrame(st.session_state['locations'])
        csv_data = df.to_csv(index=False)
        # Get the SHA of the existing file for the commit
        response = requests.get(GITHUB_API_URL, headers={'Authorization': f'token {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}'})
        if response.status_code == 200:
            sha = response.json()['sha']
            # Prepare the data payload
            payload = {
                "message": "Update locations_data.csv",
                "content": csv_data.encode('utf-8').decode('utf-8'),
                "sha": sha
            }
            # Update the file
            response = requests.put(
                GITHUB_API_URL,
                headers={'Authorization': f'token {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}'},
                data=json.dumps(payload)
            )
            if response.status_code == 200:
                st.success("Data saved successfully to GitHub.")
            else:
                st.error(f"Failed to save data to GitHub: {response.json().get('message', 'Unknown error')}")
        else:
            st.error("Failed to retrieve file SHA for updating.")
    else:
        st.warning("No data to save.")

def show():
    st.title("Data Entry")
    st.write("Enter location data here.")

    # Load existing data when the page is opened
    load_data()

    # Initialize session state for form fields
    if 'name' not in st.session_state:
        st.session_state['name'] = ""
    if 'latitude' not in st.session_state:
        st.session_state['latitude'] = 0.0
    if 'longitude' not in st.session_state:
        st.session_state['longitude'] = 0.0
    if 'location_type' not in st.session_state:
        st.session_state['location_type'] = "Excavated Site"
    if 'details' not in st.session_state:
        st.session_state['details'] = ""
    if 'condition' not in st.session_state:
        st.session_state['condition'] = "Good"  # Default value for condition
    if 'edit_index' not in st.session_state:
        st.session_state['edit_index'] = None

    # Form for data entry
    with st.form("data_entry_form"):
        # Use session state variables for inputs
        name = st.text_input("Location Name", value=st.session_state['name'])
        latitude = st.number_input("Latitude", format="%.6f", value=st.session_state['latitude'])
        longitude = st.number_input("Longitude", format="%.6f", value=st.session_state['longitude'])
        location_type = st.selectbox("Location Type", ["Excavated Site", "Monument Site"],
                                     index=0 if st.session_state['location_type'] == "Excavated Site" else 1)
        details = st.text_area("Details", value=st.session_state['details'])
        condition = st.selectbox("Condition", ["Good", "Moderate", "Urgent", "Damaged"],
                                  index=0 if st.session_state['condition'] == "Good" else (1 if st.session_state['condition'] == "Moderate" else (2 if st.session_state['condition'] == "Urgent" else 3)))

        submitted = st.form_submit_button("Submit")

        # When form is submitted, save data and reset form fields
        if submitted:
            # Update existing entry if edit_index is set
            if st.session_state['edit_index'] is not None:
                st.session_state['locations'][st.session_state['edit_index']] = {
                    "name": name,
                    "lat": latitude,
                    "lon": longitude,
                    "type": location_type,
                    "details": details,
                    "condition": condition  # Add condition to the updated entry
                }
                st.success("Location updated!")
                st.session_state['edit_index'] = None  # Reset edit index after updating
            else:
                # Append new location data
                new_location = {
                    "name": name,
                    "lat": latitude,
                    "lon": longitude,
                    "type": location_type,
                    "details": details,
                    "condition": condition  # Add condition to the new entry
                }
                st.session_state['locations'].append(new_location)
                st.success("Location added!")

            # Clear input fields in session state
            st.session_state['name'] = ""
            st.session_state['latitude'] = 0.0
            st.session_state['longitude'] = 0.0
            st.session_state['location_type'] = "Excavated Site"
            st.session_state['details'] = ""
            st.session_state['condition'] = "Good"  # Reset condition to default

            # Save the updated list to the CSV file
            save_data()

    # Display table of entered data with filtering options
    st.write("### Location Data Table")

    # Filter option for the table
    filter_type = st.selectbox("Filter by Location Type", ["All", "Excavated Site", "Monument Site"])

    # Convert session data to DataFrame for display
    if 'locations' in st.session_state and st.session_state['locations']:
        locations_df = pd.DataFrame(st.session_state['locations'])

        # Apply filter if a specific type is selected
        if filter_type != "All":
            locations_df = locations_df[locations_df['type'] == filter_type]

        # Create a more appealing layout for the data table
        for i, row in locations_df.iterrows():
            st.markdown("---")  # Add a horizontal line for separation
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**Location Name:** {row['name']}")
                st.markdown(f"**Type:** {row['type']}")
                st.markdown(f"**Details:** {row['details']}")
                st.markdown(f"**Condition:** {row['condition']}")  # Display condition
            with col2:
                st.markdown(f"**Lat:** {row['lat']}")
                st.markdown(f"**Lon:** {row['lon']}")
            with col3:
                # Update button
                if st.button("Edit", key=f"edit_{i}"):
                    st.session_state['edit_index'] = i
                    st.session_state['name'] = row['name']
                    st.session_state['latitude'] = row['lat']
                    st.session_state['longitude'] = row['lon']
                    st.session_state['location_type'] = row['type']
                    st.session_state['details'] = row['details']
                    st.session_state['condition'] = row['condition']  # Load condition for editing

    else:
        st.write("No location data available.")
