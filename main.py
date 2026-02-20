
# IMPORTS

from io_layer import load_pos_file
from earth_model import geodetic_to_ecef
from frame_transform import ecef_to_enu
from quantizer import Quantizer
from evaluator import compute_error
from benchmark import benchmark_storage
from visualisation import plot_point_cloud
from path_planner import compute_movement
import pandas as pd
import webbrowser

# USER CONFIGURATION

INPUT_PATH = r"C:\Users\ragha\OneDrive\Desktop\gcqt\gcqt_simulated_custom_area.pos"
OUTPUT_PATH = r"C:\Users\ragha\OneDrive\Desktop\gcqt\encoded.csv"

RESOLUTION = 0.05        # Grid resolution in meters
MAP_OPACITY = 0.6        # 0.0 (transparent) → 1.0 (solid)


def run_gqct():

    print("\n========== GQCT PIPELINE START ==========")

    #  Data Layer
    lat, lon, h = load_pos_file(INPUT_PATH)
    print("Loaded trajectory with", len(lat), "epochs")

    #  Earth Geometry Model (Geodetic → ECEF)
    X, Y, Z = geodetic_to_ecef(lat, lon, h)

    #  Frame Transformation (ECEF → ENU)
    lat0, lon0, h0 = lat[0], lon[0], h[0]
    E, N, U = ecef_to_enu(X, Y, Z, lat0, lon0, h0)

    #  Spatial Encoding (Quantisation)
    q = Quantizer(resolution=RESOLUTION)
    Eq, Nq, Uq = q.encode(E, N, U)


    #  Reconstruction & Error Evaluation

    E_rec, N_rec, U_rec = q.decode(Eq, Nq, Uq)

    mean_E, max_E = compute_error(E, E_rec)
    mean_N, max_N = compute_error(N, N_rec)
    mean_U, max_U = compute_error(U, U_rec)

    print("\n=== Quantisation Report ===")
    print("Resolution:", RESOLUTION, "meters")
    print("Mean Errors (m):", mean_E, mean_N, mean_U)
    print("Max Errors  (m):", max_E, max_N, max_U)


    #  Storage Benchmark

    benchmark_storage(E, N, U, Eq, Nq, Uq)

    # Save quantised output
    df_out = pd.DataFrame({
        "E_q": Eq,
        "N_q": Nq,
        "U_q": Uq
    })
    df_out.to_csv(OUTPUT_PATH, index=False)
    print("\nQuantised data saved to:", OUTPUT_PATH)


    #  Point Cloud Visualization

    print("\nGenerating map visualization...")
    map_file = "map.html"
    plot_point_cloud(lat0, lon0, h0, E_rec, N_rec, U_rec,
                     opacity=MAP_OPACITY,
                     output_html=map_file)

    webbrowser.open(map_file)


    #  Interactive Path Maker

    print("\n========== PATH MAKER ==========")

    try:
        start_lat = float(input("Enter Start Latitude: "))
        start_lon = float(input("Enter Start Longitude: "))
        start_h   = float(input("Enter Start Height (m): "))

        dest_lat = float(input("Enter Destination Latitude: "))
        dest_lon = float(input("Enter Destination Longitude: "))
        dest_h   = float(input("Enter Destination Height (m): "))

        dE, dN, dU, dist = compute_movement(
            start_lat, start_lon, start_h,
            dest_lat, dest_lon, dest_h
        )

        print("\n=== Movement Vector (ENU) ===")
        print("Move East  (m):", dE)
        print("Move North (m):", dN)
        print("Move Up    (m):", dU)
        print("3D Distance (m):", dist)

    except Exception as e:
        print("Path planner input error:", e)

    print("\n========== GQCT PIPELINE COMPLETE ==========")


if __name__ == "__main__":
    run_gqct()

"""
===========================================================
GQCT - Geodetic to Quantised Cartesian Transformer
===========================================================

This is the pipeline controller.

It performs the following steps:

1. Loads RTKLIB position data (.pos file)
2. Converts Geodetic → ECEF (Earth Geometry Model)
3. Converts ECEF → ENU (Local Frame Transformation)
4. Applies Spatial Quantisation (Grid Encoding)
5. Reconstructs and Evaluates Quantisation Error
6. Benchmarks Storage Reduction
7. Generates Map-Based Point Cloud Visualization
8. Computes Movement Vector Between User-Defined Coordinates


System Architecture


[ Data Layer ]
        ↓
[ Earth Geometry Model ]
        ↓
[ Frame Transformation ]
        ↓
[ Spatial Encoding ]
        ↓
[ Evaluation ]


"""