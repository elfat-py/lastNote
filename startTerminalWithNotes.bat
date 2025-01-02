@echo off
REM Marker file to track if the application has already run
set markerFile=C:\Users\alex\lastNote_marker.txt

REM Check if the marker file exists
if exist "%markerFile%" (
    echo Application already run for this session.
    exit
)

REM Create the marker file
echo "LastNote executed on %date% %time%" > "%markerFile%"

REM Run the application
cd /d "C:\Users\alex\PycharmProjects\lastNote"
start "" "dist\lastNote.exe" auto
exit
