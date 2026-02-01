from data.panchanga_data import *
import math

def calculate_vara(local_time, sunrise_time, lang='EN'):
    """
    Vara (Weekday) starts at Sunrise.
    """
    mapping = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0}
    
    if local_time < sunrise_time:
        weekday = (local_time.weekday() - 1) % 7
    else:
        weekday = local_time.weekday()
        
    return VARAS[lang][mapping[weekday]]

def calculate_tithi(sun_lon, moon_lon, lang='EN'):
    diff = (moon_lon - sun_lon) % 360
    tithi_index = int(diff / 12)
    paksha = PAKSHAS[lang][0] if tithi_index < 15 else PAKSHAS[lang][1]
    return TITHIS[lang][tithi_index], paksha

def calculate_nakshatra(moon_lon, lang='EN'):
    """
    Calculates Nakshatra and Pada.
    """
    nakshatra_index = int(moon_lon / (360/27))
    # Each nakshatra is 13°20' (13.333... degrees)
    # Each pada is 3°20' (3.333... degrees)
    pada = int((moon_lon % (360/27)) / (360/108)) + 1
    
    nak_name = NAKSHATRAS[lang][nakshatra_index]
    star_name = NAKSHATRA_STARS[nakshatra_index]
    
    return f"{nak_name} ({star_name})", pada

def calculate_yoga(sun_lon, moon_lon, lang='EN'):
    yoga_lon = (sun_lon + moon_lon) % 360
    yoga_index = int(yoga_lon / (360/27))
    return YOGAS[lang][yoga_index]

def calculate_karana(sun_lon, moon_lon):
    diff = (moon_lon - sun_lon) % 360
    karana_index = int(diff / 6)
    return karana_index + 1

def calculate_masa_name(sun_lon_at_nm, lang='EN'):
    rasi_index = int(sun_lon_at_nm / 30)
    masa_mapping = {
        11: 0, # Meena -> Chaitra
        0: 1,  # Mesha -> Vaishakha
        1: 2,  # Vrishabha -> Jyeshtha
        2: 3,  # Mithuna -> Ashadha
        3: 4,  # Karka -> Shravana
        4: 5,  # Simha -> Bhadrapada
        5: 6,  # Kanya -> Ashvin
        6: 7,  # Tula -> Kartika
        7: 8,  # Vrishchika -> Margashirsha
        8: 9,  # Dhanu -> Pausha
        9: 10, # Makara -> Magha
        10: 11 # Kumbha -> Phalguna
    }
    return MASAS[lang][masa_mapping[rasi_index]]

def calculate_masa_samvatsara(local_dt, sun_lon_at_nm, sun_lon_now, lang='EN'):
    """
    Calculates Masa and Samvatsara name.
    Samvatsara changes at Ugadi (Chaitra Shukla Pratipada).
    """
    # 1. Determine Masa Name
    rasi_index = int(sun_lon_at_nm / 30)
    masa_mapping = {
        11: 0, # Meena -> Chaitra
        0: 1,  # Mesha -> Vaishakha
        1: 2,  # Vrishabha -> Jyeshtha
        2: 3,  # Mithuna -> Ashadha
        3: 4,  # Karka -> Shravana
        4: 5,  # Simha -> Bhadrapada
        5: 6,  # Kanya -> Ashvin
        6: 7,  # Tula -> Kartika
        7: 8,  # Vrishchika -> Margashirsha
        8: 9,  # Dhanu -> Pausha
        9: 10, # Makara -> Magha
        10: 11 # Kumbha -> Phalguna
    }
    masa_idx = masa_mapping[rasi_index]
    masa_name = MASAS[lang][masa_idx]
    
    # 2. Determine Samvatsara Index
    # Base year 1987 was Prabhava (Index 0) at Ugadi.
    year = local_dt.year
    
    # If we are in the last few months of the Vedic year (Pausha-Phalguna) 
    # but the Gregorian year has already rolled over (Jan-Apr), 
    # we are still in the Samvatsara of the PREVIOUS Gregorian year.
    if masa_idx >= 9 and local_dt.month <= 4:
        effective_year = year - 1
    # Conversely, if Ugadi happens early (e.g. in March) and we are in Chaitra,
    # the new Samvatsara has already started even if it's "early" Gregorian.
    else:
        effective_year = year

    samvat_index = (effective_year - 1987) % 60
    return masa_name, SAMVATSARAS[lang][samvat_index]

def calculate_saka_year(date_obj):
    """
    Calculates the Saka Varsha (Saka Era) year.
    The Saka Era started in 78 AD.
    The New Year starts on March 22 (March 21 in leap years).
    """
    gregorian_year = date_obj.year
    
    # Determine cutoff date for the current year
    # Leap year check: divisible by 4 but not 100, unless divisible by 400
    is_leap = (gregorian_year % 4 == 0 and gregorian_year % 100 != 0) or (gregorian_year % 400 == 0)
    cutoff_day = 21 if is_leap else 22
    
    # Compare current date with cutoff (March = month 3)
    if date_obj.month > 3 or (date_obj.month == 3 and date_obj.day >= cutoff_day):
        return gregorian_year - 78
    else:
        return gregorian_year - 79

def format_panchanga_report(dt_local, loc_address, loc_timezone, sunrise, sunset, samvatsara, masa, paksha, tithi, vara, nakshatra, nak_pada, yoga, karana, lang='EN'):
    labels = REPORT_LABELS[lang]
    
    report = f"""
       {labels['title']}
========================================
{labels['input_dt']} : {dt_local.strftime('%Y-%m-%d %H:%M:%S')} ({loc_timezone})
{labels['location']}        : {loc_address}
{labels['sunrise']}         : {sunrise.strftime('%H:%M:%S') if sunrise else 'N/A'}
{labels['sunset']}          : {sunset.strftime('%H:%M:%S') if sunset else 'N/A'}
----------------------------------------
{labels['samvatsara']}      : {samvatsara}
{labels['masa']}    : {masa}
{labels['paksha']}          : {paksha}
{labels['tithi']}           : {tithi}
{labels['vara']}  : {vara}
{labels['nakshatra']}       : {nakshatra} {labels['pada']} {nak_pada}
{labels['yoga']}            : {yoga}
{labels['karana']}  : {karana}
========================================
"""
    return report
