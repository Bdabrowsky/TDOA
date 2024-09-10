import numpy as np
from scipy.optimize import minimize

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

def log_likelihood(position, x, y, z, toa, c=3e8, sigma=1):
    """
    Compute the log-likelihood of the position given the observations.
    
    :param position: Tuple with (x_0, y_0, z_0) for the object's position
    :param x: Array of x-coordinates of stations
    :param y: Array of y-coordinates of stations
    :param z: Array of z-coordinates of stations
    :param toa: Array of time of arrivals at each station
    :param c: Speed of signal (default is 1.0 for simplicity)
    :param sigma: Standard deviation of Gaussian noise
    :return: Log-likelihood value
    """
    x_0, y_0, z_0 = position
    distances = np.sqrt((x - x_0)**2 + (y - y_0)**2 + (z - z_0)**2)
    computed_toa = distances / c
    residuals = toa - computed_toa
    log_likelihood_value = -0.5 * np.sum((residuals / sigma)**2 + len(toa) * np.log(2 * np.pi * sigma**2))
    return -log_likelihood_value  # We minimize the negative log-likelihood

def estimate_position(x, y, z, toa, c=3e8, sigma=1.0):
    """
    Estimate the position of an object using MLE.
    
    :param x: Array of x-coordinates of stations
    :param y: Array of y-coordinates of stations
    :param z: Array of z-coordinates of stations
    :param toa: Array of time of arrivals at each station
    :param c: Speed of signal (default is 1.0 for simplicity)
    :param sigma: Standard deviation of Gaussian noise
    :return: Estimated position (x_0, y_0, z_0)
    """
    # Initial guess for the position -> add last position
    initial_guess = np.mean(x), np.mean(y), np.mean(z)
    
    # Optimize the negative log-likelihood to find the best position
    result = minimize(log_likelihood, initial_guess, args=(x, y, z, toa, c, sigma), method='Nelder-Mead')
    
    return result.x


x = np.array([3965386.88927195, 4188241.16739446, 3771037.56152003, 4840418.44462275,
 4629465.78911522])
y = np.array([  -8844.93219582,  172039.1853054,   898735.63930569, -313338.19217668,
 1026022.68645114])
z = np.array([4986508.75719321, 4797778.59456454, 5055807.64668187, 4130594.32264648,
 4254992.94409513])
toa = np.array([0.0010687,  0.00087989, 0.00216796, 0.00438087, 0.00390524])

estimated_position = estimate_position(x, y, z, toa)
print("Estimated Position:", estimated_position)

print(cartesian_to_latlon(estimated_position[0],estimated_position[1],estimated_position[2]))