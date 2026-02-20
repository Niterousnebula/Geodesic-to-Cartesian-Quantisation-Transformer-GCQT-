import numpy as np

class WGS84:
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = f * (2 - f)


def geodetic_to_ecef(lat_deg, lon_deg, h):
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)

    a = WGS84.a
    e2 = WGS84.e2

    N = a / np.sqrt(1 - e2 * np.sin(lat)**2)

    X = (N + h) * np.cos(lat) * np.cos(lon)
    Y = (N + h) * np.cos(lat) * np.sin(lon)
    Z = (N * (1 - e2) + h) * np.sin(lat)

    return X, Y, Z


"""
Latitude and longitude are:
    Angular
    On an ellipsoid
    Non-Euclidean

and cannot do grid math in lat/lon space.
So we convert to Earth-Centered Earth-Fixed coordinates:
    Geodetic --> X,Y,Z
"""