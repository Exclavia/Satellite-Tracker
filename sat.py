import time
from datetime import datetime
import requests
import pytz
from data.Sat_Info import import_data

# Imports satinfo.txt
import_data = import_data()

# Sends request to API
# Prints response, if CLI, or returns list if GUI
def get_sat(norad_id, latitude, longitude, retry=False, external=False):
    """
    norad_id = Satellite NORAD ID
    latitude/longitude = Observation location
    retry = Default: False | For internal recursion use only
    external = Default: False | Change to True if calling function from outside script.
    """
    # Set function variables
    sat_info = []
    sat_data = import_data
    sat_id = int(norad_id)
    in_lat = float(latitude)
    in_lon = float(longitude)
    pass_limit = 1
    local_tz_name = "America/Detroit"
    local_timezone = pytz.timezone(local_tz_name)
    location_dict = {"Lat": f"{in_lat}", "Lon": f"{in_lon}"}
    sat_info.append(location_dict)
    # Run through imported satellite data, checks data against norad id passed to function, appends matching satellite data to list
    parse_list = []
    for info in sat_data:
        if int(info.get("NORAD")) != sat_id: continue
        parse_list.append([int(info.get("NORAD")),
info.get("Name"), info.get("Mode"),
info.get("Uplink"), info.get("Downlink")])
    p_list = parse_list[0]
    if not retry and not external:
        print(f"\nFetching information on {p_list[1]} ({p_list[0]}) ...\n")
    base = "https://sat.terrestre.ar/passes/"
    api = f"{sat_id}?lat={in_lat}&lon={in_lon}&limit={pass_limit}"
    url = base + api
    # API request
    try:
        time.sleep(1)
        response = requests.get(url, timeout=None)

        if response.status_code == 200:
            sat_info.append(p_list)
            data = response.json()

            # Separates each part of pass
            rise_data = data[0].get("rise")
            culm_data = data[0].get("culmination")
            set_data = data[0].get("set")

            # Gets altitude (elevation)
            rise_elev = rise_data.get("alt")
            max_elev = culm_data.get("alt")
            set_elev = set_data.get("alt")
            elev_dict = {"RiseE": rise_elev, "MaxE": max_elev, "SetE": set_elev}
            sat_info.append(elev_dict)

            # Get timestamp
            rise_ts = rise_data.get("utc_timestamp")
            culm_ts = culm_data.get("utc_timestamp")
            set_ts = set_data.get("utc_timestamp")
            # Format datetime
            dt_rise = datetime.fromtimestamp(rise_ts, tz=local_timezone)
            dt_culm = datetime.fromtimestamp(culm_ts, tz=local_timezone)
            dt_set = datetime.fromtimestamp(set_ts, tz=local_timezone)
            rise_dtf = dt_rise.strftime("%Y-%m-%d at %I:%M:%S %p")
            culm_dtf = dt_culm.strftime("%Y-%m-%d at %I:%M:%S %p")
            set_dtf = dt_set.strftime("%Y-%m-%d at %I:%M:%S %p")
            dt_dict = {"RiseT": rise_dtf, "CulmT": culm_dtf, "SetT": set_dtf}
            sat_info.append(dt_dict)

            # CLI data display
            if not external:
                print(f"Next pass for: {p_list[1]} ({p_list[0]})")
                print(f"For Lat: {in_lat}, Lon: {in_lon}")
                print(f"Up: {p_list[3]}MHz | Down: {p_list[4]}MHz\nMode: {p_list[2]}")
                print("\nRise ===================")
                print(f"| {rise_dtf}")
                print(f"| Elevation: {rise_elev}°")

                print("\nCulmination ============")
                print(f"| {culm_dtf}")
                print(f"| Max Elevation: {max_elev}°")

                print("\nSet ====================")
                print(f"| {set_dtf}")
                print(f"| Elevation: {set_elev}°")
            else:
                return sat_info

        else:
            # Call function again if no response, sets retry flag to True. Won't try more than twice.
            if not retry:
                time.sleep(1)
                get_sat(sat_id, latitude=in_lat, longitude=in_lon, retry=True, external=external)
            else:

                # Request failures/errors still returns the satInfo list, with the requested data entries replaced with response code/error message.
                if not external:
                    print(f"Request failed: {response.status_code}")
                else:
                    err_msg = f"Request failed: {response.status_code}"
                    err_el = {"RiseE": err_msg, "MaxE": err_msg, "SetE": err_msg}
                    sat_info.append(err_el)
                    err_dt = {"RiseT": err_msg, "CulmT": err_msg, "SetT": err_msg}
                    sat_info.append(err_dt)

                    return sat_info

    except requests.exceptions.RequestException as e:
        if not external:
            print(f"An error occurred: {e}")
        else:
            err_msg = f"Request failed: {response.status_code}"
            err_el = {"RiseE": err_msg, "MaxE": err_msg, "SetE": err_msg}
            sat_info.append(err_el)
            err_dt = {"RiseT": err_msg, "CulmT": err_msg, "SetT": err_msg}
            sat_info.append(err_dt)
            return sat_info
