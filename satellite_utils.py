import requests
from sgp4.api import Satrec, jday
from datetime import datetime
import numpy as np

def fetch_satellite_data(norad_id):
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.strip().splitlines()
        if len(lines) >= 3:
            return {"name": lines[0], "tle1": lines[1], "tle2": lines[2]}
        else:
            return {"error": "Incomplete TLE data received."}
    except Exception as e:
        return {"error": str(e)}

def extract_satellite_info(data):
    if "error" in data:
        return None
    return {
        "name": data["name"],
        "tle_line1": data["tle1"],
        "tle_line2": data["tle2"]
    }

def compute_current_position(sat_info):
    sat = Satrec.twoline2rv(sat_info["tle_line1"], sat_info["tle_line2"])
    now = datetime.utcnow()
    jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second + now.microsecond / 1e6)
    e, r, v = sat.sgp4(jd, fr)
    if e == 0:
        x, y, z = r
        lat, lon = eci_to_latlon(x, y, z)
        return lat, lon
    else:
        raise ValueError("Failed to compute satellite position.")

def eci_to_latlon(x, y, z):
    R_earth = 6378.137  # km
    r = np.sqrt(x**2 + y**2 + z**2)
    lat = np.arcsin(z / r)
    lon = np.arctan2(y, x)
    return np.degrees(lat), np.degrees(lon)