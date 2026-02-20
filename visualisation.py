import folium
import numpy as np
from earth_model import geodetic_to_ecef, WGS84


def ecef_to_geodetic(X, Y, Z):

    a = WGS84.a
    e2 = WGS84.e2

    lon = np.arctan2(Y, X)
    p = np.sqrt(X**2 + Y**2)
    lat = np.arctan2(Z, p * (1 - e2))

    for _ in range(5):
        N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
        h = p / np.cos(lat) - N
        lat = np.arctan2(Z, p * (1 - e2 * N / (N + h)))

    return np.degrees(lat), np.degrees(lon)


def plot_point_cloud(lat0, lon0, h0, E, N, U,
                     opacity=0.6,
                     output_html="map.html"):

    X0, Y0, Z0 = geodetic_to_ecef(lat0, lon0, h0)

    lat0 = np.radians(lat0)
    lon0 = np.radians(lon0)

    R_inv = np.array([
        [-np.sin(lon0), -np.sin(lat0)*np.cos(lon0),  np.cos(lat0)*np.cos(lon0)],
        [ np.cos(lon0), -np.sin(lat0)*np.sin(lon0),  np.cos(lat0)*np.sin(lon0)],
        [ 0,             np.cos(lat0),               np.sin(lat0)]
    ])

    offsets = R_inv @ np.vstack((E, N, U))

    X = X0 + offsets[0]
    Y = Y0 + offsets[1]
    Z = Z0 + offsets[2]

    lat, lon = ecef_to_geodetic(X, Y, Z)

    m = folium.Map(location=[lat0 * 180/np.pi,
                             lon0 * 180/np.pi],
                   zoom_start=18)

    for la, lo in zip(lat, lon):
        folium.CircleMarker(
            location=[la, lo],
            radius=2,
            color='red',
            fill=True,
            fill_opacity=opacity
        ).add_to(m)

    m.save(output_html)
    print(f"Map saved to {output_html}")