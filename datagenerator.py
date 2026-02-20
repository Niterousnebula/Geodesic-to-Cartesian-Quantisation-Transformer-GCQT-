import numpy as np
import math
from datetime import datetime, timedelta

# --- Configuration ---
START_TIME_STR = "2026/01/01 06:00:00.0"
START_LAT = 28.580656480
START_LON = 77.090547032
START_ALT = 167.7769

# --- Get User Input ---
print("Please specify the area dimensions in kilometers:")
try:
    x_km = float(input("x (width) = "))
    y_km = float(input("y (height) = "))
    num_rows = int(input("Enter the number of rows to generate: "))
except ValueError:
    print("Invalid input detected. Defaulting to x = 2.0 km, y = 2.0 km, and 8000 rows.")
    x_km = 2.0
    y_km = 2.0
    num_rows = 8000

if num_rows <= 0:
    num_rows = 1

# --- Area Calculations ---
# Convert total km distance to a radius in meters
x_radius_m = (x_km * 1000.0) / 2.0
y_radius_m = (y_km * 1000.0) / 2.0

# 1 degree of latitude is ~111.32 km
LAT_AMPLITUDE = y_radius_m / 111320.0

# 1 degree of longitude varies by latitude
meters_per_deg_lon = 111320.0 * math.cos(math.radians(START_LAT))
LON_AMPLITUDE = x_radius_m / meters_per_deg_lon

# --- Time and Header Calculations ---
start_time = datetime.strptime(START_TIME_STR, "%Y/%m/%d %H:%M:%S.%f")
end_time = start_time + timedelta(seconds=num_rows - 1)
start_gps_sec = 367200.0
end_gps_sec = start_gps_sec + (num_rows - 1)

output_filename = "gcqt_simulated_custom_area.pos"

with open(output_filename, "w") as f:
    # --- Write Exact Header ---
    f.write("% program   : RTKPOST ver.2.4.2\n")
    f.write("% inp file  : C:\\Users\\ragha\\OneDrive\\Desktop\\gcqt\\Order_1\\DELH001G00.26o\n")
    f.write("% inp file  : C:\\Users\\ragha\\OneDrive\\Desktop\\gcqt\\Order_1\\DELH001G00.26n\n")
    f.write(f"% obs start : {start_time.strftime('%Y/%m/%d %H:%M:%S.0')} GPST (week2399 {start_gps_sec:.1f}s)\n")
    f.write(f"% obs end   : {end_time.strftime('%Y/%m/%d %H:%M:%S.0')} GPST (week2399 {end_gps_sec:.1f}s)\n")
    f.write("% pos mode  : single\n")
    f.write("% elev mask : 15.0 deg\n")
    f.write("% ionos opt : broadcast\n")
    f.write("% tropo opt : saastamoinen\n")
    f.write("% ephemeris : broadcast\n")
    f.write("%\n")
    f.write("% (lat/lon/height=WGS84/ellipsoidal,Q=1:fix,2:float,3:sbas,4:dgps,5:single,6:ppp,ns=# of satellites)\n")
    f.write("%  GPST                  latitude(deg) longitude(deg)  height(m)   Q  ns   sdn(m)   sde(m)   sdu(m)  sdne(m)  sdeu(m)  sdun(m) age(s)  ratio\n")

    # --- Generate Data Rows ---
    for i in range(num_rows):
        current_time = start_time + timedelta(seconds=i)
        time_str = current_time.strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
        
        # Calculate 2D XY movement
        lat_offset = LAT_AMPLITUDE * math.sin(i / 200.0)
        lon_offset = LON_AMPLITUDE * math.sin(i / 211.0)
        
        # Add offset to starting coordinates with slight GNSS jitter
        lat = START_LAT + lat_offset + np.random.normal(0, 0.00000002)
        lon = START_LON + lon_offset + np.random.normal(0, 0.00000002)
        alt = START_ALT + np.random.normal(0, 0.2)
        
        # Standard deviations and cross-covariances
        sdn = 4.6678 + np.random.normal(0, 0.05)
        sde = 4.5646 + np.random.normal(0, 0.05)
        sdu = 12.2582 + np.random.normal(0, 0.2)
        sdne = 0.8294 + np.random.normal(0, 0.02)
        sdeu = -3.4779 + np.random.normal(0, 0.02)
        sdun = 3.1510 + np.random.normal(0, 0.02)
        
        q = 5
        ns = np.random.randint(7, 11)
        age = 0.00
        ratio = 0.0

        line = (f"{time_str}  {lat:13.9f}  {lon:14.9f}  {alt:10.4f}  {q:2d}  {ns:2d}  "
                f"{sdn:7.4f}  {sde:7.4f}  {sdu:7.4f}  {sdne:7.4f}  {sdeu:8.4f}  {sdun:7.4f}  "
                f"{age:4.2f}    {ratio:3.1f}\n")
        f.write(line)

print(f"Data generation complete! Saved '{output_filename}'")
"""
Generates Data similar to real data, so sensetive data is secure, while providing a bigger dataset for training
"""