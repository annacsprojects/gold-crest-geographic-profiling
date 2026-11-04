# gold-crest-geographic-profiling (Gold CREST Award Project)

This is a Python web application built for my Gold CREST Award project. It gathers crime scene coordinates and uses them to calculate the highest probability of where the offender's base is (this would only work accurately when considering crime locations by Marauder offenders).

# How it works
1. The app reads crime locations from data/crime_scenes.csv using Pandas.
2. Instead of constantly using loops, pandas takes the latitude and longitude variables and calculates their mean to find the centre point of all of the crimes.
3. Using Streamlit (the canvas for the dashboard) and Folium (software used to apply the map and text), each crime scene is plotted as a blue pin, and the calculated mean of all of the crimes is illustrated with a red home icon.
4. To ensure the program communicates effectively, it runs a binary check; the two furthest points form the diameter of a circle, if incident site coordinates sit beyond the radius of the circle, a warning appears, telling the user that the suspect is likely to be a Commuter, of which the calculated base is a low probability of them living there.
5. On the dashboard, the user has the choice of toggling a Geographic Profiling Map or a Commerical Location Map based on Potential Customer Density in the local area. Both scenarios can be used from the same mathematical application based on their contexts.

# The Project's Structure
'data/' - Contains the crime_scenes.csv file.
'src/dashboard/app.py' - This includes the code that builds the map and UI on the web app.
'requirements.txt' - Lists the external Python libraries needed to run the map.
'.venv/' - An environemtn used to keep the project libraries isolated.

# Running the local directory

1. To activate the .venv environment:
```bash
source .venv/bin/activate
````
2. To install the required libraries
```bash
pip install -r requirements.txt
```
3. Launching the web application
```bash
streamlit run src/dashboard/app.py
```