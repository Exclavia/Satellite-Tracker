# Satellite tracker
![pylint](https://img.shields.io/badge/PyLint-10.00-brightgreen?logo=python&logoColor=white)

Simple satellite tracker with a GUI that shows the next pass for a selected satellite over a given longitude and latitude based on minimum elevation.

<img src="https://raw.githubusercontent.com/Exclavia/Satellite-Tracker/refs/heads/main/images/screenshot.png"/>

This program will download and store the Keplarian elements from Celestrak automatically and regularly based on how long since last download. (There is a command option to force a redownload)


## How to use
Program can be ran by running the `main.py` script. Once opened, you have to input your latitude, longitude and select a satellite, by default minimum elevation input is set to 20.0 degrees, but can be changed to be higher or lower.
Be careful though I haven't added any sort of checks to make sure you don't input a value to high or low (For lat/lon -200 wouldn't make sense. vice versa)

The script also has a few arguments that can be passed to it: `--force-dl` which will force a download of the keps, even if they're already downloaded + up to date, as well as a `--light` argument to switch the theme from the default darkmode to lightmode. 


## Satellites
Can be changed and added based on the keps satellite group selected. While the satinfo.txt that assists in populating the GUIs satellite selection dropdown menu is still being used, it does check itself against the downloaded keps and displays only the matches. I would like to state that I made this program with AMSAT tracking in mind mainly (As an amateur radio operator) so while options can be changed to download other keps, remember if you want to be able to actually select the satellite + any additional information, to update the satinfo.txt (Unforunately this is still done manually as there are only 27 entries. In the future I would like to implement something that can lookup the satellite description + additional information automatically, but for now I am only focusing on relatively functional things.)


## External Usage
Originally it was more setup as either CLI or GUI, but I pivoted the program more to the GUI, you can still call the get_sats() function, but rather than any built-in console printlines, all the information is just returned in list/dicts.
See the `gui.py` file to see how to implement it yourself, it's fairly straight forward at the moment.
