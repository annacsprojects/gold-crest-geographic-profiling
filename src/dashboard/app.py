# This file will run the interactive UI map

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Creating headers for the web app
st.title("Geographic Profiling Dashboard")
st.write("Visualising crime clusters to pinpoint the suspected Marauder Base.")

# Fetching Pandas to examine data/crime_scenes.csv
df = pd.read_csv("data/crime_scenes.csv")

# Calculating the mid points
base_lat = df['latitude'].mean()
base_lon = df['longitude'].mean()

# Importing the map as a canvas for plotting
crime_map = folium.Map(location=[base_lat, base_lon], zoom_start=11)

# Coding a loop to drop blue pins of each crime scene in CSV
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup="Crime Scene: {row['case_name']}",
        icon=folium.Icon(colour="blue", icon="info-sign")
    ).add_to(crime_map)

# Coding for a red pin to mark the calculted average between the crime scenes
folium.Marker(
    location=[base_lat, base_lon],
    popup="Predicted Maraunder Base",
    icon=folium.Icon(colour="red", icon="home")
).add_to(crime_map)

# Updated map on web app UI
st_folium(crime_map, width=700, height=500)