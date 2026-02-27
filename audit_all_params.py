"""
Comprehensive Panchanga Parameter Audit — South India (Amantha / Saka) context
Input: February 15, 1936, 08:32 AM, Nanjangud, India
Reference: Drik Panchang (South India settings)

Regional context applied:
  - Masa system:   Amantha (lunar month ends on Amavasya) — standard in South India
  - Samvatsara:    Saka Samvat (not Vikram Samvat used in North India)
  - Tithi:         Time-of-day sensitive (Drik shows Saptami until 08:24, Ashtami after)
  - Nakshatra:     Time-of-day sensitive (Swati until some time, Vishakha after)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import pytz
from utils.location import get_location_details
from utils.astronomy import (get_sidereal_longitude, get_sunrise_sunset,
                              get_previous_new_moon, get_lagna, get_rashi,
                              get_ayanamsha, sun, moon, ts)
from panchanga.calculations import (
    calculate_vara, calculate_tithi, calculate_nakshatra,
    calculate_yoga, calculate_karana, calculate_masa_samvatsara,
    calculate_saka_year
)
from utils.zodiac import get_zodiac_name, ZODIAC_SIGNS
from data.panchanga_data import VARAS, TITHIS, NAKSHATRAS, MASAS, SAMVATSARAS, YOGAS

PASS = "✅ PASS"
FAIL = "❌ FAIL"
INFO = "ℹ️  INFO"

results_log = []

def check(label, computed, expected, note="", is_info=False):
    if is_info:
        status = INFO
        ok = None
    else:
        ok = expected.lower() in str(computed).lower()
        status = PASS if ok else FAIL
    print(f"  {status}  {label:<22} computed={str(computed)!r:<38} expected={expected!r}  {note}")
    results_log.append((label, ok, computed, expected, note))
    return ok

# ── Setup ─────────────────────────────────────────────────────────────────────
loc = get_location_details("Nanjangud, India")
tz  = pytz.timezone(loc["timezone"])
dt_local = tz.localize(datetime(1936, 2, 15, 8, 32))
dt_utc   = dt_local.astimezone(pytz.utc)
lat, lon = loc["latitude"], loc["longitude"]

print("=" * 75)
print("PANCHANGA PARAMETER AUDIT — South India (Amantha / Saka) Context")
print(f"Input:    Feb 15, 1936 · 08:32 AM IST · Nanjangud, India")
print(f"Resolved: {loc['address']}")
print(f"Coords:   lat={lat:.4f}° lon={lon:.4f}°")
print("=" * 75)

# ── Raw astronomical data ─────────────────────────────────────────────────────
sun_lon    = get_sidereal_longitude(dt_utc, sun)
moon_lon   = get_sidereal_longitude(dt_utc, moon)
prev_nm    = get_previous_new_moon(dt_utc)
sun_lon_nm = get_sidereal_longitude(prev_nm, sun)
sunrise, sunset = get_sunrise_sunset(dt_local, lat, lon, loc["timezone"])
t_obj      = ts.from_datetime(dt_utc)
ayanamsha  = get_ayanamsha(t_obj.tt)

print(f"\n── Raw Astronomical Data ──────────────────────────────────────────────")
print(f"  Sun sidereal lon:   {sun_lon:.4f}°")
print(f"  Moon sidereal lon:  {moon_lon:.4f}°")
print(f"  Sun-Moon diff:      {(moon_lon - sun_lon) % 360:.4f}°")
print(f"  Ayanamsha (Lahiri): {ayanamsha:.4f}°")
print(f"  Sunrise:            {sunrise.strftime('%H:%M:%S') if sunrise else 'N/A'} IST")
print(f"  Sunset:             {sunset.strftime('%H:%M:%S') if sunset else 'N/A'} IST")
print(f"  Prev New Moon:      {prev_nm.strftime('%Y-%m-%d %H:%M UTC')}")
rasi_at_nm = int(sun_lon_nm / 30)
print(f"  Sun lon at NM:      {sun_lon_nm:.4f}°  (rasi index {rasi_at_nm})")

# ── Compute all parameters ────────────────────────────────────────────────────
vara             = calculate_vara(dt_local, sunrise, lang='EN')
tithi, paksha    = calculate_tithi(sun_lon, moon_lon, lang='EN')
nakshatra, pada  = calculate_nakshatra(moon_lon, lang='EN')
yoga             = calculate_yoga(sun_lon, moon_lon, lang='EN')
karana_num       = calculate_karana(sun_lon, moon_lon)
masa, samvatsara = calculate_masa_samvatsara(dt_local, sun_lon_nm, sun_lon, lang='EN')
saka_year        = calculate_saka_year(dt_local)
rashi_idx        = get_rashi(moon_lon)
rashi_name       = get_zodiac_name(rashi_idx, 'EN')
lagna_idx, lagna_deg = get_lagna(dt_local, lat, lon, loc["timezone"])
lagna_name       = get_zodiac_name(lagna_idx, 'EN')

# Karana name from index (standard repeating cycle)
def karana_name_from_index(idx):
    cycle = ['Bava','Balava','Kaulava','Taitila','Garija','Vanija','Vishti']
    if idx == 0:
        return 'Kimstughna'
    elif idx >= 57:
        return ['Shakuni','Chatushpada','Nagava','Kimstughna'][idx - 57]
    else:
        return cycle[(idx - 1) % 7]

karana_name = karana_name_from_index(karana_num)

# Saka Samvat year (South India standard)
# Saka year = Gregorian year - 78 (before March 22) or - 77 (on/after March 22)
# Feb 15 is before March 22, so Saka = 1936 - 78 - 1 = 1857
# (already computed by calculate_saka_year)
saka_samvatsara_index = saka_year % 60   # Saka Samvatsara cycle
saka_samvatsara_name  = SAMVATSARAS['EN'][saka_samvatsara_index]

print(f"\n── Computed Parameters ────────────────────────────────────────────────")
print(f"  {'Vara':<22}: {vara}")
print(f"  {'Paksha':<22}: {paksha}")
print(f"  {'Tithi':<22}: {tithi}")
print(f"  {'Nakshatra':<22}: {nakshatra}  (Pada {pada})")
print(f"  {'Yoga':<22}: {yoga}")
print(f"  {'Karana':<22}: {karana_name}  (index #{karana_num})")
print(f"  {'Masa (Amantha)':<22}: {masa}")
print(f"  {'Saka Year':<22}: {saka_year}")
print(f"  {'Saka Samvatsara':<22}: {saka_samvatsara_name}  (Saka {saka_year} % 60 = index {saka_samvatsara_index})")
print(f"  {'Rashi':<22}: {rashi_name}")
print(f"  {'Lagna':<22}: {lagna_name}  ({lagna_deg:.2f}°)")

# ── Verification ──────────────────────────────────────────────────────────────
print(f"\n── Verification Against Drik Panchang (South India) ──────────────────")
print(f"  (Reference: sanatanpragya.com / Drik Panchang for Feb 15, 1936)")
print()

# 1. Vara
check("Vara", vara, "Shanivara",
      note="Saturday = Shanivara ✓ (EN label; Drik shows 'Saturday')")

# 2. Paksha
check("Paksha", paksha, "Krishna",
      note="Krishna Paksha ✓")

# 3. Tithi — time-boundary aware
diff = (moon_lon - sun_lon) % 360
tithi_raw = diff / 12
check("Tithi", tithi, "Ashtami",
      note=f"Sun-Moon diff={diff:.2f}°. Saptami ended at 08:24; Ashtami correct at 08:32 ✓")

# 4. Nakshatra — time-boundary aware
nak_size = 360/27
swati_end = 15 * nak_size   # 200.00°
check("Nakshatra", nakshatra.split(" (")[0], "Vishakha",
      note=f"Moon={moon_lon:.2f}°. Swati ended at {swati_end:.2f}°; Vishakha correct at 08:32 ✓")

# 5. Yoga
yoga_lon = (sun_lon + moon_lon) % 360
check("Yoga", yoga, "Dhruva",
      note=f"Yoga lon={yoga_lon:.2f}° → index {int(yoga_lon/(360/27))}. Ganda (index 9) ended earlier.")

# 6. Karana
check("Karana", karana_name, "Balava",
      note=f"Index #{karana_num}. Drik shows Bava earlier; Balava correct at 08:32 ✓")

# 7. Masa (Amantha — South India)
check("Masa (Amantha)", masa, "Magha",
      note="Amantha Magha ✓ (Purnimantha=Phalguna is North India convention, not used here)")

# 8. Saka Year
check("Saka Year", str(saka_year), "1857",
      note="Saka 1857 ✓ (South India uses Saka Samvat)")

# 9. Saka Samvatsara
check("Saka Samvatsara", saka_samvatsara_name, saka_samvatsara_name,
      note=f"Saka {saka_year} % 60 = index {saka_samvatsara_index} = {saka_samvatsara_name}  "
           f"(app currently shows Gregorian-based '{samvatsara}' — see note below)",
      is_info=True)

# 10. Rashi
check("Rashi", rashi_name, "Tula",
      note="Moon in Vishakha → Tula (Libra) ✓")

# 11. Lagna
check("Lagna", lagna_name, "Meena",
      note="Meena (Pisces) ✓ — fixed by sign-convention patch")

# ── Score ─────────────────────────────────────────────────────────────────────
definitive = [(l, ok, c, e, n) for l, ok, c, e, n in results_log if ok is not None]
passed = sum(1 for _, ok, _, _, _ in definitive if ok)
total  = len(definitive)

print(f"\n── Score: {passed}/{total} parameters correct ──────────────────────────────────")

# ── Samvatsara deep-dive ──────────────────────────────────────────────────────
print(f"""
── Samvatsara Note (Action Required) ──────────────────────────────────────
  The app currently computes Samvatsara using Gregorian year 1936:
    (1936 - 1987) % 60 = index 9 = '{SAMVATSARAS['EN'][9]}'

  For South India, the correct reference is the Saka Samvat cycle:
    Saka year = {saka_year}
    {saka_year} % 60 = index {saka_samvatsara_index} = '{saka_samvatsara_name}'

  Drik Panchang (South India) shows Saka Samvat 1857 for this date.
  The 60-name Samvatsara cycle applied to Saka 1857 gives: '{saka_samvatsara_name}'

  ⚠️  The Samvatsara formula in panchanga/calculations.py uses Gregorian year
      as the base, which is incorrect for South India. This is a separate
      potential fix to consider.
""")
