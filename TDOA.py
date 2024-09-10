import numpy as np
from numpy.linalg import inv, norm
import matplotlib.pyplot as plt



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
def least_squares(X, Y):
    # Compute the transpose of X
    X_transpose = X.T
    
    # Compute X^T * X
    X_transpose_X = X_transpose @ X
    
    # Compute the inverse of X^T * X
    X_transpose_X_inv = np.linalg.inv(X_transpose_X)
    
    # Compute X^T * Y
    X_transpose_Y = X_transpose @ Y
    
    # Compute the least squares solution: β = (X^T X)^-1 * X^T Y
    beta = X_transpose_X_inv @ X_transpose_Y
    
    return beta



station_x = [3965386.88927195, 4188241.16739446, 3771037.56152003, 4840418.44462275,
 4629465.78911522]
station_y =[  -8844.93219582,  172039.1853054,   898735.63930569, -313338.19217668,
 1026022.68645114]
station_z = [4986508.75719321, 4797778.59456454, 5055807.64668187, 4130594.32264648,
 4254992.94409513]
wave_velocity = 3e8
station_time = [0.00106872, 0.00087994, 0.00216792, 0.00438078, 0.00390532]

def TDOA(station_x, station_y, station_z, station_time, wave_velocity):
    array1 = [0] * len(station_x)
    array2 = [0] * len(station_x)
    array3 = [0] * len(station_x)
    array4 = [0] * len(station_x)

    arrayI = [0] * len(station_x)
    
    for i in range(1,len(array1)):
        array1[i-1] = station_x[i]-station_x[0]
        array2[i-1] = station_y[i]-station_y[0]
        array3[i-1] = station_z[i]-station_z[0]
        array4[i-1] = wave_velocity*(station_time[i]-station_time[0])

        arrayI[i-1] = wave_velocity**2 * (station_time[i]-station_time[0])**2 - station_x[i]**2 - station_y[i]**2 - station_z[i]**2 + station_x[0]**2 + station_y[0]**2 + station_z[0]**2

    
    A = np.column_stack((array1, array2, array3, array4))
    A *= -2
    b = np.vstack(arrayI)

    return least_squares(A,b)



beta = TDOA(station_x,station_y,station_z,station_time,wave_velocity)
print("Estimated coefficients LS (beta):")
print(beta)

print(cartesian_to_latlon(beta[0],beta[1],beta[2]))




