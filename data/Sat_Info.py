import os

def importSats():
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
    satInfo = []
    with open(os.path.join(data_dir, "satinfo.txt"), "rt") as info:
        infolist = info.read().split("\n")
        for x in infolist:
            xlist = x.split(";")
            satDict = {
                "Name": xlist[0],
                "NORAD": xlist[1],
                "Mode": xlist[2],
                "Uplink": xlist[3],
                "Downlink": xlist[4],
                "AltName": xlist[5],
            }
            satInfo.append(satDict)
    return satInfo


if __name__ == "__main__":
    plist = []
    testid = 43017
    satdata = importSats()
    for i in satdata:
        if int(i.get("NORAD")) != testid:
            continue
        else:
            plist.append(
                [
                    int(i.get("NORAD")),
                    i.get("Name"),
                    i.get("Mode"),
                    i.get("Uplink"),
                    i.get("Downlink"),
                    i.get("AltName"),
                ]
            )
    uplist = plist[0]
    print(uplist[0], uplist[1])
