# Satellite tracker script + GUI
[pylint]()

Python script utilizing third-party hosted Skyfield API: [Sat.Terrestre.ar](https://sat.terrestre.ar/), as of 2025/06/23, that shows the next pass for a selected satellite over a given latitude and longitude.

<img src="https://raw.githubusercontent.com/Exclavia/Satellite-Tracker/refs/heads/main/images/screenshot.png" height="500"/>

Self-hosted API option coming soon.

## How to use
Script can be used by either running the `sat.py` script for a CLI, or by running the `gui.py` script for a Tkinter GUI.

## Satellites
Satellites currently available are a selection of FM/APRS/CW amateur radio satellites. 
- [Diwata-2B](https://db.satnogs.org/satellite/HIEK-3729-5596-2727-4744)
- [Duchifat-1](https://db.satnogs.org/satellite/KVVP-7917-6314-8782-3778)
- [EYESAT-1](https://db.satnogs.org/satellite/XTDR-0995-4168-5549-5936)
- [Fox-1B](https://db.satnogs.org/satellite/PMAW-9203-2442-8666-3249)
- [ISS](https://db.satnogs.org/satellite/XSKZ-5603-1870-9019-3066)
- [LilacSat-2](https://db.satnogs.org/satellite/AHVS-7983-8710-8819-8034)
- [PCSAT](https://db.satnogs.org/satellite/MIOI-0494-0446-3367-1916)
- [SaudiSat-1C](https://db.satnogs.org/satellite/IRES-5964-9687-1982-0089)





More to be added in future. 

Script can be modified fairly easily to add or remove satellites. Main satellite info file: `data/satinfo.txt` - See [Satellite Info Format](https://github.com/Exclavia/Satellite-Tracker/blob/main/data%2FREADME.md)


## External Usage
Since the script depends on a third-party API, correct or fully updated information cannot be guaranteed currently. This project is still fairly early in development, and plans to either create a maintained API or additions for the ability to self-host the API are being worked on.

To incorporate in your own code you can grab the full repo or just grab the `sat.py` script and `data/` directory and then import the `getSat()` function from the sat.py script. To call the function a few arguments need to be passed to it:
```
from sat import getSat
getSat( norad_id= # NORAD ID of satellite  **Required**
        latitude= # Latitude of observer   **Required**
        longitude= # Longitude of observer **Required**
        retry=False # Self use only, do not change
        external=False # Change this to True to return a list of the satellite data, otherwise it will operate like the CLI )
```
