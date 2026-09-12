@echo off
cd /d "%~dp0"

echo Updating pip...
python -m pip install --upgrade pip

echo Checking if pydirectinput is installed...
python -c "import pydirectinput" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pydirectinput not found. Installing...
    python -m pip install pydirectinput
) ELSE (
    echo pydirectinput is already installed.
)

echo Checking if tkinter is installed...
python -c "import tkinter" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo tkinter not found. Installing...
    python -m pip install tk
) ELSE (
    echo tkinter is already installed.
)

python -c "import pydirectinput, tkinter" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo One or more dependencies failed to install. Exiting...
    pause
    exit /b
)

echo All checks passed, running program...
timeout /t 5 /nobreak >nul
cls

echo "..._____._........................_........__..__..........._......";
echo "../.____|.|............/\........|.|......|..\/..|.........(_).....";
echo ".|.(___.|.|.___..._.../..\.._..._|.|_.___.|.\../.|_..._.___._..___.";
echo "..\___.\|.|/./.|.|.|././\.\|.|.|.|.__/._.\|.|\/|.|.|.|./.__|.|/.__|";
echo "..____).|...<|.|_|.|/.____.\.|_|.|.||.(_).|.|..|.|.|_|.\__.\.|.(__.";
echo ".|_____/|_|\_\\__,./_/....\_\__,_|\__\___/|_|..|_|\__,_|___/_|\___|";
echo "...............__/.|...............................................";
echo "..............|___/................................................";

python SkyAutoMusic.py

echo exiting...
timeout /t 3 /nobreak >nul
exit