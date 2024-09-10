import numpy as np
import random

# Constants
speed_of_signal = 3e8  # Speed of light in meters per second (m/s)
signal_speed = speed_of_signal   # Reduced speed for practical purposes (e.g., 300,000 km/s)

# Station locations (Latitude, Longitude)
stations = {
    'London': (51.5074, -0.1278),
    'Paris': (48.8566, 2.3522),
    'Berlin': (52.5200, 13.4050),
    'Madrid': (40.4168, -3.7038),
    'Rome': (41.9028, 12.4964)
}

# Transmitter location (Latitude, Longitude)
transmitter_location = (50.85036042316619, 4.351685055372099)  # Brussels, Belgium for example

# Convert latitude and longitude to Cartesian coordinates (simplified)
def latlon_to_cartesian(lat, lon):
    # Earth radius in meters
    R = 6371e3
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = R * np.cos(lat_rad) * np.cos(lon_rad)
    y = R * np.cos(lat_rad) * np.sin(lon_rad)
    z = R * np.sin(lat_rad)
    return x, y, z

def cartesian_to_latlon(x, y, z):
    """
    Convert Cartesian coordinates (x, y, z) to latitude and longitude.
    
    :param x: Cartesian x-coordinate
    :param y: Cartesian y-coordinate
    :param z: Cartesian z-coordinate
    :return: Tuple of (latitude, longitude)
    """
    # Earth's radius in meters
    R = 6371e3
    
    # Calculate latitude
    lat_rad = np.arcsin(z / R)
    lat = np.degrees(lat_rad)
    
    # Calculate longitude
    lon_rad = np.arctan2(y, x)
    lon = np.degrees(lon_rad)
    
    return lat, lon
# Transmitter coordinates
tx_x, tx_y, tx_z = latlon_to_cartesian(*transmitter_location)

# Initialize lists to store coordinates and TOA data
x_coords = []
y_coords = []
z_coords = []
toa_data = []

for station, (lat, lon) in stations.items():
    # Convert station coordinates to Cartesian
    st_x, st_y, st_z = latlon_to_cartesian(lat, lon)
    
    # Calculate distance between transmitter and station
    distance = np.sqrt((st_x - tx_x)**2 + (st_y - tx_y)**2 + (st_z - tx_z)**2)
    
    # Calculate time of arrival (in seconds)
    toa = distance / signal_speed

    # Generate a random integer between -100 and 100 nanoseconds
    random_nanoseconds = random.randint(-100, 100)

    # Convert nanoseconds to seconds
    random_seconds = random_nanoseconds * 1e-9

    toa += random_seconds
    
    x_coords.append(st_x)
    y_coords.append(st_y)
    z_coords.append(st_z)
    toa_data.append(toa)

# Convert lists to NumPy arrays
x_coords_array = np.array(x_coords)
y_coords_array = np.array(y_coords)
z_coords_array = np.array(z_coords)
toa_array = np.array(toa_data)

# Print the data as Python arrays
print("X Coordinates:")
print(x_coords_array)

print("\nY Coordinates:")
print(y_coords_array)

print("\nZ Coordinates:")
print(z_coords_array)

print("\nTime of Arrival (s):")
print(toa_array)



