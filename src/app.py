import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
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
df = pd.read_csv("data/crime_scenes.csv", skip_blank_lines=True)
df.columns = df.columns.str.strip()

if app_mode == "Forensic Profiling":
    df = pd.read_csv("data/crime_scenes.csv", skip_blank_lines=True)
    df.columns = df.columns.str.strip()
    unique_cases = df['case_name'].unique()
    selected_case = st.sidebar.selectbox("Select a Case", unique_cases)
    case_filtered_df = df[df['case_name'] == selected_case]
else:
    st.subheader("Enter Customer or Store Locations")
    st.write("Add, edit, or delete rows below to calculate potential warehouse/shop location.")

    starter_data = pd.DataFrame({
        "description": ["Customer Hub A", "Customer Hub B", "Customer Hub C"],
        "latitude": [51.5074, 51.5155, 51.4995],
        "longitude": [-0.1278, -0.1419, -0.1248]
    })
# Interactive table for user input
    case_filtered_df = st.data_editor(starter_data, num_rows="dynamic")
    case_filtered_df["site_number"] = range(1, len(case_filtered_df) + 1)

# Calculations not run if the user leaves blank cells in the table
case_filtered_df = case_filtered_df.dropna(subset=["latitude", "longitude"])
coords_array = case_filtered_df[["latitude", "longitude"]].to_numpy()

if len(coords_array) < 2:
    st.warning("Please enter at least two locations to calculate a base.")
    st.stop()

is_marauder_pattern, circle_center, circle_radius = engine.run_circle_theory_test(coords_array)

# If the program inputs false from engine.py, show a warning
if "Forensic" in app_mode:
        if is_marauder_pattern:
            st.info("ℹ️ Notice: Calculated Mean of Incident Site Locations Show Potential 'Marauder' Base.")
        else:
            st.warning("⚠️ Warning: The Distribution of Coordinates exhibits high 'Commuter' Traits.")

# All models calculated for
mean_base = engine.calculate_centroid(coords_array)
cmd_base = engine.calculate_cmd(coords_array)
rossmo_base, rossmo_heatmap = engine.calculate_simplified_rossmo(coords_array)

# Creating a map centered on the mean
interactive_map = folium.Map(location=[mean_base[0], mean_base[1]], zoom_start=11)

HeatMap(
    rossmo_heatmap,
    radius=38,
    blur=30,
    max_zoom=12,
    min_opacity=0.15,
    gradient={
        # Deep Blue (lowest probability)
        0.1: "#0000ff",
        0.3: "#00ffff",
        0.5: "#00ff00",
        0.7: "#ffff00",
        0.85: "#ff8000",
        1.0: "#ff0000",
        # Red (highest probability for base)
    }
        ).add_to(interactive_map)

# Adding a heatmap
HeatMap(coords_array.tolist()).add_to(interactive_map)

# Plotting the three bases with distinct colouring
models=[
     {"name": "Centroid (Mean)", "coords": mean_base, "color": "red", "icon": "home"},
     {"name": "Centre Minimum Distance (CMD)", "coords": cmd_base, "color": "green", "icon": "star"},
     {"name": "Rossmo's Distance Decay", "coords": rossmo_base, "color": "purple", "icon": "flag"}
]
for model in models:
     folium.Marker(
          location=[model["coords"][0], model["coords"][1]],
          popup=f"{base_label}: {model['name']}",
          icon=folium.Icon(color=model["color"], icon=model["icon"])
     ).add_to(interactive_map)

# The coordinates are matched to their pin type and colour
for index, row in case_filtered_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=str(row["description"]) + " #" + str(int(row["site_number"])),
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(interactive_map)

radius=9500
folium.Circle(
     location=[circle_center[0], circle_center[1]],
     radius=circle_radius,
     colour="black",
     weight=1,
     fill_opacity=0.2,
     opacity=1,
     fill_colour="crimson",
     fill=True, #gets overidden by fill colour
     popup=f"{round(circle_radius)} meters",
     tooltip="Circle Theory Boundary",
).add_to(interactive_map)

# Adding the map to Streamlit
st_folium(interactive_map, width=950, height=550)