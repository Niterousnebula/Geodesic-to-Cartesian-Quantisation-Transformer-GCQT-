import numpy as np
from earth_model import geodetic_to_ecef


def ecef_to_enu(X, Y, Z, lat0, lon0, h0):

    X0, Y0, Z0 = geodetic_to_ecef(lat0, lon0, h0)

    lat0 = np.radians(lat0)
    lon0 = np.radians(lon0)

    dX = X - X0
    dY = Y - Y0
    dZ = Z - Z0

    R = np.array([
        [-np.sin(lon0),              np.cos(lon0),               0],
        [-np.sin(lat0)*np.cos(lon0), -np.sin(lat0)*np.sin(lon0), np.cos(lat0)],
        [ np.cos(lat0)*np.cos(lon0),  np.cos(lat0)*np.sin(lon0), np.sin(lat0)]
    ])

    enu = R @ np.vstack((dX, dY, dZ))
    return enu[0], enu[1], enu[2]

"""
ECEF values are huge, so for storage we convert them into ENU (east, north, up)
    ENU values are small
    Computations become stable
    Quantisation becomes efficient
"""