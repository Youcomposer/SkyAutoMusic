@echo off
:: Wechsel zum Verzeichnis des Skripts
cd /d "%~dp0"

:: Logdatei erstellen
set LOGFILE=run_log.log
echo ========================== > %LOGFILE%
echo Skript gestartet: %date% %time% >> %LOGFILE%
echo ========================== >> %LOGFILE%

:: Überprüfen, ob Python installiert ist
where python >nul 2>nul
if errorlevel 1 (
    echo [%date% %time%] Fehler: Python ist nicht installiert oder nicht im PATH. >> %LOGFILE%
    echo Bitte installieren Sie Python und fügen Sie es zum PATH hinzu. >> %LOGFILE%
    pause
    exit /b
) else (
    echo [%date% %time%] Erfolg: Python ist installiert. >> %LOGFILE%
)

:: Überprüfen, ob das `pydirectinput`-Modul installiert ist
python -c "import pydirectinput" >nul 2>nul
if errorlevel 1 (
    echo [%date% %time%] Fehler: `pydirectinput` ist nicht installiert. >> %LOGFILE%
    echo Bitte installieren Sie `pydirectinput` mit dem folgenden Befehl: >> %LOGFILE%
    echo pip install pydirectinput >> %LOGFILE%
    pause
    exit /b
) else (
    echo [%date% %time%] Erfolg: `pydirectinput` ist installiert. >> %LOGFILE%
)

:: Überprüfen, ob der "Songs"-Ordner existiert
if not exist "Songs" (
    echo [%date% %time%] Fehler: Der "Songs"-Ordner wurde nicht gefunden. >> %LOGFILE%
    echo Bitte erstellen Sie den "Songs"-Ordner und fügen Sie Ihre Musikdateien hinzu. >> %LOGFILE%
    pause
    exit /b
) else (
    echo [%date% %time%] Erfolg: Der "Songs"-Ordner ist vorhanden. >> %LOGFILE%
)

:: Python-Skript ausführen und Details in Logdatei protokollieren
echo [%date% %time%] Starte Python-Skript... >> %LOGFILE%
echo ================================= >> %LOGFILE%
python SkyAutoMusic.py >> %LOGFILE% 2>&1

:: Beenden des Skripts und Protokollierung des Abschlusses
echo [%date% %time%] Skript abgeschlossen. >> %LOGFILE%
echo ========================== >> %LOGFILE%

:: CMD-Fenster automatisch schließen
exit
