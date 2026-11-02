# gold-crest-geographic-profiling (Gold CREST Award Project)

This is a Python web application built for my Gold CREST Award project. It gathers crime scene coordinates and uses them to calculate the highest probability of where the offender's base is (this would only work accurately when considering crime locations by Marauder offenders).

# How it works
1. The app reads crime locations from data/crime_scenes.csv using Pandas.
2. Instead of constantly using loops, pandas takes the latitude and longitude variables and calculates their mean to find the centre point of all of the crimes.
3. Using Streamlit (the canvas for the dashboard) and Folium (software used to apply the map and text), each crime scene is plotted as a blue pin, and the calculated mean of all of the crimes is illustrated with a red home icon.

# The Project's Structure
'data/' - Contains the crime_scenes.csv file.
'src/dashboard/app.py' - This includes the code that builds the map and UI on the web app.
'requirements.txt' - Lists the external Python libraries needed to run the map.
'.venv/' - An environemtn used to keep the project libraries isolated.

# Running the local directory

1. To activate the .venv environment:

source .venv/bin/activate

2. To install the required libraries

pip install -r requirements.txt

3. Launching the web application

streamlit run src/dashboard/app.py




