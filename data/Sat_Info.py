import os

def import_data():
    """Imports Satellite information via the satinfo.txt in the /data directory
    Returns->list [ {
        "Name" : Satellite Name,
        "NORAD" : NORAD ID,
        "Mode" : Transmitter Mode,
        "Uplink" : Uplink Frequency,
        "Downlink" : Downlink Frequency,
        "AltName" : Alternative satellite name  } ], ...
    """
    data_dir = os.path.dirname(__file__)
    sat_info = []
    with open(os.path.join(data_dir, "satinfo.txt"), "rt") as info:
        info_list = info.read().split("\n")
        for x in info_list:
            x_list = x.split(";")
            sat_dict = {
                "Name": x_list[0],
                "NORAD": x_list[1],
                "Mode": x_list[2],
                "Uplink": x_list[3],
                "Downlink": x_list[4],
                "AltName": x_list[5],
            }
            sat_info.append(sat_dict)
    return sat_info
