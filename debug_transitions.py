
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import pytz
from utils.astronomy import get_sidereal_longitude, sun, moon

def check_parameters():
    print("Checking Yoga and Karana transitions for Feb 15, 1936 near Nanjangud")
    location = "Nanjangud, India"
    lat, lon = 12.1221, 76.6843
    tz = pytz.timezone("Asia/Kolkata")
    
    # Check every 15 minutes from midnight to noon
    start_time = tz.localize(datetime(1936, 2, 15, 0, 0))
    for i in range(48): # 12 hours
        dt = start_time + timedelta(minutes=15 * i)
        dt_utc = dt.astimezone(pytz.utc)
        
        sun_lon = get_sidereal_longitude(dt_utc, sun)
        moon_lon = get_sidereal_longitude(dt_utc, moon)
        
        # Yoga
        yoga_lon = (sun_lon + moon_lon) % 360
        yoga_idx = int(yoga_lon / (360/27))
        
        # Karana
        diff = (moon_lon - sun_lon) % 360
        karana_idx = int(diff / 6)
        
        # Tithi
        tithi_idx = int(diff / 12)
        
        print(f"{dt.strftime('%H:%M')} -> Tithi:{tithi_idx} Karana:{karana_idx} Yoga:{yoga_idx} Sun:{sun_lon:.2f} Moon:{moon_lon:.2f}")

if __name__ == "__main__":
    check_parameters()
