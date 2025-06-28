# Satellite tracker
![pylint](https://img.shields.io/badge/PyLint-10.00-brightgreen?logo=python&logoColor=white)

Simple satellite tracker with a GUI that shows the next pass for a selected satellite over a given longitude and latitude based on minimum elevation.

<img src="https://raw.githubusercontent.com/Exclavia/Satellite-Tracker/refs/heads/main/images/screenshot.png"/>

This program will download and store the Keplarian elements from Celestrak automatically and regularly based on how long since last download. (There is a command option to force a redownload)



## Satellites
Can be changed and added based on the keps satellite group selected. While the satinfo.txt that assists in populating the GUIs satellite selection dropdown menu is still being used, it does check itself against the downloaded keps and displays only the matches. I would like to state that I made this program with AMSAT tracking in mind mainly (As an amateur radio operator) so while options can be changed to download other keps, remember if you want to be able to actually select the satellite + any additional information, to update the satinfo.txt (Unforunately this is still done manually as there are only 27 entries. In the future I would like to implement something that can lookup the satellite description + additional information automatically, but for now I am only focusing on relatively functional things.)
