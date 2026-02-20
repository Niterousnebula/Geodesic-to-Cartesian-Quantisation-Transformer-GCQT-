import numpy as np
from earth_model import geodetic_to_ecef
from frame_transform import ecef_to_enu


def compute_movement(start_lat, start_lon, start_h,
                     dest_lat, dest_lon, dest_h):

    Xd, Yd, Zd = geodetic_to_ecef(dest_lat, dest_lon, dest_h)

    E_d, N_d, U_d = ecef_to_enu(
        np.array([Xd]),
        np.array([Yd]),
        np.array([Zd]),
        start_lat,
        start_lon,
        start_h
    )

    dE = float(E_d[0])
    dN = float(N_d[0])
    dU = float(U_d[0])

    distance = np.sqrt(dE**2 + dN**2 + dU**2)

    return dE, dN, dU, distance