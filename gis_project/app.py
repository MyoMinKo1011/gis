import streamlit as st
from data_entry import show as data_entry_show
from map_view import show as map_view_show
from route_map import show as route_map_show
from dashboard import show_dashboard as dashboard_show

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Data Entry", "Map View", "Route Calculator"])

if page == "Data Entry":
    data_entry_show()
elif page == "Map View":
    map_view_show()
elif page == "Route Calculator":
    route_map_show()
elif page == "Dashboard":
    dashboard_show()
