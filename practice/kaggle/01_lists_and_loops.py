"""
Task 1. Lists, Tuples, Dictionaries, and Loops
CONTEXT: Modeling the Railway Rapist case using simplified coordinates to test logic.
OBJECTIVES:
1. Store 2 simplified incident locations using Tuples.
2. Create an empty list to act as a police file log and add both tuples into it.
3. Use a number index inside square brackets and pull the first station coordinate out of the list.
4. Unpack the first station coordinates into two variables; latitude and longitude.
5. Print the code of both the lat and lon variables using the .as_integer_ratio() method.
6. Use dictionaries and embedded for loops to ensure that the output calculates for the incident locations in the police file log.
"""

incident_location_1 = (51.55, -0.18)
incident_location_2 = (51.54, -0.02)

police_file_log = [incident_location_1, incident_location_2]

first_station = police_file_log[0]
latitude, longitude = first_station
print(latitude.as_integer_ratio())
print(longitude.as_integer_ratio())

second_station = police_file_log[1]
latitude, longitude = second_station
print(latitude.as_integer_ratio())
print(longitude.as_integer_ratio())

incident_locations = {"longitude": [51.55, 51.54], "latitude": [-0.18, -0.02]}
for key, values in incident_locations.items(): #each key is pulled out of the dictionary and the values are pulled out as a list (coord)
    for coord in values:
        ratio = coord.as_integer_ratio() #ratio is the variable chosen to store the output of the .as_integer_ratio() method and .as_integer_ratio() looks at the decimal and releases the numerator and denominator as coordinate pair
        result = ratio[0] / ratio [1]
        print(coord, "restored to:", result)