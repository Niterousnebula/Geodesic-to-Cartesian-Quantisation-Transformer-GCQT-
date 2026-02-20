# io_layer.py

import pandas as pd


def load_pos_file(path):

    df = pd.read_csv(
        path,
        sep=r"\s+",
        comment="%",
        engine="python"
    )

    lat = df.iloc[:, 2].values
    lon = df.iloc[:, 3].values
    h   = df.iloc[:, 4].values

    return lat, lon, h

"""
Reads RTKLIB .pos output
Extracts:
    Latitude
    Longitude
    Height
"""