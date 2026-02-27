"""
Diagnostic script to trace the Lagna calculation bug.
Input: February 15, 1936, 08:32 AM, Nanjangud, India
Expected Lagna: Meena (Pisces) [index 11]
Actual Lagna:   Kanya (Virgo)  [index 5]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import pytz
import numpy as np

# Load skyfield
from skyfield.api import load, Topos
eph = load('de421.bsp')
earth = eph['earth']
ts = load.timescale()

# ---- Input ----
date_str = "1936-02-15"
time_str = "08:32"
lat = 11.8745   # Nanjangud latitude
lon = 76.6832   # Nanjangud longitude
timezone_str = "Asia/Kolkata"

tz = pytz.timezone(timezone_str)
naive_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
local_dt = tz.localize(naive_dt)
utc_dt = local_dt.astimezone(pytz.utc)

print("=" * 60)
print("LAGNA CALCULATION DIAGNOSTIC")
print("=" * 60)
print(f"Local Time:  {local_dt}")
print(f"UTC Time:    {utc_dt}")
print(f"Location:    Nanjangud, India (lat={lat}, lon={lon})")
print()

# ---- Step 1: Skyfield time object ----
# BUG CANDIDATE: The code passes local_dt to ts.from_datetime()
# Skyfield requires timezone-aware datetimes, but let's check both
t_from_local = ts.from_datetime(local_dt)
t_from_utc   = ts.from_datetime(utc_dt)

print(f"t_from_local.tt (Julian TT): {t_from_local.tt:.6f}")
print(f"t_from_utc.tt   (Julian TT): {t_from_utc.tt:.6f}")
print(f"Difference in TT (should be 0 if tz-aware): {t_from_local.tt - t_from_utc.tt:.6f} days")
print()

# ---- Step 2: GAST (Greenwich Apparent Sidereal Time) ----
gast_local = t_from_local.gast
gast_utc   = t_from_utc.gast
print(f"GAST from local_dt: {gast_local:.6f} hours")
print(f"GAST from utc_dt:   {gast_utc:.6f} hours")
print(f"GAST difference:    {gast_local - gast_utc:.6f} hours")
print()

# ---- Step 3: LST (Local Sidereal Time) ----
lst_local = (gast_local + lon / 15.0) % 24.0
lst_utc   = (gast_utc   + lon / 15.0) % 24.0
print(f"LST from local_dt: {lst_local:.6f} hours ({lst_local * 15:.4f}°)")
print(f"LST from utc_dt:   {lst_utc:.6f} hours ({lst_utc * 15:.4f}°)")
print()

# ---- Step 4: Ayanamsha ----
def get_ayanamsha(jd):
    t = (jd - 2451545.0) / 36525.0
    ayanamsha = 23.8580833 + (1.3973333 * t) + (0.0003088 * t * t)
    return ayanamsha

ayanamsha = get_ayanamsha(t_from_utc.tt)
print(f"Ayanamsha (Lahiri): {ayanamsha:.6f}°")
print()

# ---- Step 5: Ascendant formula (current code) ----
eps = 23.4392911  # Hardcoded J2000 obliquity (BUG CANDIDATE)

def compute_ascendant(lst_hours, lat_deg, eps_deg, label=""):
    lat_rad = np.radians(lat_deg)
    lst_rad = np.radians(lst_hours * 15.0)
    eps_rad = np.radians(eps_deg)

    y = -np.cos(lst_rad)
    x = (np.sin(lst_rad) * np.cos(eps_rad)) + (np.tan(lat_rad) * np.sin(eps_rad))

    asc_rad = np.arctan2(y, x)
    asc_deg_tropical = np.degrees(asc_rad)
    asc_deg_tropical = (asc_deg_tropical + 360) % 360

    asc_deg_sidereal = (asc_deg_tropical - ayanamsha) % 360
    lagna_idx = int(asc_deg_sidereal / 30.0) % 12

    SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
             "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
    SIGNS_SA = ["Mesha","Vrishabha","Mithuna","Karkataka","Simha","Kanya",
                "Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]

    print(f"  [{label}]")
    print(f"    LST:              {lst_hours:.6f} h ({lst_hours*15:.4f}°)")
    print(f"    Tropical Asc:     {asc_deg_tropical:.4f}°")
    print(f"    Sidereal Asc:     {asc_deg_sidereal:.4f}°")
    print(f"    Lagna Index:      {lagna_idx} => {SIGNS_SA[lagna_idx]} ({SIGNS[lagna_idx]})")
    return lagna_idx, asc_deg_sidereal

print("=== ASCENDANT CALCULATION (current code - uses local_dt) ===")
idx1, deg1 = compute_ascendant(lst_local, lat, eps, "Using local_dt GAST")
print()

print("=== ASCENDANT CALCULATION (using utc_dt) ===")
idx2, deg2 = compute_ascendant(lst_utc, lat, eps, "Using utc_dt GAST")
print()

# ---- Step 6: Correct obliquity for 1936 ----
# Obliquity changes over time. For 1936, it's slightly different from J2000.
T = (t_from_utc.tt - 2451545.0) / 36525.0
eps_1936 = 23.439291111 - 0.013004167 * T - 0.000000164 * T**2 + 0.000000504 * T**3
print(f"=== OBLIQUITY CHECK ===")
print(f"  Hardcoded J2000 obliquity: {eps:.6f}°")
print(f"  Correct 1936 obliquity:    {eps_1936:.6f}°")
print(f"  Difference:                {eps_1936 - eps:.6f}°")
print()

print("=== ASCENDANT WITH CORRECT 1936 OBLIQUITY (using utc_dt) ===")
idx3, deg3 = compute_ascendant(lst_utc, lat, eps_1936, "utc_dt + correct obliquity")
print()

# ---- Step 7: Summary ----
print("=" * 60)
print("SUMMARY")
print("=" * 60)
SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
         "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
SIGNS_SA = ["Mesha","Vrishabha","Mithuna","Karkataka","Simha","Kanya",
            "Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]

print(f"Expected:                    Meena (Pisces) = index 11")
print(f"Current code result:         {SIGNS_SA[idx1]} ({SIGNS[idx1]}) = index {idx1}")
print(f"With UTC fix:                {SIGNS_SA[idx2]} ({SIGNS[idx2]}) = index {idx2}")
print(f"With UTC + obliquity fix:    {SIGNS_SA[idx3]} ({SIGNS[idx3]}) = index {idx3}")
print()

# ---- Step 8: Check if the formula itself is correct ----
# The standard ascendant formula is:
# RAMC = LST * 15 (Right Ascension of Midheaven in degrees)
# tan(Asc) = cos(RAMC) / -(sin(RAMC)*cos(eps) + tan(lat)*sin(eps))
# Note: some sources use a different sign convention
print("=== ALTERNATIVE FORMULA CHECK ===")
lst_rad = np.radians(lst_utc * 15.0)
lat_rad = np.radians(lat)
eps_rad = np.radians(eps_1936)

# Standard formula (Placidus/Equal house):
# Asc = atan2(cos(RAMC), -(sin(RAMC)*cos(eps) + tan(lat)*sin(eps)))
y_alt = np.cos(lst_rad)
x_alt = -(np.sin(lst_rad) * np.cos(eps_rad) + np.tan(lat_rad) * np.sin(eps_rad))
asc_alt = np.degrees(np.arctan2(y_alt, x_alt))
asc_alt = (asc_alt + 360) % 360
asc_sid_alt = (asc_alt - ayanamsha) % 360
idx_alt = int(asc_sid_alt / 30.0) % 12
print(f"  Alternative formula tropical: {asc_alt:.4f}°")
print(f"  Alternative formula sidereal: {asc_sid_alt:.4f}°")
print(f"  Result: {SIGNS_SA[idx_alt]} ({SIGNS[idx_alt]}) = index {idx_alt}")
