import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import engine

st.set_page_config(layout="wide")

# Creating headers for the web app
app_mode = st.sidebar.selectbox(
    "Select Your Profiling Map:",
    ["Forensic Profiling", "Potential Commercial Revenue Locations"])

if app_mode == "Forensic Profiling":
    title = "Geographic Profiling Map"
    subtitle = "Calculating Offender Home Base from Crime Locations"
    site_label = "Crime Scene Locations"
    base_label = "Predicted Suspect Base"
    home_icon = "home"
else: 
    title = "Commercial Locations for Potential Revenue"
    subtitle = "Calculating Best Locations for Business based on Dense Potential Customer Locations"
    site_label = "Dense Customer Demand"
    base_label = "Best Location for Facility"
    home_icon = "briefcase"

# Adding text titles to streamlit
st.title(title)
st.write(subtitle)

# Fetching Pandas to examine data/crime_scenes.csv by each case
df = pd.read_csv("data/crime_scenes.csv")

# Extracting case names - no duplicate names
unique_cases = df['case name'].unique()
selected_case = st.sidebar.selectbox("Select a Case", unique_cases)

# This ensures each case's location is kept to its file
case_filtered_df = df[df['case_name'] == selected_case]

coords_array = case_filtered_df['latitude', 'longitude'].to_numpy()

# Appending the Circle Theory from engine.py
is_marauder_pattern = engine.run_circle_theory_test(coords_array)

# If the program inputs false from engine.py, show a warning
if not is_marauder_pattern:
    if app_mode == "Forensic Profiling":
        st.warning("⚠️ Warning: The Distrubution of Coordinates exhibits high 'Commuter' Traits.")
    else:
        st.info("ℹ️ Notice: Calcuated Mean of Incident Site Locations Show Potential 'Marauder' Base.")

selected_algorithm = st.sidebar.radio()
"Select Calculation",
["Calculate Mean", "Centre Minimum Distance (CMD)", "Rosmo's Distance Decay Model"]
# Allow the user to choose what calculation they want to use for profiling from engine.py
if selected_algorithm == "Calculate Mean":
    calculated_base = engine.calculate_centroid(coords_array)
elif selected_algorithm == "Centre Minimum Distance (CMD)":
    calculated_base = engine.calculate_cmd(coords_array)
else:
    calculated_base = engine.calculate_simplified_rossmo(coords_array)

# Use Folium to illustrate the new base prediction
interactive_map = folium.Map(location=[calculated_base[0], calculated_base[1]], zoom_start=12)

# The coordinates are matched to their pin type and colour
for index, row in case_filtered_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['site_label']} #(int(row['site_number]))",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(interactive_map)

# Dropping the final calculations as the offender home base or commerical location
folium.Marker(
    location=[calculated_base[0], calculated_base[1]],
    popup=f"Calcuated {base_label} via ({selected_algorithm})",
    icon=folium.Icon(color="red", icon="home")
).add_to(interactive_map)

# Adding the map to Streamlit
st.folium(interactive_map, width=950, height=550)