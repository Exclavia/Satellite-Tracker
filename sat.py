import requests
from datetime import datetime
import pytz
import time
from data.Sat_Info import importSats

satdata = importSats()

def getSat(norad_id, latitude, longitude, retry=False, external=False, satData=satdata):
    satInfo = []
    norad_id = norad_id
    lat = latitude
    lon = longitude
    passLimit = 1
    localTzName = 'America/Detroit'
    local_timezone = pytz.timezone(localTzName)
    locDict = {
    "Latitude": f"{lat}",
    "Longitude": f"{lon}"
    }
    satInfo.append(locDict)
    parseList = []
    for inf in satData:
        if int(inf.get("NORAD")) != norad_id:
            continue
        else:
            parseList.append([int(inf.get("NORAD")), inf.get("Name"), inf.get("Mode"), inf.get("Uplink"), inf.get("Downlink"), inf.get("AltName")])       
    plist = parseList[0]
    
    if not retry and not external: print(f"\nFetching information on {plist[1]} ({plist[0]}) ...\n")
    
    url = f"https://sat.terrestre.ar/passes/{norad_id}?lat={lat}&lon={lon}&limit={passLimit}"
    
    try:
        time.sleep(1)
        response = requests.get(url, timeout=None)
        
        if response.status_code == 200:
            satInfo.append(plist)            
            data = response.json()
            rise = data[0].get("rise")
            culm = data[0].get("culmination")
            sett = data[0].get("set")
            riseElev = rise.get("alt")
            maxElev = culm.get("alt")
            setElev = sett.get("alt")
            elevDict = {
            "RiseEl": riseElev,
            "MaxEl": maxElev,
            "SetEl": setElev
            }
            satInfo.append(elevDict)
            
            rise_ts = rise.get("utc_timestamp")
            culm_ts = culm.get("utc_timestamp")
            set_ts = sett.get("utc_timestamp")
            
            dt_rise = datetime.fromtimestamp(rise_ts, tz=local_timezone)
            dt_culm = datetime.fromtimestamp(culm_ts, tz=local_timezone)
            dt_set = datetime.fromtimestamp(set_ts, tz=local_timezone)
            riseForm = dt_rise.strftime('%Y-%m-%d at %I:%M:%S %p')
            culmForm = dt_culm.strftime('%Y-%m-%d at %I:%M:%S %p')
            setForm = dt_set.strftime('%Y-%m-%d at %I:%M:%S %p')
            datetimeDict = {
            "RiseT": riseForm,
            "CulmT": culmForm,
            "SetT": setForm
            }
            satInfo.append(datetimeDict)
            if not external:
                print(f"Next pass for: {plist[1]} ({plist[0]})")
                print(f"For Lat: {lat}, Lon: {lon}")
                print(f"Up: {plist[3]}MHz | Down: {plist[4]}MHz\nMode: {plist[2]}")
                print("\nRise ===================")
                print(f"| {riseForm}")
                print(f"| Elevation: {riseElev}°")
                
                print("\nCulmination ============")
                print(f"| {culmForm}")
                print(f"| Max Elevation: {maxElev}°")
                
                print("\nSet ====================")
                print(f"| {setForm}")
                print(f"| Elevation: {setElev}°")
            else:
                return satInfo
        
        else:
            
            if not retry:
                time.sleep(1)
                getSat(norad_id, retry=True, external=external)
            else:
                if not external:
                    print(f"Request failed: {response.status_code}")
                else:
                    errmsg = f"Request failed: {response.status_code}"
                    err_el = {
                    "RiseEl": errmsg,
                    "MaxEl": errmsg,
                    "SetEl": errmsg
                    }
                    satInfo.append(err_el)
                    err_dt = {
                    "RiseT": errmsg,
                    "CulmT": errmsg,
                    "SetT": errmsg
                    }
                    satInfo.append(err_dt)
                    
                    return satInfo
    
    except requests.exceptions.RequestException as e:
        if not external:
            print(f"An error occurred: {e}")
        else:
            errmsg = f"Request failed: {response.status_code}"
            err_el = {
                    "RiseEl": errmsg,
                    "MaxEl": errmsg,
                    "SetEl": errmsg }
                    
            satInfo.append(err_el)
            err_dt = {
                    "RiseT": errmsg,
                    "CulmT": errmsg,
                    "SetT": errmsg
                    }
            satInfo.append(err_dt)
                    
            return satInfo

if __name__ == "__main__":
    lat = input("Input Latitude: ")
    lon = input("\nInput Longitude: ")
    print("")
    fulldata = []
    num = 1
    for sats in satdata:
        options = {
            "Opt": num,
            "Name": sats.get("Name"),
            "NORAD": sats.get("NORAD")
            }
        fulldata.append(options)
        num = num + 1
    for x in fulldata:
        print(f"{x.get('Opt')}. {x.get('Name')}")
    useroption = input("Please select from the satellite options: ")
    selection = 0
    for y in fulldata:
        if int(y.get("Opt")) == int(useroption):
            selection = selection + int(y.get("NORAD"))
        else:
            continue
    if selection == 0:
        print(f"Option not found")
    else:
        getSat(selection, latitude=lat, longitude=lon)
