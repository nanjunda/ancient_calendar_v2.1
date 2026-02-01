import argparse
from datetime import datetime
import pytz
from utils.location import get_location_details
from utils.astronomy import get_sidereal_longitude, get_sunrise_sunset, sun, moon, get_previous_new_moon
from panchanga.calculations import (
    calculate_vara, calculate_tithi, calculate_nakshatra, 
    calculate_yoga, calculate_karana, calculate_masa_samvatsara,
    calculate_saka_year
)

def main():
    parser = argparse.ArgumentParser(description="Gregorian to Hindu Panchanga Converter")
    parser.add_argument("--date", type=str, help="Date in YYYY-MM-DD format", required=True)
    parser.add_argument("--time", type=str, help="Time in HH:MM (24-hour) format", required=True)
    parser.add_argument("--location", type=str, help="Location (City, State, Country)", required=True)

    args = parser.parse_args()

    try:
        # 1. Resolve Location
        print(f"Resolving location: {args.location}...")
        loc = get_location_details(args.location)
        print(f"Found: {loc['address']}")
        print(f"Coords: {loc['latitude']}, {loc['longitude']} | TZ: {loc['timezone']}")

        # 2. Parse DateTime
        dt_str = f"{args.date} {args.time}"
        naive_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        local_tz = pytz.timezone(loc["timezone"])
        local_dt = local_tz.localize(naive_dt)
        utc_dt = local_dt.astimezone(pytz.utc)

        # 3. Get Astronomical Data
        print("\nCalculating astronomical positions...")
        sun_lon = get_sidereal_longitude(utc_dt, sun)
        moon_lon = get_sidereal_longitude(utc_dt, moon)
        
        sunrise, sunset = get_sunrise_sunset(local_dt, loc["latitude"], loc["longitude"], loc["timezone"])
        
        # 4. Calculate Panchanga Elements
        vara = calculate_vara(local_dt, sunrise)
        tithi, paksha = calculate_tithi(sun_lon, moon_lon)
        nakshatra, nak_pada = calculate_nakshatra(moon_lon)
        yoga = calculate_yoga(sun_lon, moon_lon)
        karana_num = calculate_karana(sun_lon, moon_lon)
        
        # New Moon for Masa/Samvatsara
        prev_nm_utc = get_previous_new_moon(utc_dt)
        sun_lon_at_nm = get_sidereal_longitude(prev_nm_utc, sun)
        
        masa, samvatsara = calculate_masa_samvatsara(local_dt, sun_lon_at_nm, sun_lon)

        # 5. Display Results
        print("\n" + "="*40)
        print("       HINDU PANCHANGA REPORT")
        print("="*40)
        print(f"Input Date/Time : {local_dt.strftime('%Y-%m-%d %H:%M:%S')} ({loc['timezone']})")
        print(f"Location        : {loc['address']}")
        print(f"Sunrise         : {sunrise.strftime('%H:%M:%S') if sunrise else 'N/A'}")
        print(f"Sunset          : {sunset.strftime('%H:%M:%S') if sunset else 'N/A'}")
        print("-"*40)
        print(f"Samvatsara      : {samvatsara}")
        print(f"Saka Varsha     : {calculate_saka_year(local_dt)} (Civil Era)")
        print(f"Masa (Month)    : {masa}")
        print(f"Paksha          : {paksha}")
        print(f"Tithi           : {tithi}")
        print(f"Vara (Weekday)  : {vara}")
        print(f"Nakshatra       : {nakshatra}")
        print(f"Yoga            : {yoga}")
        print(f"Karana (Index)  : {karana_num}")
        print("="*40)

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
