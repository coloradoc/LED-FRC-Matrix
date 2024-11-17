@echo off
rem Script to automate copying all of the files in LEDcontrol to the raspberry pi.
rem PuTTY needs to be installed for this to work: https://www.putty.org/

rem First remove everything in the raspberry pi's LEDcontrol folder (pscp will not do this)
ssh pi@raspberrypi "sudo rm -rf /home/pi/LED-FRC-Matrix/LEDcontrol"

rem Use pscp to copy the LEDcontrol folder from Windows to Raspberry Pi
pscp -r LEDcontrol pi@raspberrypi:/home/pi/LED-FRC-Matrix/

echo File transfer complete.