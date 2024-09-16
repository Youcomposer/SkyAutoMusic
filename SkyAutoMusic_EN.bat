@echo off
:: Change to the script directory
cd /d "%~dp0"

:: Create log file
set LOGFILE=run_log.log
echo ========================== > %LOGFILE%
echo Script started: %date% %time% >> %LOGFILE%
echo ========================== >> %LOGFILE%

:: Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo [%date% %time%] Error: Python is not installed or not in PATH. >> %LOGFILE%
    echo Please install Python and add it to PATH. >> %LOGFILE%
    pause
    exit /b
) else (
    echo [%date% %time%] Success: Python is installed. >> %LOGFILE%
)

:: Check if the `pydirectinput` module is installed
python -c "import pydirectinput" >nul 2>nul
if errorlevel 1 (
    echo [%date% %time%] Error: `pydirectinput` is not installed. >> %LOGFILE%
    echo Please install `pydirectinput` using the following command: >> %LOGFILE%
    echo pip install pydirectinput >> %LOGFILE%
    pause
    exit /b
) else (
    echo [%date% %time%] Success: `pydirectinput` is installed. >> %LOGFILE%
)

:: Check if the "Songs" folder exists
if not exist "Songs" (
    echo [%date% %time%] Error: The "Songs" folder was not found. >> %LOGFILE%
    echo Please create the "Songs" folder and add your music files. >> %LOGFILE%
    pause
    exit /b
) else (
    echo [%date% %time%] Success: The "Songs" folder is present. >> %LOGFILE%
)

:: Run the Python script and log details
echo [%date% %time%] Starting Python script... >> %LOGFILE%
echo ================================= >> %LOGFILE%
python SkyAutoMusic_EN.py >> %LOGFILE% 2>&1

:: End of script and log completion
echo [%date% %time%] Script completed. >> %LOGFILE%
echo ========================== >> %LOGFILE%

:: Automatically close CMD window
exit
