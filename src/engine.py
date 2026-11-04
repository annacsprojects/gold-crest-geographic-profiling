# This file calculates a Marauder's Base
import numpy as np
from scipy.optimize import minimize

# This define function calculates the mean for all of the coordinates
def calculate_centroid(coords):
    return np.mean(coords, axis=0)

# This define function calculates the Center Minimum of distance
# The Center of Minimum Distane, unlike a median, calculates from all distances and ensures the distance is as short as possible (it does not account for real world contexts eg buildings, trees)
def calculate_cmd(coords):
    # This function starts with a trial point, calculating the total distance from every crime scene
    def total_distance(point):
        return np.sum (np.sqrt(np.sum((coords - point) ** 2, axis=1)))
    # The standard average is used as the first guess
    initial_guess = calculate_centroid(coords)
    # The software minimize continues testing for guesses until the total distance is the shortest possible reached
    result = minimize (total_distance, initial_guess, method='Nelder Mead')
    return result.x

# Rossmo's Formula: Here, this function considers a buffer zone, it applies the theory that offenders don't commit crimes directly near their homes, as well as implementing distance decay, where the offender only travels locally to commit crimes, the furthest away they are, the less likely it is that they commit a crime..
def calculate_simplified_rossmo(coords, buffer_km=1.0, f=1.2, g=1.2):
    latitudes = coords[:, 0]
    longitudes = coords[:, 1]

    # A grid box overlaps the area with 50 rows and 50 columns of the test points.
    lat_grid = np.linspace(min(latitudes) - 0.1, max(latitudes) + 0.1, 50)
    lon_grid = np.linspace(min(longitudes) - 0.1, max(longitudes) + 0.1, 50)

    best_prob = -1
    best_coord = calculate_centroid(coords)

    buffer_deg = buffer_km / 111.0

    # Check every square on the grid.
    for lat in lat_grid:
        for lon in lon_grid:
            cell_prob = 0.0
            # Measure the distance from this square to each crime scene.
            for c_lat, c_lon in coords:
                dist = np.sqrt((lat - c_lat) ** 2 + (lon - c_lon) ** 2)
                if dist == 0:
                    continue

                # Apply distance decay outside the buffer zone.
                if dist > buffer_deg:
                    cell_prob += 1.0 / (dist ** f)
                # Within the buffer zone, apply the buffer penalty.
                else:
                    cell_prob += (buffer_deg ** (g - f)) / (2 * buffer_deg)

            # Keep the grid coordinate with the highest score.
            if cell_prob > best_prob:
                best_prob = cell_prob
                best_coord = [lat, lon]

    return [best_coord]

# Circle Theory finds two furthest points and establishes a diameter. Returns true it's a Marauder, False if Commuter.
# Using exception handling, if an offender has travelled too far out of the radius, instead of breaking the code, the program shows the user an error that the offender is a commuter, not a marauder.
def run_circle_theory_test(coords):
    if len(coords) < 3: 
        return True

    max_dist = 0
    p1_idx, p2_idx = 0,0

# Finding the two furthest points
    for i in range (len(coords)):
        for j in range(i+1, len(coords)):
            dist = np.sqrtnp.sum((coords[i] - (coords[j])**2))
            # The two calculated furthest coordinates are treated as the circle diameter
            if dist > max_dist:
                max_dist = dist
                p1_idx, p2_idx = i, j
    # Calculating the center and radius of the circle
    center = (coords[p1_idx] + coords[p2_idx]) / 2
    radius = max_dist / 2

    # Checking if all other points are within the circle radius
    for idx, pt in enumerate(coords):
        if idx in [p1_idx, p2_idx]:
            continue 
        dist_from_center = np.sqrt(np.sum((pt - center)**2))
        if dist_from_center > radius:
                return False #If all points fall outside the radius, offender is likely a Commuter.

    return True # All points are within circle radius, likely to be a Marauder offender