import os
import csv
import time
from datetime import datetime
from skyfield.api import EarthSatellite, wgs84, load, utc
import pytz
from mods.import_sat import import_satellites
from mods.get_keps import get_keps


# Function loads local keps file, reads it, calculates, returns in list/dict
def get_sat(norad_id, usr_lat, usr_lon, usr_minalt):
    sat_import = import_satellites()
    file_path = get_keps(sat_group='amateur', file_format='csv')
    with load.open(file_path, mode='r') as f:
        data = list(csv.DictReader(f))
    # Converting function inputs
    sat_id = int(norad_id)
    lat_float = float(usr_lat)
    lon_float = float(usr_lon)
    min_alt = float(usr_minalt)
    # Setting Timescale/Datetime/Timezone
    t_s = load.timescale()
    local_tz = pytz.timezone('America/Detroit')
    epoch_now = time.time()
    epoch_then = epoch_now + 86400.00
    t0 = t_s.from_datetime(datetime.fromtimestamp(epoch_now, tz=local_tz))
    t1 = t_s.from_datetime(datetime.fromtimestamp(epoch_then, tz=local_tz))
    # Parsing Keps and returning easily callable data.
    earth_sats = [EarthSatellite.from_omm(t_s, fields) for fields in data]
    by_number = {sat.model.satnum: sat for sat in earth_sats}
    main_satellite = by_number[sat_id]
    my_pos = wgs84.latlon(lat_float, lon_float)
    # Using parsed kep-data to make a few lists to allow easier access to the information.
    sat_data = []
    sat_info = []
    for sat in earth_sats:
        if sat.model.satnum == sat_id:
            sat_info.append(sat.name)
        sat_dict = {
            "Name": sat.name,
            "NORAD": sat.model.satnum
            }
        sat_data.append(sat_dict)
    # Finding events using the two set timescales (Current time + 24hours)
    t, sat_events = main_satellite.find_events(my_pos, t0, t1, altitude_degrees=min_alt)
    event_names = 'Rises', 'Culminates', 'Sets'
    pass_limit = 1
    format_str = "%b %d, %Y at %I:%M:%S %p"
    # For loop to loop through data and grab only what we want based on pass_limit
    # Default: Next pass that rises above set min. elevation
    # Returns Rise/Max/Set elevation, datetime and satellite distance (in miles)
    for t_i, event in zip(t, sat_events):
        event_name = event_names[event]
        utc_datetime = t_i.astimezone(local_tz)
        format_datetime = utc_datetime.strftime(format_str)
        geocentric = main_satellite.at(t_i)
        pos_diff = main_satellite - my_pos
        topocentric = pos_diff.at(t_i)
        alt_el, _, sat_dx = topocentric.altaz()
        km_mile = float(sat_dx.km) * 0.621371
        dx_format = str(km_mile)[:6]
        pass_dict = {
            "Event": f"{event_name}",
            "When": f"{format_datetime}",
            "Elev": f"{str(alt_el)[:2]}°",
            "Distance": f"{dx_format}mi"
        }
        sat_info.append(pass_dict)
        if pass_limit == 3:
            break
        pass_limit = pass_limit + 1
    # Scans through satinfo.txt, finds inputted NORAD, returns additional information
    # Uplink frequency, Downlink frequency, Transmitter mode.
    for more in sat_import:
        if int(more.get("NORAD")) != sat_id: continue
        more_dict = {
            "Uplink": more.get("Uplink"),
            "Downlink": more.get("Downlink"),
            "Mode": more.get("Mode")
            }
        sat_info.append(more_dict)
    return sat_info